# Optional local Kubernetes storage lane

The local lane provides real API-server, scheduler, controller, kubelet, and CSI interaction. It does not prove cloud durability, zone resilience, or production performance.

## Environment requirements

Use a disposable kind cluster, an exact CSI driver version, snapshot CRDs/controller, and enough Nodes to exercise topology. Record Kubernetes, container runtime, CSI sidecars, CRDs, host OS, and storage backend.

## Safe experiments

- dynamic provisioning and `WaitForFirstConsumer`;
- attachment and node publication where supported;
- expansion;
- snapshot and restore;
- StatefulSet claim identity;
- NetworkPolicy around storage components;
- controller restart and compatible retry.

Avoid destructive force-detach or retained-resource tests unless every backend object is disposable.

## Evidence collection

Export PVCs, PVs, StorageClasses, CSIDriver/CSINode, CSIStorageCapacity, VolumeAttachments, snapshot objects, Pods, Events, component logs, and backend state before cleanup. Label the result `native local cluster`, not production proof.

## Cleanup

Delete workloads through the intended lifecycle, verify retained resources, remove the cluster, and ensure no host directories, loop devices, credentials, or background processes remain.
