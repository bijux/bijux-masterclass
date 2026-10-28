# Reasoned Solutions — Module 03: Ownership, Moves, Copying, and Destruction

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-03-ownership-intake/README.md) · [Taskboard guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 3: Ownership, Moves, Copying, and Destruction**. Compare the reasoning against this question: *Who owns each resource after every assignment, call, return, destructure, and scope exit?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `01-assignment-moves-string.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** assignment transfers String ownership.
- **Causal explanation:** The compiler rejects the specimen because assignment transfers String ownership.
- **Principled repair:** Borrow the string when the second binding only needs access, or deliberately move it and stop using the old owner.
- **Weak repair to reject:** Do not clone by reflex before deciding whether two independent owned strings are required.

### 2. `02-function-consumes-argument.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** owned argument is moved into the function.
- **Causal explanation:** The compiler rejects the specimen because owned argument is moved into the function.
- **Principled repair:** Change the callee to borrow when it only observes the value, or accept the ownership transfer and use the returned/remaining owner.
- **Weak repair to reject:** Do not clone at every call boundary to avoid choosing an ownership contract.

### 3. `03-partial-move.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** moving one non-Copy field prevents whole-value use.
- **Causal explanation:** The compiler rejects the specimen because moving one non-Copy field prevents whole-value use.
- **Principled repair:** Destructure the value and use its remaining fields individually, or borrow the field instead of moving it.
- **Weak repair to reject:** Do not clone the moved field merely to preserve whole-value syntax.

### 4. `04-copy-versus-owned-tuple.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** rejects only for the tuple containing String; Copy is structural.
- **Causal explanation:** The compiler rejects the specimen because rejects only for the tuple containing String; Copy is structural.
- **Principled repair:** Treat the tuple containing `String` as move-only, or borrow it; retain `Copy` expectations only for structurally `Copy` tuples.
- **Weak repair to reject:** Do not assume a tuple is `Copy` because some of its fields are.

### 5. `05-loop-move.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** first iteration consumes the value.
- **Causal explanation:** The compiler rejects the specimen because first iteration consumes the value.
- **Principled repair:** Borrow the value inside the loop, create a fresh owned value per iteration, or move it exactly once outside the repetition.
- **Weak repair to reject:** Do not clone on every iteration unless independent ownership is the actual requirement.

### 6. `06-explicit-drop.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** drop consumes its argument.
- **Causal explanation:** The compiler rejects the specimen because drop consumes its argument.
- **Principled repair:** Use the value before `drop`, or place `drop` exactly at the point where early destruction is intended.
- **Weak repair to reject:** Do not remove explicit destruction if releasing the resource early is part of the product behavior.

## Exercise reasoning and worked answers
### 1. Ownership trace method

For each line, use a table:

| Line | Value | Owner before | Operation | Owner after |
|---:|---|---|---|---|
| 1 | string allocation | temporary | bind | `title` |
| 2 | string allocation | `title` | assignment move | `archived` |
| 3 | same allocation | `archived` | shared formatting access | `archived` |

Do not write “both variables point to it” unless the type is a reference; assignment of `String` transfers ownership.

### 2. Consume-and-return pipeline

```rust
pub fn normalize(title: String) -> String {
    title.split_whitespace().collect::<Vec<_>>().join(" ")
}

pub fn tag(mut title: String, suffix: &str) -> String {
    title.push_str(suffix);
    title
}

pub fn pipeline(raw: String) -> String {
    let normalized = normalize(raw);
    tag(normalized, " [reviewed]")
}
```

One owned string moves through each stage. `join` creates a normalized allocation because whitespace segments are recombined; this is transformation cost, not a clone workaround.

### 3. Length three ways

```rust
pub fn length_consume(text: String) -> usize {
    text.len()
}

pub fn length_return(text: String) -> (String, usize) {
    let length = text.len();
    (text, length)
}

pub fn length_borrow(text: &str) -> usize {
    text.len()
}
```

The consuming caller loses the binding. The return variant regains ownership through a new returned value. The borrowed version is the correct ordinary contract when only length is needed.

### 4. Copy classification

- `u64`, `f64`, `char`, `&str`, `(u8, bool)`, `[u8; 16]`: `Copy`.
- `(u8, String)`, `[String; 2]`: not `Copy` because `String` is not `Copy`.

A shared reference copies the reference value, not the referenced data.

### 5. Partial move

```rust
let record = (1_u64, String::from("title"), true);
let title = record.1;
println!("{} {}", record.0, record.2);
println!("{title}");
```

Whole `record` use is invalid. Destructure instead:

```rust
let (id, title, active) = record;
println!("{id} {title} {active}");
```

### 6. Drop order

For locals `a`, then nested `b`, `c`, then outer `d`, normal scope exit drops `c`, `b`, then `d`, `a` according to reverse local declaration within each scope. Early explicit `drop(b)` changes the point for `b`. Treat this as ordinary lexical resource reasoning, not a substitute for explicit protocols.

### 7. Vector transfer

```rust
pub type Record = (u64, String);

pub fn transfer(
    mut pending: Vec<Record>,
    mut completed: Vec<Record>,
    id: u64,
) -> (Vec<Record>, Vec<Record>, bool) {
    let Some(index) = pending.iter().position(|record| record.0 == id) else {
        return (pending, completed, false);
    };
    let record = pending.remove(index);
    completed.push(record);
    (pending, completed, true)
}
```

The title moves as part of the record; no duplicate allocation is created.

### 8. Clone audit categories

- **Order-removable:** value only needs observation before move.
- **Borrow-removable:** callee only reads or temporarily mutates.
- **Ownership-redesign:** API consumes although caller retains responsibility.
- **Snapshot candidate:** independent state must survive and possibly diverge.
- **True duplication:** two product entities own equal initial data.

The answer is the explanation for each call site, not a target count.

### 9. Conditional move

```rust
pub fn choose(input: String, use_input: bool) -> String {
    if use_input {
        input
    } else {
        String::from("fallback")
    }
}
```

`input` is owned by the function on entry regardless of branch. The caller already transferred it at the call; branch behavior only decides whether it becomes the return value or is dropped.

### 10. Resource narrative

A correct narrative distinguishes vector allocation, record values, and each title allocation. The vector owns records; records own titles. Removal transfers one record to a local; push transfers it into another vector. Returning moves the vector to the caller. Dropping either vector recursively drops remaining records and titles.

### Post-key transfer

Refactor an ingest pipeline so ownership crosses each boundary once, then defend every remaining clone as semantic duplication.

## Reference implementation comparison

The complete laboratory implementation is in [`module-03-ownership-intake/solution`](../../labs/module-03-ownership-intake/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Ownership, Moves, Copying, and Destruction**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Trace ownership through bindings, calls, returns, aggregates, and scopes using a move-path ledger.
- Distinguish semantic moves, Copy duplication, explicit Clone cost, and destruction without relying on stack-versus-heap folklore.
- Predict partial moves and the remaining usable fields of an aggregate.
- Choose consuming, returning, borrowing, or cloning APIs from post-call ownership requirements.
- Audit clone-heavy code and remove symptom-fixing duplication while preserving the product contract.

A complete explanation of **Ownership, Moves, Copying, and Destruction** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.

## Deep reasoning and transfer

### Decisive model

> Who owns each resource after every assignment, call, return, destructure, and scope exit?

Build a **ownership ledger**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Trace ownership through bindings, calls, returns, aggregates, and scopes using a move-path ledger.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Distinguish semantic moves, Copy duplication, explicit Clone cost, and destruction without relying on stack-versus-heap folklore.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Predict partial moves and the remaining usable fields of an aggregate.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Choose consuming, returning, borrowing, or cloning APIs from post-call ownership requirements.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Audit clone-heavy code and remove symptom-fixing duplication while preserving the product contract.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Trace ownership through bindings, calls, returns, aggregates, and scopes using a move-path ledger.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the ownership ledger.

### Laboratory transfer review

For [Ownership Intake Pipeline](../../labs/module-03-ownership-intake/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In Taskboard, Module 3 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Ownership, Moves, Copying, and Destruction**, which relationship decides this question: “Who owns each resource after every assignment, call, return, destructure, and scope exit?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to Taskboard?
