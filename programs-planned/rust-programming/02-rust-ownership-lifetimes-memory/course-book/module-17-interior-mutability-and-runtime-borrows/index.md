# 17 — Interior Mutability and Runtime Borrows

**Course 2, day 7 · Module 17 of 90**  
`██████░░░░░░░░░░░░░░` **17/90**

[← Module 16: Rc, Weak, and Ownership Graphs](../module-16-rc-weak-and-ownership-graphs/index.md) · [Course 2 overview](../index.md) · [Ninety-module map](../../../COURSE_MAP.md) · [Module 18: Memory Representation, Validity, and Layout →](../module-18-memory-representation-validity-and-layout/index.md)

## The question

> Which logically hidden mutation justifies runtime enforcement, and how can guard scope and reentrancy remain controlled?

## Why this comes now

Shared ownership alone does not permit mutation. Interior mutability introduces runtime-checked loans for cases where the public operation is logically read-only but internal state changes. It comes after ownership graphs because `RefCell` without a liveness model easily produces reentrancy failures and tangled authority.

## What you will be able to do

- Explain UnsafeCell as the primitive behind interior mutability while remaining within safe APIs.
- Choose Cell for replaceable Copy state and RefCell for single-threaded dynamically checked borrowed state.
- Treat Ref and RefMut as runtime loan guards whose scope is part of the API protocol.
- Avoid reentrant borrow panics by computing outside guards, shortening scopes, or using try_borrow variants and typed errors.
- Design caches whose mutation is observationally transparent, correctly invalidated, and memory-bounded.

## Core model

### Interior mutability preserves the aliasing rule by changing enforcement

Types built on `UnsafeCell` permit controlled mutation through shared references. Safe wrappers preserve Rust's aliasing requirements through different APIs:

- `Cell<T>` moves/copies whole values in and out without returning references to interior state;
- `RefCell<T>` tracks shared/exclusive loans at runtime and returns guard values;
- `OnceCell<T>` allows one-time initialization under its contract.

Interior mutability is justified when mutation is logically hidden behind a shared interface—caching, statistics, mock observations, graph relationships—not because a static design was inconvenient.

### Cell for replaceable scalar state

```rust
use std::cell::Cell;

pub struct Counter {
    value: Cell<u64>,
}

impl Counter {
    pub fn increment(&self) {
        self.value.set(self.value.get().saturating_add(1));
    }
}
```

No reference into the cell survives replacement. These operations are not atomic thread synchronization; `Cell` is for single-threaded use and is not `Sync`.

### RefCell is a runtime loan state machine

`borrow()` returns `Ref<T>` when no mutable guard exists. `borrow_mut()` returns `RefMut<T>` only when no other guard exists. Violations panic. `try_borrow` and `try_borrow_mut` represent contention as `Result`.

The guard's lifetime is a real part of the protocol:

```rust
let value = {
    let cache = self.cache.borrow();
    cache.lookup(key).cloned()
}; // guard dropped here
self.invoke_callback(value);
```

Holding `RefMut` across arbitrary callback code is dangerous if the callback can reenter the same object. Compute outside the guard, or finish mutation and drop the guard before invoking user code.

### Reentrancy

A method may look sequential but call a closure, formatter, error hook, or another method that reenters the object. If a dynamic borrow remains active, `borrow_mut` may panic. A robust API either:

- prevents reentrancy by construction and documents it;
- keeps guards entirely inside non-callback sections;
- exposes fallible busy errors;
- stages data outside the cell;
- redesigns ownership to regain `&mut self`.

Randomly replacing `borrow_mut` with `try_borrow_mut().unwrap()` changes nothing.

### Cache correctness

A cache needs:

- source revision or invalidation signal;
- exact derived value;
- read path and miss path;
- mutation invalidation;
- memory/retention bound;
- reentrancy behavior;
- observable-statistics policy.

