# Laboratory 61 — Thread Handoff Matrix

This is the independent product for **Course 7, Module 61**. Read the [module chapter](../../course-book/module-61-threads-schedules-send-sync-and-race-freedom/index.md) and complete its [workbook](../../course-book/module-61-threads-schedules-send-sync-and-race-freedom/workbook.md) before consulting the reference implementation.

## Learning target

> How do ownership transfer, `Send`/`Sync`, joins, and stable identity turn independent thread execution into one complete deterministic operation?

By the end, the answer must be visible in the public API, protocol diagram, failure behavior, causal tests, and explanation—not merely in a successful run.

## Product

Build a parallel digest service over owned byte payloads. Each payload has a stable source index. The service spawns finite work, joins every thread, returns digests in source order, and reports every panic after completing the join phase.

## Why this laboratory exists

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

> How do ownership transfer, `Send`/`Sync`, joins, and stable identity turn independent thread execution into one complete deterministic operation?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```
