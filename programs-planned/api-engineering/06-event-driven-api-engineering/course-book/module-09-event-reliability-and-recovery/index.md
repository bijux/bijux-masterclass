# Module 09 — Event Reliability, Backpressure, Dead Letters, and Recovery

> **Program stage:** Course 6 of 10 — Extend the promise across asynchronous time.

> **Central question:** How do lag, backpressure, retry, poison messages, dead-letter custody, broker failure, and replay storms affect recovery?

## Where this module fits

Module 08 produced **Add producer policy, tenant-scoped subscriptions/replay, exact-byte signatures, freshness, classification, and privacy rules**. This module extends that result by asking: **How do lag, backpressure, retry, poison messages, dead-letter custody, broker failure, and replay storms affect recovery?**

The new capstone increment is **Implement failure classification, bounded retry, dead-letter records, lag health, replay controls, and operational runbooks**. It becomes the prerequisite for **Event Platform Governance, Release, and Final Defense**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Classify broker, relay, consumer, dependency, schema, security, and capacity failures.
- Apply retry only to transient failures under one budget.
- Bound producer and consumer pressure with admission and backpressure.
- Diagnose lag using count, age, partition distribution, and drain rate.
- Design dead-letter records and repair workflows as controlled operational state.
- Recover from consumer crashes and broker interruption without corrupting effects.
- Prevent replay storms from overwhelming live traffic.
- Reconcile broker progress, inboxes, projections, outboxes, and source truth after incidents.

## Capstone increment

Implement failure classification, bounded retry, dead-letter records, lag health, replay controls, and operational runbooks.

## Core event model

### 1. Queues move latency and failure; they do not erase them

A producer can commit quickly while consumers work later, but the business outcome now includes queue
delay and completion lag. If arrival rate exceeds service rate, backlog grows. The user may receive an
accepted response while the promised downstream effect misses its objective.

SLOs therefore include publication delay, oldest eligible message age, consumer effect completion, and
dead-letter rate for critical journeys. Broker availability alone does not prove the event API is
healthy.

Asynchrony is successful when delay is deliberate and bounded, not when it hides work from request
metrics.

### 2. Failure classification drives retry

Transient failures include a short database outage, broker disconnect, or rate-limited dependency with a
safe retry time. Permanent failures include schema invalidity, unauthorized producer, unsupported event
version, or deterministic business conflict. Capacity failures may require slower admission rather than
per-message retry.

Retrying permanent failures consumes partitions and delays valid records. Dead-lettering transient
failures too early discards recoverable work. Classification uses stable reason codes and can be revised
by an operator under a runbook.

Retry attempts share a budget across handler and dependencies. Nested retry loops can multiply traffic.

### 3. Backpressure must reach the admission boundary

When consumers slow, the system can reduce producer rate, reject noncritical commands, shed optional
event types, increase capacity within policy, or allow bounded backlog. Merely increasing broker
retention postpones saturation.

A producer that cannot publish because its outbox exceeds storage budget must expose degraded readiness
or reject additional work truthfully. Continuing to accept unlimited commands creates obligations the
system cannot fulfill.

Priority is explicit: terminal lifecycle and security events may outrank high-frequency progress events.
Lower-priority streams can be sampled or dropped only when their contract permits it.

### 4. Lag health combines several dimensions

Count indicates volume; oldest age indicates timeliness; partition distribution exposes hot keys or
stuck partitions; arrival and service rates determine whether backlog will grow; retry/dead-letter rates
reveal failure quality. One average can hide a single partition blocking an important tenant.

Drain time is approximately backlog divided by net service rate when service exceeds arrival. If arrival
equals or exceeds service, adding time cannot recover the system. Capacity or admission must change.

Alert thresholds are tied to consumer-effect objectives and runbooks, not arbitrary round numbers.

### 5. Dead letters preserve a failed delivery for decision

A dead letter records original event identity, consumer/effect, channel/partition/offset, attempts,
failure code, safe detail, schema/profile versions, body digest, tenant scope, and timestamps. Sensitive
payload access is restricted and may be stored separately or encrypted.

Operators decide among repair-and-replay, consumer fix and bulk replay, source correction, intentional
skip, or incident escalation. Every action has a stable repair/replay ID and audit trail.

