# Kubernetes storage feature and evidence matrix

API availability, driver capability, installed controllers, backend behavior, and application correctness are separate gates.

| Feature | API or declaration | Additional dependency | Stronger evidence |
|---|---|---|---|
| dynamic provisioning | PVC + StorageClass | external provisioner and driver | real backend allocation and idempotent retry |
| topology-aware binding | `WaitForFirstConsumer` | scheduler, provisioner topology | feasible placement and replacement path |
| expansion | PVC size increase | controller/node expansion capabilities | backend, device, filesystem, and app sizes agree |
| snapshot | snapshot CRDs | snapshotter and CSI capability | isolated restore and application validation |
| group snapshot | group snapshot APIs | installed CRDs/controller/driver support | complete member set and recovery validation |
| clone/populator | PVC data source | driver or populator controller | lineage, checksum, destination policy |
| mutable attributes | VolumeAttributesClass | driver modify-volume support | observed backend class and workload impact |
| health reporting | CSI/node health integration | driver implementation | correlated device, Node, and application evidence |

## Evidence classes

1. **Static** — schema, manifest, policy, and contract inspection.
2. **Semantic** — dependency-light model tests and fault cases.
3. **Native cluster** — real API server, scheduler, sidecars, kubelet, and CSI driver.
4. **Backend** — actual storage-system operations and audit state.
5. **Service recovery** — application-level restore and critical journey.
6. **Operated** — repeated evidence at representative scale under team runbooks.

A release states the highest executed class for each feature. Missing higher-level evidence remains visible as `not-executed`.
