# Module 44 Workbook — Async Iteration, Web Streams, and Adapter Boundaries

Complete this file before opening `solutions.md`. Record predictions in writing; a result observed after running code is not a prediction.

## 1. Predict the mechanism

### Early loop exit

Predict what cleanup runs when a consumer breaks from an async generator that has a `finally` block.

### One-shot reuse

Predict the second iteration over a Node Readable that was already consumed to completion.

### Web reader lock

Predict the result of requesting a second default reader before releasing the first.

### Adapter error

A Node Readable errors after conversion to a Web Stream. Identify where the consumer observes the failure.

## 2. Diagnose and repair

### Batch retention

Repair a batching generator that yields the same mutable array and then clears it for reuse.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

### Early-source cleanup

Repair `take` so early termination closes or returns the upstream iterator rather than abandoning it.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

### Repeated conversion

Replace a design that converts Node → Web → Node for every transform with one chosen domain boundary.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

## 3. Focused construction

1. Implement cancellation-aware fixed-size batching.

2. Implement `take` with exact zero, partial, and early-return behavior.

3. Create a repeatable iterable from immutable values.

4. Round-trip byte chunks through Node and Web stream adapters.

5. Add an upstream generator whose `finally` records cleanup.

6. Test errors and early return on both sides of an adapter.

For each construction, add a negative test against the obvious shortcut. Prefer exact byte counts, source indices, or injected operation counts to arbitrary delays.

### Mechanism experiment

Recreate the chapter's extended case in the smallest executable form. Vary at least three conditions drawn from the laboratory's adversarial list:

- batch size zero and negative;

- empty source and final partial batch;

- count zero and count larger than source;

Record which observation changes, which remains stable, and whether the difference belongs to representation, scheduling, capacity, or product semantics.

## 4. Independent laboratory — Async Record Window

Build one-shot and repeatable async sources, cancellation-aware batching and take adapters, and Node/Web Stream round trips with explicit early-return and chunk-ownership tests.

Before implementation, submit:

- the public API and represented data at every boundary;

- the module-specific ledger from the chapter;

- the success and failure state machine;

- exact capacity limits and units;

- tests that distinguish the design from each prohibited shortcut in the laboratory brief.

Build from `starter/`. Open `reference/` only after your own happy-path and adversarial tests pass.

## 5. FlowLedger transfer

Express FlowLedger’s record transforms as async-generator stages where that improves clarity. Preserve pipeline cancellation and keep the byte-to-record trust boundary explicit.

Write a short change record containing:

1. the stage or edge added to FlowLedger;
2. the previous invariant most at risk;
3. the new bound or terminal state;
4. the error and cancellation route;
5. the test that proves chunking or scheduling does not change promised semantics.

## 6. Independent transfer

Design an API that tails a log file as an AsyncIterable of validated records. Explain who owns the FileHandle, what early return does, and whether a second iteration reopens the file.

Produce a small executable proof and a design note. The proof must exercise the difficult boundary directly rather than converting the task into an already bounded in-memory array.

### Review artifact

Complete the module ledger with actual names from your implementation:

- **sequence identity:** Is the value one-shot, repeatable, or a factory that creates a fresh sequence?

- **demand owner:** Who calls `next`, reads, or pulls the next chunk?

- **early stop:** What does `return()` or loop exit do to the upstream resource?

- **error channel:** Does failure reject iteration, error the stream, or both through an adapter?

- **lock state:** Does an adapter acquire an exclusive reader or writer lock?

- **chunk contract:** Are adapters preserving bytes, strings, objects, and ownership semantics?

A row containing “Node handles it” is incomplete. Replace it with the responsible object, promise, event, bound, or publication step.

## 7. Closed-book defense

1. What makes an AsyncIterable one-shot or repeatable?

2. Who owns upstream cleanup after early return?

3. What does a Web Stream lock protect?

4. When is an async generator clearer than a Transform?

Finish by drawing the smallest diagram that captures the module’s owner, retained state, pressure or progress signal, and terminal observation.
