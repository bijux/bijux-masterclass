# Module 06 — Collections, Iterators, and Closures

**Course 1 · Day 6 · Module 6 of 100**
`██░░░░░░░░░░░░░░░░░░░░░░░` **6/100**

[Program](../../../README.md) · [Course 1](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-06-in-memory-board/README.md) · [Taskboard guide](../capstone.md)

[← Module 5: Structs, Enums, Methods, and Pattern Matching](../module-05-structs-enums-methods-and-pattern-matching/index.md) · [Module 7: Errors, Parsing, Files, and Persistence →](../module-07-errors-parsing-files-and-persistence/index.md)

## The question

> Does an algorithm borrow, mutate, or consume a collection, and what complexity and invalidation consequences follow?

## Why this comes now

A useful program holds many values and processes them repeatedly. Collections therefore arrive after the element model is typed, and iterators arrive only after borrowed, mutable, and consuming access are distinguishable. Closures are introduced narrowly as behavior passed into collection operations; Course 4 later studies their full dataflow role.

### Prerequisite bridge

Module 5 established **Structs, Enums, Methods, and Pattern Matching**. Before continuing, verify that you can replace boolean-flag and stringly typed state with an explicit state machine and tested legal transitions. This module preserves that capability and adds the ability to use vec, slices, and hashmap with explicit length, capacity, invalidation, lookup, and ordering assumptions. Module 7, **Errors, Parsing, Files, and Persistence**, will rely on both when it asks: *Which failures are part of the product contract, where are they detected, and what state is visible after failure?*

### Scope boundary

This module owns the reasoning for **collections, iterators, and closures** inside Course 1. The course stays in safe Rust and mostly in the standard library. It introduces the ownership, trait, iterator, lifetime, module, and testing vocabulary required by later courses, but it does not yet pursue advanced lifetime algebra, smart-pointer architecture, unsafe code, concurrency, async runtimes, or macro construction. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- Use Vec, slices, and HashMap with explicit length, capacity, invalidation, lookup, and ordering assumptions.
- Derive item ownership for iter, iter_mut, into_iter, and for-loop desugaring contexts.
- Use closures and core iterator adapters while keeping transformations readable and cost-aware.
- Avoid mutation-during-iteration hazards by staging keys, splitting phases, or selecting a different operation.
- Produce deterministic public output even when internal storage has unspecified iteration order.

## Core model

### Why this module exists

Collections combine ownership, allocation, algorithmic cost, and invalidation. Iterator syntax can make code concise, but fluency requires knowing whether the collection is borrowed, mutably borrowed, or consumed and whether an adapter is lazy, allocates, preserves order, or short-circuits.

### Vector invariants and invalidation

A `Vec<T>` owns a contiguous allocation with length and capacity. `push` may reallocate, invalidating references into the old allocation. Therefore a design cannot keep `&T` into a vector and then mutate the vector in a way that may reallocate.

Prefer safe lookup when absence is part of the contract:

```rust
pub fn second(values: &[String]) -> Option<&str> {
    values.get(1).map(String::as_str)
}
```

Indexing is appropriate only when the index is already proved valid and a violated proof is a programmer defect.

### The iteration ownership matrix

For an owned `Vec<T>` named `values`:

| Form | Collection access | Item type (conceptually) | After loop |
|---|---|---|---|
| `for item in &values` | shared borrow | `&T` | vector remains usable |
| `for item in &mut values` | exclusive borrow | `&mut T` | vector remains usable |
| `for item in values` | consume | `T` | binding moved |

`iter`, `iter_mut`, and `into_iter` make the same intent explicit. Exact method resolution can depend on receiver type; predict from the type being iterated, not from a slogan that `into_iter` always consumes an allocation.

### Iterator pipelines are lazy plans

Most adapters create a new iterator and do no work until consumed by `collect`, `count`, `find`, a loop, or another terminal operation.

```rust
pub fn active_titles<'a>(tasks: &'a [Task]) -> impl Iterator<Item = &'a str> + 'a {
    tasks
        .iter()
        .filter(|task| task.status() != Status::Done)
        .map(Task::title)
}
```

This pipeline borrows tasks and yields borrowed titles. It does not allocate a result collection. Returning an iterator can be useful, but Course 1 keeps signatures straightforward; Course 4 develops iterator algebra and closure traits more deeply.

A loop may be clearer when several mutable accumulators, early exits, or error branches interact. “Iterator” is not a quality badge.

### HashMap and determinism

