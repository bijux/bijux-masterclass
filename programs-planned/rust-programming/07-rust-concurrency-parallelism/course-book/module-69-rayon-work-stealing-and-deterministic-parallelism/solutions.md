# Reasoned solutions — Module 69: Rayon, Work Stealing, and Deterministic Parallelism

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the BatchWeave guide](../capstone.md)

Rayon removes scheduler plumbing, not semantic proof. Strong solutions preserve item identity, use owned local accumulators, state reduction laws, isolate effects, and make pool and cutoff policy explicit. “It uses all cores” is not a correctness or performance argument.

The answers below are reasoning models, not scripts to imitate. A different implementation can be stronger when it proves the same contract more directly. Compare ownership, synchronization, progress, failure, and determinism—not only surface syntax.

## Part 1 — Prediction solutions

### Prediction 1

The mutex prevents data races but serializes insertion and makes append order schedule-dependent. Map to owned results and collect, or fold into local vectors/maps and reduce.

### Prediction 2

Subtraction is not associative: `(a-b)-c` differs from `a-(b-c)`. Parallel grouping can change the answer. Use an associative representation such as sum plus sign accounting or preserve a fixed sequential order.

### Prediction 3

Floating-point addition depends on grouping, so bitwise results may vary with partitioning and thread count. Define tolerance, deterministic partition/merge, or a more stable algorithm.

### Prediction 4

Execution order is unspecified, but indexed positional semantics allow collection into corresponding source order. Do not infer which worker handled each position.

### Prediction 5

No. Scheduler discovery order may vary. Carry indices and choose the minimum-index diagnostic after collection if that is the product rule.

### Prediction 6

Already-running tasks may still write after another task fails. Keep effects out of the parallel closure or make them idempotent and commit after successful validation.

### Prediction 7

Pool construction can dominate tiny work and multiplies thread resources. Reuse a pool and take a sequential fast path for small inputs.

### Prediction 8

The product loses bounded submission, explicit queue closure, worker panic accounting, and heterogeneous long-lived protocol state. Use Rayon only for the finite pure stage.

## Part 2 — Repair reasoning

Each parallel task builds a local map and indexed diagnostic list. Reduction merges maps under a documented law and concatenates diagnostics that are later sorted by index. Logging renders after the pool returns. The caller owns a reusable pool. Empty and small inputs use the sequential oracle. This removes shared hot-loop state and separates scheduling from product order.

## Part 3 — Focused construction guidance

### Construction 1

The empty map is identity; merging count maps is associative when count addition cannot overflow. `BTreeMap` or sorted keys make rendering deterministic even though merge order varies.

### Construction 2

Return `Vec<(index, Error)>` or optional indexed errors from tasks, combine, and choose `min_by_key(index)`. Do not depend on which worker returns first.

### Construction 3

`par_iter` shares `&Record` and requires safe shared access; `par_iter_mut` yields disjoint `&mut Record`; `into_par_iter` transfers owned records. Captures must satisfy concurrent closure bounds.

### Construction 4

Specify that hashing cost per item dominates scheduling beyond an estimated size, keep the threshold configurable/private, and benchmark in Course 9. Correctness tests compare every path to sequential.

### Construction 5

Build once with a validated nonzero thread count, pass `&ThreadPool`, and invoke `install`. The API promises only the pool bound, not stable worker assignment.

## Part 4 — Laboratory comparison

Compare the sequential oracle first. The parallel implementation should have no global lock in its hot path and should produce identical ordered output for one, two, and several pool threads. The cutoff is acceptable only as a documented hypothesis awaiting measurement.

## Part 5 — Capstone comparison

The Rayon stage begins after BatchWeave has one immutable terminal outcome per job. It performs no I/O and cannot change run status. Ordered maps and indexed diagnostics preserve deterministic rendering. The manual worker group and Rayon pool have separate resource budgets.

## Part 6 — Reconstruction and defense

The defense should explain work stealing, indexed order, closure bounds, reduction laws, fallible selection, and granularity. It should clearly state which stage remains manual because its lifecycle and backpressure cannot be represented as a pure collection reduction.

A strong defense states what is guaranteed for every allowed schedule, what is merely likely on one machine, and what the design intentionally leaves unspecified.
