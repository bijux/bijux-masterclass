# Final Review — Reasoned Guide

This guide states the causal standard. It is not a single code key for the independent products.

## Part I — Reconstruction standard

A complete property answer distinguishes data and accessor descriptors and names writable, enumerable, and configurable separately. It explains that omitted descriptor fields default differently from ordinary assignment. Enumeration must be treated as several distinct observation surfaces, not as “looping over an object.”

The prototype answer must preserve the original receiver while the lookup object changes. An inherited accessor executes with that receiver. The write answer must distinguish an inherited setter from a writable data property and from creating an own property.

The identity answer must separate constructor `.prototype`, an object's internal prototype, `instanceof` behavior, JavaScript private brand, TypeScript structural compatibility, domain identity, and reference identity. Setting a prototype does not perform private initialization.

The call answer must derive `this` from invocation form. Bound functions capture receiver and prefix arguments, arrows use lexical `this`, and `new` ignores a bound `this` while retaining bound arguments. A constructor may replace the created receiver only by returning an object.

The class timeline must show base fields before the base constructor body and derived fields only after `super` returns. An override called from a base constructor can observe an uninitialized derived state.

The composition answer is evaluated through authority, state ownership, conflict policy, construction, and lifecycle. “Composition over inheritance” without those facts is insufficient.

The protocol answer must distinguish protocol discovery from ordinary string-named methods. Coercion, inspection, serialization, and user rendering remain separate. Symbols avoid accidental string collisions but are discoverable and not secret.

The iterator answer must show that an iterable creates or supplies an iterator, the iterator owns traversal state, and early termination may call `return`. Generator `finally` can observe close when the generator is resumed and closed by the consumer protocol.

The proxy answer must state that the proxy is a new identity and that traps are constrained by the target. A legal design cannot hide a non-configurable property from `ownKeys`. Private-field behavior is not transparently forwarded through arbitrary proxies.

The clone answer must identify which object identities and domain IDs are preserved or remapped. `structuredClone` is a data-cloning algorithm, not class reconstruction. Deterministic cleanup belongs to explicit ownership, not finalizer timing.

## Part II — Prediction standard

A classification alone is partial evidence. The explanation must name the decisive rule. For example, “fails at runtime” is not sufficient when the cause is a private-brand check against a proxy receiver. Weak repairs include:

- changing a descriptor to configurable only to satisfy a proxy lie;
- binding every method eagerly rather than defining receiver policy;
- converting methods to arrows without considering per-instance allocation and subclass behavior;
- spreading an instance to make a copy;
- setting a decoded object's prototype to imitate construction;
- serializing through getters;
- using JSON to clone a graph;
- relying on `as` or `any` to hide a runtime distinction;
- swallowing disposal or persistence failure.

## Part III — Clinic guidance

### A — getter-triggering serializer

Persistence should not enumerate and read the live instance. Define a plain snapshot method or codec that selects private state deliberately and returns validated data. Descriptor-based inspection can list accessors without invoking them. Debug inspection may opt into controlled evaluation but must not be reused as storage.

### B — forged class instance

`setPrototypeOf` changes delegation. It does not execute the constructor, install public fields, or establish private brands. The record and legitimate instance have different runtime histories. Reconstruction must validate the record and call a factory or constructor that performs all invariants.

### C — lost receiver

Valid repairs include:

1. store a wrapper `(input) => service.execute(input)` that grants only the intended call;
2. bind the specific method once at the composition boundary;
3. define an explicit receiver-independent function that accepts the required capability as an argument.

Binding an entire service graph or converting every method into an arrow field is broad and changes allocation, inheritance, and testing surfaces.

### D — lying proxy

The invariant protects non-configurable target facts. Legal redaction uses a separate view object, a plain snapshot containing only approved fields, or a proxy over a target whose relevant properties remain configurable and whose contract permits omission. Weakening target invariants merely to permit a deceptive trap damages the product.

### E — clone identity collapse

First traverse source nodes and allocate a new domain ID for every source ID. Then reconstruct each new live node through a legitimate factory. Finally connect parent/child relationships using the map and copy only approved attributes. Preserve internal sharing deliberately and decide how references to nodes outside the subtree behave. A general structural clone cannot make these product decisions.

### F — finalizer as correctness

Finalizers are delayed, optional, and not ordered as application cleanup. The live counter can remain inflated indefinitely. Open must return an explicit lease/session whose close or dispose operation decrements exactly once. A finalizer may log leaked sessions as a diagnostic fallback, but correctness cannot depend on it.

## Part IV — SceneGraph evaluation

A strong product:

- uses one authority for structural mutation;
- constructs branded nodes legitimately;
- persists plain data with a version tag;
- makes traversal order deterministic;
- rejects cycles and duplicate IDs;
- uses a source-to-clone map;
- confines proxy authority to plain draft data;
- closes sessions explicitly;
- tests descriptors, brands, traversal, cloning, persistence, and process behavior.

Reject designs that persist class instances directly, expose public mutable child arrays, treat symbols as secret, or use finalizers as the only cleanup route.

## Part V — Alias extension standard

A principled implementation establishes one atlas-owned alias index. Node state may expose an immutable alias view, but only atlas operations may add or remove aliases because uniqueness is global. Loading reconstructs the index after validating all records. V1 may decode with empty aliases while canonical writes move to a documented V2 format.

Subtree cloning requires a policy. A defensible default does not copy globally unique aliases automatically; alternatively, it accepts an explicit alias-remapping function and validates the complete candidate before publication. Debug and traversal views may include aliases, while persistence writes plain arrays in deterministic order.

The transition must be failure-atomic: duplicate or invalid aliases do not partially update either node state or the global index.

## Part VI — Oral-defense standard

The answer should describe mechanisms and product consequences, not recite syntax. It must keep live instances, plain records, protocol views, and persisted data separate. It must name explicit owners for graph mutation, edit publication, storage replacement, iterator state, and cleanup. Compatibility discussion should include runtime property shape and behavior, not only TypeScript declarations.
