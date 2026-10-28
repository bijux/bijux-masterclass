# Worked answers — StatefulSets, Stable Identity, Quorum, and Fencing

These are complete reference solutions. A different design is valid only when it preserves the same authority, failure, recovery, and evidence boundaries.

## 1. Explain what StatefulSet actually guarantees

StatefulSet provides stable ordinal Pod names, stable network identity through a governing Service, deterministic PVC names from claim templates, and configurable ordered or parallel lifecycle behavior. It can retain claims across scale or deletion and orchestrate rolling updates. It does not provide consensus, elect a database leader, replicate data, fence stale writers, or establish backup consistency. It also cannot make a single-zone volume available in another zone. The controller owns Kubernetes object identity and rollout order; the database or operator owns membership, quorum, log replication, recovery, and write authority. Choosing StatefulSet is therefore a workload-identity decision, not proof that the database is highly available.

## 2. Use stable identity without confusing it with freshness

Stable identity tells clients and controllers which logical member is being referenced, and the PVC preserves one storage identity. The member may still be stale, partially recovered, restored from an older checkpoint, or fenced from writes. DNS can resolve before recovery completes; a mount can succeed before replay. Readiness must include application generation, recovery status, membership, and writer authority. In a replicated system, the current leader may be a different ordinal. Stable identity is necessary for many stateful protocols because members can recognize themselves and their data, but correctness comes from the protocol and its evidence, not from the name.

## 3. Prove fencing across replacement

Start writer generation 1 and allow a durable write. Partition or pause it so the control plane cannot confirm clean shutdown. Promote a replacement with generation 2 only after the fencing authority revokes generation 1 through a mechanism the old process cannot bypass. Let generation 2 commit. Then resume the old process and attempt a write carrying generation 1; the authoritative data path must reject it. Verify the committed value and generation after process restart. Merely observing one Running Pod is insufficient because the stale process can exist outside Kubernetes observation. The test must be bounded to synthetic data and include cleanup that proves no stale attachment or lease remains.

## 4. Distinguish quorum from replica count

The replicas may not belong to the same membership configuration, may share one failure domain, may be caught up to different log positions, or may all accept traffic despite a partition. Kubernetes readiness can be misconfigured as a TCP check and cannot infer consensus. Safe quorum depends on the database’s voting rules, term/epoch, commit index, member identity, and failure-domain placement. The application or operator must publish a readiness decision based on those facts. Three ready Pods can even represent three independent singletons if bootstrap was wrong. The decisive evidence is the engine’s membership and committed generation, not the replica count in the StatefulSet status.

## 5. Review scale-down retention

For authoritative data, retain the claim until the database confirms that member 2 has been removed safely, its data is no longer required for rollback or forensic recovery, and retention policy authorizes deletion. StatefulSet PVC retention can preserve it automatically, but the operator still needs an inventory and eventual disposition. If the workload later scales up, blindly reusing the claim may reintroduce stale membership or data; bootstrap logic must validate generation and wipe or recover deliberately. Automatic deletion is acceptable only for disposable replicas whose data can be reconstructed and whose removal protocol has completed. Scale intent is not itself deletion authority.

## 6. Choose PodManagementPolicy

`Parallel` is safe when each member can bootstrap independently or the application/operator coordinates membership without relying on ordinal startup. It speeds recovery and scaling but can amplify load or race initialization. Ordered behavior is useful when a protocol genuinely requires a predecessor, stable seed, or serialized membership transition. It is not a substitute for consensus or readiness: `atlas-db-1` starting after `atlas-db-0` does not prove member 0 is leader-ready unless the application says so. The policy should follow the engine’s documented lifecycle and failure behavior. Test restart and scale under partial failure; do not preserve ordering merely because StatefulSet defaults suggest it.

## 7. Use partitioned rolling update safely

A partition can leave lower ordinals on the old template while updating selected higher ordinals, creating a bounded canary lane. The upgrade still requires version-skew compatibility, one writer authority, schema and storage-format rules, backup/restore evidence, and quorum health. Observe the updated member’s recovery, replication, latency, and logs before lowering the partition. Rollback is possible only while data and protocol formats remain readable by the old version. The controller’s completion status does not prove database compatibility. The release plan should state exactly when crossing a format or schema boundary makes rollback impossible and who approves that transition.

## 8. Diagnose a split-brain symptom

The consensus or lease system must allow only a quorum-backed term or generation to authorize writes. A fencing token carried to the storage or transaction path should reject the stale side even if it believes it is primary. NetworkPolicy or Service routing may reduce exposure but cannot be the sole correctness mechanism because partitions and stale connections occur. The operator should stop client traffic, preserve both sides, identify membership and generations, and avoid merging writes blindly. Recovery chooses the authoritative history through protocol evidence or an explicit data-loss decision. Kubernetes replica state, Pod age, or ordinal is not enough to select the winner.

## 9. Explain the limit of a PDB

A PDB constrains voluntary disruptions such as drains or some controller evictions so too many selected Pods are not made unavailable simultaneously. It helps maintenance choreography. It does not prevent involuntary Node or zone failures, guarantee that the two Pods form database quorum, reserve replacement capacity, protect storage, or ensure readiness is truthful. It can also block maintenance indefinitely when the cluster lacks capacity or a member is already unhealthy. The disruption budget must align with database quorum, topology, and recovery time, and operators need a documented override decision. It is one control in a data-service availability design, not an HA guarantee.

## 10. Define recovery-aware readiness

It should prove that the correct persistent identity is mounted, the engine has completed crash recovery or log replay, schema and storage formats are compatible, membership is valid, its role is known, writer fencing is current, and any required replication catch-up threshold is met. A replica may be ready for bounded stale reads before it is eligible for writes, so separate endpoint roles may be appropriate. TCP acceptance or process existence is insufficient. The readiness check must be cheap, local enough not to create cascading failure, and based on engine state. The control plane then uses that truthful signal to manage traffic; it does not invent it.

## 11. Separate DNS identity from consistency

The name gives a stable way to address a particular ordinal through Kubernetes DNS. It does not say whether that member is leader, replica, caught up, fenced, or healthy. Clients may need an engine-native discovery endpoint, a role-specific Service, or a proxy that understands membership and consistency. DNS caching also means endpoint changes are not instantaneous. Connection pools can outlive DNS answers. The platform should document whether clients connect to one stable proxy, discover all members, or use separate read/write endpoints. Stable member names support protocols; they are not a routing policy or consistency contract by themselves.

## 12. Choose StatefulSet, Deployment, or operator

Workers should remain a Deployment because individual Pod identity has no business meaning; replacement is desirable, and durable work is external. Assigning each worker a retained PVC would create unnecessary lifecycle and cleanup. Database members may use StatefulSet because stable ordinal and claim identity support the engine. If the database requires membership changes, backup, failover, version upgrades, and recovery orchestration, an engine-specific operator or managed service should own those semantics rather than a bare StatefulSet plus scripts. The selection follows identity and lifecycle requirements, not whether the process “has state.” Course 6 should explicitly reject a StatefulSet when stable identity adds no value.
