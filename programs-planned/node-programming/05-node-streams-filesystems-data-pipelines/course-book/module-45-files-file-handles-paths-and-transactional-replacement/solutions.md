# Module 45 Reasoned Solutions — Files, File Handles, Paths, and Transactional Replacement

These are reasoning standards, not a mandate to copy one implementation. A different design is correct when it proves the same public behavior, ownership, bound, failure, and completion contracts.

## 1. Prediction reasoning

### Open handle after rename

The decisive relationship is **pathnames and open files are different identities**. A pathname is a lookup route in a filesystem namespace. Opening it yields a handle to an object that can remain valid even if the pathname is renamed or removed, depending on the platform. Rechecking metadata by pathname after opening can describe a different object. When identity matters, perform the operation through the owned FileHandle and avoid treating repeated path lookups as one atomic fact.

For the stated case, do not stop at the visible value. Trace the source owner, any alias or queue, and the next terminal transition. A crash or transform error can expose a truncated or semantically invalid file. The smallest useful experiment isolates this one rule and avoids unrelated configuration or type errors.
### Destination precheck

The decisive relationship is **whole-file helpers trade simplicity for retention**. readFile and writeFile are excellent when product limits guarantee the complete value fits comfortably in memory. They are not morally inferior to streams. The correct choice follows the size contract, not fashion. A whole-file helper can simplify atomic validation and error handling; a stream is justified when input may exceed the desired retained-memory bound or when processing should begin before the entire value arrives.

For the stated case, do not stop at the visible value. Trace the source owner, any alias or queue, and the next terminal transition. The namespace can change between checks and use; open errors remain authoritative. The smallest useful experiment isolates this one rule and avoids unrelated configuration or type errors.
### Post-rename sync failure

The decisive relationship is **file completion has layers**. A write callback or writable finish means Node accepted the bytes through the file descriptor. FileHandle.sync asks the operating system to synchronize file data and metadata required for retrieval. Renaming a staged file changes pathname visibility. Synchronizing the parent directory is a further durability step on systems where directory entries require it. These operations have different failure points and should not be compressed into “saved”.

For the stated case, do not stop at the visible value. Trace the source owner, any alias or queue, and the next terminal transition. Resource release becomes duplicated and errors are easily lost. The smallest useful experiment isolates this one rule and avoids unrelated configuration or type errors.
### Whole-file helper

The decisive relationship is **staged replacement preserves the previous visible candidate**. The usual single-writer pattern creates a unique temporary file beside the destination, writes and validates the complete candidate, flushes and synchronizes it, closes it, then renames it over or into the final path according to policy. Before rename, the old destination remains visible. On failure, remove the stage. After rename, a later error must be reported as post-commit because rolling back may be unsafe or impossible.

For the stated case, do not stop at the visible value. Trace the source owner, any alias or queue, and the next terminal transition. Directory-entry durability and filesystem behavior require a narrower claim. The smallest useful experiment isolates this one rule and avoids unrelated configuration or type errors.

## 2. Repair reasoning

### Direct overwrite

A principled repair begins with: **State the maximum input or output size and choose whole-file or streaming I/O accordingly.** The repair must keep incremental operation and the original product behavior. It should introduce the missing validation, owner, bound, or state transition instead of using `as`, collecting the complete source, swallowing an error, or deleting cancellation.

The acceptance test should fail against the weak design for the exact reason named in the prompt. After repair, the owning promise must settle only after the relevant resource or stage reaches its documented terminal state.
### Double handle ownership

A principled repair begins with: **Name the scope that owns each FileHandle or file stream.** The repair must keep incremental operation and the original product behavior. It should introduce the missing validation, owner, bound, or state transition instead of using `as`, collecting the complete source, swallowing an error, or deleting cancellation.

The acceptance test should fail against the weak design for the exact reason named in the prompt. After repair, the owning promise must settle only after the relevant resource or stage reaches its documented terminal state.
### Overstated durability

A principled repair begins with: **Separate candidate completion, synchronization, visibility, and durability claims.** The repair must keep incremental operation and the original product behavior. It should introduce the missing validation, owner, bound, or state transition instead of using `as`, collecting the complete source, swallowing an error, or deleting cancellation.

The acceptance test should fail against the weak design for the exact reason named in the prompt. After repair, the owning promise must settle only after the relevant resource or stage reaches its documented terminal state.

## 3. Focused construction review

A strong submission makes the module’s difficult relationship visible in function boundaries and tests. For this module, review the construction in this order:

1. State the maximum input or output size and choose whole-file or streaming I/O accordingly.

2. Name the scope that owns each FileHandle or file stream.

3. Separate candidate completion, synchronization, visibility, and durability claims.

4. Choose no-overwrite, replace-existing, or versioned-output policy explicitly.

5. Place the stage beside the destination and create it exclusively.

6. Test failure before write, during write, during sync, before rename, and after rename.

Use deterministic fault injection. Exact byte, item, write, line, or lifecycle counts identify the causal boundary more clearly than timers.

Treat counters as evidence only when categories are disjoint and satisfy a stated conservation relationship.

## 4. Laboratory acceptance — Transactional File Sink

The laboratory is complete only when all of these invariants are supported by executable evidence:

- The final path is not opened for truncating write.
- The stage is created exclusively in the destination directory.
- The candidate stream completes and the file is synchronized before rename.
- No-overwrite policy rejects an existing destination.
- Every pre-commit failure removes the stage best-effort and preserves the prior visible destination.

The reference is one possible proof. Compare the first meaningful difference and keep your simpler design when it establishes the same invariants. Do not import abstraction without a requirement.

## 5. FlowLedger transfer

Build FlowLedger’s staged output owner. The final pathname must change only after the entire stream pipeline succeeds and the candidate file is synchronized and closed.

Confirm that representation names, limits, causal errors, cancellation, accounting, CLI text, and process tests describe one feature. A passing unit test does not repair a stale public contract.

## 6. Independent transfer standard

Design a checkpoint writer for a long-running import. Decide whether checkpoints replace one file, append immutable versions, or update a directory manifest, and state the crash-recovery evidence for the choice.

A strong answer identifies the external authority, validates before retention or allocation, states the owner of every live resource, and names the exact event that changes visible product state. It also states at least one intentionally unsupported guarantee.

## 7. Defense standard

Defend the design in both directions: map each product claim to its mechanism and evidence, then map each Node event or return value to the narrower fact it proves.

Replace “the stream handled it” with representation, owner, bound, and terminal state.
