# Course 2 Reference Desk

Use this desk after learning the models in the chapters. It condenses decisions; it does not replace the explanations.

## 1. Property descriptor matrix

### Data descriptor

```ts
interface DataDescriptor {
  value?: unknown;
  writable?: boolean;
  enumerable?: boolean;
  configurable?: boolean;
}
```

### Accessor descriptor

```ts
interface AccessorDescriptor {
  get?: (() => unknown) | undefined;
  set?: ((value: unknown) => void) | undefined;
  enumerable?: boolean;
  configurable?: boolean;
}
```

A descriptor cannot be both data and accessor. Omitted fields in `Object.defineProperty` default to `false` or `undefined`, not to assignment-like attributes.

| Operation | Own only | Strings | Symbols | Enumerable only | May invoke getter |
|---|---:|---:|---:|---:|---:|
| `Object.keys` | yes | yes | no | yes | no |
| `Object.getOwnPropertyNames` | yes | yes | no | no | no |
| `Object.getOwnPropertySymbols` | yes | no | yes | no | no |
| `Reflect.ownKeys` | yes | yes | yes | no | no |
| `for...in` | no | yes | no | yes | no for names; later read may |
| object spread | yes | yes | yes | yes | yes |
| `JSON.stringify` | own string properties | yes | no | yes | yes |

For effect-free inspection, obtain descriptors rather than values.

## 2. Prototype lookup ledger

For `receiver[key]`:

1. begin at the receiver;
2. ask the current object for its own descriptor;
3. if data property, return its value;
4. if accessor, call the getter with the original receiver;
5. otherwise continue at the prototype;
6. stop at `null` and return `undefined`.

For writes, distinguish:

- existing own writable data property;
- existing own setter;
- inherited setter;
- inherited non-writable data property;
- absent property on an extensible receiver;
- absent property on a non-extensible receiver.

Do not use `in` when the policy requires own input. Prefer `Object.hasOwn(value, key)`.

## 3. Call and construction matrix

| Form | `this` source | Constructible? | Notes |
|---|---|---:|---|
| `obj.method()` | base object `obj` | depends on function | property reference matters |
| `const f = obj.method; f()` | `undefined` in modules/strict mode | depends | receiver lost |
| `f.call(x, a)` | explicit `x` | call only | `call` itself does not construct |
| `f.apply(x, args)` | explicit `x` | call only | array-like arguments |
| `f.bind(x, a)` | bound receiver and prefix args | mirrors target constructibility | bound `this` ignored by `new` |
| arrow function | lexical `this` | no | no own `arguments`, `prototype`, or `new.target` |
| `new F(a)` | newly created receiver | yes if F constructible | explicit object return may replace receiver |

TypeScript explicit `this` parameters are erased. They constrain static calls but do not create runtime binding.

## 4. Class initialization order

### Base construction

```text
allocate receiver
    ↓
install/initialize base instance fields in source order
    ↓
run base constructor body
    ↓
return receiver unless constructor returns another object
```

### Derived construction

```text
enter derived constructor without usable this
    ↓
call super(...)
    ↓
base construction completes and supplies receiver
    ↓
initialize derived fields in source order
    ↓
run remaining derived constructor body
```

Avoid calling overridable methods from constructors when derived state is not yet initialized.

JavaScript `#private` fields are private-brand checks at runtime. TypeScript `private` is primarily a static restriction and ordinarily emits a normal property.

## 5. Composition decision table

| Need | Prefer | Avoid when |
|---|---|---|
| behavior is substitutable and shares lifecycle | inheritance | only code reuse is desired |
| one object owns another capability | nested collaborator/forwarding | dependency authority is unclear |
| behavior needs hidden per-instance state | closure or private class field | many methods need awkward duplicated closure state |
| many constructors need one orthogonal behavior | carefully constrained mixin | method/state conflicts are unresolved |
| caller should receive least authority | narrow capability object/function | broad environment or service locator |
| one fixed pure transformation | ordinary function | object identity adds no value |

