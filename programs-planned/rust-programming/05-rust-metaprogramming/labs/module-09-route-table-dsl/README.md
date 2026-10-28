# Laboratory 49 — Route Table DSL

This is the independent product for **Course 5, Module 49: Function-Like Procedural Macros and Typed DSLs**. Read the [module chapter](../../course-book/module-49-function-like-procedural-macros-and-typed-dsls/index.md) and complete its [workbook](../../course-book/module-49-function-like-procedural-macros-and-typed-dsls/workbook.md) before consulting the reference implementation.

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

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/`, add the first adversarial test before the design-changing repair, and complete the workbook’s transfer problem before reading the reference implementation.

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

> How do you turn custom syntax into an AST, validate cross-entry semantics, normalize the model, and generate compact typed Rust?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Route Table DSL**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
