# Workbook — Module 14: RAII, Drop, Unwinding, and Failure Atomicity

[Chapter](index.md) · [Laboratory](../../labs/module-04-resource-pool/README.md) · [Memory Workspace guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **RAII, Drop, Unwinding, and Failure Atomicity** has become a usable model rather than remembered vocabulary. Its governing question is: *Which value owns each cleanup obligation, when does destruction run, and what state remains after early return, error, or panic?* Preserve your first prediction and record decisive facts in a **destruction trace**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 13 — Scoped Access and Escape Prevention that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **Which value owns each cleanup obligation, when does destruction run, and what state remains after early return, error, or panic?**
3. Draw the smallest **destruction trace** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **RAII, Drop, Unwinding, and Failure Atomicity** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-direct-drop-call.rs`](../../compiler-labs/module-04/01-direct-drop-call.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-move-field-from-drop-type.rs`](../../compiler-labs/module-04/02-move-field-from-drop-type.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-option-take-transition.rs`](../../compiler-labs/module-04/03-option-take-transition.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-field-drop-order.rs`](../../compiler-labs/module-04/04-field-drop-order.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-explicit-drop-releases-guard.rs`](../../compiler-labs/module-04/05-explicit-drop-releases-guard.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-consuming-commit.rs`](../../compiler-labs/module-04/06-consuming-commit.rs) | Pass or fail? What exact rule decides? |
| 7 | [`07-panicking-destructor-compiles.rs`](../../compiler-labs/module-04/07-panicking-destructor-compiles.rs) | Pass or fail? What exact rule decides? |
| 8 | [`08-forgotten-guard-compiles.rs`](../../compiler-labs/module-04/08-forgotten-guard-compiles.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 02-rust-ownership-lifetimes-memory
```

## Part 2 — Diagnose and repair

A document editor uses three booleans:

```rust
struct Editor<'a> {
    target: &'a mut String,
    active: bool,
    committed: bool,
    rolled_back: bool,
    backup: String,
}
```

Methods can produce contradictory combinations such as committed and rolled back. `Drop` branches over the booleans and calls a logging callback that may panic. Commit mutates the target before a fallible validation step.

### Repair

1. Replace contradictory flags with an enum or `Option<WorkingState>`.
2. Validate staged state before changing the target.
3. Make `commit(self)` consuming.
4. Keep `Drop` limited to infallible local restoration.
5. Move fallible reporting into `commit`/`cancel` return values.
6. Add a panic test for a mutation method that runs user-provided validation.

### Strong design

A staged session owns `working: String`, a target handle, and expected revision. It performs validation on the working copy. Commit asks the workspace to revalidate the handle/revision and swap. If commit fails, return an error carrying the still-owned session when retry is meaningful, or consume and report a terminal conflict when it is not.

### Questions

- Does a session borrow the workspace for its whole lifetime?
- Can two sessions target different documents?
- Can two sessions target the same revision?
- Which type represents conflict?
- Is rollback observable or merely absence of commit?
- What happens if the session is leaked?

The repair must answer these through types and method signatures, not comments over Boolean combinations.

## Part 3 — Focused exercises

### Access protocol

Attempt every required exercise and commit the attempt before opening `exercise-answers.md`. Mark each as:

### Exercise 1 — Destruction trace

Predict exact drop order for nested locals, tuple fields, struct fields, a shadowed binding, and an early return. Verify with a `Trace` type.

### Exercise 2 — Narrow guard

Refactor a guard that borrows an entire `Workspace` only to restore one `bool`. Make it borrow the field or a dedicated state component and demonstrate unrelated access remains possible.

### Exercise 3 — Field extraction

Implement a type with an owned buffer and a destructor. Safely transfer the buffer through an explicit consuming method using `Option::take`. Prove the destructor does not process it twice.

### Exercise 4 — Pool lease

Design a `Lease<'a, T>` that checks one item out of a `Vec<T>` and returns it on drop. Add explicit `discard(self)` and `replace(self, T)` transitions without direct destructor calls.

### Exercise 5 — Strong edit guarantee

Implement a staged string edit. A closure mutates the working copy and may panic. Prove the target remains unchanged until consuming commit.

### Exercise 6 — Basic guarantee

Write an in-place transformation that documents partial progress after panic. Explain why it remains valid even though it lacks rollback.

### Exercise 7 — Fallible finish

Design a writer-like type whose `finish(self)` can return an I/O error while `Drop` performs only infallible local cleanup. Specify what the caller loses by relying only on drop.

