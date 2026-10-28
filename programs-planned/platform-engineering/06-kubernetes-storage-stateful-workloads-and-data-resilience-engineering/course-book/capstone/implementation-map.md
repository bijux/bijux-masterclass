# Implementation and proof map

| Responsibility | Dependency-light implementation | Native/stronger lane | Primary oracle |
|---|---|---|---|
| data catalogue | `atlas_data.catalog` | service catalogue and owners | every data class has authority and recovery |
| binding | `atlas_data.binding` | binder, provisioner, scheduler | one compatible claim-to-volume identity |
| topology | `atlas_data.topology` | scheduler + CSI capacity | feasible initial and replacement placement |
| CSI lifecycle | `atlas_data.csi` | sidecars, node plugin, backend | idempotent ordered effects |
| stable identity | `atlas_data.stateful` | StatefulSet/controller | ordinal and volume lineage preserved |
| fencing | `atlas_data.fencing`, `ledger` | database or storage authority | stale generation rejected |
| snapshot | `atlas_data.snapshots` | snapshot APIs and backend | labelled recovery point and restored set |
| backup/restore | `atlas_data.backup` | independent repository | empty-destination validated restore |
| durability | Go atomic-file probe | filesystem/backend crash testing | acknowledged publication survives scope |
| performance | `atlas_data.performance` | representative workload | correctness plus latency/capacity budget |
| migration | `atlas_data.migration` | live source/target | one authority through cutover |
| release | `atlas_data.release` | cluster/backend dossier | all non-compensable gates pass |

The map prevents a local implementation from being mistaken for the native system it models. Learners should move from semantic proof to stronger lanes deliberately.
