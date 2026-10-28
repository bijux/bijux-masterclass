# Laboratory 62 — Scoped Slice Analysis

This is the independent product for **Course 7, Module 62**. Read the [module chapter](../../course-book/module-62-structured-threads-scopes-joins-and-panic-boundaries/index.md) and complete its [workbook](../../course-book/module-62-structured-threads-scopes-joins-and-panic-boundaries/workbook.md) before consulting the reference implementation.

## Learning target

> How can finite threads borrow and mutate disjoint regions of an enclosing slice while keeping every child, panic, and reference inside one parent operation?

By the end, the answer must be visible in the public API, protocol diagram, failure behavior, causal tests, and explanation—not merely in a successful run.

## Product

Build a scoped analyzer with two operations: summarize a borrowed `&[i32]` into count, sum, minimum, and maximum; and normalize a borrowed `&mut [i64]` in disjoint chunks. No source collection may be cloned.

## Why this laboratory exists

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

> How can finite threads borrow and mutate disjoint regions of an enclosing slice while keeping every child, panic, and reference inside one parent operation?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```
