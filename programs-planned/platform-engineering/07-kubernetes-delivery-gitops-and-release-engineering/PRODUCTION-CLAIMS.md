# Production claims and evidence boundary

Atlas Delivery Plane 1.0 is a release-oriented educational reference. It demonstrates delivery invariants, deterministic local Git history, semantic reconciliation, manifest validation, progressive-release decisions, protected-resource behavior, and exact handoffs.

A dependency-light proof does **not** establish operated production behavior for Argo CD, Flux, Helm, Kustomize, SOPS, External Secrets, Argo Rollouts, Kubernetes admission, a managed cluster fleet, or a hosted Git/OCI provider. Those claims require native tools, real controllers, real credentials, live clusters, and observed failure exercises.

Every environment-backed lane is labelled `not-executed` when its tool or infrastructure is absent. No static manifest is presented as proof that a controller reconciled it correctly.
