# Reasoned Solutions — Module 06: Collections, Iterators, and Closures

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-06-in-memory-board/README.md) · [Taskboard guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 6: Collections, Iterators, and Closures**. Compare the reasoning against this question: *Does an algorithm borrow, mutate, or consume a collection, and what complexity and invalidation consequences follow?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `01-into-iter-consumes-vector.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** owned for-loop consumes the vector.
- **Causal explanation:** The compiler rejects the specimen because owned for-loop consumes the vector.
- **Principled repair:** Iterate over `&values` or `values.iter()` when the vector is needed afterward; consume it only when transfer is intended.
- **Weak repair to reject:** Do not clone the vector merely to keep using the original.

### 2. `02-mutate-while-shared-iter.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** active shared iterator overlaps mutation.
- **Causal explanation:** The compiler rejects the specimen because active shared iterator overlaps mutation.
- **Principled repair:** Finish the shared traversal before mutation, or use a mutation-oriented iterator that preserves structure.
- **Weak repair to reject:** Do not hide the conflict inside `RefCell` without a shared-mutation requirement.

### 3. `03-collect-needs-type.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** collect target type is ambiguous.
- **Causal explanation:** The compiler rejects the specimen because collect target type is ambiguous.
- **Principled repair:** State the collection target with a binding annotation or `collect::<Target>()`.
- **Weak repair to reject:** Do not collect into an arbitrary intermediate collection and convert it afterward.

### 4. `04-index-can-panic.rs`

- **Outcome:** `run-fail`
- **Governing rule:** compiles then panics: indexing is not recoverable bounds handling.
- **Causal explanation:** The specimen type-checks, then its assertion or reachable operation fails because compiles then panics: indexing is not recoverable bounds handling.
- **Principled repair:** Use `get` and handle `None` when out-of-range access is recoverable.
- **Weak repair to reject:** Do not pad the collection or change the index only to avoid the demonstrated panic.

### 5. `05-hash-order-is-not-contract.rs`

- **Outcome:** `manual-review`
- **Governing rule:** compiles but assertion is unstable: hash iteration order is unspecified.
- **Causal explanation:** The specimen type-checks, but design review must reject the behavior because compiles but assertion is unstable: hash iteration order is unspecified.
- **Principled repair:** Sort keys or rendered rows before asserting or publishing deterministic output.
- **Weak repair to reject:** Do not bless one observed hash-map order as a contract.

### 6. `06-filter-borrows-source.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** retained references keep source borrowed across push.
- **Causal explanation:** The compiler rejects the specimen because retained references keep source borrowed across push.
- **Principled repair:** End the retained-reference collection before mutating the source, or store owned durable results when they must survive mutation.
- **Weak repair to reject:** Do not mutate through unsafe pointers while references remain live.

## Exercise reasoning and worked answers
These are reference solutions, not the only acceptable implementations. Compare contracts, ownership, and cost before comparing syntax.

### 1. Safe endpoints

```rust
fn endpoints<T>(values: &[T]) -> Option<(&T, &T)> {
    let first = values.first()?;
    let last = values.last()?;
    Some((first, last))
}
```

A one-element slice returns two shared references to the same element. This is legal because shared references may alias. An empty slice returns `None`.

### 2. Remove the first match

```rust
fn remove_first<T, F>(values: &mut Vec<T>, mut predicate: F) -> Option<T>
where
    F: FnMut(&T) -> bool,
{
    let index = values.iter().position(&mut predicate)?;
    Some(values.remove(index))
}
```

The search is `O(n)` and ordered removal shifts later elements, also `O(n)`. The function transfers ownership of the removed element. `FnMut` permits stateful predicates and satisfies the single-pass use.

An explicit closure is also clear:

```rust
let index = values.iter().position(|value| predicate(value))?;
```

### 3. Deduplicate preserving first occurrence

```rust
use std::collections::HashSet;

fn unique_first(values: Vec<String>) -> Vec<String> {
    let mut seen = HashSet::with_capacity(values.len());
    let mut output = Vec::with_capacity(values.len());

    for value in values {
        if seen.insert(value.clone()) {
            output.push(value);
        }
    }
    output
}
```

This duplicates each first-seen string because both the set and output own text. That clone is semantically required by this representation. An alternative set of borrowed strings cannot outlive temporary ownership manipulations without a different design. If returning values in unspecified order were acceptable, the set itself could own the strings and later be consumed, but first-occurrence order would be lost.

For a large system, an index set or interned representation might avoid duplication; that belongs beyond the standard-library boundary of this course.

### 4. Stable status counts

```rust
use std::collections::HashMap;

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
enum Status {
    Todo,
    Doing,
    Done,
}

fn counts(statuses: &[Status]) -> HashMap<Status, usize> {
    let mut result = HashMap::new();
    for status in statuses {
        *result.entry(*status).or_insert(0) += 1;
    }
    result
}

fn render(counts: &HashMap<Status, usize>) -> Vec<(Status, usize)> {
    [Status::Todo, Status::Doing, Status::Done]
        .into_iter()
        .map(|status| (status, counts.get(&status).copied().unwrap_or(0)))
        .collect()
}
```

The map is a counting implementation detail. Domain order is a separate explicit decision.

### 5. Normalize in place

```rust
fn trim_all(values: &mut [String]) {
    for value in values {
        let trimmed = value.trim();
        if trimmed.len() != value.len() {
            *value = trimmed.to_owned();
        }
    }
}

fn normalize(values: &mut Vec<String>) {
    trim_all(values);
    values.retain(|value| !value.is_empty());
}
```

The first function needs only mutable element access, so it accepts `&mut [String]`. The second changes length and therefore requires `&mut Vec<String>`.

The implementation allocates a replacement only when trimming changes the string. More elaborate in-place whitespace removal is not warranted here.

### 6. Iterator item matrix

For `Vec<String>`:

| Expression | Item | Source after traversal |
|---|---|---|
| `values.iter()` | `&String` | usable after borrow ends |
| `values.iter_mut()` | `&mut String` | usable after exclusive borrow ends |
| `values.into_iter()` | `String` | moved |
| `&values` in `for` | `&String` | usable after borrow ends |
| `&mut values` in `for` | `&mut String` | usable after borrow ends |
| `values` in `for` | `String` | moved |

### 7. Parse strategies

First-error semantics:

```rust
fn parse_all(
    inputs: &[&str],
) -> Result<Vec<u64>, std::num::ParseIntError> {
    inputs.iter().map(|text| text.parse::<u64>()).collect()
}
```

All-error semantics need a result type that carries both valid values and invalid positions:

```rust
#[derive(Debug, PartialEq, Eq)]
struct ParseReport<'a> {
    valid: Vec<u64>,
    invalid: Vec<(usize, &'a str)>,
}

fn parse_report<'a>(inputs: &'a [&'a str]) -> ParseReport<'a> {
    let mut report = ParseReport {
        valid: Vec::new(),
        invalid: Vec::new(),
    };

    for (index, text) in inputs.iter().copied().enumerate() {
        match text.parse::<u64>() {
            Ok(value) => report.valid.push(value),
            Err(_) => report.invalid.push((index, text)),
        }
    }
    report
}
```

The second design intentionally discards detailed parse-error values and retains text/index context. That is a contract choice, not a generic improvement.

### 8. Short-circuit validation

```rust
fn all_valid(titles: &[String], checks: &mut usize) -> bool {
    titles.iter().all(|title| {
        *checks += 1;
        !title.trim().is_empty() && title.len() <= 120
    })
}
```

A test can place an invalid title second and assert that later titles are not checked. The mutable counter makes the closure `FnMut`.

### 9. Closure capability

```rust
let label = String::from("task");
let read = || label.len();               // `Fn`

let mut count = 0;
let mut increment = || count += 1;       // `FnMut`

let values = vec![1, 2, 3];
let consume = || drop(values);           // only `FnOnce`
```

The strongest capability is determined by the closure body, not by whether the capture was syntactically marked `move`.

### 10. Two-phase removal

Direct `retain`:

```rust
fn remove_matches(tasks: &mut Vec<String>, query: &str) {
    tasks.retain(|task| !task.contains(query));
}
```

Index collection:

```rust
fn remove_matches_by_index(tasks: &mut Vec<String>, query: &str) {
    let indexes: Vec<usize> = tasks
        .iter()
        .enumerate()
        .filter_map(|(index, task)| task.contains(query).then_some(index))
        .collect();

    for index in indexes.into_iter().rev() {
        tasks.remove(index);
    }
}
```

The second allocates indexes and repeated removal may shift elements many times. Reversing avoids invalidating not-yet-removed indexes, but `retain` is clearer and generally more efficient for this contract.

### 11. Deterministic report

```rust
use std::collections::HashMap;

fn sorted_rows(values: &HashMap<String, u64>) -> Vec<(&str, u64)> {
    let mut rows: Vec<_> = values
        .iter()
        .map(|(key, value)| (key.as_str(), *value))
        .collect();
    rows.sort_unstable_by_key(|(key, _)| *key);
    rows
}
```

The function allocates one vector of borrowed key slices and copied integers. It does not clone keys or mutate the map. The returned rows cannot outlive the map.

### 12. Complexity review

A correct capstone ledger resembles:

| Operation | Time | Allocation | State effect | Order |
|---|---|---|---|---|
| add | amortized `O(1)` after validation | possible vector growth | append | monotonic ID |
| find | `O(n)` | none | none | unchanged |
| remove | `O(n)` search and shift | none | removes one | remaining order preserved |
| search | `O(n × title work)` | query/title normalization in reference design | none | ID order |
| list | `O(n)` when board already sorted | output string and reference vector | none | ID order |
| stats | `O(n)` | output string | none | explicit status order |

Replacing the vector with a map is not yet justified. The board is small, listing is central, and a second ordering structure would add invariants. A measured workload could change that decision later.

### Post-key transfer

Implement the same board query as a loop and as an iterator pipeline, then select one using ownership, readability, and allocation evidence.

## Reference implementation comparison

The complete laboratory implementation is in [`module-06-in-memory-board/solution`](../../labs/module-06-in-memory-board/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Collections, Iterators, and Closures**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Use Vec, slices, and HashMap with explicit length, capacity, invalidation, lookup, and ordering assumptions.
- Derive item ownership for iter, iter_mut, into_iter, and for-loop desugaring contexts.
- Use closures and core iterator adapters while keeping transformations readable and cost-aware.
- Avoid mutation-during-iteration hazards by staging keys, splitting phases, or selecting a different operation.
- Produce deterministic public output even when internal storage has unspecified iteration order.

A complete explanation of **Collections, Iterators, and Closures** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.

## Deep reasoning and transfer

### Decisive model

> Does an algorithm borrow, mutate, or consume a collection, and what complexity and invalidation consequences follow?

Build a **collection and iteration trace**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Use Vec, slices, and HashMap with explicit length, capacity, invalidation, lookup, and ordering assumptions.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Derive item ownership for iter, iter_mut, into_iter, and for-loop desugaring contexts.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Use closures and core iterator adapters while keeping transformations readable and cost-aware.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Avoid mutation-during-iteration hazards by staging keys, splitting phases, or selecting a different operation.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Produce deterministic public output even when internal storage has unspecified iteration order.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Use Vec, slices, and HashMap with explicit length, capacity, invalidation, lookup, and ordering assumptions.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the collection and iteration trace.

### Laboratory transfer review

For [In-Memory Task Board](../../labs/module-06-in-memory-board/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In Taskboard, Module 6 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Collections, Iterators, and Closures**, which relationship decides this question: “Does an algorithm borrow, mutate, or consume a collection, and what complexity and invalidation consequences follow?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to Taskboard?
