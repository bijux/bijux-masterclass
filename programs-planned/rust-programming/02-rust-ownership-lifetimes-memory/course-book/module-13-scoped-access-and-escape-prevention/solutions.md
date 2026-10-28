# Reasoned Solutions — Module 13: Scoped Access and Escape Prevention

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-03-scoped-visitors/README.md) · [Memory Workspace guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 13: Scoped Access and Escape Prevention**. Compare the reasoning against this question: *Who chooses a lifetime, and how can an API expose temporary access while making escape unrepresentable?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `01-hrtb-owned-result.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A higher-ranked callback may return owned evidence.
- **Causal explanation:** The specimen compiles because a higher-ranked callback may return owned evidence.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not weaken a scoped callback into leaked or globally stored state.

### 2. `02-hrtb-reference-escape.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A universally supplied borrow cannot become fixed R.
- **Causal explanation:** The compiler rejects the specimen because a universally supplied borrow cannot become fixed R.
- **Principled repair:** Return owned evidence from the callback or complete the borrowed work entirely inside the higher-ranked call.
- **Weak repair to reject:** Do not try to store a universally scoped reference in a fixed external lifetime.

### 3. `03-fnonce-consumes-capture.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A closure consuming capture is callable once.
- **Causal explanation:** The specimen compiles because a closure consuming capture is callable once.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not weaken a scoped callback into leaked or globally stored state.

### 4. `04-fnmut-captured-counter.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A mutating capture satisfies FnMut.
- **Causal explanation:** The specimen compiles because a mutating capture satisfies FnMut.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not weaken a scoped callback into leaked or globally stored state.

### 5. `05-scratch-view-return.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A view into mutably borrowed scratch cannot escape the method.
- **Causal explanation:** The compiler rejects the specimen because a view into mutably borrowed scratch cannot escape the method.
- **Principled repair:** Return owned ranges or invoke a callback while the scratch borrow is valid rather than returning the view.
- **Weak repair to reject:** Do not clone arbitrary scratch storage or forge a longer borrow.

### 6. `06-owned-ranges-escape.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Owned ranges can outlive temporary line views.
- **Causal explanation:** The specimen compiles because owned ranges can outlive temporary line views.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not weaken a scoped callback into leaked or globally stored state.

### 7. `07-naive-self-reference.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** An owner cannot safely store a reference into itself during construction.
- **Causal explanation:** The compiler rejects the specimen because an owner cannot safely store a reference into itself during construction.
- **Principled repair:** Store stable indices/offsets, use a scoped view, or introduce pinning only after proving a real address-sensitive invariant.
- **Weak repair to reject:** Do not construct a self-reference with raw pointers and assume moves will never happen.

### 8. `08-opaque-borrowed-iterator.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** An opaque iterator captures the receiver borrow.
- **Causal explanation:** The specimen compiles because an opaque iterator captures the receiver borrow.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not weaken a scoped callback into leaked or globally stored state.

## Exercise reasoning and worked answers
### 1. Quantifier translation

In `a`, the borrow lifetime is established for the invocation and the callback must accept that concrete lifetime. A surrounding callback type can, in principle, contain storage valid for the same `'x`. In `b`, the callback must work for every lifetime supplied by the function; it cannot demand one preselected long lifetime. In `c`, `R` is selected independently of the universally quantified input lifetime, so `R` cannot simply be the borrowed argument. It can contain owned evidence such as a range, count, or copied scalar.

### 2. Capture matrix

A closure that only reads captured state generally implements all three callable traits. A closure that mutates captured state implements `FnMut` and `FnOnce`, not `Fn`. A closure that moves a captured `String` out of itself implements only `FnOnce`. `move` transfers capture ownership but does not by itself force `FnOnce`; use inside the body determines whether captured fields are consumed.

### 3. Escape attempt

The outer `Vec<&str>` has one element reference type with one surrounding lifetime. A higher-ranked callback receives lines under lifetimes selected per invocation. Assigning any such line to the outer vector would require proving that arbitrary `'line` outlives the vector's element lifetime, which is impossible. Ranges are owned and can escape; resolving them later requires the original text and boundary validation.

### 4. Early termination

The traversal can return `ControlFlow<(usize, Range<usize>)>` or simply `Option<usize>`. Returning a borrowed line defeats the scoped policy. The producer must calculate the durable location while the line is available.

### 5. Iterator comparison

For immutable caller-owned text, `split_whitespace()` already yields slices tied to the caller's text. The standard iterator is more composable and does not permit references to outlive the owner. The visitor adds control inversion without a stronger safety property. Use it only if the producer has scratch storage, reuses buffers, or must constrain retention.

### 6. Scratch transformation

The HRTB form is:

```rust
fn with_transformed<R>(
    &mut self,
    input: &str,
    operation: impl for<'a> FnOnce(&'a str) -> R,
) -> R
```

`R` cannot vary with `'a`, so returning the scratch slice is rejected. A caller needing retention should choose an owned `String`; the allocation is then part of the product contract rather than hidden leakage.

### 7. Self-reference alternatives

Recomputation has the smallest stored invariant but repeats parsing. A range avoids address sensitivity but must remain on UTF-8 boundaries and be invalidated or adjusted on edits. A separate `DocumentView<'a>` can borrow both the document and a derived title while the document is immutably borrowed; it cannot be stored inside the document. None requires pinning.

### 8. Opaque return

The hidden iterator owns adapter values and a closure; those capture a borrow of the collection and usually the query. The yielded item lifetime comes from the collection. A fully explicit signature can use separate `'catalog` and `'query` lifetimes with an outlives relation appropriate to the lifetime chosen for the opaque value. Avoid forcing both owners to one lifetime unless the iterator genuinely requires it.

### 9. Redundant HRTB

An owned `String` contains no borrowed lifetime to quantify. `for<'a> FnMut(String)` is equivalent to a bound with an unused lifetime and communicates false sophistication. Use `FnMut(String)`.

### 10. Capstone design

`matches` is appropriate over immutable stored text when callers may retain match views while holding the workspace borrow. `visit_matches` is appropriate when match views are synthesized from temporary scratch data or when the API deliberately prevents retention. Both should return stable document handles and byte ranges as durable evidence when mutation may follow.

### Post-key transfer

Design a scratch-buffer decoder that lends temporary output to arbitrary callbacks but cannot return a reference into the scratch allocation.

## Reference implementation comparison

The complete laboratory implementation is in [`module-03-scoped-visitors/solution`](../../labs/module-03-scoped-visitors/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Scoped Access and Escape Prevention**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Distinguish caller-chosen named lifetimes from fresh lifetimes generated independently for each callback invocation.
- Read and design for<'a> higher-ranked callback bounds as universal quantification over borrow duration.
- Account for closure capture and Fn, FnMut, and FnOnce requirements at scoped boundaries.
- Use callbacks and scoped APIs to prevent temporary references or brands from escaping.
- Recognize self-reference pressure and choose indices, owned state, callbacks, or later pinning only when justified.

A complete explanation of **Scoped Access and Escape Prevention** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.

## Deep reasoning and transfer

### Decisive model

> Who chooses a lifetime, and how can an API expose temporary access while making escape unrepresentable?

Build a **scope and escape table**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Distinguish caller-chosen named lifetimes from fresh lifetimes generated independently for each callback invocation.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Read and design for<'a> higher-ranked callback bounds as universal quantification over borrow duration.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Account for closure capture and Fn, FnMut, and FnOnce requirements at scoped boundaries.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Use callbacks and scoped APIs to prevent temporary references or brands from escaping.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Recognize self-reference pressure and choose indices, owned state, callbacks, or later pinning only when justified.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Distinguish caller-chosen named lifetimes from fresh lifetimes generated independently for each callback invocation.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the scope and escape table.

### Laboratory transfer review

For [Scoped Visitors](../../labs/module-03-scoped-visitors/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In Memory Workspace, Module 13 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Scoped Access and Escape Prevention**, which relationship decides this question: “Who chooses a lifetime, and how can an API expose temporary access while making escape unrepresentable?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to Memory Workspace?
