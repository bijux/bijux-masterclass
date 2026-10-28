# 31 — Closures, Capture, and Callable Contracts

**Course 4, day 1 · Module 31 of 90**  
`██████████░░░░░░░░░░` **31/90**

[← Module 30: Architectural Synthesis](../../../03-rust-traits-generics-architectural-design/course-book/module-30-architectural-synthesis/index.md) · [Course 4 overview](../index.md) · [Ninety-module map](../../../COURSE_MAP.md) · [Module 32: The Iterator Model →](../module-32-the-iterator-model/index.md)

## The question

> What does a closure capture, which callable traits does it implement, and what invocation contract should an API require?

## Why this comes now

Course 3 treated callable behavior largely through traits and objects. Course 4 begins inside the callable value itself: what a closure captures, whether it mutates or consumes that environment, and how many times a caller may invoke it. This capability model is required before iterator pipelines can be reasoned about honestly.

## What you will be able to do

- Distinguish function items, function pointers, and anonymous closure types.
- Predict closure capture mode and the resulting `Fn`, `FnMut`, and `FnOnce` capabilities.
- Choose the weakest callable bound that exactly matches an API’s invocation contract.
- Use `move` deliberately without assuming that every move closure is `FnOnce`.
- Select among generic callables, `impl Fn*`, and boxed callable trait objects from real storage and dispatch requirements.

Rust has several things that can be called with parentheses, but they are not one type.

A named function such as:

```rust
fn normalize(value: &str) -> String {
    value.trim().to_ascii_lowercase()
}
```

has a unique **function item type**. The type is zero-sized and identifies that exact function. It can usually coerce to the function-pointer type `fn(&str) -> String` when a concrete pointer is required.

```rust
let pointer: fn(&str) -> String = normalize;
assert_eq!(pointer("  HIGH "), "high");
```

A closure expression creates another unique, anonymous type:

```rust
let prefix = String::from("acct:");
let label = |id: &str| format!("{prefix}{id}");
```

The closure value contains whatever environment it captures. Here it must retain access to `prefix`. Two textually identical closure expressions still have different anonymous types because each expression defines its own closure type.

## Core model

### Why the distinction matters

A function pointer can point only to a non-capturing callable with the required ABI and signature. A capturing closure cannot discard its environment and become a plain function pointer:

```rust,compile_fail
let threshold = 10;
let predicate: fn(i32) -> bool = |value| value >= threshold;
```

The predicate needs `threshold`; a function pointer has nowhere to store it.

Generic callable parameters preserve the concrete closure type:

```rust
fn count_matching<I, F>(items: I, predicate: F) -> usize
where
    I: IntoIterator,
    F: FnMut(&I::Item) -> bool,
{
    items.into_iter().filter(predicate).count()
}
```

This boundary accepts function items, function pointers, and suitable closures. The caller’s concrete callable type remains known to the compiler.

A trait object erases that type:

```rust
struct FilterSet<T> {
    filters: Vec<Box<dyn Fn(&T) -> bool>>,
}
```

Erasure is useful only because the vector must store different closure types behind one runtime interface. It is not a default simplification.

### Function items can be more flexible than pointers

A generic API should usually accept `F: Fn...` rather than `fn(...)` unless pointer identity or a C-compatible table is part of the design. A function item implements the callable traits and can be passed to the generic API without losing information. Requiring a function pointer excludes capturing closures for no benefit.

```rust
fn apply_twice<F>(value: i32, f: F) -> i32
where
    F: Fn(i32) -> i32,
{
    f(f(value))
}

fn increment(x: i32) -> i32 { x + 1 }

assert_eq!(apply_twice(3, increment), 5);
assert_eq!(apply_twice(3, |x| x * 2), 12);
```

### Decision rule

Use a named function when the behavior needs no environment and deserves a stable name. Use a closure when behavior is local or parameterized by nearby values. Accept a generic callable when one concrete callable flows through the call. Use a function pointer only when pointer semantics are intentional. Use a boxed callable only when heterogeneous storage, runtime replacement, or recursive type erasure is a real requirement.

A closure captures an outer place because its body uses that place. Rust then chooses a capture mode sufficient for the body: shared borrow, mutable borrow, or ownership. The mode is not selected by writing `&`, `&mut`, or `move` in a parameter list; closure parameters are inputs, while captures are stored environment.

```rust
let title = String::from("report");
let show = || title.len();
```

`show` only reads `title`, so a shared borrow is sufficient. The original remains usable while the borrow rules permit it.

```rust
let mut count = 0;
let mut record = || {
    count += 1;
    count
};
```

