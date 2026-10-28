# 46 — Procedural Macro Execution and TokenStream Engineering

**Course 5, day 6 · Module 46 of 90**  
`███████████████░░░░░` **46/90**

[← Module 45: Macro Diagnostics, Testing, and Public API Design](../module-45-macro-diagnostics-testing-and-public-api-design/index.md) · [Course 5 overview](../index.md) · [Ninety-module map](../../../COURSE_MAP.md) · [Module 47: Custom Derive Macros and Structural Generation →](../module-47-custom-derive-macros-and-structural-generation/index.md)

## The question

> What does the compiler actually give a procedural macro, what can the macro know, and how should tokens, spans, errors, and effects be handled?

## Why this comes now

The first five days established conservative mechanism choice, declarative grammar, recursive parsing, path discipline, diagnostics, and public testing. Procedural macros now enter as compiler-executed Rust programs with a broader parsing and validation surface. Without the earlier discipline, their power encourages exactly the wrong design: a large hidden compiler inside every derive or attribute.

Module 46 stays close to the raw `proc_macro` API. You will see the token boundary before `syn` and `quote` make it convenient.

## What you will be able to do

- Explain when and how a procedural macro executes.
- Distinguish `TokenStream`, `TokenTree`, `Group`, `Ident`, `Punct`, `Literal`, and `Span`.
- Avoid treating token text as a fully resolved Rust AST.
- Emit deterministic tokens and source-local diagnostics.
- Separate parsing, validation, normalization, and generation.
- Recognize procedural macro security and reproducibility concerns.
- Build a raw token inspector that exposes lexical structure without pretending to perform type analysis.

## Core model

### A procedural macro is a compiler-time program

A procedural macro is defined in a crate whose library target has:

```toml
[lib]
proc-macro = true
```

The compiler loads that crate and calls exported macro functions during compilation of a dependent crate. The three stable forms are:

```rust
#[proc_macro]
pub fn function_like(input: TokenStream) -> TokenStream;

#[proc_macro_derive(Name, attributes(helper))]
pub fn derive(input: TokenStream) -> TokenStream;

#[proc_macro_attribute]
pub fn attribute(args: TokenStream, item: TokenStream) -> TokenStream;
```

The functions exist at the crate root, use the compiler-provided `proc_macro::TokenStream`, and return tokens that replace or supplement the invocation according to the macro form.

A procedural macro is not executed in the final program. Its output is compiled into the final program.

### The execution environment is part of the threat model

Procedural macros run with the compiler process’s resources. They can read files, inspect environment variables, write output, access standard input and output, and perform arbitrary safe or unsafe Rust operations allowed by their dependencies.

That creates the same broad security concern as build scripts: adding a proc-macro dependency means executing third-party code during compilation.

A production review should ask:

- Which proc-macro crates and transitive dependencies execute?
- Are versions pinned or audited?
- Does the macro read undeclared files or environment variables?
- Does output depend on current time, network access, directory order, locale, or host state?
- Can ordinary parsing and code generation remain deterministic?
- Are errors printed to stderr, returned as tokens, or hidden behind a panic?

Course 5 macros perform deterministic token transformations and do not access the network or filesystem. Module 50 isolates filesystem generation in a build script with declared inputs.

### `TokenStream` is not source text

A `TokenStream` is a sequence of token trees. The primary variants are:

- `TokenTree::Group` — a delimited nested stream;
- `TokenTree::Ident` — an identifier;
- `TokenTree::Punct` — one punctuation character with spacing information;
- `TokenTree::Literal` — a literal token.

Consider:

```rust
handler(path::to::<Type>(value + 1))
```

The outer input contains identifiers and punctuation plus a parenthesized group. Multi-character operators and path separators are represented through adjacent punctuation tokens whose `Spacing` indicates whether they are joint with the next punctuation.

A string representation such as `input.to_string()` is useful for debugging, but it is not a stable parser interface. Converting tokens to a string and splitting on commas loses group structure, literal escaping, punctuation spacing, and reliable spans.

### Groups preserve delimiters

A `Group` contains:

- a delimiter: parentheses, braces, brackets, or none;
- an inner `TokenStream`;
- a span.

Recursive inspection should preserve group boundaries:

```rust
fn describe(stream: TokenStream, depth: usize, out: &mut String) {
    for tree in stream {
        match tree {
            TokenTree::Group(group) => {
                // record delimiter and recurse into group.stream()
            }
            TokenTree::Ident(ident) => { /* record ident */ }
            TokenTree::Punct(punct) => { /* char + spacing */ }
            TokenTree::Literal(literal) => { /* literal text */ }
        }
    }
}
```