```rust
fn ensure_cache(&self) -> Result<(), CacheBusy> {
    {
        let cache = self.cache.try_borrow().map_err(|_| CacheBusy)?;
        if cache.as_ref().is_some_and(|entry| entry.revision == self.revision) {
            self.hits.set(self.hits.get().saturating_add(1));
            return Ok(());
        }
    }

    let computed = compute_ranges(&self.text);
    *self.cache.try_borrow_mut().map_err(|_| CacheBusy)? = Some(Cache {
        revision: self.revision,
        ranges: computed,
    });
    self.misses.set(self.misses.get().saturating_add(1));
    Ok(())
}
```

Computation occurs outside the mutable guard. The exact implementation can optimize further, but the protocol is visible.

### Logical constness

A method taking `&self` may update a cache while returning the same domain answer as a pure computation. That can be observationally transparent if callers cannot observe differences except permitted metrics/performance. If cache statistics are public, they become observable state and their semantics must be documented.

Returning `Ref<'_, [Range<usize>]>` can avoid copying but exports the runtime loan duration to callers, increasing contention and reentrancy risk. An owned small descriptor or source-borrowed view may be a better boundary.

### Rc<RefCell<T>> audit

This combination provides shared single-threaded liveness plus runtime-checked mutation. It is sometimes correct for graph nodes or GUI models, but it compounds two protocols: strong-cycle risk and borrow-guard risk. Before using it, answer:

- Which edges own liveness?
- Can a callback reenter while a guard exists?
- Can an operation return `Ref` beyond a narrow scope?
- Is there a simpler owner-controlled method or arena/handle design?

### Derive it yourself

A memoized parser stores a map in `RefCell` and accepts a callback on cache miss. Redesign it so the callback can reenter safely, failures do not poison partial entries, and busy overlap becomes a typed error if it is a legitimate state.

### Misconception clinic

- RefCell moves checking to runtime; it does not weaken aliasing.
- Interior mutability is an abstraction decision, not a borrow-checker escape hatch.
- Cell is not an atomic primitive.
- Returning dynamic guards can make a “zero-copy” API much harder to compose.

Ordinary mutation through `&mut T` gives compile-time exclusive access. Interior-mutability types permit selected mutation through `&self` by encapsulating operations that would otherwise require exclusivity.

```rust
use std::cell::Cell;

struct Counter {
    hits: Cell<u64>,
}

impl Counter {
    fn record(&self) {
        self.hits.set(self.hits.get() + 1);
    }
}
```

The `Counter` itself is shared, but `Cell`'s API safely reads and replaces its contained copyable value. The compiler still prevents obtaining arbitrary aliasing `&mut u64` references from the cell.

### `UnsafeCell` is the primitive boundary

At the language level, `UnsafeCell<T>` is the marker that allows mutation through shared references. Safe cell types build rules on top of it. This course uses their safe APIs; implementing new unsafe cells belongs to the systems/unsafe course.

### Interior mutability is local authority

A shared `&Cache` does not imply every field is immutable. It implies callers have shared authority according to the type's public contract. A private cache field may change while the logical document content remains the same.

### Logical versus physical constness

A method taking `&self` may update:

- memoized derived data;
- access counters;
- lazily initialized indexes;
- one-time configuration;
- observer bookkeeping.

It should not secretly change domain state that callers reasonably expect to be stable under a shared borrow. For example, changing a document title inside `title(&self)` violates the ordinary read contract even if a `RefCell` makes it compile.

### Why compile-time borrowing can be too conservative

Some invariants depend on runtime control flow or external ownership patterns the compiler cannot prove. A graph node shared through `Rc` may need local mutation. A cache may be initialized from an immutable method because its result is logically derived. Runtime checking can be appropriate when the alternative is larger architectural complexity.

### Cost and failure mode

Interior-mutability operations may perform runtime state checks. `RefCell::borrow_mut` panics on conflict. This changes failure from compile time to runtime. The design must make conflicts impossible by control flow, handle them through `try_borrow*`, or document panic as a programming error with strong tests.

