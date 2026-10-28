# Laboratory 62 — Scoped Slice Analysis

**Course 7 · Module 62: Structured Threads: Scopes, Joins, and Panic Boundaries**

[Chapter](../../course-book/module-62-structured-threads-scopes-joins-and-panic-boundaries/index.md) · [Workbook](../../course-book/module-62-structured-threads-scopes-joins-and-panic-boundaries/workbook.md) · [BatchWeave guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Structured Threads: Scopes, Joins, and Panic Boundaries**: How can borrowed data, thread lifetime, completion, and panic handling be enclosed by one parent operation rather than leaked into the rest of the program? The product must make **Explain the real meaning of a `T: 'static` bound and why owned values can satisfy it** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **join and panic tree** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

> How can finite threads borrow and mutate disjoint regions of an enclosing slice while keeping every child, panic, and reference inside one parent operation?

By the end, the answer must be visible in the public API, protocol diagram, failure behavior, causal tests, and explanation—not merely in a successful run.

## Product

Build a scoped analyzer with two operations: summarize a borrowed `&[i32]` into count, sum, minimum, and maximum; and normalize a borrowed `&mut [i64]` in disjoint chunks. No source collection may be cloned.

## Product-specific design pressure

The product isolates lifetime structure from queueing and shared-state coordination. It requires you to derive partition boundaries before spawning and to explain why parent reuse is valid immediately after scope exit.

## Contract

Worker count must be nonzero, may exceed element count, and is capped by an explicit product limit so a tiny slice cannot request an arbitrary number of operating-system threads. Empty immutable input returns `None`; empty mutable input is a no-op. Every child is explicitly joined when the operation can report panic. Static chunking and its load-balance limitation must be documented.

## Required milestones

1. Define summary and error types.
2. Write a chunk-size function that never yields zero for nonempty input.
3. Implement borrowed immutable summary with `thread::scope`.
4. Implement mutable normalization through `chunks_mut`.
5. Add uneven-partition and parent-reuse tests.

## Adversarial cases

- empty input
- workers equal zero
- worker count above the product limit
- more workers than values
- uneven division
- negative minimum value and saturating absolute conversion
- child panic in an injected analysis closure

## Evidence to produce

- a lifetime diagram
- a disjoint-borrow proof
- complete join behavior
- parent reuse after scope exit
- a static-load-balance limitation

## Prohibited shortcuts

- cloning the source
- leaking data to satisfy `static`
- placing the slice behind a mutex
- creating overlapping ranges by index
- allowing a scoped handle to escape

## Transfer

Transfer the method to row-wise image normalization. Then add an all-or-nothing requirement and explain why disjoint in-place mutation must be replaced by owned candidate bands or a prior validation phase.

## Comparing with the reference

Compare lifetime and partition diagrams before numerical output. The reference should have no `Arc`, mutex, or source clone. Check how it handles worker counts above input length and whether every explicit handle is joined.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/` and do not open `solution/` until the protocol, adversarial cases, and transfer are implemented or a precise blocker is written.

The laboratory is complete when the tests and documented failure paths pass, and you can answer the governing question without the chapter:

For **Laboratory 62 — Scoped Slice Analysis**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Working route

1. Read the product contract and run the starter’s baseline checks for **Scoped Slice Analysis**.
2. Draw the smallest **join and panic tree** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to BatchWeave so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Explain the real meaning of a `T: 'static` bound and why owned values can satisfy it.
- Use `thread::scope` to borrow immutable and disjoint mutable data safely.
- Partition mutable state before spawning rather than attempt to prove disjointness after overlap exists.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 62 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **join and panic tree**. Defend why your design is simpler than one plausible alternative under the new requirements.