The Module 46 laboratory expands to a string literal describing exactly this structure. It does not claim that an identifier is a type, value, module, or macro, because name resolution has not established that meaning.

### Spans are source relationships

Every token carries a `Span`. Spans support diagnostics and influence name resolution for generated tokens. Stable `proc_macro::Span` is intentionally opaque; you cannot inspect or rewrite every property arbitrarily.

The practical rules are:

- preserve source spans when forwarding caller tokens;
- attach an error to the token that violates the input contract;
- use call-site spans for genuinely generated syntax unless another source token is the better origin;
- do not fabricate broad errors at the entire invocation when one field caused the problem;
- do not claim spans reveal semantic information such as the resolved definition.

With `syn`, `Error::new_spanned` and `Spanned` make this easier. The raw API still teaches the responsibility: an error should point to the source construct the reader can repair.

### Procedural macros are unhygienic

The Rust Reference describes procedural macro output as behaving as if it were written inline at the invocation. Generated paths can be affected by surrounding imports and can affect surrounding namespaces.

Use absolute paths for standard-library items:

```rust
::std::option::Option
::std::result::Result
```

Use a deliberate runtime-crate path for support types. Avoid common generated helper names. Prefer associated items, private modules, or names derived from the attached item where that policy is documented.

Unlike `macro_rules!`, there is no `$crate` token in procedural output. Module 44’s path strategies therefore remain relevant.

### Parsing is a separate phase

A strong proc macro has a pipeline:

```text
compiler TokenStream
    ↓
syntax parser
    ↓
syntax model / AST
    ↓
semantic validation
    ↓
normalized model
    ↓
code generation
    ↓
output TokenStream
```

Do not mix all phases in one match over tokens.

#### Syntax parsing

Syntax parsing answers questions such as:

- Is this a struct, enum, function, or custom DSL entry?
- Is the required comma present?
- Is a value a string literal?
- Is an attribute key known?

#### Semantic validation

Semantic validation answers relationships over the parsed model:

- Are two route keys duplicated?
- Is a field attribute used twice?
- Is this item kind supported by the derive?
- Does the handler have exactly one argument?
- Are two configuration options mutually exclusive?

#### Generated type checking

The Rust compiler should answer semantic type questions:

- Does a field type implement `FromStr`?
- Does a handler return the required result type after aliases resolve?
- Is a generated trait bound satisfied?
- Is a caller-supplied path visible and callable?

The macro may inspect syntax for a better early error, but it must not present textual path matching as full type checking.

### Error reporting: panic versus `compile_error!`

A procedural macro can report failure by panicking or by returning tokens containing `compile_error!`.

Panics are appropriate for bugs in the macro implementation, not for ordinary invalid input. A panic often produces “procedural macro panicked” and leaks internal context rather than a product-level repair.

Invalid source should become a source-located compiler error. With the raw API, you can construct a `compile_error!` invocation. With `syn`, return `syn::Error::to_compile_error()`.

A macro entry point often follows this boundary:

```rust
#[proc_macro]
pub fn command_catalog(input: TokenStream) -> TokenStream {
    match expand_command_catalog(input.into()) {
        Ok(tokens) => tokens.into(),
        Err(error) => error.to_compile_error().into(),
    }
}
```

The exported function is thin. Ordinary helper functions own parsing, validation, and generation, which makes them testable without invoking the compiler entry point directly.

### Accumulating independent errors

Suppose a derive finds two fields with unsupported duplicate helper attributes. After the item is parsed reliably, both errors can be reported in one compile:

```rust
let mut errors: Option<syn::Error> = None;

fn push_error(slot: &mut Option<syn::Error>, error: syn::Error) {
    if let Some(existing) = slot {
        existing.combine(error);
    } else {
        *slot = Some(error);
    }
}
```

Do not continue if the AST itself is invalid. Error aggregation is for independent checks over trustworthy structure, not for manufacturing cascades after a missing delimiter.

### Deterministic generation

Given the same input tokens and declared configuration, output should be stable.

Avoid:

- iterating an unordered `HashMap` into generated item order;
- embedding current timestamps;
- using random identifiers without a stable derivation;
- reading the current directory implicitly;
- depending on host locale;
- formatting tokens through unstable debug output as a semantic step.

