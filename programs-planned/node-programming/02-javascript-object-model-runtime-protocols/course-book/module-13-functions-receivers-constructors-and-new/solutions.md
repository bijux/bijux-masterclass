# Module 13 Reasoned Solutions

## A. Receiver table

`object.read()` uses `object` as receiver and returns `3`. `detached.call({ value: 5 })` explicitly supplies a receiver and returns `5`. `bound()` returns `4`. `bound.call({ value: 6 })` still returns `4` because an ordinary call cannot replace the receiver captured by `bind`.

An arrow created inside an ordinary method captures the method invocation’s `this`. An arrow created at module scope captures module lexical `this`, not whichever object later stores the arrow.

## B. Method extraction repair

Arrow adapter:

```ts
const adapter = (message: string): string => reporter.write(message);
handlers.add(adapter);
```

Stored bound adapter:

```ts
const boundWrite = reporter.write.bind(reporter);
handlers.add(boundWrite);
handlers.delete(boundWrite);
```

The arrow makes receiver selection visible. The bound function is useful when the same function identity must be passed to registration and removal APIs. Calling `bind` again during removal is a weak repair because it creates a different function object.

## C. Arrow field versus prototype method

Prototype methods are shared: two instances ordinarily have equal method function identity, and the method lives on the prototype. Arrow fields are created per instance, appear as own fields, and keep lexical receiver behavior when detached.

For a removable listener, either store a bound prototype method once or store an arrow field once. A prototype method passed directly is unsafe if it uses `this`. Choosing arrows for every method only to avoid receiver reasoning increases per-instance function allocation and changes reflection surfaces.

## D. `new` trace

`A` returns the created receiver with `x = 1`. `B` also returns the created receiver because primitive return values are ignored by construction. `C` returns the explicit `{ y: 2 }` object, replacing the created receiver.

If a constructor’s public `.prototype` value is not an object, ordinary construction uses the relevant intrinsic default prototype instead. The constructor body still receives a new object. Mutating `.prototype` after instances exist does not retroactively change their current internal prototype.

## E. Constructor or factory

When raw input may be invalid, a static parse method or external factory gives the failure boundary a name:

```ts
class NodeId {
  private constructor(readonly value: string) {}

  static parse(raw: string): NodeId {
    // validate, then construct
    return new NodeId(raw);
  }
}
```

The instance type is `NodeId`; the constructor/static side is `typeof NodeId`. A public throwing constructor can work, but it mixes raw-input validation with ordinary construction and is harder to distinguish from already-valid creation. A factory is the principled choice when parsing is a meaningful operation.

## F. Callback contract

A suitable type is:

```ts
type Visitor<T> = (this: void, value: T, depth: number) => boolean | void;
```

The traversal function calls it as `visitor(node, depth)`. A receiver-dependent method must be wrapped or bound deliberately. The contract also states non-retention; the type alone does not prove that, so implementation and tests must preserve it.

## G. Laboratory

A correct command adapter preserves stable identities, invokes handlers with documented receivers, and distinguishes callability from constructibility. It does not use broad `Function` types or silent `.bind` calls scattered across registration.

## H. ObjectAtlas transfer

Traversal callbacks should receive all context explicitly. Command registration should use module-level functions or stored adapters rather than detached instance methods. Reconstruction should validate plain data and call a factory; it should not treat prototype replacement as construction.

## I. Reconstruction standard

A complete explanation begins with the call form. It recognizes that `bind` creates identity, that arrows trade prototype sharing for lexical receiver capture, and that `new` is an object-creation protocol rather than a normal call with decoration.
