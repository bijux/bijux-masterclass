---
module_id: LSDS-015
program: Large-Scale Data Systems Engineering
level: 1
module_number: 15
title: Failure Detection and Re-Replication
status: complete
last_verified: 2026-09-03
---

# Failure Detection and Re-Replication

## One-Page Review

### Governing question

How should a distributed storage system turn incomplete liveness observations into safe membership changes and prioritized repair without copying transiently unavailable data endlessly, trusting stale replicas, or overloading the survivors?

### Essential definitions

- A **failure detector** reports suspicion or a confidence level from missing/late observations; it does not prove physical death.
- A **heartbeat** is periodic liveness evidence from a process or peer.
- An **inventory** or **block report** describes replicas/fragments observed at a storage node under a report epoch and completeness rule.
- **Membership** is the authoritative versioned set of storage participants and their states.
- **Down** commonly means presently unreachable; **out** means excluded from placement. Exact product semantics vary.
- **Under-protected** data has fewer current valid independent copies/fragments than its target policy.
- **Re-replication** creates a new full replica from a verified current source; coded protection may reconstruct a fragment instead.
- **Recovery** repairs missing or stale members of an existing placement group; **backfill** commonly populates data after placement changes or large divergence.
- A **false positive** suspects a healthy node; a **false negative** fails to suspect a failed node promptly.
- The **exposure window** spans loss/damage, detection, authoritative decision, scheduling, transfer, verification, and registration of restored protection.

### Central model, mechanism, or theorem

For object version `x`, let `E(x)` be the expected authorized recovery set under placement epoch `e`, and `V_t(x)` the current compatible verified set observed at time `t`. The deficit is not merely `|E|-|observed|`: policy evaluates `V_t` across failure domains and code requirements. Repair selects a verified source or decodable set, reserves an authorized target under a current epoch, copies or reconstructs, validates identity/length/integrity, registers the new member atomically, and only then retires obsolete copies.

Failure detection is a trade-off. Short thresholds reduce time to suspicion but increase false positives during congestion, pauses, or partitions. Delaying repair avoids copying for transient outages but extends exposure after permanent loss. Tune from fault duration, protection margin, repair bandwidth, workload, consequence, and measured detector behavior—not heartbeat interval alone.

### Critical invariants

- Missing responses create suspicion, not proof of disk destruction or data loss.
- Only an authorized membership service changes placement eligibility and epochs.
- Inventories are complete only under explicit node, report, sequence, and epoch rules.
- Only current compatible checksum-verified replicas/fragments count toward protection.
- A repair target is distinct under every required failure-domain constraint.
- Repair uses a fenced idempotent operation and cannot resurrect a deleted/stale generation.
- New protection is verified and registered before any old candidate is deleted.
- Repair/backfill concurrency and bandwidth are bounded so survivors and foreground traffic remain viable.
- Startup and control-plane recovery wait for sufficient inventory evidence before destructive reconciliation.

### Common failures

Frequent failures are equating a missed heartbeat with permanent loss, using one observer behind one failed switch, declaring membership independently on every node, repairing every transient outage immediately, counting stale reports, copying from the closest unverified replica, choosing a target in the same rack, marking repair complete after transfer but before verification/registration, deleting returning replicas before reconciliation, starting re-replication before startup inventories converge, using fixed throttles during correlated loss, and reporting node health without object protection margin.

### Compact example

With a 3-second heartbeat interval, a 15-second suspicion threshold, a 300-second down-to-out delay, and 640 GiB to rebuild at a sustained 80 MiB/s, modeled transfer time is 8,192 seconds. Even ignoring queues, verification, and registration, total exposure from last evidence through replacement is about 8,507 seconds (141.8 minutes). Reducing detection by five seconds barely matters if repair throughput dominates; adding bandwidth or reducing repair scope may matter more.

### Connections

[LSDS-009](009-cluster-failure-assumptions.md) supplies the fault model. [LSDS-011](011-distributed-block-storage.md) supplies inventory and replica states. [LSDS-013](013-replication-and-erasure-coding.md) supplies protection margin and reconstruction cost. [LSDS-014](014-read-and-write-pipelines.md) supplies transfer, acknowledgement, backpressure, and retry semantics.

## Governing Question

A storage controller cannot directly observe whether another machine has crashed, is paused, is overloaded, has lost its network path, or is merely slow. It sees missing heartbeats, failed RPCs, peer reports, device errors, and late inventories. Acting too slowly extends under-protection. Acting too quickly can move petabytes unnecessarily, fill remaining devices, saturate the network, and cause healthy nodes to miss heartbeats—a cascading failure.

Detection is only the first transition. A system must decide membership, compute changed placement, identify exactly which versions are under-protected, choose valid sources and eligible targets, schedule constrained transfers, validate reconstructed bytes, publish new inventory, and clean up stale or excess copies safely.

