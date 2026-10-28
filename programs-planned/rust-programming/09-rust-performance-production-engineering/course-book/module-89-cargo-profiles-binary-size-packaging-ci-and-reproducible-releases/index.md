# Module 89 — Cargo Profiles, Binary Size, Packaging, CI, and Reproducible Releases

**Course 9 · Day 9 · Module 89 of 100**
`██████████████████████░░░` **89/100**

[Program](../../../README.md) · [Course 9](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-09-release-matrix-and-artifact-manifest/README.md) · [MetricRail guide](../capstone.md)

[← Module 88: Security and Supply-Chain Engineering](../module-88-security-and-supply-chain-engineering/index.md) · [Module 90: Production Readiness, Capacity Planning, Rollouts, and Incident Learning →](../module-90-production-readiness-capacity-planning-rollouts-and-incident-learning/index.md)

## The question

> How is one reviewed source state transformed into a tested, traceable, appropriately optimized artifact that can be installed and reproduced without hidden local assumptions?

## Why this comes now

A reviewed source tree is not the artifact that runs. Compiler version, target, Cargo profile, features, dependencies, linker settings, generated inputs, and packaging steps all influence the delivered product. Module 89 makes that transformation explicit and reproducible to the strength the project actually claims.

Release engineering also closes a common measurement error: profiling one artifact and shipping another without comparison. Production profiles are product variants with different optimization, symbols, size, build time, and diagnostic properties.

### Prerequisite bridge

Module 88 established **Security and Supply-Chain Engineering**. Before continuing, verify that you can create security tests for traversal, injection, resource exhaustion, confused-deputy behavior, and unsafe defaults. This module preserves that capability and adds the ability to explain how cargo profile settings affect optimization, debug information, overflow checks, assertions, code generation, link-time optimization, panic behavior, and strip policy. Module 90, **Production Readiness, Capacity Planning, Rollouts, and Incident Learning**, will rely on both when it asks: *What evidence is sufficient to put this system under real load, how is risk limited during rollout, and how does operational evidence change the next design?*

### Scope boundary

This module owns the reasoning for **cargo profiles, binary size, packaging, ci, and reproducible releases** inside Course 9. The course teaches measurement and operational reasoning, not folklore optimization. It does not promise universal performance rankings, complete security proof, or production readiness from one green pipeline. Every conclusion is scoped to a workload, artifact, environment, and time. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

After completing this module, you will be able to:

- explain how Cargo profile settings affect optimization, debug information, overflow checks, assertions, code generation, link-time optimization, panic behavior, and strip policy
- separate development, test, benchmark, profiling, release, and distribution artifacts
- measure binary size by section and dependency contribution before applying size flags
- design feature combinations that do not create untested products or additive surprises
- build a CI matrix from supported targets, features, MSRV, and risk rather than every theoretical combination
- produce deterministic release metadata and cryptographic manifests without embedding wall-clock noise
- write installation, upgrade, rollback, configuration, and compatibility instructions that match the artifact

## Core model

### The governing model

A release is a transformation record: `source revision + lockfile + toolchain + target + profile + features + build environment → artifacts + tests + manifest + provenance`. Reproducibility means the relevant inputs and nondeterminism are controlled or documented. It does not mean that copying a binary between arbitrary platforms is valid. Packaging is where source assumptions become operator obligations.

### 1. Profiles encode product trade-offs

Cargo profiles control optimization level, debug information, debug assertions, overflow checks, code generation units, link-time optimization, panic strategy, incremental compilation, and stripping. These settings interact. `opt-level = 3` is not automatically best for every workload, and `panic = abort` changes unwinding and diagnostic behavior. Measure the artifact you ship.


### 2. Profiling versus distribution artifacts

A profiling build often needs optimization plus symbols. A distribution build may strip symbols or separate them. Benchmarks must use a representative optimization profile. Tests often use different assertions and overflow behavior. Name these artifacts explicitly so a benchmark result cannot be mistaken for the shipped binary.


### 3. Binary-size investigation

File size is a symptom. Inspect sections, symbols, duplicated generic instantiations, features, panic machinery, debug data, and native libraries. Link-time optimization, fewer codegen units, `opt-level = z`, stripping, or abort-on-panic can reduce size but affect build time, runtime speed, diagnostics, or semantics.


### 4. Features are product variants

Cargo features are additive within one build graph. Optional dependencies and `cfg` branches can create combinations that compile differently. Keep features small, document valid combinations, and test the supported matrix. Do not use features for runtime secrets or mutually exclusive configuration without explicit compile checks.


### 5. CI as evidence selection

