# 29 — Public API Evolution

**Course 3, day 9 · Module 29 of 60**  
`██████████░░░░░░░░░░` **29/60**

[← Module 28: Boundary Traits and Adapters](../module-28-boundary-traits-and-adapters/index.md) · [Course 3 overview](../index.md) · [Sixty-module map](../../../COURSE_MAP.md) · [Module 30: Architectural Synthesis →](../module-30-architectural-synthesis/index.md)

## The question

> How can a public trait-based API evolve when downstream crates may both call it and implement it?

## Why this comes now

A private trait can be changed whenever its crate changes. A public trait may have downstream callers, implementors, blanket impls, and MSRV constraints. This module makes evolution part of the initial design and shows why sealing, non-exhaustive models, adapter layers, and versioned traits preserve room to move.

## What you will be able to do

- Classify public trait changes by downstream source-compatibility risk.
- Design default methods and extension points without accidental semantic promises.
- Use sealing, non-exhaustive data, adapters, and versioned traits appropriately.
- Test compile-time and behavioral compatibility claims.
- Produce a semver hazard register and migration plan.

## Core model

### Public traits have two downstream audiences

When a crate publishes a trait, downstream code may be:

1. a **caller** using the trait in a bound or through a trait object;
2. an **implementor** providing behavior for its own type.

Changes affect these audiences differently. A new required method may leave callers unchanged while breaking every external implementation. A new blanket implementation may compile your crate but conflict with an implementation a downstream crate already owns. Public trait design must model both directions.

### Adding trait items can be breaking

Adding a required method breaks existing implementations:

```rust
pub trait Rule {
    fn evaluate(&self, input: &Submission) -> Vec<Finding>;
    // Adding `fn severity(&self) -> Severity;` requires every implementor to change.
}
```

A default method can preserve source compatibility:

```rust
pub trait Rule {
    fn evaluate(&self, input: &Submission) -> Vec<Finding>;

    fn enabled(&self) -> bool {
        true
    }
}
```

But “has a default” does not automatically mean “non-breaking.” Review:

- method-name collisions with inherent or extension methods;
- dyn compatibility of the trait;
- new supertrait or bound requirements;
- behavior changes for existing callers;
- whether the default is semantically valid for every implementation.

Adding an associated type, associated constant, or supertrait is generally more disruptive because implementations must satisfy the new relationship.

### Blanket implementations can break future and downstream code

Suppose version 1 publishes:

```rust
pub trait Render {
    fn render(&self) -> String;
}
```

A downstream crate implements it for `LocalType`. In version 1.1, your crate adds:

```rust
impl<T: Display> Render for T { ... }
```

If `LocalType: Display`, the new blanket implementation overlaps with downstream code. The release may be semver-incompatible even though no existing item was removed.

Treat blanket implementations as public surface. Before adding one, test representative downstream crates and review the entire family it claims.

### Sealing trades extension for evolution room

A sealed trait prevents external implementations, allowing the defining crate to add methods or reason exhaustively about implementors more safely. This is a legitimate design when the trait is a public capability of built-in types rather than a plugin point.

State the policy clearly:

- **open trait:** downstream implementation is supported;
- **sealed trait:** downstream use is supported, implementation is not;
- **internal trait:** neither is a public contract.

Do not expose a public trait accidentally and discover later that external implementations prevent evolution.

### `#[non_exhaustive]` preserves data-model room

A public enum without `#[non_exhaustive]` invites exhaustive downstream matching. Adding a variant is then breaking.

```rust
#[non_exhaustive]
pub enum FindingKind {
    Error,
    Warning,
}
```

Downstream matches must include a wildcard arm. This preserves room for variants but reduces exhaustive guarantees for callers.

For structs, `#[non_exhaustive]` prevents downstream construction with a literal and can preserve room for fields. Constructors and accessors then become the supported boundary.

Use the attribute because future extension is plausible, not reflexively. Closed domain enums benefit from exhaustiveness.

### Versioned traits make incompatible contracts explicit

