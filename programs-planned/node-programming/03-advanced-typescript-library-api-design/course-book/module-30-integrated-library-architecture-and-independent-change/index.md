# Module 30 — Integrated Library Architecture and Independent Change

> **Question:** Can the complete library preserve runtime truth, static inference, declaration quality, package boundaries, and compatibility when one feature crosses every layer?

## Why this comes now

The course has built one causal chain:

```text
structural public shapes
        ↓
generic relationships
        ↓
conditional derivation
        ↓
mapped and generated surfaces
        ↓
variance-safe callbacks
        ↓
declaration artifacts
        ↓
package entry points
        ↓
runtime schema algebra
        ↓
compatibility and migration
```

Mastery requires changing the whole system without letting one layer lie. The final module therefore treats SchemaKit as a product under change, not as a collection of combinators.

The independent extension is `discriminatedUnion(key, variants)`. It appears simple, but it affects runtime parsing, type inference, diagnostics, declaration readability, construction validation, overlap policy, examples, compatibility, and package tests. You must begin with an impact map, not with code.

## Outcomes

By the end of the module, you can:

- map a TypeScript library across runtime, type, declaration, package, test, and compatibility surfaces;
- identify one source of truth for each fact;
- review every assertion and public generic relationship;
- inspect emitted declarations without implementation source;
- test the package through documented entry points;
- control type-level complexity and diagnostic quality;
- implement an independent cross-layer feature from a written impact map;
- defend SchemaKit's mechanisms and reject unnecessary alternatives;
- state the remaining boundaries that belong to later Node.js courses.

## 1. The library contract map

SchemaKit contains several representations:

| Surface | Authority | Evidence |
|---|---|---|
| external value | caller/JSON | treated as `unknown` |
| schema declaration | runtime schema object | construction tests |
| inferred output | `Schema<T>` relation | type tests |
| parse result | decoder | runtime tests |
| issue path/code | parser context | adversarial fixtures |
| declaration | emitted `.d.ts` | consumer tests |
| package specifier | `exports` | built import tests |
| compatibility | release policy | old consumers/data |
| CLI output | renderer | process tests |

Every fact should have one owner. When two layers independently restate a fact, drift becomes possible.

## 2. Public API inventory

Review exports by category:

### Core types

`Schema`, `Infer`, `Issue`, `ParseResult`, `PathSegment`, branded helper types.

### Runtime values

primitive factories, combinators, `SchemaError`.

### Boundary helpers

JSON parsing and testing subpaths.

### Example domain

The project-manifest schema should not become a required dependency of the generic core. It belongs in an example or CLI module.

For each export, ask:

- Is it runtime, type-only, or both?
- Does it expose mutable authority?
- Does its declaration leak internals?
- Can it be removed later?
- Which consumer test proves it?

## 3. Internal architecture

A restrained source tree is sufficient:

```text
src/
├── core.ts          result, issue, Schema, makeSchema
├── primitives.ts    primitive and literal schemas
├── combinators.ts   optional, nullable, array, tuple, union, refine, transform, lazy
├── object.ts        object and record schemas
├── errors.ts        SchemaError
├── json.ts          JSON boundary
├── testing.ts       test helpers
├── project.ts       example project schema
├── index.ts         root public surface
└── main.ts          example CLI boundary
```

The exact number of files is not the goal. Each file owns a coherent authority. Avoid both one-file accumulation and a file per tiny helper.

## 4. Assertion review

Schema libraries often need localized assertions because TypeScript cannot preserve every runtime correlation through loops. Each assertion requires a ledger:

- source expression type;
- claimed target type;
- runtime facts establishing the claim;
- tests that would fail if iteration order/length/key relation changed;
- why a safer representation is not practical.

Acceptable examples include tuple accumulation and internal key-indexed handler storage. Unacceptable examples include casting unknown input to inferred output before validation.

## 5. Type complexity budget

Review public helpers for:

- number of generic parameters;
- conditional distribution;
- mapped key count;
- recursive depth/domain;
- template-literal cross product;
- declaration expansion;
- diagnostic readability;
- editor/checker cost.

A good library type is not the narrowest type the compiler can express. It is the most useful relationship readers can understand and the implementation can preserve.

