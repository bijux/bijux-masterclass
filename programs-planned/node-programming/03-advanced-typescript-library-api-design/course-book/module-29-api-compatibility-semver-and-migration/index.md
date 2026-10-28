# Module 29 — API Compatibility, Semantic Versioning, and Migration

> **Question:** What exactly can break when a TypeScript library changes, and how do you preserve callers, implementors, runtime data, and package entry points deliberately?

## Why this comes now

SchemaKit now has runtime behavior, inferred types, declarations, and package exports. Those surfaces create users. Once another package compiles, executes, stores data, catches errors, snapshots output, or implements one of your contracts, a change is no longer local.

“SemVer” is not a magic answer. You first need to classify what changed. TypeScript libraries can break in ways that a JavaScript-only API review misses:

- a generic constraint narrows;
- inference selects a different type;
- a union gains a member and breaks exhaustive consumers;
- an optional property becomes required or present-with-undefined;
- overload order changes;
- a readonly view becomes mutable or vice versa;
- a declaration helper leaks or disappears;
- an export map closes a path;
- runtime validation becomes stricter;
- error codes or ordering change;
- stored V1 data no longer parses.

This module develops a compatibility matrix and a staged migration method.

## Outcomes

By the end of the module, you can:

- distinguish source, type, declaration, runtime, behavioral, package, and data-format compatibility;
- review input and output changes from the perspective of callers and implementors;
- identify inference and overload changes that are source-invisible but type-breaking;
- apply SemVer only after classifying the affected contract;
- design deprecations with a usable replacement and removal horizon;
- preserve old runtime data through versioned parsing and migration;
- build compatibility fixtures against previous declarations and behavior;
- evolve SchemaKit without using broad casts or silent semantic changes.

## 1. Seven compatibility surfaces

### Source compatibility

Does existing consumer source still parse and type-check without edits?

### Type compatibility

Do assignments, inferred results, narrowing, overload selection, and generic instantiations remain valid?

### Declaration compatibility

Do published names, constraints, defaults, modifiers, import paths, and helper types remain stable?

### Runtime compatibility

Do imports resolve and values have the expected kind, shape, prototype, and failure mechanism?

### Behavioral compatibility

Are ordering, defaults, validation, timing, idempotency, error codes, and side effects preserved?

### Package compatibility

Do documented specifiers, module formats, engine ranges, files, and conditions remain supported?

### Data-format compatibility

Can existing stored or transmitted data still be read, interpreted, and migrated?

A release can preserve one surface while breaking another.

## 2. Inputs and outputs have different compatibility direction

For an input parameter, accepting fewer values is breaking:

```ts
// Old
function parse(value: string | Uint8Array): Result;

// New
function parse(value: string): Result;
```

Accepting more inputs is often source-compatible, but can change overload inference or runtime ambiguity.

For an output, returning a broader type can break consumers:

```ts
// Old
function status(): 'ready';

// New
function status(): 'ready' | 'busy';
```

The implementation gained behavior, but callers that assumed `'ready'` now face a new branch.

Returning a narrower structural type may also remove fields consumers accessed, even if the new object is “cleaner.”

## 3. Adding union members is usually consumer-breaking

```ts
type Result =
  | { kind: 'ok'; value: string }
  | { kind: 'error'; message: string };
```

Adding `{ kind: 'pending' }` breaks exhaustive switches and functions that return `never` in the default branch. Whether the change is SemVer-major depends on the public contract and versioning policy, but it must not be dismissed as additive.

`#[non_exhaustive]` has no direct TypeScript equivalent. A library can document open unions, include an unknown variant, or expose visitor functions, but each choice has trade-offs.

## 4. Adding object properties can also break

Adding an optional readonly output field is often compatible for property-reading consumers. It can still break:

- exact type-equality tests;
- exhaustive key maps;
- mapped types over `keyof`;
- object-spread snapshots;
- serialization snapshots;
- implementations of a public interface when the field is required;
- APIs using exactness utilities.

Adding a required property to an input/interface implemented by consumers is usually breaking. Adding a property to a type alias used only as an output may be less disruptive, but structural uses still need review.

## 5. Optionality changes are semantic changes

