# Workbook — Module 06: Collections, Iterators, and Closures

[Chapter](index.md) · [Laboratory](../../labs/module-06-in-memory-board/README.md) · [Taskboard guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Collections, Iterators, and Closures** has become a usable model rather than remembered vocabulary. Its governing question is: *Does an algorithm borrow, mutate, or consume a collection, and what complexity and invalidation consequences follow?* Preserve your first prediction and record decisive facts in a **collection and iteration trace**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 5 — Structs, Enums, Methods, and Pattern Matching that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **Does an algorithm borrow, mutate, or consume a collection, and what complexity and invalidation consequences follow?**
3. Draw the smallest **collection and iteration trace** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Collections, Iterators, and Closures** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-into-iter-consumes-vector.rs`](../../compiler-labs/module-06/01-into-iter-consumes-vector.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-mutate-while-shared-iter.rs`](../../compiler-labs/module-06/02-mutate-while-shared-iter.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-collect-needs-type.rs`](../../compiler-labs/module-06/03-collect-needs-type.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-index-can-panic.rs`](../../compiler-labs/module-06/04-index-can-panic.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-hash-order-is-not-contract.rs`](../../compiler-labs/module-06/05-hash-order-is-not-contract.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-filter-borrows-source.rs`](../../compiler-labs/module-06/06-filter-borrows-source.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 01-rust-foundations
```

## Part 2 — Diagnose and repair

The following design was “repaired” by cloning values and by rebuilding collections. It may compile after small edits, but it has weak ownership, poor complexity, and unstable output.

```rust
use std::collections::HashMap;

#[derive(Clone)]
struct Task {
    id: u64,
    title: String,
    status: String,
}

fn find(tasks: Vec<Task>, id: u64) -> Option<Task> {
    tasks.into_iter().find(|task| task.id == id)
}

fn complete(tasks: &mut Vec<Task>, id: u64) -> bool {
    if let Some(mut task) = find(tasks.clone(), id) {
        task.status = String::from("done");
        tasks.retain(|existing| existing.id != id);
        tasks.push(task);
        true
    } else {
        false
    }
}

fn counts(tasks: &[Task]) -> HashMap<String, usize> {
    let mut result = HashMap::new();
    for task in tasks {
        let current = result.get(&task.status).copied().unwrap_or(0);
        result.insert(task.status.clone(), current + 1);
    }
    result
}
```

### Defects to identify

Your report must include at least these categories:

1. `find` consumes the entire vector even though lookup should borrow;
2. `find` returns an owned clone in the calling design rather than a reference;
3. `complete` clones every task to work around its own API;
4. remove-and-push changes task order;
5. status is an arbitrary string and permits invalid state;
6. failure returns only `false`, losing not-found versus illegal-transition information;
7. counts performs two lookups/updates rather than one entry operation;
8. count keys are repeatedly cloned;
9. map iteration would make later rendering nondeterministic;
10. `Vec` in parameter position exposes growth capability that `find` does not need.

### Repair contract

Refactor toward:

```rust
#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
enum Status {
    Todo,
    Doing,
    Done,
}

fn find(tasks: &[Task], id: u64) -> Option<&Task>;
fn find_mut(tasks: &mut [Task], id: u64) -> Option<&mut Task>;
fn complete(tasks: &mut [Task], id: u64) -> Result<(), TransitionError>;
fn counts(tasks: &[Task]) -> HashMap<Status, usize>;
```

Then render counts in explicit `[Todo, Doing, Done]` order.

### Clinic: Restrictions

- Do not add a clone to library behavior.
- Do not use unsafe code.
- Do not expose task fields merely to simplify tests.
- Do not convert every function to an iterator chain.
- A failed transition must preserve the task.

### Proof

Write tests for:

- successful lookup returns a reference to the original task;
- missing lookup returns `None`;
- completing from `Doing` succeeds;
- completing from `Todo` fails without mutation;
- task order is unchanged;
- counts include zero-valued statuses in deterministic rendering;
- no invalid status can be constructed through the public API.

In the compiler journal, record which original clone hid which ownership mistake.

## Part 3 — Focused exercises

### Access protocol

Attempt every required exercise and commit the attempt before opening `exercise-answers.md`. Mark each as:

Attempt every exercise before reading the answers. Each implementation must include tests and a brief ownership note.

### 1. Safe endpoints

Implement:

```rust
fn endpoints<T>(values: &[T]) -> Option<(&T, &T)>;
```

Define behavior for an empty slice and for a one-element slice.

### 2. Remove the first match

Implement:

```rust
fn remove_first<T, F>(values: &mut Vec<T>, predicate: F) -> Option<T>
where
    F: FnMut(&T) -> bool;
```

Preserve relative order. State the worst-case complexity.

### 3. Deduplicate while preserving first occurrence

For `Vec<String>`, return a new vector that preserves the first occurrence of each exact string. Do not sort the input. Explain the allocation policy.

### 4. Stable status counts

Given typed `Status` values, count them with a `HashMap` and render all statuses in explicit domain order, including zeros.

### 5. Normalize in place

Trim leading and trailing whitespace from every `String` in a mutable slice, then remove blank strings from the owning vector. Separate the slice-only and length-changing stages.

### 6. Iterator item matrix

For each expression, state the item type and whether the source remains usable:

```rust
values.iter()
values.iter_mut()
values.into_iter()
&values
&mut values
values
```

Assume `values: Vec<String>`.

### 7. First parse error

Implement a function that converts `&[&str]` into `Result<Vec<u64>, ParseIntError>` and stops at the first error. Then implement a second version that returns every invalid `(index, text)` while retaining valid numbers.

### 8. Short-circuit validation

Check whether every title is nonblank and at most 120 bytes. Demonstrate with a counter that evaluation stops after the first invalid title.

### 9. Closure capability

Write three closures: one that only reads a captured string, one that increments a captured counter, and one that consumes a captured vector. State the strongest call trait each implements.

### 10. Two-phase removal

Given a vector of tasks and a borrowed query, remove all matching tasks without mutating the collection during a shared traversal. Provide one `retain` solution and one index-collection solution. Compare their cost and clarity.

### 11. Deterministic report

Given `HashMap<String, u64>`, produce lexicographically sorted output without mutating the map and without cloning values. State what is allocated.

### 12. Complexity review

Review the capstone's add, find, remove, search, list, and stats operations. Produce a table with traversal complexity, allocation, mutation, and order guarantees. Identify one optimization that is not yet justified.

### Interleaved reasoning pass

1. For **Use Vec, slices, and HashMap with explicit length, capacity, invalidation, lookup, and ordering assumptions**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the collection and iteration trace.
2. For **Derive item ownership for iter, iter_mut, into_iter, and for-loop desugaring contexts**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the collection and iteration trace.
3. For **Use closures and core iterator adapters while keeping transformations readable and cost-aware**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the collection and iteration trace.
4. For **Avoid mutation-during-iteration hazards by staging keys, splitting phases, or selecting a different operation**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the collection and iteration trace.

5. Identify one guarantee from an earlier course that a careless implementation of **Collections, Iterators, and Closures** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

### Objective

Build a typed, deterministic in-memory task board. This is the first lab where collection behavior, state-machine rules, and ownership design must work together.

Use the starter package:

```text
labs/module-06-in-memory-board/starter/
```

Do not inspect the reference implementation until your own public tests pass.

### Required domain

Define private-field types equivalent in responsibility to:

```rust
struct TaskId(u64);

enum Priority {
    Low,
    Normal,
    High,
}

enum Status {
    Todo,
    Doing,
    Done,
}

struct Task {
    id: TaskId,
    title: String,
    priority: Priority,
    status: Status,
}

struct TaskBoard {
    tasks: Vec<Task>,
    next_id: u64,
}
```

You may choose different names, but not a weaker representation.

### Required behavior

The board must:

1. allocate nonzero monotonically increasing IDs;
2. validate nonblank titles before mutation;
3. add every new task in `Todo`;
4. borrow tasks for read-only lookup;
5. mutate through one narrow internal lookup path;
6. permit only `Todo -> Doing`, `Doing -> Done`, and `Done -> Todo`;
7. remove a task while transferring ownership of it to the caller;
8. list all tasks in ascending ID order;
9. filter by optional status without cloning tasks;
10. search titles using a documented case policy;
11. count all statuses deterministically;
12. never reuse a removed ID.

### Required public surface

Your design must support operations equivalent to:

```text
new
add
find
start
complete
reopen
remove
filtered
search
stats
```

Do not expose mutable task fields. Do not return `bool` for failures that need not-found or illegal-transition context.

### Required tests

At minimum:

- first ID is 1;
- two additions receive distinct increasing IDs;
- blank title fails and does not advance the ID;
- skipped transition fails without changing status;
- full lifecycle succeeds;
- missing ID has a typed error;
- removal transfers the correct task and preserves remaining order;
- removed ID is not reused;
- filtering returns borrowed tasks only;
- search behavior is case-documented and tested;
- counts include zero states;
- list/filter/search order is deterministic.

### Complexity report

Submit a table for every operation. Linear lookup is accepted and expected. Do not add a hash map merely to claim constant-time lookup unless you also specify and test how it remains synchronized with deterministic order.

### Laboratory: Restrictions

- standard library only;
- safe Rust only;
- no clone used to repair borrow errors;
- no stringly typed status;
- no public fields;
- no panic for normal missing-ID or invalid-transition behavior;
- no dependence on hash-map iteration order.

### Tiered hints

Do not open a later tier until the previous tier has produced a written attempt.

- **Hint 1 — concept:** return to the governing question: Does an algorithm borrow, mutate, or consume a collection, and what complexity and invalidation consequences follow?
- **Hint 2 — topology:** draw owners/borrows/states/errors before changing syntax; identify the one boundary that should own the invariant.
- **Hint 3 — structure:** separate validation from mutation and pure transformation from effects. Use the standard operation that encodes the safety fact before inventing an abstraction.
- **Hint 4 — implementation-adjacent:** consult only the relevant standard-library or Reference page; do not open `solution/src`.

The executable starter and reference implementation are in [module-06-in-memory-board](../../labs/module-06-in-memory-board/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

### Laboratory acceptance trace

Before opening the reference implementation for **In-Memory Task Board**, record:

- the public behavior that demonstrates **Use Vec, slices, and HashMap with explicit length, capacity, invalidation, lookup, and ordering assumptions**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

### Outcomes mapped

- Use Vec, slices, and HashMap with explicit length, capacity, invalidation, lookup, and ordering assumptions.
- Derive item ownership for iter, iter_mut, into_iter, and for-loop desugaring contexts.
- Use closures and core iterator adapters while keeping transformations readable and cost-aware.
- Avoid mutation-during-iteration hazards by staging keys, splitting phases, or selecting a different operation.
- Produce deterministic public output even when internal storage has unspecified iteration order.

The capstone now stops being a list of loosely related values. Introduce the aggregate that owns task order and ID allocation.

### Required change

Implement `TaskBoard` over `Vec<Task>` with:

```text
new
add
find
private find_mut
start
complete
reopen
remove
filtered
search
stats
tasks
```

The vector must remain in ascending ID order. Ordinary additions append because IDs increase. Restored data will be sorted and validated in Module 7.

### Signature defense

For each operation, write the ownership reason:

- `tasks(&self) -> &[Task]`: exposes a read-only view without vector-specific mutation;
- `find(&self, id) -> Option<&Task>`: absence is ordinary and the board retains ownership;
- `find_mut(&mut self, id) -> Result<&mut Task, TaskError>`: only the model needs exclusive mutation capability;
- `remove(&mut self, id) -> Result<Task, TaskError>`: removed ownership leaves the board;
- `filtered(&self, status) -> impl Iterator<Item = &Task>`: lazy borrowed traversal;
- `add(&mut self, priority, title: String)`: the board adopts title ownership.

### Determinism

Do not render a `HashMap` directly for statistics. Return a typed `Stats` value or render statuses in explicit order.

Search and filtering must preserve board order. A read-only command must not reorder authoritative state merely for presentation.

### Tests to add

Add tests proving:

1. title validation occurs before ID advancement;
2. task lookup borrows rather than clones;
3. failed transitions preserve status;
4. removal does not cause ID reuse;
5. filter and search order is stable;
6. statistics count every variant;
7. no public method can create an arbitrary task status.

### Review question

Why is `Vec<Task>` an acceptable authoritative representation even though lookup is linear? Your answer must discuss expected scale, deterministic order, conceptual surface, and the invariant cost of maintaining a second index.

### Capstone defense

Implement the same board query as a loop and as an iterator pipeline, then select one using ownership, readability, and allocation evidence.

### Capstone invariant trace

For the Module 6 Taskboard increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Complete this checkpoint closed-book. Compiler access is allowed only after the prediction portion has been committed.

### Outcome reconstruction

For each outcome, write a claim, one example, one non-example, and one limitation.

Without reopening the chapter, reconstruct the outcomes for **Module 06: Collections, Iterators, and Closures**. Compare your list with the earlier outcome map only after writing it, then mark each item as modelled, predicted, repaired, built, transferred, or still unsupported.

### Closed-book checkpoint

#### Part A — Retrieval

1. Distinguish vector length from capacity.
2. Name four operations that can change element positions or allocation.
3. Explain why a reference into a vector cannot remain active across `push`.
4. When should a parameter be `&[T]` instead of `&Vec<T>`?
5. What is transferred by `Vec::remove` for a non-`Copy` element?
6. State the item type of `iter`, `iter_mut`, and `into_iter` for `Vec<String>`.
7. What causes a lazy iterator pipeline to execute?
8. Why can `collect` require an explicit output type?
9. Explain why hash-map iteration order cannot define a persistence format.
10. What duplicate-key policy does `insert` imply if its previous value is ignored?
11. What capability does the `entry` API represent?
12. Explain the difference among `Fn`, `FnMut`, and `FnOnce` in terms of captured state.
13. Why can a `move` closure still be called more than once?
14. When is stable sorting required?
15. Why can a temporary vector of references be useful for deterministic output?
16. Give a validate-then-commit collection operation and explain failure atomicity.

#### Part B — Prediction

For each fragment, state whether the source remains usable and what each item type is:

```rust
for value in values { /* ... */ }
for value in &values { /* ... */ }
for value in &mut values { /* ... */ }
```

Then predict the compiler result:

```rust
let mut values = vec![String::from("a")];
let first = values.first();
values.push(String::from("b"));
println!("{first:?}");
```

#### Part C — Construction

From memory, implement:

```rust
fn remove_first<T, F>(values: &mut Vec<T>, predicate: F) -> Option<T>
where
    F: FnMut(&T) -> bool;
```

Then implement deterministic rendering for counts stored in `HashMap<Status, usize>`.

#### Part D — Design defense

Defend or reject each statement:

1. “A map is always faster than a vector.”
2. “Iterator code is more idiomatic, so loops should be removed.”
3. “Cloning the collection is acceptable because it makes borrowing simpler.”
4. “The current hash-map output order passed the test, so it is stable.”
5. “The capstone should maintain a vector and map from the beginning.”

A passing defense discusses contracts and trade-offs, not style preferences.

### Transfer defense

Transfer **Module 06: Collections, Iterators, and Closures** to a product unrelated to the course capstone. Change the domain model and failure mode, preserve the governing relationship, and identify which part of the original design was essential rather than accidental.

Your answer must include:

- the governing rule for **Module 06: Collections, Iterators, and Closures** in plain language;
- state, ownership, or authority before and after the decisive operation;
- one causal negative case that fails for the intended reason;
- one principled repair and one easier repair that deletes a requirement;
- the limit of the evidence you used;
- one transfer to a product with different data and failure behavior.


### Closed-book defense

In five minutes, answer “Does an algorithm borrow, mutate, or consume a collection, and what complexity and invalidation consequences follow?” using the **collection and iteration trace**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside Taskboard. A list of APIs without the deciding relationship is incomplete.
