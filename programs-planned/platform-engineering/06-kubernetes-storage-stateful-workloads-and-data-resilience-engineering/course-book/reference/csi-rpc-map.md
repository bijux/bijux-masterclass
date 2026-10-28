# CSI RPC and ownership map

CSI separates storage orchestration from storage implementation. Kubernetes sidecars translate API objects into CSI calls; controller and node plugins translate CSI calls into backend and host effects.

| CSI service | Representative operations | Main evidence |
|---|---|---|
| Identity | plugin identity, readiness, capabilities | plugin registration and capability response |
| Controller | create/delete, attach/detach, expand, snapshot | sidecar logs, backend handles, `VolumeAttachment` |
| Node | stage/unstage, publish/unpublish, expand, stats | kubelet events, node-plugin logs, device and mount state |

## Lifecycle

```text
CreateVolume
→ ControllerPublishVolume
→ NodeStageVolume
→ NodePublishVolume
→ workload access
→ NodeUnpublishVolume
→ NodeUnstageVolume
→ ControllerUnpublishVolume
→ DeleteVolume
```

Some drivers omit controller attach or global staging; capability discovery determines the legal path. Every mutating request must tolerate retry after an ambiguous timeout. The same stable identity and compatible parameters must yield the same effect; changed parameters must be rejected rather than producing a second resource.

## Incident use

Classify the earliest failed phase before acting. A provisioning failure belongs to a different path from a node mount failure. Preserve API objects, operation IDs, sidecar logs, node-plugin logs, and backend state before force detach or object deletion.
