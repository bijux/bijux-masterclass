# Module 14 — RAII, Drop, Unwinding, and Failure Atomicity

**Course 2 · Day 4 · Module 14 of 100**
`████░░░░░░░░░░░░░░░░░░░░░` **14/100**

[Program](../../../README.md) · [Course 2](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-04-resource-pool/README.md) · [Memory Workspace guide](../capstone.md)

[← Module 13: Scoped Access and Escape Prevention](../module-13-scoped-access-and-escape-prevention/index.md) · [Module 15: Box, Deref, Dynamically Sized Types, and Cow →](../module-15-box-deref-dynamically-sized-types-and-cow/index.md)

## The question

> Which value owns each cleanup obligation, when does destruction run, and what state remains after early return, error, or panic?

## Why this comes now

Borrowing governs access while values live; RAII governs what happens when ownership ends. This module connects destruction order, guards, explicit commit, unwind behavior, and failure atomicity. It is the point where ownership becomes a protocol for reliable cleanup rather than only a restriction on aliasing.

### Prerequisite bridge

Module 13 established **Scoped Access and Escape Prevention**. Before continuing, verify that you can recognize self-reference pressure and choose indices, owned state, callbacks, or later pinning only when justified. This module preserves that capability and adds the ability to derive local, field, tuple, temporary, and scope destruction order from documented rules. Module 15, **Box, Deref, Dynamically Sized Types, and Cow**, will rely on both when it asks: *When is indirection required by representation or ownership, what metadata travels with a pointer, and when should an API borrow-or-own conditionally?*

### Scope boundary

This module owns the reasoning for **raii, drop, unwinding, and failure atomicity** inside Course 2. The course remains centered on safe public APIs. It explains the memory obligations behind smart pointers, interior mutability, layout, variance, and pinning, but manual allocation, raw-pointer implementation, FFI, threads, and async execution remain later responsibilities. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- Derive local, field, tuple, temporary, and scope destruction order from documented rules.
- Design RAII guards whose ownership encodes exactly one cleanup or release obligation.
- Use Option::take, mem::replace, staged candidates, and consuming transitions while preserving valid states.
- Distinguish no-throw, basic, and strong in-memory failure guarantees from crash durability.
- State when destructors may not run or cannot report failure, including abort, process exit, leaks, and power loss.

## Core model

### RAII as obligation ownership

RAII means a value owns a resource or cleanup obligation and its destructor performs the non-fallible cleanup associated with relinquishing that ownership. Examples include closing a file handle, releasing a borrow guard, returning a lease to a pool, or restoring local state during unwinding.

The crucial question is not “where can I add Drop?” It is “which value uniquely owns the obligation, and what state must remain valid when destruction begins?”

### Destruction order is structured

Rust defines drop scopes and destruction order. Important categories must not be collapsed into one slogan:

- local variables are dropped in reverse declaration/creation order within their drop scope;
- struct fields are dropped in declaration order after the type's own `Drop::drop` returns;
- tuple elements are dropped in element order;
- temporaries have scopes determined by expression rules;
- early return and unwinding leave scopes and run ordinary destructors along the path;
- aborting or process termination may bypass unwinding/destruction.

Build a trace type and predict the exact sequence before execution. Do not generalize from one trace to undocumented representation details.

### Valid states during mutation

Rust does not allow a field of a live value to be left uninitialized through safe code. Use `Option::take`, `mem::replace`, or staged owned state:

```rust
struct Session {
    pending: Option<String>,
}

impl Session {
    fn finish(mut self) -> Option<String> {
        self.pending.take()
    }
}
```

The `Option` explicitly represents whether the obligation remains. A consuming `finish(self)` can ensure the guard is not used again and can suppress default cleanup by changing state.

### Guard protocols

A resource-pool lease might borrow the pool and own one resource. Dropping an unfinished lease returns the resource; consuming `take` transfers it out and changes the obligation. The destructor must be non-panicking and cannot report failure to the caller. Operations that can fail meaningfully need an explicit `finish`/`commit` method returning `Result`.

```rust
pub struct Lease<'a, T> {
    pool: &'a mut Vec<T>,
    resource: Option<T>,
}

impl<T> Drop for Lease<'_, T> {
    fn drop(&mut self) {
        if let Some(resource) = self.resource.take() {
            self.pool.push(resource);
        }
    }
}
```

This design holds a mutable borrow of the pool for the lease duration, which may be too restrictive. An ownership-based pool or interior-mutability design has different trade-offs. The lab makes the topology explicit.

