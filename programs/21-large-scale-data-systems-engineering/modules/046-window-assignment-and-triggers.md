---
module_id: LSDS-046
program: Large-Scale Data Systems Engineering
level: 1
module_number: 46
title: Window Assignment and Triggers
status: complete
last_verified: 2026-09-04
---

# Window Assignment and Triggers

## One-Page Review

### Governing question

How can an unbounded dataflow assign events to finite logical groups and emit useful results repeatedly without confusing membership, firing, accumulation, lateness, cleanup, or downstream finality?

### Essential definitions

- A **window assigner** maps an element's event time and key to one or more logical windows; it answers membership, not when output appears.
- A **tumbling/fixed window** partitions time into equal nonoverlapping half-open intervals.
- A **sliding window** has a duration and slide; intervals can overlap, so one element may belong to several windows.
- A **session window** groups per-key events separated by less than a gap and can merge when a bridging event arrives.
- The **global window** places all elements together and therefore needs a non-default trigger and explicit state bound for unbounded input.
- A **trigger** decides when a window emits a **pane**, based on event-time progress, processing time, element count, data condition, or composition.
- A **pane** is one firing's output for a window and may be early, on-time, or late under the runtime's model.
- **accumulating mode** emits a result incorporating prior pane data; **discarding mode** emits only data since the previous firing.
- **allowed lateness** preserves a window's ability to accept updates after its event-time frontier; it is not a watermark delay.
- **purge/cleanup** removes trigger or window state. Firing, purging, finality, and durable deletion are separate events.

### Central model, mechanism, or theorem

For half-open fixed windows of width $D$ and origin $O$, exact event time $t$ belongs to

$$b=O+\left\lfloor\frac{t-O}{D}\right\rfloor D,\qquad W(t)=[b,b+D).$$

For sliding width $D$ and slide $S$, an event belongs to every aligned start $b=O+kS$ satisfying $b\le t<b+D$; membership amplification is at most $\lceil D/S\rceil$ under ordinary fixed-duration alignment. Session membership is data-dependent: per key, event intervals such as $[t,t+G)$ are merged when they overlap, so late bridging data can change window identity.

A trigger is a state machine $T(window,state,event,watermark,clock)\rightarrow(action,new\ state)$ whose action can continue, fire, purge, or fire-and-purge. Correct output also specifies accumulation, pane identity/version, timestamp, late-update policy, cleanup, and sink mutation semantics. Window assignment alone neither produces results nor establishes finality.

### Critical invariants

- Assignment uses recorded event time, key, origin, duration/slide/gap, boundary convention, calendar/zone, and version deterministically.
- Every element belongs to the declared number of windows; boundary timestamps are neither lost nor double-assigned accidentally.
- Window identity is stable and carries key plus interval/session identity; output identity additionally carries pane/version semantics.
- Trigger state and timers are managed, bounded, checkpointed, and deterministic under the promised replay model.
- Early firing does not claim completeness; on-time firing is relative to watermark behavior; late firing is an update, not a duplicate to ignore blindly.
- Accumulating versus discarding output matches the aggregation algebra and downstream interpretation.
- Allowed lateness, state cleanup, trigger purge, dedup horizon, and downstream correction horizon are mutually compatible.
- Session merges reconcile prior panes/state and stable output identities rather than leaving double-counted sessions.
- Processing-time triggers are latency aids whose exact timing can change on replay/recovery.
- Sinks can represent the selected append, upsert, retraction, or adjustment stream and converge after retries.

### Common failures

Common failures include using closed intervals on both sides; aligning by worker-local midnight; assuming one window per event; ignoring sliding-window amplification; treating a trigger as an assigner; treating every pane as a final independent result; summing accumulating panes; discarding prior data when a cumulative result is expected; using a global window with no bounded trigger/state; assuming event-time firing occurs at wall-clock window end; equating allowed lateness with watermark delay; purging state before retries/corrections finish; failing to merge late sessions; letting processing-time trigger jitter change business truth; and writing updates to an append-only sink without version or retraction semantics.

### Compact example

With origin 0 and ten-second tumbling windows, event times 1, 4, and 7 belong to `[0,10)` and 12 belongs to `[10,20)`. An accumulating count trigger fires early after two elements with result 2, then at watermark 10 with result 3. Summing those panes would incorrectly report 5; consumers must upsert the window from 2 to 3. At watermark 20, the second window emits 1. If a later event at time 6 is accepted, it produces another version for `[0,10)`, not a new independent window total.

### Connections

