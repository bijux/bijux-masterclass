# Optional local-cluster lane

The dependency-light lane is mandatory. The kind lane is optional but valuable because it exercises an independent API server, scheduler, controller manager, kubelets, and container runtime.

## Pinned environment

The course pins kind 0.32.0 and the Kubernetes 1.36.1 node image. The conceptual baseline is Kubernetes 1.36.2. The one-patch difference is recorded explicitly; it is not silently treated as exact version parity.

## Safety

Use a disposable cluster named `atlas-course4`. Do not point course scripts at a shared or production kubeconfig. Set an isolated `KUBECONFIG` and verify context before every destructive command.

## Image limitation

The Course 3 image digests are contract identities, not publicly pullable images in this package. The production-intent manifests retain them and therefore cannot run locally without access to the corresponding registry. The `overlays/kind-observation` lane substitutes a small observation image and is evidence only for Kubernetes mechanics, not for the Course 3 workload binary.

## Storage limitation

The kind lane may use `emptyDir` for mechanics. That is intentionally non-durable across Pod deletion and does not satisfy the worker storage contract. Course 6 owns storage classes, CSI, snapshots, and data resilience.

## Required records

Preserve cluster version, kind version, node-image digest, host architecture, container runtime, applied manifest digest, object snapshots, events, and cleanup result.
