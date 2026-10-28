# Laboratory 30 — Inspection Platform

This is the independent product for **Course 3, Module 30: Architectural Synthesis**. Read the [module chapter](../../course-book/module-30-architectural-synthesis/index.md) and complete its [workbook](../../course-book/module-30-architectural-synthesis/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> Given a real source of variation, how do you choose among enums, generics, trait objects, closures, functions, and ordinary composition?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Build a separate miniature inspection platform from a product brief only.

It must contain:

- one closed enum variation;
- one generic associated-type boundary;
- one heterogeneous dyn-compatible registry;
- one coherence-safe adapter;
- one short typestate protocol;
- one intentionally concrete collaborator;
- downstream-style compatibility tests;
- an architecture decision record for every polymorphism mechanism.

The domain must differ from Review Engine. Copying names and structure without re-deriving decisions fails transfer.

## Design focus

Start with a variation map before writing code. For each axis, record who chooses the alternative, when the choice is made, whether alternatives must coexist, and what information callers need to retain. Use that analysis to justify one enum, one generic associated-type boundary, one dyn-compatible registry, one local adapter, one short typestate protocol, and one collaborator that remains concrete.

The domain must not imitate Review Engine. Tests must include deterministic behavior, invalid construction, downstream-style use, and one independent extension. Add an architecture note explaining at least three mechanisms you considered and rejected. The lab is complete only when removing any trait, type parameter, box, or marker would violate a stated requirement—and when adding another abstraction would not make the product clearer.

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

> Given a real source of variation, how do you choose among enums, generics, trait objects, closures, functions, and ordinary composition?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Inspection Platform**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
