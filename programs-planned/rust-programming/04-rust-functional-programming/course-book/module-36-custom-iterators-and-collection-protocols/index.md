# Module 36 — Custom Iterators and Collection Protocols

**Course 4 · Day 6 · Module 36 of 100**
`█████████░░░░░░░░░░░░░░░░` **36/100**

[Program](../../../README.md) · [Course 4](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-06-custom-cursors/README.md) · [LedgerFlow guide](../capstone.md)

[← Module 35: Option, Result, and Fallible Traversal](../module-35-option-result-and-fallible-traversal/index.md) · [Module 37: Recursive Data and Structural Sharing →](../module-37-recursive-data-and-structural-sharing/index.md)

## The question

> What laws must a custom traversal obey, and who owns the collection when iteration begins?

## Why this comes now

Built-in adapters cover common shapes, but domain traversal sometimes needs its own state machine. Custom iterators and collection protocols are introduced after adapter algebra so you can implement `next`, exhaustion, size hints, `IntoIterator`, `FromIterator`, and `Extend` without violating caller expectations.

### Prerequisite bridge

Module 35 established **Option, Result, and Fallible Traversal**. Before continuing, verify that you can stop combinator chains when explicit control flow communicates the error topology more clearly. This module preserves that capability and adds the ability to implement a correct custom `iterator` by defining state and exhaustion behavior. Module 37, **Recursive Data and Structural Sharing**, will rely on both when it asks: *How can recursive values be transformed without hiding ownership, rebuilding cost, or structural sharing?*

### Scope boundary

This module owns the reasoning for **custom iterators and collection protocols** inside Course 4. The course uses ordinary functions, closures, iterators, and immutable public models. It does not treat mutation as forbidden, and it postpones macro construction, parallel iteration, async streams, and benchmark-driven optimization. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- Implement a correct custom `Iterator` by defining state and exhaustion behavior.
- Provide owned, shared, and mutable `IntoIterator` implementations only where their semantics are useful.
- Implement `FromIterator` and `Extend` for a domain collection with explicit invariant policy.
- Implement stronger iterator traits only when every required law holds.
- Design `size_hint` as a truthful bound and not as an unsupported performance promise.

A custom iterator is a state machine. Begin with the sequence contract and the minimal state needed to identify what remains.

Suppose a string contains nonempty comma-separated fields and the iterator should yield trimmed slices without allocating:

```rust
pub struct Fields<'a> {
    remainder: Option<&'a str>,
}

impl<'a> Fields<'a> {
    pub fn new(input: &'a str) -> Self {
        Self { remainder: Some(input) }
    }
}
```

The invariant is:

> `remainder` is `None` after exhaustion; otherwise it is the exact suffix not yet considered.

```rust
impl<'a> Iterator for Fields<'a> {
    type Item = &'a str;

    fn next(&mut self) -> Option<Self::Item> {
        loop {
            let input = self.remainder.take()?;
            let (field, rest) = match input.split_once(',') {
                Some((field, rest)) => (field, Some(rest)),
                None => (input, None),
            };
            self.remainder = rest;

            let field = field.trim();
            if !field.is_empty() {
                return Some(field);
            }
        }
    }
}
```

Taking the option first prevents borrowing `self.remainder` while assigning to it. Each loop iteration consumes one logical field, even when the field is skipped.

## Core model

### Specify exhaustion

What should an empty input yield? The implementation above treats it as one empty field and then skips it, so it yields nothing. A trailing comma creates a final empty field, also skipped. These are format decisions, not implementation trivia.

### Errors need an item shape

An iterator cannot return an error outside its `Item`. A fallible iterator commonly uses `Item = Result<T, E>`. Decide whether a yielded error is followed by more items, permanently exhausts the iterator, or leaves behavior unspecified. Encode and test the policy.

### Separate iterator state from output ownership

A borrowed iterator can yield slices when the owner outlives it. An owned iterator may consume elements. Avoid storing references into a buffer that the iterator itself mutates or replaces unless the lifetimes and pinning requirements are genuinely satisfied.

### Minimal required method

Implement `next` correctly before overriding methods such as `fold` or `nth`. Specialized methods can improve behavior, but each becomes another law surface.

### Decision rule — Minimal required method

Write the sequence, state invariant, skip policy, error policy, and exhaustion policy in prose. Then implement `next` as one invariant-preserving transition.

A domain collection can expose different item types depending on how it is received.

