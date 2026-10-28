# Atlas volume lifetime map

| Storage surface | Lifetime | Intended Atlas use | Forbidden assumption |
|---|---|---|---|
| container writable layer | container incarnation | disposable process files | survives restart or reschedule |
| `emptyDir` | Pod on one Node | bounded scratch and local exchange | durable job or result state |
| generic ephemeral CSI volume | Pod | per-Pod provisioned scratch or data | independent retention |
| PVC/PV | independent of one Pod | transactional or stateful workload storage | backup or application consistency |
| local PV | backend/Node lifetime | workloads with explicit replication or recovery | transparent Node failover |
| network/cloud volume | backend resource lifetime | durable block/filesystem storage | regional DR or stale-writer prevention |
| snapshot content | snapshot retention policy | recovery point component | application-consistent backup by default |
| object backup repository | repository policy | independent recovery and immutable artifacts | usable without catalogue and keys |

## Atlas data classes

- Transactional run state uses a data service with one authoritative history and fencing.
- Immutable artifacts use content-addressed publication and checksum verification.
- Worker scratch is disposable and size-bounded.
- Recovery evidence is retained separately from the cluster.
- Configuration and secrets are projected inputs, not application data volumes.

Every class names an acknowledgement point, deletion authority, tolerated failure, and recovery oracle.
