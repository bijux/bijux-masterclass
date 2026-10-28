# Module 3 — Functions, Scope, Closures, Callbacks, and `this`

> **Question:** What does a function capture, how can it be invoked, and which effects may occur per invocation?

## Why this comes now

Values become program behavior through functions. JavaScript functions are also objects, can capture lexical bindings, can be passed as data, and can receive a dynamic `this` value depending on invocation form. TypeScript can describe call signatures, but it does not control how many times a callback is called or whether an implementation stores it.

This module turns “callback” from an informal word into an explicit invocation contract.

## Outcomes

You can:

- distinguish declarations, expressions, arrows, and methods by behavior rather than style;
- trace lexical scope, temporal dead zones, and captured bindings;
- explain why closures capture bindings rather than frozen snapshots;
- specify callback count, ordering, storage, and failure behavior;
- choose arrow functions or ordinary functions based on `this` policy;
- inject time and other effects through small callable interfaces;
- prevent StudyLedger domain code from reading global time.

## 1. A function has several contracts

A callable boundary includes more than parameter and return types:

```ts
export type Clock = () => Date;
```

The type states that a call requires no argument and returns a `Date`. Product behavior must also answer:

- may it throw?
- may it return the same mutable `Date` object repeatedly?
- how many times will the caller invoke it?
- is the result used immediately or stored?
- does ordering among calls matter?

StudyLedger adopts a stronger policy: one application command asks the clock once, converts the result to an ISO string, and passes that value into pure domain transitions. Tests can then provide a deterministic clock.

## 2. Lexical scope and the temporal dead zone

`let` and `const` are block scoped. Their bindings exist from block entry but cannot be accessed before initialization:

```ts
{
  // console.log(topic); // ReferenceError at runtime
  const topic = 'closures';
  console.log(topic);
}
```

This is different from “the variable does not exist” and different from `var` hoisting behavior. The course uses `const` by default and `let` only for a binding that must be reassigned.

Function declarations are available throughout their containing scope, while function expressions follow the initialization rules of their binding. Do not select one only for aesthetics; understand when initialization occurs.

## 3. Closures capture bindings

```ts
function makeSequence(): () => number {
  let next = 1;
  return () => next++;
}

const sequence = makeSequence();
sequence(); // 1
sequence(); // 2
```

The returned function retains access to the `next` binding after `makeSequence` returns. It does not receive a copied immutable number. Each call reads and writes the same captured binding.

A loop illustrates the distinction:

```ts
const callbacks: Array<() => number> = [];
for (let index = 0; index < 3; index += 1) {
  callbacks.push(() => index);
}
```

Each iteration of a `let` loop creates the appropriate per-iteration binding, so the calls produce `0`, `1`, and `2`. A single outer mutable binding would produce a different result.

Draw capture ledgers:

| Closure | Captured binding | Reads | Writes | Lifetime consequence |
|---|---|---|---|---|
| sequence | `next` | current value | increment | binding retained while closure is reachable |

## 4. Invocation count is part of the API

This type is incomplete as a behavioral contract:

```ts
function inspect<T>(value: T, callback: (value: T) => void): void;
```

The implementation could call the callback zero times, once, twice, later, or after storing it. A public API should document the policy.

Array methods have defined callback behavior, but mutation during iteration can still make reasoning difficult. Your own higher-order functions should name:

- **count** — zero, at most once, exactly once, or once per item;
- **order** — source order, unspecified order, or grouped phases;
- **timing** — synchronously before return or asynchronously later;
- **storage** — callback is not retained or may outlive the call;
- **failure** — thrown errors propagate, are collected, or are translated.

## 5. `this` depends on invocation form

Ordinary functions receive `this` from the call:

```ts
const counter = {
  value: 0,
  increment(this: { value: number }): number {
    this.value += 1;
    return this.value;
  },
};

counter.increment(); // this === counter
```

Detaching the method changes the call:

```ts
const increment = counter.increment;
// increment(); // this is undefined in strict module code
```

Arrow functions do not have their own `this`; they use lexical `this`. This is useful for callbacks that should retain the surrounding method context, but arrows are not a universal method replacement.

A robust alternative is often to avoid hidden receiver state and pass required data explicitly:

```ts
function increment(value: number): number {
  return value + 1;
}
```

Course 2 returns to prototypes and method lookup. Course 1 requires enough `this` knowledge to avoid accidental receiver loss.

## 6. TypeScript callable types

Use type aliases to describe capabilities:

```ts
export type Predicate<T> = (value: T) => boolean;
export type Mapper<Input, Output> = (value: Input) => Output;
```

A function accepting a callback should require only the capability it uses. Do not claim a callback is asynchronous if the caller does not await it. This is a common defect:

```ts
function forEachWrong<T>(items: readonly T[], effect: (item: T) => Promise<void>): void {
  items.forEach(effect); // returned promises are ignored
}
```

The syntax type-checks under some contexts, but the function does not own the asynchronous work. Module 9 repairs this pattern. Here, learn to recognize that callable return values are part of the contract.

## 7. Inject effects rather than reading globals

A domain transition should not call `new Date()` internally:

```ts
function startSession(session: PlannedSession, startedAt: string): ActiveSession {
  return { ...session, status: 'active', startedAt };
}
```

The application layer supplies the time:

```ts
const now = clock().toISOString();
const updated = startSession(session, now);
```

This division gives one authority to time acquisition and keeps the transition deterministic. The same pattern later applies to random identifiers, environment variables, filesystem access, network clients, and loggers.

## 8. Error behavior in callbacks

A synchronous callback that throws normally unwinds through the caller unless caught:

```ts
function exactlyOnce<T>(value: T, effect: (value: T) => void): void {
  effect(value);
}
```

