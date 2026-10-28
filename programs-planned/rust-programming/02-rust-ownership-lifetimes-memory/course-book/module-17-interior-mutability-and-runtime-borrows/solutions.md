# Reasoned Solutions — Module 17: Interior Mutability and Runtime Borrows

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-07-interior-cache/README.md) · [Memory Workspace guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 17: Interior Mutability and Runtime Borrows**. Compare the reasoning against this question: *Which logically hidden mutation justifies runtime enforcement, and how can guard scope and reentrancy remain controlled?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `01-mutate-through-shared-self.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Ordinary field mutation requires exclusive receiver.
- **Causal explanation:** The compiler rejects the specimen because ordinary field mutation requires exclusive receiver.
- **Principled repair:** Use `&mut self` for exclusive mutation, or choose `Cell`/`RefCell` with an explicit runtime-borrow policy.
- **Weak repair to reject:** Do not use unsafe pointer casts to mutate through a shared reference.

### 2. `02-cell-scalar.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Cell safely replaces copyable scalar state.
- **Causal explanation:** The specimen compiles because cell safely replaces copyable scalar state.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not use interior mutability as a default substitute for an ordinary exclusive borrow.

### 3. `03-refcell-conflict-runtime.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Overlapping dynamic borrows compile but panic at runtime.
- **Causal explanation:** The specimen compiles because overlapping dynamic borrows compile but panic at runtime.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not use interior mutability as a default substitute for an ordinary exclusive borrow.

### 4. `04-try-borrow-conflict.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Fallible dynamic borrowing exposes conflict.
- **Causal explanation:** The specimen compiles because fallible dynamic borrowing exposes conflict.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not use interior mutability as a default substitute for an ordinary exclusive borrow.

### 5. `05-nested-reborrow-compiles.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Nested public methods can hide a runtime panic path.
- **Causal explanation:** The specimen compiles because nested public methods can hide a runtime panic path.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not use interior mutability as a default substitute for an ordinary exclusive borrow.

### 6. `06-once-cell-lazy.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** OnceCell initializes through shared access.
- **Causal explanation:** The specimen compiles because onceCell initializes through shared access.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not use interior mutability as a default substitute for an ordinary exclusive borrow.

### 7. `07-stale-once-cell-design.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A one-time cache can compile despite mutable source.
- **Causal explanation:** The specimen compiles because a one-time cache can compile despite mutable source.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not use interior mutability as a default substitute for an ordinary exclusive borrow.

### 8. `08-rc-refcell-cycle.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Interior mutation can construct a strong cycle.
- **Causal explanation:** The specimen compiles because interior mutation can construct a strong cycle.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not use interior mutability as a default substitute for an ordinary exclusive borrow.

## Exercise reasoning and worked answers
1. `Cell<u64>` copies values in/out and never creates borrow guards; it exactly matches scalar replacement. `RefCell` adds unnecessary dynamic borrow state and panic paths.
2. Store `(min, max)` or a `Bounds` copy in one `Cell` when small/Copy; otherwise one `RefCell<Bounds>`. Update under one operation so no callback observes a half-transition.
3. `borrow_mut` panics while any guard exists. `try_borrow_mut` returns `BorrowMutError`, allowing translation to `Busy` when overlap is valid product behavior.
4. Use a block to extract the required copy/owned data, let the guard drop, then call. Do not rely on a subtle final-use point when protocol clarity matters.
5. Borrow once in the outer method and pass `&mut State` to private pure helpers. This avoids re-borrowing the cell and documents one mutation phase.
6. `OnceCell` is correct only if source input never invalidates the result. Initializer code must not call the same accessor recursively.
7. Store cache revision and clear or reject on source mutation. Tests mutate content, then assert recomputation and updated ranges.
8. Mapped guards avoid copying but keep the entire cell dynamically borrowed. Owned ranges release the borrow and can be retained, with later validation. Public ergonomics often favors ranges.
9. Draw strong/weak edges separately from borrow operations. Break cycles with weak edges or central arena ownership; shorten guards before graph traversal/callbacks.
10. Metrics live in private `Cell<u64>`. Equality, snapshots, serialization, and document revisions ignore them. Tests may inspect through a read-only diagnostics method.

### Deeper reasoning notes

A cache method is easiest to review when it has three explicit phases: inspect metadata under a short shared borrow, compute outside all cache guards, then publish under one short mutable borrow. Combining lookup, computation, and publication in a single long `borrow_mut` scope creates a reentrancy trap even if current helper functions do not call back into the cache. The robust design is based on the permitted call graph, not on today's accidental implementation.

`RefCell` does not make an operation thread-safe and does not weaken Rust's aliasing rule. It moves enforcement from compile time to a dynamic state machine. One active mutable guard excludes every other guard; one or more shared guards exclude a mutable guard. A panic from `borrow_mut` is therefore evidence that the program violated its own runtime borrowing protocol. When overlap can occur through legitimate user composition, `try_borrow` and `try_borrow_mut` permit the API to represent contention as a typed error instead.

Returning `Ref<'_, [usize]>` can be zero-copy, but it exports the cache's dynamic borrow duration to the caller. That may prevent an unrelated later operation from mutating the same cell and may make callbacks unexpectedly panic. Returning an owned `Vec<Range<usize>>`, a copied small descriptor, or a slice borrowed from immutable source storage changes both cost and protocol. The correct choice is made from retention needs and invalidation rules, not from an automatic preference for zero allocation.

Finally, semantic equality must be defined from domain state. Two values with identical text and revision are semantically equal even when one has a warm cache and higher hit counters. Including cache state in `PartialEq`, persistence, or snapshot identity turns an optimization into observable product behavior and makes harmless recomputation change meaning.

### Post-key transfer

Repair a callback-capable cache that holds RefMut across user code, then prove cache invalidation and busy-state behavior.

## Reference implementation comparison

The complete laboratory implementation is in [`module-07-interior-cache/solution`](../../labs/module-07-interior-cache/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Interior Mutability and Runtime Borrows**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Explain UnsafeCell as the primitive behind interior mutability while remaining within safe APIs.
- Choose Cell for replaceable Copy state and RefCell for single-threaded dynamically checked borrowed state.
- Treat Ref and RefMut as runtime loan guards whose scope is part of the API protocol.
- Avoid reentrant borrow panics by computing outside guards, shortening scopes, or using try_borrow variants and typed errors.
- Design caches whose mutation is observationally transparent, correctly invalidated, and memory-bounded.

A complete explanation of **Interior Mutability and Runtime Borrows** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.

## Deep reasoning and transfer

### Decisive model

> Which logically hidden mutation justifies runtime enforcement, and how can guard scope and reentrancy remain controlled?

Build a **runtime-borrow trace**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Explain UnsafeCell as the primitive behind interior mutability while remaining within safe APIs.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Choose Cell for replaceable Copy state and RefCell for single-threaded dynamically checked borrowed state.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Treat Ref and RefMut as runtime loan guards whose scope is part of the API protocol.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Avoid reentrant borrow panics by computing outside guards, shortening scopes, or using try_borrow variants and typed errors.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Design caches whose mutation is observationally transparent, correctly invalidated, and memory-bounded.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Explain UnsafeCell as the primitive behind interior mutability while remaining within safe APIs.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the runtime-borrow trace.

### Laboratory transfer review

For [Revisioned Interior Cache](../../labs/module-07-interior-cache/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In Memory Workspace, Module 17 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Interior Mutability and Runtime Borrows**, which relationship decides this question: “Which logically hidden mutation justifies runtime enforcement, and how can guard scope and reentrancy remain controlled?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to Memory Workspace?