```rust
pub struct LedgerEvents {
    events: Vec<Event>,
}
```

Owned iteration can delegate to the vector:

```rust
impl IntoIterator for LedgerEvents {
    type Item = Event;
    type IntoIter = std::vec::IntoIter<Event>;

    fn into_iter(self) -> Self::IntoIter {
        self.events.into_iter()
    }
}
```

Shared iteration yields references:

```rust
impl<'a> IntoIterator for &'a LedgerEvents {
    type Item = &'a Event;
    type IntoIter = std::slice::Iter<'a, Event>;

    fn into_iter(self) -> Self::IntoIter {
        self.events.iter()
    }
}
```

### Mutable iteration is a policy decision

```rust
impl<'a> IntoIterator for &'a mut LedgerEvents {
    type Item = &'a mut Event;
    type IntoIter = std::slice::IterMut<'a, Event>;

    fn into_iter(self) -> Self::IntoIter {
        self.events.iter_mut()
    }
}
```

This is safe Rust, but it may be bad domain design. If event identifiers, ordering keys, or normalized fields must remain invariant, handing out `&mut Event` lets callers violate the collection’s contract.

Alternatives include:

- no mutable iteration;
- iterating mutable views that expose only safe fields;
- methods that apply validated updates;
- consuming transformation into a new collection.

### `for` selects from the expression type

```rust
for event in &events { /* &Event */ }
for event in events { /* Event */ }
```

The variable name does not determine the mode. The expression passed to `for` does.

### Representation exposure

Delegating to `slice::Iter` reveals that shared iteration follows current internal order, but does not necessarily expose the underlying vector as a public type. Returning `impl Iterator` from an inherent method can preserve more flexibility than naming the concrete iterator in a public associated type, although `IntoIterator` requires a concrete associated iterator type.

### Decision rule — Representation exposure

Implement only the receiver modes that express useful and safe ownership. Shared and owned iteration are common; mutable iteration must be justified against invariants.

`collect` delegates to the target type’s `FromIterator` implementation. Implementing it says how a sequence becomes one domain value.

```rust
#[derive(Debug, Default)]
pub struct Diagnostics {
    items: Vec<Diagnostic>,
}

impl FromIterator<Diagnostic> for Diagnostics {
    fn from_iter<I>(iter: I) -> Self
    where
        I: IntoIterator<Item = Diagnostic>,
    {
        Self {
            items: iter.into_iter().collect(),
        }
    }
}
```

Now:

```rust
let diagnostics: Diagnostics = checks.filter_map(check).collect();
```

### Invariants complicate collection

`FromIterator` returns `Self`, not `Result<Self, E>`. If construction can fail, common options are:

- collect `Result<Item, E>` into `Result<Collection, E>` using a validated item constructor;
- define a separate fallible constructor such as `try_from_iter`;
- choose a collection whose policy resolves duplicates or invalid items deterministically;
- avoid `FromIterator` if failure cannot be represented honestly.

Do not panic inside `from_iter` for ordinary invalid input merely to support `collect` syntax.

### Duplicate policy

A domain map collected from keyed records must decide whether later values replace earlier ones, duplicates are retained, or construction is rejected. Standard map behavior is not automatically the domain behavior.

### Capacity is an implementation detail

An implementation can inspect `size_hint` to reserve capacity, but correctness must not depend on exactness. Do not overstate allocation guarantees.

### Collection type inference

`collect` often needs an annotation because many targets can collect the same items:

```rust
let values: Vec<_> = iter.collect();
// or
let values = iter.collect::<Vec<_>>();
```

When the domain type is important, `Diagnostics::from_iter(iter)` can sometimes read more clearly.

### Decision rule — Collection type inference

Implement `FromIterator` when every sequence of item values has a well-defined, total construction policy for the target. Use an explicit fallible constructor when invariant enforcement can fail.

`FromIterator` builds a new value. `Extend` adds items to an existing value.

```rust
impl Extend<Diagnostic> for Diagnostics {
    fn extend<I>(&mut self, iter: I)
    where
        I: IntoIterator<Item = Diagnostic>,
    {
        self.items.extend(iter);
    }
}
```

This supports:

```rust
let mut all = Diagnostics::default();
all.extend(parse_diagnostics);
all.extend(validation_diagnostics);
```

### Invariant policy remains necessary

If the target requires uniqueness, sorted order, or bounded size, `extend` must preserve that contract. Because the trait method cannot return an error, ordinary invalid additions cannot be rejected with `Result`.

