# Course 4 handoff map

Kubernetes Course 4 receives a workload contract, not permission to reinterpret build internals.

| Course 3 fact | Course 4 use | Forbidden weakening |
|---|---|---|
| image repository and immutable index digest | Pod/container image identity | replace digest with mutable tag |
| supported platform descriptors and evidence | node scheduling/compatibility | assume label proves native execution |
| UID/GID 65532, no capabilities, no-new-privileges | security context | run as root to fix volume permissions |
| read-only root and declared write paths | volume/tmpfs design | rely on writable image layer for state |
| API port 8080 and health semantics | Service/probe design | redefine readiness as process existence |
| 30-second shutdown contract | termination grace and lifecycle | send SIGKILL immediately |
| durable spool/results | persistent storage requirements | store durable state in `emptyDir` |
| resource hypotheses and evidence class | initial requests/limits experiments | call hypotheses proven capacity |
| SBOM/provenance/signer/policy records | admission and release verification | verify tag or signature alone |
| known risks/unexecuted evidence | Course 4 experiment plan | hide gaps behind Kubernetes abstractions |

The handoff deliberately avoids ready-made Kubernetes manifests. Course 4 must learn Kubernetes objects and reconciliation rather than copy generated YAML. It does, however, receive enough precise input to design workloads without silently changing application, security, storage, or release semantics.