A `HashMap` does not promise a stable iteration order suitable for public output or golden tests. If deterministic output matters, sort extracted keys/entries or use a data structure with an ordering contract appropriate to the product.

The entry API centralizes insert-or-update behavior:

```rust
pub fn frequencies(words: &[&str]) -> std::collections::HashMap<String, usize> {
    let mut counts = std::collections::HashMap::new();
    for &word in words {
        *counts.entry(word.to_owned()).or_insert(0) += 1;
    }
    counts
}
```

This allocates owned keys because the returned map must outlive the borrowed slice. A borrowed-key map would need a lifetime tied to input storage and might not match retention needs.

### Mutation during traversal

A common conflict occurs when code iterates and tries to structurally modify the same collection. Repairs include:

- mutate elements in place with `iter_mut`;
- use `retain` for filtering;
- collect identifiers during a read phase, then mutate in a second phase;
- use a collection operation such as `swap`, `split_at_mut`, or `drain` that encodes safety;
- redesign the data structure.

Do not hold a reference into a vector across a `push` and then try to convince the compiler the reference is fine.

### Worked derivation: deterministic board statistics

```rust
#[derive(Debug, Default, PartialEq, Eq)]
pub struct Stats {
    pub todo: usize,
    pub doing: usize,
    pub done: usize,
}

pub fn stats(tasks: &[Task]) -> Stats {
    let mut result = Stats::default();
    for task in tasks {
        match task.status() {
            Status::Todo => result.todo += 1,
            Status::Doing => result.doing += 1,
            Status::Done => result.done += 1,
        }
    }
    result
}
```

The loop is intentionally plain: one pass, no allocation, exhaustive state handling. A fold could also be correct; the chosen form makes the state update easy to audit at this stage.

### Try without the scaffold

Implement a search that returns tasks whose titles contain an ASCII-case-insensitive query, sorted by ID. State where allocations occur. Then implement a borrowed iterator version and compare retention and API complexity.

### Misconception clinic

- **“HashMap order is random but usually stable.”** The contract is what matters; do not publish unspecified order.
- **“Iterator chains are faster.”** Performance depends on operations and optimization; choose first from semantics and clarity.
- **“Indexing is idiomatic because Rust bounds-checks.”** Bounds checking turns an invalid index into panic; it does not make absence disappear.
- **“A closure is only anonymous syntax.”** Capture mode and callable trait affect ownership; later courses deepen that model.

### A vector owns a variable-length sequence

`Vec<T>` owns zero or more values of one element type. Its logical state includes at least:

- a pointer to an allocation, or a special non-allocating representation when capacity is zero;
- a length: the number of initialized elements;
- a capacity: the number of elements that fit before another allocation is required.

The implementation details are not an API promise, but the length/capacity model explains observable behavior.

```rust
let mut values = Vec::with_capacity(4);
assert_eq!(values.len(), 0);
assert!(values.capacity() >= 4);

values.push(10);
values.push(20);
assert_eq!(values.len(), 2);
```

Capacity is not the number of meaningful values. Reading an element at an index greater than or equal to `len()` is invalid even when the allocation has spare capacity.

### Growth may move the allocation

When `push` exceeds capacity, the vector must obtain enough storage for a larger sequence and relocate its elements. Therefore a reference into the vector cannot coexist with a mutation that may grow it:

```rust,compile_fail
let mut names = vec![String::from("Ada")];
let first = &names[0];
names.push(String::from("Grace"));
println!("{first}");
```

The rejection is not arbitrary. If growth moves the allocation, `first` would point to obsolete storage. The compiler does not need to predict whether this particular `push` will reallocate; the method requires mutable access to the vector, which conflicts with the active shared reference.

Do not “repair” this by assuming reserved capacity makes the reference safe. The borrow rule remains at the API level. Reserve capacity for performance, not to bypass aliasing rules.

### Length-changing operations and element identity

Several operations change where an element appears:

- `push` appends and may reallocate;
- `insert` shifts later elements and may reallocate;
- `remove` shifts later elements left and returns the removed value;
- `swap_remove` replaces the removed slot with the final element and avoids shifting, but changes order;
- `retain` keeps elements satisfying a predicate and preserves relative order;
- `truncate` drops elements beyond a new length;
- `clear` drops all elements but may retain capacity.

Choose based on the contract. `swap_remove` is not a “faster remove” when stable order is externally visible.

```rust
let mut queue = vec!["first", "second", "third"];
let removed = queue.remove(1);
assert_eq!(removed, "second");
assert_eq!(queue, ["first", "third"]);
```

