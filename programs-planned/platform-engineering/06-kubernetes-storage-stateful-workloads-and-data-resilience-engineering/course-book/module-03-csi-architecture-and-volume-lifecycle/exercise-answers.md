# Worked answers — CSI Architecture and Volume Lifecycle

These are complete reference solutions. A different design is valid only when it preserves the same authority, failure, recovery, and evidence boundaries.

## 1. Map the CSI owners

Provisioning, deletion, controller expansion, snapshot creation, and—when required—controller publish/unpublish are controller-side operations because they manage backend or cluster-wide state. Node stage/unstage prepares a volume once per Node, while node publish/unpublish exposes it to a particular workload target. Some drivers omit optional stages or attachment services, so the capability response is authoritative. The Kubernetes sidecars translate API objects into these RPCs; kubelet drives node operations. Diagnosis must identify which phase is missing rather than saying “CSI failed.” A successful controller operation cannot prove node mount success, and a mounted volume cannot prove snapshot consistency or application readiness.

## 2. Define `CreateVolume` idempotency

The request name must be stable across retries and mapped durably to one backend volume. The driver should return the same volume ID when the existing effect satisfies the requested capacity range, capabilities, topology, parameters, and content source. If it conflicts, the driver must return a deterministic incompatibility rather than creating another object or silently changing the first. Backend creation and the name-to-handle record must survive driver restart. Tests should inject a timeout after backend success, repeat the RPC, and prove one handle exists. Idempotency means “same request, same effect”; it does not mean every repeated call succeeds regardless of changed parameters.

## 3. Trace the usable-volume lifecycle

The scheduler and binder select topology; the external provisioner calls `CreateVolume`; the PV records the returned handle; the attachment controller may create a VolumeAttachment and call `ControllerPublishVolume`; the node plugin receives `NodeStageVolume` to prepare the device or filesystem at a global path; kubelet calls `NodePublishVolume` for the Pod target; the runtime mounts the target into the container; the application performs its own recovery and readiness checks. Evidence spans PVC/PV events, selected topology, CSI request IDs, VolumeAttachment status, node-plugin logs, mount tables, filesystem identity, and application generation. Skipping the application step is a common source of false readiness.

## 4. Reverse the lifecycle safely

The Pod-specific target must stop using the volume before node-global preparation is removed. The volume must be unstaged before controller detach so the Node cannot issue I/O through a disappearing device. Backend deletion must occur only after no attachment, stage, or publication remains and after reclaim/retention authority permits it. Reordering can produce busy mounts, corrupted writes, stale devices, or data destruction while a process still runs. Timeouts complicate the path: a controller should reconcile observed state and repeat idempotent cleanup rather than assume absence. Force detach or finalizer removal is a break-glass recovery action that requires fencing evidence and data-owner approval.

## 5. Handle a Node crash without split brain

First prove the old writer cannot continue: Node status alone is insufficient because the machine, process, or storage path may still be alive. Use provider fencing, instance power-off evidence, storage attachment generation, database lease, or another mechanism that the old path cannot bypass. Inspect VolumeAttachment and backend attachment state, then detach or revoke through the supported controller path. Only after the old generation is fenced should a replacement attach, stage, recover, and become ready. Force detach trades availability for corruption risk and must be explicit. The post-recovery oracle is not merely a successful mount; it is one current writer generation, valid database recovery, and rejection of any stale writer attempt.

## 6. Interpret driver capabilities

Kubernetes exposes generic objects such as snapshots, expansion, RWOP, and VolumeAttributesClass, but a driver may not implement the relevant controller or node capability, may support it only for certain backends, or may impose topology and filesystem limits. The CSI identity, controller, and node capability responses define supported operations. Sidecar versions add another compatibility boundary. A platform service profile should bind Kubernetes API version, driver version, sidecar versions, backend class, and tested capabilities. Admission should reject unsupported requests. A field being accepted by the API server proves syntax and schema, not that a driver can perform the requested transition.

## 7. Separate controller and node expansion

Controller expansion changes backend capacity and updates the control-plane view. Node expansion—or application/filesystem work—must then make the additional space usable on the Node. The PVC may show a condition such as filesystem resize pending while the block device is already larger. Some filesystems expand online; others require remount or offline work. Repeating the request must be idempotent and shrinking must be rejected. The evidence chain includes PVC desired and status capacity, CSI controller response, backend size, node RPC, device size, filesystem size, and application observation. Reporting success after only the backend phase creates a dangerous mismatch between capacity accounting and usable space.

## 8. Analyze inline ephemeral CSI volumes

An inline ephemeral CSI volume is tied to Pod lifetime and described in the Pod spec. It can be useful for secrets, temporary data, or a driver-provided scratch capability where independent claim lifecycle is unnecessary. It is unsuitable for authoritative Atlas state because deletion, identity, retention, and recovery are coupled to the Pod. There is no separately governed PVC/PV lifecycle to preserve across workload replacement. Even if the driver stores bytes remotely, the platform contract remains ephemeral unless it explicitly exports durable identity. Authoritative data needs independent ownership, stable logical identity, retention, backup, and restore evidence. The storage technology alone cannot upgrade an ephemeral API contract into a durable one.

## 9. Design CSI observability

Metrics should aggregate operation, driver, result code, storage class, topology class, and perhaps node pool—not raw volume handles, target paths, or Pod UIDs. Useful histograms cover RPC latency by phase; counters cover retries and failures; gauges cover pending operations, attachment slots, and capacity. Detailed request IDs, volume handles, node IDs, and target paths belong in structured logs or traces with access and retention controls. Correlation must link Kubernetes objects, CSI operations, and backend requests. High-cardinality labels can make the observability system fail during the incident it should diagnose. The design should also distinguish controller and node service populations so a healthy provisioner does not hide node-publish failures.

## 10. Protect CSI credentials

Controller components may need backend credentials capable of provisioning or snapshotting, while node plugins may need narrower attach, map, or mount authority. Workload Pods should not receive either. ServiceAccounts authorize Kubernetes API access but do not automatically become backend identity. Cloud workload identity or secret delivery should bind each component to least authority. Node plugins are highly privileged and often access host mounts or devices, so compromise is severe; admission, image verification, host-path minimization, and node isolation matter. Credentials must rotate without losing volume identity. Logs and events must not expose them. The platform should document which principal performs each CSI RPC and backend action, including recovery and break-glass paths.

## 11. Design a partial-provisioning repair

The stable request name and backend tags should let the controller discover the existing volume. On retry, `CreateVolume` returns the same handle, allowing the PV to be created without duplication. If Kubernetes demand has disappeared, an orphan reconciler waits through a safety window, verifies no claim/PV references the handle, checks retention policy and data classification, then either inventories or deletes it through the normal driver path. It must not delete solely because the PV object is absent: the backend may contain imported or recovering data. Evidence includes request identity, backend creation timestamp, claim UID, controller attempts, and final disposition. Repair is a controlled state transition, not generic garbage collection.

## 12. State the native proof still required

A native lab must install the exact driver and sidecar versions, verify capability discovery, create and bind claims in real topology, exercise attach/stage/publish and reverse cleanup, inject controller and node restarts, repeat timed-out operations, test RWOP or multi-attach behavior, expand a real filesystem, create and restore snapshots, and inspect backend objects. It should test Node loss and stale attachment using safe disposable data. Version, configuration, filesystem, kernel, backend class, and cloud region must be recorded. The semantic lane catches design mistakes and supplies oracles; it cannot prove RPC implementation, host mounts, kernel behavior, or backend durability.
