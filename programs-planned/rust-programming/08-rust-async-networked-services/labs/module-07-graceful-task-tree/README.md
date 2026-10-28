# Laboratory 77 — Graceful Task Tree

**Course 8 · Module 77: Cancellation Safety, Deadlines, and Graceful Shutdown**

[Chapter](../../course-book/module-77-cancellation-safety-deadlines-and-graceful-shutdown/index.md) · [Workbook](../../course-book/module-77-cancellation-safety-deadlines-and-graceful-shutdown/workbook.md) · [JobWire guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Cancellation Safety, Deadlines, and Graceful Shutdown**: When an async operation loses a race, exceeds a deadline, or receives shutdown, what state survives, which effects may already have committed, and how does every task reach a terminal joined state? The product must make **Derive cancellation behavior from future-owned state and external side effects** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **cancellation and shutdown trace** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

> How can a supervisor stop admission, propagate cancellation, drain within one deadline, abort leftovers, and join every child exactly once?

The completed product must make the answer visible in its types, lifecycle, tests, failure behavior, and explanation. A successful happy-path run is not sufficient.

## Product

Build a small service supervisor with an admission task and dynamic child tasks. Work is classified as completed, failed, panicked, or cancelled. Shutdown is idempotent and progresses through stop-admission, signal, drain, abort, join, and report.

## Product-specific design pressure

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

For **Laboratory 77 — Graceful Task Tree**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Working route

1. Read the product contract and run the starter’s baseline checks for **Graceful Task Tree**.
2. Draw the smallest **cancellation and shutdown trace** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to JobWire so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Derive cancellation behavior from future-owned state and external side effects.
- Interpret `tokio::select!` as dropping nonselected branch futures.
- Distinguish cancellation safety from memory safety.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 77 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **cancellation and shutdown trace**. Defend why your design is simpler than one plausible alternative under the new requirements.
