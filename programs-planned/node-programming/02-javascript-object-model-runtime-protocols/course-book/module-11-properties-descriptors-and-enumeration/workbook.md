# Module 11 Workbook

Work without running the snippets until each prediction is written. The aim is to separate ownness, key type, descriptor state, and enumeration surface rather than collapsing them into “the property exists.”

## A. Descriptor prediction

For each construction, write the complete descriptor of `count`:

```ts
const a: Record<string, number> = {};
a.count = 1;
```

```ts
const b: Record<string, number> = {};
Object.defineProperty(b, 'count', { value: 1 });
```

```ts
const c = {
  get count(): number {
    return 1;
  },
};
```

Then predict whether assignment, deletion, changing enumerability, and replacing the accessor with a data property succeed in strict ESM code.

## B. Observation matrix

Construct an object containing:

- one enumerable string property;
- one non-enumerable string property;
- one enumerable symbol property;
- one non-enumerable symbol property;
- one inherited enumerable string property.

Predict the exact output of:

```ts
Object.keys(value);
Object.getOwnPropertyNames(value);
Object.getOwnPropertySymbols(value);
Reflect.ownKeys(value);
[...enumerateWithForIn(value)];
({ ...value });
JSON.stringify(value);
```

Explain each omission. Do not write only the final arrays.

## C. Getter-safe inspection

This code is advertised as a harmless shape inspector:

```ts
function inspectShape(value: object): Record<string, string> {
  return Object.fromEntries(
    Object.keys(value).map((key) => [key, typeof Reflect.get(value, key)]),
  );
}
```

Repair it so that it reports whether each own string key is a data property, getter-only property, setter-only property, or getter/setter pair without invoking any accessor. Include non-enumerable keys.

## D. Validation under prototype pollution

The following validator is incorrect:

```ts
function hasName(value: object): boolean {
  return 'name' in value && typeof Reflect.get(value, 'name') === 'string';
}
```

Create a counterexample using an inherited `name`. Repair the validator. Then explain why a null-prototype dictionary reduces one class of accidental collision but does not remove the need to validate values.

## E. Copy contract

You are given an object with a non-enumerable symbol cache, a read-only public ID, an accessor `label`, and a custom prototype. Compare these operations:

```ts
{ ...source }
Object.assign({}, source)
structuredClone(source)
Object.create(Object.getPrototypeOf(source), Object.getOwnPropertyDescriptors(source))
```

For each, state what happens to:

- prototype;
- symbol keys;
- non-enumerable keys;
- descriptor flags;
- accessors;
- nested object identity.

Choose one operation for a runtime-surface clone and a different operation for a persistence snapshot.

## F. Independent laboratory

Complete [Descriptor-Safe Settings](../../labs/module-11-descriptor-safe-settings/README.md). The reference tests inspect descriptors, enumerate surfaces, and verify that cloning does not execute getters.

## G. ObjectAtlas transfer

Implement the initial node shell described in the chapter. Write tests proving:

- `id` is own, enumerable, non-writable, and non-configurable;
- runtime metadata is a symbol-keyed, non-enumerable own property;
- attributes cannot inherit `constructor`, `toString`, or `__proto__` from `Object.prototype`;
- serialization returns plain validated data rather than spreading the live instance;
- reflective inspection can describe the node without invoking user-defined accessors.

## H. Reconstruction and defense

Without notes, explain:

1. property key versus source spelling;
2. own property versus inherited property;
3. data descriptor versus accessor descriptor;
4. the independent meanings of writable, enumerable, and configurable;
5. why object spread can execute code and weaken descriptors;
6. why symbols are collision-resistant but not secret;
7. why an application should not use incidental property insertion order as a domain ordering.

Defend one use of a non-enumerable property in ObjectAtlas and one place where an ordinary enumerable data property is better.
