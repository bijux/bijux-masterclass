# Reasoned Solutions — Module 49: Function-Like Procedural Macros and Typed DSLs

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-09-route-table-dsl/README.md) · [CommandForge guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 49: Function-Like Procedural Macros and Typed DSLs**. Compare the reasoning against this question: *How do you turn custom syntax into an AST, validate cross-entry semantics, normalize the model, and generate compact typed Rust?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `case-01/`

- **Outcome:** `compile-pass`
- **Governing rule:** function-like procedural macros can parse a custom comma-separated grammar.
- **Causal explanation:** The specimen compiles because function-like procedural macros can parse a custom comma-separated grammar.
- **Principled repair:** retain a closed grammar
- **Weak repair to reject:** split source text by commas

### 2. `case-02/`

- **Outcome:** `compile-fail`
- **Governing rule:** cross-entry uniqueness is a semantic validation rule.
- **Causal explanation:** The compiler rejects the specimen because cross-entry uniqueness is a semantic validation rule.
- **Principled repair:** report the later duplicate
- **Weak repair to reject:** let hash insertion overwrite the first

### 3. `case-03/`

- **Outcome:** `compile-fail`
- **Governing rule:** explicit separators are part of a DSL grammar.
- **Causal explanation:** The compiler rejects the specimen because explicit separators are part of a DSL grammar.
- **Principled repair:** add the required separator
- **Weak repair to reject:** accept whitespace as an implicit separator through string parsing

### 4. `case-04/`

- **Outcome:** `compile-pass`
- **Governing rule:** an empty grammar can have a deliberate normalized result.
- **Causal explanation:** The specimen compiles because an empty grammar can have a deliberate normalized result.
- **Principled repair:** document empty-catalog behavior
- **Weak repair to reject:** let emptiness fail accidentally in generation

### 5. `case-05/`

- **Outcome:** `compile-fail`
- **Governing rule:** the emitted value still has an ordinary Rust type.
- **Causal explanation:** The compiler rejects the specimen because the emitted value still has an ordinary Rust type.
- **Principled repair:** use the generated slice in a compatible context
- **Weak repair to reject:** claim the DSL bypasses type checking

### 6. `case-06/`

- **Outcome:** `compile-pass`
- **Governing rule:** normalized generation can preserve authored source order.
- **Causal explanation:** The specimen compiles because normalized generation can preserve authored source order.
- **Principled repair:** retain source-order contract
- **Weak repair to reject:** emit from a hash map

### 7. `case-07/`

- **Outcome:** `compile-fail`
- **Governing rule:** a DSL parser should reject unsupported literal categories locally.
- **Causal explanation:** The compiler rejects the specimen because a DSL parser should reject unsupported literal categories locally.
- **Principled repair:** use an identifier or extend the grammar with semantics
- **Weak repair to reject:** accept arbitrary token trees and stringify them

### 8. `case-08/`

- **Outcome:** `compile-pass`
- **Governing rule:** generated static data can be consumed through ordinary iterator APIs.
- **Causal explanation:** The specimen compiles because generated static data can be consumed through ordinary iterator APIs.
- **Principled repair:** keep runtime behavior ordinary
- **Weak repair to reject:** generate custom iteration syntax unnecessarily

## How to review the compiler specimens

The machine-readable outcomes are in [`compiler-labs/manifest.json`](../../compiler-labs/manifest.json). For **DSL phase separation and normalization**, compare your prediction against five questions:

1. Is the grammar written independently from the implementation and unambiguous at every separator?
2. Does parsing produce an AST before semantic checks such as duplicate routes or incompatible declarations?
3. Are diagnostics able to name both the first declaration and the conflicting declaration?
4. Does normalization preserve the source distinctions needed for accurate errors and deterministic output?
5. Is generated code a simple rendering of a validated model rather than a second place where semantics are decided?

Diagnostic prose may change between compiler releases. The isolated source shape and governing phase are the durable evidence.

## Broken-design repair

**Step 1.** Write the grammar and parse it into an AST that preserves source spans for every declaration.

**Step 2.** Validate syntax-independent rules over the AST: duplicate names, duplicate routes, unsupported methods, empty literals, and incompatible options.

**Step 3.** Normalize only after successful validation. Choose deterministic order deliberately—source order or sorted order—and state it as contract.

**Step 4.** Generate compact ordinary Rust from the normalized model. Keep type and handler paths as parsed Rust syntax, not strings.

**Step 5.** Attach semantic errors to the later conflicting entry while mentioning the original declaration where practical. Add malformed-input and deterministic-expansion tests.

The repaired design should make **DSL phase separation and normalization** smaller and more inspectable than the broken proposal. Judge it by whether one declaration owns the mechanical relationship, the expanded Rust remains readable, and each invalid input fails in the earliest phase that possesses the necessary information.

## Exercise reasoning

### Exercise 1 — Five-stage trace

Tokens preserve identifiers, literal, punctuation, and spans. The AST stores a route entry with method, path literal, handler path, and spans. Validation checks supported method, path shape, and uniqueness. Normalization may convert the method into an enum and retain source order. Generation emits a typed table and dispatch arms using the handler path.

### Exercise 2 — Parser/validator split

Duplicates are a cross-entry semantic rule, not a local grammar rule. Keeping the parser responsible only for structure yields a reusable AST, clearer errors, and simpler tests. The validator can inspect all entries without entangling token advancement.

### Exercise 3 — Terminator contract

Requiring a terminator makes boundaries unambiguous, improves missing-entry diagnostics, and leaves room for richer field syntax. Optional terminators may look friendly but create ambiguous recovery and compatibility constraints. CommandForge should require explicit semicolons.

### Exercise 4 — Duplicate diagnostics

Store the first name’s span in a map during validation. When a duplicate appears, create an error at the later name and optionally combine a note/error at the first span. Do not silently keep first or last unless duplicate resolution is an explicit runtime policy.

### Exercise 5 — Determinism

Source order is usually best when authors intentionally order help and dispatch tables; it is deterministic because the input is ordered. Sorting can provide canonical output but changes authored presentation. Choose one and test it; never inherit hash-map order accidentally.

### Exercise 6 — Type-checker boundary

The DSL can require syntactic paths and cross-entry uniqueness. Rust should resolve those paths, check visibility, confirm descriptor types, and verify handler/argument compatibility through generated typed expressions. Reimplementing type checking from token spelling is brittle.

## Reference implementation comparison

The reference implementation is in [`labs/module-09-route-table-dsl/solution`](../../labs/module-09-route-table-dsl/solution). Review it in this order:

1. separation of parse and semantic errors;
2. diagnostics carrying both declarations for duplicates;
3. one normalized representation driving all output;
4. generated code small enough to inspect;

Keep your implementation when its **DSL phase separation and normalization** contract is at least as precise with a clearer or smaller design. Revise it when the reference exposes an accepted input, failure phase, generated-name rule, evaluation effect, or determinism obligation missing from your tests.

## Capstone review

For the Module 49 increment, a strong result demonstrates **building a typed DSL through grammar, AST, semantic validation, normalization, and deterministic code generation**. The capstone should still read primarily as ordinary Rust. Generated surfaces must be compact enough to inspect through tests or expansion tools, and runtime domain behavior must remain callable without understanding macro internals.

## What a strong explanation includes

A strong defense of this module explains:

- why a single parse-and-emit function is difficult to review;
- which rules require cross-entry state;
- which relationships should be delegated to the type checker;
- what size or volatility would make a data file preferable;
- how the generated ordinary Rust can be inspected and tested without trusting the generator blindly;
- which simpler non-macro design was considered and why it is insufficient for this exact source-of-truth relationship.

## Deep reasoning and transfer

### Decisive model

> How do you turn custom syntax into an AST, validate cross-entry semantics, normalize the model, and generate compact typed Rust?

Build a **DSL syntax-to-model map**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Design a bounded custom grammar with explicit compatibility space.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Implement `syn::parse::Parse` for syntax nodes rather than splitting strings.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Separate syntax AST, semantic validation, normalized model, and generation.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Detect duplicates and cross-entry conflicts with useful multi-span errors.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Preserve source order or define canonical order deliberately.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Design a bounded custom grammar with explicit compatibility space.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the DSL syntax-to-model map.

### Laboratory transfer review

For [Route Table DSL](../../labs/module-09-route-table-dsl/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In CommandForge, Module 49 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Function-Like Procedural Macros and Typed DSLs**, which relationship decides this question: “How do you turn custom syntax into an AST, validate cross-entry semantics, normalize the model, and generate compact typed Rust?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to CommandForge?
