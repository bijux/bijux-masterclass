---
module_id: LSDS-045
program: Large-Scale Data Systems Engineering
level: 1
module_number: 45
title: Watermarks
status: complete
last_verified: 2026-09-04
---

# Watermarks

## One-Page Review

### Governing question

How can an unbounded distributed dataflow make an explicit, useful, and auditable claim about event-time progress when inputs are partitioned, delayed, idle, replayed, backfilled, or unable to prove that older records will never arrive?

### Essential definitions

- A **watermark** $W$ is a monotone event-time frontier used to classify records and release event-time work; it is a scoped progress claim, not wall-clock time or the newest timestamp seen.
- A **source watermark** summarizes progress knowledge at an input partition or split. Its quality depends on the source contract.
- An **operator watermark** is derived from input watermarks and any internal holds needed for buffered or pending work.
- A **watermark hold** prevents output progress from passing an event time at which an operator may still produce output.
- **bounded-out-of-orderness generation** derives a candidate from the maximum timestamp observed minus a configured disorder bound.
- A **punctuated watermark** advances from an in-band record or source marker with defined completeness semantics.
- An **idle input** is temporarily excluded from progress merging after an explicit liveness policy; it may later resume with records that are late relative to already-emitted progress.
- **watermark alignment** throttles or pauses fast inputs so their progress does not outrun slow related inputs by more than a configured drift.
- **late data** is data behind the relevant emitted watermark under a stated boundary rule; positive arrival delay alone is not the definition.
- **end-of-input progress** advances to a terminal frontier only after bounded exhaustion is proven, allowing remaining event-time work to finish.

### Central model, mechanism, or theorem

For input partition $j$ at processing instant $\tau$, let $M_j(\tau)$ be the maximum valid event timestamp observed and $B_j$ a declared disorder allowance. A simple candidate is

$$C_j(\tau)=M_j(\tau)-B_j,$$

and emitted source progress must be nondecreasing:

$$W_j(\tau)=\max(W_j(\tau^-),C_j(\tau)).$$

This formula is a guarantee only when the source truly bounds future disorder by $B_j$; otherwise it is a heuristic that deliberately makes records behind $W_j$ late. A multi-input operator commonly computes

$$W_{out}=\max(W_{out}^{old},\min_{j\in A}W_j,H),$$

where $A$ is the active input set and $H$ represents applicable output holds. Exact hold direction/representation varies by model, but output must not outrun work the operator is still contractually able to emit. If an idle input is removed from $A$, progress may advance; its resumption cannot make emitted progress retreat.

### Critical invariants

- Watermarks are nondecreasing within their declared execution/epoch; downstream progress never retreats.
- Every watermark identifies its event-time domain, source/partition scope, generation rule/version, strict boundary convention, and confidence/guarantee basis.
- The maximum observed event timestamp is state used by some generators, not proof of completeness by itself.
- Partition progress is computed before merging; interleaved consumption must not erase a slow partition's frontier.
- An operator forwards progress only after processing all preceding data/control work and honoring pending output holds.
- Idle detection names timeout/evidence, active-set epoch, resume behavior, and the consequences for returning old data.
- Backfills, new partitions, reassignment, restore, and source restarts cannot silently join with an advanced frontier.
- Late-data handling and state cleanup use the same boundary/allowed-lateness contract as the emitted watermark.
- Alignment limits relative progress/state growth but does not make clocks, timestamps, or heuristic watermarks correct.
- Metrics expose per-input and output watermarks, spread, time since advance, holds, idleness, late outcomes, and state cost.

### Common failures

Common failures include equating watermark with maximum timestamp, wall clock, broker offset, or checkpoint; emitting a frontier that regresses; subtracting one global delay after mixing partitions; ignoring an empty partition forever; marking a slow partition idle too aggressively; allowing a resumed partition to roll progress backward; marking end-of-input before exhaustion; carrying live watermarks into an uncoordinated backfill; using observed p99 lateness as a hard bound; advancing from a malicious future timestamp; choosing a maximum across inputs without accepting loss; accumulating hidden holds; measuring only the global frontier; and assuming a conservative watermark is free when it delays results and grows state.

### Compact example

Two partitions use a 10-second disorder allowance. Partition 0 observes 100 and proposes 90; partition 1 observes 80 and proposes 70, so merged progress is 70. Partition 0 then observes 130 and reaches 120, but output remains 70. If partition 1 is declared idle, output may advance to 120. When it resumes with timestamp 85, its local frontier advances to 75 but the output cannot regress from 120; under a `timestamp <= watermark` convention, that record is late. Idleness traded liveness for a late-data obligation.

### Connections

[LSDS-044](044-event-time-processing.md) defines the timestamp evidence a watermark summarizes. [LSDS-043](043-stateful-operators.md) supplies state and timers. [LSDS-046](../ROADMAP.md) applies progress to window assignment/triggers, while [LSDS-047](../ROADMAP.md) through [LSDS-050](../ROADMAP.md) distinguish temporal progress from recoverable cuts and safe effects.

## Governing Question

