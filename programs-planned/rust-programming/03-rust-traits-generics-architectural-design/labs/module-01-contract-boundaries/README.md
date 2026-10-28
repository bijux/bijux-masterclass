# Laboratory 21 — Contract Boundaries

**Course 3 · Module 21: Traits as Behavioral Contracts**

[Chapter](../../course-book/module-21-traits-as-behavioral-contracts/index.md) · [Workbook](../../course-book/module-21-traits-as-behavioral-contracts/workbook.md) · [Review Engine guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Traits as Behavioral Contracts**: What behavior truly belongs in a shared contract, and which laws must every implementation preserve? The product must make **Define a trait whose methods express a coherent behavioral contract** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **trait-law table** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

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

1. Read the product contract and run the starter’s baseline checks for **Contract Boundaries**.
2. Draw the smallest **trait-law table** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to Review Engine so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 21 — Contract Boundaries**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Contract Boundaries**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Define a trait whose methods express a coherent behavioral contract.
- Distinguish inherent behavior, free functions, and trait behavior.
- Apply bounds, `where` clauses, default methods, supertraits, and UFCS correctly.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 21 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **trait-law table**. Defend why your design is simpler than one plausible alternative under the new requirements.
