# Module 32 — The Iterator Model

**Course 4 · Day 2 · Module 32 of 100**
`████████░░░░░░░░░░░░░░░░░` **32/100**

[Program](../../../README.md) · [Course 4](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-02-lazy-log-query/README.md) · [LedgerFlow guide](../capstone.md)

[← Module 31: Closures, Capture, and Callable Contracts](../module-31-closures-capture-and-callable-contracts/index.md) · [Module 33: Iterator Algebra and Pipeline Shape →](../module-33-iterator-algebra-and-pipeline-shape/index.md)

## The question

> What state does an iterator own, when does work happen, and what is consumed by each call to next?

## Why this comes now

An iterator is not a collection and not a precomputed sequence. It is a stateful pull protocol whose work occurs on demand. This module isolates that protocol so later adapter chains can be traced in terms of source ownership, `next` calls, exhaustion, and side-effect timing.

### Prerequisite bridge

Module 31 established **Closures, Capture, and Callable Contracts**. Before continuing, verify that you can select among generic callables, `impl fn*`, and boxed callable trait objects from real storage and dispatch requirements. This module preserves that capability and adds the ability to explain the distinct roles of `intoiterator`, `iterator`, adapters, and consumers. Module 33, **Iterator Algebra and Pipeline Shape**, will rely on both when it asks: *How do adapters change item type, cardinality, order, ownership, and stopping behavior across a pipeline?*

### Scope boundary

This module owns the reasoning for **the iterator model** inside Course 4. The course uses ordinary functions, closures, iterators, and immutable public models. It does not treat mutation as forbidden, and it postpones macro construction, parallel iteration, async streams, and benchmark-driven optimization. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- Explain the distinct roles of `IntoIterator`, `Iterator`, adapters, and consumers.
- Trace the state changes caused by repeated calls to `next`.
- Predict whether an iteration path borrows, mutably borrows, or consumes its source.
- Use `by_ref`, `peekable`, and fused boundaries without losing track of consumed items.
- Treat `size_hint`, `ExactSizeIterator`, and `FusedIterator` as contracts rather than optimization decoration.

`IntoIterator` describes how a value can produce an iterator. `Iterator` describes a state machine that yields items one at a time.

```rust
fn print_all<C>(collection: C)
where
    C: IntoIterator,
    C::Item: std::fmt::Display,
{
    for item in collection {
        println!("{item}");
    }
}
```

The caller may pass a vector by value, a shared reference to a vector, a slice, an array, or another iterable type. Each expression has its own `IntoIterator` implementation and therefore its own item type.

```rust
let values = vec![10, 20, 30];

for value in &values {      // item: &i32
    println!("{value}");
}

for value in values {       // item: i32, vector consumed
    println!("{value}");
}
```

The `for` loop conceptually calls `IntoIterator::into_iter` and repeatedly calls `next`. The exact desugaring includes loop-control details, but this model is sufficient for ownership reasoning.

## Core model

### Why APIs often accept `IntoIterator`

An API that accepts `I: Iterator` requires the caller to construct an iterator first. Accepting `I: IntoIterator` is often more ergonomic when the function intends to consume one traversal and does not need to resume an existing iterator.

```rust
fn total<I>(values: I) -> i64
where
    I: IntoIterator<Item = i64>,
{
    values.into_iter().sum()
}
```

An API that needs to borrow and partially consume an existing iterator should accept `&mut I` where `I: Iterator`:

```rust
fn take_two<I>(iter: &mut I) -> Vec<I::Item>
where
    I: Iterator,
{
    iter.take(2).collect()
}
```

The caller can resume the iterator after the function returns.

### One type may have several iteration modes

A domain collection can implement:

- `IntoIterator for Collection` yielding owned items;
- `IntoIterator for &Collection` yielding shared references;
- `IntoIterator for &mut Collection` yielding mutable references.

These are independent contracts. Do not implement all three mechanically. For example, mutable iteration may let callers violate invariants if items cannot be safely modified in isolation.

### `iter()` is not the universal meaning of iteration

Methods named `iter` and `iter_mut` are conventional inherent methods. The language-level integration point for `for` and generic iterable APIs is `IntoIterator`.

### Decision rule — iter()` is not the universal meaning of iteration