The body mutates `count`, so the closure captures it through a mutable borrow. The closure value must itself be invoked mutably because each call may change captured state.

```rust
let payload = String::from("owned");
let take = || payload;
```

Calling `take` moves `payload` out of the closure environment. The closure must have captured ownership, and the call consumes the closure’s ability to produce the payload again.

### Capture precision

Modern Rust can capture a field or dereference path more precisely than an entire containing value when the language rules permit it.

```rust
struct Job {
    name: String,
    retries: u32,
}

let job = Job {
    name: String::from("index"),
    retries: 3,
};

let name_len = || job.name.len();
println!("{}", job.retries);
println!("{}", name_len());
```

Do not reduce this to “closures borrow variables.” The relevant unit is a **place expression**: perhaps a variable, a field, or a dereferenced field. Precision matters when one field can be moved or borrowed while another remains usable.

### A capture audit

For each captured place, answer:

1. What exact place does the body use?
2. Does the body only read it, mutate it, or move from it?
3. Does the closure need to outlive the current scope?
4. Does the caller invoke the closure once or repeatedly?
5. Does storing the closure extend the borrow and block later access?

Consider:

```rust
fn make_counter<'a>(count: &'a mut u64) -> impl FnMut() -> u64 + 'a {
    move || {
        *count += 1;
        *count
    }
}
```

The `move` transfers the mutable reference into the closure. It does not transfer ownership of the referent. The returned closure keeps the exclusive borrow active for its lifetime.

### Hidden lifetime extension

A common surprise is that assigning a closure to a variable can keep a borrow alive longer than an immediately invoked closure would:

```rust
let mut values = vec![1, 2, 3];
let read_len = || values.len();
// values.push(4); // may conflict while `read_len` is later used
println!("{}", read_len());
```

The repair is not automatically `move` or `clone`. Ask whether the callable must be stored. Sometimes calling a named helper immediately makes the desired borrow scope obvious.

### Decision rule

Treat closure capture as dataflow into an anonymous struct. List its fields conceptually. Then derive borrowing, mutability, and lifetime consequences from how the body uses those fields.

Every closure implements `FnOnce` because every closure can be invoked at least once. Some also implement `FnMut`; a subset of those also implement `Fn`.

The hierarchy is determined by what calling the closure does to captured values:

- **`FnOnce`**: calling may consume captured state.
- **`FnMut`**: calling does not consume captured state, but may mutate it.
- **`Fn`**: calling neither consumes nor mutates captured state through the closure.

This is a capability ladder, not three unrelated labels.

```rust
fn invoke_once<F, R>(f: F) -> R
where
    F: FnOnce() -> R,
{
    f()
}

fn invoke_three_times<F>(mut f: F) -> [u64; 3]
where
    F: FnMut() -> u64,
{
    [f(), f(), f()]
}

fn compare_twice<F>(f: F, left: i32, right: i32) -> bool
where
    F: Fn(i32) -> i32,
{
    f(left) == f(right)
}
```

`invoke_once` deliberately uses the weakest requirement. It can accept an `Fn`, `FnMut`, or `FnOnce` closure because it promises only one call.

### The body determines call capability

A `move` closure can still implement `Fn`:

```rust
let prefix = String::from("acct-");
let render = move |id: u32| format!("{prefix}{id}");

assert_eq!(render(1), "acct-1");
assert_eq!(render(2), "acct-2");
```

The closure owns `prefix`, but each call only reads it. Ownership of the environment and consumption during invocation are different questions.

By contrast:

```rust
let token = String::from("secret");
let consume = move || token;
```

The body returns `token` by value, moving it out. The closure is only `FnOnce`.

### Why `FnMut` APIs take a mutable callable

A function accepting `F: FnMut(A) -> B` must have mutable access to the callable because invocation may update its environment:

```rust
fn map_three<F>(mut f: F) -> [i32; 3]
where
    F: FnMut(i32) -> i32,
{
    [f(1), f(2), f(3)]
}
```

An `Fn` closure also satisfies this requirement; the API simply allows more behavior than an `Fn`-only boundary.

### Bound choice is an API promise

If an API calls a callback once, requiring `Fn` is unnecessarily strict. It rejects closures that would be safe because they consume a resource during that single call.

```rust
fn with_message<F>(message: String, handler: F)
where
    F: FnOnce(String),
{
    handler(message);
}
```

Conversely, an API that stores and repeatedly invokes a callback cannot accept an arbitrary `FnOnce` without adding a replacement protocol.

### Method-call intuition

Conceptually, the call traits correspond to receiver strengths:

- `FnOnce::call_once(self, ...)`
- `FnMut::call_mut(&mut self, ...)`
- `Fn::call(&self, ...)`

