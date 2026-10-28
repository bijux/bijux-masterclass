# Reasoned Solutions — Module 69: Rayon, Work Stealing, and Deterministic Parallelism

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-09-parallel-histogram/README.md) · [BatchWeave guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 69: Rayon, Work Stealing, and Deterministic Parallelism**. Compare the reasoning against this question: *How can divisible computation use a work-stealing pool while preserving item meaning, reduction laws, failure policy, result ordering, and a defensible cost model?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

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

## Deep reasoning and transfer

### Decisive model

> How can divisible computation use a work-stealing pool while preserving item meaning, reduction laws, failure policy, result ordering, and a defensible cost model?

Build a **work-partition and reduction map**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Distinguish task parallelism, data parallelism, and a long-lived message-driven worker service.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Explain work stealing without relying on worker identity or execution order.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Derive closure `Send` and captured-state `Sync` requirements from parallel execution.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Track item ownership and ordering through indexed parallel iterators.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **State identity and associativity laws for `fold`, `reduce`, and grouped aggregation.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Distinguish task parallelism, data parallelism, and a long-lived message-driven worker service.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the work-partition and reduction map.

### Reference implementation comparison

For [Parallel Histogram](../../labs/module-09-parallel-histogram/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In BatchWeave, Module 69 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Rayon, Work Stealing, and Deterministic Parallelism**, which relationship decides this question: “How can divisible computation use a work-stealing pool while preserving item meaning, reduction laws, failure policy, result ordering, and a defensible cost model?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to BatchWeave?