A CI matrix balances coverage and cost. Include the minimum supported Rust version if promised, current pinned toolchain, primary targets, supported feature sets, formatting, Clippy, tests, docs, security policy, and packaging smoke tests. Run expensive benchmarks or cross-platform tests at appropriate cadence; do not pretend a skipped dimension is covered.


### 6. Release manifests and provenance

A release manifest should contain artifact name, target, digest, size, source revision, lockfile digest, toolchain, profile, features, and compatibility version. Avoid timestamps inside binaries when byte reproducibility is required. Signatures and attestations strengthen provenance but do not replace review, isolation, or secret protection.

Artifact identity is a tuple, not a filename. A useful release record binds source revision, dependency resolution, toolchain, target, profile, features, configuration schema, and artifact digest. Rebuildability, behavioral equivalence, and byte-for-byte reproducibility are different claims and require different evidence.

### A module-specific decision table

| Release concern | Required record | Verification |
|---|---|---|
| source identity | revision and dirty state | clean checkout or declared patch set |
| dependency identity | lockfile digest and feature graph | locked resolution and review |
| compiler identity | toolchain and target | pinned toolchain file and build log |
| product variant | profile and features | explicit invocation and matrix |
| artifact identity | size and cryptographic digest | manifest generated after build |
| compatibility | protocol/config/storage versions | install, upgrade, downgrade, rollback tests |
| diagnosability | symbol and metadata policy | profile/crash inspection exercise |

### Working procedure

1. Define profiling and distribution artifacts separately and state why each exists.
2. Pin source, dependency, toolchain, target, profile, and feature inputs.
3. Build with a locked dependency graph and deterministic generated inputs.
4. Run the test matrix appropriate to the exact variant being packaged.
5. Create an artifact manifest containing identity, size, digest, and compatibility metadata.
6. Install and smoke-test the packaged artifact on a clean environment.
7. Rehearse upgrade and rollback, then state whether the release is merely rebuildable, behaviorally equivalent, or byte-identical.

### Failure patterns and principled repairs

#### Benchmarking one profile and shipping another without measuring both.

A profile result belongs to that artifact. Measure the distribution profile before assuming its code shape and cost match.

#### Setting maximum optimization and LTO everywhere without measuring runtime, size, build time, or debuggability.

Maximum optimization can increase build time, size, or diagnostic difficulty without helping the workload. Tune profiles from explicit trade-offs.

#### Stripping all symbols and discovering during an incident that profiles and crash addresses cannot be interpreted.

Removing all symbols can make production profiles and crash addresses unusable. Keep a deliberate symbol and artifact-retention policy.

#### Publishing many feature combinations while testing only defaults.

Features create product variants. Test the supported combinations and reject unsupported matrices explicitly.

#### Embedding current time, random identifiers, or absolute paths into generated artifacts.

Wall clocks, random IDs, absolute paths, and unordered generation can alter artifacts. Remove or normalize them before claiming reproducibility.

#### Calling a build reproducible because it succeeds twice on one laptop without comparing bytes or documenting environmental inputs.

Two successful builds on one host prove little. Record inputs, compare manifests, and define the exact reproducibility strength being claimed.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For explain how Cargo profile settings affect optimization, debug information, overflow checks, assertions, code generation, link-time optimization, panic behavior, and strip policy, construct one positive and one causal negative example. Mark the first decisive fact in the **release manifest** and state which evidence could falsify the claim.

2. **Outcome 2.** For separate development, test, benchmark, profiling, release, and distribution artifacts, construct one positive and one causal negative example. Mark the first decisive fact in the **release manifest** and state which evidence could falsify the claim.

3. **Outcome 3.** For measure binary size by section and dependency contribution before applying size flags, construct one positive and one causal negative example. Mark the first decisive fact in the **release manifest** and state which evidence could falsify the claim.

4. **Outcome 4.** For design feature combinations that do not create untested products or additive surprises, construct one positive and one causal negative example. Mark the first decisive fact in the **release manifest** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

```rust
use std::collections::BTreeMap;

fn manifest(fields: BTreeMap<&str, String>) -> String {
    fields
        .into_iter()
        .map(|(key, value)| format!("{key}={value}
"))
        .collect()
}

fn main() {
    let fields = BTreeMap::from([
        ("artifact", "metricrail".to_owned()),
        ("profile", "dist".to_owned()),
        ("target", std::env::consts::ARCH.to_owned()),
    ]);
    let output = manifest(fields);
    assert!(output.starts_with("artifact=metricrail
"));
}
```

