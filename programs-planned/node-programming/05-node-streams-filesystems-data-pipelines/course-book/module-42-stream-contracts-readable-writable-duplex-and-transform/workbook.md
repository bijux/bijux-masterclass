# Module 42 Workbook — Stream Contracts: Readable, Writable, Duplex, and Transform

Complete this file before opening `solutions.md`. Record predictions in writing; a result observed after running code is not a prediction.

## 1. Predict the mechanism

### Duplex half-close

A socket-like duplex receives EOF from its peer but the local side has not called `end()`. Predict readable and writable terminal state separately.

### Mixed consumption

A readable has a `data` listener and is then consumed with `for await`. Predict why the ownership model becomes unclear even when a small example appears to work.

### Transform callback timing

A transform stores a reference to an incoming mutable chunk, calls its callback, and reads the chunk later. Predict the corruption risk.

### Event trace

Rank `readable end`, `transform finish`, `writable finish`, `close`, and pipeline settlement by the product facts they establish.

## 2. Diagnose and repair

### One completion authority

Repair a function that returns when its source emits `end` even though the destination can still fail.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

### One consumer

Replace mixed `data` events and async iteration with one primary consumer and a separate non-retaining state observer.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

### Callback exactly once

Repair a custom Transform that both throws and later invokes its callback on the same input.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

## 3. Focused construction

1. Implement `ByteCounter` as a transparent Transform and prove it does not alter bytes.

2. Create a collecting Writable that copies chunks before retaining them.

3. Record terminal events from source, transform, and sink without using their order as the sole success contract.

4. Run the same graph with empty input and multiple chunks.

5. Inject a transform error and confirm the pipeline owner destroys the remaining stages.

6. Explain which stream state properties are observations rather than commands.

For each construction, add a negative test against the obvious shortcut. Prefer exact byte counts, source indices, or injected operation counts to arbitrary delays.

### Mechanism experiment

Recreate the chapter's extended case in the smallest executable form. Vary at least three conditions drawn from the laboratory's adversarial list:

- empty source;

- one chunk and many chunks;

- a zero-length chunk;

Record which observation changes, which remains stable, and whether the difference belongs to representation, scheduling, capacity, or product semantics.

## 4. Independent laboratory — Stream State Observatory

Build instrumented Readable, Writable, and Transform implementations that record state transitions, queue lengths, terminal events, and the difference between end, finish, close, error, and destroy.

Before implementation, submit:

- the public API and represented data at every boundary;

- the module-specific ledger from the chapter;

- the success and failure state machine;

- exact capacity limits and units;

- tests that distinguish the design from each prohibited shortcut in the laboratory brief.

Build from `starter/`. Open `reference/` only after your own happy-path and adversarial tests pass.

## 5. FlowLedger transfer

Define FlowLedger’s byte-mode and object-mode boundaries. Add transparent counting transforms and a single completion authority for each linear pipeline.

Write a short change record containing:

1. the stage or edge added to FlowLedger;
2. the previous invariant most at risk;
3. the new bound or terminal state;
4. the error and cancellation route;
5. the test that proves chunking or scheduling does not change promised semantics.

## 6. Independent transfer

Design a Duplex that accepts commands as objects and emits encoded response bytes. Specify separate modes, high-water-mark units, and terminal ownership.

Produce a small executable proof and a design note. The proof must exercise the difficult boundary directly rather than converting the task into an already bounded in-memory array.

### Review artifact

Complete the module ledger with actual names from your implementation:

- **role:** Is this value readable, writable, duplex, transforming, or only observing?

- **unit:** Does one chunk represent bytes, decoded strings, or domain objects?

- **consumption mode:** Will the reader use `pipe`, events, `read`, or async iteration—and only one primary mode?

- **queue state:** What is buffered on the readable side and what is queued on the writable side?

- **terminal state:** Which of `end`, `finish`, `close`, `error`, or destruction applies to each side?

- **owner:** Which scope constructs, connects, destroys, and awaits the complete graph?

A row containing “Node handles it” is incomplete. Replace it with the responsible object, promise, event, bound, or publication step.

## 7. Closed-book defense

1. Why can `finish` be true while the product is not yet committed?

2. What is the difference between a Duplex and two unrelated streams?

3. When does object mode change the meaning of `highWaterMark`?

4. Why is a custom stream implementation a protocol obligation?

Finish by drawing the smallest diagram that captures the module’s owner, retained state, pressure or progress signal, and terminal observation.
