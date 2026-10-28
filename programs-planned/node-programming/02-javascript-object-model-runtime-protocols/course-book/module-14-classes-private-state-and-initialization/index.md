# Module 14 — Classes, Fields, Private State, and Initialization

> **Question:** Which parts of a JavaScript class are syntax over prototypes, which parts create new runtime semantics, and when is an instance fully valid?

## Why this comes now

The preceding modules established property descriptors, prototype lookup, receivers, and construction. Class syntax organizes those mechanisms, but it also introduces semantics that are not captured by the phrase “classes are syntax sugar.” Public fields are installed during construction. Private fields use a private-name brand that ordinary property reflection cannot forge. Static fields and blocks initialize the constructor object. Derived constructors must call `super` before using `this`, and initialization order can make overridable methods observe partially initialized state.

A class should therefore be understood as two related runtime surfaces:

```text
constructor object and static members
             ↓ constructs
instance objects with private and public state
             ↓ delegate
prototype methods and accessors
```

ObjectAtlas uses a class only where it earns its cost: a node has identity-bearing private state and invariants that must survive every public method. Plain records remain the persistence format, and capability objects remain preferable for replaceable collaborators.

## Outcomes

By the end of this module, you can:

- distinguish a class’s constructor/static side, prototype, and instance side;
- explain where methods, public fields, private fields, accessors, and static fields live;
- predict base and derived initialization order;
- use private fields and private methods as runtime brand-protected state;
- distinguish TypeScript `private` from ECMAScript `#private`;
- use static factories and static blocks without hiding uncontrolled effects;
- explain why calling overridable methods from constructors is hazardous;
- design inheritance only when substitutability and initialization remain clear;
- choose classes, plain objects, closures, or composition from the required authority model;
- test an instance’s public behavior without coupling to private representation.

## 1. A class creates a constructor and a prototype

```ts
class AtlasNode {
  describe(): string {
    return 'node';
  }
}
```

At runtime:

- `AtlasNode` is a function object used as a constructor;
- `AtlasNode.prototype` is an object containing `describe` and `constructor`;
- instances created with `new AtlasNode()` have `AtlasNode.prototype` in their prototype chain.

```ts
const node = new AtlasNode();

console.log(typeof AtlasNode); // function
console.log(Object.getPrototypeOf(node) === AtlasNode.prototype); // true
console.log(Object.hasOwn(node, 'describe')); // false
console.log(Object.hasOwn(AtlasNode.prototype, 'describe')); // true
```

Class declarations execute in strict mode. Class methods are non-enumerable on the prototype. Unlike ordinary function declarations, class constructors cannot be called without `new`.

Calling a class “only syntax sugar” hides private fields, field initialization order, strictness, and other class-specific behavior. Calling it a completely separate object system hides the prototype machinery underneath it. Use the layered model instead.

## 2. The instance side and static side are different types

In TypeScript:

```ts
class Parser {
  static readonly format = 'atlas-v1';

  parse(input: string): number {
    return input.length;
  }
}
```

- the type `Parser` describes instances;
- the value `Parser` is the constructor object;
- the type `typeof Parser` describes the constructor object and static members.

```ts
function useInstance(parser: Parser): number {
  return parser.parse('x');
}

function useConstructor(parserClass: typeof Parser): string {
  return parserClass.format;
}
```

This distinction matters in factories, dependency injection, subclass construction, and plugin registries. A constructor type may need an explicit `new` signature rather than the exact `typeof` a specific class.

## 3. Public fields are own properties

A public instance field is initialized on each instance:

```ts
class Counter {
  count = 0;
}

const first = new Counter();
const second = new Counter();

console.log(Object.hasOwn(first, 'count')); // true
first.count += 1;
console.log(second.count); // 0
```

This avoids the shared-mutable-prototype trap from Module 12. Each instance receives its own `count` value.

Field initializers run as part of construction. In a base class they run before the constructor body. In a derived class they run after `super()` returns and before the remaining derived-constructor statements.

The exact descriptor of a normal public field is an ordinary writable, enumerable, configurable data property. If a field needs a different public descriptor contract, define it explicitly rather than assuming class syntax does so.

## 4. Private fields are runtime state, not string-key properties

```ts
class Balance {
  #amount = 0;

  deposit(value: number): void {
    if (!Number.isSafeInteger(value) || value <= 0) {
      throw new RangeError('deposit must be a positive safe integer');
    }
    this.#amount += value;
  }

  read(): number {
    return this.#amount;
  }
}
```

`#amount` is not a property keyed by the string `"#amount"`. It is a private name checked against the receiver’s private brand.

Consequences:

- `Reflect.ownKeys(instance)` cannot reveal it;
- bracket notation cannot access it;
- a proxy around the instance may fail when methods use the proxy as receiver;
- `Object.create(Balance.prototype)` does not install the brand;
- subclasses cannot access a base class’s private field directly;
- each class declaration creates a distinct private name even if the spelling matches.

