---
module_id: DE-060
program: Data Engineering
level: 2
module_number: 60
title: Handling Late, Duplicate, and Out-of-Order Events
status: complete
last_verified: 2026-09-03
---

# Handling Late, Duplicate, and Out-of-Order Events

## One-Page Review

### Governing question

How should a streaming system distinguish delayed events, transport redeliveries, repeated business occurrences, conflicting reuse of identity, and records observed outside the required order—then preserve correctness through bounded state, correction, replay, and explicit evidence rather than silently dropping inconvenient inputs?

### Essential definitions

- A **redelivery** is another delivery attempt for the same transport message or logical occurrence, commonly after uncertain acknowledgment or recovery.
- An **exact duplicate** has the same canonical occurrence identity and the same canonical semantic fingerprint as an earlier accepted record.
- A **conflicting duplicate** reuses an occurrence identity with different semantic content; it is an integrity conflict, not safely deduplicable data.
- A **repeated business event** is a distinct legitimate occurrence that may have equal values; equality of payload does not make it a duplicate.
- **Late arrival** means a record is observed after a named event-time progress, window, correction, or business deadline under an explicit policy.
- **Delay** is the interval between named timestamp observations; it may be large without making the record late for a particular operator.
- **Out of order** means observation order differs from a named relation such as source sequence, entity version, causal order, event time, or partition offset.
- A **stale update** carries an entity version older than the current accepted version; it can be new evidence even when it must not overwrite current state.
- A **gap** is a missing interval in a sequence expected to be contiguous for a named scope.
- **Deduplication** remembers occurrence identities for a declared horizon and suppresses matching repeats while detecting fingerprint conflicts.
- A **reorder buffer** retains records until a sequence can be emitted contiguously or a bounded wait/gap policy resolves uncertainty.
- A **retraction** reverses a prior contribution; an **upsert** replaces a prior materialized version; a **correction event** records a later authoritative amendment.
- A **side output/quarantine** preserves records and decision evidence outside the primary path for repair or investigation.
- A **dedup horizon** is the longest interval for which identity memory must prevent a repeated occurrence from becoming a new effect.
- A **disposition** is one mutually exclusive primary outcome such as update, stale-retain, exact-duplicate, identity-conflict, too-late, or invalid.

### Central model, mechanism, or theorem

For record $x$, let $i(x)$ be canonical occurrence identity, $h(x)$ its canonical semantic fingerprint, $q(x)$ an entity/source version when defined, $t_e(x)$ event time, and $W$ the relevant event-time progress. A simple diagnostic lateness distance is

$$
\ell(x)=\max(0,W-t_e(x)),
$$

but acceptance depends on the named window/state/business policy, not this scalar alone.

For retained receipt $R[i]=(h,expiry)$:

$$
D(x)=
\begin{cases}
\text{exact duplicate}, & i\in R\land h(x)=R[i].h,\\
\text{identity conflict}, & i\in R\land h(x)\ne R[i].h,\\
\text{new occurrence}, & i\notin R.
\end{cases}
$$

For current entity version $q^*$, a new occurrence with $q>q^*$ may advance current state, $q<q^*$ is stale, and $q=q^*$ requires idempotent equality or conflict handling. This is a business-version rule, not a timestamp comparison.

A defensible dedup horizon satisfies

$$
H\ge\max(H_{retry},H_{source\ replay},H_{disaster},H_{backfill},H_{correction})+M,
$$

unless a permanent authoritative receipt supports older reconciliation. Every input receives one primary disposition so counts reconcile; diagnostic labels such as `late`, `gap-closing`, or `replayed` may overlap.

### Critical invariants

- Occurrence identity is stable, namespaced, canonical, and distinct from payload equality, delivery attempt, partition offset, and entity key.
- A retained identity stores a semantic fingerprint; the same identity with different meaning is quarantined and never silently suppressed.
- Every ordering claim names its scope and relation: partition offset, source sequence, transaction, entity version, causality, or event time.
- Current entity state advances only under its declared version/conflict rule; arrival time and largest timestamp do not override it accidentally.
- Dedup receipts, version/gap state, reorder buffers, correction lineage, and source positions recover atomically enough for the claimed behavior.
- Dedup retention covers maximum retry/replay/disaster/backfill/correction exposure or older inputs are reconciled against a durable authority.
- Late classification records the event timestamp, watermark/deadline/window, policy version, and exact boundary decision.
- A too-late or stale record remains an obligation/evidence item when the domain requires repair; “not applied online” is not “did not happen.”
- Reorder waiting is bounded by time, count, bytes, sequence gap, and source liveness; one missing record cannot block a key forever.
- Retractions/upserts/corrections have deterministic identities and sinks/consumers understand their mutation semantics.
- Watermark, grace, history retention, state TTL, source retention, and correction horizon are compatible.
- Replay/backfill uses a separate generation or resets state/progress coherently; it does not collide with live dedup/window state silently.
- Invalid/future/malicious timestamps and identity floods cannot exhaust state or force destructive progress.
- Reconciliation partitions every input into one primary disposition and measures overlapping diagnostic cohorts separately.

### Common failures

Common failures include deduplicating identical payloads; using broker offset as a global event ID; treating every redelivery as producer duplication; suppressing conflicting IDs; expiring receipts before disaster replay; using event time as version; sorting independent partitions into invented total order; applying last-arrival-wins to stale entity changes; waiting forever for missing sequence numbers; dropping too-late payments because a window closed; adding corrected aggregates without retracting the old contribution; using a Bloom filter as authoritative rejection without a false-positive path; replaying old data into live watermarks; letting one future timestamp flush buffers; counting overlapping late/stale/duplicate labels as exclusive dispositions; and reporting a low duplicate rate while quarantines and silent drops are unmeasured.

### Compact example

Account `acct` accepts occurrence `r1`, version 1, value 5. A matching delivery of `r1` is an exact duplicate. Version 3 (`r3`, value 9) arrives next, advances current state, and opens missing-version gap 2. Version 2 (`r2`, value 7) arrives after watermark progress and closes the evidence gap but is stale, so current state remains version 3/value 9. A later `r3` with value 10 conflicts with the retained fingerprint and is quarantined. An unseen event at time 5 arriving at watermark 50 exceeds the 20-unit online lateness horizon and enters repair rather than current state.

### Connections

