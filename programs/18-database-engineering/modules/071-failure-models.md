---
module_id: DBE-071
program: Database Engineering
level: 2
module_number: 71
title: Failure Models
status: complete
last_verified: 2026-08-30
---

# Failure Models

## One-Page Review

### Governing question

Which faults, errors, failures, dependencies, correlations, timing assumptions, and recovery boundaries must a database name before its correctness, durability, availability, replication, backup, or disaster-recovery claims are meaningful?

### Essential definitions

A **fault** is an hypothesized cause such as a bug, bit flip, power loss, operator action, or malicious input. An **error** is incorrect internal state produced by an activated fault. A **failure** is externally observable deviation from the service contract. A **failure model** bounds which component behaviors and combinations a mechanism promises to handle. **Fail-stop** means a failed component halts and its halt is reliably detectable; **crash-stop** means it halts permanently but detection may be uncertain; **crash-recovery** allows restart with specified stable state. **Omission**, **timing**, **partition**, **corruption**, and **Byzantine** failures describe lost actions/messages, late/early behavior, communication separation, altered data/state, and arbitrary behavior. A **failure domain** is a set of components sharing a plausible cause. **RPO** bounds acceptable committed-data loss in time or logical position; **RTO** bounds restoration time. A **failure detector** outputs suspicions, not knowledge, under asynchronous timing.

### Central model, mechanism, or theorem

Every guarantee has the form:

\[
G = (boundary, assumptions, admitted faults, maximum concurrency/correlation,
detection, response, recovery objective, evidence).
\]

Mechanism sufficiency is conditional: redundancy tolerates only the failures outside its shared fate and within its voting/reconstruction assumptions; WAL protects only if ordering, persistence, integrity, and recovery premises hold; timeout-based detection trades completeness against false suspicion. In a fully asynchronous message-passing model, Fischer, Lynch, and Paterson show that deterministic consensus cannot guarantee termination with even one crash failure. Practical systems make additional timing, randomness, quorum, or failure-detector assumptions.

### Critical invariants

- Name the protected service and observable guarantee before listing machines or mechanisms.
- Separate fault, activation, internal error, external failure, detection, containment, repair, and restoration.
- Bind every claim to process, host/OS, power, storage, network, zone/region, dependency/control plane, operator, software/configuration, and adversarial boundaries.
- State whether faults are independent, correlated, cascading, latent, intermittent, permanent, or concurrent; never multiply probabilities without defending independence.
- A timeout establishes suspicion under a timing model, not proof that a peer crashed.
- Successful write/flush/replication acknowledgements mean only what the complete OS/filesystem/controller/device/protocol contract guarantees.
- Redundancy is not backup; backup existence is not recoverability; recovery success is not restored semantic correctness.
- Test named fault/cut-point combinations and authoritative invariants, including failures during recovery.
- Preserve safety under exceeded assumptions; when liveness cannot be guaranteed, fail closed or degrade according to explicit policy rather than inventing certainty.

### Common failures

Failures include saying “node failure” without defining process, OS, power, disk, network, or state; treating kill, reboot, power cut, and media loss as equivalent; assuming fail-stop hardware; trusting timeouts as perfect detectors; assuming replicas in one domain are independent; calculating availability from component MTTF alone; treating RAID as backup; treating a WAL write as durable without flush/order semantics; ignoring torn, lost, misdirected, reordered, stale, or falsely acknowledged writes; restoring the same corruption to every copy; omitting operator/configuration/control-plane failures; testing only steady-state faults; and claiming an RPO/RTO from architecture diagrams rather than restore evidence.

### Compact example

Three independent replicas with per-replica failure probability 0.01 lose a majority with probability (3(.01)^2(.99)+(.01)^3=0.000298). Add a shared-domain outage probability 0.005 and the modeled unavailability becomes (0.005+0.995(0.000298)=0.00529651), 17.77 times larger. With 100 independent drives each failing with probability .001, at least one fails with probability (1-.999^{100}=0.095208). A detector with 9 true detections, 1 miss, and 6 false suspicions has precision .600 and recall .900. The arithmetic demonstrates why correlation and detection errors matter; its independence assumptions are not field evidence.

### Connections

Retrieve [Life of a Transactional Write](010-life-of-a-transactional-write.md), [Dirty Pages and Writeback](028-dirty-pages-and-writeback.md), [Checksums and Page Corruption](029-checksums-and-page-corruption.md), and [Adaptive Query Processing](069-adaptive-query-processing.md). Continue through [the roadmap](../ROADMAP.md) to WAL, LSNs, undo/redo, checkpoints, ARIES, group commit, crash recovery, backups, and verified point-in-time restore.

## Governing Question

“The database survives failures” is not a testable claim. Which database service—accepted commits, authorized reads, transaction atomicity, ordering, availability, bounded staleness, backup recovery—is protected? Which failures occur, where, for how long, in which combinations, and with what detectability? What state survives? What must the system do while uncertain? How much data/time may be lost? Which evidence demonstrates the claim?

A failure model answers those questions narrowly enough that an algorithm can be proved and a system can be tested. It is not a catalog of disasters. It is the environment side of a contract. If the environment exceeds the model, safety might still be preserved, service may halt, or behavior may be undefined; engineers must not silently extrapolate.

## Why This Matters

Recovery algorithms derive their correctness from assumptions below the database. Write-ahead logging requires log records to reach a defined stable boundary before dependent page changes and commit acknowledgement. Checksums assume protected identity and coverage. Replication assumes something about message loss/reordering, replica failures, quorum membership, and shared fate. Backups assume readable, complete, authorized copies outside the destroying event. Each mechanism can pass ordinary tests while its unstated premise is false.

