# Reasoned solutions — Module 52: Files, Durability, and Transactional Replacement

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the FrameVault engineering guide](../capstone.md)

Use these solutions after freezing your own analysis. The code result matters less than locating the first broken contract and identifying who owns the repair.

Read each answer as a boundary proof: identify the missing fact, the component able to establish it, and the state that must remain unchanged when the proof fails.

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