An unbounded stream has no natural final row. An event-time window cannot wait for global end-of-input, yet seeing a record at 12:00 does not prove an 11:59 record is not delayed elsewhere. The runtime needs a declared point at which it may emit event-time timers, produce a completeness-sensitive result, or reclaim time-bounded state.

A watermark supplies that point. Depending on the source, it can be a strong frontier derived from source structure, an informed estimate from observed disorder, or a heuristic chosen to balance latency and completeness. Treating these kinds as equivalent is dangerous. A database snapshot reader may know exactly which key ranges are exhausted; a mobile event stream may only estimate its tail.

Distribution makes the problem compositional. Each partition has its own progress and liveness. Operators buffer, join, fan out, and merge streams. One idle or slow input can hold the safe minimum. Removing it improves liveness but makes its eventual return late. Letting a fast side race ahead can make a join store grow without bound.

The governing question is how to define the frontier's meaning, generate it from defensible evidence, propagate it without outrunning pending work, handle idleness and topology change safely, and measure when the latency/completeness/state trade-off no longer matches the product contract.

## Why This Matters

Watermarks convert an endless computation into actionable event-time milestones. They let runtimes fire event-time timers, close or refine windows, bound temporal joins, expire state, and report result freshness without waiting forever. They also let users reason about what a current result probably or provably includes.

An over-aggressive watermark turns ordinary disorder into late data. If the late path drops records, results become incomplete. If it retracts and updates, downstream traffic and complexity rise. If state was already deleted, correction may be impossible. A single future-poisoned timestamp can make a naive maximum-based generator leap forward and discard hours of healthy traffic.

An overly conservative watermark has a different cost. Results wait, timers do not fire, windows and joins retain state, checkpoints grow, recovery slows, and users see stale outputs. One empty partition can freeze the minimum indefinitely. A theoretically “safe” frontier that never advances is operationally useless.

Watermarks are also interfaces. Sources produce them; operators transform them; sinks and users interpret their consequences. Restart, rescale, partition discovery, backfill, idleness, and code upgrades can change the frontier. Without versioned semantics and telemetry, a small configuration adjustment silently changes product correctness.

## Prerequisites and Retrieval

Review event-time provenance, uncertainty, lateness, replay, backfill, correction, and security in [LSDS-044](044-event-time-processing.md). Retrieve partition identity and offset frontiers from [LSDS-041](041-logs-as-distributed-input.md) and [LSDS-042](042-partitioned-consumption.md), and state/timer lifecycle from [LSDS-043](043-stateful-operators.md).

You should understand monotone functions, minimum/maximum aggregation, partial orders, active sets, epochs, half-open intervals, quantiles, partitioning, source offsets, event-time timers, state retention, checkpoint recovery, and late-result representations. This module defines progress and propagation; [LSDS-046](../ROADMAP.md) develops window and trigger behavior in detail.

## Learning Objectives

After this module, you should be able to:

1. state what a watermark claims and distinguish strong source knowledge from a heuristic estimate;
2. implement monotone per-partition bounded-disorder progress with an explicit late boundary;
3. merge active input watermarks without losing slow-partition information;
4. explain how operator buffering and output holds constrain downstream progress;
5. design idle detection and resumption with epochs, fencing, and late-data consequences;
6. separate alignment, checkpointing, backpressure, offsets, and wall-clock lag from watermark semantics;
7. handle partition discovery, reassignment, restore, bounded input, and backfill without unsafe jumps;
8. evaluate fixed, punctuated, source-native, processing-lag, adaptive, and no-watermark strategies;
9. secure watermark generation against timestamp, marker, liveness, and topology manipulation; and
10. validate and observe watermark accuracy, delay, spread, stalls, holds, late outcomes, and state cost.

## Core Exposition

### Define the progress claim first

A watermark is meaningful only as a sentence. One useful convention is: after emitting $W=t$, records subsequently observed with event timestamps at or before $t$ are classified as late. Some systems phrase the boundary as “earlier than” rather than “at or before”; pin the engine and application convention.

That classification is not necessarily a promise that no late record will arrive. A source with structural knowledge may offer a guarantee. A generator based on sampled lateness offers an estimate. Label guarantee, confidence, and violation behavior. Avoid user-facing statements such as “data is complete through t” unless the source and correction contract support them.

Scope the claim by source, partition set, event-time definition, topology/epoch, rule version, and excluded channels such as authorized backfills. A global timestamp without this scope invites false comparison.

### Separate watermarks from neighboring frontiers

A source offset answers which log positions have been consumed or committed. A checkpoint captures a recoverable consistent computation prefix. A watermark estimates or guarantees event-time progress. Processing-time lag measures operational delay. Backpressure reports capacity mismatch. None substitutes for another.

Offsets can advance while event time stays flat because records share old timestamps. Event time can leap while many offsets remain. A checkpoint may persist watermark-generator state, but completing it does not make the watermark accurate. A low watermark can coexist with no broker lag when one partition is idle.

Dashboards should show these signals together precisely because their disagreement diagnoses different failures.

