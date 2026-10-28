# Module 4 — Objects, Arrays, Identity, Mutation, and Immutable Updates

> **Question:** Which references point to the same object, which updates are visible through aliases, and what does a copy actually copy?

## Why this comes now

Functions operate on objects and arrays, and JavaScript passes object references by value. That phrase is often replaced with the misleading shorthand “objects are passed by reference.” The precise model matters: assignments and parameters receive copied references to the same identity; reassigning a parameter does not reassign the caller’s binding, while mutating the shared object is observable through every alias.

StudyLedger will retain arrays of state-specific session objects. Before building those states, you must be able to prove which update mutates existing history and which constructs a new ledger.

## Outcomes

You can:

- draw alias graphs for objects, arrays, maps, and nested values;
- distinguish reference equality from domain equality;
- explain the exact depth of spread syntax, `Array.from`, and `slice`;
- use destructuring without assuming it clones nested values;
- choose mutation or immutable update from authority and observation requirements;
- use `readonly` and `Object.freeze` without overstating runtime protection;
- preserve untouched object identities during targeted StudyLedger updates.

## 1. Variables hold references to object identities

```ts
const first = { count: 1 };
const second = first;
second.count += 1;
console.log(first.count); // 2
```

There is one object and two bindings containing references to it:

```text
first ──┐
        ├──> object { count: 2 }
second ─┘
```

Passing `first` to a function copies the reference into a parameter binding. The function can mutate the shared object. Reassigning the parameter changes only the local binding.

## 2. Equality of objects is identity equality

```ts
{ count: 1 } === { count: 1 }; // false
```

The objects have equal-looking properties but distinct identities. Domain equality requires a function that names which fields matter and how they are compared.

Using `JSON.stringify` as general equality is fragile because it depends on representability and property order, ignores some values, rejects cycles, and encodes a serialization policy rather than a domain relation.

## 3. Spread is shallow

```ts
const original = {
  name: 'Ada',
  preferences: { theme: 'dark' },
};

const copy = { ...original };
copy.preferences.theme = 'light';
console.log(original.preferences.theme); // light
```

The outer object is new. The nested `preferences` reference is copied.

```text
original ──> outer A ──> preferences P
copy     ──> outer B ──┘
```

A nested immutable update copies every object along the changed path:

```ts
const updated = {
  ...original,
  preferences: {
    ...original.preferences,
    theme: 'light',
  },
};
```

Untouched nested references may remain shared deliberately.

## 4. Arrays have identity and mutation

Methods such as `push`, `pop`, `splice`, `sort`, and `reverse` mutate the array. Methods such as `map`, `filter`, `slice`, and `concat` return new arrays, though their elements may still be shared objects.

A deterministic sort that preserves input order uses a copy:

```ts
const sorted = [...sessions].sort((left, right) => left.id - right.id);
```

Modern non-mutating methods such as `toSorted` can express this directly on supported runtimes, but the course uses the copy-and-sort form to keep the operation explicit and broadly understandable.

## 5. Destructuring copies values, not object graphs

```ts
const session = {
  id: 1,
  metadata: { source: 'cli' },
};
const { id, metadata } = session;
```

`id` receives a primitive value. `metadata` receives another reference to the same nested object.

Rest syntax creates a new outer object but remains shallow:

```ts
const { metadata: ignored, ...withoutMetadata } = session;
void ignored;
```

## 6. Static readonly and runtime mutation

```ts
interface Point {
  readonly x: number;
  readonly y: number;
}
```

`readonly` constrains writes through that static view. It does not freeze the runtime object, and another mutable alias can still change it.

`Object.freeze` freezes an object’s own properties at runtime, but it is shallow. Deep freezing is a separate recursive policy with cycle and performance concerns.

Use `readonly` to express intended permissions. Do not present it as a security boundary or universal immutability guarantee.

## 7. Choosing mutation or immutable updates

Mutation is not categorically wrong. It can be the clearest design when one authority exclusively owns a local object and no observer requires prior versions. Immutable updates are valuable when:

- earlier versions remain meaningful;
- callers should not observe partial changes;
- references are shared across components;
- tests compare before and after state;
- rollback and history matter;
- the architecture uses pure transition functions.

StudyLedger uses immutable domain updates because command execution constructs one candidate ledger and persistence happens only after the candidate is valid. This supports failure atomicity at the application level.

## 8. Targeted immutable update

```ts
function replaceById<T extends { readonly id: number }>(
  values: readonly T[],
  id: number,
  replace: (value: T) => T,
): readonly T[] {
  let found = false;
  const next = values.map((value) => {
    if (value.id !== id) {
      return value;
    }
    found = true;
    return replace(value);
  });

  if (!found) {
    throw new Error(`missing id ${id}`);
  }
  return next;
}
```

Unchanged elements retain identity; the array and changed element are new. This is structural sharing, not a deep clone.

The callback must be pure for the function to guarantee that prior state remains unchanged. A type alone cannot prove that.

## 9. Serialization changes identity

A JSON round trip constructs new objects and loses non-JSON values and prototypes. It is not a safe general deep-clone strategy:

```ts
const clone = JSON.parse(JSON.stringify(value));
```

