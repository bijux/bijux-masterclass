# Laboratory 45 — Diagnostic Enum Macro

This is the independent product for **Course 5, Module 45: Macro Diagnostics, Testing, and Public API Design**. Read the [module chapter](../../course-book/module-45-macro-diagnostics-testing-and-public-api-design/index.md) and complete its [workbook](../../course-book/module-45-macro-diagnostics-testing-and-public-api-design/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> How do you prove that a macro accepts the intended language, rejects misuse for the intended reason, and remains an evolvable public API?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Generate a typed diagnostic catalog from one declaration:

```rust
diagnostic_enum! {
    pub enum Diagnostic {
        MissingField = 1001 => "missing field";
        InvalidNumber = 1002 => "invalid number";
    }
}
```

One invocation must own variants, stable codes, messages, reverse lookup, display behavior, and deterministic catalog order. The laboratory emphasizes public grammar and negative behavior as much as generated happy-path code.

## Required behavior

- Generate the enum, `code`, `message`, `from_code`, `Display`, and `ALL`.
- Preserve declaration order in `ALL`.
- Return `None` for unknown codes.
- Require numeric literal codes and string literal messages.
- Provide targeted compile errors for a missing code and missing message.
- Evaluate no caller runtime expressions; the grammar accepts declarations only.

## Adversarial cases

Test round trips for every declared code, unknown code, exact messages, display output, and table order. Preserve compile-fail examples for malformed separators and omitted fields. Explain why robust duplicate-code validation is a reason to consider a procedural macro for a larger catalog.

## Build sequence

Start from the data relationship, not from macro syntax. Generate each public surface from the same repetition. Add specific malformed-input rules before the generic fallback.

## Transfer

Add a severity literal to each declaration and generate a typed severity accessor. Do not add an independently maintained severity table.

## Compatibility proof

Treat the invocation grammar and generated items as one public contract. Test stable code lookup, display text, declaration order, and an unknown code. Then add negative cases for a missing message, malformed numeric code, and syntactically incomplete entry so the failure occurs near the incorrect token.

Do not claim compile-time uniqueness unless the implementation actually checks it. If duplicate numeric codes are delegated to a generated `match`, capture the resulting Rust diagnostic and decide whether that is sufficiently local. If not, redesign the grammar or implement explicit token-level checking.

Perform one evolution exercise: add an optional documentation string without breaking old invocations. Record which previously accepted token sequences remain valid and which generated names are part of the compatibility surface.

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

> How do you prove that a macro accepts the intended language, rejects misuse for the intended reason, and remains an evolvable public API?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Diagnostic Enum Macro**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
