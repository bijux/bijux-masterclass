# 16 — Rc, Weak, and Ownership Graphs

**Course 2, day 6 · Module 16 of 90**  
`█████░░░░░░░░░░░░░░░` **16/90**

[← Module 15: Box, Deref, Dynamically Sized Types, and Cow](../module-15-box-deref-dynamically-sized-types-and-cow/index.md) · [Course 2 overview](../index.md) · [Ninety-module map](../../../COURSE_MAP.md) · [Module 17: Interior Mutability and Runtime Borrows →](../module-17-interior-mutability-and-runtime-borrows/index.md)

## The question

> Which edges keep allocations alive, which only observe, and how does the graph dismantle when roots disappear?

## Why this comes now

A tree with one owner is simple; observers, parent links, caches, and snapshots introduce shared liveness. `Rc` and `Weak` are therefore taught as graph edges with different authority, not as ways to silence the borrow checker. You must be able to draw the graph and predict teardown before writing code.

## What you will be able to do

- Draw strong and weak ownership graphs and derive allocation liveness from roots and reference counts.
- Use Rc::clone, downgrade, upgrade, strong_count, weak_count, get_mut, and make_mut with their exact preconditions.
- Prevent strong cycles by assigning ownership direction and weak observers/backlinks deliberately.
- Distinguish value equality, allocation identity, runtime handles, and liveness observations.
- Bound retained shared state through explicit eviction or retention policy instead of assuming reference counting is collection.

## Core model

### Shared liveness, not shared mutation

`Rc<T>` provides single-threaded shared ownership of one allocation. Cloning an `Rc` increments a strong count; dropping strong owners decrements it. The allocation's `T` is dropped when the last strong owner disappears. Weak pointers do not keep `T` alive.

`Rc<T>` does not make `T` mutable or thread-safe. Mutation requires uniqueness (`Rc::get_mut`/`make_mut`) or a separate interior-mutability type with its own protocol.

### Draw the graph

For every shared design, draw nodes and label edges:

- strong edge: contributes to liveness;
- weak edge: observes without contributing;
- ordinary borrow: temporary access, not stored ownership;
- runtime handle: identity lookup, not allocation ownership.

A tree often has strong parent→child edges and weak child→parent backlinks. Observers are usually weak. A cache root may hold strong snapshot edges intentionally and must have an eviction policy.

### Counts are diagnostic facts

`Rc::strong_count` and `weak_count` report counts at an instant. In single-threaded code they are deterministic relative to the current operation, but they should not become the public correctness protocol when direct ownership operations express the need better. To use a weakly observed value, call `upgrade` and hold the returned `Rc`; `is_alive` alone does not reserve future liveness.

### Cycles

A cycle of strong `Rc` edges has no external owner but each node remains strongly referenced by another cycle node. Rust memory safety is preserved, but destruction never occurs and resources leak. Reference counting is not tracing garbage collection.

```text
root ─strong→ parent ─strong→ child
                 ↑             │
                 └────weak──────┘
```

Dropping `root` can dismantle this graph because the backlink is weak. If both directions were strong, it would remain.

### Uniqueness and copy-on-write

`Rc::get_mut(&mut rc)` returns mutable access only when the allocation is uniquely owned under its contract. `Rc::make_mut` provides copy-on-write: if aliases exist, it clones the value into a new allocation before returning mutable access. This is useful for immutable snapshots with occasional independent modification, but it changes allocation identity.

Distinguish:

- `a == b`: value equality under `PartialEq`;
- `Rc::ptr_eq(&a, &b)`: same allocation identity;
- equal handles: same logical slot/generation identity;
- same contents at different revisions: domain-dependent equality.

### Bounded retention

A snapshot cache that stores `Rc<DocumentSnapshot>` for every `(handle, revision)` will retain all snapshots until entries are evicted, even when external owners disappear. Reference counting releases unreachable allocations; it does not decide which cache entries should remain roots.

A retention policy can be:

- explicit caller eviction;
- maximum entries with deterministic least-recent/oldest policy;
- one snapshot per document;
- weak cache entries that do not own liveness;
- no cache, construct on demand.

The capstone uses an explicit policy and documents its bounds. A cache without a policy is an unbounded ownership root.

### Worked derivation: snapshots and watchers

The workspace stores a strong cache edge to each retained immutable snapshot. A caller receives an `Rc` clone. A `SnapshotWatcher` stores `Weak`; it can upgrade while any strong owner remains. Evicting the workspace edge does not guarantee immediate destruction if callers still hold `Rc`s. Dropping all caller owners after eviction makes future upgrades fail.

Tests should prove:

1. repeated snapshot request returns the same allocation while cached;
2. watcher does not increase strong count;
3. eviction removes only the workspace root;
4. external owner keeps snapshot alive after eviction;
5. watcher expires after the last strong owner drops;
6. retention limit evicts deterministically.

### Derive it yourself

Model a UI tree with parent links, listeners, and cached render snapshots. Mark every edge strong/weak/borrowed/handle. Then simulate teardown from each root and identify any cycle or unbounded cache.

### Misconception clinic

- Rc is neither thread-safe nor interior mutable by itself.
- Weak is not a promise that upgrade will succeed later.
- Dropping an external root does not collect a strong cycle.
- Reference counts explain liveness; they do not replace domain identity or cache policy.

`Rc<T>` allows multiple `Rc` values to own the same allocation in one thread. The allocation remains alive while at least one strong owner exists.

```rust
use std::rc::Rc;

let first = Rc::new(String::from("snapshot"));
let second = Rc::clone(&first);
assert_eq!(first.as_str(), second.as_str());
```

`Rc::clone` clones the owner handle and increments the strong count. It does not deep-clone the `String`. Writing the associated function makes this cost distinction visible, though `first.clone()` is equivalent.

### Shared ownership is independent ownership of one allocation

Either handle may be moved or dropped independently. A borrowed `&T` still has a validity relation to one owner borrow; an `Rc<T>` owner can be stored for an independently chosen scope. This is the real reason to use it.

### Immutability by default

Shared owners normally provide shared access to `T`. Safe mutation requires uniqueness (`get_mut`/`make_mut`) or interior mutability from Module 17. This is not a missing feature: unrestricted mutation through multiple owners would violate aliasing rules.

### `Rc` is single-threaded

It uses non-atomic reference counts and is not the shared-owner type for cross-thread transfer. `Arc<T>` uses atomic counting and belongs with concurrency in Course 7. Do not choose `Arc` “just in case”; its topology and mutation questions remain the same, with additional synchronization cost and semantics.

### Ownership edge model

Represent each `Rc<T>` stored in a field or collection as a directed strong edge to an allocation. Local clones are temporary strong edges. The allocation drops only when incoming strong-edge count reaches zero.

A borrow such as `&*node` is not another strong owner. It is a temporary loan from an existing `Rc` and cannot keep the allocation alive after all owners disappear.

### API signatures reveal liveness policy

- `fn inspect(node: &Node)` borrows; caller retains liveness responsibility.
- `fn retain(node: Rc<Node>)` takes a strong owner; callee may extend liveness.
- `fn observe(node: Weak<Node>)` may later find the node expired.

Accepting `&Rc<Node>` is appropriate only when count/identity operations on the wrapper are needed. Ordinary domain inspection should accept `&Node`.

An `Rc` allocation conceptually contains the value plus bookkeeping for strong and weak references. Exact memory layout is implementation detail. The behavioral contract is what matters.

### Strong count

`Rc::strong_count(&value)` reports current strong owners. It is useful in tests and diagnostics, but using count as application logic is fragile because temporary clones, function arguments, and refactors can change it.

### Weak count

`Rc::weak_count` reports explicit weak handles, subject to documented details. The allocation's bookkeeping may remain after the value is dropped while weak handles exist, so they can observe expiration. Do not infer domain membership from the raw count.

### Destruction phases

When the final strong owner drops:

1. `T` is dropped;
2. `Weak::upgrade` thereafter returns `None`;
3. allocation bookkeeping can remain until weak handles are also gone;
4. after the last weak handle drops, the allocation is fully reclaimed.

This separation allows observers to fail safely rather than dangle.

### Deep clone versus owner clone

```rust
let shared_copy = Rc::clone(&original);
let deep_copy = Rc::new((*original).clone());
```

The first shares one `T`; the second creates a separate `T` allocation. Name APIs to distinguish “share snapshot” from “duplicate snapshot.”

### Drop order in graphs

Dropping one root recursively decreases counts along fields as nodes are destroyed. Exact observable order can depend on field declaration and graph topology. Cleanup must not require a global graph order unless encoded separately.

### Counts are not garbage collection

Reference counting reclaims acyclic unreachable structures promptly. It cannot detect unreachable cycles because every node in the cycle still has incoming strong edges. The graph designer must ensure cycles contain at least one non-owning edge or choose a different representation.

### Cost model

Each `Rc::clone` and drop adjusts counts. Traversal through `Rc` adds indirection. These costs may be trivial or significant; Course 9 measures. In Course 2, use `Rc` only when lifetime independence and shared ownership are semantically required.

