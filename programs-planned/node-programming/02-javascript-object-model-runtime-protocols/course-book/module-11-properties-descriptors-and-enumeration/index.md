# Module 11 — Objects, Property Keys, Descriptors, and Enumeration

> **Question:** When JavaScript evaluates an object operation, which property is it talking about, what attributes govern that property, and which operations can observe it?

## Why this comes now

Course 1 treated objects mainly as identities containing named values. That model is enough for ordinary records, but it is not yet the JavaScript object model. A property is not merely a key paired with a value. It may be a data property or an accessor property. It may be writable or read-only, enumerable or hidden, configurable or permanent. Its key may be a string or a symbol. It may belong to the object itself or be found later through the prototype chain. Different enumeration operations observe different subsets of that state.

Those distinctions are not trivia. They determine whether a copy preserves behavior, whether a validator sees inherited input, whether a serializer omits metadata, whether a getter runs unexpectedly, whether an API can evolve a property, and whether a proxy may legally report a different shape. Every later module depends on this foundation.

ObjectAtlas begins here. Its public node identifiers must be stable, its internal metadata must not leak into ordinary enumeration, and its persistence layer must serialize data rather than accidentally execute accessors or capture runtime-only state.

## Outcomes

By the end of this module, you can:

- distinguish property keys from source-level spelling;
- distinguish own properties from inherited properties;
- distinguish data descriptors from accessor descriptors;
- predict the effects of `writable`, `enumerable`, and `configurable`;
- choose among assignment, `Object.defineProperty`, and `Reflect.defineProperty`;
- explain which keys are observed by `Object.keys`, `Object.getOwnPropertyNames`, `Object.getOwnPropertySymbols`, `Reflect.ownKeys`, `for...in`, object spread, and JSON serialization;
- reason about property order without treating it as arbitrary or using it as an accidental domain contract;
- inspect objects without invoking getters unintentionally;
- design an object whose public data, hidden metadata, and persistence representation are deliberately different.

## 1. An object exposes behavior through internal operations

JavaScript source gives you familiar operations:

```ts
value.name;
value.name = 'Ada';
'name' in value;
delete value.name;
Object.keys(value);
```

The language specification describes these in terms of internal methods such as `[[Get]]`, `[[Set]]`, `[[HasProperty]]`, `[[Delete]]`, `[[OwnPropertyKeys]]`, and `[[GetOwnProperty]]`. You do not call those internal methods directly. The model matters because ordinary objects, arrays, typed arrays, module namespace objects, and proxies may implement related operations differently while still obeying language invariants.

A productive mental model is:

```text
source operation
      ↓
internal object operation
      ↓
property lookup or definition rules
      ↓
observable value, Boolean result, or exception
```

Do not reduce every object operation to “look up a field in a hash map.” That shortcut fails for accessors, prototypes, arrays, proxies, private fields, and many built-ins.

## 2. Property keys are strings or symbols

At the object-model level, a property key is either a string or a symbol.

```ts
const record = {
  1: 'one',
  true: 'truth',
};

console.log(record['1']);    // one
console.log(record['true']); // truth
```

Numeric and Boolean-looking keys in object literals become strings. This is different from `Map`, where keys retain their original identity and type.

```ts
const map = new Map<unknown, string>();
map.set(1, 'number');
map.set('1', 'string');

console.log(map.size); // 2
```

Symbols provide keys that cannot collide accidentally with ordinary strings:

```ts
const revision = Symbol('revision');
const node = {
  id: 'root',
  [revision]: 3,
};
```

A symbol is not automatically private. Code that receives the symbol can access the property, and `Reflect.ownKeys` can discover symbol keys. Symbols are collision-resistant capabilities, not secrecy mechanisms.

Use this property-key ledger when reading an API:

| Question | Example consequence |
|---|---|
| Is the key a string or symbol? | JSON and `Object.keys` ignore symbols |
| Is it own or inherited? | `Object.hasOwn` and `in` answer different questions |
| Is it enumerable? | spread and `Object.keys` may omit it |
| Is it configurable? | later redefinition or deletion may be impossible |
| Is it data or accessor? | reading may execute code |

