# Laboratory 5 — Transactional File Sink

**Module 45: Files, File Handles, Paths, and Transactional Replacement**

## Product

Implement a same-directory staged sink that accepts a pipeline writer, synchronizes and closes the candidate, applies a declared overwrite policy, cleans up pre-commit failure, and reports post-commit failure separately.

This is an independent mechanism study. It deliberately excludes FlowLedger’s other stages so failures can be attributed to one contract.

## Governing question

> What does it mean for a file operation to be complete, visible, replaced, durable, and safely owned in a Node.js process?

## Public surface

- `transactionalWrite(destination, source, options)` publishes one complete candidate and returns byte accounting.

- `copyTransactional(source, destination, options)` composes file input with the same publication protocol.

- `replace`, `mode`, and `signal` are explicit options.

## Required invariants

- The final path is not opened for truncating write.

- The stage is created exclusively in the destination directory.

- The candidate stream completes and the file is synchronized before rename.

- No-overwrite policy rejects an existing destination.

- Every pre-commit failure removes the stage best-effort and preserves the prior visible destination.

## Implementation sequence

1. Implement deterministic stage-path construction and exclusive creation.

2. Connect an incremental source to a file WriteStream.

3. Reopen the completed stage for synchronization and close it.

4. Add destination-existence policy.

5. Perform rename as the publication point.

6. Inject failures at write, sync, policy, and rename boundaries.

Do not begin by reading the reference. The starter defines the vocabulary and a baseline, not the final design.

## Adversarial cases

- empty source;

- existing destination in replace and no-replace modes;

- abort during streaming;

- source error after partial candidate bytes;

- unwritable destination directory;

- a stage-name collision;

- cleanup failure after a primary error;

Add cases in the smallest order that falsifies an incorrect model. Avoid arbitrary sleeps; use exact chunks, counters, injected callbacks, or explicit state transitions.

## Prohibited shortcuts

- writing directly to the destination;

- using a predictable shared temporary name;

- claiming a preflight `stat` prevents competing writers;

- considering `finish` equivalent to publication;

- claiming universal crash durability;

A shortcut is prohibited because it removes the mechanism the laboratory exists to teach, not because one implementation style is preferred.

## Completion evidence

1. a publication-state diagram;

2. preservation tests with a pre-existing destination;

3. orphan-stage checks after injected failure;

4. an explicit durability and concurrency non-guarantee;

5. a checkpoint-writer transfer design;

## Independent transfer

Design a checkpoint writer for a long-running import. Decide whether checkpoints replace one file, append immutable versions, or update a directory manifest, and state the crash-recovery evidence for the choice.

Your transfer design must reconstruct the module ledger for the new domain. Renaming the laboratory types is not transfer.

## Publication matrix

Construct a failure matrix with rows for validation, stage creation, write, flush, file synchronization, close, replacement, and optional parent-directory synchronization. For every row, record whether the old destination remains visible, whether a stage may remain, whether the new destination may already be visible, and which error the caller receives. The matrix must distinguish a pre-publication failure from a post-replacement durability failure; those outcomes require different recovery messages.

Run the implementation against an existing destination, a missing parent, an injected write failure, and a replacement failure. Verify that the stage resides in the destination directory and that unrelated files are never removed during cleanup. State the concurrency boundary honestly: a same-directory temporary replacement protects ordinary single-writer publication from partial contents, but it does not provide a distributed lock or a portable cross-process compare-and-swap. The laboratory is complete only when its documentation claims no stronger atomicity or durability than the implementation establishes.

## Comparing with the reference

After your tests pass, inspect `reference/` and locate the first meaningful difference. Adopt it only when it proves an invariant your design misses; otherwise retain the simpler design.
