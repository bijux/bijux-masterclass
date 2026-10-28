# Module 43 Workbook — Backpressure, Pipeline, Completion, and Failure

Complete this file before opening `solutions.md`. Record predictions in writing; a result observed after running code is not a prediction.

## 1. Predict the mechanism

### False write result

Predict whether the chunk associated with a `false` return must be written again after `drain`.

### Object-mode threshold

A writable has `highWaterMark: 16` in object mode and each object contains a 10 MB Buffer. Predict the memory implication.

### Abort during drain

A producer waits only for `drain` while the destination is destroyed due to cancellation. Predict the liveness defect.

### Pipeline rejection

A middle transform fails after the source has queued more bytes. Predict which stages pipeline destroys and what the caller must still own.

## 2. Diagnose and repair

### Manual copy loop

Repair a loop that calls `write` continuously and returns after `end()` without awaiting final completion.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

### Semantic memory claim

Replace “memory is bounded by highWaterMark” with a capacity ledger covering record size, diagnostics, transform state, and destination queues.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

### Abortable wait

Repair a `drain` wait so destination error, close, and AbortSignal all settle the owner.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

## 3. Focused construction

1. Implement `writeWithBackpressure` over an AsyncIterable source.

2. Count chunks, bytes, and pressure waits without retaining all chunks.

3. Create a deliberately slow sink with a tiny high-water mark.

4. Abort while waiting for capacity and prove the owner rejects promptly.

5. Inject a sink error after an exact chunk count.

6. Compare the manual loop with `pipeline` and state why one is chosen.

For each construction, add a negative test against the obvious shortcut. Prefer exact byte counts, source indices, or injected operation counts to arbitrary delays.

### Mechanism experiment

Recreate the chapter's extended case in the smallest executable form. Vary at least three conditions drawn from the laboratory's adversarial list:

- empty input;

- a chunk larger than the high-water mark;

- many tiny chunks;

Record which observation changes, which remains stable, and whether the difference belongs to representation, scheduling, capacity, or product semantics.

## 4. Independent laboratory — Backpressure Copy Engine

Implement a bounded copy engine with a deliberately slow Writable, pressure observations, AbortSignal support, pipeline ownership, and evidence that memory does not grow with source length.

Before implementation, submit:

- the public API and represented data at every boundary;

- the module-specific ledger from the chapter;

- the success and failure state machine;

- exact capacity limits and units;

- tests that distinguish the design from each prohibited shortcut in the laboratory brief.

Build from `starter/`. Open `reference/` only after your own happy-path and adversarial tests pass.

## 5. FlowLedger transfer

Create FlowLedger’s pipeline owner. Connect source, counting, decoding, transformation, serialization, optional compression, and staged output under one AbortSignal and one terminal report.

Write a short change record containing:

1. the stage or edge added to FlowLedger;
2. the previous invariant most at risk;
3. the new bound or terminal state;
4. the error and cancellation route;
5. the test that proves chunking or scheduling does not change promised semantics.

## 6. Independent transfer

Design a network uploader whose request body is a Readable and whose response acknowledgment is the semantic commit. Separate write pressure, pipeline completion, HTTP response, and final product success.

Produce a small executable proof and a design note. The proof must exercise the difficult boundary directly rather than converting the task into an already bounded in-memory array.

### Review artifact

Complete the module ledger with actual names from your implementation:

- **producer pace:** What operation creates the next chunk or item?

- **pressure signal:** Which return value or promise indicates that capacity is exhausted?

- **resume condition:** What exact event or settlement permits production to continue?

- **queue unit:** Is the threshold measured in bytes, chunks, or objects?

- **semantic bounds:** Which record, expansion, history, or diagnostic limits exist beyond stream queues?

- **teardown:** How does one failure or abort reach every stage and every pending wait?

A row containing “Node handles it” is incomplete. Replace it with the responsible object, promise, event, bound, or publication step.

## 7. Closed-book defense

1. What does a false `write()` return mean about the current chunk?

2. Why does backpressure not bound one logical record?

3. What promise owns completion in a linear pipeline?

4. How can a wait for `drain` become permanently stuck?

Finish by drawing the smallest diagram that captures the module’s owner, retained state, pressure or progress signal, and terminal observation.