### Panic/failure guarantee levels

For an operation under its stated failure model:

- **no guarantee:** state may violate invariants or be unusable;
- **basic guarantee:** state remains valid/destructible, but may be changed;
- **strong guarantee:** failure leaves externally visible state unchanged;
- **no-fail:** under preconditions, operation cannot fail.

These are in-memory reasoning labels. They do not automatically imply filesystem crash consistency.

### Staged candidate state

For document editing, cloning current owned fields into an `EditSession` can be a justified cost. The live document remains unchanged while the session is modified. Commit validates the complete candidate and revision, computes the next revision, then replaces live fields. Dropping the session abandons candidate state with no rollback log.

```text
live document ──clone──> owned candidate session
      │                         │
      │ remains readable        ├─ validate
      │                         ├─ revision check
      └──────── commit <────────┴─ replace fields
```

This provides a strong reported-failure guarantee for the in-memory workspace, at the cost of peak memory and runtime conflict detection.

### Limits of Drop

Destructors may not run under `panic = abort`, process exit, power loss, deliberate leaks such as `mem::forget`, or other termination outside ordinary unwinding. Destructors cannot return errors. A destructor that panics during unwinding can abort the process. Therefore:

- use Drop for local non-fallible cleanup or rollback;
- use explicit completion for fallible flush/sync/commit;
- define leak tolerance where relevant;
- never call a disk protocol durable merely because a guard has Drop.

### Derive it yourself

Design an environment-variable override guard. State behavior on normal drop, explicit commit, nested guards, callback panic, and process abort. Decide whether restoring can fail and how that changes the design.

### Misconception clinic

- Drop is deterministic inside ordinary scope/unwind semantics, not universal finalization.
- “Reverse order” does not describe every field/temporary category.
- RAII rollback and durable crash consistency are different protocols.
- A staged candidate may be simpler and safer than an undo log when memory cost is acceptable.

Resource Acquisition Is Initialization means that acquiring a resource or entering a protocol state creates a value whose ownership represents the obligation to leave that state correctly. When the value is destroyed, its destructor performs infallible cleanup.

The resource may be memory, but need not be:

- a file or socket descriptor;
- a temporary directory;
- a checked-out pool item;
- a “currently editing” flag;
- a metrics span;
- a rollback snapshot;
- a lock guard in later concurrent code.

### The guard is the proof object

```rust
struct FlagGuard<'a> {
    flag: &'a mut bool,
}

impl<'a> FlagGuard<'a> {
    fn enter(flag: &'a mut bool) -> Self {
        assert!(!*flag, "scope already entered");
        *flag = true;
        Self { flag }
    }
}

impl Drop for FlagGuard<'_> {
    fn drop(&mut self) {
        *self.flag = false;
    }
}
```

While `FlagGuard` exists, the original flag remains exclusively borrowed. The caller cannot independently set it to a contradictory state. On normal return or unwinding, `drop` restores it.

### Acquisition must establish the invariant fully

A constructor should either return a complete guard or fail without leaving a cleanup obligation unrepresented. If acquisition has several steps, use local RAII values for each successful step so an error in a later step naturally releases earlier resources.

Avoid “initialized” booleans scattered across the caller. They create paths where a resource exists but no owner is responsible for it.

### Cleanup should be minimal and local

A destructor should perform the smallest action needed to restore the invariant. Complex policy, logging that can fail, network communication, or user callbacks in `Drop` increase the chance of reentrancy and double-panic problems.

### Explicit close can coexist with `Drop`

A type may expose a consuming method that reports errors:

```rust
struct Writer {
    // resource fields
}

impl Writer {
    fn finish(mut self) -> std::io::Result<()> {
        // perform fallible flush/commit here
        self.mark_finished();
        Ok(())
    }

    fn mark_finished(&mut self) {
        // leave destructor with no fallible work
    }
}
```

`Drop` remains the safety net for basic cleanup. The explicit method is the path for fallible completion and error reporting. Callers who care about completion errors must call it.

### Ownership topology question

A guard normally borrows or owns exactly the state required for cleanup. If it borrows `&mut WholeSystem` merely to reset one flag, it can block unrelated work. Split state or give the guard a narrow field reference. Module 11's place reasoning and RAII design are inseparable.

Destruction is deterministic at ordinary scope boundaries, but the exact order depends on how values are stored and introduced. Correct RAII designs must not rely on folklore.

### Local bindings

Local variables are normally dropped in reverse order of declaration when their drop scope ends:

```rust
let first = Trace("first");
let second = Trace("second");
// second drops before first
```

Shadowing introduces a new binding; it does not necessarily destroy the old value at the shadowing statement. Track each binding separately.

### Struct fields

Fields of a struct are dropped in declaration order after the struct's own `Drop::drop` method returns. Declaration order, not constructor expression order, controls field destruction.

```rust
struct Bundle {
    session: Trace,
    buffer: Trace,
}
```

If `session` cleanup depends on `buffer` still existing, declaration order above supports that: `session` is dropped first. Such dependencies should be documented and preferably minimized.

### Tuples, arrays, and collections

Tuple elements are dropped in field order. Array and slice elements are dropped from first to last. Standard collections define behavior through their own implementations; do not infer undocumented order when your invariant does not require it.

### Temporaries

Temporary values have drop scopes determined by expression context. A temporary can be extended in certain `let` bindings, while a temporary created as part of a statement is often dropped at the end of that statement.

```rust
let borrowed = &String::from("extended");
println!("{borrowed}");
```

Temporary lifetime extension makes this common pattern valid. Do not generalize it to every function call or match expression. When cleanup order matters, bind values explicitly.

### Explicit early destruction

`std::mem::drop(value)` consumes `value`, causing destruction at that point. Calling a destructor method directly is not allowed; `Drop::drop` is invoked by the language.

Early drop is useful to release a long mutable borrow represented by a guard:

```rust
let guard = begin_edit(&mut document);
// work through guard
drop(guard);
// document is directly usable again
```

Often the final use is enough for non-lexical borrow shortening, but explicit `drop` documents protocol closure and works for types whose destructor has observable effects.

### Destruction trace discipline

For a nontrivial scope, create a table:

| value | acquired | owns/borrows | explicit close | normal drop order | unwind action |
|---|---|---|---|---|---|

If correctness depends on two destructors running in a particular order, encode that order structurally and test it with a trace type.

A method cannot normally move a non-`Copy` field out through `&mut self` because the caller still owns the containing value and its destructor may later observe the field. The repair is to leave a valid replacement.

### `mem::replace`

```rust
use std::mem;

struct Slot {
    value: String,
}

impl Slot {
    fn replace(&mut self, next: String) -> String {
        mem::replace(&mut self.value, next)
    }
}
```

The old value is returned; the field is never uninitialized.

### `mem::take`

When `T: Default`, `mem::take` replaces a field with `T::default()`:

```rust
fn drain_text(slot: &mut Slot) -> String {
    std::mem::take(&mut slot.value)
}
```

Use it only when the default state is a valid, meaningful state. An empty string may be valid for a buffer but invalid for a required identifier.

### `Option::take`

`Option<T>` is the clearest representation when a field may be present during one protocol phase and absent after transfer:

```rust
struct Lease<T> {
    item: Option<T>,
}

impl<T> Lease<T> {
    fn take_item(&mut self) -> Option<T> {
        self.item.take()
    }
}
```

The type records the state transition. A destructor can check `Some` and act exactly once.

### State machines beat sentinel defaults

Replacing a required resource with a fake “empty” object can make methods callable in an invalid state. Prefer an enum:

```rust
enum Transaction<T> {
    Active { original: T, working: T },
    Committed,
}
```

or consume `self` during the transition so the invalid predecessor cannot be reused.

### Partial initialization during construction

Local values already initialized before an error are dropped automatically. This allows staged construction without manual cleanup flags:

```rust
fn build() -> Result<Bundle, Error> {
    let first = acquire_first()?;
    let second = acquire_second()?;
    Ok(Bundle { first, second })
}
```

If the second acquisition fails, `first` is dropped. This property is a primary reason to wrap each acquired resource immediately.

### Destructors and taking

A destructor receives `&mut self`, so `Option::take` is often used when cleanup requires consuming an owned field. The destructor must leave the struct in a valid state while it runs, even though the struct will then be deallocated. This avoids double destruction of the moved field.

### Review question

Whenever you see `Option<T>` used only to satisfy `Drop`, ask whether absence is a real protocol state. If it is, document it. If not, a different ownership arrangement or explicit consuming finish method may be clearer.

A guard can encode a two-outcome protocol:

- if explicitly committed, preserve the new state;
- otherwise, roll back on destruction.

### Consuming commit

