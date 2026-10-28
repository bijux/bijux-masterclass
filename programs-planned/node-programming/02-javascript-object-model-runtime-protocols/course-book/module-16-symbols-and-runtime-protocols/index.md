# Module 16 — Symbols and Runtime Protocols

> **Question:** How can an object participate in language and host behavior without reserving ordinary string names or exposing accidental methods as public domain operations?

## Why this comes now

Module 15 composed behavior through explicit collaborators and methods. JavaScript also supports protocol participation through symbol-keyed properties. Well-known symbols connect ordinary objects to conversion, iteration, matching, construction, and inspection behavior. Node.js defines shared symbols for host-specific protocols such as custom inspection.

Symbols solve a narrow but important problem: independent code can agree on a property key that will not collide with ordinary user strings. They do not create privacy, and they do not make a protocol automatically well designed. A symbol method still needs input, output, side-effect, failure, and compatibility contracts.

ObjectAtlas uses symbol protocols sparingly. Nodes have a deliberate primitive-conversion policy, a custom debugging representation that does not leak hidden state, and iterable graph views. Persistence remains an explicit method because storage is too consequential to hide behind a generic conversion hook.

## Outcomes

By the end of this module, you can:

- distinguish unique symbols, registry symbols, and well-known symbols;
- explain symbol identity independently of symbol descriptions;
- use symbol keys without claiming secrecy;
- enumerate and describe symbol-keyed properties correctly;
- implement `Symbol.toPrimitive` with a coherent hint policy;
- use `Symbol.toStringTag` without treating it as runtime type proof;
- explain and selectively implement `Symbol.iterator`, `Symbol.hasInstance`, and `Symbol.species`;
- customize Node.js inspection without making program logic depend on debug output;
- design a protocol whose side effects and failure behavior remain explicit;
- decide when an ordinary named method is clearer than a symbol hook.

## 1. Symbol identity is not its description

Each direct `Symbol` call creates a unique primitive:

```ts
const first = Symbol('node');
const second = Symbol('node');

console.log(first === second); // false
console.log(first.description); // node
```

The description helps debugging. It is not the symbol’s identity.

A symbol can be a property key:

```ts
const revision = Symbol('revision');
const node = {
  id: 'root',
  [revision]: 3,
};
```

Ordinary string-key access cannot collide with `revision`, but reflective code can still discover it:

```ts
console.log(Object.getOwnPropertySymbols(node));
console.log(Reflect.ownKeys(node));
```

A symbol is therefore a namespace mechanism and capability token. It is not an access-control boundary.

## 2. The global symbol registry coordinates identity by string

`Symbol.for(key)` looks up or creates a symbol in the process-wide global registry:

```ts
const first = Symbol.for('object-atlas.inspect');
const second = Symbol.for('object-atlas.inspect');
console.log(first === second); // true
```

`Symbol.keyFor(symbol)` returns the registry key for registry symbols and `undefined` for unique symbols.

Use registry symbols when separately loaded code must agree on identity without importing the same exported constant. This can help cross-package protocols. It can also create ambient global coordination and accidental collisions if keys are vague.

Prefer an exported unique symbol when normal module imports can establish identity:

```ts
export const atlasMetadata: unique symbol = Symbol('atlasMetadata');
```

Prefer a namespaced registry key only when global agreement is truly required.

## 3. `unique symbol` preserves static identity

TypeScript’s `unique symbol` type can represent one specific symbol identity:

```ts
export const metadataKey: unique symbol = Symbol('metadata');

interface HasMetadata {
  readonly [metadataKey]: {
    readonly revision: number;
  };
}
```

A plain `symbol` type means any symbol. A `unique symbol` type refers to the specific declaration identity and is useful for protocol keys exported by a package.

Do not overuse symbol-keyed properties simply to make interfaces look advanced. If callers should discover and invoke an operation by name, a normal method is clearer.

## 4. Well-known symbols define language protocols

The `Symbol` constructor exposes well-known symbols whose identity is recognized by ECMAScript operations. Examples include:

- `Symbol.iterator`;
- `Symbol.asyncIterator`;
- `Symbol.toPrimitive`;
- `Symbol.toStringTag`;
- `Symbol.hasInstance`;
- `Symbol.species`;
- `Symbol.match`, `Symbol.replace`, `Symbol.search`, and `Symbol.split`;
- `Symbol.dispose` and `Symbol.asyncDispose` in explicit resource-management protocols.

A well-known symbol does not grant arbitrary magic. A particular language operation looks for that exact property and applies a specified calling contract.

Protocol review should record:

```text
triggering operation
symbol key
receiver
arguments or hint
expected result type
allowed side effects
failure behavior
compatibility obligation
```

## 5. Primitive conversion and `Symbol.toPrimitive`

