# Reasoned Solutions — Module 44: Hygiene, Scope, Paths, and Cross-Crate Macros

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-04-exported-registry-macro/README.md) · [CommandForge guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 44: Hygiene, Scope, Paths, and Cross-Crate Macros**. Compare the reasoning against this question: *Whose names should generated code resolve, and how do you make exported macros survive nesting, imports, and dependency renaming?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `case-01.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** $crate refers to the defining crate in declarative expansion.
- **Causal explanation:** The specimen compiles because $crate refers to the defining crate in declarative expansion.
- **Principled repair:** retain a fully qualified $crate path
- **Weak repair to reject:** spell a dependency name that downstream code may rename

### 2. `case-02.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** bare generated paths depend on invocation-site scope.
- **Causal explanation:** The compiler rejects the specimen because bare generated paths depend on invocation-site scope.
- **Principled repair:** qualify the definition-owned path
- **Weak repair to reject:** require every caller to add a matching import

### 3. `case-03.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** caller-owned paths should be captured and inserted.
- **Causal explanation:** The specimen compiles because caller-owned paths should be captured and inserted.
- **Principled repair:** capture a path fragment
- **Weak repair to reject:** invent a fixed handler name in expansion

### 4. `case-04.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** $crate does not grant visibility through module privacy boundaries.
- **Causal explanation:** The compiler rejects the specimen because $crate does not grant visibility through module privacy boundaries.
- **Principled repair:** make the expansion support item visible at the required boundary
- **Weak repair to reject:** assume path qualification bypasses privacy

### 5. `case-05.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** block-local generated temporaries do not require caller declarations.
- **Causal explanation:** The specimen compiles because block-local generated temporaries do not require caller declarations.
- **Principled repair:** keep temporaries inside a block
- **Weak repair to reject:** emit a caller-visible fixed local name as API

### 6. `case-06.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** invocation-site identifiers are not invented bindings.
- **Causal explanation:** The compiler rejects the specimen because invocation-site identifiers are not invented bindings.
- **Principled repair:** accept the identifier as a metavariable or generate a self-contained binding
- **Weak repair to reject:** document a magical local variable requirement

### 7. `case-07.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** standard-library paths can be made collision resistant.
- **Causal explanation:** The specimen compiles because standard-library paths can be made collision resistant.
- **Principled repair:** retain explicit paths for generated support types
- **Weak repair to reject:** depend on caller prelude and imports

### 8. `case-08.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** generated public names participate in the ordinary item namespace.
- **Causal explanation:** The compiler rejects the specimen because generated public names participate in the ordinary item namespace.
- **Principled repair:** choose a deliberate naming policy or require the name as input
- **Weak repair to reject:** assume macro hygiene makes public item collisions impossible

## How to review the compiler specimens

The machine-readable outcomes are in [`compiler-labs/manifest.json`](../../compiler-labs/manifest.json). For **hygiene and cross-crate resolution**, compare your prediction against five questions:

1. Which names must resolve in the defining crate and therefore require `$crate`-relative paths?
2. Which identifiers are intentionally supplied by the invocation site?
3. Does the expansion survive dependency renaming and a downstream module that shadows helper names?
4. Are all generated references legal under the defining crate’s public visibility boundary?
5. Does the public macro expose helper implementation details as accidental compatibility commitments?

Diagnostic prose may change between compiler releases. The isolated source shape and governing phase are the durable evidence.

## Broken-design repair

**Step 1.** Classify every name in the expansion as supplied by the invocation, owned by the defining crate, or intentionally resolved at the invocation site.

**Step 2.** Use `$crate::qualified::path` for items owned by the defining crate. Do not assume the downstream dependency name.

**Step 3.** Make every definition-owned item reached by exported expansion publicly visible enough for the invocation site; `$crate` does not bypass visibility.

**Step 4.** Pass caller-owned expressions and paths as metavariables. Do not invent invocation-site local names and assume the caller can see or bind them.

**Step 5.** Test from an integration crate and, for a public package, from a fixture that renames the dependency and uses the macro under shadowing imports.

The repaired design should make **hygiene and cross-crate resolution** smaller and more inspectable than the broken proposal. Judge it by whether one declaration owns the mechanical relationship, the expanded Rust remains readable, and each invalid input fails in the earliest phase that possesses the necessary information.

## Exercise reasoning

### Exercise 1 — Name provenance ledger

Use an absolute standard-library path or prelude-stable path for `Vec` when collision resistance matters; use `$crate` for the helper type; insert the caller handler from a `path` metavariable; choose a deliberately obscure private temporary inside a block; and document any generated public item because its name becomes downstream API.

### Exercise 2 — Dependency rename

Downstream Cargo manifests may rename a dependency, so the source spelling is not stable. `$crate::helper()` resolves to the crate that defined the macro, independent of downstream naming. The helper still needs adequate visibility.

### Exercise 3 — Visibility boundary

`$crate` controls path origin, not privacy. The expanded code is checked at the invocation site, and private items remain inaccessible. Expose a deliberately public hidden support module or emit code that uses public API only.

### Exercise 4 — Caller path capture

`path` best represents a callable path without accepting arbitrary runtime expressions. `ident` is too narrow; `expr` is broader than the declared language. The expansion may call or store the captured path according to its documented contract.

### Exercise 5 — Local collision

Declarative hygiene protects many local identifiers, but generated public names and procedural output behave differently. Keep temporaries inside a block, avoid unnecessary user-visible names, and use uncommon internal names for procedural output. Do not rely on folklore; test shadowing contexts.

### Exercise 6 — Cross-crate fixture

The fixture should be a separate Cargo package with the dependency aliased in `Cargo.toml`, invoke the macro through the alias, define a local type with the same short name as the support type, avoid importing helper items, and call from a nested module. Passing this fixture proves more than an in-crate unit test.

## Reference implementation comparison

The reference implementation is in [`labs/module-04-exported-registry-macro/solution`](../../labs/module-04-exported-registry-macro/solution). Review it in this order:

1. successful use from a renamed downstream dependency;
2. independence from caller imports;
3. privacy of helpers reached through `$crate`;
4. absence of accidental capture or namespace pollution;

Keep your implementation when its **hygiene and cross-crate resolution** contract is at least as precise with a clearer or smaller design. Revise it when the reference exposes an accepted input, failure phase, generated-name rule, evaluation effect, or determinism obligation missing from your tests.

## Capstone review

For the Module 44 increment, a strong result demonstrates **making generated names and paths resolve deliberately across modules, crates, and dependency renaming**. The capstone should still read primarily as ordinary Rust. Generated surfaces must be compact enough to inspect through tests or expansion tools, and runtime domain behavior must remain callable without understanding macro internals.

## What a strong explanation includes

A strong defense of this module explains:

- why `$crate` solves only defining-crate paths;
- which names intentionally resolve at the call site;
- how visibility differs from path resolution;
- what downstream test proves the macro is actually portable;
- how the generated ordinary Rust can be inspected and tested without trusting the generator blindly;
- which simpler non-macro design was considered and why it is insufficient for this exact source-of-truth relationship.

## Deep reasoning and transfer

### Decisive model

> Whose names should generated code resolve, and how do you make exported macros survive nesting, imports, and dependency renaming?

Build a **hygiene and path map**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Distinguish textual scope, path-based scope, and expansion-site lookup for declarative macros.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Use `$crate` for defining-crate references in exported `macro_rules!` expansions.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Preserve invocation-site identifiers supplied by callers.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Avoid accidental dependence on caller imports or prelude contents.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Design visibility so generated code can legally reach helper items.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Distinguish textual scope, path-based scope, and expansion-site lookup for declarative macros.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the hygiene and path map.

### Laboratory transfer review

For [Exported Registry Macro](../../labs/module-04-exported-registry-macro/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In CommandForge, Module 44 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Hygiene, Scope, Paths, and Cross-Crate Macros**, which relationship decides this question: “Whose names should generated code resolve, and how do you make exported macros survive nesting, imports, and dependency renaming?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to CommandForge?