```rust
struct Edit<'a> {
    target: &'a mut String,
    original: Option<String>,
}

impl<'a> Edit<'a> {
    fn new(target: &'a mut String) -> Self {
        let original = target.clone();
        Self {
            target,
            original: Some(original),
        }
    }

    fn text_mut(&mut self) -> &mut String {
        self.target
    }

    fn commit(mut self) {
        self.original = None;
    }
}

impl Drop for Edit<'_> {
    fn drop(&mut self) {
        if let Some(original) = self.original.take() {
            *self.target = original;
        }
    }
}
```

`commit(self)` consumes the guard, preventing further edits. It marks rollback unnecessary; destruction then performs no restoration.

This simple implementation clones the original. In the capstone, edits may stage a separate working copy and swap only at commit, which provides a stronger guarantee without mutating the live document during the session.

### Commit should not silently fail

If commit requires fallible I/O, a consuming `commit(self) -> Result<...>` must preserve a coherent cleanup path on error. Because `self` is being consumed, fields may need `Option::take` or an internal state enum. The destructor cannot report an error after the fact.

### Cancellation can be explicit

A `cancel(self)` method can document intent, even if dropping has the same effect. It may return useful information, such as the staged edit or reason. Explicit cancellation also provides a place for fallible or observable work that should not occur in `Drop`.

### Borrow scope is part of the protocol

While an edit guard holds `&mut Document`, no other direct access to that document is possible. This protects the invariant but can be too restrictive if the session needs to inspect unrelated workspace state. Alternatives include:

- stage owned changes without borrowing the workspace for the whole session;
- split fields so the guard borrows only the edited component;
- use handles and revalidate at commit;
- later, use carefully justified interior mutability.

The correct guard topology depends on whether isolation or concurrency of operations matters.

### Guard methods should preserve a valid rollback state

Each mutating guard method must leave enough information for `Drop` to restore the invariant if the next operation panics. Avoid temporarily taking the only rollback copy and then running arbitrary user code.

### Commit token pattern

For complex protocols, commit can return an owned token or result proving the transition completed. Callers should not infer success merely because a guard disappeared; it might have rolled back through ordinary drop.

When Rust is configured to unwind, a panic walks back through stack frames and drops initialized local values. RAII guards therefore run on both normal exit and unwinding. This is powerful but not universal.

### Three useful guarantee levels

#### No safety violation

Even after panic, safe APIs must not expose memory unsafety. This is non-negotiable for safe abstractions.

#### Basic guarantee

The value remains valid and destructible, but its logical contents may reflect a partial operation. A collection transformation might have processed the first several elements before a callback panics.

#### Strong guarantee

The operation either completes fully or leaves the externally visible state unchanged. Staging changes and swapping at commit is a common technique.

A fourth concept, “no-fail,” applies only when an operation is guaranteed not to fail under its preconditions.

### User callbacks are panic boundaries

If a method calls caller code while an invariant is temporarily broken, a panic can expose the broken state to destructors or later code. Restore the invariant before invoking callbacks, use a guard that repairs it, or stage work separately.

### `catch_unwind` is not ordinary error handling

`std::panic::catch_unwind` catches unwinding panics, subject to unwind-safety bounds. It does not catch process aborts and should not convert internal programming defects into routine `Result` values indiscriminately. It is mainly useful at isolation boundaries such as plugin execution or tests of panic behavior.

### Unwind safety types

`UnwindSafe` and `RefUnwindSafe` are marker traits that help identify captured state whose invariants might be observed after a caught panic. They are a speed bump, not an unsafe-code boundary. Interior-mutability types often require special scrutiny because they can expose partially mutated state.

### Double panic

If a destructor panics while the thread is already unwinding from another panic, the process normally aborts. Destructors should therefore avoid panicking. Assertions, indexing assumptions, allocation-heavy formatting, or callbacks inside `Drop` deserve review.

### Panic strategy and process events

With `panic = "abort"`, stack unwinding and destructors for intervening stack values do not run. Operating-system process termination, `process::exit`, power failure, and `mem::forget` can also bypass ordinary cleanup. RAII is deterministic within its execution model; it is not durable transaction logging.

### Capstone consequence

An in-memory edit can use RAII rollback for unwind safety. Persisted data requires a separate atomic-write protocol. Do not claim that a destructor makes disk updates crash-safe.

`Drop` is reliable for ordinary destruction paths but deliberately cannot enforce every resource policy.

### Destructors cannot return errors

The trait method is:

```rust
fn drop(&mut self)
```

There is no result channel. Fallible flush, commit, close, or remote acknowledgement must occur in an explicit method. A destructor may make a best effort, but callers cannot treat silence as confirmed success.

