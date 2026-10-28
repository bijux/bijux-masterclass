package kubeclient

import (
	"bytes"
	"context"
	"crypto/tls"
	"crypto/x509"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"time"

	"platform.bijux.dev/atlas-controller/internal/atlas"
)

const (
	tokenPath = "/var/run/secrets/kubernetes.io/serviceaccount/token"
	caPath    = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
	nsPath    = "/var/run/secrets/kubernetes.io/serviceaccount/namespace"
)

type HTTPError struct {
	StatusCode int
	Method     string
	Path       string
	Body       string
}

func (e *HTTPError) Error() string {
	return fmt.Sprintf("kubernetes API %s %s: status=%d: %s", e.Method, e.Path, e.StatusCode, e.Body)
}

type Client struct {
	baseURL   string
	token     string
	namespace string
	http      *http.Client
}

type atlasList struct {
	Items []atlas.AtlasWorkload `json:"items"`
}

func NewInCluster() (*Client, error) {
	host := os.Getenv("KUBERNETES_SERVICE_HOST")
	port := os.Getenv("KUBERNETES_SERVICE_PORT_HTTPS")
	if host == "" || port == "" {
		return nil, errors.New("in-cluster service environment is missing")
	}
	token, err := os.ReadFile(tokenPath)
	if err != nil {
		return nil, err
	}
	ca, err := os.ReadFile(caPath)
	if err != nil {
		return nil, err
	}
	namespace, err := os.ReadFile(nsPath)
	if err != nil {
		return nil, err
	}
	roots := x509.NewCertPool()
	if !roots.AppendCertsFromPEM(ca) {
		return nil, errors.New("service-account CA is invalid")
	}
	transport := &http.Transport{TLSClientConfig: &tls.Config{RootCAs: roots, MinVersion: tls.VersionTLS12}}
	return &Client{
		baseURL:   "https://" + host + ":" + port,
		token:     strings.TrimSpace(string(token)),
		namespace: strings.TrimSpace(string(namespace)),
		http:      &http.Client{Transport: transport, Timeout: 15 * time.Second},
	}, nil
}

func (c *Client) request(ctx context.Context, method, path, contentType string, body []byte) ([]byte, error) {
	req, err := http.NewRequestWithContext(ctx, method, c.baseURL+path, bytes.NewReader(body))
	if err != nil {
		return nil, err
	}
	req.Header.Set("Authorization", "Bearer "+c.token)
	req.Header.Set("Accept", "application/json")
	if contentType != "" {
		req.Header.Set("Content-Type", contentType)
	}
	resp, err := c.http.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	raw, err := io.ReadAll(io.LimitReader(resp.Body, 4<<20))
	if err != nil {
		return nil, err
	}
	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		return nil, &HTTPError{StatusCode: resp.StatusCode, Method: method, Path: path, Body: strings.TrimSpace(string(raw))}
	}
	return raw, nil
}

func (c *Client) ListAtlasWorkloads(ctx context.Context) ([]atlas.AtlasWorkload, error) {
	path := "/apis/platform.bijux.dev/v1alpha1/namespaces/" + c.namespace + "/atlasworkloads"
	raw, err := c.request(ctx, http.MethodGet, path, "", nil)
	if err != nil {
		return nil, err
	}
	var list atlasList
	if err := json.Unmarshal(raw, &list); err != nil {
		return nil, err
	}
	return list.Items, nil
}

func deploymentObject(d atlas.Deployment) map[string]any {
	container := map[string]any{
		"name": d.Container.Name, "image": d.Container.Image,
		"resources": map[string]any{"requests": d.Container.Requests, "limits": d.Container.Limits},
		"securityContext": map[string]any{
			"runAsNonRoot": true, "runAsUser": d.Container.RunAsUser,
			"allowPrivilegeEscalation": d.Container.AllowPrivilegeEscalation,
			"readOnlyRootFilesystem":   d.Container.ReadOnlyRootFilesystem,
			"capabilities":             map[string]any{"drop": d.Container.DropCapabilities},
		},
		"volumeMounts": []map[string]any{{"name": "tmp", "mountPath": "/tmp"}},
	}
	if d.Container.Port > 0 {
		container["ports"] = []map[string]any{{"name": "http", "containerPort": d.Container.Port}}
	}
	volumes := []map[string]any{{"name": "tmp", "emptyDir": map[string]any{"sizeLimit": "64Mi"}}}
	for _, claim := range d.DurableClaimNames {
		name := strings.TrimPrefix(claim, "atlas-worker-")
		container["volumeMounts"] = append(container["volumeMounts"].([]map[string]any), map[string]any{"name": name, "mountPath": "/var/lib/atlas/" + name})
		volumes = append(volumes, map[string]any{"name": name, "persistentVolumeClaim": map[string]any{"claimName": claim}})
	}
	return map[string]any{
		"apiVersion": "apps/v1", "kind": "Deployment",
		"metadata": map[string]any{
			"name": d.Name, "namespace": d.Namespace, "labels": d.Labels,
			"ownerReferences": []map[string]any{{"apiVersion": "platform.bijux.dev/v1alpha1", "kind": "AtlasWorkload", "name": "atlas", "uid": d.OwnerUID, "controller": true, "blockOwnerDeletion": true}},
		},
		"spec": map[string]any{
			"replicas": d.Replicas, "selector": map[string]any{"matchLabels": d.Labels},
			"template": map[string]any{"metadata": map[string]any{"labels": d.Labels}, "spec": map[string]any{
				"serviceAccountName": d.ServiceAccount, "automountServiceAccountToken": d.AutomountToken,
				"terminationGracePeriodSeconds": d.TerminationGrace,
				"securityContext":               map[string]any{"runAsNonRoot": true, "seccompProfile": map[string]any{"type": "RuntimeDefault"}},
				"containers":                    []any{container}, "volumes": volumes,
			}},
		},
	}
}

