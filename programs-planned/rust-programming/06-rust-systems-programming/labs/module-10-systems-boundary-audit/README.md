# Laboratory 60 — Systems Boundary Audit

This is the independent product for **Course 6, Module 60: Integrated Systems Design, Testing, and Audit**. Read the [module chapter](../../course-book/module-60-integrated-systems-design-and-audit/index.md) and complete its [workbook](../../course-book/module-60-integrated-systems-design-and-audit/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> How do you prove a systems product across binary formats, files, paths, processes, unsafe code, allocation, and FFI without letting one boundary invalidate another?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Build a compact packet inspector that integrates a checked binary format, transactional file output, and a stateless C validator. Then produce a boundary map and safety dossier that another engineer can review without reading implementation folklore.

## Why this laboratory exists

This lab is an independent final examination of boundary reasoning. The packet product is deliberately small enough to audit end to end yet crosses bytes, storage, and C. The objective is to produce a reviewable invariant register and compatibility statement, not to add the largest number of systems features.

## Contract

Packets begin with `PKT1`, a little-endian sequence number, a little-endian `u16` payload length, payload bytes, and FNV-1a checksum. The inspector rejects truncation, oversized payloads, checksum mismatch, and trailing bytes. `write_packet_atomic` uses same-directory staging. `packet_validate` exposes a pointer-plus-length C boundary with a structured report.

## Required milestones

1. Implement the safe parser and canonical encoder first.
2. Add atomic file replacement without mixing it into parsing.
3. Add a minimal audited FFI validator over the safe parser.
4. Write golden bytes and exhaustive truncation tests.
5. Produce the final threat and compatibility tables.

## Adversarial cases

- empty input
- every truncated prefix
- declared payload above 4096
- checksum mutation
- trailing byte
- missing output parent
- null FFI arguments
- valid zero-length payload

## Evidence to produce

- a complete packet offset table and canonical golden byte sequence;
- exhaustive truncation and declared-length adversarial tests;
- a replacement state machine with an explicit commit point;
- a C/Rust ABI contract and null/overlap rules;
- an unsafe inventory mapping every block to safe entry points, assumptions, tests, and remaining target evidence.

## Prohibited shortcuts

Do not broaden the product to networking or concurrency, claim soundness because the unsafe code is short, accept `is_err()` as sufficient parser evidence, merge operational errors into strings, omit the post-commit state, or generalize one platform observation into a portable guarantee. Completeness means every stated boundary is defensible, not that every possible feature exists.

## Transfer

Add a second packet version with one optional field. Preserve version 1 parsing unchanged and explain the compatibility policy.

## Comparing with the reference

Perform the comparison as an audit: representation, validation order, allocation timing, commit semantics, ABI translation, cleanup, tests, and compatibility. Record each disagreement as a contract difference before deciding which implementation is stronger. The reference is not authoritative when its stated proof is weaker than yours.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/` and do not open `solution/` until the contract, adversarial cases, and transfer are implemented or a precise blocker is written.

The laboratory is complete when the tests and documented failure paths pass, and you can answer this question without the chapter:

> How do you prove a systems product across binary formats, files, paths, processes, unsafe code, allocation, and FFI without letting one boundary invalidate another?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```
