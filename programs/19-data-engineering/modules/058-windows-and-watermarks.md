---
module_id: DE-058
program: Data Engineering
level: 2
module_number: 58
title: Windows and Watermarks
status: complete
last_verified: 2026-09-03
---

# Windows and Watermarks

## One-Page Review

### Governing question

How should an unbounded, out-of-order stream be divided into finite event-time groups, when may each result be emitted or revised, and what evidence justifies releasing state without confusing a watermark estimate with proof that no older event can arrive?

### Essential definitions

- A **window** is a logical grouping boundary assigned from an event's timestamp, key, and a versioned window policy.
- A **tumbling window** is a fixed-size, non-overlapping, gapless interval; each event belongs to one interval under one alignment.
- A **hopping window** is a fixed-size interval started every hop; overlapping windows can assign one event to several groups.
- A **session window** groups per-key activity separated by less than a specified inactivity gap and may merge when bridging events arrive.
- The **global window** places all events for a key in one logical window and therefore needs an explicit trigger and retention policy for unbounded input.
- A **watermark** is a monotone event-time progress signal used by operators to decide when time-dependent work is eligible. Its strength depends on the source and contract.
- A **trigger** decides when a window emits a **pane**, an individual firing of that window's result.
- An **on-time pane** is associated with the watermark crossing the window end under the chosen runtime semantics; **early** and **late panes** occur before and after that point.
- **Allowed lateness** or a **grace period** is the event-time interval during which a runtime may retain window state and admit qualifying late updates after the window end.
- **Accumulation mode** defines whether a pane contains all accepted values so far or only values since the previous firing.
- A **retraction** or **upsert** tells a consumer how a later pane changes an earlier result.
- A **watermark hold** prevents downstream event-time progress from passing a timestamp for output that may still be produced.
- **Idleness detection** temporarily excludes a silent input from a minimum watermark calculation according to a timeout policy.
- **Watermark alignment** throttles inputs whose progress is too far ahead of slower inputs to control downstream buffering.
- A **finality contract** states whether a result is provisional, operationally closed, correctable, or immutable and what later evidence can change it.

### Central model, mechanism, or theorem

For event time $t$, origin $o$, tumbling size $S>0$, and integer

$$
k=\left\lfloor\frac{t-o}{S}\right\rfloor,
$$

the half-open window is $[o+kS,o+(k+1)S)$. For a hopping window of size $S$ and hop $H$, event $t$ belongs to every integer-indexed interval $[o+kH,o+kH+S)$ containing it.

Let $W_i$ be the monotone watermark of active input $i$. A conservative multi-input operator commonly advances at

$$
W=\min_{i\in A}W_i,
$$

where $A$ is the policy-defined set of active inputs. For window $[s,e)$ and allowed lateness $L\ge0$, this module's explicit boundary convention makes the on-time firing eligible when $W\ge e$ and cleanup eligible when $W\ge e+L$. Runtime APIs differ at exact equality, so production contracts must use their documented inequality.

These relations bound waiting and state; they do not prove semantic completeness. If a source watermark is heuristic, an event with $t<W$ can still arrive. The system must then update, retract, quarantine, discard, or reconcile it according to a visible policy.

### Critical invariants

- Window timestamp field, time authority, key, type, size/gap, hop, origin, timezone, boundary inclusion, and policy version are explicit.
- Window assignment depends on event attributes and declared reference data, never incidental worker arrival or wall-clock `now` unless processing-time semantics are intentionally required.
- Watermarks never regress within one operator generation; restore, rescale, partition discovery, and idle reactivation preserve that invariant.
- A watermark is interpreted according to its provenance: backlog-derived lower bound, bounded-disorder heuristic, source punctuation, or finite-input completion are not interchangeable.
- Multi-input progress states how watermarks combine and how idle, missing, new, removed, fast, and recovering inputs behave.
- Trigger, accumulation, output timestamp, update/retraction encoding, allowed lateness, cleanup, and sink compatibility form one contract.
- An emitted pane is not called final merely because a trigger fired or a watermark crossed a window end.
- Cleanup cannot precede the last promised correction opportunity; downstream deduplication and joins retain compatible horizons.
- Session merging can invalidate prior window identities, so stable business identity and correction semantics survive boundary changes.
- Future or malformed timestamps cannot advance progress unchecked and destroy valid older state.
- Backfills use an explicit watermark/replay plan and cannot be mixed silently with live progress.
- Metrics expose per-input and per-operator watermarks, idle status, holds, skew, firing counts, late acceptance/drop, state age/size, and correction lag.
- Policy changes are treated as state and data migrations with exact cuts, dual outputs, reconciliation, rollback, and consumer coordination.

### Common failures

Common failures include treating a watermark as a wall clock or completeness proof; confusing a window with a batch; omitting alignment or timezone; using inclusive ends on both adjacent windows; assuming a ten-minute watermark delay means ten minutes of processing-time waiting; advancing from one future timestamp; taking the maximum input watermark for a loss-intolerant join; letting an idle partition stall forever; declaring an active but slow partition idle; firing panes without update identity; sending accumulating panes into an additive sink; deleting state at the on-time firing; failing to merge session trigger state; replaying old data behind a live watermark; changing grace or timestamp extraction in place; and monitoring only output rate while progress is stuck.

### Compact example

A ten-second tumbling window `[0,10)` accepts values 5 and 4, then emits on-time total 9 when its watermark reaches 12. With fifteen seconds of allowed lateness, a value 3 for event time 6 arriving at watermark 18 is accepted and produces revision 12. State becomes cleanup-eligible at watermark 25; a value 2 for event time 8 arriving at watermark 26 is discarded or routed for reconciliation. The correct sink operation is an upsert from 9 to 12, not an additive `+12`.

### Connections

[DE-051](051-streams-logs-and-unbounded-data.md) established unbounded input and explicit cuts. [DE-052](052-topics-partitions-and-offsets.md) supplies partition progress, [DE-053](053-producer-keys-and-ordering.md) supplies key/order contracts, and [DE-057](057-event-time-and-processing-time.md) supplies timestamp authority and uncertainty. DE-059 develops stateful stream transformations; DE-060 develops late, duplicate, and out-of-order handling; DE-061 develops stream joins.