The governing question is how to couple these steps without conflating them. Suspicion is epistemic evidence. Membership is an authoritative control-plane decision. Placement is desired state. Inventory is observed state. Repair changes physical state. Protection is a policy predicate over verified state. Keeping these layers distinct makes false positives recoverable and repair auditable.

## Why This Matters

Large clusters continuously experience device errors, restarts, maintenance, software crashes, packet loss, congestion, slow storage, and topology changes. The normal operating state includes some failure and repair. A design that works only when every node is healthy is not a large-scale storage design.

Repair traffic can dwarf foreground traffic after a rack or zone event. Every missing replica requires source reads, network transfer, target writes, checksums, metadata updates, and often cache or device contention. Erasure-coded repair can read many fragments for one replacement. Survivors bear the work while already serving degraded reads.

False positives matter economically and operationally. Rebuilding a temporarily unreachable 100-TiB node may create 100 TiB or more of network and write work, only for the node to return with usable data. But waiting too long after permanent failure increases the chance another loss exceeds remaining redundancy. The right delay depends on the distribution of outage duration and current margin.

Control-plane restarts are especially dangerous. Before inventories arrive, every block can appear missing. Safe mode, peering, or equivalent barriers prevent a partially informed controller from initiating massive repair or deletion. The barrier must depend on evidence relevant to the policy, not elapsed time alone.

## Prerequisites and Retrieval

Recall placement epochs from [LSDS-003](003-range-hash-and-consistent-partitioning.md), locality from [LSDS-004](004-data-locality.md), workload graphs from [LSDS-005](005-distributed-task-graphs.md), dependency bottlenecks from [LSDS-007](007-narrow-and-wide-transformations.md), and failure assumptions from [LSDS-009](009-cluster-failure-assumptions.md).

Retrieve resource and recovery accounting from [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md), replica/inventory classifications from [LSDS-011](011-distributed-block-storage.md), authority epochs from [LSDS-012](012-metadata-servers-and-namespace.md), protection margin from [LSDS-013](013-replication-and-erasure-coding.md), and bounded transfer/retry from [LSDS-014](014-read-and-write-pipelines.md).

You should understand leases, clocks, timeouts, RPC failure, membership, consensus, checksums, replication, erasure coding, queues, bandwidth, percentiles, topology, idempotency, scrubbing, and capacity headroom.

## Learning Objectives

After completing this module, you should be able to:

- distinguish liveness observation, suspicion, membership, placement, inventory, and protection;
- explain false-positive/detection-delay trade-offs in heartbeat and probe systems;
- define node incarnation, membership epoch, report epoch, and placement epoch;
- reconcile full and incremental replica inventories without treating either as authority;
- classify missing, unreachable, stale, corrupt, misplaced, excess, and orphan replicas;
- compute simple detection, delay, repair, and exposure time bounds;
- prioritize repairs using remaining margin, consequence, demand, age, and cost;
- select verified sources and topology-valid targets;
- design idempotent, fenced, crash-safe re-replication;
- distinguish recovery, backfill, rebalance, and garbage collection;
- prevent retry storms, flapping, correlated overload, and full-target deadlock;
- specify safe startup, maintenance, decommission, and return-to-service workflows; and
- define telemetry, fault injection, restore evidence, and named consequence review.

## Core Exposition

### Observation is not failure

A missing heartbeat means expected evidence did not arrive. Causes include process death, device stall, CPU pause, saturated event loop, packet loss, asymmetric partition, broken observer, clock effects, or overload. No finite timeout can distinguish every case in an asynchronous network.

Use language that preserves uncertainty: alive evidence, suspect, unreachable-from-observer, down by membership decision, out of placement, administratively drained, failed device, and destroyed media. These states drive different actions.

An observer's own health matters. A rack with a broken uplink may report every outside node as failed. Multiple observers in distinct topology domains or indirect probes reduce one-observer bias. They still feed an authoritative membership mechanism rather than independently rewriting placement.

### Heartbeats, probes, and accrual evidence

Central heartbeats are simple: each storage node periodically reports liveness and perhaps load/capacity. At large scale the receiver and synchronized intervals can hotspot. Peer probing distributes work. SWIM separates randomized failure detection from gossip-style membership dissemination and introduces suspicion before declaration.

A binary detector compares last evidence with a threshold. An accrual detector instead exports a suspicion level derived from arrival history, letting consumers choose thresholds by consequence. Either approach depends on workload, pauses, network tails, clock behavior, and implementation.

Tune and measure detection latency and false positives together. A detector that fires instantly on one lost packet is fast and noisy. A detector that never makes a false accusation may react too late. Adaptive thresholds need bounds so widespread overload does not stretch detection indefinitely.

### Incarnations and membership epochs