### Prefer source-native knowledge

The strongest frontier is produced where completeness is knowable. A bounded file reader can advance after every record in a split with timestamps below a value has been enumerated, then emit terminal progress after all splits are exhausted. A database change stream may expose commit/resolve timestamps with source-defined guarantees. A transactional source can publish explicit progress markers.

Source-native markers require authenticated ordering and completeness semantics. A marker embedded in one partition says nothing about another unless the producer coordinates them. A marker that can overtake data in a different transport is unsafe.

Document failure, rollback, repartitioning, and restart behavior. “Source-native” is not automatically correct if connector implementation loses the source guarantee.

### Generate bounded-disorder candidates

For partition $j$, keep maximum valid observed event time $M_j$. With disorder allowance $B_j$, candidate $C_j=M_j-B_j$. Emit only `max(previous,C_j)` so a late record cannot move progress backward.

The bound is a hard guarantee only when the source ensures that after observing $M_j$, no later record from that scope will have event time behind $M_j-B_j$. Most user-event streams do not provide such a theorem. Then $B_j$ is a product trade-off: violations enter the late path.

Periodic emission adds scheduling delay; a generator may update $M_j$ on every event but expose a watermark on a timer. Exact `-1` millisecond adjustments and inclusive boundaries are runtime-specific. Express the semantic boundary, then test the implementation.

### Generate before merging partitions

Compute watermark state per source partition/split where disorder assumptions hold. If records from partitions are interleaved and one global maximum is tracked, a fast partition can hide a slow one and advance progress unsafely.

Combine active partition frontiers conservatively, commonly with their minimum. The minimum says output cannot outrun the least-progressed input that may still contribute relevant old events. Partition assignment changes must transfer or reconstruct each frontier without confusing worker identity with source identity.

When a new partition is discovered, its initial frontier and activation barrier matter. Adding it below an already-emitted global watermark cannot make downstream progress retreat; old records will be late unless onboarding fences or drains them through a separate policy.

### Preserve monotonicity

Once a downstream consumer acts on watermark 120, retracting the control frontier to 70 cannot restore deleted state or unfire timers. Therefore emitted watermarks are nondecreasing within their defined epoch. Internal candidates may fall, but output clamps to the prior value.

Monotonicity alone does not prove accuracy. A watermark can advance monotonically and incorrectly. Pair the invariant with source evidence, partition scope, validation, and late-violation measurement.

Epochs permit a new execution or materialization to begin from a declared baseline, but consumers must not merge different epochs as one monotone sequence. Include job/materialization identity and version in audit data.

### Propagate through operators

An operator generally processes all data/control effects preceding a watermark before forwarding it. This preserves the meaning that outputs triggered by the frontier appear before downstream observes the same frontier. Concurrency needs barriers or mailbox ordering sufficient for the runtime's contract.

A one-input stateless map can often forward input progress after preceding records. A filter still forwards progress even when it emits no data. A timestamp-shifting transform must adjust progress consistently or constrain backward timestamp movement. A buffer, join, group, or asynchronous lookup may need an output hold at the earliest event time of pending work.

Model output progress as no greater than relevant input progress and pending-output constraints. Hidden queues, retries, side inputs, user timers, and asynchronous callbacks can become hidden holds or correctness violations.

### Merge multiple inputs deliberately

For a two-input join, a safe general frontier is constrained by both inputs, often `min(W_left,W_right)`. This delays the fast side but preserves the opportunity for older matches from the slow side. State may still grow because fast records arrive while the minimum stalls.

Some systems offer a maximum-watermark policy. It reduces delay and state but treats the slower input's subsequently arriving records as late, potentially dropping matches. This is an explicit loss/latency choice, not a performance-only toggle.

Not every input constrains every output equally. Advanced systems can track capabilities/frontiers by logical timestamp or key domain. Use a coarser minimum unless a more precise dependency proof exists.

### Detect idleness as a lease

An empty partition emits no new evidence, so its last watermark can hold the minimum forever. An idle timeout removes it from the active set after no activity for a duration. This restores liveness but asserts that the absent partition may be ignored for current progress.

Treat idleness like an expiring lease with partition identity, assignment epoch, detection clock, timeout, owner, and audit event. Distinguish truly empty, temporarily disconnected, backpressured, rate-limited, failed, and lost-credential inputs where possible. Processing silence alone cannot identify the cause.

On resumption, do not regress emitted progress. Validate/fence ownership, reinitialize generator state, and route records behind current output through the declared late path. If old data must be accepted as on-time, use a new epoch/materialization or coordinated pause/backfill protocol.

### Align fast and slow inputs

Watermark alignment limits how far a fast source's frontier advances beyond the slowest member of an alignment group. A runtime may pause fast partitions, allowing slow inputs to catch up and bounding join/window buffer growth.

Alignment trades source throughput and utilization for state control. It depends on connector pause/resume support, update frequency, grouping, maximum drift, backpressure interaction, and failure behavior. Group only inputs whose temporal relationship matters.

