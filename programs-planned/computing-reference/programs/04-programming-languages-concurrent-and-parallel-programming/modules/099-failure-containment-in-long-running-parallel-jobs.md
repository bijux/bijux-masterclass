---
module_id: CONPAR-099
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 99
title: Failure Containment in Long-Running Parallel Jobs
status: complete
last_verified: 2026-08-29
---

# Failure Containment in Long-Running Parallel Jobs

## One-Page Review

### Governing question

How can a long-running parallel job detect, contain, and recover from process, node, device, storage, network, data, scheduler, and software failures without duplicating external effects, accepting corrupt state, or claiming availability beyond its tested fault model?

### Essential definitions

- A **fault** is a hypothesized cause; an **error** is an incorrect internal state; a **failure** is externally visible deviation from required service.
- A **failure domain** is a set of components likely to fail together, such as process, node, rack, power zone, filesystem, or control plane.
- A **fail-stop** component halts detectably; **omission**, **timing**, **Byzantine**, and **silent data corruption** faults require different models.
- **containment** prevents an error or failed component from corrupting unrelated state or causing unbounded propagation.
- A **checkpoint** is a validated recovery state plus identity, schema, provenance and commit metadata.
- A **consistent cut** contains no received message whose send lies outside the captured global state.
- **coordinated checkpointing** creates a consistent recovery line across participants; **uncoordinated checkpointing** needs dependency/message logging to avoid inconsistent rollback and domino effects.
- A **determinant** records a nondeterministic event needed to replay an execution after rollback.
- **restart** reconstructs computation from recovery state; **resume** continues within a surviving execution; **recompute** regenerates lost state.
- **RPO** bounds acceptable lost progress/data; **RTO** bounds recovery duration under stated assumptions.
- **idempotency** makes repeated effect attempts equivalent to one accepted effect; **deduplication** rejects repeats using durable identity.
- A **recovery epoch** identifies one lineage after checkpoint/restart and prevents stale messages or outputs from crossing generations.
- **scrubbing** validates stored/computed data before it becomes authoritative.
- A **recovery claim** binds covered fault sets, detection assumptions, redundancy independence, completed tests, observed RPO/RTO, and residual risk.

### Central model, mechanism, or theorem

Recovery correctness requires a committed state `C_k` that is internally valid, globally consistent with communication and external effects, durable across the tolerated failure domains, and readable by the pinned recovery implementation. After a failure set `F`, recovery chooses an intact generation, establishes a new epoch, restores participants and dependencies, reconciles in-flight messages and side effects, validates invariants, and only then republishes output. A simple periodic-checkpoint waste approximation is `w(T)=C/T + T/(2M)`, where `C` is checkpoint cost, `T` useful-work interval, and `M` mean time between modeled failures; its stationary interval `sqrt(2CM)` is an optimization under restrictive assumptions, not a reliability guarantee.

### Critical invariants

The fault model and shared failure domains are explicit; checkpoints capture every correctness-relevant state and schema; commit is atomic and never points to partial data; content digests and semantic invariants are checked; replicas do not share the same claimed fault domain; communication state forms a consistent recovery line or has sufficient determinants; external effects carry durable idempotency keys; epochs fence stale work/messages; detection distinguishes failure from delay within stated limits; retries are bounded; recovery cannot overwrite the last known-good generation; restart uses compatible code/configuration; reconstructed state is validated before output; RPO/RTO are measured under fault injection; original failure evidence remains; and unsupported compound/corruption faults are reported.

### Common failures

Teams checkpoint files but not queues/RNG/configuration, publish a manifest before all shards are durable, place every replica in one rack or filesystem, assume process death is always detected, mistake timeout for proof of failure, restart with a different schema, accept checksummed but semantically wrong data, replay non-idempotent writes, admit stale messages from an old epoch, combine local checkpoints into an inconsistent global state, retain only the newest generation, retry forever, checkpoint so often that jobs miss deadlines, optimize interval from an unjustified MTBF, test only clean shutdown, or call one successful restart “fault tolerant.”

### Compact example

With checkpoint cost `C=4` minutes and modeled mean failure interval `M=720` minutes, the simplified optimum is `sqrt(2CM)=75.895` minutes of useful work. Among allowed intervals 30, 60, 90, 120 and 180 minutes, the model selects 90. Real policy must also include restart cost, failures during checkpoint/recovery, correlated faults, storage capacity, queue limits and the required RPO.

