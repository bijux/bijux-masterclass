# Laboratory 44 — Exported Registry Macro

This is the independent product for **Course 5, Module 44: Hygiene, Scope, Paths, and Cross-Crate Macros**. Read the [module chapter](../../course-book/module-44-hygiene-scope-paths-and-cross-crate-macros/index.md) and complete its [workbook](../../course-book/module-44-hygiene-scope-paths-and-cross-crate-macros/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> Whose names should generated code resolve, and how do you make exported macros survive nesting, imports, and dependency renaming?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Create a library macro that downstream crates can use to declare a static command registry:

```rust
command_registry! {
    pub static COMMANDS {
        "echo" => crate::echo;
        "upper" => crate::upper;
    }
}
```

The defining crate owns the `Entry` type. The invocation owns command literals and handler paths. The expansion must use `$crate` for definition-owned items and must not depend on imports that happen to exist where the macro was written.

## Required behavior

- `Entry` contains a name and `fn(&str) -> String` handler.
- The macro emits an ordered static slice.
- Lookup is ordinary Rust over the generated slice.
- Definition-owned paths use `$crate`.
- Caller handler paths are captured with `path`.
- Invocation inside an integration test behaves like downstream use.
- Shadowing a short local type name does not affect expansion.

## Adversarial cases

Test nested-module invocation, an empty registry, source-order preservation, missing handler paths, and a local `Entry` type that would collide with an unqualified expansion. Document why `$crate` does not bypass visibility.

## Build sequence

Implement `Entry` first and prove it needs no macro. Then write the smallest item-generating matcher. Use integration tests, not only unit tests inside the defining module.

## Transfer

Create a second package locally that aliases the dependency name and invokes the macro. Record whether any generated path mentions the package’s original Cargo name. The reference includes this proof as `solution/tests/renamed-consumer`; it depends on the defining package under the alias `renamed_registry` and deliberately shadows `Entry`.

## Downstream-crate proof

The decisive test lives outside the defining crate. Invoke the macro from an integration test, place the invocation inside a nested module, rename imports, and use handler paths owned by the call site. Definition-owned support types must resolve through `$crate`; caller-provided handler paths must resolve where the invocation is written.

Add a deliberate shadow type named `Entry` in the downstream module. A robust expansion must still construct the defining crate's entry type rather than the shadow. Also verify that private definition-crate helpers are not accidentally required by the public expansion.

Document the edition and path assumptions of the exported syntax. A macro that works only because the defining crate happened to be imported under one spelling is not a stable cross-crate API.

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

> Whose names should generated code resolve, and how do you make exported macros survive nesting, imports, and dependency renaming?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Exported Registry Macro**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
