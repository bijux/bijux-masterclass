# Module 26 — Declaration Files, Declaration Emission, and Type Tests

> **Question:** How do you prove that the public declarations consumed by another package describe the JavaScript that will actually execute?

## Why this comes now

Modules 21–25 developed sophisticated static relationships. A library consumer does not normally read your implementation source to obtain those relationships. The consumer sees declaration files, package metadata, and editor information. A `.d.ts` file is therefore not build residue. It is a public artifact.

Declarations can fail in several independent ways:

- the runtime export does not exist;
- the declared parameter or result is wrong;
- an internal helper leaks into the public surface;
- a generic constraint becomes broader or narrower than intended;
- an emitted import path cannot be resolved by a consumer;
- an ambient declaration creates a global or module that the runtime never provides;
- declaration merging silently changes a contract;
- tests exercise implementation imports rather than the published entry point.

This module treats declaration design, generation, inspection, and type tests as one engineering loop.

## Outcomes

By the end of the module, you can:

- distinguish implementation files, emitted JavaScript, and emitted declarations;
- explain ambient contexts and the meaning of `declare`;
- distinguish external modules, global declarations, ambient modules, and module augmentation;
- handwrite a declaration for an existing JavaScript runtime and test agreement;
- configure declaration emission without exposing unintended internals;
- inspect inferred public signatures for widening and unstable implementation details;
- write positive and negative consumer type tests;
- use `isolatedDeclarations`-style discipline to make public types explicit where appropriate;
- review SchemaKit's declaration surface independently from its source.

## 1. Declarations describe; they do not create

```ts
declare function parse(text: string): number;
```

In a declaration context, this says a value named `parse` exists with that call signature. It emits no function.

The runtime must provide the value separately. If JavaScript returns a string, TypeScript consumers can compile and still receive the wrong runtime value.

```js
export function parse(text) {
  return text.trim();
}
```

```ts
export function parse(text: string): number;
```

This pair is internally inconsistent. Static consumer tests and runtime tests are both required.

## 2. Three artifacts, three questions

For a TypeScript source file:

```text
src/index.ts
    ↓ type checking
static relationships
    ↓ emission
JavaScript runtime artifact
    ↓ declaration emission
.d.ts consumer artifact
```

Ask separately:

1. Does the source type-check?
2. Does the emitted JavaScript perform the documented behavior?
3. Does the declaration expose the intended supported surface?

A build can succeed while question 3 has a poor answer. For example, inferred return types may leak a large internal union or a class with private implementation names.

## 3. External modules versus scripts

A file containing a top-level import or export is an external module. Its declarations are scoped to that module.

```ts
export interface User {
  readonly id: string;
}
```

A declaration file without module syntax can contribute to the global scope:

```ts
interface WindowLikeGlobal {
  version: string;
}
```

Global declarations affect every file in the compilation and are difficult to contain. Prefer module-scoped declarations for libraries. Use global declarations only when the runtime truly installs globals and the package is designed to model them.

`export {}` can force a declaration file to be treated as a module.

## 4. Ambient module declarations

An ambient module describes a module specifier:

```ts
declare module 'legacy-parser' {
  export function parse(text: string): unknown;
}
```

This can unblock an untyped dependency, but it creates a strong static claim. It should be kept near the integration boundary, tested against the actual runtime, and removed when the dependency publishes trustworthy types.

Avoid wildcard declarations such as:

```ts
declare module '*';
```

They erase resolution evidence across the entire project.

## 5. Handwritten declarations for JavaScript

A JavaScript-first package may contain:

```text
runtime.js
runtime.d.ts
```

The declaration should model the actual export shape, including:

- named versus default exports;
- call and construct signatures;
- receiver behavior;
- optional fields;
- thrown or returned failure model;
- callback invocation types;
- asynchronous results;
- mutable versus readonly data.

Do not write a richer API than JavaScript implements. A declaration is not a redesign layer unless an adapter runtime supplies the redesigned behavior.

The Module 26 laboratory gives a legacy counter runtime a precise facade. Runtime tests confirm increments and errors; type tests confirm constructor, methods, callback shapes, and rejected inputs.

## 6. Declaration emission from TypeScript

With:

```json
{
  "compilerOptions": {
    "declaration": true,
    "declarationMap": true,
    "emitDeclarationOnly": false
  }
}
```

TypeScript emits declarations for exported surfaces reachable from entry points. Public signatures should be explicit when inference would expose implementation detail.

Example:

```ts
const internalCode = Symbol('internal');

export function createIssue(message: string) {
  return {
    code: internalCode,
    message,
  };
}
```

The inferred return includes the unique symbol type and may force an internal declaration into the public graph. If callers only need a stable issue view, annotate it:

```ts
export interface PublicIssue {
  readonly code: string;
  readonly message: string;
}

export function createIssue(message: string): PublicIssue {
  return { code: 'general', message };
}
```

The public type should represent the contract, not whatever structure happened to be easiest internally.

## 7. Exported anonymous shapes

Declarations can legally contain anonymous object types:

```ts
export declare function status(): {
  readonly ready: boolean;
  readonly count: number;
};
```

This is acceptable for small one-off results. Name a type when:

- callers need to refer to it;
- it recurs across exports;
- it has semantic meaning;
- it needs documentation or deprecation;
- its evolution should be reviewed independently.

Naming every tiny shape creates ceremony; naming no meaningful shape creates unreadable declarations.

## 8. `isolatedDeclarations` discipline

Modern TypeScript supports a mode that requires declarations to be generated from local information and explicit enough source annotations. The exact compiler support and restrictions are version-specific, but the design principle is general:

> Public declaration generation should not depend on opaque whole-program inference that makes the exported contract difficult to identify.

Even without enabling the option everywhere, annotate public boundaries and keep implementation inference internal. This improves build parallelism, declaration stability, and reviewability.

Course 3 does not demand explicit types on every local variable. It demands explicit public intent.

## 9. `stripInternal` is not an API firewall

JSDoc `@internal` plus compiler configuration can remove declarations, but the runtime export or JavaScript path may still exist. Package `exports` and source organization are stronger public-boundary tools.

Do not rely on declaration stripping to make reachable runtime files private. Module 27 addresses package encapsulation.

## 10. Declaration merging

TypeScript can merge compatible declarations:

```ts
interface RequestContext {
  requestId: string;
}

interface RequestContext {
  traceId: string;
}
```

The result contains both members. Namespace, function, class, and enum merging rules also exist.

Merging can support plugin or framework ecosystems, but it creates non-local contracts. A module augmentation may change the apparent type of a dependency for every consumer in the compilation.

Use merging only when extension is an intentional architecture. Prefer explicit generic parameters or registries for local application design.

## 11. Module augmentation

```ts
declare module './client.js' {
  interface Client {
    trace(): string;
  }
}
```

This changes the static interface, but JavaScript must still install the method:

```ts
Client.prototype.trace = function () {
  return this.id;
};
```

An augmentation without runtime installation creates a false declaration. A runtime installation without loaded augmentation creates a missing static surface. The import that performs augmentation is itself an effect and must be documented.

SchemaKit avoids augmentation. Its extension mechanisms are explicit combinators and package subpaths.

## 12. Overloads in declarations

Overload order can affect inference and selection. Broad signatures placed first may capture calls intended for specific signatures.

```ts
export function read(value: string): string;
export function read(value: Uint8Array): string;
```

When evolving overloads:

- preserve existing accepted calls;
- keep specific signatures before broad catch-alls;
- ensure the runtime implementation supports every declared branch;
- type-test representative calls;
- inspect helpers such as `ReturnType` that often observe the last signature.

A declaration test should not only assert that calls compile; it should assert the inferred results.

## 13. Positive and negative type tests

A positive type test can use assignability helpers:

```ts
type Equal<A, B> =
  (<T>() => T extends A ? 1 : 2) extends
  (<T>() => T extends B ? 1 : 2) ? true : false;

type Expect<T extends true> = T;

type _Output = Expect<Equal<Infer<typeof userSchema>, User>>;
```

A negative test uses one expected diagnostic:

```ts
// @ts-expect-error unknown field is rejected
project(user, ['missing'] as const);
```

`@ts-expect-error` is useful because the test fails if the error disappears. It becomes harmful when it suppresses several unrelated diagnostics or is used in production source.

Place each negative case in a small expression with a comment naming the intended rule.

## 14. Consumer tests must import public paths

This test is weak:

```ts
import { object } from '../src/object.js';
```

It proves an internal file compiles. It does not prove the package's supported entry point.

A consumer fixture should import:

```ts
import { object } from '@bijux-masterclass/schemakit';
import { parseJson } from '@bijux-masterclass/schemakit/json';
```

It should also prove that internal paths are not supported. The fixture must run after build/package setup so it resolves the same artifacts a downstream package receives.