### Connections

[Determinism and Reproducibility](007-determinism-and-reproducibility.md) defines recoverable state. [Point-to-Point Message Passing](082-point-to-point-message-passing.md) supplies message identities. [Multi-Node Scaling](090-scaling-a-parallel-program-across-multiple-nodes.md) defines placement. [Tracing and Profiling Parallel Execution](098-tracing-and-profiling-parallel-execution.md) measures detection and recovery. The [program roadmap](../ROADMAP.md) ends with an integrated correctness, portability, and scale review.

## Governing Question

For which failure sets can the job preserve or reconstruct a consistent, semantically valid, externally reconciled state within required progress-loss and recovery-time bounds, and what evidence demonstrates that claim?

Failure containment is not merely saving memory to disk. It is a protocol across computation, communication, storage, schedulers, external systems, versions, and human operations.

## Why This Matters

As jobs run longer and use more components, the probability that some component fails rises. A week-long computation may lose days if it starts over. Yet a fast restart from an inconsistent or corrupt checkpoint can be worse: it silently publishes invalid scientific, financial, operational, or safety-relevant results.

Parallel state is distributed. A receive may be captured after its message while the sender is captured before sending, duplicating effects after restart. Device work may still be in flight. External databases or object stores may already contain output. Failure detectors cannot perfectly distinguish a dead process from a slow or partitioned one in an asynchronous environment.

Production resilience therefore makes fault assumptions and recovery state explicit, commits generations atomically, fences epochs, validates semantics, protects external effects, and continuously exercises real restart paths. Recovery performance and correctness are separate gates.

## Prerequisites and Retrieval

Retrieve:

- reproducibility, structured lifetimes, messages, nonblocking operations and collectives from [Determinism and Reproducibility](007-determinism-and-reproducibility.md), [Structured Concurrency](037-structured-concurrency.md), [Point-to-Point Message Passing](082-point-to-point-message-passing.md), [Communication–Computation Overlap](086-communication-computation-overlap.md), and [Collective Communication](083-collective-communication.md);
- bulk-synchronous iterations and hybrid/device state from [Bulk-Synchronous and Asynchronous Iterations](089-bulk-synchronous-and-asynchronous-iterations.md) and [Hybrid Threads, SIMD, GPU, and Message Passing](094-hybrid-threads-simd-gpu-and-message-passing.md); and
- verification, systematic faults and trace evidence from [Race Detection and Concurrency Sanitizers](096-race-detection-and-concurrency-sanitizers.md), [Systematic Concurrency Testing](097-systematic-concurrency-testing.md), and [Tracing and Profiling Parallel Execution](098-tracing-and-profiling-parallel-execution.md).

Retrieval prompt: define required outputs/invariants; progress unit; process/node/rack/storage/network/device/scheduler/control-plane domains; fail-stop/omission/timing/corruption/compound fault sets; detection/false-suspicion policy; checkpoint state/schema/version/RNG/communication/device/external effects; coordinated/logged protocol; generation/epoch/commit; checksums and semantic validation; redundancy placement; RPO/RTO/retention; interval model; restart compatibility; retries/escalation; fault-injection matrix; observability; security; runbook; and unsupported conditions.

## Learning Objectives

After completing this module, a learner can:

1. define faults, errors, failures, failure domains, coverage and residual risk;
2. design application/system-level checkpoint state and atomic generation commits;
3. distinguish coordinated, uncoordinated, communication-induced and message-logging recovery;
4. preserve communication, RNG, task, device and external-effect consistency;
5. use epochs, idempotency, deduplication and fencing during restart;
6. derive and critique checkpoint-interval models under explicit assumptions;
7. detect silent corruption with structural, cryptographic and semantic validation;
8. build bounded retry, rollback, restart, fallback and escalation workflows;
9. test RPO/RTO and correctness with representative single/compound fault injection; and
10. review high-stakes recovery evidence without claiming universal fault tolerance.

## Core Exposition

### Define the fault and service model

Start from required service: final output, periodic durable results, streaming availability, interactive control, or scientific progress. Define progress units and authoritative effects. RPO may be zero outputs lost but allow recomputation; RTO may apply to resuming useful work, not merely process launch.

