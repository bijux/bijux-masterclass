# 44 — Hygiene, Scope, Paths, and Cross-Crate Macros

**Course 5, day 4 · Module 44 of 60**  
`███████████████░░░░░` **44/60**

[← Module 43: Recursive Macro Parsing and Token-Tree Techniques](../module-43-recursive-macro-parsing-and-token-tree-techniques/index.md) · [Course 5 overview](../index.md) · [Sixty-module map](../../../COURSE_MAP.md) · [Module 45: Macro Diagnostics, Testing, and Public API Design →](../module-45-macro-diagnostics-testing-and-public-api-design/index.md)

## The question

> Whose names should generated code resolve, and how do you make exported macros survive nesting, imports, and dependency renaming?

## Why this comes now

A macro that works beside its definition is not yet a reusable macro. Once expansion occurs in another module or crate, every generated path must answer a scope question: does this name belong to the macro-defining crate, the invocation site, the standard library, or the macro itself?

Modules 42 and 43 established grammar and expansion. Module 44 makes that expansion portable. Without this step, later diagnostics and procedural designs would be tested against a false local environment.

## What you will be able to do

- Distinguish textual scope, path-based scope, and expansion-site lookup for declarative macros.
- Use `$crate` for defining-crate references in exported `macro_rules!` expansions.
- Preserve invocation-site identifiers supplied by callers.
- Avoid accidental dependence on caller imports or prelude contents.
- Design visibility so generated code can legally reach helper items.
- Test macros from downstream crates, nested modules, and renamed dependencies.
- Explain why procedural macros require a different path strategy from `$crate`.

## Core model

### Hygiene is not invisibility

“Hygiene” is often summarized as “macro names do not collide.” That is too vague to design with.

A macro expansion contains several classes of names:

1. **captured names** supplied by the caller, such as `$handler:path`;
2. **defining-crate names** owned by the library that exports the macro;
3. **invocation-site names** written literally in the expansion and resolved where the macro is invoked;
4. **generated helper names** introduced by the expansion;
5. **language and standard-library paths** that should not depend on local imports.

Each class requires an explicit policy.

Consider:

```rust
pub struct RegistryEntry {
    pub name: &'static str,
    pub run: fn(&str) -> String,
}

#[macro_export]
macro_rules! registry {
    ($( $name:literal => $handler:path ),+ $(,)?) => {
        &[
            $(
                RegistryEntry {
                    name: $name,
                    run: $handler,
                }
            ),+
        ]
    };
}
```

This may work inside the defining module where `RegistryEntry` is in scope. In a downstream crate, the literal name `RegistryEntry` is looked up at the invocation site and may be missing or refer to an unrelated type. The macro is not robust.

### `$crate` names the defining crate

Inside a declarative macro, `$crate` expands to the crate where the macro was defined. It remains correct when the dependency is renamed by the caller.

```rust
#[macro_export]
macro_rules! registry {
    ($( $name:literal => $handler:path ),+ $(,)?) => {
        &[
            $(
                $crate::RegistryEntry {
                    name: $name,
                    run: $handler,
                }
            ),+
        ]
    };
}
```

The caller may depend on the package under an alias:

```toml
[dependencies]
renamed_registry = { package = "registry-core", path = "../registry-core" }
```

An expansion using `::registry_core::RegistryEntry` would fail because the extern-prelude name is `renamed_registry`. `$crate::RegistryEntry` does not rely on the caller’s dependency spelling.

#### `$crate` does not bypass privacy

The helper item must still be visible from the expansion site. If an exported macro expands to `$crate::private::Helper`, ordinary visibility checking applies. `$crate` chooses the crate; it does not grant access.

You have three main options:

- make the generated dependency a real public API;
- expose a deliberately hidden-but-public support path such as `#[doc(hidden)] pub mod __private`;
- change the expansion so it does not require the helper.

The second pattern is common but creates compatibility obligations. “Hidden from docs” is not “free to break.” Downstream expanded code still refers to it.

### Captured paths belong to the caller

When a caller supplies a handler path, the macro should generally transcribe that path unchanged:

```rust
registry! {
    "trim" => handlers::trim,
    "upper" => crate::handlers::upper,
}
```