## Governing Question

An unbounded stream has no natural final row. Yet products ask for five-minute utilization, hourly fraud signals, daily revenue, user sessions, and joins between impressions and clicks. A window makes the aggregation domain finite, but it does not answer when the data is complete, when a result should appear, how long it can change, or when state may be removed.

These questions are independent. Window assignment answers **where** an event contributes. A watermark estimates **how far event-time progress has advanced**. A trigger answers **when** to emit. Accumulation and update encoding answer **what each emission means**. Allowed lateness and retention answer **how long correction remains possible**. A finality contract answers **what consumers may rely on**.

The governing task is to specify all of them as one observable, replayable contract. A pipeline that chooses only `window=5m` has not defined its semantics. It has left alignment, boundaries, timestamp source, late behavior, panes, state, sink mutation, backfill, and change safety to defaults.

No online system generally knows that every possible event has arrived. The Dataflow model frames windowing, watermarks, triggers, and accumulation as trade-offs among correctness, latency, and cost for unbounded, out-of-order input. Engineers should expose that trade rather than hide it behind the word “final.”

## Why This Matters

Window boundaries affect money and obligations. A purchase exactly at midnight must belong to one accounting day, not two or neither. A hopping alert may intentionally count one event in several overlapping horizons. A session bridge can merge two previously emitted sessions and change conversion attribution. A local civil day can be 23, 24, or 25 hours.

Watermark policy affects both correctness and liveness. A conservative minimum protects slow inputs but can delay every downstream window and grow state. An aggressive maximum improves latency but can classify valid slow-side records as too late. Idleness can unblock a silent partition, but a bad timeout can exclude a merely quiet or partitioned source.

Trigger policy affects consumer meaning. Early panes reduce visible latency but are provisional. Late panes correct results but require version-aware sinks. Discarding panes are deltas; accumulating panes are replacements. Treating both as additive creates double counting.

Retention affects recoverability. Removing window state controls cost, but later events then cannot update the result. A side output preserves evidence but does not repair the materialization automatically. Business finality may require a separate ledger correction weeks after operational state cleanup.

Replay exposes implicit time. Starting a backfill behind a live watermark can cause every historical event to be dropped. Re-evaluating session gaps or civil windows with new reference data can move facts between results. Exact-once recovery does not make a changed window contract equivalent.

## Prerequisites and Retrieval

Retrieve the business grouping question: event being grouped; authoritative event timestamp; key; fixed, hopping, sliding, session, calendar, count, or custom window; expected boundary; timezone/civil rules; alignment origin; and stable business identifier.

Retrieve arrival evidence: per-source and per-key event-minus-ingest distributions; percentiles and extreme tails; offline devices; scheduled/future events; source backlog; retries; partition skew; corrections; backfills; reordering; and known completeness markers.

Retrieve the runtime contract: timestamp assigner/extractor; watermark generator; periodic or punctuated emission; out-of-orderness bound; watermark interval; partition initialization; monotonicity; idle timeout; alignment group/drift; input combination; output watermark holds; timers; restore semantics; and end-of-input signal.

Retrieve the window contract: interval convention; size; hop; offset/origin; keying; session gap/merge rule; calendar/timezone version; custom assigner; trigger; early/on-time/late firings; pane timing; accumulation mode; output timestamp; allowed lateness/grace; state TTL; cleanup timer; late side output; and correction identity.

Retrieve sink and consumer behavior: append, upsert, retract, changelog, or versioned snapshot; primary key; ordering/version check; idempotency; transactional boundary; cache invalidation; notification behavior; query consistency; and whether consumers understand provisional results.

Retrieve state evidence: aggregate versus full-element storage; window/timer/trigger state; number of keys and concurrent windows; hopping fan-out; session merge cost; skew/hot keys; checkpoint size; compaction; state backend; spill; retention; restore time; and quota.

Retrieve operational evidence: per-partition and per-operator watermark; event-time skew; watermark age/stall; active/idle transitions; watermark holds; early/on-time/late pane count; accepted/dropped/quarantined lateness; state bytes/keys/timers; cleanup lag; correction rate; sink conflicts; and business reconciliation.

Retrieve change cases: new partitions; partition reassignment; rescale; source restart; restore from an old checkpoint; deployment with changed timestamp extraction; changed window size/hop/origin/timezone; changed idle timeout; changed watermark bound; changed grace; runner upgrade; backfill/live coexistence; and rollback.

Distinguish event-time window from processing-time batch; window end from result finality; watermark lag from processing latency; lateness from network delay; allowed lateness from retention; trigger from cleanup; pane from window; accumulating replacement from discarding delta; source watermark from operator watermark; idle from complete; alignment from synchronization; and operational closure from business correction.

Create a window-progress contract:

| Concern | Required decision and evidence |
|---|---|
| Assignment | Timestamp, key, type, size/gap, hop, origin, timezone, boundaries, version |
| Progress | Source evidence, formula, cadence, monotonicity, initialization and terminal signal |
| Composition | Per-partition/input minimum or other rule, idleness, alignment and holds |
| Emission | Early/on-time/late triggers, pane metadata, accumulation and output timestamp |
| Correction | Grace/lateness, update/retraction form, sink identity and consumer behavior |
| State | Contents, timers, merge behavior, cleanup inequality, retention and capacity |
| Recovery | Checkpointed progress/state, restore, rescale, new inputs, replay and backfill |
| Change | Exact cut, dual outputs, rebuild/translation, comparison, rollback and lineage |
| Evidence | Boundary vectors, disorder distributions, fault tests, metrics and reconciliation |

Write a falsifiable claim: “Policy `revenue-window-v4` assigns authoritative `paid_at` to UTC-aligned half-open five-minute tumbling windows; per-partition source watermarks combine by active minimum, with measured two-hour disorder allowance and audited idleness; the on-time pane is provisional, accepted late events upsert a monotonically versioned aggregate for seven days, state cleanup follows that horizon, later facts enter the correction ledger, and backfills rebuild a separate generation from exact offsets.”

## Learning Objectives

