# Workbook — Module 32: The Iterator Model

[Chapter](index.md) · [Laboratory](../../labs/module-02-lazy-log-query/README.md) · [LedgerFlow guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **The Iterator Model** has become a usable model rather than remembered vocabulary. Its governing question is: *What state does an iterator own, when does work happen, and what is consumed by each call to next?* Preserve your first prediction and record decisive facts in a **iterator state trace**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 31 — Closures, Capture, and Callable Contracts that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **What state does an iterator own, when does work happen, and what is consumed by each call to next?**
3. Draw the smallest **iterator state trace** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **The Iterator Model** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`case-01.rs`](../../compiler-labs/module-02/case-01.rs) | Pass or fail? What exact rule decides? |
| 2 | [`case-02.rs`](../../compiler-labs/module-02/case-02.rs) | Pass or fail? What exact rule decides? |
| 3 | [`case-03.rs`](../../compiler-labs/module-02/case-03.rs) | Pass or fail? What exact rule decides? |
| 4 | [`case-04.rs`](../../compiler-labs/module-02/case-04.rs) | Pass or fail? What exact rule decides? |
| 5 | [`case-05.rs`](../../compiler-labs/module-02/case-05.rs) | Pass or fail? What exact rule decides? |
| 6 | [`case-06.rs`](../../compiler-labs/module-02/case-06.rs) | Pass or fail? What exact rule decides? |
| 7 | [`case-07.rs`](../../compiler-labs/module-02/case-07.rs) | Pass or fail? What exact rule decides? |
| 8 | [`case-08.rs`](../../compiler-labs/module-02/case-08.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 04-rust-functional-programming
```

## Part 2 — Diagnose and repair

The broken function is intended to return titles up to—but not including—the first archived record:

```rust
fn active_titles(records: Vec<Record>) -> Vec<String> {
    records
        .into_iter()
        .take_while(|record| !record.archived)
        .map(|record| record.title)
        .collect()
}
```

A later phase needs the original catalog and also needs to inspect the first archived record. Both requirements are already impossible under this signature.

### Diagnose before repairing

`into_iter` transfers every `Record` into the iterator. Collecting titles then transfers each `String` out. The catalog is not “temporarily borrowed”; it has been consumed.

`take_while` must ask for the first nonmatching item to discover the boundary. That item is consumed from the underlying iterator even though it is not yielded. The adapter satisfies its contract; the product expectation was wrong.

### Contract-preserving repair

If the caller only needs a reusable query, accept `&[Record]` and return a borrowed lazy view:

```rust
fn active_titles(records: &[Record]) -> impl Iterator<Item = &str> + '_ {
    records
        .iter()
        .take_while(|record| !record.archived)
        .map(|record| record.title.as_str())
}
```

This preserves the catalog, but it still consumes the boundary item from the iterator's perspective. When later code must inspect that record through the same cursor, use `peekable` or write an explicit loop whose stopping protocol matches the requirement.

### Behavior tests
Instrument the predicate and prove no work occurs before the consumer asks. Then prove exact call count, yielded titles, catalog survival, and boundary behavior. Include empty input and a boundary at the first item.

### Weak repairs to reject

- cloning the vector before `into_iter`;
- returning `Vec<&str>` and calling it lazy;
- using indexing to avoid understanding iterator state;
- assuming `take_while` “puts back” the first nonmatch.

The lesson is not that `take_while` is dangerous. It is that a consumer's stopping semantics are part of the API contract.

## Part 3 — Focused exercises

### Exercise 1 — Trace the state machine

Given `let mut it = vec![10, 20, 30].into_iter();`, draw the iterator state before and after four calls to `next`. Record the return value and who owns each element after each call.

### Exercise 2 — Three traversal forms

For a `Vec<String>`, compare `iter`, `iter_mut`, and `into_iter` in a table containing source access, item type, allowed item operation, and source usability after traversal.

### Exercise 3 — Prove laziness

Construct a mapped iterator whose closure increments a counter. What should the counter be after adapter construction, after one `next`, and after `collect` consumes the remainder? Explain what this test does and does not prove.

### Exercise 4 — Partial parser with `by_ref`

A token stream contains a header terminated by `--` followed by records. Consume the header through a borrowed iterator and then resume the same iterator for records. State where the delimiter goes.

### Exercise 5 — Truthful iterator contracts

A custom iterator can calculate that at least two items remain but cannot determine whether filtering will remove some of them. What `size_hint` can it report? Can it implement `ExactSizeIterator`?

### Exercise 6 — Loop or chain

Rewrite one iterator chain as a `for` loop and give criteria for selecting the clearer version. The operation must parse rows, skip comments, stop at a sentinel, and accumulate diagnostics.

### Interleaved reasoning pass

1. For **Explain the distinct roles of `IntoIterator`, `Iterator`, adapters, and consumers**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the iterator state trace.
2. For **Trace the state changes caused by repeated calls to `next`**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the iterator state trace.
3. For **Predict whether an iteration path borrows, mutably borrows, or consumes its source**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the iterator state trace.
4. For **Use `by_ref`, `peekable`, and fused boundaries without losing track of consumed items**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the iterator state trace.

5. Identify one guarantee from an earlier course that a careless implementation of **The Iterator Model** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

The executable contract is in `labs/module-02-lazy-log-query/README.md`. This laboratory is about pull behavior, not just filtering syntax.

### Product problem

An in-memory log needs borrowed read-only queries and two different prefix operations. One prefix operation may consume the boundary item while discovering that it should stop. The other must preserve that boundary for the caller. Those are different contracts and must not share a misleading name.

### Pull trace before code

For the source below, write the exact sequence of `next` and predicate calls for each consumer:

```text
Debug("boot"), Info("ready"), Error("disk"), Error("network")
```

Trace:

- constructing the query and never consuming it;
- `.take(1).collect()` with minimum `Warn` and term `"disk"`;
- `.count()` with minimum `Info` and term `"e"`;
- a `take_while` prefix through marker `STOP`;
- the preserving `Peekable` variant through the same marker.

A result list without the pull trace is incomplete evidence.

### Implementation obligations

#### Borrowed query

Return `impl Iterator<Item = &LogEntry> + '_`. The query must borrow the source, retain source order, and allocate no result collection by itself. Add a test that uses the source again after the query has been consumed.