func (c *Client) DeploymentAvailable(ctx context.Context, namespace, name string, desired int32) (bool, error) {
	path := "/apis/apps/v1/namespaces/" + namespace + "/deployments/" + name
	raw, err := c.request(ctx, http.MethodGet, path, "", nil)
	if err != nil {
		var apiErr *HTTPError
		if errors.As(err, &apiErr) && apiErr.StatusCode == http.StatusNotFound {
			return false, nil
		}
		return false, err
	}
	var object struct {
		Status struct {
			AvailableReplicas  int32 `json:"availableReplicas"`
			ObservedGeneration int64 `json:"observedGeneration"`
		} `json:"status"`
		Metadata struct {
			Generation int64 `json:"generation"`
		} `json:"metadata"`
	}
	if err := json.Unmarshal(raw, &object); err != nil {
		return false, err
	}
	return object.Status.ObservedGeneration >= object.Metadata.Generation && object.Status.AvailableReplicas >= desired, nil
}

func (c *Client) ChildrenReady(ctx context.Context, workload atlas.AtlasWorkload) (bool, error) {
	apiReady, err := c.DeploymentAvailable(ctx, workload.Metadata.Namespace, "atlas-api", workload.Spec.APIReplicas)
	if err != nil {
		return false, err
	}
	workerReady, err := c.DeploymentAvailable(ctx, workload.Metadata.Namespace, "atlas-worker", workload.Spec.WorkerReplicas)
	if err != nil {
		return false, err
	}
	return apiReady && workerReady, nil
}

func (c *Client) ApplyDeployment(ctx context.Context, d atlas.Deployment) error {
	body, err := json.Marshal(deploymentObject(d))
	if err != nil {
		return err
	}
	path := "/apis/apps/v1/namespaces/" + d.Namespace + "/deployments/" + d.Name + "?fieldManager=atlas-controller&force=false"
	_, err = c.request(ctx, http.MethodPatch, path, "application/apply-patch+yaml", body)
	return err
}

func (c *Client) PatchFinalizers(ctx context.Context, workload atlas.AtlasWorkload, finalizers []string) error {
	body, _ := json.Marshal(map[string]any{"metadata": map[string]any{"finalizers": finalizers}})
	path := "/apis/platform.bijux.dev/v1alpha1/namespaces/" + workload.Metadata.Namespace + "/atlasworkloads/" + workload.Metadata.Name
	_, err := c.request(ctx, http.MethodPatch, path, "application/merge-patch+json", body)
	return err
}

func (c *Client) PatchStatus(ctx context.Context, workload atlas.AtlasWorkload, status atlas.AtlasWorkloadStatus) error {
	body, _ := json.Marshal(map[string]any{"status": status})
	path := "/apis/platform.bijux.dev/v1alpha1/namespaces/" + workload.Metadata.Namespace + "/atlasworkloads/" + workload.Metadata.Name + "/status"
	_, err := c.request(ctx, http.MethodPatch, path, "application/merge-patch+json", body)
	return err
}

func HasFinalizer(values []string, target string) bool {
	for _, value := range values {
		if value == target {
			return true
		}
	}
	return false
}

func AddFinalizer(values []string, target string) []string {
	if HasFinalizer(values, target) {
		return append([]string(nil), values...)
	}
	out := append([]string(nil), values...)
	return append(out, target)
}

func RemoveFinalizer(values []string, target string) []string {
	out := make([]string, 0, len(values))
	for _, value := range values {
		if value != target {
			out = append(out, value)
		}
	}
	return out
}

func FixturePath(parts ...string) string { return filepath.Join(parts...) }
