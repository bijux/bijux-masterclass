# Module 99 Workbook — Long-Lived APIs: SemVer, MSRV, Features, Migrations, and Workspace Stewardship

[Chapter](index.md) · [AxiomStore guide](../capstone.md) · [Solutions](solutions.md)

This workbook turns the chapter’s **compatibility and migration matrix** into evidence. Write predictions before compiling or running anything. Preserve the stated product requirement during repair; a green build obtained by deleting the difficult relationship is not a solution.

## Part 1 — Predict

For each case, submit: expected category (`compile-pass`, `compile-fail`, `run-pass`, `run-fail`, or `manual-review`), first decisive phase or event, governing relationship, and the strongest conclusion the outcome would justify.

Your prediction sheet must make the compatibility and migration matrix visible. For one case, change exactly one assumption and explain why the decisive phase or outcome moves.

### Prediction 1 — Defaulted trait method

A public trait gains a defaulted method. Identify at least three downstream surfaces that may still change.

### Prediction 2 — Nonadditive feature

Feature `fast` disables validation. Predict behavior when one dependency enables `fast` and another expects default validation.

### Prediction 3 — Declared MSRV

The manifest sets `rust-version = 1.97`, but CI runs only stable latest with default features. Is the promise supported?

### Prediction 4 — Writer upgrade

A new release reads AXIOM01 but writes AXIOM02. Can old binaries read newly written files?

## Part 2 — Diagnose and repair

Each repair must leave a more precise compatibility and migration matrix. Reject fixes that merely erase the type, lifetime, state, compatibility, or artifact fact that the exercise is designed to expose.

### Repair 1 — In-place migration

Migration rewrites the only copy before validating the new format.

Required direction: Read old data, transform into a stable model, encode and verify a separate candidate, then replace according to the documented file contract.

Submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the compatibility and migration matrix changes.

### Repair 2 — Deprecation without destination

An API is marked deprecated with only “will be removed.”

Required direction: Name the replacement, semantic differences, adapter or migration, and removal policy.

Submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the compatibility and migration matrix changes.

### Repair 3 — Workspace head as downstream proof

The project treats its own workspace compilation as SemVer validation.

Required direction: Add downstream caller/implementor fixtures, feature matrices, MSRV execution, and old-data fixtures.

Submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the compatibility and migration matrix changes.

## Part 3 — Focused exercises

### Exercise 1 — Audience matrix

Analyze a new enum variant and trait method across callers, implementors, matches, inference, and objects.

Completion standard: Each audience receives a separate compatibility judgment.

### Exercise 2 — Feature redesign

Convert mutually exclusive mode features into additive integrations plus runtime policy.

Completion standard: Feature unification cannot silently disable existing semantics.

### Exercise 3 — Candidate migration

Implement V1-to-V2 migration with source preservation and candidate revalidation.

Completion standard: Malformed source and invalid candidate leave authoritative data unchanged.

### Exercise 4 — Release evidence

Define exact MSRV/feature/data fixtures for a release.

Completion standard: Manifest declarations are backed by executable routes.

### Cross-course transfer

Choose one artifact from Courses 1–9 and reassess it through **Long-Lived APIs: SemVer, MSRV, Features, Migrations, and Workspace Stewardship**. Reconstruct its current invariant owner, then decide whether the compatibility and migration matrix reveals a genuine defect. A justified no-change decision is valid when the advanced mechanism would add proof or compatibility cost without removing a real invalid state.


### Applied case study — shipping AXIOM02 without abandoning AXIOM01

The next AxiomStore release adds a per-record schema tag and a new optional validator integration. Existing AXIOM01 files must remain readable. The crate declares an MSRV and is used both through default features and with `--no-default-features`. Some downstream crates implement a public extension trait and others store `dyn Extension`.

Prepare a compatibility matrix with rows for source callers, downstream implementors, trait-object users, stored AXIOM01 bytes, CLI scripts, MSRV, default features, and feature combinations. For each row, identify the possible break and the evidence required before release. Decide whether schema tags require AXIOM02, an additive side table, or reinterpretation of an existing reserved field; justify the authority and migration consequences.

Then propose a release sequence that keeps migration failure from destroying the source. Include golden fixtures, dual-read behavior, canonical new writes, deprecation policy, feature checks, and artifact identity. Finish by identifying one change that appears additive in Rust source but is semver-risky because it changes inference, coherence, dyn compatibility, or feature unification.

## Part 4 — Independent laboratory

Build [Versioned SDK](../../labs/module-09-versioned-sdk/README.md) from its `starter/` package.

Build a V1/V2 SDK with strict decoders, candidate-first migration, compatibility fixtures, and an explicit policy for old readers, new writers, and unknown versions.

Before implementation, freeze Versioned SDK’s public behavior and the compatibility and migration matrix. After implementation, complete its transfer task in a domain with different ownership, version, capacity, extension, or failure policy; renaming types does not demonstrate transfer.

## Part 5 — Capstone transfer

Specify AXIOM01/AXIOM02 read/write policy, old-data fixtures, migration, unknown-version behavior, CLI schema output, MSRV checks, and rollback before implementing the final extension.

Update AxiomStore’s compatibility and migration matrix before code. Record the changed invariant owner, new failure paths, compatibility effect, and falsifying evidence. Then run the full capstone route because this module can invalidate guarantees outside its local file.

### Evidence quality review

Before leaving the module, select one change that looked source-compatible but threatened a different stakeholder: implementors, feature combinations, MSRV users, stored data, generated code, or operational scripts. Record the fixture or downstream check that exposes the break. Then name one compatibility promise the library deliberately does not make and ensure the documentation does not imply it.

## Part 6 — Reconstruct and defend

Classify a proposed change separately for source callers, implementors, feature unification, minimum toolchain, persistent bytes, and release artifacts.

Finish without notes by reconstructing the compatibility and migration matrix. Name the requirement, the simpler design, the decisive rejected construction, the state after failure, and the evidence that could falsify your claim. End by stating one condition under which this mechanism should be removed.

The defense is complete only when another reader can reproduce the reasoning behind Versioned SDK and the AxiomStore increment without seeing your final implementation.
