# Module 34 — Folds, Scans, and Short-Circuiting

**Course 4 · Day 4 · Module 34 of 100**
`████████░░░░░░░░░░░░░░░░░` **34/100**

[Program](../../../README.md) · [Course 4](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-04-streaming-metrics/README.md) · [LedgerFlow guide](../capstone.md)

[← Module 33: Iterator Algebra and Pipeline Shape](../module-33-iterator-algebra-and-pipeline-shape/index.md) · [Module 35: Option, Result, and Fallible Traversal →](../module-35-option-result-and-fallible-traversal/index.md)

## The question

> What invariant does an accumulator maintain, and when should a traversal continue, emit intermediate state, or stop early?

## Why this comes now

Mapping changes items; many real analyses must accumulate state or stop when an invariant is violated. Folds, scans, `try_fold`, and short-circuiting are taught through accumulator invariants. This prevents reductions from becoming opaque one-liners whose correctness cannot be explained.

### Prerequisite bridge

Module 33 established **Iterator Algebra and Pipeline Shape**. Before continuing, verify that you can refactor long chains into named semantic stages without forcing premature collection. This module preserves that capability and adds the ability to design a fold accumulator with a precise prefix invariant. Module 35, **Option, Result, and Fallible Traversal**, will rely on both when it asks: *Should a fallible traversal skip, fail fast, recover, accumulate diagnostics, or continue with an explicit default?*

### Scope boundary

This module owns the reasoning for **folds, scans, and short-circuiting** inside Course 4. The course uses ordinary functions, closures, iterators, and immutable public models. It does not treat mutation as forbidden, and it postpones macro construction, parallel iteration, async streams, and benchmark-driven optimization. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- Design a fold accumulator with a precise prefix invariant.
- Distinguish `fold`, `reduce`, `sum`, `product`, and explicit loops by semantics rather than style.
- Use `scan` when evolving state must also yield an output stream.
- Use `try_fold` and `try_for_each` for fallible short-circuiting traversal.
- Use `ControlFlow` for domain-specific early exit without inventing an error.

`fold` consumes an iterator, begins with an initial accumulator, and combines each item into a new accumulator.

```rust
let total = amounts.into_iter().fold(0_i64, |sum, amount| sum + amount);
```

The useful mental model is not “a loop without `mut`.” It is a **prefix invariant**:

> After processing the first `k` items, `sum` equals the sum of exactly those `k` items.

The initial value must make the invariant true for the empty prefix. The closure must preserve it when one item is added.

## Core model

### Named accumulator

```rust
#[derive(Debug, Default, PartialEq)]
struct Summary {
    count: usize,
    total: i64,
    maximum: Option<i64>,
}

let summary = amounts.into_iter().fold(Summary::default(), |mut acc, amount| {
    acc.count += 1;
    acc.total += amount;
    acc.maximum = Some(acc.maximum.map_or(amount, |old| old.max(amount)));
    acc
});
```

This uses local mutation inside an owned accumulator. Publicly, each step is still a value transformation `Summary × i64 -> Summary`. Functional style does not require reallocating a fresh struct for every field update.

### Empty input

The initial accumulator defines the empty result. `count = 0`, `total = 0`, and `maximum = None` are meaningful identities. A fabricated maximum of zero would be wrong for an empty or all-negative domain.

### Order sensitivity

Some folds are order-insensitive under their domain laws; others are not. String concatenation, floating-point accumulation, state machines, and “first error” policies depend on order. Do not casually parallelize or reorder them later.

### Failure atomicity

A fold that mutates external state can leave partial results when a later item fails. Prefer the accumulator to own candidate state and return an error or surviving state explicitly.

### Proof template

For a fold, write:

1. accumulator meaning after any prefix;
2. empty-prefix truth;
3. one-step preservation;
4. overflow or failure policy;
5. order dependence;
6. final interpretation.

### Decision rule — Proof template

Use `fold` when one named state summarizes every consumed prefix and each item advances that state. If the accumulator cannot be explained without simulating code, redesign it.

`reduce` uses the first item as the initial accumulator and therefore returns `Option<Item>`:

```rust
let maximum = values.into_iter().reduce(i64::max);
```

Empty input produces `None`. This is appropriate when no universal identity exists or when the result must have the same type as the item.

### `fold` with an explicit identity

```rust
let total = values.into_iter().fold(0_i64, |acc, value| acc + value);
```

The caller chooses the initial state and may change type.

### `sum` and `product`

```rust
let total: i64 = values.iter().copied().sum();
```