After completing this module, you should be able to:

1. derive tumbling and hopping window membership with explicit alignment and half-open boundaries;
2. model session creation and merging under late, bridging events;
3. distinguish windows, watermarks, triggers, panes, accumulation, lateness, retention, and finality;
4. design source and multi-input watermark policies without assuming perfect completeness;
5. reason about idleness, alignment, watermark holds, future timestamps, and recovery;
6. connect early/on-time/late panes to compatible upsert, retract, or delta sinks;
7. calculate state and output-latency trade-offs for grace periods, joins, and overlapping windows;
8. design replay/backfill and policy migrations without mixing temporal generations;
9. instrument watermark progress, state cleanup, corrections, and business reconciliation; and
10. test boundary equality, disorder, stalls, merge, restore, and adversarial timestamp cases.

## Core Exposition

### Define window identity before implementation

A durable window identity includes the business key, interval or session identity, timestamp authority, timezone/alignment, and policy version. `customer-42/2026-09-03T10:00Z` is incomplete if two policies can produce different totals for that apparent interval.

Use half-open intervals `[start,end)` for adjacent fixed windows. The end belongs to the next window, preventing double assignment at a shared boundary. Record the exact unit and rounding behavior; converting nanoseconds to milliseconds before assignment can move boundary events.

Calendar windows need civil semantics. “Day in America/New_York” is not identical to a fixed 86,400-second duration. Retain timezone and ruleset intent, especially for backfill and future schedules.

### Choose the window family from the question

Tumbling windows produce one non-overlapping interval per timestamp. They fit independent periodic totals when alignment is meaningful.

Hopping windows start every $H$ and last $S$. When $H<S$, an event contributes to several aggregates. This supports rolling summaries but multiplies state and output. A “sliding window” label is not portable: Kafka Streams distinguishes hopping windows from record-driven sliding windows, while other systems use sliding for fixed overlapping intervals. Specify the actual membership rule.

Session windows group activity per key and merge intervals separated by less than the inactivity gap. Late bridge events can merge sessions already observed separately. The result identity and sink must support replacement or retraction of the old sessions.

The global window has no natural event-time end. It is useful only with explicit data/count/processing triggers and bounded state semantics. Count windows and custom domain windows need equally explicit behavior under retries, partitions, and replay.

### Separate assignment, progress, emission, and cleanup

Assignment is a pure mapping from record plus versioned policy to one or more window IDs. Progress is the runtime's event-time frontier. Emission is controlled by triggers. Cleanup releases state. None implies another automatically across systems.

A watermark crossing an end can make an on-time trigger eligible while state remains for late correction. A processing-time early trigger can emit before the watermark. A count trigger may never fire when too few records arrive unless composed with another condition. Cleanup without a final emission can lose accepted state; firing without cleanup can retain it indefinitely.

Write these as separate state-machine transitions and test their exact inequalities.

### Build watermarks from defensible source evidence

A source with ordered offsets and known timestamp bounds may derive a strong progress lower bound from outstanding records. A bounded-out-of-orderness heuristic often tracks the maximum observed event timestamp $M$ and emits approximately $M-B$. This is only as trustworthy as timestamp validation and the bound $B$.

Periodic generators emit on a runtime cadence; punctuated generators react to explicit markers. A finite source can emit a terminal maximum watermark only after all assigned input is exhausted under the connector contract. Do not send terminal progress merely because an upstream poll returned no record once.

Validate future timestamps before they influence $M$. One corrupt year-2099 event can push a naive watermark forward, close windows, and discard valid current traffic. Preserve the record for investigation while preventing untrusted progress advancement.

### Compose partition and input progress conservatively

For an operator with several active inputs, the minimum watermark represents the furthest-behind dependency under common event-time semantics. Flink documents that its task input watermark is the lowest upstream watermark; Spark's default multi-watermark policy likewise selects the minimum, while offering a maximum policy that trades slower-input data for faster results.

The minimum protects correctness but creates head-of-line blocking. A silent partition can hold every downstream window. Measure per-input progress so the limiting input is visible; a single global number hides the owner.

For joins, progress must account for both sides and the time-range predicate. An unmatched outer-join row cannot safely produce its null result until the opposite input's progress rules out a future match. The cleanup horizon is therefore derived from window bounds, both watermark delays, and join direction—not copied from one source.

### Treat idleness as a failure-policy decision

Idleness detection removes a silent input from the active minimum after a timeout. This restores liveness for sparse partitions. It does not prove the partition complete.

Choose the timeout from source behavior and failure detection, not desired dashboard latency alone. A quiet customer, disconnected shard, authorization failure, and exhausted finite input are different states. Expose the reason and transition.

On reactivation, do not regress operator time. Records behind current progress follow the late-data policy. New partitions need an initialization rule that cannot reset progress or immediately classify all of their legitimate backlog as irrecoverably late.

### Align fast and slow watermarks when buffering matters

Two inputs may both progress, but one can run far ahead. A downstream join then buffers fast-side records while waiting for possible slow-side matches. Flink watermark alignment can pause sources whose watermarks exceed the group minimum by a configured drift, limiting this state growth.

Alignment trades source throughput for bounded downstream skew. It requires connector support and observability. It is not clock synchronization and does not make event timestamps more accurate.

Alternative controls include admission limits, partition rebalancing, separate materializations, spill, or accepting loss with an aggressive progress rule. State the correctness cost.

### Design triggers as a product latency contract

An event-time trigger emits when watermark progress crosses a boundary. Processing-time triggers can provide periodic early estimates or delayed late corrections. Data-driven triggers fire on counts or other observed properties. Composite triggers express “early every minute, on-time at end, late after corrections.”

Every pane carries window ID, pane/revision ID, timing class, accumulation semantics, policy version, and source cut or comparable lineage. A UI may display provisional estimates; billing may wait for operational close; audit may accept later ledger corrections. One trigger cannot satisfy every consumer silently.

Trigger timing is not deterministic under changes in backlog, worker scheduling, or recovery unless those decisions are recorded. Event-time assignment can be deterministic while early pane sequence is not. Define whether replay must reproduce only the final accepted materialization or every historical pane.