A restarted process at the same address is not necessarily the same storage incarnation. Bind node ID, storage/device IDs, boot/incarnation ID, credentials, and membership epoch. Reject delayed heartbeats and reports from older incarnations.

Membership changes should be ordered by a durable authority such as consensus monitors or a metadata master. A versioned membership/placement map lets clients and storage nodes reject stale operations and redirect to a later view.

Separate `down` from `out` when useful. A down node may remain in desired placement during a transient grace period. Marking it out remaps data and initiates repair/backfill. Administratively `in/out` and operationally `up/down` are different axes.

### Inventory evidence

Heartbeats show process responsiveness; inventories show which block/fragment versions a node claims to store. A full report establishes a baseline under a report ID, incarnation, start/end marker, sequence, and completeness rule. Incremental reports describe additions, finalization, corruption, or deletion after that baseline.

Reports can be delayed, duplicated, reordered, or interrupted. Do not replace a complete inventory with a partial report. Reconcile tuple `(object, generation, fragment/copy index, length, checksum evidence, node/device, report epoch)` against authoritative namespace and placement.

Inventory presence is not validity. The reported copy may be stale, corrupt, incomplete, unauthorized, or from a deleted version. Conversely, a temporarily missing report does not prove the bytes vanished.

### Protection state

For each live/snapshot version, compute the compatible verified set across failure domains. States can include fully protected, under-protected, minimally decodable/readable, unavailable, irrecoverable, misplaced, and over-protected. Desired replica count alone is not current state.

Count margins by modeled event. Three current replicas across three hosts but one rack have host margin and no rack margin. A coded stripe at exactly `k` valid fragments is readable with zero additional erasure margin.

Prioritize from current evidence, not last configuration. A corrupt copy should stop counting immediately even if the node remains up. A newly returned verified copy can reduce deficit after reconciliation.

### Detection-to-repair state machine

A durable workflow can use states: observed healthy, suspect, down, grace, out/remapped, repair planned, target reserved, transferring, verifying, registered, policy restored, and cleanup eligible. Transitions carry membership, placement, object, and operation epochs.

Not every down event reaches out/remapped. A node that returns during grace can rejoin after incarnation and inventory validation. A permanently failed node advances to repair. Administrative maintenance can pre-copy or preserve `noout` behavior under explicit risk control.

Make every transition observable and retryable. A controller restart reconstructs workflow from durable intent and physical evidence rather than issuing duplicate copies blindly.

### Source selection

A repair source must match authoritative object version, generation, length, protection profile, and integrity. For replication, choose one or more verified current copies. For erasure coding, choose a decodable compatible fragment set and validate inputs.

Selection balances source health, topology, load, queueing, network path, and integrity recency. The closest source may already be overloaded. Spread repair reads so one survivor does not become the next failure.

When replicas disagree, stop ordinary repair. Use trusted end-to-end digests, version history, commit logs, or recovery authority. Copying the majority can replicate common corruption or stale data.

### Target selection and reservation

The target must be eligible under current placement and distinct across required failure domains. Check device class, capacity, performance tier, encryption/tenant policy, maintenance state, and network reachability.

Reserve bytes and admission capacity before expensive transfer. Aggregate free space is insufficient if eligible racks are full. Reservations expire or are released idempotently after failure; they are bound to repair operation and object generation.

Avoid placing replacements on a node likely to be drained or sharing the suspected domain. Placement maps can change mid-repair, so validate epoch at registration and redirect safely if needed.

### Transfer, verification, and registration

Issue a repair intent with unique operation ID, source set, target, object/generation, expected length/digest, placement epoch, and token. Transfer through bounded pipelines with checksums and backpressure. Duplicate retries resume or return prior outcome.

After writing, verify target length and integrity; for coded data, verify the reconstructed fragment and, where required, logical stripe digest. Persist it under the intended generation. Only then atomically register it in authoritative inventory/protection state.

“Bytes copied” is not repair complete. Registration can fail after transfer, leaving an orphan candidate. Reconciliation identifies and completes or removes it after grace. Never delete the last old good copy based on an unregistered candidate.

### Recovery, backfill, and rebalance

Recovery often updates missing or stale objects among a placement group's current acting members. Backfill commonly populates a new or far-behind target after placement change and can scan/compare large ranges. Rebalance moves data to restore distribution after membership or weights change.

Product terms differ, so describe actual state and work. All three consume source reads, network, target writes, checksums, metadata, and queues. Garbage collection removes obsolete or excess state only after safety proof.

Moving data for balance is lower urgency than restoring a zero-margin object unless performance availability requires otherwise. Maintain distinct queues/priorities and prevent starvation.

### Grace periods and transient failures

A down-to-out delay trades wasted copy work against longer under-protection. Estimate outage-duration distribution, object margin, correlated risk, node data volume, repair throughput, and consequence. One fixed delay may be wrong for a minimally protected stripe and an over-replicated cache.

