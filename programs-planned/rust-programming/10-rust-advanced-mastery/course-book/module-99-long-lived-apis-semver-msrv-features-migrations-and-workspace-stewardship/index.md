# Module 99 — Long-Lived APIs: SemVer, MSRV, Features, Migrations, and Workspace Stewardship

**Course 10 · Day 9 · Module 99 of 100**
`█████████████████████████` **99/100**

[Program](../../../README.md) · [Course 10](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-09-versioned-sdk/README.md) · [AxiomStore guide](../capstone.md)

[← Module 98: Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration](../module-98-verification-beyond-examples-compile-fail-property-model-fuzz-miri-and-concurrency-exploration/index.md) · [Module 100: Architectural Synthesis: Building and Defending a Long-Lived Rust System →](../module-100-architectural-synthesis-building-and-defending-a-long-lived-rust-system/index.md)

## The question

> How do you evolve a Rust library, data format, feature graph, and workspace without silently breaking downstream source, behavior, tools, or stored data?

## Why this comes now

Course 3 introduced public API evolution and Course 9 covered release artifacts. Module 99 treats maintenance as a technical design problem spanning source compatibility, trait implementations, inference, feature unification, minimum supported Rust version, file formats, migrations, deprecations, and workspace policy. A change can be semver-significant even when current tests pass. Long-lived systems need compatibility matrices and migration ownership before the first release, not after the first breaking change.

Course 3 addressed API evolution and Course 9 addressed release identity. This module treats source, feature, toolchain, data-format, and migration compatibility as one long-lived stewardship problem.

A library becomes difficult not when it has many lines but when many parties depend on different surfaces: source signatures, trait implementations, inference, feature combinations, minimum toolchains, stored bytes, migrations, generated artifacts, and operational behavior. Module 99 makes those audiences explicit before changes are called compatible.

### Prerequisite bridge

Module 98 established **Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration**. Before continuing, verify that you can build a verification matrix that names uncovered claims and the reason they remain manual review obligations. This module preserves that capability and adds the ability to analyze a proposed change from the perspectives of downstream callers, downstream implementors, type inference, pattern matching, and stored data. Module 100, **Architectural Synthesis: Building and Defending a Long-Lived Rust System**, will rely on both when it asks: *Can you turn ten courses of mechanisms into one restrained architecture whose guarantees, unsafe core, verification evidence, compatibility policy, and operating limits can survive independent review?*

### Scope boundary

This module owns the reasoning for **long-lived apis: semver, msrv, features, migrations, and workspace stewardship** inside Course 10. The course selects stable mechanisms that serve real product requirements. It does not reward obscure syntax, nightly-feature collecting, unsafe code retained for display, or lower-level compiler output used where source-level reasoning is already decisive. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

After completing this module, you will be able to:

- analyze a proposed change from the perspectives of downstream callers, downstream implementors, type inference, pattern matching, and stored data
- define and test an MSRV policy without confusing the manifest declaration with actual verification
- design additive Cargo features that do not change unrelated semantics or create unsupported combinations
- version persistent formats and implement deterministic, failure-atomic migrations with preserved fixtures
- use deprecation, adapters, extension traits, sealed traits, and non-exhaustive models according to extension ownership
- govern a multi-crate workspace through dependency direction, shared policy, release order, and compatibility evidence

## Core model

### The governing model

Use a **compatibility and migration matrix**. Rows are proposed changes; columns are downstream callers, downstream implementors, type inference, exhaustive matches, feature unification, MSRV, persistent data, tools, and release artifacts. A change is safe only for the audiences the project explicitly supports and tests.

### 1. Compatibility has several audiences

A function signature affects callers. A public trait affects implementors as well as callers. A public enum affects exhaustive matches. Blanket implementations affect coherence and method resolution. Defaults affect behavior. Serialization formats affect data written by older binaries. Evaluate each change against all audiences that own code or data outside the current crate.

