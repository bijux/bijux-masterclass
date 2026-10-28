# Module 13 Workbook

The work in this module is call-site analysis. For every prediction, write the function value, call form, receiver, arguments, and whether construction is involved.

## A. Receiver table

Predict the result or failure for each call:

```ts
function read(this: { value: number }): number {
  return this.value;
}

const object = { value: 3, read };
const detached = object.read;
const bound = object.read.bind({ value: 4 });

object.read();
detached.call({ value: 5 });
bound();
bound.call({ value: 6 });
```

Add an arrow created inside an object method and explain which `this` it captures.

## B. Method extraction repair

Repair this registration system in two different ways:

```ts
class Reporter {
  #prefix = 'report';

  write(message: string): string {
    return `${this.#prefix}:${message}`;
  }
}

const handlers = new Set<(message: string) => string>();
const reporter = new Reporter();
handlers.add(reporter.write);
```

One repair should use an arrow adapter. The other should retain one bound function so it can later be removed by identity. Compare lifecycle consequences.

## C. Arrow field versus prototype method

Implement both versions of a counter. Compare:

- `first.method === second.method`;
- detached-call behavior;
- location in `Reflect.ownKeys(instance)`;
- location in `Reflect.ownKeys(Object.getPrototypeOf(instance))`;
- ability to override or replace behavior;
- memory and identity implications.

State which form you would use for an event listener that must be removed later.

## D. `new` trace

Trace these constructors step by step:

```ts
function A(this: { x: number }): void {
  this.x = 1;
}

function B(this: { x: number }): number {
  this.x = 1;
  return 7;
}

function C(this: { x: number }): { y: number } {
  this.x = 1;
  return { y: 2 };
}
```

For each, identify the result object and prototype. Then change one `.prototype` property to a primitive before construction and predict the fallback.

## E. Constructor or factory

Design creation for a validated `NodeId`. Compare:

```ts
new NodeId(raw)
NodeId.parse(raw)
createNodeId(raw)
```

The operation may fail with a detailed validation error. Decide which public surface best separates runtime parsing from an already-valid instance. Include the static and instance TypeScript types.

## F. Callback contract

Define a traversal function that:

- calls the visitor exactly once for each node;
- supplies node and depth as parameters;
- never supplies a receiver;
- does not retain the visitor after return;
- stops when the visitor returns `false`.

Write the callback type and a test that a receiver-dependent method is rejected unless adapted.

## G. Independent laboratory

Complete [Receiver-Safe Command Adapter](../../labs/module-13-receiver-safe-command-adapter/README.md). The reference tests include extracted methods, stable listener identity, bound leading arguments, and constructible versus callable functions.

## H. ObjectAtlas transfer

Add receiver-safe traversal and command registration. Test:

- ordinary method calls;
- an intentionally rejected detached method;
- an arrow adapter;
- one stored bound callback removed successfully;
- factory-based validated reconstruction;
- prototype method sharing across node instances.

## I. Reconstruction and defense

Without notes, explain:

- callability versus constructibility;
- call-site `this` versus lexical arrow `this`;
- the role of explicit TypeScript `this` parameters;
- `call` versus `apply` versus `bind`;
- the conceptual steps of `new`;
- constructor object returns;
- `new.target`;
- why listener removal and bound function identity are connected.