[LSDS-044](044-event-time-processing.md) defines timestamps and late evidence; [LSDS-045](045-watermarks.md) defines progress. [LSDS-043](043-stateful-operators.md) provides state/timers. [LSDS-047](../ROADMAP.md) through [LSDS-050](../ROADMAP.md) connect panes to checkpoint recovery, replay, and effect-safe sinks.

## Governing Question

Unbounded input cannot be grouped with an ordinary “collect everything, then aggregate” operation. Windows create finite logical scopes, but finite membership does not imply finite processing time: late data can revise a window, and speculative outputs can appear before completeness. A useful streaming result therefore needs several independent decisions.

First, which window or windows contain an element? Second, when should current state be emitted? Third, does each firing contain only new data or the accumulated result? Fourth, how long can late data update state? Fifth, when is state reclaimed? Sixth, how do downstream systems distinguish versions, replacements, retractions, and final results?

Libraries often make a simple tumbling count look like one API call, hiding these contracts in defaults. Defaults vary across runtimes and versions. A pipeline can pass tests yet double-count in production because an append-only sink receives accumulating panes, or lose data because a watermark cleans state before a retry horizon ends.

The governing question is how to specify window topology, trigger state machines, pane semantics, state lifecycle, and downstream convergence as one reviewable design whose latency and cost are measured rather than guessed.

## Why This Matters

Windows make continuously changing data intelligible: requests per minute, revenue per billing day, rolling error rate, user sessions, and correlations within an interval. Early triggers reduce perceived latency. Event-time triggers make output follow data progress. Late panes let systems refine provisional answers instead of waiting indefinitely.

The flexibility multiplies state. A sliding window with one-hour width and one-minute slide can assign each event to 60 windows. A full-buffer window retains every element; an incremental associative aggregate may retain one accumulator. Sessions can merge after outputs have been published, forcing retractions or stable replacement logic.

Correctness crosses system boundaries. A runtime might faithfully emit pane 1 and pane 2, while a sink retries pane 1 or a consumer sums cumulative panes. “Exactly once” within the operator does not establish the meaning of a dashboard, database table, alert, invoice, or external notification.

Time zones and calendars add product semantics. “Daily” can mean 24-hour UTC buckets, local civil days of 23/24/25 hours, market calendars, or tenant business periods. Choosing fixed milliseconds for a legal local day can silently move facts across reporting boundaries.

## Prerequisites and Retrieval

Review timestamp provenance, uncertainty, replay, correction, and backfill in [LSDS-044](044-event-time-processing.md); watermark meaning, idleness, composition, and late boundaries in [LSDS-045](045-watermarks.md); and keyed/window/timer state in [LSDS-043](043-stateful-operators.md). Retrieve aggregation algebra and combiners from [LSDS-023](023-partitioners-and-combiners.md) and [LSDS-038](038-distributed-aggregation.md).

You should understand half-open intervals, floor/ceiling, modular alignment, associative/commutative aggregation, event versus processing time, stable identity, watermarks, state cleanup, idempotency, upserts, retractions, and checkpoint replay.

## Learning Objectives

After this module, you should be able to:

1. compute deterministic tumbling and sliding membership with origin and half-open boundaries;
2. explain session construction, gap semantics, late bridging, and mergeable state/output requirements;
3. separate window assignment from triggers, panes, accumulation, allowed lateness, purge, and cleanup;
4. design event-time, processing-time, count/data-driven, repeated, and composite triggers as bounded state machines;
5. choose incremental aggregation versus full buffering from algebra and access requirements;
6. give panes stable identities and select append, upsert, retraction, or adjustment semantics;
7. estimate assignment, state, timer, output, checkpoint, and correction amplification;
8. handle calendar windows, zones, uncertainty, empty windows, hot keys, and global windows explicitly;
9. test replay, recovery, retries, late updates, session merges, and downstream convergence; and
10. observe and secure trigger/window configuration, state, firing delay, pane churn, and lifecycle.

## Core Exposition

### Separate the six contracts

Write six fields before selecting an API: assignment, trigger, accumulation, allowed lateness, cleanup/purge, and output mutation. Two pipelines with identical fixed windows can differ completely because one emits a single append after progress while another emits repeated accumulating upserts.

Assignment is pure logical membership. Triggering observes state/progress/clock to request output. Accumulation defines pane contents. Allowed lateness governs post-frontier updates. Cleanup governs state lifetime. Output mutation tells consumers how pane versions converge.