### Safe Rust permits leaks

`std::mem::forget` consumes a value without running its destructor. Reference-counting cycles can also keep values alive indefinitely. `Box::leak` intentionally converts owned allocation into a long-lived borrow. Therefore, unsafe code may not rely on every destructor inevitably running for memory safety.

This course stays in safe Rust, but the design lesson is broader: `Drop` should maintain local resource hygiene, not serve as the sole guardian of an externally critical invariant.

### `process::exit` and abort

Immediate process termination does not unwind ordinary stack frames. OS-managed resources are reclaimed by the OS, but application-level actions—flushing user-space buffers, deleting temporary files, releasing distributed leases—may not happen.

### Leaking a guard

If forgetting a guard leaves an object permanently marked “editing,” the API is logically vulnerable to a safe leak. That may be acceptable if the object becomes unusable rather than unsafe. It must not allow aliasing or memory unsafety.

This is why the standard library's unsafe abstractions assume destructors may be skipped. Safe product APIs should similarly avoid irreversible external corruption when a guard is leaked.

### Idempotence

Cleanup often benefits from being idempotent: repeated attempts have no additional harmful effect. `Option::take` helps ensure a destructor acts at most once within a value. External resources may need their own idempotency tokens.

### Explicit completion pattern

Expose:

```text
finish(self) -> Result<Receipt, Error>
```

and document that dropping without `finish` performs only best-effort rollback or release. Tests should cover both paths.

### Do not suppress all destructor observability

A destructor may update in-memory counters or return a pool item. Such work is appropriate when infallible and local. The rule is not “Drop may only free memory”; it is “Drop must remain robust under constrained and surprising exit paths.”

A transaction-like in-memory edit should define isolation, visibility, commit, rollback, and conflict behavior explicitly.

### In-place with snapshot

The guard mutates live state and keeps an original snapshot for rollback. Reads through the guard see new state; other access is usually blocked by an exclusive borrow. Cost is proportional to snapshot size even when few bytes change.

### Staged working copy

The session owns a separate working value and borrows or identifies the target. Live state remains unchanged until commit swaps the working value in. A panic during editing leaves live state untouched. This is often the simplest strong guarantee.

```rust
struct StagedEdit<'a> {
    target: &'a mut String,
    working: Option<String>,
}

impl<'a> StagedEdit<'a> {
    fn new(target: &'a mut String) -> Self {
        Self {
            working: Some(target.clone()),
            target,
        }
    }

    fn working_mut(&mut self) -> &mut String {
        self.working.as_mut().expect("working state is present before commit")
    }

    fn commit(mut self) {
        if let Some(working) = self.working.take() {
            *self.target = working;
        }
    }
}
```

Production code under this course's lint policy would avoid `expect` by representing active/finished state more directly or handling the impossible branch explicitly.

### Handle-based optimistic session

The session stores a handle, original generation/revision, and owned working state without borrowing the workspace continuously. At commit, it revalidates that the document still exists and has the expected revision. This permits unrelated workspace activity but introduces conflict errors.

The capstone uses this approach because a ten-day memory course should expose the trade between borrow-enforced isolation and handle/revision validation.

### Undo log

For large data, an undo log can record inverse operations rather than clone the whole value. Every mutation must append enough information before changing live state. Panic ordering becomes critical. This pattern belongs in later production/performance work unless data scale justifies it.

### Invariants

For every edit strategy, specify:

- whether uncommitted state is externally visible;
- what happens when the target is removed;
- whether commit can fail;
- whether rollback allocates or panics;
- whether a leaked session blocks future work;
- which revision changes invalidate saved ranges and views.

“RAII rollback” is not a complete transaction design until these questions are answered.

### Obligation inventory

List every acquired obligation and the value that owns it. An obligation without a unique owner is a cleanup bug waiting for an early return.

### Exit matrix

For each public operation, inspect:

| exit | destructors run? | expected state |
|---|---|---|
| success | yes for locals | committed or released |
| returned error | yes for locals | unchanged or documented partial state |
| unwind panic | normally yes | valid, preferably rolled back |
| abort / process exit | not guaranteed | no memory-safety reliance on cleanup |
| leaked guard | no | logical degradation only, never unsafety |

### Destructor audit

A destructor should be:

- infallible in its type contract;
- non-panicking under reachable state;
- bounded in work;
- free of arbitrary callbacks;
- safe when called during unwinding;
- correct after every partial protocol state represented by the type.