### First question

Before selecting a cell, ask whether a narrower `&mut` receiver, split state, staged mutation, or owner-controlled method would solve the problem with static guarantees. Interior mutability is justified by the abstraction, not by frustration.

`Cell<T>` allows getting and setting a value without exposing references into its interior. It is especially simple for `Copy` types.

```rust
use std::cell::Cell;

let cell = Cell::new(3_u32);
let current = cell.get();
cell.set(current + 1);
assert_eq!(cell.get(), 4);
```

Because `get` copies, no borrow guard survives the call. There is no dynamic “currently borrowed” state for ordinary `Cell` access.

### Replacing non-`Copy` values

`Cell<T>` can still replace or take owned values through methods such as `replace`, `swap`, `take` when bounds allow, and `into_inner`. It does not provide `&T` for arbitrary inspection.

```rust
let cell = Cell::new(String::from("draft"));
let old = cell.replace(String::from("final"));
assert_eq!(old, "draft");
```

If callers need to inspect a non-`Copy` value repeatedly without moving it out, `RefCell<T>` or ordinary borrowing may be more appropriate.

### Good uses

- counters;
- Boolean flags that do not guard external aliasing invariants;
- cached scalar metadata;
- generation numbers under single-threaded ownership;
- small state machines represented by `Copy` enums.

### Composite invariants

Two independent cells can expose transient contradictions:

```rust
struct Bounds {
    min: Cell<i32>,
    max: Cell<i32>,
}
```

Updating `min` then `max` allows code invoked between operations to observe an invalid range. Store one `Copy` pair/state enum in one `Cell`, or use a `RefCell<BoundsValue>` and mutate under one guard.

### `Cell` does not make operations atomic

Single-threaded `Cell` operations are not concurrency synchronization. `Cell` is not `Sync`; cross-thread shared mutation belongs to Course 7. “Atomic” in the logical all-or-nothing sense also requires careful composite representation.

### Aliasing model

The cell never hands out a long-lived shared reference that could be invalidated by replacement. This is why its API can safely mutate through `&self`. The absence of interior references is the central mechanism, not the smallness of `T`.

### API boundary

Keep cells private. Expose domain methods such as `record_hit` or `revision`, not the `Cell` itself. Returning `&Cell<T>` exports mutation authority and couples callers to the implementation.

`RefCell<T>` enforces the familiar rule at runtime:

- any number of active shared borrows, or
- exactly one active mutable borrow.

Methods return guard types whose destruction releases the dynamic loan.

```rust
use std::cell::RefCell;

let values = RefCell::new(vec![1, 2]);
{
    let read = values.borrow();
    assert_eq!(read.len(), 2);
}
values.borrow_mut().push(3);
```

### Runtime failure

This compiles but panics:

```rust,should_panic
use std::cell::RefCell;
let value = RefCell::new(String::from("x"));
let read = value.borrow();
let _write = value.borrow_mut();
drop(read);
```

The compiler cannot see the conflict because both methods take `&self`. The cell's borrow flag detects it.

### Fallible borrowing

Use `try_borrow` and `try_borrow_mut` when contention is a possible product state:

```rust
match value.try_borrow_mut() {
    Ok(mut text) => text.push('!'),
    Err(_) => return Err(EditError::Busy),
}
```

In single-threaded code, “busy” normally means reentrant or overlapping control flow, not another thread.

### Guard types are references with runtime release

`Ref<'a, T>` dereferences to `T`; `RefMut<'a, T>` dereferences mutably. They remain tied to the `RefCell` borrow and keep its borrow state active until their last use/drop.

Returning a guard can be valid but exposes runtime borrow duration to callers. Returning `&T` directly is impossible because the cell must keep tracking the borrow through the guard.

### Mapping guards

Guard mapping can project a borrow to a field without releasing the original dynamic loan. This can provide a narrower view while still locking the entire `RefCell` at runtime. Do not mistake projection for independent sub-cell borrowing.

