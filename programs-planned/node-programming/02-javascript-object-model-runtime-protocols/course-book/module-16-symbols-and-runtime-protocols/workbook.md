# Module 16 Workbook

For every protocol, write the trigger, symbol, receiver, arguments, result type, and allowed effects before implementing it.

## A. Symbol identity

Predict and then verify:

```ts
const a = Symbol('x');
const b = Symbol('x');
const c = Symbol.for('course.object.x');
const d = Symbol.for('course.object.x');

[a === b, c === d, Symbol.keyFor(a), Symbol.keyFor(c)];
```

Explain why descriptions are suitable for diagnostics but not for identity or persistence.

## B. Enumeration surface

Create an object containing two string keys, two unique symbol keys, and one registry symbol key with mixed enumerability. Predict `Object.keys`, symbol enumeration, `Reflect.ownKeys`, spread, and JSON output.

Then decide which surface a debugging tool, a persistence codec, and a protocol registry should observe.

## C. Primitive conversion policy

Design a `Temperature` value. Decide what should happen for:

```ts
String(value)
Number(value)
`${value}`
value + 1
value == 20
```

Reject any policy that silently mixes Celsius and Fahrenheit. Compare `Symbol.toPrimitive` with explicit `toCelsius()` and `format(unit)` methods.

## D. Diagnostic tag counterfeit

Create two unrelated objects with the same `Symbol.toStringTag`. Prove that `Object.prototype.toString.call` cannot establish domain validity. Design a validator that checks actual data or a controlled brand.

## E. Custom inspection

Implement a Node custom-inspection method for an API token. It must:

- reveal only the final four characters;
- avoid calling a getter that may perform I/O;
- bound output;
- remain stable across repeated calls;
- not be used by JSON persistence.

Explain which parts of the resulting string are your contract and which parts belong to Node’s formatter.

## F. Protocol decision table

For each requirement, choose a normal method, symbol method, private field, or exported capability symbol:

- persistence snapshot;
- default graph traversal;
- alternate breadth-first traversal;
- debug summary;
- hidden cache key;
- runtime validator;
- numeric conversion of a duration;
- mutation transaction commit.

## G. Independent laboratory

Complete [Protocol-Aware Value Object](../../labs/module-16-protocol-aware-value-object/README.md). It implements deliberate conversion, tagging, inspection, symbol metadata, and negative counterfeit tests.

## H. ObjectAtlas transfer

Add `Symbol.toPrimitive`, `Symbol.toStringTag`, Node custom inspection, and the exported metadata symbol. Prove that:

- protocols are pure and bounded;
- metadata is omitted from ordinary enumeration but visible reflectively;
- custom inspection redacts large or sensitive attributes;
- persistence uses `toRecord`, not conversion or inspection;
- custom tags do not validate instances.

## I. Reconstruction and defense

Without notes, explain:

- unique versus registry symbols;
- `unique symbol` typing;
- well-known symbols;
- implicit conversion hints;
- `Symbol.toStringTag` limitations;
- custom `instanceof` risks;
- Node custom inspection’s stability boundary;
- why symbol-keyed methods are protocols rather than privacy.
