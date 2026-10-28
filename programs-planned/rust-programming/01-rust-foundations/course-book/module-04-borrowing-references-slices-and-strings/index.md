# 04 — Borrowing, References, Slices, and Strings

**Course 1, day 4 · Module 4 of 60**  
`█░░░░░░░░░░░░░░░░░░░` **4/60**

[← Module 3: Ownership, Moves, Copying, and Destruction](../module-03-ownership-moves-copying-and-destruction/index.md) · [Course 1 overview](../index.md) · [Sixty-module map](../../../COURSE_MAP.md) · [Module 5: Structs, Enums, Methods, and Pattern Matching →](../module-05-structs-enums-methods-and-pattern-matching/index.md)

## The question

> Which temporary permissions does an operation require, and how narrowly can those permissions be scoped?

## Why this comes now

Moving every value would make useful APIs clumsy. Borrowing introduces temporary access without transferring destruction responsibility, but only after ownership itself is stable. Slices then show why a borrowed view can be more expressive than a borrowed container and why string APIs must respect UTF-8 rather than pretend text is an array of characters.

## What you will be able to do

- Model shared and mutable references as permissions constrained by aliasing and validity.
- Shorten borrow scopes, reborrow correctly, and split disjoint data instead of cloning or over-owning.
- Design slice-based APIs and distinguish String, str, &String, and &str by ownership and representation.
- Handle UTF-8 text without assuming character indexing or byte-boundary equivalence.
- Return borrowed views only when provenance remains valid and explain the source of every returned reference.

## Core model

### Why this module exists

Ownership answers who is responsible for a value. Borrowing answers who may temporarily access it and with which permissions. The most productive mental model is not “references are pointers”; it is “a borrow grants a scoped capability over a place while the owner remains responsible for storage.”

### Shared and exclusive permissions

A shared reference `&T` permits observation according to `T`'s API. Multiple shared borrows can coexist. A mutable reference `&mut T` grants exclusive access for its active use: while that loan is active, competing accesses to the same place are restricted.

The rule is about aliases and operations, not about whether code text contains an assignment. A function taking `&mut T` receives exclusive capability even if one branch does not mutate. Conversely, some types in Course 2 can mutate internal state through `&self` using controlled interior mutability; `&T` does not universally imply that no bits change.

### Borrow scopes and reborrowing

```rust
fn append_marker(text: &mut String) {
    let length = text.len();
    text.push_str(" #");
    text.push_str(&length.to_string());
}
```

The immutable access for `len()` ends before mutation because the resulting `usize` is owned. Non-lexical lifetimes allow a borrow to end at its last use rather than necessarily at the end of the textual block. This is not permission for overlap; it is more precise scope analysis.

When a function receives `&mut T`, passing it to another function usually creates a shorter **reborrow** rather than permanently moving the original reference:

```rust
fn clear_then_len(text: &mut String) -> usize {
    clear(text);      // shorter reborrow
    text.len()        // original capability usable again
}

fn clear(text: &mut String) {
    text.clear();
}
```

### Disjoint data

The compiler can often see that named struct fields are disjoint, but dynamic indices require proof. This does not compile:

```rust,compile_fail
fn swap_bad(values: &mut [i32], a: usize, b: usize) {
    let left = &mut values[a];
    let right = &mut values[b];
    std::mem::swap(left, right);
}
```

Even if `a != b` at runtime, the indexing operations do not encode disjointness. Use `slice::swap`, or split at a boundary and index each disjoint subslice. The right repair changes the access topology; cloning the values would change semantics and cost.

### Slices are borrowed views

A slice `&[T]` contains a pointer to elements plus a length and does not own the allocation. Accept a slice when an operation needs a contiguous borrowed sequence regardless of whether the owner is a vector, array, or boxed slice.

```rust
pub fn first_negative(values: &[i64]) -> Option<&i64> {
    values.iter().find(|&&value| value < 0)
}
```

The returned reference borrows from `values`; it cannot outlive the underlying owner. The signature does not create that relationship—it exposes and constrains it.

### String layers

`String` is an owned, growable UTF-8 byte buffer. `str` is an unsized UTF-8 string slice; it normally appears behind `&str`, `Box<str>`, or another pointer. Prefer `&str` for read-only text parameters because callers can provide a borrowed `String`, a literal, or another string slice.

“Character” is ambiguous:

- bytes: `as_bytes()`;
- Unicode scalar values: `chars()`;
- grapheme clusters: requires a Unicode segmentation algorithm/crate;
- displayed columns: depends on rendering and width rules.

