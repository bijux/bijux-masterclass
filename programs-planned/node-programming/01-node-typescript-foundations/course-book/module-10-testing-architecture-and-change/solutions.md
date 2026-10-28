# Module 10 Solutions

## A. Evidence

Transition: unit test. Import side effect: integration test importing the public entry in an isolated process if necessary. Corrupted JSON: persistence fixture test. Help contract: process test. Union exhaustiveness: type-check investigation plus runtime cases. Ordering: exact canonical-output persistence test. Save-before-success: application test with a rejecting repository and process/integration test.

## B. Faults

A fixed-clock application test catches global time. Identity and order tests catch mutating sort. Permission/corruption persistence tests catch the empty-state fallback. A rejecting-save test catches premature success. Package export tests catch internal exposure. Process stream assertions catch stdout/stderr confusion.

## C. Change plan

The plan must begin with domain ownership. For labels, decide normalization, duplicates, ordering, maximum count, and whether old V1 files imply empty labels or require V2. Only then alter grammar and storage.

## D. Process harness

Use `spawn` or `execFile` with the Node executable and compiled entry path. Set a temporary environment variable for the data path. Capture buffers, wait for close, and return both spawn errors and process exit information explicitly.

## E–F. Design notes

Reading Ledger should share reasoning patterns, not names or file copies. The final StudyLedger feature must preserve promise observation and candidate-before-save behavior.

## G. Completion answer

The strongest response identifies a concrete unproved boundary—for example Windows rename behavior or concurrent writers—and names an appropriate cross-platform test, platform contract review, or later-course redesign rather than making an unsupported claim.

## Extended solution

Search case behavior belongs in a pure query test; duplicate IDs belong in codec fixtures; help streams and status need a process test; immutable transitions need retained-value domain tests; export shape needs a module integration or structural check; save-before-success needs an application test with a rejecting fake plus one process smoke test.

A `reopen` feature requires a new command, a domain transition with explicit legal source states, timestamp policy, help text, application dispatch, and tests. V1 can already encode planned sessions, so no new field is required if reopening discards terminal detail under a documented policy. If history must be retained, the schema must change. Storage mechanics and unrelated query implementations need no change when their contracts remain valid.

The final reconstruction order should follow dependency direction: package/toolchain, domain, pure parsing and rendering, codec, storage, application, process adapter, then evidence at increasing distance. Open non-contracts include concurrent writers, crash durability, and hostile-size memory bounds.
