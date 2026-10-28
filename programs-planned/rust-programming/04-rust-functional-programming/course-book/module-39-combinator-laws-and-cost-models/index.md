# 39 — Combinator Laws and Cost Models

**Course 4, day 9 · Module 39 of 90**  
`█████████████░░░░░░░` **39/90**

[← Module 38: Functional Core and Effect Isolation](../module-38-functional-core-and-effect-isolation/index.md) · [Course 4 overview](../index.md) · [Ninety-module map](../../../COURSE_MAP.md) · [Module 40: Functional Architecture Synthesis →](../module-40-functional-architecture-synthesis/index.md)

## The question

> What semantic laws should a combinator preserve, and what can honestly be claimed about evaluation and cost?

## Why this comes now

Reusable combinators can make a codebase concise while quietly changing order, failure, duplication, or cost. Laws and counterexamples now provide a review method. Complexity claims are tied to named operations and data shapes rather than to the visual length of an iterator chain.

## What you will be able to do

- Design domain combinators that preserve type and error meaning.
- State and test laws such as identity, idempotence, order preservation, and partition consistency where they truly apply.
- Reason about closure capture, allocation, cloning, and materialization costs without claiming unmeasured optimization.
- Choose lazy or eager return types based on lifetime, API, and reuse constraints.
- Reject combinator designs that hide control flow, destroy diagnostics, or produce unusable types.

Rust can compose callables explicitly:

```rust
fn compose<A, B, C, F, G>(f: F, g: G) -> impl Fn(A) -> C
where
    F: Fn(A) -> B,
    G: Fn(B) -> C,
{
    move |value| g(f(value))
}
```

This version requires both callables to implement `Fn`. A more permissive `FnMut` composition needs mutable captured callables and returns `impl FnMut`. An `FnOnce` composition can consume either callable once.

## Core model

### Generic complexity

A universal composition utility quickly encounters lifetimes, borrowing outputs, heterogeneous error types, and callable capability choices. The standard library often provides composition at the data-container level through `map`, `and_then`, and iterator adapters.

### Name domain composition

Instead of a generic `compose`, domain functions can be clearer:

```rust
fn parse_and_validate(line: &str) -> Result<Event, Diagnostic> {
    parse_line(line).and_then(validate_event)
}
```

### Partial application through closures

```rust
fn at_least(minimum: i64) -> impl Fn(&i64) -> bool {
    move |value| *value >= minimum
}
```

The returned closure captures configuration and can be used in a filter.

### Lifetime limits

Composing functions that return references tied to inputs may require higher-ranked bounds or named functions. Do not box to suppress every type error. Course 3’s trait and lifetime tools remain available, but complexity must earn its value.

### Decision rule

Use generic composition when the abstraction appears repeatedly and its callable contract is stable. Prefer domain-named functions and built-in combinators for ordinary pipelines.

A combinator builds new behavior from smaller behavior.

### Predicate conjunction

```rust
fn both<T, P, Q>(mut left: P, mut right: Q) -> impl FnMut(&T) -> bool
where
    P: FnMut(&T) -> bool,
    Q: FnMut(&T) -> bool,
{
    move |value| left(value) && right(value)
}
```

Short-circuiting means `right` is not called when `left` is false. If predicates have effects, order is observable.

### Validator composition

Fail-fast validators can use `and_then`. Accumulating validators need a type that combines diagnostics rather than stopping.

```rust
fn validate_all<T, E>(
    value: &T,
    validators: &mut [impl FnMut(&T) -> Option<E>],
) -> Vec<E> {
    validators.iter_mut().filter_map(|validate| validate(value)).collect()
}
```

A slice of `impl Trait` in this exact nested form is not a generally usable heterogeneous storage design; all elements still share one concrete closure type. For heterogeneous validators, use named enum variants, boxed callable objects, or separate calls. This example is a review trap.

A practical generic helper accepts an iterator of one validator type, or a trait-object slice when runtime heterogeneity is required.

### Reducer combinators

A reducer can be decorated with auditing or invariant checks, but wrappers must preserve failure and state semantics. Required effects should not be smuggled into a generic reducer combinator.

### Domain vocabulary

`both`, `contramap`, and `lift` may be familiar in functional libraries, but domain names such as `requires_all`, `on_field`, or `validate_each` are often clearer to Rust readers.

### Decision rule

Create combinators for repeated domain composition with explicit call order, short-circuiting, error, and ownership contracts. Reject abstractions that require explaining more vocabulary than they remove.

