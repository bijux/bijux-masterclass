# Laboratory 23 — Coherence Adapters

This is the independent product for **Course 3, Module 23: Coherence and Implementation Ownership**. Read the [module chapter](../../course-book/module-23-coherence-and-implementation-ownership/index.md) and complete its [workbook](../../course-book/module-23-coherence-and-implementation-ownership/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> Which crate owns the right to create an implementation, and how can a public design preserve coherence without giving up adaptation?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Integrate two foreign-style model types with two local formatting and validation contracts.

Requirements:

- one local extension trait over a foreign-like type;
- one newtype implementing an external standard trait;
- one intentionally rejected blanket implementation with a written overlap proof;
- a sealed internal capability and public read-only extension surface;
- compile-fail evidence for a forbidden downstream implementation;
- a semver note describing the implementation space reserved by each blanket impl.

## Design focus

Begin from an implementation Rust forbids: a foreign formatting trait for a foreign vendor type. Do not treat the orphan rule as an obstacle to bypass. Identify which semantic behavior belongs to your crate, introduce a validated local newtype, and put the implementation there. Add an extension trait only for behavior that should be callable on the foreign value without changing its identity.

The lab must include one narrowly bounded blanket implementation and a written overlap analysis. Show which future implementations that blanket consumes. Add a sealed marker only where downstream implementation would freeze an internal classification; leave intended extension points open. Tests must cover newtype validation, formatting, adapter behavior, and method resolution. A wrapper that merely forwards every vendor method without adding an invariant does not satisfy the lab.

## Working route

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/`, add the first adversarial test before the design-changing repair, and complete the workbook’s transfer problem before reading the reference implementation.

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

> Which crate owns the right to create an implementation, and how can a public design preserve coherence without giving up adaptation?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Coherence Adapters**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
