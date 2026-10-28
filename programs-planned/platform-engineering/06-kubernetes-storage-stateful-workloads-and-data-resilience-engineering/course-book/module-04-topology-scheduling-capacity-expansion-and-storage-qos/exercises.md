# Exercises — Topology, Scheduling, Capacity, Expansion, and Storage QoS

Work from the chapter and executable artifacts, but write your own reasoning before reading the solutions. Each answer should name the authoritative state, the unsafe shortcut, and the evidence that would decide the case.

## 1. Solve the topology conjunction

A Pod has zone affinity, anti-affinity, two PVCs, and a node-pool constraint. Explain how the scheduler should report failure.

## 2. Interpret CSIStorageCapacity cautiously

What can a `CSIStorageCapacity` object tell the scheduler, and what can it not prove?

## 3. Budget attachment slots

A Node supports 39 attachable volumes and already has 38. A Pod needs two PVCs. Why should the platform reject it before provisioning?

## 4. Handle partial multi-volume provisioning

A database Pod requires data and WAL volumes. The first provisions; the second fails for quota. Design the recovery behavior.

## 5. Analyze an expansion failure

A PVC requests 100 GiB, the backend reports 100 GiB, the device reports 100 GiB, but the filesystem reports 50 GiB. What is the next safe action?

## 6. Evaluate VolumeAttributesClass

A team wants to change provisioned IOPS through `VolumeAttributesClass`. What gates should apply?

## 7. Separate locality from availability

Why can hard zone-local storage improve latency while reducing service availability?

## 8. Break a scheduler-binder deadlock

How can immediate binding, hard Pod affinity, and zonal capacity create a circular dependency?

## 9. Model storage QoS honestly

Define a storage service tier without using only “standard,” “premium,” or provider marketing names.

## 10. Plan recovery headroom

A cluster uses 80% of storage capacity. Explain why 20% free may still be inadequate.

## 11. Review a performance mutation release

A new storage tier reduces p99 latency by 30% but changes reclaim policy from `Retain` to `Delete`. What is the release decision?

## 12. Define evidence for a supported topology profile

What evidence is needed before claiming that `atlas-rwo-durable` supports two zones?