A law is a property claimed for every value in a stated domain. It needs preconditions and a way to falsify overbroad versions.

### Normalization idempotence

```text
normalize(normalize(x)) = normalize(x)
```

This may hold for whitespace and case normalization. It may fail if normalization appends a timestamp or truncates differently after encoding.

### Map identity and composition

For a deterministic structure-preserving map:

```text
map(identity, xs) = xs
map(g, map(f, xs)) = map(g ∘ f, xs)
```

Effects, panic behavior, overflow, and ownership-sensitive cloning can make observational equality more complex.

### Filter laws

Two pure filters preserve order and can combine:

```text
filter(q, filter(p, xs)) = filter(|x| p(x) && q(x), xs)
```

Call counts differ when predicates have effects or can fail. The law requires pure, total predicates and equality over yielded values.

### Partition consistency

For a deterministic predicate, concatenating accepted and rejected values does not generally reconstruct original order. A stronger law compares multisets or uses tagged output preserving positions.

### Counterexample discipline

For every proposed law, try:

- empty input;
- duplicate values;
- boundary numeric values;
- stateful closures;
- errors or panics;
- order-sensitive outputs;
- Unicode text;
- repeated application.

### Law tests are not proofs

Tests increase confidence and expose counterexamples. They do not mathematically prove arbitrary domains. State the validation scope honestly.

### Decision rule

Write the domain, preconditions, observation notion, and counterexamples before adopting a law as an API contract.

A cost model identifies operations that may matter. It does not replace measurement.

### Closure storage

A closure value stores captured data. Capturing a large configuration by value can enlarge every stored closure instance. Capturing an `Rc` or reference changes ownership and access costs. The exact layout remains an implementation detail unless guaranteed.

### Iterator adapters

Adapters are usually small state values containing the inner iterator and closure. Building a chain is lazy, but eventual traversal still executes closures and source pulls. Generic chains may be monomorphized; this does not guarantee a particular optimization outcome.

### Materialization

`collect::<Vec<_>>()` allocates storage according to collection implementation and hints. It enables repeated traversal, sorting, indexing, and ownership decoupling. It also extends value lifetime and may retain capacity.

### Cloning

`cloned()` or explicit clone can be correct ownership policy. Count the cloned data and ask whether consuming iteration, borrowing, `Rc`, or smaller derived values are better.

### Dynamic dispatch

`Box<dyn Fn...>` commonly implies heap allocation for the box and indirect calls. It may reduce code-size duplication or enable runtime heterogeneity. Only measurement resolves workload performance.

### Multiple passes

Two passes over a small in-memory slice may be cheaper in engineering complexity than one accumulator with many branches. A single pass matters for streams, cache behavior, or expensive sources only under real constraints.

### Decision rule

Write a qualitative cost ledger: allocations, clones, retained ownership, traversal count, dispatch, and early exit. Label it a model until benchmarks validate claims.

A lazy API returns an iterator and lets callers choose how much to consume.

```rust
fn errors(report: &Report) -> impl Iterator<Item = &Diagnostic> + '_ {
    report.items.iter().filter(|item| item.is_error())
}
```

An eager API returns owned storage:

```rust
fn error_messages(report: &Report) -> Vec<String> {
    report
        .items
        .iter()
        .filter(|item| item.is_error())
        .map(ToString::to_string)
        .collect()
}
```

### Lazy advantages

- short-circuiting and partial consumption;
- no required intermediate collection;
- borrowed outputs;
- caller-selected consumer.

### Lazy constraints

- lifetime ties to the source;
- opaque or complex return types;
- one-shot iterator state;
- borrow duration;
- callers may trigger work at surprising times if effects exist.

### Eager advantages

- owned, stable snapshot;
- repeated traversal;
- easy storage and return across boundaries;
- sorting, indexing, grouping, and serialization.

### Eager costs

- materialization and ownership transfer;
- complete traversal before return;
- possible loss of short-circuiting;
- allocation or cloning.

### API combinations

A type may expose both a borrowed iterator view and an explicit `to_owned_*` collection method. Names should make materialization visible.

### Decision rule

Return a lazy iterator when caller-selected consumption and borrowing are part of the value. Return an owned collection when stability, repeated use, reordering, or boundary transfer is required.

A reusable combinator that changes errors must state how context and source information survive.

### Mapping errors