#### Consuming prefix

Accept `&mut I` where `I: Iterator<Item = &str>`. Document that `take_while` consumes the first rejected item. Prove the contract with `['a', 'STOP', 'b']`: the result is `['a']`, and the remaining iterator begins at `'b'`.

#### Preserving prefix

Accept `&mut Peekable<I>`. Inspect the next item before deciding whether to consume it. The same source must leave `STOP` available as the next item.

#### Laziness proof

Instrument the query predicate with `Cell<usize>`. Assert zero calls after construction, the exact number after `.take(1)`, and no inspection of later entries once the consumer has enough output.

### Failure modes to expose

Reject implementations that:

- accept `Vec<LogEntry>` and consume the catalog;
- return `Vec<&LogEntry>` by default and call that “lazy”;
- allocate lowercase copies of every message before a case-sensitive query;
- use `take_while` while promising boundary preservation;
- hide delimiter consumption in documentation rather than a test;
- claim zero work without measuring predicate calls.

### Laboratory transfer

Design a lazy query over timestamped sensor readings that can consume a prefix and resume from the remainder. Produce:

Add `first_n_matching`, still as a lazy borrowed view. Use a predicate ledger to prove that matching stops after `n` retained entries, not after `n` source entries. Define `n = 0` explicitly and test it.

### Defense

Explain where iterator state lives, why `next` needs `&mut self`, how `by_ref` changes ownership of the iterator value, and why “adapter construction is lazy” does not mean “the eventual query is free.”

