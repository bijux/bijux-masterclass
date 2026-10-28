# Volume snapshot object map

| Object | Scope | Responsibility |
|---|---|---|
| `VolumeSnapshot` | namespaced | user request and observed readiness |
| `VolumeSnapshotContent` | cluster | binding to one backend snapshot handle |
| `VolumeSnapshotClass` | cluster | driver and deletion policy |
| external snapshotter/controller | controller | reconciliation between API objects and CSI calls |
| CSI driver/backend | external | actual snapshot creation, deletion, and restoration source |

## Important distinctions

- `readyToUse` means the snapshot system considers the content ready for use; it does not prove application consistency.
- `Delete` versus `Retain` controls backend snapshot lifecycle when API objects are removed.
- A restored PVC is a new writable data surface and needs lineage, access policy, and validation.
- Snapshot APIs are extension APIs installed separately from the core Kubernetes API.
- Driver support, sidecar versions, CRDs, and backend capabilities must all align.

## Recovery proof

Record source PVC UID, PV/backend handle, consistency class, application generation, snapshot content identity, class, key context, and capture time. Restore to a new claim, start the application in isolation, and validate domain invariants before declaring success.