Rust does not permit integer indexing into strings because an arbitrary byte offset may not be a UTF-8 boundary and “the nth character” is not a constant-time operation under variable-width encoding.

### Worked derivation: catalog update

```rust
#[derive(Debug, PartialEq, Eq)]
pub struct Item {
    id: u64,
    name: String,
    count: u32,
}

pub fn find(items: &[Item], id: u64) -> Option<&Item> {
    items.iter().find(|item| item.id == id)
}

pub fn increment(items: &mut [Item], id: u64) -> bool {
    let Some(item) = items.iter_mut().find(|item| item.id == id) else {
        return false;
    };
    item.count = item.count.saturating_add(1);
    true
}
```

The query borrows shared access; the update borrows exclusive access. Returning `Option<&mut Item>` could be useful if the caller should control mutation, but it also exposes a broader mutation capability. The boolean API preserves a narrower invariant: only count increments.

### Try without the scaffold

Write `find_title(items: &[Item], id: u64) -> Option<&str>` and derive the provenance. Then write `rename(items: &mut [Item], id: u64, title: &str) -> bool` without cloning until the matching item is found. Explain which allocation is unavoidable if the item must retain the new title.

### Misconception clinic

- **“`&mut` means mutation happens.”** It means exclusive capability is granted.
- **“`&String` is more specific and therefore safer.”** It unnecessarily restricts callers when only string contents are needed.
- **“NLL relaxes aliasing.”** It shortens proven loan duration; it does not permit simultaneous conflicting access.
- **“UTF-8 strings are arrays of characters.”** They are byte sequences satisfying UTF-8 validity.

### A shared reference grants temporary read access

```rust
fn length(text: &String) -> usize {
    text.len()
}

let title = String::from("borrow");
let count = length(&title);
println!("{title}: {count}");
```

`&title` creates a shared reference. Ownership remains with `title`; the function receives temporary access. When the call ends and no reference remains in use, the owner is freely usable again.

For text, prefer `&str` rather than `&String`; that refinement appears later in this module.

### Many readers can coexist

```rust
let title = String::from("shared");
let first = &title;
let second = &title;
println!("{first} {second}");
```

Both shared references can read because neither can mutate through ordinary safe operations. The invariant is that shared observations are not invalidated by concurrent mutation through the same access path.

This is the foundation of Rust's aliasing discipline:

> For an overlapping value region and active interval: many shared accesses, or one exclusive mutable access.

### References are values

A shared reference such as `&String` or `&str` is itself a value and is usually `Copy`. Copying the reference creates another alias, not another `String` allocation.

```rust
let first = &title;
let second = first;
println!("{first} {second}");
```

The owner remains `title`. Both references are constrained by the owner's lifetime.

### Dereference and method calls

```rust
fn is_empty(text: &String) -> bool {
    (*text).len() == 0
}
```

The explicit `*` dereferences the reference. Method-call syntax performs automatic referencing/dereferencing where unambiguous, so `text.is_empty()` is idiomatic.

Do not interpret auto-deref as ownership transfer. The receiver type of a method determines whether it borrows, mutably borrows, or consumes `self`.

### Shared references prevent overlapping mutation

```rust
let mut title = String::from("draft");
let view = &title;
title.push('!');
println!("{view}");
```

This fails because `view` is used after the mutation. Its shared borrow must remain active until that final use, while `push` requires exclusive mutable access to the string. The risk is concrete: `push` may reallocate, invalidating a pointer into the old buffer.

Move the final shared use before mutation:

```rust
println!("{view}");
title.push('!');
```

Now the compiler can end the shared borrow after its final use.

### Borrowing a field

```rust
let title = &record.1;
println!("{title}");
```

The reference borrows the field/aggregate region. Depending on later operations, mutation of disjoint fields may be allowed because the compiler can reason about field separation. Indexing into collections is harder because indices may alias at runtime; APIs such as `split_at_mut` prove disjointness.

### References are not ownership insurance

A reference cannot outlive the owner. Borrowing does not make a value immortal or garbage-collected. It creates a statically checked relationship: every use of the reference occurs while the source remains valid.

### `&mut T` grants exclusive temporary access

```rust
fn append_mark(text: &mut String) {
    text.push('!');
}

let mut title = String::from("draft");
append_mark(&mut title);
println!("{title}");
```

Ownership remains with `title`, but the callee receives exclusive access during the borrow. The owner cannot be used in conflicting ways while that access remains active.

### Exclusivity is stronger than mutation