Under exact optional property types:

```ts
field?: T
field: T | undefined
field?: T | undefined
```

are different construction contracts.

Changing from optional to required is breaking for constructors and object literals. Changing from required-undefined to optional changes own-property presence. Runtime codecs and JSON output may also change.

A migration should state whether missing values receive a default, whether present `undefined` is accepted, and whether canonical output omits or writes the field.

## 6. Readonly changes affect capability

Adding readonly to an input view can break callers that mutate through the reference. Removing readonly from an output does not force runtime mutability but expands apparent capability and may weaken variance.

Changing `readonly T[]` to `T[]` may look permissive, but it permits consumers to mutate data the implementation may share internally. Public mutation authority is a behavioral commitment.

Prefer capability-stable interfaces and create new mutable builder types when mutation becomes a product feature.

## 7. Generic constraints and defaults are public

```ts
function register<T extends object>(value: T): void;
```

Changing the constraint to `{ id: string }` rejects existing callers. Changing a default type parameter can change inferred types without any source edit.

Adding a type parameter may be compatible when it has a default and does not alter inference. Reordering parameters or removing defaults is breaking.

Generic inference is observable. Compatibility tests should compile representative call sites and assert inferred output types.

## 8. Conditional and mapped types amplify source changes

A source interface used by mapped types is an authority for multiple generated surfaces. Adding a field can add events, getters, patches, and schema outputs. Changing a conditional branch can alter many downstream instantiations.

Review:

- union member growth;
- `keyof` growth;
- distribution changes;
- `never` filtering;
- optional/readonly modifier changes;
- template-literal expansion;
- recursive helper domain.

A small alias edit can be a large public change.

## 9. Overload order and catch-all signatures

Adding an overload can change which signature is selected. Moving a broad overload earlier can widen or narrow results unexpectedly. Helpers such as `ReturnType` often observe the final signature rather than full call resolution.

Maintain consumer fixtures for representative overloads. If overload growth becomes difficult to reason about, a discriminated input object or explicit method names may provide a more stable API.

## 10. Error compatibility

Consumers may depend on:

- error class identity;
- `instanceof` behavior;
- error code strings;
- issue paths;
- thrown versus returned failures;
- message text;
- issue ordering;
- aggregation limits.

SchemaKit treats stable issue codes and paths as the primary programmatic contract. English messages are human-facing and may receive non-breaking clarification. Changing fail-fast to accumulated errors or reordering union alternatives can still be behavioral changes.

## 11. Package compatibility

Removing an export, changing module format, tightening `engines`, changing side effects, or omitting files can break consumers without any type signature change.

An ESM-only package that later adds CommonJS must review module identity and dual loading. A package that adds `exports` must preserve or migrate historic deep paths.

Package metadata belongs in release review.

## 12. Versioned data and migrations

A stored record should carry a version discriminator:

```ts
type V1 = {
  readonly format: 'SCHEMAKIT_PROJECT_V1';
  readonly name: string;
};

type V2 = {
  readonly format: 'SCHEMAKIT_PROJECT_V2';
  readonly name: string;
  readonly tags: readonly string[];
};
```

A migration owns the meaning:

```ts
function migrateV1(value: V1): V2 {
  return {
    format: 'SCHEMAKIT_PROJECT_V2',
    name: value.name,
    tags: [],
  };
}
```

Do not make the V2 schema silently accept a missing required field and call that migration unless the default and canonical re-encoding policy are explicit.

Keep fixtures for old versions. Test parse, migration, and canonical output.

## 13. Deprecation is a transition, not a comment

A useful deprecation includes:

- what is deprecated;
- why;
- exact replacement;
- semantic differences;
- migration example;
- release in which removal may occur;
- whether automatic adaptation exists.

```ts
/**
 * @deprecated Use `safeParseJson`; it preserves structured schema issues.
 */
export function parseJsonOrThrow(...): ...
```

The old function must continue to behave according to its contract during the deprecation window. A comment without a working alternative is not a migration.

## 14. Compatibility adapters

Adapters can preserve old call shapes while routing to new internals:

```ts
export function parseLegacy<T>(schema: Schema<T>, text: string): T {
  return parseJson(schema, text);
}
```

