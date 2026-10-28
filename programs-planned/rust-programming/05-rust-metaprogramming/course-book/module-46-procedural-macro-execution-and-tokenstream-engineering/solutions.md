# Reasoned Solutions — Module 46: Procedural Macro Execution and TokenStream Engineering

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-06-token-stream-inspector/README.md) · [CommandForge guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 46: Procedural Macro Execution and TokenStream Engineering**. Compare the reasoning against this question: *What does the compiler actually give a procedural macro, what can the macro know, and how should tokens, spans, errors, and effects be handled?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `case-01/`

- **Outcome:** `compile-pass`
- **Governing rule:** function-like procedural macros replace an invocation with emitted tokens.
- **Causal explanation:** The specimen compiles because function-like procedural macros replace an invocation with emitted tokens.
- **Principled repair:** retain the expression-position contract
- **Weak repair to reject:** parse emitted token text at runtime

### 2. `case-02/`

- **Outcome:** `compile-fail`
- **Governing rule:** procedural-macro output is checked in the surrounding type context.
- **Causal explanation:** The compiler rejects the specimen because procedural-macro output is checked in the surrounding type context.
- **Principled repair:** use a compatible context or generate the intended type
- **Weak repair to reject:** cast unrelated output until it compiles

### 3. `case-03/`

- **Outcome:** `compile-pass`
- **Governing rule:** token streams preserve top-level token-tree structure.
- **Causal explanation:** The specimen compiles because token streams preserve top-level token-tree structure.
- **Principled repair:** reason about TokenTree rather than whitespace
- **Weak repair to reject:** split input.to_string() on spaces

### 4. `case-04/`

- **Outcome:** `compile-fail`
- **Governing rule:** procedural macros must be imported or path-invoked in the macro namespace.
- **Causal explanation:** The compiler rejects the specimen because procedural macros must be imported or path-invoked in the macro namespace.
- **Principled repair:** import the macro or invoke through its crate path
- **Weak repair to reject:** define a runtime function with the same name

### 5. `case-05/`

- **Outcome:** `compile-pass`
- **Governing rule:** procedural macro output can participate in const expressions when emitted Rust permits it.
- **Causal explanation:** The specimen compiles because procedural macro output can participate in const expressions when emitted Rust permits it.
- **Principled repair:** retain ordinary emitted Rust
- **Weak repair to reject:** claim all procedural macros run at runtime

### 6. `case-06/`

- **Outcome:** `compile-fail`
- **Governing rule:** macro input grammar belongs to the procedural parser.
- **Causal explanation:** The compiler rejects the specimen because macro input grammar belongs to the procedural parser.
- **Principled repair:** supply the documented grammar
- **Weak repair to reject:** convert the entire input to a string and accept anything

### 7. `case-07/`

- **Outcome:** `compile-pass`
- **Governing rule:** a proc macro may emit a borrowed static slice with deterministic source order.
- **Causal explanation:** The specimen compiles because a proc macro may emit a borrowed static slice with deterministic source order.
- **Principled repair:** retain ordered normalized generation
- **Weak repair to reject:** collect through an unordered set for output

### 8. `case-08/`

- **Outcome:** `compile-fail`
- **Governing rule:** semantic validation may reject syntactically valid repeated declarations.
- **Causal explanation:** The compiler rejects the specimen because semantic validation may reject syntactically valid repeated declarations.
- **Principled repair:** remove or rename the duplicate
- **Weak repair to reject:** silently keep the last declaration

## How to review the compiler specimens

The machine-readable outcomes are in [`compiler-labs/manifest.json`](../../compiler-labs/manifest.json). For **token-stream structure and spans**, compare your prediction against five questions:

1. What exact token-tree structure reaches the procedural macro, including groups and punctuation spacing?
2. Which facts are syntactic and available now, and which require later name or type resolution?
3. Do generated spans point diagnostics toward caller-authored tokens rather than opaque generated code?
4. Is expansion deterministic and independent of undeclared process state?
5. Does every error become emitted compiler input rather than a panic from the macro process?

Diagnostic prose may change between compiler releases. The isolated source shape and governing phase are the durable evidence.

## Broken-design repair

**Step 1.** Treat `TokenStream` as structured tokens with groups, identifiers, punctuation, literals, and spans. Do not use source-text splitting as a Rust parser.

**Step 2.** Keep the macro entry point thin: parse into an explicit representation, validate, generate tokens, and convert accumulated errors to compiler output.

**Step 3.** Use spans from the offending input token for diagnostics and generated identifiers derived from user syntax. Use stable call-site spans only for genuinely generated support tokens.

**Step 4.** Avoid file and environment effects unless the mechanism explicitly owns them. Procedural macros run during compilation and carry build-script-like security concerns.

**Step 5.** Generate absolute or runtime-crate-qualified paths, deterministic item order, and no debug output. Return `compile_error!`-equivalent errors rather than panicking for user mistakes.

The repaired design should make **token-stream structure and spans** smaller and more inspectable than the broken proposal. Judge it by whether one declaration owns the mechanical relationship, the expanded Rust remains readable, and each invalid input fails in the earliest phase that possesses the necessary information.

## Exercise reasoning

### Exercise 1 — Token structure

The input is a sequence of identifiers, punctuation tokens (with spacing information), a literal, and path punctuation around `::`; grouped tokens would appear as `Group` values with nested streams. Treating the input as whitespace-delimited text would lose punctuation structure and spans.

### Exercise 2 — Cheap clone meaning

Cheap structural cloning avoids copying a large source string, but parsing, validation, allocation, and generated-code complexity still matter. Clone only when ownership boundaries require it; keep one normalized model so later phases do not reinterpret raw tokens.

### Exercise 3 — Span policy

The unknown key error should point at the key token. The implementation scaffolding can use call-site or quote-propagated spans. A generated identifier that corresponds to a field should generally carry the field’s span so later errors lead back to the source relationship. Span choice is diagnostic design.

### Exercise 4 — Error accumulation

Independent field-local errors can be combined so one compile cycle reports all of them. Errors whose interpretation depends on earlier successful parsing may need early return. The implementation should avoid cascades that report consequences rather than root causes.

### Exercise 5 — Security boundary

It executes during compilation with compiler-process access to files, environment, standard streams, and other resources. Reviewing only generated API shape ignores supply-chain and reproducibility risk. Minimize dependencies and avoid undeclared effects.

### Exercise 6 — Deterministic expansion

Hash-map iteration, filesystem enumeration, environment-dependent paths, and timestamps can vary. Sort semantic entries, validate and order directory inputs explicitly, avoid embedding machine paths, and exclude wall-clock data unless it is a declared input. Determinism reduces rebuild noise and makes testing meaningful.

## Reference implementation comparison

The reference implementation is in [`labs/module-06-token-stream-inspector/solution`](../../labs/module-06-token-stream-inspector/solution). Review it in this order:

1. whether joint punctuation is observed correctly;
2. whether token text is not mistaken for type information;
3. whether output is deterministic;
4. whether span claims are limited to supported behavior;

Keep your implementation when its **token-stream structure and spans** contract is at least as precise with a clearer or smaller design. Revise it when the reference exposes an accepted input, failure phase, generated-name rule, evaluation effect, or determinism obligation missing from your tests.

## Capstone review

For the Module 46 increment, a strong result demonstrates **engineering procedural macros as compiler-executed token transformations with explicit parsing, spans, determinism, and security boundaries**. The capstone should still read primarily as ordinary Rust. Generated surfaces must be compact enough to inspect through tests or expansion tools, and runtime domain behavior must remain callable without understanding macro internals.

## What a strong explanation includes

A strong defense of this module explains:

- what a procedural macro knows before type checking;
- why stringifying and reparsing tokens is fragile;
- which span is used for each emitted error;
- which effects would make expansion non-reproducible;
- how the generated ordinary Rust can be inspected and tested without trusting the generator blindly;
- which simpler non-macro design was considered and why it is insufficient for this exact source-of-truth relationship.

## Deep reasoning and transfer

### Decisive model

> What does the compiler actually give a procedural macro, what can the macro know, and how should tokens, spans, errors, and effects be handled?

Build a **token-stream phase map**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Explain when and how a procedural macro executes.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Distinguish `TokenStream`, `TokenTree`, `Group`, `Ident`, `Punct`, `Literal`, and `Span`.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Avoid treating token text as a fully resolved Rust AST.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Emit deterministic tokens and source-local diagnostics.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Separate parsing, validation, normalization, and generation.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Explain when and how a procedural macro executes.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the token-stream phase map.

### Laboratory transfer review

For [TokenStream Inspector](../../labs/module-06-token-stream-inspector/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In CommandForge, Module 46 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Procedural Macro Execution and TokenStream Engineering**, which relationship decides this question: “What does the compiler actually give a procedural macro, what can the macro know, and how should tokens, spans, errors, and effects be handled?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to CommandForge?
