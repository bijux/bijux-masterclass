# Workbook — Module 03: Ownership, Moves, Copying, and Destruction

[Chapter](index.md) · [Laboratory](../../labs/module-03-ownership-intake/README.md) · [Taskboard guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Ownership, Moves, Copying, and Destruction** has become a usable model rather than remembered vocabulary. Its governing question is: *Who owns each resource after every assignment, call, return, destructure, and scope exit?* Preserve your first prediction and record decisive facts in a **ownership ledger**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 2 — Control Flow, Functions, and Invariants that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **Who owns each resource after every assignment, call, return, destructure, and scope exit?**
3. Draw the smallest **ownership ledger** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Ownership, Moves, Copying, and Destruction** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-assignment-moves-string.rs`](../../compiler-labs/module-03/01-assignment-moves-string.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-function-consumes-argument.rs`](../../compiler-labs/module-03/02-function-consumes-argument.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-partial-move.rs`](../../compiler-labs/module-03/03-partial-move.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-copy-versus-owned-tuple.rs`](../../compiler-labs/module-03/04-copy-versus-owned-tuple.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-loop-move.rs`](../../compiler-labs/module-03/05-loop-move.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-explicit-drop.rs`](../../compiler-labs/module-03/06-explicit-drop.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 01-rust-foundations
```

## Part 2 — Diagnose and repair

A developer repaired ownership errors by cloning at every call:

```rust
fn normalize(mut title: String) -> String {
    title.make_ascii_lowercase();
    title
}

fn make_record(id: u64, title: String) -> (u64, String) {
    (id, title)
}

fn insert(mut records: Vec<(u64, String)>, record: (u64, String)) -> Vec<(u64, String)> {
    records.push(record);
    records
}

fn build(raw: String) -> Vec<(u64, String)> {
    let normalized = normalize(raw.clone());
    let record = make_record(1, normalized.clone());
    let records = insert(Vec::new(), record.clone());
    println!("{} {} {}", raw, normalized, record.1);
    records.clone()
}
```

### Clinic: Ownership requirements

The product needs one final vector containing one normalized title. It also prints a progress message during construction. It does not require raw, normalized, record, and vector snapshots after return.

### Minimal-duplication repair

```rust
fn build(raw: String) -> Vec<(u64, String)> {
    let normalized = normalize(raw);
    println!("normalized title: {normalized}");
    let record = make_record(1, normalized);
    insert(Vec::new(), record)
}
```

Zero clones are needed. Each value is observed before movement, then transferred to the next owner.

### Ownership ledger

```text
raw String      build::raw -> normalize::title -> return `normalized`
normalized      local -> make_record::title -> tuple field
record tuple    local -> insert::record -> vector element
records vector  insert::records -> return caller
```

### When one clone would be justified

If the product also required an independent immutable audit snapshot returned with the records:

```rust
fn build(raw: String) -> (Vec<(u64, String)>, String) {
    let normalized = normalize(raw);
    let audit_title = normalized.clone();
    let record = make_record(1, normalized);
    (insert(Vec::new(), record), audit_title)
}
```

Now two owners outlive the duplication point. The design should still ask whether the audit can instead be emitted or borrowed during construction.

### Exercise

Add two records and move one from pending to completed. No title clone. Preserve both vectors when the requested ID is absent.

## Part 3 — Focused exercises

### Access protocol

Attempt every required exercise and commit the attempt before opening `exercise-answers.md`. Mark each as:

### Exercise 1 — Ownership traces

For 20 short snippets covering assignment, call, return, branch, loop, tuple, array, and vector, write owner after each line. Compile only after prediction.

### Exercise 2 — Consume and return

Implement `normalize(String) -> String`, `tag(String, &str) -> String` using supplied borrowed suffix syntax, and a pipeline that moves one string through both.

### Exercise 3 — Length three ways

Implement and compare:

```rust
fn length_consume(String) -> usize;
fn length_return(String) -> (String, usize);
// borrowing version is supplied for preview:
fn length_borrow(&str) -> usize;
```

Write caller code showing which original bindings remain usable.

### Exercise 4 — Copy classification

Predict whether these are `Copy`: `u64`, `f64`, `char`, `&str`, `(u8, bool)`, `(u8, String)`, `[u8; 16]`, `[String; 2]`. Verify through assignment/use specimens.

### Exercise 5 — Partial move

Create a tuple `(u64, String, bool)`. Move the string, then demonstrate which remaining fields are usable and why whole-tuple use fails. Repair with destructuring.

### Exercise 6 — Drop order

Create a small `Tracer` type with a supplied `Drop` implementation that prints its name. Predict nested-scope destruction order. Do not implement `Drop` yourself; use the provided specimen.

### Exercise 7 — Ownership transfer between vectors

Implement:

```rust
pub type Record = (u64, String);
pub fn transfer(
    pending: Vec<Record>,
    completed: Vec<Record>,
    id: u64,
) -> (Vec<Record>, Vec<Record>, bool);
```

No clones. Preserve both collections on failure.

### Exercise 8 — Clone audit

Given a 15-clone program, classify each clone as necessary, avoidable by order, avoidable by borrowing, or potentially necessary snapshot. Remove all unjustified clones.

### Exercise 9 — Conditional move

Write two variants of a function choosing either an owned input or fallback. Explain why the input cannot be used afterward when one branch may move it.

### Exercise 10 — Resource narrative

Write a one-page ownership narrative for a vector of records: creation, insertion, removal, transfer, return, and destruction. Avoid machine-address language.

### Interleaved reasoning pass

1. For **Trace ownership through bindings, calls, returns, aggregates, and scopes using a move-path ledger**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the ownership ledger.
2. For **Distinguish semantic moves, Copy duplication, explicit Clone cost, and destruction without relying on stack-versus-heap folklore**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the ownership ledger.
3. For **Predict partial moves and the remaining usable fields of an aggregate**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the ownership ledger.
4. For **Choose consuming, returning, borrowing, or cloning APIs from post-call ownership requirements**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the ownership ledger.

5. Identify one guarantee from an earlier course that a careless implementation of **Ownership, Moves, Copying, and Destruction** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

### Product contract

Use:

```rust
pub type Record = (u64, String);
```

Implement:

```rust
pub fn normalize_title(title: String) -> String;
pub fn insert(records: Vec<Record>, id: u64, title: String) -> Vec<Record>;
pub fn transfer(
    pending: Vec<Record>,
    completed: Vec<Record>,
    id: u64,
) -> (Vec<Record>, Vec<Record>, bool);
pub fn retain_with_audit(record: Record) -> (Record, String);
```

### Requirements

- normalization trims/collapses whitespace and returns one owned title;
- insertion moves normalized title into a record and vector;
- transfer moves one record between vectors without cloning;
- failed transfer returns both collections unchanged;
- `retain_with_audit` returns the original record and an independently owned audit message;
- every clone in tests/reference data is classified; production implementation should need none in the first three operations.

### Ownership defense

For each function, submit an ownership ledger. For `transfer`, trace:

```text
pending vector -> parameter -> mutable local
record element -> remove return -> local record -> completed element
completed vector -> parameter -> mutable local -> returned tuple field
```

### Test requirements

- normalization consumes original and produces expected title;
- insertion preserves prior records and appends one;
- successful transfer preserves record ID/title exactly;
- failed transfer preserves values/order;
- audit output and retained record both survive return;
- no duplicate record appears after transfer.

### Why `retain_with_audit` is not a clone exercise

The audit message is not a second raw title owner; it is a new formatted product value. `format!` reads fields and creates a distinct message while the record remains owned for return. This demonstrates independent output without cloning the record.

### Proof

Run full format/check/clippy/test. Then search production source for `.clone()` and explain every match.

Reference: `labs/module-03-ownership-intake/solution/`.

### Tiered hints

Do not open a later tier until the previous tier has produced a written attempt.

- **Hint 1 — concept:** return to the governing question: Who owns each resource after every assignment, call, return, destructure, and scope exit?
- **Hint 2 — topology:** draw owners/borrows/states/errors before changing syntax; identify the one boundary that should own the invariant.
- **Hint 3 — structure:** separate validation from mutation and pure transformation from effects. Use the standard operation that encodes the safety fact before inventing an abstraction.
- **Hint 4 — implementation-adjacent:** consult only the relevant standard-library or Reference page; do not open `solution/src`.

The executable starter and reference implementation are in [module-03-ownership-intake](../../labs/module-03-ownership-intake/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

### Laboratory acceptance trace

Before opening the reference implementation for **Ownership Intake Pipeline**, record:

- the public behavior that demonstrates **Trace ownership through bindings, calls, returns, aggregates, and scopes using a move-path ledger**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

### Outcomes mapped

- Trace ownership through bindings, calls, returns, aggregates, and scopes using a move-path ledger.
- Distinguish semantic moves, Copy duplication, explicit Clone cost, and destruction without relying on stack-versus-heap folklore.
- Predict partial moves and the remaining usable fields of an aggregate.
- Choose consuming, returning, borrowing, or cloning APIs from post-call ownership requirements.
- Audit clone-heavy code and remove symptom-fixing duplication while preserving the product contract.

Replace fixed policy demonstrations with an early owned task collection.

### Temporary representation

```rust
pub type TaskRecord = (u64, String, String, String);
// id, title, priority, status
```

This representation is deliberately awkward. Module 5 will replace positional/string fields with named typed values.

### Operations

```rust
pub fn add_task(
    tasks: Vec<TaskRecord>,
    id: u64,
    title: String,
    priority: String,
) -> Vec<TaskRecord>;

pub fn remove_task(
    tasks: Vec<TaskRecord>,
    id: u64,
) -> (Vec<TaskRecord>, Option<TaskRecord>);
```

`Option` is supplied syntax for “removed record or none.”

### Capstone: Ownership requirements

- title and priority move into the task record;
- task record moves into the vector;
- no clone is used merely to print or preserve temporary bindings;
- removal returns ownership of the selected record;
- a missing ID returns the original vector and `None`;
- output observes values before movement or uses returned owners.

### Required trace

For one `add_task` call, record ownership from:

```text
String::from title temporary
→ caller `title`
→ function parameter
→ tuple field
→ vector element
→ returned vector
→ caller binding
```

### Regression risk

A function that consumes `Vec<TaskRecord>` makes every read operation awkward. Do not “solve” this by cloning the vector. Record this API pressure explicitly; Module 4 will refactor reads to borrow and mutations to use `&mut`.

### Commit criterion

The commit passes tests and contains a clone audit. Its design note must identify the tuple's positional risk and string-state risk without prematurely introducing Module 5 types.

### Capstone defense

Refactor an ingest pipeline so ownership crosses each boundary once, then defend every remaining clone as semantic duplication.

### Capstone invariant trace

For the Module 3 Taskboard increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Complete this checkpoint closed-book. Compiler access is allowed only after the prediction portion has been committed.

### Outcome reconstruction

For each outcome, write a claim, one example, one non-example, and one limitation.

Without reopening the chapter, reconstruct the outcomes for **Module 03: Ownership, Moves, Copying, and Destruction**. Compare your list with the earlier outcome map only after writing it, then mark each item as modelled, predicted, repaired, built, transferred, or still unsupported.

### Closed-book checkpoint

#### Closed-book questions

1. Define ownership as responsibility rather than location.
2. What happens when a `String` is assigned to another binding?
3. Why does passing `String` by value consume caller ownership?
4. How does returning a value transfer ownership?
5. Distinguish `Copy` and `Clone`.
6. Why is a shared reference `Copy` without copying referenced data?
7. What is a partial move?
8. How does moving a vector affect element ownership?
9. What product statement justifies a clone?
10. Why does `drop(value)` make later use invalid?

#### Trace

Without compiling, annotate owner after each line:

```rust
let raw = String::from("  Rust  ");
let normalized = normalize(raw);
let record = (1_u64, normalized);
let mut records = Vec::new();
records.push(record);
let removed = records.remove(0);
let title = removed.1;
println!("{}", removed.0);
```

State whether whole `removed` can be printed afterward.

#### Reconstruction

Implement vector-to-vector `transfer` from memory with no clones and preservation on missing ID.

### Transfer defense

Transfer **Module 03: Ownership, Moves, Copying, and Destruction** to a product unrelated to the course capstone. Change the domain model and failure mode, preserve the governing relationship, and identify which part of the original design was essential rather than accidental.

Your answer must include:

- the governing rule for **Module 03: Ownership, Moves, Copying, and Destruction** in plain language;
- state, ownership, or authority before and after the decisive operation;
- one causal negative case that fails for the intended reason;
- one principled repair and one easier repair that deletes a requirement;
- the limit of the evidence you used;
- one transfer to a product with different data and failure behavior.


### Closed-book defense

In five minutes, answer “Who owns each resource after every assignment, call, return, destructure, and scope exit?” using the **ownership ledger**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside Taskboard. A list of APIs without the deciding relationship is incomplete.