Alignment does not improve timestamp quality or prove completeness. It limits relative progress and arrival, while a bad watermark can remain bad in perfect alignment.

### Use punctuated progress carefully

A punctuated generator advances when it reads a marker such as “all events through day D have been emitted.” This can be more accurate than a time-delay heuristic when the producer truly knows completeness.

The marker needs ordering with the governed data, partition scope, authentication, version, deduplication, replay behavior, and crash semantics. If a marker travels on one partition while older data travels on another, receipt order is insufficient. A malicious or buggy marker can cause irreversible early cleanup.

Heartbeats prove some liveness but not necessarily event-time completeness. Define whether a heartbeat carries a safe frontier, merely repeats current progress, or only prevents failure detection.

### Treat adaptive estimates as control systems

An adaptive generator can estimate a lateness quantile by cohort and set its delay dynamically. It may reduce latency during healthy periods and become conservative during incidents. But the sample is censored: records not yet arrived are absent from the estimated tail.

Adaptation needs bounded rate of change, minimum/maximum delay, enough samples, cold-start policy, robust statistics, versioned state, and alerting. If it shortens delay after a quiet period just before a delayed batch arrives, it creates a late-data surge. An estimator influenced by its own dropping policy can hide violations.

Replay must either restore recorded estimator decisions/state or accept explicitly different temporal results. Do not market adaptive confidence as a deterministic guarantee.

### Handle processing-time lag heuristics

Some sources cannot infer progress from event timestamps but expect events to arrive within wall-clock delay $D$. A candidate such as `processing_now-D` advances during silence, unlike max-seen generation. It assumes comparable event and processing clocks and a delay bound.

This is vulnerable to source outage: wall time continues while old records remain upstream. It can be appropriate for controlled telemetry with strong clock and delivery SLOs, but it needs outage detection, source health gating, maximum advance, and a late-data plan.

Use a monotonic clock for local elapsed-time scheduling but convert the declared frontier in the event-time domain carefully. Wall-clock corrections must not make output regress or leap.

### Handle bounded completion

For bounded input, a terminal watermark (conceptually positive infinity) can flush all remaining windows/timers. Emit it only after source enumeration, split completion, retries, and dynamic discovery are closed under the source contract.

Premature terminal progress is especially destructive because every later finite timestamp is late. A coordinator should fence old owners, confirm each split exactly once under the completion protocol, persist completion, and define restore behavior.

An idle source is not a completed source. A day boundary is not end-of-input when corrections or backfills remain possible.

### Isolate backfills and topology changes

Historical backfills intentionally violate live watermark assumptions. Feeding them into an advanced live stream makes all records late or tempts operators to reset progress, which they cannot safely do. Use a dedicated input/materialization, correction stream, or coordinated rebuild and deterministic merge.

Partition split/merge, resharding, topic expansion, and reassignment need frontier migration. Persist progress by stable source split identity, not worker. New children inherit only a frontier justified by the source's split semantics; otherwise start conservatively and manage late data.

Deploying a new watermark rule changes product output and state. Version it, shadow it on captured traffic, compare lateness/result/state distributions, and roll forward through a declared epoch or compatible state migration.

### Couple progress to late-data policy

Define late at the point where the relevant emitted watermark has passed the record timestamp under exact equality semantics. Then decide whether to update open state, emit a late pane, retract/replace output, append an adjustment, quarantine, or drop.

Allowed lateness extends how long state accepts updates after an initial frontier/window result. It does not make the original watermark later or guarantee arrival within the allowance. Cleanup boundaries must match trigger/result semantics and downstream mutation support.

Count violations by how far behind the watermark they arrive, not only their arrival delay from event time. A record can have high arrival delay but still precede a conservative watermark, or small delay but fall behind an aggressive one.

### Manage state and holds

Watermark delay translates directly into retained window/join/timer state. Estimate state arrival rate times effective retention plus skew and amplification. Per-key hot spots and cross-input drift can dominate the total.

Inventory holds: window end, pending async work, side-input readiness, user timer, buffered reordering, sink coordination, and engine internals. Every hold needs owner, reason, event timestamp, creation time, bound, cancellation/recovery behavior, and metrics. A leaked hold freezes progress.

Do not advance progress merely to solve memory pressure. Apply admission, alignment, backpressure, spill, capacity, approximation, or explicit loss policy; hiding forced data loss as a watermark adjustment makes correctness unauditable.

### Recover and upgrade deliberately

Checkpoint or reconstruct generator state needed for consistent behavior: per-partition maximum seen, last emitted watermark, active/idle status and epoch, adaptive estimator state, source markers, and operator holds. Exact runtime persistence varies; test it rather than assuming.

After restore, replayed records behind a previously acted-upon frontier need defined treatment. Some runtimes rebuild watermarks from sources and checkpoints while protecting state/output through their recovery model. External consumers may already have observed results, so effect identity and correction semantics remain necessary.

Upgrade tests compare frontier sequences or semantic outcomes under old/new code, including idleness, partition changes, and restored state. A nondecreasing but faster new sequence can still change results.

