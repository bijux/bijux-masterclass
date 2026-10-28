# Reasoned Solutions — Module 23: Coherence and Implementation Ownership

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-03-coherence-adapters/README.md) · [Review Engine guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 23: Coherence and Implementation Ownership**. Compare the reasoning against this question: *Which crate owns the right to create an implementation, and how can a public design preserve coherence without giving up adaptation?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `01-local-trait-foreign-type.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A crate may implement a trait it owns for a type it does not own.
- **Causal explanation:** Because `Words` is local, this crate is the coherence authority for its implementations and may lawfully implement it for the foreign type `str`.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Create a wrapper when no distinct semantics exist.

### 2. `02-foreign-trait-local-type.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A crate may implement a foreign trait for a type it owns.
- **Causal explanation:** `Local` is defined in this crate, so the orphan rules permit a `Display` implementation even though `Display` comes from the standard library.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Use a type alias and expect new ownership.

### 3. `03-foreign-trait-foreign-type.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** The orphan rules prohibit implementing a foreign trait for a foreign type when the current crate owns neither side of the relationship.
- **Causal explanation:** Both `Display` and `Vec<u8>` are defined elsewhere; accepting this implementation would let unrelated crates create conflicting global meanings for the same pair.
- **Principled repair:** Introduce a local semantic newtype.
- **Weak repair to reject:** Use a type alias, which does not create a new type.

### 4. `04-overlapping-blanket-impls.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Two implementations are illegal when some possible type could satisfy both implementation heads.
- **Causal explanation:** A type may implement both `A` and `B`, so the two blanket implementations could both claim `Mark` for the same type. Rust rejects the overlap even if no such concrete type is written yet.
- **Principled repair:** Use disjoint wrapper types or explicit dispatch.
- **Weak repair to reject:** Wait for specialization or add arbitrary marker exclusions.

### 5. `05-newtype-ownership.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A local newtype creates a distinct nominal type and gives the current crate coherence ownership over foreign-trait implementations for it.
- **Causal explanation:** `Hex` is not an alias for `Vec<u8>`; it is a new local type, so its `Display` implementation is legal and can express hexadecimal semantics without changing `Vec` globally.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Implement Deref solely to expose every inner method.

### 6. `06-extension-trait-scope.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Extension methods participate in receiver syntax only while their trait is in scope.
- **Causal explanation:** The implementation for `str` exists, but `ext::X` is not imported at the call site, so method lookup does not consider `X::x`.
- **Principled repair:** Import the extension trait or use qualified syntax.
- **Weak repair to reject:** Add an inherent method to a type you do not own.

### 7. `07-sealed-trait-implementation.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A public trait sealed by a private supertrait can be implemented only by types for which the defining crate supplies the private prerequisite.
- **Causal explanation:** `Mine` cannot implement the inaccessible `private::Sealed` trait, so it cannot satisfy the supertrait contract required by `api::Token`.
- **Principled repair:** Use supported implementors or an exposed adapter.
- **Weak repair to reject:** Make the private trait public only to silence the error.

### 8. `08-type-alias-identity.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A type alias introduces another name, not a new nominal type or a new coherence identity.
- **Causal explanation:** `Bytes` and `Vec<u8>` are the same type, so the second `Mark` implementation duplicates the first instead of defining a separate relationship.
- **Principled repair:** Use a newtype for a distinct relationship.
- **Weak repair to reject:** Rename the alias again.

## Exercise reasoning

The decisive first question is whether the trait or relevant type is local. Generic cases then require the exact reference rules for covered parameters. Overlap is rejected whenever one type could satisfy both implementations. A newtype creates local ownership; an alias does not. Sealing is justified when implementation membership is controlled and evolution freedom matters more than downstream participation. Blanket implementations are public compatibility commitments because they reserve relationships for every matching current and future type.

## The orphan rule as ownership

Coherence guarantees that, for a trait/type pair, Rust can identify at most one applicable implementation. A crate may add an implementation when it owns the trait or an eligible local type in the relationship. This prevents two unrelated downstream crates from defining conflicting `Display for ExternalId` implementations that a third crate could observe unpredictably.

A local `struct ProductId(ExternalId);` owns the presentation policy. `From<ExternalId> for ProductId` is appropriate when wrapping is total and lossless; `AsRef<ExternalId>` can expose a borrowed view. Conversion back may also be `From<ProductId>` if consuming the wrapper loses no validation or policy information. `Deref` should not be added merely for convenience: it expands the apparent method surface and can make later inherent methods or invariants difficult to introduce.

## Blanket overlap

`impl<T: Display> Encode for T` covers every current and future `Display` type, including `Secret`, so the specific implementation overlaps. A wrapper such as `PublicEncoding<T>` narrows the implementation to values explicitly placed under that policy. An extension trait can offer `encode_public(&self)` without claiming the core `Encode` relationship for all types. Wrappers are stronger type-level policy; free or extension methods are lighter and preserve more coherence space.

## Sealing

The public trait inherits from a trait in a private module. External crates can name and use the public trait but cannot satisfy the private supertrait, so they cannot implement it. This lets the defining crate add methods or blanket implementations with fewer downstream conflicts. Sealing is therefore part of the promised extension model and must be documented.

## Extension traits

An extension trait is useful when method syntax improves discoverability and the trait is tightly named to avoid collisions. A free function is better when the operation is uncommon, when multiple extension crates may choose the same method name, or when the operation is conceptually owned by a service rather than the receiver.

## Implementation ledger

The ledger should expose accidental global claims. The strongest redesign often makes policy local: wrap the foreign value, define the domain trait in the domain crate, or use an adapter value rather than a blanket implementation over every satisfying type.

## Reference implementation comparison

The complete laboratory implementation is in [`module-03-coherence-adapters/solution`](../../labs/module-03-coherence-adapters/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Coherence and Implementation Ownership**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Predict whether an implementation satisfies coherence and orphan rules.
- Detect overlapping blanket implementations and downstream compatibility hazards.
- Use a newtype to establish local implementation ownership.
- Design sealed and extension traits deliberately.
- Produce an implementation-ownership map for a public API.

A complete explanation of **Coherence and Implementation Ownership** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.

## Deep reasoning and transfer

### Decisive model

> Which crate owns the right to create an implementation, and how can a public design preserve coherence without giving up adaptation?

Build a **coherence ownership map**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Predict whether an implementation satisfies coherence and orphan rules.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Detect overlapping blanket implementations and downstream compatibility hazards.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Use a newtype to establish local implementation ownership.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Design sealed and extension traits deliberately.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Produce an implementation-ownership map for a public API.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Predict whether an implementation satisfies coherence and orphan rules.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the coherence ownership map.

### Laboratory transfer review

For [Coherence Adapters](../../labs/module-03-coherence-adapters/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In Review Engine, Module 23 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Coherence and Implementation Ownership**, which relationship decides this question: “Which crate owns the right to create an implementation, and how can a public design preserve coherence without giving up adaptation?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to Review Engine?
