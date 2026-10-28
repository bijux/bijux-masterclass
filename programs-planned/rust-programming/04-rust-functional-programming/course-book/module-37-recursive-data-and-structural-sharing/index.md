# 37 — Recursive Data and Structural Sharing

**Course 4, day 7 · Module 37 of 90**  
`████████████░░░░░░░░` **37/90**

[← Module 36: Custom Iterators and Collection Protocols](../module-36-custom-iterators-and-collection-protocols/index.md) · [Course 4 overview](../index.md) · [Ninety-module map](../../../COURSE_MAP.md) · [Module 38: Functional Core and Effect Isolation →](../module-38-functional-core-and-effect-isolation/index.md)

## The question

> How can recursive values be transformed without hiding ownership, rebuilding cost, or structural sharing?

## Why this comes now

Linear streams are only one data shape. Recursive trees and persistent histories require structure-directed transformation and selective rebuilding. The module connects Course 2's shared ownership with Course 4's functional updates so structural sharing is explicit rather than advertised as 'immutability for free.'

## What you will be able to do

- Define recursive algebraic data with the appropriate indirection.
- Implement structural map, fold, and search operations with explicit base and recursive cases.
- Use `Rc` structural sharing when immutable versions must coexist.
- Distinguish immutable public semantics from efficient local mutation of uniquely owned data.
- Recognize recursion-depth and allocation costs and select iterative alternatives when required.

A recursive type needs indirection because its size must be finite and known.

```rust
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Expr {
    Literal(i64),
    Add(Box<Expr>, Box<Expr>),
    Negate(Box<Expr>),
}
```

`Box` gives each recursive edge a known pointer size and unique ownership.

For persistent shared versions, `Rc` may be more appropriate:

```rust
use std::rc::Rc;

type Link<T> = Option<Rc<Node<T>>>;

struct Node<T> {
    value: T,
    next: Link<T>,
}
```

## Core model

### Shape is the program guide

Operations follow variants:

```rust
fn depth(expr: &Expr) -> usize {
    match expr {
        Expr::Literal(_) => 1,
        Expr::Add(left, right) => 1 + depth(left).max(depth(right)),
        Expr::Negate(inner) => 1 + depth(inner),
    }
}
```

Every recursive branch reduces the problem to structurally smaller children. Exhaustive matching helps keep operations aligned with the data model.

### Ownership choices

- `&Expr -> R`: inspect without consuming.
- `Expr -> R`: consume and potentially reuse owned children.
- `&mut Expr`: update in place under exclusive access.
- `Rc<Expr> -> Rc<Expr>`: create versions that may share unchanged subtrees.

The same algorithm can have very different allocation and reuse behavior depending on the receiver.

### Closed variants versus open behavior

Recursive enums are closed sets. Course 3 traits are better when third-party node types must participate. For many ASTs and domain trees, exhaustive closed variants are a strength.

### Decision rule

Choose recursive representation from ownership and versioning needs. Then let exhaustive shape guide transformations. Do not add traits merely to avoid matching a closed domain.

A structural map preserves shape while transforming payloads.

```rust
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Tree<T> {
    Leaf(T),
    Branch(Vec<Tree<T>>),
}

impl<T> Tree<T> {
    pub fn map<U, F>(self, f: &mut F) -> Tree<U>
    where
        F: FnMut(T) -> U,
    {
        match self {
            Tree::Leaf(value) => Tree::Leaf(f(value)),
            Tree::Branch(children) => Tree::Branch(
                children.into_iter().map(|child| child.map(f)).collect()
            ),
        }
    }
}
```

The closure is borrowed mutably so one stateful mapper can be reused through recursion.

### Rendering fold over recursive data

A fold replaces constructors with combining functions:

```rust
impl<T> Tree<T> {
    pub fn fold<R, L, B>(&self, leaf: &mut L, branch: &mut B) -> R
    where
        L: FnMut(&T) -> R,
        B: FnMut(Vec<R>) -> R,
    {
        match self {
            Tree::Leaf(value) => leaf(value),
            Tree::Branch(children) => {
                let folded = children
                    .iter()
                    .map(|child| child.fold(leaf, branch))
                    .collect();
                branch(folded)
            }
        }
    }
}
```

Depth, leaf count, rendering, and evaluation can be expressed by different algebras. However, a generic fold may allocate intermediate vectors. A direct recursive function can be clearer and cheaper for one operation.

### Laws

For pure deterministic functions:

- mapping identity should preserve the tree;
- mapping `f` then `g` should equal mapping composition `g(f(x))`;
- shape should remain unchanged under map.

Stateful or effectful mappers can invalidate simple composition laws because call order becomes observable.

### Decision rule

Use structural map when shape is preserved and payload changes. Use a structural fold when many operations share the same traversal shape and the intermediate cost is acceptable. Keep direct recursion when it is clearer.

