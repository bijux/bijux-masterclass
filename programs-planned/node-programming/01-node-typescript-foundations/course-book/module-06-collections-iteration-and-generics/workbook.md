# Module 6 Workbook

## A. Pipeline ledger

For each pipeline, record item type, order, and cardinality after every stage:

```ts
values.filter(isValid).map(toKey)
```

```ts
records.flatMap((record) => record.tags).filter(uniquePredicate)
```

```ts
sessions
  .filter((session) => session.status === 'completed')
  .map((session) => session.actualMinutes)
  .reduce((sum, value) => sum + value, 0)
```

## B. Duplicate policy

Implement `indexUniqueBy` with an error that reports both source positions of a duplicate key. Preserve the first value; do not overwrite it before reporting.

## C. Stable grouping

Write a generic `groupBy` that returns a `Map<Key, T[]>` and preserves source order within every group. Explain whether group iteration order is part of the contract.

## D. Query design

Build a case-normalized search over title and optional note. Ensure an empty normalized query is rejected rather than matching everything accidentally.

## E. Independent laboratory

Complete [Record Query](../../labs/module-06-record-query/README.md). It requires deterministic sort, unique indexing, narrowed filtering, and generic projection.

## F. StudyLedger transfer

Add list, search, and summary operations. Prove they do not mutate ledger order. Test duplicate IDs as invalid persisted state rather than letting a map select the final record.

## G. Reconstruction

Explain `for...of` versus `for...in`, map/filter/flatMap cardinality, generic relationship, Map versus object, stable sort policy, and local mutation inside a pure outward function.

## H. Collection and order clinic

For each operation—lookup by ID, list in ID order, group by status, deduplicate tags, preserve duplicate sessions—choose Array, Map, Set, or a combination. Explain construction cost, duplicate policy, and output order.

Implement `indexUniqueBy` so a duplicate error includes the first and second source positions. Then implement `groupBy` so source order inside groups is preserved. Neither helper may use `any`.

## I. Fold invariant

Define a summary accumulator for planned and completed minutes. State the prefix invariant after `k` records. Test the empty prefix, one record of each state, and a mixed ledger.

## J. StudyLedger checkpoint

Add list, search, and summary. Prove they do not mutate the ledger. Define case handling and ordering in tests rather than relying on insertion accidents.