Failures also compose. A disk fails during RAID rebuild and exposes a latent sector error. A regional outage removes the primary and the credential/control plane needed to promote the remote replica. A timeout suspects a slow leader, and two sides accept writes without fencing. An operator deletes data, replication faithfully deletes every online copy, and the backup catalog shares the same credentials. A recovery routine crashes midway or repeats a non-idempotent action. The useful model includes correlations, cascades, latent faults, and recovery itself.

Jim Gray's 1985 field analysis separated hardware, software, operations, environment, and unknown causes and emphasized repair/recovery structure. Schneider's fail-stop work formalized a useful abstraction precisely because ordinary components do not automatically fail that way. FLP and Chandra–Toueg show why asynchronous failure detection and agreement need explicit extra assumptions. Storage field studies show whole-device failure is not the only mode: latent sectors and silent corruption are real categories. These durable lessons prevent the comforting but invalid shortcut “we have replicas, therefore we are safe.”

## Prerequisites and Retrieval

Retrieve these concepts:

- database boundaries: transaction, commit acknowledgement, snapshot, page, WAL record, checkpoint, replica, backup, and restore;
- safety means nothing bad happens; liveness means something good eventually happens;
- atomicity, consistency, isolation, and durability protect different properties;
- checksums detect covered corruption but do not normally repair it;
- replication copies state and operations, including bad ones, unless independent recovery history exists;
- a quorum argument needs membership, intersection, state persistence, and fencing assumptions;
- probability multiplication requires independence, while real infrastructure has shared dependencies;
- monitoring is sampled evidence and a timeout is a timing judgment.

This module establishes assumptions. Later modules derive logging and recovery mechanisms within them.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish fault, error, failure, detector suspicion, containment, repair, and recovery;
2. specify crash-stop, crash-recovery, omission, timing, partition, corruption, and Byzantine models;
3. map database guarantees across process, machine, storage, network, region, dependency, operator, and adversarial boundaries;
4. reason about independence, correlation, quorum loss, latent faults, RPO/RTO, and detector errors;
5. identify when WAL, replication, checksums, RAID, backup, or fencing assumptions are insufficient;
6. design a failure/cut-point matrix with invariant, liveness, and recovery oracles;
7. validate and operate a failure model without overstating simulation, fault injection, or restore evidence.

## Core Exposition

**Begin with service failure, then work inward.** A failure is observed at a boundary: an acknowledged commit disappears after restart; a read violates the declared consistency model; an authorized request cannot complete within its availability target; a restore exceeds RTO; a page returns unauthenticated bytes. Starting from “disk failure” prematurely chooses a cause. Start with the externally promised behavior, then trace internal erroneous state and activating faults.

The fault–error–failure chain is not one-to-one. A latent bit flip is a fault whose error remains dormant until read. Redundant state can mask an error so no service failure occurs. One configuration fault can activate across every replica. A network delay can trigger an inaccurate suspicion, which triggers unsafe promotion, which creates divergent writes. Detection and response are part of the causal chain.

**Specify dimensions, not one label.** For each fault state:

- **location/boundary:** thread/process, kernel, host, power supply, controller, device/sector, rack/zone/region, network path, clock, dependency/control plane, human/operator, software/configuration, credential/security boundary;
- **behavior:** stop, restart, omission, duplication, reordering, delay, partial response, corruption, stale/rollback state, equivocation/arbitrary action;
- **duration:** transient, intermittent, permanent, latent until access, recurring;
- **detectability:** explicit error, checksum mismatch, timeout suspicion, delayed audit, silent;
- **scope/correlation:** one component, k simultaneous, common-mode domain, cascade, adversarial coordination;
- **state after recovery:** empty, last durable prefix, possibly stale snapshot, corrupted, duplicated effects, unknown;
- **response:** retry, fence, failover, reconstruct, quarantine, degrade, stop, restore, escalate;
- **objective/evidence:** safety invariant, availability bound, RPO/RTO, test/monitor/restore proof.

“One node may crash” is incomplete until node, crash, persistence, detection, restart, network, concurrency, and service behavior are defined.

**Distinguish stop models.** In **fail-stop**, other participants reliably learn a component has failed and it stops producing effects. This is a designed abstraction, often implemented with replication, detection, and fencing, not a natural property of commodity hardware. In **crash-stop**, a process halts permanently but peers may not distinguish it from delay. In **crash-recovery**, it returns; define which memory, local disk, identity, epoch, locks/leases, and messages survive.

A process kill leaves kernel/filesystem/device caches and the host running. An OS crash loses volatile kernel state. A power cut tests controller/device power-loss behavior. Device loss removes media. Zone loss may remove power/network/control plane together. Replacing these with `kill -9` covers one narrow model.

**Model communication behavior.** Channels can lose, duplicate, reorder, delay, corrupt, or partition messages. Retries convert loss into duplication unless requests carry stable identity and deduplication state. TCP supplies an ordered byte stream per live connection, not exactly-once application operations across reconnects. A response lost after commit creates an ambiguous outcome: the client does not know whether retry should reapply the transaction.

Partitions are communication failures, not necessarily clean cuts; connectivity can be asymmetric or partial. A node isolated from peers may still serve clients or storage. Safety requires membership/lease/epoch fencing so old actors cannot continue mutating authoritative state after replacement. Clocks can stop, jump, drift, or be merely delayed observations; leases require explicit bounded-skew/delay premises.