### Secure the progress plane

Validate event timestamps before they influence maxima. Bound future skew and resource impact. Authenticate source-native markers, partition membership, completion, and control messages. Fence stale owners so duplicate generators cannot publish conflicting progress.

Attackers can send sparse keepalives to prevent idleness, suppress traffic to trigger idleness, poison future timestamps, forge completion, or create partitions that stall the minimum. Rate limits, quotas, trusted infrastructure stamps, source authorization, topology controls, and anomaly detection protect availability and integrity.

Watermark telemetry can expose customer activity times. Apply aggregation, access control, retention, and careful labeling while preserving enough per-partition evidence for operators.

### Observe frontier quality and cost

Record each per-partition input watermark, merged/operator/output watermark, current processing time minus watermark where meaningful, maximum observed event time, watermark spread, age since last advance, active/idle set, alignment pauses, and holds.

Measure late count/rate and distance behind watermark by result type and cohort; corrections, drops, side-output backlog; window/timer firing delay; state bytes/keys/age; checkpoint/restore cost; and output freshness. Correlate with broker lag, input rate, backpressure, errors, retries, and source health.

Do not put raw partition/cardinality dimensions into an unbounded metric backend. Preserve detailed protected diagnostics in sampled logs/traces or queryable operational stores.

### Validate with temporal fault injection

Replay captured traffic with deterministic permutations, partition skew, long pauses, idle/resume, duplicates, timestamp ties, negative/future skew, marker reordering, ownership change, source failure, backpressure, dynamic partitions, checkpoint/restore, and historical backfill.

Assert non-regression, partition-min behavior, hold propagation, exact late boundary, no premature terminal frontier, bounded alignment/state, deterministic rule version, and downstream convergence. Compare candidate delays against authoritative eventual input to compute violation curves.

Shadow more-aggressive and more-conservative policies before rollout. Evaluate not only latency but changed results, correction load, state/checkpoint size, recovery, cost, and affected users.

## Definitions and Notation

For partition $j$ and processing instant $\tau$:

- $M_j(\tau)$ is the maximum validated event timestamp observed;
- $B_j$ is a configured or guaranteed disorder bound;
- $C_j(\tau)=M_j(\tau)-B_j$ is a simple candidate frontier;
- $W_j(\tau)$ is the last emitted per-partition watermark;
- $A(\tau)$ is the set of inputs considered active;
- $H(\tau)$ is an abstract upper constraint from pending output work;
- $W_o(\tau)$ is the last emitted operator/output watermark; and
- $e_i$ is record $i$'s event timestamp.

A monotone generator satisfies $W_j(\tau_2)\ge W_j(\tau_1)$ for $\tau_2\ge\tau_1$ within one epoch. A conservative multi-input merge commonly uses $G(\tau)=\min_{j\in A(\tau)}W_j(\tau)$. Output applies non-regression and holds, conceptually $W_o=\max(W_o^{old},\min(G,H))$ when $H$ is expressed as the latest safe output frontier.

Under this module's explicit fixture convention, record $i$ is late when $e_i\le W_o$ at arrival. An engine may use a different equality convention; tests must pin it. Watermark delay $D_w=\tau-W_o$ is meaningful only if $\tau$ and the event-time domain are comparable.

For inputs $j,k$, watermark spread is $S=\max_{j\in A}W_j-\min_{j\in A}W_j$. Large $S$ signals relative temporal drift and potential multi-input state pressure; it does not identify the cause.

## Mechanisms, Invariants, or Proof Structure

Audit a watermark design in this order:

1. **Meaning:** write the exact late boundary and distinguish guarantee from estimate.
2. **Scope:** identify event-time field, partitions/splits, epoch/topology, rule version, and excluded backfills.
3. **Evidence:** show how source offsets, markers, timestamps, wall clock, or source-native knowledge justify each candidate.
4. **Per-input state:** preserve maximum/marker/frontier by stable partition identity and prevent regression.
5. **Composition:** merge only relevant active inputs and propagate after preceding records and pending work.
6. **Liveness:** define idle detection as an auditable lease and specify safe resume/new-partition behavior.
7. **Control:** bound fast/slow drift through alignment, admission, or capacity without disguising loss.
8. **Consequences:** align timers, windows, late results, cleanup, sinks, and correction semantics.
9. **Lifecycle:** checkpoint/reconstruct state; fence owners; handle restart, rescale, upgrade, completion, and backfill.
10. **Evidence loop:** measure violations, delay, spread, stalls, holds, state, cost, and user-visible result changes.

Non-regression proof is local: because every emitted value is `max(previous,candidate)`, induction gives a nondecreasing sequence. This proves only monotonicity, not that candidates are safe.

Partition-merge safety follows from the minimum under the assumption that every relevant active input frontier is itself valid and no excluded input can contribute on-time data. Removing an idle input invalidates the second premise for its old data, so resuming records behind output must become late or enter a separate coordinated epoch.

Propagation safety requires the operator not to emit progress beyond any timestamp at which accepted pending work could still produce an output. This premise is violated by untracked asynchronous queues or holds, even if input watermarks are perfect.

