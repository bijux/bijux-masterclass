# Module 50 Workbook — Integrated Streaming Architecture, Testing, and Independent Change

Complete this file before opening `solutions.md`. Record predictions in writing; a result observed after running code is not a prediction.

## 1. Predict the mechanism

### Cross-layer cancellation

Cancellation arrives while the source is paused on file I/O, the child writes stderr, and the sink waits for capacity. Trace every owner that must settle.

### Digest drift

A gzip stage is moved after the output hash tap. Predict which report field silently changes meaning.

### Late schema failure

Record 500 is domain-invalid after 499 canonical records reached the staged file. Predict visible final and temporary artifacts.

### Post-commit report failure

Rename succeeds and JSON report rendering throws. Classify product state and the correct public error wording.

## 2. Diagnose and repair

### Disconnected owners

Repair an architecture with separate unjoined promises for source, child, and destination.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

### Capacity gap

Find a retained structure not covered by stream high-water marks and assign a product bound.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

### Inconsistent terminal evidence

Replace live counters and event order with authoritative post-completion reconciliation.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

## 3. Focused construction

1. Produce FlowLedger’s complete representation graph.

2. Produce a resource tree and cancellation route.

3. Produce a capacity map including unfinished frames and child stderr.

4. Produce a pre-commit/post-commit failure matrix.

5. Build a chunk-partition and fault-position test generator.

6. Implement one independent feature and update every affected contract surface.

For each construction, add a negative test against the obvious shortcut. Prefer exact byte counts, source indices, or injected operation counts to arbitrary delays.

### Mechanism experiment

Recreate the chapter's extended case in the smallest executable form. Vary at least three conditions drawn from the laboratory's adversarial list:

- one-byte chunks and one complete chunk;

- multibyte text split at every byte;

- line exactly at and beyond the limit;

Record which observation changes, which remains stable, and whether the difference belongs to representation, scheduling, capacity, or product semantics.

## 4. Independent laboratory — Streaming Architecture Audit

Audit and repair an independent NDJSON export system. Produce the representation graph, queue budget, resource ledger, commit matrix, chunk-boundary test set, and an implementation that survives injected failures.

Before implementation, submit:

- the public API and represented data at every boundary;

- the module-specific ledger from the chapter;

- the success and failure state machine;

- exact capacity limits and units;

- tests that distinguish the design from each prohibited shortcut in the laboratory brief.

Build from `starter/`. Open `reference/` only after your own happy-path and adversarial tests pass.

## 5. FlowLedger transfer

Complete FlowLedger, its process-level CLI tests, compatibility fixtures, fault-injection suite, architecture ledger, and final independent rejects-bundle extension.

Write a short change record containing:

1. the stage or edge added to FlowLedger;
2. the previous invariant most at risk;
3. the new bound or terminal state;
4. the error and cancellation route;
5. the test that proves chunking or scheduling does not change promised semantics.

## 6. Independent transfer

Add a resumable import checkpoint to a streaming system. Define what state can be replayed safely, what byte position means after decoding and filtering, and how the checkpoint is committed with the data.

Produce a small executable proof and a design note. The proof must exercise the difficult boundary directly rather than converting the task into an already bounded in-memory array.

### Review artifact

Complete the module ledger with actual names from your implementation:

- **representation graph:** What does data mean on every edge from input bytes to final bytes?

- **resource tree:** Which owner closes each stream, handle, child, iterator, timer, and stage file?

- **capacity map:** Which queue or retained state can grow, in what unit, and to what maximum?

- **failure graph:** Which failures cancel which stages and which evidence survives?

- **commit matrix:** What is visible before, at, and after publication?

- **verification map:** Which test, investigation, or review can falsify each product claim?

A row containing “Node handles it” is incomplete. Replace it with the responsible object, promise, event, bound, or publication step.

## 7. Closed-book defense

1. Which stage owns semantic trust?

2. Which promise owns the complete operation?

3. What is FlowLedger’s publication point?

4. Which claims remain deliberately unmade?

5. How would you add a rejects bundle without false multi-file atomicity?

Finish by drawing the smallest diagram that captures the module’s owner, retained state, pressure or progress signal, and terminal observation.
