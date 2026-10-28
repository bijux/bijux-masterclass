# Laboratory 99 — Versioned SDK

**Course 10 · Module 99: Long-Lived APIs: SemVer, MSRV, Features, Migrations, and Workspace Stewardship**

[Chapter](../../course-book/module-99-long-lived-apis-semver-msrv-features-migrations-and-workspace-stewardship/index.md) · [Workbook](../../course-book/module-99-long-lived-apis-semver-msrv-features-migrations-and-workspace-stewardship/workbook.md) · [AxiomStore guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Long-Lived APIs: SemVer, MSRV, Features, Migrations, and Workspace Stewardship**: How do you evolve a Rust library, data format, feature graph, and workspace without silently breaking downstream source, behavior, tools, or stored data? The product must make **Analyze a proposed change from the perspectives of downstream callers, downstream implementors, type inference, pattern matching, and stored data** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **compatibility and migration matrix** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Product

Build a small public configuration crate that can read a V1 stored form, write a canonical V2 form, and migrate without destroying the source on validation failure. Treat source callers, downstream implementors, feature combinations, MSRV, stored bytes, and release artifacts as different compatibility audiences.

The starter defines V1 and V2 domain types. Add strict decoders, canonical encoding, an explicit migration, golden fixtures, and a compatibility note suitable for a release review.

### Stored format contract

Define exact line order, accepted Boolean spelling, duplicate-field behavior, trailing-data behavior, and newline policy. V1 fixtures are immutable historical evidence. V2 encoding must be deterministic. Migration performs:

```text
read old
    -> decode old
    -> construct candidate
    -> encode candidate
    -> decode and verify candidate
    -> return or install candidate
```

The library-level lab may return candidate bytes rather than touch the filesystem, but the README must state which outer layer owns atomic replacement.

### Public API and features

Declare `rust-version` and edition in Cargo metadata. Add one optional, additive integration feature whose disabled state leaves baseline semantics unchanged. Define supported checks for no-default, default, and all-features builds. Do not use a feature to silently reinterpret existing fields.

Review one public trait as though downstream crates implement it and store trait objects. Explain why adding a required method, a blanket implementation, or a non-dyn-compatible default method may be breaking even when no existing item is removed.

### Migration failures

Test malformed headers, missing fields, duplicate fields, invalid Boolean text, trailing lines, empty paths, and a candidate that fails V2 validation. The original V1 input must remain available to the caller after every failure.

### Transfer

Design V3 as an additive optional integration. Produce a matrix covering callers, implementors, object users, stored V1/V2 forms, features, MSRV, and artifact identity. Decide whether V3 requires a new stored version or only a new runtime capability.

### Using the reference

Inspect `solution/` after your strict parser and fixtures pass. The reference is a minimal migration sketch; your final lab should be more explicit about duplicate fields, canonical newlines, and feature checks. Compare compatibility obligations rather than line count.

### Mechanism-specific completion standard

You can ship a new stored form without reinterpreting old bytes, name every affected audience, and prove that failed migration preserves the source. “It compiles for me” is not a compatibility argument.

## Design record

Before implementation, complete this record for **Versioned SDK**:

| Question | Required answer |
|---|---|
| Module decision | How does **Long-Lived APIs: SemVer, MSRV, Features, Migrations, and Workspace Stewardship** answer its governing question in this product? |
| Authority | Which type or component decides the main rule? |
| Valid states | Which states may be observed through the public API? |
| Rejection | What exact input or transition is refused, and what remains unchanged? |
| Ownership | Who owns every resource before, during, and after the decisive operation? |
| Order and bounds | Which sequence, capacity, lifetime, or compatibility limit is promised? |
| Evidence | Which test, compiler case, model, trace, or review could falsify the claim? |

Use the **compatibility and migration matrix** to answer the table. Then add at least three adversarial cases: one at the smallest boundary, one at the largest accepted or rejected boundary, and one that leaves partial work before failure. For each, state the final observable state before running the test.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Versioned SDK**.
2. Draw the smallest **compatibility and migration matrix** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to AxiomStore so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Whole-laboratory completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Analyze a proposed change from the perspectives of downstream callers, downstream implementors, type inference, pattern matching, and stored data.
- Define and test an MSRV policy without confusing the manifest declaration with actual verification.
- Design additive Cargo features that do not change unrelated semantics or create unsupported combinations.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 99 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **compatibility and migration matrix**. Defend why your design is simpler than one plausible alternative under the new requirements.
