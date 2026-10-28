# Reasoned Solutions — Module 31: Closures, Capture, and Callable Contracts

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-01-closure-policy-matrix/README.md) · [LedgerFlow guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 31: Closures, Capture, and Callable Contracts**. Compare the reasoning against this question: *What does a closure capture, which callable traits does it implement, and what invocation contract should an API require?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `case-01.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** FnOnce accepts a callable that consumes captured state.
- **Causal explanation:** The specimen compiles because fnOnce accepts a callable that consumes captured state.
- **Principled repair:** retain the FnOnce boundary
- **Weak repair to reject:** clone the capture and require Fn

### 2. `case-02.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** an FnOnce closure cannot be called after it has been consumed.
- **Causal explanation:** The compiler rejects the specimen because an FnOnce closure cannot be called after it has been consumed.
- **Principled repair:** call once or redesign the closure to borrow/clone deliberately
- **Weak repair to reject:** clone every captured value to silence the move

### 3. `case-03.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** move capture does not imply FnOnce call capability.
- **Causal explanation:** The specimen compiles because move capture does not imply FnOnce call capability.
- **Principled repair:** keep move for ownership and Fn for repeated reading
- **Weak repair to reject:** remove move without checking the deferred lifetime

### 4. `case-04.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** a mutable-capture closure does not satisfy Fn.
- **Causal explanation:** The compiler rejects the specimen because a mutable-capture closure does not satisfy Fn.
- **Principled repair:** change the API to FnMut and bind the callable mutably
- **Weak repair to reject:** hide state in a global variable

### 5. `case-05.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** FnMut supports repeated stateful calls.
- **Causal explanation:** The specimen compiles because fnMut supports repeated stateful calls.
- **Principled repair:** use FnMut as the weakest sufficient repeated-call bound
- **Weak repair to reject:** box the closure despite one concrete caller type

### 6. `case-06.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** a capturing closure cannot coerce to a function pointer.
- **Causal explanation:** The compiler rejects the specimen because a capturing closure cannot coerce to a function pointer.
- **Principled repair:** accept a generic callable or move the branch inside one closure
- **Weak repair to reject:** make the offset global

### 7. `case-07.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** return-position impl Fn preserves one anonymous closure type.
- **Causal explanation:** The specimen compiles because return-position impl Fn preserves one anonymous closure type.
- **Principled repair:** use impl Fn for one concrete hidden callable type
- **Weak repair to reject:** allocate Box<dyn Fn> without runtime heterogeneity

### 8. `case-08.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** a stored closure keeps its captured borrow alive until last use.
- **Causal explanation:** The compiler rejects the specimen because a stored closure keeps its captured borrow alive until last use.
- **Principled repair:** call/drop the closure before mutation or capture only derived data
- **Weak repair to reject:** clone the whole vector without a semantic need

## Exercise reasoning

### Exercise 1 — Capture and capability table

`a` captures `name` by shared borrow and can implement `Fn`, `FnMut`, and `FnOnce`; the binding need not be mutable. `name` cannot be mutably used while a later call to `a` keeps the borrow live. `b` captures `hits` by mutable borrow, implements `FnMut` and `FnOnce`, and requires a mutable closure binding for calls. `c` owns `payload` and moves it out when called, so its useful call capability is `FnOnce`; the first call consumes the stored payload. `d` owns `prefix` but only reads it during formatting. It can still implement all three callable traits and can be called repeatedly. The exercise separates capture mode from call capability.

### Exercise 2 — Weakest sufficient bounds

A suitable set is:

```rust
fn with_default<T, F: FnOnce() -> T>(value: Option<T>, fallback: F) -> T;
fn map_all<T, U, F: Fn(&T) -> U>(items: &[T], f: F) -> Vec<U>;
fn number_all<T, U, F: FnMut(&T) -> U>(items: &[T], mut f: F) -> Vec<U>;
```

`with_default` must allow ownership-consuming fallback closures. Requiring `Fn` would forbid them without adding value because the implementation performs at most one call. `map_all` promises shared repeated calls and therefore permits concurrent-looking reuse at the semantic level, although this course makes no parallel-execution claim. `number_all` must permit mutation of captured numbering state. `FnMut` also accepts ordinary `Fn` closures because the capability hierarchy is substitutive in that direction.

### Exercise 3 — Return one anonymous type

`offsetter` can return one closure expression:

```rust
fn offsetter(offset: i64) -> impl Fn(i64) -> i64 {
    move |value| value + offset
}
```

Return-position `impl Trait` hides one concrete type chosen by the function body. Every closure expression has a distinct anonymous type. Two branch-local closure expressions therefore do not become one type merely because their signatures match. A principled repair is to move the branch inside one closure expression, return an enum that delegates, or deliberately erase to `Box<dyn Fn(i64) -> i64>` when runtime heterogeneity is part of the requirement.

### Exercise 4 — Repair a borrow extended by storage

The best repair depends on the actual lifetime requirement. First, call immediately and store the numeric result: `let length = values.len();`; no closure is needed. Second, put closure construction and use in a smaller block so the shared borrow ends before mutation. Third, if deferred execution genuinely requires an independent snapshot, clone or move a deliberately owned snapshot into a `move` closure. The third changes semantics and cost: the callback observes old data, not the later vector. Adding `move` to the original closure may consume `values` and is not a general repair.

### Exercise 5 — Generic storage versus boxed storage

The static version should be `Policy<N, S>` with bounds on the methods that invoke `N` and `S`. It has one concrete policy type per callable combination and avoids heap allocation and dynamic dispatch. Boxing becomes justified when one policy instance must select among scorer implementations at runtime or when a heterogeneous collection of scorers must share one storage type. “The type is long” is not sufficient. The change also introduces object-lifetime questions, potential allocation, indirect calls, and loss of some compiler-visible concrete-type information.

### Exercise 6 — Call ledger test

Use an owned or mutably borrowed event ledger captured by the callbacks. The normalizer appends `normalize:<id>`, the scorer appends `score:<id>`, and the fallback appends `fallback`. After evaluation assert the exact sequence for multiple items and assert absence of `fallback`. A separate missing-value case should prove exactly one fallback call. This is stronger than output-only testing because a defective implementation could produce the same result while evaluating callbacks twice, in the wrong order, or eagerly.

## Reference implementation comparison

The complete laboratory implementation is in [`module-01-closure-policy-matrix/solution`](../../labs/module-01-closure-policy-matrix/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Closures, Capture, and Callable Contracts**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Distinguish function items, function pointers, and anonymous closure types.
- Predict closure capture mode and the resulting `Fn`, `FnMut`, and `FnOnce` capabilities.
- Choose the weakest callable bound that exactly matches an API’s invocation contract.
- Use `move` deliberately without assuming that every move closure is `FnOnce`.
- Select among generic callables, `impl Fn*`, and boxed callable trait objects from real storage and dispatch requirements.

A complete explanation of **Closures, Capture, and Callable Contracts** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.

## Deep reasoning and transfer

### Decisive model

> What does a closure capture, which callable traits does it implement, and what invocation contract should an API require?

Build a **closure capture map**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Distinguish function items, function pointers, and anonymous closure types.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Predict closure capture mode and the resulting `Fn`, `FnMut`, and `FnOnce` capabilities.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Choose the weakest callable bound that exactly matches an API’s invocation contract.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Use `move` deliberately without assuming that every move closure is `FnOnce`.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Select among generic callables, `impl Fn*`, and boxed callable trait objects from real storage and dispatch requirements.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Distinguish function items, function pointers, and anonymous closure types.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the closure capture map.

### Laboratory transfer review

For [Closure Policy Matrix](../../labs/module-01-closure-policy-matrix/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In LedgerFlow, Module 31 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Closures, Capture, and Callable Contracts**, which relationship decides this question: “What does a closure capture, which callable traits does it implement, and what invocation contract should an API require?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to LedgerFlow?