Even if code only reads through `&mut T`, the reference carries exclusive capability. This permits APIs to rely on no competing aliases and enables optimization/safety properties.

```rust
let access = &mut title;
println!("{}", access.len());
```

`access` is still mutable/exclusive even if this statement reads.

### One overlapping mutable reference

```rust
let first = &mut value;
let second = &mut value; // rejected while first remains active
```

Two mutable references could write/read the same region without coordination. Safe Rust requires proof of disjointness.

For arrays/slices, indexing alone may not prove disjointness:

```rust
let first = &mut values[0];
let second = &mut values[1];
```

Use a splitting API:

```rust
let (left, right) = values.split_at_mut(1);
let first = &mut left[0];
let second = &mut right[0];
```

The API's contract proves the slices do not overlap.

### Mutation through iteration

```rust
for value in &mut values {
    *value *= 2;
}
```

The loop owns one mutable borrow of the slice/vector for traversal and yields one mutable reference to each element sequentially. You cannot push into the vector during iteration because push needs separate mutable access to the vector and may reallocate.

### Exclusive access can be shortened

```rust
let access = &mut title;
access.push('!');
println!("{access}");
// access final use above
title.push('?');
```

Non-lexical lifetime analysis can end the borrow after final use, before the closing brace. An explicit nested scope is still useful when humans or the compiler need a clear boundary:

```rust
{
    let access = &mut title;
    access.push('!');
}
title.push('?');
```

### Replace versus mutate

A function taking `&mut String` can change the caller's existing string. A function taking `String` can consume and return a replacement. Choose based on responsibility:

```rust
fn normalize_in_place(text: &mut String) { /* caller retains identity */ }
fn into_normalized(text: String) -> String { /* transformation transfers ownership */ }
```

The in-place version may avoid allocation for some operations but exposes mutation. The owned version can be easier to compose. Neither is universally superior.

### `&mut` is not “pass by reference” in a vague sense

The signature states exclusivity, not merely implementation efficiency. A caller cannot assume a function with `&mut T` only reads; it has permission to mutate any reachable state allowed by the type.

### Borrow lifetime is about use, not braces alone

```rust
let view = &title;
println!("{view}");
title.push('!');
```

The shared borrow ends after `view`'s final use, even though the binding remains lexically in scope. This is non-lexical lifetime behavior: compiler analysis tracks the region over which the reference must remain valid.

Do not say “references live until the end of the block” as a universal rule. Their validity requirement extends through possible uses; the binding's scope and active borrow interval can differ.

### Reborrowing a mutable reference

```rust
fn append_mark(text: &mut String) {
    text.push('!');
}

let access = &mut title;
append_mark(access);
println!("{access}");
```

The call does not permanently move `access` in the ordinary case. The compiler creates a shorter reborrow `&mut *access` for the call, allowing `access` to be used afterward once the callee borrow ends.

This is why passing `&mut T` repeatedly is practical despite references being values. Context selects reborrowing semantics.

### Returning a reference

```rust
fn first(values: &[i32]) -> Option<&i32> {
    values.first()
}
```

The returned reference points into caller-owned input. It remains usable only while the input remains valid and not conflictingly mutated. Lifetime elision infers this single-input relationship; Module 8 makes it explicit when multiple sources exist.

### Cannot return reference to a local owner

```rust
fn title() -> &str {
    let text = String::from("temporary");
    &text
}
```

This fails because `text` is destroyed at function exit. A lifetime annotation could describe a relationship but cannot make the local allocation outlive the function.

Correct choices:

- return owned `String`;
- return a reference to caller-provided storage;
- return a string literal with `'static` lifetime when the content is fixed;
- store the value in a longer-lived owner and borrow from it.

### Borrowed return constrains later mutation

```rust
let first = first_word(&title);
title.push('!');
println!("{first}");
```

If `first` points into `title`, mutation conflicts until `first`'s final use. Returning a borrow is allocation-free but ties caller operations to the source.

An owned return may be correct when the result must survive source mutation/destruction. API design balances allocation/independence against borrowing relationships.

### `let` binding can extend temporary lifetime in limited cases

Rust has precise temporary lifetime extension rules, but Course 1 avoids depending on subtle cases. Bind owned values clearly before borrowing and never assume a reference can outlive an expression-created owner without checking the language rule.

### Visualizing intervals

```text
owner title:  |-------------------------------|
view borrow:       |-----------last use|
mutation:                              |--|
```

Conflicts occur when incompatible intervals overlap over the same region.

### Slice type

A slice `[T]` is a dynamically sized contiguous sequence. It is normally used behind a reference:

- `&[T]`: shared borrowed sequence;
- `&mut [T]`: exclusively borrowed mutable sequence.

A slice reference carries enough information to identify a starting location and length. It does not own the elements.

### Array and vector coercion

```rust
fn total(values: &[i32]) -> i32 {
    values.iter().sum()
}

let array = [1, 2, 3];
let vector = vec![4, 5, 6];
println!("{}", total(&array));
println!("{}", total(&vector));
```

Both can be borrowed as slices. The function does not care whether storage came from an array, vector, or subslice.

### Subslice ranges

```rust
let middle = &values[1..4];
```

The range is checked against length at runtime. Invalid bounds panic. When input may be untrusted or bounds computed dynamically, use `get`:

```rust
let middle = values.get(1..4); // Option<&[T]>
```

This makes out-of-range behavior recoverable absence.

### Slice API versus vector API

Use `&[T]` when the function:

- reads elements;
- does not need capacity;
- does not push/remove/reallocate;
- should accept arrays and vectors.

Use `&mut [T]` when it mutates/reorders existing elements without changing length.

Use `&mut Vec<T>` when it must change length/capacity through vector operations. Use `Vec<T>` when it takes ownership.

```rust
fn sort_existing(values: &mut [i32]) {
    values.sort();
}

fn append_default(values: &mut Vec<i32>) {
    values.push(0);
}
```

The narrower slice signature communicates fewer capabilities and supports more callers.

### Split for disjoint access

```rust
let (left, right) = values.split_at_mut(midpoint);
```

This safely produces two nonoverlapping mutable slices. The borrow checker trusts the standard API's implementation/contract; callers gain two exclusive references to disjoint regions, not two to the same slice.

### Returning subslices

```rust
fn prefix(values: &[i32], count: usize) -> Option<&[i32]> {
    values.get(..count)
}
```

The result borrows from `values`. No elements are copied. The caller cannot mutate the overlapping source while using the prefix.

### Empty slices

Empty slices are valid. Functions should define empty behavior explicitly. A total sum can return zero; a first-element lookup returns `None`; sorting is a no-op.

### Owned versus borrowed text

`String` is an owned, growable UTF-8 string. `str` is a string slice type, normally used as `&str`.

```rust
let owned = String::from("Rust");
let borrowed: &str = &owned;
let literal: &'static str = "Rust";
```

A string literal is embedded in the program and has `'static` lifetime. Borrowing a `String` as `&str` exposes its text without transferring or duplicating ownership.

### Prefer `&str` for read-only text parameters

```rust
fn word_count(text: &str) -> usize {
    text.split_whitespace().count()
}
```

Callers can pass:

```rust
word_count("literal");
word_count(&owned_string);
word_count(&owned_string[0..4]);
```

A parameter `&String` unnecessarily excludes literals and arbitrary string slices while using no extra capability.

### Mutation requires `&mut String`

`str` is dynamically sized and not independently growable. To append or change allocation-backed text:

```rust
fn add_period(text: &mut String) {
    if !text.ends_with('.') {
        text.push('.');
    }
}
```

A mutable `&mut str` can mutate bytes only under UTF-8-preserving APIs and cannot change length; it is uncommon in beginner APIs.

### Why no integer string indexing

UTF-8 uses variable-width byte sequences. For `"é"`:

- `len()` is 2 bytes;
- `chars().count()` is 1 Unicode scalar value.

Indexing `text[0]` would be ambiguous: byte, Unicode scalar, or user-perceived grapheme cluster? Rust requires explicit iteration or slicing at valid byte boundaries.

```rust
for character in text.chars() {
    println!("{character}");
}

for byte in text.bytes() {
    println!("{byte}");
}
```

Grapheme clusters such as some emoji or combined accents require Unicode-segmentation logic beyond the standard library and this course.

### Slicing strings

```rust
let ascii = "hello";
let prefix = &ascii[..2]; // "he"
```

String slice ranges are byte ranges and must fall on UTF-8 boundaries. `&"é"[..1]` panics because byte 1 splits the encoding. Use safe methods (`get`) when boundaries are not guaranteed.

### Borrowed substrings

```rust
fn first_word(text: &str) -> &str {
    text.split_whitespace().next().unwrap_or("")
}
```

The returned slice points into the input or is a static empty literal. No allocation. Its use remains tied to input validity.

### Normalization and allocation

`trim()` returns a borrowed `&str`; it does not allocate. `to_lowercase()` returns a new `String` because Unicode lowercasing may change length and content. `split_whitespace().collect::<Vec<_>>().join(" ")` allocates normalized owned text.