### Match accumulation and sink mutation

An accumulating pane contains the aggregate over all accepted elements so far. It normally replaces the preceding value for the same window/version. A discarding pane contains only newly accumulated contributions since the prior firing and normally acts as a delta.

Sending accumulating values 9 then 12 to an additive sink yields 21, not 12. Sending discarding deltas 9 then 3 to a replacement sink yields 3, not 12. Changelog systems may issue before/after retractions; append-only sinks can store immutable pane versions and expose a latest-view query.

The sink must reject stale revisions and make retry idempotent. Notification and irreversible side effects should not fire once per pane unless duplicates and corrections are intended.

### Bound lateness without inventing completeness

Allowed lateness controls how long late events can update retained window state in a particular runtime. Kafka Streams calls a related duration a grace period; Flink and Beam expose allowed-lateness concepts with product-specific boundaries and defaults.

Select the horizon from measured delay distributions plus business obligations, disaster recovery, offline behavior, and cost. A percentile alone may exclude rare but legally significant records. Define separate channels for accepted correction, too-late reconciliation, invalid timestamp, and suspected abuse.

After cleanup, a valid event can still exist. The online operator may no longer revise its state, but a governed correction ledger or rebuild can repair the business result. “Dropped from this window operator” must not mean “the obligation ceased to exist.”

### Manage window state and watermark holds

Incremental aggregates store compact accumulator state; full-window functions and evictors may retain every element. Hopping windows multiply membership. Session windows retain mergeable structures and timers. Hot keys can dominate state even when the global average looks safe.

State lifetime is approximately the interval from first accepted event until cleanup, extended by stalls, holds, retries, and checkpoint behavior. Estimate keys × concurrent windows × bytes per state plus timers and backend overhead. Validate with production cardinality and skew.

An operator that buffers records to emit later must hold its output watermark so downstream windows do not close before those records appear. Beam documents timer output timestamps and watermark holds for this purpose. A leaked hold can stall the graph; a missing hold can make correct buffered output late downstream.

### Make session merging and joins correct under disorder

For one key, a late event can bridge two sessions. The runtime must merge aggregate state, trigger state, timers, and window identity as its API requires. Custom triggers that ignore merge callbacks can fire incorrectly or leak state.

Consumers must learn that session boundaries are provisional until the merge/correction horizon passes. Use stable entity-level identity plus versioned session IDs or explicit retractions of the old windows followed by the merged replacement.

Stream joins retain candidates until watermark and time-range evidence makes future matches impossible. Inner joins can emit matches early, but outer joins must delay absence claims. Missing time bounds make state unbounded even when both sources have watermarks.

### Isolate replay, backfill, and live generations

A backfill begins with old event timestamps. Feeding it into an operator whose live watermark is current can classify the entire backfill as late. Use a separate job/state/output generation, reset progress under a controlled finite cut, or a product-supported backfill path.

Pin timestamp extraction, window policy, timezone/reference data, and source offsets. Decide whether replay reproduces historical early panes or only the converged result. Do not use current wall time to reconstruct event-time triggers.

At convergence, compare per-window membership, totals, correction counts, and source coverage. Merge generations only through an explicit cut and version rule.

### Change temporal policy as a data migration

Changing size, hop, origin, timezone, gap, timestamp field, watermark bound, idleness, trigger, grace, or accumulation changes state and often result meaning. A rolling deployment with mixed policies can create windows that no single version owns correctly.

Choose compatible state translation only when the runtime and semantics prove it. Otherwise rebuild a new generation from retained source cuts. Dual-publish distinguishable window-policy versions; compare authoritative totals and boundary samples; coordinate consumers; cut over; and retain rollback evidence.

Runner upgrades can also alter supported trigger behavior or defaults. Verify effective configuration and checkpoint/savepoint compatibility instead of trusting source code alone.

### Observe progress and reconcile results

Graph per-input and per-operator watermarks against maximum observed event time and wall time, but name each lag correctly. Watermark lag indicates event-time progress; system latency and source backlog measure other queues. Google Cloud Dataflow exposes separate system and data watermark/lag concepts, illustrating why one metric is insufficient.

Alert on regression, no advance under expected traffic, growing input skew, repeated idle transitions, future timestamp suppression, excessive holds, late-drop/accept spikes, state growth, timer backlog, pane storms, sink stale-version conflicts, and reconciliation differences.

Keep exemplars: source partition/offset, event timestamp, assigned windows, input/operator watermark at arrival, pane IDs, decision reason, and correction route. Aggregate rates alone cannot explain a disputed record.

### Test the complete temporal state machine

Test timestamps one unit before, at, and after every boundary; negative epochs if supported; precision conversion; overlapping hopping membership; session gap equality and bridge merges; key skew; empty windows; and global-window termination.

Test watermark duplicate/regression, future outlier, stalled/idle/reactivated/new partitions, fast/slow alignment, output holds, finite completion, source restart, checkpoint restore, rescale, and terminal markers.

Test early/on-time/late trigger order, retry of each pane, accumulating/discarding/retracting sinks, grace equality, cleanup, too-late reconciliation, consumer cache, and irreversible notification guards.

Use a controllable event-time and processing-time test source. Apache Beam's `TestStream` support is an example of advancing watermarks and processing time explicitly. Reconcile results against a bounded oracle over the exact same records and policy version.

### Review the complete window argument

A defensible design connects fifteen claims: timestamp authority is valid; key and window membership are explicit; boundaries and alignment are tested; progress provenance is known; watermarks are monotone; multi-input combination is safe; idleness and alignment are governed; triggers express product latency; panes encode meaning; sink mutation matches accumulation; correction horizon matches obligations; cleanup matches promises; sessions/joins handle disorder; replay/change isolate generations; and metrics plus finite-cut reconciliation validate behavior.

If any link is absent, narrow the claim. A window can be assigned correctly while emitted too early, corrected incorrectly, retained forever, or deleted before a promised update. A watermark can advance monotonically while being semantically unsafe. Temporal correctness comes from the composition, not one API call.

## Definitions and Notation

For event $x$, define:

- $t(x)$: authoritative event timestamp after validated conversion.
- $k(x)$: business/partitioning key.
- $o$: window alignment origin.
- $S>0$: fixed window size.
- $H>0$: hopping advance or hop.
- $G>0$: session inactivity gap.
- $W_i$: watermark emitted by input $i$.
- $A$: set of inputs currently active under idleness policy.
- $W$: effective operator input watermark.
- $L\ge0$: allowed lateness or grace duration under a stated runtime convention.
- $P_{w,j}$: pane $j$ emitted for window $w$.
- $v_{w,j}$: monotone sink revision for that pane.

For tumbling windows,

$$
k=\left\lfloor\frac{t-o}{S}\right\rfloor,
\qquad w(t)=[o+kS,o+(k+1)S).
$$

For hopping windows, membership is

$$
\mathcal W(t)=\{[o+kH,o+kH+S):k\in\mathbb Z,\ o+kH\le t<o+kH+S\}.
$$

When $S/H$ is an integer, an interior event ordinarily belongs to $S/H$ hopping windows. Boundary and finite-domain rules still require tests.

For a bounded-disorder input with maximum valid observed timestamp $M_i$ and chosen bound $B_i$,

$$
W_i^{new}=\max(W_i^{old},M_i-B_i)
$$

under this chapter's simplified convention. Some runtimes subtract an additional clock unit or use different equality rules; use the effective product definition.

A conservative active-input composition is

$$
W=\min_{i\in A}W_i.
$$

For window $w=[s,e)$, this module uses:

$$
\text{on-time-eligible}(w)\iff W\ge e,
$$

$$
\text{cleanup-eligible}(w)\iff W\ge e+L.
$$

An event arriving when $t(x)<W$ is behind current progress. Whether it is late for a particular window and accepted depends on that runtime's trigger and cleanup rules. Do not collapse these predicates.

For an accumulating aggregate $C_{w,j}$ and newly accepted contribution $\Delta_{w,j}$,

$$
C_{w,j}=C_{w,j-1}+\Delta_{w,j}.
$$

An upsert sink stores $C_{w,j}$ at revision $v_{w,j}$; an additive sink consumes only $\Delta_{w,j}$. Mixing the two double-counts or loses history.

For sorted per-key event times $t_1\le\dots\le t_n$, this module's session convention starts a new session when $t_j-t_{j-1}\ge G$. Frameworks may define gap equality differently, so equality is a contract test.

## Mechanisms, Invariants, or Proof Structure

Use this review sequence:

1. **Name the business grouping.** Identify event, timestamp authority, key, civil/instant basis, and required corrections.
2. **Define membership.** Specify type, size/gap, hop, origin, timezone, half-open boundaries, precision, and version.
3. **Establish source progress.** Document ordering/backlog evidence, generator formula, cadence, initialization, validation, and terminal signal.
4. **Compose progress.** Define per-partition/input minimum or alternative, idleness, new/reactivated inputs, alignment, and output holds.
5. **Define firing.** Specify early, on-time, late, repeated/final triggers and pane metadata.
6. **Define mutation.** Match accumulating, discarding, or retracting panes to idempotent sink operations and consumer semantics.
7. **Set correction horizons.** Derive allowed lateness, state retention, join bounds, cleanup inequality, and post-cleanup reconciliation.
8. **Bound resources.** Estimate keys, window fan-out, merge/full-element state, timers, skew, checkpoint, and restore.
9. **Control recovery and change.** Pin source cuts/policies, isolate backfills, dual-run migrations, compare, cut over, and preserve rollback.
10. **Prove with evidence.** Run boundary/fault tests, inspect per-input/operator metrics, trace exemplars, and reconcile finite cuts.

The assignment invariant is:

> The same accepted record, key, timestamp, policy version, and reference-data version map to the same window identities on live execution and replay.

The progress invariant is:

> An operator watermark never regresses, and every advance is justified by the declared active-input and source-evidence policy.

The correction invariant is:

> Every accepted pane has unambiguous replacement, delta, or retraction semantics, and state remains until the last promised online correction opportunity.

The finality invariant is:

> Operational window closure is never represented as proof that no older fact exists; later obligations have an explicit correction or reconciliation path.

This executable demonstrates fixed/hopping membership, session gaps, late correction before cleanup, discard after cleanup, and minimum/idle watermark composition. It models the stated integer-time convention only; it does not prove a production source watermark, runtime boundary, or business completeness guarantee.