A persistent structure keeps old versions usable. New versions share unchanged nodes and allocate only changed paths.

```rust
use std::rc::Rc;

#[derive(Debug, Clone)]
pub enum List<T> {
    Empty,
    Node(T, Rc<List<T>>),
}

impl<T> List<T> {
    pub fn prepend(self: &Rc<Self>, value: T) -> Rc<Self>
    where
        T: Clone,
    {
        Rc::new(List::Node(value, Rc::clone(self)))
    }
}
```

The `T: Clone` bound above is unnecessary because `value` is owned; a careful API removes it. This is a deliberate review example: persistent sharing does not imply cloning payloads.

```rust
impl<T> List<T> {
    pub fn prepend(self: &Rc<Self>, value: T) -> Rc<Self> {
        Rc::new(List::Node(value, Rc::clone(self)))
    }
}
```

### Sharing is explicit ownership

`Rc::clone` increments a reference count and shares the same allocation. It does not deep-copy the list.

Old and new versions:

```rust
let empty = Rc::new(List::Empty);
let one = empty.prepend(1);
let two = one.prepend(2);
```

`one` remains valid; `two` points to a new head whose tail is shared with `one`.

### Trade-offs

- reference-count operations on shared edges;
- heap allocation for new nodes;
- single-threaded ownership with `Rc`;
- potential cycles if back edges use strong ownership;
- less in-place update opportunity unless uniqueness is detected.

Persistent structures are not automatically memory-efficient. They are useful when version coexistence and sharing matter.

### `Rc::make_mut`

Copy-on-write can mutate uniquely owned data in place or clone when shared, given `Clone`. This creates an immutable-looking API with adaptive implementation cost. The cost must be described as conditional.

### Decision rule

Use `Rc` structural sharing when old versions must coexist and unchanged structure is substantial. Use owned mutation when only one version is needed. Do not introduce persistence for stylistic purity.

Functional architecture is about observable behavior and compositional boundaries, not banning `mut`.

```rust
fn normalized(mut values: Vec<String>) -> Vec<String> {
    for value in &mut values {
        *value = value.trim().to_ascii_lowercase();
    }
    values.sort();
    values.dedup();
    values
}
```

The function consumes its input and returns a new owned result. No caller can observe intermediate mutation. This can be a clean value transformation.

### Uniqueness enables efficient updates

Ownership proves that no aliases observe the vector while it is being mutated. Rebuilding a vector through repeated concatenation to appear “pure” may allocate more and obscure the simple invariant.

### Observable mutation differs

Mutating a shared `Rc<RefCell<T>>`, global variable, file, or caller-owned `&mut T` is observable beyond the returned value. It belongs in the effect or state contract.

### Persistent API, mutable builder

A persistent structure can use a temporary mutable builder during bulk construction, then freeze it into an immutable representation. The phase boundary should be explicit.

### Law testing still applies

A locally mutating implementation can satisfy idempotence, order normalization, or preservation laws. Tests target observable results, not absence of assignment statements.

### Decision rule

Prefer unique local mutation when it simplifies implementation without exposing temporal state. Reserve persistent or copy-on-write structures for actual versioning and sharing requirements.

Updating one leaf in a persistent tree allocates new nodes along the root-to-leaf path and shares every untouched subtree.

```rust
use std::rc::Rc;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Tree<T> {
    Leaf(T),
    Branch(Rc<Tree<T>>, Rc<Tree<T>>),
}
```

A path can be represented explicitly:

```rust
#[derive(Clone, Copy)]
pub enum Direction { Left, Right }
```

The update function consumes a path iterator and returns a new root. At each branch, it recursively updates one side and `Rc::clone`s the other.

### Failure policy

An invalid path can return:

- `Result<Rc<Tree<T>>, PathError>` and leave the original root untouched;
- `Option<Rc<Tree<T>>>` if absence is enough;
- the original root plus a diagnostic for best-effort editing.

Because the original structure is immutable, failure atomicity is natural: no visible partial mutation occurs.

### Allocation bound

A successful update allocates proportional to path length, not total tree size, assuming payload replacement does not require deep copying. This is a cost model, not a claim about allocator overhead.

### Identity and equality

Two versions may contain equal values but have different root allocations. `Rc::ptr_eq` can detect shared identity for diagnostics, but domain equality should usually compare values.

### Batch updates

Applying many path-copy updates one at a time can repeatedly allocate overlapping paths. A transient mutable builder or grouped update algorithm may be better. Persistent semantics do not mandate one implementation strategy.

### Decision rule

Use path copying for isolated updates with version retention. Specify invalid-path behavior, allocation scale, and whether pointer identity is observable.

An event reducer applies an event to a state and returns the next state:

```rust
fn apply(state: Ledger, event: Event) -> Result<Ledger, ApplyError> {
    // state is owned candidate state
}
```

