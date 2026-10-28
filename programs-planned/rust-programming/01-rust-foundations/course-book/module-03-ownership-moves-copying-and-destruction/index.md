# 03 — Ownership, Moves, Copying, and Destruction

**Course 1, day 3 · Module 3 of 90**  
`█░░░░░░░░░░░░░░░░░░░` **3/90**

[← Module 2: Control Flow, Functions, and Invariants](../module-02-control-flow-functions-and-invariants/index.md) · [Course 1 overview](../index.md) · [Ninety-module map](../../../COURSE_MAP.md) · [Module 4: Borrowing, References, Slices, and Strings →](../module-04-borrowing-references-slices-and-strings/index.md)

## The question

> Who owns each resource after every assignment, call, return, destructure, and scope exit?

## Why this comes now

Functions now create real ownership boundaries: arguments enter, results leave, and locals are destroyed. That makes this the right moment to replace the vague idea of 'variables holding data' with a precise resource ledger. Every later borrow, smart pointer, iterator, and trait object rests on this transfer model.

## What you will be able to do

- Trace ownership through bindings, calls, returns, aggregates, and scopes using a move-path ledger.
- Distinguish semantic moves, Copy duplication, explicit Clone cost, and destruction without relying on stack-versus-heap folklore.
- Predict partial moves and the remaining usable fields of an aggregate.
- Choose consuming, returning, borrowing, or cloning APIs from post-call ownership requirements.
- Audit clone-heavy code and remove symptom-fixing duplication while preserving the product contract.

## Core model

### Why this module exists

Ownership is not a compiler obstacle; it is a resource-accounting model. A value may own memory, a file descriptor, a lock guard, a callback, or a cleanup obligation. Rust requires the program to make transfers and duplication explicit so that each resource has one unambiguous destruction path unless its type deliberately implements shared ownership later.

### The ownership ledger

For every non-`Copy` value, record:

```text
value/resource:
current owner:
moved at:
borrowed by:
duplicated at:
dropped at:
usable bindings after the statement:
```

A move is a semantic transfer of ownership. The language does not promise that bytes are physically copied or not copied. A `String` move typically copies its small inline handle while transferring responsibility for the allocation, but that implementation picture is not the rule. The rule is that the source binding may no longer be used as an initialized owner.

```rust
let title = String::from("compile report");
let queued = title;
// title is moved; queued owns the String.
```

For `Copy` types, assignment creates another independent value:

```rust
let count = 4_u32;
let snapshot = count;
assert_eq!(count, snapshot);
```

`Copy` is not “stack semantics.” It is a type contract that ordinary duplication is implicit and has no custom destruction behavior. `Clone` is explicit duplication and may allocate or perform arbitrary type-defined work.

### Calls and returns are ownership edges

```rust
fn normalize(mut title: String) -> String {
    title.make_ascii_lowercase();
    title
}

let raw = String::from("REPORT");
let normalized = normalize(raw);
```

The call transfers ownership into the parameter. Returning transfers it back under a new binding. This design can be appropriate when the operation must retain or transform owned storage. If the caller needs the original as well, choose between borrowing, returning both values, or semantic duplication based on the product requirement—not based on which edit silences an error.

### Partial moves

Patterns can move selected fields while leaving others accessible when the remaining use is legal:

```rust
struct Record {
    id: u64,
    title: String,
    score: u32,
}

let record = Record {
    id: 7,
    title: String::from("audit"),
    score: 92,
};

let title = record.title;
assert_eq!(record.id, 7);
assert_eq!(record.score, 92);
// `record` as a whole cannot be used because one field was moved.
```

A type implementing `Drop` cannot generally have fields moved out this way because its destructor expects a valid whole value. Later courses study `Option::take`, `mem::replace`, and protocol design for controlled field extraction.

### Worked derivation: intake pipeline

Suppose an intake function validates and stores owned records:

```rust
#[derive(Debug, PartialEq, Eq)]
pub struct IntakeRecord {
    title: String,
    source: String,
}

pub fn accept(
    queue: &mut Vec<IntakeRecord>,
    title: String,
    source: String,
) -> Result<usize, (String, String)> {
    if title.trim().is_empty() || source.trim().is_empty() {
        return Err((title, source));
    }

    queue.push(IntakeRecord { title, source });
    Ok(queue.len() - 1)
}
```

The function takes ownership because successful execution stores both strings beyond the call. On failure it returns them, preserving caller ownership rather than destroying possibly valuable input. The mutable borrow of the queue is temporary; the strings move into the vector only on the success path.