**Separate audiences.** Add a defaulted method to a public trait. Which source callers remain compatible, and which third-party implementors or trait objects may still be affected?

### 2. SemVer is a decision framework, not a compiler theorem

Rust’s evolving ecosystem has edge cases around inference, auto traits, object safety, and implementation overlap. Adding a generic parameter with a default, a trait method with a default body, or a blanket implementation can still disrupt downstream code. Maintain representative downstream fixtures and run them against candidate releases. Document which forms of extension are supported instead of relying on “technically additive.”

**Test feature unification.** If feature `fast` disables validation, explain why it is not an additive Cargo capability and what happens when dependencies request both modes.

### 3. MSRV is a tested compatibility promise

The `rust-version` field communicates the intended minimum toolchain and lets Cargo diagnose some incompatibility. It does not prove that all code, build scripts, dependencies, features, and documentation compile there. CI must run the selected workspace and feature combinations on the declared minimum. Raising MSRV needs a release policy and downstream communication because it changes who can build the crate.

**Prove the MSRV.** Distinguish declaring `rust-version` from compiling supported feature sets on the minimum toolchain.

### 4. Features should be additive capabilities

Feature unification means a dependency may be built with the union of features requested by several graph paths. Features that disable behavior, select mutually exclusive global modes, or change the meaning of existing APIs compose poorly. Prefer additive optional integrations and explicit runtime configuration for policy. Test no-default, each supported feature, and meaningful combinations; do not claim every power-set combination unless you support it.

**Version stored data.** State the read-old/write-new policy and the exact behavior for unknown future versions.

### 5. Persistent formats need read and write policy

A new writer version does not automatically justify dropping old readers. Define which versions can be read, which version is written by default, whether downgrade is possible, and how unknown fields or records are handled. Migrations should parse the old format into a validated model, transform that model, encode a complete candidate, verify it, and replace storage failure atomically. Keep golden fixtures from every supported version.

**Migrate failure-atomically.** Identify when the old source remains authoritative, when the candidate becomes committed, and how verification precedes replacement.

### 6. Deprecation needs a destination

A deprecation warning without a replacement and semantic comparison merely transfers maintenance work to callers. Provide an adapter or new method, state behavior differences, and keep the old route long enough for supported consumers. If a safe migration is impossible, make the breaking release and migration guide explicit rather than hiding a new interpretation behind the old name.

**Deprecate toward a destination.** Write a deprecation note that names the replacement and semantic difference rather than only a removal date.

### 7. Workspace policy controls coupling

A workspace should have an intentional dependency direction. Core crates should not depend on CLI or integration crates. Shared versions and lints can reduce drift, but blanket workspace inheritance can also make publishing boundaries unclear. Record which crates are public, which release together, which may remain internal, and how examples and compatibility fixtures consume them as external users.

**Control workspace coupling.** Identify which internal crate boundaries are implementation details and which become published compatibility commitments.

### 8. Compatibility evidence belongs in the release

A release dossier should include current and MSRV checks, supported feature matrices, downstream compile fixtures, format fixtures, migration tests, public API review, and changed guarantees. The absence of a known break is not equivalent to compatibility evidence. Make unsupported combinations explicit so users can distinguish policy from omission.

**Package evidence.** List the lockfile, toolchain, feature matrix, fixtures, and artifact identity that accompany one release decision.

### Worked evolution: introducing AXIOM02

Assume AXIOM02 adds a schema tag before each record while AXIOM01 remains in deployed archives. A complete compatibility decision answers at least these questions:

```text
Which versions can the new reader open?
Which version does the new writer emit?
How is an unknown future magic rejected?
Can old software open newly written files?
Is explicit migration available?
What happens if migration validation or replacement fails?
Which CLI output reveals the active schema?
Which fixtures remain permanent?
```

