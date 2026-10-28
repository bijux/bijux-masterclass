# Laboratory 23 — Coherence Adapters

**Course 3 · Module 23: Coherence and Implementation Ownership**

[Chapter](../../course-book/module-23-coherence-and-implementation-ownership/index.md) · [Workbook](../../course-book/module-23-coherence-and-implementation-ownership/workbook.md) · [Review Engine guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Coherence and Implementation Ownership**: Which crate owns the right to create an implementation, and how can a public design preserve coherence without giving up adaptation? The product must make **Predict whether an implementation satisfies coherence and orphan rules** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **coherence ownership map** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> Which crate owns the right to create an implementation, and how can a public design preserve coherence without giving up adaptation?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Integrate two foreign-style model types with two local formatting and validation contracts.

Requirements:

- one local extension trait over a foreign-like type;
- one newtype implementing an external standard trait;
- one intentionally rejected blanket implementation with a written overlap proof;
- a sealed internal capability and public read-only extension surface;
- compile-fail evidence for a forbidden downstream implementation;
- a semver note describing the implementation space reserved by each blanket impl.

## Design focus

Begin from an implementation Rust forbids: a foreign formatting trait for a foreign vendor type. Do not treat the orphan rule as an obstacle to bypass. Identify which semantic behavior belongs to your crate, introduce a validated local newtype, and put the implementation there. Add an extension trait only for behavior that should be callable on the foreign value without changing its identity.

The lab must include one narrowly bounded blanket implementation and a written overlap analysis. Show which future implementations that blanket consumes. Add a sealed marker only where downstream implementation would freeze an internal classification; leave intended extension points open. Tests must cover newtype validation, formatting, adapter behavior, and method resolution. A wrapper that merely forwards every vendor method without adding an invariant does not satisfy the lab.

## Design record

Before implementation, complete this record for **Coherence Adapters**:

| Question | Required answer |
|---|---|
| Module decision | How does **Coherence and Implementation Ownership** answer its governing question in this product? |
| Authority | Which type or component decides the main rule? |
| Valid states | Which states may be observed through the public API? |
| Rejection | What exact input or transition is refused, and what remains unchanged? |
| Ownership | Who owns every resource before, during, and after the decisive operation? |
| Order and bounds | Which sequence, capacity, lifetime, or compatibility limit is promised? |
| Evidence | Which test, compiler case, model, trace, or review could falsify the claim? |

Use the **coherence ownership map** to answer the table. Then add at least three adversarial cases: one at the smallest boundary, one at the largest accepted or rejected boundary, and one that leaves partial work before failure. For each, state the final observable state before running the test.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Coherence Adapters**.
2. Draw the smallest **coherence ownership map** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to Review Engine so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 23 — Coherence Adapters**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Coherence Adapters**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Predict whether an implementation satisfies coherence and orphan rules.
- Detect overlapping blanket implementations and downstream compatibility hazards.
- Use a newtype to establish local implementation ownership.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 23 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **coherence ownership map**. Defend why your design is simpler than one plausible alternative under the new requirements.
