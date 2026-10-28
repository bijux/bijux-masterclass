# Reasoned Solutions — Module 04: Borrowing, References, Slices, and Strings

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-04-borrowed-catalog/README.md) · [Taskboard guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 4: Borrowing, References, Slices, and Strings**. Compare the reasoning against this question: *Which temporary permissions does an operation require, and how narrowly can those permissions be scoped?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `01-shared-then-mutable.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** shared borrow remains live across mutation.
- **Causal explanation:** The compiler rejects the specimen because shared borrow remains live across mutation.
- **Principled repair:** End the shared reference’s last use before mutation, or copy only the small durable fact needed after mutation.
- **Weak repair to reject:** Do not clone the whole owner merely to extend an observation.

### 2. `02-two-indexed-mutable-borrows.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** separate indexing does not prove disjoint mutable access.
- **Causal explanation:** The compiler rejects the specimen because separate indexing does not prove disjoint mutable access.
- **Principled repair:** Prove disjointness with `split_at_mut` or another API that returns nonoverlapping regions.
- **Weak repair to reject:** Do not use raw pointers or unchecked indexing to bypass an unproved aliasing condition.

### 3. `03-return-reference-to-local.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** returned reference would outlive local owner.
- **Causal explanation:** The compiler rejects the specimen because returned reference would outlive local owner.
- **Principled repair:** Return an owned value, or return a reference into storage supplied by and owned by the caller.
- **Weak repair to reject:** Do not leak or assign a fake `static` lifetime to local storage.

### 4. `04-mutate-during-iteration.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** iteration borrow overlaps structural mutation.
- **Causal explanation:** The compiler rejects the specimen because iteration borrow overlaps structural mutation.
- **Principled repair:** Separate traversal from structural mutation, for example by finding an index first and mutating afterward.
- **Weak repair to reject:** Do not collect unnecessary clones just to keep an iterator alive during mutation.

### 5. `05-slice-outlives-owner.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** slice is used after String owner drops.
- **Causal explanation:** The compiler rejects the specimen because slice is used after String owner drops.
- **Principled repair:** Keep the `String` owner alive for every use of the slice, or return owned text.
- **Weak repair to reject:** Do not transmute the slice lifetime or leak the string.

### 6. `06-reborrow.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** temporary reborrow and last-use analysis permit later mutation.
- **Causal explanation:** The specimen compiles because temporary reborrow and last-use analysis permit later mutation.
- **Principled repair:** No repair is required. Preserve the example and explain the exact type, ownership, or visibility rule that permits it.
- **Weak repair to reject:** Do not replace this demonstration—temporary reborrow and last-use analysis permit later mutation—with broader ownership, visibility, or allocation merely to make the reasoning easier.

## Exercise reasoning and worked answers
### 1. Signature classification rules

- callee stores value after return: `T` (or owns a clone explicitly requested by caller/product);
- print/measure/search only: `&T`, slice, or `&str`;
- mutate existing value: `&mut T`;
- mutate fixed elements: `&mut [T]`;
- push/remove vector elements: `&mut Vec<T>`;
- consume and transform identity: `T -> T`;
- independent snapshot: clone at the boundary where second ownership is created.

### 2. Borrowed length

```rust
pub fn length(text: &str) -> usize {
    text.len()
}

pub fn print_title(text: &str) {
    println!("{text}");
}
```

Caller:

```rust
let title = String::from("retained");
print_title(&title);
assert_eq!(length(&title), 8);
println!("{title}");
```

### 3. First word

```rust
pub fn first_word(text: &str) -> &str {
    text.split_whitespace().next().unwrap_or("")
}
```

The nonempty result is a slice into `text`; empty result is a static literal. No owned text is created.

### 4. Slice prefix

```rust
pub fn prefix<T>(values: &[T], count: usize) -> Option<&[T]> {
    values.get(..count)
}
```

The output lifetime is inferred from the single borrowed input.

### 5. Terminal period

```rust
pub fn ensure_terminal_period(text: &mut String) {
    if !text.ends_with('.') {
        text.push('.');
    }
}
```

Calling twice produces same final result. Empty becomes `"."`; if product policy rejects empty, validation belongs before this transformation.

### 6. Lookups

```rust
pub type Record = (u64, String);

pub fn find(records: &[Record], id: u64) -> Option<&Record> {
    records.iter().find(|record| record.0 == id)
}

pub fn find_mut(records: &mut [Record], id: u64) -> Option<&mut Record> {
    records.iter_mut().find(|record| record.0 == id)
}
```

### 7. Rename

```rust
pub fn rename(records: &mut [Record], id: u64, replacement: &str) -> bool {
    let Some(record) = find_mut(records, id) else {
        return false;
    };
    record.1.clear();
    record.1.push_str(replacement);
    true
}
```

The borrowed replacement is copied into storage because the record must own it after return; this is not a clone of an existing owned input.

### 8. Disjoint mutation

```rust
pub fn add_other(values: &mut [i32], first: usize, second: usize) -> bool {
    if first == second || first >= values.len() || second >= values.len() {
        return false;
    }
    let (low, high) = if first < second { (first, second) } else { (second, first) };
    let (left, right) = values.split_at_mut(high);
    let low_value = &mut left[low];
    let high_value = &mut right[0];
    *low_value += *high_value;
    true
}
```

This chooses which requested element receives the addition only if specification says “lower index receives higher.” If order matters, branch and name targets accordingly.

### 9. Removal variants

Discard removed values:

```rust
pub fn retain_nonempty(records: &mut Vec<Record>) {
    records.retain(|record| !record.1.is_empty());
}
```

Return removed ownership:

```rust
pub fn partition_nonempty(records: Vec<Record>) -> (Vec<Record>, Vec<Record>) {
    let mut kept = Vec::new();
    let mut removed = Vec::new();
    for record in records {
        if record.1.is_empty() {
            removed.push(record);
        } else {
            kept.push(record);
        }
    }
    (kept, removed)
}
```

Consuming iteration lets each record move to exactly one destination.

### 10. String audit

- `fn read(x: String)` → `fn read(x: &str)` when no ownership retained;
- `fn read(x: &String)` → `fn read(x: &str)` for broader callers;
- `fn append(x: String)` → `fn append(x: &mut String)` when caller-owned string identity remains;
- `fn store(x: &str)` may internally call `to_owned` because storage requires ownership;
- returning `String` is correct when result must survive input destruction or is newly constructed.

### Post-key transfer

Repair a catalog update that conflicts with an active search borrow by changing access topology rather than extending ownership.

## Reference implementation comparison

The complete laboratory implementation is in [`module-04-borrowed-catalog/solution`](../../labs/module-04-borrowed-catalog/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Borrowing, References, Slices, and Strings**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Model shared and mutable references as permissions constrained by aliasing and validity.
- Shorten borrow scopes, reborrow correctly, and split disjoint data instead of cloning or over-owning.
- Design slice-based APIs and distinguish String, str, &String, and &str by ownership and representation.
- Handle UTF-8 text without assuming character indexing or byte-boundary equivalence.
- Return borrowed views only when provenance remains valid and explain the source of every returned reference.

A complete explanation of **Borrowing, References, Slices, and Strings** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.

## Deep reasoning and transfer

### Decisive model

> Which temporary permissions does an operation require, and how narrowly can those permissions be scoped?

Build a **borrow map**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Model shared and mutable references as permissions constrained by aliasing and validity.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Shorten borrow scopes, reborrow correctly, and split disjoint data instead of cloning or over-owning.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Design slice-based APIs and distinguish String, str, &String, and &str by ownership and representation.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Handle UTF-8 text without assuming character indexing or byte-boundary equivalence.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Return borrowed views only when provenance remains valid and explain the source of every returned reference.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Model shared and mutable references as permissions constrained by aliasing and validity.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the borrow map.

### Laboratory transfer review

For [Borrowed Catalog](../../labs/module-04-borrowed-catalog/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In Taskboard, Module 4 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Borrowing, References, Slices, and Strings**, which relationship decides this question: “Which temporary permissions does an operation require, and how narrowly can those permissions be scoped?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to Taskboard?
