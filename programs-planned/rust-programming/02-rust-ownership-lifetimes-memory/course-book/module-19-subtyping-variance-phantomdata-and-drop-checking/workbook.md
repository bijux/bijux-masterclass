# Workbook — Module 19: Subtyping, Variance, PhantomData, and Drop Checking

[Return to the chapter](index.md) · [Open the Memory Workspace engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether you can use **Subtyping, Variance, PhantomData, and Drop Checking** without relying on surface syntax. Keep the module question in view: *When may a longer-lived capability substitute for a shorter requirement, and what semantic relationships must marker types communicate?* For every task, identify the program point where the decisive type, ownership, dispatch, failure, or cost relationship is established. Compile only after committing to a prediction, and preserve the smallest counterexample that changes your model.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Subtyping, Variance, PhantomData, and Drop Checking** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-lifetime-shortening.rs`](../../compiler-labs/module-09/01-lifetime-shortening.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-mut-reference-invariance.rs`](../../compiler-labs/module-09/02-mut-reference-invariance.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-cell-invariance.rs`](../../compiler-labs/module-09/03-cell-invariance.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-function-argument-contravariance.rs`](../../compiler-labs/module-09/04-function-argument-contravariance.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-owned-t-outlives.rs`](../../compiler-labs/module-09/05-owned-t-outlives.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-destructor-keeps-borrow-live.rs`](../../compiler-labs/module-09/06-destructor-keeps-borrow-live.rs) | Pass or fail? What exact rule decides? |
| 7 | [`07-invariant-marker-size.rs`](../../compiler-labs/module-09/07-invariant-marker-size.rs) | Pass or fail? What exact rule decides? |
| 8 | [`08-cross-brand-id.rs`](../../compiler-labs/module-09/08-cross-brand-id.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 02-rust-ownership-lifetimes-memory
```

## Part 2 — Diagnose and repair


A library creates a handle type with `PhantomData<&'a T>` but uses it to grant mutable access to `T`. Because the marker is covariant, the handle lifetime/type can be shortened/substituted more freely than exclusive mutation permits. The author then adds transmute in an unsafe implementation to force conversions.

### Safe-course repair

Do not implement raw-handle dereference. Redesign the exercise as a branded index accepted only by an arena method that owns the actual `Vec<T>`. The arena performs bounds checking and returns ordinary borrows. The marker separates brands; it does not pretend to own or directly point to `T`.

### Required analysis

- variance trace of the wrong marker;
- authority promised by each method;
- drop-check implications;
- why lifetime invariance does not replace generation/bounds validation;
- why the capstone's runtime generational handle is preferable for escaping IDs.

## Part 3 — Focused exercises

### Access protocol

Attempt every required exercise and commit the attempt before opening `exercise-answers.md`. Mark each as:


1. Draw lifetime subtype relations for three nested scopes and apply shortening.
2. Derive covariance of `&T` and invariance of `&mut T` with a write counterexample.
3. Trace variance through `&Cell<&'a str>` and `&mut Vec<&'a str>`.
4. Demonstrate function argument contravariance with a function accepting any `&str`.
5. Explain `String: 'a` versus `&'short str: 'a`.
6. Add a destructor to a borrowed wrapper and locate the new effective final use.
7. Compare `PhantomData<T>`, `PhantomData<&'a T>`, `PhantomData<&'a mut T>`, and invariant function markers.
8. Implement `with_brand`, a branded arena, and compile-fail cross-brand access.
9. Add removal to the arena on paper and explain why branding alone does not reject stale same-brand IDs.
10. Review capstone handles and explain why they should not carry lifetime brands.



## Part 4 — Independent laboratory



Build a scoped arena whose IDs cannot be mixed across arena instances created by separate brand scopes.

```text
labs/module-09-variance-branding/
├── starter/
└── solution/
```

### Required API shape

```rust
pub fn with_arena<R>(operation: impl for<'id> FnOnce(Arena<'id>) -> R) -> R;

pub struct Arena<'id, T> { /* private */ }
pub struct Id<'id> { /* private, Copy */ }
```

The exact constructor arrangement may differ, but:

- the brand is invariant;
- IDs do not escape `with_arena` as part of `R`;
- IDs from separate scopes cannot mix;
- lookup is bounds-checked;
- the lab does not remove/reuse slots;
- no raw pointers or unsafe code are used;
- rustdoc `compile_fail` examples prove cross-brand rejection and escape prevention.

### Variance report

Submit a written trace for every marker field and explain why a covariant brand would weaken separation.

### Acceptance

```bash
cargo test -p rust-olm-lab-09-variance-branding --all-targets
cargo clippy -p rust-olm-lab-09-variance-branding --all-targets -- -D warnings
```

### Why the brand must be invariant

The lifetime parameter is not borrowed storage; it is an unforgeable scope identity generated by the callback. A covariant marker would permit shortening the brand lifetime and could make values from distinct logical capabilities appear substitutable in broader APIs. Encode invariance deliberately, for example through a marker whose type position is invariant in `'id`, and document the derivation rather than copying a `PhantomData` spelling without understanding it.

The callback must be higher-ranked: the caller chooses no concrete brand and must provide code valid for whichever fresh lifetime the function introduces. Consequently, `R` cannot contain `Id<'id>` or `Arena<'id, T>` tied to that hidden brand. A rustdoc `compile_fail` example should try to return an ID and should fail for the intended provenance reason.

### Arena behavior

Keep storage ordinary and safe, such as `Vec<T>`. `insert` returns a branded slot index. `get` and `get_mut` require an ID with the same brand and perform bounds checking. Since the lab does not reuse slots, the brand proves arena provenance while bounds checking proves current index validity. Do not overclaim that the design solves deletion or generational reuse.

Write positive tests for insertion, immutable lookup, mutable lookup, and multiple values. Add compile-fail evidence for cross-scope mixing, escape, and construction of an ID outside the private constructor. The exact compiler wording is not the contract; the rejected program is.

### Variance and drop report

For every marker field, derive variance by following the constructor positions rather than consulting a memorized table alone. State whether the type semantically owns, borrows, or merely brands `T` and `'id`, and explain how that affects auto traits and drop checking. If the implementation stores `Vec<T>`, ordinary ownership already communicates ownership of `T`; the brand marker should communicate only the additional invariant identity.

The final defense must distinguish three properties: a fresh brand prevents mixing across scopes; the vector bounds check prevents invalid numeric slots; and the callback prevents brand escape. None alone proves all three.

### Tiered hints

Do not open a later tier until the previous tier has produced a written attempt.

- **Hint 1 — concept:** return to the governing question: When may a longer-lived capability substitute for a shorter requirement, and what semantic relationships must marker types communicate?
- **Hint 2 — topology:** draw owners/borrows/states/errors before changing syntax; identify the one boundary that should own the invariant.
- **Hint 3 — structure:** separate validation from mutation and pure transformation from effects. Use the standard operation that encodes the safety fact before inventing an abstraction.
- **Hint 4 — implementation-adjacent:** consult only the relevant standard-library or Reference page; do not open `solution/src`.

The executable starter and reference implementation are in [module-09-variance-branding](../../labs/module-09-variance-branding/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

## Part 5 — Capstone transfer

### Outcomes mapped

- State lifetime subtype direction through substitutability and derive covariance, contravariance, and invariance operationally.
- Compose variance through shared references, mutable references, cells, function arguments/results, and generic wrappers.
- Read outlives bounds and destructor use without claiming owned values are borrowed for the bound lifetime.
- Choose PhantomData shapes from ownership, borrowing, variance, auto-trait, and drop-check semantics, while treating current drop-check details as version-sensitive.
- Use higher-ranked generative brands to prevent cross-scope identity mixing and explain why generations remain necessary for slot reuse.


Audit `DocumentHandle`, snapshot identities, views, and edit sessions.

### Runtime handles

`DocumentHandle { slot, generation }` contains no borrow and needs no `PhantomData` lifetime. It is validated at every workspace boundary. It can be copied, serialized in a future explicit format, and retained independently.

### Reference-bearing views

`DocumentView<'a>` has real reference fields; those fields already establish covariance/outlives relationships. Do not add ceremonial markers.

### Session markers

If edit sessions use type states such as `EditSession<Open>` and `EditSession<Validated>`, zero-sized marker types can restrict methods. The marker communicates state, not ownership of a domain value. Document its variance, though state types normally contain no lifetimes.

### Proof

Add compile-fail diagnostics for:

- returning a view after workspace drop;
- mixing a branded lab ID with a runtime capstone handle (different types);
- using an open session where a validated session is required;
- attempting to reinterpret generation through lifetime annotations.

The capstone should use marker complexity only where it removes a real invalid transition.



### Capstone defense

Derive the variance of an unfamiliar wrapper, choose a marker deliberately, and compare compile-time brands with runtime generational handles.

## Part 6 — Reconstruct and defend

Complete this checkpoint closed-book. Compiler access is allowed only after the prediction portion has been committed.

### Outcome reconstruction

For each outcome, write a claim, one example, one non-example, and one limitation.

- State lifetime subtype direction through substitutability and derive covariance, contravariance, and invariance operationally.
- Compose variance through shared references, mutable references, cells, function arguments/results, and generic wrappers.
- Read outlives bounds and destructor use without claiming owned values are borrowed for the bound lifetime.
- Choose PhantomData shapes from ownership, borrowing, variance, auto-trait, and drop-check semantics, while treating current drop-check details as version-sensitive.
- Use higher-ranked generative brands to prevent cross-scope identity mixing and explain why generations remain necessary for slot reuse.

### Closed-book checkpoint

1. State lifetime subtype direction through substitutability.
2. Define covariance, contravariance, and invariance.
3. Prove `&mut T` invariance in `T` with a write example.
4. Trace a lifetime through nested reference/cell/function constructors.
5. Read `T: 'a` without claiming owned values live for `'a`.
6. Identify destruction as a hidden final use.
7. Select and defend a `PhantomData` shape.
8. Build an invariant generative brand with HRTB.
9. Explain why branding does not solve stale index reuse.
10. Defend capstone runtime handles over lifetime-branded handles.

### Transfer defense

Derive the variance of an unfamiliar wrapper, choose a marker deliberately, and compare compile-time brands with runtime generational handles.

Your answer must include:

Complete Parts A–C before compiling any specimen. Variance is assessed by derivation from permitted operations, not by reproducing a memorized table.

#### Part A — Closed-book retrieval

1. What does `'long: 'short` state?
2. Why may `&'long T` be used where `&'short T` is required?
3. Define covariance as a substitution property.
4. Define contravariance as a substitution property.
5. Define invariance as a substitution property.
6. Why is a shared reference covariant in its referent type?
7. Why is `&'a mut T` invariant in `T`?
8. Why is `&'long mut T` still reborrowable for a shorter lifetime?
9. What operation makes `Cell<T>` and `RefCell<T>` invariant in `T`?
10. Why are function argument positions contravariant?
11. Why are function return positions covariant?
12. How do variances compose through nested constructors?
13. Why does one invariant constructor make the whole path invariant?
14. What does `T: 'a` mean?
15. Why can adding `T: 'a` overconstrain an API when ownership already makes the value independent?
16. What does `PhantomData<T>` communicate broadly?
17. How does `PhantomData<&'a T>` differ from `PhantomData<T>`?
18. Why does marker choice affect more than unused-parameter diagnostics?
19. What is drop checking protecting?
20. Why does drop checking not guarantee that a destructor runs?
21. How can a phantom field influence auto traits?
22. What makes a lifetime brand fresh?
23. Why must a generative brand usually be invariant?
24. Why is `PhantomData<&'id T>` often too weak for brand identity?
25. What does `for<'id> FnOnce(...) -> R` prevent `R` from doing?
26. What problem does a brand solve that an integer index does not?
27. What problem does a brand fail to solve after deletion and slot reuse?
28. When are runtime generations preferable to brands?
29. What does `PhantomPinned` change?
30. Why does `PhantomPinned` not pin an ordinary local value by itself?

#### Part B — Capability derivations

For every type, derive variance in the named parameter. Do not answer with one word only. State the operation that permits or blocks substitution.

1. `&'a T` in `'a`.
2. `&'a T` in `T`.
3. `&'a mut T` in `'a`.
4. `&'a mut T` in `T`.
5. `Box<T>` in `T`.
6. `Vec<T>` in `T`.
7. `Cell<T>` in `T`.
8. `RefCell<T>` in `T`.
9. `Option<&'a str>` in `'a`.
10. `Cell<Option<&'a str>>` in `'a`.
11. `fn(T)` in `T`.
12. `fn() -> T` in `T`.
13. `fn(T) -> T` in `T`.
14. `PhantomData<&'a T>` in `'a` and `T`.
15. `PhantomData<fn(&'a ()) -> &'a ()>` in `'a`.

Use the substitution test:

```text
Known relation:
Actual type:
Expected type:
Constructor path:
Operation that would become unsafe if substitution were allowed:
Conclusion:
```

For `Cell<Option<&'a str>>`, the critical operation is replacement. If a long-lived cell could be treated as a short-lived cell, code could store a short reference and the original owner could later read it under the long lifetime.

#### Part C — Predict the compiler

##### Specimen 1 — shortening a shared borrow

```rust
fn shorten<'long, 'short>(value: &'long str) -> &'short str
where
    'long: 'short,
{
    value
}
```

Predict why this is valid and what the function does *not* do.

##### Specimen 2 — mutable referent substitution

```rust,compile_fail
fn replace<'a>(slot: &'a mut &'static str, short: &'a str) {
    let widened: &'a mut &'a str = slot;
    *widened = short;
}
```

Identify the hypothetical invalid state Rust prevents.

##### Specimen 3 — invariant cell

```rust,compile_fail
use std::cell::Cell;

fn shorten_cell<'long, 'short>(
    value: Cell<&'long str>,
) -> Cell<&'short str>
where
    'long: 'short,
{
    value
}
```

Explain why moving ownership of the cell does not make the stored-lifetime substitution safe.

##### Specimen 4 — higher-ranked brand escape

```rust,compile_fail
use std::marker::PhantomData;

#[derive(Clone, Copy)]
struct Brand<'id>(PhantomData<fn(&'id ()) -> &'id ()>);

fn with_brand<R>(f: impl for<'id> FnOnce(Brand<'id>) -> R) -> R {
    f(Brand(PhantomData))
}

let escaped = with_brand(|brand| brand);
```

Explain why the fixed return type `R` cannot depend on the callee-chosen lifetime.

##### Specimen 5 — owned summary escape

```rust
use std::marker::PhantomData;

struct Brand<'id>(PhantomData<fn(&'id ()) -> &'id ()>);

fn with_brand<R>(f: impl for<'id> FnOnce(Brand<'id>) -> R) -> R {
    f(Brand(PhantomData))
}

let count = with_brand(|_brand| 42_usize);
assert_eq!(count, 42);
```

Explain why an owned result independent of `'id` may escape.

#### Part D — Marker design review

For each proposed marker, complete this record:

```text
Runtime data absent:
Logical relationship claimed:
Variance required:
Values that must remain valid at drop:
Expected auto-trait influence:
Evidence:
```

##### Proposal 1 — borrowed index

```rust
struct ViewId<'a, T: ?Sized> {
    index: usize,
    marker: std::marker::PhantomData<&'a T>,
}
```

Decide whether the type truly borrows `T` for `'a` or merely names an arena entry. If it merely names an entry, a brand or runtime generation may be more accurate.

##### Proposal 2 — hidden owner

```rust
struct RawOwner<T> {
    address: usize,
    marker: std::marker::PhantomData<T>,
}
```

Course 2 does not implement this type. State the unsafe-course obligations: allocation provenance, destruction, ownership uniqueness, marker effects, and why `usize` is not a pointer-provenance proof.

##### Proposal 3 — invariant brand

```rust
struct Id<'id> {
    index: usize,
    marker: std::marker::PhantomData<fn(&'id ()) -> &'id ()>,
}
```

Explain why the function-shaped marker is invariant and why the ID still requires bounds checks.

##### Proposal 4 — pinned marker

```rust
struct Node {
    payload: String,
    marker: std::marker::PhantomPinned,
}
```

Explain what operations remain possible before pinning, what safe access changes after pinning, and why no self-reference exists merely because the marker is present.

#### Part E — Arena transfer task

Design a scoped parser arena with these properties:

- every invocation creates a fresh brand;
- node IDs from one invocation cannot be used in another;
- IDs cannot escape the scope as the direct return value;
- nodes are stored in `Vec<Node>`;
- no deletion occurs;
- lookup is bounds checked;
- an owned syntax summary may escape.

A suitable surface is:

```rust
pub struct Arena<'id> {
    nodes: Vec<Node>,
    brand: PhantomData<fn(&'id ()) -> &'id ()>,
}

pub struct NodeId<'id> {
    index: usize,
    brand: PhantomData<fn(&'id ()) -> &'id ()>,
}

pub fn with_arena<R>(operation: impl for<'id> FnOnce(&mut Arena<'id>) -> R) -> R;
```

Write:

- `insert`;
- `get`;
- one `compile_fail` example mixing nested arenas;
- one `compile_fail` example returning `NodeId<'id>`;
- one passing example returning an owned node count or owned summary.

Then extend the *design*, not necessarily the code, with deletion and slot reuse. Explain why the same-brand ID may become temporally stale. Add a generation to the runtime ID or forbid reuse. Branding proves arena identity; generation proves occupancy identity over time.

#### Part F — Durable-identity comparison

Complete this table:

| Property | Borrowed reference | Branded ID | Generational handle | `Rc<T>` |
|---|---|---|---|---|
| May escape local owner scope | limited by lifetime | normally no | yes | yes |
| Keeps value alive | through borrow exclusion | no | no | yes |
| Detects deletion | reference prevents conflicting deletion while alive | only if deletion forbidden or checked | generation lookup | value remains alive if directly owned |
| Storage may move | referent constraints apply during borrow | arena may move internally if IDs are indices | yes, lookup resolves location | allocation remains while strong-owned |
| Runtime lookup failure | usually before reference creation | bounds/index failure | stale/not-found | weak upgrade may fail, strong access does not |
| Best fit | immediate access | scoped non-mixing | durable mutable collections | shared immutable or shared-owner lifecycle |

Defend which identity form belongs in:

1. a one-pass scoped parser;
2. a long-lived workspace command language;
3. an immutable snapshot panel;
4. a removable arena with external IDs.

#### Part G — Answer criteria

A passing response must:

- distinguish lifetime covariance from referent invariance for `&mut`;
- derive nested variance rather than quote the outer constructor only;
- explain replacement capability as the reason for invariance;
- treat `PhantomData` as semantic, not decorative;
- distinguish drop validity from destructor liveness;
- explain HRTB freshness and fixed return type `R`;
- distinguish cross-arena non-mixing from stale-slot detection;
- reserve runtime generational handles for values that must escape and survive mutation;
- explain `PhantomPinned` without claiming it pins construction automatically.
