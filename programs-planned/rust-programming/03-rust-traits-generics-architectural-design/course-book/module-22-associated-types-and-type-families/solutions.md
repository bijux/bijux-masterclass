# Reasoned Solutions — Module 22: Associated Types and Type Families

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-02-associated-families/README.md) · [Review Engine guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 22: Associated Types and Type Families**. Compare the reasoning against this question: *When is a type chosen once by an implementation, when may callers choose it repeatedly, and how should that relationship appear in the API?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `01-associated-projection.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** For a fixed trait implementation, an associated type projection is uniquely determined by the implementor.
- **Causal explanation:** `S: Source` fixes `S::Item` to `u8`; therefore `T::Item` in `first` is a well-formed return type and `s.get()` produces exactly that projection.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Add an unrelated generic type parameter.

### 2. `02-ambiguous-associated-type.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** When several traits define an associated item with the same name, the projection must identify the owning trait.
- **Causal explanation:** `X` implements both `A` and `B`, and each supplies a different `Item`; `X::Item` omits the trait path, so the compiler cannot know whether the intended type is `u8` or `u16`.
- **Principled repair:** Use `<X as A>::Item` or `<X as B>::Item`.
- **Weak repair to reject:** Rename associated items only to silence one call.

### 3. `03-generic-relationship-multiplicity.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A trait type parameter permits one implementor to participate in distinct implementations for different parameter values.
- **Causal explanation:** `Bytes` implements `Convert<Vec<u8>>` and `Convert<String>` as separate relationships. The expected result type at each assignment selects the corresponding implementation.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Replace both outputs with strings.

### 4. `04-associated-type-uniqueness.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A type may provide only one implementation of a trait, and that implementation fixes each associated type once.
- **Causal explanation:** The two `Source for S` implementations overlap completely and attempt to assign two incompatible meanings to `Source::Item`; coherence rejects the second implementation.
- **Principled repair:** Use a generic trait parameter if multiple relationships are real.
- **Weak repair to reject:** Wrap arbitrary branches in `Box<dyn Any>`.

### 5. `05-generic-associated-type.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A generic associated type may produce a family of types indexed by the lifetime of each borrow.
- **Causal explanation:** `Text::Out<'a>` is `&'a str`, and `view` returns a slice whose lifetime is tied to the particular borrow of `self` rather than to one global associated type.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Return owned strings without considering the requirement.

### 6. `06-lending-borrow-overlap.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A value returned from a lending method may keep the mutable borrow of the lender active until that value is last used.
- **Causal explanation:** `a` borrows from `s` through the first `next`; the second call needs another mutable borrow of `s` while `a` is still used later, so the two loans overlap.
- **Principled repair:** Finish using or drop the first view before advancing.
- **Weak repair to reject:** Clone all source state without requirement evidence.

### 7. `07-unspecified-associated-type.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A trait object with associated types must fix those associated types so its erased method signatures are complete.
- **Causal explanation:** `dyn Source` leaves `Source::Item` unknown, so the return type of `get` cannot be represented as one object-safe callable signature. The object type must state an equality such as `Item = u8` or remain generic.
- **Principled repair:** Write `dyn Source<Item = u8>` or use a generic boundary.
- **Weak repair to reject:** Erase outputs into strings.

### 8. `08-gat-dyn-incompatibility.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A trait whose dispatch surface depends on a generic associated type is not dyn-compatible under the current object model.
- **Causal explanation:** The erased object would need to represent the lifetime-indexed family `Item<'a>` for arbitrary caller borrows, but one vtable method signature cannot encode that family here.
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

## Reference implementation comparison

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

## Deep reasoning and transfer

### Decisive model

> When is a type chosen once by an implementation, when may callers choose it repeatedly, and how should that relationship appear in the API?

Build a **associated-type relationship map**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Choose between generic parameters and associated types from relationship cardinality.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Use associated constants and associated types without hiding call-site variation.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Derive a generic associated type from a borrowing family requirement.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Explain the effect of associated-item choices on dyn compatibility and callers.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Write law-oriented tests for a type-family abstraction.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Choose between generic parameters and associated types from relationship cardinality.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the associated-type relationship map.

### Laboratory transfer review

For [Associated Families](../../labs/module-02-associated-families/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In Review Engine, Module 22 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Associated Types and Type Families**, which relationship decides this question: “When is a type chosen once by an implementation, when may callers choose it repeatedly, and how should that relationship appear in the API?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to Review Engine?