Accept `IntoIterator` when you need one complete traversal and want callers to choose owned or borrowed input. Accept or return `Iterator` when iterator state, laziness, partial consumption, or adapter composition is part of the contract.

The required method of `Iterator` is conceptually simple:

```rust
trait Iterator {
    type Item;
    fn next(&mut self) -> Option<Self::Item>;
}
```

Every adapter and consumer is built on a state machine that advances through `next` or equivalent specialized traversal methods.

```rust
let mut iter = [10, 20, 30].into_iter();
assert_eq!(iter.next(), Some(10));
assert_eq!(iter.next(), Some(20));
assert_eq!(iter.next(), Some(30));
assert_eq!(iter.next(), None);
```

The iterator value is mutable because each call changes what remains.

### Adapters are state machines too

```rust
let mut iter = (1..)
    .map(|x| x * 2)
    .filter(|x| x % 3 == 0)
    .take(2);
```

A call to the outer `next` may call the inner iterator several times. To yield the first item, `filter` may reject values before finding one. `take` counts yielded items, not source attempts.

Trace it:

1. `take.next()` asks `filter.next()`.
2. `filter` asks `map` for 2, rejects it.
3. `filter` asks for 4, rejects it.
4. `filter` asks for 6, accepts it.
5. `take` yields 6 and records one remaining output.

This explains why required side effects inside adapter closures can occur more or fewer times than output count.

### Exhaustion contracts

The basic `Iterator` trait does not require every iterator to remain exhausted forever after returning `None`. Many iterators do, and `FusedIterator` expresses that stronger contract. Adapters such as `fuse` can enforce fused behavior for callers that need it.

### Mutation inside `next`

A custom iterator should update state in an order that preserves its exhaustion and error semantics. If `next` advances an index before validating an item, a failed validation may consume the item. That may be correct or wrong; it must be specified.

### Debugging with explicit pulls

When a chain is confusing, assign it to a mutable variable and call `next` manually. Record source position, closure calls, yielded value, and remaining state. This converts a declarative-looking chain back into a concrete transition system.

### Decision rule — Debugging with explicit pulls

Treat every iterator as a mutable machine whose public operation is “produce the next item or report no item now.” Derive adapter behavior by nesting those machines, not by assuming a bulk collection transformation.

Creating an iterator adapter does not normally traverse the source.

```rust
let mapped = [1, 2, 3]
    .into_iter()
    .map(|value| {
        println!("mapping {value}");
        value * 2
    });
```

No mapping is required until something calls `next`. A consumer such as `collect`, `sum`, `find`, `for_each`, or a `for` loop requests items.

```rust
let first = mapped.take(1).collect::<Vec<_>>();
```

Only enough work to produce one output is required.

### Laziness is not free work

Laziness changes timing and may avoid unused work. It does not make required work disappear. A full `collect` still drives the entire finite pipeline unless the collection target itself short-circuits, as `Result` collection can.

### Consumers have different traversal behavior

- `count`, `fold`, and `collect::<Vec<_>>()` normally traverse to exhaustion for finite input.
- `find`, `position`, `any`, and `all` short-circuit.
- `nth` consumes preceding items and the selected item.
- `last` consumes the iterator to exhaustion.
- `for_each` offers no `break` or `continue` from the closure.
- `try_for_each` can short-circuit through its return type.

The consumer determines how much of the lazy description is executed.

### Infinite iterators require bounded consumers

```rust
let first_five: Vec<_> = (0..).map(|n| n * n).take(5).collect();
```

A consumer that requires exhaustion will not terminate on an infinite iterator. Some mathematical results could be known early, but the generic consumer’s contract may still traverse indefinitely.

### Side effects reveal execution but can change design

Using a counter or `println!` while learning can reveal calls. In production, required behavior should not depend on diagnostic observation. `inspect` is useful for tracing, but removing it should not change the product result.

### Borrow duration and laziness

A lazy iterator that borrows a source keeps that borrow for as long as the iterator may be used:

```rust
let mut values = vec![1, 2, 3];
let evens = values.iter().filter(|value| **value % 2 == 0);
// values.push(4); // conflicts while `evens` may still be consumed
let collected: Vec<_> = evens.collect();
```

