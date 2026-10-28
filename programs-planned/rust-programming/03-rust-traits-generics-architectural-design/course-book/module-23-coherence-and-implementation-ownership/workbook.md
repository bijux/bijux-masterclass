# Workbook — Module 23: Coherence and Implementation Ownership

[Chapter](index.md) · [Laboratory](../../labs/module-03-coherence-adapters/README.md) · [Review Engine guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Coherence and Implementation Ownership** has become a usable model rather than remembered vocabulary. Its governing question is: *Which crate owns the right to create an implementation, and how can a public design preserve coherence without giving up adaptation?* Preserve your first prediction and record decisive facts in a **coherence ownership map**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 22 — Associated Types and Type Families that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **Which crate owns the right to create an implementation, and how can a public design preserve coherence without giving up adaptation?**
3. Draw the smallest **coherence ownership map** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Coherence and Implementation Ownership** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-local-trait-foreign-type.rs`](../../compiler-labs/module-03/01-local-trait-foreign-type.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-foreign-trait-local-type.rs`](../../compiler-labs/module-03/02-foreign-trait-local-type.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-foreign-trait-foreign-type.rs`](../../compiler-labs/module-03/03-foreign-trait-foreign-type.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-overlapping-blanket-impls.rs`](../../compiler-labs/module-03/04-overlapping-blanket-impls.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-newtype-ownership.rs`](../../compiler-labs/module-03/05-newtype-ownership.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-extension-trait-scope.rs`](../../compiler-labs/module-03/06-extension-trait-scope.rs) | Pass or fail? What exact rule decides? |
| 7 | [`07-sealed-trait-implementation.rs`](../../compiler-labs/module-03/07-sealed-trait-implementation.rs) | Pass or fail? What exact rule decides? |
| 8 | [`08-type-alias-identity.rs`](../../compiler-labs/module-03/08-type-alias-identity.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 03-rust-traits-generics-architectural-design
```

## Part 2 — Diagnose and repair

A library released `impl<T: Display> Audit for T`. A downstream application already implements `Audit` for its local `Account`, which also implements `Display`. Upgrade now fails.

Produce three repairs and compare migration cost:

- remove or narrow the blanket implementation;
- introduce an explicit `Displayed<T>` adapter newtype;
- redesign `Audit` as a caller-owned formatter operation.

Do not use a feature flag that silently changes which implementation applies.

## Part 3 — Focused exercises

1. Predict ten local/foreign trait–type implementation combinations.
2. Explain why coherence is checked across possible future types.
3. Find the overlap between two bounded blanket implementations.
4. Replace a forbidden `Display for Vec<u8>` implementation with a semantic newtype.
5. Compare a type alias and newtype for implementation ownership.
6. Design a sealed core trait and public convenience extension trait.
7. State when sealing would damage a plugin ecosystem.
8. Audit a blanket implementation as a semver change.
9. Write an extension trait for `str` and explain import-dependent method visibility.
10. Produce an implementation-ownership map for the capstone rule interfaces.

### Coherence incident

Your crate uses a foreign `ExternalId` and wants a custom `Display` form. The direct implementation is illegal because both the trait and type are foreign.

1. Explain the orphan-rule rejection in terms of implementation ownership rather than memorizing “one side must be local.”
2. Design a transparent local newtype that owns the display policy.
3. Decide which conversions are lossless and should be `From`, which are only borrowed views, and which should remain explicit constructors.
4. State whether the newtype should implement `Deref<Target = ExternalId>`. Give one API-evolution risk of automatic dereference coercion.

### Blanket overlap

Consider:

```rust
trait Encode { /* ... */ }

impl<T: Display> Encode for T { /* ... */ }
// Later:
impl Encode for Secret { /* redacted form */ }
```

Explain why the first implementation consumes future design space. Produce two alternative designs: one based on a local wrapper and one based on an extension method. Compare caller ergonomics and coherence cost.

### Sealing decision

A crate exports a `BuiltinRule` marker used only to identify its own rule set. Downstream implementation would prevent future blanket implementations. Design a sealed-trait pattern, then list the operations downstream users can still perform. Explain why sealing is a compatibility decision, not merely privacy.

### Extension trait discipline

Create an extension trait for `[Record]` with one domain-specific query. Keep the implementation local and the method discoverable. Then challenge the design: would a free function communicate the operation more clearly? Use method-chaining, namespace ownership, and potential name collisions as criteria.

: implementation ledger

For every `impl` in one laboratory or capstone module, record the trait owner, type owner, implementation owner, and whether a blanket implementation could overlap with a plausible future type. Redesign one relationship whose ownership is unclear.

### Interleaved reasoning pass

1. For **Predict whether an implementation satisfies coherence and orphan rules**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the coherence ownership map.
2. For **Detect overlapping blanket implementations and downstream compatibility hazards**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the coherence ownership map.
3. For **Use a newtype to establish local implementation ownership**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the coherence ownership map.
4. For **Design sealed and extension traits deliberately**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the coherence ownership map.

5. Identify one guarantee from an earlier course that a careless implementation of **Coherence and Implementation Ownership** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Integrate two foreign-style model types with two local formatting and validation contracts.

Requirements:

- one local extension trait over a foreign-like type;
- one newtype implementing an external standard trait;
- one intentionally rejected blanket implementation with a written overlap proof;
- a sealed internal capability and public read-only extension surface;
- compile-fail evidence for a forbidden downstream implementation;
- a semver note describing the implementation space reserved by each blanket impl.

The executable starter and reference implementation are in [module-03-coherence-adapters](../../labs/module-03-coherence-adapters/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

### Laboratory acceptance trace

Before opening the reference implementation for **Coherence Adapters**, record:

- the public behavior that demonstrates **Predict whether an implementation satisfies coherence and orphan rules**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Create local rule types and local `Rule`/`RuleFactory` traits. Use a newtype to adapt a closure into a rule instead of attempting to implement a foreign callable trait for a foreign closure type.

Decide explicitly:

- `Rule` is open to downstream implementation or sealed;
- `RuleFactory` is public or internal;
- which blanket implementations are forbidden to preserve future adapters;
- how built-in rule identifiers avoid collisions.

Record the implementation-ownership map.

### Capstone invariant trace

For the Module 23 Review Engine increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

You must predict orphan and overlap outcomes, repair a forbidden relationship with a newtype, explain the cost of a public blanket implementation, and defend the capstone's extension policy.

Oral prompt: **“What implementation space does this API consume today, and who might need it tomorrow?”**
### Closed-book reconstruction

1. What relationship does the orphan rule require your crate to own?
2. Why can two individually reasonable blanket implementations overlap?
3. What semantic responsibility does a newtype acquire?
4. Which future implementations can a public blanket implementation consume?
5. When does sealing protect evolution, and when does it prevent a legitimate extension?

### Independent transfer

A foreign timestamp type must participate in a foreign formatting trait, and downstream crates also need local formatting policy. Produce a coherence-safe design using a local type or local trait. Include conversion cost, discoverability, implementation ownership, and the future extension space you intentionally preserve.

### Closed-book defense

In five minutes, answer “Which crate owns the right to create an implementation, and how can a public design preserve coherence without giving up adaptation?” using the **coherence ownership map**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside Review Engine. A list of APIs without the deciding relationship is incomplete.