When an object must be converted to a primitive, JavaScript may call `value[Symbol.toPrimitive](hint)`.

The hint is usually:

- `"string"`;
- `"number"`;
- `"default"`.

```ts
class Duration {
  constructor(readonly milliseconds: number) {
    if (!Number.isFinite(milliseconds) || milliseconds < 0) {
      throw new RangeError('duration must be finite and non-negative');
    }
  }

  [Symbol.toPrimitive](hint: string): string | number {
    if (hint === 'number') {
      return this.milliseconds;
    }
    return `${this.milliseconds}ms`;
  }
}

const duration = new Duration(250);
console.log(Number(duration)); // 250
console.log(String(duration)); // 250ms
```

The method must return a primitive. Returning an object throws.

Design conversion conservatively. Implicit arithmetic and string concatenation can call conversion in places readers do not expect. For domain types where ambiguity is dangerous—money, identifiers, timestamps—explicit methods such as `toMilliseconds()` or `format()` may be safer.

ObjectAtlas node conversion returns a stable human label for string contexts and refuses misleading numeric meaning. It does not use primitive conversion as serialization.

## 6. Ordinary fallback conversion

Without `Symbol.toPrimitive`, ordinary conversion generally tries `valueOf` and `toString` in an order influenced by the hint. Dates have special default behavior.

A legacy design that overloads both methods can be difficult to reason about:

```ts
const value = {
  valueOf(): number {
    return 10;
  },
  toString(): string {
    return 'ten';
  },
};
```

`Symbol.toPrimitive` centralizes the conversion policy, but an explicit named method remains better when conversion should never be implicit.

Never perform I/O, mutate domain state, or return unstable values from primitive conversion. Conversion can be triggered by logging, template literals, comparisons, property-key coercion, or debugging.

## 7. `Symbol.toStringTag` changes a label, not the object’s nature

```ts
class AtlasNode {
  get [Symbol.toStringTag](): string {
    return 'AtlasNode';
  }
}

const node = new AtlasNode();
console.log(Object.prototype.toString.call(node));
// [object AtlasNode]
```

The tag improves diagnostics. It does not prove class identity, private brand, or domain validity. Any object can define the same tag.

Do not use `Object.prototype.toString` with a custom tag as a trust boundary. Validation must inspect actual required data or use a controlled brand mechanism.

## 8. `Symbol.iterator` defines synchronous iteration

An iterable object has a method under `Symbol.iterator` that returns an iterator. Module 17 develops the full protocol.

```ts
class Pair<T> implements Iterable<T> {
  constructor(
    private readonly left: T,
    private readonly right: T,
  ) {}

  *[Symbol.iterator](): Iterator<T> {
    yield this.left;
    yield this.right;
  }
}
```

This lets `for...of`, spread, destructuring, and many collection constructors consume the object.

Iteration is a strong semantic commitment. It should represent the object’s obvious sequence. If an atlas can be traversed in preorder, postorder, breadth-first order, and source order, only one should become the default iterator. Others should be named methods.

## 9. `Symbol.hasInstance` customizes `instanceof`

A constructible object can define `Symbol.hasInstance` to customize `value instanceof Constructor`:

```ts
class EvenNumber {
  static [Symbol.hasInstance](value: unknown): boolean {
    return typeof value === 'number' && Number.isSafeInteger(value) && value % 2 === 0;
  }
}

console.log(4 instanceof EvenNumber); // true
```

This is legal but surprising: the right-hand side looks like a constructor relation while the implementation performs arbitrary classification.

Use it rarely. A named predicate such as `isEvenNumber(value)` is clearer and works naturally with TypeScript type predicates. Custom `instanceof` behavior can confuse tooling, maintainers, and cross-realm reasoning.

ObjectAtlas does not customize `instanceof`. Class private brands and explicit validation are clearer.

## 10. `Symbol.species` controls derived construction in selected built-ins

Some built-in subclass operations consult `constructor[Symbol.species]` to choose the constructor used for derived results. This appears in types such as `Array`, typed arrays, and some other built-ins depending on current language semantics.

Subclassing built-in collections can therefore have surprising result types and constructor behavior. Before relying on species:

- identify the exact methods that consult it;
- test the target runtime;
- decide whether subclassing the built-in is justified;
- consider composition around an ordinary collection.

The course does not use `Symbol.species` in ObjectAtlas. It is taught so that readers can recognize the protocol and avoid accidentally building a collection hierarchy around it.

## 11. Node.js custom inspection

Node.js exposes `util.inspect.custom`, a shared symbol used by `util.inspect` and console formatting.

```ts
import { inspect } from 'node:util';

class SecretLabel {
  constructor(private readonly visible: string) {}

  [inspect.custom](): string {
    return `SecretLabel<${this.visible}>`;
  }
}
```

