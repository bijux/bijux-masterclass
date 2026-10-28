# Laboratory 30 — Inspection Platform

**Course 3 · Module 30: Architectural Synthesis**

[Chapter](../../course-book/module-30-architectural-synthesis/index.md) · [Workbook](../../course-book/module-30-architectural-synthesis/workbook.md) · [Review Engine guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Architectural Synthesis**: Given a real source of variation, how do you choose among enums, generics, trait objects, closures, functions, and ordinary composition? The product must make **Map axes of variation before selecting polymorphism mechanisms** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **architecture decision record** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

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

## Design record

Before implementation, complete this record for **Inspection Platform**:

| Question | Required answer |
|---|---|
| Module decision | How does **Architectural Synthesis** answer its governing question in this product? |
| Authority | Which type or component decides the main rule? |
| Valid states | Which states may be observed through the public API? |
| Rejection | What exact input or transition is refused, and what remains unchanged? |
| Ownership | Who owns every resource before, during, and after the decisive operation? |
| Order and bounds | Which sequence, capacity, lifetime, or compatibility limit is promised? |
| Evidence | Which test, compiler case, model, trace, or review could falsify the claim? |

Use the **architecture decision record** to answer the table. Then add at least three adversarial cases: one at the smallest boundary, one at the largest accepted or rejected boundary, and one that leaves partial work before failure. For each, state the final observable state before running the test.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Inspection Platform**.
2. Draw the smallest **architecture decision record** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to Review Engine so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 30 — Inspection Platform**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Inspection Platform**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Map axes of variation before selecting polymorphism mechanisms.
- Combine static and dynamic dispatch without duplicating domain semantics.
- Review an architecture for coherence, dyn compatibility, state validity, and evolution.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 30 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **architecture decision record**. Defend why your design is simpler than one plausible alternative under the new requirements.