When a contract changes substantially, a new trait can be clearer than stretching the old one:

```rust
pub trait RuleV1 {
    fn evaluate(&self, input: &Submission) -> Vec<Finding>;
}

pub trait RuleV2 {
    type Error;
    fn evaluate(&self, input: &Submission, out: &mut Vec<Finding>) -> Result<(), Self::Error>;
}
```

Provide adapters where semantics permit:

```rust
struct V1Adapter<R>(R);
```

A migration path should state:

- what behavior changed;
- which old guarantees remain;
- whether adaptation is lossless;
- deprecation timeline;
- how callers and implementors migrate separately.

Do not call a semantic break a rename.

### Object-facing changes require a dyn review

A method can be valid for static trait use but make the trait no longer dyn-compatible. Adding an associated constant, generic associated type, generic dispatchable method, or opaque-returning method may invalidate `dyn Trait` users.

If the trait is used as an object, maintain a small compile-time compatibility fixture:

```rust
fn assert_dyn_compatible(_: &dyn Rule) {}
```

Also test important object type aliases, such as `Box<dyn Rule + Send + Sync + 'static>`.

Sometimes the correct evolution is to keep a small dyn-compatible core trait and add a static extension trait for richer operations.

### MSRV is part of the product contract

The minimum supported Rust version determines which language and standard-library features downstream users may compile with. Raising MSRV can break users even when the public Rust API is unchanged.

A responsible policy states:

- current MSRV;
- how and when it may increase;
- whether increases require a major or minor release under the project’s policy;
- which CI job tests it;
- whether dependencies can raise it indirectly.

Do not declare an MSRV that is not tested. Pinning a development toolchain is not the same as proving a minimum version.

### Public dependencies can leak into the API

If a public method returns a dependency’s type, that dependency version becomes part of your compatibility surface. Upgrading it may create type mismatches for callers or force synchronized dependency versions.

Prefer domain-owned types at stable boundaries when practical. Re-export a dependency type deliberately when interoperability is the product goal, and document that decision.

### Compatibility tests need downstream perspective

Internal unit tests cannot prove that downstream code still compiles. Maintain small fixture crates that:

- implement open traits;
- use trait objects;
- rely on associated-type constraints;
- import extension traits;
- match non-exhaustive enums correctly;
- compile on the declared MSRV;
- avoid private implementation details.

Behavioral tests should also protect defaults and ordering. Compilation compatibility without semantic compatibility is insufficient.

### Review every public change with a matrix

| Change | Callers | External implementors | Trait-object users | Coherence |
|---|---|---|---|---|
| add required method | usually compile | break | maybe | unchanged |
| add default method | possible collision/behavior | usually compile | dyn review | unchanged |
| add supertrait | stronger bounds | break unless already satisfied | dyn review | unchanged |
| add blanket impl | may change method resolution | may overlap | usually indirect | high risk |
| add enum variant | exhaustive matches break | n/a | n/a | unchanged |
| raise MSRV | compile break | compile break | compile break | unchanged |

A release decision should be based on this downstream model, not only on whether the defining crate’s tests pass.

#### Two audiences

Public traits have callers and implementors. A change can preserve callers while breaking implementors, or the reverse.

- callers depend on available methods, bounds, associated items, dyn compatibility, and semantics;
- implementors depend on required items, supertraits, coherence space, and allowed state.

#### Unknown code matters

Library review must imagine downstream types and implementations not present in the repository. A local test suite cannot enumerate the ecosystem.

#### Compatibility dimensions

- source compatibility;
- binary/ABI compatibility, generally not promised by ordinary Rust libraries;
- behavioral compatibility;
- MSRV compatibility;
- inference and method-resolution compatibility;
- serialization or textual format compatibility.

Record which dimensions the crate promises.

#### Adding a required method

Breaks every downstream implementation. Use a major version or a new trait.

#### Adding a default method

Usually avoids implementation edits, but can collide with inherent or extension methods, alter method resolution, and create a new semantic promise. Review names and laws.

#### Adding an associated type or constant

