# Workbook — Module 04: Borrowing, References, Slices, and Strings

[Chapter](index.md) · [Laboratory](../../labs/module-04-borrowed-catalog/README.md) · [Taskboard guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Borrowing, References, Slices, and Strings** has become a usable model rather than remembered vocabulary. Its governing question is: *Which temporary permissions does an operation require, and how narrowly can those permissions be scoped?* Preserve your first prediction and record decisive facts in a **borrow map**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 3 — Ownership, Moves, Copying, and Destruction that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **Which temporary permissions does an operation require, and how narrowly can those permissions be scoped?**
3. Draw the smallest **borrow map** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Borrowing, References, Slices, and Strings** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-shared-then-mutable.rs`](../../compiler-labs/module-04/01-shared-then-mutable.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-two-indexed-mutable-borrows.rs`](../../compiler-labs/module-04/02-two-indexed-mutable-borrows.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-return-reference-to-local.rs`](../../compiler-labs/module-04/03-return-reference-to-local.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-mutate-during-iteration.rs`](../../compiler-labs/module-04/04-mutate-during-iteration.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-slice-outlives-owner.rs`](../../compiler-labs/module-04/05-slice-outlives-owner.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-reborrow.rs`](../../compiler-labs/module-04/06-reborrow.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 01-rust-foundations
```

## Part 2 — Diagnose and repair

Defective code:

```rust
pub type Record = (u64, String);

fn find(records: Vec<Record>, id: u64) -> Option<Record> {
    for record in records {
        if record.0 == id {
            return Some(record.clone());
        }
    }
    None
}

fn rename(records: &mut Vec<Record>, id: u64, title: String) -> bool {
    let existing = find(records.clone(), id);
    if existing.is_none() {
        return false;
    }
    for record in records {
        if record.0 == id {
            record.1 = title.clone();
        }
    }
    true
}
```

### Disease analysis

- `find` consumes the whole vector and returns a cloned record.
- caller clones the vector to preserve it.
- lookup result is used only to test existence, then a second search occurs.
- `rename` accepts owned title though it can copy bytes into existing storage from `&str`.
- assignment clone is unnecessary because only one matching record is changed.
- `&mut Vec` grants length-changing capability although only elements are changed; `&mut [Record]` is narrower.

### Repair

```rust
pub fn find(records: &[Record], id: u64) -> Option<&Record> {
    records.iter().find(|record| record.0 == id)
}

pub fn rename(records: &mut [Record], id: u64, replacement: &str) -> bool {
    let Some(record) = records.iter_mut().find(|record| record.0 == id) else {
        return false;
    };
    record.1.clear();
    record.1.push_str(replacement);
    true
}
```

One traversal, one mutable borrow, no clone, narrower API.

### Alternative assignment

```rust
record.1 = replacement.to_owned();
```

This allocates/creates an owned replacement and is semantically correct. `clear` + `push_str` may reuse capacity. Do not claim one is always faster without measurement; the core contract is that the record must own text after the borrowed replacement disappears.

### Returned reference consequence

```rust
let found = find(&records, id);
rename(&mut records, id, "new");
println!("{found:?}");
```

This fails because `found` remains used after mutation. Consume the observation before mutation, or do not retain the reference.

### Required variation

Implement `matching_titles(&[Record], &str) -> Vec<&str>` and explain why returned slices cannot outlive the records.

## Part 3 — Focused exercises

### Access protocol

Attempt every required exercise and commit the attempt before opening `exercise-answers.md`. Mark each as:

### Exercise 1 — Signature classification

For 20 requirements, choose `T`, `&T`, or `&mut T` and justify. Include store-after-return, print-only, in-place sort, consume-and-transform, and independent snapshot cases.

### Exercise 2 — Borrowed length/refactor

Refactor Module 3's consuming length and print functions to `&str`. Demonstrate caller retains ownership and no clones remain.

### Exercise 3 — First word

Implement `first_word(&str) -> &str` without allocation. Test empty, leading whitespace, Unicode text, and multiple spaces. Explain source relationship.

### Exercise 4 — Slice prefix

Implement `prefix<T>(&[T], usize) -> Option<&[T]>` using `get`, not indexing. Generic syntax is supplied; focus on view behavior.

### Exercise 5 — In-place normalization

Implement `ensure_terminal_period(&mut String)`. It adds a period only when missing. Test idempotence and empty input.

### Exercise 6 — Borrowed lookup

Using `(u64, String)` records, implement shared `find` and mutable `find_mut`. No vector consumption.

### Exercise 7 — Rename

Implement `rename(&mut [Record], id, &str) -> bool` with one search. Test found/missing and preservation of other records.

### Exercise 8 — Disjoint mutation

Given a mutable slice and two distinct indices, swap/increment values safely. First implement with `split_at_mut`; reject equal/out-of-range indices.

### Exercise 9 — Remove while traversing

Implement removal policy using `retain`. Then implement a variant returning removed owned records without mutating during a shared iteration. Compare ownership.

### Exercise 10 — String boundary audit

Review ten APIs using `String`, `&String`, `&str`, `&mut String`. Correct each signature and state allocation/ownership consequences.

### Interleaved reasoning pass

1. For **Model shared and mutable references as permissions constrained by aliasing and validity**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the borrow map.
2. For **Shorten borrow scopes, reborrow correctly, and split disjoint data instead of cloning or over-owning**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the borrow map.
3. For **Design slice-based APIs and distinguish String, str, &String, and &str by ownership and representation**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the borrow map.
4. For **Handle UTF-8 text without assuming character indexing or byte-boundary equivalence**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the borrow map.

5. Identify one guarantee from an earlier course that a careless implementation of **Borrowing, References, Slices, and Strings** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

### Product contract

Use:

```rust
pub type Record = (u64, String);
```

Implement:

```rust
pub fn find(records: &[Record], id: u64) -> Option<&Record>;
pub fn rename(records: &mut [Record], id: u64, replacement: &str) -> bool;
pub fn first_word(title: &str) -> &str;
pub fn matching_titles<'a>(records: &'a [Record], query: &str) -> Vec<&'a str>;
pub fn total_title_bytes(records: &[Record]) -> usize;
```

The explicit lifetime in `matching_titles` is supplied; Module 8 explains why output is tied to `records` rather than `query`.

### Constraints

- no `.clone()` in production code;
- no `&String` parameters;
- no `&Vec<Record>` parameters;
- listing/searching does not consume the collection;
- renaming performs one mutable search and changes one record;
- returned title slices borrow record strings;
- byte total is explicitly bytes, not characters;
- tests include multibyte UTF-8 text.

### Borrow defense

For each function, state:

- owner of records/titles;
- shared or exclusive access;
- whether result is owned or borrowed;
- final use that ends each borrow;
- caller operations blocked while returned references remain used.

### Adversarial test

Attempt this in a separate specimen:

```rust
let matches = matching_titles(&records, "parser");
rename(&mut records, 1, "decoder");
println!("{matches:?}");
```

Predict the failure. Then reorder use so mutation becomes valid.

### Proof

Run full format/check/clippy/test and a source search for `.clone()`.

Reference: `labs/module-04-borrowed-catalog/solution/`.

### Tiered hints

Do not open a later tier until the previous tier has produced a written attempt.

- **Hint 1 — concept:** return to the governing question: Which temporary permissions does an operation require, and how narrowly can those permissions be scoped?
- **Hint 2 — topology:** draw owners/borrows/states/errors before changing syntax; identify the one boundary that should own the invariant.
- **Hint 3 — structure:** separate validation from mutation and pure transformation from effects. Use the standard operation that encodes the safety fact before inventing an abstraction.
- **Hint 4 — implementation-adjacent:** consult only the relevant standard-library or Reference page; do not open `solution/src`.

The executable starter and reference implementation are in [module-04-borrowed-catalog](../../labs/module-04-borrowed-catalog/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

### Laboratory acceptance trace

Before opening the reference implementation for **Borrowed Catalog**, record:

- the public behavior that demonstrates **Model shared and mutable references as permissions constrained by aliasing and validity**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

### Outcomes mapped

- Model shared and mutable references as permissions constrained by aliasing and validity.
- Shorten borrow scopes, reborrow correctly, and split disjoint data instead of cloning or over-owning.
- Design slice-based APIs and distinguish String, str, &String, and &str by ownership and representation.
- Handle UTF-8 text without assuming character indexing or byte-boundary equivalence.
- Return borrowed views only when provenance remains valid and explain the source of every returned reference.

Refactor the temporary tuple-based capstone APIs from ownership shuttling to borrowing.

### Required signatures

```rust
pub fn list_tasks(tasks: &[TaskRecord]) -> String;
pub fn find_task(tasks: &[TaskRecord], id: u64) -> Option<&TaskRecord>;
pub fn find_task_mut(tasks: &mut [TaskRecord], id: u64) -> Option<&mut TaskRecord>;
pub fn set_status(tasks: &mut [TaskRecord], id: u64, status: &str) -> bool;
```

Keep `add_task(&mut Vec<TaskRecord>, ...)` because insertion changes vector length. Refactor removal to `&mut Vec<TaskRecord>` because it changes length and transfers one removed record.

### Acceptance

- listing can be called twice without rebuilding/cloning the vector;
- lookup returns a borrowed record;
- status update performs one mutable search;
- a missing ID preserves the vector;
- no clone is introduced by the refactor;
- parameters use slices unless vector capacity/length behavior is required.

### Borrow interval test

Write a compile-fail scratch specimen retaining `find_task` result across `set_status`. Explain why it fails. Then write valid code that reads the result before mutation and looks up again afterward.

### Design result

The capstone now reveals three access classes:

- read operations: `&[TaskRecord]`;
- fixed-length element mutation: `&mut [TaskRecord]`;
- length-changing operations: `&mut Vec<TaskRecord>`.

This distinction must survive the Module 5 typed refactor.

### Capstone defense

Repair a catalog update that conflicts with an active search borrow by changing access topology rather than extending ownership.

### Capstone invariant trace

For the Module 4 Taskboard increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Complete this checkpoint closed-book. Compiler access is allowed only after the prediction portion has been committed.

### Outcome reconstruction

For each outcome, write a claim, one example, one non-example, and one limitation.

Without reopening the chapter, reconstruct the outcomes for **Module 04: Borrowing, References, Slices, and Strings**. Compare your list with the earlier outcome map only after writing it, then mark each item as modelled, predicted, repaired, built, transferred, or still unsupported.

### Closed-book checkpoint

#### Closed-book questions

1. State the aliasing rule precisely enough to include time and overlapping regions.
2. What does `&T` permit and preserve?
3. What does `&mut T` guarantee beyond actual mutation?
4. Why can a shared borrow end before the closing brace?
5. What is reborrowing?
6. Why can a reference to a local not be returned?
7. Distinguish `&[T]`, `&mut [T]`, `&mut Vec<T>`, and `Vec<T>`.
8. Why is `&str` preferred over `&String` for reading?
9. What does `String::len()` count?
10. Name three borrow repairs that do not clone.

#### Prediction

Trace borrow intervals:

```rust
let mut title = String::from("borrow");
let first = &title;
println!("{first}");
let second = &mut title;
second.push('!');
println!("{second}");
println!("{title}");
```

Then move the first print below `second.push` and predict the diagnostic category.

#### Reconstruction

Implement shared lookup, mutable rename, and borrowed `first_word` from a blank file. No clones.

### Transfer defense

Transfer **Module 04: Borrowing, References, Slices, and Strings** to a product unrelated to the course capstone. Change the domain model and failure mode, preserve the governing relationship, and identify which part of the original design was essential rather than accidental.

Your answer must include:

- the governing rule for **Module 04: Borrowing, References, Slices, and Strings** in plain language;
- state, ownership, or authority before and after the decisive operation;
- one causal negative case that fails for the intended reason;
- one principled repair and one easier repair that deletes a requirement;
- the limit of the evidence you used;
- one transfer to a product with different data and failure behavior.


### Closed-book defense

In five minutes, answer “Which temporary permissions does an operation require, and how narrowly can those permissions be scoped?” using the **borrow map**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside Taskboard. A list of APIs without the deciding relationship is incomplete.