SchemaKit intentionally omits universal exact-object types, compile-time nested path enumeration, arbitrary schema-to-JSON-schema generation, and an open plugin type algebra. Those features would create additional authorities and compatibility burdens beyond Course 3.

## 6. Runtime resource review

Even a synchronous schema library needs resource policy:

- maximum array length;
- maximum object keys;
- maximum issue count;
- maximum recursion depth;
- bounded union-member detail;
- no retained full rejected values;
- copied outputs where later input mutation would invalidate trust;
- deterministic issue order.

Types do not express these bounds. Documentation and runtime tests do.

## 7. Declaration review

Build, then read only:

```text
dist/index.d.ts
dist/json.d.ts
dist/testing.d.ts
```

Ask whether a consumer can understand:

- how to create a schema;
- how output is inferred;
- how failure is represented;
- which members are optional;
- which callbacks are accepted;
- which names are deprecated;
- which internal types are absent.

If understanding requires opening source, the declaration surface is too opaque.

## 8. Package review

Test all supported specifiers through the built package. Confirm:

- ESM import succeeds;
- declarations resolve;
- no default export appears accidentally;
- internal paths fail;
- import has no external side effect;
- package files contain required artifacts;
- Node and TypeScript baselines are stated;
- source and declaration maps do not leak construction paths.

## 9. Test architecture by claim

| Claim | Evidence |
|---|---|
| generic inference | compile-time equality |
| rejected usage | isolated `@ts-expect-error` |
| external validation | runtime unit/adversarial test |
| exact issue path | runtime assertion |
| package resolution | built consumer fixture |
| CLI behavior | process test |
| old compatibility | previous consumer/data fixture |
| declaration cleanliness | emitted artifact inspection |
| resource bound | limit test |
| no import effect | process/import observation |

Coverage percentage does not replace claim-oriented evidence.

## 10. The independent feature: discriminated unions

Desired public shape:

```ts
const eventSchema = discriminatedUnion('kind', {
  created: object({
    kind: literal('created'),
    id: string(),
  }),
  deleted: object({
    kind: literal('deleted'),
    id: string(),
    reason: optional(string()),
  }),
});

type Event = Infer<typeof eventSchema>;
```

The output should be the union of variant outputs.

## 11. Construction-time obligations

At construction, validate:

- non-empty discriminator key;
- non-empty variant map;
- safe own variant keys;
- every variant is an object schema or otherwise guarantees a compatible discriminator;
- map key and literal discriminator agree when statically/runtime inspectable;
- no duplicate normalized variant keys;
- bounded variant count.

Do not defer programmer configuration errors to every parse call.

## 12. Runtime parse algorithm

1. Require a supported plain object.
2. Read the discriminator as an own data value according to object policy.
3. Require a string discriminator for this API.
4. Select the matching variant schema without trying every member.
5. On unknown variant, emit one issue at the discriminator path with bounded allowed values.
6. Parse with the selected schema.
7. Preserve the selected schema's issue paths and deterministic ordering.

This differs from ordinary union search. It is faster, more predictable, and produces better errors for tagged models.

## 13. Static derivation

For:

```ts
type VariantMap = Readonly<Record<string, Schema<unknown>>>;
```

The output is:

```ts
type VariantOutput<V extends VariantMap> = Infer<V[keyof V]>;
```

A stronger signature can relate each map key to a schema output whose discriminator field contains that same literal, but overly complex constraints may damage inference and diagnostics. Decide whether construction-time runtime validation plus representative type tests is the clearer contract.

The final design should preserve useful literal output without exposing a page of conditional internals.

## 14. Diagnostic contract

New stable codes might include:

```text
union.discriminator.missing
union.discriminator.type
union.discriminator.unknown
```

Review whether adding codes widens a public code union. If issue codes are documented as open strings, adding codes is compatible. If exported as a closed literal union, exhaustive consumers may break.

SchemaKit uses stable string codes but does not export one closed exhaustive union. This preserves extension room.

## 15. Compatibility analysis

Adding the new combinator is additive if:

- existing combinators are unchanged;
- issue ordering for ordinary unions is unchanged;
- package entry points remain stable;
- no new import-time effect appears;
- declarations add only new exports;
- Node/TypeScript support is unchanged.

Changing `union` internally to auto-detect discriminators could be breaking because overlapping schemas, member order, and errors change. Keep the new mechanism explicit.

## 16. Documentation as part of the feature

Add:

- one complete example;
- construction rules;
- runtime discriminator policy;
- inferred output demonstration;
- unknown-variant issue example;
- comparison with ordinary `union`;
- compatibility note;
- resource bound.

A feature is not complete when only its implementation exists.

## 17. Independent change procedure

Before editing code, produce:

```text
requirement
→ affected runtime modules
→ affected public types
→ declaration changes
→ package exports
→ error codes
→ tests
→ documentation
→ compatibility
→ resource bounds
```

Then implement in small commits/steps:

1. failing runtime tests;
2. failing type tests;
3. construction validation;
4. runtime parse;
5. static output;
6. public export;
7. declaration inspection;
8. consumer test;
9. docs;
10. compatibility review.

## 18. Architectural alternatives

### Reuse ordinary union

Simpler implementation, but tries every member and produces weaker discriminator errors.

### Accept a list of schemas

Loses direct key lookup and may require extracting discriminator literals at runtime.

### Generate a class hierarchy

Unnecessary; the domain values are plain validated data.

### Use assertions to coerce a variant map

Hides mismatched key/literal configuration.

### Make it a package plugin

Far more extension machinery than the feature needs.

The explicit variant map is the least powerful adequate design.

## 19. Whole-course mechanism defense

You should be able to explain one place each mechanism is used and one place it is rejected:

- structural interface;
- brand;
- generic parameter;
- `keyof`/indexed access;
- conditional type;
- mapped type;
- template-literal type;
- variance annotation;
- handwritten or emitted declaration;
- package subpath;
- runtime schema;
- compatibility adapter.

Mastery includes restraint.

## 20. Boundary to Course 4

Course 3's schemas are synchronous. The CLI performs simple asynchronous file reading, but the schema algebra does not own task scheduling, cancellation, event emitters, supervision, or graceful shutdown. Those are Course 4 responsibilities.

A future async refinement should be a separate abstraction, not a promise silently accepted by the synchronous `refine` callback.

## 21. Common wrong models

### “The final feature is only one function”

Public type, runtime behavior, declarations, errors, tests, docs, and compatibility all change.

### “The most precise constraint is the best API”

Unreadable constraints can harm inference and consumer diagnostics.

### “Trying every union member is equivalent”

Discriminator lookup has different semantics, cost, and errors.

### “New error codes are always compatible”

Not if the code type is a closed union used exhaustively.

### “Passing source tests proves package readiness”

Consumers use built declarations and exported specifiers.

### “More abstraction demonstrates mastery”

The final design should have no mechanism without a named requirement.

## 22. Completion standard

Course 3 is complete when you can:

- run all investigations and explain their causal outcomes;
- complete all labs independently;
- build and test SchemaKit;
- inspect declarations and package entry points;
- validate old compatibility fixtures;
- implement discriminated unions from an impact map;
- defend every assertion and public generic;
- explain which facts remain runtime-only;
- identify what is intentionally postponed to later Node.js courses.

## Practice sequence

1. Complete the whole-library map in the workbook.
2. Predict the eight Module 30 investigations.
3. Complete [Typed Library Architecture Audit](../../labs/module-30-typed-library-architecture-audit/README.md).
4. Run the complete SchemaKit proof route.
5. Implement the independent discriminated-union extension.
6. Complete [the final review](../final-review.md) before reading its solutions.

## Ready to finish

You have completed Course 3 when you can make a cross-layer library change without type assertions at unvalidated boundaries, without hidden package paths, without declaration drift, and without calling an unclassified compatibility break “additive.”

## 14. Architecture is the agreement among surfaces

A mature TypeScript library does not have one API. It has several coupled surfaces:

```text
runtime values
static source types
emitted declarations
package entry points
error behavior
stored formats
consumer extension points
compatibility policy
```

A change is complete only when these surfaces agree. A green local type check can coexist with a broken package export, dishonest declaration, incompatible runtime parser, or stranded stored data. Module 30 therefore reviews the library as a relation among artifacts rather than as a directory of source files.

## 15. Independent change begins with an impact map

Before adding `discriminatedUnion`, list every affected surface and the invariant at risk. This prevents implementation-first tunnel vision. The map should name runtime dispatch, duplicate discriminants, inferred output, declaration emission, package exports, diagnostics, tests, documentation, versioning, and migration. Only then choose implementation details.
