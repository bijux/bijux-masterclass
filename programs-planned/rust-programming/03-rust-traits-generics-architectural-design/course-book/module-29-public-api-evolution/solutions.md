# Reasoned solutions — Module 29: Public API Evolution

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the Review Engine engineering guide](../capstone.md)

Use these explanations to review your reasoning about **Public API Evolution**, not to substitute for an attempt. The decisive question is: *How can a public trait-based API evolve when downstream crates may both call it and implement it?* When your design differs, separate three possibilities: a Rust rule was applied incorrectly, the product contract changed, or two architectures satisfy the same contract with different trade-offs.

## Compiler specimen reasoning

### 1. `01-required-method-addition.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Required method addition.
- **Causal explanation:** The compiler rejects the specimen because required method addition.
- **Principled repair:** Use a major version, defensible default, or new trait.
- **Weak repair to reject:** Add a meaningless empty implementation.

### 2. `02-default-method-collision.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Default method collision.
- **Causal explanation:** The compiler rejects the specimen because default method collision.
- **Principled repair:** Use qualification or redesign names/extensions.
- **Weak repair to reject:** Rely on import order.

### 3. `03-new-supertrait-obligation.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** New supertrait obligation.
- **Causal explanation:** The compiler rejects the specimen because new supertrait obligation.
- **Principled repair:** Make a major change or separate extension trait.
- **Weak repair to reject:** Add false prerequisite implementations.

### 4. `04-blanket-impl-downstream-conflict.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Blanket impl downstream conflict.
- **Causal explanation:** The compiler rejects the specimen because blanket impl downstream conflict.
- **Principled repair:** Use an adapter newtype or avoid the blanket impl.
- **Weak repair to reject:** Delete downstream semantics.

### 5. `05-sealed-compatibility-surface.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Sealed compatibility surface.
- **Causal explanation:** The specimen compiles because sealed compatibility surface.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Promise downstream implementation accidentally.

### 6. `06-nonexhaustive-matching.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Nonexhaustive matching.
- **Causal explanation:** The compiler rejects the specimen because nonexhaustive matching.
- **Principled repair:** Add a documented fallback.
- **Weak repair to reject:** Assume no variants will be added.

### 7. `07-version-adapter.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Version adapter.
- **Causal explanation:** The specimen compiles because version adapter.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Pretend a required V2 semantic can be defaulted.

### 8. `08-strengthened-bound.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Strengthened bound.
- **Causal explanation:** The compiler rejects the specimen because strengthened bound.
- **Principled repair:** Treat the stronger requirement as breaking or move it to the specific method.
- **Weak repair to reject:** Implement meaningless Clone solely for compatibility.

## Exercise reasoning

Required items and supertraits break implementors. Defaults can create ambiguity and semantic obligations. Blanket implementations consume downstream relationship space. Sealing trades ecosystem implementation for evolution freedom. `non_exhaustive` affects construction and matching, not trait implementation. Material contract changes deserve versioned traits and adapters. Compatibility proof needs downstream-style compilation plus semantic review and MSRV checks.

## Change analysis

Adding a required method breaks every downstream implementation. A default method may preserve compilation but can still create behavioral conflict, method-name ambiguity, or object-safety/dyn-compatibility changes. A new supertrait breaks implementors that do not satisfy it. Bounds and associated-type changes can reject existing types. Blanket implementations can overlap with downstream impls that were previously legal. Sealing an already open trait removes a promised capability and is breaking.

Callers and implementors are distinct compatibility audiences. A change that helps callers may still make implementation impossible, and vice versa.

## Non-exhaustive design

`#[non_exhaustive]` prevents downstream exhaustive construction or matching and preserves room for variants or fields, but callers must use wildcards. Private fields with constructors provide stronger validation and evolution. Opaque errors preserve maximum freedom but expose less structured recovery. Choose according to the downstream operations you intend to support.

## Versioning

When no honest default exists, a capability subtrait or V2 trait can allow gradual adoption. An adapter can preserve old implementations while providing reduced behavior explicitly. A major release is clearer when the core contract itself changes. Capability discovery can use trait bounds at static boundaries or explicit runtime registration for objects.

## MSRV

MSRV is a published compatibility contract. Test it with the exact declared compiler and test current stable separately. Dependencies and dev-dependencies must also respect the route used. A feature compiling on the newest toolchain says nothing about the oldest supported one.

## Downstream simulation

An external fixture catches visibility, construction, coherence, and inference changes that in-crate tests miss. Record whether the change breaks source, behavior, or only documentation. The exercise turns semver from a checklist into an observable contract.

## Release council reasoning

Adding required methods is directly breaking for external implementors. Defaults reduce that immediate break but consume names and are lawful only when their behavior can be derived from the existing contract. A `Display` supertrait imposes an unrelated formatting obligation and breaks implementations that intentionally keep presentation separate.

A sealed companion trait can attach richer metadata to crate-controlled built-ins without changing the third-party `Rule` contract, but it does not help external rules expose the same metadata. `RuleV2` is appropriate when the new semantics genuinely change what every implementation must promise. An adapter can preserve old implementations with explicit fallback behavior, making semantic compromise visible instead of hiding it in defaults. Free helpers or wrapper metadata are best when identifiers and explanations belong to registration rather than to rule behavior itself.

The release evidence must compile fixture crates representing both roles. Main-crate tests cannot reveal orphan/coherence conflicts, downstream method ambiguity, missing required methods, or a raised MSRV. A credible migration example shows how an existing external implementation continues, adapts, or opts into the new contract, and states which behavior is preserved versus approximated.

## Laboratory comparison

The complete laboratory implementation is in [`module-09-evolvable-sdk/solution`](../../labs/module-09-evolvable-sdk/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Public API Evolution**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Classify public trait changes by downstream source-compatibility risk.
- Design default methods and extension points without accidental semantic promises.
- Use sealing, non-exhaustive data, adapters, and versioned traits appropriately.
- Test compile-time and behavioral compatibility claims.
- Produce a semver hazard register and migration plan.

A complete explanation of **Public API Evolution** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.
