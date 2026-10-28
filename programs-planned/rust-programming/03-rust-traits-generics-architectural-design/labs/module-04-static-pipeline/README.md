# Laboratory 24 — Static Pipeline

This is the independent product for **Course 3, Module 24: Static Polymorphism and Opaque Types**. Read the [module chapter](../../course-book/module-24-static-polymorphism-and-opaque-types/index.md) and complete its [workbook](../../course-book/module-24-static-polymorphism-and-opaque-types/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> When should concrete types remain visible to the compiler, and how can an API hide implementation details without erasing static guarantees?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Build a statically composed validation pipeline whose source code selects concrete validator types.

Requirements:

- a generic `Validate` contract with associated input and error types;
- a pipeline that composes two concrete validators without trait objects;
- minimal bounds at method level;
- an opaque iterator returned from the report view;
- a map operation that consumes the pipeline and changes one strategy type;
- a design memo explaining why runtime heterogeneity is not required.

## Design focus

Construct a three-stage pipeline whose stage types remain visible to the compiler. Each stage has one responsibility and the weakest sufficient bounds. Use argument-position `impl Trait` only when callers do not need to name the parameter type and return-position `impl Trait` only when one hidden concrete return type is produced on every branch. Do not introduce `Box<dyn Trait>` merely to make unlike branch types agree.

Record the item type and error type after every stage. Add tests for success, early failure, and a stage that borrows configuration. Include one compile-fail example where two branches attempt to return different opaque concrete types. Then repair the design with either an enum, one shared adapter shape, or a trait object, and justify the choice from the product requirement rather than from syntax convenience.

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

> When should concrete types remain visible to the compiler, and how can an API hide implementation details without erasing static guarantees?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Static Pipeline**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
