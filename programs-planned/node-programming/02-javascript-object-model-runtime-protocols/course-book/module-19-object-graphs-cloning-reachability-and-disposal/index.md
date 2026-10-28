# Module 19 — Object Graphs, Cloning, Reachability, Weak References, and Disposal

> **Question:** Which identities must remain shared, which data may be copied, what keeps an object reachable, and which cleanup obligations must be completed explicitly rather than left to garbage collection?

## Why this comes now

The object model is not complete until identity and lifetime are considered across a graph. Prototypes, closures, iterators, proxies, maps, event listeners, and caches can all keep objects reachable. Copying one object may preserve nested aliases, discard prototypes, reject functions, or duplicate data while losing behavior. Weak references change reachability but do not create deterministic lifecycle events. Finalization can observe collection eventually, but cannot be used to protect correctness.

JavaScript uses garbage collection for memory. It does not automatically close application resources such as file handles, locks, subscriptions, transactions, or temporary directories at a predictable point. Explicit resource management protocols provide deterministic scope exit, while ordinary `close` methods and `try/finally` remain essential.

ObjectAtlas must distinguish three products:

- a live graph of branded class instances;
- a plain persistence record;
- an immutable snapshot for callers.

It also owns edit sessions that must terminate explicitly. Weak references are used only for optional caches and observation, never for graph correctness.

## Outcomes

By the end of this module, you can:

- draw strong reachability through objects, arrays, maps, closures, iterators, proxies, and listeners;
- distinguish shallow copy, descriptor-preserving clone, structured clone, JSON serialization, and domain reconstruction;
- explain how cycles affect copying and serialization;
- use memoization to clone graph structure without duplicating shared identities accidentally;
- state what `WeakMap`, `WeakSet`, `WeakRef`, and `FinalizationRegistry` do and do not guarantee;
- identify common memory-retention paths in Node.js applications;
- design idempotent `close` and `[Symbol.dispose]` protocols;
- use `try/finally` and `using`-style scope ownership without depending on finalization;
- decide which object lifecycle belongs to garbage collection and which belongs to application control;
- build ObjectAtlas snapshots and edit-session cleanup with explicit semantics.

## 1. Garbage collection follows reachability, not usefulness

An object is collectible when the runtime can no longer reach it from roots such as active execution state, modules, globals, native resources, or other reachable objects. “The program no longer needs it” is not enough if a reference remains.

```ts
const cache = new Map<string, object>();

function remember(id: string, value: object): void {
  cache.set(id, value);
}
```

Values remain strongly reachable through `cache` until entries are removed or the map itself becomes unreachable.

A reachability graph might be:

```text
module binding cache
        ↓
Map entry
        ↓
Atlas snapshot
        ↓
large attribute objects
```

To diagnose retention, follow reference edges. Do not reason from lexical scope alone; closures, listeners, timers, promises, maps, iterators, and native bindings may keep references alive.

## 2. Shallow copies preserve nested identities

Object spread, `Object.assign`, array spread, `slice`, and many collection conversions create a new outer container while copying contained values.

```ts
const original = {
  metadata: { revision: 1 },
};
const copy = { ...original };

console.log(copy !== original); // true
console.log(copy.metadata === original.metadata); // true
```

This can be the correct form of structural sharing. It is not a deep clone.

A copy review should record:

```text
new outer identity?
prototype preserved?
descriptors preserved?
symbols preserved?
non-enumerable properties preserved?
accessors executed or preserved?
nested identities shared or copied?
cycles supported?
functions supported?
resource handles duplicated or shared?
```

## 3. Descriptor-preserving shallow clones are runtime-surface clones

Module 11 built:

```ts
function cloneOwnSurface<T extends object>(source: T): T {
  return Object.create(
    Object.getPrototypeOf(source),
    Object.getOwnPropertyDescriptors(source),
  ) as T;
}
```

This preserves prototype and own descriptors without invoking getters. It still shares nested references and does not duplicate internal slots or private fields. Applying it to a class instance can produce an object with the same prototype but without legitimate private brand state.

Therefore this technique is suitable for selected ordinary objects whose semantics are fully represented by prototype and descriptors. It is not a universal instance clone.

## 4. JSON is a serialization format, not a graph clone

JSON supports a restricted data model. It does not preserve:

- custom prototypes or class identity;
- methods, symbols, or private fields;
- `Map`, `Set`, `Date`, `BigInt`, typed-array semantics, or `undefined` in general form;
- object identity sharing;
- cycles;
- descriptors;
- non-enumerable properties.

```ts
const shared = { value: 1 };
const source = { left: shared, right: shared };
const parsed = JSON.parse(JSON.stringify(source)) as {
  left: { value: number };
  right: { value: number };
};

console.log(parsed.left === parsed.right); // false
```

The alias relationship is lost.

JSON is appropriate for ObjectAtlas persistence because the storage schema deliberately contains plain acyclic data with explicit IDs representing graph relationships. It is not used to clone live nodes.

## 5. `structuredClone` copies supported structured data

The global `structuredClone` function supports cycles and preserves sharing within the cloned graph for supported types:

```ts
const shared = { value: 1 };
const source = { left: shared, right: shared };
const clone = structuredClone(source);

console.log(clone.left === clone.right); // true
console.log(clone.left !== shared);      // true
```

It supports several built-in structured types and can transfer selected transferable objects when requested.

Important limitations for this course:

- functions cannot be cloned;
- weak collections cannot be cloned;
- custom class prototypes and methods are not reconstructed as live domain instances in Node’s ordinary structured-clone behavior;
- property descriptors are not a general preservation contract;
- private fields are not recreated through public object shape;
- resource handles need specific transfer support or cannot be cloned.

Use it for supported data graphs, not for duplicating arbitrary application objects.

## 6. Domain cloning should follow domain identity

A graph clone may need new stable identifiers, preserved internal sharing, and rewritten edges.

For an ObjectAtlas subtree clone:

1. collect the source nodes in deterministic traversal order;
2. allocate and validate all new IDs before mutation;
3. create a source-ID to target-ID mapping;
4. clone node data into plain candidates;
5. rewrite parent and child references through the mapping;
6. validate the complete candidate subtree;
7. publish all nodes as one graph transition.

This is not equivalent to cloning object memory. It is a domain transformation with identity policy.

A weak repair calls `structuredClone` on live instances and then changes prototypes. That loses private state and does not establish graph invariants.

## 7. Graph cloning needs memoization

A generic graph copy must preserve cycles and shared substructure. The usual algorithm stores a mapping from source object identity to clone identity before recursively copying children.

```ts
function clonePlainGraph<T extends object>(source: T): T {
  const seen = new WeakMap<object, object>();

  function clone(value: unknown): unknown {
    if (value === null || typeof value !== 'object') {
      return value;
    }

    const existing = seen.get(value);
    if (existing !== undefined) {
      return existing;
    }

    if (Array.isArray(value)) {
      const result: unknown[] = [];
      seen.set(value, result);
      for (const item of value) {
        result.push(clone(item));
      }
      return result;
    }

    const result = Object.create(null) as Record<PropertyKey, unknown>;
    seen.set(value, result);
    for (const key of Reflect.ownKeys(value)) {
      const descriptor = Object.getOwnPropertyDescriptor(value, key);
      if (descriptor === undefined || !('value' in descriptor)) {
        throw new TypeError('accessor properties are not supported');
      }
      result[key] = clone(descriptor.value);
    }
    return result;
  }

  return clone(source) as T;
}
```

This example deliberately supports only a narrow plain-data contract. A general clone must define prototypes, descriptors, built-ins, symbols, accessors, transferables, and resources. That complexity is why domain-specific copying is usually preferable.

## 8. `WeakMap` and `WeakSet` avoid strong key retention

A `WeakMap` associates data with object keys without keeping those keys strongly reachable solely because of the mapping.

```ts
const metadata = new WeakMap<object, { inspected: number }>();
```

Limitations are part of the design:

- keys must be objects or non-registered symbols under current language rules, depending on runtime support;
- entries are not enumerable;
- size is not observable;
- collection timing is not observable reliably;
- values can still retain other objects strongly;
- a reachable key keeps its associated value reachable through the weak map.

Weak collections are useful for per-object metadata and memoization that should not extend key lifetime. They are not suitable when the application must list, count, persist, or explicitly evict entries.

ObjectAtlas may use a `WeakMap<AtlasNode, InspectionCache>` for optional derived diagnostic data. Correctness never depends on the cache existing.

## 9. `WeakRef` is an observation tool with unstable availability

A `WeakRef` can be dereferenced to obtain the target if it has not been collected:

```ts
const reference = new WeakRef(object);
const current = reference.deref();
```

The target may be present now and absent later. Code must hold a strong local reference while using the result.

Weak references are difficult to test deterministically because collection timing is implementation-controlled. They should not determine whether a required event occurs or whether a resource is released.

Suitable uses are narrow caches where recomputation is correct. Unsuitable uses include ownership registries, subscription cleanup, file closing, transaction rollback, and user-visible liveness.

## 10. `FinalizationRegistry` is not deterministic cleanup

A finalization registry can request a callback after a registered target becomes unreachable and is collected. The callback may run much later or not before process exit.

Do not use finalizers to:

- close required resources;
- release locks promptly;
- commit or roll back transactions;
- send network protocol messages;
- decrement authoritative counters;
- make tests pass;
- preserve security boundaries.

Finalization can support diagnostics or best-effort native-resource backup when an explicit close path already exists. The held value must not keep the target alive indirectly.

The rule is:

> Garbage collection may reclaim memory. Application correctness requires deterministic ownership of non-memory resources.

## 11. Common retention paths in Node.js

Objects can remain reachable through:

- module-level maps and arrays;
- event listeners on long-lived emitters;
- timers and intervals;
- unresolved promises and captured closures;
- queued callbacks;
- async iterators and suspended generators;
- caches without eviction;
- bound functions retaining their receiver;
- proxy handlers retaining targets;
- test globals;
- child process or stream callbacks;
- diagnostic contexts.

A retention investigation should ask:

1. What root remains reachable?
2. Which edge leads to the unexpected object?
3. Who owns removal of that edge?
4. Is removal tied to a deterministic lifecycle event?
5. Can a bounded cache or weak association express the real requirement?

## 12. Explicit close is a state transition

A resource-owning class should define states and idempotency:

```ts
class Lease {
  #closed = false;

  use(): void {
    if (this.#closed) {
      throw new Error('lease is closed');
    }
  }

  close(): void {
    if (this.#closed) {
      return;
    }
    this.#closed = true;
    // release resource exactly once
  }
}
```

Questions:

- Is `close` idempotent?
- Can it fail?
- What state follows failure?
- Are operations rejected after close?
- Does close release nested resources in reverse order?
- Who calls close on partial construction failure?
- Is asynchronous cleanup required?

A destructor-like method with unspecified state is not enough.

## 13. `Symbol.dispose` and `using`

The explicit resource-management protocol associates synchronous cleanup with `Symbol.dispose`. TypeScript can compile `using` declarations according to the configured target and runtime support.

```ts
class EditLease implements Disposable {
  #closed = false;

  [Symbol.dispose](): void {
    if (!this.#closed) {
      this.#closed = true;
      this.rollback();
    }
  }

  private rollback(): void {
    // discard uncommitted candidate
  }
}
```

Conceptual use:

```ts
{
  using lease = openLease();
  // scope owns cleanup
}
```

The cleanup protocol does not make an object collectible and does not replace error design. If body execution and disposal both fail, the language represents both failures through suppression semantics. Readers must understand that cleanup can itself fail.

For broad compatibility, ObjectAtlas also exposes an explicit `close()`/`rollback()` method. Its `Symbol.dispose` method delegates to the same idempotent state transition.

## 14. Resource stacks and reverse-order cleanup

When several resources are acquired, cleanup usually happens in reverse acquisition order:

```text
acquire A
acquire B
acquire C
work
release C
release B
release A
```

This preserves nesting assumptions: C may depend on B, and B may depend on A.

A small manual stack can register cleanup actions immediately after each successful acquisition. If a later acquisition fails, the stack releases earlier resources.

Do not wait until the end to record cleanup. Partial construction paths are where leaks occur.

## 15. ObjectAtlas increment

Add two lifetime features.

### Subtree snapshots

- clone through explicit node records and ID remapping;
- preserve child order;
- allocate all destination IDs before publication;
- reject collisions and cycles before changing the atlas;
- publish the complete cloned subtree atomically;
- never clone live instances with spread, JSON, or prototype replacement.

### Edit-session disposal

- session states are open, committed, or rolled back;
- `commit` and `rollback` are terminal;
- `close` and `[Symbol.dispose]` roll back an open session and are idempotent;
- terminal sessions release references to large base snapshots and change maps;
- correctness does not depend on `FinalizationRegistry`;
- an optional weak diagnostic registry may observe abandoned sessions but cannot perform required rollback.

Tests must prove alias preservation within snapshots, new identity across snapshots, failure atomicity, explicit cleanup, reverse-order cleanup for nested sessions where supported, and no dependence on forced garbage collection.

## Common wrong models

### “Out of scope means collectible”

Closures, maps, listeners, iterators, and native bindings can retain the object.

### “Deep clone is one universal operation”

Different mechanisms preserve different data, identity, prototype, descriptor, and resource semantics.

### “Structured clone recreates my class instance”

It copies supported structured data; custom live class invariants require domain reconstruction.

### “Weak references tell me when an object dies”

Availability and finalization timing are nondeterministic.

### “The garbage collector closes resources”

It reclaims memory. Application resources require explicit deterministic lifecycle.

### “A dispose method can be called twice safely by default”

Idempotency and failure state must be designed and tested.

## Practice sequence

1. Draw a reachability path through a listener, bound method, and instance.
2. Compare four clone mechanisms against one requirement ledger.
3. Implement a cycle-preserving narrow graph copy with memoization.
4. Build a weak metadata cache and explain why it cannot report size.
5. Demonstrate explicit cleanup with `try/finally` and `[Symbol.dispose]`.
6. Complete the Graph Snapshot and Lease laboratory.
7. Add ObjectAtlas subtree cloning and session disposal.
8. Defend every place the capstone uses strong, weak, or explicit lifetime management.

## Ready to continue

Continue when you can trace why an object remains reachable and can state exactly what each copy mechanism preserves. You must also be able to explain why memory reclamation and application resource cleanup are different responsibilities.

Module 20 integrates the entire object model into a public architecture and requires an independent change that crosses descriptors, prototypes, protocols, traversal, reflection, persistence, and lifecycle.

## Primary references

- ECMAScript Language Specification: structured clone integration points where applicable, weak references, finalization, symbols for disposal, and suppressed errors.
- Node.js global APIs: `structuredClone`, weak-reference support, and resource APIs with explicit close behavior.
- TypeScript library and release documentation for `Disposable`, `Symbol.dispose`, and `using` declarations.

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory 19 — Graph Snapshot and Lease](../../labs/module-19-graph-snapshot-and-lease/README.md)
- [ObjectAtlas engineering guide](../capstone.md)
