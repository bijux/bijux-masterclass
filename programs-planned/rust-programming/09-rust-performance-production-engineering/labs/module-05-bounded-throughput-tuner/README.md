# Laboratory 85 — Bounded Throughput Tuner

**Course 9 · Module 85: Runtime Efficiency: Contention, Queueing, Batching, and Async Load**

[Chapter](../../course-book/module-85-runtime-efficiency-contention-queueing-batching-and-async-load/index.md) · [Workbook](../../course-book/module-85-runtime-efficiency-contention-queueing-batching-and-async-load/workbook.md) · [MetricRail guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Runtime Efficiency: Contention, Queueing, Batching, and Async Load**: When work is correct and bounded, where do contention, waiting, scheduling, queueing, batching, and blocking determine throughput and tail latency? The product must make **Separate service time, wait time, queue depth, concurrency, throughput, and utilization** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **saturation and queueing curve** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Product

Build a Tokio work service that accepts a finite vector of numeric jobs under two independent limits: bounded queue capacity and bounded active execution. It returns one source-ordered terminal `Outcome` for every offered job and phase samples for admitted work.

The laboratory is a controlled saturation instrument. It is not enough to return doubled values. You must account for offered, accepted, completed, failed, and rejected work so that tuning cannot hide overload.

## Public contract

`Tuning` contains `queue_capacity` and `max_active`, both nonzero. `run(values, tuning)` must:

- offer every source item exactly once;
- reject explicitly when immediate bounded admission is unavailable under the defined burst model;
- never lose an accepted item;
- treat arithmetic overflow as `Failed`, not panic or missing output;
- cap concurrent service at `max_active`;
- record queue-wait and service durations for accepted items;
- return outcomes in source order regardless of completion order;
- satisfy `offered = accepted + rejected` and `accepted = completed + failed` after completion.

The implementation may use channels, semaphores, `JoinSet`, or another owned task structure, but all tasks must be joined.

## Construction route

1. Define terminal outcome types and accounting identities before spawning work.
2. Assign each input a source index.
3. Create a bounded queue and active-work permits.
4. Record admission/enqueue time.
5. Transfer ownership of accepted jobs to the service.
6. Collect `(index, outcome, phase sample)` and reject duplicates/out-of-range indices.
7. Fill explicit rejected outcomes for jobs not admitted.
8. Verify every slot is terminal before constructing the report.

## Tuning experiment

Run at least six configurations combining small/large queue and low/high active counts. Use workloads containing normal values and an overflow case. For each configuration report:

- offered/accepted/rejected;
- completed/failed;
- queue-wait distribution;
- service distribution;
- total elapsed time;
- maximum active work if you instrument it.

Do not call the configuration with the most completions “best” without stating latency and memory consequences. The input vector is finite; explain how the burst model differs from a rate-controlled production load.

## Adversarial cases

Test zero limits, empty input, one item, queue smaller than offered burst, active limit greater than queue, arithmetic overflow, and task completion out of source order. Missing terminal results are invariant violations, not default rejection.

## Transfer

Add an overall deadline. Decide what happens to waiting and active jobs when it expires, and add `Cancelled` if needed. Preserve exactly one terminal outcome per source item. Explain how a deadline changes the accounting identity and what late blocking work may still do.

## Completion

The laboratory is complete when capacity is actually bounded, task ownership is closed, accounting identities hold, failures are terminal, results are deterministic, and the tuning report discusses the saturation trade-off rather than a single throughput number.

Use `solution/` only after you can explain every accepted and rejected source index. Compare accounting and phase boundaries; a shorter async implementation that drops results or hides rejections is not a valid improvement.

## Saturation experiment matrix

Run a two-dimensional sweep over offered concurrency and one policy variable such as worker count, queue capacity, or batch size. For each cell record offered, admitted, completed, rejected, and timed-out work; p50 and p99 completion latency; queue high-water mark; active-worker utilization; and total experiment duration. Use an identical deterministic workload for every comparison.

Identify the first saturation knee and the failure mode beyond it. Then select one configuration for low latency and one for maximum useful throughput. Explain why increasing queue capacity may increase accepted work temporarily while worsening tail latency and shutdown time. The final recommendation must include a hard upper bound for every queue and a reason the admission point occurs before expensive commitment.

## Terminal-accounting checks

For every accepted unit of work, prove that the experiment records exactly one terminal category: completed, rejected after admission, cancelled, timed out, or failed. Compare that authoritative count with live gauges after the system returns to quiescence. A throughput number is invalid if accepted work disappears from accounting or remains stranded in a queue when the run ends. Include shutdown while saturated and report the time required to drain or cancel bounded outstanding work.

## Completion question

Which number in your report represents useful service capacity rather than admitted demand or queued intent? Defend that choice and show the terminal-accounting equation for the most overloaded run. If the equation does not balance, no batching or worker configuration may be recommended.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Bounded Throughput Tuner**.
2. Draw the smallest **saturation and queueing curve** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to MetricRail so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Separate service time, wait time, queue depth, concurrency, throughput, and utilization.
- Apply Little’s Law as a consistency check while stating its steady-state assumptions.
- Find lock contention, convoying, hot sharding, wake amplification, and blocking-runtime violations.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 85 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **saturation and queueing curve**. Defend why your design is simpler than one plausible alternative under the new requirements.
