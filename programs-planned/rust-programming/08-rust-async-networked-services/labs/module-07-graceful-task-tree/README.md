# Laboratory 77 — Graceful Task Tree

This is the independent product for **Course 8, Module 77**. Read the [module chapter](../../course-book/module-77-cancellation-safety-deadlines-and-graceful-shutdown/index.md) and complete its [workbook](../../course-book/module-77-cancellation-safety-deadlines-and-graceful-shutdown/workbook.md) before consulting the reference implementation.

## Learning target

> How can a supervisor stop admission, propagate cancellation, drain within one deadline, abort leftovers, and join every child exactly once?

The completed product must make the answer visible in its types, lifecycle, tests, failure behavior, and explanation. A successful happy-path run is not sufficient.

## Product

Build a small service supervisor with an admission task and dynamic child tasks. Work is classified as completed, failed, panicked, or cancelled. Shutdown is idempotent and progresses through stop-admission, signal, drain, abort, join, and report.

## Why this laboratory exists

The lab isolates lifecycle from network protocols. It makes the difference between sending cancellation and proving terminal completion observable in one controlled product.

## Contract

No child is detached. Repeated shutdown signals start one shutdown transition. The grace period is one absolute deadline. Tasks that finish during grace retain their real outcome. Remaining tasks are aborted and then joined. The final report accounts for every accepted child.

## Required milestones

1. Define the task tree and terminal report.
2. Implement idempotent root cancellation.
3. Stop admission before child drain.
4. Use one grace deadline.
5. Abort leftovers and drain every handle.

## Adversarial cases

- no children
- all finish before shutdown
- domain failure
- panic
- one task ignores cancellation but yields
- grace expiry
- repeated shutdown calls

## Evidence to produce

- a task-tree diagram
- one outcome per accepted child
- paused-time grace tests
- proof that admission is closed first
- join counts after abort

## Prohibited shortcuts

- dropping the JoinSet as the only shutdown step
- one fresh timeout per task
- returning after cancellation token fires
- using wall-clock sleeps for phase placement
- erasing panic and cancellation into one outcome

## Transfer

Transfer the supervisor to an upload service with temporary files. State cleanup for uncommitted, committed, and actively writing uploads.

## Comparing with the reference

Compare phase order and terminal accounting. The reference is stronger only if cancellation intent and completed shutdown are separate observable states.

The `solution/` directory is a reference after independent work, not a sequence of blanks to copy. Compare invariants, task ownership, cancellation behavior, bounds, and tests before comparing line count.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Begin in `starter/`. Do not open `solution/` until the state diagram, failure cases, and transfer design are written or a precise blocker is recorded.

The laboratory is complete when its tests pass and you can answer the governing question without the chapter:

> How can a supervisor stop admission, propagate cancellation, drain within one deadline, abort leftovers, and join every child exactly once?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```
