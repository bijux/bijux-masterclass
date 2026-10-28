# Laboratory 28 — Boundary Ports

This is the independent product for **Course 3, Module 28: Boundary Traits and Adapters**. Read the [module chapter](../../course-book/module-28-boundary-traits-and-adapters/index.md) and complete its [workbook](../../course-book/module-28-boundary-traits-and-adapters/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> How should a Rust program adapt external data, effects, closures, and foreign types without contaminating its core model?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Build a small inspection service with a domain core independent from input and output mechanisms.

Requirements:

- one consumer-owned source port with associated item/error types;
- one generic in-memory implementation and one text adapter;
- a closure adapter for a local policy;
- a behavioral fake with controlled failure injection;
- reusable contract tests;
- no trait for the concrete orchestrator unless a real second implementation exists;
- a boundary map showing where conversion and error translation occur.

## Design focus

Design narrow ports around application needs rather than around a database, HTTP client, or framework. The core service should depend on behavior such as loading a record, checking a policy, and publishing a result—not on transport-specific types. Provide a production adapter, an in-memory fake, and one closure adapter where a named trait implementation would add no semantic value.

Use `From` only for infallible, unsurprising, value-preserving conversion; use `TryFrom` when validation can fail; use `AsRef` for cheap reference views; and use `Borrow` only when equality, ordering, and hashing semantics agree. Apply the same contract tests to every port implementation. Reject a repository trait that simply copies every method from an external client, and reject an abstraction that has only one caller and no realistic substitute.

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

> How should a Rust program adapt external data, effects, closures, and foreign types without contaminating its core model?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Boundary Ports**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
