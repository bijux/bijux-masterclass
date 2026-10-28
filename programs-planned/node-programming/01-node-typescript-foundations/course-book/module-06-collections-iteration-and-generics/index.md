# Module 6 — Collections, Iteration, Generic Relationships, and Deterministic Data

> **Question:** What happens to item type, order, cardinality, identity, and key uniqueness through a transformation?

## Why this comes now

The first five modules established trusted domain values. Real programs hold many of them. Collection code becomes unreliable when `map`, `filter`, `reduce`, `Map`, `Set`, and sorting are treated as interchangeable convenience APIs. Each operation changes a different part of the data contract.

The module uses a transformation ledger:

| Stage | Item type | Order | Cardinality | Identity | Failure | Allocation |
|---|---|---|---|---|---|---|

Write one row per stage when the pipeline is not immediately obvious.

## Outcomes

You can:

- distinguish arrays, maps, and sets by lookup, ordering, and uniqueness policy;
- choose `for...of` rather than `for...in` for iterable values;
- trace order and cardinality through `map`, `filter`, `flatMap`, and `reduce`;
- preserve input order when concurrency or indexing changes processing order;
- write basic generic functions that preserve a real input/output relationship;
- reject duplicate keys rather than silently selecting an accidental winner;
- produce deterministic StudyLedger listings, searches, and summaries.

## 1. Array, Map, and Set answer different questions

An array is an ordered sequence. A map associates unique keys with values. A set represents unique values under its equality semantics. Choosing among them is a product decision.

StudyLedger stores sessions in an array because canonical source order is ascending ID and the course values direct iteration and simple persistence. A temporary `Map<number, StudySession>` may accelerate a local lookup, but it must not become a competing state authority.

## 2. Iteration protocols and loop choice

```ts
for (const session of sessions) {
  // session is an element
}
```

`for...of` consumes an iterable. `for...in` enumerates string property keys and is not an array-element loop:

```ts
for (const key in sessions) {
  // key is "0", "1", ... and inherited enumerable keys are relevant
}
```

Use indexing only when the index itself is part of the algorithm. Under `noUncheckedIndexedAccess`, `values[index]` remains possibly undefined because the type checker does not prove arbitrary bounds from loop arithmetic.

## 3. Adapter semantics

### `map`

One output per input, same order, same cardinality:

```ts
const topics = sessions.map((session) => session.topic);
```

### `filter`

Zero or one output per input, source order preserved:

```ts
const completed = sessions.filter(
  (session): session is CompletedSession => session.status === 'completed',
);
```

The explicit predicate return type teaches TypeScript the narrowed result. Modern inference can derive some predicates, but a public helper should make its contract visible when the relationship matters.

### `flatMap`

Zero or more outputs per input, grouped in source order:

```ts
const notes = sessions.flatMap((session) =>
  session.status === 'completed' && session.note !== undefined
    ? [session.note]
    : [],
);
```

### `reduce`

One accumulator updated for every item. Use it when one named invariant connects the steps. Do not force every loop into `reduce`; an opaque accumulator can be less readable than a direct loop.

## 4. Deterministic sorting

JavaScript’s modern array sort is stable, but the comparator still must define an ordering and should return a finite negative, zero, or positive number.

```ts
const ordered = [...sessions].sort((left, right) => left.id - right.id);
```

Do not mutate retained application state merely to render it. Copy before sorting or maintain the invariant at construction.

Text ordering needs a policy. `localeCompare` can depend on locale options and environment. StudyLedger search normalizes case using a documented simple policy and output order remains numeric ID order.

## 5. Duplicate-key policy

This code silently lets the last item win:

```ts
const byId = new Map(sessions.map((session) => [session.id, session]));
```

If duplicate IDs indicate corrupted state, silent replacement destroys evidence. Build the map with an explicit check:

```ts
function indexUniqueBy<T, Key>(
  values: readonly T[],
  keyOf: (value: T) => Key,
): Map<Key, T> {
  const result = new Map<Key, T>();
  for (const value of values) {
    const key = keyOf(value);
    if (result.has(key)) {
      throw new Error('duplicate key');
    }
    result.set(key, value);
  }
  return result;
}
```

The generic parameters preserve the relationship between input item and key types. They do not validate semantic uniqueness; the loop does.

## 6. Generic relationships, not decorative letters

A generic is justified when callers select a type and the function preserves a relationship involving it:

```ts
function first<T>(values: readonly T[]): T | undefined {
  return values[0];
}
```

The return type is the same element type as the input. Replacing `T` with `unknown` would lose useful information.

A constrained generic requires an operation:

```ts
function findById<T extends { readonly id: number }>(
  values: readonly T[],
  id: number,
): T | undefined {
  return values.find((value) => value.id === id);
}
```

Do not add a constraint for fields the implementation never uses. The weakest sufficient contract admits more valid callers.

## 7. `Map` and object records

A plain object is often suitable for a closed set of known string fields. `Map` is useful when keys are dynamic, non-string, or require direct size/iteration methods. Avoid using an object as an untrusted string-key dictionary without considering prototype keys; `Map` or an object with a null prototype can make the policy clearer.

JSON cannot directly encode `Map` or `Set`. Persistence must define a conversion and ordering. StudyLedger retains plain arrays for canonical storage.

## 8. Summary as an invariant-bearing fold

```ts
interface Summary {
  readonly planned: number;
  readonly active: number;
  readonly completed: number;
  readonly abandoned: number;
  readonly completedMinutes: number;
}
```

A clear implementation can use a local mutable accumulator owned by one function:

```ts
function summarize(sessions: readonly StudySession[]): Summary {
  const result = {
    planned: 0,
    active: 0,
    completed: 0,
    abandoned: 0,
    completedMinutes: 0,
  };

  for (const session of sessions) {
    result[session.status] += 1;
    if (session.status === 'completed') {
      result.completedMinutes += session.actualMinutes;
    }
  }
  return result;
}
```