When `T` is not `Copy`, `remove` transfers ownership of the element to the caller. The remaining vector continues to own the retained elements.

### Access: proof, checked failure, or explicit panic

Indexing expresses a strong claim:

```rust
let value = values[2];
```

The program asserts that index 2 exists. Violation causes a panic. Use indexing only when the invariant proving the index is local and obvious, or when panic is the intentional boundary.

Checked access exposes uncertainty:

```rust
fn third(values: &[i32]) -> Option<i32> {
    values.get(2).copied()
}
```

Pattern access often communicates structure more directly:

```rust
fn endpoints(values: &[i32]) -> Option<(i32, i32)> {
    let [first, .., last] = values else {
        return None;
    };
    Some((*first, *last))
}
```

The last version states the required shape rather than manipulating numeric indices.

### Ownership of elements

A vector owns its elements. Traversal decides what access leaves the vector:

```rust
let words = vec![String::from("red"), String::from("blue")];

for word in &words {
    // word: &String
    println!("{word}");
}

assert_eq!(words.len(), 2);
```

Consuming traversal transfers each element:

```rust
let words = vec![String::from("red"), String::from("blue")];

for word in words {
    // word: String
    println!("{word}");
}

// words is no longer usable
```

Moving elements out one at a time by indexing is generally unavailable because it would leave an uninitialized hole. Operations such as `remove`, `pop`, `drain`, or consuming iteration preserve the collection's validity while transferring elements.

### Preallocation is an evidence-based optimization

Use `Vec::with_capacity(n)` when a credible upper bound or exact count is already known. Avoid speculative capacity arithmetic that complicates code without measured value.

A two-pass design may count first and allocate exactly, but it also traverses twice. An approximate reserve may reduce reallocations while retaining one pass. The correct choice depends on input cost and evidence.

### API design

Prefer slices when the function needs a borrowed sequence but not vector-specific growth:

```rust
fn average(values: &[f64]) -> Option<f64> {
    if values.is_empty() {
        return None;
    }
    Some(values.iter().sum::<f64>() / values.len() as f64)
}
```

Accept `&mut Vec<T>` only when the function needs length-changing vector operations. Accept `&mut [T]` for in-place reordering or element mutation without growth. Take `Vec<T>` by value when the operation consumes or assumes ownership of the sequence.

### A slice is a borrowed contiguous region

`&[T]` carries a pointer to the first element and a length. It does not own the elements. It can refer to an array, a vector, another slice, or another contiguous owner.

```rust
fn sum(values: &[i64]) -> i64 {
    values.iter().sum()
}

let array = [1, 2, 3];
let vector = vec![4, 5, 6];
assert_eq!(sum(&array), 6);
assert_eq!(sum(&vector), 15);
```

A slice parameter removes irrelevant ownership choices from the API. The function above needs a sequence view, not the ability to grow a vector or own an array.

### Slicing is a runtime-checked boundary

A range index such as `&values[2..5]` checks that both boundaries are valid and ordered. Invalid boundaries panic. `get` expresses uncertainty:

```rust
fn middle_three(values: &[i32]) -> Option<&[i32]> {
    values.get(2..5)
}
```

Returning a subslice is allocation-free. Its lifetime is tied to the input owner. The caller cannot retain it after the owner is destroyed or mutate the owner in a conflicting way while the slice remains active.

### Split disjoint mutable access explicitly

Two independently written mutable indexes appear suspicious to the borrow checker because the expressions could alias:

```rust,compile_fail
fn swap_bad(values: &mut [i32], left: usize, right: usize) {
    let a = &mut values[left];
    let b = &mut values[right];
    std::mem::swap(a, b);
}
```

The standard library provides operations that prove disjointness. For custom logic, `split_at_mut` creates two non-overlapping mutable slices:

```rust
fn two_mut<T>(values: &mut [T], left: usize, right: usize) -> Option<(&mut T, &mut T)> {
    if left == right || left >= values.len() || right >= values.len() {
        return None;
    }

    let (low, high, flipped) = if left < right {
        (left, right, false)
    } else {
        (right, left, true)
    };

    let (before_high, from_high) = values.split_at_mut(high);
    let low_ref = &mut before_high[low];
    let high_ref = &mut from_high[0];
    if flipped {
        Some((high_ref, low_ref))
    } else {
        Some((low_ref, high_ref))
    }
}
```

The code is longer because its contract is stronger: it returns two exclusive references and must prove they differ.

