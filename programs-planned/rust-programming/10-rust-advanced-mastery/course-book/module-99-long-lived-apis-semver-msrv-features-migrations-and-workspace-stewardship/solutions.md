# Module 99 Solutions — Long-Lived APIs: SemVer, MSRV, Features, Migrations, and Workspace Stewardship

[Workbook](workbook.md) · [Chapter](index.md) · [AxiomStore guide](../capstone.md)

These are reasoned reference answers. Compare your predicted phase, invariant owner, and failure state before comparing syntax. A different implementation is stronger when it preserves the same contract with a smaller proof surface.

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

A strong answer updates the compatibility and migration matrix and includes a negative case that fails for the original cause.

### Repair 2 — Deprecation without destination

**Causal defect.** An API is marked deprecated with only “will be removed.”

**Principled repair.** Name the replacement, semantic differences, adapter or migration, and removal policy.

A strong answer updates the compatibility and migration matrix and includes a negative case that fails for the original cause.

### Repair 3 — Workspace head as downstream proof

**Causal defect.** The project treats its own workspace compilation as SemVer validation.

**Principled repair.** Add downstream caller/implementor fixtures, feature matrices, MSRV execution, and old-data fixtures.

A strong answer updates the compatibility and migration matrix and includes a negative case that fails for the original cause.

## Part 3 — Focused exercises

### Exercise 1 — Audience matrix

The construction should answer: Analyze a new enum variant and trait method across callers, implementors, matches, inference, and objects.

The decisive acceptance criterion is: Each audience receives a separate compatibility judgment.

Evaluate the result through the compatibility and migration matrix; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 2 — Feature redesign

The construction should answer: Convert mutually exclusive mode features into additive integrations plus runtime policy.

The decisive acceptance criterion is: Feature unification cannot silently disable existing semantics.

Evaluate the result through the compatibility and migration matrix; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 3 — Candidate migration

The construction should answer: Implement V1-to-V2 migration with source preservation and candidate revalidation.

The decisive acceptance criterion is: Malformed source and invalid candidate leave authoritative data unchanged.

Evaluate the result through the compatibility and migration matrix; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 4 — Release evidence

The construction should answer: Define exact MSRV/feature/data fixtures for a release.

The decisive acceptance criterion is: Manifest declarations are backed by executable routes.

Evaluate the result through the compatibility and migration matrix; helper names may differ, but the invariant owner and adversarial case must be explicit.

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
