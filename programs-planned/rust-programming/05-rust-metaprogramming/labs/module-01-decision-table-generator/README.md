# Laboratory 41 — Decision Table Generator

This is the independent product for **Course 5, Module 41: Metaprogramming Boundaries and the Expansion Model**. Read the [module chapter](../../course-book/module-41-metaprogramming-boundaries-and-expansion-model/index.md) and complete its [workbook](../../course-book/module-41-metaprogramming-boundaries-and-expansion-model/workbook.md) before consulting the reference implementation.

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

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/`, add the first adversarial test before the design-changing repair, and complete the workbook’s transfer problem before reading the reference implementation.

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

> Which facts deserve generation, and what exactly happens between macro input and the Rust program that finally runs?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Decision Table Generator**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