`$handler:path` is parsed in the caller’s context and resolves as caller code. The macro should not prefix it with `$crate` unless the contract explicitly says that handlers come from the defining crate.

This gives a useful split:

```rust
$crate::RegistryEntry {          // library-owned type
    name: $name,                 // caller-supplied literal
    run: $handler,               // caller-supplied path
}
```

The expansion’s path policy is visible line by line.

### Do not depend on caller imports accidentally

A public macro should not assume that common names are imported:

```rust
#[macro_export]
macro_rules! collect_names {
    ($( $name:expr ),* $(,)?) => {{
        let mut result = Vec::new();
        $(result.push($name.to_owned());)*
        result
    }};
}
```

`Vec` and `ToOwned` may resolve through the prelude today, but a robust expansion should make dependencies deliberate when ambiguity or `no_std` policy matters:

```rust
let mut result = ::std::vec::Vec::new();
```

Absolute standard-library paths avoid caller shadowing. They also commit the macro to `std`. If the library supports `no_std` with `alloc`, route through a defining-crate re-export:

```rust
#[doc(hidden)]
pub extern crate alloc as __alloc;
```

and use `$crate::__alloc::vec::Vec` in the expansion. The path design should match the crate’s platform contract.

### Local helper bindings and labels

Declarative hygiene protects many local identifiers introduced inside a macro from accidentally capturing caller bindings, but you should still create the smallest possible scope.

```rust
macro_rules! evaluate_once {
    ($expression:expr) => {{
        let __value = $expression;
        __value
    }};
}
```

The generated block keeps the binding local. A distinctive name helps diagnostics, but the scope is the stronger defense.

Labels and local variables have hygiene behavior distinct from item paths. Do not generalize one example into “all generated identifiers are private.” Generated public functions, constants, modules, and types enter ordinary namespaces and can conflict with other generated or handwritten items.

For item names, prefer one of these designs:

- require the caller to supply the generated name;
- generate a name derived from the attached item in a procedural macro with a documented convention;
- keep generated helpers inside a private module or associated implementation;
- avoid generating named helpers when an anonymous block or const expression suffices.

### Textual and path-based macro scope

`macro_rules!` macros have both textual and path-based scoping behavior.

A local macro can be available after its definition in textual scope without a `use` item. Exported macros can be imported and invoked through paths. The details matter when two macros share a name or when definitions occur inside modules.

Reader-first design avoids relying on surprising textual scope across distant files. For public macros:

- export intentionally with `#[macro_export]` when root export is desired;
- document the import form;
- invoke through an explicit path in examples where it improves clarity;
- avoid shadowing a public macro with a local macro of the same name;
- keep internal helper macros near their use and use distinctive internal arms where possible.

Do not assume macro location mirrors module location. `#[macro_export]` exports the macro at the crate root macro namespace, even if its source definition is nested.

### Re-exporting macros

A library can re-export a macro through an ordinary `pub use` path. This is often clearer than asking users to know the source module.

```rust
pub use crate::registry;
```

For procedural macros, re-exporting from a runtime crate is a standard way to offer one public dependency:

```rust
pub use commandforge_macros::{command_catalog, command_handler, CommandArgs};
```

The proc-macro crate remains a separate package because Rust requires procedural macros to be defined in a `proc-macro` crate. The runtime crate can present a unified user-facing API.

### Dependency renaming and procedural macros

Procedural macros do not have `$crate`. Their output behaves as if written into the caller’s code. A generated absolute path such as `::commandforge::CommandArgs` assumes that the runtime dependency is available under the name `commandforge`.

Production macro libraries use several strategies:

1. require and document a fixed runtime crate name;
2. accept a helper attribute specifying the runtime path;
3. generate code that refers only to caller-owned items;
4. use a crate-name discovery helper such as `proc-macro-crate`;
5. re-export the procedural macro and keep expansion paths inside one known facade contract.

Each strategy has costs. Course 5’s capstone is a single integrated package and uses `extern crate self as commandforge;` so generated `::commandforge::...` paths work inside the crate. The chapter names that constraint rather than pretending the macro is already a general-purpose published derive.

A production library intended for arbitrary dependency renaming would need an explicit path strategy before release.

