# Course 4 study plan — Functional Rust

This plan turns ten chapters into ten days of deliberate practice. A day is complete only when the model, independent laboratory, and LedgerFlow increment agree. If the lab passes while the explanation remains vague, repair the model before moving on.

## Daily rhythm

| Time | Work | Required output |
|---|---|---|
| 08:30–09:00 | closed-book reconstruction | one page of the previous mechanism from memory |
| 09:00–11:00 | authoritative chapter and typed examples | annotated model and changed-assumption predictions |
| 11:15–12:30 | compiler or boundary specimens | frozen predictions and causal comparison |
| 13:30–15:00 | repair and focused construction | smallest principled repair plus rejected shortcut |
| 15:15–17:30 | independent laboratory | working behavior, adversarial tests, design record |
| 18:30–20:00 | LedgerFlow increment | integrated change and regression evidence |
| 20:00–20:30 | explanation and retrieval | invariant, decisive rule, failure state, transfer case |

Take real breaks. Dense work is not continuous screen time. The weekend between Days 5 and 6 is for repair, reconstruction, and rest rather than new material.

## Day 1 — Closures, Capture, and Callable Contracts

**Governing question:** What does a closure capture, which callable traits does it implement, and what invocation contract should an API require?

### Morning: derive the model

Read [Module 31](module-31-closures-capture-and-callable-contracts/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-31-closures-capture-and-callable-contracts/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 31 — Closure Policy Matrix](../labs/module-01-closure-policy-matrix/README.md). This laboratory turns closure capability into observable product behavior. The executable surface is in `labs/module-01-closure-policy-matrix/README.md`.

### Evening: integrate the course product

The course capstone is **LedgerFlow**, a deterministic event-analysis pipeline with diagnostics, audit history, queries, and reports. Define LedgerFlow callbacks for filtering, mapping, and policy decisions with the weakest callable capability that matches actual invocation and capture behavior. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“What does a closure capture, which callable traits does it implement, and what invocation contract should an API require?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Distinguish function items, function pointers, and anonymous closure types;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 2 — The Iterator Model

**Governing question:** What state does an iterator own, when does work happen, and what is consumed by each call to next?

### Morning: derive the model

Read [Module 32](module-32-the-iterator-model/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-32-the-iterator-model/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 32 — Lazy Log Query](../labs/module-02-lazy-log-query/README.md). The executable contract is in `labs/module-02-lazy-log-query/README.md`. This laboratory is about pull behavior, not just filtering syntax.

### Evening: integrate the course product

The course capstone is **LedgerFlow**, a deterministic event-analysis pipeline with diagnostics, audit history, queries, and reports. Expose lazy borrowed event queries and trace when parsing, filtering, and inspection actually occur. Avoid collecting merely to make a borrow problem disappear. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“What state does an iterator own, when does work happen, and what is consumed by each call to next?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Explain the distinct roles of `IntoIterator`, `Iterator`, adapters, and consumers;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 3 — Iterator Algebra and Pipeline Shape

**Governing question:** How do adapters change item type, cardinality, order, ownership, and stopping behavior across a pipeline?

### Morning: derive the model

Read [Module 33](module-33-iterator-algebra-and-pipeline-shape/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-33-iterator-algebra-and-pipeline-shape/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 33 — Record-Shaping Pipeline](../labs/module-03-record-shaping-pipeline/README.md). Use `labs/module-03-record-shaping-pipeline/README.md` for the executable package. The purpose is to make every shape change reviewable.

### Evening: integrate the course product

The course capstone is **LedgerFlow**, a deterministic event-analysis pipeline with diagnostics, audit history, queries, and reports. Build the ordered event-shaping pipeline and document each stage's item type, cardinality, order, borrowing, and allocation behavior. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“How do adapters change item type, cardinality, order, ownership, and stopping behavior across a pipeline?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Derive the item type and cardinality effect of common iterator adapters;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 4 — Folds, Scans, and Short-Circuiting

**Governing question:** What invariant does an accumulator maintain, and when should a traversal continue, emit intermediate state, or stop early?

### Morning: derive the model

Read [Module 34](module-34-folds-scans-and-short-circuiting/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-34-folds-scans-and-short-circuiting/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 34 — Streaming Metrics](../labs/module-04-streaming-metrics/README.md). The crate in `labs/module-04-streaming-metrics/README.md` asks for four related but different traversals. Treat them as separate contracts.

### Evening: integrate the course product

The course capstone is **LedgerFlow**, a deterministic event-analysis pipeline with diagnostics, audit history, queries, and reports. Reduce valid events into ledger state with an explicit prefix invariant and short-circuit on fatal violations without leaving partial mutation. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“What invariant does an accumulator maintain, and when should a traversal continue, emit intermediate state, or stop early?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Design a fold accumulator with a precise prefix invariant;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 5 — Option, Result, and Fallible Traversal

**Governing question:** Should a fallible traversal skip, fail fast, recover, accumulate diagnostics, or continue with an explicit default?

### Morning: derive the model

Read [Module 35](module-35-option-result-and-fallible-traversal/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-35-option-result-and-fallible-traversal/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 35 — Resilient Import](../labs/module-05-resilient-import/README.md). The executable package is `labs/module-05-resilient-import/README.md`. This laboratory separates optional data from invalid data and fail-fast policy from accumulation policy.

### Evening: integrate the course product