[DE-028](028-deduplication-and-record-identity.md) establishes batch identity, [DE-038](038-late-corrections-and-restatement.md) establishes analytical restatement, and [DE-044](044-retries-timeouts-and-idempotency.md) establishes retry identity. [DE-052](052-topics-partitions-and-offsets.md) through [DE-059](059-stateful-stream-transformations.md) supply log coordinates, ordering, delivery/effects, event time, windows/watermarks, and recoverable state. DE-061 begins lakehouse and analytical storage practice, where these correction facts must survive in durable files and table metadata.

## Governing Question

Streaming systems observe records under variable delay and partial failure. A subscriber may see the same message again after an acknowledgment timeout. A producer may publish one business occurrence twice under two message IDs. Two legitimate orders may carry identical payloads. Version 12 may arrive before version 11. A device may upload yesterday's measurement after reconnecting. These cases demand different decisions.

The governing task is classification before action. Determine what identity is repeated, which order relation matters, what event-time progress has passed, which business obligation remains, and which prior state/output exists. Then choose one primary disposition with durable evidence.

There is no universal “remove duplicates” operation. `DISTINCT` over all columns can merge legitimate occurrences and fail to merge semantically identical retries whose metadata changed. Keeping the first arrival can preserve a corrupt partial message. Keeping the last timestamp can accept a skewed or malicious future record. An approximate membership structure can reject new events falsely.

Nor is sorting a universal solution. An unbounded stream cannot wait forever for a total order, and independent partitions may have no meaningful global sequence. A bounded reorder buffer trades latency and state for a stronger local order; version-aware commutative updates may avoid sorting entirely.

The design must state which histories are equivalent under retry, failure, replay, and correction. That requires identity, order, progress, retention, mutation, and reconciliation contracts—not one lateness parameter.

## Why This Matters

Duplicates bias non-idempotent computations. Counts, sums, billing, inventory, notifications, and model features can all double. A downstream `COUNT(DISTINCT id)` may hide the symptom in one query while duplicated side effects or joins remain.

Out-of-order updates corrupt current state when arrival order is treated as business order. A delayed “address version 4” can overwrite version 5. A delete can arrive before a create during snapshot/CDC overlap. A stream-table join can use a future table value for an older event when history is not versioned.

Late events create product decisions. A dashboard may revise yesterday. A regulatory report may require an adjusting entry rather than mutation. A fraud alert received after shipment may still open an investigation. A window operator's state cleanup cannot decide these obligations by itself.

Deduplication consumes durable state. Retaining identifiers for seven days may be useless when disaster recovery replays thirty. Retaining permanent raw identifiers may violate privacy or scale limits. Hashing can reduce exposure but creates collision and key-rotation considerations.

Silent disposal destroys evidence. Engineers cannot diagnose whether “missing revenue” came from invalid input, watermark policy, dedup false match, stale-version suppression, or sink rejection if these all increment one dropped counter. Mutually exclusive disposition accounting makes loss visible.

## Prerequisites and Retrieval

Retrieve occurrence identity: business event ID; producer/message ID; entity key; tenant/source namespace; generation; canonical encoding; idempotency key; semantic fingerprint fields; correction/supersedes relation; and collision/conflict policy.

Retrieve all order relations: topic/partition/offset; producer epoch/sequence; database transaction/LSN; entity version; causal parent; event time and uncertainty; ingest time; attempt; snapshot marker; and tie rule. Ask which relation each consumer actually requires.

Retrieve delivery behavior: publisher retry; broker guarantee; lease/ack deadline; negative acknowledgment; consumer commit boundary; rebalance; checkpoint; source restart; connector batch/offset flush; sink transaction; replay; and regional scope.

Retrieve lateness evidence: event-time authority; watermark per input/operator; window end; grace/allowed lateness; history retention; state cleanup; event-minus-ingest distribution; offline sources; future timestamps; expected backfill; and business correction deadline.

Retrieve state: dedup receipts and fingerprints; first/last observation; expiry clock; entity current/history versions; seen sequence ranges; gap set; reorder buffers; timers; window accumulators; correction ledger; source positions; checkpoint/changelog; and rebuild authority.

Retrieve disposition paths: applied update; accepted stale evidence; exact duplicate suppression; identity-conflict quarantine; invalid schema/security quarantine; too-late online rejection; repair ledger; dead-letter/side output; replay hold; and manual adjudication.

Retrieve output semantics: append, upsert, retraction, changelog, compensating event, adjusting ledger entry, notification, cache, API finality/version, idempotency, ordering, and consumer acknowledgment of corrections.

Retrieve capacity and abuse evidence: identities/second; receipt bytes; retention; distinct keys; reorder events/bytes/key; maximum gaps; late tail; quarantine rate; conflict cardinality; fingerprint cost; Bloom false-positive target; hot/malicious IDs; and cleanup/checkpoint/restore load.

Retrieve governance: sensitive fingerprint fields; hashing/key rotation; tenant isolation; retention/erasure/legal hold; evidence access; quarantine encryption; replay authorization; manual repair separation of duties; and audit.

Retrieve change history: identity version; canonicalization/fingerprint version; dedup horizon; clock; watermark/grace; version comparator; reorder bounds; output mutation; state schema; source retention; connector/runtime version; cutover; rollback; and historical rematerialization.

Distinguish transport message ID from business occurrence ID; redelivery from duplicate publish; duplicate from equal payload; exact duplicate from identity conflict; entity key from event ID; offset order from event/business/causal order; delay from lateness; late from stale; gap from loss; accepted stale evidence from applied current update; online state cleanup from business finality; and disposition from overlapping diagnostic label.

Create a disorder contract:

| Concern | Required decision and evidence |
|---|---|
| Identity | Namespace, occurrence key, generation, canonical fingerprint, conflict and version |
| Order | Relation, scope, sequence/version/timestamp, ties, gaps and authority |
| Lateness | Progress/deadline/window, equality, grace, retained state and business horizon |
| Dedup | Receipt contents, atomicity, horizon, expiry clock, old-replay and collision path |
| Reorder | Buffer key, expected sequence, wait/count/byte bound, gap resolution and liveness |
| Mutation | Apply/stale/retract/upsert/correct semantics, sink identity and consumer contract |
| Routing | Exact duplicate, conflict, invalid, too-late, repair, quarantine and ownership |
| Recovery | Source cut, state/timers, replay/backfill generation, checkpoint and reconciliation |
| Evidence | Primary disposition counts, diagnostic labels, exemplars, oracle and audit |