These consumers use the `Sum` and `Product` traits. They are concise when arithmetic aggregation is the whole meaning. They do not remove the need for an overflow policy. In debug builds, integer overflow may panic; release behavior depends on compiler overflow checks and operation. Use checked arithmetic when overflow is a product error.

```rust
let total = values
    .into_iter()
    .try_fold(0_i64, |acc, value| acc.checked_add(value).ok_or(Error::Overflow));
```

### Identity laws

An identity `e` for operation `⊕` must satisfy `e ⊕ x = x` and `x ⊕ e = x` within the domain. Zero is an identity for integer addition; an empty string is an identity for concatenation. There may be no valid identity for “latest timestamp” without an optional result.

### Non-associative operations

Changing grouping is valid only when the operation is associative under the domain semantics. Floating-point addition is not mathematically associative due to rounding. A future parallel reduction may produce a different result from a left fold even if both are reasonable.

### Choose from semantics

- `reduce` when the first item is a natural seed and empty input means no result;
- `fold` when you have a meaningful explicit initial state or a different accumulator type;
- `sum`/`product` for standard arithmetic aggregation with accepted numeric behavior;
- `try_fold` for checked or fallible accumulation.

A fold returns one final accumulator. `scan` retains evolving state and yields zero or one output per input until it stops.

```rust
let running_totals = amounts.into_iter().scan(0_i64, |total, amount| {
    *total += amount;
    Some(*total)
});
```

For input `10, -3, 5`, the iterator yields `10, 7, 12`.

### State and output may differ

```rust
#[derive(Default)]
struct State {
    seen: usize,
    total: i64,
}

let averages = amounts.into_iter().scan(State::default(), |state, amount| {
    state.seen += 1;
    state.total += amount;
    Some(state.total as f64 / state.seen as f64)
});
```

The internal state is `State`; the yielded item is `f64`.

### `None` stops the scan

Returning `None` signals the adapter to stop yielding. It is not merely “skip this item.” For optional filtering, use `filter_map`. For fallible stopping with an error, consider an iterator of `Result`, `map_while` with explicit loss, or a custom iterator.

### Stateful laziness

The scan state advances only as downstream consumers pull. Reusing, partially consuming, or dropping the iterator affects how much state transition occurs.

### Stateful adapters and laws

A scan may depend on left-to-right history. Reordering changes outputs, and reverse iteration is generally not meaningful. A stateful closure may also make repeated traversals differ if it captures external state; keep state inside the scan when possible.

### Named scan state

As with folds, use a struct when the state has several fields or invariants. Avoid tuples that force readers to remember positions.

### Use cases

- running totals and averages;
- sequence numbering with resets;
- decoding deltas into absolute positions;
- emitting state transitions;
- stopping after a threshold while preserving prefix outputs.

### Decision rule — Use cases

Use `scan` when each input updates state and that evolving state must produce a lazy stream. Use `fold` when only the final state matters. Use `filter_map` when `None` means skip rather than terminate.

`try_fold` is the fallible counterpart to `fold`. The closure returns a type that can signal continuation or early exit, commonly `Result` or `Option`.

```rust
fn checked_total(values: impl IntoIterator<Item = i64>) -> Result<i64, Error> {
    values
        .into_iter()
        .try_fold(0_i64, |acc, value| {
            acc.checked_add(value).ok_or(Error::Overflow)
        })
}
```

On the first overflow, traversal stops and the error is returned.

### Iterator state after failure

`try_fold` takes `&mut self` internally in the iterator API, and callers working with a mutable iterator can sometimes resume after short-circuiting. The exact item consumption depends on where failure occurred. Test it when resumption is part of the contract.

### `try_for_each`

Use `try_for_each` when no accumulator is needed:

```rust
files.iter().try_for_each(|path| validate_path(path))?;
```

This communicates “perform a fallible operation for each item until one fails.” If the operation is an external effect, partial completion remains possible; `try_for_each` does not provide transactionality.

### `Option` short-circuiting

```rust
let total = values.into_iter().try_fold(0_u64, |acc, value| {
    acc.checked_add(value)
});
```

The result is `Option<u64>`. `None` signals failure but carries no reason. Use it only when absence is sufficient.

### Do not confuse short-circuiting with accumulation

`try_fold` intentionally stops at the first residual. To collect all validation errors, the accumulator must store diagnostics and continue, or the pipeline must partition results.

### Error context

Map low-level errors into domain context inside the closure:

```rust
lines.enumerate().try_fold(Vec::new(), |mut records, (index, line)| {
    let record = parse(line).map_err(|source| Error::Line {
        number: index + 1,
        source,
    })?;
    records.push(record);
    Ok(records)
})
```