Materializing earlier can end the borrow, but it allocates and changes the API. Prefer scoping the iterator tightly when that is the real need.

### Decision rule — Borrow duration and laziness

For every lazy pipeline, identify its consumers and ask how far each may traverse. Effects, borrows, failures, and cost occur when the consumer pulls, not when the adapter chain is merely constructed.

Iteration mode is an ownership decision.

```rust
let mut names = vec![String::from("a"), String::from("b")];

let lengths: Vec<usize> = names.iter().map(String::len).collect();

for name in names.iter_mut() {
    name.make_ascii_uppercase();
}

let owned: Vec<String> = names.into_iter().collect();
```

The first path yields `&String`; the collection survives unchanged. The second yields `&mut String`; the collection remains but its elements may change. The third yields owned `String` values and consumes the vector.

### Item types drive closure signatures

`filter` passes a reference to each iterator item. If the iterator item is already a reference, the predicate may receive a double reference:

```rust
let values = [-2, 0, 3];
let positive: Vec<&i32> = values.iter().filter(|value| **value > 0).collect();
```

Pattern matching can make this clearer:

```rust
let positive: Vec<&i32> = values.iter().filter(|&&value| value > 0).collect();
```

Do not add dereferences by trial. State `Iterator::Item`, then apply the adapter’s callback signature.

### Copying and cloning are explicit ownership changes

```rust
let copied: Vec<i32> = values.iter().copied().collect();
```

`copied` converts `&i32` items to `i32` because `i32: Copy`. `cloned` performs `Clone`. Both are deliberate materialization choices.

### Mutating while iterating

You cannot structurally modify a vector while an iterator borrows it. Updating each item through `iter_mut` is permitted because the iterator controls disjoint sequential mutable references. Pushing may reallocate and invalidate references, so it is rejected.

When you need removal or insertion, choose an operation designed for structural mutation, such as `retain`, `drain`, or a two-phase plan.

### Consuming iteration can avoid cloning

If a transformation no longer needs the source collection, use `into_iter` to move values into the result:

```rust
fn normalize_all(values: Vec<String>) -> Vec<String> {
    values
        .into_iter()
        .map(|value| value.trim().to_ascii_lowercase())
        .collect()
}
```

The function’s signature communicates consumption. Cloning every element to preserve an unused source would be weaker design.

### Decision rule — Consuming iteration can avoid cloning

Choose the iteration mode from postconditions: must the source remain usable, may elements change, or should ownership transfer? Then derive item and closure types. Do not start with `.iter()` by habit.

Most iterator adapters take `self` by value. Applying them normally moves the iterator value. `by_ref` temporarily borrows a mutable iterator so the original can be resumed.

```rust
let mut iter = 1..=6;
let first: Vec<_> = iter.by_ref().take(2).collect();
let rest: Vec<_> = iter.collect();

assert_eq!(first, [1, 2]);
assert_eq!(rest, [3, 4, 5, 6]);
```

`by_ref` does not rewind or clone state. It lets an adapter consume through a mutable borrow.

### Stopping adapters may consume the boundary item

```rust
let mut iter = [1, 2, 3, 4].into_iter();
let prefix: Vec<_> = iter.by_ref().take_while(|value| *value < 3).collect();
let remainder: Vec<_> = iter.collect();

assert_eq!(prefix, [1, 2]);
assert_eq!(remainder, [4]);
```

The value `3` was pulled to test the predicate and was not yielded. If the boundary item must remain available, use `peekable` or another protocol that inspects without consuming.

### `peekable`

```rust
let mut iter = [1, 2, 3].into_iter().peekable();
assert_eq!(iter.peek(), Some(&1));
assert_eq!(iter.peek(), Some(&1));
assert_eq!(iter.next(), Some(1));
```

`peek` returns a reference to the next item held inside the adapter. `peek_mut` permits modifying that buffered item before it is yielded.

### Parsing with lookahead

A small parser may inspect the next token to choose a branch. Keep lookahead local and document whether whitespace or separators are consumed before failure. Complex backtracking is not a natural fit for a one-way iterator without an explicit buffer.

### Partial consumers as APIs