Possible designs:

- make the item type validated and extension total;
- define deterministic conflict resolution;
- expose a fallible inherent `try_extend` instead;
- omit `Extend`.

### Relationship to `FromIterator`

A common implementation of `FromIterator` creates a default value and calls `extend`, but only when `Default + Extend` represents the correct construction semantics.

```rust
impl FromIterator<Diagnostic> for Diagnostics {
    fn from_iter<I: IntoIterator<Item = Diagnostic>>(iter: I) -> Self {
        let mut value = Self::default();
        value.extend(iter);
        value
    }
}
```

### Extending borrowed items

Targets can implement `Extend<&'a T>` when cloning or copying is an intentional policy, but this hides ownership work in a generic operation. Prefer explicit item ownership unless borrowed extension is common and documented.

### Phase boundaries

`extend` is useful when several independent validation phases contribute to one report. It is weaker when phases must remain distinguishable; separate fields may communicate more.

### Decision rule — Phase boundaries

Implement `Extend` only when adding an arbitrary iterable of items is total and preserves the target invariant. Use `try_extend` or phase-specific methods when addition can fail or carries distinct meaning.

Stronger iterator traits are not difficult to write syntactically. They are difficult to justify semantically.

### `DoubleEndedIterator`

A range over an indexed slice can support front and back pulls by maintaining two indices:

```rust
pub struct Window<'a, T> {
    slice: &'a [T],
    front: usize,
    back: usize,
}
```

The invariant is `front <= back <= slice.len()`. `next` yields `slice[front]` and increments. `next_back` decrements `back` and yields that item. Mixed calls must never duplicate or omit an item.

A running-average iterator cannot simply reverse because each output depends on the prefix state. Do not implement double-endedness by collecting and reversing unless that eager behavior is the documented abstraction.

### `ExactSizeIterator`

If remaining length is `back - front`, exact size is straightforward. Filters normally cannot know exact output count without scanning remaining items, so they do not generally implement exact size.

### `FusedIterator`

When state has a permanent exhausted marker, implementing `FusedIterator` may be valid. If the source can later produce items after `None`, it is not.

### Law tests

For a custom double-ended exact iterator:

- collect using only `next`;
- collect using only `next_back` and compare reversed order;
- alternate front and back;
- assert `len` before and after each successful pull;
- exhaust and call both ends repeatedly;
- test empty and one-item states.

### Marker implementation without methods

`FusedIterator` is a marker, but its lack of methods does not reduce the semantic burden. Generic code may rely on the promise.

### Decision rule — Marker implementation without methods

Implement stronger traits only when state makes the law obvious and tests exercise mixed operations. Do not simulate a stronger contract through hidden full collection unless eager materialization is acceptable.

A custom adapter wraps another iterator and changes its output behavior. Prefer a named type when the transformation has domain meaning or state not expressible clearly through standard adapters.

Example: yield every `step`th source item, beginning with the first.

```rust
pub struct Stride<I> {
    inner: I,
    step: usize,
    first: bool,
}

impl<I> Stride<I> {
    pub fn new(inner: I, step: usize) -> Option<Self> {
        (step > 0).then_some(Self { inner, step, first: true })
    }
}

impl<I> Iterator for Stride<I>
where
    I: Iterator,
{
    type Item = I::Item;

    fn next(&mut self) -> Option<Self::Item> {
        if self.first {
            self.first = false;
            return self.inner.next();
        }
        self.inner.nth(self.step - 1)
    }
}
```

### Consumption semantics

After yielding an item, the adapter consumes `step - 1` intervening items and then yields the next. The contract must state whether the first item is yielded and how short sources behave.

### Extension trait for ergonomics

Course 3 established extension traits. A sealed or local extension trait can add `.stride(step)` to iterators, but the constructor’s invalid-step policy must still be expressed. Returning `Result` or `Option` from an extension method can make chains awkward; a validated `NonZeroUsize` parameter may be better.

### Forward methods conservatively

You may derive a lower `size_hint`, but do not claim exactness without proof. Do not override `fold`, `nth`, or `count` until baseline behavior is correct and tests show a reason.

### Avoid adapters for one-off policy

A custom type adds vocabulary and public surface. A local `enumerate().filter_map(...)` may be clearer for one call site. Create an adapter when its state machine, laws, and reuse justify a name.

### Decision rule — Avoid adapters for one-off policy