“Keep backward compatibility” is not a design. One reasonable policy is: the new reader accepts AXIOM01 and AXIOM02; the default writer emits AXIOM02 after the release transition; old readers are not forward compatible; explicit migration reads old bytes into the stable model, validates and encodes a complete candidate, verifies it with the new reader, and only then replaces or creates the destination. Unknown versions fail without reinterpretation.

Source compatibility has different audiences. Adding a public `SchemaTag` field to `Record` may break constructors and pattern matches. Adding a method to a public trait may burden downstream implementors even with a default through object-safety or blanket interactions. Changing a feature from “add integration” to “disable validation” makes feature unification semantically dangerous. Raising MSRV affects builders even when source APIs are unchanged.

The release record must therefore include source fixtures, old-format fixtures, migration fixtures, supported feature combinations, and actual compilation on the declared minimum toolchain. `rust-version = "1.97"` is metadata until the matrix executes.

### A decision table

| Design question | Principled evidence or mechanism | Weak substitute to reject |
|---|---|---|
| Who can break? | analyze callers, implementors, inference, matches, data, and tools separately | only compiling the current workspace |
| Is a feature additive? | it adds capability under feature unification | it disables or globally changes existing semantics |
| Is MSRV a real promise? | execute supported feature/workspace checks on the declared minimum | manifest declaration without CI evidence |
| How does stored data evolve? | versioned read/write policy and failure-atomic migration | silently reinterpreting old bytes |

### A rigorous working procedure

1. Inventory every supported downstream audience and persistent artifact.
2. Write the proposed change without assuming SemVer classification.
3. Evaluate each audience separately: compile, implement, infer, match, unify features, read data, run tools.
4. Define migration or adapter behavior before changing the writer or public API.
5. Execute compatibility fixtures on the declared MSRV and supported feature combinations.
6. Publish the decision, deprecation destination, residual incompatibilities, and rollback path with the artifact.

### Failure patterns and principled repairs

Stewardship failures come from changing code without modeling the downstream parties that depend on it. Repair them by listing callers, implementors, stored data, enabled feature combinations, supported toolchains, and release artifacts, then make compatibility and migration decisions against that explicit surface.

### Adding a trait method with a default and assuming no implementor risk

Run downstream implementation fixtures and review object/blanket interactions.

### Using mutually exclusive Cargo features as global modes

Prefer additive integrations or explicit runtime policy; reject unsupported combinations clearly.

### Migrating in place before validating the candidate

Read old data, transform a model, encode and verify a candidate, then replace atomically.

### Deprecating without a semantic destination

Provide a replacement, adapter, difference table, and removal policy.

### What the compiler cannot decide for you

Cargo and the compiler can enforce syntax, type, and selected dependency constraints. They cannot prove that all downstream source still infers the same type, that every third-party implementation remains viable, that old data migration is safe, or that the declared MSRV was actually exercised. SemVer is a communication and risk framework, not an automatic theorem.

Compatibility is multidimensional. A source-compatible change may alter stored bytes; a data-compatible reader may change output ordering; an additive feature may become nonadditive under unification. Record the dimensions instead of using one green label.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For analyze a proposed change from the perspectives of downstream callers, downstream implementors, type inference, pattern matching, and stored data, construct one positive and one causal negative example. Mark the first decisive fact in the **compatibility and migration matrix** and state which evidence could falsify the claim.

2. **Outcome 2.** For define and test an MSRV policy without confusing the manifest declaration with actual verification, construct one positive and one causal negative example. Mark the first decisive fact in the **compatibility and migration matrix** and state which evidence could falsify the claim.

3. **Outcome 3.** For design additive Cargo features that do not change unrelated semantics or create unsupported combinations, construct one positive and one causal negative example. Mark the first decisive fact in the **compatibility and migration matrix** and state which evidence could falsify the claim.

4. **Outcome 4.** For version persistent formats and implement deterministic, failure-atomic migrations with preserved fixtures, construct one positive and one causal negative example. Mark the first decisive fact in the **compatibility and migration matrix** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

