# Laboratory 26 — Composed Renderer

**Course 3 · Module 26: Composition and OOP-Style Design Without Inheritance**

[Chapter](../../course-book/module-26-composition-and-oop-style-design-without-inheritance/index.md) · [Workbook](../../course-book/module-26-composition-and-oop-style-design-without-inheritance/workbook.md) · [Review Engine guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Composition and OOP-Style Design Without Inheritance**: How do you obtain encapsulation, substitution, and reusable behavior through composition rather than inheritance? The product must make **Model encapsulation, substitution, and delegation without class inheritance** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **composition diagram** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

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

## Design record

Before implementation, complete this record for **Composed Renderer**:

| Question | Required answer |
|---|---|
| Module decision | How does **Composition and OOP-Style Design Without Inheritance** answer its governing question in this product? |
| Authority | Which type or component decides the main rule? |
| Valid states | Which states may be observed through the public API? |
| Rejection | What exact input or transition is refused, and what remains unchanged? |
| Ownership | Who owns every resource before, during, and after the decisive operation? |
| Order and bounds | Which sequence, capacity, lifetime, or compatibility limit is promised? |
| Evidence | Which test, compiler case, model, trace, or review could falsify the claim? |

Use the **composition diagram** to answer the table. Then add at least three adversarial cases: one at the smallest boundary, one at the largest accepted or rejected boundary, and one that leaves partial work before failure. For each, state the final observable state before running the test.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Composed Renderer**.
2. Draw the smallest **composition diagram** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to Review Engine so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 26 — Composed Renderer**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Composed Renderer**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Model encapsulation, substitution, and delegation without class inheritance.
- Apply composition, strategy, adapter, decorator, and command patterns selectively.
- Separate domain state from interchangeable behavior.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 26 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **composition diagram**. Defend why your design is simpler than one plausible alternative under the new requirements.