### Ownership-width audit

Check whether the guard borrows too much. A guard on one document should not freeze an entire workspace unless atomic cross-workspace isolation is required.

### Commit audit

A consuming commit should make double commit impossible. A fallible commit must specify ownership of the resource after failure. If the caller can retry, the error may need to return the session.

A test helper temporarily sets several process-like configuration values in an in-memory environment and must restore them after normal completion, `?`, or panic.

### Protocol

The environment uniquely owns a map. `OverrideGuard` records prior states:

```text
key existed -> old owned value
key absent -> absence marker
```

Construction validates every requested key and clones only the old values required for restoration. It then applies changes. If application itself can fail midway, either prepare a complete new map and swap once, or roll back already-applied keys before returning construction error.

### Guard state

```rust
struct OverrideGuard<'a> {
    environment: &'a mut Environment,
    previous: Vec<(String, Option<String>)>,
    active: bool,
}
```

`Drop` restores only when active. A consuming `commit(mut self)` sets `active = false`, preserving overrides. A consuming `rollback(mut self)` performs restoration explicitly and disarms destructor. Restoration code should be shared through an internal infallible method.

### Borrow cost

Because the guard holds `&mut Environment`, callers cannot inspect the environment through its original binding. Methods on the guard can expose read-only access. If tests need broad simultaneous access, an alternative is to own the environment in a transaction value and return it, or use an index/handle-backed store. `RefCell` would trade this static restriction for runtime conflict.

### Unwinding

During callback panic, locals created after the guard drop first, then the guard restores. Its destructor must not format through user-defined code or allocate unnecessarily. If restoration can fail, process-like environment mutation cannot be made reliably transactional through `Drop`; explicit cleanup and documented best effort are required.

### Drop order test

Use probes to record:

1. callback local destruction;
2. override restoration;
3. environment destruction.

Do not assert unspecified order among hash-map entries. Test semantic restored values after `catch_unwind`.

### Leak boundary

`mem::forget(guard)` leaves overrides active. Safe Rust permits leaking. RAII guarantees cleanup under ordinary destruction/unwinding, not under deliberate forget, process abort, or power loss. State this limitation.

### Safer alternative

For purely in-memory configuration, the strongest API may avoid mutation entirely: clone a small configuration, apply overrides to the clone, and pass `&Config` to the operation. This is semantic duplication because two configurations coexist. RAII is useful when a shared resource truly must be restored, not when immutable value passing solves the domain.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For derive local, field, tuple, temporary, and scope destruction order from documented rules, construct one positive and one causal negative example. Mark the first decisive fact in the **destruction trace** and state which evidence could falsify the claim.

2. **Outcome 2.** For design RAII guards whose ownership encodes exactly one cleanup or release obligation, construct one positive and one causal negative example. Mark the first decisive fact in the **destruction trace** and state which evidence could falsify the claim.

3. **Outcome 3.** For use Option::take, mem::replace, staged candidates, and consuming transitions while preserving valid states, construct one positive and one causal negative example. Mark the first decisive fact in the **destruction trace** and state which evidence could falsify the claim.

4. **Outcome 4.** For distinguish no-throw, basic, and strong in-memory failure guarantees from crash durability, construct one positive and one causal negative example. Mark the first decisive fact in the **destruction trace** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

The course capstone is **Memory Workspace**, an in-memory document workspace with handles, snapshots, edit sessions, and caches. Add staged edit sessions whose owned candidate state can be committed or abandoned. A failed commit must preserve the documented state without relying on fallible destructors. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-04-resource-pool/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 15 when you can:

- answer the module question—“Which value owns each cleanup obligation, when does destruction run, and what state remains after early return, error, or panic?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Derive local, field, tuple, temporary, and scope destruction order from documented rules;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [Rust Reference: Destructors](https://doc.rust-lang.org/reference/destructors.html)
- [std::mem](https://doc.rust-lang.org/std/mem/)
- [std::panic](https://doc.rust-lang.org/std/panic/)

[← Module 13](../../../02-rust-ownership-lifetimes-memory/course-book/module-13-scoped-access-and-escape-prevention/index.md) · [one-hundred-module map](../../../COURSE_MAP.md) · [Module 15 →](../../../02-rust-ownership-lifetimes-memory/course-book/module-15-box-deref-dynamically-sized-types-and-cow/index.md)

## Continue

Continue to [Module 15 — Box, Deref, Dynamically Sized Types, and Cow](../module-15-box-deref-dynamically-sized-types-and-cow/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