Read the example manifest as a chain of custody. Ask which value identifies source, which identifies dependencies, which identifies code generation, and which identifies the final bytes. A missing field is not merely documentation debt; it can prevent rollback or make incident evidence ambiguous.

Then build the same source under profiling and distribution profiles. Compare size, symbols, startup, and representative workload results. The exercise teaches why “release build” is not one universal product.

### MetricRail consequence

MetricRail defines `profiling` and `dist` profiles separately. The profiling artifact keeps enough debug information for attribution; the distribution artifact uses thin LTO, one codegen unit, and symbol stripping. Neither profile is declared superior without measurement.

`metricrail version` reports package version, source revision supplied by the build environment, target, profile, and pinned toolchain without a wall-clock timestamp. The release script builds with `--locked`, computes a SHA-256 digest and size, and emits a sorted manifest.

The supplied release script can bootstrap a lockfile when the exercise begins without one, then immediately switches to locked mode. That first resolution is not yet a reproducible release: inspect the resolved graph, review it, and commit the lockfile before treating later artifacts as controlled products. The course distinguishes dependency bootstrap from the stronger claim that the same reviewed dependency graph was used for testing and packaging.

### Release matrix example: reduce combinations without hiding variants

MetricRail has two profiles, two supported targets, and a hypothetical optional JSON diagnostic feature. The mathematical matrix has eight combinations, but not every combination needs the same frequency. Every change can check the default target under `profiling` and `dist`, run tests with and without the feature, and build the secondary target. A scheduled job can execute the full cross-product, benchmark the distribution variants, and compare package manifests.

The matrix must still declare all eight combinations as supported or unsupported. “Not tested on every change” is different from “unknown product.” If JSON diagnostics alter dependencies or cardinality risk, the feature-enabled distribution artifact needs its own security and size evidence. If the secondary target lacks a required system capability, fail configuration early rather than letting users discover the gap during deployment.

Record the exact command and artifact digest for every release candidate. A later smoke test must consume the packaged bytes, not rebuild from source. This prevents a green installation test from proving only that the repository can produce some artifact rather than that the reviewed artifact can be installed.

### Boundary case: two deterministic builds with different meaning

Two artifacts can be byte-for-byte identical and still be the wrong release if both were built from an unreviewed revision or unsupported feature set. Conversely, two artifacts may differ in debug paths or platform metadata while behaving equivalently under the declared compatibility tests. Reproducibility strength must be named rather than implied.

Consider a profiling build and a distribution build from the same revision. The profiling artifact retains line tables and symbols; the distribution artifact strips symbols and enables thin LTO. Their digests and perhaps code layout differ intentionally. The benchmark report must identify which artifact it measured, and the release decision must include a confirmation on the distribution artifact.

A strong pipeline treats the artifact manifest as part of the product. It verifies the source revision, lockfile, toolchain, target, profile, features, size, and digest after packaging. Installation and rollback tests consume that packaged artifact rather than rebuilding from source, because rebuilding would create a different object and weaken chain-of-custody evidence.

## Practice sequence

1. Compare MetricRail’s profiling and distribution profiles against a stated workload and diagnostic need.
2. Complete the Release Matrix and Artifact Manifest lab.
3. Define supported feature and target combinations and map each to CI evidence.
4. Generate a release manifest and verify its digest after copying the artifact.
5. Test clean installation, version output, smoke behavior, and rollback.
6. State the exact reproducibility strength reached and list the remaining uncontrolled inputs.

Use the [workbook](workbook.md) to freeze predictions and complete the causal repairs. Build the module laboratory before reading its reference implementation, then transfer the mechanism into the [MetricRail engineering guide](../capstone.md).

## Ready to continue

Continue only when you can:

- identify an artifact by source, lockfile, toolchain, target, profile, features, and digest;
- explain why profiling and distribution profiles may intentionally differ;
- design a finite supported feature matrix;
- separate rebuildable, behaviorally equivalent, and byte-identical claims;
- construct CI evidence for the exact artifact variant;
- describe MetricRail’s lockfile bootstrap limitation without overstating reproducibility.

## Primary Rust references

- Cargo documentation for profiles, features, lockfiles, package metadata, and build scripts
- The Rust Reference for conditional compilation and panic behavior
- Target-platform packaging and code-signing documentation for supported release systems

These references are for verification and deeper lookup after the chapter’s model is understood. The course-book chapter remains the complete learning route for the required concepts.

## Continue

Continue to [Module 90 — Production Readiness, Capacity Planning, Rollouts, and Incident Learning](../module-90-production-readiness-capacity-planning-rollouts-and-incident-learning/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
