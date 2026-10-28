# Module 19 Reasoned Solutions

## A. Retention graph

The emitter strongly owns the listener function. A bound listener strongly retains its receiver. The receiver owns the cache map, and the map owns snapshots. Leaving the lexical scope that created the instance changes none of those edges.

The principled repair stores the registered listener identity and removes it during explicit close. The cache has an explicit size/eviction policy. A weak cache cannot break the emitter-to-bound-function-to-instance path.

## B. Clone comparison

Spread and `Object.assign` copy enumerable values, execute getters, omit hidden state, normalize descriptors, and fail on cycles only indirectly if later serialization is attempted. Descriptor cloning preserves the shallow runtime surface but not private fields or deep identities. JSON loses prototypes, symbols, functions, aliases, and cycles. Structured clone preserves supported cycles and aliases but does not reconstruct arbitrary custom class semantics. Domain reconstruction chooses exactly which data and identity relationships belong to the product.

The principled answer chooses from a preservation matrix, not from the label “deep clone.”

## C. Alias-preserving graph clone

The clone creates and memoizes the destination container before recursing. That early memoization resolves self-cycles and repeated references. It inspects descriptors so accessors are rejected without execution. Path-aware errors name the unsupported source location.

## D. Weak-cache design

The cache exists only to avoid recomputing diagnostic data while a node is live. A `WeakMap` does not extend node lifetime, and a missing entry can be recomputed. Values must not contain a strong path back to their key. Because entries cannot be listed or counted, operational cache metrics require a different explicit mechanism.

## E. Finalizer rejection

Required close, listener removal, authoritative counters, and rollback cannot depend on finalization. Best-effort leak warnings are a plausible diagnostic use. A recomputable weak cache needs no finalizer for correctness. The rule is whether late or absent execution changes product correctness.

## F. Disposal state machine

Commit after commit and commit after rollback should fail or return an explicit already-terminal result. Rollback and disposal can be idempotent. Disposal after commit should do nothing beyond releasing references. If disposal can fail, the terminal state and remaining resource obligation must be explicit. When body and disposal both fail, preserve both causes rather than silently replacing the original error.

## G. Laboratory

A complete implementation separates plain graph snapshotting from live instance construction, preserves alias mapping, and makes cleanup an explicit terminal transition. Weak metadata is optional and never authoritative.

## H. ObjectAtlas transfer

The atlas builds a complete source-to-destination ID map and candidate records before changing membership. It constructs new valid node instances at publication. Edit sessions clear base snapshots and change maps on terminal transitions so callers do not retain large graphs accidentally.

## I. Reconstruction standard

A complete answer treats lifetime as a graph and cleanup as a protocol. It does not rely on lexical scope, weak references, or finalizers where deterministic application state is required.