For ordinary swapping, use the existing `slice::swap`; the example is for reasoning about disjoint mutable regions.

### Prefer structural iteration over manual indexes

Index loops are justified when the index itself is part of the algorithm. Otherwise they add an unnecessary failure surface:

```rust
fn normalize(values: &mut [i32]) {
    for value in values {
        *value = (*value).clamp(0, 100);
    }
}
```

The traversal cannot go out of bounds. The item type `&mut i32` makes mutation explicit.

When positions matter, `enumerate` keeps access checked:

```rust
fn first_negative(values: &[i32]) -> Option<usize> {
    values
        .iter()
        .enumerate()
        .find_map(|(index, value)| (*value < 0).then_some(index))
}
```

### In-place filtering

`retain` is usually preferable to repeatedly removing inside an index loop:

```rust
fn retain_valid_titles(titles: &mut Vec<String>) {
    titles.retain(|title| !title.trim().is_empty());
}
```

The predicate receives a shared reference because deciding whether to retain an item should not replace it. `retain_mut` exists when the decision process legitimately mutates each retained element.

Removing by repeated `Vec::remove` inside a forward loop can both skip elements and produce quadratic shifting cost.

### Sorting and contract design

Sorting mutates order. That is observable state and must be justified.

```rust
records.sort_by_key(|record| record.id());
```

`sort_by_key` is stable: equal keys retain relative order. `sort_unstable_by_key` may be faster and use less memory but does not preserve equal-key order. Use unstable sorting only when tie order is irrelevant or separately defined.

Do not use a comparator that violates ordering laws. A comparator must be consistent and transitive. For floating-point values, ordinary `partial_cmp` can return `None` for NaN; choose a documented policy such as `total_cmp` when a total order is required.

### Windows and chunks

Slice views can express local algorithms without copying:

```rust
fn is_non_decreasing(values: &[i32]) -> bool {
    values.windows(2).all(|pair| pair[0] <= pair[1])
}
```

Each window here has known length 2 because `windows(2)` guarantees it. Indexing inside the window is therefore supported by a local invariant.

`chunks(n)` yields the final shorter chunk if the length is not divisible by `n`. `chunks_exact(n)` separates complete chunks from the remainder. The choice is part of the input contract.

### Borrow duration and mutation

A borrow generally ends after its last use, not necessarily at the closing brace:

```rust
let mut values = vec![1, 2, 3];
let first = values.first();
assert_eq!(first, Some(&1));
// `first` is no longer used.
values.push(4);
```

This non-lexical behavior is not permission to ignore borrow ranges. Read diagnostics in terms of the last use that keeps a borrow active.

### A map represents keyed association

`HashMap<K, V>` is appropriate when the problem's primary operation is finding a value by a key. It is not automatically better than a vector. A small ordered set that is always listed and rarely searched may be simpler as `Vec<T>`.

Keys require equality and hashing behavior. The map relies on the rule that equal keys produce equal hashes. Standard types such as integers and strings already satisfy the contract.

```rust
use std::collections::HashMap;

let mut owners = HashMap::new();
owners.insert(17_u64, String::from("Ada"));
assert_eq!(owners.get(&17).map(String::as_str), Some("Ada"));
```

Insertion transfers ownership of non-`Copy` keys and values unless references are stored deliberately.

### Borrowed lookup avoids temporary ownership

A `HashMap<String, V>` can usually be queried with `&str`:

```rust
let mut counts: HashMap<String, usize> = HashMap::new();
counts.insert(String::from("rust"), 3);
assert_eq!(counts.get("rust"), Some(&3));
```

The standard library's borrowed-key support lets the lookup use the logical text without allocating a new `String`. Do not write `counts.get(&String::from("rust"))`; that creates temporary ownership for no value.

### Distinguish replacement from first insertion

`insert` returns the previous value:

```rust
let old = counts.insert(String::from("rust"), 4);
assert_eq!(old, Some(3));
```

Ignoring that return value is a policy decision. If duplicate keys indicate corrupted input, silently replacing is wrong. If “latest value wins” is the contract, replacement may be correct.

The type cannot choose the duplicate-key policy for you.

### The entry API performs one keyed decision

Frequency counting is the canonical example:

```rust
for word in ["red", "blue", "red"] {
    *counts.entry(word.to_owned()).or_insert(0) += 1;
}
```

`entry` represents either an occupied or vacant position found by one lookup. It supports policies that differ by case:

```rust
use std::collections::hash_map::Entry;

match owners.entry(17) {
    Entry::Vacant(slot) => {
        slot.insert(String::from("Ada"));
    }
    Entry::Occupied(existing) => {
        eprintln!("ID already owned by {}", existing.get());
    }
}
```

Use explicit matching when duplicate handling is important enough to name. Use `or_insert`, `or_insert_with`, or `and_modify` for compact, clear update policies.

### Mutation through a map borrow

`get_mut` grants exclusive access to one value while the map remains borrowed:

```rust
if let Some(count) = counts.get_mut("rust") {
    *count += 1;
}
```

While that mutable reference is active, operations requiring another borrow of the map may be rejected. Keep the reference's use narrow.

Do not remove and reinsert merely to mutate a value. That transfers ownership and may obscure duplicate or missing-key behavior.

### Iteration order is not a public order

The standard `HashMap` does not promise a stable iteration order. The order can differ across runs, compiler versions, insertion histories, or hash seeds.

This is invalid as a deterministic output contract:

```rust
for (status, count) in &counts {
    println!("{status}: {count}");
}
```

It is valid only when order is explicitly irrelevant. For stable output, sort keys or render in a domain-defined order:

```rust
for status in ["todo", "doing", "done"] {
    let count = counts.get(status).copied().unwrap_or(0);
    println!("{status}: {count}");
}
```

In capstoneion library code, prefer an explicit match or a method rather than routine `unwrap`; the example uses `unwrap_or`, which supplies a normal default rather than asserting success.

Alternatively:

```rust
let mut rows: Vec<_> = counts.iter().collect();
rows.sort_unstable_by_key(|(key, _)| key.as_str());
```

The allocation and sort are the price of converting an unordered representation into an ordered report.

### Choosing between `Vec` and `HashMap`

Ask what must be authoritative:

| Requirement | Likely representation |
|---|---|
| preserve insertion/ID order and scan all values | `Vec<T>` |
| frequent lookup by unique key | `HashMap<K, V>` |
| both stable order and fast lookup | two coordinated structures, or a later ecosystem type |
| very small set with simple behavior | often `Vec<T>` |

Maintaining both a vector and a map introduces synchronization invariants. That can be justified, but it is not free. The capstone uses a vector because deterministic listing and conceptual simplicity matter more than optimizing a small local board.

### Hash maps and domain invariants

A map can encode uniqueness by key, but it does not automatically validate values or allocation metadata. A persisted snapshot still needs checks for invalid keys, missing metadata, and contradictory domain state.

Never infer “map insertion succeeded” to mean “the record was valid.” It means only that the data structure accepted a key/value pair.

### An iterator is a stateful traversal

An iterator does not normally contain the final output. It contains the state required to produce the next item. Most adapters construct another iterator and do no traversal until a consuming operation requests items.

```rust
let values = [1, 2, 3, 4];
let evens = values.iter().filter(|value| **value % 2 == 0);
// No result collection has been built yet.
assert_eq!(evens.count(), 2);
```

`count` consumes the iterator. After consumption, that iterator binding cannot be reused unless the iterator itself is cloned and supports meaningful cloning.

### The three traversal modes

For `Vec<T>` the central matrix is:

| Expression | Iterator item | Effect on vector |
|---|---|---|
| `values.iter()` or `&values` | `&T` | shared borrow |
| `values.iter_mut()` or `&mut values` | `&mut T` | exclusive borrow |
| `values.into_iter()` or `values` | `T` | consumes vector |

The same conceptual distinction applies across many collections, though exact `IntoIterator` implementations differ.

```rust
let mut labels = vec![String::from("a"), String::from("b")];

for label in &mut labels {
    label.make_ascii_uppercase();
}

let lengths: Vec<usize> = labels.iter().map(String::len).collect();
assert_eq!(lengths, [1, 1]);

let owned: Vec<String> = labels.into_iter().collect();
```

State the item type before writing an adapter closure. Many confusing dereference patterns disappear when the input is explicit.

### Adapters transform traversal, not necessarily data

Common adapters include:

- `map`: transform every item;
- `filter`: retain items satisfying a predicate;
- `filter_map`: combine filtering and optional transformation;
- `enumerate`: pair items with positions;
- `take` and `skip`: constrain traversal;
- `chain`: traverse one iterator then another;
- `zip`: traverse two iterators together until either ends;
- `flat_map` and `flatten`: traverse nested sources;
- `inspect`: observe items for diagnostics without changing them.

A long adapter chain is not automatically better than a loop. Each stage should correspond to a comprehensible operation.

### Consumers answer different questions

Consumers include:

- `collect` to build a collection;
- `sum` and `product` to aggregate;
- `count` to measure items;
- `find` to stop at the first match;
- `position` to find the first matching index;
- `any` and `all` to short-circuit predicates;
- `fold` to carry an accumulator;
- `for_each` to perform an action for every item.

Use a short-circuiting consumer when the answer does not require visiting all elements:

```rust
fn contains_blank(values: &[String]) -> bool {
    values.iter().any(|value| value.trim().is_empty())
}
```

`any` stops once it finds a blank. A `filter(...).count() > 0` pipeline communicates less and may traverse more.

### `collect` needs an output type

The iterator knows its item type but not which compatible collection you want. Provide type context:

```rust
let squares: Vec<i32> = (1..=4).map(|value| value * value).collect();
```

Turbofish is useful when the binding does not provide enough context:

```rust
let squares = (1..=4).map(|value| value * value).collect::<Vec<_>>();
```

Avoid collecting merely because a later method is familiar. Many operations can remain lazy or stream directly into a fold, writer, or search.

### Fallible iteration

An iterator of `Result<T, E>` can be collected into `Result<Vec<T>, E>`:

```rust
fn parse_numbers(inputs: &[&str]) -> Result<Vec<u64>, std::num::ParseIntError> {
    inputs.iter().map(|text| text.parse::<u64>()).collect()
}
```

The operation stops at the first error. This is a powerful consequence of `collect` and `FromIterator`, not magic syntax. The output type determines how items are combined.

Use it only when first-error semantics are correct. If the contract requires every invalid record to be reported, a separate accumulation design is needed.

### Borrowed results from iterator searches

`find` over `slice.iter()` returns a reference because the items are references:

```rust
fn find_long(values: &[String]) -> Option<&String> {
    values.iter().find(|value| value.len() > 20)
}
```

The closure receives an additional reference to the item in many adapter signatures, which can make types appear nested. Method-call autoderef often hides this, but ownership reasoning should not.

A public API may prefer `Option<&str>` to avoid exposing the owned string type:

```rust
fn find_long_text(values: &[String]) -> Option<&str> {
    values
        .iter()
        .find(|value| value.len() > 20)
        .map(String::as_str)
}
```

### Iterator invalidation and mutation

An iterator borrows or owns its source for the duration of traversal. Mutating collection length inside a borrowed iteration is rejected:

```rust,compile_fail
let mut values = vec![1, 2, 3];
for value in &values {
    if *value == 2 {
        values.push(4);
    }
}
```

Use a two-phase algorithm, `retain`, `drain`, or ownership-consuming transformation depending on the required behavior.

### A closure can carry environment access

A free function receives only its explicit parameters. A closure may also capture names from its surrounding scope:

```rust
let threshold = 10;
let above = |value: &i32| *value > threshold;
assert!([4, 11, 8].iter().any(above));
```

The closure needs read access to `threshold`, so it captures a shared borrow. Its effective value contains both executable behavior and the environment required by that behavior.

This is why a closure is not merely “an anonymous function.” Capture affects ownership, lifetime, mutability, and which call trait the closure implements.

### Capture is inferred from use

#### Shared capture

```rust
let prefix = String::from("task:");
let render = |title: &str| format!("{prefix} {title}");
println!("{}", render("compile"));
println!("{prefix}");
```

Reading `prefix` permits shared capture, so the outer binding remains usable while borrow rules permit.

#### Mutable capture

```rust
let mut calls = 0_u64;
let mut record_call = || {
    calls += 1;
};
record_call();
record_call();
assert_eq!(calls, 2);
```

The closure mutates captured state and therefore requires mutable access to itself when called. The binding is declared `mut` because calling changes the closure's captured environment.

#### Ownership capture

```rust
let message = String::from("finished");
let consume = || drop(message);
consume();
// `message` was moved into and then out of the closure.
```

Using a captured value by ownership may make the closure callable only once.

### `move` changes capture, not call frequency by itself

A `move` closure takes ownership of captured variables:

```rust
let label = String::from("owned");
let show = move || println!("{label}");
show();
show();
```

This closure can still be called multiple times because it only borrows the owned `label` when executing. `move` does not automatically mean `FnOnce`; the closure body determines whether captured values are consumed.

`move` is common when the closure must outlive the current stack frame, as in later concurrency and async courses. This module focuses only on the ownership consequence.

### The call-trait hierarchy

Closure capabilities are described by three traits:

- `Fn`: can be called through shared access; it does not mutate or consume captured state during a call;
- `FnMut`: can be called through mutable access; it may mutate captured state;
- `FnOnce`: can be called with ownership of the closure; it may consume captured values.

A closure that implements `Fn` also satisfies requirements for `FnMut` and `FnOnce`. A closure that only implements `FnOnce` cannot satisfy a requirement that promises repeated calls.

You do not need advanced generic closure design yet, but you must understand why standard-library algorithms request different capabilities.

```rust
fn apply_twice<F>(mut operation: F)
where
    F: FnMut(),
{
    operation();
    operation();
}
```

`FnMut` is sufficient because the function promises two calls and allows captured mutation. Requiring only `FnOnce` would be too weak to justify the second call. Requiring `Fn` would unnecessarily reject stateful operations.

### Iterator predicates often receive references

Consider:

```rust
let values = [1, 2, 3];
let even_count = values.iter().filter(|value| **value % 2 == 0).count();
```

`iter()` yields `&i32`. `filter` must inspect an item without consuming it because a rejected item may simply be skipped, so its predicate receives a reference to the iterator item: `&&i32` in this case. Pattern syntax can make the expectation clearer:

```rust
let even_count = values.iter().filter(|&&value| value % 2 == 0).count();
```

Do not memorize dereference counts. Derive them from the iterator item and adapter signature.

### Closures in sorting and lookup

Key-extraction closures borrow elements:

```rust
records.sort_by_key(|record| record.id());
```

If a key is owned and expensive to clone, do not return an owned clone merely to satisfy the closure. Prefer a cheap `Copy` key, or use a comparator that borrows values:

```rust
records.sort_by(|left, right| left.title().cmp(right.title()));
```

The choice affects allocation and may affect sort performance because key extraction can be repeated. Later performance work should measure rather than guess.

### Returning closures is an abstraction boundary

A function can return `impl Fn(...)` when the concrete closure type should remain hidden:

```rust
fn greater_than(limit: i32) -> impl Fn(i32) -> bool {
    move |value| value > limit
}
```

The `move` capture gives the returned closure ownership of `limit`; for `i32` this is also a copy. Returning a closure that borrows a local variable would be invalid because the local would be destroyed.

Keep this use narrow in Course 1. Trait objects and complex callback architecture belong to later courses.

### Correctness includes resource behavior

A program can return the right value while violating important engineering contracts:

- quadratic time where a linear pass was available;
- unbounded allocation where streaming was expected;
- unstable output that breaks reproducible tests;
- unnecessary cloning of large values;
- mutation before validation, leaving partial state on failure.

Course 1 does not require advanced optimization, but it does require a cost vocabulary strong enough to reject structurally poor designs.

### Count passes and nested work

A single scan over `n` elements is `O(n)`. A scan that performs another full scan for every element is `O(n²)`.

```rust
fn contains_duplicate_slow(values: &[u64]) -> bool {
    for (index, value) in values.iter().enumerate() {
        if values[index + 1..].contains(value) {
            return true;
        }
    }
    false
}
```

The code is correct and allocation-free, but worst-case work is quadratic. A hash set can provide expected linear behavior at the cost of allocation and hashing:

```rust
use std::collections::HashSet;

fn contains_duplicate(values: &[u64]) -> bool {
    let mut seen = HashSet::with_capacity(values.len());
    values.iter().any(|value| !seen.insert(*value))
}
```

Neither implementation is universally superior. For tiny inputs or constrained environments, the simple scan may be appropriate. State the trade-off.

### Distinguish transient and retained allocation

This search allocates a lowercase copy of every title during comparison:

```rust
fn contains_ascii_case_insensitive(title: &str, query: &str) -> bool {
    title.to_ascii_lowercase().contains(&query.to_ascii_lowercase())
}
```

The query is redundantly normalized for every title if called inside a loop. Hoist work that depends only on the query. The title allocation remains and may be acceptable for a small course application, but it must be recognized.

Optimization starts with identifying where ownership causes allocation. It does not start with unsafe code.

### Avoid collect-then-process without a reason

```rust
let selected: Vec<_> = tasks.iter().filter(|task| task.is_open()).collect();
let count = selected.len();
```

If only the count is required, use `.count()` and allocate nothing. If the selected values are rendered twice, stored, sorted, or passed to an API requiring a slice, collection may be justified.

Every `collect` should answer: which later requirement needs retained random access or ownership?

### Mutation strategy and failure atomicity

A method that validates after mutation may leave state changed on error:

```rust
fn rename_bad(task: &mut Task, title: String) -> Result<(), TitleError> {
    task.title = title;
    validate(&task.title)
}
```

Validate the candidate first, then commit:

```rust
fn rename(task: &mut Task, title: String) -> Result<(), TitleError> {
    validate(&title)?;
    task.title = title;
    Ok(())
}
```

This local transaction pattern applies to collection operations: parse and validate an incoming record before pushing it; build a restored board before replacing an existing one; save successfully before reporting mutation success.

### Determinism is a deliberate conversion

Internal structures may be unordered. External snapshots and command output should usually be stable. Convert at the boundary:

1. gather borrowed rows;
2. sort by the documented key;
3. render in that order.

Do not sort the authoritative collection on every read unless changing its order is harmless. A temporary vector of references can provide deterministic reporting without mutating domain state.

### Loops versus iterator chains

Choose the form that makes state and early exits visible.

A loop is often clearer when:

- multiple accumulators change together;
- several error cases need distinct context;
- control flow uses `continue` or early return;
- mutation order is central;
- a dense closure would hide item types.

An iterator pipeline is often clearer when:

- the operation is a recognizable sequence of selection and transformation;
- the consumer states the question (`any`, `all`, `find`, `sum`);
- ownership remains straightforward;
- laziness or short-circuiting is useful.

The course rejects style dogma in both directions.

### Complexity ledger

For a capstone operation, record:

| Operation | Traversal | Allocation | Mutation | Order |
|---|---|---|---|---|
| find by ID in `Vec<Task>` | worst-case `O(n)` | none | none | preserves |
| add task | amortized `O(1)` push | title already owned; vector may grow | append | ID order |
| remove by position | `O(n)` search + shift | none | length/order | preserves relative order |
| list sorted copy of refs | `O(n log n)` | `O(n)` references | none | explicit ID order |
| status counts | `O(n)` | none | none | explicit rendering order |

A small local board can legitimately use linear lookup. Documenting the ledger prevents accidental claims of constant-time behavior and creates a clear trigger for later redesign.

### Review method

Before accepting a collection algorithm, answer:

1. What is the authoritative representation?
2. Which invariants hold before and after the operation?
3. What is moved, borrowed, cloned, or allocated?
4. Can an error leave partial mutation?
5. What is the worst-case number of element visits?
6. Is output ordering explicit?
7. Are tests checking behavior rather than incidental implementation?

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For use Vec, slices, and HashMap with explicit length, capacity, invalidation, lookup, and ordering assumptions, construct one positive and one causal negative example. Mark the first decisive fact in the **collection and iteration trace** and state which evidence could falsify the claim.

2. **Outcome 2.** For derive item ownership for iter, iter_mut, into_iter, and for-loop desugaring contexts, construct one positive and one causal negative example. Mark the first decisive fact in the **collection and iteration trace** and state which evidence could falsify the claim.

3. **Outcome 3.** For use closures and core iterator adapters while keeping transformations readable and cost-aware, construct one positive and one causal negative example. Mark the first decisive fact in the **collection and iteration trace** and state which evidence could falsify the claim.

4. **Outcome 4.** For avoid mutation-during-iteration hazards by staging keys, splitting phases, or selecting a different operation, construct one positive and one causal negative example. Mark the first decisive fact in the **collection and iteration trace** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

The course capstone is **Taskboard**, a persistent command-line task board. Implement board operations, deterministic listing, filtering, search, and statistics. For each traversal, state whether it borrows, mutates, or consumes the collection. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-06-in-memory-board/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 7 when you can:

- answer the module question—“Does an algorithm borrow, mutate, or consume a collection, and what complexity and invalidation consequences follow?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Use Vec, slices, and HashMap with explicit length, capacity, invalidation, lookup, and ordering assumptions;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [The Rust Book: Collections](https://doc.rust-lang.org/book/ch08-00-common-collections.html)
- [The Rust Book: Closures and Iterators](https://doc.rust-lang.org/book/ch13-00-functional-features.html)
- [Iterator documentation](https://doc.rust-lang.org/std/iter/trait.Iterator.html)

[← Module 5](../../../01-rust-foundations/course-book/module-05-structs-enums-methods-and-pattern-matching/index.md) · [one-hundred-module map](../../../COURSE_MAP.md) · [Module 7 →](../../../01-rust-foundations/course-book/module-07-errors-parsing-files-and-persistence/index.md)

## Continue

Continue to [Module 7 — Errors, Parsing, Files, and Persistence](../module-07-errors-parsing-files-and-persistence/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