## Alternatives and Trade-Offs

**Source-native frontiers** can be strong and low-latency but need source/connector support. **Bounded disorder** is simple and tunable but is only as strong as the bound. **Processing-time lag** advances during silence but fails under outage/clock mismatch. **Adaptive estimates** follow changing tails but add state, feedback, and replay complexity.

**Punctuated markers** express producer knowledge directly but require ordered authenticated coordination. **Periodic watermarks** amortize control overhead but add emission delay. **Per-event emission** minimizes control latency while increasing overhead and rarely adds value beyond time resolution.

**Minimum multi-input merge** favors completeness and can grow delay/state. **Maximum merge** favors latency/cost while declaring slow-input records late. **Dependency-aware frontiers** can be more precise but require a sound dataflow capability model.

**Never mark idle** protects against returning old data but can stall forever. **Short idle timeout** improves liveness but increases false idleness and late data. **Source health signals** improve classification but add integration and their own failure modes.

**Alignment** bounds cross-input drift/state at throughput cost. **Unaligned consumption** maximizes source progress but may require large buffers or lossy result policy. **Separate backfill lanes** preserve live assumptions while adding merge/operations complexity.

**Aggressive watermark** gives early results and cleanup with more corrections/loss. **Conservative watermark** improves initial completeness with higher latency/state. **Early speculative plus later correction** can offer both responsiveness and eventual quality only when all consumers support mutation.

**No watermarks** is valid for pure processing-time operations or computations that never finalize on event time. It avoids false claims but cannot drive event-time cleanup/timers without another completion mechanism.

## Failure Modes and Misconceptions

1. **“The watermark is the newest timestamp.”** The newest observation does not prove older data is absent.
2. **“Subtract p99 lateness and the result is safe.”** The unseen tail and incidents still violate it.
3. **“One generator after partition merge is equivalent.”** A fast partition can mask a slow one.
4. **“Monotone means correct.”** A frontier can advance consistently and too early.
5. **“A watermark is a wall clock.”** It lives in the stream's event-time domain.
6. **“A watermark is a committed offset.”** Position and event-time progress answer different questions.
7. **“A checkpoint advances the watermark.”** Recovery and temporal progress are distinct.
8. **“No broker lag means current event time.”** Empty or old-timestamp partitions contradict this.
9. **“The minimum always works.”** Only relevant active inputs with valid frontiers make the premise hold.
10. **“Maximum multi-input policy is an optimization.”** It explicitly risks slow-stream data loss/correction.
11. **“Idle means complete.”** A disconnected partition can return with old data.
12. **“The watermark can regress on resume.”** Downstream state and fired timers cannot be unfired.
13. **“A heartbeat proves completeness.”** It may show liveness only.
14. **“Alignment improves accuracy.”** It limits relative drift and state, not timestamp truth.
15. **“Allowed lateness delays the watermark.”** It retains correction opportunity after progress.
16. **“Late data is arrival delay above zero.”** Lateness is relative to the emitted frontier.
17. **“End of a day is end-of-input.”** corrections/backfills may remain.
18. **“Restore naturally reproduces progress.”** Generator state, source behavior, holds, and external outputs require testing.
19. **“Future timestamps only spoil charts.”** They can force cleanup, effects, and denial of service.
20. **“Global watermark is enough to monitor.”** It hides the slow partition, active set, and holds.

## Worked Examples

### Example 1

A partition observes maximum event time 1,000 seconds with a 30-second disorder allowance. Its candidate is 970. If its prior emitted watermark is 980, it remains 980 rather than regressing; a late observation cannot undo downstream decisions.

### Example 2

Partition watermarks are 400, 390, and 250. The active-input minimum is 250. Computing one global maximum timestamp and subtracting a delay could approach 400 and misclassify valid records from the third partition.

### Example 3

At 2,000 events/s, a join retains 150-byte physical entries from its fast side while the other side's watermark stalls for 15 minutes. The base buffered state is $2000\times900\times150=270$ MB before indexes, matching side, checkpoint, replication, and headroom.

### Example 4

An idle timeout removes partition B when A is at watermark 600 and B at 300; output advances to 600. B resumes with event timestamp 350. Output cannot regress, so the record is late even though it advances B's own observed maximum.

### Example 5

An authenticated source marker says all records through 10:00 have been emitted, but it shares no order with records on other partitions. It safely advances only its governed partition unless the producer protocol proves a coordinated cut.

### Example 6

Two joined streams have watermarks 900 and 700. A minimum policy exposes 700 and retains fast-side data; a maximum policy exposes 900 and makes slow-side records up to 900 late. The second choice changes results, not merely latency.

### Example 7

A watermark hold at event time 480 represents a pending asynchronous lookup while input progress reaches 600. Output stays constrained by 480. If the callback is lost and the hold is never released/cancelled, event-time progress stalls despite healthy sources.

### Example 8

A bounded reader finishes nine of ten splits and emits terminal progress. The last split later produces finite events, all now late. Terminal progress requires coordinated proof that all discoverable splits and retries are exhausted.