**Timeouts are failure detectors.** In an asynchronous system, a slow process and a failed process are indistinguishable from silence alone. FLP proves a termination impossibility for deterministic consensus in its fully asynchronous model with one crash fault; it does not say practical consensus is impossible. Practical protocols use partial synchrony/eventual timing, randomized progress, quorums, stable storage, leaders, or failure-detector assumptions.

Chandra and Toueg characterize detectors by completeness and accuracy. Operationally, shorter timeouts improve detection latency/recall during genuine failures but increase false suspicions under pauses, queueing, packet loss, overload, or long tails. Evaluate confusion matrices by region/resource class and the consequence of each error. Fencing can make a false suspicion safe but still costly; without fencing, a false promotion can violate safety.

**Classify storage failures end to end.** A storage operation can fail explicitly, be lost, be only partially/torn, be misdirected to the wrong address, reorder across a required barrier, return stale data, corrupt data silently, or acknowledge volatile state as durable. Media may become unreadable only when a latent sector is accessed. Capacity exhaustion, permission change, filesystem bugs, controller firmware, DMA/memory corruption, cables, and cloud-volume control planes belong to the path.

SQLite's atomic-commit documentation makes pessimistic filesystem/device assumptions explicit. PostgreSQL 18 documents that `fsync`/equivalent methods, `wal_sync_method`, `synchronous_commit`, and full-page writes establish different recovery properties; it warns that disabling `fsync` or full-page writes risks corruption and that asynchronous commit can lose recent acknowledged work while retaining database consistency. These are scoped product contracts, not proof that every storage stack honors flushes.

WAL requires more than “append a record”: integrity/identity, atomic or recoverable record boundaries, log-before-data ordering, durable commit prefix, detection of partial/corrupt tails, and idempotent recovery. A device that lies about flush or reorders writes beyond the assumed interface can defeat the proof. Qualification needs power-cut testing on the actual stack, not faith in an API name.

**Separate detected from silent corruption.** Checksums transform some silent corruptions into detected failures. Coverage must include bytes plus object/address/generation/algorithm context to catch misdirection and stale images. Collision probability, unprotected metadata, corrupted checksum fields, memory-before-check, and malicious changes bound the guarantee. On mismatch, quarantine and recover from an independently verified source; “choose any readable replica” can propagate corrupt but well-formed state.

Bairavasundaram and colleagues found latent sector errors in a large production drive population and separately studied storage-stack corruption. Their empirical distributions are evidence for those populations and eras, not universal current rates. The durable lesson is categorical: whole-disk fail-stop models omit sector-level, latent, silent, and correlated error modes, so scrubbing and end-to-end integrity matter.

**Reason about redundancy and shared fate.** Replication tolerates a bounded number/type of replica failures only if copies and the mechanisms selecting them do not share the same fault. Three VMs on one power domain do not tolerate its outage. Cross-region replicas may still share credentials, software deployment, schema migration, operator automation, DNS/control plane, account, key management, or logical corruption.

Quorum safety relies on intersection plus durable state and correct membership/epoch rules. Availability requires enough reachable eligible replicas. Byzantine tolerance needs stronger voting/authentication assumptions and replica counts than crash tolerance. RAID reconstructs device data under its layout/fault premises but does not provide historical recovery from deletion, ransomware, software corruption, or site loss. Online replicas and RAID are availability/integrity mechanisms; backups provide an independent recovery history only if isolation and restoration work.

Do not multiply component reliabilities blindly. Independence is a modeling claim. Condition on failure domains or use a common-cause mixture. The executable shows a 0.5% shared-domain event dominating an otherwise small independent majority-loss probability. More components can increase the chance that at least one component needs repair even when redundancy improves service availability.

**Model software, configuration, and human faults.** Deterministic bugs reproduce on every replica receiving the same input. Nondeterministic races can evade ordinary tests. A bad rollout, expired certificate, destructive migration, privilege change, capacity limit, or automation loop can disable all supposedly independent copies. Gray distinguished software and operations as material sources of outages; modern systems add global control planes and rapid fleet automation.

Treat operator action neither as blame nor as unmodelable. Design approvals, least privilege, staged rollout, rate/impact limits, immutable audit, two-person controls for irreversible actions, protected recovery credentials, and undo/restore paths. Make safe behavior easier than dangerous behavior. Adversarial faults add intent, credential compromise, equivocation, anti-forensics, and targeted correlation; ordinary checksums and replicas do not constitute a security model.

**Define durability and availability precisely.** A commit acknowledgement may promise survival of process crash, host/OS crash, power loss, one device loss, one zone loss, or regional disaster—each is different. It may wait for local durable WAL, remote receipt, remote durable flush, remote apply, or quorum commit. PostgreSQL 18's `synchronous_commit` modes illustrate that acknowledgement points can distinguish local durability, standby write/flush/apply, and different crash boundaries.

RPO is not “we back up daily” unless the latest restorable consistent point is demonstrated. Express RPO in time and, where possible, log/transaction position. RTO begins at a declared event/detection point and ends when a declared service and correctness verification are restored, not merely when a VM boots. Availability needs a measurement boundary, exclusions, latency/error threshold, and error budget. A 99.95% 30-day availability target permits 21.6 minutes under a simple continuous-time budget, but it does not specify allowed data loss.