Transient nodes returning after replacement can create excess copies. Reconcile their incarnation and inventory; reuse a valid authorized copy when safe or delete only after current protection and lifecycle checks.

Flapping repeatedly triggers view changes, peering, and repairs. Add hysteresis, suspicion phases, domain-aware reporters, local-health signals, and operational quarantine. Fix the underlying latency or network issue rather than only lengthening timeouts.

### Repair prioritization

Primary priority is risk of irreversible loss: lowest remaining independent margin, correlated domain exposure, latent corruption, and predicted time to another failure. Add data consequence, age, demand/availability, repair size, source scarcity, and policy deadlines.

Avoid a single scalar that hides hard constraints. Use priority classes—critical zero-margin, policy deficit, misplaced, rebalance—and fair scheduling within classes. Prevent a stream of tiny low-value repairs from indefinitely starving a large critical object.

Recompute priority as nodes return, new faults occur, or integrity evidence changes. Cancel or redirect stale work safely using operation and placement epochs.

### Bandwidth, concurrency, and feedback

Repair is a dependency graph over sources, network links, targets, checksum/decoder CPU, and metadata. Per-node and per-domain concurrency limits prevent thundering herds. Byte-rate controls handle different object sizes better than operation counts alone.

Static throttles are simple and can be too slow during disaster or too aggressive at peak. Feedback control can use foreground latency/error objectives, queue age, remaining margin, and predicted completion. Bound its response to prevent oscillation.

Separate inbound and outbound reservations: a node can serve several repairs while receiving several more. Account both. Preserve headroom for another failure and production growth during the repair window.

### Cascading failure prevention

Repair traffic can delay heartbeats, fill queues, and make healthy nodes look dead. Retry storms and hedged degraded reads amplify load. Control traffic needs reserved capacity or priority, but a separate network is not automatically isolated if it shares switches, power, CPU, or disks.

Use admission control, exponential backoff with jitter, bounded retries, circuit breaking, per-domain rate limits, and local health. Do not allow every controller or client to initiate the same repair independently.

During broad correlated faults, stabilize membership and establish authoritative scope before maximizing repair. Moving data based on a partitioned minority view can worsen loss.

### Startup and safe mode

After controller restart, the authoritative namespace may know desired blocks but not current locations until reports arrive. Treating all absent observations as loss would initiate a repair storm and potentially delete valid returning copies.

A safe-mode or peering barrier gathers sufficient reports and reconstructs authoritative histories before normal repair/deletion. Exit criteria should cover a justified fraction or policy state, minimum domains, journal/map readiness, and known exceptions. Time alone is weak evidence.

Read availability during this phase depends on semantics and verified inventories. Writes may remain blocked to prevent divergent histories. Operators need progress, missing-domain, and override risk visibility.

### Maintenance and decommission

Planned maintenance differs from surprise failure. Mark intent, prevent new placement, pre-copy data or verify alternate protection, drain client I/O, preserve return identity, and confirm policy before shutdown. A maintenance window can avoid immediate remap if redundancy remains sufficient.

Decommission permanently removes placement eligibility and waits until every affected live/snapshot object satisfies policy elsewhere. Count bytes and objects, not just node status. Handle stuck open writers, full target domains, and obsolete generations explicitly.

Returning service requires hardware/software validation, new incarnation where appropriate, inventory reconciliation, scrub sampling, and gradual load. Do not count old replicas until compatible and verified.

### Latent corruption and scrubbing

Failure detection includes integrity failure, not only liveness. A responsive node can return wrong bytes. Scrubbing discovers latent sector, memory, firmware, or software corruption before another replica disappears.

A checksum mismatch turns a suspected fragment into a known invalid input under the checksum's trust assumptions. Prioritize repair based on remaining verified margin. Preserve evidence and quarantine recurring faulty paths.

Scrub consumes the same resources as reads and repair. Coordinate rates, but do not defer so long that cold corruption remains hidden across the entire redundancy lifetime.

### Security and governance

Attackers can forge heartbeats, reports, repair requests, or placement updates; replay old epochs; exhaust repair bandwidth; or use repair paths to exfiltrate data. Authenticate nodes and controllers, authorize exact objects/actions, protect maps and reports, rate-limit, and audit decisions.

Repair must preserve encryption and tenant boundaries. A target needs approved location/residency and key access. Logs and inventories expose object identifiers, topology, and health; restrict and minimize them.

Deletion, legal holds, snapshots, and retention interact with returning and orphan replicas. A repair controller cannot decide domain policy from copy count. Consequence-bearing repair and disaster actions need named data-owner, security, legal/records, ethics, and recovery authority.

### Observability and evidence

