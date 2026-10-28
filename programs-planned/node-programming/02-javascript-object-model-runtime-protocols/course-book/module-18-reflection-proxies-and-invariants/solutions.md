# Module 18 Reasoned Solutions

## A. Reflect equivalence

`Reflect.get`, `Reflect.set`, `Reflect.has`, `Reflect.deleteProperty`, `Reflect.apply`, `Reflect.construct`, and `Reflect.defineProperty` make operands explicit. `Reflect.set`, `deleteProperty`, and `defineProperty` return Booleans. Ignoring `false` can leave a metaprogram believing an operation succeeded. Syntax may throw in strict code when a corresponding set or delete operation returns false.

## B. Receiver forwarding

Using the original receiver preserves ordinary accessor semantics. Using the target can make accessors observe target state and can help private-field methods only when method invocation is also rebound. No generic handler preserves every identity, private brand, accessor, and inheritance behavior. Therefore “transparent proxy” must be treated as a limited claim.

## C. Invariant failures

Each TypeError protects a target fact that cannot be contradicted:

- non-configurable properties cannot disappear from own-key reports;
- a non-extensible target cannot gain or lose reported own keys;
- permanent descriptors cannot be weakened or contradicted;
- own keys cannot contain duplicates;
- a non-configurable property cannot be reported as successfully deleted.

The language checks the handler result against the target after the trap returns.

## D. Complete validation surface

Assignment-only validation is bypassed by direct property definition, deletion, nested mutable references, or direct target access. A correct draft restricts values to immutable JSON-like snapshots, hides the target, handles set/define/delete consistently, and validates the complete candidate at commit. If this remains complex, explicit `setAttribute` and `deleteAttribute` methods are the better design.

## E. Revocation semantics

The revoked proxy rejects future operations. The target reference remains usable. Nested objects extracted earlier remain usable. A bound method extracted earlier may remain callable because it is already a separate function linked to its receiver. Revocation is not retroactive capability erasure and not resource cleanup.

## F. Inspector design

Descriptors avoid getter execution on ordinary objects. Prototype traversal uses `Object.getPrototypeOf`. Seal/freeze checks are reflective. A proxy can still run traps for own keys, descriptors, prototypes, and extensibility. Therefore inspecting an untrusted proxy can execute handler code even without reading property values.

## G. Laboratory

A complete transaction stores base state, proposed writes, and deletions separately. Commit constructs a candidate, validates once, publishes once, transitions to a terminal state, and revokes. Rollback publishes nothing and revokes. Nested values are copied/frozen or excluded by grammar.

## H. ObjectAtlas transfer

The session proxy must front plain draft state, not the node. The node receives one complete validated attribute snapshot at commit. All mutation paths share the same key and value rules. Tests retain the original snapshot and prove no reachable change before successful publication.

## I. Reconstruction standard

A complete answer connects each trap to the corresponding internal operation and target invariant. It does not claim proxy transparency, sandboxing, or cleanup beyond the exact reference surface.
