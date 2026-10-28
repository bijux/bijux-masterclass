# Laboratory 6 — In-Memory Task Board

**Course 1 · Module 6: Collections, Iterators, and Closures**

[Chapter](../../course-book/module-06-collections-iterators-and-closures/index.md) · [Workbook](../../course-book/module-06-collections-iterators-and-closures/workbook.md) · [Taskboard guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Collections, Iterators, and Closures**: Does an algorithm borrow, mutate, or consume a collection, and what complexity and invalidation consequences follow? The product must make **Use Vec, slices, and HashMap with explicit length, capacity, invalidation, lookup, and ordering assumptions** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **collection and iteration trace** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> Does an algorithm borrow, mutate, or consume a collection, and what complexity and invalidation consequences follow?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

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

### Restrictions

- standard library only;
- safe Rust only;
- no clone used to repair borrow errors;
- no stringly typed status;
- no public fields;
- no panic for normal missing-ID or invalid-transition behavior;
- no dependence on hash-map iteration order.

## Working route

1. Read the product contract and run the starter’s baseline checks for **In-Memory Task Board**.
2. Draw the smallest **collection and iteration trace** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to Taskboard so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 6 — In-Memory Task Board**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **In-Memory Task Board**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Use Vec, slices, and HashMap with explicit length, capacity, invalidation, lookup, and ordering assumptions.
- Derive item ownership for iter, iter_mut, into_iter, and for-loop desugaring contexts.
- Use closures and core iterator adapters while keeping transformations readable and cost-aware.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 6 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **collection and iteration trace**. Defend why your design is simpler than one plausible alternative under the new requirements.
