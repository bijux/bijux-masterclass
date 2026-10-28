# 48 — Attribute Macros and Item Transformation

**Course 5, day 8 · Module 48 of 60**  
`████████████████░░░░` **48/60**

[← Module 47: Custom Derive Macros and Structural Generation](../module-47-custom-derive-macros-and-structural-generation/index.md) · [Course 5 overview](../index.md) · [Sixty-module map](../../../COURSE_MAP.md) · [Module 49: Function-Like Procedural Macros and Typed DSLs →](../module-49-function-like-procedural-macros-and-typed-dsls/index.md)

## The question

> How do you validate and transform an attached item while preserving the parts of its public contract that the attribute does not own?

## Why this comes now

A derive can inspect an item but cannot replace it. An attribute macro receives configuration tokens and the complete attached item, then replaces that item with its output. This enables wrappers, registration metadata, signature checks, instrumentation, and companion items. It also creates a much larger responsibility: anything not re-emitted disappears.

Module 48 therefore treats transformation as a preservation contract, not as an opportunity to rewrite arbitrary code.

## What you will be able to do

- Parse attribute arguments independently from the attached item.
- Validate supported item kinds and function signatures.
- Preserve visibility, attributes, generics, ABI, safety, asyncness, and body when the macro does not own them.
- Decide whether to preserve, augment, wrap, or replace an item.
- Generate companion metadata and wrappers with collision-resistant names.
- Distinguish syntax-level signature checks from actual type checking.
- Test local behavior, downstream visibility, and invalid transformations.

## Core model

### Attribute macros replace their input

An attribute macro has two inputs:

```rust
#[proc_macro_attribute]
pub fn checked_handler(
    args: TokenStream,
    item: TokenStream,
) -> TokenStream {
    /* ... */
}
```

For:

```rust
#[checked_handler(about = "add two integers")]
pub fn add(args: AddArgs) -> Result<String, CommandError> {
    /* body */
}
```

`args` contains the tokens inside the attribute parentheses. `item` contains the entire function item.

The compiler removes the original attributed item and inserts the output tokens. If the macro forgets to emit the function, the function is gone. If it reconstructs only the signature and loses documentation attributes, those attributes are gone. If it changes visibility accidentally, the API changes.

A derive adds. An attribute transforms.

### Four transformation modes

Name the mode before implementation.

#### Preserve

Validate the item, then emit it unchanged.

Use this when the attribute is a compile-time assertion or marker and no companion surface is needed.

#### Augment

Emit the original item plus additional metadata, implementations, or helper functions.

CommandForge’s handler attribute uses this mode.

#### Wrap

Rename or move the original implementation, then emit a public wrapper around it.

This is useful for instrumentation, authorization, retries, or registration, but it can alter stack traces, generic inference, attributes, and visibility. It needs a stronger contract.

#### Replace

Generate a fundamentally different item. This is the most invasive mode and should be rare. The source syntax becomes a DSL disguised as Rust item syntax.

Do not mix modes implicitly. A reader should know whether the function they wrote remains the function callers invoke.

### Parse configuration as its own grammar

For CommandForge:

```rust
#[command_handler(about = "add two signed integers")]
```

The grammar is:

```text
handler-args = `about` `=` string-literal
```

A production attribute might support additional keys, but each key needs:

- accepted value syntax;
- required or optional status;
- default;
- duplicate policy;
- conflict rules;
- effect on generated output;
- compatibility meaning.

Using `syn::punctuated::Punctuated<Meta, Token![,]>` or a custom `Parse` type makes the grammar explicit. For conventional key-value options, `syn::meta::parser` and nested-meta helpers are useful.

Unknown keys should fail at the key. Duplicate `about` should fail at the second occurrence. An empty string should be accepted or rejected by an explicit product rule, not by accident.

### Parse the attached item at the right level

If the attribute supports functions only, parse `syn::ItemFn` rather than generic `syn::Item` and a later match. A non-function then fails as close as possible to the contract.

```rust
let function = syn::parse::<syn::ItemFn>(item)?;
```

`ItemFn` contains:

- outer attributes;
- visibility;
- signature;
- body block.

The signature includes constness, asyncness, safety, ABI, name, generics, parameters, variadic marker, and return type. Decide which are supported before generation.

