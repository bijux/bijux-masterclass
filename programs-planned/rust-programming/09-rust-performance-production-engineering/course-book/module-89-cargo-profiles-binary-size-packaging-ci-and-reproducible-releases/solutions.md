# Reasoned Solutions — Module 89: Cargo Profiles, Binary Size, Packaging, CI, and Reproducible Releases

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-09-release-matrix-and-artifact-manifest/README.md) · [MetricRail guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 89: Cargo Profiles, Binary Size, Packaging, CI, and Reproducible Releases**. Compare the reasoning against this question: *How is one reviewed source state transformed into a tested, traceable, appropriately optimized artifact that can be installed and reproduced without hidden local assumptions?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Part 1 — Artifact reasoning

### 1. Benchmark profile versus shipped profile

The benchmark characterizes only its profile. LTO, codegen units, symbol settings, panic strategy, target features, and link layout can change both performance and diagnosability. Measure the shipped `dist` artifact for release claims. Keep a `profiling` profile close to `dist` in optimization while retaining sufficient symbols; document differences and confirm that they do not invert the cost structure.

### 2. Binary size

Consider startup/page faults, runtime performance, compile/link time, crash/profile symbolization, package transfer, update storage, attack/dependency surface, feature capability, and supportability. Stripping may reduce bytes but external symbol files can preserve diagnosis. Feature removal is valuable only if behavior remains required-complete.

### 3. Feature combinations

Four independent booleans yield 16 combinations. Default-only tests miss interaction and no-default behavior. Reduce the public matrix by making features additive, forbidding incompatible combinations at compile time, defining a few supported sets, and testing every supported set rather than advertising an unconstrained power set.

### 4. Reproducibility

Pin toolchain and lockfile; declare target/profile/features; make generated order deterministic; avoid current time/randomness/absolute paths; control environment inputs; use stable source revision. Linkers and platform metadata may still limit byte identity across hosts, so state the reproducibility scope. Compare manifests and bytes under the declared environment rather than claiming universal reproducibility.

### 5. Lockfile policy

Applications should commit the lockfile so the complete resolved graph is reviewed and repeatable. `--locked` prevents silent resolution changes. It does not prove source integrity, absence of vulnerabilities, identical native toolchains, identical features, or byte-for-byte builds.

### 6. Rollback artifact

Rebuilding may resolve different dependencies, use a changed toolchain, unavailable build input, or produce a different package. Reliable rollback retains the exact previously accepted artifact, manifest, configuration/schema compatibility, and installation instructions, then rehearses the transition.

## Part 2 — Repairs

### Case A

Move the dependency into the repository/workspace, publish it with a version, or replace the path with an explicit supported source. Build from a clean checkout/container with no undeclared parent files. Audit all path dependencies and package includes. Local success is not release evidence.

### Case B

Use ordered maps/sorting, remove wall-clock input or require an explicit `SOURCE_DATE_EPOCH`-style value, avoid absolute paths, and write generated output deterministically. Generated identity should derive from reviewed inputs. Add a test that runs generation twice and compares bytes.

### Case C

Measure runtime, binary size, build time, and profile quality for candidate settings. If 4% matters to the SLO/cost and build/diagnostic costs are acceptable, retain full optimization for `dist` and a symbol-rich `profiling` sibling. Otherwise choose faster builds or more symbols. Profiles encode different product workflows, not a universal maximum.

### Case D

The matrix proves source compilation/tests, not package correctness. Install the produced archive into a clean destination, verify paths/permissions/configuration, run version/health/smoke tests, exercise upgrade, and install the retained previous artifact for rollback. Test the thing operators receive.

## Part 3 — Model answers

### Exercise 1

`dev` prioritizes fast edit/compile and rich debug information. `test` keeps deterministic assertions and enough optimization only if test realism needs it. `profiling` approximates production optimization while retaining symbols and avoids stripping. `dist` is the measured shipped profile with deliberate LTO/codegen/panic/strip choices. Overflow/assertion behavior must not create semantic differences that invalidate tests; critical checked arithmetic remains explicit in all profiles.

### Exercise 2

Publish only combinations you can support. A common route tests the host target fully, cross-checks additional targets, runs each supported feature set, and creates release artifacts only for a smaller signed matrix. The MSRV/toolchain and target libc/ABI assumptions are part of compatibility. Unsupported combinations should fail clearly rather than accidentally compile.

### Exercise 3

Use a canonical key order and normalized values. The manifest binds the binary to source revision, lockfile, toolchain, target, profile, features, config/schema version, digest, and size. Wall-clock build time can be metadata supplied externally but should not define the artifact if byte reproducibility is required.

### Exercise 4

A strong sequence is: clean checkout; verify toolchain and lockfile; run format/lint/tests/docs; run targeted benchmarks and security/dependency checks; build `--locked --profile dist`; produce manifest/digest/SBOM or dependency inventory; package licenses/config/docs; install in clean environment; run smoke and compatibility checks; rehearse upgrade/rollback; sign/publish; retain previous artifacts and evidence.

## Part 4 — Laboratory review

`Matrix::validate` should reject unsupported target/profile/feature set. Artifact names must not contain path separators. Digests must have exact allowed form. `BTreeSet` and explicit field order make rendering deterministic. The manifest describes an artifact; it does not calculate cryptographic trust by itself.

## Part 5 — MetricRail transfer

Build metadata should be supplied by the release environment and embedded deterministically. `build.rs` may expose target/profile/source revision, but not silently insert current time. The release script generates/uses the lockfile, builds locked, emits a sorted manifest, and verifies digest. Installation and rollback are tested from produced artifacts, not source trees.

## Part 6 — Defense

Profile differences can change performance. LTO/codegen units trade runtime, size, build time, and profile quality; stripping/debug info trade package size and diagnosis. Features multiply supported behavior. Artifact identity includes source, dependency graph, toolchain, target, profile, features, generation inputs, and binary digest. A lockfile fixes resolution, not security or toolchain. Retained artifacts make rollback exact. Package proof requires clean install and execution. Leaving symbols or faster codegen is rational when operational diagnosis/build feedback outweighs a small runtime gain.

## Deep reasoning and transfer

### Decisive model

> How is one reviewed source state transformed into a tested, traceable, appropriately optimized artifact that can be installed and reproduced without hidden local assumptions?

Build a **release manifest**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Explain how Cargo profile settings affect optimization, debug information, overflow checks, assertions, code generation, link-time optimization, panic behavior, and strip policy.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Separate development, test, benchmark, profiling, release, and distribution artifacts.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Measure binary size by section and dependency contribution before applying size flags.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Design feature combinations that do not create untested products or additive surprises.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Build a CI matrix from supported targets, features, MSRV, and risk rather than every theoretical combination.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Explain how Cargo profile settings affect optimization, debug information, overflow checks, assertions, code generation, link-time optimization, panic behavior, and strip policy.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the release manifest.

### Reference implementation comparison

For [Release Matrix and Artifact Manifest](../../labs/module-09-release-matrix-and-artifact-manifest/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In MetricRail, Module 89 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Cargo Profiles, Binary Size, Packaging, CI, and Reproducible Releases**, which relationship decides this question: “How is one reviewed source state transformed into a tested, traceable, appropriately optimized artifact that can be installed and reproduced without hidden local assumptions?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to MetricRail?