### Exercise 8 — Leak review

Use `mem::forget` on your lease in a test. Document the logical consequence. Explain why safe APIs cannot treat destructor execution as a memory-safety precondition.

### Exercise 9 — Double panic audit

Find every operation in a destructor that could panic, including indexing and formatting assumptions. Replace or justify it.

### Exercise 10 — Capstone session

Choose borrow-held or handle/revision edit sessions for `memory-workspace`. Defend isolation, conflict, and leaked-session behavior.

### Interleaved reasoning pass

1. For **Derive local, field, tuple, temporary, and scope destruction order from documented rules**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the destruction trace.
2. For **Design RAII guards whose ownership encodes exactly one cleanup or release obligation**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the destruction trace.
3. For **Use Option::take, mem::replace, staged candidates, and consuming transitions while preserving valid states**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the destruction trace.
4. For **Distinguish no-throw, basic, and strong in-memory failure guarantees from crash durability**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the destruction trace.

5. Identify one guarantee from an earlier course that a careless implementation of **RAII, Drop, Unwinding, and Failure Atomicity** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

### Product

Build a generic single-threaded resource pool whose checked-out item is owned by a lease guard and automatically returned unless an explicit consuming transition says otherwise.

```text
labs/module-04-resource-pool/
├── starter/
└── solution/
```

### Required API

```rust
pub struct Pool<T> { /* private */ }
pub struct Lease<'a, T> { /* private */ }

impl<T> Pool<T> {
    pub fn new(items: Vec<T>) -> Self;
    pub fn available(&self) -> usize;
    pub fn checkout(&mut self) -> Option<Lease<'_, T>>;
}

impl<T> Lease<'_, T> {
    pub fn get(&self) -> &T;
    pub fn get_mut(&mut self) -> &mut T;
    pub fn discard(self);
    pub fn replace(self, replacement: T) -> T;
}
```

`replace` returns the checked-out item and puts the replacement into the pool. Ordinary drop returns the checked-out item. `discard` permanently removes it.

### Design constraints

- no cloning requirement on `T`;
- no direct call to `Drop::drop`;
- no `unsafe`, raw pointers, reference counting, or interior mutability;
- no destructor panic under any represented state;
- the item is acted on at most once;
- method signatures make double return impossible;
- tests include ordinary return, mutation, discard, replace, early return, and panic unwinding.

### Limitation analysis

Because `Lease` borrows the pool mutably, only one lease can exist and the pool cannot be inspected directly while the lease is active. This is intentional in Module 14. Later modules can compare a `RefCell`-backed or shared-ownership topology, but do not weaken this lab to anticipate them.

### Acceptance

```bash
cargo test -p rust-olm-lab-04-resource-pool --all-targets
cargo clippy -p rust-olm-lab-04-resource-pool --all-targets -- -D warnings
```

### Tiered hints

Do not open a later tier until the previous tier has produced a written attempt.

- **Hint 1 — concept:** return to the governing question: Which value owns each cleanup obligation, when does destruction run, and what state remains after early return, error, or panic?
- **Hint 2 — topology:** draw owners/borrows/states/errors before changing syntax; identify the one boundary that should own the invariant.
- **Hint 3 — structure:** separate validation from mutation and pure transformation from effects. Use the standard operation that encodes the safety fact before inventing an abstraction.
- **Hint 4 — implementation-adjacent:** consult only the relevant standard-library or Reference page; do not open `solution/src`.

