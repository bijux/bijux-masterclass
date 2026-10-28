---
module_id: DARCH-047
program: Data Architecture Engineering
level: 1
module_number: 47
title: Streaming Analytics Architecture
status: complete
last_verified: 2026-09-03
---

# Streaming Analytics Architecture

## One-Page Review

### Governing question

How should architects publish continuously changing analytical products from unbounded data while making event time, completeness, revisions, state, failure, protection, and consumer effects explicit rather than equating low transport latency with correct real-time insight?

### Essential definitions

- A **streaming analytical product** continuously derives and publishes observations, aggregates, detections, features, or decisions from unbounded inputs under a governed time and revision contract.
- **event time** is when a source-domain occurrence happened; **processing time** is when a computation observed or processed it.
- A **window** groups unbounded observations into finite analytical scopes by time, count, session, or another declared boundary.
- A **watermark** is a system's estimate or assertion about event-time progress; it does not prove that no earlier event can arrive.
- A **trigger** decides when to emit a result for a window independently of the window's logical membership.
- An **accumulation mode** states whether later outputs replace, append to, retract, or revise earlier outputs.
- A **revision** is a versioned correction or refinement of an already published analytical result.
- **stream state** is retained information needed across records, such as windows, joins, deduplication sets, models, timers, or partial aggregates.
- A **checkpoint** records restorable processing state and source progress under a declared consistency boundary.
- **end-to-end effect semantics** describe observable sink or decision outcomes across source delivery, processing, retries, and external side effects.
- **backpressure** propagates capacity pressure upstream or constrains admission so queued work does not grow without bound.
- A **replay contract** defines which inputs, code, configuration, reference data, clocks, randomness, policies, and outputs are required to reconstruct state.

### Central model, mechanism, or theorem

Represent a streaming analytical product as:

`S = (outcomes, inputs, identities, time, windows, state, delivery, publication, revisions, serving, protection, service, ownership, evidence, lifecycle)`

For each published result, bind input positions, event-time boundary, watermark, trigger, state and code version, reference-data versions, revision number, quality, and policy. Low latency is meaningful only for a named source event and consumer observation. A watermark enables bounded progress but late events remain possible; the architecture must decide whether to revise, compensate, quarantine, ignore, or escalate. Exactly-once processing claims do not automatically cover emails, payments, APIs, caches, or human decisions.

### Critical invariants

- Every input has stable identity, source authority, partition and order scope, event-time semantics, schema, retention, and correction behavior.
- Event, ingestion, processing, publication, serving, and decision time remain distinct.
- Window membership, triggering, accumulation, lateness, finality, and revision are explicit consumer contracts.
- Watermarks and idle detection never masquerade as proof of source completeness.
- Checkpoints bind compatible source positions, operator state, code and configuration, and sink publication evidence.
- Duplicate, gap, reordering, late, corrected, retracted, and deleted inputs have defined state and output effects.
- Stateful recovery and replay reproduce or explain outputs under pinned dependencies, or limitations are declared.
- Backpressure, retry, skew, hot keys, replay, and downstream outages cannot grow state or source load without bounds.
- Protection follows events, metadata, state, checkpoints, dead letters, materialized views, alerts, exports, and models.
- Retirement drains or transfers consumers, state, offsets, histories, alerts, credentials, and retained inputs under verified closure.

### Common failures

Common failures are calling an event bus streaming analytics; using processing time for business windows; treating a watermark as completeness; using one global watermark while a partition is idle or lost; hiding late-event policy; emitting revisions to append-only consumers; promising exactly once without naming the observer; deduplicating by payload; joining unbounded streams without time bounds; retaining state forever; checkpointing state without sink effects; replaying with current reference data; changing code without output versioning; sending alerts before durable state; letting one hot key exhaust workers; retrying a failing sink indefinitely; counting broker lag as consumer freshness; storing protected payloads in dead letters; using streaming for workloads that tolerate batches; combining batch and stream outputs without precedence; and decommissioning jobs while offsets, topics, alerts, or consumers remain.

### Compact example

A ten-minute fraud-rate window emits value 10 when its watermark crosses the window end. A valid late event adds 3 before the allowed-lateness horizon, so the product publishes revision 2 with value 13 and consumers upsert by window ID and revision. A later event valued 5 arrives after finality and enters a governed exception path rather than silently changing or disappearing. The result contract exposes event-time range, watermark, completeness status, revision, input positions, and correction policy.

### Connections

