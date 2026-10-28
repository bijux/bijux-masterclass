# Module 13 — Functions, Receivers, Constructors, and `new`

> **Question:** When a function runs, how were its arguments, receiver, construct target, and lexical environment chosen—and which of those facts survive when the function is passed elsewhere?

## Why this comes now

Course 1 introduced functions, closures, callbacks, and the most visible `this` pitfalls. Module 12 showed that method lookup and invocation are separate stages: a function can be found on a prototype but still run with the original object as receiver. This module makes that call model precise.

JavaScript functions are objects. Some can be called, some can be constructed, some can do both, and arrows can be called but cannot be constructed. `call`, `apply`, and `bind` alter invocation. `new` performs a sequence of object-creation steps rather than merely calling a function with special punctuation. Method extraction loses the reference base that supplied `this`. Bound functions preserve a chosen receiver for ordinary calls but interact differently with construction.

ObjectAtlas has callbacks for traversal, formatting, and command execution. Those APIs must state whether they call a function as a plain callback, as a method, with a specific receiver, once, or many times. Receiver accidents must not become hidden product state.

## Outcomes

By the end of this module, you can:

- distinguish callable and constructible function objects;
- derive `this` from the call expression rather than the function’s source location;
- explain why method extraction changes behavior;
- use explicit `this` parameters in TypeScript callback contracts;
- choose among ordinary functions, arrow functions, bound functions, and object methods;
- trace `call`, `apply`, and `bind` without treating them as interchangeable;
- state the conceptual steps performed by `new`;
- explain constructor return-value rules and `new.target`;
- distinguish a constructor function’s instance prototype from its own function-object behavior;
- design receiver-safe APIs and adapters.

## 1. Functions are values with callable behavior

A function declaration creates a function object:

```ts
function add(left: number, right: number): number {
  return left + right;
}

console.log(typeof add);       // function
console.log(add.name);         // add
console.log(add.length);       // 2
console.log(Object.getPrototypeOf(add) === Function.prototype); // true
```

Function objects can own properties, participate in prototype relationships, and be passed like other values. Their important internal capabilities include:

- `[[Call]]`: the object can be invoked as a function;
- `[[Construct]]`: the object can be invoked with `new`.

Not every callable is constructible. Arrow functions have `[[Call]]` but not `[[Construct]]`:

```ts
const factory = (id: string) => ({ id });
// new factory('x') // runtime TypeError; TypeScript rejects it
```

Methods defined with concise method syntax are also not ordinarily constructible:

```ts
const service = {
  run(): void {},
};
// new service.run() // TypeError
```

A function’s usability as a constructor is a runtime capability, not a naming convention.

## 2. `this` is selected by invocation

For ordinary non-arrow functions, `this` is determined by how the function is called.

```ts
function identify(this: { id: string }): string {
  return this.id;
}

const item = { id: 'item-1', identify };
console.log(item.identify()); // item-1
```

The call expression contains a reference with base object `item`. That base becomes the receiver.

Compare:

```ts
const detached = item.identify;
// detached(); // TypeScript rejects because the explicit this requirement is missing
```

At runtime in ESM strict mode, a plain detached call receives `undefined` as `this`. The function did not carry `item` with it. The method relationship existed in the reference expression `item.identify()`, not permanently inside the function value.

Use this call-site ledger:

| Call form | Ordinary `this` |
|---|---|
| `object.method()` | `object` |
| `functionValue()` in strict mode | `undefined` |
| `functionValue.call(receiver, ...)` | supplied receiver |
| `functionValue.apply(receiver, args)` | supplied receiver |
| `boundFunction(...)` | receiver captured by `bind` for ordinary calls |
| arrow call | lexical `this` from surrounding scope |
| `new Constructor(...)` | newly created instance receiver, subject to constructor rules |

## 3. TypeScript’s explicit `this` parameter documents the contract

A TypeScript `this` parameter is erased from emitted JavaScript. It constrains call sites and documents receiver requirements.

```ts
interface NodeView {
  readonly id: string;
}

function render(this: NodeView, prefix: string): string {
  return `${prefix}${this.id}`;
}
```

The `this` parameter does not count as a runtime argument. It helps prevent accidental detached calls and clarifies adapter requirements.

A callback that must not depend on `this` can say so:

```ts
type Visitor<T> = (this: void, value: T) => void;
```

This is useful for collection and traversal APIs. It prevents callers from supplying a method that silently expects an object receiver.

Do not add explicit `this` parameters everywhere. Use them when receiver behavior is part of the public contract or when detached use is plausible.

## 4. Arrow functions capture lexical `this`

An arrow does not receive a dynamic receiver from call syntax. It closes over `this` from the surrounding lexical environment.