Their direct methods are not ordinary stable syntax for application code, but this receiver model explains why the bounds differ.

### Decision rule

Count invocations first. Then determine whether the callback must remain callable after each invocation. Choose `FnOnce` for at-most-once, `FnMut` for repeated calls with permitted state mutation, and `Fn` only when repeated calls must not require mutable access to the callable.

The `move` keyword asks the closure to capture used outer places by value rather than by borrowing them. It is primarily about the lifetime and ownership of the closure environment.

```rust
fn deferred_label(prefix: String) -> impl Fn(u32) -> String {
    move |id| format!("{prefix}{id}")
}
```

Without `move`, the closure would try to borrow the local `prefix`, but the returned closure outlives the function call. Moving `prefix` into the closure gives the closure an owned environment.

### `move` does not mean “consume on call”

The closure above can be called repeatedly because formatting only borrows its owned `String`. Call capability still comes from the body.

A second closure is different:

```rust
fn deferred_take(value: String) -> impl FnOnce() -> String {
    move || value
}
```

This body moves `value` out when called, so the result is `FnOnce`.

### Moving references

If the outer variable is a reference, `move` moves the reference value:

```rust
fn borrowed_predicate<'a>(prefix: &'a str) -> impl Fn(&str) -> bool + 'a {
    move |candidate| candidate.starts_with(prefix)
}
```

The closure remains limited by `'a`; `move` cannot make borrowed data owned or extend a referent’s lifetime.

### Deferred execution changes failure timing

Closures are often used to defer work:

```rust
let fallback = || expensive_default();
let value = maybe_value.unwrap_or_else(fallback);
```

The closure is called only if needed. This changes when effects and failures occur. Compare:

```rust
let eager = maybe_value.unwrap_or(expensive_default());
```

The default expression is evaluated before `unwrap_or` is called, even when `maybe_value` is `Some`.

Deferral therefore belongs in the effect and cost flow. A callback may capture a file path now and open the file later; the creation site is not the failure site.

### Repeated deferred work

A closure can accidentally repeat expensive work:

```rust
let parse = || source.parse::<u64>();
let first = parse();
let second = parse();
```

If the intended semantics are “compute once, then reuse,” store the result rather than a repeated computation, or design a cache explicitly. A closure is not memoization.

### Deferred borrows

A stored non-`move` closure may hold a borrow across a larger region than expected. When a later mutation conflicts, identify the required lifetime of deferred execution. Possible repairs include:

- invoke immediately;
- move owned data into the closure;
- capture a smaller field or derived value;
- shorten the scope that stores the closure;
- redesign the API to accept data rather than delayed behavior.

Cloning the entire environment is not a neutral repair.

### Decision rule

Use `move` when the callable must own its environment or cross a scope that borrowed captures cannot. Then separately derive the call trait from what invocation does. Record when deferred work and deferred failure occur.

A higher-order function accepts or returns behavior. Its callable bound should describe how the function actually uses that behavior.

Suppose a parser needs a fallback exactly once:

```rust
fn parse_or_else<T, E, F>(text: &str, fallback: F) -> T
where
    T: std::str::FromStr<Err = E>,
    F: FnOnce(E) -> T,
{
    match text.parse() {
        Ok(value) => value,
        Err(error) => fallback(error),
    }
}
```

Requiring `Fn` would reject a fallback that consumes an owned recovery value, even though the parser never calls it twice.

A traversal is different:

```rust
fn count_by<I, P>(items: I, mut predicate: P) -> usize
where
    I: IntoIterator,
    P: FnMut(&I::Item) -> bool,
{
    items
        .into_iter()
        .filter(|item| predicate(item))
        .count()
}
```

The predicate may be called once per item and may maintain local counters. `FnMut` is the honest contract.

### Separate roles instead of overloading one callback

An API that calls one callback for validation, transformation, logging, and error recovery is difficult to reason about. Separate roles when they have different call counts or effect contracts:

```rust
fn transform_batch<I, T, U, P, M>(items: I, mut accept: P, mut map: M) -> Vec<U>
where
    I: IntoIterator<Item = T>,
    P: FnMut(&T) -> bool,
    M: FnMut(T) -> U,
{
    items
        .into_iter()
        .filter(|item| accept(item))
        .map(|item| map(item))
        .collect()
}
```

The two callbacks make the dataflow visible. Whether this is better than a single `filter_map` closure depends on whether acceptance and mapping are separate domain concepts.

### Bound only what the body needs

Do not require `Clone`, `Copy`, `Send`, `'static`, or `Sync` because a future use might need them. Every extra bound excludes callers and becomes part of the public contract.

