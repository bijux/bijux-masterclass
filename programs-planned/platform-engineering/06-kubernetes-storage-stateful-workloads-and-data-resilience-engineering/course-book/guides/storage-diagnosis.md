# Storage diagnosis by earliest missing transition

Start by naming the workload, claim, volume, Node, storage class, CSI driver, and backend handle. Do not start by restarting the driver.

## 1. Is the claim admitted?

Inspect the PVC specification and events. Verify the class exists, the request is valid, quotas permit it, the data source exists, and no selector makes dynamic provisioning impossible. A Pending PVC with no provisioner event is different from one whose backend request failed.

## 2. Has binding or provisioning happened?

For Immediate binding, inspect the PV and its topology. For WaitForFirstConsumer, inspect Pod scheduling constraints, selected-node state, CSIStorageCapacity, and provisioner events. Preserve evidence before deleting anything.

## 3. Can the Pod be scheduled with the volume?

Check PV node affinity, Node labels, access mode, attach limits, existing attachments, taints, affinity, resources, and all other claims. Store per-Node rejection reasons.

## 4. Did controller attachment complete?

Inspect VolumeAttachment, external-attacher logs, driver controller logs, backend attachment state, credentials, and quotas. A timeout may hide backend success, so retries must be idempotent.

## 5. Did node staging and publication complete?

Inspect kubelet events, node-plugin logs, device discovery, filesystem checks, mount options, encryption state, global staging path, and Pod target path. `FailedMount` is not one failure class.

## 6. Is the application allowed to become ready?

Verify log replay, fencing, schema, filesystem writability, checksum state, database role, and dependency readiness. A mounted filesystem and open port are insufficient.

## Unsafe shortcuts

Do not remove finalizers, delete VolumeAttachments, force detach, recreate PVCs, or edit PV affinity until the data owner and backend state are understood. Every such action can change the system from unavailable to corrupt.