Document defaults explicitly. An upgrade that changes a default is then detected as a contract change rather than an invisible runtime detail.

### Use half-open intervals

Prefer `[start,end)` so adjacent fixed windows partition exact instants without overlap. An event exactly at end belongs to the next interval. Declare timestamp precision and rounding before assignment; rounding after assignment can move boundary data inconsistently.

For width $D$ and origin $O$, floor division gives the aligned start. Negative timestamps require mathematical floor, not truncation toward zero. Test times immediately before, at, and after origin/boundaries and maximum/minimum representable values.

Do not infer completion from membership. `[0,10)` is mathematically bounded even if its records arrive forever late.

### Align fixed windows intentionally

Origins determine boundaries. Unix-epoch alignment, tenant signup time, exchange session start, and local civil midnight answer different questions. Persist origin and rule version as durable configuration.

Fixed-duration UTC windows are stable instants. Calendar windows depend on zone and calendar rules; local days can vary in duration and zone databases change. Preserve the civil label, zone, and rule version alongside UTC endpoints when humans or law care about the period.

If tenants use distinct origins/zones, assignment may increase configuration and state cardinality. Validate authorization so producers cannot choose arbitrary windows that evade retention or explode state.

### Account for sliding amplification

Sliding windows use width $D$ and slide $S$. With $S<D$, an event belongs to multiple aligned intervals. The typical upper membership count is $\lceil D/S\rceil$, subject to endpoint alignment. Ten-minute width and five-minute slide gives up to two; one hour and one minute gives up to 60.

Naively duplicating per-window state multiplies CPU, bytes, timers, checkpoints, and outputs. Algebraic pane decomposition can aggregate smaller base intervals and combine them, trading read/merge complexity for lower write amplification.

Measure actual key and event distributions. A small average hides bursts where every event fans into the maximum number of windows.

### Design session identity and merging