### Example 9

An adaptive policy observes a healthy hour with p99 lateness 20 seconds and shrinks its delay. A disconnected device cohort returns with two-hour-old events. The estimator never observed that future tail while choosing; shadow violation curves and minimum incident bounds prevent false confidence.

### Example 10

This fixture demonstrates per-partition candidates, active-input minimum, idleness, non-regression, and late resumption.

<!-- bijux-verify: {"id":"watermark-idle-resume","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"emitted=(70, 70, 120, 120)\npartition_watermarks={'p0': 120, 'p1': 75}\nactive=('p0', 'p1') resumed_event=85 late=True\n","stderr":""}} -->
```python
bound = 10
partition_watermarks = {"p0": None, "p1": None}
active = ("p0", "p1")
output_watermark = None
emitted = []

def observe(partition, event_time):
    candidate = event_time - bound
    previous = partition_watermarks[partition]
    partition_watermarks[partition] = (
        candidate if previous is None else max(previous, candidate)
    )

def emit():
    global output_watermark
    candidates = [partition_watermarks[p] for p in active]
    if None in candidates:
        return
    merged = min(candidates)
    output_watermark = (
        merged if output_watermark is None else max(output_watermark, merged)
    )
    emitted.append(output_watermark)

observe("p0", 100)
observe("p1", 80)
emit()
observe("p0", 130)
emit()
active = ("p0",)
emit()
active = ("p0", "p1")
resumed_event = 85
observe("p1", resumed_event)
emit()
late = resumed_event <= output_watermark

print(f"emitted={tuple(emitted)}")
print(f"partition_watermarks={partition_watermarks}")
print(
    f"active={tuple(sorted(active))} resumed_event={resumed_event} "
    f"late={late}"
)
```

The fixture validates one integer model and an explicit inclusive late boundary. It does not implement distributed ordering, source guarantees, timers, holds, checkpointing, fencing, dynamic discovery, alignment, adaptive estimation, or downstream corrections.

## Cross-Program Connections

- **Distributed Systems:** logical time, partial-order frontiers, failure detectors, leases, fencing, epochs, consistent cuts, and monotonicity underpin progress.
- **Data Engineering:** source timestamps, CDC resolve points, broker partitions, backfills, joins, late corrections, and reconciliation define source evidence.
- **Database Systems:** low-water marks, MVCC visibility, compaction horizons, temporal tables, and transaction frontiers echo the same safe-reclamation problem.
- **Reliability Engineering:** stalls, skew, tail delay, backpressure, state capacity, checkpoint/restore, and fault injection determine operational behavior.
- **Security Engineering:** marker authentication, timestamp validation, partition authorization, anti-replay, quotas, and topology control protect progress integrity.
- **Platform Engineering:** connector capabilities, watermark APIs, alignment groups, idle policy, configuration rollout, and telemetry make progress a governed service.
- **API and Service Engineering:** cursors, deadlines, pagination completion, webhook retry horizons, and freshness promises require equally scoped progress claims.
- **Systems Engineering:** latency, completeness, state, cost, liveness, security, topology, and downstream mutability form one control problem.

## References

1. Akidau, T., et al. [“The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing.”](https://research.google/pubs/the-dataflow-model-a-practical-approach-to-balancing-correctness-latency-and-cost-in-massive-scale-unbounded-out-of-order-data-processing/) PVLDB, 2015. Foundational event-time, watermark, trigger, refinement, and latency/completeness/cost model.
2. Akidau, T., et al. [“MillWheel: Fault-Tolerant Stream Processing at Internet Scale.”](https://research.google/pubs/millwheel-fault-tolerant-stream-processing-at-internet-scale/) PVLDB, 2013. Low-watermarks, source progress, pending work, timers, persistence, and recovery foundations.
3. Apache Beam. [Beam Programming Model Basics.](https://beam.apache.org/documentation/basics/) Current concepts for event time, processing time, watermarks, windows, late data, and event-time timers.
4. Apache Beam. [Programming Guide.](https://beam.apache.org/documentation/programming-guide/) Current watermarks/late-data, window, trigger, state, timer, and timestamp contracts.
5. Apache Beam. [Python Watermark Estimators API.](https://beam.apache.org/releases/pydoc/current/apache_beam.io.watermark_estimators.html) Current manual, monotonic, observed-timestamp, and wall-time estimator behavior for splittable processing.
6. Apache Beam. [Runner Authoring Guide.](https://beam.apache.org/contribute/runner-guide/) Primary runner contract for input/output watermarks, pending elements, holds, timers, bundles, and checkpointed work.
7. Apache Flink. [Generating Watermarks.](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/event-time/generating_watermarks/) Current per-partition generation, merging, idleness, alignment, periodic/punctuated generation, and operator propagation behavior.
8. Apache Flink. [Built-in Watermark Generators.](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/event-time/built_in/) Current monotonous and bounded-out-of-orderness generator semantics.
9. Apache Flink. [BoundedOutOfOrdernessWatermarks API.](https://nightlies.apache.org/flink/flink-docs-stable/api/java/org/apache/flink/api/common/eventtime/BoundedOutOfOrdernessWatermarks.html) Current bound and periodic-emission contract.
10. Apache Flink. [WatermarkStrategy API.](https://nightlies.apache.org/flink/flink-docs-stable/api/java/org/apache/flink/api/common/eventtime/WatermarkStrategy.html) Current no-watermark, bounded, monotonous, idleness, and alignment strategy API.
11. Apache Spark. [Structured Streaming: Operations on Streaming DataFrames and Datasets.](https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html) Current event-time windows, watermark state cleanup, late data, and multi-stream watermark policies.
12. Apache Spark. [Structured Streaming Programming Guide.](https://spark.apache.org/docs/latest/streaming/index.html) Current execution, fault-tolerance, event-time, stateful processing, and operational model entry point.
13. Murray, D. G., et al. [“Naiad: A Timely Dataflow System.”](https://www.microsoft.com/en-us/research/publication/naiad-a-timely-dataflow-system/) SOSP, 2013. Progress tracking with logical timestamps, capabilities, and frontiers in cyclic dataflows.

## Exercises

### Exercise 1

Three active partitions have maximum observed event times 500, 460, and 530 seconds and respective disorder allowances 20, 40, and 10 seconds. Their previous watermarks are 470, 430, and 500. Compute each new nondecreasing watermark and the minimum merged watermark.

### Exercise 2

A two-input join receives 3,000 fast-side records/s, each retaining 180 physical bytes, while the slow input's watermark stalls for 12 minutes. Estimate base fast-side buffered state. Explain missing terms and how alignment changes throughput and state rather than accuracy.

### Exercise 3

An input watermark is 900, an operator has pending output work at event time 760, and its prior output watermark is 700. Using the module's abstract hold model, compute the safe next output watermark. Explain what must happen before it can advance to 900.

### Exercise 4

A partition at watermark 300 is declared idle while another advances output to 650. The partition resumes with events 340, 700, and 620 under a `timestamp <= watermark` late convention and a non-regressing output. Classify them on arrival and state the operational steps for safe resumption.

### Exercise 5

Design a production watermark review for a six-partition mobile-event source joined with a transactional payment stream. Cover evidence strength, per-partition state, idleness, merge policy, alignment, backfill, checkpoint/upgrade, security, late outputs, state sizing, and validation.

## Answers to the Exercises

### Answer 1

Candidates are $500-20=480$, $460-40=420$, and $530-10=520$. Applying non-regression gives `max(470,480)=480`, `max(430,420)=430`, and `max(500,520)=520`. The active minimum is 430. The second partition's newer candidate fell below its prior frontier, so it cannot pull its own or merged emitted progress backward.

### Answer 2

Twelve minutes is 720 seconds. Base retained entries are $3000\times720=2{,}160{,}000$ and bytes are $2{,}160{,}000\times180=388{,}800{,}000$, or 388.8 MB decimal. This excludes keys/values on the other side, indexes, allocator/backend amplification, timers, checkpoints, replication, skew, and headroom. Alignment can pause/throttle the fast input to bound relative drift and buffer growth, but it reduces source throughput and does not validate either timestamp or watermark.

### Answer 3

The input permits 900, but pending output at 760 constrains the next output to `max(700,min(900,760))=760`. The lookup/buffer/timer responsible for the hold must complete, fail through an explicit policy, or be durably cancelled so no accepted work can later emit at/before the released frontier. Then a later emission may reach 900 after preceding outputs are processed.

### Answer 4

Output cannot regress from 650. Events 340 and 620 satisfy `e<=650` and are late; event 700 is ahead and is not late under this convention. Safe resumption fences stale ownership, verifies the assignment epoch, restores/reinitializes per-partition generator state without reducing output, validates timestamps, sends old records through update/retraction/quarantine/drop policy, updates metrics, and avoids treating the partition as on-time until its local evidence catches up. A separate epoch/rebuild is needed if old records must be on-time.

### Answer 5

Document mobile watermarking as an estimate based on validated device event time and observed disorder, while treating a payment source's transactional resolve frontier according to its source guarantee. Maintain six mobile partition states plus payment splits by stable identity; merge relevant active inputs conservatively unless loss from a faster policy is approved. Define idle leases and returning-old-data behavior, align fast payments/mobile cohorts when join state threatens capacity, and isolate historical backfills. Persist or reconstruct maxima, emitted frontiers, active epochs, markers, and holds; shadow rule upgrades and rehearse restore/reassignment. Validate future poisoning, forged markers, sparse keepalives, partition creation, and stale owners. Define stable join result identity and late upsert/retraction/adjustment semantics. Size unmatched state from rate, watermark spread, lateness/outage tails, entry amplification, checkpoints, and headroom. Test deterministic permutations, pause/resume, marker disorder, skew, duplicates, failures, recovery, and eventual authoritative reconciliation while monitoring per-input progress, violations, holds, state, and user-visible differences.
