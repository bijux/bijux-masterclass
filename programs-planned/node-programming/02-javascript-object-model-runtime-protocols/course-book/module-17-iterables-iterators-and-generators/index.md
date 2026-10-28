# Module 17 — Iterables, Iterators, Generators, and Traversal State

> **Question:** What sequence does an object promise, where is traversal state stored, and what cleanup must happen when a consumer stops early?

## Why this comes now

Module 16 introduced symbol protocols. `Symbol.iterator` is the most widely used object protocol in everyday JavaScript. It powers `for...of`, spread, destructuring, `Array.from`, collection constructors, and many library APIs. A correct iterator is not merely an object with a `next` method. It is a state machine with completion semantics, optional `return` and `throw` methods, one-shot or reusable identity, and mutation behavior that must be part of the product contract.

Generators provide syntax for implementing that state machine, but they do not remove design decisions. A generator can retain references longer than expected, execute `finally` during early close, delegate with `yield*`, accept values through `next`, and throw at a suspended point. Tree traversal adds ordering, cycle, and mutation questions.

ObjectAtlas becomes naturally iterable in this module. Its default iteration is deterministic preorder over roots and children. Breadth-first and postorder traversals remain named methods because they represent different semantics rather than interchangeable implementation details.

## Outcomes

By the end of this module, you can:

- distinguish an iterable from an iterator and an iterable iterator;
- implement and inspect the iterator result protocol;
- explain one-shot versus reusable iteration;
- predict how `for...of` closes an iterator after `break`, `return`, or throw;
- implement generator functions with `yield`, `return`, `throw`, and `finally`;
- use `yield*` while preserving delegated completion behavior;
- design preorder, postorder, and breadth-first graph traversal;
- state mutation-during-iteration policy explicitly;
- prevent cycles and duplicate visits in graph traversal;
- choose lazy traversal without overstating memory savings or retention behavior.

## 1. Iterable and iterator are different roles

An iterator supplies successive results:

```ts
interface IteratorResultLike<T> {
  readonly value?: T;
  readonly done: boolean;
}

interface IteratorLike<T> {
  next(): IteratorResultLike<T>;
}
```

An iterable can produce an iterator:

```ts
interface IterableLike<T> {
  [Symbol.iterator](): Iterator<T>;
}
```

Many built-in iterator objects are also iterable: their `Symbol.iterator` method returns themselves. This lets them participate in `for...of` after partial consumption.

```ts
const iterator = [1, 2, 3][Symbol.iterator]();
console.log(iterator[Symbol.iterator]() === iterator); // true
```

Do not assume every iterable is its own iterator. Arrays are reusable iterables that create a fresh iterator each time.

## 2. Iterator results carry completion state

A call to `next()` returns an object with `done` and `value`.

```ts
const iterator = ['a'][Symbol.iterator]();
console.log(iterator.next()); // { value: 'a', done: false }
console.log(iterator.next()); // { value: undefined, done: true }
```

The important semantic distinction is completion, not whether `value` is `undefined`. An iterator may legitimately yield `undefined` with `done: false`.

```ts
function* values(): Generator<undefined, void, void> {
  yield undefined;
}
```

Consumers must examine `done`. Never use `value === undefined` as the exhaustion test.

After completion, a well-behaved iterator remains completed on later `next` calls. This is often called a fused completion property. The language does not force every custom iterator to be philosophically “fused,” but surprising resurrection is almost always a bad public contract.

## 3. Reusable iterable versus one-shot iterator

A range object can produce a fresh traversal each time:

```ts
class Range implements Iterable<number> {
  constructor(
    private readonly start: number,
    private readonly endExclusive: number,
  ) {}

  *[Symbol.iterator](): Iterator<number> {
    for (let value = this.start; value < this.endExclusive; value += 1) {
      yield value;
    }
  }
}
```

```ts
const range = new Range(0, 3);
console.log([...range]); // [0, 1, 2]
console.log([...range]); // [0, 1, 2]
```

A generator object is usually one-shot:

```ts
const once = (function* (): Generator<number, void, void> {
  yield 1;
  yield 2;
})();

console.log([...once]); // [1, 2]
console.log([...once]); // []
```

The API must make this distinction visible. Returning an iterable collection suggests repeatability; returning an iterator or generator object suggests consumable traversal state.

## 4. Manual iterator state machines

A manual iterator makes state explicit:

```ts
class CountdownIterator implements Iterator<number>, Iterable<number> {
  #current: number;
  #done = false;

  constructor(start: number) {
    this.#current = start;
  }

  next(): IteratorResult<number, void> {
    if (this.#done) {
      return { done: true, value: undefined };
    }

    if (this.#current < 0) {
      this.#done = true;
      return { done: true, value: undefined };
    }

    const value = this.#current;
    this.#current -= 1;
    return { done: false, value };
  }

  [Symbol.iterator](): Iterator<number> {
    return this;
  }
}
```

