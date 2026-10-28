# Laboratory 5 — Bounded Throughput Tuner

[Common laboratory method](../../../START_HERE.md#laboratory-method) · [Module 85 chapter](../../course-book/module-85-runtime-efficiency-contention-queueing-batching-and-async-load/index.md)

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