### Replacement methods

Methods such as `replace` or `take` require no active borrow and may panic if one exists. The same dynamic-state review applies.

### Error location

A `RefCell` conflict often panics far from the architectural mistake. Record where every guard is created and its last use, just as with static borrows. Runtime enforcement does not remove lifetime reasoning; it makes evidence more important.

The most common `RefCell` defect is holding a borrow guard while calling code that may reenter the same component.

```rust
struct Registry {
    callbacks: RefCell<Vec<Box<dyn Fn()>>>,
}
```

If notification holds `callbacks.borrow()` while invoking callbacks, a callback that attempts to register another callback will request a mutable borrow and panic.

Trait-object architecture belongs to Course 3, but the borrow pattern is already instructive.

### Shorten guards before calls

Extract owned/copyable work first, release the guard, then call:

```text
borrow registry
copy or clone callback handles according to policy
release borrow
invoke callbacks
```

This may require shared ownership for callbacks or a queue of deferred mutations. The correct repair depends on reentrancy semantics.

### Nested method calls

A method may borrow mutably and call another method that also borrows:

```rust
fn outer(&self) {
    let mut state = self.state.borrow_mut();
    self.recompute(); // recompute borrows state again
    state.version += 1;
}
```

Refactor the inner logic to accept `&mut State`, or drop the first guard before the call. Avoid public methods calling public methods through the cell when a private helper can reuse one guard.

### Guard lifetime in expressions

Temporaries may keep a guard alive through an entire statement. Bind and explicitly scope when ordering matters:

```rust
let current = {
    let state = self.state.borrow();
    state.version
};
self.state.borrow_mut().version = current + 1;
```

### Returning guards

An accessor can return `Ref<'_, T>` or mapped guard, but callers must understand that future mutations can panic until it is dropped. Often a copied scalar, owned snapshot, or callback is a better public surface.

### Panic while mutably borrowed

If user code panics while a `RefMut` guard exists, unwinding drops the guard and resets borrow state. The underlying value may be partially changed, so panic-safety reasoning from Module 14 still applies.

### Reentrancy policy

Choose one:

- prohibited and detected as a domain error;
- permitted through deferred operations;
- permitted for read-only calls only;
- structurally impossible because no callbacks occur under borrow.

A runtime panic should not be the undocumented policy.

`std::cell::OnceCell<T>` allows a value to be initialized at most once through shared access in single-threaded contexts.

```rust
use std::cell::OnceCell;

struct Document {
    text: String,
    line_count: OnceCell<usize>,
}

impl Document {
    fn line_count(&self) -> usize {
        *self.line_count.get_or_init(|| self.text.lines().count())
    }
}
```

The cached value can be read thereafter without reinitialization.

### One-time means invalidation is not expected

`OnceCell` fits immutable source data. If `text` can change, the cached line count becomes stale unless mutation takes `&mut self` and resets/takes the cell according to available API. A repeatedly invalidated cache may be better represented by `RefCell<Option<Cache>>` or an explicit revision-tagged cache.

### Reentrant initialization

An initializer that recursively requests the same cell can panic or otherwise fail according to the API contract. Keep initialization free of calls that loop back into the same lazy accessor.

### Fallible initialization

Use fallible initialization APIs where available and appropriate rather than caching a fake value after error. Define whether failures are retried or remembered. Do not store `Result<T, E>` automatically without deciding that policy.

### `LazyCell`

A lazy cell stores an initializer and initializes on first access. It is useful when construction always knows the initializer. Compare with explicit `OnceCell` when initialization needs method context or can be supplied from multiple paths.

### Thread-safe counterparts

`std::sync::OnceLock` and synchronization-aware lazy types belong to concurrent design. Do not swap them in solely because they sound more production-ready; the threading contract matters.

### Cache identity

A one-time cache should derive solely from immutable state. If it depends on environment, clock, or mutable global configuration, the accessor is not observationally transparent and needs a stronger contract.