Manual iterators are appropriate when state transitions, object allocation, or non-generator integration matters. Generators are usually clearer for ordinary traversal.

The state machine must specify:

- initial position;
- value produced by each transition;
- terminal state;
- repeated terminal calls;
- exceptional state;
- cleanup after early close.

## 5. Generator functions construct suspended computations

Calling a generator function does not execute its body immediately:

```ts
function* trace(): Generator<number, void, void> {
  console.log('start');
  yield 1;
  console.log('resume');
}

const iterator = trace();
console.log('created');
iterator.next();
```

The first `next` starts execution and suspends at `yield`. A later `next` resumes after the suspended `yield`.

A generator stores:

- instruction position;
- local variables;
- active `try`/`finally` regions;
- references reachable from locals;
- completion state.

Laziness can reduce eager work, but a suspended generator can retain a large source object. “Lazy” does not automatically mean “low memory.” Retention must be measured from reachable state.

## 6. Values can travel into and out of a generator

A generator type has three type parameters:

```ts
Generator<Yield, Return, Next>
```

A value passed to `next(value)` becomes the result of the previous suspended `yield` expression. The first `next` argument is ignored because there is no suspended `yield` yet.

```ts
function* accumulator(): Generator<number, number, number> {
  let total = 0;
  while (true) {
    const increment = yield total;
    if (increment < 0) {
      return total;
    }
    total += increment;
  }
}
```

This bidirectional style can model coroutines, but it increases the protocol surface. For ordinary collection traversal, use `Generator<T, void, void>` so callers do not need to understand input and final-return channels.

## 7. Early termination invokes iterator closing

When a `for...of` loop stops early due to `break`, `return`, or an exception, it performs iterator closing. If the iterator has a callable `return` method, that method is invoked.

Generators use this to run `finally` blocks:

```ts
function* resourceful(): Generator<number, void, void> {
  try {
    yield 1;
    yield 2;
  } finally {
    console.log('closed');
  }
}

for (const value of resourceful()) {
  console.log(value);
  break;
}
// logs closed
```

This supports cleanup for resources owned by the iterator. It does not justify hiding arbitrary long-lived resources inside a lazy sequence without documenting ownership.

Consumers that manually call `next` and then abandon the iterator do not automatically call `return`. The consumer protocol matters.

## 8. Iterator `return` is not the generator’s ordinary return value

A generator can complete with a return value:

```ts
function* sample(): Generator<number, string, void> {
  yield 1;
  return 'finished';
}
```

`for...of` ignores the final return value. Manual callers can observe it in the terminal iterator result.

Calling `iterator.return(value)` requests completion and may execute `finally`. The supplied value participates in the resulting completion subject to generator semantics.

Do not encode essential collection output in a generator return value if ordinary iteration is the public consumption path.

## 9. `throw` resumes at the suspension point

`iterator.throw(error)` injects a throw at the currently suspended `yield`. The generator can catch it:

```ts
function* guarded(): Generator<string, void, void> {
  try {
    yield 'ready';
  } catch (error: unknown) {
    yield `caught:${String(error)}`;
  }
}
```

This is useful for coroutine protocols, not normally for tree traversal. A traversal generator should propagate underlying graph errors rather than define a hidden command channel through `throw`.

## 10. `yield*` delegates iteration

`yield* iterable` delegates to another iterable:

```ts
function* flatten<T>(groups: Iterable<Iterable<T>>): Generator<T, void, void> {
  for (const group of groups) {
    yield* group;
  }
}
```

Delegation forwards `next`, `return`, and `throw` interactions according to the iterator protocol. It is more than a textual loop replacement when bidirectional generator channels are involved.

For recursive tree traversal:

```ts
function* preorder<T>(
  root: T,
  childrenOf: (value: T) => Iterable<T>,
): Generator<T, void, void> {
  yield root;
  for (const child of childrenOf(root)) {
    yield* preorder(child, childrenOf);
  }
}
```

This simple recursion assumes an acyclic tree and manageable call depth. ObjectAtlas is a validated forest, so those assumptions are explicit. A general graph traversal needs a visited set and may need an iterative stack.

## 11. Preorder, postorder, and breadth-first are different contracts

Given:

```text
root
├── a
│   └── a1
└── b
```

Preorder:

```text
root, a, a1, b
```

Postorder:

```text
a1, a, b, root
```

Breadth-first:

```text
root, a, b, a1
```

The order affects rendering, deletion, dependency processing, and user expectations. Do not expose a generic `walk(mode)` only to avoid naming methods if the modes have different use cases. A good API may provide:

```ts
atlas[Symbol.iterator]()       // documented default preorder
atlas.preorder(rootId?)
atlas.postorder(rootId?)
atlas.breadthFirst(rootId?)
```

The default iterator should be the most unsurprising whole-object sequence.

## 12. Traversal must define cycle and duplicate policy

A tree promises one parent per non-root node and no cycles. A graph may allow multiple paths to the same node. Traversal must state whether it:

- yields once per node;
- yields once per edge/path;
- detects and rejects cycles;
- skips previously visited nodes;
- reports the path of a cycle;
- preserves source edge order.

ObjectAtlas enforces forest invariants during mutation, so traversal can assume acyclicity. It still uses a defensive visited set in public decoding and audit paths to avoid infinite loops if internal corruption is introduced by a bug.

## 13. Mutation during iteration is a product rule

Built-in collections have specific live-iteration behavior. A custom graph must choose.

Options:

1. **Live traversal:** changes may affect remaining results.
2. **Snapshot traversal:** capture identifiers or structure at iterator creation.
3. **Fail-fast traversal:** detect a revision change and throw.
4. **Exclusive traversal:** mutation is impossible while a traversal capability exists.

ObjectAtlas uses fail-fast traversal for live instances. The atlas increments a structural revision on graph-shape changes. Each iterator captures the initial revision and checks it before yielding the next node.

Attribute changes that do not alter structure may or may not invalidate traversal; the policy must state which revision they affect.

A weak implementation silently produces a mixture of old and new structure.

## 14. Iterator cleanup and retained references

A traversal iterator may retain:

- the atlas;
- a stack or queue of pending node IDs;
- a visited set;
- path state;
- a captured revision;
- callback closures.

If the consumer stores the iterator, these references remain reachable. A breadth-first queue may retain an entire frontier. A recursive generator may retain frames and ancestor references.

Use named traversal objects only when callers need explicit control. For simple loops, generator methods are readable. When memory bounds matter, inspect the maximum stack, queue, and visited-set sizes rather than saying “generators are memory efficient.”

## 15. ObjectAtlas increment

Make `ObjectAtlas` implement `Iterable<AtlasNodeView>`.

Contract:

- default iteration is root-order preorder;
- each call to `[Symbol.iterator]()` returns a fresh iterator;
- named preorder, postorder, and breadth-first methods are available;
- root and child order are deterministic and persisted;
- structural mutation during traversal throws a specific revision error before another value is yielded;
- early loop exit does not leave locks or mutable global traversal state;
- traversal yields read-only views, not mutable child arrays;
- corrupted cycles are detected defensively in audit traversal;
- large traversal state is bounded by documented graph size limits.

Tests must cover empty atlas, one node, multiple roots, deep chains, wide levels, early break, repeated iteration, structural mutation, and defensive cycle detection.

## Common wrong models

### “Iterable and iterator mean the same thing”

An iterable produces iterators. An iterator owns traversal state. Some values implement both roles.

### “`undefined` means done”

Completion is determined by `done`; `undefined` can be a yielded value.

### “Generators run when called”

Calling a generator function creates a suspended generator object. Execution starts on `next`.

### “Lazy means no retained memory”

Suspended locals and source references remain reachable.

### “Breaking a loop just stops calling `next`”

Language iteration performs iterator closing and may call `return`.

### “Tree traversal order is an implementation detail”

Order is observable and often part of the product contract.

## Practice sequence

1. Distinguish reusable iterable and one-shot iterator examples.
2. Implement a manual fused countdown iterator.
3. Trace generator execution across `next`, `return`, and `throw`.
4. Demonstrate `finally` during early loop termination.
5. Implement preorder, postorder, and breadth-first traversals.
6. Complete the Hierarchy Walker laboratory.
7. Add ObjectAtlas traversal with revision checks.
8. Defend the default iteration order and mutation policy.

## Ready to continue

Continue when you can draw an iterator’s state machine, explain how early close is delivered, and state exactly which references the iterator retains. You must also be able to distinguish default sequence semantics from alternate named traversals.

Module 18 intercepts the object operations behind properties and protocols. Proxies can observe or redefine those operations, but only within strict invariants.

## Primary references

- ECMAScript Language Specification: iterable and iterator protocols, iterator closing, generator objects, and `yield*` delegation.
- TypeScript standard library types: `Iterable`, `Iterator`, `Generator`, and `IteratorResult`.
- Node.js APIs that consume iterables, with attention to whether they consume synchronously and whether they close early.

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory 17 — Hierarchy Walker](../../labs/module-17-hierarchy-walker/README.md)
- [ObjectAtlas engineering guide](../capstone.md)
