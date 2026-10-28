# Module 17 Workbook

Write the iterator state before and after every operation. For generators, include suspended location, locals, active `finally` regions, and retained references.

## A. Iterable classification

Classify each as reusable iterable, one-shot iterator, iterable iterator, or none:

- array;
- array iterator;
- generator function;
- generator object;
- custom object with `[Symbol.iterator]` returning a fresh generator;
- custom object with `next` but no `[Symbol.iterator]`.

Explain which can be used directly by `for...of` and which produce the same values twice.

## B. Manual iterator

Implement a fused `StepRangeIterator` that yields `start`, then increments by positive `step` until reaching `endExclusive`. Validate safe integers and prevent overflow. Repeated terminal `next` calls must remain terminal.

Then wrap it in a reusable `StepRange` iterable.

## C. Generator control trace

Predict every log and iterator result:

```ts
function* sample(): Generator<number, string, number> {
  try {
    const first = yield 1;
    const second = yield first + 1;
    return `done:${second}`;
  } finally {
    console.log('cleanup');
  }
}
```

Trace normal completion, `return`, and `throw` from the first suspension point.

## D. Early close

Build a generator that owns a mock resource and closes it in `finally`. Compare:

- complete `for...of` consumption;
- `break` after one value;
- loop body throw;
- one manual `next` followed by abandonment;
- explicit `iterator.return()`.

State which paths execute cleanup and why.

## E. Traversal orders

Implement preorder, postorder, and breadth-first traversal over an immutable tree. Prove exact order. Then adapt the design to a directed graph and choose once-per-node versus once-per-path semantics.

## F. Mutation policy

Design tests for live, snapshot, and fail-fast traversal. For each policy, state the behavior when:

- a child is appended after the parent is yielded;
- the next pending node is removed;
- a label changes;
- the graph is cleared;
- a second iterator is active.

Choose and defend the ObjectAtlas policy.

## G. Independent laboratory

Complete [Hierarchy Walker](../../labs/module-17-hierarchy-walker/README.md). The lab requires three traversal orders, cycle detection, repeatability, early-close cleanup evidence, and fail-fast structural revision checks.

## H. ObjectAtlas transfer

Implement default and named traversals. Tests must cover:

- empty and single-node cases;
- deterministic multiple-root order;
- deep and wide structures;
- repeated iteration;
- one-shot iterator identity;
- early break;
- structural mutation;
- label-only change policy;
- corrupted cycle defense.

## I. Reconstruction and defense

Without notes, explain:

- iterable versus iterator;
- `done` versus `value`;
- generator suspension;
- `Generator<Yield, Return, Next>`;
- iterator closing;
- `yield*`;
- traversal order as contract;
- graph duplicate and cycle policy;
- retention costs of lazy traversal.