A simple loop may be more readable for this multi-step case. The point is the short-circuiting contract, not syntax compression.

### Decision rule — Error context

Use `try_fold` when a prefix accumulator should be returned only if every processed step succeeds. Use `try_for_each` for fallible traversal without an aggregate. State partial-effect behavior separately.

Sometimes traversal should stop successfully because a condition has been met. Calling that condition an error distorts the domain.

`ControlFlow` has two variants:

```rust
use std::ops::ControlFlow;

ControlFlow::Continue(state)
ControlFlow::Break(value)
```

It works with `try_fold` and `try_for_each` because those consumers support short-circuiting control types.

```rust
use std::ops::ControlFlow;

fn first_prefix_over<I>(values: I, limit: i64) -> Option<(usize, i64)>
where
    I: IntoIterator<Item = i64>,
{
    let result = values
        .into_iter()
        .enumerate()
        .try_fold(0_i64, |total, (index, value)| {
            let next = total + value;
            if next > limit {
                ControlFlow::Break((index, next))
            } else {
                ControlFlow::Continue(next)
            }
        });

    match result {
        ControlFlow::Break(found) => Some(found),
        ControlFlow::Continue(_) => None,
    }
}
```

Crossing the threshold is a successful search result, not a failure.

### Break and continue payloads have different meanings

The continue payload is the state needed for the next item. The break payload is the final answer available at termination. They need not be the same type.

### Compare with `find`

`find` is simpler when the decision depends only on one item. `ControlFlow` is useful when the stop condition depends on accumulated state, recursion, or a richer answer.

### Recursive traversal

Tree walks can use `ControlFlow` to stop after finding a node while avoiding a fabricated error type. This pattern appears in visitor-style APIs.

### Avoid custom control enums without need

A domain enum may be appropriate when there are several terminal outcomes. For simple continue/break semantics, the standard type communicates integration with short-circuiting APIs.

### Decision rule — Avoid custom control enums without need

Use `ControlFlow` when early termination is a normal control result and the stop condition needs accumulated or recursive context. Use `Result` when termination represents failure with error meaning.

A single pass can compute several summaries, but the accumulator must remain coherent.

```rust
#[derive(Debug, Default, PartialEq)]
struct Metrics {
    accepted: usize,
    rejected: usize,
    total: i64,
    minimum: Option<i64>,
    maximum: Option<i64>,
}

impl Metrics {
    fn observe_ok(mut self, value: i64) -> Result<Self, Error> {
        self.accepted += 1;
        self.total = self.total.checked_add(value).ok_or(Error::Overflow)?;
        self.minimum = Some(self.minimum.map_or(value, |old| old.min(value)));
        self.maximum = Some(self.maximum.map_or(value, |old| old.max(value)));
        Ok(self)
    }

    fn observe_error(mut self) -> Self {
        self.rejected += 1;
        self
    }
}
```

The fold can distinguish valid and invalid observations:

```rust
let metrics = parsed.into_iter().try_fold(Metrics::default(), |metrics, item| {
    match item {
        Ok(value) => metrics.observe_ok(value),
        Err(_) => Ok(metrics.observe_error()),
    }
})?;
```

Whether discarding error details is acceptable is a separate product decision.

### Partition before aggregate when semantics differ

If errors need detailed reporting, first collect or partition them, then aggregate accepted values. One pass is not automatically better if it produces an opaque accumulator that mixes unrelated concerns.

### Stable order and grouped aggregation

Grouping often requires a map, which is local mutation inside the accumulator:

```rust
use std::collections::BTreeMap;

let totals = events.into_iter().fold(BTreeMap::new(), |mut by_account, event| {
    *by_account.entry(event.account).or_insert(0_i64) += event.amount;
    by_account
});
```

`BTreeMap` provides deterministic key order. Overflow still needs checked handling in real financial code.

### Multiple passes may be clearer

For an in-memory slice, two simple passes can be better than one complicated fold. The cost difference may be irrelevant, and separate passes allow independent tests. One-pass design matters for streams, expensive sources, or large data only after requirements and measurement.

### Decision rule — Multiple passes may be clearer

Use one-pass aggregation when the accumulator has one coherent invariant and source traversal is meaningfully constrained. Split phases when error reporting, sorting, or review clarity requires different structures.

Folds do not solve numeric correctness. An elegant reducer can still overflow, lose precision, or encode the wrong empty-input policy.

### Checked integer accumulation

```rust
fn checked_sum(values: impl IntoIterator<Item = i64>) -> Result<i64, Error> {
    let mut total = 0_i64;
    for value in values {
        total = total.checked_add(value).ok_or(Error::Overflow)?;
    }
    Ok(total)
}
```

