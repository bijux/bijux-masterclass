# Reasoned solutions — Module 22: Associated Types and Type Families

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the Review Engine engineering guide](../capstone.md)

Use these explanations to review your reasoning about **Associated Types and Type Families**, not to substitute for an attempt. The decisive question is: *When is a type chosen once by an implementation, when may callers choose it repeatedly, and how should that relationship appear in the API?* When your design differs, separate three possibilities: a Rust rule was applied incorrectly, the product contract changed, or two architectures satisfy the same contract with different trade-offs.

## Compiler specimen reasoning

### 1. `01-associated-projection.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Associated projection.
- **Causal explanation:** The specimen compiles because associated projection.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Add an unrelated generic type parameter.

### 2. `02-ambiguous-associated-type.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Ambiguous associated type.
- **Causal explanation:** The compiler rejects the specimen because ambiguous associated type.
- **Principled repair:** Use `<X as A>::Item` or `<X as B>::Item`.
- **Weak repair to reject:** Rename associated items only to silence one call.

### 3. `03-generic-relationship-multiplicity.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Generic relationship multiplicity.
- **Causal explanation:** The specimen compiles because generic relationship multiplicity.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Replace both outputs with strings.

### 4. `04-associated-type-uniqueness.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Associated type uniqueness.
- **Causal explanation:** The compiler rejects the specimen because associated type uniqueness.
- **Principled repair:** Use a generic trait parameter if multiple relationships are real.
- **Weak repair to reject:** Wrap arbitrary branches in `Box<dyn Any>`.

### 5. `05-generic-associated-type.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Generic associated type.
- **Causal explanation:** The specimen compiles because generic associated type.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Return owned strings without considering the requirement.

### 6. `06-lending-borrow-overlap.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Lending borrow overlap.
- **Causal explanation:** The compiler rejects the specimen because lending borrow overlap.
- **Principled repair:** Finish using or drop the first view before advancing.
- **Weak repair to reject:** Clone all source state without requirement evidence.

### 7. `07-unspecified-associated-type.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Unspecified associated type.
- **Causal explanation:** The compiler rejects the specimen because unspecified associated type.
- **Principled repair:** Write `dyn Source<Item = u8>` or use a generic boundary.
- **Weak repair to reject:** Erase outputs into strings.

### 8. `08-gat-dyn-incompatibility.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** GAT dyn incompatibility.
- **Causal explanation:** The compiler rejects the specimen because gAT dyn incompatibility.
- **Principled repair:** Keep static dispatch or define a separate dyn-compatible adapter.
- **Weak repair to reject:** Delete borrowing semantics from the core trait without review.

## Exercise reasoning

1. Use relationship count and selection point, not naming convenience. A collection's element type is associated; a conversion target is often generic; a borrowed view tied to each borrow is a GAT; configuration is a value.
2. `trait Parser { type Output; type Error; fn parse(&self, input: &str) -> Result<Self::Output, Self::Error>; }` captures one canonical pair per implementation.
3. A byte buffer can convert to UTF-8 text with validation and also to a copied byte vector; those are distinct target relationships.
4. If only formatting is needed, require `S::Item: Display`, not `Item = String`.
5. The capability bound accepts newtypes and borrowed displayable values, preserving abstraction.
6. A format magic number is type-level and fixed. Chunk size varies by instance or environment.
7. The second `&mut self` borrow is rejected while the first row view remains alive because the view's type is indexed by that borrow lifetime.
8. Keep `LendingRows` internal and provide `OwnedRows` that materializes each view. Most callers receive simpler ownership.
9. Use `Box<dyn Source<Item = Record, Error = SourceError>>`.
10. A generic associated type prevents dyn compatibility; rule execution should expose concrete method signatures and move typed construction metadata to a separate static trait.

## Choosing the family owner

The generic-parameter form permits the same parser type to implement `Parser<T, E>` for multiple `T` and `E` combinations, subject to coherence. That flexibility is useful only when callers genuinely select among several interpretations. It also makes calls more ambiguous because the desired implementation may not be inferable.

Associated types say that one implementation determines one output and error family. This is the usual parser contract: once `JsonRecordParser` is chosen, its output is not an arbitrary caller decision. The relationship is visible as `P::Output` and `P::Error`.

## Projection constraints

Two parser parameters can be related with an equality constraint such as `Q: Parser<Output = P::Output>`. Requiring a concrete result is `P: Parser<Output = Record>`. The prose matters: the first function coordinates two families; the second restricts one family to the domain type the algorithm consumes.

## Constants and configuration

A format version fixed for every implementation instance is an associated constant. A maximum imposed by the format may also be a constant; a limit selected by deployment is constructor data. A delimiter that can differ between two values of the same codec type cannot be an associated constant without encoding the delimiter in the type itself. Use an instance method or field instead.

## GAT reasoning

A plain associated type is selected once for the implementation and cannot contain a fresh reference lifetime tied to each call unless that lifetime is part of the trait implementation in an overconstrained way. A GAT is a family indexed by the borrow lifetime. `Self: 'a` states that the implementor remains valid for the period in which the yielded item may borrow from it.

GATs are not a prestige feature. If the product can yield owned records, or if `Iterator<Item = &str>` over a separately borrowed iterator already works, prefer the simpler contract.

## Family map

In the capstone, `Source` naturally owns its `Item` and `Error` families; `Reporter` owns `Output` and `Error`; `Rule` operates on the common domain submission and produces a common finding shape so heterogeneous rules can coexist. Turning `Source::Item` into a freely selected generic would admit combinations the source does not actually support.

## Laboratory comparison

The complete laboratory implementation is in [`module-02-associated-families/solution`](../../labs/module-02-associated-families/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Associated Types and Type Families**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Choose between generic parameters and associated types from relationship cardinality.
- Use associated constants and associated types without hiding call-site variation.
- Derive a generic associated type from a borrowing family requirement.
- Explain the effect of associated-item choices on dyn compatibility and callers.
- Write law-oriented tests for a type-family abstraction.

A complete explanation of **Associated Types and Type Families** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.