A common accidental bound is `'static` on a callback stored only for the duration of a local operation. `'static` means the captured references, if any, must be valid for the static lifetime; it does not mean the closure value is immortal. Use an explicit lifetime when storage is borrowed and bounded.

### Passing by value or by reference

Generic callables are usually passed by value. This allows the function to own the closure environment and works well with `FnOnce`. Passing `&mut F` is useful when several operations must share one stateful callable:

```rust
fn process_part<T, F>(items: &[T], f: &mut F)
where
    F: FnMut(&T),
{
    for item in items {
        f(item);
    }
}
```

The caller can reuse the same counter or collector across parts.

### Return type and API stability

Returning `impl Fn(A) -> B` hides the concrete closure type but still commits to one concrete type per function body. Different branches cannot return unrelated closure types under one `impl Fn` without additional erasure or restructuring.

### Decision rule

Write the invocation protocol in prose: maximum call count, whether captured state may change, whether the callable is stored, whether it crosses threads, and whether borrowed captures are permitted. Derive bounds from that protocol only.

Because every closure expression has an anonymous type, APIs cannot spell that type directly. Rust provides several strategies, each preserving or erasing different information.

### Return one concrete hidden type

```rust
fn threshold(minimum: i64) -> impl Fn(i64) -> bool {
    move |value| value >= minimum
}
```

The caller does not know the closure type, but the compiler does. Dispatch remains static. Every return path must produce the same concrete hidden type.

This fails:

```rust,compile_fail
fn choose(flag: bool) -> impl Fn(i32) -> i32 {
    if flag {
        |x| x + 1
    } else {
        |x| x * 2
    }
}
```

The branches contain different closure expressions and therefore different types. Possible repairs are:

- move the branch inside one closure;
- return an enum that implements a method;
- use a function pointer if neither branch captures;
- box a trait object when runtime heterogeneity is real.

```rust
fn choose(flag: bool) -> impl Fn(i32) -> i32 {
    move |x| if flag { x + 1 } else { x * 2 }
}
```

### Store one generic callable type

```rust
struct Mapper<F> {
    map: F,
}

impl<F> Mapper<F> {
    fn new(map: F) -> Self { Self { map } }
}

impl<F> Mapper<F>
where
    F: Fn(i32) -> i32,
{
    fn apply(&self, value: i32) -> i32 {
        (self.map)(value)
    }
}
```

This is ideal when each `Mapper` instance has one concrete callable type and callers do not require a heterogeneous collection.

### Store heterogeneous callables

```rust
struct RuleBook {
    rules: Vec<Box<dyn Fn(&str) -> bool>>,
}
```

Now each element may have a different concrete closure type. Costs and constraints include allocation per box in this design, dynamic dispatch at invocation, an object-lifetime bound, and loss of closure-specific traits unless included in the object type.

A borrowed trait object can avoid owning the callable:

```rust
fn all_match(value: &str, rules: &[&dyn Fn(&str) -> bool]) -> bool {
    rules.iter().all(|rule| rule(value))
}
```

The caller controls the callable lifetimes.

### Returning borrowed closures is rarely the right abstraction

A closure that borrows local state cannot escape that state. When an API becomes lifetime-heavy, ask whether it should return transformed data, a named state object, or a function that owns a small derived value instead.

### Type aliases do not erase generic complexity

A type alias can improve readability for a boxed callable:

```rust
type Predicate<T> = Box<dyn Fn(&T) -> bool>;
```

It does not change ownership, allocation, lifetime, or dispatch semantics. Names are not mechanisms.

### Decision rule

Return `impl Fn*` when one hidden concrete callable is enough. Parameterize a struct by `F` when each instance stores one concrete callable. Use `Box<dyn Fn*>` only for true runtime heterogeneity, recursive erasure, or stable binary-facing storage constraints that generic types cannot satisfy.

Closures are concise enough to conceal design mistakes. Review them as state-bearing values.

### Hidden mutable state

```rust
let mut accepted = 0;
let mut predicate = |value: &i32| {
    let ok = *value >= 0;
    if ok { accepted += 1; }
    ok
};
```

This predicate both decides and counts. Reordering or repeating evaluation changes `accepted`. A caller may reasonably expect a predicate to be observationally stable. Prefer a pure predicate followed by an explicit count, or name the callback as an observer with documented call semantics.

### Required effects in `inspect`

```rust
let records = input
    .iter()
    .inspect(|record| persist(record))
    .filter(|record| record.valid());
```

Nothing happens until a consumer runs, and short-circuiting may persist only a prefix. `inspect` is for nonessential observation, not required business effects. Build an effect plan or use an explicit execution loop.

