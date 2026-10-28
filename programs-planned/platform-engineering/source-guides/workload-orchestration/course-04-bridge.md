# Course 4 bridge — from OCI release to reconciled workload

| Course 3 guarantee | Course 4 expression |
|---|---|
| immutable image identity | repository plus digest in every Pod template |
| UID/GID 65532 | Pod/container security context |
| no privilege escalation | dropped capabilities and `allowPrivilegeEscalation: false` |
| read-only root | declared writable mounts only |
| separate liveness/readiness | distinct probes with distinct consequences |
| thirty-second shutdown | termination grace plus application cooperation |
| resource hypotheses | requests and limits labelled as hypotheses |
| runtime-only secrets | projected data, never image layers |
| durable paths | PVC interface; storage implementation deferred to Course 6 |
| accepted artifact evidence | digest-only workload identity; admission enforcement deferred to Course 8 |
