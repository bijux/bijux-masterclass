# Module 21 Workbook

Do not answer with “TypeScript is structural.” Name source, target, member relationship, freshness, literal state, and runtime evidence.

## A. Predict assignability

For each statement, predict whether it type-checks and explain the first decisive rule.

```ts
interface ReadUser { readonly id: string }
const value = { id: 'u1', role: 'admin' };
const a: ReadUser = value;
const b: ReadUser = { id: 'u1', role: 'admin' };
```

```ts
interface Options { cache?: boolean }
const a: Options = {};
const b: Options = { cache: false };
const c: Options = { cache: undefined };
```

```ts
interface Table { [key: string]: number }
const table: Table = { total: 1 };
const value: number = table['missing'];
```

```ts
const modes = {
  fast: { retries: 1 },
  safe: { retries: 4 },
} satisfies Record<string, { retries: number }>;

type Mode = keyof typeof modes;
```

State the exact inferred `Mode` and explain how an annotation would change it.

## B. Assertion audit

Review each assertion:

```ts
const raw: unknown = JSON.parse(text);
const config = raw as { port: number };
```

```ts
const descriptor = Object.getOwnPropertyDescriptor(value, 'id')!;
```

```ts
return validated as UserId;
```

For each, write:

- the fact the assertion claims;
- whether another operation established it;
- the runtime failure if the claim is false;
- the smallest principled repair.

## C. Exactness policy

Design runtime rules for:

```ts
interface ProjectInput {
  name: string;
  tags?: readonly string[];
}
```

Decide and justify:

- own keys only or inherited keys;
- unknown string keys;
- symbol keys;
- null-prototype objects;
- class instances;
- missing tags versus present `undefined`;
- duplicate tags;
- copying and freezing;
- error paths.

Then write the static interface that describes the validated result, not the raw input.

## D. Brand design

For each candidate, decide whether a brand is useful:

- trimmed display name;
- database user ID;
- port number validated to `1..65535`;
- ordinary search query;
- canonical package subpath;
- JSON string before parsing.

A brand is justified only when creation centralizes a meaningful invariant and accidental interchange matters.

## E. Repair public result states

Replace this interface with a model that prevents contradictory states:

```ts
interface LoadResult<T> {
  loaded: boolean;
  value?: T;
  error?: Error;
  fromCache?: boolean;
}
```

Document whether cache origin exists on failures. Write one exhaustive consumer.

## F. Independent laboratory

Complete [Structural Contract Catalog](../../labs/module-21-structural-contract-catalog/README.md).

Before coding, prepare:

- a source/target table for the public feature declaration;
- a runtime duplicate policy;
- a branded identifier construction rule;
- one example where `satisfies` preserves useful literals;
- one invalid value that type-checking alone cannot reject.

## G. SchemaKit transfer

Implement the Module 21 increment:

- `PathSegment`;
- `Issue`;
- `ParseResult<T>`;
- `SchemaName` brand and parser;
- exact plain-object helper for the example project manifest;
- narrowing tests for success and failure.

Do not implement schema combinators yet. The goal is a truthful public shape.

## H. Reconstruction

Without notes, answer:

1. What is the difference between extra source members and excess object-literal properties?
2. Why can `readonly` be safely exposed while the original object remains mutable?
3. Which operation makes a brand legitimate?
4. Why should a schema accept `unknown`?
5. Which runtime policies cannot be represented by an interface alone?

## I. Assignability matrix

For each source/target pair below, predict assignment, fresh-literal diagnostics, and runtime evidence separately. Do not answer only “passes” or “fails.” Name the rule.

1. A stored value `{ id: 'u1', role: 'admin' }` assigned to `{ id: string }`.
2. The same shape written directly as a fresh object literal.
3. `{ timeout: undefined }` assigned to `{ timeout?: number }` under exact optional properties.
4. A branded `OrderId` assigned to a branded `UserId`.
5. A readonly view whose mutable source alias remains reachable.

Then design the smallest API change that makes each rejected use legitimate without erasing the distinction the type was protecting.

## J. Exactness as a product decision

A configuration loader accepts a fixed public object shape. Compare three policies:

- ignore unknown keys;
- reject unknown keys;
- preserve unknown keys.

For each, state the runtime representation, the static output type, migration consequences, and whether a caller can round-trip data it does not understand. Explain why excess-property checking alone implements none of these runtime policies.

## K. `satisfies`, annotation, and assertion

Create one route table three ways:

```ts
const annotated: Record<string, string> = /* ... */;
const checked = /* ... */ satisfies Record<string, `/${string}`>;
const asserted = /* ... */ as Record<string, `/${string}`>;
```

Record the inferred type of each property, the errors each form can detect, and the unsupported claim made by the assertion. Add a use that benefits from preserved literal information.

## L. Runtime boundary

Write `parseFeatureId(input: unknown): FeatureId`. Reject empty strings, excessive length, and unsupported characters before branding. Add tests showing that a direct assertion can manufacture the brand but cannot make invalid input satisfy the product invariant.

## M. Public-shape review

Inspect the Structural Contract Catalog reference declarations. Mark every exported name as one of:

- consumer capability;
- consumer data model;
- construction boundary;
- implementation detail that escaped accidentally.

If you identify an accidental export, redesign tests so they do not require it.