If the function promises “exactly once,” retrying after a throw could violate the contract by repeating an effect that partially succeeded. Count and failure policy must be designed together.

For Course 1, prefer small deterministic callbacks and keep external effects at named boundaries.

## 9. StudyLedger increment

Introduce dependencies:

```ts
export interface AppDependencies {
  readonly now: () => Date;
}
```

The application calls `now` at most once for a command that needs time. Domain transition functions accept the ISO timestamp as data. Tests use a fixed clock and verify call count.

Add pure functions for:

- allocating the next ID from a ledger value;
- creating a planned session;
- starting a session at a supplied timestamp.

Do not store a callback inside the ledger. The ledger is serializable domain state, not an effect container.

## 10. Common wrong models

### “A closure captures the value at creation”

It captures access to lexical bindings. Whether the observed value changes depends on the binding and surrounding code.

### “Arrow functions fix `this`”

They remove dynamic receiver binding. That is correct only when lexical `this` is the intended policy.

### “The callback type tells me how often it runs”

Call count and storage are behavioral contracts, not ordinary TypeScript syntax.

### “Injecting every function is architecture”

Inject effects whose nondeterminism or environment matters. Keep ordinary pure helpers as ordinary functions.

### “An async callback passed to `forEach` is awaited”

`forEach` ignores callback return values. Ownership of promises must be explicit.

## 11. The callable contract ledger

A function type such as `(value: Item) => Result` describes parameter and result relationships. It does not describe every behavior a caller may depend on. Record the missing dimensions explicitly:

| Dimension | Questions |
|---|---|
| timing | called synchronously, in a later microtask, or after I/O? |
| count | zero, once, at most N times, or until accepted? |
| order | source order, completion order, or unspecified? |
| retention | discarded before return or stored for later? |
| concurrency | can calls overlap? |
| failure | propagated, translated, retried, or ignored? |
| receiver | is a particular `this` value required? |

The Callback Budget lab exists because TypeScript cannot express “called at most N times, synchronously, in source order, and never retained” in an ordinary callable type. Documentation and tests carry that contract.

### Capture bindings, not frozen snapshots

A closure refers to bindings in its lexical environment:

```ts
let mode = 'draft';
const read = () => mode;
mode = 'published';
console.log(read()); // published
```

If a snapshot is required, create one deliberately:

```ts
const capturedMode = mode;
const readSnapshot = () => capturedMode;
```

This distinction matters with loops, configuration reloads, and callbacks registered for later execution. Ask whether the callback should observe the current binding or the value at registration time.

## 12. Invocation form determines `this`

The function body alone does not determine its receiver:

```ts
const counter = {
  value: 1,
  read() { return this.value; },
};

counter.read();       // receiver is counter
const read = counter.read;
// read();            // receiver is undefined in strict module code
read.call({ value: 9 });
```

An arrow function has lexical `this`; it does not receive a dynamic method receiver. That is useful for callbacks that should retain the enclosing receiver, but it is not a universal repair. Arrow properties also create one function per instance and change prototype behavior.

TypeScript’s pseudo-parameter makes a receiver requirement visible:

```ts
function read(this: { value: number }): number {
  return this.value;
}
```

It is erased from JavaScript and cannot be passed as an ordinary argument. It documents and checks invocation shape.

## 13. Function parameter variance in practical APIs

Under strict function checking, a callback that accepts only a narrower input cannot safely stand in for one that may receive a wider input:

```ts
interface Animal { name: string }
interface Dog extends Animal { bark(): void }

function visitAll(visit: (animal: Animal) => void): void {
  // The implementation is allowed to pass any Animal.
}

const dogOnly = (dog: Dog) => dog.bark();
// visitAll(dogOnly); // unsafe: visitAll may pass a non-Dog
```

The governing question is not “which type is more specific?” It is “what values may the caller legally supply?” Return types move in the opposite practical direction: a function returning a `Dog` can satisfy a requirement to return an `Animal`.

Course 3 of the wider program will formalize variance and library API design. Here, use it to avoid callbacks that claim less input capacity than the producer requires.

## 14. Sync and async callbacks are different contracts

JavaScript permits an `async` function where a callback’s return value is ignored:

```ts
items.forEach(async (item) => {
  await save(item);
});
```

`forEach` does not await those promises. The outer operation returns before saves complete, and rejections may become unowned.

Choose the control flow that states ownership:

```ts
for (const item of items) {
  await save(item); // sequential
}

await Promise.all(items.map((item) => save(item))); // started together; one owner
```

A callback API should state whether it observes returned promises. Do not infer asynchronous ownership from an `async` keyword at the call site.

## 15. Effect injection without a framework

StudyLedger injects `now`, `load`, and `save` as ordinary function values. This makes three nondeterministic boundaries explicit:

```ts
interface Dependencies {
  now(): Date;
  load(path: string): Promise<Ledger>;
  save(path: string, ledger: Ledger): Promise<void>;
}
```

The design is useful because tests can supply deterministic functions and because the application layer reveals the order in which effects occur. It would be harmful to abstract every string operation behind an interface. Inject effects and policy boundaries, not arbitrary implementation details.

A good dependency is small enough to fake faithfully and meaningful enough to represent one authority. The filesystem repository owns persistence. The clock owns current time. Neither owns domain transitions.

## Practice sequence

Complete the [workbook](workbook.md), then [Callback Budget](../../labs/module-03-callback-budget/README.md). Add a fixed clock to StudyLedger tests and prove the application does not call it for `help`, `version`, or read-only commands.

## Ready to continue

Continue when you can draw every captured binding, state the callback invocation policy, and explain the receiver of each ordinary function call.

Next: [Module 4 — Objects, Arrays, Identity, Mutation, and Immutable Updates](../module-04-objects-arrays-identity-and-mutation/index.md)