Session windows are keyed and data-dependent. Model each event as interval `[t,t+gap)` (or the runtime's declared endpoint convention) and merge overlapping intervals. A late event can bridge two sessions previously considered separate.

Merging requires mergeable trigger state, timers, aggregation state, and output semantics. If sessions A and B were published and then become C, downstream needs retractions for A/B plus C, or stable logical identities and a reconciliation/upsert scheme. Choosing the earliest start as identity can still change when older data arrives.

Dynamic gaps must be positive, bounded, deterministic, and versioned. A producer-controlled huge gap can create unbounded state.

### Treat the global window as unbounded

The global window is convenient for running totals, custom sessions, or non-time triggers, but it does not bound state. A default event-time trigger may never produce meaningful finality on unbounded input.

Use incremental sufficient state, periodic/count triggers, explicit retention, and a result contract such as current running value. If the computation requires every historical element, externalize/bound history or admit that storage grows with input.

Global state and global output hotspots also defeat key parallelism; partition and merge only when the aggregation algebra supports it.

### Model triggers as state machines

A trigger observes an element, watermark, processing clock, or composition state and returns continue, fire, purge, or fire-and-purge. It registers/cancels managed timers and persists counters/flags with the window.

Specify whether it fires once or repeatedly, which subtrigger can finish, how repetitions reset, and how merged windows combine trigger state. Hidden “finished” bits can prevent late firing after a session merge.

Trigger callbacks may be retried after failure. Pane/output identity must make repeated execution safe; a trigger is not an exactly-once external notification service.

### Use event-time triggers for progress

An event-time trigger commonly fires when the input watermark passes the window end. This is “on-time” relative to that watermark, not wall-clock punctuality or guaranteed completeness. A stalled watermark delays firing; an early watermark makes later records late.

The exact equality comparison and maximum timestamp conventions vary. Test the runtime boundary rather than relying on informal phrases such as “at window end.”

Event-time firing can be followed by late firings while state remains within allowed lateness. Consumers must expect multiple versions if this is enabled.

### Use processing-time triggers for responsiveness

A processing-time trigger can emit a pane a duration after the first element or periodically. It provides low-latency speculative results when event-time progress is slow.

Wall-clock scheduling, load, checkpoint recovery, and downtime can shift or bunch firings. Replay on another day may produce a different number and grouping of early panes. Keep the eventual event-time result semantically stable and label processing-time panes provisional.

Bound timer count: one timer per element is usually expensive; coalesce per key/window and cancel obsolete timers.

### Use count and data-driven triggers carefully

A count trigger fires after $N$ observed elements, independent of event-time completeness. It is useful for progress visibility and batching but skew makes latency variable: hot keys fire constantly while cold keys wait forever.

Counts under replay require trigger state and input recovery to align. Duplicate delivery can reach the threshold early unless the runtime rolls state back consistently or input is deduplicated.

Data-driven triggers such as convergence or threshold crossing encode domain behavior. Define monotonicity, hysteresis, retraction, numerical tolerance, and adversarial inputs so one event cannot cause unbounded pane churn.

### Compose early, on-time, and late behavior

A common composite emits early processing/count panes until the watermark reaches window end, then an on-time pane, then repeated late panes until cleanup. Specify which subtriggers repeat and whether firing resets their state.

Pane timing is separate from contents. In accumulating mode, early count 2 followed by on-time count 3 represents replacement 2→3. In discarding mode, panes might contain 2 then 1 and require summing for a total—unless retries duplicate a pane.

Pane timing labels are runtime-relative metadata, not business truth. A watermark can make an “on-time” pane incomplete.

### Match accumulation to algebra

Accumulating panes simplify current-value upserts: every pane carries the aggregate so far. They can repeat large outputs and must not be summed downstream. Discarding panes reduce repeated data but consumers must combine deltas exactly once or idempotently.

Accumulating-and-retracting models emit changes that reverse prior results, useful for nonmonotone updates but more complex. Choose based on sink capabilities and algebra, not preference.

Record pane index/version, timing, window/key, accumulation mode, and result schema. If an engine's pane index is not stable across recovery, derive durable business version/identity separately.

### Aggregate incrementally when possible

Associative combine functions retain compact accumulators and can merge across workers/windows. Count, sum, min/max, and sufficient statistics often qualify, with numerical/order caveats. Full-window process functions retain all elements when arbitrary ordering or cross-element logic is required.

Full buffering increases memory/disk, serialization, checkpoint, restore, and privacy exposure. Sorting a window adds $O(n\log n)$ work and needs deterministic tie-breaking. An evictor that inspects individual elements may disable pre-aggregation.

State choice is a semantic proof: show that the accumulator contains all information required for every firing and late merge.

### Define allowed lateness and cleanup

Allowed lateness keeps window state after the initial event-time boundary so accepted late elements can update results. It is distinct from the watermark generator's delay. Specify strict comparison at window end plus allowance.

Cleanup must remove aggregation state, trigger counters, timers, pane metadata, buffered elements, indexes, and any dedup/correction state only when their contracts permit. Logical expiry can precede physical deletion.

Trigger purge may clear pane contents before the window's lifecycle ends. Do not assume fire-and-purge equals final output or secure erasure. Backups, checkpoints, sinks, and correction ledgers retain separate copies.

### Handle too-late data explicitly

Data arriving after cleanup cannot update absent state without reconstruction. Route it to a governed side output, correction workflow, immutable adjustment, quarantine, or measured drop. Side output needs retention, ownership, retry, observability, and access control.

If exact correction is required, retain/reconstruct enough input and state or rebuild the affected window in a new version. Do not silently recreate an empty window and call its partial aggregate a correction.

Distinguish source-invalid timestamps, watermark-late but accepted data, and beyond-retention data; their remediation differs.

### Design stable output identity

Use identity such as `(job/materialization version,key,window identity,result kind)` plus an ordered pane/result version. Fixed window identity can use canonical endpoints. Session identity needs a merge-aware scheme or explicit retractions of superseded identities.

Append sinks suit truly single/final immutable outputs. Upsert sinks replace a current window row. Retraction streams reverse previous rows. Ledgers append adjustments. Every protocol needs idempotency for retries and conflict rules for out-of-order pane delivery.

“Final” should be a scoped flag with frontier, lateness policy, correction policy, and version; future authorized corrections may still create a new assertion.

### Bound output and state amplification

Cost includes input rate times window membership, keys/windows, accumulator or raw-element bytes, trigger/timer metadata, allowed-lateness horizon, session merge work, pane frequency/size, checkpoint/replication, corrections, and headroom.

Early triggers can reduce user latency while multiplying sink writes. A hot key with one pane per element becomes an output denial of service. Set minimum periods/counts, coalesce updates, apply quotas, and preserve an authoritative later result.

Measure tail windows per event, active windows per key, elements/state bytes per window, timer count, pane count, merge fan-in, correction rate, and cleanup backlog.

### Recover and replay semantics

Checkpoint window contents/accumulators, trigger state, timers, pane/version metadata, session merge state, and source positions consistently. Recovery can re-fire a pane or delay a processing timer; external writes still need idempotency/transactions.

Event-time assignment and final aggregate should reproduce from captured input/rules. Processing-time early pane boundaries may be intentionally non-reproducible; document which outputs are authoritative and suppress external irreversible effects from speculative panes.

Upgrades to duration, slide, origin, gap, trigger, accumulation, lateness, or output identity are semantic migrations. Shadow/rebuild rather than restoring incompatible window state blindly.

### Secure and observe the lifecycle

Validate event time, keys, gap/window configuration, and tenant calendars before allocation. Bound windows per event, active windows/key, raw elements, timers, late updates, and panes. Prevent users from selecting tiny slides, huge gaps, or high-frequency triggers without quota.

Observe assigned and dropped counts, membership amplification, active/expired windows, state bytes/age, watermark-to-fire delay, processing timer delay, early/on-time/late panes, pane versions/retries, session merges, late side outputs, cleanup backlog, sink conflicts, and end-to-end freshness.

Trace sampled records through assignment, pane versions, cleanup, and sink convergence without leaking sensitive keys or timestamps.

### Validate boundary and failure behavior

Test just before/at/after every boundary, negative epochs, time-zone gaps/folds, calendar changes, empty windows, ties, duplicate/reordered events, watermark leaps/stalls, late bridging sessions, exact cleanup thresholds, hot keys, and maximum membership.

Inject failure before/after trigger state update and sink write, timer recovery, session merge, checkpoint, rescale, and rule upgrade. Deliver pane versions out of order and duplicated. Verify the sink converges and no trigger state leaks.

Use production-derived distributions to benchmark state, checkpoint, restore, merge, and output cost. Correct toy arithmetic is not capacity evidence.

## Definitions and Notation

Let event $i$ have time $t_i$ and key $k_i$. A window assigner $A(t_i,k_i;v)$ returns a finite set of window identities under rule version $v$.

For fixed width $D>0$ and origin $O$, $b=O+\lfloor(t-O)/D\rfloor D$ and $A(t)=\{[b,b+D)\}$. For sliding width $D>0$ and slide $S>0$, $A(t)=\{[O+nS,O+nS+D):O+nS\le t<O+nS+D\}$.

For session gap $G>0$, each keyed event contributes interval $[t_i,t_i+G)$; the session set is the union of connected overlapping intervals under the declared endpoint rule. Changing $G$ can change the entire partitioning.

For key-window pair $(k,w)$, state $s_{k,w}$ includes accumulator/content, trigger state, timers, pane metadata, and cleanup metadata. A trigger action belongs to `{continue, fire, purge, fire-and-purge}`. Pane identity $P=(materialization,k,w,r)$ includes durable result version $r$ even if runtime pane metadata is weaker.

If input rate is $\lambda$, maximum memberships/event $m$, physical state contribution $b$, and effective retention $R$, a crude upper base is $\lambda m b R$ before aggregation reduction, keys, indexes, timers, checkpoints, replication, skew, and headroom.

## Mechanisms, Invariants, or Proof Structure

Audit a design in this order:

1. **Time domain:** establish event-time provenance, precision, zone/calendar, uncertainty, and version.
2. **Assignment:** prove boundary coverage, membership count, origin, key scope, session gap/merge, and determinism.
3. **Computation:** select sufficient accumulator or justify full buffering/order.
4. **Trigger:** specify inputs, timers/state, repetition/finish, merge, and fire/purge actions.
5. **Pane contents:** declare accumulating, discarding, retracting, and early/on-time/late meaning.
6. **Progress/lateness:** pin watermark equality, allowed lateness, late acceptance, and reconstruction/drop behavior.
7. **Lifecycle:** align cleanup of state/timers/dedup with checkpoint, retry, correction, retention, and deletion.
8. **Output:** prove stable identity, ordering/conflict handling, idempotency, and sink/consumer convergence.
9. **Capacity/security:** bound membership, raw state, timers, panes, merges, hot keys, and user configuration.
10. **Evidence:** test boundaries/replay/failures/upgrades and measure result, latency, state, and cost distributions.

Fixed half-open coverage follows because floor selects exactly one integer $n$ with $O+nD\le t<O+(n+1)D$. Sliding assignment deliberately relaxes uniqueness; every matching aligned start must be enumerated exactly once.

Trigger correctness is conditional: a firing is correct only relative to its trigger state and input/progress contract. It does not imply completeness. Downstream correctness additionally requires interpreting pane accumulation and versions correctly.

Cleanup safety requires proof that no accepted future event, retry, timer, merge, or correction needs the deleted state—or a reconstruction path that restores it. A watermark alone is insufficient when allowed lateness or external correction remains.

## Alternatives and Trade-Offs

**Tumbling windows** give one membership and simple identity. **Sliding windows** provide rolling views with multiplication cost. **Sessions** match activity bursts but require merging and unstable boundaries. **Global windows** support running/custom logic while providing no time bound.

**Fixed UTC duration** is deterministic and uniform. **Civil calendar windows** match human/legal periods but require zone/calendar versioning and variable duration. **Per-tenant calendars** improve semantics at configuration/cardinality cost.

**Event-time trigger** follows data progress but stalls with watermarks. **Processing-time trigger** improves responsiveness but is replay/scheduling-dependent. **Count/data trigger** reacts to volume/content but gives variable latency and no completeness.

**Accumulating panes** are easy current-value replacements but expensive and dangerous to sum. **Discarding panes** are compact deltas but need exactly-once/idempotent combination. **Retractions/adjustments** represent nonmonotone changes at greater consumer complexity.

**Incremental aggregation** bounds state for suitable algebra. **Full buffering** enables arbitrary inspection/order at high state/checkpoint/privacy cost. **Pane decomposition** reduces sliding duplication while increasing merge/query complexity.

**Long allowed lateness** supports more corrections but retains state and produces churn. **Short lateness** bounds cost but shifts data to reconstruction/drop. **Rebuild-on-correction** keeps live state small but adds archival availability and latency.

## Failure Modes and Misconceptions

1. **“A window closes at wall-clock end.”** Event-time output follows progress and trigger semantics.
2. **“Both endpoints can be inclusive.”** Adjacent windows then double-own boundary events.
3. **“Every event has one window.”** Sliding assignment deliberately multiplies membership.
4. **“Windowing decides when to emit.”** Assignment and trigger are separate.
5. **“A trigger result is final.”** Early and late panes can revise it.
6. **“On-time means complete.”** It means relative to a watermark estimate/guarantee.
7. **“Allowed lateness slows the watermark.”** It extends update/state policy after progress.
8. **“Fire means purge.”** Actions and cleanup are distinct.
9. **“Purge means erased everywhere.”** checkpoints, sinks, and backups remain.
10. **“Accumulating panes should be summed.”** They already include prior data.
11. **“Discarding panes are naturally exactly once.”** retries can duplicate deltas.
12. **“Sessions never change after emission.”** late bridging events can merge them.
13. **“Session start is stable identity.”** earlier events can move it.
14. **“Global window bounds global state.”** It does the opposite without other controls.
15. **“Processing-time panes replay exactly.”** timing and recovery can regroup them.
16. **“Full buffering is harmless for small averages.”** tails and hot keys dominate.
17. **“Append sinks accept late updates.”** repeated results need versions/retractions/adjustments.
18. **“Exactly-once operator means exactly-once alert.”** external effects need their own protocol.
19. **“Daily always means 24 hours.”** civil days and business calendars vary.
20. **“Changing a slide is configuration only.”** it changes state, identity, results, and cost.

## Worked Examples

### Example 1

For origin 0 and width 10, timestamps 0 and 9 belong to `[0,10)`; 10 belongs to `[10,20)`. Half-open boundaries give exact coverage without duplication.

### Example 2

With width 10 and slide 5, timestamp 12 belongs to `[5,15)` and `[10,20)`. It does not belong to `[0,10)` because 12 is beyond its end.

### Example 3

One-hour windows sliding every minute assign an event to at most 60 windows. At 50,000 events/s, naive assignment attempts up to three million memberships/s before aggregation.

### Example 4

Per-key events at times 1 and 9 with gap 5 create sessions `[1,6)` and `[9,14)`. A late event at 5 contributes `[5,10)`, overlaps both, and merges them into `[1,14)` under half-open overlap.

### Example 5

An accumulating trigger emits counts 2, 5, then 6. The current answer is 6, not 13. An upsert sink replaces the same window row using increasing result versions.

### Example 6

A discarding trigger emits deltas 2, 3, then 1. Summing yields 6 only if each pane is applied once; a retry of delta 3 produces 9 unless pane identity deduplicates it.

### Example 7

A processing-time trigger scheduled five minutes after the first element fires eight minutes later during overload. This affects speculative latency, not event-time membership. Monitoring records scheduled and actual fire time.

### Example 8

A window ends at 600 with allowed lateness 120. State remains correction-capable until the declared cleanup comparison around frontier 720. Exact equality is tested because `<`, `<=`, `>`, and `>=` differ at one instant.

### Example 9

A pane is written successfully but acknowledgment is lost before checkpoint completion. Recovery fires it again. Stable `(materialization,key,window,result_version)` makes the sink idempotently replace/deduplicate rather than sending two alerts.

### Example 10

This fixture assigns fixed windows and emits an early accumulating pane plus event-time panes.

<!-- bijux-verify: {"id":"fixed-window-trigger-panes","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"assignments=((1, 0), (4, 0), (7, 0), (12, 10))\npanes=((0, 'early', 2), (0, 'on_time', 3), (10, 'on_time', 1))\n","stderr":""}} -->
```python
events = (1, 4, 7, 12)
width = 10
counts = {}
assignments = []
panes = []

for event_time in events:
    start = (event_time // width) * width
    assignments.append((event_time, start))
    counts[start] = counts.get(start, 0) + 1
    if counts[start] == 2:
        panes.append((start, "early", counts[start]))

for watermark in (10, 20):
    start = watermark - width
    if start in counts:
        panes.append((start, "on_time", counts[start]))

print(f"assignments={tuple(assignments)}")
print(f"panes={tuple(panes)}")
```

The fixture proves one exact integer assignment and accumulating count schedule. It does not implement distributed watermarks, allowed lateness, cleanup, timer recovery, session merging, checkpointing, or sink idempotency.

## Cross-Program Connections

- **Data Structures:** interval indexes, heaps/timer wheels, hash maps, mergeable sets, logs, and sketches determine window state operations.
- **Distributed Systems:** logical time, progress, consistent snapshots, retries, deterministic replay, fencing, and idempotent effects govern pane recovery.
- **Database Systems:** group-by, materialized views, upserts, MVCC, temporal tables, retractions, and compaction mirror window lifecycle.
- **Data Engineering:** CDC timestamps, backfills, deduplication, sessionization, stream joins, reconciliation, and schemas shape assignment and correction.
- **Reliability Engineering:** watermark stalls, timer delay, hot keys, state/checkpoint growth, restore, and fault injection expose operational risk.
- **Security Engineering:** timestamp/config validation, quotas, tenant isolation, side-output access, retention, and audit constrain abuse.
- **Platform Engineering:** runtime APIs, calendar services, state backends, sink capabilities, rollout, and telemetry provide governed primitives.
- **Systems Engineering:** semantic periods, response latency, completeness, state, output churn, recovery, cost, and privacy are coupled.

## References

1. Akidau, T., et al. [“The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing.”](https://research.google/pubs/the-dataflow-model-a-practical-approach-to-balancing-correctness-latency-and-cost-in-massive-scale-unbounded-out-of-order-data-processing/) PVLDB, 2015. Foundational windowing, triggers, watermarks, accumulation, and refinement model.
2. Apache Beam. [Programming Guide: Windowing and Triggers.](https://beam.apache.org/documentation/programming-guide/) Current fixed, sliding, session/global windows, timestamps, triggers, accumulation, allowed lateness, state, and timers.
3. Apache Beam. [Beam Programming Model Basics.](https://beam.apache.org/documentation/basics/) Current conceptual model for windows, watermarks, panes, triggers, late data, and expiration.
4. Apache Beam. [Window Javadoc.](https://beam.apache.org/releases/javadoc/current/org/apache/beam/sdk/transforms/windowing/Window.html) Current window transform, trigger, allowed lateness, accumulation, timestamp combiner, and compatibility API.
5. Apache Beam. [Trigger Javadoc.](https://beam.apache.org/releases/javadoc/current/org/apache/beam/sdk/transforms/windowing/Trigger.html) Current trigger continuation, merge, and finished-state programming contract.
6. Apache Beam. [Runner Capability Matrix.](https://beam.apache.org/documentation/runners/capability-matrix/) Current runner support distinctions for windowing, triggers, accumulation, and allowed lateness.
7. Apache Flink. [Windows.](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/operators/windows/) Current assigners, triggers, evictors, functions, lifecycle, allowed lateness, side outputs, and late firing behavior.
8. Apache Flink. [Trigger API.](https://nightlies.apache.org/flink/flink-docs-stable/api/java/org/apache/flink/streaming/api/windowing/triggers/Trigger.html) Current fire, purge, merge, timer, and clear contract.
9. Apache Flink. [WindowAssigner API.](https://nightlies.apache.org/flink/flink-docs-stable/api/java/org/apache/flink/streaming/api/windowing/assigners/WindowAssigner.html) Current element assignment, trigger selection, merging, and time-context contract.
10. Apache Spark. [Structured Streaming: Operations on Streaming DataFrames and Datasets.](https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html) Current tumbling/sliding/session windows, watermark cleanup, output modes, dynamic gaps, deduplication, and multi-input behavior.
11. Apache Spark. [Window Functions API.](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.window.html) Current duration, slide, start offset, half-open interval, and precision behavior.
12. Apache Spark. [Session Window API.](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.session_window.html) Current static/dynamic gap session expression behavior.
13. Apache Flink. [Streaming Analytics: Windows and Late Events.](https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/streaming_analytics/) Current applied guidance for incremental/process functions, allowed lateness, and side outputs.

## Exercises

### Exercise 1

For origin 0, width 12, assign event times `-1, 0, 11, 12, 25` to half-open tumbling windows using mathematical floor. Explain the boundary result and why truncation toward zero fails for `-1`.

### Exercise 2

Windows have width 20 and slide 5. Enumerate windows containing timestamp 23 and give the maximum membership amplification. At 10,000 events/s with 64 physical bytes per membership and 30 seconds effective retention, estimate naive base state.

### Exercise 3

An accumulating trigger emits values 4, 9, and 10 for one key-window. Show correct upsert interpretation and the erroneous sum. Then give a safe interpretation if the panes instead were discarding deltas 4, 5, and 1.

### Exercise 4

With gap 6, keyed events at 2, 10, and later 6 contribute `[2,8)`, `[10,16)`, and `[6,12)`. Determine the final session and describe downstream changes if the first two sessions were already published.

### Exercise 5

Design a production review for tenant-local daily revenue with an early processing-time trigger, watermark on-time trigger, 24-hour correction allowance, accumulating panes, and an upsert sink. Cover calendar semantics, identity, state/cost, recovery, security, validation, and observability.

## Answers to the Exercises

### Answer 1

Starts are `-12, 0, 0, 12, 24`, so windows are `[-12,0)`, `[0,12)`, `[0,12)`, `[12,24)`, and `[24,36)`. Timestamp 12 belongs only to the next window because the prior end is exclusive. Truncating `-1/12` toward zero would choose start 0, whose interval does not contain -1; mathematical floor chooses -1 as the quotient and start -12.

### Answer 2

Aligned starts satisfying `b<=23<b+20` are 5, 10, 15, and 20, giving `[5,25)`, `[10,30)`, `[15,35)`, and `[20,40)`. Maximum amplification is $\lceil20/5\rceil=4$. Base state is $10{,}000\times4\times64\times30=76{,}800{,}000$ bytes, or 76.8 MB decimal, excluding keys, accumulators, indexes, timers, checkpoints, skew, and headroom.

### Answer 3

Accumulating panes replace the same result: version 1 is 4, version 2 is 9, and version 3/current is 10. Summing gives 23, which double-counts prior contributions. Discarding deltas 4, 5, and 1 sum to 10 only if each pane has stable identity and is applied exactly once/idempotently; out-of-order delivery needs ordered versions or a commutative deduplicated ledger.

### Answer 4

The late interval `[6,12)` overlaps `[2,8)` and `[10,16)`, so the connected union becomes `[2,16)`. If the first sessions were published, emit retractions/tombstones for their stable identities plus the merged result, or use a merge-aware reconciliation protocol that supersedes both. Simply appending the merged total leaves consumers double-counting three results.

### Answer 5

Define a day in each tenant's named zone/calendar with versioned rules, preserving civil label and UTC endpoints across 23/24/25-hour days. Identity includes materialization, tenant, canonical local date/window endpoints, metric, and ordered result version. Early processing panes are provisional; watermark panes remain correctable for 24 hours; accumulating outputs upsert rather than sum. Size active tenants/windows, event rates, accumulator/timer bytes, watermark delay, 24-hour state, pane frequency, checkpoints, retries, and headroom. Checkpoint state/timers/version with input positions and make sink writes idempotent; replay must reproduce authoritative aggregates though early timing may differ. Authorize tenant calendar/config, validate timestamps, quota triggers/windows, isolate tenants, and protect revenue/late outputs. Test zone folds/gaps/rule changes, exact endpoints, late corrections, watermark stall/leap, duplicate/out-of-order panes, crash around sink write, restore/rescale, and rule upgrade. Observe assignment errors, active state, watermark/fire delay, pane classes/versions/retries, correction rate, cleanup, sink conflicts, and final reconciliation.