The course capstone is **LedgerFlow**, a deterministic event-analysis pipeline with diagnostics, audit history, queries, and reports. Separate row-local diagnostics, fatal stream failures, warnings, and duplicate policy. Preserve physical source order when diagnostics from multiple phases are combined. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“Should a fallible traversal skip, fail fast, recover, accumulate diagnostics, or continue with an explicit default?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Compose optional and fallible transformations while preserving ownership and error meaning;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 6 — Custom Iterators and Collection Protocols

**Governing question:** What laws must a custom traversal obey, and who owns the collection when iteration begins?

### Morning: derive the model

Read [Module 36](module-36-custom-iterators-and-collection-protocols/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-36-custom-iterators-and-collection-protocols/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 36 — Custom Cursors](../labs/module-06-custom-cursors/README.md). The executable work is in `labs/module-06-custom-cursors/README.md`. This is a law laboratory: each implemented trait makes a promise stronger than “the examples passed.”

### Evening: integrate the course product

The course capstone is **LedgerFlow**, a deterministic event-analysis pipeline with diagnostics, audit history, queries, and reports. Implement domain traversal for accounts or audit history where a named iterator clarifies state and exhaustion better than another anonymous chain. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“What laws must a custom traversal obey, and who owns the collection when iteration begins?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Implement a correct custom `Iterator` by defining state and exhaustion behavior;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 7 — Recursive Data and Structural Sharing

**Governing question:** How can recursive values be transformed without hiding ownership, rebuilding cost, or structural sharing?

### Morning: derive the model

Read [Module 37](module-37-recursive-data-and-structural-sharing/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-37-recursive-data-and-structural-sharing/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 37 — Persistent History](../labs/module-07-persistent-history/README.md). The executable crate is `labs/module-07-persistent-history/README.md`. The target is an immutable outline whose versions share unchanged nodes.

### Evening: integrate the course product

The course capstone is **LedgerFlow**, a deterministic event-analysis pipeline with diagnostics, audit history, queries, and reports. Retain persistent audit versions through structural sharing and prove which nodes are rebuilt after an update. State the memory cost without claiming zero-copy magic. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“How can recursive values be transformed without hiding ownership, rebuilding cost, or structural sharing?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Define recursive algebraic data with the appropriate indirection;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 8 — Functional Core and Effect Isolation

**Governing question:** Which decisions can remain pure, which effects must occur at the boundary, and what data should cross between them?

### Morning: derive the model

Read [Module 38](module-38-functional-core-and-effect-isolation/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-38-functional-core-and-effect-isolation/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 38 — Deterministic Batch Runner](../labs/module-08-deterministic-batch-runner/README.md). The executable package is `labs/module-08-deterministic-batch-runner/README.md`. The laboratory separates decisions from effect execution and makes partial effects explicit.

### Evening: integrate the course product

The course capstone is **LedgerFlow**, a deterministic event-analysis pipeline with diagnostics, audit history, queries, and reports. Move filesystem and terminal operations into an effect shell around a deterministic analysis core. Represent intended effects as data where that improves testing. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“Which decisions can remain pure, which effects must occur at the boundary, and what data should cross between them?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Separate deterministic domain decisions from filesystem, time, environment, and terminal effects;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 9 — Combinator Laws and Cost Models

**Governing question:** What semantic laws should a combinator preserve, and what can honestly be claimed about evaluation and cost?

### Morning: derive the model

Read [Module 39](module-39-combinator-laws-and-cost-models/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-39-combinator-laws-and-cost-models/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 39 — Combinator Contracts](../labs/module-09-combinator-contracts/README.md). The executable package is `labs/module-09-combinator-contracts/README.md`. The objective is not to create a large helper library. It is to admit only combinators with stable semantics, bounded claims, and a real reuse case.

### Evening: integrate the course product

The course capstone is **LedgerFlow**, a deterministic event-analysis pipeline with diagnostics, audit history, queries, and reports. Review reusable LedgerFlow combinators with laws and counterexamples for order, identity, error propagation, and duplication. Attach honest operation-count claims. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“What semantic laws should a combinator preserve, and what can honestly be claimed about evaluation and cost?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Design domain combinators that preserve type and error meaning;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 10 — Functional Architecture Synthesis

**Governing question:** How do closure, iterator, error, reduction, structural-sharing, and effect decisions compose into a readable whole system?

### Morning: derive the model

Read [Module 40](module-40-functional-architecture-synthesis/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-40-functional-architecture-synthesis/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 40 — Route Analysis Engine](../labs/module-10-route-analysis-engine/README.md). The executable crate is `labs/module-10-route-analysis-engine/README.md`. This is an independent transfer laboratory. It uses Course 4 mechanisms but does not copy LedgerFlow’s domain or architecture mechanically.

### Evening: integrate the course product

The course capstone is **LedgerFlow**, a deterministic event-analysis pipeline with diagnostics, audit history, queries, and reports. Add an unseen cross-cutting analysis or reporting requirement while preserving deterministic output, audit history, and explicit failure. Defend the revised dataflow end to end. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“How do closure, iterator, error, reduction, structural-sharing, and effect decisions compose into a readable whole system?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Produce a transformation map that identifies source, shape, ownership, failure, state, and effect boundaries;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;


## Mid-course reconstruction

After Day 5, rebuild the five-module dependency chain without notes. Select the two compiler specimens that changed your model most, rerun them, and explain why the wrong prediction was plausible. Repair every incomplete lab before opening Day 6; later mechanisms assume that the earlier contract is stable.

## Final consolidation

After Day 10, use the [course reference](reference.md) to compress the material, not to relearn it. Complete the [final review](final-review.md) from an empty directory. Then defend LedgerFlow by tracing one successful operation and one adversarial failure through every layer touched by the course.
