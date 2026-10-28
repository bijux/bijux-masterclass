# Reasoned Solutions — Module 39: Combinator Laws and Cost Models

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-09-combinator-contracts/README.md) · [LedgerFlow guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 39: Combinator Laws and Cost Models**. Compare the reasoning against this question: *What semantic laws should a combinator preserve, and what can honestly be claimed about evaluation and cost?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `case-01.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** predicate composition can retain short-circuit semantics.
- **Causal explanation:** The specimen compiles because predicate composition can retain short-circuit semantics.
- **Principled repair:** document order and effect-free law assumptions
- **Weak repair to reject:** reorder predicates as if effects and cost never matter

### 2. `case-02.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** different closure expressions have distinct concrete types.
- **Causal explanation:** The compiler rejects the specimen because different closure expressions have distinct concrete types.
- **Principled repair:** move the branch inside one closure, return fn pointer for noncapturing cases, or erase deliberately
- **Weak repair to reject:** box by default without stating runtime heterogeneity

### 3. `case-03.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** placing runtime choice inside one closure preserves one closure type.
- **Causal explanation:** The specimen compiles because placing runtime choice inside one closure preserves one closure type.
- **Principled repair:** use this when per-call branch cost is acceptable
- **Weak repair to reject:** claim it is always equivalent to choosing once outside

### 4. `case-04.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** a context adapter can preserve the source error type.
- **Causal explanation:** The specimen compiles because a context adapter can preserve the source error type.
- **Principled repair:** use a generic FieldError
- **Weak repair to reject:** format errors into strings in every leaf parser

### 5. `case-05.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** a stateful predicate does not satisfy an Fn-only combinator contract.
- **Causal explanation:** The compiler rejects the specimen because a stateful predicate does not satisfy an Fn-only combinator contract.
- **Principled repair:** accept FnMut when repeated state is supported
- **Weak repair to reject:** hide mutation in a global counter

### 6. `case-06.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** normalization idempotence can be tested as a law on a bounded domain.
- **Causal explanation:** The specimen compiles because normalization idempotence can be tested as a law on a bounded domain.
- **Principled repair:** state the domain and counterexamples
- **Weak repair to reject:** claim a universal theorem from one example

### 7. `case-07.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** lazy and eager APIs can coexist with distinct names and return shapes.
- **Causal explanation:** The specimen compiles because lazy and eager APIs can coexist with distinct names and return shapes.
- **Principled repair:** make materialization explicit at the call site
- **Weak repair to reject:** return Vec from every query

### 8. `case-08.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** one closure expression has one inferred parameter and return type.
- **Causal explanation:** The compiler rejects the specimen because one closure expression has one inferred parameter and return type.
- **Principled repair:** use a generic named function or separate closure expressions
- **Weak repair to reject:** erase all values to a dynamic type without need

## Exercise reasoning

### Exercise 1 — State a law honestly

For Unicode strings under a specified normalization that trims ends and collapses each run of Unicode whitespace to one ASCII space, claim `normalize(normalize(x)) == normalize(x)` by string equality. Counterexamples to broader claims include a normalizer that appends a timestamp, performs lossy length truncation after encoding, or alternates quote style. The implementation and tests must use the same whitespace definition; “all normalization is idempotent” is false.

### Exercise 2 — Compose predicates with effects

For pure, total predicates, yielded values and order are equivalent. With effects, call counts and ordering are observable: `q` runs only when `p` succeeds in both versions, but capture and borrow structure may differ; with adapters reused or errors encoded differently, behavior can diverge. If predicates can return `Result`, ordinary `filter` cannot preserve failure. State the law only for pure deterministic predicates and an observation limited to yielded sequence.

### Exercise 3 — Design lazy and eager names

For example, `fn matches<'a>(&'a self, query: &'a Query) -> impl Iterator<Item=&'a Record> + 'a` exposes lazy borrowed traversal. `fn matching_records(&self, query: &Query) -> Vec<Record>` materializes owned clones for storage beyond the borrow. Distinct names prevent hidden allocation. The lazy form ties result use to source/query lifetimes and concrete hidden iterator type; the eager form pays traversal and cloning immediately but is easy to store and cross boundaries.

### Exercise 4 — Preserve context through composition

Use a wrapper such as `Context<E> { stage: &'static str, source: E }` and a function `at_stage(result, stage) -> Result<T, Context<E>>` implemented with `map_err`. Implement `Display` separately and `Error::source` where `E: Error + 'static`. This retains typed source information and permits later matching or chained reporting.

### Exercise 5 — Write a cost ledger

The single chain generally performs one traversal and no intermediate collection, with adapter state stored on the stack and output materialized only by the final consumer. Intermediate collection adds allocation and stores every normalized record, but may be justified for sorting, reuse, or borrow separation. Cloning into boxed trait-object iteration adds clones, possible heap allocation for the box, dynamic dispatch, and erases concrete type; it may be justified for runtime-selected pipeline shapes. These are cost models, not benchmark results.

### Exercise 6 — De-combinatorize

Extract named parsing and validation functions, choose one explicit error policy, and use a small loop or named iterator adaptor where state is substantial. Materialize only at an algorithmic boundary such as sorting. Return a domain result type if callers need diagnostics and values together. The goal is not fewer lines; it is making item type, failure, order, and ownership apparent. Keep combinators where they express simple local transformations.

## Reference implementation comparison

The complete laboratory implementation is in [`module-09-combinator-contracts/solution`](../../labs/module-09-combinator-contracts/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Combinator Laws and Cost Models**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Design domain combinators that preserve type and error meaning.
- State and test laws such as identity, idempotence, order preservation, and partition consistency where they truly apply.
- Reason about closure capture, allocation, cloning, and materialization costs without claiming unmeasured optimization.
- Choose lazy or eager return types based on lifetime, API, and reuse constraints.
- Reject combinator designs that hide control flow, destroy diagnostics, or produce unusable types.

A complete explanation of **Combinator Laws and Cost Models** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.

## Deep reasoning and transfer

### Decisive model

> What semantic laws should a combinator preserve, and what can honestly be claimed about evaluation and cost?

Build a **law and counterexample table**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Design domain combinators that preserve type and error meaning.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **State and test laws such as identity, idempotence, order preservation, and partition consistency where they truly apply.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Reason about closure capture, allocation, cloning, and materialization costs without claiming unmeasured optimization.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Choose lazy or eager return types based on lifetime, API, and reuse constraints.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Reject combinator designs that hide control flow, destroy diagnostics, or produce unusable types.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Design domain combinators that preserve type and error meaning.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the law and counterexample table.

### Laboratory transfer review

For [Combinator Contracts](../../labs/module-09-combinator-contracts/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In LedgerFlow, Module 39 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Combinator Laws and Cost Models**, which relationship decides this question: “What semantic laws should a combinator preserve, and what can honestly be claimed about evaluation and cost?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to LedgerFlow?