Distinguish views from transformations:

```rust
let trimmed: &str = input.trim();
let lowercase: String = input.to_lowercase();
```

### Search semantics

`to_lowercase().contains(...)` is a Unicode lowercase-based search, not full locale-aware case folding. Course examples describe this honestly. Product requirements involving human language need a more precise Unicode/search specification.

When borrowing fails, classify the conflict before editing.

### Pattern 1 — Callee asks for ownership but only reads

Before:

```rust
fn print_title(title: String) {
    println!("{title}");
}
```

After:

```rust
fn print_title(title: &str) {
    println!("{title}");
}
```

This removes transfer and caller cloning. The repair is an API correction.

### Pattern 2 — Shared reference used after mutation

Before:

```rust
let view = &title;
title.push('!');
println!("{view}");
```

Repair by reordering final use, shortening scope, or creating an owned snapshot only if independence is required.

### Pattern 3 — Need find then mutate one element

```rust
fn find_mut(records: &mut [Record], id: u64) -> Option<&mut Record> {
    records.iter_mut().find(|record| record.id == id)
}
```

Perform one traversal yielding one mutable reference. Avoid taking an immutable result then searching/mutating while the immutable reference is still used.

### Pattern 4 — Need two disjoint mutable elements

Use `split_at_mut`, or an API such as `get_many_mut` where available/appropriate, to prove disjointness. Unsafe pointer arithmetic is outside this course.

### Pattern 5 — Mutate collection while iterating

Separate phases:

```rust
let ids_to_remove = records
    .iter()
    .filter(|record| should_remove(record))
    .map(|record| record.id)
    .collect::<Vec<_>>();

records.retain(|record| !ids_to_remove.contains(&record.id));
```

Or use a purpose-built one-pass method such as `retain`:

```rust
records.retain(|record| !should_remove(record));
```

Choose based on whether removed values/IDs are needed. Do not push/remove through a vector while an iterator borrow is active.

### Pattern 6 — Return local reference

Return ownership instead:

```rust
fn title() -> String {
    String::from("owned result")
}
```

Or borrow caller storage:

```rust
fn normalized_view(input: &str) -> &str {
    input.trim()
}
```

A lifetime annotation is not a storage allocation.

### Pattern 7 — Method chain extends temporary/borrow unexpectedly

Break the chain into named steps and inspect receiver/output types. A method may return a reference tied to its receiver; using it later can keep the receiver borrowed.

### Pattern 8 — Clone “fix”

Before accepting clone, write the two-owner requirement. If the second owner exists only because an API takes `String`, change the API. If a returned value must outlive its source, owned duplication may be correct.

### Repair decision tree

```text
Does callee need ownership after return?
├─ yes → move/own; clone only for two independent owners
└─ no
   ├─ only reads → &T / &[T] / &str
   └─ mutates
      ├─ changes existing value only → &mut T / &mut [T]
      └─ changes vector length/capacity → &mut Vec<T>
```

### Review lens: copy the fact, not the owner

A long borrow often exists because the code retains a reference after extracting a small fact. Prefer computing the needed `bool`, index, identifier, or count inside a narrow scope and carrying that copied fact into the next phase. This is not a workaround: it replaces broad capability over an object with the exact information the later operation needs. Do not apply the pattern when later code genuinely needs to mutate or inspect the same object; in that case redesign the phases or use a suitable collection API.

## Use the idea in a complete program

The course capstone is **Taskboard**, a persistent command-line task board. Refactor read operations to borrow the board and updates to use one narrow mutable path. The signatures should make inspection, mutation, and ownership transfer visibly different. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-04-borrowed-catalog/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 5 when you can:

- answer the module question—“Which temporary permissions does an operation require, and how narrowly can those permissions be scoped?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Model shared and mutable references as permissions constrained by aliasing and validity;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [The Rust Book: References and Borrowing](https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html)
- [The Rust Book: Slices](https://doc.rust-lang.org/book/ch04-03-slices.html)

[← Module 3](../../../01-rust-foundations/course-book/module-03-ownership-moves-copying-and-destruction/index.md) · [sixty-module map](../../../COURSE_MAP.md) · [Module 5 →](../../../01-rust-foundations/course-book/module-05-structs-enums-methods-and-pattern-matching/index.md)

## Continue

1. Complete the [Module 4 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 4 — Borrowed Catalog](../../labs/module-04-borrowed-catalog/README.md) from its public contract.
3. Apply the Module 4 increment in the [Taskboard engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
