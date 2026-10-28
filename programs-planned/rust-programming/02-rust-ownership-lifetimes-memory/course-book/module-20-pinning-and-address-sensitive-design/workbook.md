# Workbook — Module 20: Pinning and Address-Sensitive Design

[Return to the chapter](index.md) · [Open the Memory Workspace engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether you can use **Pinning and Address-Sensitive Design** without relying on surface syntax. Keep the module question in view: *What invariant becomes invalid after mechanical movement, who promises not to move the value, and can the design avoid address sensitivity entirely?* For every task, identify the program point where the decisive type, ownership, dispatch, failure, or cost relationship is established. Compile only after committing to a prediction, and preserve the smallest counterexample that changes your model.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Pinning and Address-Sensitive Design** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-normal-value-moves.rs`](../../compiler-labs/module-10/01-normal-value-moves.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-box-pin-phantom-pinned.rs`](../../compiler-labs/module-10/02-box-pin-phantom-pinned.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-get-mut-requires-unpin.rs`](../../compiler-labs/module-10/03-get-mut-requires-unpin.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-pin-reborrow.rs`](../../compiler-labs/module-10/04-pin-reborrow.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-stack-pin-escape.rs`](../../compiler-labs/module-10/05-stack-pin-escape.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-move-out-of-pinned-box.rs`](../../compiler-labs/module-10/06-move-out-of-pinned-box.rs) | Pass or fail? What exact rule decides? |
| 7 | [`07-safe-address-token.rs`](../../compiler-labs/module-10/07-safe-address-token.rs) | Pass or fail? What exact rule decides? |
| 8 | [`08-unnecessary-pin-compiles.rs`](../../compiler-labs/module-10/08-unnecessary-pin-compiles.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 02-rust-ownership-lifetimes-memory
```

## Part 2 — Diagnose and repair


A type pins an outer struct and stores a raw pointer into its `String` buffer. A safe method calls `push_str`, which can reallocate the buffer. The author argues that `Pin<Box<Outer>>` keeps everything at one address.

### Diagnosis

Pinning the outer `Outer` allocation stabilizes the location of its fields, including the `String` control block. It does not guarantee the separately allocated string buffer will never reallocate. The internal pointer can dangle after growth.

### Repairs

- freeze the backing text as `Box<str>` before initializing pointers and expose no mutation;
- store ranges rather than pointers and resolve against current text;
- keep mutable `String` but invalidate/recompute derived data by revision;
- use separate immutable shared backing for views.

## Part 3 — Focused exercises

### Access protocol

Attempt every required exercise and commit the attempt before opening `exercise-answers.md`. Mark each as:


1. For ten move operations, distinguish semantic ownership transfer from likely pointee relocation and state which matters to validity.
2. Build a `!Unpin` value with `PhantomPinned`, then pin it safely with `Box::pin` and `pin!`.
3. Compare `Pin<&T>`, `Pin<&mut T>`, and `Pin<Box<T>>` by ownership and access.
4. Attempt `get_mut` on `!Unpin` and explain the rejected move capability.
5. Reborrow a pinned mutable reference for repeated method calls without consuming the original handle.
6. Label structurally pinned and unpinned fields in a supplied type.
7. Audit a destructor for the drop guarantee.
8. Diagnose an internal pointer into a reallocating `String` despite outer pinning.
9. Replace a self-reference with ranges/handles and remove pinning.
10. Complete the full capstone design defense and independent change.



## Part 4 — Independent laboratory



Build an address-sensitive tracker that can be initialized only after pinning and can then report whether every observation occurs at its initialized address. The implementation remains entirely safe Rust.

```text
labs/module-10-pinned-tracker/
├── starter/
└── solution/
```

### Required type

The tracker contains:

- an owned label;
- `Cell<Option<NonNull<PinnedTracker>>>` storing its initialized address;
- an observation counter;
- `PhantomPinned`.

No raw pointer is dereferenced. `NonNull` is used only as a copyable address token obtained safely from a reference.

### Required API

- constructor returns an unpinned, uninitialized value;
- `initialize(self: Pin<&Self>)` records the address once;
- `observe(self: Pin<&Self>)` verifies the current address and increments a counter;
- accessors use `Pin<&Self>` after initialization;
- safe heap and stack pin examples;
- no unchecked pin constructors;
- compile-fail evidence that unrestricted mutable access/move-out is unavailable after pinning;
- no panicking destructor.

### Interpretation

The address token simulates an external registration without performing FFI. The type demonstrates the safe-facing pin contract; it is not a self-referential pointer implementation.

### Acceptance

```bash
cargo test -p rust-olm-lab-10-pinned-tracker --all-targets
cargo clippy -p rust-olm-lab-10-pinned-tracker --all-targets -- -D warnings
```

### Tiered hints

Do not open a later tier until the previous tier has produced a written attempt.

- **Hint 1 — concept:** return to the governing question: What invariant becomes invalid after mechanical movement, who promises not to move the value, and can the design avoid address sensitivity entirely?
- **Hint 2 — topology:** draw owners/borrows/states/errors before changing syntax; identify the one boundary that should own the invariant.
- **Hint 3 — structure:** separate validation from mutation and pure transformation from effects. Use the standard operation that encodes the safety fact before inventing an abstraction.
- **Hint 4 — implementation-adjacent:** consult only the relevant standard-library or Reference page; do not open `solution/src`.

The executable starter and reference implementation are in [module-10-pinned-tracker](../../labs/module-10-pinned-tracker/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

## Part 5 — Capstone transfer

### Outcomes mapped

- Distinguish ownership movement from mechanical relocation and identify genuine address-sensitive invariants.
- Explain Pin<P> as a contract on the pointee mediated by a pointer, not as a magical immovable allocation.
- Use Unpin and PhantomPinned correctly and construct pinned values without exposing moves after invariant activation.
- Reason about structural pinning, field projection, the drop guarantee, and why unsafe projection requires proof beyond compiler acceptance.
- Prefer handles, indices, owned indirection, scoped callbacks, or redesigned state when they eliminate self-reference or address dependence.


Complete the library and CLI, then perform an independent cross-cutting change.

### Required commands

```text
memory-workspace add <title> <text>
memory-workspace show <handle>
memory-workspace edit <handle> <expected-revision> <replacement-text>
memory-workspace rename <handle> <expected-revision> <title>
memory-workspace remove <handle>
memory-workspace search <query>
memory-workspace snapshot <handle>
memory-workspace watch <handle> <revision>
memory-workspace memory-report
memory-workspace demo
```

The CLI may operate as a deterministic scripted in-memory scenario rather than persistence; Course 1 already proved file storage. The capstone's responsibility is memory topology and API proof.

### Hard requirements

- generational stale-handle rejection;
- borrowed views with precise lifetimes;
- staged edit sessions with revision conflict detection;
- immutable fixed snapshots shared by `Rc`;
- weak watchers that do not preserve snapshots;
- revision-tagged interior caches;
- honest memory report;
- no ownership cycles;
- no `unsafe` in production workspace;
- no routine `unwrap`/`expect` in library paths;
- no unnecessary `Pin` in the workspace model.

### Independent feature

Add document labels/tags from a behavioral specification only. The change must cross model, views, snapshots, edit validation, cache invalidation where relevant, memory reporting, CLI rendering, and tests. The implementation route is not supplied.

### Final checks
Run the full proof route, submit ownership graph, lifetime ledger, destruction trace, guarantee ledger, variance trace, and pinning non-use decision. Defend one bug found by each artifact.



### Capstone defense

Audit a proposed self-referential cache, decide whether pinning is necessary, and either derive the full contract or redesign it away.

## Part 6 — Reconstruct and defend

Complete this checkpoint closed-book. Compiler access is allowed only after the prediction portion has been committed.

### Outcome reconstruction

For each outcome, write a claim, one example, one non-example, and one limitation.

- Distinguish ownership movement from mechanical relocation and identify genuine address-sensitive invariants.
- Explain Pin<P> as a contract on the pointee mediated by a pointer, not as a magical immovable allocation.
- Use Unpin and PhantomPinned correctly and construct pinned values without exposing moves after invariant activation.
- Reason about structural pinning, field projection, the drop guarantee, and why unsafe projection requires proof beyond compiler acceptance.
- Prefer handles, indices, owned indirection, scoped callbacks, or redesigned state when they eliminate self-reference or address dependence.

### Closed-book checkpoint

Without notes and against unseen code:

1. Identify the exact address-sensitive invariant, or reject pinning.
2. Explain `Pin<P>` separately from `P`'s ownership.
3. Distinguish `Unpin` and `PhantomPinned` without saying pinned values are immutable.
4. Construct and reborrow pinned values safely.
5. Explain why projection requires field-level proof.
6. State the drop guarantee and leak boundary.
7. Diagnose outer pinning plus inner buffer reallocation.
8. Audit a supplied unsafe pinning abstraction through construction, movement, projection, aliasing, and drop.
9. Defend why the capstone uses handles/ranges rather than self-reference.
10. Complete the independent capstone feature and all verification.
11. Reconstruct the full ownership graph from memory.
12. Explain every runtime borrow-failure path and why valid use avoids it.
13. Separate every memory-report guarantee from observation.
14. Trace one difficult lifetime through variance layers.
15. Name the next-course topics deliberately excluded from this course.

Completion requires executable correctness and a coherent explanation of the design. If you can use `Pin` syntax but cannot reject unnecessary pinning has not mastered the module.

### Transfer defense

Audit a proposed self-referential cache, decide whether pinning is necessary, and either derive the full contract or redesign it away.

Your answer must include:

1. Distinguish semantic and mechanical move.
2. What contract does `Pin<P>` add?
3. What assumptions must already hold when a pin is created?
4. What is `Unpin`?
5. What does `PhantomPinned` do?
6. What does it not do?
7. Why initialize address-sensitive state after pinning?
8. Why publish initialized state last?
9. What is structural pinning?
10. Why is field projection not automatic?
11. Can a pinned struct's heap-owned buffer reallocate?
12. What is the drop guarantee concerned with?
13. Why can `Box<T>` move while the pointee allocation stays?
14. When are handles/offsets superior?
15. What evidence audits safe move prevention?

#### Answer notes

Ownership transfer and byte relocation differ. `Pin` restricts safe access according to a contract; sound construction must already place the pointee so it will not be moved improperly. `Unpin` makes restrictions irrelevant. `PhantomPinned` opts out of automatic `Unpin` but establishes no pointer invariant. Initialize after stable placement and publish last. Pinned outer address does not freeze separately allocated field buffers. Projection/drop require explicit invariants. Compile-fail specimens prove unavailable safe move-out; they do not prove unsafe internals.

#### Transfer task

Write two architecture decisions: one for a callback registration that truly needs pinning, and one for a parser that replaces self-references with byte offsets. Compare initialization, mutation, and teardown obligations.
