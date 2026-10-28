# Worked answers

## 1. What identity does a StatefulSet preserve?

It preserves stable ordinal-based Pod names and associations such as governing DNS identity and per-ordinal PVCs. Replacement Pods still receive new UIDs and processes. The application must decide what the ordinal means. Stable name is not leadership, durability, or availability.

## 2. Why does a StatefulSet not make emptyDir durable?

emptyDir follows the Pod lifetime. A replacement with the same ordinal gets a new empty directory. StatefulSet controls Pod identity and can associate PVCs; it cannot change a volume type’s persistence semantics. The decisive evidence is the volume source and data lifecycle.

## 3. Why is pod-0 not automatically a safe leader?

Ordinal assignment is deterministic, but leadership requires coordination that handles partitions, delayed messages, failure, and fencing. Two processes can each believe they should lead if the protocol is naive. Use a correct consensus/lease design and preserve leadership evidence.

## 4. What can OrderedReady block?

Creation, scale, or rollout can wait for a lower ordinal to become Ready. This protects order but can extend outages or deadlock on one broken member. The operator should repair or deliberately change strategy; deleting later/earlier Pods blindly may violate application invariants.

## 5. When is Parallel pod management appropriate?

When members do not require ordered startup, scale, or termination. It improves speed and independence. The decision must come from application semantics; it is unsafe if membership initialization or data recovery depends on ordinal order.

## 6. What does a rolling-update partition do?

It restricts automatic updates to ordinals at or above the partition, leaving lower ordinals on the old revision. This enables staged rollout or canarying. Release evidence must track which members run which template and whether mixed versions are compatible.

## 7. Why are StatefulSet PVCs commonly retained?

Automatic deletion could destroy data when a workload is scaled or removed accidentally. Retention separates compute lifecycle from data lifecycle. It also leaves explicit cleanup, cost, and compliance work. Course 6 defines backup/restore and safe deletion policy.

## 8. Why should Atlas worker remain a Deployment?

Its instances consume shared durable work but do not need stable ordinal identity. Correctness should come from durable queue leases/idempotency, not a fixed Pod name. Using StatefulSet would add ordered identity without solving storage or work coordination.

## 9. What does a headless Service contribute?

It provides a governing service identity and typically individual DNS records for StatefulSet Pods rather than virtual-IP load balancing. Course 5 owns DNS and packet behavior. The Service does not prove process readiness or data-system health by itself.

## 10. When might OnDelete update strategy be chosen?

When application-specific orchestration must decide when each member restarts, such as a carefully controlled stateful upgrade. It transfers rollout responsibility to another workflow and can leave mixed versions indefinitely. Course 7 would need explicit choreography and evidence.

## 11. What is the difference between stable Pod name and Pod UID?

The ordinal name is reused for the logical member. Each replacement is a new API object with a new UID. Logs, ownership, and destructive preconditions should retain UID so evidence does not conflate two lifetimes under one stable name.

## 12. Which proof would justify a production StatefulSet?

Beyond manifest correctness, evidence must cover application replication/consensus, storage durability/topology, backup/restore, failover, fencing, version skew, rollout, disruption, capacity, and operator runbooks. Course 4 intentionally cannot make that production claim alone.
