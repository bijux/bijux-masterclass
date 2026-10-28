# Workbook — Module 69: Rayon, Work Stealing, and Deterministic Parallelism

[Chapter](index.md) · [Laboratory](../../labs/module-09-parallel-histogram/README.md) · [BatchWeave guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Rayon, Work Stealing, and Deterministic Parallelism** has become a usable model rather than remembered vocabulary. Its governing question is: *How can divisible computation use a work-stealing pool while preserving item meaning, reduction laws, failure policy, result ordering, and a defensible cost model?* Preserve your first prediction and record decisive facts in a **work-partition and reduction map**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 68 — Lock-Free Protocols, Reclamation, and Unsafe Send/Sync that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **How can divisible computation use a work-stealing pool while preserving item meaning, reduction laws, failure policy, result ordering, and a defensible cost model?**
3. Draw the smallest **work-partition and reduction map** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

### Prediction 1

A `par_iter().map(...)` closure pushes into one `Arc<Mutex<Vec<_>>>`. Predict correctness and contention.

Record: **data-race status, order, and better collection design**.

### Prediction 2

A parallel reduction subtracts partial sums. Predict result stability.

Record: **associativity counterexample**.

### Prediction 3

A floating-point sum uses `par_iter().sum()`. Predict bitwise reproducibility across thread counts.

Record: **rounding and grouping**.

### Prediction 4

An indexed slice parallel map collects into `Vec`. Predict relation between execution order and output position.

Record: **indexed ordering**.

### Prediction 5

A fallible parallel parse returns one error. Predict whether it is always the lowest input index.

Record: **error selection policy**.

### Prediction 6

A closure performs file writes and expects no later item to run after one error. Predict effect behavior.

Record: **cooperative short-circuit and effect isolation**.

### Prediction 7

A new Rayon pool is created for every 20-item request. Predict the cost model.

Record: **pool lifecycle and granularity**.

### Prediction 8

A manual blocking worker queue is replaced wholesale with `par_iter`. Predict lost product features.

Record: **backpressure, cancellation, lifecycle, and heterogeneous operations**.

## Part 2 — Diagnose and repair

Review an analytics function that calls `par_iter`, locks one global `HashMap` per item, appends errors to one shared vector, writes progress lines from worker closures, and returns the first vector element as the “first error.” It creates a new eight-thread pool for every call, even for empty input.

Replace shared hot-loop mutation with local fold/reduce, attach source indices to diagnostics, select errors deterministically after the parallel phase, move terminal output outside the parallel core, reuse a caller-owned pool, and add a sequential cutoff. State the algebraic laws and resource hypotheses.

### Weak repairs to reject

Reject each of these shortcuts and replace it with the smallest repair that preserves the product requirement:

- adding a larger mutex or switching to a concurrent map without removing hot-loop contention;
- assuming `reduce` preserves left-to-right grouping;
- calling floating-point rounding differences a bug without defining reproducibility;
- performing irreversible effects inside a fallible parallel closure;
- creating pools per request;
- using Rayon for a protocol that requires blocking backpressure and explicit shutdown events;

For every repair, identify which of the six review dimensions it restores: ownership, visibility, exclusion, progress, failure, or determinism. A repair that improves one dimension may damage another; record both effects.

## Part 3 — Focused exercises

### Construction 1

Prove laws for a word-frequency map merge.

Required evidence: State identity, associativity, overflow bounds, and deterministic rendering order.

### Construction 2

Build a parallel validator that reports the lowest-index error deterministically.

Required evidence: Attach indices, isolate pure validation, and select after bounded parallel work.

### Construction 3

Compare `par_iter`, `par_iter_mut`, and `into_par_iter` for a vector of records.

Required evidence: Track ownership and `Send`/`Sync` requirements through each API.

### Construction 4

Design a sequential cutoff for expensive hashing.

Required evidence: Write a falsifiable cost hypothesis and tests against a sequential oracle; do not claim performance yet.

### Construction 5

Create and reuse a custom pool in a library API.

Required evidence: Make thread count explicit, reject zero, and avoid relying on worker identity.

### Interleaved reasoning pass

1. For **Distinguish task parallelism, data parallelism, and a long-lived message-driven worker service**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the work-partition and reduction map.
2. For **Explain work stealing without relying on worker identity or execution order**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the work-partition and reduction map.
3. For **Derive closure `Send` and captured-state `Sync` requirements from parallel execution**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the work-partition and reduction map.
4. For **Track item ownership and ordering through indexed parallel iterators**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the work-partition and reduction map.

5. Identify one guarantee from an earlier course that a careless implementation of **Rayon, Work Stealing, and Deterministic Parallelism** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Parallel Histogram](../../labs/module-09-parallel-histogram/README.md) from the starter. Before opening the solution, produce:

- a sequential oracle and equality tests across sizes and pool widths;
- a written identity/associativity proof for map merge;
- no mutex in the per-item accumulation path;
- deterministic key rendering;
- a documented sequential cutoff hypothesis rather than a speed claim;

Your submission must also identify one schedule that the implementation handles correctly and one product claim it deliberately does not make.

### Laboratory acceptance trace

Before opening the reference implementation for **Parallel Histogram**, record:

- the public behavior that demonstrates **Distinguish task parallelism, data parallelism, and a long-lived message-driven worker service**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Implement BatchWeave’s pure report stage with Rayon 1.12.0 in a caller-configured custom pool. Derive operation and outcome histograms from the immutable final outcome slice using local fold/reduce. Render through ordered maps. Keep job execution, queueing, cancellation, file input, and terminal output outside Rayon.

Required capstone evidence:

- a sequential report oracle and cross-thread-count equality tests;
- law statements for every reduction;
- deterministic error and key ordering;
- a pool-lifecycle decision and valid thread-count bounds;
- a cost hypothesis and sequential cutoff;

Add at least one regression test that fails if this module's governing contract is removed. Tests that merely sleep and hope for a schedule do not count as causal evidence.

### Capstone invariant trace

For the Module 69 BatchWeave increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Answer without the chapter:

1. What does work stealing allow the scheduler to change?
2. Which parallel iterator property supports stable positional collection?
3. Why do parallel reductions need identity and associativity?
4. Why can error discovery and short-circuit timing vary?
5. When is a manual worker protocol more appropriate than Rayon?

### Independent transfer

Build a parallel source-code statistics function over an in-memory file list. Parsing is pure and may fail. Return deterministic per-language counts plus diagnostics sorted by source index. Use a custom pool and sequential oracle. Then add a requirement to stream files from disk with bounded in-flight bytes and explain why the I/O stage should remain outside the Rayon reduction.

### Closed-book defense

In five minutes, answer “How can divisible computation use a work-stealing pool while preserving item meaning, reduction laws, failure policy, result ordering, and a defensible cost model?” using the **work-partition and reduction map**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside BatchWeave. A list of APIs without the deciding relationship is incomplete.