A clone-heavy alternative might validate cloned strings, clone again into the queue, and retain the originals “just in case.” That design obscures whether duplication is actually required and doubles allocation work.

### Clone audit

For every `clone()` ask:

1. Must two logically independent values survive afterward?
2. Is the clone duplicating a small copyable token, a shared handle, or an owned allocation?
3. Could the API borrow for inspection?
4. Could ownership be returned on failure?
5. Is the clone preserving evidence needed after mutation?

Not every clone is wrong. Copying a durable identifier before a mutable phase can be the clearest design. The defect is unexplained duplication used as a universal repair.

### Destruction boundaries

Values are dropped when their owner leaves its drop scope, subject to execution mode and deliberate leaks. Ordinary scope exit, early return, and unwinding generally run destructors. Process abort, `process::exit`, power failure, and leaked values can bypass ordinary destruction. Course 2 derives exact drop scopes and panic-safety protocols; Course 1 must avoid the false slogan “Drop always runs.”

### Try without the scaffold

Refactor a function that receives `Vec<String>`, produces accepted and rejected records, and currently clones every element. Decide whether to consume the vector with `into_iter`, borrow it, or return rejected ownership. Draw the ledger before coding.

### Misconception clinic

- **“Moves happen only for heap values.”** Move semantics belong to types; inline non-`Copy` values move too.
- **“A move means an expensive memory copy.”** It is an ownership transfer; physical movement is not the semantic contract.
- **“Clone is bad.”** Unjustified clone is bad. Required independent ownership is legitimate.
- **“The compiler owns cleanup.”** Values own cleanup obligations; the compiler enforces the type rules that make their destruction paths coherent.

### Ownership as responsibility

At any moment, a value has an owner: the binding, field, collection element, or temporary responsible for it. When the owner leaves scope, Rust runs the value's destructor and releases owned resources.

```rust
fn main() {
    let title = String::from("owned text");
    println!("{title}");
} // `title` is dropped here
```

`String` owns a UTF-8 allocation. Dropping it releases that allocation. The same scope rule can close a file or release a lock guard because destruction is type-defined.

This pattern is often called RAII—resource acquisition is initialization—but the course's operational question is simpler: **which value owns the resource, and where is that value destroyed?**

### Scope is lexical, destruction is deterministic

```rust
fn example() {
    let outer = String::from("outer");
    {
        let inner = String::from("inner");
        println!("{inner}");
    } // inner drops
    println!("{outer}");
} // outer drops
```

Values in a scope are generally dropped in reverse order of declaration when normal control leaves the scope. Fields are dropped according to the language's field-drop rules after the containing value's destructor runs. Do not build product logic around incidental destruction ordering among unrelated values; use explicit scopes when order matters.

### Temporary values

```rust
println!("{}", String::from("temporary").len());
```

The temporary `String` owns its allocation until the statement's temporary scope ends. A named binding is not required for ownership to exist.

Temporaries become important when borrowing them; a reference cannot remain valid after the temporary owner is destroyed.

### `Drop` and explicit `drop`

The standard `drop` function consumes a value, causing destruction at that point:

```rust
let buffer = String::from("sensitive intermediate");
process(&buffer); // borrowing is taught next module
drop(buffer);
// buffer cannot be used here
```

Do not call a destructor method directly. `drop(value)` is an ownership transfer into a function that immediately ends the value.

Course 1 does not implement custom `Drop`; that subject interacts with move restrictions and advanced resource design. You must still understand when standard and user-defined values are destroyed.

### Ownership is not synonymous with heap allocation

A user-defined struct containing only integers can be non-`Copy` and therefore moved even if its representation is entirely inline. Conversely, references are `Copy` values even though they point elsewhere. The rule comes from the type's implemented semantics, not from a simplistic stack-versus-heap category.

A `String` can be mentally pictured as small metadata—pointer, length, capacity—owning separate allocated bytes. Moving a `String` commonly transfers/copies that metadata and invalidates the source binding; it need not copy the text bytes. This is an implementation-oriented intuition, not the language guarantee to reason from.

### Resource safety under early return

```rust
fn work() -> Result<(), WorkError> {
    let file = open_file()?;
    validate()?;
    process(file)?;
    Ok(())
}
```

If validation fails, owned locals are still destroyed while the function unwinds normally through `Result` propagation. Scope-based cleanup removes the need to manually release resources on every branch.

### Ownership ledger

For nontrivial code, record:

```text
Value          Owner at creation     Transfer          Final owner/drop
text bytes     title                 title -> record   record at vector drop
record         local record          record -> vector  vector element
vector buffer  tasks                 return to caller  caller binding
```

The ledger tracks logical responsibility, not machine addresses.

### Assignment moves non-`Copy` values

```rust
let first = String::from("alpha");
let second = first;
```

After assignment, `second` owns the string. `first` is no longer usable. This prevents two owners from independently freeing the same allocation.

The compiler reports later use of `first` as a use-after-move. The move happens at assignment; the later line only reveals the conflict.

### Function arguments are assignments to parameters

```rust
fn consume(text: String) -> usize {
    text.len()
}

let title = String::from("ownership");
let length = consume(title);
```

Calling `consume(title)` moves the `String` into parameter `text`. It is dropped at function exit unless moved onward or returned. The caller cannot use `title` afterward.

Read a by-value parameter as: **the callee may retain, transform, return, or destroy this value; the caller transfers responsibility.**

### Returning transfers ownership outward

```rust
fn normalize(mut text: String) -> String {
    text.make_ascii_lowercase();
    text
}

let title = String::from("RUST");
let title = normalize(title);
```

Ownership moves into the function and then back in the returned value. Shadowing binds the returned owner to the same name. No text clone is required.

This consume-transform-return pattern is useful when a function legitimately takes exclusive responsibility for a value. Module 4 will show why borrowing is usually better for read-only access.

### Branches and ownership

```rust
let title = String::from("task");
let selected = if urgent { title } else { String::from("fallback") };
```

If the condition is runtime, `title` is considered moved because one possible executed path transfers it. It cannot be used after the `if` regardless of which branch happened in a particular run. Static validity must hold for all paths.

A value can be conditionally moved while still usable in a branch where the compiler proves it was not moved, but cross-branch use quickly becomes complex. Prefer clear ownership flow.

### Moves in loops

```rust
let title = String::from("once");
for _ in 0..2 {
    consume(title);
}
```

The first iteration would move `title`; the second would reuse a moved value. Rust rejects the loop because the body must be valid for every iteration.

Potential designs:

- create a new owned value each iteration when each consumer needs independent data;
- borrow one value each iteration when consumers only inspect it;
- move once outside the repeated loop;
- restructure the collection so each iteration owns a distinct element.

Cloning in the loop is correct only for the first case.

### Reinitialization after move

A moved binding can become usable again if assigned a new value before use:

```rust
let mut title = String::from("first");
consume(title);
title = String::from("second");
println!("{title}");
```

The name is reused, but the original value remains moved. Definite-initialization analysis ensures the new value exists before use.

### Move is type-directed

Generic code cannot assume an argument is copied:

```rust
fn identity<T>(value: T) -> T {
    value
}
```

`value` moves into and out of the function for arbitrary `T`. If `T` is `Copy`, the call syntax may leave the caller's source usable because copying occurs at the call site; the generic function's by-value contract still receives its own `T`.

### `Copy` is implicit bitwise duplication with semantic guarantees

Simple types such as integers, Booleans, characters, floating-point values, and shared references implement `Copy`.

```rust
let first = 7_u64;
let second = first;
println!("{first} {second}");
```

Assignment copies the value, so both bindings remain usable. The source is not invalidated.

A type can implement `Copy` only when it does not require custom destruction and all of its fields are `Copy`. `String` cannot be `Copy`: blindly duplicating its pointer metadata would create two owners of one allocation.

### `Clone` is explicit duplication

```rust
let first = String::from("alpha");
let second = first.clone();
```

Both strings own independent allocations/content after cloning. `.clone()` calls a trait method whose cost and behavior depend on the type. It may be cheap for small inline types or expensive for large recursive structures.

Explicitness is the point: duplication deserves review.

### A type may be `Clone` without `Copy`

`String` is cloneable but not copyable. Most owned collections follow this pattern when their elements can be cloned. A custom type may derive `Clone` while intentionally not deriving `Copy` to make duplication visible.

```rust
#[derive(Clone, Debug)]
struct Record {
    title: String,
}
```

Structs are formally taught in Module 5; here observe that cloning the record clones its owned string.

### When cloning is semantically required

Two components need independent ownership beyond the current call:

```rust
let title = String::from("Repair parser");
let task_title = title.clone();
let audit_snapshot = title;
```

If both task storage and an audit snapshot must survive independently and may diverge, duplication is real product behavior.

Often only one owned copy is needed and another consumer can format or inspect before movement:

```rust
let title = String::from("Repair parser");
println!("adding {title}");
store(title);
```