Dates become strings, `undefined` can disappear, `BigInt` fails, map/set structure is lost, and cycles throw. In StudyLedger, JSON is a deliberate persistence format for plain data. The validator reconstructs trusted plain objects; the program does not use JSON as an identity-preserving clone.

## 10. StudyLedger increment

Define a ledger as a readonly object containing `nextId` and a readonly session array. Implement pure operations that return a new ledger:

- append a planned session;
- replace one session by ID;
- reject a missing ID without mutating the input;
- preserve unrelated session object identities;
- allocate `nextId` only in the successful candidate.

Tests should keep the original reference and prove it remains deeply equal after both success and failure paths.

## Common wrong models

### “Objects are passed by reference”

References are values copied into bindings. Mutation and reassignment have different effects.

### “Spread clones the object”

Spread creates a new outer object and copies property values, including nested references.

### “Readonly means immutable at runtime”

It is a static access restriction through a particular view.

### “Immutable code copies everything”

Good immutable updates copy the changed path and share unchanged structure.

### “JSON is a deep clone”

JSON is a serialization format with representational loss and new identities.

## 11. Draw the heap graph before repairing mutation

When identity behavior is unclear, draw variables and objects separately:

```text
inventory ──► object A
               │ items
               ▼
             array B ──► item C ──► supplier D
                    └──► item E ──► supplier F
```

After a targeted supplier-email update, a well-designed immutable result is:

```text
updated ──► object A2
             │ items
             ▼
           array B2 ──► item C2 ──► supplier D2
                   └──► item E  ──► supplier F
```

Unchanged item E and supplier F retain identity. The changed path receives new identities. This is structural sharing, not deep cloning.

The graph also clarifies failed operations. If validation fails before publication, no pointer from the caller should be redirected and no reachable object should have been mutated.

## 12. “Pass by reference” is an imprecise model

JavaScript passes argument values. For an object argument, the value is a reference to an object identity. The parameter receives a copy of that reference:

```ts
function replace(value: { count: number }): void {
  value = { count: 99 }; // changes only the local binding
}

function mutate(value: { count: number }): void {
  value.count = 99; // changes the shared object
}
```

Calling both “pass by reference” obscures why rebinding and mutation differ. Use this sentence instead:

> The object reference is passed by value; aliases can observe mutations to the referenced object.

## 13. Array details that affect correctness

Arrays are objects with integer-like property names and a special `length`. They may be sparse:

```ts
const values = new Array<number>(3);
values.length; // 3
values[0];     // undefined
```

Several array methods treat holes differently. Avoid sparse arrays in ordinary domain models unless the distinction between a missing property and an explicit `undefined` value is intentional.

Mutation methods have different effects:

| Method | Mutates array | Returns |
|---|---:|---|
| `push` | yes | new length |
| `sort` | yes | same array |
| `splice` | yes | removed items |
| `map` | no | new array |
| `filter` | no | new array |
| `toSorted` | no | sorted copy |

The presence of a nonmutating method does not guarantee deep immutability of its elements.

## 14. Readonly is a capability view

`readonly` prevents writes through a particular static reference. It does not freeze the runtime value and does not prevent another mutable alias from changing it.

```ts
const mutable = { count: 1 };
const view: Readonly<{ count: number }> = mutable;
mutable.count = 2;
console.log(view.count); // 2
```

This is still useful. An API can promise not to mutate through a parameter and deny accidental writes in its implementation. But it must not claim snapshot semantics unless it owns a copy or an immutable representation.

`Object.freeze` is also shallow. It prevents changes to the immediate object under ordinary operations but leaves nested objects mutable unless they are frozen separately. Proxies and host objects add further nuance; Course 1 uses plain data objects.

## 15. Candidate-state publication

For a multi-step update, do not publish each mutation as validation proceeds. Build or validate a candidate first:

```ts
function applyAdjustments(
  inventory: Inventory,
  changes: readonly Adjustment[],
): Inventory {
  let candidate = inventory;
  for (const change of changes) {
    candidate = adjustStock(candidate, change.id, change.delta);
  }
  return candidate;
}
```

Because each step returns a new value and the original remains untouched, a later rejection prevents publication of the candidate. With mutable internals, the same property requires rollback or staging.

This pattern reappears in JSON decoding, persistence, transactions, and concurrent systems: construct a complete valid candidate, then publish once.

## 16. Cloning and serialization are policies, not repairs

`structuredClone` can copy many built-in values and handle cycles, but it still changes identity for the whole copied graph and rejects or transforms some kinds of values. JSON round trips lose `undefined`, symbols, prototypes, methods, `bigint`, and special numeric values.

Before cloning, state the required identity policy. If only one nested field changes, path-local copying is more precise and usually cheaper. If isolation from all future mutation is required, a deeper copy may be justified, but its supported value vocabulary becomes part of the API contract.

## Practice sequence

Complete the [workbook](workbook.md), then [Inventory Transform](../../labs/module-04-inventory-transform/README.md). Refactor StudyLedger updates until failure paths leave the original ledger unchanged.

## Ready to continue

Continue when you can draw the identity graph before and after every spread, map, destructuring, or nested update used in your code.

Next: [Module 5 — TypeScript Modeling, Unions, Narrowing, `unknown`, and `never`](../module-05-typescript-modeling-and-narrowing/index.md)
