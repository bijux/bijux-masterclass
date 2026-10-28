# Reasoned solutions — Module 41: Metaprogramming Boundaries and the Expansion Model

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the CommandForge engineering guide](../capstone.md)

Use this file after freezing an independent attempt. In this module, compare whether generation eliminates a real competing authority, whether the ordinary-Rust reference remains simpler for small inputs, whether each validation rule lives in the earliest honest phase, whether runtime policy remains outside the macro. A different implementation is valid only when those contracts survive; matching the reference token-for-token is irrelevant.

## Compiler specimen reasoning

### 1. `case-01.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** ordinary functions remain preferable for runtime value behavior.
- **Causal explanation:** The specimen compiles because ordinary functions remain preferable for runtime value behavior.
- **Principled repair:** keep the function boundary
- **Weak repair to reject:** replace it with a macro merely to remove a call

### 2. `case-02.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** an item macro may generate a mechanical family of declarations.
- **Causal explanation:** The specimen compiles because an item macro may generate a mechanical family of declarations.
- **Principled repair:** retain the compact item-generating declaration
- **Weak repair to reject:** hand-copy the items and allow drift

### 3. `case-03.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** an expression-position invocation must expand to an expression.
- **Causal explanation:** The compiler rejects the specimen because an expression-position invocation must expand to an expression.
- **Principled repair:** invoke the item macro in item position or emit an expression
- **Weak repair to reject:** wrap arbitrary item tokens in extra delimiters

### 4. `case-04.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** successful expansion does not imply successful name resolution.
- **Causal explanation:** The compiler rejects the specimen because successful expansion does not imply successful name resolution.
- **Principled repair:** emit a valid path or require the path as input
- **Weak repair to reject:** call the failure a parser error

### 5. `case-05.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** generated trait bounds are established by ordinary type checking.
- **Causal explanation:** The specimen compiles because generated trait bounds are established by ordinary type checking.
- **Principled repair:** keep the bound in emitted ordinary Rust
- **Weak repair to reject:** inspect token spelling to guess trait support

### 6. `case-06.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** a generated trait bound may reject a concrete downstream type.
- **Causal explanation:** The compiler rejects the specimen because a generated trait bound may reject a concrete downstream type.
- **Principled repair:** implement the required trait or change the generated contract
- **Weak repair to reject:** stringify the source tokens instead of formatting the value

### 7. `case-07.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** runtime tables are often sufficient sources of truth.
- **Causal explanation:** The specimen compiles because runtime tables are often sufficient sources of truth.
- **Principled repair:** retain ordinary data
- **Weak repair to reject:** introduce a macro only because the rows look repetitive

### 8. `case-08.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** macro syntax must match one declared invocation grammar.
- **Causal explanation:** The compiler rejects the specimen because macro syntax must match one declared invocation grammar.
- **Principled repair:** write the required separator or add a deliberately specified grammar form
- **Weak repair to reject:** capture every token with tt and defer the error

## How to review the compiler specimens

The machine-readable outcomes are in [`compiler-labs/manifest.json`](../../compiler-labs/manifest.json). For **mechanism selection and phase ownership**, compare your prediction against five questions:

1. Did you identify the earliest phase that knows enough to enforce the requirement?
2. Did you distinguish a repeated syntactic relationship from ordinary runtime policy?
3. Can one declaration genuinely replace two or more drifting sources of truth?
4. Would deleting the generator make the product clearer with little meaningful duplication?
5. Does the chosen mechanism fail before invalid data reaches a later, less informative phase?

Diagnostic prose may change between compiler releases. The isolated source shape and governing phase are the durable evidence.

## Broken-design repair

**Step 1.** Write a source-of-truth table. For every fact, name who declares it, who validates it, who consumes it, and when it becomes known.

**Step 2.** Move runtime values and permission checks into ordinary functions. Keep runtime dispatch in ordinary Rust unless a compile-time relation actually needs generation.

**Step 3.** Use a small declarative macro only for the declaration that must appear in several Rust syntactic positions, such as an enum variant and exhaustive match arms.

