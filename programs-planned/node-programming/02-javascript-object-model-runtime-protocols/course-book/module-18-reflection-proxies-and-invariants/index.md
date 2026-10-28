# Module 18 — Reflection, Proxies, and Meta-Object Invariants

> **Question:** Which object operation is being reflected or intercepted, what receiver and descriptor constraints must be preserved, and where does a proxy cease to be transparent?

## Why this comes now

Modules 11–17 built the object model from ordinary operations: properties, prototypes, calls, construction, classes, symbols, and iteration. Reflection exposes those operations as functions. Proxies interpose on them through traps. This is JavaScript’s runtime meta-object protocol.

That power is easy to misuse. A proxy can validate writes, implement virtual properties, trace access, revoke a capability, or adapt a foreign object. It can also violate assumptions about identity, private fields, method receivers, descriptors, enumeration, performance, and debugging. The language enforces invariants so a proxy cannot report impossible states for non-configurable properties or non-extensible targets.

ObjectAtlas uses one proxy-backed draft surface over a plain attribute record. It does not proxy `AtlasNode` instances. The draft records proposed changes and validates them before commit. The proxy is an interaction tool, not the source of truth and not a security sandbox.

## Outcomes

By the end of this module, you can:

- use `Reflect` methods as operation-shaped alternatives to syntax;
- distinguish target, handler, receiver, and proxy identity;
- implement `get`, `set`, `defineProperty`, `deleteProperty`, `ownKeys`, and `getOwnPropertyDescriptor` traps coherently;
- preserve accessor receiver behavior with reflective forwarding;
- explain the proxy invariants enforced around non-configurable properties and non-extensible targets;
- identify private-field incompatibility and method-binding trade-offs;
- use revocable proxies as lifecycle capabilities without treating revocation as resource cleanup;
- design proxy-backed validation without allowing alternate operations to bypass it;
- explain why a proxy is not a security sandbox;
- decide when explicit methods are clearer than interception.

## 1. Reflection turns syntax-level operations into functions

The `Reflect` object provides methods aligned with object internal operations:

```ts
Reflect.get(target, key, receiver);
Reflect.set(target, key, value, receiver);
Reflect.has(target, key);
Reflect.deleteProperty(target, key);
Reflect.defineProperty(target, key, descriptor);
Reflect.getOwnPropertyDescriptor(target, key);
Reflect.ownKeys(target);
Reflect.getPrototypeOf(target);
Reflect.setPrototypeOf(target, prototype);
Reflect.isExtensible(target);
Reflect.preventExtensions(target);
Reflect.apply(functionValue, receiver, args);
Reflect.construct(constructor, args, newTarget);
```

Reflective operations are not “more powerful syntax.” Their value is explicit operands and consistent result shapes. For example, `Reflect.defineProperty` returns a Boolean instead of throwing for ordinary rejection.

```ts
const target = Object.preventExtensions({});
const accepted = Reflect.defineProperty(target, 'x', { value: 1 });
console.log(accepted); // false
```

Use reflection when the operation itself is data-driven or must be forwarded. Prefer ordinary syntax when it communicates intent more directly.

## 2. A proxy has target, handler, and distinct identity

```ts
const target = { count: 1 };
const handler: ProxyHandler<typeof target> = {};
const proxy = new Proxy(target, handler);

console.log(proxy === target); // false
```

The proxy is a different object identity. Operations on the proxy may invoke traps. Operations on the target bypass the proxy.

This has immediate consequences:

- a `WeakMap` keyed by target does not recognize proxy;
- equality checks differ;
- listener or registry identity differs;
- direct target references can bypass validation or logging;
- private brands belong to the target, not automatically to the proxy;
- wrapping the same target twice creates two proxies.

If the proxy is intended as the only mutation surface, do not leak the target to untrusted callers.

## 3. The `get` trap and receiver preservation

A basic forwarding handler is:

```ts
const proxy = new Proxy(target, {
  get(current, key, receiver) {
    return Reflect.get(current, key, receiver);
  },
});
```

Why pass `receiver`? Because an accessor found on `current` or its prototype should run with the original receiver used by the operation.

```ts
const base = {
  get doubled(): number {
    return Number(Reflect.get(this, 'value')) * 2;
  },
};
const target = Object.create(base) as { value: number; readonly doubled: number };
target.value = 3;
const proxy = new Proxy(target, {
  get(current, key, receiver) {
    return Reflect.get(current, key, receiver);
  },
});
```

`proxy.doubled` uses `proxy` as receiver. A different forwarding choice, `Reflect.get(current, key, current)`, changes accessor behavior.

There is no universally transparent choice because private fields introduce a competing requirement.

## 4. Private fields break transparent forwarding

```ts
class Counter {
  #value = 0;

  increment(): number {
    this.#value += 1;
    return this.#value;
  }
}

const target = new Counter();
const proxy = new Proxy(target, {});
// proxy.increment() can fail: method receives proxy as this, and proxy lacks Counter's private brand
```

A handler may bind methods to the target:

```ts
get(current, key, receiver) {
  const value = Reflect.get(current, key, receiver);
  return typeof value === 'function' ? value.bind(current) : value;
}
```

This repair has costs:

- each read can create a new bound function identity unless cached;
- accessors still have receiver questions;
- methods intentionally expecting a derived receiver are changed;
- `this` becomes the target even when called through another inheriting object;
- method metadata and listener removal behavior change.

Therefore ObjectAtlas does not proxy class instances. It proxies plain draft records whose behavior is defined entirely by the handler.

## 5. `set` and `defineProperty` can interact

A `set` trap that forwards through `Reflect.set` may trigger property definition behavior involving the proxy receiver. Depending on the target descriptor and receiver, the proxy’s `defineProperty` trap can also be involved.

```ts
const events: string[] = [];
const target: Record<string, unknown> = {};
const proxy = new Proxy(target, {
  set(current, key, value, receiver) {
    events.push(`set:${String(key)}`);
    return Reflect.set(current, key, value, receiver);
  },
  defineProperty(current, key, descriptor) {
    events.push(`define:${String(key)}`);
    return Reflect.defineProperty(current, key, descriptor);
  },
});

proxy.name = 'atlas';
```

Do not assume each source assignment maps to exactly one trap. The internal operation graph matters.

A validation proxy must cover every mutation path it intends to constrain:

- assignment;
- `Object.defineProperty`;
- `Reflect.defineProperty`;
- deletion;
- prototype changes;
- mutation through nested object references;
- direct target access.

Intercepting only `set` is not a complete object invariant.

## 6. Trap return values are part of strict-mode behavior

`set`, `deleteProperty`, `defineProperty`, `setPrototypeOf`, and `preventExtensions` traps return Booleans.

```ts
const proxy = new Proxy({}, {
  set(): boolean {
    return false;
  },
});

proxy.value = 1; // throws in strict ESM code
```

A handler that forgets to return the forwarding result returns `undefined`, which is falsy and may cause a TypeError.

Use the `Reflect` result and propagate it unless the handler has a deliberate different contract permitted by invariants.

## 7. Proxy invariants prevent impossible reports

A proxy cannot report arbitrary facts when the target has non-configurable properties or is non-extensible.

Example: if the target owns a non-configurable key, `ownKeys` cannot omit it.

```ts
const target = {};
Object.defineProperty(target, 'fixed', {
  value: 1,
  configurable: false,
});

const proxy = new Proxy(target, {
  ownKeys(): PropertyKey[] {
    return [];
  },
});

// Reflect.ownKeys(proxy) throws TypeError
```

If the target is non-extensible, `ownKeys` must report exactly the target’s own keys, without extras or omissions. Duplicate keys are always invalid.

Similarly, a proxy cannot claim that a non-configurable property does not exist or report a descriptor incompatible with the target’s permanent state.

These are language-enforced consistency constraints, not style recommendations.

## 8. Coherent virtual properties require several traps

Suppose a proxy exposes a virtual `fullName` derived from `first` and `last`. If `get` reports it but `has`, `ownKeys`, and `getOwnPropertyDescriptor` do not, consumers observe inconsistent surfaces.

A coherent design must decide:

- is the virtual property own or inherited?
- is it enumerable?
- is it configurable?
- can it be assigned?
- does `in` report it?
- does spread include it?
- does JSON include it?
- can it be deleted?

For most application logic, an explicit getter on a class or plain object is clearer. Proxies are justified when the property set is dynamic or the object adapts another runtime surface.

## 9. `deleteProperty` and tombstone policy

A draft proxy may treat deletion as a proposed change rather than immediate mutation:

```ts
const deleted = new Set<PropertyKey>();

const handler: ProxyHandler<Record<PropertyKey, unknown>> = {
  deleteProperty(_target, key): boolean {
    deleted.add(key);
    return true;
  },
};
```

The complete design must define:

- whether deleting a missing key is accepted;
- whether required keys can be deleted;
- whether deletion is visible to reads before commit;
- how repeated delete/set operations resolve;
- whether symbol keys are allowed;
- how nested objects are handled;
- what happens after rollback or commit.

A transaction is a state machine. The proxy syntax is only one interface to it.

## 10. Revocable proxies model capability expiry

`Proxy.revocable` returns a proxy and a revoke function:

```ts
const { proxy, revoke } = Proxy.revocable(
  { value: 1 },
  {},
);

console.log(proxy.value); // 1
revoke();
// proxy.value throws TypeError
```

Revocation invalidates future operations through that proxy. It does not:

- destroy the target;
- remove other references to the target;
- close files or sockets;
- undo earlier mutations;
- revoke nested objects already extracted;
- guarantee garbage collection.

Use revocation as a capability-lifecycle tool. Resource cleanup remains an explicit resource obligation.

ObjectAtlas revokes a draft proxy after commit or rollback so callers cannot keep mutating the completed transaction surface.

## 11. Proxies are not security sandboxes

A proxy can restrict operations performed through that proxy reference. It cannot make arbitrary JavaScript code safe.

