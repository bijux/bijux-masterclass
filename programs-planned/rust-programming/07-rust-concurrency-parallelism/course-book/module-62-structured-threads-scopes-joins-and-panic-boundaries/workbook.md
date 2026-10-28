# Workbook — Module 62: Structured Threads: Scopes, Joins, and Panic Boundaries

[Return to the chapter](index.md) · [Open the BatchWeave engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether the chapter has become an operational model. Freeze predictions, protocol diagrams, and invariants before compiling. Concurrency is unusually forgiving of explanations written after observing one successful run; that is exactly why the reasoning record must come first.

## Part 1 — Predict

### Prediction 1

An owned `String` is moved into ordinary `thread::spawn`. Does the value itself need to live for the entire process?

Record: **the meaning of `T: 'static` and ownership**.

### Prediction 2

A worker closure borrows a local vector under ordinary `spawn`. Predict the lifetime error and the scope-based repair.

Record: **outlives relationship and lifecycle boundary**.

### Prediction 3

Two scoped workers receive `&mut values[..10]` and `&mut values[10..]` created by two independent slices. Predict whether the compiler can prove disjointness.

Record: **borrow construction order and `split_at_mut` repair**.

### Prediction 4

A scoped child creates a local `String` and returns `&str` into it. Predict whether scope completion changes owner lifetime.

Record: **reference provenance and destruction**.

### Prediction 5

One explicitly joined scoped worker panics and the function immediately returns. Other handles are unjoined. Predict the lifecycle defect.

Record: **join completeness and failure aggregation**.

### Prediction 6

A child returns `Err(ParseError)` rather than panicking. Describe the nested result observed by the parent.

Record: **domain error versus panic channel**.

### Prediction 7

Four static chunks differ radically in work cost. Predict whether scoped lifetime safety implies balanced completion.

Record: **safety versus scheduling performance**.

### Prediction 8

A scoped handle is stored outside the scope closure. Predict why the type system rejects it.

Record: **handle lifetime and structural containment**.

## Part 2 — Diagnose and repair

Review a matrix normalizer that clones the entire matrix into each ordinary spawned thread, lets every thread mutate its clone, joins only the first handle, and keeps the fastest result. The author claims the clones are necessary because threads require `'static` and the fastest result is acceptable because all normalizations are equivalent.

Identify the semantic duplication, hidden nondeterminism, incomplete joins, and missing proof that all normalizations are equivalent. Repair the design by partitioning rows into disjoint mutable slices inside a scope. If a worker can fail, define whether the parent commits partial mutation or operates on owned candidate buffers first.

### Weak repairs to reject

Reject each of these shortcuts and replace it with the smallest repair that preserves the product requirement:

- using `Box::leak` to manufacture a static reference for finite borrowed work;
- cloning an entire input because ordinary `spawn` rejects a local borrow;
- creating overlapping mutable ranges and relying on runtime indices;
- returning immediately after the first failed join;
- mapping panic and domain error to the same undifferentiated string;
- assuming static chunks balance because they have equal element counts;

For every repair, identify which of the six review dimensions it restores: ownership, visibility, exclusion, progress, failure, or determinism. A repair that improves one dimension may damage another; record both effects.

## Part 3 — Focused exercises

### Construction 1

Draw the lifetime diagram for an enclosing slice, a call to `thread::scope`, two child closures, and parent reuse after the scope.

Required evidence: State which relationship the API proves and which progress property it does not prove.

### Construction 2

Implement a scoped parallel maximum over borrowed data.

Required evidence: Handle empty input, join every child, and avoid cloning the data.

### Construction 3

Normalize a mutable slice through disjoint chunks.

Required evidence: Construct the disjoint borrows before spawning and prove parent access resumes only after scope exit.

### Construction 4

Design a result type for scoped workers that can return a domain error or panic.

Required evidence: Preserve the distinction and aggregate all child outcomes before returning.

### Construction 5

Compare scoped threads and Rayon for a workload whose item costs are unpredictable.

Required evidence: Discuss lifetime, scheduling, failure, ordering, and dependency cost.

## Part 4 — Independent laboratory

Build [Scoped Slice Analysis](../../labs/module-02-scoped-slice-analysis/README.md) from the starter. Before opening the solution, produce:

- a lifetime diagram for the source slice, scope, child borrows, and result;
- an immutable summary operation and a disjoint mutable operation without input cloning;
- tests for empty input, fewer items than workers, uneven partitions, and negative values;
- an explicit join and panic policy;
- a workload-skew note explaining the limit of static chunking;

Your submission must also identify one schedule that the implementation handles correctly and one product claim it deliberately does not make.

## Part 5 — Capstone transfer

Implement BatchWeave’s pure manifest inspection stage with scoped threads over borrowed job definitions. The stage may compute deterministic per-job estimates or validation summaries, but it must not start the long-lived worker engine. Preserve source order, join all children, and keep borrowed data inside the inspection call.

Required capstone evidence:

- a lifetime diagram separating manifest storage from scoped inspection children;
- a test proving the manifest can be used again immediately after scope exit;
- a panic/domain-error distinction for inspection work;
- a written decision explaining why the execution engine will use owned jobs instead;

Add at least one regression test that fails if this module's governing contract is removed. Tests that merely sleep and hope for a schedule do not count as causal evidence.

## Part 6 — Reconstruct and defend

Answer without the chapter:

1. What does `T: 'static` actually constrain?
2. What relationship does `thread::scope` establish?
3. Why must mutable data be partitioned before spawning?
4. How do panic and domain failure appear after join?
5. When is Rayon a better boundary than scoped operating-system threads?

### Independent transfer

Build a finite image-row transformer that borrows one mutable pixel buffer, gives disjoint row bands to scoped workers, and returns after all bands are complete. Add a fallible validation pass that occurs before mutation. Then change the design so one band can discover a domain error during mutation: choose and defend either partial-commit semantics or candidate-buffer rollback semantics.
