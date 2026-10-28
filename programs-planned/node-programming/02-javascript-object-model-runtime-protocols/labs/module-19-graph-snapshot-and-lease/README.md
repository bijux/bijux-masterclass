# Laboratory 19 — Graph Snapshot and Lease

## Product

Build two related mechanisms: a domain-aware graph clone and a deterministic resource lease. Together they force a clean distinction among object identity, domain identity, graph sharing, reachability, and cleanup.

## Graph contract

A graph node has a stable domain ID, label, and edges to other nodes. The clone operation accepts one root and an ID-remapping function. It must:

- preserve internal sharing;
- preserve cycles;
- create new JavaScript object identities;
- assign one new domain ID per source node;
- never invoke source getters accidentally;
- return the source-to-clone map for audit.

A shallow copy is insufficient because edges still point at source nodes. JSON is insufficient because cycles fail and sharing disappears. `structuredClone` preserves graph shape but cannot choose domain IDs or reconstruct product-specific invariants.

## Lease contract

A `LeasePool` has a bounded number of slots. `acquire` returns a `Lease`. `close` or `[Symbol.dispose]` releases exactly once. Repeated close is harmless or explicitly rejected according to a documented policy. Correct capacity must never depend on garbage collection or finalizer timing.

## Required cases

- diamond sharing;
- a self-cycle;
- a multi-node cycle;
- deterministic ID remapping;
- source mutation after clone;
- lease exhaustion;
- normal close;
- disposal;
- repeated close;
- callback failure while a lease is owned.

## Transfer

Add an optional `FinalizationRegistry` only to report leaked leases. Prove that pool capacity remains correct without the finalizer ever running.
## Two different ownership problems

The graph clone owns a temporary source-to-copy map until every edge has been reconstructed. That map is not domain state; it is proof machinery for preserving sharing and cycles. The lease, by contrast, owns a live capacity obligation until close. Its terminal operation changes the pool immediately and exactly once.

Keep these roles separate in the implementation and the explanation. A clone map may disappear after construction because the cloned graph now carries its own references. A lease cannot disappear merely because user code has dropped the last obvious variable; correctness requires explicit release. Optional leak diagnostics may observe garbage collection, but they must never return capacity.