### Signature validation is syntax validation

Suppose the handler contract requires one owned argument and a `Result<String, CommandError>` return.

The macro can check:

- exactly one `FnArg::Typed` parameter;
- no receiver;
- no variadic argument;
- no generic parameters if unsupported;
- no `async`, `const`, `unsafe`, or external ABI if unsupported;
- a syntactic return type shaped like `Result<..., ...>`.

It cannot prove that a path spelled `Result` resolves to `std::result::Result`, that a type alias has a particular target, or that the error type implements a conversion. Generated code and the compiler should establish those semantic obligations.

Be honest in diagnostics:

- accurate: “`command_handler` requires an explicit `Result<_, _>` return syntax”;
- inaccurate: “handler does not return `std::result::Result`” when only tokens were inspected.

Sometimes the better design is not to inspect the return syntax at all. Generate a wrapper with an expected function-pointer type or trait bound and let type checking report mismatch. Choose based on diagnostic quality and supported aliases.

### Preservation checklist

Before emitting the original function, audit:

| Surface | Preserve? | Reason |
|---|---:|---|
| documentation attributes | yes | public docs belong to the function |
| lint attributes | yes | caller owns lint policy |
| `cfg` attributes | usually yes | item availability must remain consistent |
| visibility | yes | macro does not own access policy |
| function name | yes | caller selected public symbol |
| generics and where clause | yes or reject | silent loss is invalid |
| ABI and safety | preserve or reject | wrapper semantics differ |
| asyncness and constness | preserve or reject | generated invocation changes |
| body | yes | runtime behavior remains ordinary Rust |

A safe implementation often quotes the parsed `ItemFn` directly:

```rust
quote! {
    #function
    // companion items
}
```

This preserves the syntax represented by `syn`. If attributes consumed by the macro should not remain, remove only those specific attributes intentionally.

### Companion metadata

The lab generates a metadata constant and wrapper function beside the original handler:

```rust
pub const ADD_HANDLER: HandlerDescriptor = HandlerDescriptor {
    about: "add two signed integers",
    invoke: __commandforge_invoke_add,
};
```

The wrapper decodes arguments and calls the original function. Its name is derived deterministically from the function name:

```rust
let wrapper = format_ident!("__commandforge_invoke_{}", function.sig.ident);
```

Generated names create collision risks. A caller could already define that name. Options include:

- generate inside a private module named from the function;
- use an associated const on a generated marker type;
- require a caller-supplied metadata name;
- document a reserved prefix and diagnose collisions when possible.

CommandForge uses a documented `__commandforge_` prefix in a module controlled by the capstone and derives the public descriptor constant from the handler name. That bounded product accepts the reserved namespace. A reusable public macro should prefer an explicit caller-supplied item name or a stronger generated namespace.

### Visibility coupling

If the handler is private and the metadata is public, public API may expose a function pointer to an otherwise private implementation. If the handler is public and metadata is private, another module cannot build the catalog.

Possible policies:

1. generated metadata uses the same visibility as the handler;
2. all handlers must be public within the crate and metadata is `pub(crate)`;
3. the attribute accepts an explicit metadata visibility;
4. the catalog invocation occurs in the same module.

CommandForge requires `pub` handlers and emits public descriptor constants because the capstone exposes its command catalog as a public teaching API. The macro validates that narrow policy instead of silently widening a private function. A reusable library could instead preserve an explicit visibility or accept a metadata-visibility argument.

### Wrapping changes semantics

An instrumentation attribute might generate:

```rust
fn original_name(args: Args) -> Output {
    let started = Instant::now();
    let result = __original_name(args);
    record(started.elapsed());
    result
}
```

This changes:

- function identity;
- backtraces;
- panic paths;
- drop timing;
- async cancellation behavior;
- const eligibility;
- borrow scopes;
- tail-call shape;
- visibility of attributes on the original body.

Do not call this “preserving the function” merely because input and output types match. The wrapper contract must own these changes.

Course 5’s handler attribute avoids behavioral wrapping. It augments the function with decoding metadata and a separate invocation wrapper used by the catalog. Direct calls to the function remain direct.

### Attribute ordering matters

Multiple attributes may transform the same item. Expansion order and whether an attribute is preserved can affect the result.