## 15. Declaration/runtime parity matrix

For each public export, record:

| Export | Runtime kind | Declaration kind | Test |
|---|---|---|---|
| `string` | function | function returning `Schema<string>` | call + output inference |
| `Schema` | erased interface | type-only export | type import test |
| `parseJson` | function | generic function | malformed JSON + inferred output |
| `SchemaError` | class | constructible class | `instanceof` + declared fields |

This matrix catches declarations that refer to nonexistent runtime values or runtime values exported only as types.

## 16. Declaration maps and source maps

Declaration maps help editors navigate from emitted declarations to source. Source maps help runtime debugging. They are useful package artifacts but affect published size and path privacy. Review:

- whether sources are included in the package;
- whether absolute build paths leak;
- whether maps point to available files;
- whether consumers need source navigation;
- whether proprietary source should be published.

The course emits both for transparency in the local package, then inspects the packed file list.

## 17. Common declaration defects

### Boxed primitive types

Use `string`, `number`, `boolean`, `symbol`, and `object`, not `String`, `Number`, `Boolean`, `Symbol`, or broad `Object` for ordinary values.

### Unused type parameters

A generic parameter appearing once adds confusion and may imply a relation that does not exist.

### Callback `any`

`any` disables checking for both the library and consumers. Use a specific parameter or `unknown` with narrowing.

### Optional callback when always called

A declaration that marks a callback optional while runtime unconditionally invokes it is wrong.

### Declared default export with named runtime export

Module shape mismatch causes runtime import failures despite type success.

### Internal path imports

Declarations that import from private source paths create brittle consumer resolution.

## 18. SchemaKit declaration design

SchemaKit's public declarations should expose:

- `Schema<out T>`;
- `Infer<S>`;
- `ParseResult<T>` and `Issue`;
- public combinator functions;
- `SchemaError`;
- JSON and testing subpath exports.

They should not expose:

- internal decoder function types;
- mutable issue accumulators;
- implementation symbols;
- local parser context objects;
- source-directory paths;
- test-only assertion helpers from the main entry point.

Module 26 adds declaration inspection and type tests before package exports are finalized in Module 27.

## 19. A declaration review procedure

1. Clean the output directory.
2. Build with declarations.
3. Read every public `.d.ts` entry point without source.
4. List every exported runtime and type name.
5. Compare against the runtime export matrix.
6. Search for internal file names and helper types.
7. Run positive and negative consumer tests.
8. Execute runtime tests through emitted JavaScript.
9. Review changes to declarations as API changes.
10. Keep a representative previous declaration fixture for compatibility.

## 20. Common wrong models

### “Emitted means correct”

Emission can faithfully describe an accidentally bad inferred API.

### “`declare` creates a runtime value”

It only tells the checker a value exists.

### “Type tests replace runtime tests”

Erased declarations cannot prove JavaScript behavior.

### “Internal types are harmless if undocumented”

If reachable through public declarations, consumers can depend on them.

### “Module augmentation adds the method”

Runtime installation remains a separate effect.

### “A package has types because source is TypeScript”

Consumers receive declarations and entry-point metadata, not your development experience.

## 21. Use the idea in a complete program

Module 26 adds to SchemaKit:

- explicit public return types where inference leaks internals;
- declaration emission and maps;
- a declaration-parity test matrix;
- positive and negative type tests;
- public deprecation tags where appropriate;
- inspection ensuring internal decoder types remain private.

The legacy declaration lab proves the harder case: JavaScript exists first, so the declaration must be validated against an independent runtime.

## Practice sequence

1. Inspect a declaration before reading its source.
2. Predict the eight Module 26 investigations.
3. Find one exported function whose inferred declaration leaks implementation detail.
4. Complete [Legacy Runtime Declaration Facade](../../labs/module-26-legacy-runtime-declaration-facade/README.md).
5. Implement the Module 26 SchemaKit declaration tests in [the capstone guide](../capstone.md#module-26--declarations-and-type-tests).
6. Compare runtime exports and declaration exports mechanically.

## Ready to continue

You are ready for Module 27 when you can explain:

- why declarations describe rather than create;
- external module versus global ambient scope;
- handwritten declaration/runtime parity;
- why emitted declarations still require review;
- positive and negative type tests;
- overload and augmentation risks;
- which SchemaKit internals must remain absent from public declarations.

Next: [Node ESM Packages, Exports, and Consumer Contracts](../module-27-node-esm-packages-exports-and-consumer-contracts/index.md).
