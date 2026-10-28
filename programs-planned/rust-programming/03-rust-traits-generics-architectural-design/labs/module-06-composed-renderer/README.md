# Laboratory 26 — Composed Renderer

This is the independent product for **Course 3, Module 26: Composition and OOP-Style Design Without Inheritance**. Read the [module chapter](../../course-book/module-26-composition-and-oop-style-design-without-inheritance/index.md) and complete its [workbook](../../course-book/module-26-composition-and-oop-style-design-without-inheritance/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> How do you obtain encapsulation, substitution, and reusable behavior through composition rather than inheritance?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Build a report-rendering system with two base formats and two optional wrappers.

Requirements:

- the report domain has no formatting trait methods;
- base formats implement one narrow formatter contract;
- signature and line-number behavior use composition;
- one static composition path and one runtime-selected path are demonstrated;
- a closed enum alternative is implemented for comparison;
- tests prove wrappers preserve base errors and deterministic ordering;
- the design memo rejects an inheritance-shaped hierarchy.

## Design focus

Build the renderer from components with distinct reasons to change: content selection, formatting strategy, destination adaptation, and optional decoration. Use delegation to forward stable behavior and decorators to add behavior in a documented order. Do not create a base-class-shaped trait with protected hooks or a single object that owns every responsibility.

Tests must prove order-sensitive decoration, adapter correctness, and substitutability of at least two strategies. Include a failure-producing destination so that error ownership remains visible. Document which components are generic, which are concrete, and whether any run-time erasure is actually required. A design that boxes every collaborator or mirrors inheritance vocabulary without a product need fails the lab even when output is correct.

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

> How do you obtain encapsulation, substitution, and reusable behavior through composition rather than inheritance?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Composed Renderer**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
