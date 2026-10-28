# Workbook — Module 37: Recursive Data and Structural Sharing

[Return to the chapter](index.md) · [Open the LedgerFlow engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether you can use **Recursive Data and Structural Sharing** without relying on surface syntax. Keep the module question in view: *How can recursive values be transformed without hiding ownership, rebuilding cost, or structural sharing?* For every task, identify the program point where the decisive type, ownership, dispatch, failure, or cost relationship is established. Compile only after committing to a prediction, and preserve the smallest counterexample that changes your model.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Recursive Data and Structural Sharing** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`case-01.rs`](../../compiler-labs/module-07/case-01.rs) | Pass or fail? What exact rule decides? |
| 2 | [`case-02.rs`](../../compiler-labs/module-07/case-02.rs) | Pass or fail? What exact rule decides? |
| 3 | [`case-03.rs`](../../compiler-labs/module-07/case-03.rs) | Pass or fail? What exact rule decides? |
| 4 | [`case-04.rs`](../../compiler-labs/module-07/case-04.rs) | Pass or fail? What exact rule decides? |
| 5 | [`case-05.rs`](../../compiler-labs/module-07/case-05.rs) | Pass or fail? What exact rule decides? |
| 6 | [`case-06.rs`](../../compiler-labs/module-07/case-06.rs) | Pass or fail? What exact rule decides? |
| 7 | [`case-07.rs`](../../compiler-labs/module-07/case-07.rs) | Pass or fail? What exact rule decides? |
| 8 | [`case-08.rs`](../../compiler-labs/module-07/case-08.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 04-rust-functional-programming
```

## Part 2 — Diagnose and repair

Every append clones the complete audit tree. Parent links are strong `Rc` pointers, traversal is recursive over untrusted depth, and equality is implemented with `Rc::ptr_eq`.

The program appears immutable at the API surface, but it has combined the costs of deep copying with the cycle risk of shared ownership.

### Separate four concepts

1. **Domain equality**: two histories contain equal entries in equal order.
2. **Identity**: two handles point to the same allocation.
3. **Structural sharing**: two versions reuse a tail.
4. **Persistence**: an older version remains usable after a newer version is created.

Pointer identity can provide evidence for sharing; it cannot define domain equality.

### Repair the topology

For an append-only newest-first history, each node needs only a strong edge to the previous tail. There is no need for a parent backlink. Appending allocates one new node and clones one `Rc` handle to the old head. Old versions remain unchanged.

If a tree genuinely needs back edges, use `Weak` for non-owning navigation and define liveness explicitly. Do not add parent links merely to make traversal convenient.

### Bound depth risk

Use an explicit stack or iterative linked-list traversal for untrusted depth. Document drop behavior for very deep recursive ownership. A persistent API does not automatically make recursion safe.

### Weak repair to reject

Replacing deep clone with `Rc<RefCell<Node>>` would allow shared mutation and make old “versions” change underneath observers. That solves allocation symptoms by destroying persistence semantics.

## Part 3 — Focused exercises

### Exercise 1 — Model recursive data

Define an expression tree with integer literals, addition, and negation. Explain why the recursive variants require `Box` or another pointer and why `Vec<Expr>` can sometimes remove explicit boxing.

### Exercise 2 — Structural map and fold

Implement conceptually a map that doubles every literal and a fold that counts nodes. State the base and recursive cases.

### Exercise 3 — Trace path copying

A persistent binary tree updates one leaf. Draw which nodes are newly allocated and which child pointers are shared. State the complexity in tree height.

### Exercise 4 — Immutable interface, local mutation

Explain when `Rc::make_mut` can optimize a persistent update and what trait bound it may require.

### Exercise 5 — Persistent audit ordering

A history stores each new entry at the head. Design APIs for newest-first iteration and chronological reporting without rebuilding the data structure on every append.

### Exercise 6 — Choose mutable or persistent

Compare a single-owner batch accumulator with a persistent history retained by several report snapshots. Which deserves persistent structure?



## Part 4 — Independent laboratory

The executable crate is `labs/module-07-persistent-history/README.md`. The target is an immutable outline whose versions share unchanged nodes.

### Representation and identity

A node owns a title and `Vec<Rc<Node>>` children. Domain equality is value equality. `Rc::ptr_eq` is used only in tests that inspect structural sharing; it is not the definition of equal outlines.

Draw the ownership graph for a root with two children, then draw the graph after renaming path `[0]`. Mark newly allocated nodes and shared nodes. The expected update copies only the target and its ancestor spine.

### `rename_at_path`

The operation returns a new root or `PathError`. It must:

- leave the old root usable and unchanged;
- share siblings outside the changed path;
- preserve child order;
- report depth and invalid child index;
- perform no mutation through interior mutability.

Test the root path, a one-level path, a deeper path, and an invalid path. On failure, no partial version exists.

### Depth-first traversal

Provide an explicit-stack traversal for titles. Push children in reverse so output remains left-to-right. This design avoids call-stack depth as the traversal mechanism. State its auxiliary-space model in terms of tree shape.

### Transfer: insertion by path copying

Add a child to the node at a selected path. Share all existing unaffected children. Define whether the new child is appended or inserted at a position; the published solution appends. Test that the previous version has no new child and that an unchanged subtree retains pointer identity.

### Cost ledger

Do not claim persistent updates are categorically faster than cloning. Record:

- allocations proportional to changed path length;
- `Rc` clone operations for shared child handles;
- retained memory while old versions remain alive;
- traversal stack allocation;
- title cloning on rebuilt ancestors.

This is a model, not a benchmark result.

### Defects your tests must catch

- deep-cloning the entire tree;
- modifying children through `RefCell` and calling the result persistent;
- strong parent backlinks that create cycles;
- returning references into a newly created temporary version;
- comparing versions only by pointer identity;
- recursive traversal over attacker-controlled depth without a documented bound.

Submit graph diagrams, sharing assertions, value-equality assertions, invalid-path evidence, and the cost ledger. Defend why `Rc` is used for immutable shared ownership, why no `Weak` parent edge is needed in this model, and how the algorithm would change if nodes required stable globally unique identities.

The executable starter and reference implementation are in [module-07-persistent-history](../../labs/module-07-persistent-history/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

## Part 5 — Capstone transfer

Day 7 gives LedgerFlow an audit history whose old versions remain observable after new entries are appended. The purpose is not universal immutability. It is to learn when persistent structure provides a clear product capability: cheap version retention and explicit history values.

### Define the persistent node

Represent history as an immutable node containing an audit entry and an optional shared link to the previous version. `Rc` is appropriate because multiple history values may own the same tail in one thread.

```rust
struct AuditNode {
    entry: AuditEntry,
    previous: Option<Rc<AuditNode>>,
}
```

The public wrapper should hide representation details. Appending consumes or borrows the current wrapper and returns a new history without changing the old one.

### Draw the sharing graph

For versions `h0`, `h1`, `h2`, and a branch `h2b`, draw:

- each allocated node;
- every strong edge;
- which public history values own which head;
- which tails are shared;
- strong counts at one selected checkpoint.

Use `Rc::ptr_eq` and `Rc::strong_count` only as implementation evidence. Domain equality must remain value-based.

### Traversal contracts

Provide a newest-to-oldest iterator whose state is the next optional node reference. State its exact item type and whether it is exact-sized or fused. If the history stores a known length and the implementation can prove exact remaining items, test that promise; otherwise keep `size_hint` conservative.

Chronological rendering may require reversing a materialized sequence or using an explicit stack. Name that allocation boundary. Do not pretend a singly linked newest-first structure produces oldest-first output for free.

### Allocation and clone ledger

For appending one entry, record:

| Operation | Node allocation | Payload clone | `Rc` clone | Full-history clone |
|---|---:|---:|---:|---:|

Distinguish cloning an `Rc` handle from cloning its payload. State which parts of the new value are physically new and which are shared.

### Failure and depth considerations

If audit history can be untrusted or unbounded, discuss recursive drop and traversal depth. Provide an iterative traversal for public rendering. Do not write a recursive fold over arbitrary depth without documenting the risk.

If an audit entry can fail validation, validate before allocating and publishing the new head. The old version must remain usable after a failed append.

### Required tests

- old histories produce unchanged output after later appends;
- two branches share their common tail;
- newest-first and chronological views produce specified order;
- empty and one-entry histories behave correctly;
- failed append leaves the prior history intact;
- allocation evidence does not claim a deep copy;
- value equality does not depend on pointer identity.

## Part 6 — Reconstruct and defend

Do not advance because the calendar day ended. Advance when all hard evidence is present.

### Advancement decision

Advance only when you can identify every reused node, every rebuilt path, the base case, and the cost of retaining old versions.

### Closed-book retrieval

1. Why does a directly recursive enum need indirection?
2. What base and recursive cases define a structural fold?
3. What does cloning `Rc<T>` clone?
4. How does path copying preserve old versions?
5. When can `Rc::make_mut` use local mutation efficiently?
6. Why is moving out of shared `Rc` ownership forbidden?
7. What ordering does a linked history iterator naturally expose?
8. How can recursive traversal overflow the call stack?
9. What is the distinction between immutable API and no mutation anywhere?
10. When is persistent structure wasteful compared with one mutable owner?

### Reconstruction task

Build a persistent singly linked history with prepend, iteration, and one path-copying update. Prove that an earlier version remains unchanged.

### Transfer task

Design a structurally shared undo history for a text command stream, including retention limits and the point at which one mutable owner would be simpler. Produce:

- recursive shape and base cases;
- path-copying or structural-sharing diagram;
- identity of reused and rebuilt nodes;
- test proving the previous version remains unchanged after update;

### Spaced review

Repeat questions 2, 4, 7, and 10 after 24 hours. Repeat the reconstruction after seven days with a different domain.