No clone.

### Clone as a design smell, not a ban

Flag a clone for review when:

- added immediately after a moved-value error;
- occurs in a loop;
- duplicates an entire collection;
- preserves a caller value although the callee only reads;
- hides a partial-move problem;
- appears at every API boundary.

Ask: **Which two owners must exist after this line, and how long must each live?** If no product answer exists, redesign.

### Copy bounds in generic code

```rust
fn duplicate<T: Copy>(value: T) -> (T, T) {
    (value, value)
}
```

The `Copy` bound proves implicit duplication is valid. Adding `T: Clone` instead would require explicit `value.clone()` and permit non-`Copy` types. Bounds are contracts, covered deeply in Module 8.

### Do not force `Copy` onto identity-bearing values

A small newtype ID can reasonably be `Copy`; duplicating an identifier does not duplicate the entity. A resource handle or mutable state owner should usually not be `Copy` even if its machine representation is small. Type semantics, not byte size, determine the choice.

### Tuples own their fields

```rust
let record = (1_u64, String::from("partial"));
let title = record.1;
```

Moving `record.1` transfers the `String` field. `record.0` remains usable because it is a separate `Copy` field, but the whole tuple can no longer be used as an intact value.

```rust
println!("{}", record.0); // valid
println!("{record:?}");   // invalid: record is partially moved
```

This is a **partial move**.

### Destructuring makes field movement explicit

```rust
let (id, title) = record;
```

Both fields leave the tuple. `id` is copied or moved according to its type; `title` is moved. The tuple is consumed as a whole pattern source.

Borrowing fields rather than moving them is introduced next module.

### Arrays and tuples move as values

An array is `Copy` only when its element type is `Copy` and length/type supports the implementation. An array of `String` values is moved by assignment.

```rust
let names = [String::from("a"), String::from("b")];
let moved = names;
```

`names` becomes unusable. Indexing an array element to move it has restrictions because leaving an uninitialized hole in an indexed aggregate is unsafe; collection APIs such as `remove`, `swap_remove`, or consuming iteration provide valid transfer patterns.

### Vectors own elements and a buffer

```rust
let tasks = vec![String::from("first"), String::from("second")];
```

The vector value owns its allocation, and each element owns its own resources. Moving the vector transfers the entire collection ownership without cloning each element.

```rust
fn process(tasks: Vec<String>) {
    // owns vector and all elements
}
```

Passing `Vec<T>` by value is a strong API statement: caller gives up the collection.

### Removing transfers one element

```rust
let mut tasks = vec![String::from("a"), String::from("b")];
let first = tasks.remove(0);
```

`first` now owns the removed `String`; the vector owns the remaining elements. `remove` shifts later elements. `swap_remove` can avoid order-preserving shifts but changes order. Module 6 studies collection tradeoffs.

### Moving between collections

```rust
let record = pending.remove(index);
completed.push(record);
```

The record is not cloned. Ownership moves from one vector element, into a local, then into the destination vector. This is the core of the Module 3 lab.

### Conditional extraction

Validate/index-find before removal:

```rust
let Some(index) = pending.iter().position(|record| record.0 == id) else {
    return (pending, completed, false);
};
let record = pending.remove(index);
completed.push(record);
```

Even before borrowing is formally covered, observe the sequencing: search first, mutate after the search result is obtained. Later, this avoids overlapping collection borrows.

### Aggregate drop

Dropping a vector drops its elements, which drop their owned resources. The programmer does not manually traverse and free strings. Ownership composes recursively.

A by-value signature should be deliberate, not the default copied from another language.

### Four common ownership shapes

#### Consume

```rust
fn archive(task: String) {
    // task ends here or moves onward
}
```

Use when the operation logically takes over the value.

#### Consume and return

```rust
fn normalize(mut title: String) -> String {
    title.make_ascii_lowercase();
    title
}
```

Use when exclusive transformation is appropriate and the caller should regain ownership.

#### Combine owned inputs into a new owner

```rust
fn record(id: u64, title: String) -> (u64, String) {
    (id, title)
}
```

The returned aggregate owns the title.

#### Split ownership

```rust
fn split(record: (u64, String)) -> (u64, String) {
    record
}
```

Destructuring can distribute fields to new owners.

Module 4 adds shared and mutable borrowing as two more shapes.

### The caller-use test

Before choosing by value, ask:

1. Does the callee store the value after return?
2. Does the callee destroy/replace it as part of product behavior?
3. Does exclusive transformation avoid a required copy?
4. Does the caller need the original value afterward?

