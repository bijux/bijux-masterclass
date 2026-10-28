# Reasoned Solutions — Module 20: Pinning and Address-Sensitive Design

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-10-pinned-tracker/README.md) · [Memory Workspace guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 20: Pinning and Address-Sensitive Design**. Compare the reasoning against this question: *What invariant becomes invalid after mechanical movement, who promises not to move the value, and can the design avoid address sensitivity entirely?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `01-normal-value-moves.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Ordinary values remain movable.
- **Causal explanation:** The specimen compiles because ordinary values remain movable.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not add pinning when no address-sensitive invariant exists, and do not use unchecked projection casually.

### 2. `02-box-pin-phantom-pinned.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Box::pin safely pins a !Unpin value.
- **Causal explanation:** The specimen compiles because box::pin safely pins a !Unpin value.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not add pinning when no address-sensitive invariant exists, and do not use unchecked projection casually.

### 3. `03-get-mut-requires-unpin.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Unrestricted mutable access is unavailable for !Unpin.
- **Causal explanation:** The compiler rejects the specimen because unrestricted mutable access is unavailable for !Unpin.
- **Principled repair:** Operate through `Pin<&mut T>` and provide only projections that preserve the pinned fields’ invariants.
- **Weak repair to reject:** Do not call `get_unchecked_mut` without a complete projection proof.

### 4. `04-pin-reborrow.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** as_mut creates shorter pinned reborrows.
- **Causal explanation:** The specimen compiles because as_mut creates shorter pinned reborrows.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not add pinning when no address-sensitive invariant exists, and do not use unchecked projection casually.

### 5. `05-stack-pin-escape.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A pinned stack borrow cannot escape its storage lifetime.
- **Causal explanation:** The compiler rejects the specimen because a pinned stack borrow cannot escape its storage lifetime.
- **Principled repair:** Pin owned storage such as `Box::pin`, or keep every pinned stack use inside the stack owner’s scope.
- **Weak repair to reject:** Do not leak stack-backed state or return a pointer to it.

### 6. `06-move-out-of-pinned-box.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A !Unpin pointee cannot be moved out through Pin<Box<T>>.
- **Causal explanation:** The compiler rejects the specimen because a !Unpin pointee cannot be moved out through Pin<Box<T>>.
- **Principled repair:** Keep the `!Unpin` value inside its pinned owner and expose operations that do not move it.
- **Weak repair to reject:** Do not use `ptr::read` or unchecked mutable access to extract the pointee.

### 7. `07-safe-address-token.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** An address can be observed without dereferencing raw pointers.
- **Causal explanation:** The specimen compiles because an address can be observed without dereferencing raw pointers.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not add pinning when no address-sensitive invariant exists, and do not use unchecked projection casually.

### 8. `08-unnecessary-pin-compiles.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Pin can compile even when no address invariant justifies it.
- **Causal explanation:** The specimen compiles because pin can compile even when no address invariant justifies it.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not add pinning when no address-sensitive invariant exists, and do not use unchecked projection casually.

## Exercise reasoning and worked answers
1. A Rust move always transfers ownership semantically; actual bytes may or may not relocate after optimization. Address-sensitive validity cares whether the pinned pointee's storage changes, not whether an owner handle moves.
2. `PhantomPinned` opts out of `Unpin`. `Box::pin` establishes owning pinned heap storage; `pin!` establishes scoped stack storage. Neither alone creates self-pointers.
3. `Pin<&T>` is shared borrowed pinned access; `Pin<&mut T>` is exclusive borrowed pinned access with movement restrictions; `Pin<Box<T>>` owns pinned heap storage. All carry ordinary lifetime/ownership rules in addition to pinning.
4. Unrestricted `&mut T` permits `mem::replace` and moving the old value. For `!Unpin`, safe `get_mut` is withheld because that would break the no-move promise.
5. Call `as_mut()` to create shorter pinned reborrows for each method; `as_ref()` creates shared pinned access. Moving the pin handle is harmless.
6. A field participating in an address relationship is structurally pinned. Scalar counters or replaceable metadata may be unpinned if methods can reach them without moving pinned fields. The type must document this table.
7. The destructor must run in place, avoid moving structurally pinned fields, invalidate external links before storage release, and avoid panic. The owning pointer must deallocate only after in-place drop.
8. The outer struct address is stable, but `String` owns a separate buffer whose address may change on capacity growth. Store immutable backing or offsets/revisions instead.
9. Ranges are owned, movable, serializable evidence. Validate UTF-8 boundaries and revision before resolving. No address invariant remains, so pinning is unnecessary.
10. A complete defense connects topology, lifetime contracts, cleanup, shared ownership, runtime caches, representation claims, variance markers, and deliberate non-use of pinning. Passing tests without this explanation is insufficient.

### Post-key transfer

Audit a proposed self-referential cache, decide whether pinning is necessary, and either derive the full contract or redesign it away.

## Reference implementation comparison

The complete laboratory implementation is in [`module-10-pinned-tracker/solution`](../../labs/module-10-pinned-tracker/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Pinning and Address-Sensitive Design**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Distinguish ownership movement from mechanical relocation and identify genuine address-sensitive invariants.
- Explain Pin<P> as a contract on the pointee mediated by a pointer, not as a magical immovable allocation.
- Use Unpin and PhantomPinned correctly and construct pinned values without exposing moves after invariant activation.
- Reason about structural pinning, field projection, the drop guarantee, and why unsafe projection requires proof beyond compiler acceptance.
- Prefer handles, indices, owned indirection, scoped callbacks, or redesigned state when they eliminate self-reference or address dependence.

A complete explanation of **Pinning and Address-Sensitive Design** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.

## Deep reasoning and transfer

### Decisive model

> What invariant becomes invalid after mechanical movement, who promises not to move the value, and can the design avoid address sensitivity entirely?

Build a **pinning contract**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Distinguish ownership movement from mechanical relocation and identify genuine address-sensitive invariants.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Explain Pin<P> as a contract on the pointee mediated by a pointer, not as a magical immovable allocation.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Use Unpin and PhantomPinned correctly and construct pinned values without exposing moves after invariant activation.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Reason about structural pinning, field projection, the drop guarantee, and why unsafe projection requires proof beyond compiler acceptance.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Prefer handles, indices, owned indirection, scoped callbacks, or redesigned state when they eliminate self-reference or address dependence.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Distinguish ownership movement from mechanical relocation and identify genuine address-sensitive invariants.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the pinning contract.

### Laboratory transfer review

For [Pinned Tracker](../../labs/module-10-pinned-tracker/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In Memory Workspace, Module 20 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Pinning and Address-Sensitive Design**, which relationship decides this question: “What invariant becomes invalid after mechanical movement, who promises not to move the value, and can the design avoid address sensitivity entirely?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to Memory Workspace?
