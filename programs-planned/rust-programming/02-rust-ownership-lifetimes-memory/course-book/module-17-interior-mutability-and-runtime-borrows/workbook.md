# Workbook — Module 17: Interior Mutability and Runtime Borrows

[Return to the chapter](index.md) · [Open the Memory Workspace engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether you can use **Interior Mutability and Runtime Borrows** without relying on surface syntax. Keep the module question in view: *Which logically hidden mutation justifies runtime enforcement, and how can guard scope and reentrancy remain controlled?* For every task, identify the program point where the decisive type, ownership, dispatch, failure, or cost relationship is established. Compile only after committing to a prediction, and preserve the smallest counterexample that changes your model.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Interior Mutability and Runtime Borrows** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-mutate-through-shared-self.rs`](../../compiler-labs/module-07/01-mutate-through-shared-self.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-cell-scalar.rs`](../../compiler-labs/module-07/02-cell-scalar.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-refcell-conflict-runtime.rs`](../../compiler-labs/module-07/03-refcell-conflict-runtime.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-try-borrow-conflict.rs`](../../compiler-labs/module-07/04-try-borrow-conflict.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-nested-reborrow-compiles.rs`](../../compiler-labs/module-07/05-nested-reborrow-compiles.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-once-cell-lazy.rs`](../../compiler-labs/module-07/06-once-cell-lazy.rs) | Pass or fail? What exact rule decides? |
| 7 | [`07-stale-once-cell-design.rs`](../../compiler-labs/module-07/07-stale-once-cell-design.rs) | Pass or fail? What exact rule decides? |
| 8 | [`08-rc-refcell-cycle.rs`](../../compiler-labs/module-07/08-rc-refcell-cycle.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 02-rust-ownership-lifetimes-memory
```

## Part 2 — Diagnose and repair


A search index stores `RefCell<Option<Index>>`. `search(&self)` takes a mutable borrow, computes the index by calling `self.tokenize()`, and `tokenize()` calls `self.search_stats()`, which borrows the same cell. The program panics only on a cold cache.

### Repair

- check cache under a short shared borrow;
- release the guard;
- compute the index from immutable text without touching cache-facing methods;
- acquire a mutable borrow only to install;
- separate statistics into `Cell` fields or update after the cache guard is released;
- prohibit callbacks during installation.

### Stronger redesign

If source text is immutable, use `OnceCell<Index>`. If it changes, keep a revision-tagged `RefCell<Option<Index>>` and invalidate under ordinary `&mut self` edits.

## Part 3 — Focused exercises

### Access protocol

Attempt every required exercise and commit the attempt before opening `exercise-answers.md`. Mark each as:


1. Refactor a scalar access counter from `RefCell<u64>` to `Cell<u64>` and explain the simpler aliasing contract.
2. Represent related min/max state atomically in one cell or one `RefCell` value.
3. Predict and verify overlapping `RefCell` borrows; then replace panic with `try_borrow_mut` and a domain error.
4. Shorten a guard that accidentally spans a method call.
5. Refactor nested public-method borrowing into one private helper receiving `&mut State`.
6. Build an immutable-source `OnceCell` index and document reentrant initialization restrictions.
7. Build a revision-tagged mutable cache and prove invalidation.
8. Return a mapped `Ref` view, then compare its usability with an owned range result.
9. Audit an `Rc<RefCell>` graph for cycles and runtime borrow paths.
10. Add capstone cache metrics without making semantic equality depend on them.



## Part 4 — Independent laboratory



Build `IndexedText`, an editable string with a lazily computed line-start index.

```text
labs/module-07-interior-cache/
├── starter/
└── solution/
```

### Required topology

- text and revision mutate only through `&mut self`;
- cache is private interior state reachable through `&self`;
- cache stores the revision it was computed from;
- hit/miss counters use `Cell<u64>`;
- no cache guard escapes the public API;
- public queries return copied ranges or borrowed slices tied to `&self`, not `Ref` unless explicitly justified.

### Required behavior

- line lookup by index;
- cold computation and hot reuse;
- invalidation after append/replace;
- UTF-8-safe ranges;
- no reentrant borrow panic;
- fallible `try_*` diagnostic route for a deliberately held internal borrow in tests;
- metrics excluded from semantic equality.

### Acceptance

```bash
cargo test -p rust-olm-lab-07-interior-cache --all-targets
cargo clippy -p rust-olm-lab-07-interior-cache --all-targets -- -D warnings
```

### Cache state machine

Model the private cache as `Empty` or `Ready { revision, line_starts }`, not as unrelated optional fields whose combinations can contradict one another. A query first checks whether a ready entry matches the current source revision. A miss computes line starts from immutable text without holding a cache guard, then installs the complete result in one mutation phase. Source mutation increments the revision and invalidates the cache before returning.

Line starts are byte offsets, because Rust string slicing operates at UTF-8 boundaries. Tests must contain multibyte characters and verify that every returned range is accepted by `str::get`. Do not claim character-index access unless you actually define and implement character counting.

### Failure and reentrancy tests
Add a private test hook or narrowly scoped diagnostic method that holds a cache borrow while invoking a supplied closure. Use it to prove that the fallible `try_*` route reports `CacheBusy` rather than panicking. The ordinary public query should not expose this hook. Also create a test in which an expensive computation helper calls a read-only source method; it must remain safe because computation occurs outside the mutable cache guard.

Required assertions cover cold miss, hot hit, append invalidation, full replacement, empty text, trailing newline, Unicode text, out-of-range line number, and metric behavior. Counters must not alter equality or the document revision.

### Design note
Provide a borrow timeline for one cache miss and one hit. Mark exactly when each `Ref` or `RefMut` guard is created and dropped. Then justify the public return type: state what callers can retain, what mutation it blocks, and what allocation it requires. The review rejects a design whose safety depends on callers remembering to drop an undocumented guard early.

### Tiered hints

Do not open a later tier until the previous tier has produced a written attempt.

- **Hint 1 — concept:** return to the governing question: Which logically hidden mutation justifies runtime enforcement, and how can guard scope and reentrancy remain controlled?
- **Hint 2 — topology:** draw owners/borrows/states/errors before changing syntax; identify the one boundary that should own the invariant.
- **Hint 3 — structure:** separate validation from mutation and pure transformation from effects. Use the standard operation that encodes the safety fact before inventing an abstraction.
- **Hint 4 — implementation-adjacent:** consult only the relevant standard-library or Reference page; do not open `solution/src`.

The executable starter and reference implementation are in [module-07-interior-cache](../../labs/module-07-interior-cache/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

## Part 5 — Capstone transfer

### Outcomes mapped

- Explain UnsafeCell as the primitive behind interior mutability while remaining within safe APIs.
- Choose Cell for replaceable Copy state and RefCell for single-threaded dynamically checked borrowed state.
- Treat Ref and RefMut as runtime loan guards whose scope is part of the API protocol.
- Avoid reentrant borrow panics by computing outside guards, shortening scopes, or using try_borrow variants and typed errors.
- Design caches whose mutation is observationally transparent, correctly invalidated, and memory-bounded.


Add a private revision-tagged cache to each live capstone document.

The cache contains line starts and normalized search metadata. Shared read methods may populate it. All semantic document edits still require `&mut Document` through validated workspace operations.

### Rules

- cache revision must equal document revision before use;
- mutation increments revision and clears cache;
- cache guards do not cross user callbacks or rendering;
- search returns ranges/views, not `RefCell` guards;
- hit/miss counters are diagnostics only;
- snapshots do not serialize cache state;
- no `Rc<RefCell<Document>>` is introduced.

Add tests for cold/hot queries, edit invalidation, cache-independent equality, and an internal reentrancy regression.



### Capstone defense

Repair a callback-capable cache that holds RefMut across user code, then prove cache invalidation and busy-state behavior.

## Part 6 — Reconstruct and defend

Complete this checkpoint closed-book. Compiler access is allowed only after the prediction portion has been committed.

### Outcome reconstruction

For each outcome, write a claim, one example, one non-example, and one limitation.

- Explain UnsafeCell as the primitive behind interior mutability while remaining within safe APIs.
- Choose Cell for replaceable Copy state and RefCell for single-threaded dynamically checked borrowed state.
- Treat Ref and RefMut as runtime loan guards whose scope is part of the API protocol.
- Avoid reentrant borrow panics by computing outside guards, shortening scopes, or using try_borrow variants and typed errors.
- Design caches whose mutation is observationally transparent, correctly invalidated, and memory-bounded.

### Closed-book checkpoint

1. Explain how interior mutability preserves safe aliasing rules.
2. Choose `Cell` versus `RefCell` for five fields.
3. Predict a runtime borrow panic and shorten the responsible guard.
4. Use `try_borrow_mut` for a valid conflict state.
5. Explain why returning `Ref<T>` extends dynamic borrowing.
6. Prevent reentrant initialization of a lazy cell.
7. Design a revision-tagged cache.
8. Separate physical cache mutation from logical domain constness.
9. Audit `Rc<RefCell<T>>` as two policies, not one idiom.
10. Prove capstone cache invalidation without exposing the cell publicly.

### Transfer defense

Repair a callback-capable cache that holds RefMut across user code, then prove cache invalidation and busy-state behavior.

Your answer must include:

1. What rule does `Cell` enforce by not returning references?
2. What values can `Cell::get` return?
3. What guards does `RefCell` return?
4. When does a borrow conflict panic?
5. How can `try_borrow` change the API?
6. Why must a reference into `RefCell` remain tied to a guard?
7. What does `Ref::map` accomplish?
8. Why release guards before callbacks?
9. What is semantic versus derived mutation?
10. What proves cache freshness?
11. Why store offsets instead of self-references?
12. What happens after text mutation?
13. Why is `RefCell` not thread synchronization?
14. When is ordinary `&mut self` better?
15. What evidence detects reentrancy?

#### Answer notes

`Cell` uses whole-value replacement and gives copies where supported. `RefCell` guards are runtime permission tokens. Mapped guards preserve the token while exposing a subfield. Callbacks can re-enter. Revision/invalidation logic proves freshness, not borrowing. Offsets remain valid across object movement but must be invalidated when text changes. Use `&mut` when mutation can be phased exclusively. Test recursive callback behavior.

#### Transfer task

Build a lazy checksum cache whose calculator can call a read-only metadata method. Prove no guard crosses callback, define same-key recursive behavior, and test invalidation after payload replacement.