**Design a failure matrix.** Rows are named cut points: before log creation; after log append but before flush; after durable commit before response; during page write; during checkpoint; during replica acknowledgement; during backup; during restore; during recovery redo/undo; after promotion before old-primary fencing. Columns are process kill, OS crash, power cut, lost/torn/misdirected/corrupt write, ENOSPC, path loss, delayed/duplicate/reordered message, partition, clock jump, worker/coordinator loss, operator/config rollout, credential/control-plane failure, and simultaneous/correlated faults.

Each cell declares applicability, injection method/fidelity, expected safety state, liveness/recovery objective, oracle, cleanup, and retained evidence. Not every Cartesian cell is meaningful, but omission must be reasoned. Test failures during error handling and recovery, because these paths mutate authoritative state under stress.

The executable below evaluates a finite probability and detector model. Independence is an explicit hypothetical assumption, not a measured claim.

<!-- bijux-verify: {"id":"finite-failure-model-arithmetic","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"replicas=3\nindependent_node_failure_probability=0.010000\nindependent_quorum_unavailable=0.000298\ncorrelated_domain_failure=0.005000\ncombined_unavailable=0.005297\ncorrelation_multiplier=17.77\nhundred_drive_any_failure=0.095208\nfailure_detector_precision=0.600\nfailure_detector_recall=0.900\nfalse_positive_rate=0.067\nfalse_negative_rate=0.100\nmonthly_error_budget_minutes=21.60\nfault_injection_cases=90\ntimeout_is_suspicion=true\nrestore_verification_required=true\nindependence_is_assumption=true\nevidence=finite_failure_model\n","stderr":""}} -->
```python
from math import comb

replicas = 3
node_failure = 0.01
quorum_unavailable = sum(
    comb(replicas, failed)
    * node_failure**failed
    * (1 - node_failure) ** (replicas - failed)
    for failed in range(2, replicas + 1)
)

domain_failure = 0.005
combined_unavailable = domain_failure + (1 - domain_failure) * quorum_unavailable

drives = 100
drive_failure = 0.001
any_drive_failure = 1 - (1 - drive_failure) ** drives

true_positive = 9
false_negative = 1
false_positive = 6
true_negative = 84
precision = true_positive / (true_positive + false_positive)
recall = true_positive / (true_positive + false_negative)
false_positive_rate = false_positive / (false_positive + true_negative)
false_negative_rate = false_negative / (true_positive + false_negative)

availability_target = 0.9995
minutes_in_30_days = 30 * 24 * 60
error_budget_minutes = (1 - availability_target) * minutes_in_30_days

cut_points = 10
fault_classes = 9

print(f"replicas={replicas}")
print(f"independent_node_failure_probability={node_failure:.6f}")
print(f"independent_quorum_unavailable={quorum_unavailable:.6f}")
print(f"correlated_domain_failure={domain_failure:.6f}")
print(f"combined_unavailable={combined_unavailable:.6f}")
print(f"correlation_multiplier={combined_unavailable / quorum_unavailable:.2f}")
print(f"hundred_drive_any_failure={any_drive_failure:.6f}")
print(f"failure_detector_precision={precision:.3f}")
print(f"failure_detector_recall={recall:.3f}")
print(f"false_positive_rate={false_positive_rate:.3f}")
print(f"false_negative_rate={false_negative_rate:.3f}")
print(f"monthly_error_budget_minutes={error_budget_minutes:.2f}")
print(f"fault_injection_cases={cut_points * fault_classes}")
print("timeout_is_suspicion=true")
print("restore_verification_required=true")
print("independence_is_assumption=true")
print("evidence=finite_failure_model")
```

**Build layered evidence.** Static analysis/model checking covers finite protocol/state invariants under an exact model. Unit/property tests cover local error handling. Deterministic simulation explores schedules and faults reproducibly; FoundationDB documents simulation as a central testing technique, but simulated components and distributions bound its claim. Fault injection exercises real binaries/interfaces. Power-cut and storage fault tests validate persistence assumptions. Backup restore and regional game days validate operational dependencies. Production incidents reveal unmodeled combinations but are uncontrolled and ethically cannot be the primary experiment.

Use an authoritative oracle: committed transaction ledger, invariants over balances/keys, snapshot consistency, log/page checksums, replica convergence after fencing, no duplicate external effects, RPO position, RTO timeline, and authorization. Merely restarting successfully is not proof; silent loss/corruption can remain.

**Observe and revise the model.** Record attempt/epoch, injected or observed fault, detector suspicion and confidence, component/domain topology, commit/log positions, acknowledgements, error codes, checksum/corruption location, fencing/membership, recovery action, invariant results, RPO/RTO, and residual uncertainty. Redact protected data and secure fault-injection controls.

Near misses, false suspicions, latent errors found by scrub, restore failures, and correlated incidents update the failure model. Version it with architecture, hardware/firmware, filesystem, cloud service, topology, dependencies, software, and operational controls. A model that never changes despite incidents is probably ceremonial.

**Productionize degradation and recovery.** State behavior when assumptions are exceeded: reject writes, serve bounded-stale reads, enter read-only mode, isolate a tenant/shard, require operator approval, or stop. Prefer detectable unavailability over silent divergence when safety cannot be established. Provide immutable break-glass records, protected recovery credentials, communication/escalation, and customer-visible semantics.

Canary changes to logging, persistence, replication, detector thresholds, membership, backup, or recovery. Gate correctness, durability acknowledgements, detector false positives/negatives, failover time, error budget, RPO/RTO, resource cost, and recovery under secondary faults. Preserve rollback only if rollback itself is compatible with written formats and protocol epochs.

## Definitions and Notation

- **Fault / error / failure**: cause, erroneous internal state, and observable contract deviation.
- **Fault activation**: event that makes a dormant fault produce an error.
- **Failure model M**: bounded set of admitted behaviors, combinations, timing, and recovery assumptions.
- **Safety / liveness**: nothing forbidden occurs / a required outcome eventually occurs.
- **Fail-stop / crash-stop / crash-recovery**: reliably detected halt / permanent uncertain halt / restart with specified surviving state.
- **Omission / timing / partition**: absent action/message / behavior outside timing bounds / lost connectivity among subsets.
- **Corruption / Byzantine failure**: altered state/data / arbitrary potentially inconsistent behavior.
- **Failure detector**: module producing suspicions with declared completeness and accuracy properties.
- **Failure domain**: components sharing a plausible cause or control dependency.
- **Common-mode/correlated fault**: one cause or dependency affects multiple nominal copies.
- **Latent fault/error**: present but not yet detected or activated at the service boundary.
- **RPO / RTO**: maximum acceptable recovery-point loss / maximum acceptable restoration time.
- **Fencing**: mechanism preventing an obsolete actor from continuing authoritative effects.
- **Scrubbing**: proactive read/verification intended to surface latent corruption.
- **Error budget**: permitted service failure under a defined SLO window; not a durability-loss allowance.

A “fault-tolerant” system tolerates only the faults and combinations in its declared model while meeting specified properties.

## Mechanisms, Invariants, or Proof Structure

**Guarantee implication.** For implementation I and environment trace t, a claimed guarantee is conditional: if `t ∈ M` and implementation assumptions A hold, then observable history satisfies G. Testing traces outside M is valuable robustness evidence but cannot retroactively expand the proof. An exceeded model should have defined safe degradation.

**Independent quorum calculation.** For three identical independent replicas failing with probability p during a window, majority loss is `C(3,2)p²(1-p)+p³`. This follows by summing mutually exclusive exactly-two and exactly-three failure cases. It is invalid for a shared-domain event unless conditioned on that event. A mixture adds domain loss then independent residual loss only when those conditional assumptions are stated.

**At-least-one calculation.** For n independent components each avoiding failure with probability `1-p`, all avoid failure with `(1-p)^n`; complement gives `1-(1-p)^n`. It estimates repair exposure, not service unavailability under redundancy, and fails under correlation or unequal probabilities.

**Detector confusion matrix.** Precision `TP/(TP+FP)` answers how often suspicion is correct; recall/completeness sample `TP/(TP+FN)` answers how many observed crashes are detected. False-positive rate `FP/(FP+TN)` measures healthy cases falsely suspected. These empirical rates depend on workload, timing, labels, censoring, and class distribution; they do not establish formal eventual properties.

**WAL conditional proof shape.** If every committed transaction's complete log prefix is durable; log records precede dependent data writes; corrupt/partial log tails are detected; and redo/undo is correct/idempotent under the page/log identity model, recovery can reconstruct the promised state after admitted crashes. A lying flush, unprotected misdirection, lost required log, or recovery bug violates a premise.

**Quorum/fencing shape.** Majority intersection prevents two disjoint majorities within one fixed membership, but safe leadership also needs durable votes/terms, current membership, state/log rules, and fencing of obsolete actors. Network reachability plus vote count alone is insufficient.

**Evidence separation.** Probability arithmetic validates a hypothetical model. Field studies characterize sampled populations. Simulation covers encoded components/schedules. Injection covers selected real interfaces. Restore exercises cover one retained recovery chain. None alone proves future independence, all correlated disasters, adversarial security, universal durability, or recovery fitness.

## Alternatives and Trade-Offs

**Fail-stop models** enable simple protocols but require detection/fencing machinery. **Crash-recovery models** match operations better but add persistent epochs, replay, duplicate effects, and recovery races. **Byzantine models** tolerate arbitrary faults at higher replica, protocol, cryptographic, latency, and operational cost; they still do not cover compromised clients or every shared dependency automatically.

**Synchronous timing** makes deadlines and detectors stronger but may sacrifice availability outside bounds. **Asynchronous safety** tolerates unpredictable delay but cannot guarantee deterministic consensus termination under FLP's model. **Partial synchrony** reflects eventual operational bounds but requires careful timeout/backoff and preserves uncertainty before stabilization.

**Replication** improves availability and can reduce RPO; it rapidly copies logical corruption and shares software/control faults. **RAID/erasure coding** handles specified device loss efficiently; rebuild exposes latent errors and it lacks history. **Backups** provide history/isolation; restore is slower and copies can be stale, corrupt, inaccessible, or untested. Layer them under distinct domains.

**Synchronous durability** reduces acknowledged-loss windows but adds latency and dependency coupling. **Asynchronous commit/replication** improves latency/availability while accepting explicit RPO. **Checksums** detect covered corruption at CPU/space/read cost; **scrubbing** reduces detection latency but consumes I/O and can trigger recovery load.

**Fast failure detection** reduces failover time but increases false suspicion under tail latency. **Conservative detection** avoids churn but delays recovery. Fencing decouples some safety from detection accuracy. **Automatic recovery** is fast and repeatable; correlated bad automation spreads harm. Human approval adds judgment and delay/error. Use bounded automation with immutable evidence and rehearsed break-glass paths.

## Failure Modes and Misconceptions

1. “Failure means crash” omits omission, timing, partition, corruption, stale state, and arbitrary behavior.
2. “Kill -9 tests crash safety” covers process death, not OS, power, device-cache, media, or domain loss.
3. “A timeout proves death” silence is ambiguous without timing assumptions.
4. “Fail-stop is how servers fail” it is an abstraction requiring reliable detection and cessation/fencing.
5. “Three replicas tolerate any two failures” quorum, domain, membership, durability, and fault type constrain tolerance.
6. “Different zones are independent” software, credentials, control planes, accounts, regions, and operators may be shared.
7. “RAID is backup” RAID has no independent history against deletion, corruption, compromise, or site loss.
8. “Replication is backup” it faithfully propagates many damaging operations and corruptions.
9. “Successful write means durable” acknowledgement may stop at process, kernel, controller, or volatile cache.
10. “Checksums prevent corruption” they detect covered mismatches probabilistically and need a repair source.
11. “MTTF predicts the next device failure” population averages and component metrics do not predict individual or service events.
12. “Independent availability multiplies” independence must be defended against common cause and cascade.
13. “Recovery started successfully” does not prove semantic invariants, RPO, completeness, or future readability.
14. “RPO is backup frequency” it is the latest verified recoverable consistent point under the named disaster.
15. “RTO ends when infrastructure is up” service correctness, dependencies, validation, and traffic restoration belong to the boundary.
16. “Chaos testing proves resilience” only injected faults, schedules, oracles, environments, and recovery paths were exercised.

## Worked Examples

### Example 1

**Fault–error–failure chain.** A memory bit flips in an unprotected page address (fault), a dirty page is written to the wrong block (error), checksum context detects mismatch on read and quarantines it, so the service returns an explicit unavailable error rather than wrong data (failure). Conclusion: detection changes silent corruption into bounded unavailability but does not repair it.

### Example 2

**Process versus power.** Killing the database after WAL flush leaves kernel/device state intact; cutting power can lose volatile caches and tear a page write. Both restart cleanly in one test does not make them equivalent. Conclusion: fault-injection fidelity must match the claim.

### Example 3

**Ambiguous commit.** Server durably commits, response is lost, client times out and retries. Without idempotency identity, the business operation may occur twice even though each transaction is atomic. Conclusion: omission failure crosses database/API boundaries.

### Example 4

**False suspicion.** A 2-second pause exceeds a 1-second detector timeout; the leader is suspected but still alive. Promotion without fencing allows both leaders to accept writes. Conclusion: detector accuracy is a liveness/operational property; epochs/leases/fencing protect safety.

### Example 5

**Independent quorum model.** Three replicas at independent p=.01 have modeled majority loss .000298. A shared-domain p=.005 raises total to .00529651. Conclusion: small common-mode risk dominates optimistic independent arithmetic.

### Example 6

**Larger repair surface.** One drive has p=.001 failure in a window; 100 independent drives have 9.5208% chance at least one fails. Redundancy may preserve service while repair/rebuild frequency rises. Conclusion: component-event probability is not service unavailability.

### Example 7

**Latent rebuild error.** One RAID member fails; reconstruction reads every sector from survivors and discovers an old unreadable sector. Conclusion: redundancy plus periodic scrubbing and sufficient additional repair information must cover latent/concurrent faults.

### Example 8

**Replicated deletion.** An authorized but mistaken automation deletes a tenant, and synchronous replicas confirm deletion. An immutable separately credentialed backup restores it. Conclusion: replication met availability semantics while historical recovery required another failure domain.

### Example 9

**Recovery failure.** Crash recovery replays a record, crashes before recording completion, and replays it again. A non-idempotent physical action double-applies. Conclusion: test faults during recovery and make redo/undo actions repeatable under page/log state tests.

### Example 10

**RPO/RTO evidence.** Backup policy says hourly, but latest two backups share corrupt catalog metadata; the verified recoverable point is three hours old and credential restoration adds 90 minutes. Conclusion: measured RPO is three hours and RTO includes dependency plus semantic validation, not the nominal schedule.

## Cross-Program Connections

- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md): crashes, cancellation, races, epochs, idempotency, and memory ordering shape local failure behavior.
- [Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md): circuit breakers, retries, bulkheads, state machines, and sagas must declare fault and ambiguity models.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md): checksums, logs, trees, coding, and persistent metadata need corruption and partial-write invariants.
- [Data Engineering](../../19-data-engineering/ROADMAP.md): lineage, replay, checkpointing, duplication, late data, and orchestration failures define pipeline recovery.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md): domains, replication, recovery tiers, ownership, and RPO/RTO translate business impact into system boundaries.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): adversarial faults, compromised credentials, ransomware, integrity, audit, and recovery isolation extend accidental models.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md): timeout ambiguity, idempotency, retries, partial responses, and error semantics expose database failures to clients.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): zones, control planes, rollout, observability, fault injection, game days, and capacity implement failure-domain controls.

