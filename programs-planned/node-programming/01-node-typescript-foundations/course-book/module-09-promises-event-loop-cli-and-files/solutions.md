# Module 9 Solutions

## A. Ordering

The synchronous trace is `start`, `end`. Microtasks then run in enqueue order: `microtask`, `promise`. The timer runs later. Exact interactions with I/O phases and recursively queued tasks require the deeper event-loop model in Course 4.

## B. Ownership

`forEach` ignores every save promise. Sequential repair uses `for...of` with `await`. Concurrent repair uses `await Promise.all(paths.map(save))`. `notify().catch(console.error)` observes rejection but intentionally detaches success from notification; that is valid only if the product says notification is best effort and logging itself is sufficient.

## C. Grammar

The specification must state duplicate-option behavior, order, `--` handling, missing values, and cross-field constraints before implementation. A typed command is returned only after all token checks pass.

## D. Missing file

Catch unknown, check a narrow `code === 'ENOENT'` predicate, and return the empty initial value only then. Wrap other I/O errors with cause. Let JSON/validation failures retain their own category.

## E–F. Design notes

File indexing may use `Promise.all` only after enforcing a small entry bound. Sort results after completion. StudyLedger’s process tests should observe file output only after the child exits successfully.

## G. Readiness answer

Promises settle once and require an observer. Microtasks run after the current stack. Starting before awaiting creates overlapping lifetimes. `Promise.all` owns results but does not cancel inputs. Abort is cooperative. `exitCode` allows normal event-loop completion. Missing-file policy must not swallow unrelated errors.

## Extended solution

Promise reactions are predictably after the current stack. A zero-delay timer and an unrelated I/O completion should not be assigned a universal order without controlling when each becomes ready. The file-index repair uses either sequential `for...of` or `Promise.all` over mapped promises; both own every started operation but have different concurrency.

Save must be awaited before success is produced. `void` merely discards the promise value. Rejection should reach the application shell and create a nonzero status.

The command grammar rejects duplicate singleton options, unknown options, extra positionals, and missing values. A note beginning with `--` needs a documented escape such as `--note=--text` if supported by the parser or a `--` terminator policy; the course CLI keeps the simple quoted-value contract and tests the chosen behavior. Process tests observe status, both streams, and persisted state across invocations.