Treat V1 and V2 configuration formats as separate contracts. Decode V1, transform into a stable model, encode V2, decode the candidate again, and only then make it eligible for installation. The migration must never reinterpret malformed V1 as valid V2.

```rust
#[derive(Clone, Debug, PartialEq, Eq)]
struct ConfigV1 {
    path: String,
}

#[derive(Clone, Debug, PartialEq, Eq)]
struct ConfigV2 {
    path: String,
    verify_on_open: bool,
}

impl From<ConfigV1> for ConfigV2 {
    fn from(old: ConfigV1) -> Self {
        Self {
            path: old.path,
            verify_on_open: true,
        }
    }
}

fn migrate_v1(bytes: &[u8]) -> Result<Vec<u8>, MigrationError> {
    let old = decode_v1(bytes)?;
    let candidate = encode_v2(&ConfigV2::from(old))?;
    decode_v2(&candidate)?;
    Ok(candidate)
}
```

### Trace the example

Write a table for `ConfigV1 -> ConfigV2`: preserved fields, new default, invalid old inputs, unknown new fields, candidate validation, and failure state. Then introduce a V3 proposal and decide whether the current public types or decoder architecture leave enough evolution room.

For the crate API, add one public enum variant and one trait method on paper. Analyze callers, exhaustive matches, implementors, objects, and generated documentation separately. The exercise is complete only when “minor change” is replaced by a documented audience-specific judgment.

### Use it in AxiomStore

AxiomStore defines stable `AXIOM01` bytes, a legacy text migration, a versioned public schema description, a no-default feature baseline, and an MSRV policy. Course 10’s final independent change introduces `AXIOM02` schema tags while preserving reads of `AXIOM01`. The change must update compatibility fixtures, migration behavior, CLI evidence, and the architecture decision record without exposing internal codecs as permanent public API.

AxiomStore’s compatibility record includes:

```text
surface: Rust source / format bytes / CLI / feature / MSRV / artifact
current contract
proposed change
supported downstream audiences
adapter or migration
negative fixture
toolchain/feature evidence
rollback path
removal or write-policy date
```

AXIOM01 remains readable when AXIOM02 is introduced. The default writer changes only after fixtures, migration behavior, CLI schema output, and documentation move together.

## Practice sequence

1. **Trait evolution review.** Evaluate a defaulted method against callers, implementors, objects, and blanket impls.
2. **Feature design.** Convert two mutually exclusive “modes” into additive capabilities plus explicit runtime policy.
3. **MSRV matrix.** Define no-default, default, and all-supported feature checks on the minimum and current toolchains.
4. **Failure-atomic migration.** Implement V1-to-V2 conversion with candidate revalidation and unchanged source on failure.
5. **Deprecation route.** Write a complete migration guide, adapter, semantic difference table, and removal criterion.

Complete the [workbook](workbook.md) and [Versioned SDK](../../labs/module-09-versioned-sdk/README.md). Manual-review investigations must name the downstream audience and cannot be answered by compiling only the workspace head.

## Ready to continue

Proceed to synthesis when you can analyze source, implementor, inference, feature, MSRV, data, and artifact compatibility separately; design a candidate-first migration; and publish a deprecation with a real destination. You should be able to explain why passing on the newest toolchain says nothing about the declared minimum.

## Primary Rust references

- Cargo Reference: rust-version, features, workspaces, and resolver
- The Rust API Guidelines and SemVer compatibility guidance
- The Rust Reference: visibility, traits, and non-exhaustive items

Use Cargo’s `rust-version`, features, workspace, and SemVer guidance as operational contracts. Keep actual support claims tied to executed matrices and stored-format fixtures rather than manifest text alone.

## Continue

Continue to [Module 100 — Architectural Synthesis: Building and Defending a Long-Lived Rust System](../module-100-architectural-synthesis-building-and-defending-a-long-lived-rust-system/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
