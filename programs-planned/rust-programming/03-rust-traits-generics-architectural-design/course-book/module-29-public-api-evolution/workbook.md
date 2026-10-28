# Workbook — Module 29: Public API Evolution

[Return to the chapter](index.md) · [Open the Review Engine engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether you can use **Public API Evolution** without relying on surface syntax. Keep the module question in view: *How can a public trait-based API evolve when downstream crates may both call it and implement it?* For every task, identify the program point where the decisive type, ownership, dispatch, failure, or cost relationship is established. Compile only after committing to a prediction, and preserve the smallest counterexample that changes your model.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Public API Evolution** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-required-method-addition.rs`](../../compiler-labs/module-09/01-required-method-addition.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-default-method-collision.rs`](../../compiler-labs/module-09/02-default-method-collision.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-new-supertrait-obligation.rs`](../../compiler-labs/module-09/03-new-supertrait-obligation.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-blanket-impl-downstream-conflict.rs`](../../compiler-labs/module-09/04-blanket-impl-downstream-conflict.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-sealed-compatibility-surface.rs`](../../compiler-labs/module-09/05-sealed-compatibility-surface.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-nonexhaustive-matching.rs`](../../compiler-labs/module-09/06-nonexhaustive-matching.rs) | Pass or fail? What exact rule decides? |
| 7 | [`07-version-adapter.rs`](../../compiler-labs/module-09/07-version-adapter.rs) | Pass or fail? What exact rule decides? |
| 8 | [`08-strengthened-bound.rs`](../../compiler-labs/module-09/08-strengthened-bound.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 03-rust-traits-generics-architectural-design
```

## Part 2 — Diagnose and repair

A proposed minor release adds a supertrait, a default `name` method, and `impl<T: Display> Rule for T`. Build a hazard register showing which downstream callers and implementors can fail. Redesign the release using an extension trait, adapter newtype, or new major-version contract.

## Part 3 — Focused exercises

1. Classify fifteen trait changes by caller and implementor risk.
2. Show a default-method name collision.
3. Demonstrate a new blanket implementation conflicting downstream.
4. Decide whether to seal a public trait under two ecosystem models.
5. Use `#[non_exhaustive]` for a public error enum and explain its limits.
6. Design a V1-to-V2 adapter and identify lost semantics.
7. Write a positive downstream compile fixture.
8. Write a negative sealed-trait fixture with intended cause.
9. Produce an MSRV and public-dependency audit.
10. Build the capstone semver hazard register.

### Breaking-change analysis

A public trait is implemented by downstream crates. Classify each proposed change:

1. add a required method;
2. add a method with a default;
3. add a supertrait;
4. add a generic parameter with a default;
5. add a blanket implementation;
6. change an associated type bound;
7. seal the trait in a minor release.

For each, analyze downstream callers and downstream implementors separately. Do not assume a default method is automatically harmless.

### Non-exhaustive models

Design a public error enum and configuration struct that may gain variants or fields. Compare `#[non_exhaustive]`, private fields with constructors, and an opaque error type with inspection methods. State what pattern matching downstream users lose and what evolution room the crate gains.

### Versioned extension surface

A plugin API needs a new operation that old implementors cannot sensibly default. Compare: a new `PluginV2` supertrait, a capability subtrait, an adapter from V1, and a breaking major release. Choose a migration path and show how callers discover support.

### MSRV review

A patch uses a language or library feature newer than the declared minimum supported Rust version. Explain why successful compilation on the author's toolchain is insufficient. Define a compatibility matrix that tests the declared MSRV and current stable separately.

: downstream simulation

Create a tiny external consumer crate for Review Engine. It should call the public API and implement any intentionally open trait. Make one proposed evolution and observe which consumer source changes. Record the compatibility lesson before changing the library.

### Release council — evaluate a trait change from both downstream roles

A public `Rule` trait currently has one required method:

```rust
trait Rule {
    fn evaluate(&self, input: &Submission) -> Finding;
}
```

The crate wants to add stable rule identifiers, optional explanation text, and batch evaluation. Consider these proposals:

1. add three required methods;
2. add three default methods;
3. add a supertrait requiring `Display`;
4. create a sealed companion trait for built-in metadata;
5. introduce `RuleV2` plus an adapter from `Rule`;
6. keep `Rule` unchanged and add free helper functions or wrapper types.

For each proposal, complete a matrix for existing callers, external implementors, method-resolution risk, coherence space, MSRV, and future extensibility. Choose a release strategy and write a migration example. Include one fixture representing a third-party implementation and one representing a caller using a trait object.

Finally, add a new built-in rule through the chosen design. Explain why successful compilation of the main crate is insufficient evidence for a public API change.

## Part 4 — Independent laboratory

Start from a small public plugin contract and evolve it through two versions.

Requirements:

- downstream-style fixture crate implementing V1;
- a proposed breaking change and hazard analysis;
- a nonbreaking extension trait where semantics permit;
- a V2 trait where new required semantics cannot be defaulted;
- a newtype adapter from V1 to V2 with explicit information loss;
- a sealed internal trait and one open public trait;
- compile-positive and compile-negative compatibility evidence.

The executable starter and reference implementation are in [module-09-evolvable-sdk](../../labs/module-09-evolvable-sdk/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

## Part 5 — Capstone transfer

Audit every public capstone trait and type:

- intended callers and implementors;
- open or sealed status;
- required and default methods;
- associated items;
- dyn compatibility;
- blanket implementations;
- object lifetime expectations;
- MSRV-sensitive features;
- migration plan for one hypothetical V2 requirement.

Add downstream-style integration tests and compile-fail documentation for prohibited construction.

## Part 6 — Reconstruct and defend

Pass when you can find non-obvious downstream breakage, redesign a minor release, and explain why public trait evolution must consider implementation space.

Oral prompt: **“Which future change did this extension policy make impossible, and why is that trade acceptable?”**
### Closed-book reconstruction

1. How can adding a required method break downstream implementors without breaking callers?
2. What evolution room does sealing preserve?
3. When does a default method preserve source compatibility but change semantics?
4. What does `#[non_exhaustive]` require from downstream matching?
5. How do MSRV and semver interact with public trait syntax and standard-library use?

### Independent transfer

Take a public plugin trait with downstream implementations and plan two years of evolution. Add one capability, one error detail, and one configuration option. Compare a required method, default method, extension trait, versioned trait, adapter, and sealed redesign. State the migration path for both callers and implementors.
