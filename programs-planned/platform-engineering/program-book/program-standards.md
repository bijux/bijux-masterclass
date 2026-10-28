# Program standards and version policy

The program separates standards from reference implementations and course profiles. POSIX, Linux, HTTP, TLS, OCI, Kubernetes APIs, CSI, Gateway API, OpenGitOps, and other specifications define interoperable semantics where applicable. OpenTofu, Helm, Kustomize, Argo CD, Flux, SOPS, External Secrets, and Argo Rollouts are reference implementations or tools, not the underlying concept.

Course 7 inherits Kubernetes 1.36.2 and the Course 6 data contract. Its pinned reference lane uses Kustomize 5.8.1, Helm 4.2.3, Argo CD 3.5.0, Flux 2.9.4, SOPS 3.13.3, External Secrets 2.9.0, and Argo Rollouts 1.9.1. Pins are evidence anchors for this release. A production program may select another supported patch version after compatibility and recovery proof.

Version axes remain separate: Kubernetes version, controller version, renderer version, chart version and digest, source revision, image digest, Atlas delivery profile, environment release, and data migration phase. A semantic version string does not replace immutable subjects.
