# Laboratory 72 — Task Nursery

**Course 8 · Module 72: Tokio Runtimes, Tasks, and Structured Async Lifecycles**

[Chapter](../../course-book/module-72-tokio-runtimes-tasks-and-structured-async-lifecycles/index.md) · [Workbook](../../course-book/module-72-tokio-runtimes-tasks-and-structured-async-lifecycles/workbook.md) · [JobWire guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Tokio Runtimes, Tasks, and Structured Async Lifecycles**: Once futures are understood as poll-driven state machines, how should a runtime own, schedule, observe, cancel, and finish the tasks that execute them? The product must make **Distinguish a runtime, worker thread, task, future, reactor, and blocking pool** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **task ownership tree** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

> How can one async owner start dynamic child work, preserve source identity, cancel by policy, and observe every success, failure, panic, and cancellation before returning?

The completed product must make the answer visible in its types, lifecycle, tests, failure behavior, and explanation. A successful happy-path run is not sufficient.

## Product

Build a bounded task nursery. It accepts indexed async jobs, supports complete-all and fail-fast modes, preserves stable source order in the final report, cancels siblings after the first domain failure in fail-fast mode, and drains every task to a terminal outcome.

## Product-specific design pressure

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

For **Laboratory 72 — Task Nursery**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Working route

1. Read the product contract and run the starter’s baseline checks for **Task Nursery**.
2. Draw the smallest **task ownership tree** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to JobWire so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Distinguish a runtime, worker thread, task, future, reactor, and blocking pool.
- Explain the `Send + 'static` requirements of ordinary multi-threaded task spawning.
- Derive when a task should borrow through an enclosing async scope versus own cloned or moved data.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 72 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **task ownership tree**. Defend why your design is simpler than one plausible alternative under the new requirements.
