# Worked answers — Topology, Scheduling, Capacity, Expansion, and Storage QoS

These are complete reference solutions. A different design is valid only when it preserves the same authority, failure, recovery, and evidence boundaries.

## 1. Solve the topology conjunction

The scheduler must evaluate every candidate Node against the conjunction of workload and storage predicates: allowed zone, node labels, taints/tolerations, anti-affinity, volume topology, accessible capacity for both claims, and attachment limits. It should preserve a rejection list per Node rather than return a single generic “unschedulable.” That evidence distinguishes no feasible topology from temporary capacity or policy failures. Delayed binding should occur only after a feasible Node or topology is identified; provisioning claims independently can create stranded volumes. A useful report names the earliest failed predicate and the authoritative source—Pod spec, PV node affinity, CSIStorageCapacity, or driver limit—so remediation does not weaken unrelated constraints.

## 2. Interpret CSIStorageCapacity cautiously

It can advertise that a CSI provisioner reports some capacity for a StorageClass within a topology segment, helping the scheduler avoid selecting a Node where provisioning is predictably impossible. It may also indicate a maximum volume size. It cannot prove a reservation, future availability, backend health, performance, quota, attachment capacity, or successful provisioning. Capacity can change between scheduling and allocation, and a driver may publish conservative or stale information. The object is an input to feasibility, not a durability or service-level guarantee. Evidence for a failed allocation still requires the provisioner request, backend response, quota state, and selected topology.

## 3. Budget attachment slots

The Pod cannot become usable on that Node because it would require 40 attachments. If the Node is the only topology-compatible candidate, provisioning volumes first creates physical effects with no feasible workload placement. Admission or scheduling should account for all required claims and the driver’s allocatable attachment limit, including in-flight operations. The rejection should be explicit and should not trigger a desperate force-detach of unrelated workloads. Capacity planning must include volume count and attach slots, not only GiB. The fix may be a different Node, a workload/storage redesign, or a node class with suitable limits—not an arbitrary increase in claimed capacity.

## 4. Handle partial multi-volume provisioning

The system records a stable operation covering both claims and exposes the partial state instead of forgetting it. It should retry the failed allocation idempotently if the failure is transient, preserving the first volume’s identity. If policy or quota makes completion impossible, it should leave the first volume inventoried and retained until the data owner chooses cleanup; automatic deletion may destroy data if initialization already occurred. Scheduling and readiness remain blocked until both volumes are bound and accessible in one compatible topology. A higher-level platform API can preflight aggregate quota and capacity, but it cannot make external allocation atomic. Reconciliation and compensating cleanup must therefore be explicit.

## 5. Analyze an expansion failure

Do not repeat controller expansion blindly; that phase already succeeded. Determine whether node expansion is required, whether the Pod must restart or remount, and whether the filesystem supports online growth. Inspect PVC conditions, node-plugin logs, device geometry, mount identity, and filesystem tools. Ensure the correct volume is staged and no stale mount masks the device. Then perform or trigger node/filesystem expansion through the supported path and verify application-visible capacity. The workload should not be admitted to consume the extra 50 GiB until the final phase is complete. Shrink is not a rollback; if expansion introduces cost or performance issues, the migration plan may require a new volume and data copy.

## 6. Evaluate VolumeAttributesClass

First confirm Kubernetes and the selected CSI driver support modify-volume behavior for the backend class. Define which attributes are mutable, their allowed ranges, cost, expected latency, and rollback semantics. Ensure the change does not weaken encryption, replication, reclaim, or snapshot compatibility. Apply it to a non-authoritative or replicated test volume, record controller/backend transitions, and run representative workload evidence before and after. Observe throttling and queue depth during convergence. A successful object update is not proof that the backend changed, and a lower latency result does not automatically justify higher cost or reduced durability. The release gate should classify unsupported or unexecuted native evidence honestly.

## 7. Separate locality from availability

Locality reduces network distance and may give predictable throughput, but it narrows the set of Nodes and zones that can run the workload. If the zone fails or all compatible Nodes exhaust attachment capacity, the data may remain durable yet unavailable. Hard locality can also overload local replicas while capacity exists elsewhere. A complete design states whether the application replicates across zones, how failover changes writer authority, how traffic follows the data, and what RTO applies. “Keep compute near storage” is a performance rule, not an availability strategy. Course 5 topology and Course 6 data placement must be reviewed together.

## 8. Break a scheduler-binder deadlock

Immediate binding chooses a storage topology without knowing the final Pod placement, while the scheduler later must honor the PV’s node affinity. If the Pod also has a hard zone or node-pool rule that conflicts, no Node is feasible. Operators may then change affinity or prebind another PV, obscuring the original decision and risking data identity. `WaitForFirstConsumer` breaks the cycle by letting the scheduler choose a feasible topology from the full workload constraints, then provisioning there. The proof should show the chosen Node/topology and preserve why other Nodes failed. Delayed binding does not guarantee success—quota or backend allocation can still race—but it removes one avoidable contradiction.

## 9. Model storage QoS honestly

Describe the workload envelope: operation mix, block sizes, read/write ratio, concurrency, working set, cache state, expected p99 latency, throughput, IOPS, and queue depth. Add capacity and burst behavior, failure domains, replication, encryption, snapshot/clone support, expansion, cost, and evidence status. State whether performance is provisioned, shared, or adaptive and which metrics reveal throttling. Include a representative benchmark and an application-level oracle because device throughput alone may not improve transaction latency. The platform can map this profile to a provider tier, but the profile remains the stable contract. If no operated evidence exists, label the numbers hypotheses rather than guarantees.

## 10. Plan recovery headroom

Recovery may require a full replacement volume, snapshot copy-on-write growth, temporary restore space, replication catch-up, filesystem expansion, or data migration while the source remains online. Capacity is also segmented by zone, class, quota, attachment count, inodes, and object count; aggregate free bytes can be unusable. Thin provisioning may hide physical exhaustion. Headroom should be derived from the largest credible recovery or migration operation plus growth during RTO, not a fixed percentage alone. Admission should reserve or protect recovery capacity so ordinary workloads cannot consume it. The plan must include snapshots and backup repository capacity, because source and recovery systems often fail together under pressure.

## 11. Review a performance mutation release

Reject it before considering the performance improvement. Reclaim policy is a non-compensable data-safety boundary for authoritative production state. A faster service that can automatically destroy the volume after claim deletion violates the established data contract. Create a corrected class that preserves retention, then repeat native capability, migration, restore, cost, and workload evidence. If the provider cannot offer the performance tier with the required lifecycle, the platform must present the trade-off explicitly rather than hide it behind a “premium” label. Performance gates are evaluated only after correctness, authority, and recoverability gates pass.

## 12. Define evidence for a supported topology profile

Static evidence includes class allowed topologies and workload placement rules. Semantic evidence shows delayed binding and per-Node feasibility. Native cluster evidence must provision in each zone, schedule compatible Pods, reject cross-zone attachment, survive controller and node restarts, and verify capacity publication. Backend evidence must establish volume durability and attachment behavior. Recovery evidence should restore or fail over according to the declared RPO/RTO. Operated evidence includes capacity alarms, maintenance, quota, and real incidents over time. Merely listing two zones in a StorageClass proves only intended placement, not replicated data or cross-zone availability.
