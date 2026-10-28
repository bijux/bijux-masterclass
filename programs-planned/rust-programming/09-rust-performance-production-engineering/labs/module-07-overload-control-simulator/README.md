# Laboratory 7 — Overload Control Simulator

[Common laboratory method](../../../START_HERE.md#laboratory-method) · [Module 87 chapter](../../course-book/module-87-reliability-under-load-slos-load-shedding-retries-and-degradation/index.md)

## Product

Build a deterministic discrete-event simulator for bounded service capacity, queueing, rejection, retry, and recovery. Wall-clock async code is deliberately excluded: the goal is to make policy causality visible and testable.

Input is a sequence of ticks, each containing source `Arrival`s. `Policy` defines queue capacity, service completions per tick, retry limit, a threshold for entering recovery, and a lower threshold for leaving it. The report distinguishes source demand from generated attempts and gives each source exactly one terminal result.

## Identity and accounting

A source ID represents one semantic request. `attempt` counts retry attempts and begins at zero. Reject duplicate source IDs and malformed initial attempts before simulation.

The final report must distinguish:

- `source_offered`: original semantic requests;
- `attempts`: all initial and retry attempts considered;
- `admitted_attempts`: attempts placed in the queue;
- `retries_scheduled`;
- completed sources;
- terminally rejected sources;
- maximum queue depth;
- ticks spent in recovery;
- one terminal outcome per source ID.

Do not count a retry as a new successful source request. Do not let a source both complete and terminate rejected.

## Policy behavior

Validate all policy relationships before work:

- queue and service capacities are nonzero;
- recovery exit threshold is not above entry threshold;
- entry threshold does not exceed queue capacity;
- retry arithmetic cannot overflow.

At each tick, process the declared sequence consistently: arrivals/retries, admission, service, and recovery transitions. Document the order because changing it changes results. Recovery must use hysteresis; one low sample must not immediately reopen the system if the policy says otherwise.

## Construction route

1. Normalize and validate source arrivals.
2. Create deterministic queues for pending work and scheduled retries.
3. Track per-source state explicitly.
4. Apply the tick transition in one documented order.
5. On rejection, schedule a bounded retry or make the source terminal.
6. Service at most `service_per_tick` attempts.
7. Enter/leave recovery from the policy thresholds.
8. Continue after external arrivals end until all scheduled/queued sources are terminal, with a justified safety bound.
9. Sort terminal output deterministically.

## Scenario suite

Run and explain:

1. steady load below capacity;
2. one short burst that the queue absorbs;
3. sustained overload that sheds;
4. overload followed by recovery;
5. retry amplification with low retry limit;
6. a policy whose thresholds are invalid.

Compare at least two policies. A policy with fewer immediate rejections may still be worse if attempts, queue depth, and recovery time grow.

## Adversarial cases

Test duplicate IDs, nonzero initial attempt, zero capacity, inverted thresholds, entry threshold above capacity, no arrivals, all arrivals at one tick, and retry limit zero. Ensure simulation cannot loop forever because a source remains neither scheduled nor terminal.

## Transfer

Add one absolute source deadline expressed in ticks. Retries and queue residence consume the same budget. Add `Expired` as a terminal outcome and prove terminal accounting remains one-per-source.

## Completion

The laboratory is complete when the simulator is deterministic, invalid policy is rejected, source/attempt identities remain separate, hysteresis is observable, every source is terminal, and the report supports a policy decision rather than merely producing counts.

Use `solution/` after implementing your own transition order. Compare state invariants and accounting. A simulator that gives plausible numbers but cannot explain one source’s path is not complete.

## Reliability scenario table

Evaluate at least six scenarios: normal load, brief overload, sustained overload, slow downstream work, retrying clients, and one partially failing dependency. For each, record admission behavior, queue growth, completion latency, rejected work, retries generated, degraded features, and recovery time after offered load returns to normal. Identify which events consume the error budget and which are intentional protection mechanisms.

Your final policy must distinguish rejection before commitment from failure after commitment. Define one overall deadline, an attempt limit, and a retryable failure set. Show that retries cannot multiply offered load without bound. Include a degradation mode that protects the primary operation and a recovery condition that prevents the service from oscillating rapidly between normal and degraded states.

## Recovery experiment

After each overload scenario, return offered load to a sustainable level and measure queue drain, latency recovery, rejection recovery, and any retry aftershock. A protective policy is incomplete if it survives overload but requires a restart to recover. Test hysteresis or recovery thresholds where applicable, and verify that retained failure state, open permits, and retry timers all converge to the declared quiescent condition.