`Weak<T>` refers to an `Rc` allocation without keeping `T` alive. Create it with `Rc::downgrade` and access the value by attempting `upgrade`.

```rust
use std::rc::{Rc, Weak};

let owner = Rc::new(String::from("live"));
let observer: Weak<String> = Rc::downgrade(&owner);
assert_eq!(observer.upgrade().as_deref().map(String::as_str), Some("live"));
drop(owner);
assert!(observer.upgrade().is_none());
```

The `Option` is essential. Expiration is an ordinary state, not an exceptional dangling pointer.

### Owner tree with weak parent

A tree can store children strongly and parent backlinks weakly:

```text
parent --strong--> child
child  --weak----> parent
```

Dropping the root removes the strong path to descendants; child backlinks do not keep ancestors alive. Methods navigating upward must handle an absent parent.

### Observer registries

A registry may store `Weak<Subscriber>` values so registration does not own subscribers forever. Before notification, upgrade each observer and remove expired entries. The registry must define ordering and reentrancy separately.

### Weak is not a universally stable ID

A weak handle identifies one allocation while its bookkeeping exists, but it is not serializable domain identity and should not replace explicit IDs. It cannot be upgraded after liveness ends, and it couples identity to allocation strategy.

### Races are absent here, but expiration remains

In single-threaded code, liveness changes only through local control flow, so reasoning is simpler. Still, an upgraded `Rc` is the strong owner that guarantees validity for subsequent use. Do not call `upgrade` twice and assume both results match across intervening code that can drop owners.

### API naming

Use names such as `parent() -> Option<Rc<Node>>` or `upgrade()` that expose possible absence. Returning `Weak<Node>` shifts the upgrade policy to the caller. Choose based on whether observation itself should extend liveness.

### Capstone watchers

A document watcher can hold `Weak<DocumentSnapshot>` so it observes a snapshot without preventing reclamation. If the product requires watchers to preserve history, the edge should be strong instead. The type is a policy choice, not an optimization toggle.

A strong cycle keeps every member's strong count above zero even when no external root can reach it.

Conceptually:

```text
A --strong--> B
^             |
|             v
+---strong----+
```

Dropping external handles does not destroy A or B. Safe Rust permits this memory leak.

### Typical accidental cycle

A parent owns children with `Rc`; each child owns the parent with `Rc`. The intended model is a tree, but ownership edges form cycles. Make parent links `Weak`.

### Closure cycles

A callback stored in an `Rc`-owned object may capture an `Rc` back to that object. The cycle can be less visible than a node field. Draw captures as graph edges too.

### `Rc<RefCell<T>>` amplifies risk

Interior mutability allows building cycles incrementally after construction. Because mutation is easy, topology can drift without constructor review. Module 17 requires explicit edge policies before combining these wrappers.

### Detecting cycles

Tests can hold `Weak` probes, drop all intended roots, and assert `upgrade().is_none()`. Strong-count snapshots can aid diagnosis but should not be the sole proof because temporary owners alter counts.

### Breaking cycles

Options:

- make back/observer edges weak;
- add explicit disconnect that removes strong edges before roots drop;
- represent graph relationships with IDs into an owning arena;
- centralize ownership in one collection and borrow/lookup nodes;
- redesign callbacks to avoid capturing owners.

Explicit disconnect is vulnerable to forgotten calls and leaks; it can still be necessary for timely external cleanup but should not be the only memory-reclamation mechanism.

### Leak versus unsafety

A cycle leaks memory and may leak logical resources held by destructors. It does not by itself permit use-after-free. This distinction matters: Rust's memory safety permits leaks, but production quality may not.

### Review proof

For every strongly connected component, identify an external root or show at least one edge is non-owning. Then write a reclamation test. A diagram without executable liveness evidence is incomplete.

Shared ownership does not always mean permanent immutability. When one strong owner is unique, mutation can be safe without runtime borrow checking.

### `Rc::get_mut`

```rust
use std::rc::Rc;

let mut value = Rc::new(String::from("draft"));
Rc::get_mut(&mut value).unwrap().push_str(" one");
let alias = Rc::clone(&value);
assert!(Rc::get_mut(&mut value).is_none());
drop(alias);
assert!(Rc::get_mut(&mut value).is_some());
```

Production course code should avoid `unwrap`, but the semantic point is that mutable access is returned only when uniqueness conditions hold. Existing weak pointers can also affect which APIs guarantee uniqueness; follow the exact standard-library contract rather than memorizing only strong count.

### `Rc::make_mut`

When `T: Clone`, `make_mut` provides mutable access, cloning the value into a new allocation if shared ownership prevents in-place mutation:

```rust
let mut left = Rc::new(String::from("base"));
let right = Rc::clone(&left);
Rc::make_mut(&mut left).push_str(" changed");
assert_eq!(left.as_str(), "base changed");
assert_eq!(right.as_str(), "base");
```

This is clone-on-write at the owner level. It changes allocation identity for `left` when necessary.

### Identity-sensitive data

`make_mut` is inappropriate when aliases are expected to observe mutation or allocation identity is domain-significant. It intentionally creates divergence. Use explicit versioned snapshots when that is the product model; use interior mutability when all owners must observe shared mutation and runtime borrow rules are acceptable.

### Weak observers

Copy-on-write can detach weak observers from the newly cloned allocation or alter upgrade behavior according to the exact operation and uniqueness state. Test observer semantics if weak links coexist with `make_mut`.

### API design

A type can expose a mutation method on `&mut Rc<T>` and internally use `make_mut`, making copy-on-write part of its contract. Do not hide potentially large deep clones behind innocuous method names without documentation.

### Capstone use

Immutable snapshots can be shared as `Rc<DocumentSnapshot>`. If metadata annotation should create a divergent snapshot, `make_mut` may be appropriate. Live documents should not be modeled this way if all handles must observe the same edit.

Two `Rc<T>` values can be equal because their `T` values are equal even when they own different allocations. `Rc::ptr_eq` tests whether they point to the same allocation.

```rust
use std::rc::Rc;

let first = Rc::new(String::from("same"));
let second = Rc::new(String::from("same"));
assert_eq!(first, second);
assert!(!Rc::ptr_eq(&first, &second));
```

### Domain identity should be explicit

Pointer identity is tied to allocation choices, cloning, and reconstruction. Persistent or logical identity should use a domain identifier such as a generational handle. Otherwise refactoring from `Rc` to an arena changes semantics unexpectedly.

### When allocation identity matters

It can be useful for:

- deduplication caches keyed by interned allocation;
- graph algorithms detecting shared substructure;
- tests that verify owner cloning versus deep cloning;
- avoiding duplicate work on the same in-memory node.

Document that it is process-local and representation-dependent.

### Equality can recurse through cycles

Derived structural equality over graph nodes with cycles may recurse indefinitely or overflow. Often nodes should compare IDs, not recursively compare the entire reachable graph. Derive choices are part of topology design.

### Hashing

Hashing an `Rc<T>` generally hashes the target value through trait implementations, not allocation address. If identity hashing is required, use an explicit stable key or carefully defined pointer wrapper within process boundaries. Do not cast addresses into persistent IDs.

### Snapshot semantics

Two snapshots with identical content but different revision/handle identity may be value-equal in text yet distinct domain events. Define separate operations such as `same_content` and `same_snapshot` instead of overloading one equality relation ambiguously.

An arena owns many values in one collection. Relationships are IDs or indices resolved through the arena. Reference counting distributes ownership across edges. These topologies solve different problems.

### `Rc` strengths

- independent owners with automatic prompt reclamation in acyclic graphs;
- direct access after clone without central lookup;
- natural immutable shared trees/DAGs;
- weak observers and backlinks.

### `Rc` costs

- per-allocation bookkeeping and indirection;
- cycles require design discipline;
- mutation often leads to uniqueness checks or interior mutability;
- allocation identity can leak into APIs;
- each node often allocates independently.

### Arena/handle strengths

- centralized ownership and reclamation policy;
- compact storage possibilities;
- relationships do not keep targets alive implicitly;
- generational handles can reject stale reuse;
- serialization and domain identity can be explicit.

### Arena/handle costs

- every access performs lookup/validation;
- borrowed references can couple to arena borrow scope;
- removing nodes requires relationship cleanup policy;
- stable address is not implied if storage moves.

### Owner tree plus weak links

For strict hierarchy, `Rc` children and weak parents can be clear. For arbitrary mutable graph editing, arenas often avoid `Rc<RefCell<Node>>` complexity.

### Shared snapshots versus live entities

Immutable snapshots are excellent `Rc` candidates: many consumers may retain one immutable value, and cycles are unlikely. Live workspace documents already have centralized ownership and handles; wrapping each in `Rc<RefCell<_>>` would duplicate identity and mutation mechanisms.

### Decision statement

Write one sentence:

> This value has multiple independent owners because ______, and those owners should/should not extend its lifetime.

If the blank cannot be filled concretely, borrow or use handles instead.

### Draw three graphs

1. **Domain graph** — logical relationships.
2. **Ownership graph** — strong edges that determine liveness.
3. **Observation graph** — weak edges and temporary borrows.

