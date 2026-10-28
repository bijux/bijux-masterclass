# Workbook — Module 89: Cargo Profiles, Binary Size, Packaging, CI, and Reproducible Releases

[Chapter](index.md) · [Laboratory](../../labs/module-09-release-matrix-and-artifact-manifest/README.md) · [MetricRail guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Cargo Profiles, Binary Size, Packaging, CI, and Reproducible Releases** has become a usable model rather than remembered vocabulary. Its governing question is: *How is one reviewed source state transformed into a tested, traceable, appropriately optimized artifact that can be installed and reproduced without hidden local assumptions?* Preserve your first prediction and record decisive facts in a **release manifest**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 88 — Security and Supply-Chain Engineering that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **How is one reviewed source state transformed into a tested, traceable, appropriately optimized artifact that can be installed and reproduced without hidden local assumptions?**
3. Draw the smallest **release manifest** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

### 1. Benchmark profile versus shipped profile

Benchmarks use `opt-level=3`, thin LTO, and debug symbols. Production uses a different release profile with full LTO and stripped symbols. What can and cannot be inferred from the benchmark? Design a profile policy that preserves diagnostic usefulness.

### 2. Binary size

A patch reduces the binary by 20% by disabling features and stripping symbols, but startup and incident diagnosis worsen. Identify at least five components of the trade-off beyond file bytes.

### 3. Feature combinations

The crate exposes four independent features. How many combinations exist? Why is “test defaults only” insufficient, and how can the public matrix be reduced deliberately?

### 4. Reproducibility

Two builds from the same Git commit produce different bytes. List possible sources: toolchain, target, paths, timestamps, environment, generated order, linker, dependencies, and metadata. Classify which can be controlled and which require documented limits.

### 5. Lockfile policy

When should a Rust application commit `Cargo.lock`? Why does `--locked` matter in CI/release? What does it still not prove?

### 6. Rollback artifact

A deployment system can rebuild the previous Git tag but does not retain the previous binary/configuration. Is that a reliable rollback? Explain.

## Part 2 — Diagnose and repair

### Case A — Hidden local dependency

A build succeeds on a developer machine because a path dependency exists outside the repository. CI fails. Repair the package boundary and add a clean-environment proof.

### Case B — Nondeterministic generated file

A build script iterates a `HashMap` and embeds current time. Explain why two correct builds differ and repair the source of identity.

### Case C — Over-optimized release

Full LTO and one codegen unit save 4% runtime but triple build time and remove enough symbols that profiles are hard to interpret. Write a decision process rather than choosing one setting universally.

### Case D — Matrix theater

CI runs many targets but never installs/tests the packaged artifact. Identify the missing proof and design one installation/smoke/rollback route.

## Part 3 — Focused exercises

### Exercise 1 — Profile table

Define `dev`, `test`, `profiling`, and `dist` profiles. For each, state optimization, debug info, assertions, overflow behavior, LTO/codegen intent, and allowed use. Avoid copying settings without purpose.

### Exercise 2 — Supported matrix

Declare supported targets, feature sets, toolchain/MSRV, and package formats. Distinguish compile-only, test, integration, and release tiers.

### Exercise 3 — Artifact manifest

Design a deterministic manifest containing product, version, source revision, lockfile digest, toolchain, target, profile, features, artifact digest/size, and compatibility/configuration identity. Sort fields and forbid wall-clock identity unless explicitly supplied.

### Exercise 4 — Clean release route

Write a release sequence from clean checkout to signed/published artifact, including dependency resolution policy, tests, docs, benchmarks/security checks, packaging, install smoke, rollback smoke, and retention.

### Exercise 5 — Artifact equivalence

Define what it means for two release artifacts to be “the same” for your product. Distinguish byte-identical, behaviorally compatible, built from the same source, and installable under the same configuration. List every input that must match for byte comparison, then define the weaker compatibility evidence used across supported targets where byte identity is not expected. Explain which identity appears in rollback records.

### Exercise 6 — Package contents review

Write the exact files that belong in a MetricRail release package: executable, configuration example/schema, licenses, manifest/digest, operations documentation, and optional symbol artifact. For each file, identify its source of truth and compatibility relationship. List files that must never be copied accidentally, such as local secrets, benchmark corpora with sensitive data, target directories, or developer-specific paths.

### Interleaved reasoning pass

1. For **Explain how Cargo profile settings affect optimization, debug information, overflow checks, assertions, code generation, link-time optimization, panic behavior, and strip policy**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the release manifest.
2. For **Separate development, test, benchmark, profiling, release, and distribution artifacts**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the release manifest.
3. For **Measure binary size by section and dependency contribution before applying size flags**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the release manifest.
4. For **Design feature combinations that do not create untested products or additive surprises**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the release manifest.

5. Identify one guarantee from an earlier course that a careless implementation of **Cargo Profiles, Binary Size, Packaging, CI, and Reproducible Releases** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build the [Release Matrix and Artifact Manifest](../../labs/module-09-release-matrix-and-artifact-manifest/README.md). Validate target, profile, and allowed feature set. Reject malformed artifact names and digests. Render one deterministic manifest whose order does not depend on hash iteration. Add tests for unsupported products and invalid identity fields.

### Laboratory acceptance trace

Before opening the reference implementation for **Release Matrix and Artifact Manifest**, record:

- the public behavior that demonstrates **Explain how Cargo profile settings affect optimization, debug information, overflow checks, assertions, code generation, link-time optimization, panic behavior, and strip policy**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Create `profiling` and `dist` profiles with documented purposes. Add deterministic build metadata from explicit environment/source inputs, not the current clock. Generate and verify a release manifest and digest. Build with `--locked`, package configuration and operations documents, install into a clean directory, run smoke/load/health checks, then rehearse rollback to the retained previous artifact.

### Capstone invariant trace

For the Module 89 MetricRail increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

1. Why must the measured profile match the product claim?
2. What trade-offs do LTO, codegen units, stripping, and debug info affect?
3. How does feature count expand the test surface?
4. What inputs determine artifact identity?
5. What does a lockfile guarantee and not guarantee?
6. Why is rebuilding an old tag weaker than retaining its artifact?
7. What proves packaging rather than only compilation?
8. Defend one release setting you would leave less optimized.

### Exercise 6 — Prove artifact identity across a release matrix

Define a release matrix containing target triple, Rust toolchain, Cargo profile, enabled features, lockfile digest, source revision, and build environment identity. For each produced binary, record its digest, size, debug-symbol policy, embedded version output, and associated test report. Then describe how a consumer verifies that the artifact they received is the artifact reviewed. Explain why rebuilding without a committed lockfile establishes dependency resolution for the first time rather than proving reproduction of an earlier release.

### Release acceptance gate

A release is not a directory containing a binary. It is a linked evidence set: immutable source identity, reviewed dependency resolution, exact build inputs, executable test results, artifact digests, compatibility claims, operational documentation, and rollback instructions. A smaller or faster binary is useful only after it remains traceable and compatible with the declared deployment contract.

### Closed-book defense

In five minutes, answer “How is one reviewed source state transformed into a tested, traceable, appropriately optimized artifact that can be installed and reproduced without hidden local assumptions?” using the **release manifest**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside MetricRail. A list of APIs without the deciding relationship is incomplete.