This is real runtime encapsulation, subject to the class’s public methods. It is not cryptographic secrecy: a public method can expose the data, a debugger can inspect process memory, and the class can deliberately leak references.

## 5. TypeScript `private` and ECMAScript `#private`

TypeScript also supports the `private` modifier:

```ts
class LegacyPrivacy {
  private amount = 0;
}
```

That restriction is primarily enforced by the TypeScript checker. Depending on target and emission, the runtime property may still be an ordinary named property. ECMAScript `#amount` is enforced by the runtime brand mechanism.

Use `#private` when runtime encapsulation is part of the design. Use TypeScript visibility modifiers for static API guidance where runtime hiding is unnecessary. Do not claim that a TypeScript-only private member is unreachable from emitted JavaScript.

The course favors `#private` for invariant-bearing instance state and plain closures for truly local module state.

## 6. Private methods and static private state

Private names can refer to methods, accessors, and static members:

```ts
class Token {
  static #issued = 0;

  #value: string;

  constructor(value: string) {
    this.#value = value;
    Token.#issued += 1;
  }

  #normalized(): string {
    return this.#value.trim().toLowerCase();
  }

  equals(other: Token): boolean {
    return this.#normalized() === other.#normalized();
  }

  static issuedCount(): number {
    return Token.#issued;
  }
}
```

Private state follows the class that declares it. `this.#issued` would be wrong for a static private field because the receiver and declaration authority differ.

Global static counters introduce process-wide state. They may be useful for metrics or identity factories, but they complicate tests and multiple isolated instances. Prefer instance-owned authorities when independent application contexts must coexist.

## 7. Static factories can separate parsing from valid construction

A static factory can validate raw input while keeping the constructor focused on already-valid state:

```ts
class NodeId {
  readonly value: string;

  private constructor(value: string) {
    this.value = value;
  }

  static parse(raw: string): NodeId {
    const value = raw.trim();
    if (!/^[a-z][a-z0-9-]{0,31}$/.test(value)) {
      throw new TypeError(`invalid node id: ${raw}`);
    }
    return new NodeId(value);
  }
}
```

The TypeScript-private constructor prevents ordinary typed callers from using `new NodeId`. At runtime, emitted JavaScript privacy depends on the emitted class shape; the invariant is also protected because only module code exports the class and raw data is validated before public use.

When runtime-enforced private construction is essential, a module-scoped token or closure factory may be needed. Do not assume the TypeScript `private constructor` is an ECMAScript private brand.

## 8. Static blocks initialize the constructor object

Static fields and blocks run when the class definition is evaluated:

```ts
class Registry {
  static readonly builtIns = new Map<string, string>();

  static {
    Registry.builtIns.set('folder', 'container node');
    Registry.builtIns.set('note', 'leaf node');
  }
}
```

A static block has access to private static state and can perform multi-step initialization. It also creates module-evaluation effects. Keep those effects deterministic, synchronous, and bounded.

Do not read environment variables, perform I/O, or register global listeners in a static block unless module import is deliberately the authority for those effects. Hidden import-time effects make tests, tooling, and application startup harder to reason about.

## 9. Base-class initialization order

For a base class:

1. the instance is created;
2. instance field initializers run in source order;
3. the constructor body runs.

```ts
class Base {
  first = this.trace('first');
  second = this.trace('second');

  constructor() {
    this.trace('constructor');
  }

  trace(label: string): string {
    console.log(label);
    return label;
  }
}
```

This prints field initialization before constructor-body output.

Field initializers can refer to earlier initialized fields. Referring to later fields may observe `undefined` or trigger TypeScript warnings depending on the code. Keep initialization order obvious and avoid complex cross-field effects.

## 10. Derived-class initialization order

A derived constructor must call `super()` before using `this`.

Conceptually:

1. the base constructor begins the instance construction;
2. base fields initialize;
3. the base constructor body runs;
4. `super()` returns to the derived constructor;
5. derived fields initialize;
6. the rest of the derived constructor body runs.

```ts
class Base {
  name = 'base';

  constructor() {
    console.log(this.name);
  }
}

class Derived extends Base {
  override name = 'derived';
}

new Derived(); // base constructor observes 'base'
```

The derived field override has not run while the base constructor is executing.

This becomes more dangerous when the base constructor calls an overridable method.

## 11. Do not call overridable methods from constructors

```ts
class BaseLoader {
  constructor() {
    this.load();
  }

  load(): void {}
}

class FileLoader extends BaseLoader {
  #path: string;

  constructor(path: string) {
    super();
    this.#path = path;
  }

  override load(): void {
    console.log(this.#path); // private field not installed yet when called by base constructor
  }
}
```

During `super()`, dynamic dispatch can reach the derived override before derived private fields are initialized. The result may be a private-brand error or partially initialized behavior.

Principled repairs:

- keep constructors limited to local state establishment;
- invoke overridable lifecycle methods only after complete construction;
- use a static async or validating factory that constructs, then initializes;
- prefer composition when base construction depends on replaceable behavior.

A weak repair makes derived fields optional and sprinkles undefined checks. That normalizes invalid intermediate state instead of removing the dangerous call.

## 12. Inheritance must preserve substitutability

Inheritance is not merely code reuse. A derived instance is accepted where a base instance is expected. It must preserve the base public contract.

Warning signs:

- derived methods reject inputs accepted by the base;
- derived methods return weaker results;
- base invariants are bypassed;
- initialization requires callers to know the concrete subclass;
- the hierarchy exists only to share two helper methods;
- subclasses switch behavior by inspecting their own class name.

Prefer composition when behaviors vary independently. Use inheritance when there is one stable substitutable abstraction with shared construction and state semantics.

Course 3 will study advanced TypeScript API design. Here the goal is to avoid a class hierarchy that conflicts with JavaScript runtime initialization.

## 13. Private fields and proxies

Consider:

```ts
class Secret {
  #value = 1;

  read(): number {
    return this.#value;
  }
}

const original = new Secret();
const proxy = new Proxy(original, {});
// proxy.read() may throw because this is the proxy, which lacks Secret's private brand
```

A transparent-looking proxy is not transparent to private fields. A handler can bind methods back to the target, but that changes method identity, accessor receivers, and general forwarding behavior.

The safest rule for ObjectAtlas is:

> Do not proxy invariant-bearing class instances. Proxy a plain draft record with an explicit contract.

Module 18 explains proxy invariants and forwarding in detail.

## 14. Testing classes through contracts

Private state should not force tests to break encapsulation. Test:

- constructor and factory validation;
- public state transitions;
- error behavior;
- descriptor and prototype surfaces that are public commitments;
- independence between instances;
- reconstruction from persisted data;
- behavior under subclassing only if subclassing is supported.

Do not use string-key casts to access private fields. That does not work for ECMAScript private names and encourages tests to depend on representation.

If an invariant is hard to observe through public behavior, ask whether the public contract is underspecified or whether the test is targeting an implementation detail.

## 15. ObjectAtlas increment

Implement `AtlasNode` as the first invariant-bearing class.

Required state:

- validated immutable `NodeId`;
- `#kind` and `#label` with validated transitions;
- `#parentId` as `NodeId | null`;
- `#childIds` as an instance-owned array not exposed mutably;
- `#attributes` as a null-prototype record;
- prototype methods for reads and state transitions;
- an explicit plain-data `toRecord()` snapshot;
- a static `fromRecord()` validation boundary.

Rules:

- construction creates a fully valid node;
- methods never expose private mutable containers;
- no base constructor calls overridable behavior;
- the class is not designed for subclassing unless a later requirement justifies it;
- tests prove separate instances do not share child or attribute state;
- tests prove a counterfeit prototype object lacks the private brand.

## Common wrong models

### “Classes replace prototypes”

Class instances still delegate to class prototypes.

### “Private fields are hidden string properties”

They use private names and brand checks outside ordinary property reflection.

### “TypeScript `private` and `#private` are equivalent”

One is primarily a checker restriction; the other is an ECMAScript runtime mechanism.

### “Fields run before everything in the constructor”

Base and derived field timing differ. Derived fields do not exist before `super()` returns.

### “Calling a method from a constructor is normal reuse”

If the method is overridable, it may observe an incompletely initialized derived instance.

### “Inheritance is the standard way to share methods”

Prototype methods already share behavior. Inheritance also promises substitutability and coupled initialization.

## Practice sequence

1. Inspect the own and prototype keys of a simple class instance.
2. Compare TypeScript `private` with `#private` in emitted and runtime behavior.
3. Trace base and derived field initialization in source order.
4. Repair a constructor that calls an overridable method.
5. Compare a class with private fields to a closure-based factory.
6. Complete the Private Counter Bank laboratory.
7. Implement the full `AtlasNode` invariant surface.
8. Defend why ObjectAtlas uses a class for nodes but plain records for persistence.

## Ready to continue

Continue when you can draw the constructor object, prototype object, instance own properties, and private state as separate surfaces. You must be able to trace derived initialization and explain why a valid instance cannot be produced by merely changing a plain object’s prototype.

Module 15 turns from one invariant-bearing class to multi-capability object architecture. The question changes from “how is one object initialized?” to “how should independent behaviors be composed?”

## Primary references

- ECMAScript Language Specification: class definitions, fields, private names, constructors, and derived initialization.
- TypeScript Handbook: classes, visibility, static members, constructor types, and `override`.
- Node.js runtime conventions for module evaluation and avoiding hidden import-time effects.

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory 14 — Private Counter Bank](../../labs/module-14-private-counter-bank/README.md)
- [ObjectAtlas engineering guide](../capstone.md)
