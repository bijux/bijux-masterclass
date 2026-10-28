# Laboratory 9 — Release Matrix and Artifact Manifest

[Common laboratory method](../../../START_HERE.md#laboratory-method) · [Module 89 chapter](../../course-book/module-89-cargo-profiles-binary-size-packaging-ci-and-reproducible-releases/index.md)

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

