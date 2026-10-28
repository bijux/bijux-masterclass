# Go AtlasWorkload controller

This directory contains two layers:

1. `internal/atlas` — deterministic reconciliation and status logic tested without a cluster;
2. `internal/kubeclient` plus `cmd/atlas-controller serve` — a standard-library in-cluster adapter using the Kubernetes HTTPS API, Server-Side Apply, finalizers, and the status subresource.

The adapter uses bounded polling rather than an informer cache so the course can expose each API interaction without importing a large framework. It is deployable reference code, but it is not claimed as a production controller manager: it lacks leader election, watch/informer efficiency, rate-limited work queues, metrics, admission webhooks, and operated SLO evidence. Those limitations are explicit teaching boundaries.

`render` reads one AtlasWorkload JSON document from standard input and writes desired children/status. `serve` uses in-cluster identity and reconciles namespaced AtlasWorkloads.
