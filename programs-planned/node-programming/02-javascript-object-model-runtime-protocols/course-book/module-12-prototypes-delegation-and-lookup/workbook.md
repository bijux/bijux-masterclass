# Module 12 Workbook

Use diagrams. A prototype question answered only with prose often hides whether you are talking about the receiver, the current lookup object, or the constructor’s public `.prototype` property.

## A. Three prototype relationships

Given:

```ts
function RecordItem(this: { id: string }, id: string): void {
  this.id = id;
}
const item = new RecordItem('a');
```

Draw and label:

- `Object.getPrototypeOf(item)`;
- `RecordItem.prototype`;
- `Object.getPrototypeOf(RecordItem)`;
- `Object.getPrototypeOf(RecordItem.prototype)`.

Explain why the phrase “the prototype of `RecordItem`” is ambiguous.

## B. Read trace with receiver

Predict `rectangle.area` and identify the receiver at every step:

```ts
const base = {
  get area(): number {
    return Number(Reflect.get(this, 'width')) * Number(Reflect.get(this, 'height'));
  },
};
const middle = Object.create(base) as object;
const rectangle = Object.create(middle) as {
  width: number;
  height: number;
  readonly area: number;
};
rectangle.width = 5;
rectangle.height = 4;
```

Then explain what would break if a proxy forwarded the getter with `base` as the receiver.

## C. Assignment classification

Classify each assignment as:

- creates or updates an own property;
- invokes an inherited setter;
- fails;
- mutates a shared object reached through an inherited property.

Construct examples for all four categories and prove the resulting ownership with `Object.hasOwn` and descriptors.

## D. Shared mutable state repair

Repair this prototype design:

```ts
const queueBehavior = {
  items: [] as string[],
  push(this: { items: string[] }, value: string): void {
    this.items.push(value);
  },
};
```

Each queue must have independent items while sharing methods. Compare three repairs:

1. own property installed with `Object.create`;
2. constructor function;
3. class with a private field.

State which repair you would publish and why.

## E. Pollution-resistant merge

Design a function that accepts an `unknown` value and produces a null-prototype dictionary containing only keys matching `/^[a-z][a-z0-9-]{0,31}$/` and JSON scalar values. It must:

- ignore no inherited properties silently;
- reject accessors;
- reject duplicate semantic keys after lowercasing;
- reject `__proto__`, `constructor`, and `prototype` explicitly;
- return a fresh dictionary.

Explain why copying with object spread is not sufficient validation.

## F. `instanceof` counterexample

Create an object that passes `instanceof` for a class with a private field but fails when a private-field method is called. Explain what each observation proves.

Then design a public predicate for a domain object. Decide whether it should use `instanceof`, a private-brand check inside the class, runtime data validation, or a combination.

## G. Independent laboratory

Complete [Prototype-Based Policy Catalog](../../labs/module-12-prototype-policy-catalog/README.md). The lab requires shared behavior, per-policy own state, explicit overrides, safe unknown-key storage, and tests for shadowing.

## H. ObjectAtlas transfer

Add:

- a class-prototype method surface;
- a null-prototype attribute store;
- a getter-safe prototype-chain report;
- a test that legitimate reconstruction uses a constructor or factory;
- a test that `Object.setPrototypeOf(plain, AtlasNode.prototype)` does not create a valid node.

## I. Reconstruction and defense

Without notes, explain:

- internal prototype versus function `.prototype`;
- lookup base versus receiver;
- shadowing versus shared mutation;
- inherited setter behavior;
- why mutable data on a prototype is dangerous;
- what `instanceof` proves and does not prove;
- why prototype mutation during ordinary domain updates is a design smell.
