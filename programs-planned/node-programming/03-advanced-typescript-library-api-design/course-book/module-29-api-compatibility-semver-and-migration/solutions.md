# Module 29 Reasoned Solutions

## A. Matrix

Adding an optional output may still break exact key consumers; adding a required implementor member is breaking. Widening outputs and narrowing inputs are usually breaking. A defaulted generic can be additive only if inference remains stable. Tightening a constraint is breaking. Exact optionality changes construction/presence. `exports` can close old paths. Error ordering and format removal are behavioral/data breaks.

## B. Fixtures

A compatibility fixture must use old source and old data, not source rewritten for V2. Compile success is only one dimension; runtime import and behavior are separate.

## C. Deprecation

The adapter keeps old thrown-error semantics while delegating to the new structured parser. Documentation names the replacement and semantic difference. Removal waits for a major release after a supported transition period.

## D. Migration

Parse each version with its own schema, then migrate V1 to canonical V2. A V2 schema should not contain undocumented defaults solely to absorb V1.

## E. Laboratory

The release decision should identify callers, plugin implementors, package specifiers, and stored request fixtures. A version label without that matrix is unsupported.

## F. SchemaKit

Issue codes, unknown-key behavior, and union ordering remain explicit compatibility contracts. Old data fixtures prove migration. Declarations and package exports are reviewed alongside runtime code.

## G. Reconstruction standard

A complete defense states the old promise, new promise, affected role, evidence, adapter possibility, release level, and migration action.

## I. Matrix reasoning

An optional output field may still break exact snapshots, serializers, exhaustive key iteration, and runtime schema strictness. A required input field is directly source-breaking. A union member can break exhaustive consumers. Reordering overlapping validators changes behavior without changing types. A defaulted generic can be compatible if inference and declarations remain stable; tighter constraints reject old programs. Adding `exports` can break deep imports. Error codes and toolchain baselines are contracts when consumers automate around them.

## J. Fixtures

Library-local tests are written from the new author's perspective. An old caller fixture proves source compatibility. An implementor fixture catches changes to extensible interfaces, abstract classes, or callbacks. Persisted fixtures prove runtime compatibility and migration. These are different failure surfaces and should remain in the repository after the release.

## K. Deprecation

First publish the replacement and mark the old helper deprecated while preserving behavior. Documentation should show mechanical migration. A later release can add tooling or warnings only if they do not destabilize ordinary output. Removal belongs in a major version and should include a compatibility note. If the old behavior can be implemented as a thin adapter indefinitely, the team must still own its maintenance cost explicitly.

## L. Future versions

Reject is safest when unknown semantics could be misinterpreted. Preserve is useful for round-trip tools but requires an output model for unknown data. Opaque pass-through can maintain transport without granting trusted access to fields. A V2 output type must not pretend a V3 value has V2 semantics merely because common properties exist.

## M. Breaking release note

A useful note identifies the exact import, call, or stored format that stops working. It provides before/after code, a migration command or adapter, data-version behavior, and rollback requirements. “Internal refactor” is not an explanation when observable behavior changes.

## N. Declaration diff

A source refactor that leaves declarations identical may still change runtime behavior, so declaration diff is necessary but insufficient. New exports expand the supported surface. A changed input, output, union, overload, constraint, or default can affect consumers. Accidental internal names in declarations are defects even when no current test imports them, because they complicate emission and may become relied upon.

## O. Error surface

Consumers should branch on stable structured codes or classes, not full prose. Message wording can improve in a compatible release when documentation says it is human-facing. Codes, path structures, and error categories need stronger stability because automation may depend on them. Changing a stable code requires migration and usually a breaking-release decision.
