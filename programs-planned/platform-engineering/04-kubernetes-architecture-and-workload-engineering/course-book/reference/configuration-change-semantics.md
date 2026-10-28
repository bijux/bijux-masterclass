# Configuration change semantics

Kubernetes can project configuration; it cannot decide how an application consumes or validates it.

## Environment snapshot

Environment values are fixed at container creation. Updating a referenced ConfigMap or Secret does not rewrite a running process environment. Trigger Pod replacement intentionally when these values change.

## Projected files

Projected volumes can update eventually. Updates are not synchronous with the API write, and applications must reread or watch files. Atomic writer behavior can replace symlinks/directories; applications should not assume an in-place file mutation.

## Immutable configuration

Immutable ConfigMaps/Secrets reduce accidental mutation and API/kubelet watch load. A new named object plus Pod-template change creates a clearer release history. The trade-off is explicit garbage collection and naming/version policy.

## Hash-triggered rollouts

A template annotation containing a deterministic hash can bind a Pod revision to effective configuration. The hash must cover exact key/value content and references, use stable serialization, and exclude secret values from logs or annotations.

## Rotation

Secret rotation is a protocol: introduce new authority, make consumers accept/use it, verify, then retire old authority. Restarting Pods is only one step and can cause outage if overlap is absent.
