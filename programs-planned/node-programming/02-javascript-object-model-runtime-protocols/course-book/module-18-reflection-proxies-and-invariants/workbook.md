# Module 18 Workbook

For each proxy design, list all relevant internal operations. A handler that discusses only `get` and `set` is usually incomplete.

## A. Reflect equivalence

Rewrite these with `Reflect` and state any return-value difference:

```ts
object[key]
object[key] = value
key in object
delete object[key]
fn.call(receiver, left, right)
new Constructor(left, right)
Object.defineProperty(object, key, descriptor)
```

Explain when the Boolean result from a reflective operation must be checked.

## B. Receiver forwarding

Create a prototype getter that reads receiver state. Compare these proxy handlers:

```ts
Reflect.get(target, key, receiver)
Reflect.get(target, key, target)
```

Then proxy a class with a private field. Explain why neither forwarding policy is universally transparent.

## C. Invariant failures

Construct and explain TypeErrors for:

- omitting a non-configurable key from `ownKeys`;
- adding an extra key to a non-extensible target;
- reporting a configurable descriptor for a non-configurable target property;
- returning duplicate keys;
- claiming successful deletion of a non-configurable property.

For each, name the target fact that constrains the proxy report.

## D. Complete validation surface

A proxy validates assignments but ignores `defineProperty`, delete, and nested mutation. Create bypasses for each. Then design either:

- a complete top-level immutable-value draft protocol;
- explicit named mutation methods without a proxy.

Defend the simpler correct design.

## E. Revocation semantics

Use `Proxy.revocable` and retain:

- the target;
- the proxy;
- a nested object extracted before revocation;
- a bound method extracted before revocation.

After revocation, test each reference. Explain exactly what revocation did and did not invalidate.

## F. Inspector design

Build a bounded inspector that reports:

- own keys;
- descriptor kind and flags;
- prototype-chain constructor names;
- whether the object is extensible, sealed, or frozen.

It must not invoke getters. Explain the remaining risk from proxy traps even when using reflective operations.

## G. Independent laboratory

Complete [Transactional Draft Proxy](../../labs/module-18-transactional-draft-proxy/README.md). It requires complete top-level mutation coverage, candidate validation, revocation, deterministic change logs, and no proxying of private-field class instances.

## H. ObjectAtlas transfer

Implement attribute edit sessions. Prove:

- live node state is unchanged before commit;
- invalid candidate state does not publish;
- assignment, definition, and deletion share one validation policy;
- nested bypass is impossible under the value grammar;
- proxy access fails after terminal state;
- rollback is idempotent;
- no node instance is proxied.

## I. Reconstruction and defense

Without notes, explain:

- Reflect as operation-shaped functions;
- target, proxy, handler, receiver;
- private-field incompatibility;
- trap return values;
- key and descriptor invariants;
- virtual-property coherence;
- revocation limits;
- why proxies are not sandboxes;
- when explicit methods are better.