Measure heartbeat/probe latency and loss, suspicion/down/out events, false positives, flapping, report completeness/lag, membership/map propagation, protected objects/bytes by margin/domain, and corrupt/stale/missing/misplaced states.

For repair, record queue age, priority, object/version, source/target domains, operation/placement epochs, bytes read/transferred/written, throughput, retries, checksum results, duration by stage, registration, and cleanup. Aggregate sensitive identifiers carefully.

Validate with process kill, pause, CPU/disk/network delay, packet loss, asymmetric partition, rack isolation, restart/incarnation, corrupt reports/data, full targets, controller failover, multiple simultaneous losses, and foreground load. Prove recovery by exact digest and authoritative registration, not a green node dashboard.

## Definitions and Notation

Let authoritative placement epoch `e` define expected set `E_e(x)` for object version `x`. Let observed set `O_t(x)` come from reports at time `t`. Let `V_t(x)` be the subset that is current, compatible, authorized, integrity-valid, and accessible enough for the policy.

For replication target `r`, count deficit `d=max(0,r-|V_t|)` is useful only after failure-domain constraints. For an MDS `k+m` stripe, count erasure margin is `g=|V_t|-k`; `g=0` is decodable with no additional count margin and `g<0` is not ordinarily decodable.

Let last accepted liveness evidence arrive at `t_0`, suspicion/decision delay be `T_d`, grace before remap be `T_g`, queue/reservation delay `T_q`, transfer time `T_x`, verification/registration time `T_v`, and total exposure estimate `T_e=T_d+T_g+T_q+T_x+T_v`. The actual loss may precede `t_0`; state the measurement origin.

For bytes `B` and sustained effective repair throughput `u>0`, ideal transfer duration is `T_x=B/u`. Shared sources, coding fan-in, topology, foreground work, retries, and tail skew reduce effective throughput. Aggregate throughput does not prove each critical object finishes promptly.

Let detector false-positive rate be `F_p` under a named workload and observation window and detection latency distribution be `D`. Threshold choice is multi-objective; minimizing one without bounding the other is not a correct optimization.

## Mechanisms, Invariants, or Proof Structure

To design or audit failure detection and repair:

1. Define faults, observers, heartbeats/probes, suspicion, and detector evidence.
2. Separate node incarnation, membership decision, placement epoch, and client maps.
3. Define complete/incremental inventory identity, sequencing, and reconciliation.
4. Compute current verified protection by code and real failure domain.
5. Choose grace and priority from margin, outage evidence, consequence, and repair cost.
6. Select verified sources and authorized reserved topology-valid targets.
7. Transfer under bounded backpressure with fenced idempotent repair identity.
8. Verify and register new state before cleanup; reconcile crash candidates safely.
9. Protect foreground/control traffic and adapt recovery without oscillation.
10. Test startup, partitions, flapping, correlated loss, corruption, full capacity, and restore.

The following fixture computes a simple exposure timeline and a large repair backlog. It assumes constant effective throughput and omits queue, verification, contention, coding fan-in, and topology constraints.

