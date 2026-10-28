# Module 45 Workbook — Files, File Handles, Paths, and Transactional Replacement

Complete this file before opening `solutions.md`. Record predictions in writing; a result observed after running code is not a prediction.

## 1. Predict the mechanism

### Open handle after rename

A file is opened, its pathname is renamed, and then the handle is read. Predict whether the handle necessarily becomes invalid.

### Destination precheck

Two writers both call `stat` and see no destination before either renames. Predict why the precheck is not multi-writer exclusion.

### Post-rename sync failure

Rename succeeds and a later durability step fails. Classify the error as pre-commit or post-commit.

### Whole-file helper

A product allows 10 MB files. Decide whether `readFile` is inherently wrong and state the missing evidence.

## 2. Diagnose and repair

### Direct overwrite

Repair a normalizer that opens the final path with truncation before validation completes.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

### Double handle ownership

Repair code that both manually closes a FileHandle and lets a stream auto-close the same descriptor.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

### Overstated durability

Rewrite an API contract that claims “atomic and durable on every filesystem” after a same-directory rename.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

## 3. Focused construction

1. Generate an exclusive same-directory stage path.

2. Stream source bytes into the stage and count accepted bytes.

3. Await stream completion, reopen or retain the handle for synchronization, then close it.

4. Implement explicit replace and no-overwrite policies.

5. Remove the stage on every pre-commit failure.

6. Write tests for failure during write, sync, destination policy, and rename.

For each construction, add a negative test against the obvious shortcut. Prefer exact byte counts, source indices, or injected operation counts to arbitrary delays.

### Mechanism experiment

Recreate the chapter's extended case in the smallest executable form. Vary at least three conditions drawn from the laboratory's adversarial list:

- empty source;

- existing destination in replace and no-replace modes;

- abort during streaming;

Record which observation changes, which remains stable, and whether the difference belongs to representation, scheduling, capacity, or product semantics.

## 4. Independent laboratory — Transactional File Sink

Implement a same-directory staged sink that accepts a pipeline writer, synchronizes and closes the candidate, applies a declared overwrite policy, cleans up pre-commit failure, and reports post-commit failure separately.

Before implementation, submit:

- the public API and represented data at every boundary;

- the module-specific ledger from the chapter;

- the success and failure state machine;

- exact capacity limits and units;

- tests that distinguish the design from each prohibited shortcut in the laboratory brief.

Build from `starter/`. Open `reference/` only after your own happy-path and adversarial tests pass.

## 5. FlowLedger transfer

Build FlowLedger’s staged output owner. The final pathname must change only after the entire stream pipeline succeeds and the candidate file is synchronized and closed.

Write a short change record containing:

1. the stage or edge added to FlowLedger;
2. the previous invariant most at risk;
3. the new bound or terminal state;
4. the error and cancellation route;
5. the test that proves chunking or scheduling does not change promised semantics.

## 6. Independent transfer

Design a checkpoint writer for a long-running import. Decide whether checkpoints replace one file, append immutable versions, or update a directory manifest, and state the crash-recovery evidence for the choice.

Produce a small executable proof and a design note. The proof must exercise the difficult boundary directly rather than converting the task into an already bounded in-memory array.

### Review artifact

Complete the module ledger with actual names from your implementation:

- **namespace:** Which pathname is looked up, created, replaced, or removed?

- **open identity:** Which `FileHandle` or stream owns the opened file object?

- **candidate state:** Where are incomplete bytes kept before publication?

- **overwrite policy:** Must an existing destination be preserved, rejected, or replaced?

- **publication point:** Which rename or manifest update makes the candidate visible?

- **durability claim:** What does synchronization establish in the intended filesystem environment?

A row containing “Node handles it” is incomplete. Replace it with the responsible object, promise, event, bound, or publication step.

## 7. Closed-book defense

1. What does writable finish prove for a file stream?

2. Why must the stage be in the destination directory?

3. Which failure is no longer safely reversible after rename?

4. When is a whole-file helper the clearer design?

Finish by drawing the smallest diagram that captures the module’s owner, retained state, pressure or progress signal, and terminal observation.
