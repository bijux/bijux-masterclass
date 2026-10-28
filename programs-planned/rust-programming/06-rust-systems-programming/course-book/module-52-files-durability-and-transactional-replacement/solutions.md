# Reasoned Solutions — Module 52: Files, Durability, and Transactional Replacement

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-02-atomic-archive-store/README.md) · [FrameVault guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 52: Files, Durability, and Transactional Replacement**. Compare the reasoning against this question: *What has actually been promised after a file operation succeeds: bytes written, buffers flushed, data synchronized, a name replaced, or a recoverable durable state?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Prediction analysis

### Prediction 1

**Problem.** `write` returns `Ok(12)` for a 20-byte buffer. Has the operation failed?

**Reasoned answer.** No. Partial writes are permitted. The caller must continue with the unwritten suffix or use `write_all`.

### Prediction 2

**Problem.** `BufWriter::flush` succeeds. Are bytes durable on storage media?

**Reasoned answer.** Not necessarily. Flush only moves buffered data to the underlying writer; synchronization is a separate request and still target-dependent.

### Prediction 3

**Problem.** The destination is truncated before encoding finishes. What guarantee is already lost?

**Reasoned answer.** The previous valid value has been destroyed before the new value is ready.

### Prediction 4

**Problem.** A temp file is created in `/tmp` and renamed to another filesystem. What can happen?

**Reasoned answer.** Rename can fail across filesystem boundaries. Same-directory staging avoids this common mismatch.

### Prediction 5

**Problem.** The program checks `destination.exists()` and then chooses a create mode. Is the check authoritative?

**Reasoned answer.** No. Another actor can change the path between check and use. Attempt the desired operation atomically where supported.

### Prediction 6

**Problem.** `read_dir` succeeds initially. Can a later iterator item still be an error?

**Reasoned answer.** Yes. Directory iteration can encounter errors after construction.

### Prediction 7

**Problem.** The temp file is synchronized and renamed. Is directory-entry durability universally established?

**Reasoned answer.** No. Some targets require directory synchronization and filesystem semantics still matter.

### Prediction 8

**Problem.** Cleanup of the temp file fails after a write error. Which error should be primary?

**Reasoned answer.** The write error. Cleanup failure can be attached as context but must not replace the cause that aborted the save.

## Construction guidance

### Commit point

The destination must remain untouched until the rename operation. Every earlier state is private staging.

### Short writes

Loop over the remaining suffix, treat zero progress as `WriteZero`, and preserve the original error.

### Error context

Use an operation enum or specific variants such as `CreateTemp`, `WriteTemp`, `SyncTemp`, and `Replace` with owned paths.

### Honest guarantee

The protocol avoids exposing a partially written destination before rename. It does not by itself prove power-loss durability on every target.

### Configuration transfer

Small complete snapshots favor replacement; very large or high-frequency stores may need a journal whose recovery algorithm is part of the format.

## Boundary-trace reference

A strong solution trace for this module must draw the replacement state machine from encoded candidate through sibling reservation, partial writes, flush, file synchronization, close, rename, parent-directory synchronization, and cleanup. Mark the commit point and classify every failure as pre-commit, committed-with-follow-up-failure, or cleanup failure. It should reveal the earliest point at which an invalid assumption would become observable and the unique owner responsible for cleanup or rollback.

## Weak repairs to reject

Reject solutions built around these shortcuts:

- truncating the destination before the complete candidate exists;
- assuming one `write` call consumes the whole buffer;
- treating `flush` as storage durability;
- staging on a different filesystem;
- using `exists` as an authoritative precondition;
- replacing the primary write error with a later cleanup error;

A principled repair makes the missing fact explicit in a type, checked operation, state transition, safety contract, platform qualification, or foreign-call contract. It does not merely move the assumption to a less visible line.

## Commit-state proof

Write the operation as an explicit state machine:

```text
NoTemp
  -> TempCreated
  -> CandidateWritten
  -> TempFlushed
  -> TempSynced
  -> TempClosed
  -> NameInstalled
  -> DirectorySynced
```

Before `NameInstalled`, failure means the previous destination remains authoritative and temporary cleanup is best effort. After `NameInstalled`, the new pathname is visible; a later directory-sync error cannot honestly be reported as “nothing changed.” Returning a distinct post-commit error preserves that fact.

| Transition | Resource owner | Failure result |
|---|---|---|
| create temporary file | store operation | retry a collision with a new bounded candidate name |
| write and flush | open file handle | keep old destination; remove temporary file if possible |
| file synchronization | open file handle | old destination remains authoritative |
| rename/install | operating system | platform-specific replacement semantics decide the result |
| parent-directory synchronization | parent directory handle | new name may already be installed; durability remains uncertain |

## Counterexample clinic

“Write to a temporary file and rename it” is not yet a durability contract. A temporary file in another filesystem can make rename non-atomic or impossible. A reused temporary pathname can truncate another process’s candidate. A successful rename can still be followed by a directory-sync failure. Windows and Unix do not provide identical overwrite behavior through every standard-library route.

The principled implementation therefore states the supported replacement policy, creates the candidate beside the destination, uses exclusive creation, closes the file before installation where required, and returns enough state for the caller to distinguish pre-commit from post-commit uncertainty.

## Completion check

Use the chapter’s readiness statement as the first threshold:

You are ready when you can name the commit point, distinguish buffering from synchronization, explain why the old file survives every pre-commit failure, and qualify every portability claim about rename and durability.

Then perform this destructive regression check: inject a failure before and after the rename and verify that the destination-state assertions distinguish the two sides of the commit point. The resulting failure should be caught for the causal reason predicted in the workbook, not by an unrelated panic or syntax error.

## Deep reasoning and transfer

### Decisive model

> What has actually been promised after a file operation succeeds: bytes written, buffers flushed, data synchronized, a name replaced, or a recoverable durable state?

Build a **durability timeline**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Distinguish read, write, flush, data synchronization, metadata synchronization, and directory-entry durability.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Handle short reads and writes through the `Read` and `Write` contracts.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Use `OpenOptions` to make creation and truncation policy explicit.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Design a same-directory temporary-file replacement with cleanup on failure.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **State the portability limits of `rename`, file locking, and durable replacement.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Distinguish read, write, flush, data synchronization, metadata synchronization, and directory-entry durability.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the durability timeline.

### Reference implementation comparison

For [Atomic Archive Store](../../labs/module-02-atomic-archive-store/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In FrameVault, Module 52 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Files, Durability, and Transactional Replacement**, which relationship decides this question: “What has actually been promised after a file operation succeeds: bytes written, buffers flushed, data synchronized, a name replaced, or a recoverable durable state?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to FrameVault?