A cache is observationally transparent when populating or clearing it does not change the domain result that callers observe, except for documented performance and diagnostic effects.

### Revision-tagged cache

For mutable documents:

```rust
struct CachedIndex {
    revision: u64,
    line_starts: Vec<usize>,
}

struct Document {
    text: String,
    revision: u64,
    cache: RefCell<Option<CachedIndex>>,
}
```

A shared accessor checks whether cached revision matches current revision. Mutation through `&mut self` increments revision and can clear cache directly with `get_mut` or replace it.

### Never return references into replaceable cache casually

A `RefCell` guard can return a mapped view tied to the dynamic borrow, but it keeps the cell borrowed. If callers need durable evidence, copy ranges/handles or return an owned shared snapshot.

### Cache computation and reentrancy

Compute derived data outside a mutable cache borrow when possible:

1. check under short shared borrow;
2. release guard;
3. compute from immutable domain state;
4. acquire mutable borrow;
5. recheck if reentrancy/concurrency could change state;
6. install.

In this single-threaded course, reentrancy can still occur through callbacks. If no callbacks exist, the second check may be unnecessary but the scope discipline remains useful.

### Cache errors

Decide whether failed computation is cached. Caching errors can prevent repeated expensive failure but may become stale. Retrying every call can be costly. Represent policy explicitly.

### Metrics are observable

A hit counter changes under `&self`. Tests or monitoring can observe it, so “transparent” has limits. Keep metrics separate from semantic equality and serialization.

### Mutation authority

If cache invalidation is easy only because every field is a `RefCell`, the domain model is too porous. Live domain mutation should still prefer `&mut self`; interior mutability should be isolated to derived state.

### Proof

Tests must show:

- same semantic result before/after cache fill;
- invalidation after mutation;
- no stale revision served;
- no active guard spans user callback;
- cache inspection does not become public mutation authority.

`Rc<RefCell<T>>` combines:

- independent shared ownership of one allocation;
- runtime-checked shared mutation of its contents.

Each part needs separate justification.

### Questions before use

1. Are multiple independent owners required, or would one owner plus handles work?
2. Must all owners observe the same mutations, or should edits create versions?
3. Can dynamic borrow conflicts occur through nested calls or callbacks?
4. Can strong edges cycle?
5. Is domain identity explicit, or will allocation identity leak?
6. What happens when a weak observer upgrades during mutation?

### Public wrapper exposure

Returning `Rc<RefCell<Node>>` gives callers power to retain, mutate, and participate in borrow panics. Prefer a domain handle/object with methods that enforce invariants. Keep the wrapper private when possible.

### Borrowing across collection operations

A common failure collects `RefMut` guards or holds one while iterating to another node. Runtime conflicts may depend on graph shape. Extract owned commands, release guards, then apply mutations in a controlled phase.

### Cycle plus destructor obligations

A leaked cycle also prevents destructors of contained resources. If nodes own files, leases, or external registrations, the cycle is more than memory growth. Weak-edge design remains mandatory.

### Alternatives

- arena + generational handles for mutable graphs;
- `Rc<Node>` for immutable shared DAGs;
- `Rc<Cell<SmallState>>` for truly scalar shared state;
- owner-controlled `RefCell<Collection>` when one component owns all entries;
- staged commands instead of live shared mutation.

### Course boundary

Thread-safe analogues (`Arc<Mutex<T>>`, `RwLock`) have blocking, poisoning, and memory-order semantics. They are not drop-in “better RefCell” replacements and belong to Course 7.

For every cell field, document:

| field | logical or cache state | read API | mutation trigger | conflict policy | invalidation |
|---|---|---|---|---|---|

Then run four audits.

### Authority audit

Does a shared method mutate only state callers consider observationally stable? If it changes domain identity/content, require exclusive authority or document a fundamentally shared-mutable abstraction.

### Guard audit