```rust
#[cfg(feature = "commands")]
#[command_handler(about = "...")]
pub fn add(...) { ... }
```

The generated companion items must follow the same configuration or they may refer to an absent function. Quoting the original `cfg` only on the original function is not enough if companions remain unconditional.

Copy relevant conditional attributes to generated companion items or wrap all output under the same configuration. Be conservative with arbitrary attributes: some are meaningful only on functions and invalid on constants.

Document interactions you support. Do not promise composability with every attribute macro; transformations can be order-dependent.

### Error accumulation for signature problems

After successfully parsing the function, several signature defects may be independent:

- `async` is unsupported;
- there are two parameters;
- generics are unsupported;
- return type is missing.

Combining these can reduce edit-compile cycles. Attach each error to its own token. But if the parameter syntax cannot be interpreted reliably, stop before generating secondary assumptions.

The expansion entry should return all combined errors as `compile_error!` tokens and not emit half-valid companion items.

### Testing an attribute macro

#### Preservation tests

- documentation remains visible;
- visibility remains correct;
- `cfg` behavior applies to companions;
- original function can still be called directly;
- body behavior is unchanged;
- supported generics or deliberate rejection are proved.

#### Generated-surface tests

- metadata name and visibility;
- wrapper function signature;
- handler description;
- decode-then-call order;
- error conversion;
- no duplicate evaluation.

#### Invalid-input tests

- attribute on non-function;
- unknown key;
- duplicate key;
- missing required key;
- unsupported async/const/unsafe/extern/generic form;
- wrong parameter count;
- receiver parameter;
- missing or unsupported return form.

#### Composition tests

- nested module;
- conditional compilation where practical;
- documentation attribute;
- another harmless built-in attribute.

## Use the idea in a complete program

CommandForge’s handler functions remain ordinary domain code:

```rust
#[command_handler(about = "add two signed integers")]
pub fn add(args: AddArgs) -> Result<String, CommandError> {
    args.left
        .checked_add(args.right)
        .map(|value| value.to_string())
        .ok_or(CommandError::Overflow)
}
```

The attribute generates:

- a private decode-and-invoke wrapper;
- a public `HandlerDescriptor` constant under the documented generated name;
- no change to the direct function body;
- no command name, because Module 49’s catalog owns names and uniqueness.

That separation prevents the command name from being repeated in both an attribute and a catalog.

The independent [Checked Handler Attribute](../../labs/module-08-checked-handler-attribute/README.md) validates a smaller function contract and proves preservation before the capstone adds argument decoding.

## Practice sequence

1. Classify an attribute as preserve, augment, wrap, or replace.
2. Write its argument grammar and duplicate policy.
3. Create a preservation table for the attached item.
4. Move semantic type obligations from syntax inspection into generated checking where appropriate.
5. Add source-located errors for unsupported signature features.
6. Test a `cfg`-guarded attributed item and its companions.
7. Complete the checked-handler laboratory.
8. Implement CommandForge’s descriptor generation without duplicating command names.

## Ready to continue

Continue when you can state:

- which transformation mode the attribute uses;
- which item kinds and signatures it supports;
- which original surfaces are preserved or rejected;
- which generated names and visibility are introduced;
- which checks are syntactic versus semantic;
- how configuration attributes affect companions;
- how direct calls differ from catalog-mediated calls;
- what evidence proves the original behavior remains intact.

Do not continue if the macro reconstructs a function from selected fields and silently drops attributes, generics, ABI, or visibility.

## Primary Rust references

- Rust Reference, attribute macros: <https://doc.rust-lang.org/reference/procedural-macros.html#attribute-macros>
- `syn::ItemFn`: <https://docs.rs/syn/3.0.3/syn/struct.ItemFn.html>
- `syn::Signature`: <https://docs.rs/syn/3.0.3/syn/struct.Signature.html>
- `syn::Meta`: <https://docs.rs/syn/3.0.3/syn/enum.Meta.html>
- `quote::format_ident!`: <https://docs.rs/quote/1.0.47/quote/macro.format_ident.html>

## Continue

1. Complete the [Module 48 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 48 — Checked Handler Attribute](../../labs/module-08-checked-handler-attribute/README.md) from its public contract.
3. Apply the Module 48 increment in the [CommandForge engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