Required associated items break implementors. Associated constants also affect dyn compatibility. A new GAT can fundamentally change the trait's use.

#### Adding a supertrait

Every implementor must satisfy the new prerequisite. Trait objects may also be affected by supertrait dyn compatibility and auto-trait behavior.

#### Changing bounds

Strengthening input bounds rejects callers and implementors. Weakening output guarantees can break callers. Adding bounds to opaque returns changes exposed capability and may affect downstream assumptions.

#### Additive syntax, conflicting relationship

A new blanket implementation can overlap with a downstream implementation that compiled against the prior release. The library did not see that code, but the upgrade fails.

#### Conservative policy

Treat broad blanket implementations as major API decisions. Document them, test representative overlap scenarios, and prefer explicit adapter newtypes when semantics are optional.

#### New trait implementations for existing public types

Even implementing an existing trait for your own public type can create method ambiguity or inference changes downstream. “Adding an impl” is not always harmless.

#### Future-proofing fallacy

Reserving every possible implementation through blanket impls does not future-proof an API. It prevents downstream adaptation and may encode weak semantics. Reserve only relationships the crate can defend.

#### Sealing controls implementors

A sealed trait can gain internal implementations and required details with fewer downstream break risks, because external implementation was never promised. Callers can still use it as a bound.

#### `#[non_exhaustive]` controls construction and matching

For public enums or structs, `#[non_exhaustive]` tells downstream users to allow future variants or fields. It does not apply the same way as trait sealing and does not solve implementation overlap.

#### Open data versus open behavior

An enum is closed behaviorally to its defining crate unless non-exhaustive matching is required downstream; a trait may be open to implementations. Choose independently:

- closed variants, open operations;
- open implementors, fixed methods;
- sealed implementors, evolving internal methods.

#### Honest documentation

State whether downstream implementation is supported. Users should not infer extension policy from visibility alone.

#### New contract, new trait

When semantics or required methods change materially, define `RuleV2` or a differently named contract rather than contorting defaults to preserve incompatible meanings.

#### Adapter bridge

Provide an adapter from old to new when semantics can be preserved:

```rust
struct V1Adapter<T>(T);
impl<T: RuleV1> RuleV2 for V1Adapter<T> { /* translate */ }
```

Document information loss and error mapping.

#### Deprecation sequence

1. introduce new trait and adapters;
2. migrate internal implementations;
3. provide compiler-guided deprecations;
4. publish migration examples;
5. remove old surface only at the promised version boundary.

#### Avoid permanent dual abstractions

A migration layer should have an exit plan. Two nearly identical traits increase coherence and method-resolution complexity.

#### Positive compilation tests

Maintain small downstream-style crates that use the public API through documented patterns. They detect accidental visibility, bound, and inference changes.

#### Negative tests

Compile-fail examples prove restrictions such as sealed implementation or unavailable typestate methods. They must fail for the intended cause.

#### Behavioral contract tests

Source compatibility is insufficient if output ordering, errors, or law semantics change. Golden files can help for stable text formats; property-style law tests help implementations.

#### Version comparison

An API diff tool can identify surface changes, but human review is still needed for coherence, semantic laws, and method resolution. This course uses explicit hazard registers rather than claiming automation proves semver safety.

#### Minimum supported Rust version

Using a newer language or standard-library feature raises MSRV even if the public signatures appear unchanged. Record the policy and test it with the declared compiler.

#### Public dependencies

A dependency type appearing in a public signature becomes part of the consumer contract and can constrain upgrades. Prefer local domain types at stable boundaries when translation is reasonable.

#### Feature combinations

Optional implementations and blanket impls behind features can create different coherence surfaces. Test supported combinations and avoid features that silently change semantics.

#### Documentation examples are API tests

Examples teach construction and method resolution. Keep them compiling under the MSRV and current toolchain, and avoid exposing unstable internal type names.

Version 1:

```rust
pub trait Rule {
    fn evaluate(&self, input: &Submission, out: &mut Vec<Finding>);
}
```

The library wants rule identity and configuration explanation.

