# Module 49 Workbook — Multi-Stage Dataflow, Fan-Out, and Commit Coordination

Complete this file before opening `solutions.md`. Record predictions in writing; a result observed after running code is not a prediction.

## 1. Predict the mechanism

### Slow required branch

Two sinks must receive every chunk; one is ten times slower. Predict the permitted producer rate and queue behavior.

### Advisory metrics failure

A metrics listener throws after a record commits. Decide whether the primary export should fail and justify the authority classification.

### Sequential renames

Three staged files are renamed one after another. List visible states after each rename.

### Completion-order report

Branches finish in different orders across runs. Predict how appending results on completion affects deterministic output.

## 2. Diagnose and repair

### Uncoordinated pipes

Repair source piping to two required sinks without one shared completion and failure owner.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

### Generic side-output event

Replace a single EventEmitter mechanism used for required rejects, metrics, and audit authority with explicit classes and policies.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

### False transaction claim

Design a versioned bundle or manifest-last protocol for three output files.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

## 3. Focused construction

1. Write one chunk to every required destination while respecting each pressure signal.

2. End and await every destination on source exhaustion.

3. Destroy all required branches on one failure.

4. Track chunks and bytes without schedule-dependent presentation.

5. Assert a record conservation equation.

6. Model a manifest-last multi-file publication protocol.

For each construction, add a negative test against the obvious shortcut. Prefer exact byte counts, source indices, or injected operation counts to arbitrary delays.

### Mechanism experiment

Recreate the chapter's extended case in the smallest executable form. Vary at least three conditions drawn from the laboratory's adversarial list:

- zero destinations;

- one fast and one slow branch;

- a branch returning false on the first write;

Record which observation changes, which remains stable, and whether the difference belongs to representation, scheduling, capacity, or product semantics.

## 4. Independent laboratory — Coordinated Fan-Out Writer

Build a required two-sink writer that respects both destinations’ pressure, propagates one branch failure to the complete operation, tracks visible-byte conservation, and demonstrates a versioned-bundle commit protocol.

Before implementation, submit:

- the public API and represented data at every boundary;

- the module-specific ledger from the chapter;

- the success and failure state machine;

- exact capacity limits and units;

- tests that distinguish the design from each prohibited shortcut in the laboratory brief.

Build from `starter/`. Open `reference/` only after your own happy-path and adversarial tests pass.

## 5. FlowLedger transfer

Finalize FlowLedger reports and conservation equations. Keep the main output as the sole committed file, return digest and accounting metadata only after commit, and document how a future multi-file bundle would be versioned.

Write a short change record containing:

1. the stage or edge added to FlowLedger;
2. the previous invariant most at risk;
3. the new bound or terminal state;
4. the error and cancellation route;
5. the test that proves chunking or scheduling does not change promised semantics.

## 6. Independent transfer

Design an export that produces data.ndjson, rejects.ndjson, and manifest.json. Choose a publication protocol and give the visible-artifact state after each possible failure.

Produce a small executable proof and a design note. The proof must exercise the difficult boundary directly rather than converting the task into an already bounded in-memory array.

### Review artifact

Complete the module ledger with actual names from your implementation:

- **branch class:** Is the branch authoritative, required derivative, advisory, or debugging-only?

- **delivery rule:** Must every item reach every branch, or can observation be lossy?

- **pressure join:** Which branch determines when the producer may continue?

- **failure propagation:** Does one branch failure cancel siblings and upstream?

- **publication unit:** Is one path committed, several files staged, or an immutable bundle published by a pointer?

- **conservation:** Which equations prove every record and byte reached exactly one permitted outcome?

A row containing “Node handles it” is incomplete. Replace it with the responsible object, promise, event, bound, or publication step.

## 7. Closed-book defense

1. Why does the slowest required branch control progress?

2. Which side outputs may be lossy?

3. Why are sequential renames not one atomic commit?

4. How does stable identity restore deterministic reporting?

Finish by drawing the smallest diagram that captures the module’s owner, retained state, pressure or progress signal, and terminal observation.
