# Laboratory 8 — Supervised Child Filter

**Module 48: Child Processes, Stdio, and Supervised Pipelines**

## Product

Implement a direct-spawn filter that streams input to stdin, stages stdout transactionally, drains and bounds stderr, handles spawn failure and nonzero exit, supports AbortSignal, and waits for complete close before deciding commit.

This is an independent mechanism study. It deliberately excludes FlowLedger’s other stages so failures can be attributed to one contract.

## Governing question

> How do you integrate another executable into a Node.js data pipeline without introducing shell ambiguity, unbounded output capture, orphan processes, or incomplete terminal accounting?

## Public surface

- `runChildFilter(options)` returns stdout, bounded stderr, truncation status, and zero exit code. The caller supplies separate `maxStdoutBytes` and `stderrLimit` policies: semantic stdout is rejected when it exceeds its bound, while diagnostic stderr is drained completely and retained only up to its limit.

- Options separate program, argument vector, input bytes, stderr limit, and cancellation signal.

- Command validation rejects an empty program and NUL-containing arguments.

## Required invariants

- No shell command string is constructed.

- Spawn failure is observed before stdio tasks become orphaned.

- Stdin, stdout, and stderr progress concurrently.

- Retained stderr is bounded while the complete stream is drained.

- Semantic stdout is bounded and overflow rejects the operation rather than silently truncating the product.

- Only zero exit with complete stdio produces a successful result.

## Implementation sequence

1. Validate the command boundary.

2. Wait for spawn or error explicitly.

3. Start bounded stdout/stderr collectors and stdin pipeline.

4. Own the close promise before awaiting any one branch.

5. Add nonzero status and signal handling.

6. Add cancellation and verify the child is reaped.

Do not begin by reading the reference. The starter defines the vocabulary and a baseline, not the final design.

## Adversarial cases

- absent executable;

- an argument containing spaces;

- child closes stdin early;

- large stdout and stderr concurrently;

- stdout exactly at and beyond its semantic limit;

- stderr exactly at and beyond the retention limit;

- nonzero exit after producing stdout;

- signal termination;

- abort during active stdio;

Add cases in the smallest order that falsifies an incorrect model. Avoid arbitrary sleeps; use exact chunks, counters, injected callbacks, or explicit state transitions.

## Prohibited shortcuts

- building a shell string from untrusted values;

- using `exec` and accepting its whole-output buffer for unbounded data;

- ignoring stderr;

- committing stdout on stream end alone;

- returning immediately after `kill()` without waiting for close;

A shortcut is prohibited because it removes the mechanism the laboratory exists to teach, not because one implementation style is preferred.

## Completion evidence

1. a process-lifecycle timeline;

2. bounded stderr tests that still allow child completion;

3. nonzero-exit preservation tests;

4. spawn-failure and cancellation tests;

5. an argument-boundary test containing spaces;

## Independent transfer

Design an image-conversion wrapper around a native tool. State argument validation, executable policy, output-size limits, stderr retention, timeout, exit handling, and stage replacement.

Your transfer design must reconstruct the module ledger for the new domain. Renaming the laboratory types is not transfer.

## Process-state table

Build a state table for `created`, `spawning`, `running`, `stdin closed`, `exited`, `stdio drained`, and `reaped`. For normal exit, nonzero exit, signal termination, spawn failure, stdin failure, and cancellation, identify which states are reached and which promise owns the final result. A process exit does not by itself prove that all captured stdout and stderr bytes have been consumed.

Use a child fixture that writes stdout and stderr concurrently, another that exits nonzero after output, and another that ignores input long enough for cancellation to occur. Bound retained stderr while continuing to drain its complete stream; truncation of retained diagnostics must not block the child. Show that arguments containing spaces remain one argument by avoiding a shell. Finally, document the kill boundary honestly: sending a signal requests termination, while observing `close` after complete stdio settlement proves the child has been reaped by this operation.

## Comparing with the reference

After your tests pass, inspect `reference/` and locate the first meaningful difference. Adopt it only when it proves an invariant your design misses; otherwise retain the simpler design.
