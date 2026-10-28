# Reasoned solutions — Module 21: Traits as Behavioral Contracts

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the Review Engine engineering guide](../capstone.md)

Use these explanations to review your reasoning about **Traits as Behavioral Contracts**, not to substitute for an attempt. The decisive question is: *What behavior truly belongs in a shared contract, and which laws must every implementation preserve?* When your design differs, separate three possibilities: a Rust rule was applied incorrectly, the product contract changed, or two architectures satisfy the same contract with different trade-offs.

## Compiler specimen reasoning

### 1. `01-trait-import.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Trait import.
- **Causal explanation:** The specimen compiles because trait import.
- **Principled repair:** Keep the import near the consumer.
- **Weak repair to reject:** Replace method syntax with unrelated code.

### 2. `02-missing-generic-bound.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Missing generic bound.
- **Causal explanation:** The compiler rejects the specimen because missing generic bound.
- **Principled repair:** Add the weakest `T: Label` bound.
- **Weak repair to reject:** Make the function accept only one concrete type without reviewing the API.

### 3. `03-default-method.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Default method.
- **Causal explanation:** The specimen compiles because default method.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Override every implementation without semantic need.

### 4. `04-ambiguous-method.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Ambiguous method.
- **Causal explanation:** The compiler rejects the specimen because ambiguous method.
- **Principled repair:** Use fully qualified syntax to select the contract.
- **Weak repair to reject:** Rename methods arbitrarily without reviewing semantics.

### 5. `05-self-sized-boundary.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Self Sized boundary.
- **Causal explanation:** The specimen compiles because self Sized boundary.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Remove the trait-object use entirely.

### 6. `06-supertrait-obligation.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Supertrait obligation.
- **Causal explanation:** The compiler rejects the specimen because supertrait obligation.
- **Principled repair:** Implement the real prerequisite or remove an unjustified supertrait.
- **Weak repair to reject:** Add an empty prerequisite implementation with no valid semantics.

### 7. `07-conditional-implementation.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Conditional implementation.
- **Causal explanation:** The specimen compiles because conditional implementation.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Clone or stringify without the contract.

### 8. `08-consuming-receiver.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Consuming receiver.
- **Causal explanation:** The compiler rejects the specimen because consuming receiver.
- **Principled repair:** Use the returned value or redesign the receiver if consumption is not semantic.
- **Weak repair to reject:** Clone before every call without ownership justification.

## Exercise reasoning

These are design answers, not unique line-for-line solutions.

1. Logging intrinsic state can remain an inherent method when only `Order` exists. If multiple unrelated values must produce structured audit records for a generic sink, a narrow `AuditRecord` trait is defensible. A run-time choice of logging format may use an enum when formats are closed.
2. `T: Display` is sufficient when both values share a type; use separate `L: Display, R: Display` when they need not. `Debug`, `Clone`, and `'static` are unjustified.
3. Plausible laws: normalization is idempotent, preserves semantic identity, and produces a canonical form. A lossy compressor cannot implement that contract if it changes identity.
4. `finish(self)` consumes a builder or session; `peek(&self)` observes; `advance(&mut self)` mutates in place; `reset(&mut self)` usually preserves identity while changing state. A reset that returns ownership to a pool could consume instead.
5. A default retry is unsafe without an idempotence contract. It can duplicate effects. Retry policy belongs in a separate capability or caller with explicit semantics.
6. Consumers should request `Named`, `Identified`, or serialization separately. A type is not obligated to implement all because it is an “entity.”
7. Use `<Concrete as Trait>::function()`. Without a receiver, Rust lacks a value whose type narrows the implementation.
8. The shared test should check range and any monotonic or determinism law, while implementation-specific tests cover domain calculations.
9. Replace the generic caller with a concrete parameter and remove the trait. The loss is downstream substitution; the gain is a smaller API and easier evolution.
10. An open public trait allows ecosystem implementations but makes required-item additions breaking. A sealed trait preserves internal implementation control and broader evolution freedom.

## Contract workshop

A shared `Render` trait is justified only when every implementation preserves the same caller-visible meaning. A name such as `render` is not the contract. If one implementation returns diagnostic detail while another returns stable user output, combining them creates accidental substitutability. Either split the contracts—for example, `DisplayReport` and `DebugReport`—or introduce an explicit mode whose semantics are documented.

Redaction is usually clearer as a wrapper or strategy when the underlying value should not mutate merely because one presentation policy changes. `&self` then communicates repeatable inspection; `&mut self` would imply rendering changes meaningful state, and `self` would imply rendering consumes the report. Those receiver choices should follow product behavior, not implementation convenience.

A safe default method is one derivable from required behavior, such as `is_empty` defined from a required `len`. A default that silently catches errors, allocates unexpectedly, or changes ordering is not mechanical and should not be imposed on all implementors.

## Bound derivation

`T: Display` is the most direct contract when the output is the public textual form. `ToString` works because it is blanket-implemented for `Display`, but it obscures the source contract. `Debug` promises diagnostic representation and is therefore semantically wrong even when formatting compiles. A custom trait is warranted only when the domain needs laws or context not represented by `Display`.

The bound belongs because the body invokes formatting behavior. No `Clone`, `Eq`, or `'static` bound should appear unless the algorithm actually requires it.

## Law tests

Idempotence means `normalize(normalize(x)) == normalize(x)` for every successful input. Preservation means a valid canonical identifier is unchanged. A table-driven test should include ASCII case, surrounding whitespace if trimming is allowed, Unicode normalization assumptions, and an input the contract rejects. If some input cannot be normalized without guessing, return `Result` rather than inventing data.

## Method resolution

The inherent method wins ordinary method lookup when applicable. Trait-qualified calls select the named contract explicitly. Fully qualified syntax is useful when associated types or multiple implementations make the receiver type important. In review, UFCS is not noise when it shows that the same method name carries different behavioral promises.

## Transfer standard

A strong trait document says what downstream code may rely on and what implementors must preserve. If the only purpose is grouping methods on one concrete type, an inherent implementation is simpler and leaves future coherence space untouched.

## Laboratory comparison

The complete laboratory implementation is in [`module-01-contract-boundaries/solution`](../../labs/module-01-contract-boundaries/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Traits as Behavioral Contracts**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Define a trait whose methods express a coherent behavioral contract.
- Distinguish inherent behavior, free functions, and trait behavior.
- Apply bounds, `where` clauses, default methods, supertraits, and UFCS correctly.
- Detect traits that merely rename data access or create false substitutability.
- Test semantic laws shared by multiple implementations.

A complete explanation of **Traits as Behavioral Contracts** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.