Enumerate failure domains and correlations: worker process, node, GPU, local SSD, top-of-rack switch, rack power, parallel filesystem, metadata service, scheduler, container registry, identity/key service, monitoring, and operator action. Replication across two devices in one node does not tolerate node loss. A checkpoint on the same filesystem as its manifest shares that domain.

Classify faults. Fail-stop is easier than a process that hangs, partitions, emits corrupt data, or continues after being declared failed. Timeouts create suspicions; they do not prove death. Split-brain prevention requires leases, epochs, quorum/fencing, or a job-wide abort/relaunch policy appropriate to the system.

Write a coverage matrix: tolerated single faults, selected correlated/compound faults, maximum simultaneous losses, detection latency, false-positive response, data corruption, recovery resources, and explicitly unsupported Byzantine or regional events. Availability arithmetic is invalid unless independence assumptions hold.

### Define checkpoint completeness

Application-level checkpoints save semantic state: iteration/time step, partitions and ownership, model parameters, optimizer state, RNG algorithm/state/stream mapping, pending tasks, convergence criteria, input offsets, schema/unit/configuration versions, deduplication ledger, external-effect tokens, and provenance. Derived caches may be recomputed if their invalidation is safe.

System-level checkpointing can capture memory, registers and runtime state with less application code, but kernels, networks, GPUs, files, drivers and external resources may be unsupported or nonportable. Application checkpoints are more explicit and versionable but demand careful ownership and reconstruction. Hybrid schemes are common.

Quiesce or capture asynchronous work. Complete/cancel device operations and transfers according to API semantics; settle or log nonblocking messages; freeze task creation; flush required buffers; and establish object generations. A local file being closed does not make a distributed checkpoint globally consistent.

### Commit immutable generations

Write a new generation without overwriting the last good one. Each shard has run/job ID, generation, epoch, rank/partition identity, schema, source/config/input digests, byte count, checksum, progress position, dependencies and completion marker. Write to temporary object names, flush/durably close according to storage semantics, validate, then atomically publish a small manifest or consensus decision that names all committed shards.

Atomic rename semantics differ across local, parallel and object stores. Object stores may not provide filesystem rename; use immutable objects plus conditional manifest update. Do not infer durability from API return without its documented guarantees. Keep multiple generations and garbage-collect only after the new generation has survived restore validation and retention policy.

Checksums detect some accidental change; cryptographic hashes strengthen accidental/adversarial integrity but do not prove semantic correctness. Validate dimensions, types, ranges, units, conserved quantities, partition coverage/nonoverlap, monotonic progress, reference samples and application invariants. Signed manifests may authenticate provenance where required.

### Establish a consistent recovery line

In coordinated checkpointing, participants agree on a global generation and capture a consistent cut, often at a barrier or nonblocking coordination point. It avoids domino rollback but can synchronize I/O and amplify pauses. Stagger data movement while preserving one logical commit.

Uncoordinated local checkpoints reduce coordination but a receiver may restore a message effect whose sender rolls back before sending it. Dependency tracking or message logging must find a consistent recovery line and prevent orphan processes; otherwise cascading rollback can reach the beginning. Communication-induced protocols force selected checkpoints to preserve consistency.

Message logging records nondeterministic determinants—such as receive order—so restarted processes can replay. Pessimistic logging makes determinants stable before their dependent effects, simplifying recovery at runtime cost. Optimistic or causal logging changes overhead and rollback/exposure risks. Payload recovery, sender-based logs, garbage collection and failures during recovery need explicit protocols.

Chandy–Lamport snapshots capture a consistent global state under specific channel assumptions using markers and channel-state recording. Production checkpoint protocols must account for their actual ordered/unordered channels, collectives, RMA, retries, devices and external effects; citing the algorithm does not automatically satisfy these mappings.

### Optimize interval only after correctness

This executable model evaluates a simplified expected waste fraction. It assumes constant checkpoint cost, exponentially distributed independent fail-stop events, failure-free checkpoints/restarts, negligible restart/detection cost, and uniform failure position. It does not prove availability or choose policy for correlated faults, queue/preemption limits, tiered storage, corruption, or RPO.

