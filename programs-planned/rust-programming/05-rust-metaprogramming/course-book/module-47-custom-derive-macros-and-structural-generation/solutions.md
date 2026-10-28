# Reasoned solutions — Module 47: Custom Derive Macros and Structural Generation

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the CommandForge engineering guide](../capstone.md)

Use this file after freezing an independent attempt. In this module, compare compilation for lifetime, type, const, and where-clause fixtures, absence of unnecessary field-type bounds, causal errors for tuple structs, enums, and unions, one normalized interpretation of helper attributes. A different implementation is valid only when those contracts survive; matching the reference token-for-token is irrelevant.

## Compiler specimen reasoning

### 1. `case-01/`

- **Outcome:** `compile-pass`
- **Governing rule:** derive macros can preserve generic parameters without adding unrelated bounds.
- **Causal explanation:** The specimen compiles because derive macros can preserve generic parameters without adding unrelated bounds.
- **Principled repair:** preserve generics with split_for_impl
- **Weak repair to reject:** drop generics from the generated impl

### 2. `case-02/`

- **Outcome:** `compile-pass`
- **Governing rule:** derive input includes enum declarations as well as structs.
- **Causal explanation:** The specimen compiles because derive input includes enum declarations as well as structs.
- **Principled repair:** retain the documented broad support
- **Weak repair to reject:** assume every derive receives named fields

### 3. `case-03/`

- **Outcome:** `compile-fail`
- **Governing rule:** derive-generated associated items use ordinary Rust namespaces.
- **Causal explanation:** The compiler rejects the specimen because derive-generated associated items use ordinary Rust namespaces.
- **Principled repair:** choose a noncolliding contract or avoid duplicate derive output
- **Weak repair to reject:** assume derives have a private namespace

### 4. `case-04/`

- **Outcome:** `compile-pass`
- **Governing rule:** a structural derive can generate metadata without field-type trait bounds.
- **Causal explanation:** The specimen compiles because a structural derive can generate metadata without field-type trait bounds.
- **Principled repair:** avoid unrelated bounds
- **Weak repair to reject:** require every field to implement Display

### 5. `case-05/`

- **Outcome:** `compile-fail`
- **Governing rule:** a derive should reject unsupported input explicitly.
- **Causal explanation:** The compiler rejects the specimen because a derive should reject unsupported input explicitly.
- **Principled repair:** use a supported struct or extend the documented semantics
- **Weak repair to reject:** emit an empty implementation for every unsupported item

### 6. `case-06/`

- **Outcome:** `compile-pass`
- **Governing rule:** existing where clauses are preserved in generated implementations.
- **Causal explanation:** The specimen compiles because existing where clauses are preserved in generated implementations.
- **Principled repair:** retain split_for_impl output
- **Weak repair to reject:** reconstruct generics from identifier text

### 7. `case-07/`

- **Outcome:** `compile-fail`
- **Governing rule:** derive output is subject to ordinary generic well-formedness.
- **Causal explanation:** The compiler rejects the specimen because derive output is subject to ordinary generic well-formedness.
- **Principled repair:** use a type satisfying the original bound
- **Weak repair to reject:** blame the derive for an original item constraint

### 8. `case-08/`

- **Outcome:** `compile-pass`
- **Governing rule:** unit structs have a defined zero-field structural result.
- **Causal explanation:** The specimen compiles because unit structs have a defined zero-field structural result.
- **Principled repair:** document unit-struct behavior
- **Weak repair to reject:** reject every non-named struct without reason

## How to review the compiler specimens

The machine-readable outcomes are in [`compiler-labs/manifest.json`](../../compiler-labs/manifest.json). For **derive structure and generic preservation**, compare your prediction against five questions:

1. Which `DeriveInput` forms are supported, and are unsupported structs, enums, and unions rejected deliberately?
2. Are lifetimes, type parameters, const parameters, defaults, and existing where predicates preserved?
3. Are added bounds limited to the field types whose behavior the generated implementation actually uses?
4. Does helper-attribute parsing reject unknown keys, duplicates, and contradictory options at the right span?
5. Does the derive leave semantic trait satisfaction to ordinary Rust type checking rather than guessing from tokens?