Untrusted code may still:

- consume CPU or memory;
- access globals and imported modules;
- retain nested references;
- exploit target references leaked elsewhere;
- use reflection against exposed values;
- trigger getters and callbacks;
- perform I/O through other capabilities.

Security requires a threat model and stronger isolation such as a separate process, restricted runtime, or carefully controlled VM context—topics reserved for later courses.

A read-only proxy is an API aid, not a hostile-code boundary.

## 12. Proxy performance and debuggability

Proxy traps add indirection to fundamental operations. Runtime optimizers may have fewer assumptions, and debugging stack traces can point into handlers rather than domain operations.

Before using a proxy in a hot or broad object surface:

- measure the representative workload;
- keep handler behavior deterministic;
- avoid per-read allocation such as uncached `bind`;
- expose explicit diagnostic state;
- provide named operations for consequential mutations;
- ensure errors name the domain rule, not only “proxy trap failed.”

Course 9 will treat performance evidence systematically. Here the design rule is: do not intercept every property operation when three explicit methods would be clearer.

## 13. A transactional draft proxy

ObjectAtlas attribute edits use a plain draft model:

```text
base snapshot
    ↓
change map + deletion set
    ↓
proxy read surface
    ↓
validate complete candidate
    ↓
commit or rollback
    ↓
revoke proxy
```

The proxy does not mutate the live node. It records proposed top-level attribute changes. Commit constructs a plain candidate record, validates key and value policy, then asks the node to publish the new attributes in one operation.

Nested mutable values are not exposed. Attribute values are restricted to immutable JSON-like primitives and recursively frozen snapshots. This prevents a caller from extracting a nested object and bypassing the proxy.

The session state is:

```text
open → committed
open → rolled-back
```

Operations after either terminal state fail.

## 14. Reflective inspection must avoid accidental execution

A meta-object inspector should use:

- `Reflect.ownKeys`;
- `Object.getOwnPropertyDescriptor`;
- `Object.getPrototypeOf`;
- explicit proxy-awareness only where Node’s debugging APIs permit it;
- bounded depth and key count.

It should not read every property value. Getters and proxies can execute arbitrary code.

ObjectAtlas `inspect` reports descriptors and prototype names. It reads domain values only through trusted public methods after the instance has been validated.

## 15. ObjectAtlas increment

Implement `AttributeEditSession`:

- created from an immutable attribute snapshot;
- exposes a revocable proxy over a plain draft surface;
- supports top-level string keys matching the atlas key grammar;
- rejects symbols and structural names;
- validates values as JSON-safe, bounded data;
- tracks set and delete operations deterministically;
- constructs and validates the complete candidate before commit;
- publishes once through a node method;
- supports rollback;
- revokes the proxy after commit or rollback;
- implements idempotent explicit close/rollback behavior;
- never proxies `AtlasNode` itself.

Tests must cover assignment, `defineProperty`, deletion, duplicate edits, invalid nested values, direct target isolation, post-revocation access, commit failure, rollback, and private-field compatibility.

## Common wrong models

### “A proxy changes the target’s identity”

The proxy is a separate identity that forwards or intercepts operations on the target.

### “An empty handler is perfectly transparent”

Private fields, equality, weak collections, and identity-sensitive APIs distinguish proxy from target.

### “Intercepting `set` validates all writes”

Definition, deletion, nested mutation, direct target access, and prototype changes are separate paths.

### “A trap can report any virtual shape”

Proxy invariants constrain keys, descriptors, extensibility, and permanent target state.

### “Revocation cleans up the target”

It disables operations through one proxy. It does not release unrelated resources or references.

### “A read-only proxy safely runs untrusted plugins”

It limits one reference surface. It is not process isolation.

## Practice sequence

1. Rewrite property operations with corresponding `Reflect` calls.
2. Trace receiver behavior through a forwarding `get` trap.
3. Demonstrate private-field failure through a proxy.
4. Trigger and explain an `ownKeys` invariant violation.
5. Build a coherent virtual property or decide an explicit getter is clearer.
6. Complete the Transactional Draft Proxy laboratory.
7. Implement ObjectAtlas edit sessions and revocation.
8. Defend why the atlas proxies plain drafts but not nodes.

## Ready to continue

Continue when you can list every mutation path relevant to a proxy-backed invariant and explain the target state that constrains each trap. You must be able to separate capability revocation from resource cleanup and proxy identity from target identity.

Module 19 studies object graphs, cloning, weak reachability, and deterministic cleanup. Those concerns determine what happens to targets, proxies, iterators, and sessions after ordinary references disappear.

## Primary references

- ECMAScript Language Specification: Proxy exotic objects, trap invariants, and Reflect operations.
- TypeScript standard library: `ProxyHandler`, `ProxyConstructor`, and reflective types.
- Node.js `util.inspect` documentation: proxy inspection and the warning that inspection output is not a stable program format.

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory 18 — Transactional Draft Proxy](../../labs/module-18-transactional-draft-proxy/README.md)
- [ObjectAtlas engineering guide](../capstone.md)