## 3. Own properties and inherited properties are different facts

An own property belongs directly to an object. An inherited property is found through another object in the prototype chain.

```ts
const behavior = {
  describe(): string {
    return 'shared behavior';
  },
};

const item = Object.create(behavior) as {
  id: string;
  describe(): string;
};
item.id = 'item-1';
```

`id` is own. `describe` is inherited.

```ts
console.log(Object.hasOwn(item, 'id'));       // true
console.log(Object.hasOwn(item, 'describe')); // false
console.log('describe' in item);              // true
```

These operations answer different questions:

- `Object.hasOwn(object, key)` asks whether the object itself owns the property.
- `key in object` asks whether lookup can find the property anywhere in the chain.
- `object[key]` performs a get operation and may invoke an inherited accessor.

At untrusted-data boundaries, own-property checks are usually the correct starting point. A validator for parsed JSON should not accept a required field merely because somebody attached it to `Object.prototype`.

```ts
function hasOwnString(
  value: object,
  key: PropertyKey,
): value is Record<PropertyKey, unknown> {
  return Object.hasOwn(value, key) && typeof Reflect.get(value, key) === 'string';
}
```

Even this helper invokes the value through `Reflect.get`; a getter could run. For hostile or highly reflective inputs, inspect the descriptor first.

## 4. Data descriptors and accessor descriptors

Every own property has a descriptor. A data descriptor contains a value and a writability attribute. An accessor descriptor contains getter and setter functions.

```ts
const dataDescriptor: PropertyDescriptor = {
  value: 3,
  writable: false,
  enumerable: true,
  configurable: false,
};

const accessorDescriptor: PropertyDescriptor = {
  get(): number {
    return 3;
  },
  enumerable: true,
  configurable: false,
};
```

A descriptor cannot be both a data descriptor and an accessor descriptor. A definition that supplies `value` together with `get` is invalid.

Ordinary assignment usually creates a property with all three ordinary flags enabled:

```ts
const assigned: Record<string, number> = {};
assigned.count = 1;

console.log(Object.getOwnPropertyDescriptor(assigned, 'count'));
// { value: 1, writable: true, enumerable: true, configurable: true }
```

`Object.defineProperty` defaults omitted Boolean attributes to `false`:

```ts
const defined: Record<string, number> = {};
Object.defineProperty(defined, 'count', { value: 1 });

console.log(Object.getOwnPropertyDescriptor(defined, 'count'));
// { value: 1, writable: false, enumerable: false, configurable: false }
```

That difference is a common source of accidental hidden, read-only, permanent properties.

## 5. The three descriptor permissions are independent

For a data property:

- `writable` controls ordinary changes to the stored value;
- `enumerable` controls participation in several enumeration and copy operations;
- `configurable` controls deletion and most descriptor reconfiguration.

Consider:

```ts
const node: Record<string, unknown> = {};
Object.defineProperty(node, 'id', {
  value: 'root',
  writable: false,
  enumerable: true,
  configurable: false,
});
```

In strict-mode ESM code, assigning another value throws. Deleting the property throws. Changing it into an accessor throws. Changing `enumerable` throws.

A non-configurable, non-writable data property may sometimes be redefined with the same value, but it cannot be changed to a different value. Do not rely on edge cases as an update strategy. Treat a non-configurable property as a permanent public commitment.

`configurable: false` is therefore stronger than “please do not delete this.” Once published, it constrains future maintenance. Use it only when permanence is part of the contract.

## 6. `Object.defineProperty` and `Reflect.defineProperty`

Both operations attempt to define an own property using a descriptor. They differ in failure reporting:

- `Object.defineProperty` returns the object and throws if the definition is rejected;
- `Reflect.defineProperty` returns `true` or `false` for ordinary definition failure.

```ts
const value = Object.preventExtensions({});

const accepted = Reflect.defineProperty(value, 'x', {
  value: 1,
});

console.log(accepted); // false
```