Automatically replaying a dead-letter channel into the same broken consumer creates an infinite loop.

### 6. Consumer recovery preserves ownership and fencing

A crashed consumer loses in-flight deliveries; acknowledgement expiry makes them eligible. Group
rebalancing assigns partitions to healthy instances. A stale instance must not commit or acknowledge
after ownership moves if the handler uses leases or external state.

Inbox uniqueness protects duplicate effects, but long-running external work may need fencing tokens or
provider idempotency. Shutdown should stop polling, finish or safely abandon in-flight work, persist
checkpoints, and release resources.

Recovery tests kill the process at named points rather than merely stopping it cleanly.

### 7. Broker outage and outbox growth need capacity policy

During broker outage, producer transactions continue writing outbox rows until a budget is reached.
Measure row count, oldest age, bytes, database impact, and estimated drain time. A bounded buffer allows
short outages; beyond it, admission degrades or rejects commands whose events cannot be delayed safely.

On recovery, relays should not flood the broker or downstream consumers. Use controlled concurrency and
rate limits, preserving priority. The system may need to process live and backlog traffic with fairness.

A successful reconnect is not recovery; backlog and downstream effects must return within objective.

### 8. Replay is production traffic

Replay consumes broker bandwidth, consumer capacity, databases, caches, and downstream limits. It can
compete with live events and create an incident even when side effects are disabled.

Replay plans declare rate/concurrency budgets, priority, tenant/range, maximum records, pause/abort
thresholds, and live-traffic protection. Large replays run canaries and checkpoints.

Course 5’s workload and capacity methods apply directly: offered replay rate, admitted rate, completed
effects, failures, lag impact, and resource saturation are measured.

### 9. Reconciliation proves recovery

After an incident, “lag is zero” is not sufficient. Offsets may have been skipped, dead letters ignored,
or projections corrupted. Reconciliation compares source facts, outbox rows, broker records/positions,
inbox rows, projection state, and external delivery records.

Discrepancies are classified as missing publication, duplicate publication, unapplied event, duplicate
effect, orphaned effect, or unknown. Repair uses stable IDs and dry-run evidence before mutation.

Recovery completes when critical journey outcomes and durable invariants are restored, not when the
dashboard returns to green.

## Engineering requirements

| Rule | Required behavior | Failure if omitted | Decisive evidence |
|---|---|---|---|
| Failure classification | Every retry/dead-letter decision uses a stable transient/permanent/capacity/security class. | Permanent poison retries forever or transient work is discarded. | Failure vectors and dead-letter codes |
| Bounded retry | Attempts, delay, total age, and dependency budgets are finite. | Retry storms consume partitions and dependencies. | Consumer policy and attempt trace |
| Backpressure admission | Backlog/storage thresholds influence new work acceptance. | The system accumulates unfulfillable obligations. | Outbox/lag budgets and API degradation |
| Lag multidimensional | Count, age, partition, rates, and drain time are evaluated. | Averages hide stuck work or nonrecovering backlog. | Lag report |
| Dead-letter ownership | Every dead letter has owner, repair action, retention, and replay guard. | Failures become an unmanaged second queue. | Runbook and repair evidence |
| Safe recovery | Crash, rebalance, and stale ownership preserve one effect. | Recovered consumers duplicate or corrupt work. | Kill-point tests and inbox/fencing |
| Replay isolation | Historical traffic has admission, priority, and abort thresholds. | Replay harms live SLOs. | Replay workload report |
| Durable reconciliation | Recovery is checked against source and effect stores. | Zero lag is mistaken for correctness. | Reconciliation report |

## Worked failures

### Case 1 — retry storm after database outage

Ten consumers each retry immediately while database connections are saturated. Add bounded backoff,
shared concurrency limits, and one retry budget. If the dependency remains unavailable, allow lag to grow
within policy rather than multiplying calls.

### Case 2 — dead-letter auto-loop

A dead-letter consumer republishes every record to the original channel without checking schema version
or repair approval. The same poison record cycles forever. Require an explicit repair/replay plan with a
changed condition and stable replay ID.

### Case 3 — broker recovery flooded consumers