### Visibility is part of generated API design

Suppose an attribute macro emits a public constant beside a public function. The function’s visibility may need to carry over:

```rust
pub struct HandlerDescriptor {
    pub name: &'static str,
}

pub fn add() {}

pub const ADD_HANDLER: HandlerDescriptor = HandlerDescriptor { name: "add" };
```

If the macro emits the constant privately, a catalog in another module may fail. If it always emits the constant publicly, a private handler unexpectedly creates public surface.

A good transformation specifies:

- which original visibility is preserved;
- which generated items share that visibility;
- which helper items are private;
- whether generated names are stable API;
- which module is expected to host the invocation.

Do not “fix” visibility errors by making every helper `pub`. That broadens the compatibility contract and can expose types that were never designed for callers.

### Cross-crate tests are mandatory for exported macros

Unit tests beside a macro definition cannot prove downstream resolution. Create a real consumer crate or integration test that compiles as an external crate.

Test at least:

- invocation from the defining crate;
- invocation from another crate;
- invocation inside a nested module;
- caller-supplied relative and absolute handler paths;
- renamed dependency;
- absent convenience imports;
- a name in the caller that could shadow an unqualified generated path;
- intended visibility failure for inaccessible helpers.

The Module 44 laboratory includes a `consumer` package whose dependency key deliberately differs from the package name. The macro must continue to reach its defining-crate entry type through `$crate`.

### A path ledger

For every generated path, record one of four owners:

| Path | Owner | Typical form |
|---|---|---|
| runtime support type | defining crate | `$crate::Type` for `macro_rules!` |
| caller handler | invocation site | captured `$handler:path` |
| standard library | language environment | `::std::...` or facade re-export |
| generated sibling | macro expansion | caller-supplied name or documented generated name |

If you cannot classify a path, the expansion is not ready for public use.

## Use the idea in a complete program

CommandForge’s declarative diagnostic macro will expand inside the `commandforge` runtime crate. It uses `$crate` for the generated support table type and standard absolute paths for formatting traits where appropriate. Later procedural macros will be re-exported from the runtime crate and generate paths through `::commandforge` under a documented integrated-crate assumption.

For this increment:

1. move the diagnostic catalog invocation into a nested module;
2. remove all local imports that the expansion should not need;
3. add `extern crate self as commandforge;` at the library root for future procedural expansions;
4. test that generated public items are accessible exactly where intended;
5. document every generated path in a path ledger.

The independent [Exported Registry Macro](../../labs/module-04-exported-registry-macro/README.md) proves the harder declarative case: a downstream crate renames the dependency and supplies its own handler paths.

## Practice sequence

1. Hand-expand a public macro and classify every identifier by owner.
2. Replace defining-crate literal paths with `$crate` where appropriate.
3. Remove accidental reliance on caller imports.
4. Test a macro from a nested module with a shadowing local type.
5. Rename the dependency in a consumer manifest and repair resolution.
6. Review generated visibility and reduce unnecessary `pub` surfaces.
7. Build the exported-registry laboratory.
8. Complete CommandForge’s path ledger.

## Ready to continue

Continue when you can explain, for every name in an expansion:

- where it originates;
- where it resolves;
- whether dependency renaming affects it;
- whether privacy permits access;
- whether it becomes public API;
- how a downstream test proves the claim.

Do not continue if your macro works only because the caller imported the same helpers as the defining module.

## Primary Rust references

- Rust Reference, macro scoping, exporting, and importing: <https://doc.rust-lang.org/reference/macros-by-example.html#scoping-exporting-and-importing>
- Rust Reference, `$crate`: <https://doc.rust-lang.org/reference/macros-by-example.html#hygiene>
- Rust Reference, procedural macro hygiene: <https://doc.rust-lang.org/reference/procedural-macros.html#procedural-macro-hygiene>
- Rust Reference, visibility and privacy: <https://doc.rust-lang.org/reference/visibility-and-privacy.html>

## Continue

1. Complete the [Module 44 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 44 — Exported Registry Macro](../../labs/module-04-exported-registry-macro/README.md) from its public contract.
3. Apply the Module 44 increment in the [CommandForge engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