The reflective form is useful when rejection is an expected branch in a metaprogram. The throwing form is often clearer when failure means the program’s invariant is broken.

Do not ignore the Boolean result from `Reflect.defineProperty`. A silent `false` can leave code believing that metadata was installed when it was not.

## 7. Accessors execute behavior during property access

An accessor property can validate, compute, cache, log, allocate, throw, or mutate unrelated state.

```ts
let reads = 0;
const measured = {
  get value(): number {
    reads += 1;
    return 42;
  },
};

console.log(measured.value); // 42
console.log(reads);          // 1
```

Several apparently observational operations may invoke getters. Object spread reads enumerable property values:

```ts
const copy = { ...measured };
console.log(copy);  // { value: 42 }
console.log(reads); // 2
```

The copy contains a plain data property, not the original accessor descriptor.

When you need to inspect shape without executing accessors, use descriptors:

```ts
const descriptors = Object.getOwnPropertyDescriptors(measured);
console.log(typeof descriptors.value?.get); // function
```

This distinction matters in debuggers, validators, serializers, test fixtures, and proxy handlers. “Reading an object” is not always free of effects.

## 8. Enumeration operations observe different surfaces

There is no single operation called “all object keys.” Use the operation whose contract matches the question.

| Operation | Own strings | Own symbols | Inherited enumerable strings | Non-enumerable |
|---|---:|---:|---:|---:|
| `Object.keys` | enumerable | no | no | no |
| `Object.getOwnPropertyNames` | yes | no | no | yes |
| `Object.getOwnPropertySymbols` | no | yes | no | yes |
| `Reflect.ownKeys` | yes | yes | no | yes |
| `for...in` | enumerable | no | yes | no |
| object spread | enumerable | enumerable | no | no |
| `JSON.stringify` | enumerable string keys selected by JSON rules | no | no | no |

Example:

```ts
const hidden = Symbol('hidden');
const base = { inherited: true };
const value = Object.create(base) as Record<PropertyKey, unknown>;

Object.defineProperties(value, {
  visible: {
    value: 1,
    enumerable: true,
    configurable: true,
    writable: true,
  },
  secret: {
    value: 2,
    enumerable: false,
    configurable: true,
    writable: true,
  },
  [hidden]: {
    value: 3,
    enumerable: true,
    configurable: true,
    writable: true,
  },
});
```

Predictions:

```ts
Object.keys(value);                  // ['visible']
Object.getOwnPropertyNames(value);   // ['visible', 'secret']
Object.getOwnPropertySymbols(value); // [hidden]
Reflect.ownKeys(value);              // ['visible', 'secret', hidden]
```

A `for...in` loop also observes `inherited` because it is enumerable on the prototype. That is why `for...in` is usually wrong for record validation unless it is paired with an own-property filter.

## 9. Property order is specified, but it should be a deliberate contract

Modern JavaScript specifies an ordering for ordinary own keys:

1. array-index-like string keys in ascending numeric order;
2. other string keys in creation order;
3. symbol keys in creation order.

```ts
const value = {
  b: 1,
  10: 'ten',
  2: 'two',
  a: 2,
};

console.log(Reflect.ownKeys(value));
// ['2', '10', 'b', 'a']
```

This is no longer well described as “object order is random.” However, an application should not accidentally turn object insertion history into a domain ordering. If output order matters to users, encode and test that order explicitly—often with an array or a sorted list of keys.

ObjectAtlas stores child order as an array because graph traversal order is a product rule. It does not depend on the order in which properties happened to be attached to a node object.

## 10. Extensible, sealed, and frozen objects

`Object.preventExtensions` prevents new own properties and prototype replacement. Existing configurable properties may still be changed or removed.

`Object.seal` prevents extensions and makes existing own properties non-configurable. Writable data properties may still change value.

`Object.freeze` seals the object and makes existing data properties non-writable. It is shallow:

```ts
const state = Object.freeze({
  nested: { count: 1 },
});

state.nested.count = 2; // nested object was not frozen
```