An adapter should:

- preserve old behavior intentionally;
- translate new errors to the old model when promised;
- avoid silently changing ordering/defaults;
- emit deprecation documentation;
- have dedicated old-consumer tests;
- remain isolated so it can be removed in a major release.

## 15. Compatibility fixtures

A compatibility suite can include:

- previous `.d.ts` snapshots or a previous package fixture;
- representative consumer source;
- old data files;
- old import specifiers;
- expected runtime outputs/errors;
- migration outputs.

Avoid asserting every formatting detail. Focus on supported public contracts.

Type-only snapshots are insufficient; runtime fixtures catch declaration/runtime drift.

## 16. SemVer decision procedure

1. Name the affected public surface.
2. Identify downstream roles: caller, implementor, subclass, plugin, data producer, data reader, operator.
3. Classify input/output direction.
4. Run old consumer and data fixtures.
5. Determine whether an adapter preserves the contract.
6. Decide patch/minor/major according to documented policy.
7. Write migration notes before release.
8. Preserve evidence with the release artifact.

A version number is the result of analysis, not the analysis itself.

## 17. SchemaKit evolution cases

### Add a new standalone combinator

Usually additive if it does not change existing declarations, runtime behavior, package side effects, or inference.

### Change `number()` to accept `NaN`

Behavioral change. Existing consumers may rely on rejection. Treat carefully, likely major unless introduced as a new combinator.

### Add a union member to an issue-code type

Potentially breaking for exhaustive consumers.

### Add a testing subpath

Additive if existing exports and package resolution remain unchanged.

### Change unknown object keys from reject to strip

Behavioral and security-policy change; likely major.

### Reorder union schema members

May change which overlapping schema wins and which issues appear.

### Tighten Node engine range

Package compatibility change.

## 18. A compatibility ledger

For each proposed change, record:

| Surface | Question |
|---|---|
| source | Does existing source compile? |
| type | Do assignments and inference remain? |
| declaration | Which exported types changed? |
| runtime | Which values, errors, or identities changed? |
| behavior | Ordering, defaults, validation, timing? |
| package | Specifiers, format, engines, files? |
| data | Can old records/messages still be read? |
| adapter | Can old behavior be preserved? |
| release | Patch, minor, major, or no release? |
| migration | What exact action must users take? |

## 19. Common wrong models

### “Adding is always non-breaking”

Union members, keys, overloads, and required implementation members can break consumers.

### “Types do not count for SemVer because JavaScript runs”

TypeScript consumers compile against declarations as a product surface.

### “Optional and undefined are equivalent”

Presence and construction differ.

### “Deprecation makes removal safe”

Only a usable transition and documented major release make removal manageable.

### “Old JSON can be fixed by loosening the new schema”

Migration semantics should be explicit and canonical.

### “Passing current tests proves compatibility”

You need old consumers and old data as evidence.

## 20. Use the idea in a complete program

Module 29 adds to SchemaKit:

- V1/V2 project schemas and migration;
- old-record fixtures;
- a deprecated throwing JSON helper with a structured replacement;
- declaration compatibility checks;
- issue-code and package-export review;
- a release note describing supported Node, TypeScript, and ESM boundaries.

The Evolvable Client SDK lab applies the same method to a request/response library.

## Practice sequence

1. Classify every workbook change across seven surfaces.
2. Predict the eight Module 29 investigations.
3. Compile one previous-consumer fixture against the new declarations.
4. Complete [Evolvable Client SDK](../../labs/module-29-evolvable-client-sdk/README.md).
5. Implement SchemaKit migration and compatibility fixtures from [the capstone guide](../capstone.md#module-29--compatibility-and-migration).
6. Write a SemVer decision before reading the reference rationale.

## Ready to continue

You are ready for Module 30 when you can explain:

- input/output compatibility direction;
- why union and key growth can break consumers;
- generic inference as a public behavior;
- exact optionality changes;
- error and package compatibility;
- versioned migration versus permissive parsing;
- what evidence supports a SemVer decision.

Next: [Integrated Library Architecture and Independent Change](../module-30-integrated-library-architecture-and-independent-change/index.md).