List each guard's creation, last use, and every call made while active. User callbacks, formatting, equality, and other methods can reenter unexpectedly.

### Conflict audit

If conflict is possible under valid usage, use `try_borrow*` and a domain result. If conflict indicates an internal programming defect, make it structurally difficult and test the panic boundary.

### Topology audit

When combined with `Rc`, draw cycles and liveness. Runtime borrow checking does not solve ownership reclamation.

### Invariant audit

Group fields whose values must change atomically under one cell/state object. Multiple cells can expose contradictory intermediate state.

A cell that exists only because receiver methods were written too broadly fails review.

A document exposes immutable search while lazily building a token index. Text changes only through exclusive edit commits. Index construction is logically derived mutation.

### Representation

```rust
struct Document {
    text: String,
    revision: u64,
    index: RefCell<Option<Index>>,
    hits: Cell<u64>,
}

struct Index {
    revision: u64,
    ranges: Vec<Range<usize>>,
}
```

The index contains ranges into conceptual text but stores owned offsets, not references. Moving the document is harmless. On lookup, ranges are validated by revision and used to slice text.

### Guard sequence

1. acquire shared borrow of `index` and test current revision;
2. release guard;
3. compute ranges from `&self.text` with no cell guard;
4. acquire mutable guard only to install;
5. release guard;
6. acquire short shared guard, clone required range;
7. release and return `&self.text[range]`.

No `Ref` escapes. No mutable guard crosses tokenization callbacks.

### Reentrancy failure

A tempting implementation holds `borrow_mut` while calling a customizable tokenizer. If tokenizer queries document lines, nested borrow panics. Compute outside guards. If reentrant code installs an index first, recheck under the final guard and choose a winner policy.

### Why `Cell`

Hit count is copyable scalar. `Cell::get`/`set` avoids a guard. Saturating increment provides a defined diagnostic overflow policy. This counter is not a synchronization primitive.

### Cache freshness

Successful text commit increments revision and removes index. Revision field inside `Index` is defense in depth. Tests must show miss, hit, edit, miss. The borrow checker cannot prove freshness; the revision protocol does.

### API alternatives

If callers need references into data stored inside `RefCell`, return `Ref<'_, T>`/mapped guards or use callbacks. Returning owned clones may be simplest for small values. Moving immutable source text outside `RefCell` often enables ordinary borrows.

### `try_borrow`

Use `try_borrow` only when conflict is an expected state with a meaningful caller response. In this design, conflict indicates an implementation bug, so panicking `borrow` keeps the contract narrow and tests prevent reentrancy.

## Use the idea in a complete program

The course capstone is **Memory Workspace**, an in-memory document workspace with handles, snapshots, edit sessions, and caches. Add a revision-aware line cache with short `RefCell` guard scopes and explicit hit/miss behavior. No callback may run while a mutable runtime borrow is held. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-07-interior-cache/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 18 when you can:

- answer the module question—“Which logically hidden mutation justifies runtime enforcement, and how can guard scope and reentrancy remain controlled?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Explain UnsafeCell as the primitive behind interior mutability while remaining within safe APIs;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [std::cell](https://doc.rust-lang.org/std/cell/)
- [RefCell](https://doc.rust-lang.org/std/cell/struct.RefCell.html)
- [UnsafeCell](https://doc.rust-lang.org/std/cell/struct.UnsafeCell.html)

[← Module 16](../../../02-rust-ownership-lifetimes-memory/course-book/module-16-rc-weak-and-ownership-graphs/index.md) · [ninety-module map](../../../COURSE_MAP.md) · [Module 18 →](../../../02-rust-ownership-lifetimes-memory/course-book/module-18-memory-representation-validity-and-layout/index.md)

## Continue

1. Complete the [Module 17 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 17 — Revisioned Interior Cache](../../labs/module-07-interior-cache/README.md) from its public contract.
3. Apply the Module 17 increment in the [Memory Workspace engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