The executable starter and reference implementation are in [module-02-lazy-log-query](../../labs/module-02-lazy-log-query/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

### Laboratory acceptance trace

Before opening the reference implementation for **Lazy Log Query**, record:

- the public behavior that demonstrates **Explain the distinct roles of `IntoIterator`, `Iterator`, adapters, and consumers**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Day 2 gives LedgerFlow an explicit iteration surface. The purpose is not to produce a long chain. It is to make four questions answerable for every stream: **who owns the source, what state advances, when work happens, and what remains after partial consumption?**

### Product slice

LedgerFlow stores an accepted batch of events. Callers need two different views:

- a borrowed view for repeated analysis without destroying the batch;
- an owning view for a terminal operation that transfers every event out.

Implement both. Their names and return item types must expose the difference.

```rust
impl AcceptedBatch {
    pub fn events(&self) -> impl Iterator<Item = &Event> + '_ { /* ... */ }

    pub fn into_events(self) -> impl Iterator<Item = Event> { /* ... */ }
}
```

Do not return a collected vector from `events`. The batch already owns storage; another allocation would erase the value of the view.

### Draw the pull trace

For one query, draw a trace with these columns:

| Consumer request | Adapter receiving request | Source item requested | Predicate/map call | Item yielded | Source position after call |
|---:|---|---|---|---|---:|

Trace at least five calls, including the first `None`. Continue with one additional call after exhaustion and record whether the contract remains exhausted.

### Prove laziness, not merely state it

Use a local counter or a test probe captured by a closure. Construct an adapter chain and assert that the counter remains zero. Consume one item and assert the exact number of source and transformation calls. Then consume the remainder. The test must distinguish adapter construction from execution.

Avoid production instrumentation whose only purpose is the test. The probe belongs at the test boundary.

### Partial-consumption exercise

Use `by_ref` to let one consumer take a prefix while retaining access to the same iterator for a second phase. Record the items consumed by each phase. The exercise must demonstrate that `by_ref` borrows the iterator; it does not duplicate iterator state.

Add a look-ahead case only when the parser genuinely needs to inspect a boundary item without treating it as accepted. Decide whether `peekable` is sufficient. Do not use `take_while` if consuming the first nonmatching item would violate the product rule.

### Ownership trace
Add compile-prediction notes for all three loops:

```rust
for event in batch.events() { /* borrowed */ }
for event in &stored_events { /* borrowed */ }
for event in batch.into_events() { /* owning */ }
```

For each, state the loop item type, the owner that remains afterward, and whether the source can be traversed again.

### Required tests

- borrowed iteration preserves insertion order;
- two borrowed traversals can occur sequentially;
- owning iteration yields owned `Event` values;
- transformation work is zero before consumption;
- partial consumption leaves the documented suffix;
- the iterator remains exhausted after returning `None` if the concrete iterator promises fused behavior;
- empty and one-item batches behave without special-case panics.

### Capstone invariant trace

For the Module 32 LedgerFlow increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Do not advance because the calendar day ended. Advance when all hard evidence is present.

### Advancement decision

Advance only when you can draw an iterator’s state before and after each `next`, distinguish borrowed and consuming traversal, and prove laziness with an observable counter.

### Closed-book retrieval

1. What state is changed by every call to `next`?
2. Why does an iterator binding often need `mut` even when yielded items are shared references?
3. What does `into_iter()` on an owned `Vec<T>` transfer?
4. How does `by_ref()` preserve the ability to resume an iterator?
5. What exactly does `peek()` borrow, and when does the item become consumed?
6. Why is an iterator adapter lazy but its source construction not necessarily free?
7. What may a truthful `size_hint` claim?
8. When is `ExactSizeIterator` valid?
9. What does `FusedIterator` promise after the first `None`?
10. Why can two `iter_mut()` values over one collection not coexist?

### Reconstruction task

Implement a small iterator over every second element of a borrowed slice, including lawful exhaustion and a truthful `size_hint`. Then show the consuming alternative for an owned vector.

### Transfer task

Transfer **Module 32: The Iterator Model** to a product unrelated to the course capstone. Change the domain model and failure mode, preserve the governing relationship, and identify which part of the original design was essential rather than accidental.

- source ownership and iterator-state diagram;
- item type produced by each `next` call;
- exhaustion and post-exhaustion behavior;
- test proving that constructing adapters alone performs no work;

### Spaced review

Repeat questions 2, 4, 7, and 10 after 24 hours. Repeat the reconstruction after seven days with a different domain.

### Closed-book defense

In five minutes, answer “What state does an iterator own, when does work happen, and what is consumed by each call to next?” using the **iterator state trace**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside LedgerFlow. A list of APIs without the deciding relationship is incomplete.