The mutation is local and exclusively owned. The returned object is a new summary. “Functional style” does not require an allocation per input when a direct fold is clearer.

## 9. Search policy

A useful search normalizes both query and candidate through one authority:

```ts
function normalizeSearch(value: string): string {
  return value.trim().toLocaleLowerCase('en-US');
}
```

This is a product policy, not universal Unicode case folding. Course 9 revisits locale, performance, and indexing evidence. Course 1 documents the chosen behavior and tests it.

## 10. StudyLedger increment

Implement:

- `findSession` without mutation;
- status filtering with a narrowing predicate;
- normalized topic/note search;
- stable ID ordering;
- summary counts and completed minutes;
- duplicate-ID rejection during index construction or validation.

Render from derived data; do not reorder the retained ledger merely for presentation.

## Common wrong models

### “Map and object are the same dictionary”

They differ in key domain, prototype behavior, iteration, serialization, and API.

### “`map` is a generic loop”

It promises one output per input. Use an operation whose cardinality matches the problem.

### “Generics make code reusable”

A generic should preserve a meaningful type relationship. Otherwise it may only obscure the contract.

### “Sorting is harmless”

`sort` mutates. Ordering policy and comparator validity are product concerns.

### “Map construction validates uniqueness”

It may silently overwrite. Duplicate policy must be explicit.

## 11. Choose a collection from the dominant operation

A collection is an API decision, not merely a storage syntax choice.

| Need | Natural starting point |
|---|---|
| stable ordered sequence, duplicates allowed | `Array<T>` |
| unique keys with arbitrary key types | `Map<K, V>` |
| unique values and membership checks | `Set<T>` |
| fixed known string-key object shape | object/interface |

StudyLedger stores sessions in an array because source order by allocated ID is meaningful, records are small, and Course 1 favors a transparent representation. A large system might add an index, but replacing the array with a `Map` would change serialization and ordering policy rather than automatically improve the design.

## 12. Iteration consumes a protocol

`for...of` asks a value for an iterator and repeatedly calls `next`. Arrays, maps, sets, strings, and many Node objects are iterable. This protocol matters because iteration order and yielded item shape differ:

```ts
for (const value of array) { /* value */ }
for (const [key, value] of map) { /* entry tuple */ }
for (const character of text) { /* Unicode code point string */ }
```

Array methods add conventions around source index, holes, and new collection allocation. Select a method whose result communicates intent:

- `map` — one output slot per visited input slot;
- `filter` — preserve accepted source values;
- `flatMap` — zero or more outputs per input;
- `find` — first matching value or `undefined`;
- `some`/`every` — short-circuiting predicates;
- `reduce` — explicit accumulator transition.

A long adapter chain can obscure item shape. Write a stage table when necessary:

| Stage | Item type | Cardinality | Order | Allocation |
|---|---|---|---|---|
| source | `Session` | N | ID order | existing |
| filter completed | `CompletedSession` | 0..N | preserved | new array |
| map minutes | `number` | same as previous | preserved | new array |
| reduce sum | one number | 1 | not applicable | accumulator |

## 13. Complexity claims require a workload

`Map.get` is generally chosen for direct key lookup; `Array.find` scans in order. That does not prove a map is better for every product. Index construction costs time and memory, and duplicate policy must be decided.

For small ledgers, a linear scan keeps one source of truth and simplifies persistence. When workloads grow, measure or model:

- number of records;
- lookup frequency;
- update frequency;
- memory retained by indexes;
- need for deterministic order;
- cost of keeping indexes coherent.

Course 9 will make performance claims empirical. Course 1 simply prevents complexity folklore from replacing product reasoning.

## 14. Generic parameters must express a relationship

This helper earns its generic parameters:

```ts
function indexUniqueBy<T, K>(
  values: readonly T[],
  keyOf: (value: T) => K,
): Map<K, T> {
  // ...
}
```

`T` connects source items, callback input, and map values. `K` connects callback output and map keys. A generic that appears only once often tells callers nothing useful:

```ts
function parse<T>(text: string): T // cannot prove T
```

That signature manufactures trust. A parser should return a concrete type after validation or accept a decoder that establishes `T`.

## 15. Determinism must be designed

Array order is explicit. Map iteration follows insertion order. Object property order has specified categories but is a poor place to hide a report contract. Sorting introduces another policy: comparator, case handling, locale, tie breaking, and mutation.

For stable output, sort a copy with a total tie breaker:

```ts
const ordered = [...sessions].sort(
  (left, right) => left.id - right.id,
);
```

A title sort might require `localeCompare`, but the chosen locale and sensitivity become observable. StudyLedger orders by numeric ID to avoid locale dependence.

## 16. Folds carry invariants

A summary reducer is a small state machine. Define its accumulator before writing the loop:

```ts
interface Summary {
  total: number;
  completed: number;
  plannedMinutes: number;
  completedMinutes: number;
}
```

After processing the first `k` sessions, the accumulator must equal the summary of exactly that prefix. This prefix invariant makes the reducer reviewable and supports tests that compare partial and complete inputs.

Do not combine unrelated facts simply because one loop can compute them. The accumulator should remain understandable and bounded.

## Practice sequence

Complete the [workbook](workbook.md), then [Record Query](../../labs/module-06-record-query/README.md). Add deterministic queries and summaries to StudyLedger.

## Ready to continue

Continue when you can state type, order, cardinality, identity, and duplicate policy for every collection stage in the product.

Next: [Module 7 — Modules, Packages, Resolution, and Public API Boundaries](../module-07-modules-packages-and-public-apis/index.md)
