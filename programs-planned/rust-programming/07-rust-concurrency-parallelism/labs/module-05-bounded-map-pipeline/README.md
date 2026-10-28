# Laboratory 65 — Bounded Map Pipeline

This is the independent product for **Course 7, Module 65**. Read the [module chapter](../../course-book/module-65-message-passing-backpressure-and-shutdown/index.md) and complete its [workbook](../../course-book/module-65-message-passing-backpressure-and-shutdown/workbook.md) before consulting the reference implementation.

## Learning target

> How do channel topology, capacity, ownership transfer, endpoint lifetime, and stable identity produce bounded work with complete shutdown?

By the end, the answer must be visible in the public API, protocol diagram, failure behavior, causal tests, and explanation—not merely in a successful run.

## Product

Build a finite integer mapping pipeline using a fixed worker set. Work is bounded, results carry source indices, all endpoints have documented owners, and final values remain in input order.

## Why this laboratory exists

The lab forces the limitations of the standard MPSC receiver to become architectural decisions. It can use per-worker bounded channels with a dispatcher or a shared queue from Module 64, but it must prove no work/result wait cycle.

## Contract

Accept a nonzero, explicitly bounded worker count and bounded input. Square values with checked arithmetic and return per-item success or overflow. Close work after submission, drain terminal results, join every worker, reject duplicate or missing result indices, and render by source order.

## Required milestones

1. Draw endpoint topology.
2. Choose a bounded work strategy and state capacity.
3. Send indexed owned work.
4. Receive typed indexed outcomes and reject duplicates.
5. Close endpoints and join all workers on every path.

## Adversarial cases

- zero workers
- worker count above the product limit
- zero inputs
- capacity one
- overflow
- worker completion reverse order
- failed send after worker loss
- out-of-range result index
- retained sender clone
- duplicate result injection

## Evidence to produce

- endpoint owner/drop table
- capacity argument
- deterministic assembly tests
- join evidence
- disconnect-cause analysis

## Prohibited shortcuts

- cloning the standard receiver
- unbounded work without input bound
- magic shutdown values
- holding a lock during send
- assuming disconnect means all jobs succeeded

## Transfer

Transfer the topology to format-specific document workers. Unsupported formats must become typed outcomes rather than failed sends or silent drops.

## Comparing with the reference

Compare endpoint accounting and terminal reconciliation. The first valid result for an index must remain intact when a duplicate arrives; protocol detection must not mutate already accepted product truth. The reference may use a different topology, but it must make capacity, receiver ownership, sender drops, and complete joins easier—not harder—to prove.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/` and do not open `solution/` until the protocol, adversarial cases, and transfer are implemented or a precise blocker is written.

The laboratory is complete when the tests and documented failure paths pass, and you can answer the governing question without the chapter:

> How do channel topology, capacity, ownership transfer, endpoint lifetime, and stable identity produce bounded work with complete shutdown?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```