Write a falsifiable claim: “Policy `account-events-v5` uses tenant-scoped occurrence ID plus canonical semantic digest, retains receipts for the 45-day maximum disaster/backfill horizon plus five days, applies only strictly increasing signed entity versions, records and times out sequence gaps, accepts event-time corrections online for seven days, routes older valid events to a repair ledger, emits revisioned upserts/retractions, and reconciles each exact source cut into one primary disposition with no unexplained residue.”

## Learning Objectives

After completing this module, you should be able to:

1. distinguish redelivery, exact duplicate, identity conflict, repeated occurrence, lateness, staleness, gaps, and disorder;
2. design canonical occurrence IDs and semantic fingerprints without merging valid equal-valued events;
3. name and enforce partition, source, causal, entity-version, and event-time order separately;
4. implement bounded dedup receipts and calculate retention from retry/replay/correction horizons;
5. design gap-aware reorder buffers with explicit latency, bytes, and liveness limits;
6. apply stale/new/corrected versions through compatible upsert, retraction, or ledger semantics;
7. route invalid, conflicting, and too-late evidence without silent obligation loss;
8. isolate replay/backfill from live progress and identity state;
9. capacity-plan identity, version-history, gap, buffer, quarantine, and correction state; and
10. fault-test and reconcile every input to a primary disposition and authoritative finite result.

## Core Exposition

### Classify identity before suppressing records

Start with the business occurrence. A payment authorization, sensor sample, user click, and account-version update need different identifiers. Namespace by tenant/source/type and include a generation when IDs can restart after device reset or restore.

Store a canonical semantic fingerprint with the receipt. Canonicalization specifies included fields, ordering, number/string/time normalization, absent versus null, schema/default version, and excluded transport metadata. A cryptographic digest reduces storage but does not repair ambiguous semantics.

When identity and fingerprint match, suppression may be safe within the receipt's effect scope. When identity matches and fingerprint differs, quarantine both versions and prevent an automatic winner unless the domain defines signed revision authority. A conflict metric must not be hidden inside duplicate count.

Never infer occurrence identity solely from payload equality. Two \$10 purchases by one customer may be legitimate. Conversely, a retry may add a new attempt timestamp and no longer be byte-equal.

### Separate delivery attempts from producer occurrences

A broker redelivery often retains the same transport message ID. Google Cloud Pub/Sub explicitly distinguishes valid redelivery after deadline/negative acknowledgment from an unexpected duplicate, and its exactly-once scope uses a service-defined message ID within stated subscription/region constraints. Multiple publisher submissions can still represent separate service messages.

Debezium documents at-least-once delivery in which records can repeat, including after crash/restart around offset persistence. A source LSN/transaction/row identity can support downstream dedup, but its granularity must match the logical change.

Record message ID, delivery attempt, lease/ack ID, source offset, and business occurrence ID separately. A transport feature reduces one class of repeats; it does not deduplicate business-level double publication or external effects automatically.

### Name the order relation and its scope

Partition offsets provide a total order only within a partition generation. Source LSNs order database log positions. Entity versions order changes for one entity. Causation IDs create partial order. Event timestamps support temporal analysis with clock uncertainty. Arrival order says only what one observer saw.

Do not synthesize a global total order across independent partitions by comparing offsets or worker clocks. If a computation is associative/commutative, exploit that. If it requires one order, route the relevant domain key to one owner or use an authoritative sequencer.

Kafka Streams documents causes of timestamp disorder even while processing records in partition offset order. That is not contradiction: offset and event-time orders differ.

### Apply entity versions, not last arrival

For current version $q^*$, accept a record with $q>q^*$ under gap/conflict policy, retain but do not overwrite for $q<q^*$, and require equality or explicit conflict handling for $q=q^*$. A tombstone/delete also carries a version; otherwise an old create can resurrect deleted state.

An advance from version 10 to 13 opens gap `[11,12]` if contiguity is expected. It may still be correct to expose version 13 immediately while tracking the gap. Another domain may buffer 13 until gaps fill. State the liveness/correctness choice.

Timestamp-based latest is valid only when timestamp authority, equality, corrections, and clock bounds define the business version. Kafka Streams versioned stores expose timestamp-based table semantics and history retention, contrasting with offset-based latest; use the exact product behavior rather than generalizing it to every stream.

### Design dedup state as a durable index

One atomic decision must read/insert the receipt and coordinate the protected state/effect. A non-atomic “check then act then remember” races concurrent deliveries and crashes between the effect and receipt.

Receipt contents can include identity, semantic digest, first source coordinate, accepted outcome/effect ID, policy version, created/expiry, and conflict evidence. Store only what is needed; sensitive payload copies increase risk.

Derive retention from the longest repeat source, not ordinary retry p99. Include source retention/replay, disaster restore, authorized backfill, producer offline buffer, and correction. If permanent effects outlive feasible receipts, reconcile old replay against a permanent target ledger.

Expiry uses a named clock. Event-time expiry can stall with watermarks; processing-time expiry advances during outages; wall-clock correction can affect naive jobs. Recovery must preserve the same logical receipt horizon.

### Use approximate membership only with a safe false-positive path

A Bloom or Cuckoo-style filter can cheaply reject most unseen checks or reduce remote lookups. A positive Bloom result can be false, so it cannot authoritatively discard a payment or compliance record without checking an exact store. A negative result has the structure's documented guarantee only while construction/state is correct.

Size the filter from expected insertions and acceptable false-positive probability, monitor saturation, version/hash seeds, and rebuild safely. Tenant/adversarial identity floods can poison shared capacity.

Use approximate structures as accelerators or for explicitly loss-tolerant analytics, never as an unlabeled business truth.

### Define lateness relative to a decision

A record can be behind a watermark yet still accepted during allowed lateness. It can be too late for one online window but timely for a regulatory correction deadline. It can be delayed six hours but arrive before a monthly close.

Record the decision frontier: input/operator watermark, window end, grace, state cleanup, entity history retention, or business deadline. Define exact equality from the runtime contract. DE-058 supplies the window/watermark mechanics.

Spark's structured streaming APIs document watermark-bounded deduplication and note that sufficiently old data may be dropped. Flink can retain allowed-late events and route those beyond its window policy to a side output. These are operator behaviors, not universal obligation policies.

### Preserve too-late evidence and repair ownership

For each valid too-late record, decide whether to update an online materialization, create an immutable correction, rebuild a partition, adjust a ledger, notify a user, or document accepted loss. Side output alone is plumbing, not repair.

