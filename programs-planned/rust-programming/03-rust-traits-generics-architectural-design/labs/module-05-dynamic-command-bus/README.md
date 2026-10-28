# Laboratory 25 — Dynamic Command Bus

**Course 3 · Module 25: Trait Objects and Dynamic Polymorphism**

[Chapter](../../course-book/module-25-trait-objects-and-dynamic-polymorphism/index.md) · [Workbook](../../course-book/module-25-trait-objects-and-dynamic-polymorphism/workbook.md) · [Review Engine guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Trait Objects and Dynamic Polymorphism**: When is run-time heterogeneity real, what information does a trait object erase, and what must remain dispatchable? The product must make **Derive whether a trait is dyn-compatible and repair it without erasing its meaning** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **dynamic-dispatch map** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> When is run-time heterogeneity real, what information does a trait object erase, and what must remain dispatchable?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Build a command bus that owns heterogeneous command handlers behind a dyn-compatible interface.

Requirements:

- a stable command envelope and typed execution result;
- at least three concrete handlers;
- deterministic registration and dispatch;
- no downcasting in ordinary execution;
- a separate factory or constructor surface for handler-specific configuration;
- borrowed-handler support demonstrated through an explicit object lifetime;
- a comparison with a closed command enum.

## Design focus

The command bus exists because handler kinds are selected and stored at run time. Derive the erased contract from dispatch needs: stable command identity, one object-safe invocation method, and a concrete result envelope. Construction and handler-specific configuration belong outside the trait. Keep registration order deterministic and reject duplicate command names before dispatch.

Demonstrate both owned handlers and a borrowed handler whose object lifetime is explicit; do not add `'static` by reflex. Add negative examples for a generic trait method and an associated function without a receiver, then explain why each is not dyn-compatible. Ordinary execution must not downcast. Finish with an enum comparison that names the exact requirement under which a closed enum would be simpler and safer than the registry.

## Design record

Before implementation, complete this record for **Dynamic Command Bus**:

| Question | Required answer |
|---|---|
| Module decision | How does **Trait Objects and Dynamic Polymorphism** answer its governing question in this product? |
| Authority | Which type or component decides the main rule? |
| Valid states | Which states may be observed through the public API? |
| Rejection | What exact input or transition is refused, and what remains unchanged? |
| Ownership | Who owns every resource before, during, and after the decisive operation? |
| Order and bounds | Which sequence, capacity, lifetime, or compatibility limit is promised? |
| Evidence | Which test, compiler case, model, trace, or review could falsify the claim? |

Use the **dynamic-dispatch map** to answer the table. Then add at least three adversarial cases: one at the smallest boundary, one at the largest accepted or rejected boundary, and one that leaves partial work before failure. For each, state the final observable state before running the test.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Dynamic Command Bus**.
2. Draw the smallest **dynamic-dispatch map** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to Review Engine so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 25 — Dynamic Command Bus**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Dynamic Command Bus**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Derive whether a trait is dyn-compatible and repair it without erasing its meaning.
- Use borrowed and owned trait objects with correct object lifetimes.
- Build a heterogeneous runtime collection behind one behavioral interface.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 25 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **dynamic-dispatch map**. Defend why your design is simpler than one plausible alternative under the new requirements.