<!-- bijux-verify: {"id":"repair-exposure-accounting","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"heartbeat_interval_s=3 detection_s=15 grace_s=300\nrepair_bytes=687194767360 throughput_mib_s=80 transfer_s=8192.0\nmodeled_exposure_s=8507.0 modeled_exposure_min=141.8\nbacklog_bytes=131941395333120 aggregate_gib_s=2 backlog_hours=17.07\nreplica_margin_before=2 replica_margin_after_loss=1 replica_margin_after_repair=2\n","stderr":""}} -->
```python
MIB = 1024 * 1024
GIB = 1024 * MIB
TIB = 1024 * GIB

heartbeat_interval = 3
detection = 15
grace = 300
repair_bytes = 640 * GIB
throughput = 80 * MIB
transfer = repair_bytes / throughput
exposure = detection + grace + transfer

print(
    f"heartbeat_interval_s={heartbeat_interval} "
    f"detection_s={detection} grace_s={grace}"
)
print(
    f"repair_bytes={repair_bytes} throughput_mib_s={throughput // MIB} "
    f"transfer_s={transfer:.1f}"
)
print(
    f"modeled_exposure_s={exposure:.1f} "
    f"modeled_exposure_min={exposure / 60:.1f}"
)

backlog = 120 * TIB
aggregate = 2 * GIB
print(
    f"backlog_bytes={backlog} aggregate_gib_s={aggregate // GIB} "
    f"backlog_hours={backlog / aggregate / 3600:.2f}"
)

replication_target = 3
valid_before = 3
valid_after_loss = 2
valid_after_repair = 3
print(
    f"replica_margin_before={valid_before - 1} "
    f"replica_margin_after_loss={valid_after_loss - 1} "
    f"replica_margin_after_repair={valid_after_repair - 1}"
)
```

The margin output counts further copy erasures before zero readable copies, assuming valid independent copies; a real policy also checks domains. Heartbeat interval is context, not added to detection because the model defines detection from last accepted evidence. Production exposure includes queue and verification and may start before the final heartbeat.

Correctness proof separates suspicion from membership, validates inventories and sources, fences epochs, and registers verified replacements before cleanup. Availability and risk evidence need detector distributions, actual topology, repair tails, foreground contention, and correlated-fault exercises.

## Alternatives and Trade-Offs

Central heartbeats provide a simple authoritative view and concentrate receiver load. Peer probes spread detection and require membership dissemination/decision. Direct probes are fast on healthy networks; indirect probes reduce path-specific false positives and add traffic.

Fixed timeouts are predictable and insensitive to learned bad history. Adaptive/accrual thresholds follow observed latency and can mask changing overload or behave poorly with sparse samples. Both need explicit bounds and measurement.

Immediate remap shortens permanent-failure exposure and wastes work on transient faults. Long grace reduces churn and prolongs risk. Per-policy grace uses margin and consequence and adds complexity.

Eager parallel repair minimizes backlog in isolation and overloads survivors. Strict throttling protects foreground work and lengthens exposure. Feedback scheduling balances objectives and must be stable under missing metrics.

Copy from one replica is simple and concentrates source load. Multi-source/subrange repair can parallelize and increases coordination. Erasure reconstruction requires sufficient fragments and may use local or regenerating techniques.

Full inventories establish a baseline and are large. Incremental reports are efficient and can drift after gaps. Use both with sequence/completeness rules. Scanning storage on every restart maximizes local evidence and delays return.

Static repair priorities are auditable and slow to respond. Dynamic risk scores adapt and can hide policy in weights. Hard priority classes plus dynamic ordering within them preserve safety constraints.

Reusing a returning replica saves transfer if compatible and verified. Always discarding it simplifies reasoning and wastes I/O. Never trusting it ignores valuable recovery information; reconcile rather than assume.

## Failure Modes and Misconceptions

- **“No heartbeat means the disk is dead.”** It means expected liveness evidence is absent.
- **“The shortest timeout is safest.”** False positives and repair storms can create greater risk.
- **“One observer can declare global failure.”** Its own network domain may be isolated.
- **“Membership gossip is authoritative placement.”** Weak dissemination needs a defined decision layer for mutations.
- **“A block report authorizes every reported replica.”** Namespace/version/integrity policy remains authoritative.
- **“Observed count equals valid protection.”** Stale, corrupt, colocated, or unauthorized copies do not count.
- **“Down and out are synonyms.”** Liveness and placement eligibility are distinct axes in many systems.
- **“Repair starts when copying begins.”** Detection, decision, queue, and reservation already consume exposure time.
- **“Repair finishes when bytes arrive.”** Verification and authoritative registration remain.
- **“Closest is the best source.”** Integrity, load, diversity, and path health can dominate distance.
- **“Any empty node is a valid target.”** Policy, domain, class, tenancy, maintenance, and reserve apply.
- **“Returning replicas should be deleted immediately.”** Reconcile generations, snapshots, and current protection first.
- **“Every transient outage should trigger full repair.”** Grace can avoid costly churn when margin permits.
- **“A fixed low recovery rate protects production.”** It can leave data exposed beyond its objective.
- **“Maximum repair bandwidth is always safest.”** It can overload survivors and trigger cascade.
- **“Aggregate backlog age shows critical risk.”** Track per-object margin and tail age.
- **“Safe mode is a timer.”** It should be an evidence barrier over authoritative history and inventories.
- **“Maintenance is the same as crash failure.”** Planned drain can preserve protection before shutdown.
- **“Responsive means uncorrupted.”** Liveness and integrity are independent.
- **“Internal repair success certifies regulated recovery.”** Named domain review and restore evidence remain required.

## Worked Examples

### Example 1

**Situation:** Ten nodes behind one top-of-rack switch cannot reach a target node. **Reasoning:** Reports are numerous but share one observer domain. Seek independent observers and authoritative topology evidence before declaring the target globally down.

### Example 2

**Situation:** A node pauses for 40 seconds during a 300-second down-to-out grace. **Reasoning:** It may be marked down but can return before remap. Validate incarnation and inventory, then restore service without a full-node rebuild if policy permits.

### Example 3

**Situation:** Triple-replicated data loses one node; the two survivors share a rack. **Reasoning:** Copy count remains two and present readability may exist, but rack-domain protection is poor. Prioritize targets in a distinct authorized rack and verify the source.

### Example 4

**Situation:** A `10+4` stripe has exactly ten checksum-valid fragments after a rack event. **Reasoning:** It is decodable with zero count margin. Put it in the highest repair class, reserve a valid domain target, reconstruct from compatible verified inputs, and register before lower-risk rebalance.

### Example 5

**Situation:** Repair transfer succeeds and the controller crashes before registration. **Reasoning:** The target holds a candidate tied to an operation ID. Recovery queries durable intent and target evidence, verifies it, and registers or expires it; it does not copy again or treat it as an arbitrary orphan.

### Example 6

**Situation:** A node repeatedly flaps under repair load. **Reasoning:** Reduce cascading pressure, inspect device/network/event-loop latency, use hysteresis and distinct reporters, quarantine if needed, and avoid oscillating placement every cycle.

### Example 7

**Situation:** A controller restarts and only 60% of node reports have arrived. **Reasoning:** Do not infer 40% data loss. Remain in an evidence-gathering/peering mode, expose progress and known risks, and avoid destructive repair/cleanup until exit criteria hold.

### Example 8

**Situation:** A 120-TiB backlog has 2 GiB/s effective aggregate throughput. **Reasoning:** Ideal drain time is 61,440 seconds or 17.07 hours before new faults, skew, verification, and contention. Per-object critical tails may be longer despite that average.

### Example 9

**Situation:** A source replica is nearest but last scrubbed 18 months ago; another is remote and recently verified. **Reasoning:** Integrity recency and consequence may favor the remote source. Verify before and after copying; proximity is not authority.

### Example 10

**Situation:** An archive target rack has capacity but violates residency and key policy. **Reasoning:** It is ineligible. Protection repair must honor security and governance domains; escalate lack of eligible capacity rather than silently crossing the boundary.

## Cross-Program Connections

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns failure-detector theory, membership, consensus, leases, epochs, idempotency, and partitions. [Network Engineering](../../24-network-engineering/ROADMAP.md) supplies loss, latency, asymmetric reachability, congestion, topology, and control/data paths.

[Operating Systems](../../22-operating-systems/ROADMAP.md) supplies process pauses, scheduling, devices, filesystem errors, caches, checksums, and I/O queues. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies media/controller faults, memory corruption, buses, power, and hardware topology.

[Security Engineering](../../25-security-engineering/ROADMAP.md) supplies node identity, mutual authentication, authorization, anti-replay, key domains, audit, and adversarial availability. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies hazard analysis, correlated failures, feedback stability, evidence, and recovery governance.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns operational membership, topology labels, capacity, maintenance, alerts, automation, SLOs, and incidents. [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns data consequence, authoritative versions, retention, residency, holds, and recovery policy.

GFS and HDFS describe master-driven heartbeats, inventories, placement, and re-replication. Ceph documents peer reports, monitor map decisions, down/out states, peering, recovery, backfill, scrubbing, and concurrency reservation. SWIM and failure-detector research formalize suspicion and scalability trade-offs. Replica-maintenance research emphasizes repair faster than permanent losses while avoiding transient-failure churn.

## References

- Tushar D. Chandra and Sam Toueg, [*Unreliable Failure Detectors for Reliable Distributed Systems*](https://research.google/pubs/unreliable-failure-detectors-for-reliable-distributed-systems/), Journal of the ACM, 1996. Primary failure-detector abstraction and reliability theory.
- Abhinandan Das, Indranil Gupta, and Ashish Motivala, [*SWIM: Scalable Weakly-Consistent Infection-Style Process Group Membership Protocol*](https://research.google/pubs/swim-scalable-weakly-consistent-infection-style-process-group-membership-protocol/), DSN, 2002. Primary probing, suspicion, dissemination, scale, and false-positive design.
- Sanjay Ghemawat, Howard Gobioff, and Shun-Tak Leung, [*The Google File System*](https://research.google/pubs/the-google-file-system/), SOSP, 2003. Primary heartbeat, chunk report, placement, re-replication priority, and garbage-collection design.
- Apache Hadoop Project, [*HDFS Architecture*](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html), checked 2026-09-03. Official current heartbeat, block report, rack placement, re-replication, corruption, and safe-mode overview.
- Ceph Foundation, [*Configuring Monitor/OSD Interaction*](https://docs.ceph.com/en/latest/rados/configuration/mon-osd-interaction/), checked 2026-09-03. Official current OSD heartbeat, peer reporter, grace, and monitor map behavior.
- Ceph Foundation, [*Troubleshooting OSDs*](https://docs.ceph.com/en/latest/rados/troubleshooting/troubleshooting-osd/), checked 2026-09-03. Official current down/out, flapping, full/backfill-full, topology, and cascading-load operational guidance.
- Ceph Foundation, [*Monitoring OSDs and Placement Groups*](https://docs.ceph.com/en/latest/rados/operations/monitoring-osd-pg/), checked 2026-09-03. Official current peering, active/clean/degraded, recovery, missing/unfound, and authoritative history states.
- Ceph Foundation, [*Backfill Reservation*](https://docs.ceph.com/en/latest/dev/osd_internals/backfill_reservation/), checked 2026-09-03. Official incoming/outgoing recovery reservation and thundering-herd control design.
- Byung-Gon Chun et al., [*Efficient Replica Maintenance for Distributed Storage Systems*](https://research.google/pubs/efficient-replica-maintenance-for-distributed-storage-systems/), NSDI, 2006. Primary repair-rate, placement, transient failure, and replica-maintenance research.
- Bianca Schroeder, Sotirios Damouras, and Phillipa Gill, [*Understanding Latent Sector Errors and How to Protect Against Them*](https://www.usenix.org/conference/fast-10/understanding-latent-sector-errors-and-how-protect-against-them), FAST, 2010. Primary latent-error prevalence and protection analysis.

## Exercises

### Exercise 1

Calculate the simple modeled exposure for 20-second detection, 10-minute grace, 2 TiB repair at 128 MiB/s, 90-second queue delay, and 30-second verification/registration. State omitted risks.

### Exercise 2

Design a report protocol that safely combines periodic full inventories with incremental changes across node restart, duplicated/reordered messages, and controller failover.

### Exercise 3

Rank these repairs: a triple-replicated 10-TiB object with two valid same-rack copies; a `10+4` stripe with ten valid fragments; a four-copy cache with three valid domains; and a corrupt single replica whose backup is offline. State assumptions.

### Exercise 4

Design a safe workflow for planned decommission of a 500-TiB storage node while foreground latency objectives remain active.

### Exercise 5

Specify failure-detection and repair evidence plus named review for an irreplaceable regulated archive under rack loss, latent corruption, and returning media.

## Answers to the Exercises

### Answer 1

Two TiB is 2,097,152 MiB, so ideal transfer time at 128 MiB/s is 16,384 seconds. Total modeled exposure is `20+600+90+16384+30=17,124` seconds, or 285.4 minutes (4.757 hours), measured from the stated last-evidence/detection origin. Omitted terms include loss before last evidence, source/coded read amplification, contention, retries, tail skew, target reservation, checksum CPU, metadata failover, new failures, topology constraints, and foreground throttling.

### Answer 2

Give each storage process stable node/device IDs plus a new incarnation ID after restart. A full report has report ID, membership/map epoch, baseline sequence, start/end framing, checksums, and declared completeness; apply it only after the complete validated report arrives. Incrementals carry incarnation, monotonically ordered sequence, object/generation/action, and deduplication identity. Buffer or request replay across gaps; never treat later messages as proving an omitted interval. Controller failover recovers the last committed baseline and incremental position. Reject older incarnations/epochs, reconcile every reported copy against authoritative namespace/version/integrity state, and require a new full baseline when continuity cannot be proven.

### Answer 3

Assuming the corrupt singleton has no other current recovery information, it is already irrecoverable from ordinary storage and needs immediate escalation to backup/forensics rather than normal repair. The `10+4` stripe at exactly ten valid fragments has zero count margin and is the highest ordinarily repairable item. The triple-replicated object has two copies but only one rack domain, so rack risk is severe; place a verified replacement in another rack, with size affecting completion. The cache has three valid domains and likely lower consequence, so it follows. Exact order can change with data consequence, backup quality, active hazards, source integrity, and deadlines.

### Answer 4

Mark the node draining so new placements avoid it; bind a decommission operation and inventory baseline; compute every live/snapshot object's verified protection and destination domain needs; reserve distributed target capacity; and schedule highest-risk moves with per-source/target/domain byte and concurrency limits. Keep foreground latency/error feedback and a completion deadline, adapting rates without oscillation. Verify and register each replacement before marking its source copy cleanup-eligible. Reconcile writes and snapshots during the drain, handle stuck writers and full domains, scrub questionable sources, and checkpoint progress for retry. Declare decommission complete only when policy is satisfied elsewhere and audit/retention permits source removal; then secure-erase or retire media with evidence.

### Answer 5

Define detector observers and domains, suspicion/down/out authority, outage thresholds, map/incarnation epochs, and safe-mode criteria. Maintain complete signed/authenticated inventories of archive versions, replicas/fragments, checksums, scrub age, racks, keys, snapshots, and holds. Inject rack partition/loss, slow observers, controller restart, multiple latent corruptions, target-full conditions, repair overload, and old media return. Repair from verified compatible sources into eligible residency/key domains, compare reconstructed end-to-end fixity, register before cleanup, quarantine disagreement, and prove disaster restore with metadata and keys. Record exposure by protection margin and retain tamper-evident decisions. Named review includes archive/data owners, records/legal/privacy, security/key management, storage/network operators, disaster recovery, accessibility, affected-community or research-ethics representatives where applicable, and independent assurance. Internal repair success is not regulatory or archival certification.
