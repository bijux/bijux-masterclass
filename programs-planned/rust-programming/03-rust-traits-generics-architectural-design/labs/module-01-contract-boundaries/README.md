# Laboratory 21 — Contract Boundaries

This is the independent product for **Course 3, Module 21: Traits as Behavioral Contracts**. Read the [module chapter](../../course-book/module-21-traits-as-behavioral-contracts/index.md) and complete its [workbook](../../course-book/module-21-traits-as-behavioral-contracts/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> What behavior truly belongs in a shared contract, and which laws must every implementation preserve?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Build a small pricing library for `Book`, `CourseLicense`, and `SupportPlan`.

The starter intentionally duplicates concrete pricing calls. Your task is not “add a trait.” First identify which operations are genuinely substitutable.

### Product requirements

- each product can produce a nonnegative base price in cents;
- promotional adjustment is a separate policy selected by the caller;
- invoice rendering must not become part of the pricing contract;
- a caller can price any product through one generic function;
- shared law tests verify that price values never exceed a declared domain limit;
- invalid discount percentages are rejected at construction.

### Required design record
- one narrow behavioral trait;
- one operation left as an inherent method or free function, with justification;
- a `where` clause containing only body-required bounds;
- one default method derived from a required primitive;
- one shared law test across all product implementations;
- a memo explaining why a trait object is unnecessary in this laboratory.

See `labs/module-01-contract-boundaries/README.md` for the executable contract.

## Design focus

Treat the trait as a behavioral boundary, not as a container for every shared method. Implement two meaningfully different concrete types so that defaults, receiver choices, and supertrait requirements are exercised rather than decorative. State at least three semantic laws in prose and encode them as reusable contract tests. Include one inherent method with the same name as a trait method and use fully qualified syntax to demonstrate which contract is being called. Reject a getter-only trait, a one-implementation trait, and a broad supertrait bound unless the product contract genuinely requires them. The final API should remain understandable to a caller who never sees the concrete implementation.

Your tests should distinguish shape from meaning: compilation proves that a method exists, while contract tests prove stable identity, deterministic output, and preservation of the required invariant.

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

> What behavior truly belongs in a shared contract, and which laws must every implementation preserve?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Contract Boundaries**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