The symbol is also available through the global registry key `nodejs.util.inspect.custom`.

Custom inspection is for diagnostics. Node’s documentation explicitly warns that `util.inspect` output is not a stable programmatic format. Therefore:

- do not parse it;
- do not use it for persistence;
- do not put secrets into it;
- bound output size;
- avoid expensive work and side effects;
- test only the stable part of your own custom representation, not incidental Node formatting.

ObjectAtlas uses custom inspection to show node ID, kind, label, and child count. It omits attributes that may contain sensitive or large values.

## 12. Protocol methods must preserve object invariants

Symbol hooks may be triggered implicitly. A robust protocol method should:

- avoid partial mutation;
- avoid hidden I/O;
- produce a value of the required type;
- remain bounded;
- preserve deterministic output where users rely on it;
- avoid leaking private state;
- document whether repeated calls are stable;
- throw only for meaningful contract violations.

A debugging hook that increments a read counter changes program behavior merely because an operator logs the object. A primitive conversion that reads the current time makes equality and output unstable. These are poor protocol designs even if the code is valid.

## 13. Symbols versus private fields versus module scope

Choose based on the requirement:

| Requirement | Suitable mechanism |
|---|---|
| Avoid collision with string keys | symbol |
| Share one protocol key across imported code | exported `unique symbol` |
| Share identity across separately loaded packages | carefully namespaced `Symbol.for` |
| Runtime per-instance encapsulation | `#private` |
| Module-internal capability not exposed to callers | unexported symbol or closure |
| Truly discoverable public method | ordinary named method |

An unexported symbol is difficult for ordinary callers to name, but reflection can still discover the key. If secrecy or authority matters, do not expose the object with a powerful symbol method and assume the key is invisible.

## 14. ObjectAtlas increment

Add three deliberate protocols:

1. `AtlasNode[Symbol.toPrimitive]` returns the node ID for string/default hints and rejects or returns a deliberate numeric policy rather than accidental `NaN`;
2. `AtlasNode[Symbol.toStringTag]` improves generic diagnostics without serving as a validator;
3. `AtlasNode[util.inspect.custom]` returns a bounded, secret-safe summary.

Also define one exported `unique symbol` for an internal read-only metadata capability used by trusted atlas components. Do not place persistence or graph mutation behind a symbol hook.

Tests must prove:

- same descriptions do not make symbols equal;
- the exported symbol has one stable identity across imports;
- ordinary enumeration omits the metadata key;
- `Reflect.ownKeys` can still observe it;
- custom inspection omits large attributes;
- primitive conversion is stable and side-effect free;
- `Symbol.toStringTag` does not make a counterfeit object valid.

## Common wrong models

### “Symbols are private fields”

They are property keys with special identity and enumeration behavior. Reflection can find them.

### “The symbol description identifies the symbol”

Descriptions are not identity. `Symbol('x') !== Symbol('x')`.

### “`Symbol.for` is always better because it is reusable”

It creates global registry coordination. Prefer imported unique symbols when possible.

### “A custom tag proves the object type”

`Symbol.toStringTag` changes a diagnostic label.

### “Implicit conversion is convenient, so it should do domain work”

Conversion can happen unexpectedly. Keep it pure, bounded, and unsurprising.

### “Custom inspect output is a serialization format”

It is debugging output and may change. Persistence needs a separate explicit contract.

## Practice sequence

1. Compare unique symbols with registry symbols and record their identities.
2. Build an object with symbol and string keys and enumerate every surface.
3. Implement a value object with a conservative `Symbol.toPrimitive` policy.
4. Create a counterfeit `Symbol.toStringTag` and prove it passes only the label check.
5. Write a bounded Node custom-inspection method that redacts a secret.
6. Complete the Protocol-Aware Value Object laboratory.
7. Add ObjectAtlas protocols and negative tests.
8. Defend one operation that should remain a named method instead of becoming a symbol protocol.

## Ready to continue

Continue when you can identify the exact operation that triggers each well-known symbol, the required return type, and the side effects that would make the protocol unsafe or surprising. You must also be able to explain why symbol identity, private-brand identity, and class identity are different.

Module 17 takes the most important collection protocol—synchronous iteration—and develops its state machine, cleanup behavior, and generator implementation in depth.

## Primary references

- ECMAScript Language Specification: Symbol values and well-known symbol protocols.
- Node.js `util.inspect` documentation: custom inspection functions and `util.inspect.custom`.
- TypeScript Handbook: `unique symbol`, computed properties, iterables, and symbol-keyed members.

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory 16 — Protocol-Aware Value Object](../../labs/module-16-protocol-aware-value-object/README.md)
- [ObjectAtlas engineering guide](../capstone.md)
