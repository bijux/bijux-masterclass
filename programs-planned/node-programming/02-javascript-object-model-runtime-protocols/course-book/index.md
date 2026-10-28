# Course 2 — JavaScript Object Model and Runtime Protocols

## Properties, prototypes, classes, iteration, reflection, and object lifecycles

Course 1 taught you to build complete strict-TypeScript programs. Course 2 teaches what those programs are made of at runtime when their values are objects.

A JavaScript object is not merely a dictionary and a class is not merely a familiar spelling of a class from another language. Property access may traverse a prototype chain. A write may create an own property, invoke an inherited setter, or fail. A method receives a `this` value because of how it is called, not because of where it was written. A class method is a prototype property. A private field is enforced by a private brand, not by a TypeScript visibility annotation. An iterator is a stateful protocol object. A proxy can intercept operations but cannot lie about non-configurable facts. A clone may copy data while losing prototypes, descriptors, symbols, accessors, and identity relationships.

These mechanisms matter in ordinary Node.js products. They shape package APIs, domain models, debuggers, serializers, caches, plugin systems, resource wrappers, command registries, and long-lived object graphs.

> **Governing question:** How do JavaScript objects acquire state and behavior, participate in runtime protocols, preserve or hide identity, and remain correct across reflection, copying, persistence, and cleanup?

## The ten-module progression

| Module | Governing problem | Independent laboratory | ObjectAtlas increment |
|---:|---|---|---|
| 11 | Which property exists, where, with which attributes, and who can observe it? | Descriptor-Safe Settings | Node shell and stable property contracts |
| 12 | How does lookup traverse prototypes and preserve the original receiver? | Prototype-Based Policy Catalog | Node kinds and inherited policy behavior |
| 13 | What determines `this`, callability, constructibility, and `new`? | Receiver-Safe Command Adapter | Bound command surface and factory boundary |
| 14 | How do classes initialize public, private, and inherited state? | Private Counter Bank | Branded node instances and legal construction |
| 15 | How should independent behaviors and authorities be composed? | Capability-Composed Document | Atlas, node, codec, store, and renderer boundaries |
| 16 | How do symbol-keyed protocols connect objects to the language and Node? | Protocol-Aware Value Object | primitive conversion, tags, and custom inspection |
| 17 | How do stateful traversals produce values, stop, close, and detect mutation? | Hierarchy Walker | preorder, postorder, and breadth-first traversal |
| 18 | How can operations be reflected or intercepted without breaking invariants? | Transactional Draft Proxy | attribute edit sessions and revocable drafts |
| 19 | What survives copying, what remains reachable, and who owns cleanup? | Graph Snapshot and Lease | subtree cloning, snapshots, and session disposal |
| 20 | Can the whole object architecture survive an unseen cross-layer change? | Object-Model Audit | complete library, CLI, and independent alias feature |

The sequence is causal:

```text
property semantics
        ↓
prototype lookup
        ↓
invocation and construction
        ↓
class and private initialization
        ↓
composition and authority
        ↓
runtime protocols
        ↓
stateful traversal
        ↓
reflection and interception
        ↓
copying and lifecycle
        ↓
whole-product change
```

## How to study each module

1. Read the authoritative chapter without immediately running every example.
2. Write the module's model table: descriptor, lookup, call, initialization, authority, protocol, iterator, proxy, graph, or architecture.
3. Predict all eight investigations before using TypeScript or Node.
4. Diagnose every incorrect prediction by phase and causal rule.
5. Complete the focused workbook exercises.
6. Build the independent laboratory from its starter contract.
7. Transfer the mechanism into ObjectAtlas.
8. Compare with the reference only after producing a working attempt.
9. Reconstruct the central model without notes.

Compilation is not the only success criterion. Some weak designs compile while invoking getters unexpectedly, losing descriptors, binding the wrong receiver, producing nondeterministic traversal, leaking proxy authority, duplicating identity, or relying on garbage collection for correctness. Your explanation must cover the product contract, not only the checker.

## The four identities you must keep separate

This course repeatedly distinguishes:

- **domain identity** — the stable identifier used by product rules;
- **object identity** — reference equality of one live JavaScript object;
- **prototype identity** — membership in a delegation or constructor lineage;
- **persisted identity** — the representation stored and reconstructed later.

Private-brand membership is a fifth related fact. It answers whether an object was legitimately initialized by the declaring class, not whether its prototype currently points to that class's prototype.

Many object-model bugs are identity collapses. A plain decoded record is treated as a live class instance. A proxy is treated as its target. A clone is assumed to preserve external references. A domain ID is assumed to imply reference equality. The course trains you to name the identity that each operation preserves.

## ObjectAtlas

ObjectAtlas is a persistent component graph. It stores nodes with stable IDs, kinds, labels, attributes, ordered parent/child relationships, and runtime-only metadata. It provides deterministic traversal, descriptor-safe inspection, protocol-aware rendering, transactional attribute edits, subtree cloning, and versioned persistence.

ObjectAtlas is not designed to maximize advanced syntax. Plain records remain plain. Ordinary functions remain functions. Symbols, generators, proxies, private fields, and explicit cleanup appear only where their semantics improve the product.

Read [the ObjectAtlas engineering guide](capstone.md) before Module 11, then return to the relevant increment each day.

## Completion standard

Course completion requires more than reading all pages. You should be able to:

- classify an object operation as own-property, prototype, receiver, call, construction, protocol, iteration, reflection, clone, or lifecycle behavior;
- predict both TypeScript and runtime outcomes;
- inspect unfamiliar values without triggering hidden effects accidentally;
- repair object-model defects without replacing the requirement with a cast, spread copy, arrow function, bound wrapper, JSON round trip, or catch-all proxy;
- construct all ten laboratories;
- extend ObjectAtlas across domain, runtime, persistence, rendering, tests, and CLI layers;
- defend why each chosen mechanism is simpler and safer than the alternatives.

Continue with [outcomes](outcomes.md), then [the ten-day study plan](study-plan.md).