These operations constrain runtime mutation. They do not make a complete object graph immutable, and they do not replace an application authority model.

Use them to enforce a specific boundary, not to advertise vague “immutability.” A frozen object containing a mutable `Map` still exposes a mutable map.

## 11. Copying values is not copying descriptors

Object spread and `Object.assign` copy enumerable own property values. They do not preserve descriptor attributes, getters, setters, non-enumerable properties, or the original prototype.

```ts
const source = {};
Object.defineProperty(source, 'id', {
  value: 'node-1',
  writable: false,
  enumerable: true,
  configurable: false,
});

const copy = { ...source };
console.log(Object.getOwnPropertyDescriptor(copy, 'id'));
// writable: true, enumerable: true, configurable: true
```

A descriptor-preserving shallow clone can be built explicitly:

```ts
function cloneOwnSurface<T extends object>(source: T): T {
  const prototype = Object.getPrototypeOf(source) as object | null;
  return Object.create(
    prototype,
    Object.getOwnPropertyDescriptors(source),
  ) as T;
}
```

This still does not deep-clone nested values or internal slots. It also invokes no getters while obtaining descriptors. Use it only when preserving the runtime own-property surface is the actual requirement.

## 12. ObjectAtlas increment

Create the first `AtlasNode` runtime shell.

Requirements:

- `id` is an enumerable, non-writable, non-configurable own data property;
- runtime-only metadata uses a symbol key and is non-enumerable;
- user attributes are stored in a plain null-prototype object so inherited names cannot masquerade as attributes;
- serialization reads validated data through an explicit method rather than spreading the class instance;
- inspection tests compare property descriptors, not only values;
- no getter performs mutation or I/O.

The purpose is not to make every property exotic. Most application data should remain ordinary. The purpose is to make each deviation from ordinary assignment intentional and testable.

## Common wrong models

### “An object is just a dictionary”

Objects have prototypes, property descriptors, symbols, accessors, and internal methods. Use `Map` or a null-prototype object when dictionary semantics are the real requirement.

### “A symbol is private”

A symbol avoids accidental string-key collision. It can still be discovered through reflective operations.

### “`in` checks whether the input contains a field”

`in` includes inherited properties. External record validation generally needs an own-property check.

### “Spread copies the object”

Spread copies enumerable own values into ordinary writable, enumerable, configurable data properties.

### “Freeze makes the graph immutable”

`Object.freeze` is shallow and says nothing about authority held through other references.

### “Enumeration order is random”

Ordinary own-key order is specified, but domain order should still be modeled deliberately.

## Practice sequence

1. Predict the exact descriptor created by assignment and by `Object.defineProperty`.
2. Build one object containing enumerable and non-enumerable string and symbol properties.
3. Record the output of every enumeration operation in the table above.
4. Repair a validator that uses `for...in` over untrusted input.
5. Repair a copy routine that unintentionally executes getters and loses descriptors.
6. Complete the Descriptor-Safe Settings laboratory.
7. Add the ObjectAtlas node shell and descriptor tests.
8. Explain why ObjectAtlas persistence must serialize a plain snapshot rather than the live instance.

## Ready to continue

Continue only when you can inspect an unfamiliar object and answer all of these without guessing:

- Which keys are own?
- Which keys are symbols?
- Which properties are enumerable?
- Which reads may execute code?
- Which properties can be redefined or deleted?
- Which copy operation preserves the required contract?
- Which surface should persistence observe?

The next module adds prototype lookup. Every distinction established here remains active when the requested property is not found on the receiver itself.

## Primary references

- ECMAScript Language Specification: property keys, property descriptors, object internal methods, and ordinary object behavior.
- Node.js `util.inspect` documentation: hidden properties, symbols, getters, proxies, and custom inspection.
- TypeScript Handbook: object types and readonly properties, read as static permissions rather than runtime descriptors.

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory 11 — Descriptor-Safe Settings](../../labs/module-11-descriptor-safe-settings/README.md)
- [ObjectAtlas engineering guide](../capstone.md)
