# Course 3 Reference Desk

This page summarizes decisions. It is not a substitute for the chapters.

## Structural assignability

Ask:

1. What is the source type?
2. What is the target type?
3. Which target members are required?
4. Are optional and readonly capabilities compatible?
5. Is this a fresh object literal subject to excess-property checking?
6. Has literal information widened?
7. Is an assertion bypassing evidence?
8. Does the runtime validate exactness or identity?

## Generic design

A type parameter should represent a relationship visible in at least two meaningful places. Common relationships:

```ts
function get<T, K extends keyof T>(value: T, key: K): T[K]
```

`T` connects value and key domain. `K` connects the selected key and result type.

## Conditional types

```ts
type Output<T> = T extends Schema<infer Value> ? Value : never;
```

A conditional distributes when the checked type is a naked type parameter. Disable distribution with a tuple wrapper:

```ts
type NonDistributive<T> = [T] extends [string] ? true : false;
```

## Mapped types

```ts
type ReadModels<T> = {
  readonly [K in keyof T]-?: T[K];
};
```

Use `as` to remap or filter keys. Estimate the resulting key set before writing a template-literal transformation.

## Variance

- producer of `T` → covariance may be valid;
- consumer of `T` → contravariance may be valid;
- both producer and consumer → invariance is usually required;
- mutable collection → do not assume safe covariance;
- method parameters receive historically permissive checking in some contexts.

## Declaration review

Inspect:

- exported names;
- inferred public types;
- leaked internal helpers;
- overload order;
- generic defaults and constraints;
- optional and readonly modifiers;
- import paths inside declarations;
- documentation and deprecation tags;
- alignment with runtime exports.

## Package review

Trace:

```text
consumer specifier
  → package exports key
  → types condition / declaration file
  → import condition / JavaScript file
  → internal imports
  → Node execution
```

A deep path that works only because a file exists is not a supported entry point unless exported deliberately.

## Compatibility surfaces

| Surface | Typical break |
|---|---|
| source | renamed export, changed call syntax |
| type | narrower input, wider callback argument, changed generic inference |
| declaration | leaked helper, changed overload order, missing subpath types |
| runtime | changed return shape or thrown error |
| behavior | changed ordering, defaults, validation, or timing |
| package | removed export or changed module format |
| data | new required field or incompatible version |

## Primary sources

- Type compatibility: <https://www.typescriptlang.org/docs/handbook/type-compatibility.html>
- Generics: <https://www.typescriptlang.org/docs/handbook/2/generics.html>
- Conditional types: <https://www.typescriptlang.org/docs/handbook/2/conditional-types.html>
- Mapped types: <https://www.typescriptlang.org/docs/handbook/2/mapped-types.html>
- Template-literal types: <https://www.typescriptlang.org/docs/handbook/2/template-literal-types.html>
- Declaration files: <https://www.typescriptlang.org/docs/handbook/declaration-files/introduction.html>
- Node package entry points: <https://nodejs.org/api/packages.html#package-entry-points>
- Node ESM: <https://nodejs.org/api/esm.html>