<!-- bijux-verify: {"id":"window-watermark-state","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"fixed_windows=((3, (0, 10)), (7, (0, 10)), (13, (10, 20)), (19, (10, 20)), (22, (20, 30)))\nhopping_windows_for_19=((0, 20), (10, 30))\nsessions_gap_10=((2, 8), (25, 31), (50, 50))\npanes=((1, 'on-time', 9), (2, 'late', 12))\naccepted=('a', 'b', 'c')\ndiscarded=('d',)\nfinal_total=12\ncleanup_boundary=25\nactive_watermark_min=18\nidle_excluded_watermark=42\nnonregressing_after_reactivation=42\n","stderr":""}} -->
```python
from math import floor


def fixed_window(timestamp, size, origin=0):
    start = origin + floor((timestamp - origin) / size) * size
    return (start, start + size)


def hopping_windows(timestamp, size, hop, origin=0):
    candidates = range(floor((timestamp - origin - size) / hop) + 1,
                       floor((timestamp - origin) / hop) + 1)
    return tuple(
        (origin + index * hop, origin + index * hop + size)
        for index in candidates
        if origin + index * hop <= timestamp < origin + index * hop + size
    )


def sessions(timestamps, gap):
    groups = []
    for timestamp in sorted(timestamps):
        if not groups or timestamp - groups[-1][1] >= gap:
            groups.append([timestamp, timestamp])
        else:
            groups[-1][1] = timestamp
    return tuple(tuple(group) for group in groups)


fixed = tuple((time, fixed_window(time, 10)) for time in (3, 7, 13, 19, 22))
hopping = hopping_windows(19, size=20, hop=10)
session_groups = sessions((2, 8, 25, 31, 50), gap=10)

window_end = 10
allowed_lateness = 15
cleanup_boundary = window_end + allowed_lateness
total = 0
accepted = []
discarded = []
panes = []

for identifier, event_time, value, watermark in (
    ("a", 3, 5, 0),
    ("b", 7, 4, 5),
):
    total += value
    accepted.append(identifier)

panes.append((1, "on-time", total))  # watermark advanced to 12

identifier, event_time, value, watermark = ("c", 6, 3, 18)
if watermark < cleanup_boundary:
    total += value
    accepted.append(identifier)
    panes.append((2, "late", total))

identifier, event_time, value, watermark = ("d", 8, 2, 26)
if watermark >= cleanup_boundary:
    discarded.append(identifier)

partition_watermarks = {"p0": 42, "p1": 18}
active_minimum = min(partition_watermarks.values())
idle_excluded = partition_watermarks["p0"]
reactivated_candidate = 10
nonregressing = max(idle_excluded, reactivated_candidate)

print(f"fixed_windows={fixed}")
print(f"hopping_windows_for_19={hopping}")
print(f"sessions_gap_10={session_groups}")
print(f"panes={tuple(panes)}")
print(f"accepted={tuple(accepted)}")
print(f"discarded={tuple(discarded)}")
print(f"final_total={total}")
print(f"cleanup_boundary={cleanup_boundary}")
print(f"active_watermark_min={active_minimum}")
print(f"idle_excluded_watermark={idle_excluded}")
print(f"nonregressing_after_reactivation={nonregressing}")
```

The event sequence and watermark values are supplied examples. Production acceptance must use the runtime's documented boundary semantics and persisted operator state.

## Alternatives and Trade-Offs

**Tumbling versus hopping windows.** Tumbling windows assign once and bound fan-out. Hopping windows expose rolling context but multiply state, compute, output, and corrections.

**Fixed-duration versus calendar windows.** Fixed duration is stable in UTC-like time. Calendar windows match human/legal periods but depend on timezone, daylight changes, and ruleset versions.

**Session versus fixed windows.** Sessions model activity naturally but merge under disorder and create unstable boundaries. Fixed windows are predictable but split one interaction across arbitrary cuts.

**Conservative minimum versus aggressive maximum watermark.** Minimum protects lagging inputs but increases latency/state. Maximum advances quickly but can drop or misclassify slow-side data. Spark documents both policies and their trade-off.

**Bounded-disorder heuristic versus source-completeness watermark.** A simple maximum-minus-bound is cheap and responsive but vulnerable to tail/future timestamps. Source backlog/offset knowledge can be stronger but is connector-specific and operationally complex.

**Long idleness timeout versus short timeout.** Long timeouts reduce false-idle exclusions but stall sparse streams. Short timeouts improve liveness but turn normal silence or outages into late data on reactivation.

**Watermark alignment versus unrestricted sources.** Alignment bounds downstream skew/state but throttles fast inputs and adds coordination. Unrestricted consumption maximizes input throughput but can overwhelm join/window state.

**Early panes versus on-time-only output.** Early panes improve perceived latency and monitoring but add provisional values, output load, and consumer complexity. On-time-only output is simpler but can be delayed by conservative progress.

**Accumulating versus discarding panes.** Accumulating panes are self-contained replacements but repeat data. Discarding panes are compact deltas but require exact ordered application and recovery history.

**Upsert/retraction versus immutable pane log.** Upserts provide a convenient latest view but obscure history unless audited. Immutable versions preserve history but require consumers to select or fold the latest valid revision.

**Long allowed lateness versus bounded state.** Long horizons capture more tail events but cost state, checkpoint, restore, and output corrections. Short horizons control cost but require a durable post-cleanup repair path.

**Pre-aggregation versus full-window storage.** Incremental associative aggregates are compact and scalable. Full-element functions permit richer logic but amplify state; Flink notes that evictors prevent pre-aggregation because elements must be retained.

**Mixed live/backfill versus isolated generation.** Mixing avoids duplicate infrastructure but risks immediate late classification and ambiguous outputs. Isolation costs resources but preserves progress and comparison boundaries.

## Failure Modes and Misconceptions

**“A window turns a stream into a batch.”** The logical interval can emit many panes and receive corrections; it is not necessarily immutable.

**“The watermark is current wall time.”** It is event-time progress derived from source/operator policy and can lag, jump, or stall independently.

**“Past the watermark means impossible.”** Heuristic watermarks can be followed by older events. Product docs explicitly define late-data paths.

**“Ten-minute watermark means wait ten processing minutes.”** A delay bound is expressed relative to observed event time; wall waiting depends on arrivals and progress.

**“Window end is inclusive.”** Adjacent half-open windows place an event at the end in the next interval. Equality must be tested.

**“All sliding windows mean the same thing.”** Terminology differs. Specify size, hop, membership, and boundary behavior.

**“Sessions close permanently after inactivity.”** Late bridge events can merge previously separate sessions while state is retained.

**“The fastest input should drive the join.”** That sacrifices slower-side records unless the business explicitly accepts the loss.

**“A silent partition is complete.”** Silence may mean sparse traffic, outage, lost authorization, or stalled consumption. Idleness is policy, not proof.

**“Idleness may reset the watermark on return.”** Operator event time must remain monotone; returning old records are handled as late.

**“Alignment synchronizes event clocks.”** It throttles consumption/progress skew; it does not correct timestamp accuracy.

**“Trigger firing deletes state.”** Fire and purge/cleanup are distinct operations in windowing APIs.

**“On-time is final.”** On-time is a pane timing classification. Allowed late updates or business corrections can follow.

**“Accumulating panes can be summed.”** Each usually replaces the prior aggregate. Summation double-counts history.

**“Allowed lateness guarantees acceptance.”** Runtime-specific guarantees, equality, state cleanup, trigger, and operator support determine behavior.

**“State TTL and allowed lateness are interchangeable.”** Generic TTL may expire state on different clocks or access rules and violate the window promise.

**“Side output fixes dropped late data.”** It preserves a route/evidence; repair still requires ownership, identity, and reconciliation.

**“Watermarks alone bound a stream join.”** The time-range predicate and both input horizons are required to evict unmatched candidates safely.

**“Exactly-once makes panes deterministic.”** Early trigger schedules and changed policy can differ even when state recovery is exactly once.

**“A backfill can share live state.”** Old events behind live progress may be discarded and session/window identities may collide.

**“Changing grace is only a configuration update.”** It changes admitted facts, state lifetime, output corrections, and possibly business totals.

**“Output rate proves progress.”** Processing-time outputs may continue while event-time watermarks are stuck and old state grows.

## Worked Examples

### Example 1

With UTC origin, ten-minute tumbling windows are `[10:00,10:10)` and `[10:10,10:20)`. Events at 10:09:59.999 and 10:10:00 belong to different windows. A test at exact precision proves the boundary instead of relying on diagrams.

### Example 2

A 20-minute hopping window starts every 5 minutes. An event at minute 19 belongs to starts 0, 5, 10, and 15 under half-open boundaries. One input contribution creates four aggregate updates, so capacity estimates include the fan-out.

### Example 3

User events occur at minutes 2, 8, 25, and 31 with a ten-minute session gap. They form `[2,8]` and `[25,31]` under the stated equality convention. A late event at 17 is within ten minutes of both edges and bridges them, requiring one merged replacement and retirement of both earlier identities.

### Example 4

Partitions have watermarks 42 and 18, so a conservative operator watermark is 18. Marking the second idle advances effective progress to 42. When it returns with event time 10, progress cannot regress; the record follows late/correction policy.

### Example 5

A `[0,10)` aggregate emits accumulating total 9 on time, then total 12 after a late value. An upsert sink stores revision 2 value 12. An additive sink would need deltas 9 and 3; adding 9 and 12 is wrong.

### Example 6

An event timestamped year 2099 reaches a maximum-minus-five-minute watermark generator. Without validation, the watermark leaps decades and cleans current state. The source quarantines the outlier and bases progress only on valid timestamps.

### Example 7

An impressions-clicks left outer join allows clicks up to one hour after impressions. A null-click result cannot be emitted merely when the impression-side watermark passes the impression; the click-side watermark must pass the latest permitted match time under its delay contract.

### Example 8

A sparse tenant partition is silent for 30 minutes by design, but the idle timeout is five minutes. Its next legitimate event is late relative to current operator progress. The policy retains it through a correction channel and records that the liveness choice creates revisions for sparse tenants.

### Example 9

A seven-day backfill is sent to a live operator whose watermark is today. Every historical record is beyond online grace. A separate output generation rebuilds from exact offsets with fresh progress, then reconciles and atomically replaces the affected date range.

### Example 10

A processing-time early trigger emits every minute while the watermark is stalled by one input. Output appears healthy, but state and data freshness grow. Per-input watermark, hold, state-size, and source-backlog metrics reveal the stuck dependency.

## Cross-Program Connections

Distributed systems contributes partial order, logical progress frontiers, failure detection, monotonicity, coordination, recovery epochs, and the distinction between evidence and certainty.

Database systems contributes materialized views, incremental aggregation, changelogs, upserts, retractions, MVCC versions, indexes, state cleanup, and transactionally visible cutover.

Algorithms and data structures contributes interval arithmetic, floor division, sweep/merge algorithms, heaps, timers, sketches, associative monoids, and hot-key complexity.

Formal methods contributes state machines, safety/liveness, invariants, temporal logic, refinement, and adversarial traces for firing/cleanup races.

Probability and statistics contributes delay distributions, tail estimation, censoring, sampling bias, confidence, anomaly detection, and the cost of percentile-based lateness choices.

Site reliability engineering contributes backlog/freshness SLOs, per-stage metrics, alerting, checkpoint/restore drills, capacity, fault injection, and operational runbooks.

API and service engineering contributes versioned result resources, ETags/revisions, idempotent upserts, status/finality fields, webhooks, and consumer-compatible corrections.

Platform engineering contributes connector capabilities, state backends, autoscaling, partition lifecycle, deployment/savepoint compatibility, isolation, quotas, and managed observability.

Security engineering contributes malicious future/old timestamps, tenant isolation, watermark denial of service, authorization failures disguised as idleness, audit, and repair controls.

Data governance contributes business-effective time, correction lineage, retention, legal finality, timezone policy, traceable source cuts, and accountable ownership of discarded facts.

Human-computer interaction contributes labeling provisional results, revision explanations, notification restraint, civil-time display, and user trust when totals change.

Accounting contributes closing periods, adjusting entries, immutable ledgers, reconciliation, and the distinction between operational close and later correction.

## References

1. Akidau, Tyler, et al. [The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing](https://research.google/pubs/the-dataflow-model-a-practical-approach-to-balancing-correctness-latency-and-cost-in-massive-scale-unbounded-out-of-order-data-processing/). Accessed 2026-09-03. Primary research source for event-time windowing, watermarks, triggers, accumulation, and correctness/latency/cost trade-offs.
2. Akidau, Tyler, et al. [MillWheel: Fault-Tolerant Stream Processing at Internet Scale](https://research.google/pubs/millwheel-fault-tolerant-stream-processing-at-internet-scale/). Accessed 2026-09-03. Primary research source for low watermarks, per-key computation, timers, persistent state, and fault-tolerant stream progress.
3. Apache Beam. [Basics of the Beam Model](https://beam.apache.org/documentation/basics/). Accessed 2026-09-03. Primary documentation for fixed/sliding window assignment, element timestamps, watermarks, late data, and the distinction between event and processing time.
4. Apache Beam. [Programming Guide](https://beam.apache.org/documentation/programming-guide/). Accessed 2026-09-03. Primary documentation for triggers, panes, accumulation modes, allowed lateness, composite firings, timer output timestamps, and watermark holds.
5. Apache Beam. [Test Your Pipeline](https://beam.apache.org/documentation/pipelines/test-your-pipeline/). Accessed 2026-09-03. Primary testing documentation for `TestStream` control of event-time watermarks, processing-time advancement, and event sequences.
6. Apache Flink. [Generating Watermarks](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/event-time/generating_watermarks/). Accessed 2026-09-03. Primary documentation for timestamp/watermark strategies, periodic and punctuated generation, per-partition progress, idleness, and alignment.
7. Apache Flink. [Windows](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/operators/windows/). Accessed 2026-09-03. Primary documentation for tumbling, sliding, session, and global windows; triggers; allowed lateness; side outputs; cleanup; merging; and evictors.
8. Apache Flink. [Debugging Windows and Event Time](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/debugging/debugging_event_time/). Accessed 2026-09-03. Primary operations documentation for task input-watermark metrics, minimum upstream composition, stalled progress, and straggler strategies.
9. Apache Spark. [Structured Streaming Programming Guide](https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html). Accessed 2026-09-03. Primary documentation for event-time windows, watermark state cleanup, late-data guarantees, multiple-watermark policies, and bounded stream-stream joins.
10. Apache Kafka. [Kafka Streams DSL, Apache Kafka 4.3](https://kafka.apache.org/43/streams/developer-guide/dsl-api/). Accessed 2026-09-03. Primary documentation for hopping, tumbling, sliding, and session windows; grace periods; state stores; joins; and final-result suppression.
11. Google Cloud. [Dataflow Job Step Information](https://cloud.google.com/dataflow/docs/guides/step-info-panel). Accessed 2026-09-03. Primary product documentation distinguishing system watermark/lag, data watermark/lag, and wall-time metrics for diagnosis.

## Exercises

### Exercise 1

For origin 0, tumbling size 10, and event times `-1, 0, 9, 10, 19, 20`, compute the half-open window assigned to each event. Then list all size-20, hop-10 windows containing event time 19. State the precision/boundary assumption.

### Exercise 2

A window is `[100,120)`, this module's on-time rule is $W\ge120$, allowed lateness is 15, and cleanup occurs at $W\ge135$. Events `(a,t=118)` at watermark 110, `(b,t=119)` at watermark 125, and `(c,t=117)` at watermark 136 carry values 5, 3, and 7. Starting from zero, classify each as pre-on-time, accepted late, or post-cleanup; give accumulating pane totals if the on-time pane fires at 120 and each accepted late event fires immediately.

### Exercise 3

Per-input watermarks are `p0=80`, `p1=55`, and `p2=70`. Compute conservative progress. If `p1` becomes idle, compute progress. If it reactivates with candidate watermark 40 after operator progress reached 70, state the non-regression result and how an event at time 45 is handled conceptually. Explain the risk of false idleness.

### Exercise 4

A hopping aggregation has size 60 minutes, hop 5 minutes, 2,000 active keys per hour, 240 bytes per key-window accumulator including timer estimate, and a two-hour effective retention from first open to cleanup. Approximate concurrent key-window states and bytes, assuming each key is active across all overlapping windows and ignoring backend/checkpoint overhead. Explain why the estimate is only a lower-bound planning model.

### Exercise 5

Design a migration from UTC-aligned 15-minute tumbling windows with one-hour lateness and append-only panes to tenant-local hourly calendar windows with seven-day correction and upsert semantics. Include source cuts, policy identity, timezone rules, state/output isolation, backfill/live coordination, comparison, consumer cutover, rollback, observability, and post-cleanup correction.

## Answers to the Exercises

### Answer 1

With floor division and half-open integer intervals, `-1 -> [-10,0)`, `0 -> [0,10)`, `9 -> [0,10)`, `10 -> [10,20)`, `19 -> [10,20)`, and `20 -> [20,30)`. For size 20 and hop 10, time 19 belongs to `[0,20)` and `[10,30)`. The answer assumes exact integer units, origin zero, intervals extending to negative indices, inclusive starts, and exclusive ends. A runtime that truncates precision before assignment must test values around each converted boundary.

### Answer 2

`a` is accepted before the on-time firing, so the on-time accumulating pane at watermark 120 is total 5. `b` belongs to the window and arrives after its end/on-time threshold but before cleanup at 135, so it is accepted late and produces accumulating revision total 8. `c` arrives at watermark 136, after cleanup eligibility, so the online window cannot accept it and total remains 8; it must be discarded or routed to governed reconciliation. Equality at 135 follows the stated cleanup rule and would be ineligible; another runtime may document a different boundary.

### Answer 3

The active minimum is `min(80,55,70)=55`. Excluding policy-confirmed idle `p1` gives `min(80,70)=70`. Reactivation with candidate 40 cannot regress effective operator progress, so it remains at least 70. An event at 45 is behind current progress and follows the window's retained-state/late/reconciliation policy rather than moving time backward. A false-idle decision can let windows fire and clean state before legitimate `p1` records arrive, converting normal sparse or failed traffic into corrections or loss.

### Answer 4

Each event-time position overlaps $60/5=12$ hopping windows. Two hours cover two hourly active-key cohorts in this simplified model, so concurrent key-window states are approximately $2{,}000\times12\times2=48{,}000$. Raw estimated bytes are $48{,}000\times240=11{,}520{,}000$ bytes, about 11.52 MB decimal or 10.99 MiB. This ignores key skew, windows from partial hours, late tails, trigger state, serializer/index/backend overhead, RocksDB or heap amplification, checkpoints, changelogs, retries, sessions/joins, and stalled watermarks; validate with measured state metrics and restore tests.

### Answer 5

Define `tenant-hour-v1` with authoritative timestamp/key, local calendar membership, half-open boundaries, IANA zone and pinned rules/version policy, seven-day correction, pane revision, upsert key, and post-cleanup ledger route. Capture exact source offsets and the old `utc-15m` policy/configuration. Build new isolated state and distinguishable output generation; never reinterpret old window IDs in place. Backfill the retained source cut with a fresh watermark generation while live changes are buffered or dual-routed at a named boundary. Compare record membership, tenant/day totals, DST overlap/gap cases, pane revisions, late/too-late rates, state/checkpoint/restore size, and authoritative finite totals. Update consumers to read revisioned replacements and expose provisional/finality status. Cut over atomically by generation after reconciliation and domain approval; retain old state/source/output and routing for rollback. Monitor timezone resolution, per-input/operator progress, idleness, pane/update conflicts, state, correction latency, and ledger reconciliation. Facts after seven days create auditable business corrections rather than silently disappearing.