Carry original payload/reference, event ID, source coordinate, event/arrival times, observed watermark/window, policy version, decision reason, target result IDs, and adjudication status. Encrypt and minimize according to classification.

Quarantine queues need SLOs, capacity, replay idempotency, poison isolation, escalation, and terminal resolution. An unowned dead-letter topic is deferred data loss.

### Bound reorder buffers and gaps

A sequence reorderer maintains expected next $q_e$, a map/heap of future versions, and a timer/deadline. On $q=q_e$, emit and drain consecutive buffered versions. On $q>q_e$, buffer and record the missing range. On $q<q_e$, classify duplicate/stale/conflict using retained history.

Bound per-key and global event count, bytes, sequence distance, event/processing wait, and source health. When bounds expire, choose skip-with-gap, emit marked partial, request retransmission, quarantine future values, rebuild from authority, or fail the key—not indefinite blocking.

Future timestamps cannot define buffer release without validation. Sequence wrap/reset and source generation must be explicit so `1` after restart is not mistaken for ancient data.

### Prefer commutative or version-aware designs when possible

Some aggregates can apply out of order: set union, maximum monotone version, or commutative sums over unique occurrence IDs. This eliminates reorder latency but not dedup identity, deletion, or correction semantics.

Last-write-wins is order-sensitive even if expressed as maximum timestamp. A version-aware map retains prior versions or uses authoritative sequence. CRDT-like merges require proven algebra and domain conflict resolution; calling an operation commutative does not make double application idempotent.

Document whether output converges after all accepted records or whether every intermediate output must be correct.

### Emit corrections that consumers can apply

For an aggregate contribution $f(x)$ replaced by corrected $x'$, emit a retraction and addition or an upserted total:

$$
A'=A-f(x)+f(x').
$$

Do not append the new total to an additive sink. Include materialization/window/entity key, revision, supersedes ID, source cut, policy version, and correction reason. Sink writes reject stale revisions and retry idempotently.

Kafka Streams models aggregation output as a table/changelog so an out-of-order update can replace the prior keyed result under supported semantics. Beam's accumulating/discarding panes and allowed-late firings likewise require consumers to understand pane meaning.

Irreversible notifications and actions need a separate policy. A corrected dashboard is easy; retracting a shipped item or sent message is not. Use hold periods, confirmation states, compensating workflows, or accept provisional risk explicitly.

### Align state and retention horizons

Dedup receipt horizon, versioned-store history, reorder buffer, window grace, state TTL, source log retention, changelog/checkpoint retention, sink idempotency, and correction ledger must compose. The shortest link can define actual safety.

If source history retains 30 days but dedup receipts retain 7, disaster replay can double days 8–30. If table history is one hour but stream join grace is two, an older stream record cannot retrieve the required table version. If state TTL expires before late acceptance, the operator reinitializes instead of correcting.

Capacity estimates include identity cardinality, fingerprint/metadata, indexes, version history, gaps, buffers, timers, quarantine, checkpoint/changelog amplification, and replay load. Measure distributions and adversarial keys.

### Isolate replay and backfill generations

Replay can repeat every event intentionally. A correct deduplicator either restores receipts/state at the matching source cut or rebuilds all outputs in a separate generation. Starting from empty receipts while writing to live sinks turns historical occurrences into new effects.

Backfill timestamps may be behind live watermarks and version histories. Use isolated progress/state/output, explicit source ranges, pinned identity/fingerprint/order policies, and deterministic effect IDs. Merge only at a named cut with consumer rules.

Reprocessing with a corrected policy should not be suppressed by old receipts accidentally. Namespace materialization/policy generation while preserving business occurrence identity and lineage.

### Reconcile dispositions and diagnostic labels

Choose primary dispositions that partition inputs. For example:

$$
N_{in}=N_{update}+N_{stale}+N_{exactdup}+N_{conflict}+N_{toolate}+N_{invalid}.
$$

This equality requires a precedence rule. An invalid record with a repeated raw ID might be both diagnostically duplicate and invalid, but it has one primary route. Labels such as late, replayed, gap-opening, gap-closing, future-clock, and corrected may overlap and therefore must not be summed as a partition.

Reconcile accepted source identities to current materialization and correction ledger at exact cuts. Explain every residue: buffered, in flight, quarantined, expired, or lost under an approved policy.

### Observe disorder and repair health

Measure redeliveries by cause/attempt, exact duplicate and identity conflict rates, distinct IDs, receipt hit/expiry, stale/new/equal versions, opened/closed/aged gaps, reorder events/bytes/wait, lateness distribution, accepted versus too-late, future/invalid timestamps, side-output/quarantine depth/age, corrections/retractions, stale sink revisions, and reconciliation residue.

Break down by source, partition, schema, tenant, producer/runtime version, and deployment. A spike confined to one producer suggests identity or clock regression; all partitions may indicate recovery replay.

Trace exemplars with privacy-safe IDs, source coordinates, fingerprint/policy version, current/record version, watermark/deadline, primary disposition, labels, state/checkpoint generation, and repair outcome.

### Test adversarial histories and change

Test exact duplicates before/during/after receipt expiry; conflicting reuse; equal payload/different ID; different payload/same ID; identity collision; producer generation reset; sequence wrap; gap open/close/timeout; version equality; delete/resurrection; and multi-partition reorder.

Test watermark boundary equality, future timestamp, late within/beyond grace, cleanup, offline upload, source stall, snapshot/CDC overlap, crash around receipt/effect/offset, rebalance, restore, old disaster cut, backfill/live collision, and quarantine replay.

Migrate identity, fingerprint, version, horizon, watermark, buffer, or sink semantics through dual state/output generations. Compare decisions for each exact input cut, investigate cohort deltas, test rollback after new-format writes, and require domain approval for changed totals or discarded obligations.

### Review the complete disorder argument

A defensible design connects fifteen claims: occurrence identity is correct; fingerprints detect conflict; transport attempts remain separate; order relation is named; entity versions guard current state; gaps and buffers are bounded; lateness frontier is recorded; valid too-late evidence has repair; dedup horizon covers replay; approximate filters cannot silently lose; state and source cuts recover; corrections match sink/consumer semantics; replay/backfill is isolated; disposition counts reconcile; and adversarial/fault/migration tests validate outcomes.

If one link is missing, narrow the claim. A pipeline can suppress transport repeats yet double business events, retain every late record yet apply stale state, order by timestamp yet violate entity versions, or reconcile counts while misclassifying legitimate equal-valued occurrences.

## Definitions and Notation

For input record $x$, define:

- $i(x)$: canonical occurrence identity including namespace/generation.
- $h_v(x)$: canonical semantic fingerprint under version $v$.
- $e(x)$: entity/business state key.
- $q(x)$: authoritative version/sequence when defined.
- $t_e(x)$: authoritative event timestamp.
- $a(x)$: arrival attempt metadata and source coordinate.
- $W(x)$: relevant observed watermark/progress at decision.
- $R[i]$: retained dedup receipt.
- $Q[e]$: current accepted entity version.
- $G[e]$: missing sequence ranges.
- $B[e]$: bounded reorder buffer.
- $H$: dedup retention horizon.
- $L$: online lateness/correction allowance under an explicit boundary.

Diagnostic lateness distance is

$$
\ell(x)=\max(0,W(x)-t_e(x)).
$$

This does not by itself decide acceptance because window end, grace, state retention, history, and business deadlines also matter.

Identity classification while the receipt is retained is

$$
D_i(x)=
\begin{cases}
new, & i(x)\notin R,\\
exact, & i(x)\in R\land h_v(x)=R[i].h,\\
conflict, & i(x)\in R\land h_v(x)\ne R[i].h.
\end{cases}
$$

For current entity version $q^*=Q[e]$:

$$
D_q(x)=
\begin{cases}
advance, & q(x)>q^*,\\
equal, & q(x)=q^*,\\
stale, & q(x)<q^*.
\end{cases}
$$

When contiguity is required, advance $q>q^*+1$ opens the integer gap

$$
[q^*+1,q-1].
$$

Later arrival in this range may close evidence without rolling current state backward.

The dedup retention condition is

$$
H\ge\max(H_{retry},H_{replay},H_{DR},H_{backfill},H_{correction})+M.
$$

If storage cannot satisfy it, the older path must consult a longer-lived authority or explicitly accept loss/duplication.

For corrected aggregate contribution,

$$
A_{new}=A_{old}-f(x_{old})+f(x_{new}).
$$

An upsert may publish $A_{new}$; a delta/changelog publishes the negative and positive contributions with deterministic identities.

With mutually exclusive primary dispositions $P$, reconciliation requires

$$
N_{in}=\sum_{p\in P}N_p.
$$

Overlapping diagnostic labels are analyzed as sets/intersections and are not substituted into this sum.

## Mechanisms, Invariants, or Proof Structure

Use this review sequence:

1. **Name occurrence identity.** Define namespace, generation, canonicalization, fingerprint version, correction relation, and conflict authority.
2. **Inventory attempts and coordinates.** Preserve producer/message/delivery IDs, source transaction/partition/offset, checkpoint, and replay context.
3. **Name each order.** Specify partition/source/entity/causal/event relation, scope, tie/gap/reset rule, and which decision uses it.
4. **Classify primary disposition.** Apply validation, retained identity conflict/exactness, online lateness, and version rules with documented precedence.
5. **Bound memory.** Set receipt/history/buffer/gap/timer/quarantine horizons from retry, replay, disaster, backfill, correction, and abuse evidence.
6. **Apply or repair.** Advance, retain stale, suppress, quarantine, buffer, retract/upsert, adjust ledger, rebuild, or accept documented loss.
7. **Coordinate recovery/effects.** Couple decisions with source positions and state; use deterministic sink identities and reconciliation.
8. **Isolate replay/change.** Separate generations, pin policies/cuts, dual-run new identity/order/lateness semantics, compare, cut over, and roll back.
9. **Observe.** Reconcile disposition totals; measure overlapping labels, state, gap/buffer, lateness, conflict, repair, and residue.
10. **Test.** Exercise boundaries, collisions, reorder, crash windows, old replay, future clocks, migration, and authoritative finite oracles.

The identity invariant is:

> A canonical occurrence ID identifies one semantic occurrence within its namespace/generation; matching fingerprints suppress retries, while mismatches create visible conflicts.

The order invariant is:

> Current state advances only under the declared authoritative version/order relation; arrival, offset, and event-time order are never substituted silently.

The obligation invariant is:

> Every valid record either contributes to the intended materialization or enters a durable, owned correction/reconciliation outcome; online lateness and cleanup do not erase domain obligations.

The accounting invariant is:

> Every observed input has exactly one primary disposition, while nonexclusive diagnostic labels remain separately queryable and traceable to the decision evidence.

This executable demonstrates exact/conflicting duplicates, version advance/gaps, accepted stale late evidence, a too-late repair route, and disposition reconciliation. It uses supplied fingerprints and integer progress; it does not prove identity authority, real watermark safety, storage atomicity, or a production correction policy.

