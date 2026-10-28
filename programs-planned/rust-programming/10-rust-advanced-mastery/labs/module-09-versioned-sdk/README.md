# Laboratory 9 — Versioned SDK

[Course 10](../../README.md) · [Common laboratory method](../../../START_HERE.md#laboratory-method)

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

### Completion standard

You can ship a new stored form without reinterpreting old bytes, name every affected audience, and prove that failed migration preserves the source. “It compiles for me” is not a compatibility argument.
