# Laboratory 22 — Associated Families

**Course 3 · Module 22: Associated Types and Type Families**

[Chapter](../../course-book/module-22-associated-types-and-type-families/index.md) · [Workbook](../../course-book/module-22-associated-types-and-type-families/workbook.md) · [Review Engine guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Associated Types and Type Families**: When is a type chosen once by an implementation, when may callers choose it repeatedly, and how should that relationship appear in the API? The product must make **Choose between generic parameters and associated types from relationship cardinality** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **associated-type relationship map** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> When is a type chosen once by an implementation, when may callers choose it repeatedly, and how should that relationship appear in the API?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Implement a tabular source abstraction with two layers:

- `LendingRows`, whose `Row<'a>` borrows from the source's current buffer;
- `OwnedRows`, an adapter that materializes durable `OwnedRow` values.

The lab must demonstrate why ordinary `Iterator` cannot express the lending relationship and must include a compile-fail example preventing a borrowed row from surviving the next mutable advance.

The solution must not expose the GAT to callers that only need owned rows.

## Design focus

The source reuses an internal text buffer, so each borrowed row is valid only until the next mutable advance. Model that relationship directly: `Row<'a>` must be tied to the borrow used for one call, not to an invented long-lived lifetime. The owned adapter should copy only at the boundary where durable storage is requested. Callers that need ordinary owned iteration should not have to understand the lending protocol or name its GAT.

Test empty input, multiple rows, repeated advancement, and conversion to owned rows. Add a negative example showing that a borrowed row cannot survive another mutable call. Compare the design with three weaker alternatives: returning `String` for every row, exposing internal buffer indices, and claiming ordinary `Iterator<Item = &str>` can borrow from mutable iterator state. Explain exactly what information each alternative loses or misrepresents.

## Design record

Before implementation, complete this record for **Associated Families**:

| Question | Required answer |
|---|---|
| Module decision | How does **Associated Types and Type Families** answer its governing question in this product? |
| Authority | Which type or component decides the main rule? |
| Valid states | Which states may be observed through the public API? |
| Rejection | What exact input or transition is refused, and what remains unchanged? |
| Ownership | Who owns every resource before, during, and after the decisive operation? |
| Order and bounds | Which sequence, capacity, lifetime, or compatibility limit is promised? |
| Evidence | Which test, compiler case, model, trace, or review could falsify the claim? |

Use the **associated-type relationship map** to answer the table. Then add at least three adversarial cases: one at the smallest boundary, one at the largest accepted or rejected boundary, and one that leaves partial work before failure. For each, state the final observable state before running the test.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Associated Families**.
2. Draw the smallest **associated-type relationship map** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to Review Engine so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 22 — Associated Families**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Associated Families**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Choose between generic parameters and associated types from relationship cardinality.
- Use associated constants and associated types without hiding call-site variation.
- Derive a generic associated type from a borrowing family requirement.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 22 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **associated-type relationship map**. Defend why your design is simpler than one plausible alternative under the new requirements.
