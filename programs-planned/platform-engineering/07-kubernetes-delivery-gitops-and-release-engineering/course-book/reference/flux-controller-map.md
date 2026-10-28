# Reference — Flux controller map

source-controller creates immutable source artifacts. kustomize-controller renders and applies Kustomizations. helm-controller manages HelmRelease lifecycle. notification-controller emits and receives events. image-reflector selects registry metadata; image-automation writes governed Git updates.

Diagnose the first non-Ready resource and verify observed generation, source revision, and digest at every edge.

## Extended reader notes

`source-controller` turns Git, OCI, bucket, and Helm sources into revisioned artifacts. `kustomize-controller` renders and applies Kustomizations with inventory and health. `helm-controller` operates Helm releases and remediation. `image-reflector-controller` discovers registry metadata and evaluates image policies. `image-automation-controller` writes proposed Git changes. `notification-controller` sends alerts and receives trigger events.

The dependency chain is visible in status references. Diagnose the first artifact or controller object that has not observed its current generation. A Ready GitRepository does not prove Kustomization success; a Ready ImagePolicy does not prove production approval; a Receiver event does not replace interval reconciliation.

Controller separation enables narrow identities, but only if RBAC and repository credentials follow the same boundaries. Atlas keeps image automation on a candidate branch and keeps protected data inventory in a non-pruning Kustomization.