This loop and a `try_fold` can express the same contract. Choose based on readability.

### Floating-point considerations

Order affects rounding. Filtering, sorting, parallelization, or changing fold direction may change the result. If the domain requires decimal exactness, binary floating point may be the wrong representation. Course 4 does not introduce a decimal crate; it requires the representation decision to be explicit.

### Early exit and diagnostics

A loop is often clearer when several actions happen on each item:

```rust
for (line_number, line) in lines.enumerate() {
    let parsed = match parse(line) {
        Ok(value) => value,
        Err(source) => {
            diagnostics.push(Diagnostic::parse(line_number + 1, source));
            continue;
        }
    };

    if let Err(error) = state.apply(parsed) {
        diagnostics.push(error.into());
    }
}
```

A fold could carry both state and diagnostics, but explicit branches may be easier to review.

### Mutation is not the enemy

A local `mut` variable with exclusive ownership is often the clearest implementation. Functional architecture concerns observable state and compositional contracts, not a ban on assignments.

### Optimization claims

Iterator chains and loops are both subject to compiler optimization. Do not teach that one is categorically faster. Course 9 measures real workloads.

### Decision rule — Optimization claims

Choose the control form that makes overflow, early exit, diagnostics, and state invariants visible. Functional skill includes knowing when not to use a fold.

### Reducer: account balance

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct Account {
    balance: i64,
    deposits: u64,
    withdrawals: u64,
}

fn apply(mut account: Account, amount: i64) -> Result<Account, Error> {
    account.balance = account.balance.checked_add(amount).ok_or(Error::Overflow)?;
    if amount >= 0 {
        account.deposits += 1;
    } else {
        account.withdrawals += 1;
    }
    Ok(account)
}

let final_account = amounts.into_iter().try_fold(initial, apply)?;
```

Prefix invariant: after `k` amounts, balance equals checked sum of initial balance and the first `k` amounts; counters equal sign classifications of those amounts. On overflow, no final account is returned. Because `Account` is copied in this example, the caller can retain `initial`; a larger owned state may be moved.

### Scan: balances after each event

```rust
let balances = amounts.into_iter().scan(initial, |state, amount| {
    match apply(*state, amount) {
        Ok(next) => { *state = next; Some(Ok(next.balance)) }
        Err(error) => Some(Err(error)),
    }
});
```

This yields an error item but continues unless the consumer stops; it does not automatically terminate after error. A custom iterator or `map_while` would encode different semantics.

### `ControlFlow`: first overdraft

Use `try_fold` with `ControlFlow::Break` when finding the first negative balance is a search result rather than an error.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For design a fold accumulator with a precise prefix invariant, construct one positive and one causal negative example. Mark the first decisive fact in the **accumulator invariant** and state which evidence could falsify the claim.

2. **Outcome 2.** For distinguish `fold`, `reduce`, `sum`, `product`, and explicit loops by semantics rather than style, construct one positive and one causal negative example. Mark the first decisive fact in the **accumulator invariant** and state which evidence could falsify the claim.

3. **Outcome 3.** For use `scan` when evolving state must also yield an output stream, construct one positive and one causal negative example. Mark the first decisive fact in the **accumulator invariant** and state which evidence could falsify the claim.

4. **Outcome 4.** For use `try_fold` and `try_for_each` for fallible short-circuiting traversal, construct one positive and one causal negative example. Mark the first decisive fact in the **accumulator invariant** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

The course capstone is **LedgerFlow**, a deterministic event-analysis pipeline with diagnostics, audit history, queries, and reports. Reduce valid events into ledger state with an explicit prefix invariant and short-circuit on fatal violations without leaving partial mutation. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-04-streaming-metrics/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 35 when you can:

- answer the module question—“What invariant does an accumulator maintain, and when should a traversal continue, emit intermediate state, or stop early?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Design a fold accumulator with a precise prefix invariant;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [Iterator::fold](https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.fold)
- [Iterator::try_fold](https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.try_fold)
- [ControlFlow](https://doc.rust-lang.org/std/ops/enum.ControlFlow.html)

[← Module 33](../../../04-rust-functional-programming/course-book/module-33-iterator-algebra-and-pipeline-shape/index.md) · [one-hundred-module map](../../../COURSE_MAP.md) · [Module 35 →](../../../04-rust-functional-programming/course-book/module-35-option-result-and-fallible-traversal/index.md)

## Continue

Continue to [Module 35 — Option, Result, and Fallible Traversal](../module-35-option-result-and-fallible-traversal/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
