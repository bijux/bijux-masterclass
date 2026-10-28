# Reference — Tool, version, and evidence matrix

The reference lane pins Kubernetes 1.36.2, Helm 4.2.3, Kustomize 5.8.1, Argo CD 3.5.0, Flux 2.9.4, Argo Rollouts 1.9.1, SOPS 3.13.3, and External Secrets 2.9.0.

A version pin is not execution evidence. E0 validates course semantics and files; E1 executes native renderers or CLIs; E2 executes live disposable controllers; E3 exercises operated repositories, identities, clusters, and failure domains. Reports record exact versions and missing lanes.

## Extended reader notes

Tool pins establish the reference lane, not universal production requirements. For each tool record: version, digest or package source, purpose, configuration, evidence executed, evidence not executed, and compatibility assumptions.

Kustomize and Helm versions affect rendering. Argo CD and Flux versions affect source resolution, normalization, inventory, health, and APIs. SOPS and External Secrets affect key and secret behavior. Argo Rollouts affects progressive state transitions. Kubernetes version and installed CRDs determine admission and runtime semantics.

A local semantic test can prove the course invariant without proving native conformance. Native CLI output can prove rendering without proving controller behavior. A kind cluster can prove bounded integration without proving managed-cloud identity, load balancers, fleet scale, or production recovery. Keep these evidence classes visible.
