# Workbook — Module 69: Rayon, Work Stealing, and Deterministic Parallelism

[Return to the chapter](index.md) · [Open the BatchWeave engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether the chapter has become an operational model. Freeze predictions, protocol diagrams, and invariants before compiling. Concurrency is unusually forgiving of explanations written after observing one successful run; that is exactly why the reasoning record must come first.

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

## Part 4 — Independent laboratory

Build [Parallel Histogram](../../labs/module-09-parallel-histogram/README.md) from the starter. Before opening the solution, produce:

- a sequential oracle and equality tests across sizes and pool widths;
- a written identity/associativity proof for map merge;
- no mutex in the per-item accumulation path;
- deterministic key rendering;
- a documented sequential cutoff hypothesis rather than a speed claim;

Your submission must also identify one schedule that the implementation handles correctly and one product claim it deliberately does not make.

## Part 5 — Capstone transfer

Implement BatchWeave’s pure report stage with Rayon 1.12.0 in a caller-configured custom pool. Derive operation and outcome histograms from the immutable final outcome slice using local fold/reduce. Render through ordered maps. Keep job execution, queueing, cancellation, file input, and terminal output outside Rayon.

Required capstone evidence:

- a sequential report oracle and cross-thread-count equality tests;
- law statements for every reduction;
- deterministic error and key ordering;
- a pool-lifecycle decision and valid thread-count bounds;
- a cost hypothesis and sequential cutoff;

Add at least one regression test that fails if this module's governing contract is removed. Tests that merely sleep and hope for a schedule do not count as causal evidence.

## Part 6 — Reconstruct and defend

Answer without the chapter:

1. What does work stealing allow the scheduler to change?
2. Which parallel iterator property supports stable positional collection?
3. Why do parallel reductions need identity and associativity?
4. Why can error discovery and short-circuit timing vary?
5. When is a manual worker protocol more appropriate than Rayon?

### Independent transfer

Build a parallel source-code statistics function over an in-memory file list. Parsing is pure and may fail. Return deterministic per-language counts plus diagnostics sorted by source index. Use a custom pool and sequential oracle. Then add a requirement to stream files from disk with bounded in-flight bytes and explain why the I/O stage should remain outside the Rayon reduction.