The executable starter and reference implementation are in [module-04-resource-pool](../../labs/module-04-resource-pool/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

### Laboratory acceptance trace

Before opening the reference implementation for **RAII Resource Pool**, record:

- the public behavior that demonstrates **Derive local, field, tuple, temporary, and scope destruction order from documented rules**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

### Outcomes mapped

- Derive local, field, tuple, temporary, and scope destruction order from documented rules.
- Design RAII guards whose ownership encodes exactly one cleanup or release obligation.
- Use Option::take, mem::replace, staged candidates, and consuming transitions while preserving valid states.
- Distinguish no-throw, basic, and strong in-memory failure guarantees from crash durability.
- State when destructors may not run or cannot report failure, including abort, process exit, leaks, and power loss.

Add an owned `EditSession` to `memory-workspace`.

### Topology

The session contains:

- a `DocumentHandle`;
- the target revision observed at creation;
- an owned working title/text;
- optional staged metadata;
- no reference into the workspace.

Creation borrows the workspace briefly to clone the current document into staged state. The borrow then ends.

### Commit

`Workspace::commit(session)` must:

1. validate the handle generation;
2. validate the expected revision;
3. validate all staged text/ranges;
4. swap in staged state only after validation succeeds;
5. increment revision with checked arithmetic;
6. invalidate or recompute caches;
7. return a receipt containing handle and new revision.

A conflict must leave the workspace unchanged. Decide whether the error returns the session for inspection/retry.

### Drop behavior

Dropping an uncommitted session discards owned staged state. No custom destructor is required unless the course adds observable rollback metrics. Prefer ordinary field destruction over an empty ceremonial `Drop` implementation.

### Panic-path tests
Run a user-supplied transformation against the working copy before commit. A panic must not alter the live document. Catching the panic is test machinery, not application error handling.

### Why RAII still matters without custom `Drop`

The owned session itself is RAII: uncommitted working allocations are reclaimed and cannot affect live state. `Drop` should be implemented only when a protocol action beyond ordinary field destruction is necessary.

### Capstone defense

Review a boolean transaction guard, redesign it as an ownership protocol, and specify its exact unwind and explicit-finish guarantees.

### Capstone invariant trace

For the Module 14 Memory Workspace increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Complete this checkpoint closed-book. Compiler access is allowed only after the prediction portion has been committed.

### Outcome reconstruction

For each outcome, write a claim, one example, one non-example, and one limitation.

Without reopening the chapter, reconstruct the outcomes for **Module 14: RAII, Drop, Unwinding, and Failure Atomicity**. Compare your list with the earlier outcome map only after writing it, then mark each item as modelled, predicted, repaired, built, transferred, or still unsupported.

### Closed-book checkpoint

Without notes:

1. Trace local, struct-field, and temporary destruction for an unseen program.
2. Explain why safe code cannot directly call `Drop::drop`.
3. Move an owned field out of a drop type using a valid state transition.
4. Design a guard whose cleanup cannot happen twice.
5. State basic and strong panic guarantees for two different operations.
6. Explain double-panic risk in destructors.
7. State four situations where normal stack destructors may not run.
8. Separate RAII rollback from durable crash consistency.
9. Defend whether a custom `Drop` implementation is needed for an owned staged edit.
10. Explain the consequence of leaking a guard without making a memory-safety claim.

At this point, you treat destruction as a protocol with explicit limits, not as magical guaranteed finalization.

### Transfer defense

Transfer **Module 14: RAII, Drop, Unwinding, and Failure Atomicity** to a product unrelated to the course capstone. Change the domain model and failure mode, preserve the governing relationship, and identify which part of the original design was essential rather than accidental.

Your answer must include:

- the governing rule for **Module 14: RAII, Drop, Unwinding, and Failure Atomicity** in plain language;
- state, ownership, or authority before and after the decisive operation;
- one causal negative case that fails for the intended reason;
- one principled repair and one easier repair that deletes a requirement;
- the limit of the evidence you used;
- one transfer to a product with different data and failure behavior.


1. What does RAII bind to value lifetime?
2. Why can ordinary ownership provide RAII without custom `Drop`?
3. When is a guard needed?
4. Why should `Drop` not return a recoverable error?
5. What happens if `Drop` panics during unwinding?
6. How does `Option::take` disarm cleanup?
7. What runs first: destructor body or field drops?
8. In what order do struct fields drop?
9. What state must construction leave on partial failure?
10. How do you test panic restoration?
11. Why is `mem::forget` relevant?
12. What is a consuming transition?
13. When should interrupted resources be quarantined?
14. Why avoid user callbacks in destructors?
15. When is immutable staging better than rollback?

#### Answer notes

RAII ties acquisition/release obligations to owned values. A staged edit already abandons work when dropped; no custom destructor is necessary. Guards encode restoration obligations. Destructor bodies run before fields, fields in declaration order. Construction must either establish a valid guard or leave original state restored. Test post-panic state. Leaks and aborts limit cleanup guarantees. Quarantine resources whose invariants may be damaged. Prefer staging when fallible rollback would be complex.

#### Transfer task

Implement a directory-like current-context guard over an in-memory path stack. Add commit, rollback, panic tests, nested guards, and a written leak limitation.

### Closed-book defense

In five minutes, answer “Which value owns each cleanup obligation, when does destruction run, and what state remains after early return, error, or panic?” using the **destruction trace**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside Memory Workspace. A list of APIs without the deciding relationship is incomplete.