They need not be identical.

### Root analysis

Identify roots owned by application state. For each node, determine which path keeps it alive. If a node remains alive only because of a cycle, the model leaks.

### Mutation analysis

State whether mutation requires:

- unique `Rc` access;
- copy-on-write divergence;
- shared observable mutation via interior mutability;
- central arena mutation through handles.

Do not combine all mechanisms.

### Identity analysis

Separate domain ID, revision, value equality, and allocation identity. Specify which is used for deduplication, lookup, display, and tests.

### Reclamation checks
Create weak probes for representative components, drop roots, and prove expiration. Include closure captures and registries in the graph.

### API-width analysis

Functions that only inspect receive `&T`. Functions that retain receive `Rc<T>` explicitly. Observer registration receives or creates `Weak<T>` according to policy. Wrapper-specific arguments make liveness changes visible.

### Failure policy

Every `Weak::upgrade` has an expiration branch. Treating `None` as impossible requires a stronger owner elsewhere and should be encoded by borrowing/strong ownership instead.

A scene graph has a root. Parents conceptually own children; children need to navigate to parents; selection panels may observe nodes without keeping removed subtrees alive.

### Edge classification

```text
Scene -> Rc<Node> root                     strong root
Node -> RefCell<Vec<Rc<Node>>> children    strong ownership
Node -> RefCell<Weak<Node>> parent         weak navigation
Panel -> Weak<Node> selection              weak observation
```

If a panel must preserve a detached node for editing, it intentionally stores `Rc<Node>` and that retention is part of product behavior.

### Construction

Create root with empty weak parent. Create child with parent `Rc::downgrade(&root)`, then push strong child edge into root. `Rc::new_cyclic` is needed only for a weak self-reference, not ordinary parent wiring.

### Reparenting

Before mutable guards:

- verify nodes differ;
- walk weak parents to reject a cycle;
- find child index under old parent.

Then scope guards so no `RefMut` overlaps unknown callbacks. Remove strong child edge, update weak parent, add strong edge to new parent. If any later operation can fail, stage vector changes or define rollback.

### Cycle proof

A parent-child cycle through all-strong edges leaks. The weak parent convention means strong edges form a rooted tree. An external `Rc` can keep a detached subtree alive intentionally; this is not a leak if reachable from a documented owner.

### Reclamation test

Retain `Weak` to a leaf, drop all panel strong owners and the scene root, then assert `upgrade` is `None`. Test detached-subtree liveness separately with an intentional `Rc` owner.

### Runtime borrow risk

`Rc` enables shared liveness but not mutation. `RefCell` enables runtime mutation and can panic. A renderer should borrow child lists briefly, clone only `Rc` handles if traversal must continue after guard release, and never call arbitrary node callbacks while holding `RefMut`.

### Alternative arena

A central `Scene` owning nodes in slots with generational handles eliminates reference cycles and runtime borrow cells. Parent/child edges become handles; every lookup validates. This may be better for heavy mutation and serialization. `Rc` graph is suitable when independent node liveness and pointer-like sharing are product requirements.

### Thread boundary

The design is single-threaded. Replacing `Rc` with `Arc` is insufficient because `RefCell` is not thread-safe and rendering/mutation protocols need synchronization. Do not imply future thread support.

## Use the idea in a complete program

The course capstone is **Memory Workspace**, an in-memory document workspace with handles, snapshots, edit sessions, and caches. Store snapshots with strong ownership, expose weak observers, and define eviction. Draw the liveness graph and prove that observers do not keep snapshots alive. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-06-rc-weak-graph/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 17 when you can:

- answer the module question—“Which edges keep allocations alive, which only observe, and how does the graph dismantle when roots disappear?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Draw strong and weak ownership graphs and derive allocation liveness from roots and reference counts;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [std::rc](https://doc.rust-lang.org/std/rc/)
- [Rc](https://doc.rust-lang.org/std/rc/struct.Rc.html)
- [Weak](https://doc.rust-lang.org/std/rc/struct.Weak.html)

[← Module 15](../../../02-rust-ownership-lifetimes-memory/course-book/module-15-box-deref-dynamically-sized-types-and-cow/index.md) · [ninety-module map](../../../COURSE_MAP.md) · [Module 17 →](../../../02-rust-ownership-lifetimes-memory/course-book/module-17-interior-mutability-and-runtime-borrows/index.md)

## Continue

1. Complete the [Module 16 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 16 — Shared Ownership Graph](../../labs/module-06-rc-weak-graph/README.md) from its public contract.
3. Apply the Module 16 increment in the [Memory Workspace engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