A custom adapter should have a stable sequence contract, minimal state, law tests, and a reason standard adapters do not communicate the behavior adequately.

`size_hint` returns a lower bound and optional upper bound for remaining items. Its primary requirement is truth.

For `Stride` with `n` remaining source items and a pending first output, the exact formula depends on state. A conservative implementation can return `(0, source_upper)` and still be correct. A tighter formula is useful only if proven for every state.

### Property-style tests without a framework

Enumerate small domains:

```rust
for len in 0..20 {
    for step in 1..8 {
        let source: Vec<_> = (0..len).collect();
        let expected: Vec<_> = source.iter().step_by(step).copied().collect();
        let actual: Vec<_> = Stride::new(source.into_iter(), step)
            .expect("positive step")
            .collect();
        assert_eq!(actual, expected);
    }
}
```

This is a law-oriented test: many generated examples exercise one general claim.

### Check hints during traversal

At each state, clone or construct an equivalent iterator when possible, count actual remaining items, and assert:

```text
lower <= actual
upper is None or actual <= upper
```

Do not consume the production iterator merely to test its hint unless the test owns it.

### Exhaustion laws

Test repeated `next` after exhaustion for fused implementations. Test that skipped or failed items are consumed according to contract.

### Compare semantics, not implementation

Reference tests should compare yielded sequences and public contracts, not private fields or exact internal method-call counts unless those counts are documented behavior.

### Decision rule — Compare semantics, not implementation

Begin with a conservative truthful hint. Tighten it only after deriving the formula and adding state-by-state law tests. Correctness outranks speculative reservation gains.

### Domain iterator: nonempty fields

The `Fields<'a>` iterator stores `Option<&'a str>` as unprocessed suffix. `next` takes the suffix, splits once, installs the rest, trims the field, and loops past empty fields.

Proof obligations:

- every comma-delimited segment is considered exactly once;
- yielded slices borrow from original input;
- empty segments are consumed but not yielded;
- after suffix becomes `None`, later calls remain `None`;
- lower size hint may be zero; upper bound can be comma count plus one while nonexhausted.

### Collection: validated IDs

`FromIterator<ValidatedId>` is total because the item constructor already enforces syntax. Duplicate rejection cannot fit `FromIterator` without a policy, so the domain exposes `try_from_iter` returning a duplicate error.

### Rejected marker

Implementing `ExactSizeIterator` because examples happen to show exact counts is rejected; empty-field skipping makes remaining output count unknown without scanning.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For implement a correct custom `Iterator` by defining state and exhaustion behavior, construct one positive and one causal negative example. Mark the first decisive fact in the **collection protocol map** and state which evidence could falsify the claim.

2. **Outcome 2.** For provide owned, shared, and mutable `IntoIterator` implementations only where their semantics are useful, construct one positive and one causal negative example. Mark the first decisive fact in the **collection protocol map** and state which evidence could falsify the claim.

3. **Outcome 3.** For implement `FromIterator` and `Extend` for a domain collection with explicit invariant policy, construct one positive and one causal negative example. Mark the first decisive fact in the **collection protocol map** and state which evidence could falsify the claim.

4. **Outcome 4.** For implement stronger iterator traits only when every required law holds, construct one positive and one causal negative example. Mark the first decisive fact in the **collection protocol map** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

The course capstone is **LedgerFlow**, a deterministic event-analysis pipeline with diagnostics, audit history, queries, and reports. Implement domain traversal for accounts or audit history where a named iterator clarifies state and exhaustion better than another anonymous chain. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-06-custom-cursors/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 37 when you can:

- answer the module question—“What laws must a custom traversal obey, and who owns the collection when iteration begins?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Implement a correct custom `Iterator` by defining state and exhaustion behavior;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [Iterator](https://doc.rust-lang.org/std/iter/trait.Iterator.html)
- [FromIterator](https://doc.rust-lang.org/std/iter/trait.FromIterator.html)
- [Extend](https://doc.rust-lang.org/std/iter/trait.Extend.html)

[← Module 35](../../../04-rust-functional-programming/course-book/module-35-option-result-and-fallible-traversal/index.md) · [one-hundred-module map](../../../COURSE_MAP.md) · [Module 37 →](../../../04-rust-functional-programming/course-book/module-37-recursive-data-and-structural-sharing/index.md)

## Continue

Continue to [Module 37 — Recursive Data and Structural Sharing](../module-37-recursive-data-and-structural-sharing/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