```rust
fn on_field<T, U, E, F>(field: &'static str, f: F) -> impl Fn(T) -> Result<U, FieldError<E>>
where
    F: Fn(T) -> Result<U, E>,
{
    move |value| f(value).map_err(|source| FieldError { field, source })
}
```

This preserves the typed source and adds static context.

### Heterogeneous errors

Composing functions with different error types requires a unifying enum, conversion, or boundary-specific wrapper. Converting everything to `String` makes composition easy but weakens programmatic handling.

### Accumulation combinators

A validator combinator must specify order, duplicates, and whether later validators run after a fatal condition. “Collect all errors” may expose sensitive or cascading diagnostics that should stop.

### Recovery combinators

A retry or fallback combinator needs call-count, idempotence, and effect policy. Reinvoking an effectful closure can duplicate writes or consume IDs.

### Diagnostics as output

Warnings can coexist with success. A combinator that returns only `Result<T, E>` cannot express successful output plus warnings without another layer.

### Decision rule

Preserve typed sources and deterministic diagnostic order. Separate fatal failure, recoverable alternatives, warnings, and accumulated validation rather than flattening them into one string channel.

Over-combinatorization occurs when abstraction density exceeds semantic value.

### Symptoms

- nested closures with several inferred parameter types;
- many `move` keywords added without a capture audit;
- boxed callables to unify branches that form a closed enum;
- custom `pipe`, `tap`, `lift`, and `compose` helpers used once;
- errors converted to `Option` to fit `filter_map`;
- folds with tuple accumulators and external mutation;
- required effects inside `inspect`;
- eager collection between adapters solely to simplify types.

### Compiler diagnostics become indirect

Deep generic types can move error messages far from the domain mistake. Named functions, type annotations, and phase boundaries improve both reader and compiler feedback.

### Refactoring method

1. expand to an explicit loop or match;
2. state the domain branches;
3. isolate pure transformations;
4. reintroduce standard adapters where they name one stage;
5. keep intermediate variables with meaningful names;
6. remove one-off combinators.

### API burden

Every public combinator needs documentation, laws, examples, versioning, and error contracts. A private three-line helper can remain concrete.

### Functional architecture is not fluent syntax

A program can have an effect-isolated deterministic core implemented mostly with loops. A long chain can be highly stateful and effectful. Judge flows, not appearance.

### Decision rule

Stop abstracting when the next layer hides domain control flow, weakens diagnostics, or introduces vocabulary without repeated proof value.

### Predicate combinator

```rust
fn both<T, P, Q>(mut p: P, mut q: Q) -> impl FnMut(&T) -> bool
where
    P: FnMut(&T) -> bool,
    Q: FnMut(&T) -> bool,
{
    move |value| p(value) && q(value)
}
```

Law candidate for pure total predicates:

```text
filter(both(p, q), xs) = filter(q, filter(p, xs))
```

Counterexample: if `q` increments a counter, the two forms may call it a different number of times or in different closure-storage contexts. The law must exclude observable effects.

### Validator wrapper

A wrapper adds field context while retaining typed source error. It does not stringify. The error type becomes larger but remains inspectable.

### Cost ledger

- two captured predicate values stored in returned closure;
- no required allocation under generic return;
- short-circuit may avoid `q`;
- each retained item may invoke both predicates;
- no performance claim without measurement.

### Rejected helper

A global `Pipe` trait adding `.pipe`, `.tap`, `.also`, and `.apply` is rejected because the course has one use and standard expressions are clearer.

## Use the idea in a complete program

The course capstone is **LedgerFlow**, a deterministic event-analysis pipeline with diagnostics, audit history, queries, and reports. Review reusable LedgerFlow combinators with laws and counterexamples for order, identity, error propagation, and duplication. Attach honest operation-count claims. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-09-combinator-contracts/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 40 when you can:

- answer the module question—“What semantic laws should a combinator preserve, and what can honestly be claimed about evaluation and cost?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Design domain combinators that preserve type and error meaning;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [Iterator](https://doc.rust-lang.org/std/iter/trait.Iterator.html)
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)

[← Module 38](../../../04-rust-functional-programming/course-book/module-38-functional-core-and-effect-isolation/index.md) · [ninety-module map](../../../COURSE_MAP.md) · [Module 40 →](../../../04-rust-functional-programming/course-book/module-40-functional-architecture-synthesis/index.md)

## Continue

1. Complete the [Module 39 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 39 — Combinator Contracts](../../labs/module-09-combinator-contracts/README.md) from its public contract.
3. Apply the Module 39 increment in the [LedgerFlow engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