### Accidental `FnOnce`

```rust
let message = String::from("done");
let callback = move || drop(message);
```

If the API needs repeated calls, the design is incompatible. Cloning `message` on every call may alter both cost and semantics. Ask whether the resource should be borrowed, shared, or consumed only at finalization.

### Boxing to silence type errors

Boxing unrelated closures can make branches type-check, but it may hide a closed set that an enum expresses better. If the variants are known and behavior differs by a small mode, use an enum and `match`.

### Capturing too much

A `move` closure that references a whole configuration struct may move large owned fields that it never needs independently. Derive the small captured values first:

```rust
let minimum = config.minimum;
let prefix = config.prefix.clone();
let rule = move |record: &Record| {
    record.score >= minimum && record.name.starts_with(&prefix)
};
```

The clone must still be justified, but the capture is explicit.

### Callback pyramids

Nested callbacks can obscure linear control flow. Rust has `Result`, iterators, and ordinary functions; use them. A callback is appropriate when behavior itself is a parameter, not merely to avoid naming intermediate values.

### Unstable call-count assumptions

Algorithms such as sorting may call key or comparison closures an implementation-dependent number of times. Do not attach required accounting to those callbacks. If each item must be observed exactly once, perform an explicit pass and store derived keys.

### Review checklist

- Is the callback’s call count specified?
- Is repeated invocation semantically stable where required?
- Are effects essential or diagnostic?
- Is capture smaller than the surrounding object?
- Does boxing solve a real heterogeneity boundary?
- Would a named function or enum communicate more?
- Is `clone` repairing semantics or hiding ownership uncertainty?

### Case: a configurable deduplicator

```rust
fn retain_first_by<T, K, F>(items: Vec<T>, mut key: F) -> Vec<T>
where
    K: Eq + std::hash::Hash,
    F: FnMut(&T) -> K,
{
    use std::collections::HashSet;
    let mut seen = HashSet::new();
    items
        .into_iter()
        .filter(|item| seen.insert(key(item)))
        .collect()
}
```

#### Derivation

- `items.into_iter()` yields owned `T`; retained items can move into the result without cloning.
- `filter` receives `&T` because it must decide while retaining ownership of the item.
- `key` may be called once per item and may maintain state, so `FnMut` is the weakest honest repeated-call bound.
- The filter closure captures `seen` and `key` mutably, so it is `FnMut`.
- Output order is first occurrence order, although `HashSet` iteration order is irrelevant because the set is not rendered.
- A panic or side effect in `key` can leave call-count-dependent observations; the API should not promise exactly-once under future algorithm changes unless that is essential.

### Case: fallback consumes a recovery token

```rust
fn resolve<F>(primary: Option<String>, fallback: F) -> String
where
    F: FnOnce() -> String,
{
    primary.unwrap_or_else(fallback)
}
```

`FnOnce` accepts a closure that moves a prebuilt token out of its environment. Requiring `Fn` would reject it without benefit because the fallback is called at most once.

### Rejected design

```rust
fn resolve(primary: Option<String>, fallback: Box<dyn Fn() -> String>) -> String
```

Boxing adds allocation and erasure without heterogeneous storage or runtime replacement. It also requires `Fn`, excluding consuming fallbacks. Generic `FnOnce` is both simpler and more capable.

## Use the idea in a complete program

The course capstone is **LedgerFlow**, a deterministic event-analysis pipeline with diagnostics, audit history, queries, and reports. Define LedgerFlow callbacks for filtering, mapping, and policy decisions with the weakest callable capability that matches actual invocation and capture behavior. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-01-closure-policy-matrix/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 32 when you can:

- answer the module question—“What does a closure capture, which callable traits does it implement, and what invocation contract should an API require?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Distinguish function items, function pointers, and anonymous closure types;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [The Rust Book: Closures](https://doc.rust-lang.org/book/ch13-01-closures.html)
- [Rust Reference: Closure expressions](https://doc.rust-lang.org/reference/expressions/closure-expr.html)
- [Fn traits](https://doc.rust-lang.org/std/ops/trait.Fn.html)

[← Module 30](../../../03-rust-traits-generics-architectural-design/course-book/module-30-architectural-synthesis/index.md) · [ninety-module map](../../../COURSE_MAP.md) · [Module 32 →](../../../04-rust-functional-programming/course-book/module-32-the-iterator-model/index.md)

## Continue

1. Complete the [Module 31 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 31 — Closure Policy Matrix](../../labs/module-01-closure-policy-matrix/README.md) from its public contract.
3. Apply the Module 31 increment in the [LedgerFlow engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