Relays publish an hour of outbox backlog at maximum speed. Live completion notifications miss SLOs and
the database saturates. Apply paced backlog drain, priority/fairness, and measured net recovery capacity.

### Case 4 — zero lag hid missing effects

An operator manually advanced the group offset past a poison event. Lag becomes zero but analytics lacks
one completion. Reconcile event IDs against inbox/projection and create an audited repair; offset state
alone is not the truth oracle.

## Python implementation

`ConsumerRunner` performs one bounded attempt, classifies success/retry/dead-letter, and stores safe
dead-letter evidence. `classify_lag()` evaluates count and oldest age.

```text
capstone/tracks/python-fastapi/src/event_engineering/reliability.py
capstone/operations/
capstone/tracks/python-fastapi/tests_event/test_reliability_catalog_release.py
```

The retry-delay function is injected so tests are deterministic. Production adapters may use jitter, but
shared vectors test boundaries rather than wall-clock sleep.

Extend the runner with typed failure classes instead of retrying every exception. The catch-all path must
default to safe bounded behavior and preserve evidence.

## TypeScript implementation

TypeScript uses the same attempt and dead-letter state while preserving integer offsets and safe error
detail.

```text
capstone/tracks/typescript-fastify/src/event-engineering/reliability.ts
capstone/tracks/typescript-fastify/test-event-core/security-reliability.test.mjs
```

Never use an unhandled rejected promise as retry policy. Await the handler, classify the failure, settle the
delivery exactly once, and expose a structured outcome. Shutdown waits for the owned attempt or lets the
acknowledgement expire under documented behavior.

## Cross-language invariant

Both tracks must classify the same fixture failures, schedule the same semantic retry attempts, create
equivalent dead-letter records, and report the same lag health. Randomized jitter values may differ in live
adapters; the bounded ranges and attempt decisions must agree.

## Design review

Review each channel/consumer pair with a failure worksheet: objective, arrival rate, service rate, backlog
budget, retention, retry classes, maximum attempts/age, dead-letter owner, replay capacity, and reconciliation
oracle. Then run fault injection at receive, effect commit, acknowledgement, broker disconnect, and recovery.

A runbook that says “restart the consumer” without checking effect state and lag drain is not sufficient.

## End-to-end worked example

The broker becomes unavailable for 15 minutes. Completion transactions continue creating outbox rows until
the declared byte/age budget approaches warning. Low-priority progress production is shed; new expensive run
submissions are throttled before the database buffer is exhausted.

When the broker recovers, relays publish terminal facts at a paced rate. Notification and analytics groups
process live and backlog traffic under fairness. One malformed event reaches maximum attempts and a dead
letter; it no longer blocks the partition. Operators repair its schema mapping and launch a bounded replay.

Recovery is complete only after outbox age, broker lag, inbox/event reconciliation, projection totals, and
notification intent counts satisfy their oracles.

## Failure patterns

- **Queue as hiding place.** Accepted work accumulates with no delay or capacity objective.
- **Retry-all.** Schema, authorization, and deterministic conflicts consume transient retry budgets.
- **Infinite backoff loop.** No maximum attempts or total age leads to permanent lag.
- **Dead-letter landfill.** Records have no owner, repair path, or retention.
- **Count-only alert.** One old stuck partition is hidden.
- **Reconnect equals recovery.** Backlog and effects remain unhealthy after transport returns.
- **Unbounded replay.** Historical traffic starves live consumers.
- **Offset-only proof.** Zero lag is accepted despite missing or duplicated effects.

## Module synthesis

You are ready to leave this module when you can **classify broker, relay, consumer, dependency, schema, security, and capacity failures, apply retry only to transient failures under one budget, and bound producer and consumer pressure with admission and backpressure** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Plant a retry-all defect and show dependency calls exceed the budget** and requiring the following oracle: **The system does not exceed declared outbox, retry, or replay budgets; permanent failure does not retry forever; critical live events retain priority; backlog drain is measurable; dead letter has an owner and repair record; reconciliation proves one effect per event/effect identity. The retry-all mutant fails.**

The cumulative platform now includes **Implement failure classification, bounded retry, dead-letter records, lag health, replay controls, and operational runbooks**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Event Platform Governance, Release, and Final Defense](../module-10-governance-release-and-final-defense/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