[DARCH-017](017-event-schemas-and-information-models.md), [DARCH-035](035-event-driven-data-integration.md), [DARCH-040](040-choosing-an-integration-style-from-semantics-and-latency.md), and [DARCH-046](046-operational-data-stores.md) establish event, integration, and serving boundaries. Data Engineering [DENG-051](../../19-data-engineering/modules/051-streams-logs-and-unbounded-data.md) through [DENG-060](../../19-data-engineering/modules/060-handling-late-duplicate-and-out-of-order-events.md) own stream-processing implementation. This module defines architecture and prepares [DARCH-048](../ROADMAP.md) on feature and training data architecture.

## Governing Question

Streaming analytics is often justified by the phrase “real time.” That phrase hides whether the consumer needs seconds, minutes, provisional evidence, a current state, an anomaly notification, or an irreversible action. It also hides event-time disorder, replay, state, corrections, and downstream effects.

The governing question is not whether data can flow continuously. It is which continuously updated analytical contract makes a decision better, what error and revision behavior the consumer can tolerate, and which system evidence proves that contract under ordinary and exceptional conditions.

## Why This Matters

Apache Flink's [Time and Watermarks](https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/time/) documentation distinguishes event and processing time and explains watermarks. Apache Beam's [Programming Guide](https://beam.apache.org/documentation/programming-guide/#watermarks-and-late-data) describes watermarks, late data, windows, triggers, and accumulation behavior. Apache Kafka's [Delivery Semantics](https://kafka.apache.org/documentation/#semantics) documentation qualifies producer and consumer delivery guarantees. Product guarantees must remain narrower than the mechanisms they compose.

Google's [MillWheel paper](https://research.google/pubs/millwheel-fault-tolerant-stream-processing-at-internet-scale/) describes fault-tolerant stateful stream processing, and Akidau and colleagues' [Dataflow Model paper](https://www.vldb.org/pvldb/vol8/p1792-Akidau.pdf) develops event-time windows, watermarks, triggers, and refinements. These are research mechanisms and models, not proof that every consumer needs continuous computation.

[CloudEvents 1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md) standardizes common event context. Google's [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) explains overload and retry amplification. NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) frames trustworthy lifecycle engineering. Streaming architectures must unite event meaning, computation, operation, and governance.

## Prerequisites and Retrieval

You should understand events, logs, partitions, offsets, delivery, idempotency, event and processing time, windows, watermarks, triggers, state, checkpoints, consistency, materialized views, APIs, quality, protection, and recovery.

Retrieve unbounded data, event time, ingestion time, processing time, watermark, window, trigger, accumulation, allowed lateness, finality, revision, retraction, state, timer, checkpoint, savepoint, offset, replay, backpressure, hot key, end-to-end effect, and dead letter.

As a retrieval test, inspect “show live revenue.” Ask which revenue event, authority, grain, currency, event time, window, watermark, late and correction policy, publication latency, provisional status, dimensions, source positions, consumer effects, and owner apply. “Live” alone is not a selectable requirement.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish event transport, stream processing, streaming analytics, operational action, and continuously served state;
2. define event identities, authority, schemas, ordering, time, and correction contracts;
3. design windows, watermarks, triggers, allowed lateness, accumulation, finality, and revisions;
4. scope delivery, processing, state, checkpoint, sink, and end-to-end effect guarantees;
5. design bounded joins, deduplication, state retention, replay, backfill, and batch reconciliation;
6. publish streams, changelogs, tables, APIs, alerts, and dashboards with consumer-compatible semantics;
7. handle capacity, backpressure, skew, retries, downstream outage, regional failure, and recovery;
8. propagate purpose, minimization, authorization, derived sensitivity, retention, deletion, and audit;
9. assign producer, streaming product, platform, consumer, operations, protection, and incident responsibilities;
10. compare streaming, batch, and hybrid architectures and plan migration, review, and verified retirement.

## Core Exposition

**Start with the consumer outcome.** Name the decision, action, observation, actor, useful deadline, consequence of stale or revised data, frequency, and fallback.

Streaming is justified when earlier partial or current evidence changes an outcome enough to fund continuous operation and correction.

**Distinguish transport from analytics.** A broker carries ordered records within declared scopes. A processor derives state. A serving layer exposes results. A consumer makes a decision.

Low broker latency does not prove low decision latency or analytical correctness. Measure every boundary.

**Distinguish analytical notification from command.** An alert reports derived evidence; a command asks an accountable service to act.

Fraud analytics can recommend review or block, but any irreversible action needs explicit authority, thresholds, idempotency, appeal, and failure behavior.

**Define the input fact.** Record event identity, type, authority, key, grain, schema, units, event time, publication time, source position, correction, deletion, and limitations.

Transport envelopes help routing. They do not guarantee domain semantics or completeness.

**Separate time concepts.** Event time describes source occurrence; ingestion time describes platform receipt; processing time describes computation; publication and decision time describe consumer experience.

Choose each purpose deliberately. Processing-time windows answer system-observation questions, not necessarily business questions.

**Validate event time.** Check timezone, precision, clock source, plausible bounds, future events, defaults, missing values, and relationship to source order.

Do not replace invalid event time silently with processing time. Quarantine, use an explicitly named fallback, or publish limitations.

**Define ordering scope.** Topics and partitions may order records per key or partition, not globally.

Use stable keys for state that requires order. Sequence numbers and domain versions can detect gaps or stale updates more reliably than wall clocks.

**Define windows from questions.** Tumbling windows partition time; sliding windows overlap; session windows depend on activity gaps; global windows rely on triggers and state.

Specify interval boundaries, timezone, key, membership, merge behavior, and empty windows. Familiar labels such as “daily” remain ambiguous.

**Separate windows from triggers.** A window says which events belong together. A trigger says when to emit.

Early triggers reduce latency but publish provisional results. Event-time triggers use watermarks. Processing-time triggers depend on system observation. Late triggers revise.

**Define watermark meaning.** A watermark usually indicates the system does not expect, or chooses not to wait for, events earlier than a time.

It is a progress mechanism and estimate, not a mathematical completeness proof. Sources, partitions, idle detection, failure, and clock behavior shape it.

**Combine per-partition progress carefully.** The minimum active partition watermark protects completeness but one idle partition can stall progress.

Idle detection improves liveness and can hide a broken or delayed partition. Require heartbeats, source health, expected population, and resumption rules.

**Define allowed lateness.** State how long after a window or watermark an event may revise output, measured by which clock and failure context.

Allowed lateness is an economic and consumer decision. It also controls state retention and correction burden.

**Define finality honestly.** A result can be operationally final after a deadline while later source corrections remain possible.

Use statuses such as provisional, revised, operationally closed, and superseded with version evidence. Avoid claiming immutable truth.

**Choose accumulation behavior.** Discarding panes emit only new contributions; accumulating panes emit full current values; retractions negate earlier outputs; upserts replace by stable result key and revision.

Consumers must understand the chosen mode. An append-only sink cannot safely consume replacement semantics without adaptation.

**Give results stable identity.** Use product, key, window, metric or detection, model or rule version, and revision identity.

Stable identity lets consumers upsert, retract, correct, deduplicate, audit, and communicate affected outcomes.

**Publish revision contracts.** State what can change, why, for how long, how consumers learn, whether earlier values remain visible, and which effects require compensation.

Dashboards can redraw easily; sent alerts, human actions, or external API calls need different correction plans.

**Bound state.** Every aggregation, join, deduplication set, timer, model, and pattern retains state under a key and time horizon.

Define expiry from lateness, replay, correction, and consumer needs. Unbounded keys or time create unbounded storage and recovery.

**Design stream joins.** Declare key, cardinality, time relationship, interval, event-time behavior, unmatched records, late matches, duplicates, and state expiry.

Joining two unbounded streams without bounds can retain state forever. Joining a stream with a table needs table version and time semantics.

**Version reference data.** A replay should use the same pricing, identity, hierarchy, model, policy, or exchange-rate version when reproducibility is required.

Using today's table rewrites historical meaning. Preserve snapshots or explicitly publish restated results.

**Deduplicate by event identity and scope.** Record producer, epoch, partition or entity, event ID, and retention horizon.

Payload equality can collapse distinct legitimate events. Expiring deduplication state reopens duplicate risk and must match replay horizons.

**Define gap behavior.** Sequence gaps, missing partitions, expired retention, corrupt records, and source silence can make aggregates incomplete.

Pause, mark partial, repair from source, rebuild from snapshot, or publish bounded uncertainty. Do not let a moving watermark hide missing facts.

**Scope delivery claims.** At-most-once, at-least-once, and exactly-once terms apply at a named interface and observer.

A broker can avoid redelivery while a sink repeats. A framework can restore state consistently while an email or payment happens twice.

**Design exactly-once effects where needed.** Couple source positions, processing state, result identity, and sink commit through transactions, idempotent upserts, deduplication ledgers, or reconciliation.

External side effects need stable operation IDs and outcome discovery after timeouts. Be explicit when only processing state is exactly once.

**Checkpoint a consistent boundary.** A checkpoint binds operator state, timers, source positions, code or state schema, configuration, and compatible sink state.

Successful checkpoint creation does not prove restorable consumer outcomes. Exercise restore and reconciliation.

**Handle unknown outcomes.** A sink timeout may occur before or after commit. Retry only with idempotent identity or outcome discovery.

Blind retries can double effects; abandoning can lose them. Preserve evidence and escalate irreconcilable ambiguity.

**Design replay as a product operation.** Pin input range, source epochs, code, dependencies, reference data, state bootstrap, output namespace, policy, and comparison.

Replay should not write over live outputs until validated. Use shadow releases, stable revisions, and controlled cutover.

**Separate replay from backfill.** Replay reprocesses retained inputs; backfill may acquire missing historical facts or compute a new product interval.

Both require source load, ordering, identity, correction, capacity, and consumer effect controls.

**Reconcile with batch evidence.** Periodic source snapshots or authoritative aggregates can reveal lost, duplicated, or misinterpreted stream effects.

Compare keys, counts, measures, windows, positions, revisions, and distributions at compatible cutoffs. Batch is a verification path, not an admission of failure.

**Choose the serving form.** Publish append streams for immutable facts, changelogs for evolving tables, materialized views for current state, APIs for bounded queries, and dashboards for human interpretation.

Match consumer update behavior, history, latency, authorization, and recovery. One output cannot serve every observer safely.

**Expose freshness and completeness.** Include event-time coverage, watermark, input positions, last update, provisional or final status, revision, quality, and incident state.

Avoid overloading business payloads with infrastructure secrets. Provide stable metadata appropriate to the interface.

**Define consumer acknowledgements.** Broker offsets show receipt progress, not correct application or decision.

Critical consumers can publish applied positions, revision support, errors, or outcome evidence. Registration enables incident and change management.

**Control alerts.** Deduplicate alert identity, separate detection from notification, rate-limit storms, group related cases, suppress known maintenance, and preserve escalation.

Alert corrections and withdrawals need human-readable context. High sensitivity or consequence may require review before action.

**Design hybrid batch and stream products.** Streaming can publish early results while batch establishes a later reconciled release.

Define shared identity, precedence, replacement, correction, and consumer transition. Do not add streaming and batch totals together.

**Compare lambda-like dual computation.** Independent batch and speed implementations can provide correction but duplicate logic and drift.

Shared contracts, code generation, reconciliation, and bounded responsibility reduce divergence. Sometimes a single replayable stream path is simpler.

**Compare a unified replay path.** One code path can reduce semantic duplication but may make large backfills slow or operationally risky.

Evaluate retained inputs, state size, deterministic dependencies, compute cost, and isolation. Architectural unity is not automatically operational simplicity.

**Apply backpressure.** Slow sinks and skewed state should reduce intake, buffer within bounds, shed noncritical work, or route to alternate capacity.

Unbounded queues convert latency incidents into storage and recovery incidents. Define maximum lag and stop conditions.

**Handle hot keys.** One customer, campaign, device, or global aggregation can concentrate state and processing.

Use preaggregation, sharding with associative combination, dedicated capacity, sampling, or redesigned questions only when semantics permit.

**Plan capacity for recovery.** Normal utilization must leave room for checkpoint, failover, replay, backlog catch-up, late bursts, schema changes, and downstream outage.

Average input rate is insufficient. Model peaks, skew, state, network, storage, control-plane, and sink limits.

**Protect downstream systems.** Rate-limit writes, batch effects, use circuit breakers, bounded retries, dead-letter policy, and admission control.

A recovering database or API can collapse under replay. Consumer protection belongs in stream architecture.

**Treat dead letters as governed data.** Store failure reason, source identity, schema, classification, attempts, owner, retention, and resolution.

Dead letters can contain malformed secrets or personal data. Restrict access and prevent permanent accumulation.

**Apply purpose and minimization.** Stream only fields and histories justified for the analytical outcome.

Low latency can distribute sensitive errors rapidly. Protection review covers payload, keys, headers, state, checkpoints, and derived results.

**Propagate row and field policy.** Authorization must hold in topics, processors, state stores, sinks, APIs, caches, dashboards, and replay environments.

Partitioning by tenant helps isolation only when every path enforces it. Shared operator state can still mix principals.

**Trace derived sensitivity.** Correlations, anomalies, locations, behavior patterns, scores, and small cohorts can reveal protected facts.

Classify analytical outputs and alerts, not only source fields. Limit explanations, exports, and notification recipients.

**Propagate deletion and restriction.** Remove or restrict current materializations, retained events where policy permits, state, checkpoints, dead letters, caches, features, alerts, and downstream copies.

Use tombstones and restore-time replay rules to prevent resurrection. Document immutable or held exceptions truthfully.

**Observe the full path.** Measure source publication, partition progress, watermark, queue, processing, state, checkpoint, sink, serving, cache, and decision delay.

Track duplicates, gaps, late rates, revisions, dropped events, state size, skew, restore time, and consumer outcomes.

**Avoid metric self-deception.** A high watermark can advance after idle detection; low average lag can hide one critical partition; successful checkpoints can restore slowly.

Use per-key and per-partition distributions, synthetic good events, source reconciliation, and failure exercises.

**Set service objectives at outcome boundaries.** Define event-to-result freshness, provisional and final completeness, revision delay, availability, recovery, and notification for named workloads.

Measure percentiles and failure states. One latency objective cannot represent both dashboard and fraud actions.

**Design regional behavior.** Define source authority, partition ownership, replication, failover, duplicate producers, clock uncertainty, state movement, and result precedence.

Fence old writers and consumers where necessary. Reconcile before merging regional outputs.

**Exercise recovery.** Test worker loss, checkpoint corruption, source retention expiry, sink outage, schema incompatibility, hot key, region loss, and bad deployment.

Restore into isolation, compare positions and state, validate outputs, and resume with explicit authority. RTO includes backlog catch-up.

**Assign incident authority.** Name who can pause sources, stop publication, mark results provisional, activate fallback, replay, revise, notify, and resume.

Producer, product, platform, consumer, operations, security, and privacy responsibilities need explicit handoffs.

**Evaluate total cost.** Include brokers, storage, state, compute, network, checkpoints, serving, on-call, replay, reconciliation, protection, incidents, migration, and retirement.

Compare with frequent batch, incremental queries, ODS projections, or direct event consumers under the same outcome.

**Migrate with shadow outputs.** Pin inputs, run old and new logic in isolated namespaces, compare windows and revisions, and validate consumer decisions.

Move cohorts with explicit authority, offsets, state bootstrap, rollback, and bounded coexistence. Avoid dual external side effects.

**Retire completely.** Stop producers or routes, drain or transfer consumers, preserve required positions and evidence, revoke identities, remove jobs, state, checkpoints, topics, sinks, alerts, dashboards, caches, and docs.

Apply retention, deletion, and holds. Verify no consumer or automated action remains.

**Measure streaming value.** Track decision improvement, time saved, corrected errors, useful freshness, availability, revision burden, source and sink impact, protection incidents, cost, and retired alternatives.

Event volume and low latency are activity. Value is trustworthy, timely, correctable analytical outcomes.

## Definitions and Notation

Represent streaming architecture as $S=(U,I,T,W,G,P,R,V,Z,Q,O,E,L)$, where $U$ is outcomes, $I$ inputs and identities, $T$ time, $W$ windows and watermarks, $G$ state and processing, $P$ positions and checkpoints, $R$ revisions, $V$ serving, $Z$ protection, $Q$ service, $O$ ownership, $E$ evidence, and $L$ lifecycle.

For event-time window $w=[a,b)$ and revision $j$, let $V_{w,j}$ be its published value. A later admissible event can produce $V_{w,j+1}$ according to accumulation policy. Operational finality after deadline $f_w$ is a contract decision, not proof that no source correction exists.

Let end-to-end freshness for event $e$ be $F_e=t_{consumer\ observation}-t_{event}$ under compatible time meaning and clocks. Broker, processing, and serving delays are components; measuring one does not establish $F_e$.

Define `FitStream(S,u,t)` as a review predicate requiring justified outcome, authoritative inputs, valid time and windows, bounded state and lateness, scoped delivery and effect semantics, revision-compatible consumers, effective protection, capacity and recovery evidence, ownership, alternatives, and lifecycle at time $t$.

## Mechanisms, Invariants, or Proof Structure

Use ten gates for every consequential streaming analytical product.

**1. Outcome gate.** Name decision, actor, consequence, useful deadline, provisional tolerance, correction, value, owner, and alternatives.

**2. Input gate.** Define authority, identity, key, grain, schema, time, order, positions, duplicates, gaps, corrections, deletes, and retention.

**3. Time gate.** Define event and processing time, windows, watermarks, idle detection, triggers, lateness, accumulation, finality, and revisions.

**4. State gate.** Define keys, joins, deduplication, timers, reference versions, bounds, expiry, checkpoints, schemas, and restore.

**5. Effect gate.** Scope source delivery, processing, state, sink, serving, external side effects, idempotency, unknown outcomes, and reconciliation.

**6. Serving gate.** Define streams, changelogs, tables, APIs, dashboards, alerts, result identity, metadata, consumers, and update behavior.

**7. Protection gate.** Apply purpose, minimization, identity, derived sensitivity, state, dead letters, regions, retention, deletion, egress, and audit.

**8. Operations gate.** Test capacity, skew, backpressure, retry, sink protection, checkpoints, lag, observability, incidents, support, and cost.

**9. Recovery gate.** Exercise replay, backfill, source and sink loss, corrupt state, expired retention, regional failure, reconciliation, and resumption.

**10. Lifecycle gate.** Record evidence, hybrid precedence, migration, shadow outputs, coexistence, rollback, review triggers, and verified retirement.

The executable example models early publication, an admissible late revision, and a too-late exception.

<!-- bijux-verify: {"id":"streaming-window-revision-contract","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"window=0-10\ninitial_value=10\nlate_event_value=3\nrevised_value=13\nrevision_number=2\ntoo_late_event_value=5\nfinal_value=13\nconsumer_action=upsert_revision_2\n","stderr":""}} -->
```python
window = (0, 10)
on_time_events = [
    {"event_time": 2, "value": 4},
    {"event_time": 7, "value": 6},
]
late_event = {"event_time": 8, "value": 3, "arrival_time": 12}
too_late_event = {"event_time": 9, "value": 5, "arrival_time": 16}
allowed_lateness_deadline = 15

initial_value = sum(event["value"] for event in on_time_events)
revision = 1
current_value = initial_value

if late_event["arrival_time"] <= allowed_lateness_deadline:
    current_value += late_event["value"]
    revision += 1

if too_late_event["arrival_time"] <= allowed_lateness_deadline:
    current_value += too_late_event["value"]
    revision += 1

print(f"window={window[0]}-{window[1]}")
print(f"initial_value={initial_value}")
print(f"late_event_value={late_event['value']}")
print(f"revised_value={current_value}")
print(f"revision_number={revision}")
print(f"too_late_event_value={too_late_event['value']}")
print(f"final_value={current_value}")
print(f"consumer_action=upsert_revision_{revision}")
```

The result proves only the declared arithmetic and deadline logic for three in-memory events. It is not proof of watermark completeness, a stream processor, distributed state, delivery semantics, correct event time, durable publication, source correction, consumer effects, or an appropriate lateness policy.

## Alternatives and Trade-Offs

**Streaming versus frequent batch.** Streaming lowers observation delay and supports continuous state while adding state, disorder, revision, and on-call complexity. Batch can provide coherent releases efficiently when delay is acceptable.

**Event time versus processing time.** Event time preserves source chronology under disorder. Processing time simplifies low-latency system monitoring. Match the question.

**Early provisional versus later complete output.** Early results aid action but create revision burden. Waiting improves completeness while delaying value. Consumers determine the balance.

**Append versus upsert or retract output.** Append is simple for immutable facts. Evolving results need stable keys and revision semantics or compensating records.

**Long lateness versus bounded state.** Longer horizons capture delayed data but increase state, cost, and revision exposure. Later corrections can move to batch restatement.

**One unified path versus separate speed and batch paths.** Unity reduces duplicate logic; separate paths can optimize latency and authoritative correction. Reconciliation and precedence are required either way.

**Stream-table join versus stream-stream join.** Table joins use a selected reference state; stream joins can preserve temporal relationships but need bounds and unmatched policy.

**Managed service versus portable framework.** Managed operation can reduce toil; portable contracts reduce exit risk. State, connectors, semantics, and recovery still need tests.

**Exactly-once machinery versus idempotent effects.** Transactions can simplify bounded sinks. Stable identities and reconciliation often cover heterogeneous external effects more honestly.

**Central platform versus domain stream products.** Shared infrastructure reuses controls; domains retain fact meaning. Combine platform operation with producer and product accountability.

## Failure Modes and Misconceptions

1. **A broker creates streaming analytics.** Transport does not define state, time, products, or decisions.
2. **Real time means zero latency.** Boundaries, percentiles, usefulness, and failure matter.
3. **Processing time is close enough to event time.** Disorder and outage can change business windows.
4. **A watermark proves completeness.** It is an estimate or progress assertion under assumptions.
5. **Late events are errors.** They may be valid facts requiring revision.
6. **Final results never change.** Source corrections can supersede operational finality.
7. **Exactly once covers all side effects.** Guarantees stop at named observers.
8. **Payload equality deduplicates safely.** Distinct facts can share payloads.
9. **Unbounded joins are just large joins.** They create unbounded state without time or other bounds.
10. **A checkpoint proves recovery.** Restore speed and sink reconciliation remain.
11. **Replay with current reference data is reproduction.** It may restate history.
12. **Append-only consumers can accept revisions.** Replacement needs explicit adaptation.
13. **Low average lag means healthy service.** Critical partitions and keys can be far behind.
14. **Dead letters are harmless diagnostics.** They retain sensitive and unresolved data.
15. **Streaming always beats batch.** Complexity may exceed the value of lower latency.
16. **More retries improve delivery.** They can amplify sink and control-plane failure.
17. **Stopping the job retires the product.** Inputs, state, outputs, consumers, and effects remain.

## Worked Examples

### Example 1

A dashboard needs five-minute provisional orders and a reconciled daily close. Streaming publishes versioned early windows; batch replaces them under declared precedence. **Conclusion:** one decision landscape can justify two publication modes.

### Example 2

A device event occurs at 09:58 but arrives at 10:07 after network recovery. Event-time windows revise 09:50–10:00; processing-time windows would classify it after 10:00. **Conclusion:** time choice changes meaning.

### Example 3

One partition becomes idle and the global watermark advances after timeout. Source heartbeats later show the partition was disconnected, so outputs remain marked incomplete. **Conclusion:** idle detection improves progress, not source proof.

### Example 4

A valid late event changes a window from 10 to 13 and emits revision 2. An append-only notification consumer is excluded; a table consumer upserts by window and revision. **Conclusion:** consumer capability constrains accumulation.

### Example 5

A stream joins orders with current customer tier during replay and changes last month's segmentation. Pinning tier snapshots restores reproducibility; a separate restatement uses current tiers. **Conclusion:** reference time belongs in replay contracts.

### Example 6

A processor restores its state exactly once but calls an email API twice after a timeout. Stable notification IDs and outcome lookup prevent a duplicate send. **Conclusion:** processing and external effect guarantees differ.

### Example 7

A celebrity account creates a hot key that stalls its partition. Associative preaggregation shards compatible counts, while non-associative pattern state receives dedicated capacity. **Conclusion:** skew remedies must preserve algebra.

### Example 8

A sink outage causes unbounded retries and checkpoint growth. Admission control, backpressure, bounded buffers, circuit breaking, and a recovery queue prevent collapse. **Conclusion:** downstream failure is an architectural input.

### Example 9

Malformed events containing credentials enter a broadly readable dead-letter topic. Access is restricted, payloads minimized, retention shortened, and a resolution workflow assigned. **Conclusion:** failure paths need equal protection.

### Example 10

After a batch redesign removes the latency need, consumers migrate, offsets and state evidence are archived under policy, jobs and topics stop, alerts and caches are removed, and no automated action remains. **Conclusion:** streaming products can be retired deliberately.

## Cross-Program Connections

- **Data engineering:** logs, partitions, delivery, time, windows, state, checkpoints, late data, replay, and sinks implement streams.
- **Database engineering:** transactions, changelogs, materialized views, indexes, isolation, temporal data, compaction, and recovery shape state.
- **Distributed systems:** clocks, ordering, consensus boundaries, retries, partitions, replication, consistency, and convergence govern behavior.
- **API and service engineering:** event and result contracts, idempotency, webhooks, authentication, quotas, errors, and deprecation serve consumers.
- **Platform engineering:** brokers, processors, schemas, state backends, observability, capacity, tenancy, upgrades, and support enable products.
- **Cybersecurity and privacy:** payloads, keys, metadata, state, dead letters, derived sensitivity, retention, deletion, and alerts constrain design.
- **Economics and decision science:** timeliness value, false positives, revision cost, queueing, capacity, uncertainty, and action consequence guide choices.
- **Systems engineering:** requirements, interfaces, failure analysis, verification, configuration, assurance, recovery exercises, and closure structure trust.

## References

1. Apache Flink Project, *Time and Watermarks*. <https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/time/>
2. Apache Beam Project, *Programming Guide: Watermarks and Late Data*. <https://beam.apache.org/documentation/programming-guide/#watermarks-and-late-data>
3. Apache Kafka Project, *Delivery Semantics*. <https://kafka.apache.org/documentation/#semantics>
4. Akidau, T., et al., *MillWheel: Fault-Tolerant Stream Processing at Internet Scale*, 2013. <https://research.google/pubs/millwheel-fault-tolerant-stream-processing-at-internet-scale/>
5. Akidau, T., et al., *The Dataflow Model*, PVLDB 8(12), 2015. <https://www.vldb.org/pvldb/vol8/p1792-Akidau.pdf>
6. Cloud Native Computing Foundation, *CloudEvents Specification 1.0.2*. <https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md>
7. Beyer, B., Jones, C., Petoff, J., and Murphy, N. R., eds., *Site Reliability Engineering: Addressing Cascading Failures*, Google, 2016. <https://sre.google/sre-book/addressing-cascading-failures/>
8. NIST, *Systems Security Engineering: Considerations for a Multidisciplinary Approach in the Engineering of Trustworthy Secure Systems*, SP 800-160 Volume 1 Revision 1, 2022. <https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final>

## Exercises

### Exercise 1

Design a streaming analytical product for fraud-rate monitoring. Define facts, identity, event time, windows, watermarks, revisions, state, serving, alerts, protection, and lifecycle.

### Exercise 2

Specify end-to-end effect semantics for a stream that reads orders, updates a materialized view, calls a case-management API, and emails an analyst.

### Exercise 3

Design a bounded stream-stream join between orders and payments with late, duplicate, corrected, unmatched, and deleted inputs.

### Exercise 4

Plan recovery from checkpoint corruption and expired broker retention while the sink contains partially applied results and consumers have acted on alerts.

### Exercise 5

Compare streaming, frequent batch, and a hybrid for revenue dashboards, regulatory close, anomaly detection, and customer notifications.

## Answers to the Exercises

### Answer 1

Define the decision: prioritize fraud investigation, not automatically reject payment unless separately authorized. PaymentAccepted and FraudSignal facts have stable IDs, account or instrument keys, schemas, event and publication time, source partitions and positions, corrections, and protected classification. Use event-time tumbling and sliding windows aligned to the business question, per-key and global progress, heartbeats, watermark assumptions, allowed lateness, early triggers, upsert revisions, operational finality, and later source-correction policy.

State includes deduplication, partial aggregates, model version, timers, and alert suppression with bounded horizons. Checkpoints bind source offsets, state and sink versions. Serve a versioned table and API with event-time coverage, watermark, revision, quality, and provisional status. Alerts use stable identities, thresholds, grouping, rate limits, authorized recipients, withdrawal, and human review. Protect payload, state, checkpoints, dead letters, model outputs, and explanations. Test skew, gaps, late bursts, sink outage, replay, and region loss; assign producer, product, platform, fraud, operations, and protection owners; define batch reconciliation, model and rule review, and retirement.

### Answer 2

Name observers separately. Source receipt may be at least once. Processing state and the materialized view can share a transactional or idempotent checkpoint-to-sink boundary keyed by order and revision. The processor records source position, state checkpoint, output version, and stable operation IDs. After timeout it discovers whether the view update committed before retrying.

Case creation uses an idempotency key derived from product, order, rule version, and detection revision; the client queries or reconciles unknown outcomes. Email uses a stable notification ID stored in a durable outbox or deduplication ledger and may still offer weaker provider guarantees, which are documented. A revised or retracted detection updates the view, amends or closes the case, and sends a correction only under notification policy. Checkpoint success alone never claims external effects. Reconciliation compares offsets, results, case IDs, notification outcomes, and consumer acknowledgements.

### Answer 3

Define OrderAccepted and PaymentSettled identities, order key, amounts and currency, source order, event time, schemas, corrections, and deletion. Join within a justified interval, such as settlement from 30 minutes before to seven days after acceptance, using event time and stable order identity. Specify one-to-many partial payments, unmatched orders and payments, duplicate IDs, late arrivals, currency conversion version, and disputed or reversed payments.

Retain state through maximum join interval plus allowed lateness and recovery horizon. Watermarks from both sources govern provisional unmatched output, but source completeness and gap checks remain separate. Deduplicate by source event identity, not payload. Publish stable result IDs and revisions for new matches, amount changes, reversals, and final unmatched cases. Too-late valid facts enter reconciliation and restatement. Protect cross-source relationships, bound state and hot keys, checkpoint both inputs consistently, replay with pinned reference data, and compare with periodic authoritative batch populations.

### Answer 4

Stop or isolate publication and mark affected windows provisional. Inventory last trusted checkpoint, source epochs and positions, retained inputs, state schemas, code and reference versions, sink commits, result revisions, downstream consumers, cases or alerts, and protection constraints. Do not restart from an arbitrary offset. If no compatible checkpoint and broker history is incomplete, obtain an authoritative snapshot or batch product plus a declared handoff, then rebuild state in an isolated namespace.

Reconcile existing sink keys, windows, revisions, duplicates, gaps, and external effects. Replay available inputs idempotently with source and sink load limits. Produce a correction set for missing or conflicting history; notify consumers and compensate alerts or cases according to consequence. Validate event-time coverage, positions, aggregates, state, policies, and consumer decisions before cutover. Record irrecoverable uncertainty rather than inventing completeness. Establish a new checkpoint lineage, preserve incident evidence, and change retention, backup, and recovery tests based on the failure.

### Answer 5

Revenue dashboards may use five-minute provisional streaming values with revision support and a daily reconciled batch release. Regulatory close should use a pinned, complete, approved batch or warehouse release; streaming can signal readiness but not replace close evidence without equivalent assurance. Anomaly detection can justify streaming because early observation changes response, with explicit false-positive, late-data, revision, model, and alert contracts. Customer notifications need authoritative domain events and idempotent effect workflows; an analytical anomaly alone should not trigger irreversible messaging without policy.

Compare useful deadline, event-time correctness, completeness, revision tolerance, source retention, state, serving, protection, capacity, recovery, skill, cost, and retirement. Frequent incremental batches may satisfy dashboards at lower complexity. A hybrid needs shared fact identity, semantic rules, source cutoffs, precedence, correction, and consumer transition so streaming provisional values are replaced rather than combined with batch truth.
