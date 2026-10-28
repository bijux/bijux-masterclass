# Reasoned solutions — Module 26: Composition and OOP-Style Design Without Inheritance

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the Review Engine engineering guide](../capstone.md)

Use these explanations to review your reasoning about **Composition and OOP-Style Design Without Inheritance**, not to substitute for an attempt. The decisive question is: *How do you obtain encapsulation, substitution, and reusable behavior through composition rather than inheritance?* When your design differs, separate three possibilities: a Rust rule was applied incorrectly, the product contract changed, or two architectures satisfy the same contract with different trade-offs.

## Compiler specimen reasoning

### 1. `01-private-invariant.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Private invariant.
- **Causal explanation:** The specimen compiles because private invariant.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Expose the field and rely on callers.

### 2. `02-private-field-construction.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Private field construction.
- **Causal explanation:** The compiler rejects the specimen because private field construction.
- **Principled repair:** Use the validated constructor.
- **Weak repair to reject:** Make the field public.

### 3. `03-generic-delegation.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Generic delegation.
- **Causal explanation:** The specimen compiles because generic delegation.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Implement unrelated capabilities blindly.

### 4. `04-recursive-wrapper-sizing.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Recursive wrapper sizing.
- **Causal explanation:** The compiler rejects the specimen because recursive wrapper sizing.
- **Principled repair:** Add indirection or use a nonrecursive composition.
- **Weak repair to reject:** Use Rc without shared ownership need.

### 5. `05-closed-command-enum.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Closed command enum.
- **Causal explanation:** The specimen compiles because closed command enum.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Replace with trait objects absent extension needs.

### 6. `06-nonexhaustive-state-handling.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Nonexhaustive state handling.
- **Causal explanation:** The compiler rejects the specimen because nonexhaustive state handling.
- **Principled repair:** Add meaningful handling for the state.
- **Weak repair to reject:** Use a wildcard that hides future semantics.

### 7. `07-unmet-composition-bound.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Unmet composition bound.
- **Causal explanation:** The compiler rejects the specimen because unmet composition bound.
- **Principled repair:** Use an inner type satisfying the contract or remove invalid delegation.
- **Weak repair to reject:** Add an empty implementation with false semantics.

### 8. `08-capability-intersection.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Capability intersection.
- **Causal explanation:** The specimen compiles because capability intersection.
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

## Laboratory comparison

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