## References

1. Jim Gray, [“Why Do Computers Stop and What Can Be Done About It?”](https://www.bitsavers.org/pdf/tandem/technical_reports/TR85-07_Why_Do_Computers_Stop_and_What_Can_Be_Done_About_IT_Jun85.pdf), Tandem Technical Report 85.7, 1985. Foundational field-oriented failure and availability analysis.
2. Fred B. Schneider, [“Byzantine Generals in Action: Implementing Fail-Stop Processors”](https://www.cs.cornell.edu/fbs/publications/FailStop.pdf), *ACM Transactions on Computer Systems* 2(2), 1984. Primary fail-stop abstraction and implementation reasoning.
3. Michael J. Fischer, Nancy A. Lynch, and Michael S. Paterson, [“Impossibility of Distributed Consensus with One Faulty Process”](https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf), *JACM* 32(2), 1985. Primary asynchronous consensus nontermination result.
4. Tushar Deepak Chandra and Sam Toueg, [“Unreliable Failure Detectors for Reliable Distributed Systems”](https://www.cs.cornell.edu/courses/cs734/2000FA/cached%20papers/ct96.pdf), *JACM* 43(2), 1996. Primary completeness/accuracy failure-detector framework.
5. David A. Patterson, Garth Gibson, and Randy H. Katz, [“A Case for Redundant Arrays of Inexpensive Disks (RAID)”](https://doi.org/10.1145/50202.50214), *SIGMOD 1988*. Foundational storage redundancy taxonomy and assumptions.
6. Lakshmi N. Bairavasundaram et al., [“An Analysis of Latent Sector Errors in Disk Drives”](https://research.cs.wisc.edu/adsl/Publications/latent-sigmetrics07.pdf), *SIGMETRICS 2007*. Primary large-scale field study of latent sector errors.
7. SQLite Project, [Atomic Commit in SQLite](https://www.sqlite.org/atomiccommit.html), retrieved 2026-08-30. Current explicit filesystem/storage assumptions and power-loss commit protocol.
8. PostgreSQL Global Development Group, [PostgreSQL 18: Reliability and the Write-Ahead Log](https://www.postgresql.org/docs/18/wal.html), retrieved 2026-08-30. Current WAL, checksums, asynchronous commit, configuration, and reliability scope.
9. PostgreSQL Global Development Group, [PostgreSQL 18: Write-Ahead Log Configuration](https://www.postgresql.org/docs/18/runtime-config-wal.html), retrieved 2026-08-30. Current fsync, synchronous-commit, WAL synchronization, full-page-write, and crash-boundary behavior.
10. Google, [Site Reliability Engineering: Data Integrity—What You Read Is What You Wrote](https://sre.google/sre-book/data-integrity/), retrieved 2026-08-30. Operational data-integrity, correlated loss, backup, and recovery lessons.
11. Google, [Site Reliability Engineering: Managing Critical State—Distributed Consensus](https://sre.google/sre-book/managing-critical-state/), retrieved 2026-08-30. Operational consensus, quorum, latency, failure-domain, and replica-placement reasoning.
12. Qizhong Zhou et al., [“FoundationDB: A Distributed Unbundled Transactional Key Value Store”](https://www.foundationdb.org/files/fdb-paper.pdf), *SIGMOD 2021*. Primary architecture and deterministic simulation-testing account.
13. NIST, [SP 800-34 Rev. 1: Contingency Planning Guide for Federal Information Systems](https://doi.org/10.6028/NIST.SP.800-34r1), 2010. Authoritative contingency, business-impact, recovery-strategy, testing, and plan-maintenance framework.

## Exercises

### Exercise 1

For an acknowledged database commit, define fault, error, failure, fail-stop, crash-stop, crash-recovery, omission, timing, partition, corruption, Byzantine behavior, failure domain, RPO, RTO, and fencing.

### Exercise 2

Recompute every executable value. Derive the independent majority-loss and common-domain mixture formulas, detector metrics, and error budget; state why none is a field reliability claim.

### Exercise 3

A three-zone database acknowledges after one local flush and one remote receipt. Analyze process crash, remote OS crash, regional power loss, partition, false suspicion, stale leader, lying flush, lost response, and simultaneous latent corruption. State the actual durability and availability boundaries.

### Exercise 4

Design a failure/cut-point test matrix for WAL commit, page flushing, checkpoint, failover, backup, restore, and recovery. Include exact oracles, secondary failures, reproducibility, security, evidence, and limits.

### Exercise 5

Design an elite production failure-model governance and rollout system for a multi-tenant database spanning zones and regions, including dependencies, correlated/operator/adversarial faults, RPO/RTO, drills, canaries, degradation, and model revision.

## Answers to the Exercises

### Answer 1

The fault is a cause such as process bug, power cut, packet loss, misconfiguration, or malicious action. The error is internal incorrect state—missing durable log, divergent term, corrupted page, duplicated request. Failure is observable deviation: acknowledged commit lost, wrong/unauthorized read, unavailable service, exceeded RTO. Fail-stop halts and is reliably detected; crash-stop halts permanently without perfect detection; crash-recovery restarts with explicitly surviving stable state. Omission loses an action/message; timing violates a bound; partition prevents subsets communicating; corruption alters bytes/state; Byzantine behavior is arbitrary, possibly equivocal. A failure domain groups components sharing a cause. RPO bounds latest acceptable lost recoverable history; RTO bounds restoration from a declared start to validated service. Fencing prevents an obsolete actor from continuing authoritative effects. For the commit, every term must name process/host/storage/network/region/security boundaries and the exact acknowledgement semantics.

### Answer 2

Exactly k independent failures among three have probability `C(3,k)p^k(1-p)^(3-k)`. Majority loss sums k=2,3: `3*.01²*.99+.01³=.000298`. If shared-domain failure D=.005 makes the service unavailable and, conditional on no D, residual failures follow the independent model, total is `.005+.995*.000298=.00529651`, displayed .005297; ratio to independent is 17.77. For 100 independent p=.001 drives, none fails with `.999^100`; complement is `.09520785`, displayed .095208.

Detector precision is `9/(9+6)=.600`; recall `9/(9+1)=.900`; false-positive rate `6/(6+84)=.0667`, displayed .067; false-negative rate `1/10=.100`. At target .9995 over 43,200 minutes, budget is `.0005*43200=21.6` minutes. Ten cut points times nine fault classes gives 90 candidate cells before applicability pruning.

All results depend on hypothetical equal independent probabilities, a particular common-cause mixture, correctly labeled sampled detector outcomes, continuous-time SLO arithmetic, and a simple matrix count. They do not measure future hardware, correlation, workload timing, service availability, detector formal properties, RPO, durability, or test coverage.

### Answer 3

“Remote receipt” must be located. If it means remote process/kernel memory rather than durable flush, acknowledgement survives local process/OS/device failure only while the remote volatile state remains and can safely become authoritative; it does not survive simultaneous remote OS/power loss. Local flush protects only if filesystem/controller/device honor ordering/durability and log integrity. A regional power event affecting both placements defeats the two-domain assumption. A partition preserves safety only if quorum/membership rules deny conflicting commits and availability only on a side with sufficient eligible durable state.

A false suspicion cannot authorize two writers: promotion needs durable term/vote and storage/client fencing of the old leader. A stale leader returning cannot reuse its old epoch. A lying local flush invalidates local durability; remote receipt alone may leave acknowledged loss. A lost response after durable commit makes client outcome ambiguous and needs idempotency/status resolution. Latent corruption on the remaining/rebuild source can make nominal redundancy unrecoverable unless checksums, scrubbing, another verified copy, or coding covers the combination.

Thus actual durability is at most the strongest independently recoverable state established before acknowledgement: local durable WAL plus only volatile remote receipt is not remote durable commit. Availability during local loss additionally requires remote promotion, complete log, dependencies, keys/credentials, capacity, and fencing. Document process, OS, power, device, zone/region, network, control-plane, and concurrent-fault boundaries separately; choose synchronous remote flush/apply or quorum if the required RPO demands it, accepting latency/availability coupling.

### Answer 4

Enumerate cut points before log creation, partial/complete append, before/after log flush, before/after commit acknowledgement, before/during/after data-page write, checkpoint record and page flush, replica receipt/flush/apply/ack, promotion/fencing, backup snapshot/copy/catalog publication, restore acquisition/replay/validation, and recovery analysis/redo/undo/completion. Cross applicable process kill, OS crash, power cut, lost/torn/misdirected/reordered/corrupt write, false flush, ENOSPC/path loss, delayed/lost/duplicate/reordered messages, partitions, clock faults, worker/coordinator loss, operator/config/credential faults, and selected simultaneous/latent faults.

For each cell record exact stack/version/topology, injection mechanism and fidelity, deterministic seed/schedule where possible, prestate/workload, expected committed/aborted/unknown ledger, page/log checksums and positions, snapshot/transaction invariants, duplicate external-effect oracle, replica membership/epoch and convergence, expected RPO/RTO, liveness timeout, cleanup, and raw evidence. Inject again during retry, failover, reconstruction, restore, and recovery. Use protected synthetic data and least-privilege authenticated injectors; prevent experiments escaping isolated environments or canary budgets; audit every action.

Compare recovered state to an independent commit-intent/acknowledgement oracle, not “server started.” Verify every acknowledged transaction required by the model, no forbidden partial/uncommitted effect, semantic constraints, authorization, indexes, replica agreement after fencing, and readable restored history. Simulation/model checking, syscall/device injection, real power cut, and regional game day cover different claims. Publish uncovered cells, non-equivalent emulation, sampling, hardware limitations, and no-external-review status.

### Answer 5

Maintain a versioned failure-model registry per service/tenant tier: protected operations and semantics; commit/read/availability contracts; process/host/storage/network/zone/region/control-plane/security boundaries; topology and dependencies including DNS, IAM/KMS, artifacts, telemetry and humans; admitted behaviors, concurrency/correlation, timing/detector assumptions; persistent state, membership/fencing; degradation; RPO/RTO; owner; evidence and expiry. Threat modeling extends accidental faults to compromised credentials, forged/withheld messages, ransomware, insider action, and anti-forensics; recovery credentials/copies require separate administration and immutable audit.

Map each guarantee to mechanisms and proof premises—WAL/order/flush/checksum, quorum/intersection/epochs, redundancy domains, backup history/isolation, restore dependencies—and to tests/metrics. CI runs deterministic simulations and targeted error paths. Hardware qualification runs power-loss/flush/corruption tests. Scheduled restores verify content, log position, dependencies, access, and timed RPO/RTO. Game days cover zone/region/control-plane/operator faults plus secondary recovery failure. Production telemetry measures acknowledgements, durable/applied positions, detector confusion proxies, false promotions, fencing, checksums/scrubs, degraded redundancy, backup age/verification, failover, error budget, RPO/RTO, and unmodeled events without exposing tenant data.

Shadow detector/membership/persistence changes, then canary bounded shards/tenants/domains with correctness, acknowledged-loss, false-suspicion, failover, latency/resource, and fleet gates. Pre-provision kill switches and format/protocol-compatible rollback; reject rollback that cannot read new state. When assumptions are exceeded, preserve safety through fenced read-only/reject/isolate behavior and communicate explicit semantics. Every incident, near miss, scrub discovery, failed restore, dependency change, topology/cloud/firmware/software upgrade, and threat finding triggers model/evidence review. Internal tests remain scoped; named human owners and independent reviewers are required before claiming regulatory, security, or external production assurance.
