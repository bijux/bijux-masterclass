# Laboratory 87 — Overload Control Simulator

**Course 9 · Module 87: Reliability Under Load: SLOs, Load Shedding, Retries, and Degradation**

[Chapter](../../course-book/module-87-reliability-under-load-slos-load-shedding-retries-and-degradation/index.md) · [Workbook](../../course-book/module-87-reliability-under-load-slos-load-shedding-retries-and-degradation/workbook.md) · [MetricRail guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Reliability Under Load: SLOs, Load Shedding, Retries, and Degradation**: How does the service preserve useful work and recover predictably when demand, dependency latency, error rate, or resource pressure exceeds the normal operating envelope? The product must make **Write a service-level indicator and objective whose population, success condition, window, and exclusions are unambiguous** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **SLO and overload policy** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

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

## Working route

1. Read the product contract and run the starter’s baseline checks for **Overload Control Simulator**.
2. Draw the smallest **SLO and overload policy** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to MetricRail so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Write a service-level indicator and objective whose population, success condition, window, and exclusions are unambiguous.
- Derive admission and shedding policies from protected resources and customer-visible priorities.
- Build retries around idempotency, one deadline budget, bounded attempts, and retryable classifications.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 87 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **SLO and overload policy**. Defend why your design is simpler than one plausible alternative under the new requirements.
