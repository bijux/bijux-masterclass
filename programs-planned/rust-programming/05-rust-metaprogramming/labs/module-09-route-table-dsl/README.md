# Laboratory 49 — Route Table DSL

**Course 5 · Module 49: Function-Like Procedural Macros and Typed DSLs**

[Chapter](../../course-book/module-49-function-like-procedural-macros-and-typed-dsls/index.md) · [Workbook](../../course-book/module-49-function-like-procedural-macros-and-typed-dsls/workbook.md) · [CommandForge guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Function-Like Procedural Macros and Typed DSLs**: How do you turn custom syntax into an AST, validate cross-entry semantics, normalize the model, and generate compact typed Rust? The product must make **Design a bounded custom grammar with explicit compatibility space** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **DSL syntax-to-model map** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> How do you turn custom syntax into an AST, validate cross-entry semantics, normalize the model, and generate compact typed Rust?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Build a function-like procedural macro for a small typed route catalog:

```rust
route_table! {
    pub static ROUTES {
        GET "/users" => list_users;
        POST "/users" => create_user;
    }
}
```

The parser owns syntax, a separate validator owns supported methods and duplicate `(method, path)` pairs, and Rust owns path resolution and handler type checking.

## Required behavior

- Require visibility, `static`, a table name, braces, and semicolon-terminated entries.
- Support `GET`, `POST`, `PUT`, and `DELETE`.
- Require paths to start with `/`.
- Reject duplicate method/path pairs at the later entry.
- Preserve source order.
- Generate `Method`, `Route`, the static table, and a dispatch function.
- Keep handler paths as Rust paths rather than strings.

## Adversarial cases

Test missing semicolon, unsupported method, empty path, relative path, duplicate pair, same path with different method, nested handler path, and handler with the wrong function type. The last error should come from generated ordinary Rust type checking.

## Build sequence

Implement `Parse` for the AST only. Then validate to a normalized model. Generate only after validation succeeds. Do not insert entries into a hash map during parsing.

## Transfer

Add an optional route name and generate a reverse lookup. Define whether names must be unique and where that rule belongs.

## Phase separation proof

Keep parsing, semantic validation, normalization, and emission as separate functions. Parsing should accept syntactically valid entries without deciding whether a method is supported. Validation should reject unsupported methods and duplicate `(method, path)` pairs while retaining both the current span and enough context to explain the conflict.

Test routes in source order and compare the generated table order exactly. Add failures for a missing semicolon, unsupported method, empty path, path without a leading slash, duplicate pair, and unresolved handler path. The unresolved path should be left to ordinary Rust name resolution; the DSL cannot honestly prove that a path exists.

A transfer variant should add one optional route label while keeping old syntax valid. Record the normalized internal representation before changing code generation.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Route Table DSL**.
2. Draw the smallest **DSL syntax-to-model map** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to CommandForge so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 49 — Route Table DSL**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Route Table DSL**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Design a bounded custom grammar with explicit compatibility space.
- Implement `syn::parse::Parse` for syntax nodes rather than splitting strings.
- Separate syntax AST, semantic validation, normalized model, and generation.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 49 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **DSL syntax-to-model map**. Defend why your design is simpler than one plausible alternative under the new requirements.
