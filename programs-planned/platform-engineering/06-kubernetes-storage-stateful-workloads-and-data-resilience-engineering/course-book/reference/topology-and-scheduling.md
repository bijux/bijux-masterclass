# Topology and storage-aware scheduling

Storage placement combines compute constraints and storage accessibility. The feasible Node set is the intersection of:

```text
CPU/memory fit
∩ taints and affinity
∩ topology policy
∩ PV node affinity or provisionable zones
∩ CSI attach capacity
∩ security and tenancy rules
```

`WaitForFirstConsumer` delays dynamic provisioning until a consumer’s scheduling context is available. It prevents one common race—provisioning a zonal volume before placement—but does not guarantee capacity, replacement options, or recovery topology.

## Diagnostic method

For every candidate Node, preserve each rejection reason. Then inspect:

- PVC binding mode and selected-node annotation;
- StorageClass allowed topologies;
- PV node affinity;
- CSIStorageCapacity where supported;
- CSINode attach limits;
- existing attachments;
- Pod affinity, spread, resources, and taints.

## Availability review

Initial schedulability is not enough. Confirm that the workload can be replaced after one planned Node loss and, where claimed, one zone loss. Rollout surge and recovery may need additional attach slots and capacity. A singleton zonal volume can be perfectly schedulable and still have poor availability.
