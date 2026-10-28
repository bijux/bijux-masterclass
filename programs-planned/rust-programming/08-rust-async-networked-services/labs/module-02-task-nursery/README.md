# Laboratory 72 — Task Nursery

This is the independent product for **Course 8, Module 72**. Read the [module chapter](../../course-book/module-72-tokio-runtimes-tasks-and-structured-async-lifecycles/index.md) and complete its [workbook](../../course-book/module-72-tokio-runtimes-tasks-and-structured-async-lifecycles/workbook.md) before consulting the reference implementation.

## Learning target

> How can one async owner start dynamic child work, preserve source identity, cancel by policy, and observe every success, failure, panic, and cancellation before returning?

The completed product must make the answer visible in its types, lifecycle, tests, failure behavior, and explanation. A successful happy-path run is not sufficient.

## Product

Build a bounded task nursery. It accepts indexed async jobs, supports complete-all and fail-fast modes, preserves stable source order in the final report, cancels siblings after the first domain failure in fail-fast mode, and drains every task to a terminal outcome.

## Why this laboratory exists

The lab turns `JoinSet` from an API into a lifecycle owner. It distinguishes domain failure from task panic and cancellation, and it rejects the common repair of returning after the first failed join.

## Contract

At most 32 jobs are accepted. Every accepted source index appears exactly once in the report. Fail-fast stops admitting no new work because all jobs are known at start, signals siblings, and still drains them. No task remains detached after `run` returns.

## Required milestones

1. Define indexed job and terminal outcome types.
2. Spawn all bounded jobs under one cancellation tree.
3. Classify nested domain and join outcomes.
4. Implement complete-all and fail-fast policies.
5. Reconstruct source order after completion-order collection.

## Adversarial cases

- zero jobs
- reverse completion order
- one domain failure
- one panic
- several tasks completing as cancellation propagates
- input above the job bound

## Evidence to produce

- a task-tree ledger
- stable source-order tests
- panic and domain failure kept distinct
- proof that every accepted job has one terminal outcome
- a test that no child completes after nursery return

## Prohibited shortcuts

- dropping join handles
- returning on the first error
- sorting by completion time
- using sleeps as the only schedule control
- converting every failure into one string

## Transfer

Transfer the nursery to a DNS probe group in which one failed host does not cancel others, while an operator cancellation stops all probes. Define the changed policy explicitly.

## Comparing with the reference

Compare terminal accounting and ownership first. A reference that collects values but erases panics or leaves children active is weaker even when its successful output matches.

The `solution/` directory is a reference after independent work, not a sequence of blanks to copy. Compare invariants, task ownership, cancellation behavior, bounds, and tests before comparing line count.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Begin in `starter/`. Do not open `solution/` until the state diagram, failure cases, and transfer design are written or a precise blocker is recorded.

The laboratory is complete when its tests pass and you can answer the governing question without the chapter:

> How can one async owner start dynamic child work, preserve source identity, cancel by policy, and observe every success, failure, panic, and cancellation before returning?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```