<!-- bijux-verify: {"id":"disorder-dispositions","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"decisions=((0, 'r1', 'update'), (1, 'r1', 'exact_duplicate'), (2, 'r3', 'update_gap_2_2'), (3, 'r2', 'stale_late'), (4, 'r3', 'identity_conflict'), (5, 'r4', 'too_late'))\nlatest_state=(('acct', (3, 9)),)\nreceived_versions=(('acct', (1, 2, 3)),)\nopen_gaps=()\naccepted_ids=('r1', 'r3', 'r2')\nexact_duplicate_ids=('r1',)\nconflicting_ids=('r3',)\nlate_accepted_ids=('r2',)\ntoo_late_ids=('r4',)\ndisposition_counts=(('exact_duplicate', 1), ('identity_conflict', 1), ('stale_late', 1), ('too_late', 1), ('update', 1), ('update_gap_2_2', 1))\ninput_count_reconciles=True\n","stderr":""}} -->
```python
records = (
    {"id": "r1", "entity": "acct", "version": 1, "event": 10, "value": 5, "fingerprint": "h1", "watermark": 0},
    {"id": "r1", "entity": "acct", "version": 1, "event": 10, "value": 5, "fingerprint": "h1", "watermark": 5},
    {"id": "r3", "entity": "acct", "version": 3, "event": 30, "value": 9, "fingerprint": "h3", "watermark": 15},
    {"id": "r2", "entity": "acct", "version": 2, "event": 20, "value": 7, "fingerprint": "h2", "watermark": 35},
    {"id": "r3", "entity": "acct", "version": 3, "event": 30, "value": 10, "fingerprint": "conflict", "watermark": 35},
    {"id": "r4", "entity": "other", "version": 1, "event": 5, "value": 4, "fingerprint": "h4", "watermark": 50},
)
online_lateness = 20
receipts = {}
latest = {}
received = {}
decisions = []
accepted = []
exact = []
conflicts = []
late_accepted = []
too_late = []

for index, record in enumerate(records):
    identifier = record["id"]
    if identifier in receipts:
        if receipts[identifier] == record["fingerprint"]:
            decision = "exact_duplicate"
            exact.append(identifier)
        else:
            decision = "identity_conflict"
            conflicts.append(identifier)
        decisions.append((index, identifier, decision))
        continue

    lateness = max(0, record["watermark"] - record["event"])
    if lateness > online_lateness:
        decision = "too_late"
        too_late.append(identifier)
        decisions.append((index, identifier, decision))
        continue

    receipts[identifier] = record["fingerprint"]
    accepted.append(identifier)
    entity = record["entity"]
    versions = received.setdefault(entity, set())
    versions.add(record["version"])
    current_version, current_value = latest.get(entity, (0, 0))

    if record["version"] > current_version:
        if record["version"] > current_version + 1:
            decision = f"update_gap_{current_version + 1}_{record['version'] - 1}"
        else:
            decision = "update"
        latest[entity] = (record["version"], record["value"])
    else:
        decision = "stale_late" if lateness > 0 else "stale"
        if lateness > 0:
            late_accepted.append(identifier)
    decisions.append((index, identifier, decision))

gaps = []
for entity, (maximum, _) in sorted(latest.items()):
    missing = sorted(set(range(1, maximum + 1)) - received[entity])
    if missing:
        gaps.append((entity, tuple(missing)))

counts = {}
for _, _, decision in decisions:
    counts[decision] = counts.get(decision, 0) + 1

print(f"decisions={tuple(decisions)}")
print(f"latest_state={tuple(sorted(latest.items()))}")
print(f"received_versions={tuple((key, tuple(sorted(value))) for key, value in sorted(received.items()))}")
print(f"open_gaps={tuple(gaps)}")
print(f"accepted_ids={tuple(accepted)}")
print(f"exact_duplicate_ids={tuple(exact)}")
print(f"conflicting_ids={tuple(conflicts)}")
print(f"late_accepted_ids={tuple(late_accepted)}")
print(f"too_late_ids={tuple(too_late)}")
print(f"disposition_counts={tuple(sorted(counts.items()))}")
print(f"input_count_reconciles={sum(counts.values()) == len(records)}")
```

The 20-unit lateness threshold and fingerprints are supplied assumptions. A production design derives identity, canonicalization, ordering, progress, retention, atomicity, and repair from authoritative evidence.

## Alternatives and Trade-Offs

**Business occurrence ID versus transport message ID.** Business identity survives republishing and broker changes but must be designed by the domain. Transport IDs are readily available and strong only within their documented delivery scope.

**First-seen versus last-seen dedup.** First-seen is stable and cheap but can preserve an incomplete/corrupt first record. Last-seen permits correction but needs version authority and retractions. Identity conflicts should not be resolved by arrival implicitly.

**Exact store versus approximate filter.** Exact receipts support authoritative equality/conflict checks at higher storage/lookup cost. Approximate filters save resources but need a safe exact fallback or explicit loss tolerance.

**Permanent receipts versus bounded horizon.** Permanent memory protects arbitrarily old replay but grows and complicates privacy. Bounded receipts control cost but require source/recovery bounds or a permanent external ledger.

**Apply newest version immediately versus buffer gaps.** Immediate advance improves liveness/freshness but exposes incomplete history. Buffering preserves contiguous order but can block indefinitely and consume state.

**Reorder buffer versus commutative merge.** Buffering reproduces required order at latency/state cost. A proven commutative/version-aware operation accepts disorder efficiently but may not support noncommutative workflows.

**Offset-based latest versus timestamp/version-based latest.** Offset order is deterministic within a partition but may not express business recency. Timestamp/version semantics fit domain order when authoritative but require history, ties, and late policy.

**Online correction versus repair ledger.** Online update keeps current views fresh while state exists. A ledger preserves late obligations after cleanup and audit close but adds reconciliation latency and workflow.

**Upsert versus retraction stream.** Upserts simplify latest-state consumers but can obscure old contribution history. Retractions express algebraic changes but require ordered, idempotent downstream application.

**Long grace/history versus bounded state.** Longer horizons accept more disorder and improve historical lookup while increasing state, checkpoint, restore, and output revision cost.

**Side output versus inline handling.** Side outputs isolate exceptional work and main-path latency but can become unowned queues. Inline repair preserves one transaction flow but complicates and slows normal processing.

**Strict sequence versus gap-tolerant progress.** Strict sequencing protects dependent transitions but sacrifices liveness on loss. Gap-tolerant processing must mark uncertainty and define later closure/correction.

**Live replay with restored receipts versus isolated rebuild.** Restored receipts can safely resume the same generation. Isolated rebuild handles changed policy and full recomputation at duplicate infrastructure and cutover cost.

## Failure Modes and Misconceptions

**“Same payload means duplicate.”** Legitimate occurrences can have identical values; identity must represent occurrence.

**“Different message ID means new business event.”** Publisher retries can create multiple messages for one occurrence.

**“Redelivery means the broker malfunctioned.”** Deadline expiry, negative acknowledgment, or uncertain commit can make redelivery expected.

**“Exactly-once delivery deduplicates the producer.”** Service guarantees are scoped to service message identity and do not merge separate publishes.

**“Same event ID always means suppress.”** Different fingerprints under one ID signal corruption, collision, or unauthorized rewrite.

**“Hashing creates identity.”** A digest represents canonical bytes; it cannot decide which fields define one occurrence.

**“Offset is a global sequence.”** It is local to a partition/generation and differs from entity, causal, and event-time order.

**“Timestamp is the version.”** Clock skew, equal values, correction, and different authorities can invert or tie records.

**“Last arrival wins eventually.”** A stale retry can arrive last and permanently regress state.

**“A version gap proves record loss.”** The record may be delayed, filtered, in another transaction/partition, or the sequence may intentionally skip.

**“Wait for every gap forever.”** Missing or poisoned sequence stalls liveness and grows buffers without bound.

**“Behind watermark means discard.”** Allowed lateness, retained state, operator semantics, and business correction can still admit it.

**“Not in the online window means irrelevant.”** Financial, legal, safety, or customer obligations can outlive state cleanup.

**“Side output handles late data.”** It only routes records; repair needs identity, ownership, SLO, mutation, and reconciliation.

**“Bloom positive proves duplicate.”** False positives exist; authoritative loss-intolerant suppression needs exact confirmation.

**“Receipt TTL can match normal retry.”** Disaster restore, replay, offline sources, and backfill often exceed ordinary retries.

**“State retention can exceed source retention harmlessly.”** Receipts without reconstructable source may not support audit, while source without receipts can replay unsafe effects.

**“An updated aggregate can be appended.”** Accumulating totals need replacement; correction deltas need explicit negative/positive semantics.

**“Exactly-once state removes duplicate effects.”** Sink/target identity and commit uncertainty remain.

**“Replay should be deduplicated away.”** Same-generation recovery suppresses repeats; intentional rematerialization may need a new output generation while preserving lineage.

**“Low duplicate count proves healthy input.”** Conflicts, invalids, too-late drops, and expired-receipt repeats may be elsewhere or invisible.

**“Late + stale + duplicate totals should equal input.”** These labels can overlap; only precedence-defined primary dispositions form a partition.

## Worked Examples

### Example 1

A subscriber processes message `m7`, then its acknowledgment response is lost. Redelivery retains `m7`. The consumer's occurrence receipt returns the prior result and acknowledges the new attempt; it does not run the payment effect again.

### Example 2

A publisher times out and generates a new UUID on retry for the same order command. The broker sees two distinct messages. A caller-supplied order-command ID exposes one business occurrence; message-ID dedup alone would fail.

### Example 3

Two customers each buy the same SKU for the same price at the same second. Payload fingerprints match except occurrence IDs. A payload-wide `DISTINCT` would delete legitimate revenue; occurrence identity retains both.

### Example 4

Event `e9` first arrives with amount 10, then the same ID arrives with amount 100. The receipt digest differs. The system quarantines the conflict, preserves both source coordinates, and blocks automatic current-state change pending signed correction authority.

### Example 5

Entity versions arrive 10, 13, 12, 11. A freshness-oriented projection exposes 13 immediately, records gap 11–12, then closes evidence as older versions arrive without rolling current state backward. An audit projection retains the full version sequence.

### Example 6

A device measurement is six hours delayed but a daily window retains seven days of corrections. It is late relative to the watermark and accepted by the online correction policy. Delay magnitude alone did not determine disposition.

### Example 7

A valid tax adjustment arrives after window state and grace expire but before the filing correction deadline. It enters a correction ledger and generates an adjusting entry tied to the closed report, rather than disappearing or mutating the signed original invisibly.

### Example 8

A Bloom filter reports that a new claim ID was probably seen. The exact receipt store has no row, so processing continues. Treating the approximate positive as authoritative would have silently lost a legitimate claim.

### Example 9

A disaster restore replays 21 days while receipts retain 7. The system compares days 8–21 against a permanent target ledger before effects and restores recent receipts at the matching cut. Normal consumer processing does not assume the short TTL is sufficient.

### Example 10

A future-dated malicious record would push a timestamp-based reorder frontier forward and mark normal records late. Timestamp validation quarantines it before progress influence; source sequence continues to govern entity order.

## Cross-Program Connections

Distributed systems contributes at-least-once delivery, uncertain acknowledgment, partial order, failure detectors, idempotence, fencing, consensus, and replay.

Database systems contributes unique constraints, conditional/versioned writes, MVCC history, transactions, CDC/LSNs, tombstones, temporal tables, and correction ledgers.

Algorithms and data structures contributes hash indexes, Bloom/Cuckoo filters, interval/range sets, heaps, reorder buffers, sketches, TTL wheels, and complexity bounds.

Probability and statistics contributes delay-tail estimation, false-positive rates, collision probability, anomaly detection, censored samples, and risk-based horizons.

Formal methods contributes state-machine invariants, partial orders, commutativity, idempotence, convergence, refinement, and adversarial trace exploration.

API and service engineering contributes idempotency keys, canonical request fingerprints, conditional requests, status resources, retries, webhook redelivery, and correction versions.

Platform engineering contributes broker delivery scope, partitioning, checkpoint/changelog state, managed side outputs, quotas, replay controls, and tenant isolation.

Site reliability engineering contributes retry/backlog metrics, replay drills, quarantine SLOs, capacity, fault injection, runbooks, and reconciliation residue alerts.

Security engineering contributes identity forgery, replay attacks, malicious future timestamps, state-exhaustion floods, signed versions, tenant namespace, and evidence integrity.

Privacy and governance contributes minimization, hashed identity, retention/erasure, legal hold, quarantine access, correction lineage, and accountable disposition.

Accounting contributes immutable entries, reversals, adjusting periods, balance reconciliation, close, and the difference between restatement and hidden overwrite.

Machine learning contributes online feature corrections, label delay, point-in-time joins, training/serving consistency, dedup leakage, and late-label backfill.

## References

1. Apache Beam. [Programming Guide](https://beam.apache.org/documentation/programming-guide/). Accessed 2026-09-03. Primary documentation for watermarks, allowed lateness, early/on-time/late triggers, accumulation modes, panes, state, and timers.
2. Apache Flink. [Windows](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/operators/windows/). Accessed 2026-09-03. Primary documentation for event-time late elements, allowed lateness, retained window state, late firings, cleanup, and side outputs.
3. Apache Flink. [Deduplication](https://nightlies.apache.org/flink/flink-docs-stable/docs/sql/reference/queries/deduplication/). Accessed 2026-09-03. Primary SQL documentation for first/last row deduplication by partition columns and processing- or event-time ordering.
4. Apache Spark. [Structured Streaming Programming Guide](https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html). Accessed 2026-09-03. Primary documentation for watermark-bounded state, late-data guarantees, deduplication, joins, and multiple-watermark trade-offs.
5. Apache Spark. [`dropDuplicatesWithinWatermark`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.dropDuplicatesWithinWatermark.html). Accessed 2026-09-03. Primary API documentation for stateful duplicate suppression within a watermark delay and treatment of data older than progress.
6. Apache Kafka. [Kafka Streams Core Concepts, Apache Kafka 4.3](https://kafka.apache.org/43/streams/core-concepts/). Accessed 2026-09-03. Primary documentation for offset versus timestamp disorder, grace periods, changelog table updates, stateful operation effects, and join qualifications.
7. Apache Kafka. [Kafka Streams DSL, Apache Kafka 4.3](https://kafka.apache.org/43/streams/developer-guide/dsl-api/). Accessed 2026-09-03. Primary documentation for window grace, update tables, versioned-store timestamp semantics, history retention, joins, and suppression constraints.
8. Apache Kafka. [Processor API, Apache Kafka 4.3](https://kafka.apache.org/43/streams/developer-guide/processor-api/). Accessed 2026-09-03. Primary documentation for timestamped/versioned state stores, out-of-order writes, partition-scoped stream time, history retention, and performance trade-offs.
9. Debezium. [Exactly-Once Delivery](https://debezium.io/documentation/reference/configuration/eos.html). Accessed 2026-09-03. Primary documentation distinguishing Debezium's at-least-once baseline and possible repeated records from Kafka Connect exactly-once support.
10. Debezium. [Debezium Engine](https://debezium.io/documentation/reference/development/engine.html). Accessed 2026-09-03. Primary documentation for crash/restart duplicate exposure, offset flush and batch effects, and downstream tolerance requirements.
11. Google Cloud. [Pub/Sub Exactly-Once Delivery](https://cloud.google.com/pubsub/docs/exactly-once-delivery). Accessed 2026-09-03. Primary product documentation distinguishing valid redelivery from duplicates, message-ID scope, acknowledgment outcomes, publisher duplicates, and regional/subscription constraints.

## Exercises

### Exercise 1

Process records `(id,entity,version,event,value,fingerprint,watermark)` in order: `(r1,a,1,10,5,h1,0)`, matching `r1` at watermark 5, `(r3,a,3,30,9,h3,15)`, `(r2,a,2,20,7,h2,35)`, conflicting `(r3,a,3,30,10,hX,35)`, and `(r4,b,1,5,4,h4,50)`. With online lateness allowed through distance 20 and retained receipts, give each primary disposition, final current state, received versions/gaps, and overlapping late-accepted cohort.

### Exercise 2

Automatic retries can last 45 minutes, source replay 14 days, disaster restore 35 days, authorized backfill 60 days, correction 21 days, and safety margin 7 days. Compute minimum dedup horizon. Explain how a target with permanent effect receipts can qualify replay beyond a shorter online receipt store.

### Exercise 3

A reorderer has expected sequence 40 and receives 42, 44, 41, 43. Show buffer/gap/drain state after each arrival. Then suppose 40 never arrives and bounds are 3 buffered events or 30 seconds. Describe at least three valid timeout policies and their semantic costs.

### Exercise 4

An aggregate is 100 from occurrence `x` contributing 12. A signed correction `x2` supersedes `x` and contributes 17. Compute corrected aggregate using retraction/addition. Specify immutable changelog records and an upsert representation that remain idempotent under replay; explain why appending total 105 to an additive sink is wrong.

### Exercise 5

Design a migration from payload-hash-only, seven-day first-seen dedup with last-arrival-wins state and silent late drop to tenant-scoped occurrence IDs, canonical fingerprints, 67-day receipts, entity versions/gaps, repair ledger, and revisioned upserts. Include source cuts, dual decisions, state/output generation, backfill, consumer change, conflicts, privacy, capacity, cutover, rollback, and reconciliation.

## Answers to the Exercises

### Answer 1

The first `r1` is `update`; matching `r1` is `exact_duplicate`. `r3` is `update_gap_2_2` and makes current `a=(version 3,value 9)`. `r2` has lateness $35-20=15$, so it is accepted within 20 but is stale relative to version 3; primary disposition is `stale_late`, it joins diagnostic cohort `late-accepted`, and it fills received version 2. Conflicting `r3` is `identity_conflict` because its retained fingerprint differs. `r4` has lateness $50-5=45>20$, so it is `too_late`. Final current state contains only `a=(3,9)`; received versions for `a` are `{1,2,3}` and no gap remains. Six primary dispositions reconcile six inputs; late is an overlapping diagnostic label.

### Answer 2

The maximum exposure is the 60-day authorized backfill. Adding 7 days gives minimum horizon 67 days under the formula. The online store must also use an expiry clock and atomic receipt/effect rule that survive recovery. If cost/privacy prevents 67-day online receipts, an older replay can query a permanent target ledger keyed by occurrence/effect identity before acting, route uncertain cases to reconciliation, and keep live automatic retry on the shorter fast path. The permanent ledger must itself be complete, tenant-scoped, queryable at the required cut, retained, and protected from collision/conflicting intent.

### Answer 3

Expected 40 receiving 42 buffers 42 and records gaps 40–41. Receiving 44 buffers 44 and gaps 40–41 plus 43. Receiving 41 buffers 41; 40 is still missing, so nothing drains. Receiving 43 buffers 43; 40 remains the blocker, with 41–44 available. At the bound, valid policies include: skip missing 40 and emit buffered records marked with a permanent gap, improving liveness but accepting incomplete history; quarantine the buffered future records and fail/alert the key, protecting ordered output but withholding valid data; request or rebuild missing history from an authoritative source, improving correctness at recovery cost; or emit a provisional snapshot and later retract or correct it. None may wait unboundedly without violating the declared liveness/state limit.

### Answer 4

The corrected aggregate is $100-12+17=105$. An immutable changelog can record `retract(x, -12, correction=x2)` and `add(x2, +17, supersedes=x)` with stable effect IDs and one correction transaction/version; replayed IDs do not apply twice. An upsert stores `(aggregate-key, revision r+1, total 105, source-cut, correction x2)` and rejects older/equal conflicting revisions. Appending `105` to an additive sink that already holds 100 yields 205, not 105; the additive representation needs only net `+5` (or explicit `-12,+17`).

### Answer 5

Define identity/fingerprint versions, canonical fields and tenant/generation namespaces; signed correction/conflict authority; entity version/tombstone/gap rules; 67-day horizon/expiry clock; too-late repair lifecycle; and revisioned sink keys first. Capture exact source positions plus old receipts/current state/watermarks and retain raw history. Run a new isolated state/output generation over the same cut, computing both old and new primary dispositions without letting either trigger shared effects. Backfill at least the new horizon with fresh progress; compare per-record decisions, legitimate equal-payload occurrences recovered, conflicts exposed, current entity states, gaps, late repairs, aggregate totals, and every disposition count. Size receipts, fingerprints, history, gaps, quarantine, checkpoints, and replay; minimize/hash sensitive fields with versioned keys and erasure rules. Upgrade consumers from additive/arrival semantics to revisioned upserts and visible repair/finality. Cut over by fenced generation at a named offset after domain approval; retain old state/output/source and reverse routing for rollback. Reconcile source identities to receipts, latest state, repairs, conflicts, and outputs until residue is zero or explicitly adjudicated.
