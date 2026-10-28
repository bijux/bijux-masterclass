# Laboratory 44 — Exported Registry Macro

**Course 5 · Module 44: Hygiene, Scope, Paths, and Cross-Crate Macros**

[Chapter](../../course-book/module-44-hygiene-scope-paths-and-cross-crate-macros/index.md) · [Workbook](../../course-book/module-44-hygiene-scope-paths-and-cross-crate-macros/workbook.md) · [CommandForge guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Hygiene, Scope, Paths, and Cross-Crate Macros**: Whose names should generated code resolve, and how do you make exported macros survive nesting, imports, and dependency renaming? The product must make **Distinguish textual scope, path-based scope, and expansion-site lookup for declarative macros** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **hygiene and path map** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

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

1. Read the product contract and run the starter’s baseline checks for **Exported Registry Macro**.
2. Draw the smallest **hygiene and path map** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to CommandForge so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 44 — Exported Registry Macro**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Exported Registry Macro**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Distinguish textual scope, path-based scope, and expansion-site lookup for declarative macros.
- Use `$crate` for defining-crate references in exported `macro_rules!` expansions.
- Preserve invocation-site identifiers supplied by callers.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 44 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **hygiene and path map**. Defend why your design is simpler than one plausible alternative under the new requirements.