```ts
class Counter {
  #value = 0;

  readonly increment = (): number => {
    this.#value += 1;
    return this.#value;
  };
}

const counter = new Counter();
const detached = counter.increment;
console.log(detached()); // 1
```

The field initializer creates a distinct arrow function per instance. That preserves receiver behavior during extraction, but it also changes memory identity and prototype sharing:

```ts
const first = new Counter();
const second = new Counter();
console.log(first.increment === second.increment); // false
```

A prototype method would be shared but require receiver-safe invocation.

Use an arrow field when stable extracted callback identity is genuinely part of the API. Do not replace every method with an arrow simply to avoid learning call semantics.

## 5. `call` and `apply` perform an invocation now

`call` accepts the receiver followed by ordinary arguments:

```ts
function format(this: { id: string }, prefix: string, suffix: string): string {
  return `${prefix}${this.id}${suffix}`;
}

const value = format.call({ id: 'n1' }, '[', ']');
```

`apply` accepts the receiver and an array-like argument list:

```ts
const args: [string, string] = ['[', ']'];
const same = format.apply({ id: 'n1' }, args);
```

Both invoke immediately. They do not create a new reusable function.

Modern code often uses spread instead of `apply` when only argument-array expansion is required:

```ts
const result = format.call({ id: 'n1' }, ...args);
```

The important design question is not syntax preference. It is who owns receiver selection. A framework that calls handlers with an undocumented receiver creates invisible coupling.

## 6. `bind` creates a new function object

`bind` returns a new bound function that remembers a receiver and optionally leading arguments:

```ts
const bracketed = format.bind({ id: 'n1' }, '[');
console.log(bracketed(']')); // [n1]
```

Consequences:

- the bound function has a different identity;
- repeated `bind` calls create different functions;
- removing listeners by identity fails if code binds again during removal;
- leading arguments reduce the visible `length` metadata;
- for ordinary calls, later `call` or `apply` cannot replace the bound receiver.

```ts
const first = item.identify.bind(item);
const second = item.identify.bind(item);
console.log(first === second); // false
```

Store the bound function when identity matters.

Binding is a valid adapter. It is weak when used to hide an unclear receiver contract across an entire architecture.

## 7. The conceptual work performed by `new`

For an ordinary constructible function `Constructor`, a `new Constructor(args)` expression conceptually:

1. creates a new object;
2. chooses its internal prototype from `Constructor.prototype` if that value is an object, otherwise uses an ordinary fallback;
3. calls `Constructor` with the new object as receiver and with `new.target` set;
4. if the constructor returns an object, uses that returned object;
5. otherwise returns the newly created receiver.

Example:

```ts
function Entry(this: { id: string }, id: string): void {
  this.id = id;
}
Entry.prototype.describe = function describe(this: { id: string }): string {
  return this.id;
};

const entry = new Entry('e1');
```

The constructor body initializes own state. The prototype object supplies shared behavior.

## 8. Constructor return values can replace the instance

A constructor that returns a primitive does not replace the newly created receiver:

```ts
function PrimitiveReturn(this: { value: number }): number {
  this.value = 1;
  return 99;
}

const value = new PrimitiveReturn();
console.log(value.value); // 1
```

A constructor that returns an object replaces it:

```ts
function ObjectReturn(this: { value: number }): { replacement: true } {
  this.value = 1;
  return { replacement: true };
}

const replacement = new ObjectReturn();
```

TypeScript constructor typing and JavaScript runtime rules can make unusual constructor-return designs awkward. Prefer constructors that establish the class instance. Use a factory when the operation may return different representations.

## 9. `new.target` identifies construction

Inside an ordinary function or class constructor, `new.target` indicates the constructor invoked by `new`.

```ts
function RequiredNew(this: object): void {
  if (new.target === undefined) {
    throw new TypeError('RequiredNew must be constructed');
  }
}
```

In a base class constructor called through a subclass, `new.target` refers to the most-derived constructor. This supports abstract-construction checks and factory-like behavior, but it also couples construction logic to inheritance.

Do not use `new.target` as a substitute for a clear API. If callers should use `createNode`, export a factory and keep the constructor private where TypeScript can enforce that boundary.

## 10. Bound functions and construction

A bound function used with `new` does not use the bound receiver. Construction must create a new receiver. Bound leading arguments still apply, and `new.target` behavior follows specification rules.

```ts
function Point(this: { x: number; y: number }, x: number, y: number): void {
  this.x = x;
  this.y = y;
}

const PointAtX1 = Point.bind({ ignored: true }, 1);
const point = new PointAtX1(2);
console.log(point); // instance with x=1, y=2
```

This is another reason not to summarize `bind` as “permanently sets `this`.” It sets the receiver for ordinary calls; construction has different receiver semantics.

## 11. Method extraction in real Node.js APIs