Adding required `id` and `explain` breaks downstream implementations. Default methods could preserve compilation but cannot invent stable unique IDs. A better migration may add a separate `DescribedRule` extension trait, keep `Rule` minimal, and require built-in registry entries to carry identity outside the trait. If every runtime caller truly needs identity, a `RuleV2` migration is more honest.

The answer depends on the original documented semantic contract. Compatibility cannot be decided from syntax alone.

### Public traits evolve in two directions

A public trait creates two distinct downstream populations:

1. **callers**, which use values through the trait;
2. **implementors**, which provide implementations in other crates.

A change may preserve one population while breaking the other. Adding a required method can leave caller code unchanged but break every external implementation. Adding a default method avoids that immediate compile break, yet can collide with an inherent or extension method already used downstream. Strengthening a bound can reject previously valid callers and implementations. Adding a broad blanket implementation can overlap with an implementation a downstream crate was legally able to write yesterday.

Use a change matrix before modifying a public trait:

| Proposed change | Existing callers | Existing implementors | Future design space |
|---|---|---|---|
| add required method | usually source-compatible | breaking | narrows implementation freedom |
| add default method | often source-compatible | usually compiles; method resolution may change | consumes a method name |
| add supertrait | may strengthen usable operations | breaking unless already satisfied | couples two contracts |
| strengthen generic bound | rejects some callers | may reject implementations | narrows accepted type set |
| add blanket implementation | may change method resolution | may overlap downstream impls | consumes coherence space |
| seal trait | callers usually unaffected | prevents new external implementations | preserves crate control |
| add non-exhaustive variant | requires wildcard-aware callers | not an implementation issue | preserves data-model growth |

#### Sealing is an evolution decision, not a hiding trick

Seal a trait when external implementation is not part of the product promise and the crate needs room to add methods or implementations. Document that callers may use the trait but cannot implement it. If third-party implementation is the core value, sealing would destroy the extension model; versioned traits or adapter registration may be more honest.

#### Default methods are not free compatibility

A default body must be correct for every existing implementation using only already-promised primitives. If it assumes a new law, adding it silently changes the semantic contract. A new method name can also affect resolution in downstream code. Treat default additions as compatibility reviews, not automatic non-breaking changes.

#### Version behavior, not only names

When a contract must change materially, a new trait or versioned adapter can be clearer than accumulating defaults and deprecated methods. Provide an explicit bridge from old to new where semantics allow it, and test both old callers and representative external implementors in separate fixture crates.

#### MSRV belongs to the public contract

Using a newer language or standard-library feature can be a breaking release for users whose toolchain remains within the documented minimum. Record the minimum supported Rust version, test it in CI, and review generated code from macros against the same boundary. Semver, coherence, and MSRV are connected: downstream compatibility includes source, implementation rights, and toolchain availability.

## Use the idea in a complete program

The course capstone is **Review Engine**, a policy evaluation engine with static boundaries, a dynamic rule registry, and typestate construction. Review the public extension surface from both downstream perspectives: callers and implementors. Preserve evolution room with sealing, non-exhaustive data, and compatibility tests. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-09-evolvable-sdk/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 30 when you can:

- answer the module question—“How can a public trait-based API evolve when downstream crates may both call it and implement it?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Classify public trait changes by downstream source-compatibility risk;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [Cargo SemVer compatibility](https://doc.rust-lang.org/cargo/reference/semver.html)
- [Rust API Guidelines: Dependability](https://rust-lang.github.io/api-guidelines/dependability.html)

[← Module 28](../../../03-rust-traits-generics-architectural-design/course-book/module-28-boundary-traits-and-adapters/index.md) · [sixty-module map](../../../COURSE_MAP.md) · [Module 30 →](../../../03-rust-traits-generics-architectural-design/course-book/module-30-architectural-synthesis/index.md)

## Continue

1. Complete the [Module 29 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 29 — Evolvable SDK](../../labs/module-09-evolvable-sdk/README.md) from its public contract.
3. Apply the Module 29 increment in the [Review Engine engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
