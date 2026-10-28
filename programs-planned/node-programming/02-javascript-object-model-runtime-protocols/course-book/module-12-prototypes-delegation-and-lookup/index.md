# Module 12 — Prototypes, Delegation, Lookup, and Shadowing

> **Question:** When an object does not own a requested property, where does JavaScript look next, which receiver is used, and what changes when an own property shadows inherited behavior?

## Why this comes now

Module 11 established the own-property surface. JavaScript property access does not stop there. Ordinary objects have an internal `[[Prototype]]` link to another object or to `null`. Lookup can walk that chain. Methods are commonly shared through prototypes, setters can be inherited but write to a different receiver, and an assignment may create a shadowing own property rather than changing the prototype object.

The prototype model is the semantic foundation beneath class syntax, constructor instances, many built-ins, and several security failures. It is also different from copying behavior into every object. Delegation means that an object can use behavior owned elsewhere while keeping its own state.

ObjectAtlas uses shared node behavior without storing duplicate method functions on every instance. It also uses null-prototype dictionaries for user attributes so names such as `constructor` and `toString` are treated as data rather than inherited behavior.

## Outcomes

By the end of this module, you can:

- draw a finite prototype chain and trace `[[Get]]`, `[[HasProperty]]`, and ordinary assignment through it;
- distinguish an object’s internal prototype from a function’s public `.prototype` property;
- predict shadowing of inherited data properties, methods, getters, and setters;
- explain why an inherited accessor receives the original receiver;
- create objects with `Object.create` and choose ordinary versus null prototypes deliberately;
- inspect and change prototypes without using legacy `__proto__` syntax;
- identify prototype pollution and inherited-key hazards at external boundaries;
- decide when delegation is clearer than copying, classes, or nested composition;
- avoid mutable state on shared prototypes.

## 1. `[[Prototype]]` is a link used during lookup

An ordinary object’s internal prototype is either another object or `null`.

```ts
const behavior = {
  describe(): string {
    return `node:${String(Reflect.get(this, 'id'))}`;
  },
};

const node = Object.create(behavior) as {
  id: string;
  describe(): string;
};
node.id = 'root';

console.log(node.describe()); // node:root
```

The graph is:

```text
node own properties: id
   │ [[Prototype]]
   ▼
behavior own properties: describe
   │ [[Prototype]]
   ▼
Object.prototype
   │ [[Prototype]]
   ▼
null
```

The method is not copied into `node`. Lookup finds it on `behavior`; invocation still uses `node` as the receiver because the call expression was `node.describe()`.

A prototype chain must eventually terminate at `null`. Cyclic ordinary prototype chains are rejected.

## 2. Internal prototype versus constructor `.prototype`

These are related but different facts:

- every ordinary object has an internal `[[Prototype]]` link;
- many function objects have a public property named `prototype`;
- when a constructible function is used with `new`, its `.prototype` value is normally used as the new object’s internal prototype.

```ts
function Node(this: { id: string }, id: string): void {
  this.id = id;
}

const instance = new Node('root');

console.log(Object.getPrototypeOf(instance) === Node.prototype); // true
console.log(Object.getPrototypeOf(Node) === Function.prototype); // true
```

`Node.prototype` is itself an object. It is not “the prototype of the function Node.” The function’s own internal prototype is usually `Function.prototype`.

Use this vocabulary precisely:

```text
Object.getPrototypeOf(instance)  → internal prototype of instance
Node.prototype                   → public property used by new
Object.getPrototypeOf(Node)      → internal prototype of function object
```

Confusing these relationships makes constructor, class, and inheritance behavior look arbitrary.

## 3. Ordinary get walks the chain but preserves the receiver

A simplified ordinary read looks like this:

```text
Get(base object, key, receiver)
  if base has own data property key:
      return stored value
  if base has own accessor key:
      call getter with receiver as this
  otherwise:
      repeat on base.[[Prototype]], preserving receiver
```

The receiver is why inherited accessors can read instance-specific state:

```ts
const dimensions = {
  get area(): number {
    const width = Number(Reflect.get(this, 'width'));
    const height = Number(Reflect.get(this, 'height'));
    return width * height;
  },
};

const rectangle = Object.create(dimensions) as {
  width: number;
  height: number;
  readonly area: number;
};
rectangle.width = 4;
rectangle.height = 3;

console.log(rectangle.area); // 12
```

The getter is owned by `dimensions`; `this` is `rectangle`.

This same receiver distinction becomes critical in proxy forwarding. A handler that reads from the target with the wrong receiver can change accessor and private-field behavior.

## 4. Shadowing an inherited data property

Suppose a prototype owns a writable data property:

```ts
const defaults = { mode: 'normal' };
const first = Object.create(defaults) as { mode: string };
const second = Object.create(defaults) as { mode: string };

first.mode = 'strict';
```

The assignment usually creates an own property on `first`:

```ts
console.log(first.mode);                   // strict
console.log(second.mode);                  // normal
console.log(defaults.mode);                // normal
console.log(Object.hasOwn(first, 'mode')); // true
```

