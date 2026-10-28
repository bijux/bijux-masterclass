# Reasoned solutions — Module 19: Subtyping, Variance, PhantomData, and Drop Checking

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the Memory Workspace engineering guide](../capstone.md)

Use these explanations to review your reasoning about **Subtyping, Variance, PhantomData, and Drop Checking**, not to substitute for an attempt. The decisive question is: *When may a longer-lived capability substitute for a shorter requirement, and what semantic relationships must marker types communicate?* When your design differs, separate three possibilities: a Rust rule was applied incorrectly, the product contract changed, or two architectures satisfy the same contract with different trade-offs.

## Compiler specimen reasoning

### 1. `01-lifetime-shortening.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Longer validity can be exposed under a shorter promise.
- **Causal explanation:** The specimen compiles because longer validity can be exposed under a shorter promise.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not use lifetime casts or phantom markers without deriving the substitution and drop-checking consequences.

### 2. `02-mut-reference-invariance.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Mutable storage cannot accept a shorter inner reference.
- **Causal explanation:** The compiler rejects the specimen because mutable storage cannot accept a shorter inner reference.
- **Principled repair:** Preserve invariance: keep the original inner lifetime, use shared access where covariance is sufficient, or move owned data instead.
- **Weak repair to reject:** Do not transmute a mutable reference to a shorter inner lifetime.

### 3. `03-cell-invariance.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Cell is invariant over its contained reference lifetime.
- **Causal explanation:** The compiler rejects the specimen because cell is invariant over its contained reference lifetime.
- **Principled repair:** Do not substitute a different lifetime through `Cell`; redesign around owned values or an explicitly invariant API.
- **Weak repair to reject:** Do not use raw writes to defeat `Cell` invariance.

### 4. `04-function-argument-contravariance.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A general accepter can satisfy a static-only call site.
- **Causal explanation:** The specimen compiles because a general accepter can satisfy a static-only call site.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not use lifetime casts or phantom markers without deriving the substitution and drop-checking consequences.

### 5. `05-owned-t-outlives.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** An owned String satisfies arbitrary outlives bounds.
- **Causal explanation:** The specimen compiles because an owned String satisfies arbitrary outlives bounds.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not use lifetime casts or phantom markers without deriving the substitution and drop-checking consequences.

### 6. `06-destructor-keeps-borrow-live.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Drop can be the final use of a borrowed field.
- **Causal explanation:** The compiler rejects the specimen because drop can be the final use of a borrowed field.
- **Principled repair:** Ensure every borrowed field remains valid through destructor execution, drop the owner earlier, or change the destructor/ownership model.
- **Weak repair to reject:** Do not leak the value with `ManuallyDrop` merely to silence drop checking.

### 7. `07-invariant-marker-size.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** An invariant marker is zero-sized but type-significant.
- **Causal explanation:** The specimen compiles because an invariant marker is zero-sized but type-significant.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not use lifetime casts or phantom markers without deriving the substitution and drop-checking consequences.

### 8. `08-cross-brand-id.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Generative invariant brands cannot mix.
- **Causal explanation:** The compiler rejects the specimen because generative invariant brands cannot mix.
- **Principled repair:** Keep the generative brand parameter attached to every identifier and arena operation.
- **Weak repair to reject:** Do not erase or cast brands to mix values from different arenas.

## Exercise reasoning and worked answers
1. The outer/longer lifetime is a subtype of each nested shorter lifetime for covariant reference use. Short borrows cannot be extended outward.
2. Shared access only observes `T`, so substituting a subtype preserves safety. Mutable access can write `T`; if covariance were allowed, a shorter reference could be written into storage typed for a longer one, producing dangling data.
3. The outer shared reference is covariant in its lifetime/referent, but `Cell` is invariant over contained `&'a str`, stopping lifetime substitution. `Vec` itself is covariant in elements, but the surrounding `&mut` is invariant over the whole `Vec<...>` referent type.
4. A function that accepts any `&str` can be used at a site that supplies only `'static` strings. A function requiring `'static` cannot accept arbitrary short strings. Argument variance reverses the relation.
5. Owned `String` contains no non-static borrow, so `String: 'a` does not keep the local value alive. `&'short str: 'a` requires `'short: 'a` because the type contains that borrow.
6. The destructor can read borrowed fields, so the referent must remain valid until the wrapper is dropped, not merely until the last explicit method call.
7. `PhantomData<T>` models ownership; shared-reference marker models borrowed covariance; mutable-reference marker models exclusive relation/invariance in `T`; `fn(T)->T` marker enforces invariance without claiming a stored `T` in the same way. Full auto-trait/drop behavior must match the abstraction.
8. The HRTB chooses a fresh invariant brand lifetime. IDs from separate invocations have incompatible types and cannot be passed to the other arena. Bounds checks remain necessary.
9. Same-brand index reuse can make an old ID resolve to a new item. Add generations or forbid removal; branding addresses scope identity, not temporal reuse.
10. Capstone handles must be stored, returned from CLI operations, and survive borrow scopes. Runtime index+generation validation expresses those requirements better than a pervasive lifetime brand.

### Post-key transfer

Derive the variance of an unfamiliar wrapper, choose a marker deliberately, and compare compile-time brands with runtime generational handles.



## Laboratory comparison

The complete laboratory implementation is in [`module-09-variance-branding/solution`](../../labs/module-09-variance-branding/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Subtyping, Variance, PhantomData, and Drop Checking**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- State lifetime subtype direction through substitutability and derive covariance, contravariance, and invariance operationally.
- Compose variance through shared references, mutable references, cells, function arguments/results, and generic wrappers.
- Read outlives bounds and destructor use without claiming owned values are borrowed for the bound lifetime.
- Choose PhantomData shapes from ownership, borrowing, variance, auto-trait, and drop-check semantics, while treating current drop-check details as version-sensitive.
- Use higher-ranked generative brands to prevent cross-scope identity mixing and explain why generations remain necessary for slot reuse.

A complete explanation of **Subtyping, Variance, PhantomData, and Drop Checking** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.
