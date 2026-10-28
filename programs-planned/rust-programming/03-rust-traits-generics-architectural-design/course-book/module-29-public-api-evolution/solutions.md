# Reasoned Solutions — Module 29: Public API Evolution

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-09-evolvable-sdk/README.md) · [Review Engine guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 29: Public API Evolution**. Compare the reasoning against this question: *How can a public trait-based API evolve when downstream crates may both call it and implement it?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `01-required-method-addition.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Adding a required method to a public trait invalidates existing implementations that cannot supply the new item.
- **Causal explanation:** `Old` implements the previous `run` contract but omits the newly required `id`; the compiler exposes the downstream implementation break immediately.
- **Principled repair:** Use a major version, defensible default, or new trait.
- **Weak repair to reject:** Add a meaningless empty implementation.

### 2. `02-default-method-collision.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** When two imported traits provide the same applicable method name, receiver syntax becomes ambiguous even if both methods have defaults.
- **Causal explanation:** `X` implements both `A` and `B`; `X.name()` does not select which default is intended, so qualification or a redesigned extension surface is required.
- **Principled repair:** Use qualification or redesign names/extensions.
- **Weak repair to reject:** Rely on import order.

### 3. `03-new-supertrait-obligation.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Adding a supertrait strengthens the implementation contract for every existing implementor.
- **Causal explanation:** `P: Id` now requires `Old` to implement `Id` before its `P` implementation is valid; this is a downstream breaking change, not a free refactor.
- **Principled repair:** Make a major change or separate extension trait.
- **Weak repair to reject:** Add false prerequisite implementations.

### 4. `04-blanket-impl-downstream-conflict.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A new blanket implementation can overlap with a downstream explicit implementation for a type that satisfies the blanket bound.
- **Causal explanation:** `Local: Display` makes the blanket `impl<T: Display> P for T` apply, while the explicit `impl P for Local` claims the same pair; coherence rejects the conflict.
- **Principled repair:** Use an adapter newtype or avoid the blanket impl.
- **Weak repair to reject:** Delete downstream semantics.

### 5. `05-sealed-compatibility-surface.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A sealed trait limits the set of implementors, allowing the defining crate to evolve implementation obligations without breaking third-party implementations.
- **Causal explanation:** Only `api` can satisfy the private prerequisite for `T`; `X` is an authorized implementor and downstream crates are consumers rather than uncontrolled implementors.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Promise downstream implementation accidentally.

### 6. `06-nonexhaustive-matching.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A non-exhaustive public enum requires downstream matches to include a fallback for variants that may be added later.
- **Causal explanation:** `std::io::ErrorKind` is non-exhaustive; matching only two known variants would make downstream code source-incompatible with future additions, so a wildcard or equivalent fallback is mandatory.
- **Principled repair:** Add a documented fallback.
- **Weak repair to reject:** Assume no variants will be added.

### 7. `07-version-adapter.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** An adapter can preserve an old contract while presenting a newer interface with added metadata or failure structure.
- **Causal explanation:** `A<T>` delegates `V1::run`, supplies the new identifier, and lifts the infallible old result into `Result`, allowing old behavior to participate in the V2 boundary.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Pretend a required V2 semantic can be defaulted.

### 8. `08-strengthened-bound.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Adding a trait bound excludes callers whose types previously satisfied the public function signature.
- **Causal explanation:** `use_it` now requires `Clone`, but `NotClone` lacks that capability; the call demonstrates the source break caused by strengthening a generic requirement.
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

## Reference implementation comparison

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

## Deep reasoning and transfer

### Decisive model

> How can a public trait-based API evolve when downstream crates may both call it and implement it?

Build a **compatibility matrix**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Classify public trait changes by downstream source-compatibility risk.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Design default methods and extension points without accidental semantic promises.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Use sealing, non-exhaustive data, adapters, and versioned traits appropriately.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Test compile-time and behavioral compatibility claims.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Produce a semver hazard register and migration plan.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Classify public trait changes by downstream source-compatibility risk.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the compatibility matrix.

### Laboratory transfer review

For [Evolvable SDK](../../labs/module-09-evolvable-sdk/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In Review Engine, Module 29 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Public API Evolution**, which relationship decides this question: “How can a public trait-based API evolve when downstream crates may both call it and implement it?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to Review Engine?
