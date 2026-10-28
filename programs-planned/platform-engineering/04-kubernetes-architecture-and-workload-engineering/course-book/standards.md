# Standards and version policy

Course 4 separates Kubernetes API stability, reference-tool versions, and environment evidence.

## Kubernetes baseline

The conceptual and manifest baseline is Kubernetes **1.36.2**. Stable API groups used by the release include:

```text
v1
apps/v1
batch/v1
policy/v1
rbac.authorization.k8s.io/v1
apiextensions.k8s.io/v1
```

The custom API is `platform.bijux.dev/v1alpha1`. The alpha label is honest: the API is educational and not yet a stable organizational contract. Structural schema, status subresource, defaults, bounds, and evolution obligations are still treated seriously.

Kubernetes 1.37 was not a released stable baseline when the course was finalized. Preview or scheduled behavior is not taught as current stable behavior.

## Local-cluster reference

The optional local lane pins:

```text
kind 0.32.0
kindest/node v1.36.1
sha256:3489c7674813ba5d8b1a9977baea8a6e553784dab7b84759d1014dbd78f7ebd5
```

The conceptual baseline and node image differ by one patch release. The evidence packet must record this rather than claiming exact parity.

## API authority

The Kubernetes API is authoritative. `kubectl`, controllers, CI systems, GitOps reconcilers, operators, and platform APIs are clients.

The course relies on these API concepts:

- optimistic concurrency through resource versions;
- desired-state changes represented by generation where supported;
- observed generation in status;
- owner references and garbage collection;
- finalizers and deletion timestamps;
- Server-Side Apply managed fields;
- structural CRD schemas and status subresources;
- stable conditions with typed reasons.

These are not command-line conventions.

## Image and supply-chain identity

Workload images remain bound to the exact Course 3 repository-plus-digest subjects. Tags may exist for discovery but are not deployment identity. The Course 4 release does not claim that the target cluster enforces signature or provenance policy; Course 8 owns admission enforcement.

## Deferred standards

- Kubernetes networking model, CNI, NetworkPolicy, DNS, and Gateway API — Course 5;
- CSI, StorageClass, snapshots, backup/restore — Course 6;
- Kustomize, Helm, Argo CD, Flux, progressive delivery — Course 7;
- Pod Security Standards, policy engines, multi-tenancy — Course 8;
- OpenTelemetry, autoscaling, upgrades, fleet operations — Course 9;
- Crossplane and internal developer-platform APIs — Course 10.

## Reference links

- Kubernetes components: <https://kubernetes.io/docs/concepts/overview/components/>
- API concepts: <https://kubernetes.io/docs/reference/using-api/api-concepts/>
- Workloads: <https://kubernetes.io/docs/concepts/workloads/>
- Controllers: <https://kubernetes.io/docs/concepts/architecture/controller/>
- Custom resources: <https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/>
- kind releases: <https://github.com/kubernetes-sigs/kind/releases>
