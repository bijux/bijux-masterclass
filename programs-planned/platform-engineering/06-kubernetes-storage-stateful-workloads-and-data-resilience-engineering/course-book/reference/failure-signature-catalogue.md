# Storage failure signature catalogue

Use this catalogue to map an observation to the earliest likely missing transition. It is a starting hypothesis, not a replacement for evidence.

| Observation | Likely boundary | First evidence |
|---|---|---|
| PVC remains Pending with no provisioner event | class selection, admission, or delayed binding | PVC spec, default class, selected-node state |
| provisioning retries | controller plugin or backend | provisioner logs, request identity, backend allocation |
| Pod unschedulable after binding | topology, attach limit, compute constraint | per-Node scheduler reasons, PV node affinity |
| `Multi-Attach` | old attachment or incompatible access model | `VolumeAttachment`, backend attachment, fencing generation |
| `FailedMount` | stage/publish, filesystem, permissions | kubelet and node-plugin logs, device and mount state |
| filesystem resize pending | node expansion or filesystem step | PVC/PV capacity, device and filesystem sizes |
| snapshot Ready but restore fails | consistency, content, key, or schema | content handle, restore logs, application validation |
| backup succeeded but RPO missed | schedule, log gap, catalogue, or replication | latest restorable generation and timestamps |
| latency rises during snapshot | copy-on-write or backend contention | workload latency, queue depth, backend metrics |
| Pod Ready but data stale | application readiness or replication lag | role, generation, log position, consistency level |

## Unsafe responses

Do not begin by deleting PVCs, VolumeAttachments, snapshot contents, or finalizers. Those actions mutate the evidence and can turn unavailability into corruption. First identify authority, writer state, backend identity, and the recovery point you are protecting.
