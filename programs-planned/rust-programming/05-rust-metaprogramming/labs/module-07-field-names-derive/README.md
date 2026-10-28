# Laboratory 47 — Field Names Derive

**Course 5 · Module 47: Custom Derive Macros and Structural Generation**

[Chapter](../../course-book/module-47-custom-derive-macros-and-structural-generation/index.md) · [Workbook](../../course-book/module-47-custom-derive-macros-and-structural-generation/workbook.md) · [CommandForge guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Custom Derive Macros and Structural Generation**: How do you inspect a Rust item, preserve its generics and constraints, and generate a lawful implementation without pretending to perform type checking? The product must make **Parse `DeriveInput` and distinguish structs, enums, and unions** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **derive expansion ledger** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> How do you inspect a Rust item, preserve its generics and constraints, and generate a lawful implementation without pretending to perform type checking?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Implement:

```rust
#[derive(FieldNames)]
struct User<T> {
    id: u64,
    #[field_names(rename = "display-name")]
    name: String,
    #[field_names(skip)]
    cache: T,
}
```

The derive generates `User::<T>::FIELD_NAMES` without adding bounds on `T`. The source struct remains the authority for field shape; helper attributes own only exposure policy.

## Required behavior

- Support named-field structs and unit structs.
- Reject tuple structs, enums, and unions with spanned errors.
- Preserve lifetimes, type parameters, const parameters, and where clauses.
- Support `skip` and `rename = "..."`.
- Reject unknown keys, duplicates, empty rename values, and `skip` plus `rename` on one field.
- Generate an inherent `&'static [&'static str]` constant.
- Add no field-type trait bounds.

## Adversarial cases

Use generic and const-generic structs, an existing where clause, raw identifiers, several helper attributes, and unsupported input forms. Include a field type that implements no formatting traits to prove that the derive does not overconstrain it.

## Build sequence

Parse `DeriveInput`, classify data shape, parse every field policy, combine independent errors where useful, then generate with `split_for_impl`. Do not infer type semantics from path spelling.

## Transfer

Add a `FieldCount` associated constant derived from the exposed names. It must share the same normalized field policy rather than parse attributes a second time.

## Structural and generic proof

Use a generic struct with a lifetime, a type parameter, a const parameter, and an existing `where` clause. The generated associated constant must compile without inventing bounds on fields that are only inspected syntactically. A skipped field of an otherwise unconstrained type is the most direct test.

Test a raw identifier, a renamed field, a skipped field, an empty named struct, and a unit struct if the documented contract supports it. Tuple structs and enums must be rejected with diagnostics attached to the unsupported shape rather than failing later in generated code.

Inspect the expanded implementation and confirm that `split_for_impl` preserves declaration generics and the original `where` clause. The derive owns field-name metadata only; it must not duplicate or reconstruct the source struct.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Field Names Derive**.
2. Draw the smallest **derive expansion ledger** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to CommandForge so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 47 — Field Names Derive**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Field Names Derive**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Parse `DeriveInput` and distinguish structs, enums, and unions.
- Support only documented item shapes and reject others at useful spans.
- Inspect named, unnamed, and unit fields without losing source order.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 47 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **derive expansion ledger**. Defend why your design is simpler than one plausible alternative under the new requirements.