A function that takes `&mut impl Iterator` can consume a prefix and return, leaving the caller in control of the remainder. Its contract must specify whether boundary markers are consumed.

```rust
fn take_until_zero<I>(iter: &mut I) -> Vec<i32>
where
    I: Iterator<Item = i32>,
{
    iter.by_ref().take_while(|value| *value != 0).collect()
}
```

This function consumes the zero. Rename or redesign if callers would assume otherwise.

### Decision rule — Partial consumers as APIs

Use `by_ref` when partial consumption and resumption are explicit product behavior. Use `peekable` when one-item lookahead must not consume. Record boundary-item semantics in tests.

The base `Iterator` contract is intentionally weak. Additional traits and methods communicate stronger facts.

### `size_hint`

```rust
fn size_hint(&self) -> (usize, Option<usize>)
```

The lower bound must not exceed the number of remaining items. If an upper bound exists, the remaining count must not exceed it. It is legal for both bounds to be conservative.

Callers may use the hint for allocation decisions, but correctness must not depend on an exact hint unless a stronger contract applies.

### `ExactSizeIterator`

An exact-size iterator can report the precise remaining length through `len`. Implement it only when the remaining length is always representable in `usize` and exact. A plausible upper bound is not enough.

### `DoubleEndedIterator`

This trait adds `next_back`. Front and back pulls must operate on one coherent remaining sequence:

```rust
let mut iter = [1, 2, 3].into_iter();
assert_eq!(iter.next(), Some(1));
assert_eq!(iter.next_back(), Some(3));
assert_eq!(iter.next(), Some(2));
```

A filter can be double-ended when its source is and the predicate can be applied from either end. A stateful adapter whose result depends on left-to-right history may not support meaningful reverse traversal.

### `FusedIterator`

A fused iterator promises that once `next` returns `None`, later calls also return `None`. The `fuse` adapter can wrap an iterator to provide this behavior.

Do not assume every iterator is fused. In particular, some adapters document unspecified behavior after an early `None` unless fused.

### Marker traits are semantic commitments

Implementing a stronger trait can affect generic caller behavior. It must be backed by tests and reasoning, not the observation that current examples work.

Useful law tests include:

- lower bound never exceeds actual remaining items;
- upper bound, when present, never understates them;
- `len` decreases exactly with successful pulls;
- mixed front/back iteration yields every item once;
- after exhaustion, repeated `next` remains `None` for fused iterators.

### Cost claims remain separate

Exact size may permit preallocation, but it does not guarantee a specific allocation strategy or speedup in a particular build. State the contract, then benchmark performance claims in Course 9.

### Decision rule — Cost claims remain separate

Expose only the strongest contract you can prove for every legal state. Stronger iterator traits exist for callers, not for decoration.

Rust does not award style points for adapter count. Choose the form that exposes the invariant and control flow.

### A chain is strong when stages are uniform

```rust
let total: i64 = records
    .iter()
    .filter(|record| record.active)
    .map(|record| record.amount)
    .sum();
```

The stages are recognizable: select, project, aggregate. There is one failure-free flow and no hidden state.

### A loop is strong when decisions interact

```rust
let mut total = 0_i64;
let mut rejected = Vec::new();

for record in records {
    if !record.active {
        continue;
    }
    match validate(record) {
        Ok(amount) => total = total.checked_add(amount).ok_or(Error::Overflow)?,
        Err(error) => rejected.push(error),
    }
}
```

This loop contains accumulation, validation, overflow, and diagnostic collection. It can be expressed through folds and combinators, but the loop may expose the business branches more clearly.

### Named iterators are strong reusable boundaries

A function returning `impl Iterator` can name a semantic query without collecting:

```rust
fn active_amounts(records: &[Record]) -> impl Iterator<Item = i64> + '_ {
    records
        .iter()
        .filter(|record| record.active)
        .map(|record| record.amount)
}
```

Callers can choose `sum`, `take`, `find`, or `collect`. The function preserves laziness and borrowing.

### Refactoring test

When deciding, perform two rewrites:

1. expand the chain into a loop;
2. split the chain into named stage functions.

Compare:

- visibility of item types;
- visibility of early exit;
- error topology;
- reuse;
- borrow duration;
- test boundaries.

Keep the version that makes product semantics easiest to verify.

