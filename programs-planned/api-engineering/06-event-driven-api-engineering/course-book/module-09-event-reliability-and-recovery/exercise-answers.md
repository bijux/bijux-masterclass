# Reference Answers — Module 09: Worked answers — Module 09 — Event Reliability, Backpressure, Dead Letters, and Recovery

Read after attempting all twelve Event Reliability, Backpressure, Dead Letters, and Recovery exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Classify failures

Schema invalidity, authorization rejection, and unsupported version are permanent/security contract failures for the current record. Database timeout and broker outage are transient under bounded retry. A hot partition is a capacity/design failure requiring admission, scaling, or repartitioning—not repeated handler retries.

## 2. Build a retry budget

For example: maximum 4 attempts over 60 seconds, exponential delays 1/3/9 seconds plus bounded jitter, per-consumer database concurrency 8, one total dependency deadline per attempt, and dead-letter/escalation after total age. Exact numbers are measured policy; the key is one finite budget.

## 3. Calculate drain feasibility

Net drain is 300/s, so ideal drain time is 120,000/300 = 400 seconds, about 6.7 minutes. This assumes service remains 800/s while live arrivals continue at 500/s, no retries, balanced partitions, and dependencies have capacity. Add headroom and measure actual rates.

## 4. Interpret two lags

The 30-minute single record may violate timeliness and block an ordered partition, so it is urgent. The 20,000-record burst may be healthy if service rate exceeds arrival and age remains bounded. Inspect partition, failure reason, arrival/service rates, and projected drain time.

## 5. Design backpressure

Warn and pace relays first; shed optional progress events if contract permits; reduce acceptance of new expensive runs; reject with truthful retry guidance before storage exhaustion; preserve terminal/security events; expose degraded readiness and operator alert. Do not continue unlimited writes.

## 6. Design a dead letter

Include stable dead-letter ID, original event ID/type/subject/tenant scope, channel/partition/offset, consumer/effect version, attempts, first/last failure time, safe code/detail, schema/profile versions, body digest, and repair state. Restrict raw body access and retention.

## 7. Repair a poison record

Identify owner and classify cause; verify source truth and body digest; fix consumer/schema or produce a correction; create a dry-run bounded replay plan with a new replay ID; test one canary; apply under rate limits; confirm inbox/effect; mark dead letter resolved with evidence. Never blind-republish.

## 8. Protect live traffic

Use an isolated consumer/effect target, capped rate/concurrency, lower priority than critical live events, tenant/range chunks, event maximum, checkpoints, lag/resource abort thresholds, canary partition, and pause/resume. Measure live SLO impact and net replay completion.

## 9. Test crash recovery

Kill after receive before effect: expect redelivery/no effect. Kill after effect before ack: expect redelivery/one effect via inbox. Kill relay after broker accept before outbox mark: expect duplicate broker record/same event ID. Verify group positions, inbox, projections, and outbox states.

## 10. Handle partition imbalance

Short term: add consumer capacity only if partition ownership can use it, pace dominant tenant, prioritize critical types, and isolate replay. Long term: revisit key granularity or virtual sharding with a new versioned channel and migration, preserving per-run order. Do not mutate partitioning in place.

## 11. Reconcile after manual offset change

Compare authoritative domain facts, outbox rows, broker records/archives, group offsets, inbox rows, projection/effect state, dead letters, and external delivery records by event/effect identity. Identify skipped range and use dry-run repair, not just offset rollback.

## 12. Define recovery complete

Broker is available; outbox and group age/count are below objectives; net drain is nonnegative and backlog cleared or bounded; no unowned dead letters; source/outbox/broker/inbox/projection reconciliation passes; critical journey effects are restored; incident evidence and residual risks are recorded.
