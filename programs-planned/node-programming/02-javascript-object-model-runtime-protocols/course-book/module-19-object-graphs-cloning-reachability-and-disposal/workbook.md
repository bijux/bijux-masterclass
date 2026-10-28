# Module 19 Workbook

For every lifetime problem, draw strong edges first. For every copy problem, write a preservation matrix before choosing an API.

## A. Retention graph

A long-lived emitter stores a bound instance method. The instance stores a cache map containing snapshots. Draw the complete strong path from module root to snapshots. Then design deterministic listener removal and cache eviction.

Explain why changing the cache to a `WeakMap` does not solve listener retention.

## B. Clone comparison

For a class instance containing:

- private state;
- enumerable data;
- non-enumerable metadata;
- symbol metadata;
- accessor;
- shared nested object;
- cycle;
- function;

compare:

```text
spread
Object.assign
complete descriptors + same prototype
JSON round trip
structuredClone
domain reconstruction
```

Mark preserved, transformed, rejected, shared, or lost for each feature.

## C. Alias-preserving graph clone

Implement a narrow clone for arrays and null-prototype records containing JSON scalar leaves. It must preserve cycles and shared aliases using a `WeakMap`. It must reject accessors, custom prototypes, symbols, and unsupported built-ins with path-aware errors.

## D. Weak-cache design

Design a derived-inspection cache keyed by live node instances. State:

- why keys may be weak;
- why values must not retain keys;
- why entries cannot be enumerated;
- how cache misses are handled;
- why tests must not depend on collection timing.

## E. Finalizer rejection

Review these proposed uses of `FinalizationRegistry`:

- close a file;
- remove a listener;
- decrement active-session count;
- log a best-effort leak warning;
- evict a recomputable cache entry;
- roll back an edit.

Classify each and explain the deterministic alternative where needed.

## F. Disposal state machine

Design `open → committed` and `open → rolled-back` transitions for an edit lease. Specify results of:

- commit twice;
- rollback twice;
- dispose after commit;
- commit after dispose;
- disposal failure;
- body failure plus disposal failure.

## G. Independent laboratory

Complete [Graph Snapshot and Lease](../../labs/module-19-graph-snapshot-and-lease/README.md). It requires alias-preserving graph snapshots, explicit ID remapping, weak optional metadata, and idempotent deterministic disposal.

## H. ObjectAtlas transfer

Implement subtree clone and edit-session cleanup. Tests must prove:

- destination IDs are allocated and validated before publication;
- source aliases map consistently;
- destination nodes are new live instances;
- child order is preserved;
- failure changes nothing;
- session terminal operations release large references;
- finalization is not required for correctness.

## I. Reconstruction and defense

Without notes, explain:

- reachability roots and edges;
- shallow versus domain clone;
- JSON and structured clone boundaries;
- memoization for cycles and aliases;
- weak collection limitations;
- finalizer nondeterminism;
- explicit disposal and idempotency;
- reverse-order cleanup;
- why ObjectAtlas reconstructs branded nodes instead of cloning runtime surfaces.
