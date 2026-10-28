# Laboratory 89 — Release Matrix and Artifact Manifest

**Course 9 · Module 89: Cargo Profiles, Binary Size, Packaging, CI, and Reproducible Releases**

[Chapter](../../course-book/module-89-cargo-profiles-binary-size-packaging-ci-and-reproducible-releases/index.md) · [Workbook](../../course-book/module-89-cargo-profiles-binary-size-packaging-ci-and-reproducible-releases/workbook.md) · [MetricRail guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Cargo Profiles, Binary Size, Packaging, CI, and Reproducible Releases**: How is one reviewed source state transformed into a tested, traceable, appropriately optimized artifact that can be installed and reproduced without hidden local assumptions? The product must make **Explain how Cargo profile settings affect optimization, debug information, overflow checks, assertions, code generation, link-time optimization, panic behavior, and strip policy** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **release manifest** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Product

Build a release planner that accepts only supported target/profile/feature combinations and renders one deterministic artifact manifest. The manifest binds a binary to the reviewed inputs that produced it; it is not a substitute for signatures or a build system.

`Matrix` declares supported targets, profiles, and complete allowed feature sets. `Product` describes one requested combination. `Artifact` adds name, version, source revision, lockfile digest, toolchain, size, and artifact digest. `render_manifest` first validates the product and identity fields, then emits a stable text representation.

## Matrix semantics

Feature support is set-based, not “any subset happens to compile.” If only default and `tls,metrics` are supported, `tls` alone is unsupported even if Cargo accepts it. This keeps the public release matrix smaller than the power set.

Validation must distinguish unsupported target, profile, and feature set. Empty matrices or duplicate entries should be treated according to the declared construction contract, not ignored.

## Artifact identity

Reject artifact names that are empty or contain path separators. Require canonical digest form: exact hexadecimal length and character set under the laboratory’s policy. The manifest should include:

- artifact name and semantic version;
- source revision;
- lockfile digest;
- toolchain;
- target;
- profile;
- sorted feature set;
- artifact size;
- artifact digest.

Do not embed current wall-clock time or unordered map iteration into the canonical identity.

## Construction route

1. Define explicit `ReleaseError` variants for unsupported and malformed states.
2. Implement exact set membership for the product matrix.
3. Validate name/version/revision/digest fields before rendering.
4. Use ordered collections or explicit field order.
5. Render features canonically.
6. Add tests comparing exact output bytes across repeated calls.
7. Add negative tests for every unsupported dimension and malformed digest.

## Release thought experiment

Create a matrix with two targets, two profiles, and three feature sets. Enumerate which combinations are supported and why. Design a CI tier for every supported combination, then a smaller artifact-publishing tier. Explain why compiling an unsupported combination locally does not make it a supported product.

## Adversarial cases

Test empty artifact name, `../name`, backslash path, uppercase/nonhex/wrong-length digest, unsupported target/profile/features, feature order changes, zero-byte artifact, and repeated rendering. Decide whether zero-byte artifacts are forbidden by this product and encode the decision.

## Transfer

Add configuration schema version and dependency/SBOM digest to the manifest. Then design a verifier that compares a running binary’s embedded build information with its external manifest without trusting filenames.

## Completion

The laboratory is complete when the matrix is an explicit support contract, manifest rendering is deterministic, malformed identity is rejected causally, and tests prove repeated byte equality.

Use `solution/` after implementing your own canonical format. Compare which inputs define identity and which combinations are supported. Field order can differ if it is stable and documented.

## Release evidence package

Generate artifacts for at least two profiles or targets and produce a machine-readable manifest containing source revision, Rust toolchain, target triple, Cargo profile, enabled features, lockfile digest, artifact path, artifact digest, byte size, and build timestamp policy. Verify that all paths in the manifest exist and that changing one artifact makes verification fail.

Perform a clean-room-style rebuild from a fresh source copy using the committed lockfile and locked dependency resolution. Compare artifact identity where the environment supports deterministic output; otherwise document the exact non-reproducible fields and still verify behavioral equivalence and provenance. Test version output, migration or compatibility assumptions, packaging layout, and rollback instructions. A release is rejected if the artifact cannot be tied back to the reviewed source and dependency graph.

## Negative release tests

Corrupt one manifest digest, omit one artifact, change the lockfile after building, and run the verifier against a binary whose embedded version does not match the release record. Each case must fail with a causal message. Then rehearse rollback using only the release package and runbook. The exercise is complete when a second reader can identify, verify, deploy, and roll back the intended artifact without relying on undocumented state from the construction machine.

## Completion question

Could a release operator prove the exact binary’s source, dependencies, profile, target, and review evidence after the build machine has disappeared? Demonstrate the lookup using only the package. Any answer that requires shell history, an uncommitted lockfile, or a mutable “latest” tag fails the exercise.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Release Matrix and Artifact Manifest**.
2. Draw the smallest **release manifest** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to MetricRail so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Explain how Cargo profile settings affect optimization, debug information, overflow checks, assertions, code generation, link-time optimization, panic behavior, and strip policy.
- Separate development, test, benchmark, profiling, release, and distribution artifacts.
- Measure binary size by section and dependency contribution before applying size flags.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 89 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **release manifest**. Defend why your design is simpler than one plausible alternative under the new requirements.
