# Laboratory 24 — Static Pipeline

**Course 3 · Module 24: Static Polymorphism and Opaque Types**

[Chapter](../../course-book/module-24-static-polymorphism-and-opaque-types/index.md) · [Workbook](../../course-book/module-24-static-polymorphism-and-opaque-types/workbook.md) · [Review Engine guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Static Polymorphism and Opaque Types**: When should concrete types remain visible to the compiler, and how can an API hide implementation details without erasing static guarantees? The product must make **Design generic functions and types with the weakest sufficient bounds** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **static-dispatch map** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

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

## Design record

Before implementation, complete this record for **Static Pipeline**:

| Question | Required answer |
|---|---|
| Module decision | How does **Static Polymorphism and Opaque Types** answer its governing question in this product? |
| Authority | Which type or component decides the main rule? |
| Valid states | Which states may be observed through the public API? |
| Rejection | What exact input or transition is refused, and what remains unchanged? |
| Ownership | Who owns every resource before, during, and after the decisive operation? |
| Order and bounds | Which sequence, capacity, lifetime, or compatibility limit is promised? |
| Evidence | Which test, compiler case, model, trace, or review could falsify the claim? |

Use the **static-dispatch map** to answer the table. Then add at least three adversarial cases: one at the smallest boundary, one at the largest accepted or rejected boundary, and one that leaves partial work before failure. For each, state the final observable state before running the test.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Static Pipeline**.
2. Draw the smallest **static-dispatch map** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to Review Engine so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 24 — Static Pipeline**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Static Pipeline**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Design generic functions and types with the weakest sufficient bounds.
- Distinguish argument-position and return-position `impl Trait`.
- Explain monomorphization without promising optimization outcomes.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 24 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **static-dispatch map**. Defend why your design is simpler than one plausible alternative under the new requirements.