Diagnostic prose may change between compiler releases. The isolated source shape and governing phase are the durable evidence.

## Broken-design repair

**Step 1.** Parse the complete `DeriveInput` and classify struct, enum, and union forms explicitly.

**Step 2.** Define the supported input set. Reject unsupported forms with a diagnostic at the relevant item or field rather than producing meaningless output.

**Step 3.** Use `split_for_impl()` and preserve every generic parameter and existing where predicate. Add bounds only for fields that generated behavior actually uses.

**Step 4.** Parse helper attributes through one documented grammar, reject unknown keys and duplicates, and attach errors to the offending metadata.

**Step 5.** Generate the smallest implementation. Let Rust name resolution and trait checking establish semantic facts the derive cannot know from syntax alone.

The repaired design should make **derive structure and generic preservation** smaller and more inspectable than the broken proposal. Judge it by whether one declaration owns the mechanical relationship, the expanded Rust remains readable, and each invalid input fails in the earliest phase that possesses the necessary information.

## Exercise reasoning

### Exercise 1 — Generic preservation

Use the original generics split into implementation generics, type generics, and where clause: conceptually `impl<T, const N: usize> Trait for Pair<T, N> where T: Clone`. The derive must not drop const parameters, lifetimes, defaults, or existing predicates.

### Exercise 2 — Minimal bounds

No field-type bound is required because the implementation reads syntax-level field identifiers and emits static strings. Adding bounds would reject valid types and reveal that the implementation was copied from a different derive purpose.

### Exercise 3 — Input support table

A coherent contract can support named structs, return an empty list for unit structs if documented, and reject tuple structs, enums, and unions because positional or variant fields require a different API. The key is explicit behavior, not maximum acceptance.

### Exercise 4 — Attribute grammar

Each field may have at most one helper attribute policy. Unknown keys, duplicate `skip`, duplicate `rename`, simultaneous `skip` and `rename`, non-string rename values, and empty names should be diagnosed. The grammar should not silently ignore metadata.

### Exercise 5 — Syntax versus semantics

No. Syntax inspection sees a path spelling, not final name resolution. Structural special-casing of `Option` is a convention and can be shadowed. When semantics matter, generate trait-based code or document a restricted syntactic contract with care.

### Exercise 6 — Union rejection

A union is valid Rust and user input may legitimately reach the derive. It is not an internal invariant violation. A spanned compile error explains the supported surface; panic hides context, and empty output falsely suggests success.

## Laboratory comparison

The reference implementation is in [`labs/module-07-field-names-derive/solution`](../../labs/module-07-field-names-derive/solution). Review it in this order:

1. compilation for lifetime, type, const, and where-clause fixtures;
2. absence of unnecessary field-type bounds;
3. causal errors for tuple structs, enums, and unions;
4. one normalized interpretation of helper attributes;

Keep your implementation when its **derive structure and generic preservation** contract is at least as precise with a clearer or smaller design. Revise it when the reference exposes an accepted input, failure phase, generated-name rule, evaluation effect, or determinism obligation missing from your tests.

## Capstone review

For the Module 47 increment, a strong result demonstrates **deriving lawful behavior from item structure while preserving generics, where clauses, attributes, and the boundary between syntax and type checking**. The capstone should still read primarily as ordinary Rust. Generated surfaces must be compact enough to inspect through tests or expansion tools, and runtime domain behavior must remain callable without understanding macro internals.

## What a strong explanation includes

A strong defense of this module explains:

- why derive inspects syntax rather than resolved field semantics;
- how `split_for_impl` preserves the source declaration;
- why skipped fields must not acquire bounds;
- which helper-attribute change would be breaking;
- how the generated ordinary Rust can be inspected and tested without trusting the generator blindly;
- which simpler non-macro design was considered and why it is insufficient for this exact source-of-truth relationship.
