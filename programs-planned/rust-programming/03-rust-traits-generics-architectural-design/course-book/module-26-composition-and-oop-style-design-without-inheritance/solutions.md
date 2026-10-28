# Reasoned Solutions — Module 26: Composition and OOP-Style Design Without Inheritance

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-06-composed-renderer/README.md) · [Review Engine guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 26: Composition and OOP-Style Design Without Inheritance**. Compare the reasoning against this question: *How do you obtain encapsulation, substitution, and reusable behavior through composition rather than inheritance?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `01-private-invariant.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Private fields plus a validating constructor can make every externally constructible value satisfy a domain invariant.
- **Causal explanation:** Callers cannot write the inner byte directly; `Percent::new` is the authority that admits only values at most 100, and `get` exposes observation without reopening construction.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Expose the field and rely on callers.

### 2. `02-private-field-construction.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A public tuple struct with a private field cannot be constructed outside its defining module.
- **Causal explanation:** `m::Percent(200)` attempts to bypass the module’s construction authority, but the private field keeps the representation and its invariant inaccessible.
- **Principled repair:** Use the validated constructor.
- **Weak repair to reject:** Make the field public.

### 3. `03-generic-delegation.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A wrapper may delegate behavior only for inner types that satisfy the delegated trait contract.
- **Causal explanation:** `Signed<T>` implements `R` under `T: R`; the concrete inner `&str` satisfies that bound, so the wrapper can call `self.0.r()` and add its own behavior.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Implement unrelated capabilities blindly.

### 4. `04-recursive-wrapper-sizing.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A directly recursive field requires indirection because a value cannot contain another complete value of the same type inline.
- **Causal explanation:** `Decorator { inner: Decorator }` has no finite size: determining its size requires determining itself again. A pointer-like indirection or nonrecursive representation must break the cycle.
- **Principled repair:** Add indirection or use a nonrecursive composition.
- **Weak repair to reject:** Use Rc without shared ownership need.

### 5. `05-closed-command-enum.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** An enum represents a closed set of variants that can be handled exhaustively with direct pattern matching.
- **Causal explanation:** `run` covers both `Add` and `Clear`, so every possible `C` value has a defined branch and no dynamic registry is required.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Replace with trait objects absent extension needs.

### 6. `06-nonexhaustive-state-handling.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A match over a locally known enum must cover every variant unless an explicit fallback handles the remainder.
- **Causal explanation:** `Published` has no arm, so `code` is not total over `State`; the compiler rejects a function that could receive an unhandled value.
- **Principled repair:** Add meaningful handling for the state.
- **Weak repair to reject:** Use a wildcard that hides future semantics.

### 7. `07-unmet-composition-bound.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Delegated behavior is available only when the composed inner type satisfies the wrapper implementation’s trait bound.
- **Causal explanation:** `D<T>: R` exists only for `T: R`; `X` has no `R` implementation, so `D(X)` does not have the delegated `r` method.
- **Principled repair:** Use an inner type satisfying the contract or remove invalid delegation.
- **Weak repair to reject:** Add an empty implementation with false semantics.

### 8. `08-capability-intersection.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A generic bound `A + B` requires one concrete value to satisfy both capability contracts simultaneously.
- **Causal explanation:** `X` implements both traits, so `sum` may call `a` and `b` through the same borrowed value and combine their results.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Create a nominal supertrait with no new law.

## Exercise reasoning

Rust encapsulation relies on modules and private fields; polymorphism may be closed or open and static or dynamic; inheritance is generally replaced by capability composition and delegation. Strategy is justified by replaceable policy, adapter by interface/semantic mismatch, decorator by contract-preserving wrapped behavior, and command objects only by open runtime handling. Enums are usually stronger for closed command/state sets. Broad supertrait hierarchies should be decomposed around actual consumers.

## Composition instead of hierarchy

The core renderer should own or borrow the data needed to render; redaction is a strategy applied before or during rendering; an adapter translates the result to a target interface; a decorator wraps a reporter or renderer to add timing without changing its core responsibility. Components can then be combined orthogonally—for example, timed plain text without redaction—without adding another subclass.

## Delegation

A wrapper must preserve the trait laws except where its documented policy intentionally changes them. Forwarding every method can be wrong when a default method calls another required method in a way that bypasses observation or redaction. Review each method at the contract level. Generated delegation saves typing but does not make the semantic decision.

## State choices

A `Status` enum is usually best when state is runtime data and values of different states share one collection. Typestate is best when construction or protocol order must be checked statically and states do not need easy heterogeneous storage. State objects behind trait objects are warranted only when behavior is open and runtime-extensible. Separate structs can be clear when their data and behavior genuinely diverge.

## Adapter and decorator

A foreign logger adapter changes interface. A metrics wrapper is a decorator that preserves the interface while adding behavior. Error-to-exit-code translation is a boundary adapter. Changing output format is usually a strategy or separate renderer, not necessarily a decorator unless it wraps a stable intermediate representation.

## Composition map

The capstone should have static outer boundaries for source and reporter, dynamic owned rule entries for runtime heterogeneity, and concrete domain data between them. A trait with one implementation and no test or deployment substitute should be challenged; a concrete component often communicates more.

## Reference implementation comparison

The complete laboratory implementation is in [`module-06-composed-renderer/solution`](../../labs/module-06-composed-renderer/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Composition and OOP-Style Design Without Inheritance**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Model encapsulation, substitution, and delegation without class inheritance.
- Apply composition, strategy, adapter, decorator, and command patterns selectively.
- Separate domain state from interchangeable behavior.
- Detect inheritance-shaped trait hierarchies and replace them with smaller capabilities.
- Test composed behavior without coupling tests to concrete collaborators.

A complete explanation of **Composition and OOP-Style Design Without Inheritance** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.

## Deep reasoning and transfer

### Decisive model

> How do you obtain encapsulation, substitution, and reusable behavior through composition rather than inheritance?

Build a **composition diagram**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Model encapsulation, substitution, and delegation without class inheritance.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Apply composition, strategy, adapter, decorator, and command patterns selectively.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Separate domain state from interchangeable behavior.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Detect inheritance-shaped trait hierarchies and replace them with smaller capabilities.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Test composed behavior without coupling tests to concrete collaborators.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Model encapsulation, substitution, and delegation without class inheritance.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the composition diagram.

### Laboratory transfer review

For [Composed Renderer](../../labs/module-06-composed-renderer/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In Review Engine, Module 26 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Composition and OOP-Style Design Without Inheritance**, which relationship decides this question: “How do you obtain encapsulation, substitution, and reusable behavior through composition rather than inheritance?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to Review Engine?