Always write the authority map before choosing syntax.

## 6. Symbol and protocol desk

| Protocol | Trigger | Contract |
|---|---|---|
| `Symbol.iterator` | `for...of`, spread, destructuring, `Array.from` | return iterator |
| `Symbol.asyncIterator` | `for await...of` | deferred to later async course |
| `Symbol.toPrimitive` | coercion | return primitive for hint |
| `Symbol.toStringTag` | `Object.prototype.toString` | tag string |
| `Symbol.hasInstance` | `instanceof` | customize instance test |
| `Symbol.species` | selected built-in derived construction | often unnecessary in application classes |
| `util.inspect.custom` | Node inspection | return debug representation |
| `Symbol.dispose` | explicit resource management | deterministic synchronous cleanup |
| `Symbol.asyncDispose` | async disposal | deferred to async lifecycle course |

Symbols prevent accidental string-key collisions. They do not create secrecy.

## 7. Iterator protocol

```ts
interface IteratorResult<T, TReturn = unknown> {
  done: boolean;
  value: T | TReturn;
}
```

A repeatable iterable creates a fresh iterator each time. An iterator may be iterable by returning itself from `[Symbol.iterator]()`, but it remains single-pass.

Design questions:

- snapshot or live traversal?
- stable source order?
- behavior under mutation?
- cycle handling?
- early-close behavior?
- error cleanup?
- whether values are borrowed live views or owned snapshots?

Generators simplify state machines but do not choose those policies for you.

## 8. Reflect and proxy desk

Prefer `Reflect.get(target, key, receiver)` inside a `get` trap when ordinary receiver-preserving semantics are intended. Similar `Reflect` methods exist for set, define, delete, construct, apply, own keys, and prototype operations.

A proxy must respect target invariants. Examples:

- non-configurable own properties cannot disappear from `ownKeys`;
- non-extensible targets cannot report extra own keys;
- a non-configurable, non-writable data property cannot report a different value;
- a non-configurable accessor without a getter must report `undefined`.

A proxy is a new identity. Private fields normally reject the proxy as receiver unless methods deliberately recover the target, which changes semantics and can leak authority. Prefer plain-data proxy boundaries.

## 9. Copy and clone matrix

| Mechanism | Own enumerable data | Symbols | Descriptors | Prototype | Accessors | Cycles/sharing | Domain invariants |
|---|---|---|---|---|---|---|---|
| spread/assign | copied by value read | enumerable symbols yes | no | no | invoked | shallow only | no |
| descriptor copy | configurable choice | yes | yes | optional | preserved | shallow only | no |
| `structuredClone` | supported data | symbol-keyed props generally not a domain contract | no | ordinary reconstructed objects | not preserved as accessors | yes | no |
| JSON round trip | JSON-compatible enumerable string data | no | no | no | invoked | no cycles; sharing lost | no |
| domain reconstruction | selected explicitly | selected explicitly | selected explicitly | selected explicitly | selected explicitly | explicit map | yes, if implemented correctly |

Use a source-to-clone identity map when graph sharing or cycles matter. Use an explicit domain-ID remapping table when cloned entities require new product identities.

## 10. Reachability and cleanup

Garbage collection answers whether an object remains strongly reachable, not when external resources are released. Weak references and finalizers cannot support correctness-critical cleanup because timing is unspecified and execution is not guaranteed.

Use explicit ownership and cleanup for files, handles, subscriptions, sessions, and locks. Make terminal operations idempotent or explicitly reject repeated use according to the product contract.

## 11. ObjectAtlas invariant summary

- valid unique IDs;
- one parent for each non-root node;
- parent/child agreement;
- acyclic graph;
- deterministic root and child order;
- valid bounded JSON-safe attributes;
- private branded live nodes;
- versioned plain persistence records;
- structural revision increments on structural change;
- iterator revision policy is explicit;
- edit sessions publish at most once;
- subtree clones remap domain IDs consistently;
- runtime-only metadata is not persisted accidentally.
