# Laboratory 29 — Evolvable SDK

**Course 3 · Module 29: Public API Evolution**

[Chapter](../../course-book/module-29-public-api-evolution/index.md) · [Workbook](../../course-book/module-29-public-api-evolution/workbook.md) · [Review Engine guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Public API Evolution**: How can a public trait-based API evolve when downstream crates may both call it and implement it? The product must make **Classify public trait changes by downstream source-compatibility risk** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **compatibility matrix** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> How can a public trait-based API evolve when downstream crates may both call it and implement it?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Start from a small public plugin contract and evolve it through two versions.

Requirements:

- downstream-style fixture crate implementing V1;
- a proposed breaking change and hazard analysis;
- a nonbreaking extension trait where semantics permit;
- a V2 trait where new required semantics cannot be defaulted;
- a newtype adapter from V1 to V2 with explicit information loss;
- a sealed internal trait and one open public trait;
- compile-positive and compile-negative compatibility evidence.

## Design focus

Treat the package as a public SDK with two downstream audiences: callers and implementors. Build one open extension trait, one sealed internal trait, and one non-exhaustive public data model. For every public item, record whether adding a method, variant, bound, blanket implementation, or supertrait would affect callers, implementors, or both.

Create a small downstream-style test crate that uses only the public API. Preserve it while making one compatible addition and deliberately demonstrate one breaking change in an isolated negative example. Avoid promising object safety or downstream implementation unless the product needs it; both promises restrict future evolution. The final README must state the extension policy in ordinary product language, not in semver slogans alone.

## Design record

Before implementation, complete this record for **Evolvable SDK**:

| Question | Required answer |
|---|---|
| Module decision | How does **Public API Evolution** answer its governing question in this product? |
| Authority | Which type or component decides the main rule? |
| Valid states | Which states may be observed through the public API? |
| Rejection | What exact input or transition is refused, and what remains unchanged? |
| Ownership | Who owns every resource before, during, and after the decisive operation? |
| Order and bounds | Which sequence, capacity, lifetime, or compatibility limit is promised? |
| Evidence | Which test, compiler case, model, trace, or review could falsify the claim? |

Use the **compatibility matrix** to answer the table. Then add at least three adversarial cases: one at the smallest boundary, one at the largest accepted or rejected boundary, and one that leaves partial work before failure. For each, state the final observable state before running the test.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Evolvable SDK**.
2. Draw the smallest **compatibility matrix** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to Review Engine so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 29 — Evolvable SDK**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Evolvable SDK**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Classify public trait changes by downstream source-compatibility risk.
- Design default methods and extension points without accidental semantic promises.
- Use sealing, non-exhaustive data, adapters, and versioned traits appropriately.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 29 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **compatibility matrix**. Defend why your design is simpler than one plausible alternative under the new requirements.