<!-- bijux-verify: {"id":"checkpoint-interval-waste-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"continuous_optimum_minutes=75.895\ninterval=30 waste_fraction=0.154167\ninterval=60 waste_fraction=0.108333\ninterval=90 waste_fraction=0.106944\ninterval=120 waste_fraction=0.116667\ninterval=180 waste_fraction=0.147222\nbest_allowed_interval=90\n","stderr":""}} -->
```python
checkpoint_cost = 4
mean_failure_interval = 720
continuous_optimum = (2 * checkpoint_cost * mean_failure_interval) ** 0.5
allowed_intervals = [30, 60, 90, 120, 180]
best_interval = None
best_waste = None
print(f"continuous_optimum_minutes={continuous_optimum:.3f}")
for interval in allowed_intervals:
    waste = checkpoint_cost / interval + interval / (2 * mean_failure_interval)
    print(f"interval={interval} waste_fraction={waste:.6f}")
    if best_waste is None or waste < best_waste:
        best_interval = interval
        best_waste = waste
print(f"best_allowed_interval={best_interval}")
```

The derivative of `C/T + T/(2M)` is `-C/T^2 + 1/(2M)`; setting it to zero gives `T=sqrt(2CM)`, and the positive second derivative gives a minimum. This is Young's first-order reasoning. Higher-order models include restart and checkpoint duration more carefully.

Policy also obeys maximum RPO, wall-time/preemption signals, checkpoint bandwidth and burst limits, storage quotas, convergence/value boundaries, failure-rate uncertainty and multi-level costs. Measure `C`, restore duration and failure statistics by scale/phase; do not copy a cluster-wide MTBF into a job model without exposure analysis.

### Use multi-level redundancy deliberately

Memory or local SSD checkpoints are fast but vanish with node loss. Partner replication or erasure codes tolerate configured local failures. Burst buffers or distributed cache add scope. Parallel filesystem/object storage survives broader domains but costs bandwidth and may share regional/control-plane risks. Archive tiers protect final results differently.

For each level, state tolerated failures, placement constraints, replication/code parameters, write/read bandwidth, capacity, flush lag, integrity, encryption, retention and fallback. Verify physical placement, not labels. A background flush must not cause the job to call an unflushed checkpoint durable.

Recovery selection chooses the newest committed generation intact in an available tier, then validates every shard and cross-shard invariant. If corrupt, fall back without overwriting evidence. Record actual lost progress and recovery time.

### Fence epochs and external effects

On restart, create a new recovery epoch. Every task, message, lease, output fragment and callback carries run/epoch/operation identity. Receivers reject older epochs; stores use conditional writes/fencing tokens; duplicate messages are deduplicated. Draining a network is rarely provable, so identity is safer than timing.

Exactly-once external effects usually require an atomic transaction with computation state or an idempotent protocol. Prepare output under immutable operation ID, commit once using a durable ledger, and treat ambiguous timeout as unknown—not safe to repeat blindly. Reconcile database/object/queue state during recovery before new output.

Temporary files, partial datasets and leases from failed epochs need ownership and garbage collection. Never delete artifacts until the authoritative manifest and retention rules identify them as unreachable; recovery can race cleanup.

### Detect failure without spreading it

Heartbeat and timeout parameters trade detection speed, overhead and false suspicion. Use monotonic clocks, bounded queues and backpressure. Distinguish application progress failure from node/process failure, storage slowdown and network partition. Watchdogs need an independent enough execution/resource domain.

Contain by stopping publication, revoking/fencing affected communication, cancelling structured descendants, freezing checkpoint garbage collection, preserving diagnostics and transitioning all survivors to an agreed recovery state. Continuing some ranks while others assume abort can corrupt communication and output.

Standard MPI error handlers do not by themselves make process-failure recovery portable. MPI 5.0 explicitly limits standard process-failure handling; implementations/extensions such as ULFM add semantics but require supported components, runtime enablement, communicator revoke/shrink/agreement and application state recovery. Test the exact MPI/runtime/scheduler launch path.

Retries must be bounded by count, elapsed time and error class with exponential/backoff/jitter where appropriate. Permanent corruption, schema incompatibility, repeated same-domain loss or exhausted capacity should escalate to fallback/abort/operator rather than loop.

### Restore and validate in stages

Recovery is a state machine: detect/suspect; stop or fence old epoch; preserve evidence; inventory survivors/resources; select generation; authenticate/verify bytes; validate schema/configuration; allocate new topology; restore partitions/RNG/tasks; rebuild derived state; reconcile messages/external effects; run semantic probes; establish new epoch; resume shadow/limited output; then declare useful progress.

Process/rank counts may change. Partition formats should be independent of rank number or have a proved redistribution path. RNG streams must remain tied to logical work rather than replacement rank if reproducibility matters. Device-specific serialized state may need portable reconstruction.

Measure RTO from service failure to validated useful progress, not from executable start. Decompose detection, allocation, data fetch, read/decode, redistribution, rebuild, reconciliation, validation and warm-up. RPO measures committed progress actually lost. Report tail and worst observed values under stated tests.

### Detect silent corruption

Fail-stop injection is insufficient. Flip bits/bytes, truncate/reorder/duplicate shards, alter manifests, swap generations, corrupt RNG/configuration, inject NaN/Inf and plausible-but-wrong values, and simulate stale cache. Test data in memory, transfer and storage where mechanisms allow.

End-to-end checksums follow data across stages; ECC/device/storage checks cover different layers. Semantic invariants detect correctly checksummed wrong computation. Redundant recomputation, algorithm-based fault tolerance, replicated voting or independent reference calculations add evidence but have common-mode risks.

Never automatically promote a recovered result merely because deserialization succeeds. Quarantine, preserve provenance and run independent validation before authoritative publication.

### Exercise recovery continuously

Unit tests crash at each checkpoint protocol transition. Systematic tests reorder commit/cancel/message events. Integration tests kill processes/nodes/devices, revoke networks, exhaust storage, preempt allocations, corrupt generations and fail during recovery. Test repeated and compound faults up to declared coverage, including unavailable newest tier and fallback to older data.

Run game days on production-like isolated systems with scheduler/storage/operators. Verify alarms, runbooks, permissions, keys, quotas, spare resources and evidence. A checkpoint never restored is an untested backup. Track restore-success rate by generation/tier, validation failures, actual RPO/RTO, retry/escalation, orphan cleanup and fault-coverage gaps.

### Security, operations, and high-stakes limits

Checkpoints contain full memory/model/data, credentials, keys, paths and proprietary inputs. Minimize secrets; rotate credentials after restore; encrypt/authenticate; restrict access; audit; separate tenant/job namespaces; validate parsers; pin schemas; bound decompression; and protect manifests from rollback or substitution attacks. Recovery code processes attacker-controlled/corrupt bytes and needs isolation.

High-stakes recovery requires named domain, algorithm/numerics, distributed/concurrency/runtime, storage/network/device, security/privacy, operations/reliability, safety, quality/regulatory, human-factors/accessibility, ethics and independent validation reviewers. Recovery cannot certify correctness of the resumed computation or authorize operational use.

## Definitions and Notation

- `F`: declared tolerated fault sets and correlation assumptions.
- `C_k`: committed checkpoint generation `k` and its manifest/shards.
- `e`: recovery epoch fencing old work and effects.
- `C`: checkpoint duration/cost in useful-work units.
- `T`: useful-work interval between checkpoints.
- `M`: modeled mean interval between relevant independent failures.
- `w(T)=C/T+T/(2M)`: simplified expected waste approximation.
- `RPO_obs`: observed committed progress lost under a test.
- `RTO_obs`: observed failure-to-validated-useful-progress duration.
- `I(C_k)`: byte, schema, partition, semantic and provenance invariants.
- `E`: evidence: model, topology, generations, injections, traces, validations, RPO/RTO, limits and reviewers.

## Mechanisms, Invariants, or Proof Structure

### State-completeness proof

Inventory authoritative application, communication, RNG, task, device, configuration and external-effect state; show every item is stored, reconstructed, recomputed safely or explicitly excluded.

### Commit/consistency proof

Show immutable shards become durable and valid before atomic manifest publication; derive a consistent recovery line through coordination, dependency tracking or sufficient determinants; preserve older committed generations.

### Fault-containment proof

Map each `F` to detection, fencing/revocation, redundancy placement, recovery resources and bounded retry/escalation. Demonstrate stale epochs and ambiguous external effects cannot become authoritative.

### Restore-validation proof

Inject faults; select/fallback; authenticate bytes; validate schema and semantic invariants; reconstruct topology/state; reconcile effects; prove before/after output and progress properties; measure RPO/RTO and repeated-failure behavior.

### Claim-boundary proof

Handoff names covered and unsupported faults, correlation assumptions, shared domains, runtime/storage semantics, interval assumptions, tests, observed tails, unavailable platforms, security controls and human review. It never says universally fault tolerant.

## Alternatives and Trade-Offs

| Mechanism | Strength | Principal limitation |
|---|---|---|
| full restart | simple clean process state | loses all progress; high RTO |
| application checkpoint | semantic, portable state | engineering/schema burden |
| system checkpoint | transparent process capture | external/device/kernel portability gaps |
| coordinated checkpoint | simple consistent recovery line | coordination and I/O burst |
| uncoordinated checkpoint | less global pause | orphan/domino risk; dependency complexity |
| message logging | replay with localized rollback | determinant/payload overhead and GC |
| local/memory checkpoint | low latency/bandwidth | narrow failure-domain coverage |
| remote/erasure-coded tier | broader coverage/capacity efficiency | compute/network/rebuild complexity |
| replication | immediate failover potential | resource cost and common-mode faults |
| algorithm-based recovery | protects selected numerical state | algorithm-specific coverage |

## Failure Modes and Misconceptions

- **“A file is a checkpoint.”** recovery needs complete, consistent, committed, validated state.
- **“Checksum valid means result correct.”** semantic errors can be checksummed.
- **“Two copies mean redundancy.”** shared failure domains can remove both.
- **“Latest is best.”** newest generation may be partial/corrupt; preserve fallback.
- **“Rename is atomic everywhere.”** storage semantics differ.
- **“Timeout proves death.”** it establishes suspicion under a policy.
- **“MPI errors guarantee continuation.”** standard and implementation recovery scope differ.
- **“Restarted ranks can reuse old messages.”** epochs must fence stale traffic.
- **“Exactly once follows from retries.”** effects need transaction/idempotency/deduplication.
- **“Local checkpoints compose globally.”** communication consistency is required.
- **“RTO ends at process launch.”** validation and useful progress belong in it.
- **“RPO is the checkpoint interval.”** flush lag/commit/fallback can increase loss.
- **“Young's formula is policy.”** its assumptions omit many production costs/faults.
- **“More frequent is always safer.”** overhead and checkpoint failure exposure rise.
- **“One restart proves resilience.”** inject faults across transitions and domains.
- **“Fail-stop tests cover corruption.”** silent wrong state needs separate detection.
- **“Recovery can overwrite evidence.”** preserve failed generations and diagnostics.
- **“Checkpointing certifies output.”** computation and domain validation remain.

## Worked Examples

### Example 1

**Interval model.** `C=4`, `M=720` gives 75.895 minutes continuous optimum and 90 among allowed choices. **Conclusion:** optimize only inside explicit assumptions and RPO.

### Example 2

**Partial generation.** Rank 7 upload fails before manifest commit. Recovery ignores all uncommitted shards and retains `C_(k-1)`. **Conclusion:** commit pointer defines authority.

### Example 3

**Inconsistent locals.** Receiver checkpoint contains a message effect while sender checkpoint predates send. Coordinate or log dependencies/determinants. **Conclusion:** local validity is not global consistency.

### Example 4

**Shared domain.** Primary and replica on two SSDs in one node vanish together. Place according to node/rack fault claim. **Conclusion:** independence is physical and operational.

### Example 5

**Stale epoch.** Delayed result from epoch 12 arrives after recovery epoch 13. Receiver rejects it by `(run,epoch,operation)` identity. **Conclusion:** fencing beats timing assumptions.

### Example 6

**Ambiguous write.** Object-store timeout occurs after server commit. Retry uses immutable key/idempotency ledger rather than creating another output. **Conclusion:** timeout outcome may be unknown.

### Example 7

**Semantic corruption.** All bytes/hash match, but concentration units in configuration are wrong. Unit/range/reference validation rejects restore. **Conclusion:** integrity and meaning differ.

### Example 8

**Topology change.** Eight surviving ranks restore sixteen-rank partition files using logical partition IDs and deterministic redistribution. **Conclusion:** avoid binding recovery state to transient rank numbers.

### Example 9

**Failure during recovery.** Newest tier becomes unavailable mid-read; state machine preserves evidence and falls back to an older independently stored committed generation. **Conclusion:** recovery itself belongs in fault tests.

### Example 10

**Flood-forecast and warning job.** Recovery must preserve observation/source/unit/time/model/mesh/ensemble/region/warning/configuration generations, validate hydrological conservation and uncertainty, fence stale alerts, reconcile already issued warnings, bound detection/RPO/RTO against warning horizons, protect location/person data, and degrade safely when inputs or compute are unavailable. Named hydrology/meteorology/emergency-management, numerical-model, distributed/runtime/storage/network, geospatial/data-quality, safety/security/privacy, operations/reliability, quality/regulatory, human-factors/accessibility, ethics and independent validation reviewers must approve it; none is claimed here. **Conclusion:** successful restart cannot authorize public warnings.

## Cross-Program Connections

- **Distributed systems:** consistent cuts, failure detectors, epochs, leases, replication and message logging structure recovery.
- **Databases:** atomic commits, transactions, idempotency, deduplication and isolation protect effects.
- **Storage:** durability, checksums, erasure codes, manifests and retention determine recoverability.
- **Cloud/platform:** schedulers, preemption, placement, identity, keys, quotas and runbooks affect RTO.
- **Security:** checkpoints are sensitive executable/data artifacts and rollback targets.
- **Numerical computing:** convergence, RNG and conservation invariants detect semantic corruption.
- **Testing/formal methods:** transition faults, crash points and invariants validate protocols.
- **Observability:** epochs, state transitions, RPO/RTO and loss require durable telemetry.
- **Economics/sustainability:** redundancy and recomputation trade cost, energy and completion risk.
- **Safety:** hazard deadlines and authoritative external effects require independent assurance.

## References

1. MPI Forum, *MPI 5.0: Error Handling*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node49.htm>
2. Open MPI Project, *User-Level Fault Mitigation (ULFM)*, Open MPI 5.0.9 documentation; retrieved 2026-08-29. <https://docs.open-mpi.org/en/v5.0.9/features/ulfm.html>
3. Lawrence Livermore National Laboratory, *Scalable Checkpoint/Restart 3.1.0 User Guide*, current documentation; retrieved 2026-08-29. <https://scr.readthedocs.io/en/latest/>
4. Fault Tolerance Interface Project, *FTI Documentation*, current documentation; retrieved 2026-08-29. <https://fault-tolerance-interface.readthedocs.io/en/latest/>
5. K. Mani Chandy and Leslie Lamport, “Distributed Snapshots: Determining Global States of a Distributed System,” ACM TOCS, 1985. <https://www.microsoft.com/en-us/research/publication/distributed-snapshots-determining-global-states-distributed-system/>
6. E. N. Elnozahy et al., “A Survey of Rollback-Recovery Protocols in Message-Passing Systems,” *ACM Computing Surveys*, 2002. <https://research.ibm.com/publications/a-survey-of-rollback-recovery-protocols-in-message-passing-systems>
7. John W. Young, “A First Order Approximation to the Optimum Checkpoint Interval,” *Communications of the ACM*, 1974. <https://doi.org/10.1145/361147.361115>
8. John T. Daly, “A Higher Order Estimate of the Optimum Checkpoint Interval for Restart Dumps,” *Future Generation Computer Systems*, 2006. <https://doi.org/10.1016/j.future.2004.11.016>
9. Adam Moody et al., “Design, Modeling, and Evaluation of a Scalable Multi-Level Checkpointing System,” SC, 2010. <https://doi.org/10.1109/SC.2010.18>
10. Wesley Bland et al., “Post-Failure Recovery of MPI Communication Capability: Design and Rationale,” *International Journal of High Performance Computing Applications*, 2013. <https://icl.utk.edu/files/publications/2013/icl-utk-569-2013.pdf>

## Exercises

### Exercise 1

Derive the stationary point of `w(T)=C/T+T/(2M)`, verify it is a minimum, and compute it for `C=9` minutes and `M=800` minutes. State at least six invalidating assumptions.

### Exercise 2

Design an immutable sharded checkpoint protocol for 32 ranks with local, partner and object-store tiers. Include commit, consistency, validation, placement, retention and recovery selection.

### Exercise 3

Compare coordinated checkpointing, uncoordinated checkpointing and pessimistic message logging for an asynchronous solver. Cover orphan messages, domino effect, pause, storage, determinants and recovery complexity.

### Exercise 4

Design a fault-injection and RPO/RTO evidence matrix including process/node/storage/network/device/corruption faults, failures during checkpoint/recovery, stale epochs, external effects, false suspicion and escalation.

### Exercise 5

Transfer recovery engineering to a long-running concurrent clinical genomics pipeline. Specify state, consistency, privacy/security, scientific/clinical validation, RPO/RTO, failure tests and named reviewer roles without claiming review or clinical authorization.

## Answers to the Exercises

### Answer 1

`w'(T)=-C/T^2+1/(2M)`. Setting it to zero gives `T^2=2CM`, so positive `T*=sqrt(2CM)`. `w''(T)=2C/T^3>0`, hence a local and, for positive `T`, global minimum of this approximation. For `C=9`, `M=800`, `T*=sqrt(14400)=120` minutes. Invalidating/omitted assumptions include nonconstant checkpoint cost; nonexponential/nonindependent or correlated failures; failure during checkpoint/restart; nonnegligible detection/restart time; limited storage/bandwidth; multi-level flush lag; variable workload phases; scheduler/preemption deadlines; silent corruption; compound faults; and an RPO stricter than 120 minutes. Measure inputs and use a richer model/policy.

### Answer 2

At generation `k`, quiesce/log communication to establish one recovery line, assign immutable `(run,k,logical-partition)` shards, and write each shard with schema/config/input/progress/checksum/semantic metadata to local storage and a partner on a different node/failure group. Validate byte count/hash and partition coverage/nonoverlap; asynchronously upload immutable objects, but label tier durability only after all required objects validate. Publish the generation manifest using conditional atomic update after required tier/redundancy acknowledgments. Retain at least two older committed manifests/shards until restore probes and policy permit GC. Recovery authenticates manifests newest-to-oldest, verifies actual placement/availability and every shard/cross-shard invariant, selects the newest intact generation in an available tier, redistributes logical partitions to current ranks, establishes a new epoch and reconciles effects. Partial shards without a committed manifest are never authoritative.

### Answer 3

Coordinated checkpointing makes one consistent recovery line and avoids orphans/domino rollback, but imposes coordination and potentially bursty pause/I/O; nonblocking/staggered writes can reduce physical pause without changing logical commit. Uncoordinated checkpoints reduce global coordination and let ranks checkpoint independently, but dependency analysis must locate a consistent line and may cascade rollback. Pessimistic message logging stabilizes each nondeterministic determinant before dependent delivery, enabling replay/localized recovery and avoiding orphan effects under its protocol, at latency/storage/log-GC cost. Payload availability, receive order, collectives/RMA, failures during recovery and external effects complicate all choices. Select from communication pattern, tolerated fault set, pause/RPO/RTO and proven runtime semantics rather than generic speed.

### Answer 4

Cross fault class and crash point with scale/topology/generation/tier: kill one process, node and GPU; remove local/partner/object tier; partition network/storage/control plane; fill quota; delay heartbeat to cause false suspicion; truncate/flip/swap/replay shards/manifests; fail before shard close, after shard validation, before/after manifest commit, during flush, selection, read, redistribution, reconciliation and resumed output; inject a second fault during recovery. Deliver stale old-epoch messages/callbacks and ambiguous external-write timeouts. For each test record expected detection/fencing/fallback/escalation, authoritative output/idempotency, validation result, actual lost committed progress (`RPO_obs`), failure-to-validated-progress (`RTO_obs`), retries and preserved evidence. Include unsupported correlated/Byzantine faults explicitly. Test bounded retry and operator alerts/runbook/permissions/spare capacity, not only automated restart.

### Answer 5

Checkpoint immutable sample/specimen/consent/patient-pseudonym/reference-build/pipeline/container/tool/database/model/variant/annotation/provenance and logical-task generations; include input offsets, partitions, RNG where used, pending workflows, quality thresholds and deduplication/external-report tokens. Coordinate stages or log dependencies so no downstream result survives without its upstream determinant; atomically commit signed/encrypted manifests after all shards validate, fence old epochs and reconcile already published records idempotently. Validate hashes/schema plus read coverage, reference coordinates, units, contamination, controls, provenance, representative known variants and independent recomputation. Separate research output from clinically reportable output. Test crashes/corruption/partition/quota/schema incompatibility during checkpoint and recovery, fallback and repeated faults; measure RPO/RTO against laboratory workflow needs. Use least privilege, managed keys, audit, deidentification, access/retention/deletion governance and isolated parser restoration. Named molecular genetics/pathology/laboratory medicine, bioinformatics/genomics/statistics, clinical informatics, distributed/runtime/storage, cybersecurity/privacy/data governance, operations, quality/regulatory, ethics, accessibility/human-factors and independent validation reviewers must approve claims. No external review, analytical/clinical validity, privacy guarantee, regulatory approval or clinical authorization is claimed.
