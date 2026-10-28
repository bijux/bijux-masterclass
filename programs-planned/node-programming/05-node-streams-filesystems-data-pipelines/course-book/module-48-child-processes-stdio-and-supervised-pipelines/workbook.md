# Module 48 Workbook — Child Processes, Stdio, and Supervised Pipelines

Complete this file before opening `solutions.md`. Record predictions in writing; a result observed after running code is not a prediction.

## 1. Predict the mechanism

### Shell interpolation

Predict how a filename containing spaces and shell metacharacters differs between an argument vector and a concatenated shell command.

### Undrained stderr

A child writes enough stderr to fill its pipe before reading stdin. Predict the parent/child wait cycle.

### Exit before close

Predict why zero `exit` status can occur before all stdout data has been observed.

### Spawn failure

Identify which promises and streams exist when executable creation fails with ENOENT.

## 2. Diagnose and repair

### Sequential stdio

Repair a parent that writes all stdin, then reads stdout, then reads stderr.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

### Unbounded diagnostics

Keep stderr useful while bounding retained bytes and continuing to drain the pipe.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

### Premature commit

Repair a staged-output operation that renames after stdout ends without checking child close and status.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

## 3. Focused construction

1. Spawn directly with program and argument array.

2. Wait for successful spawn before starting collectors that would otherwise reject unowned.

3. Pump stdin and drain stdout/stderr concurrently.

4. Bound retained stderr while counting total stderr bytes.

5. Kill the child on pipeline failure or AbortSignal.

6. Commit output only after close with zero status and successful streams.

For each construction, add a negative test against the obvious shortcut. Prefer exact byte counts, source indices, or injected operation counts to arbitrary delays.

### Mechanism experiment

Recreate the chapter's extended case in the smallest executable form. Vary at least three conditions drawn from the laboratory's adversarial list:

- absent executable;

- an argument containing spaces;

- child closes stdin early;

Record which observation changes, which remains stable, and whether the difference belongs to representation, scheduling, capacity, or product semantics.

## 4. Independent laboratory — Supervised Child Filter

Implement a direct-spawn filter that streams input to stdin, stages stdout transactionally, drains and bounds stderr, handles spawn failure and nonzero exit, supports AbortSignal, and waits for complete close before deciding commit.

Before implementation, submit:

- the public API and represented data at every boundary;

- the module-specific ledger from the chapter;

- the success and failure state machine;

- exact capacity limits and units;

- tests that distinguish the design from each prohibited shortcut in the laboratory brief.

Build from `starter/`. Open `reference/` only after your own happy-path and adversarial tests pass.

## 5. FlowLedger transfer

Add FlowLedger’s through command. It must preserve raw byte backpressure, reject nonzero child status, retain bounded stderr, abort the direct child, and commit stdout only after process and stream success agree.

Write a short change record containing:

1. the stage or edge added to FlowLedger;
2. the previous invariant most at risk;
3. the new bound or terminal state;
4. the error and cancellation route;
5. the test that proves chunking or scheduling does not change promised semantics.

## 6. Independent transfer

Design an image-conversion wrapper around a native tool. State argument validation, executable policy, output-size limits, stderr retention, timeout, exit handling, and stage replacement.

Produce a small executable proof and a design note. The proof must exercise the difficult boundary directly rather than converting the task into an already bounded in-memory array.

### Review artifact

Complete the module ledger with actual names from your implementation:

- **invocation:** Which executable, argument vector, environment, and working directory are used?

- **stdin owner:** Who writes, closes, and aborts child input?

- **stdout owner:** Who drains and stages child output?

- **stderr policy:** How much diagnostic data is retained and what happens beyond the limit?

- **termination:** How are spawn error, exit code, signal, close, and abort distinguished?

- **commit rule:** Which combination of stdio completion and child status authorizes publication?

A row containing “Node handles it” is incomplete. Replace it with the responsible object, promise, event, bound, or publication step.

## 7. Closed-book defense

1. Why is `shell: false` the default safe architecture?

2. What is the difference between `exit` and `close`?

3. How can bounded retention still drain unbounded stderr?

4. Which terminal facts jointly authorize stdout publication?

Finish by drawing the smallest diagram that captures the module’s owner, retained state, pressure or progress signal, and terminal observation.