**Step 4.** Use a build script only for checked external data that exists before compilation and must become Rust source. Make the input path and rerun rule explicit.

**Step 5.** Run the deletion test: remove the generator mentally and estimate the manual duplication. If deletion produces only a short table or one ordinary function, reject the generator.

The repaired design should make **mechanism selection and phase ownership** smaller and more inspectable than the broken proposal. Judge it by whether one declaration owns the mechanical relationship, the expanded Rust remains readable, and each invalid input fails in the earliest phase that possesses the necessary information.

## Exercise reasoning

### Exercise 1 — Mechanism matrix

A strong matrix keeps runtime behavior in functions or values, uses traits or generics for type-level substitution, uses `macro_rules!` for bounded token-local syntax relationships, uses a derive when an existing item shape is the source of truth, uses an attribute when one attached item must be validated or augmented, uses a function-like procedural macro for a real custom grammar with cross-entry rules, and uses `build.rs` for checked external data. The answer must name the source of truth rather than choosing by aesthetics.

### Exercise 2 — Two-program trace

The generator can inspect token spelling and emit an `impl` with a bound, but it does not prove that a concrete downstream type satisfies the bound. Expansion produces ordinary Rust tokens. Parsing and name resolution establish paths; trait checking rejects an use whose type does not satisfy `Display`. Calling the whole event “a macro parsing error” loses the causal phase.

### Exercise 3 — Position audit

An expression macro must expand to an expression where an expression is expected; an item macro must produce items in an item context; a type macro must produce a type in type position. Balanced token trees can still form the wrong grammatical category. Expansion is inserted into surrounding Rust syntax and parsed according to that position.

### Exercise 4 — Deletion test

The original table is already one runtime source of truth, so a macro adds syntax and compatibility cost without removing drift. The revised requirement repeats one association across several syntactic positions that ordinary values cannot generate, so a small macro may be justified. The source declaration should remain compact and the emitted surfaces should be documented.

### Exercise 5 — Failure taxonomy

They belong respectively to syntax parsing, procedural semantic validation, name resolution, trait checking, build-script input validation, and runtime I/O. Each should be reported by the earliest phase that can know the truth. Earlier is not always possible; later usually worsens context.

### Exercise 6 — Authority ledger

Command names and cross-command uniqueness belong to the catalog DSL; handler signature belongs to the attached function plus attribute validation; argument fields belong to the ordinary struct plus derive helper attributes; diagnostic variants/codes/messages belong to the declarative diagnostic declaration; external exit codes belong to the checked TSV consumed by `build.rs`. No fact should be independently declared by two mechanisms.

## Laboratory comparison

The reference implementation is in [`labs/module-01-decision-table-generator/solution`](../../labs/module-01-decision-table-generator/solution). Review it in this order:

1. whether generation eliminates a real competing authority;
2. whether the ordinary-Rust reference remains simpler for small inputs;
3. whether each validation rule lives in the earliest honest phase;
4. whether runtime policy remains outside the macro;

Keep your implementation when its **mechanism selection and phase ownership** contract is at least as precise with a clearer or smaller design. Revise it when the reference exposes an accepted input, failure phase, generated-name rule, evaluation effect, or determinism obligation missing from your tests.

## Capstone review

For the Module 41 increment, a strong result demonstrates **choosing the smallest compile-time mechanism that owns one source of truth**. The capstone should still read primarily as ordinary Rust. Generated surfaces must be compact enough to inspect through tests or expansion tools, and runtime domain behavior must remain callable without understanding macro internals.

## What a strong explanation includes

A strong defense of this module explains:

- why repetition alone is not sufficient justification;
- which facts become duplicated if generation is removed;
- why the selected mechanism is weaker than the alternatives above it;
- what change would make the macro unnecessary;
- how the generated ordinary Rust can be inspected and tested without trusting the generator blindly;
- which simpler non-macro design was considered and why it is insufficient for this exact source-of-truth relationship.