### Avoid collection as punctuation

Collecting between every stage can make types simple but creates allocations and prevents streaming or early exit. Materialize when the next operation requires ownership, repeated traversal, sorting, grouping, stable storage, or a shorter borrow—not merely to make an error disappear.

### Avoid “one expression” as a goal

Intermediate variables are free semantic labels:

```rust
let parsed = lines.map(parse_line);
let valid = parsed.filter_map(Result::ok); // only if discard is the stated policy
let amounts = valid.map(|event| event.amount);
```

Here the comment exposes a dangerous policy. Better code might preserve errors instead.

### Decision rule — Avoid “one expression” as a goal

Use a chain for a linear, reviewable transformation; a loop for interacting control flow; and a named iterator when a lazy semantic view deserves reuse. Readability is a property of the domain contract, not expression length.

### Case: parse a header, then resume

```rust
fn read_header<'a, I>(lines: &mut I) -> Result<&'a str, Error>
where
    I: Iterator<Item = &'a str>,
{
    lines.next().ok_or(Error::MissingHeader)
}
```

The caller owns iterator state. The function consumes exactly one item and returns a borrow originating from the source, not from the iterator object itself.

```rust
let mut lines = input.lines();
let header = read_header(&mut lines)?;
let body: Vec<_> = lines.collect();
```

### Case: boundary consumption

```rust
let mut numbers = [2, 4, 7, 8].into_iter();
let evens: Vec<_> = numbers.by_ref().take_while(|n| n % 2 == 0).collect();
let rest: Vec<_> = numbers.collect();
```

Prediction: `evens = [2, 4]`; `rest = [8]`. The `7` was consumed to discover the stop.

### Case: laziness and call count

```rust
let mut calls = 0;
let found = (1..)
    .map(|n| { calls += 1; n * 3 })
    .find(|n| *n > 10);
```

The closure is called four times and `found` is `Some(12)`. The infinite source is safe because `find` short-circuits. The mapping closure is `FnMut` due to `calls`.

### Rejected conclusion

“`map` processes all values” is false. “`map` is free” is also false. It defines lazy work driven by a consumer.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For explain the distinct roles of `IntoIterator`, `Iterator`, adapters, and consumers, construct one positive and one causal negative example. Mark the first decisive fact in the **iterator state trace** and state which evidence could falsify the claim.

2. **Outcome 2.** For trace the state changes caused by repeated calls to `next`, construct one positive and one causal negative example. Mark the first decisive fact in the **iterator state trace** and state which evidence could falsify the claim.

3. **Outcome 3.** For predict whether an iteration path borrows, mutably borrows, or consumes its source, construct one positive and one causal negative example. Mark the first decisive fact in the **iterator state trace** and state which evidence could falsify the claim.

4. **Outcome 4.** For use `by_ref`, `peekable`, and fused boundaries without losing track of consumed items, construct one positive and one causal negative example. Mark the first decisive fact in the **iterator state trace** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

The course capstone is **LedgerFlow**, a deterministic event-analysis pipeline with diagnostics, audit history, queries, and reports. Expose lazy borrowed event queries and trace when parsing, filtering, and inspection actually occur. Avoid collecting merely to make a borrow problem disappear. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-02-lazy-log-query/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 33 when you can:

- answer the module question—“What state does an iterator own, when does work happen, and what is consumed by each call to next?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Explain the distinct roles of `IntoIterator`, `Iterator`, adapters, and consumers;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [The Rust Book: Iterators](https://doc.rust-lang.org/book/ch13-02-iterators.html)
- [Iterator](https://doc.rust-lang.org/std/iter/trait.Iterator.html)
- [IntoIterator](https://doc.rust-lang.org/std/iter/trait.IntoIterator.html)

[← Module 31](../../../04-rust-functional-programming/course-book/module-31-closures-capture-and-callable-contracts/index.md) · [one-hundred-module map](../../../COURSE_MAP.md) · [Module 33 →](../../../04-rust-functional-programming/course-book/module-33-iterator-algebra-and-pipeline-shape/index.md)

## Continue

Continue to [Module 33 — Iterator Algebra and Pipeline Shape](../module-33-iterator-algebra-and-pipeline-shape/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
