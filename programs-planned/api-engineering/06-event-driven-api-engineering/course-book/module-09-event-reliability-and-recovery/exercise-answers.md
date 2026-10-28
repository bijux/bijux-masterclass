# Worked Answers — Module 09: Event Reliability, Backpressure, Dead Letters, and Recovery

Use these solutions to audit your reasoning for **Event Reliability, Backpressure, Dead Letters, and Recovery**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Classify failures

Schema invalidity, authorization rejection, and unsupported version are permanent/security contract failures for the current record. Database timeout and broker outage are transient under bounded retry. A hot partition is a capacity/design failure requiring admission, scaling, or repartitioning—not repeated handler retries.

The chapter’s decisive distinction is this: Transient failures include a short database outage, broker disconnect, or rate-limited dependency with a safe retry time. Permanent failures include schema invalidity, unauthorized producer, unsupported event version, or deterministic business conflict. Capacity failures may require slower admission rather than per-message retry.

## 2. Build a retry budget

For example: maximum 4 attempts over 60 seconds, exponential delays 1/3/9 seconds plus bounded jitter, per-consumer database concurrency 8, one total dependency deadline per attempt, and dead-letter/escalation after total age. Exact numbers are measured policy; the key is one finite budget.

In the cumulative capstone, the rule becomes concrete: Ten consumers each retry immediately while database connections are saturated. Add bounded backoff, shared concurrency limits, and one retry budget. If the dependency remains unavailable, allow lag to grow within policy rather than multiplying calls.

## 3. Calculate drain feasibility

Net drain is 300/s, so ideal drain time is 120,000/300 = 400 seconds, about 6.7 minutes. This assumes service remains 800/s while live arrivals continue at 500/s, no retries, balanced partitions, and dependencies have capacity. Add headroom and measure actual rates.

A useful way to reason about the boundary is: During broker outage, producer transactions continue writing outbox rows until a budget is reached. Measure row count, oldest age, bytes, database impact, and estimated drain time. A bounded buffer allows short outages; beyond it, admission degrades or rejects commands whose events cannot be delayed safely.

## 4. Interpret two lags

The 30-minute single record may violate timeliness and block an ordered partition, so it is urgent. The 20,000-record burst may be healthy if service rate exceeds arrival and age remains bounded. Inspect partition, failure reason, arrival/service rates, and projected drain time.

The implementation consequence is: A producer can commit quickly while consumers work later, but the business outcome now includes queue delay and completion lag. If arrival rate exceeds service rate, backlog grows. The user may receive an accepted response while the promised downstream effect misses its objective.

## 5. Design backpressure

Warn and pace relays first; shed optional progress events if contract permits; reduce acceptance of new expensive runs; reject with truthful retry guidance before storage exhaustion; preserve terminal/security events; expose degraded readiness and operator alert. Do not continue unlimited writes.

The important nuance is: The broker becomes unavailable for 15 minutes. Completion transactions continue creating outbox rows until the declared byte/age budget approaches warning. Low-priority progress production is shed; new expensive run submissions are throttled before the database buffer is exhausted.

## 6. Design a dead letter

Include stable dead-letter ID, original event ID/type/subject/tenant scope, channel/partition/offset, consumer/effect version, attempts, first/last failure time, safe code/detail, schema/profile versions, body digest, and repair state. Restrict raw body access and retention.

Under concurrency or failure, the distinction becomes: A dead letter records original event identity, consumer/effect, channel/partition/offset, attempts, failure code, safe detail, schema/profile versions, body digest, tenant scope, and timestamps. Sensitive payload access is restricted and may be stored separately or encrypted.

## 7. Repair a poison record

Identify owner and classify cause; verify source truth and body digest; fix consumer/schema or produce a correction; create a dry-run bounded replay plan with a new replay ID; test one canary; apply under rate limits; confirm inbox/effect; mark dead letter resolved with evidence. Never blind-republish.

The design remains honest only if: A dead-letter consumer republishes every record to the original channel without checking schema version or repair approval. The same poison record cycles forever. Require an explicit repair/replay plan with a changed condition and stable replay ID.

## 8. Protect live traffic

Use an isolated consumer/effect target, capped rate/concurrency, lower priority than critical live events, tenant/range chunks, event maximum, checkpoints, lag/resource abort thresholds, canary partition, and pause/resume. Measure live SLO impact and net replay completion.

The consumer-facing consequence is: Review each channel/consumer pair with a failure worksheet: objective, arrival rate, service rate, backlog budget, retention, retry classes, maximum attempts/age, dead-letter owner, replay capacity, and reconciliation oracle. Then run fault injection at receive, effect commit, acknowledgement, broker disconnect, and recovery.

## 9. Test crash recovery

Kill after receive before effect: expect redelivery/no effect. Kill after effect before ack: expect redelivery/one effect via inbox. Kill relay after broker accept before outbox mark: expect duplicate broker record/same event ID. Verify group positions, inbox, projections, and outbox states.

The operational consequence is: After an incident, “lag is zero” is not sufficient. Offsets may have been skipped, dead letters ignored, or projections corrupted. Reconciliation compares source facts, outbox rows, broker records/positions, inbox rows, projection state, and external delivery records.

## 10. Handle partition imbalance

Short term: add consumer capacity only if partition ownership can use it, pace dominant tenant, prioritize critical types, and isolate replay. Long term: revisit key granularity or virtual sharding with a new versioned channel and migration, preserving per-run order. Do not mutate partitioning in place.

The strongest engineering interpretation is: A crashed consumer loses in-flight deliveries; acknowledgement expiry makes them eligible. Group rebalancing assigns partitions to healthy instances. A stale instance must not commit or acknowledge after ownership moves if the handler uses leases or external state.

## 11. Reconcile after manual offset change

Compare authoritative domain facts, outbox rows, broker records/archives, group offsets, inbox rows, projection/effect state, dead letters, and external delivery records by event/effect identity. Identify skipped range and use dry-run repair, not just offset rollback.

The defect-oriented view is: After an incident, “lag is zero” is not sufficient. Offsets may have been skipped, dead letters ignored, or projections corrupted. Reconciliation compares source facts, outbox rows, broker records/positions, inbox rows, projection state, and external delivery records.

## 12. Define recovery complete

Broker is available; outbox and group age/count are below objectives; net drain is nonnegative and backlog cleared or bounded; no unowned dead letters; source/outbox/broker/inbox/projection reconciliation passes; critical journey effects are restored; incident evidence and residual risks are recorded.

Across the Python and TypeScript tracks, the invariant is: An operator manually advanced the group offset past a poison event. Lag becomes zero but analytics lacks one completion. Reconcile event IDs against inbox/projection and create an audited repair; offset state alone is not the truth oracle.