Method extraction errors appear in callback registration:

```ts
class Registry {
  #items: string[] = [];

  add(value: string): void {
    this.#items.push(value);
  }
}

const registry = new Registry();
const values = ['a', 'b'];
// values.forEach(registry.add); // receiver is not registry
```

Principled repairs include:

```ts
values.forEach((value) => registry.add(value));
```

or a deliberately stable bound adapter stored once:

```ts
const addToRegistry = registry.add.bind(registry);
values.forEach(addToRegistry);
```

The arrow wrapper makes the receiver dependency visible at registration. Binding creates a reusable callback identity. Choose from lifecycle requirements, not style preference.

Passing a method directly is safe only if it does not use `this`, or if the receiving API explicitly invokes it with the required receiver.

## 12. Functions as objects and static responsibility

A function object can carry metadata:

```ts
interface ParserFunction {
  (input: string): number;
  readonly formatName: string;
}

const parseCount = Object.assign(
  (input: string): number => Number.parseInt(input, 10),
  { formatName: 'decimal-count' },
) satisfies ParserFunction;
```

This pattern can be useful for small callable strategies. It should not become an untyped bag of mutable configuration. If metadata has lifecycle, validation, or multiple methods, an ordinary object may be clearer.

TypeScript distinguishes the instance side of a class from its static/constructor side. A variable of type `typeof AtlasNode` refers to the constructor object and static members; `AtlasNode` as a type name refers to instances. Module 14 develops that distinction.

## 13. Receiver-safe API design

A public callback API should answer:

- Is the callback called as a plain function?
- Is `this` always `undefined`?
- Is a receiver supplied deliberately?
- How many times may it run?
- May it be retained after the call?
- May it throw?
- Is its identity used for later removal?

A strong traversal contract is:

```ts
export type NodeVisitor<T> = (
  this: void,
  node: T,
  depth: number,
) => void;
```

The callback receives all required context as parameters. It does not depend on an invisible receiver.

A method-oriented extension point may intentionally use a receiver:

```ts
interface Renderer {
  render(node: NodeView): string;
}
```

The architecture then passes a renderer object and calls `renderer.render(node)` rather than extracting the method.

## 14. ObjectAtlas increment

Add receiver-safe public behavior:

- `AtlasNode` methods remain prototype methods;
- traversal callbacks use `this: void` and receive node/depth explicitly;
- no command handler is registered by extracting an unbound instance method;
- any bound callback used for later removal is created once and retained;
- factories are used for reconstruction when creation can fail;
- tests cover method calls, detached-method rejection, explicit adapters, and callback identity.

Also add a small reflective command that reports whether a value is callable, constructible under the course’s controlled test, and which own metadata fields the function object exposes. Do not attempt to infer universal constructibility by calling arbitrary untrusted functions.

## Common wrong models

### “`this` belongs to the function”

Ordinary-function receivers are selected by invocation. Arrows capture lexical `this`.

### “A method remains attached when stored in a variable”

Property access produces a function value. A later plain call has no original base object.

### “`bind` changes the original function”

It creates a new bound function object.

### “Bound `this` also controls construction”

`new` creates its own receiver. Bound arguments still participate.

### “`new` just calls the constructor”

It creates an object, selects a prototype, establishes receiver and `new.target`, then applies constructor-return rules.

### “Any function can be used with `new`”

Constructibility is a separate runtime capability.

## Practice sequence

1. Predict `this` for eight call forms before execution.
2. Repair a detached method passed to an array callback.
3. Compare a prototype method, arrow field, and stored bound method for identity and memory shape.
4. Trace a constructor that returns a primitive and one that returns an object.
5. Use an explicit `this: void` callback type and observe rejected receiver-dependent functions.
6. Complete the Receiver-Safe Command Adapter laboratory.
7. Add ObjectAtlas traversal callback contracts and adapter tests.
8. Defend where the architecture uses objects with methods and where it uses plain functions.

## Ready to continue

Continue when you can derive receiver and construction behavior from the call expression, not from the function’s name or source location. You should be able to explain the instance prototype chosen by `new`, the role of `new.target`, and why a bound callback’s identity must often be retained.

Module 14 uses class syntax to package constructor, prototype, private state, fields, and static behavior. The call model from this module remains underneath every class method.

## Primary references

- ECMAScript Language Specification: function objects, call expressions, bound functions, `[[Call]]`, `[[Construct]]`, and `new` expressions.
- TypeScript Handbook: functions, explicit `this` parameters, classes, and constructor types.
- Node.js API conventions for callbacks and listener removal, where function identity and receiver behavior matter.

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory 13 — Receiver-Safe Command Adapter](../../labs/module-13-receiver-safe-command-adapter/README.md)
- [ObjectAtlas engineering guide](../capstone.md)
