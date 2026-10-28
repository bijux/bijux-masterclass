# Laboratory 61 — Thread Handoff Matrix

**Course 7 · Module 61: Threads, Schedules, Send, Sync, and Race Freedom**

[Chapter](../../course-book/module-61-threads-schedules-send-sync-and-race-freedom/index.md) · [Workbook](../../course-book/module-61-threads-schedules-send-sync-and-race-freedom/workbook.md) · [BatchWeave guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Threads, Schedules, Send, Sync, and Race Freedom**: What may cross a thread boundary, what may be shared through a reference, and which correctness problems remain after Rust has ruled out data races? The product must make **Distinguish concurrency, parallelism, scheduling, interleaving, data races, and broader race conditions** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **thread ownership map** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

> How do ownership transfer, `Send`/`Sync`, joins, and stable identity turn independent thread execution into one complete deterministic operation?

By the end, the answer must be visible in the public API, protocol diagram, failure behavior, causal tests, and explanation—not merely in a successful run.

## Product

Build a parallel digest service over owned byte payloads. Each payload has a stable source index. The service spawns finite work, joins every thread, returns digests in source order, and reports every panic after completing the join phase.

## Product-specific design pressure

The first concurrency lab deliberately avoids locks and channels. It tests whether you can remove shared mutation, derive auto-trait requirements, and treat join handles as resources before later mechanisms add more ways to wait.

## Contract

Accept at most 32 payloads. Move each payload into exactly one worker. Return one FNV-1a digest or one panic outcome per source index. The public function must join all handles even when more than one worker panics. Completion order is unspecified; rendered result order is source order.

## Required milestones

1. Freeze the public result and panic model.
2. Complete the `Send`/`Sync` matrix for every public type.
3. Move indexed payloads into workers and retain all handles.
4. Join all workers and assemble by index.
5. Add controlled panic and varied-duration tests.

## Adversarial cases

- zero payloads
- one payload
- worker completion in reverse source order
- two worker panics
- maximum accepted payload count
- input above the accepted bound

## Evidence to produce

- a thread ledger
- a `Send`/`Sync` derivation matrix
- tests proving every handle is joined after panic
- stable-order tests independent of completion
- an explicit thread-count bound

## Prohibited shortcuts

- one shared mutex-protected input vector
- detaching handles
- sorting by digest rather than source index
- cloning payloads solely to satisfy ownership
- returning after the first panic

## Transfer

Transfer the design to image thumbnails whose rendering profile is immutable and shared. Decide whether the profile should be cloned, moved, or placed in `Arc`, and justify the choice from ownership rather than size alone.

## Comparing with the reference

Compare handle ownership and failure aggregation first. The reference is stronger only if every child reaches a join, stable indices survive, and the thread bound is explicit. A shorter implementation that returns on the first panic is weaker.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/` and do not open `solution/` until the protocol, adversarial cases, and transfer are implemented or a precise blocker is written.

The laboratory is complete when the tests and documented failure paths pass, and you can answer the governing question without the chapter:

For **Laboratory 61 — Thread Handoff Matrix**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Working route

1. Read the product contract and run the starter’s baseline checks for **Thread Handoff Matrix**.
2. Draw the smallest **thread ownership map** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to BatchWeave so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Distinguish concurrency, parallelism, scheduling, interleaving, data races, and broader race conditions.
- Derive whether an owned value may move into a thread from its `Send` obligation.
- Derive whether a shared reference may cross a thread boundary from the referent’s `Sync` obligation.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 61 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **thread ownership map**. Defend why your design is simpler than one plausible alternative under the new requirements.
