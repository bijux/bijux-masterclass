# Workbook — Module 36: Custom Iterators and Collection Protocols

[Chapter](index.md) · [Laboratory](../../labs/module-06-custom-cursors/README.md) · [LedgerFlow guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Custom Iterators and Collection Protocols** has become a usable model rather than remembered vocabulary. Its governing question is: *What laws must a custom traversal obey, and who owns the collection when iteration begins?* Preserve your first prediction and record decisive facts in a **collection protocol map**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 35 — Option, Result, and Fallible Traversal that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **What laws must a custom traversal obey, and who owns the collection when iteration begins?**
3. Draw the smallest **collection protocol map** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Custom Iterators and Collection Protocols** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`case-01.rs`](../../compiler-labs/module-06/case-01.rs) | Pass or fail? What exact rule decides? |
| 2 | [`case-02.rs`](../../compiler-labs/module-06/case-02.rs) | Pass or fail? What exact rule decides? |
| 3 | [`case-03.rs`](../../compiler-labs/module-06/case-03.rs) | Pass or fail? What exact rule decides? |
| 4 | [`case-04.rs`](../../compiler-labs/module-06/case-04.rs) | Pass or fail? What exact rule decides? |
| 5 | [`case-05.rs`](../../compiler-labs/module-06/case-05.rs) | Pass or fail? What exact rule decides? |
| 6 | [`case-06.rs`](../../compiler-labs/module-06/case-06.rs) | Pass or fail? What exact rule decides? |
| 7 | [`case-07.rs`](../../compiler-labs/module-06/case-07.rs) | Pass or fail? What exact rule decides? |
| 8 | [`case-08.rs`](../../compiler-labs/module-06/case-08.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 04-rust-functional-programming
```

## Part 2 — Diagnose and repair

A custom segment iterator skips empty segments but reports:

```rust
fn size_hint(&self) -> (usize, Option<usize>) {
    let remaining_raw = self.parts.len() - self.index;
    (remaining_raw, Some(remaining_raw))
}
```

It also implements `ExactSizeIterator`, accidentally yields the final segment again after returning `None`, and exposes mutable iteration over keys whose sorted order is an invariant.

### Diagnose each contract separately

Because empty segments are skipped, the number of yielded items can be **less** than remaining raw parts. `remaining_raw` is a valid upper bound, not a valid lower bound. `ExactSizeIterator` is therefore false unless the iterator precomputes or otherwise knows the exact remaining yield count.

Returning a value after `None` violates fused behavior. The base `Iterator` trait does not require fusion, but the implementation and tests must not accidentally claim it. Exposing `&mut Key` lets callers invalidate sorting and any derived index.

### Repair the state machine

1. Write the states: searching, yielding, exhausted.
2. Make exhausted state permanent.
3. Use `(0, Some(remaining_raw))` or a tighter proved lower bound.
4. Remove `ExactSizeIterator` unless exactness is derived.
5. Implement `FusedIterator` only after permanent exhaustion is tested.
6. Expose mutable access only to fields whose mutation cannot violate collection invariants.

### Law-driven tests

Exhaustively generate short segment lists including empty, leading-empty, trailing-empty, and all-empty cases. After every `next`, assert that actual remaining yields remain inside `size_hint`. Call `next` multiple times after `None`. Construct two iterators and prove cursor independence.

### Collection protocol review

If invalid configuration can make construction fail, do not implement an infallible `FromIterator` that must panic or discard errors. Provide `try_from_iter` or a constructor returning `Result`.

The lesson is that stronger iterator traits are public promises. Implementing them for prestige is a correctness defect.

## Part 3 — Focused exercises

### Exercise 1 — Design `next` from state

Design an inclusive integer range iterator with checked increment. List its fields, exhaustion state, and behavior at `i64::MAX` before implementing `next`.

### Exercise 2 — Choose receiver implementations

A `Bag<T>` stores a private vector. Specify item types and semantics for `IntoIterator` on `Bag<T>`, `&Bag<T>`, and `&mut Bag<T>`. Then give one reason to omit the mutable implementation.

### Exercise 3 — Fallible invariants and `FromIterator`

A `UniqueNames` collection must reject duplicates with the duplicate’s source position. Should it implement `FromIterator<String>`?

### Exercise 4 — Extend and partial mutation

Explain why implementing `Extend<Record>` for a collection whose insertion can fail may create partial mutation. Propose an atomic alternative.

### Exercise 5 — Validate `size_hint`

For a custom adapter that yields every third upstream item, derive a truthful lower and upper bound from upstream `(lower, upper)`.

### Exercise 6 — Custom adapter law review

Implement or review an adapter that stops after the first predicate failure. State whether it may be fused and whether the failing item is consumed.

### Interleaved reasoning pass

1. For **Implement a correct custom `Iterator` by defining state and exhaustion behavior**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the collection protocol map.
2. For **Provide owned, shared, and mutable `IntoIterator` implementations only where their semantics are useful**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the collection protocol map.
3. For **Implement `FromIterator` and `Extend` for a domain collection with explicit invariant policy**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the collection protocol map.
4. For **Implement stronger iterator traits only when every required law holds**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the collection protocol map.

5. Identify one guarantee from an earlier course that a careless implementation of **Custom Iterators and Collection Protocols** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

The executable work is in `labs/module-06-custom-cursors/README.md`. This is a law laboratory: each implemented trait makes a promise stronger than “the examples passed.”

### Part A — `Fields<'a>` state machine

Represent only the unprocessed suffix. On each `next` call, consume one raw comma-delimited segment, trim it, skip empties, and either yield a borrowed slice or continue. Draw states for:

- untouched input;
- remaining suffix;
- trailing comma;
- all-empty input;
- permanent exhaustion.

The lower size hint is zero because remaining raw segments may all be empty. The upper bound may be remaining comma count plus one. Do not implement `ExactSizeIterator`.

### Part B — `EventLog` traversal ownership

Provide two deliberate `IntoIterator` implementations:

- owned `EventLog` yields owned `Event` values;
- `&EventLog` yields `&Event` values.

Do not expose mutable iteration because the future log invariant may require event order and identity to remain controlled. Show with tests that borrowed traversal leaves the log available and consuming traversal transfers its storage.

### Part C — collection protocols

`Diagnostics` supports both `FromIterator<String>` and `Extend<String>`. Explain why one creates a collection from a complete stream while the other grows existing state.

`UniqueIds` cannot lawfully implement ordinary `FromIterator<u64>` if duplicate rejection must be reported. Expose `try_from_iter` instead. Returning a partial collection on duplicate is not the contract.

### Part D — `Stride<I>`

Reject step zero at construction. The first `next` yields the source’s first item; later calls skip `step - 1` items and yield the next. Derive the size hint separately before and after the first call. Test exact iterators and an iterator with only an upper bound.

### Step-iterator law matrix

Your evidence must cover:

| Law | Proof case |
|---|---|
| fused exhaustion | at least two `next` calls after `None` |
| order preservation | source order under all traversal modes |
| conservative size hint | actual remaining count always inside bounds |
| owned/borrowed distinction | source availability after traversal |
| duplicate failure | first duplicate and no panic |
| extension order | existing diagnostics followed by new items |

### Transfer

Build a separate front/back cursor over a slice and implement `DoubleEndedIterator`. Test mixed `next`/`next_back` sequences, odd and even lengths, crossing in the middle, and permanent exhaustion. Do not add `ExactSizeIterator` until the remaining count is actually exact.

### Defense

Every marker trait must be defended as a semantic promise. Explain why a truthful weak hint is better than a precise-looking lie, why mutable iteration is an API decision rather than a convenience, and why fallible collection needs a different constructor shape.

The executable starter and reference implementation are in [module-06-custom-cursors](../../labs/module-06-custom-cursors/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

### Laboratory acceptance trace

Before opening the reference implementation for **Custom Cursors**, record:

- the public behavior that demonstrates **Implement a correct custom `Iterator` by defining state and exhaustion behavior**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Day 6 replaces ad hoc traversal with domain-specific iterator types only where those types clarify a stable public operation. The objective is not to implement every iterator trait. It is to implement the **smallest truthful protocol** and prove its laws.

### Choose one domain iterator

Create a concrete iterator for one useful LedgerFlow view, such as:

- audit entries from newest to oldest;
- account events filtered by a borrowed account key;
- physical source rows with preserved positions;
- accepted events plus their stable acceptance index.

Write the item type, iterator-owned state, borrowed source, and exhaustion rule before coding.

### Implement `next` from a state machine

Describe the states in plain language. Then implement `Iterator::next` so each call either advances state or reaches permanent exhaustion. Do not perform hidden restart, allocate a new collection per call, or yield a value twice after `None`.

If the iterator skips internal elements, its `size_hint` lower bound must remain conservative. Claim an exact upper bound only when it is derivable. Implement `ExactSizeIterator`, `DoubleEndedIterator`, or `FusedIterator` only after separately proving the corresponding contract.

### Collection-protocol law matrix

Test the iterator against this matrix:

| Law | Evidence |
|---|---|
| Sequence | Collected output equals the specified domain order |
| Progress | Every successful `next` advances state |
| Exhaustion | After `None`, later calls obey the documented contract |
| Size hint | Actual remaining length stays within lower/upper bounds |
| Ownership | Item borrowing/ownership matches the public signature |
| Independence | Two iterators have independent cursors unless documented otherwise |

Generate exhaustive small cases where practical: empty, one element, all skipped, alternating skipped, and all yielded.

### Collection protocols

Add `FromIterator` only if collecting arbitrary valid items into the domain type has a coherent invariant-preserving meaning. If construction can fail, use a fallible constructor rather than an impossible infallible `FromIterator` implementation.

Add `Extend` only if incremental addition has a clear duplicate and failure policy. Do not expose mutable iteration over fields whose mutation could violate ordering, identity, or index consistency.

### Compare wrapper versus custom type

Implement the same view once with a standard adapter chain. Decide whether the custom iterator earns its existence through one of these benefits:

- a stable named public type;
- more precise state or size semantics;
- encapsulation of domain traversal rules;
- support for multiple related trait implementations;
- substantially clearer debugging.

If none applies, retain the adapter chain and document the rejected custom type.

### Capstone invariant trace

For the Module 36 LedgerFlow increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Do not advance because the calendar day ended. Advance when all hard evidence is present.

### Advancement decision

Advance only when your iterator remains lawful after exhaustion, its size claim is truthful in every internal phase, and collection traits preserve domain invariants.

### Closed-book retrieval

1. What state is minimally required by a custom iterator?
2. Why must `next` remain valid after exhaustion?
3. What does implementing `IntoIterator for &T` communicate?
4. When can `FromIterator` not honestly enforce a fallible invariant?
5. Why is `Extend` a poor fit for an operation that must reject items?
6. What lower and upper bounds may `size_hint` return?
7. What extra law does `DoubleEndedIterator` require?
8. When may an iterator implement `ExactSizeIterator`?
9. How can a custom adapter retain a closure and upstream iterator?
10. Why is exposing `slice::Iter` directly sometimes an API commitment?

### Reconstruction task

Implement a window iterator from memory, exercise partial consumption, repeated `None`, and lower/upper bounds, then justify whether it deserves a named public type.

### Transfer task

Create a calendar-range iterator that skips excluded dates without exposing mutable access that could invalidate ordering. Produce:

- iterator state machine and remaining-item invariant;
- `Item` type and ownership for borrowed, mutable, and consuming traversal;
- lawful exhaustion and size-hint statement;
- test covering empty, partial, complete, and repeated-after-exhaustion traversal;

### Spaced review

Repeat questions 2, 4, 7, and 10 after 24 hours. Repeat the reconstruction after seven days with a different domain.

### Closed-book defense

In five minutes, answer “What laws must a custom traversal obey, and who owns the collection when iteration begins?” using the **collection protocol map**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside LedgerFlow. A list of APIs without the deciding relationship is incomplete.
