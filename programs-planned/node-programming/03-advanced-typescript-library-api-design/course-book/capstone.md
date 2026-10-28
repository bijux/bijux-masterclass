# Capstone — SchemaKit

SchemaKit is the cumulative product of Course 3: an ESM schema-combinator library whose runtime validators, inferred output types, declaration files, package exports, examples, and compatibility policy describe the same system.

The capstone is not “a validation library because validation is useful.” It is chosen because it forces every Course 3 mechanism to interact:

```text
unknown external value
        ↓ runtime schema
validated output
        ↓ generic extraction
inferred consumer type
        ↓ declaration emission
published type contract
        ↓ package exports
supported import paths
        ↓ compatibility policy
safe future change
```

## Product contract

SchemaKit must provide:

- `Schema<T>` as one runtime parser associated with one output type;
- `Infer<S>` as a type-level projection from schema value to output;
- non-throwing `safeParse` and throwing `parse` operations driven by the same decoder;
- structured issues with bounded path data;
- primitive and literal schemas;
- optional, nullable, array, tuple, object, record, and union combinators;
- refinement, transformation, and lazy recursion;
- strict unknown-key handling with an explicit strip mode;
- a JSON helper subpath;
- a testing-helper subpath;
- emitted declarations for all public entry points;
- a versioned example format and migration;
- a process-level CLI;
- runtime, type-level, package, compatibility, and process tests.

The library must not claim that TypeScript validates external values. It must not let public types promise behavior that the runtime parser does not implement.

## Architecture

```text
src/core.ts          Schema, Infer, ParseResult, Issue, SchemaError
src/primitives.ts    string, number, Boolean, literal, unknown
src/combinators.ts   optional, nullable, array, tuple, union, refine, transform, lazy
src/object.ts        object and record schemas
src/json.ts          JSON syntax boundary and canonical rendering
src/testing.ts       type and result helpers for consumers
src/project.ts       versioned example schema and migration
src/index.ts         main public entry point
src/main.ts          CLI boundary
```

Only `index`, `json`, and `testing` are exported package entry points. Internal decoder authority is intentionally absent from the package contract.

## Module increments

### Module 21 — Public structural contract

Write the first `Schema<T>`, `Issue`, and `ParseResult<T>` surfaces. Decide which members consumers may implement or inspect. Use readonly output and avoid exposing an internal callback that would let consumers manufacture trusted values.

**Invariant:** a failure cannot also contain a value, and a success cannot also contain issues.

### Module 22 — Generic relationships

Add `Infer<S>` and generic helpers. Test that schema values preserve exact literal and tuple relationships.

**Invariant:** every generic parameter expresses a relation that callers can observe; no unused or independently selectable parameter pretends to be safer than runtime behavior.

### Module 23 — Conditional extraction

Implement `Infer<S>`, optional-output extraction, and union output computation. Add type tests for distribution and `never` behavior.

**Invariant:** type-level branching transforms known types; it never substitutes for runtime parsing.

### Module 24 — Shape transformation

Implement object and tuple output computation with mapped types. Preserve required and optional keys under `exactOptionalPropertyTypes`.

**Invariant:** a missing optional property is different from a present property containing `undefined`.

### Module 25 — Variance and callback safety

Audit `Schema<out T>`, refinement predicates, transformation callbacks, and lazy factories. Do not expose bivariant callback methods where a narrower callback could receive a wider value.

**Invariant:** every callback is invoked only with values its parameter type can safely consume.

### Module 26 — Declarations and type tests

Enable declaration emission. Add consumer-style type tests that inspect public entry points rather than importing implementation files.

**Invariant:** emitted declarations are generated from the same source that runs; handwritten declaration claims do not drift from runtime behavior.

### Module 27 — ESM package contract

Publish exactly three entry points through `exports`. Test their declaration and runtime targets. Keep internal files private even though they exist under `dist`.

**Invariant:** an import path is supported only when it appears in the package contract.

### Module 28 — Validation algebra

Complete all combinators, resource bounds, plain-object policy, paths, issue accumulation, cycle handling, and JSON helpers.

**Invariant:** no external value becomes trusted solely because a caller asserted a type.

### Module 29 — Versioning and migration

Add `SCHEMAKIT_PROJECT_V1`, `SCHEMAKIT_PROJECT_V2`, and a V1-to-V2 migration. Record compatibility effects of strict object validation, union ordering, new error codes, and new export paths.

**Invariant:** migration is an explicit semantic operation; successful parsing of both versions is not itself a migration policy.

### Module 30 — Whole-library defense

Complete CLI, package tests, declaration tests, malformed-input tests, compatibility fixtures, and the final architecture review.

**Invariant:** runtime, static, package, and compatibility contracts agree at the release boundary.

## Final independent extension

Add:

```ts
discriminatedUnion(key, variants)
```

The extension must:

- require every variant schema to accept one distinct literal discriminant;
- infer the union of variant outputs;
- reject duplicate discriminants at construction;
- read the discriminant once from a supported plain object;
- report a precise path for missing or unsupported discriminants;
- delegate full validation to the selected variant;
- appear in the main declaration surface;
- include runtime, type, package, and compatibility tests;
- document whether adding a new variant is compatible for producers and exhaustive consumers.

Begin with an impact map. The reference product intentionally does not contain this feature. The omission is the assessment boundary, not unfinished course material.

## Acceptance route

```bash
npm run typecheck
npm run build
npm test
```

Then inspect:

- `dist/src/index.d.ts`;
- the package export map;
- malformed nested paths;
- optional-field behavior;
- canonical V2 output;
- process exit statuses;
- the independent extension's compatibility analysis.
