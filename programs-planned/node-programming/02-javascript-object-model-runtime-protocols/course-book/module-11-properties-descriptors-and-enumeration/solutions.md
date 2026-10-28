# Module 11 Reasoned Solutions

## A. Descriptor prediction

Assignment creates an ordinary data property:

```text
value: 1
writable: true
enumerable: true
configurable: true
```

The minimal `Object.defineProperty` call creates:

```text
value: 1
writable: false
enumerable: false
configurable: false
```

Omitted descriptor Boolean fields default to `false`; they do not inherit assignment defaults.

The object-literal getter creates an accessor property with a getter, no setter, `enumerable: true`, and `configurable: true`. Assignment to a getter-only property fails in strict code. Because it is configurable, it can be deleted, made non-enumerable, or replaced with a data property. The property created by minimal `defineProperty` cannot be deleted or reconfigured, and its value cannot be changed.

The governing rule is descriptor state, not whether the property was written with concise syntax.

## B. Observation matrix

`Object.keys` returns enumerable own string keys. `Object.getOwnPropertyNames` returns all own string keys. `Object.getOwnPropertySymbols` returns all own symbol keys. `Reflect.ownKeys` returns all own string and symbol keys. `for...in` walks enumerable string keys across the prototype chain. Spread copies enumerable own string and symbol values. JSON ignores symbols and non-enumerable properties and uses its own value rules.

A correct answer names both the included set and the reason. “The symbol is hidden” is too vague: it may be visible to `Reflect.ownKeys` and `Object.getOwnPropertySymbols`.

## C. Getter-safe inspection

A principled repair uses descriptors as the observation surface:

```ts
function inspectShape(value: object): Record<string, string> {
  const report: Record<string, string> = Object.create(null) as Record<string, string>;

  for (const key of Object.getOwnPropertyNames(value)) {
    const descriptor = Object.getOwnPropertyDescriptor(value, key);
    if (descriptor === undefined) {
      continue;
    }

    if ('value' in descriptor) {
      report[key] = `data:${typeof descriptor.value}`;
    } else if (descriptor.get && descriptor.set) {
      report[key] = 'accessor:get+set';
    } else if (descriptor.get) {
      report[key] = 'accessor:get';
    } else {
      report[key] = 'accessor:set';
    }
  }

  return report;
}
```

The repair preserves the requirement that inspection must not execute application behavior. A weak repair wraps `Reflect.get` in `try/catch`; it still runs getters and merely handles some consequences after the effect occurred.

## D. Validation under prototype pollution

A counterexample is:

```ts
const inherited = { name: 'inherited' };
const candidate = Object.create(inherited) as object;
```

The original function accepts `candidate` even though it has no own `name` field.

A better boundary begins with `Object.hasOwn` and examines the own descriptor:

```ts
function hasOwnDataString(value: object, key: PropertyKey): boolean {
  const descriptor = Object.getOwnPropertyDescriptor(value, key);
  return descriptor !== undefined && 'value' in descriptor && typeof descriptor.value === 'string';
}
```

This deliberately rejects accessor-backed input. If the format allows accessors, that must be a separate explicit contract.

A null-prototype dictionary prevents collisions with `Object.prototype`, but keys and values can still be malformed. It is a representation decision, not a validator.

## E. Copy contract

Spread and `Object.assign` copy enumerable own values. They invoke getters, include enumerable symbols, omit non-enumerable keys, create ordinary writable/configurable data properties, and do not preserve the source prototype.

`structuredClone` creates a data clone according to the structured-clone algorithm. For ordinary user-defined class instances in Node, it does not reconstruct the custom prototype or methods. It does not preserve property descriptors as a runtime API clone. It is useful only when its supported data semantics match the product requirement.

`Object.create` with the source prototype and complete own descriptors preserves the shallow runtime surface without invoking getters. Nested values remain shared because this is a shallow descriptor clone.

Therefore:

- use descriptor-preserving `Object.create` when the contract is “same prototype and own-property semantics”;
- use an explicit plain-data snapshot for persistence, because persistence should not depend on runtime methods, symbols, accessors, or non-enumerable implementation metadata.

Using JSON or structured cloning simply because it feels “deep” is a weak repair. The choice must follow the representation contract.

## F. Laboratory

A complete Descriptor-Safe Settings implementation should separate public options from hidden metadata and should test every descriptor flag. The clone operation should use descriptors rather than value reads. Its tests should include a getter that throws if invoked; successful cloning proves the operation remained observational.

## G. ObjectAtlas transfer

The `id` property can be installed during construction with `Object.defineProperty`. The metadata symbol should be module-owned and non-enumerable. Attributes should use `Object.create(null)` and be exposed only through validated methods or snapshots.

A weak design spreads the instance into storage. That leaks whichever enumerable properties happen to exist today, loses private and symbol state unpredictably, and couples file compatibility to object layout. The principled design defines `toRecord()` or an equivalent explicit snapshot method whose fields are part of the storage contract.

## H. Reconstruction standard

A defensible answer connects each object operation to its observation surface. It does not say only that descriptors are “metadata.” Descriptor flags are executable constraints on assignment, enumeration, deletion, and future API evolution. It also distinguishes a symbol’s collision properties from privacy and distinguishes specified key order from a deliberate application ordering.
