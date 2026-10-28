# Laboratory 17 — Hierarchy Walker

## Product

Build a hierarchy container with deterministic preorder, postorder, and breadth-first traversal. The default iterable is preorder. Traversal is lazy, detects structural mutation, closes cleanly on early consumer termination, and rejects cycles during construction.

## Contract

A hierarchy owns immutable node records and one structural revision. Creating an iterator captures that revision. Every `next` verifies that the hierarchy still has the same revision. A structural change therefore produces a typed error rather than combining two versions silently.

The laboratory must distinguish:

- iterable from iterator;
- repeatable container from single-pass traversal;
- traversal state from graph state;
- `next` completion from early `return`;
- eager materialization from lazy production.

## Required cases

- empty hierarchy;
- one root;
- multiple roots;
- deep tree;
- sibling order;
- all three traversal orders;
- early `break` and cleanup observation;
- mutation after iterator creation;
- attempted cycle;
- repeated traversal creating independent iterators.

## Prohibited shortcuts

Do not implement every traversal by first returning one fully materialized array. Do not ignore cycles. Do not silently restart after mutation. Do not make the hierarchy itself the one-shot iterator.

## Transfer

Add an ancestor iterator that walks from one node toward the root. Explain whether its mutation policy should match structural traversal and whether the starting node is yielded.
## Traversal-state ledger

For each order, record the data structure that owns pending work. Preorder uses a stack whose children are pushed in reverse order. Postorder needs an explicit visited/expanded state or equivalent recursive suspension. Breadth-first uses a queue with a moving read index rather than repeated `shift` operations. The hierarchy owns nodes and revision; each iterator owns only its pending traversal state.

When a consumer breaks, the iterator is closed. The reference implementation exposes close evidence so the test can distinguish early termination from complete exhaustion. Mutation invalidation is checked before each yielded element, which makes the failure point deterministic.