Use source order where it is meaningful. Sort explicitly where canonical order is the contract. Keep generated identifiers deterministic and collision-resistant through documented namespacing.

### Token generation approaches

#### Raw token construction

The standard `proc_macro` API can construct `Ident`, `Punct`, `Literal`, `Group`, and `TokenStream` values manually. This is useful for understanding or very small outputs, but verbose for full Rust items.

#### Parsing generated strings

Building a Rust source string and calling `.parse()` is tempting. It loses structured spans, invites escaping errors, and makes interpolation difficult. Keep it for tiny educational examples such as emitting one string literal in the token-inspector lab.

#### `quote`

`quote!` writes Rust-like syntax and interpolates syntax values:

```rust
let name = &input.ident;
let expanded = quote::quote! {
    impl #name {
        pub const GENERATED: bool = true;
    }
};
```

`quote` produces `proc_macro2::TokenStream`, which converts to compiler `TokenStream` at the entry boundary. It is the standard choice for Modules 47–49.

### `proc_macro2` separates compiler entry from ordinary logic

The compiler-provided `proc_macro` types are available only in procedural macro context. `proc_macro2` offers compatible token types usable in tests, build scripts, and ordinary libraries.

A clean architecture is:

```text
#[proc_macro] entry
    proc_macro::TokenStream
        ↓ into
ordinary expand function
    proc_macro2::TokenStream
        ↓
    syn parsing + validation + quote generation
        ↓ into
    proc_macro::TokenStream
```

This keeps the compiler-specific boundary thin and makes expansion logic unit-testable.

### Compile-time cost is product cost

Proc macros add compilation work and often bring parsing dependencies. `syn` feature flags exist partly to control that cost. Enable only what the macro needs.

A derive inspecting structs and enums may need the default `derive`, `parsing`, `printing`, and `proc-macro` features. An attribute parsing full functions requires `full`. `extra-traits` is useful for tests and debugging but should be justified.

Do not claim a macro is “zero cost” because runtime code is unchanged. Build time, dependency graph, cache invalidation, diagnostics, and editor responsiveness are real costs.

## Use the idea in a complete program

CommandForge introduces its `commandforge-macros` crate in this module. The first implementation is intentionally small:

- configure `[lib] proc-macro = true`;
- pin `proc-macro2`, `quote`, and `syn`;
- create thin entry points that call ordinary expansion functions;
- add a raw `token_structure!` experiment used only in tests;
- document that no filesystem or environment input is read;
- establish an error conversion boundary that returns `compile_error!` tokens for invalid source.

Do not implement the final derive or DSL yet. The goal is to establish the compiler boundary correctly before adding item semantics.

The independent [TokenStream Inspector](../../labs/module-06-token-stream-inspector/README.md) uses only `proc_macro`. It recursively describes groups, identifiers, literals, punctuation, and spacing, proving what the compiler provides and what it does not.

## Practice sequence

1. Draw the full expansion pipeline for a procedural macro.
2. Inspect a nested token stream and preserve group boundaries.
3. Compare `TokenStream::to_string()` with structural token inspection.
4. Emit one source-located `compile_error!` rather than panicking.
5. Separate a macro entry point from an ordinary expansion function.
6. Identify every environmental input a proc macro could accidentally read.
7. Build the token-stream inspector laboratory.
8. Establish CommandForge’s proc-macro crate and thin entry boundary.

## Ready to continue

Continue when you can explain:

- when the macro executes;
- what token structure it receives;
- what spans can and cannot establish;
- why token text is not a resolved AST;
- where syntax parsing ends and semantic validation begins;
- why invalid input should not panic;
- how deterministic output is established;
- what build-time security and cost the dependency introduces.

Do not continue if your proc macro is one large function converting the input to a string, splitting it, and parsing generated source text back into tokens.

## Primary Rust references

- Rust Reference, procedural macros: <https://doc.rust-lang.org/reference/procedural-macros.html>
- Standard library `proc_macro`: <https://doc.rust-lang.org/proc_macro/>
- `proc_macro::TokenTree`: <https://doc.rust-lang.org/proc_macro/enum.TokenTree.html>
- `proc_macro2` documentation: <https://docs.rs/proc-macro2/1.0.107/proc_macro2/>
- `quote` documentation: <https://docs.rs/quote/1.0.47/quote/>

## Continue

1. Complete the [Module 46 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 46 — TokenStream Inspector](../../labs/module-06-token-stream-inspector/README.md) from its public contract.
3. Apply the Module 46 increment in the [CommandForge engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
