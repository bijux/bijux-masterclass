# Reasoned Solutions — Module 32: The Iterator Model

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-02-lazy-log-query/README.md) · [LedgerFlow guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 32: The Iterator Model**. Compare the reasoning against this question: *What state does an iterator own, when does work happen, and what is consumed by each call to next?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `case-01.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** iter borrows a collection and yields shared references.
- **Causal explanation:** The specimen compiles because iter borrows a collection and yields shared references.
- **Principled repair:** retain borrowed iteration
- **Weak repair to reject:** clone the vector before every traversal

### 2. `case-02.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** into_iter on an owned Vec consumes the vector.
- **Causal explanation:** The compiler rejects the specimen because into_iter on an owned Vec consumes the vector.
- **Principled repair:** borrow with iter or stop using the vector afterward
- **Weak repair to reject:** clone solely to retain a redundant copy

### 3. `case-03.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** iter_mut yields exclusive element references.
- **Causal explanation:** The specimen compiles because iter_mut yields exclusive element references.
- **Principled repair:** keep the mutable borrow scoped to the traversal
- **Weak repair to reject:** use interior mutability without shared-ownership pressure

### 4. `case-04.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** next requires mutable access to iterator state.
- **Causal explanation:** The compiler rejects the specimen because next requires mutable access to iterator state.
- **Principled repair:** declare the iterator mutable
- **Weak repair to reject:** recreate the iterator for every item

### 5. `case-05.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** by_ref permits partial consumption followed by resumption.
- **Causal explanation:** The specimen compiles because by_ref permits partial consumption followed by resumption.
- **Principled repair:** use by_ref at a deliberate phase boundary
- **Weak repair to reject:** collect the entire source before splitting phases

### 6. `case-06.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** peekable can inspect a boundary without consuming it.
- **Causal explanation:** The specimen compiles because peekable can inspect a boundary without consuming it.
- **Principled repair:** use Peekable when boundary preservation is product behavior
- **Weak repair to reject:** assume take_while preserves the rejected item

### 7. `case-07.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** two live iter_mut traversals would alias the same elements.
- **Causal explanation:** The compiler rejects the specimen because two live iter_mut traversals would alias the same elements.
- **Principled repair:** finish/drop one traversal before starting the other or split disjoint regions
- **Weak repair to reject:** wrap every element in RefCell to bypass a design error

### 8. `case-08.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** iterator adapters are lazy until a consumer pulls.
- **Causal explanation:** The specimen compiles because iterator adapters are lazy until a consumer pulls.
- **Principled repair:** choose a consumer intentionally
- **Weak repair to reject:** add collect only to make the code appear to do work

## Exercise reasoning

### Exercise 1 — Trace the state machine

Before the first call, the iterator owns the vector allocation and all three elements. Each successful `next` transfers one `i32` item to the caller and advances internal position. After calls one, two, and three, the caller receives `Some(10)`, `Some(20)`, and `Some(30)`. After the fourth, the iterator returns `None`. The original vector binding was moved at iterator construction and is unusable. For a fused iterator such as the standard vector iterator, later calls remain `None`.

### Exercise 2 — Three traversal forms

`iter()` borrows the vector immutably and yields `&String`; values can be inspected but not mutated through these references, and the vector is usable after the iterator borrow ends. `iter_mut()` exclusively borrows the vector and yields `&mut String`; elements can be modified and the vector is usable after the traversal ends. `into_iter()` on the owned vector consumes it and yields `String`; each element can be moved elsewhere, but the original vector binding is gone. The table must describe ownership, not only syntax.

### Exercise 3 — Prove laziness

Use `Cell<usize>` or a mutable counter with an appropriate scope. After `map` construction the count is zero. After one `next`, it is one. After collecting the remaining `n - 1` items, it is `n`. This proves the mapped body runs on demand for this pipeline. It does not prove absence of all work: source creation, allocation already performed by an owned collection, or other eager setup may have happened before iteration.

### Exercise 4 — Partial parser with `by_ref`

Create one mutable iterator, then call `iterator.by_ref().take_while(|token| *token != "--")` only if losing the delimiter is acceptable: `take_while` consumes the first failing item. If the delimiter must remain observable, use `peekable`, inspect with `peek`, and consume deliberately with `next`. The important design question is not merely using `by_ref`; it is specifying boundary consumption semantics.

### Exercise 5 — Truthful iterator contracts

After a filter whose predicate outcome is unknown, the lower bound may be zero and the upper bound can be the unfiltered remaining count: `(0, Some(n))`. It cannot implement `ExactSizeIterator` because `len()` would need the exact remaining yield count in constant time and must remain consistent with `size_hint`. Overstating the lower bound is a contract violation, not a harmless optimization hint.

### Exercise 6 — Loop or chain

The explicit loop is usually clearer because the control flow contains four different outcomes: skip, stop, accept, and diagnose. A chain can still be appropriate if named stage functions preserve these distinctions, but a dense mixture of `take_while`, `filter_map`, `inspect`, and external mutation obscures stopping and error policy. Select by whether a reader can identify item type, consumption, order, and failure without mentally executing nested closures.

## Reference implementation comparison

The complete laboratory implementation is in [`module-02-lazy-log-query/solution`](../../labs/module-02-lazy-log-query/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **The Iterator Model**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Explain the distinct roles of `IntoIterator`, `Iterator`, adapters, and consumers.
- Trace the state changes caused by repeated calls to `next`.
- Predict whether an iteration path borrows, mutably borrows, or consumes its source.
- Use `by_ref`, `peekable`, and fused boundaries without losing track of consumed items.
- Treat `size_hint`, `ExactSizeIterator`, and `FusedIterator` as contracts rather than optimization decoration.

A complete explanation of **The Iterator Model** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.

## Deep reasoning and transfer

### Decisive model

> What state does an iterator own, when does work happen, and what is consumed by each call to next?

Build a **iterator state trace**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Explain the distinct roles of `IntoIterator`, `Iterator`, adapters, and consumers.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Trace the state changes caused by repeated calls to `next`.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Predict whether an iteration path borrows, mutably borrows, or consumes its source.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Use `by_ref`, `peekable`, and fused boundaries without losing track of consumed items.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Treat `size_hint`, `ExactSizeIterator`, and `FusedIterator` as contracts rather than optimization decoration.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Explain the distinct roles of `IntoIterator`, `Iterator`, adapters, and consumers.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the iterator state trace.

### Laboratory transfer review

For [Lazy Log Query](../../labs/module-02-lazy-log-query/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In LedgerFlow, Module 32 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **The Iterator Model**, which relationship decides this question: “What state does an iterator own, when does work happen, and what is consumed by each call to next?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to LedgerFlow?