A sequence can be folded:

```rust
let final_state = events.into_iter().try_fold(Ledger::new(), apply)?;
```

### Snapshot semantics

A snapshot can mean:

- a deep owned copy;
- an `Rc` shared immutable state;
- a compact derived report;
- a persistent root sharing prior structure;
- a serialized external record.

Name the meaning. “Snapshot” alone does not guarantee isolation or cheapness.

### Histories with `scan`

```rust
let history = events.into_iter().scan(Ledger::new(), |state, event| {
    match apply(std::mem::take(state), event) {
        Ok(next) => {
            *state = next;
            Some(Ok(state.clone()))
        }
        Err(error) => Some(Err(error)),
    }
});
```

This example requires `Ledger: Clone` and clones every accepted state; that may be expensive. A persistent state representation or derived snapshot can reduce copying. The example is for semantic analysis, not a recommended default.

### Rejected events

A reducer may stop at the first invalid transition or continue with diagnostics while preserving the last valid state. These are different functions and should have different names and return types.

### Replay determinism

Given the same initial state and ordered events, a deterministic reducer should produce the same state and diagnostics. Time, random IDs, and filesystem lookups break replay unless injected as explicit inputs.

### Decision rule

Use reducers when state evolution is a deterministic function of prior state and one event. Define snapshot ownership and rejection policy; do not clone entire state by habit.

Structural recursion is clear, but Rust does not guarantee tail-call optimization. Deep input can overflow the call stack.

### Depth risk

A balanced tree with millions of nodes may have modest depth; a degenerate linked tree may have depth proportional to node count. Evaluate the shape, not only total size.

### Explicit stack traversal

```rust
fn count_leaves<T>(root: &Tree<T>) -> usize {
    let mut stack = vec![root];
    let mut count = 0;

    while let Some(node) = stack.pop() {
        match node {
            Tree::Leaf(_) => count += 1,
            Tree::Branch(children) => stack.extend(children.iter()),
        }
    }
    count
}
```

This moves traversal state to the heap-backed vector and makes order explicit.

### Iterator-based tree walks

A custom iterator can expose depth-first traversal lazily. Its state is an explicit stack of node references. This is useful when callers may stop early and when multiple consumers need the view.

### Allocation and sharing

`Box` and `Rc` nodes usually allocate individually in simple designs. Arena storage or compact vectors can improve locality but change ownership and belong partly to later systems/performance courses.

### Recursive drops

Deep recursive ownership may also recurse during destruction. Safe code can still exhaust the stack. Advanced iterative-drop designs should be driven by real depth requirements.

### Decision rule

Use recursive code for bounded or naturally shallow structures. Use an explicit stack or custom iterator when depth is untrusted, early exit matters, or traversal should be reusable.

### Persistent outline update

An outline node is `Rc<Node>`, with a title and vector of child `Rc<Node>` values. Updating path `[1, 0]`:

1. allocate a new target node with transformed title;
2. allocate a new parent at depth 1, sharing all siblings;
3. allocate a new root, sharing every untouched top-level child;
4. retain the old root unchanged.

Allocation is proportional to path length plus any replaced payload, under this representation.

### Structural fold

A rendering fold maps leaves to lines and branches to concatenated child documents. The generic fold allocates intermediate vectors, so the final implementation uses direct recursion with one mutable `String` buffer. The public operation remains deterministic and immutable from the caller’s view.

### Rejected purity performance claim

“Persistent update is cheaper than cloning the tree” is a cost model dependent on shape, allocation, payloads, and version lifetime. The course states path-copy scale, not measured superiority.

## Use the idea in a complete program

The course capstone is **LedgerFlow**, a deterministic event-analysis pipeline with diagnostics, audit history, queries, and reports. Retain persistent audit versions through structural sharing and prove which nodes are rebuilt after an update. State the memory cost without claiming zero-copy magic. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-07-persistent-history/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 38 when you can:

- answer the module question—“How can recursive values be transformed without hiding ownership, rebuilding cost, or structural sharing?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Define recursive algebraic data with the appropriate indirection;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [Box](https://doc.rust-lang.org/std/boxed/struct.Box.html)
- [Rc](https://doc.rust-lang.org/std/rc/struct.Rc.html)
- [The Rust Book: Recursive types](https://doc.rust-lang.org/book/ch15-01-box.html)

[← Module 36](../../../04-rust-functional-programming/course-book/module-36-custom-iterators-and-collection-protocols/index.md) · [ninety-module map](../../../COURSE_MAP.md) · [Module 38 →](../../../04-rust-functional-programming/course-book/module-38-functional-core-and-effect-isolation/index.md)

## Continue

1. Complete the [Module 37 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 37 — Persistent History](../../labs/module-07-persistent-history/README.md) from its public contract.
3. Apply the Module 37 increment in the [LedgerFlow engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