The inherited property is shadowed, not modified.

This makes prototypes useful for shared defaults only when shadowing is an acceptable update model. If all instances must observe one authoritative changing setting, store that setting in an explicitly shared object rather than relying on accidental prototype mutation.

## 5. Inherited non-writable data properties block assignment

If the prototype’s data property is non-writable, ordinary assignment through a descendant fails in strict code instead of creating a shadow:

```ts
const policy = {};
Object.defineProperty(policy, 'version', {
  value: 1,
  writable: false,
  enumerable: true,
  configurable: false,
});

const candidate = Object.create(policy) as { version: number };
candidate.version = 2; // TypeError at runtime in strict ESM
```

The prototype-chain descriptor participates in the set algorithm. “Assignment always creates an own property” is therefore false.

A direct `Object.defineProperty(candidate, 'version', ...)` is a different operation and may create an own property if `candidate` is extensible. That is not a reason to bypass the policy casually. It is evidence that assignment and explicit property definition have different contracts.

## 6. Inherited setters write through the receiver

An inherited setter can route a write into receiver-specific storage:

```ts
const state = new WeakMap<object, string>();

const named = {
  set name(value: string) {
    state.set(this, value.trim());
  },
  get name(): string {
    return state.get(this) ?? '';
  },
};

const first = Object.create(named) as { name: string };
const second = Object.create(named) as { name: string };

first.name = ' Ada ';
second.name = ' Linus ';

console.log(first.name);  // Ada
console.log(second.name); // Linus
```

No own `name` property is created. The setter and getter are inherited; the weak map is keyed by the receiver.

This pattern can provide shared behavior with per-object state, but it has a larger reasoning surface than an ordinary class with private fields. Use it when prototype-level delegation is itself useful, not merely to appear clever.

## 7. `Object.create` expresses delegation directly

`Object.create(prototype, descriptors?)` constructs an object with an explicit internal prototype and optional own descriptors.

```ts
const nodeBehavior = {
  label(this: { id: string }): string {
    return `Node(${this.id})`;
  },
};

const root = Object.create(nodeBehavior, {
  id: {
    value: 'root',
    writable: false,
    enumerable: true,
    configurable: false,
  },
}) as { readonly id: string; label(): string };
```

This is not a “pre-class” feature. It is the direct primitive for prototype delegation. Classes compile down to related object and prototype relationships, while adding construction syntax, private fields, and inheritance rules.

`Object.create(null)` creates an object with no inherited properties:

```ts
const attributes = Object.create(null) as Record<string, unknown>;
attributes.constructor = 'data';
attributes.toString = 'also data';
```

Such an object lacks methods such as `hasOwnProperty` and `toString`. Use static operations like `Object.hasOwn` and `Reflect.ownKeys` rather than borrowing methods implicitly.

## 8. Method sharing and the shared mutable state trap

Methods on a prototype are intentionally shared:

```ts
const behavior = {
  describe(this: { id: string }): string {
    return this.id;
  },
};
```

Mutable containers on a prototype are usually accidental global state:

```ts
const broken = {
  tags: [] as string[],
};

const a = Object.create(broken) as { tags: string[] };
const b = Object.create(broken) as { tags: string[] };

a.tags.push('shared');
console.log(b.tags); // ['shared']
```

Neither object owns `tags`; both reads find the same array on the prototype.

A repair gives each instance its own container:

```ts
function createTagged(): { tags: string[] } {
  return Object.create(broken, {
    tags: {
      value: [],
      writable: false,
      enumerable: true,
      configurable: false,
    },
  }) as { tags: string[] };
}
```

Whether the `tags` binding itself should be writable is separate from whether the array contents may mutate.

## 9. Prototype mutation is a broad effect

`Object.setPrototypeOf` changes lookup behavior for an existing object. It is semantically powerful and can be difficult for readers and runtimes to optimize.

```ts
Object.setPrototypeOf(node, differentBehavior);
```

The operation can alter:

- which methods are found;
- which accessors run;
- which `in` checks succeed;
- `instanceof` results;
- proxy invariants;
- assumptions made by code that previously inspected the object.

Prefer choosing the prototype at construction. Treat later mutation as a migration or metaprogramming operation requiring explicit tests, not as an ordinary way to change an object’s role.

Use `Object.getPrototypeOf` and `Object.setPrototypeOf`, not the legacy `__proto__` accessor. The string `"__proto__"` also creates security and data-model ambiguity when untrusted keys are merged into ordinary objects.

## 10. Prototype pollution and dictionary boundaries

Prototype pollution occurs when untrusted input can modify a prototype object or introduce attacker-controlled properties that later appear inherited.

A vulnerable merge may look like:

```ts
function merge(target: Record<string, unknown>, input: Record<string, unknown>): void {
  for (const key in input) {
    target[key] = input[key];
  }
}
```

Problems include:

- `for...in` accepts inherited input;
- dangerous names such as `__proto__`, `constructor`, and `prototype` may change or reach object behavior;
- later code may use `in` and accept inherited attacker-controlled values.

A safer record boundary:

1. requires an ordinary data object or a specifically accepted representation;
2. iterates own keys explicitly;
3. validates an allowlist or grammar of keys;
4. rejects dangerous structural names where ordinary objects are used;
5. stores open-ended user keys in a `Map` or null-prototype object;
6. uses `Object.hasOwn` for required fields.

This is defense in depth. A null-prototype destination alone does not make arbitrary values safe.

## 11. Delegation versus composition

Prototype delegation says:

> If this object does not own a property, continue lookup in that other object.

Nested composition says:

> This object owns or references another capability and calls it explicitly.

```ts
const node = {
  formatter,
  describe(): string {
    return this.formatter.format(this);
  },
};
```

Composition makes authority and dependency names explicit. Delegation can be concise when a family of objects genuinely shares one behavioral surface.

Use this decision table:

| Requirement | Often clearer mechanism |
|---|---|
| Shared stateless methods across many instances | prototype or class methods |
| Open-ended user keys | `Map` or null-prototype object |
| Replaceable collaborator with explicit authority | nested composition |
| Per-instance validated hidden state | private class fields |
| Dynamic fallback defaults | prototype only if shadowing semantics are desired |
| Multiple independent capabilities | composition; mixins only with a controlled conflict policy |

Module 15 returns to composition after classes and private state are understood.

## 12. `instanceof` follows prototype relationships

For ordinary constructible functions, `value instanceof Constructor` checks whether `Constructor.prototype` appears in `value`’s prototype chain. It does not prove that a constructor body ran, that private fields exist, or that the object satisfies a TypeScript interface.

```ts
class Box {
  #value = 1;

  read(): number {
    return this.#value;
  }
}

const counterfeit = Object.create(Box.prototype) as Box;
console.log(counterfeit instanceof Box); // true
counterfeit.read(); // TypeError: private brand is missing
```

This is a critical distinction:

```text
prototype-chain membership ≠ private-brand membership ≠ structural type evidence
```

Classes and private brands are the subject of Module 14. For now, do not use `instanceof` as a universal trust boundary.

## 13. ObjectAtlas increment

Introduce the runtime prototype architecture deliberately.

Requirements:

- `AtlasNode` instances share methods through the class prototype rather than owning method functions;
- user attributes remain in a null-prototype dictionary;
- no mutable array, map, or object is stored on a shared prototype;
- reflective inspection reports the prototype chain without reading arbitrary getters;
- a test creates an object with `AtlasNode.prototype` but without the class’s private state and proves that prototype membership alone is insufficient;
- persistence reconstructs legitimate instances through the public constructor or factory rather than changing prototypes after parsing.

Do not use `Object.setPrototypeOf` as a deserialization shortcut. Reconstructing valid state is different from giving a plain object a familiar method table.

## Common wrong models

### “The prototype is the `.prototype` property”

Objects have internal prototypes. Constructible functions often expose a `.prototype` object used by `new`.

### “Inherited properties belong to the instance”

Lookup can find them, but descriptors and ownership remain on the prototype object.

### “Assignment changes whichever object owns the property”

It may create a shadowing own property, invoke an inherited setter, or fail because of an inherited non-writable property.

### “Methods are copied into each instance”

Prototype methods are shared and found through lookup.

### “`instanceof` proves the object was correctly constructed”

It ordinarily proves prototype-chain membership. Private brands and domain invariants are separate.

### “A null-prototype object is automatically secure”

It removes inherited names. Values, key grammar, size, and authority still require validation.

## Practice sequence

1. Draw the three different prototype relationships around a constructor function.
2. Trace reads through a two-level chain containing a data property and an accessor.
3. Predict whether assignments shadow, invoke a setter, or fail.
4. Repair shared mutable state stored on a prototype.
5. Build a null-prototype dictionary and enumerate it without borrowed instance methods.
6. Complete the Prototype-Based Policy Catalog laboratory.
7. Add ObjectAtlas prototype-chain inspection and counterfeit-instance tests.
8. Explain why changing a parsed object’s prototype does not establish private fields or domain validity.

## Ready to continue

Continue when you can trace a property operation using all three participants:

```text
base object where lookup currently occurs
requested property key
original receiver used by accessors and writes
```

You should also be able to distinguish internal prototype, constructor `.prototype`, and private brand. Module 13 adds call and construction semantics, including the exact work performed by `new`.

## Primary references

- ECMAScript Language Specification: ordinary `[[Get]]`, `[[Set]]`, `[[GetPrototypeOf]]`, and `[[SetPrototypeOf]]` behavior.
- ECMAScript overview: constructor functions, prototype chains, and property lookup.
- Node.js security guidance and runtime documentation where untrusted object keys cross application boundaries.

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory 12 — Prototype-Based Policy Catalog](../../labs/module-12-prototype-policy-catalog/README.md)
- [ObjectAtlas engineering guide](../capstone.md)
