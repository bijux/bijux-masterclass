# Module 47 Workbook — Transform Pipelines: Compression, Hashing, and Integrity

Complete this file before opening `solutions.md`. Record predictions in writing; a result observed after running code is not a prediction.

## 1. Predict the mechanism

### Tap placement

Predict how moving a hash tap from before gzip to after gzip changes repeatability and meaning.

### Compression bomb

A 10 KB gzip file expands to 2 GB. Identify which stream thresholds do and do not protect the process.

### Flush timing

Predict why reading a digest before the hash tap’s final flush is a lifecycle error.

### Canonicalization

Two JSON objects have the same fields in different source order. Decide whether source and canonical digests should match.

## 2. Diagnose and repair

### Unnamed digest

Replace one `sha256` field with representation-specific evidence and update verification semantics.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

### Input-only limit

Add an expanded-byte budget to a decompression pipeline that currently limits only compressed input.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

### Premature metadata

Repair a pipeline that publishes digest metadata before the output candidate commits.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

## 3. Focused construction

1. Implement a transparent hash-and-byte-count Transform.

2. Place one tap before gzip and one after gzip.

3. Round-trip compressed data and compare source bytes.

4. Enforce a maximum expanded output.

5. Corrupt compressed bytes and preserve the zlib cause.

6. Return metadata only after complete pipeline settlement.

For each construction, add a negative test against the obvious shortcut. Prefer exact byte counts, source indices, or injected operation counts to arbitrary delays.

### Mechanism experiment

Recreate the chapter's extended case in the smallest executable form. Vary at least three conditions drawn from the laboratory's adversarial list:

- empty source;

- many tiny source chunks;

- incompressible and highly compressible input;

Record which observation changes, which remains stable, and whether the difference belongs to representation, scheduling, capacity, or product semantics.

## 4. Independent laboratory — Compressed Digest Pipeline

Build a gzip pipeline that records source, canonical, and compressed byte counts, computes explicitly named SHA-256 digests, rejects corrupt input, enforces an expanded-byte limit, and publishes metadata only after successful completion.

Before implementation, submit:

- the public API and represented data at every boundary;

- the module-specific ledger from the chapter;

- the success and failure state machine;

- exact capacity limits and units;

- tests that distinguish the design from each prohibited shortcut in the laboratory brief.

Build from `starter/`. Open `reference/` only after your own happy-path and adversarial tests pass.

## 5. FlowLedger transfer

Add optional gzip input and output to FlowLedger, separate raw-input and canonical-output digests, and ensure digest metadata is committed only with the staged output.

Write a short change record containing:

1. the stage or edge added to FlowLedger;
2. the previous invariant most at risk;
3. the new bound or terminal state;
4. the error and cancellation route;
5. the test that proves chunking or scheduling does not change promised semantics.

## 6. Independent transfer

Design a backup verifier for compressed archives. Decide which digests are stored, which representation each covers, and how an expansion limit is enforced during verification.

Produce a small executable proof and a design note. The proof must exercise the difficult boundary directly rather than converting the task into an already bounded in-memory array.

### Review artifact

Complete the module ledger with actual names from your implementation:

- **edge representation:** Are these source, decoded, canonical, compressed, encrypted, or output bytes?

- **transform state:** What window or native state does the transform retain?

- **expansion bound:** What limits decompressed or transformed output independently of input size?

- **digest domain:** Which exact bytes feed each hash?

- **metadata authority:** When may counts and digests be reported as final?

- **integrity claim:** Does the mechanism detect accidents, authenticate an origin, or neither?

A row containing “Node handles it” is incomplete. Replace it with the responsible object, promise, event, bound, or publication step.

## 7. Closed-book defense

1. Which representation does each digest identify?

2. Why does backpressure not stop a compression bomb by total size?

3. What fact does SHA-256 establish without a trusted expected value?

4. When is digest metadata authoritative?

Finish by drawing the smallest diagram that captures the module’s owner, retained state, pressure or progress signal, and terminal observation.
