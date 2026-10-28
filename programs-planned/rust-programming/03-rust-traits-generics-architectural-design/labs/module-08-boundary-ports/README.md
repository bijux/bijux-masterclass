# Laboratory 28 — Boundary Ports

**Course 3 · Module 28: Boundary Traits and Adapters**

[Chapter](../../course-book/module-28-boundary-traits-and-adapters/index.md) · [Workbook](../../course-book/module-28-boundary-traits-and-adapters/workbook.md) · [Review Engine guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Boundary Traits and Adapters**: How should a Rust program adapt external data, effects, closures, and foreign types without contaminating its core model? The product must make **Design extension traits, closure adapters, and conversion boundaries with precise contracts** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **adapter boundary map** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

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

## Design record

Before implementation, complete this record for **Boundary Ports**:

| Question | Required answer |
|---|---|
| Module decision | How does **Boundary Traits and Adapters** answer its governing question in this product? |
| Authority | Which type or component decides the main rule? |
| Valid states | Which states may be observed through the public API? |
| Rejection | What exact input or transition is refused, and what remains unchanged? |
| Ownership | Who owns every resource before, during, and after the decisive operation? |
| Order and bounds | Which sequence, capacity, lifetime, or compatibility limit is promised? |
| Evidence | Which test, compiler case, model, trace, or review could falsify the claim? |

Use the **adapter boundary map** to answer the table. Then add at least three adversarial cases: one at the smallest boundary, one at the largest accepted or rejected boundary, and one that leaves partial work before failure. For each, state the final observable state before running the test.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Boundary Ports**.
2. Draw the smallest **adapter boundary map** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to Review Engine so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 28 — Boundary Ports**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Boundary Ports**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Design extension traits, closure adapters, and conversion boundaries with precise contracts.
- Use generic or dynamic ports according to ownership and deployment needs.
- Build test doubles that preserve the production contract rather than mirror internals.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 28 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **adapter boundary map**. Defend why your design is simpler than one plausible alternative under the new requirements.
