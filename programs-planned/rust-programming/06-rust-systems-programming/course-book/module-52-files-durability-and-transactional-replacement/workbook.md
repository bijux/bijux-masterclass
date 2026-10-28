# Workbook — Module 52: Files, Durability, and Transactional Replacement

[Chapter](index.md) · [Laboratory](../../labs/module-02-atomic-archive-store/README.md) · [FrameVault guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Files, Durability, and Transactional Replacement** has become a usable model rather than remembered vocabulary. Its governing question is: *What has actually been promised after a file operation succeeds: bytes written, buffers flushed, data synchronized, a name replaced, or a recoverable durable state?* Preserve your first prediction and record decisive facts in a **durability timeline**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 51 — Binary Data Contracts: Bytes, Endianness, and Checked Parsing that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **What has actually been promised after a file operation succeeds: bytes written, buffers flushed, data synchronized, a name replaced, or a recoverable durable state?**
3. Draw the smallest **durability timeline** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

### Prediction 1

`write` returns `Ok(12)` for a 20-byte buffer. Has the operation failed?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 2

`BufWriter::flush` succeeds. Are bytes durable on storage media?

For **Prediction 2**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 3

The destination is truncated before encoding finishes. What guarantee is already lost?

For **Prediction 3**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 4

A temp file is created in `/tmp` and renamed to another filesystem. What can happen?

For **Prediction 4**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 5

The program checks `destination.exists()` and then chooses a create mode. Is the check authoritative?

For **Prediction 5**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 6

`read_dir` succeeds initially. Can a later iterator item still be an error?

For **Prediction 6**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 7

The temp file is synchronized and renamed. Is directory-entry durability universally established?

For **Prediction 7**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 8

Cleanup of the temp file fails after a write error. Which error should be primary?

For **Prediction 8**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

## Part 2 — Diagnose and repair

### Boundary trace

Draw the replacement state machine from encoded candidate through sibling reservation, partial writes, flush, file synchronization, close, rename, parent-directory synchronization, and cleanup. Mark the commit point and classify every failure as pre-commit, committed-with-follow-up-failure, or cleanup failure.

For **Files, Durability, and Transactional Replacement**, choose table columns that expose the actual states rather than copying a generic checklist. Every row must name the owner, the fact established, the fact still delegated, the visible failure effect, and the component responsible for cleanup or rollback.

### Weak repairs to reject

For each prediction, identify a superficially convenient repair that violates the module contract. Reject at least these module-specific shortcuts:

- truncating the destination before the complete candidate exists;
- assuming one `write` call consumes the whole buffer;
- treating `flush` as storage durability;
- staging on a different filesystem;
- using `exists` as an authoritative precondition;
- replacing the primary write error with a later cleanup error;

Replace each with the smallest repair that preserves the requirement and state what evidence would distinguish the two designs.

## Part 3 — Focused exercises

### Construction 1

Draw the file-update state machine and mark the commit point.

Required evidence: Include encoded, temp-created, writing, synchronized, renamed, and cleanup states.

### Construction 2

Implement `write_all_checked` over a writer that intentionally accepts three bytes per call.

Required evidence: Prove forward progress and handle `WriteZero`.

### Construction 3

Design an error type that preserves operation, path, and underlying `io::Error`.

Required evidence: Avoid erasing which stage failed.

### Construction 4

State the strongest honest guarantee of same-directory temp-and-rename.

Required evidence: Separate failure atomicity before rename, name replacement, and crash durability.

### Construction 5

Transfer the method to updating a configuration snapshot.

Required evidence: Decide whether full replacement, append-only journal, or direct update fits its size and recovery needs.

### Interleaved reasoning pass

1. For **Distinguish read, write, flush, data synchronization, metadata synchronization, and directory-entry durability**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the durability timeline.
2. For **Handle short reads and writes through the `Read` and `Write` contracts**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the durability timeline.
3. For **Use `OpenOptions` to make creation and truncation policy explicit**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the durability timeline.
4. For **Design a same-directory temporary-file replacement with cleanup on failure**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the durability timeline.

5. Identify one guarantee from an earlier course that a careless implementation of **Files, Durability, and Transactional Replacement** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Atomic Archive Store](../../labs/module-02-atomic-archive-store/README.md) from the starter. Freeze the public boundary and adversarial cases before opening the solution. Produce the evidence required by the lab:

- a state diagram from old destination through staged candidate and committed replacement;
- a failure table covering create, write, flush, file sync, rename, and parent sync;
- tests that inspect destination bytes after representative pre-commit failures;
- proof that the temporary file is created in the destination directory with `create_new`;
- a qualified success claim for each supported target family.

Also identify one feature deliberately excluded because it would enlarge the trust, portability, concurrency, or unsafe proof surface.

### Laboratory acceptance trace

Before opening the reference implementation for **Atomic Archive Store**, record:

- the public behavior that demonstrates **Distinguish read, write, flush, data synchronization, metadata synchronization, and directory-entry durability**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Implement the matching increment from the [capstone engineering guide](../capstone.md). Add one regression test that fails if this module’s central contract is removed.

### Capstone invariant trace

For the Module 52 FrameVault increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Answer these questions without the chapter:

1. What exact state remains after each pre-commit failure?
2. What operation makes the new pathname authoritative?
3. Which durability claims are target- or filesystem-conditioned?
4. How are temporary-name collision and cleanup ownership handled?

End by naming the strongest honest claim after success and one claim the implementation deliberately does not make.

### Independent transfer

Implement replacement for a small configuration file while preserving the old valid file on every failure before installation. Write a state table for candidate reservation, write, flush, synchronization, close, install, and directory synchronization. Inject one failure at each boundary through a small I/O trait or closure seam. For each failure, assert destination contents and temporary-file cleanup. End with a written claim that distinguishes visibility, crash consistency, and durability.

### Closed-book defense

In five minutes, answer “What has actually been promised after a file operation succeeds: bytes written, buffers flushed, data synchronized, a name replaced, or a recoverable durable state?” using the **durability timeline**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside FrameVault. A list of APIs without the deciding relationship is incomplete.
