package probe

import (
	"context"
	"crypto/tls"
	"fmt"
	"net"
	"net/http"
	"time"
)

type Result struct {
	Target     string        `json:"target"`
	Addresses  []string      `json:"addresses,omitempty"`
	Remote     string        `json:"remote,omitempty"`
	StatusCode int           `json:"statusCode,omitempty"`
	TLSVersion string        `json:"tlsVersion,omitempty"`
	ServerName string        `json:"serverName,omitempty"`
	Duration   time.Duration `json:"duration"`
}

func Resolve(ctx context.Context, resolver *net.Resolver, name string) (Result, error) {
	started := time.Now()
	values, err := resolver.LookupHost(ctx, name)
	if err != nil {
		return Result{}, err
	}
	return Result{Target: name, Addresses: values, Duration: time.Since(started)}, nil
}

func HTTP(ctx context.Context, client *http.Client, url string) (Result, error) {
	started := time.Now()
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
	if err != nil {
		return Result{}, err
	}
	response, err := client.Do(req)
	if err != nil {
		return Result{}, err
	}
	defer response.Body.Close()
	result := Result{Target: url, StatusCode: response.StatusCode, Duration: time.Since(started)}
	if response.TLS != nil {
		result.TLSVersion = tls.VersionName(response.TLS.Version)
		result.ServerName = response.TLS.ServerName
	}
	return result, nil
}

func TCP(ctx context.Context, network, address string, timeout time.Duration) (Result, error) {
	started := time.Now()
	dialer := &net.Dialer{Timeout: timeout}
	conn, err := dialer.DialContext(ctx, network, address)
	if err != nil {
		return Result{}, err
	}
	defer conn.Close()
	remote := conn.RemoteAddr().String()
	if remote == "" {
		return Result{}, fmt.Errorf("missing remote address")
	}
	return Result{Target: address, Remote: remote, Duration: time.Since(started)}, nil
}
