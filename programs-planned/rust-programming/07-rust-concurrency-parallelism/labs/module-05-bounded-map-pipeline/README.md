# Laboratory 65 — Bounded Map Pipeline

**Course 7 · Module 65: Message Passing, Backpressure, and Shutdown**

[Chapter](../../course-book/module-65-message-passing-backpressure-and-shutdown/index.md) · [Workbook](../../course-book/module-65-message-passing-backpressure-and-shutdown/workbook.md) · [BatchWeave guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Message Passing, Backpressure, and Shutdown**: Which values cross ownership boundaries, how is capacity bounded, and which explicit protocol event proves that every sender, receiver, and worker can terminate? The product must make **Model channel operations as ownership transfer rather than shared access** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **channel topology** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

> How do channel topology, capacity, ownership transfer, endpoint lifetime, and stable identity produce bounded work with complete shutdown?

By the end, the answer must be visible in the public API, protocol diagram, failure behavior, causal tests, and explanation—not merely in a successful run.

## Product

Build a finite integer mapping pipeline using a fixed worker set. Work is bounded, results carry source indices, all endpoints have documented owners, and final values remain in input order.

## Product-specific design pressure

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

For **Laboratory 65 — Bounded Map Pipeline**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Working route

1. Read the product contract and run the starter’s baseline checks for **Bounded Map Pipeline**.
2. Draw the smallest **channel topology** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to BatchWeave so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Model channel operations as ownership transfer rather than shared access.
- Choose bounded, zero-capacity, or unbounded channels from an explicit resource and latency policy.
- Draw sender/receiver topology and identify which endpoints are clonable.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 65 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **channel topology**. Defend why your design is simpler than one plausible alternative under the new requirements.
