# Module 29 Workbook

For every change, classify all seven compatibility surfaces and identify affected downstream roles.

## A. Change matrix

Review:

- add optional output field;
- add required interface member;
- widen returned union;
- narrow accepted input;
- add generic default;
- tighten generic constraint;
- change `field?: T` to `field: T | undefined`;
- add `exports` to a previously open package;
- change error aggregation order;
- drop an old file format.

## B. Old consumer fixture

Write consumer source against a V1 library surface. Compile and run it against V2. Record failures by source, type, runtime, behavior, package, and data.

## C. Deprecation plan

Design a complete transition from one throwing API to a structured result API. Include adapter behavior, JSDoc, examples, timeline, and error translation.

## D. Data migration

Implement V1/V2 parsing and a canonical migration. Test malformed V1, valid V1, valid V2, and round-trip V2 output.

## E. Independent laboratory

Complete [Evolvable Client SDK](../../labs/module-29-evolvable-client-sdk/README.md). Produce a release decision and migration guide.

## F. SchemaKit transfer

Add compatibility fixtures, V1/V2 project records, deprecation, and release notes. Do not loosen V2 validation merely to accept V1 silently.

## G. Reconstruction

Defend one major, one minor, and one patch change using affected roles and evidence rather than intuition.

## I. Compatibility matrix

For each proposed change, classify effects on callers, implementors, runtime behavior, declarations, package resolution, persisted data, diagnostics, and tooling:

- add an optional output property;
- add a required input property;
- add a union member;
- reorder union parsers;
- add a defaulted generic parameter;
- tighten a generic constraint;
- add an export map;
- remove a deprecated subpath;
- change an error code;
- increase the MSRV-equivalent TypeScript baseline.

Do not reduce the answer to one semver label until every surface has been considered.

## J. Consumer fixtures

Create one fixture for an old caller, one for a third-party implementor, and one for old persisted data. Run each against the new candidate. Explain why compiling the library's own tests is insufficient.

## K. Deprecation path

Design a two-release migration from `displayName(user)` to `migrateUser(user).displayName`. Include documentation, declarations, runtime behavior, warnings or lack thereof, removal criteria, and the major release boundary.

## L. Unknown future versions

Compare reject, preserve, and opaque-pass-through policies for a `USER_V3` value read by a V2 client. State when each policy is safe and what the output type must say.

## M. Compatibility budget

Write a release note for one deliberately breaking change. Name the old supported behavior, the reason it cannot be preserved, the mechanical migration, the data migration, and a rollback route.

## N. Declaration diff review

Build declarations before and after a candidate change. Classify each diff as source-only refactoring, public type change, documentation change, new supported surface, or accidental leakage. Do not assume a small textual diff is a small compatibility change.

## O. Error compatibility

Select one error class, code, path format, and message. Decide which parts consumers may branch on. Change the message wording while preserving code and structured fields; then change the code. Explain why machine-readable and human-readable error surfaces need different stability promises.
