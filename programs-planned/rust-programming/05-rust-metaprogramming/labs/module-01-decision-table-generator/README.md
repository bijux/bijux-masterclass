# Laboratory 41 — Decision Table Generator

**Course 5 · Module 41: Metaprogramming Boundaries and the Expansion Model**

[Chapter](../../course-book/module-41-metaprogramming-boundaries-and-expansion-model/index.md) · [Workbook](../../course-book/module-41-metaprogramming-boundaries-and-expansion-model/workbook.md) · [CommandForge guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Metaprogramming Boundaries and the Expansion Model**: Which facts deserve generation, and what exactly happens between macro input and the Rust program that finally runs? The product must make **Separate runtime abstraction from compile-time generation** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **mechanism-selection record** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> Which facts deserve generation, and what exactly happens between macro input and the Rust program that finally runs?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Build a small mechanism-selection library for a design review. The product receives a concrete requirement and returns the least powerful mechanism that can honestly own it: ordinary Rust, `macro_rules!`, custom derive, attribute macro, function-like procedural macro, or build script.

The point is not to generate the decision algorithm. Runtime judgment remains ordinary Rust. A declarative macro is used only for the stable relationship among criterion variants, labels, and explanatory text. This division makes the deletion test visible: removing the macro would force the same criterion association into several exhaustive surfaces, while removing the ordinary function would erase real policy.

## Required behavior

- One declaration generates `Criterion`, its label, its explanation, and an ordered `ALL_CRITERIA` table.
- `Problem` records whether inputs are runtime values, existing Rust items, attached items, custom syntax, or checked external files.
- `recommend` returns a `Decision` with a mechanism and a reason.
- Contradictory requirements are rejected instead of being assigned an arbitrary macro.
- Table order is declaration order.

## Adversarial cases

Test a runtime normalization request, enum/code/message drift, field-shape metadata, attached function validation, a route DSL with duplicate checks, and constants generated from TSV. Add one requirement where a runtime table is already a single source of truth and prove that the answer is ordinary Rust.

## Build sequence

Start from `starter`, write the source-of-truth table, then implement the generated criterion surfaces. Keep the policy function ordinary. Add tests before comparing with `solution`.

## Transfer

Add a seventh mechanism category only after identifying a requirement that the existing ladder cannot express. Defend why it is not merely a renamed procedural macro or build script.

## Review record

For every recommendation, emit a compact record with four fields: the requirement, the selected mechanism, the decisive property, and the strongest rejected alternative. A recommendation without a rejected alternative is incomplete because it does not show that you considered a less powerful or more explicit design.

Use at least these adversarial requirements during review:

- several callers need the same runtime calculation;
- a public struct needs one repetitive implementation derived from its fields;
- a command table must reject duplicate literal names before type checking;
- checked-in tabular data must become constants during a build;
- a function needs ordinary precondition checking but no generated companion item.

The final report should make deletion possible. For each use of generation, state what handwritten code would replace it and which relationship could drift. If the answer is only “more lines,” recommend ordinary Rust instead.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Decision Table Generator**.
2. Draw the smallest **mechanism-selection record** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to CommandForge so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 41 — Decision Table Generator**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Decision Table Generator**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Separate runtime abstraction from compile-time generation.
- Identify the source of truth and generated surface of a proposed macro.
- Explain expansion as a staged production of ordinary Rust tokens.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 41 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **mechanism-selection record**. Defend why your design is simpler than one plausible alternative under the new requirements.