If the callee only calculates length or prints, by-value ownership is excessive.

### Builder-like pipelines without borrowing

```rust
let title = normalize(raw_title);
let record = attach_id(title, 1);
let records = insert(records, record);
```

Each function consumes and returns ownership. This can be coherent for transformation pipelines, though it may become awkward when multiple parts need read access. Borrowing reduces unnecessary ownership shuttling.

### Preserve failure state

A by-value function can return original inputs on failure:

```rust
fn transfer(
    pending: Vec<Record>,
    completed: Vec<Record>,
    id: u64,
) -> (Vec<Record>, Vec<Record>, bool)
```

This signature is cumbersome but honest before borrowing. If transfer fails, both vectors are returned. A function that consumes collections and returns only `false` would destroy caller state on failure.

Module 4 replaces this shape with `&mut` collections, making preservation more natural.

### Ownership in error values

An error may own invalid input so the caller can inspect/recover it:

```rust
fn parse_title(input: String) -> Result<String, String> {
    if input.trim().is_empty() {
        Err(input)
    } else {
        Ok(input)
    }
}
```

Later, typed error enums can own context without conflating error and input types.

### Avoid “return everything” as permanent architecture

Consume-and-return is a bridge when borrowing is not yet available or exclusive transformation is genuinely desired. APIs that repeatedly return all inputs in giant tuples are hard to compose and signal missing reference-based design.

### Example: logging before transfer

Defective:

```rust
let stored = title.clone();
println!("adding {title}");
tasks.push(stored);
```

No two long-lived owners are needed. Print first, then move:

```rust
println!("adding {title}");
tasks.push(title);
```

### Example: independent snapshot

Justified:

```rust
let snapshot = board.clone();
apply_mutation(&mut board);
if save(&board).is_err() {
    board = snapshot;
}
```

This duplicates the complete board to implement rollback. It may be semantically valid but expensive. A better architecture might validate before mutation, write to a temporary file, or represent a transaction. The clone is justified yet still open to performance/design review.

### Resource types make cloning unavailable or meaningful

Many resources do not implement `Clone` because duplication is ambiguous or unsafe. A file may support an explicit `try_clone` operation with OS-defined behavior, not ordinary value cloning. A lock guard should not be duplicable. The type system prevents the clone workaround and forces an ownership decision.

### Clone can hide lifetime ignorance

Later, a common anti-pattern is returning owned `String` from a lookup because returning a borrowed `&str` seems difficult. Owned return may be correct when the result must outlive the source or be modified independently. Otherwise it duplicates storage and obscures the source relationship.

### Benchmarking is not the first question

Do not defend unnecessary clones with “performance probably does not matter.” Ownership clarity matters even for tiny data:

- duplicated state can diverge;
- hidden ownership obscures APIs;
- resources may be noncloneable;
- cost scales unexpectedly when data grows.

First establish semantic need; then measure cost if relevant.

### Clone count is not a quality metric

Zero clones is not inherently superior. A program that moves ownership through awkward APIs, recomputes expensive data, or introduces global mutation to avoid one justified clone can be worse. The target is **every clone explained**, not “clone-free at any cost.”

### Final ownership defense

For a function, be able to say:

- caller owns X before call;
- X moves into parameter Y;
- field Z moves into collection element;
- scalar ID copies because it is `Copy`;
- no duplicate title allocation is created;
- collection drops remaining records at scope exit.

This level of explanation becomes concise with practice.

## Use the idea in a complete program

The course capstone is **Taskboard**, a persistent command-line task board. Move owned task titles into board storage and document the owner after each operation. Avoid cloning simply because a caller's postcondition was never stated. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-03-ownership-intake/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 4 when you can:

- answer the module question—“Who owns each resource after every assignment, call, return, destructure, and scope exit?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Trace ownership through bindings, calls, returns, aggregates, and scopes using a move-path ledger;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [The Rust Book: Ownership](https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html)
- [Rust Reference: Destructors](https://doc.rust-lang.org/reference/destructors.html)

[← Module 2](../../../01-rust-foundations/course-book/module-02-control-flow-functions-and-invariants/index.md) · [ninety-module map](../../../COURSE_MAP.md) · [Module 4 →](../../../01-rust-foundations/course-book/module-04-borrowing-references-slices-and-strings/index.md)

## Continue

1. Complete the [Module 3 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 3 — Ownership Intake Pipeline](../../labs/module-03-ownership-intake/README.md) from its public contract.
3. Apply the Module 3 increment in the [Taskboard engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
