package atlas

import (
	"crypto/sha256"
	"encoding/hex"
	"errors"
	"regexp"
	"sort"
)

const Finalizer = "platform.bijux.dev/release-reservation"

var digestImage = regexp.MustCompile(`^[^[:space:]@]+@sha256:[0-9a-f]{64}$`)

func Validate(in AtlasWorkload) error {
	if in.APIVersion != "platform.bijux.dev/v1alpha1" || in.Kind != "AtlasWorkload" {
		return errors.New("unsupported type")
	}
	if in.Metadata.Name == "" || in.Metadata.Namespace == "" {
		return errors.New("name and namespace are required")
	}
	if !digestImage.MatchString(in.Spec.APIImage) || !digestImage.MatchString(in.Spec.WorkerImage) {
		return errors.New("images must use immutable sha256 identities")
	}
	if in.Spec.APIReplicas < 1 || in.Spec.APIReplicas > 20 {
		return errors.New("apiReplicas must be between 1 and 20")
	}
	if in.Spec.WorkerReplicas != 1 {
		return errors.New("workerReplicas must remain 1 until storage concurrency is proven")
	}
	if in.Spec.ConfigurationRef == "" {
		return errors.New("configurationRef is required")
	}
	return nil
}

func StableUID(namespace, name string) string {
	sum := sha256.Sum256([]byte(namespace + "/" + name))
	return hex.EncodeToString(sum[:16])
}

func condition(previous []Condition, desired Condition) Condition {
	for _, item := range previous {
		if item.Type == desired.Type && item.Status == desired.Status {
			desired.LastTransitionTime = item.LastTransitionTime
			return desired
		}
	}
	desired.LastTransitionTime = now()
	return desired
}

func deployment(in AtlasWorkload, component, image string, replicas int32, port int32) Deployment {
	labels := map[string]string{
		"app.kubernetes.io/name":       "atlas-" + component,
		"app.kubernetes.io/part-of":    "atlas",
		"app.kubernetes.io/managed-by": "atlas-controller",
	}
	claims := []string{}
	if component == "worker" {
		claims = []string{"atlas-worker-spool", "atlas-worker-results"}
	}
	return Deployment{
		Name:              "atlas-" + component,
		Namespace:         in.Metadata.Namespace,
		OwnerUID:          in.Metadata.UID,
		Replicas:          replicas,
		Labels:            labels,
		ServiceAccount:    "atlas-" + component,
		AutomountToken:    false,
		TerminationGrace:  30,
		DurableClaimNames: claims,
		Container: Container{
			Name:                     "atlas-" + component,
			Image:                    image,
			Port:                     port,
			RunAsUser:                65532,
			ReadOnlyRootFilesystem:   true,
			AllowPrivilegeEscalation: false,
			DropCapabilities:         []string{"ALL"},
			Requests:                 map[string]string{"cpu": "100m", "memory": "64Mi"},
			Limits:                   map[string]string{"cpu": "500m", "memory": "128Mi"},
		},
	}
}

func Reconcile(in AtlasWorkload, childrenReady bool) (ReconcileOutput, error) {
	if in.Metadata.UID == "" {
		in.Metadata.UID = StableUID(in.Metadata.Namespace, in.Metadata.Name)
	}
	if err := Validate(in); err != nil {
		return ReconcileOutput{}, err
	}
	if in.Metadata.DeletionTimestamp != nil {
		ready := condition(in.Status.Conditions, Condition{
			Type: "Ready", Status: "False", Reason: "Deleting",
			Message:            "release reservation cleanup must complete before finalizer removal",
			ObservedGeneration: in.Metadata.Generation,
		})
		return ReconcileOutput{
			FinalizerRequired: true,
			DeleteChildren:    true,
			Status: AtlasWorkloadStatus{
				ObservedGeneration: in.Metadata.Generation,
				ChildDeployments:   []string{},
				Conditions:         []Condition{ready},
			},
		}, nil
	}
	children := []Deployment{
		deployment(in, "api", in.Spec.APIImage, in.Spec.APIReplicas, 8080),
		deployment(in, "worker", in.Spec.WorkerImage, in.Spec.WorkerReplicas, 0),
	}
	sort.Slice(children, func(i, j int) bool { return children[i].Name < children[j].Name })
	names := []string{children[0].Name, children[1].Name}
	status := "False"
	reason := "ChildrenProgressing"
	message := "waiting for child readiness"
	if childrenReady {
		status, reason, message = "True", "ChildrenAvailable", "all child deployments are available"
	}
	ready := condition(in.Status.Conditions, Condition{
		Type: "Ready", Status: status, Reason: reason, Message: message,
		ObservedGeneration: in.Metadata.Generation,
	})
	return ReconcileOutput{
		FinalizerRequired: true,
		Children:          children,
		Status: AtlasWorkloadStatus{
			ObservedGeneration: in.Metadata.Generation,
			ChildDeployments:   names,
			Conditions:         []Condition{ready},
		},
	}, nil
}
