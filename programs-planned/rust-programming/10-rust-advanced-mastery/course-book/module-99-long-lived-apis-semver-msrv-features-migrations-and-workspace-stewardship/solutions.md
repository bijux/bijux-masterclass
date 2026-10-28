# Reasoned Solutions — Module 99: Long-Lived APIs: SemVer, MSRV, Features, Migrations, and Workspace Stewardship

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-09-versioned-sdk/README.md) · [AxiomStore guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 99: Long-Lived APIs: SemVer, MSRV, Features, Migrations, and Workspace Stewardship**. Compare the reasoning against this question: *How do you evolve a Rust library, data format, feature graph, and workspace without silently breaking downstream source, behavior, tools, or stored data?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Part 1 — Prediction

### Prediction 1 — Defaulted trait method

Third-party implementors, object/dyn compatibility, blanket impl interactions, method-name collisions, and inference may be affected even when existing callers compile.

### Prediction 2 — Nonadditive feature

Cargo feature unification can enable `fast` globally, silently changing semantics. Features should add capabilities; runtime policy should choose mutually exclusive behavior.

### Prediction 3 — Declared MSRV

No. The minimum toolchain and supported feature combinations must actually compile and test.

### Prediction 4 — Writer upgrade

Not unless explicitly designed. The matrix must distinguish backward reader compatibility from forward compatibility and publish the writer transition.

## Part 2 — Diagnose and repair

Judge every repair against the compatibility and migration matrix: the decisive relationship must become clearer, not disappear behind cloning, erasure, broad bounds, visibility, unchecked construction, or deleted validation.

### Repair 1 — In-place migration

**Causal defect.** Migration rewrites the only copy before validating the new format.

**Principled repair.** Read old data, transform into a stable model, encode and verify a separate candidate, then replace according to the documented file contract.

The negative case should reintroduce **In-place migration** while preserving the surrounding requirement. The compatibility and migration matrix must identify the first phase at which the original assumption becomes invalid.

### Repair 2 — Deprecation without destination

**Causal defect.** An API is marked deprecated with only “will be removed.”

**Principled repair.** Name the replacement, semantic differences, adapter or migration, and removal policy.

The negative case should reintroduce **Deprecation without destination** while preserving the surrounding requirement. The compatibility and migration matrix must identify the first phase at which the original assumption becomes invalid.

### Repair 3 — Workspace head as downstream proof

**Causal defect.** The project treats its own workspace compilation as SemVer validation.

**Principled repair.** Add downstream caller/implementor fixtures, feature matrices, MSRV execution, and old-data fixtures.

The negative case should reintroduce **Workspace head as downstream proof** while preserving the surrounding requirement. The compatibility and migration matrix must identify the first phase at which the original assumption becomes invalid.

## Part 3 — Focused exercises

### Exercise 1 — Audience matrix

The construction should answer: Analyze a new enum variant and trait method across callers, implementors, matches, inference, and objects.

The decisive acceptance criterion is: Each audience receives a separate compatibility judgment.

For **Audience matrix**, apply the compatibility and migration matrix to the exact construction above and to its closest simpler alternative. The answer is complete only when the stated acceptance criterion survives a counterexample aimed at that design choice.

### Exercise 2 — Feature redesign

The construction should answer: Convert mutually exclusive mode features into additive integrations plus runtime policy.

The decisive acceptance criterion is: Feature unification cannot silently disable existing semantics.

For **Feature redesign**, apply the compatibility and migration matrix to the exact construction above and to its closest simpler alternative. The answer is complete only when the stated acceptance criterion survives a counterexample aimed at that design choice.

### Exercise 3 — Candidate migration

The construction should answer: Implement V1-to-V2 migration with source preservation and candidate revalidation.

The decisive acceptance criterion is: Malformed source and invalid candidate leave authoritative data unchanged.

For **Candidate migration**, apply the compatibility and migration matrix to the exact construction above and to its closest simpler alternative. The answer is complete only when the stated acceptance criterion survives a counterexample aimed at that design choice.

### Exercise 4 — Release evidence

The construction should answer: Define exact MSRV/feature/data fixtures for a release.

The decisive acceptance criterion is: Manifest declarations are backed by executable routes.

For **Release evidence**, apply the compatibility and migration matrix to the exact construction above and to its closest simpler alternative. The answer is complete only when the stated acceptance criterion survives a counterexample aimed at that design choice.

### Cross-course transfer

Full credit may conclude that **Long-Lived APIs: SemVer, MSRV, Features, Migrations, and Workspace Stewardship** should not be retrofitted into the earlier artifact. The comparison must identify the current owner, the proof benefit, maintenance cost, and a concrete failure that would change.

### Applied case study — shipping AXIOM02 without abandoning AXIOM01

The compatibility matrix separates audiences. Ordinary callers may break through renamed items, changed inference, or altered defaults. Implementors break when a required trait method is added or a blanket implementation creates overlap. Trait-object users break if the trait loses dyn compatibility. Stored files break if existing bytes are reinterpreted. Scripts break through output or exit-code changes. MSRV breaks when new syntax or library APIs enter the supported build. Feature users break when optional dependencies become mandatory or feature combinations change semantics.

A schema tag changes record meaning and should not be smuggled into an old field unless AXIOM01 explicitly reserved that field with defined forward semantics. The clearer design is AXIOM02 with dual readers: read AXIOM01 and AXIOM02, write only canonical AXIOM02 after explicit migration or creation, and preserve the source until the complete candidate verifies and replaces it successfully.

The release route checks immutable AXIOM01 fixtures, migration failures, AXIOM02 canonical vectors, no-default builds, each supported feature set, all-features, and the declared MSRV. Deprecations name the replacement and remain for the documented window. Artifacts embed or report source revision, version, features, target, and lockfile identity.

An apparently additive blanket implementation is semver-risky because it can overlap a downstream implementation that was previously legal. Adding a generic defaulted parameter can also change inference. Adding a default trait method can break dyn compatibility if its signature is not object-safe. “Additive” must therefore be evaluated through callers, implementors, objects, features, stored data, and artifacts rather than item count.

## Part 4 — Independent laboratory

A complete [Versioned SDK](../../labs/module-09-versioned-sdk/README.md) satisfies its public contract and makes the compatibility and migration matrix inspectable. The reference implementation is not canonical; compare accepted input, rejected input, state after failure, ownership/lifetime surface, deterministic behavior, and extension authority in that order.

Build a V1/V2 SDK with strict decoders, candidate-first migration, compatibility fixtures, and an explicit policy for old readers, new writers, and unknown versions.

The transfer variant for Versioned SDK must alter at least two substantive dimensions and preserve an independent oracle; a domain-name substitution is not evidence of mastery.

## Part 5 — Capstone transfer

Specify AXIOM01/AXIOM02 read/write policy, old-data fixtures, migration, unknown-version behavior, CLI schema output, MSRV checks, and rollback before implementing the final extension.

A strong capstone change keeps the responsibility described by the compatibility and migration matrix local. Reject any design that spreads the mechanism across unrelated AxiomStore modules without a named requirement.

## Part 6 — Reconstruct and defend

Classify a proposed change separately for source callers, implementors, feature unification, minimum toolchain, persistent bytes, and release artifacts.

The defense passes when it reconstructs the compatibility and migration matrix from the requirement, shows a causal rejected construction, compares a simpler alternative, maps evidence, and names residual risk. Terminology without that chain is not mastery.

## Deep reasoning and transfer

### Decisive model

> How do you evolve a Rust library, data format, feature graph, and workspace without silently breaking downstream source, behavior, tools, or stored data?

Build a **compatibility and migration matrix**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Analyze a proposed change from the perspectives of downstream callers, downstream implementors, type inference, pattern matching, and stored data.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Define and test an MSRV policy without confusing the manifest declaration with actual verification.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Design additive Cargo features that do not change unrelated semantics or create unsupported combinations.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Version persistent formats and implement deterministic, failure-atomic migrations with preserved fixtures.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Use deprecation, adapters, extension traits, sealed traits, and non-exhaustive models according to extension ownership.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Analyze a proposed change from the perspectives of downstream callers, downstream implementors, type inference, pattern matching, and stored data.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the compatibility and migration matrix.

### Reference implementation comparison

For [Versioned SDK](../../labs/module-09-versioned-sdk/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In AxiomStore, Module 99 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Long-Lived APIs: SemVer, MSRV, Features, Migrations, and Workspace Stewardship**, which relationship decides this question: “How do you evolve a Rust library, data format, feature graph, and workspace without silently breaking downstream source, behavior, tools, or stored data?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to AxiomStore?
