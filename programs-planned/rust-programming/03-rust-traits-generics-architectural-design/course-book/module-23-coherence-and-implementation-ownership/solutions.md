# Reasoned solutions — Module 23: Coherence and Implementation Ownership

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the Review Engine engineering guide](../capstone.md)

Use these explanations to review your reasoning about **Coherence and Implementation Ownership**, not to substitute for an attempt. The decisive question is: *Which crate owns the right to create an implementation, and how can a public design preserve coherence without giving up adaptation?* When your design differs, separate three possibilities: a Rust rule was applied incorrectly, the product contract changed, or two architectures satisfy the same contract with different trade-offs.

## Compiler specimen reasoning

### 1. `01-local-trait-foreign-type.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Local trait foreign type.
- **Causal explanation:** The specimen compiles because local trait foreign type.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Create a wrapper when no distinct semantics exist.

### 2. `02-foreign-trait-local-type.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Foreign trait local type.
- **Causal explanation:** The specimen compiles because foreign trait local type.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Use a type alias and expect new ownership.

### 3. `03-foreign-trait-foreign-type.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Foreign trait foreign type.
- **Causal explanation:** The compiler rejects the specimen because foreign trait foreign type.
- **Principled repair:** Introduce a local semantic newtype.
- **Weak repair to reject:** Use a type alias, which does not create a new type.

### 4. `04-overlapping-blanket-impls.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Overlapping blanket impls.
- **Causal explanation:** The compiler rejects the specimen because overlapping blanket impls.
- **Principled repair:** Use disjoint wrapper types or explicit dispatch.
- **Weak repair to reject:** Wait for specialization or add arbitrary marker exclusions.

### 5. `05-newtype-ownership.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Newtype ownership.
- **Causal explanation:** The specimen compiles because newtype ownership.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Implement Deref solely to expose every inner method.

### 6. `06-extension-trait-scope.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Extension trait scope.
- **Causal explanation:** The compiler rejects the specimen because extension trait scope.
- **Principled repair:** Import the extension trait or use qualified syntax.
- **Weak repair to reject:** Add an inherent method to a type you do not own.

### 7. `07-sealed-trait-implementation.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Sealed trait implementation.
- **Causal explanation:** The compiler rejects the specimen because sealed trait implementation.
- **Principled repair:** Use supported implementors or an exposed adapter.
- **Weak repair to reject:** Make the private trait public only to silence the error.

### 8. `08-type-alias-identity.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Type alias identity.
- **Causal explanation:** The compiler rejects the specimen because type alias identity.
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

## Laboratory comparison

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
