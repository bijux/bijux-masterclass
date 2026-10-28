# Reasoned Solutions — Module 11: Places, Move Paths, and Advanced Borrowing

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-01-borrow-surgery/README.md) · [Memory Workspace guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 11: Places, Move Paths, and Advanced Borrowing**. Compare the reasoning against this question: *Which places, projections, move paths, and loans are active at each program point, and how can access be decomposed safely?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `01-disjoint-fields.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Named fields can be borrowed independently.
- **Causal explanation:** The specimen compiles because named fields can be borrowed independently.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not replace a statically proved access pattern with cloning, global state, or runtime borrow checking.

### 2. `02-indexed-exclusive-borrows.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Two indexing operations do not prove disjointness.
- **Causal explanation:** The compiler rejects the specimen because two indexing operations do not prove disjointness.
- **Principled repair:** Order the two indices and use `split_at_mut` to obtain nonoverlapping regions before selecting each element.
- **Weak repair to reject:** Do not use raw pointers or unchecked indexing as a substitute for proving disjointness.

### 3. `03-split-at-mut-proof.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** split_at_mut returns nonoverlapping slices.
- **Causal explanation:** The specimen compiles because split_at_mut returns nonoverlapping slices.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not replace a statically proved access pattern with cloning, global state, or runtime borrow checking.

### 4. `04-partial-move-whole-use.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A partially moved struct cannot be used as a whole.
- **Causal explanation:** The compiler rejects the specimen because a partially moved struct cannot be used as a whole.
- **Principled repair:** Use the remaining fields individually after the partial move, borrow the moved field, or destructure the value completely.
- **Weak repair to reject:** Do not clone the moved field merely to preserve whole-struct syntax.

### 5. `05-reborrow-exclusive.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A mutable reference can be reborrowed for a shorter call.
- **Causal explanation:** The specimen compiles because a mutable reference can be reborrowed for a shorter call.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not replace a statically proved access pattern with cloning, global state, or runtime borrow checking.

### 6. `06-two-phase-method-borrow.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Method receiver reservation permits vec.push(vec.len()).
- **Causal explanation:** The specimen compiles because method receiver reservation permits vec.push(vec.len()).
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not replace a statically proved access pattern with cloning, global state, or runtime borrow checking.

### 7. `07-shared-loan-still-used.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A shared loan conflicts when it is used after mutation.
- **Causal explanation:** The compiler rejects the specimen because a shared loan conflicts when it is used after mutation.
- **Principled repair:** Finish the shared loan before mutation, or copy the small observation that must survive the write phase.
- **Weak repair to reject:** Do not clone the entire aggregate to keep one shared reference alive.

### 8. `08-separate-read-and-write-phases.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Copy durable evidence before mutation.
- **Causal explanation:** The specimen compiles because copy durable evidence before mutation.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not replace a statically proved access pattern with cloning, global state, or runtime borrow checking.

## Exercise reasoning and worked answers
### 1. Place classification

`record.count` and `record.title` are field projections. Reading `count` copies if its type is `Copy`; reading `title` moves if it is an owned non-`Copy` value. `&record.title` creates a shared loan of that field. `&mut records[2].count` projects through indexing and a field, creating an exclusive loan whose conflict surface may include the indexed container. `*handle` is a dereference projection; the surrounding context decides whether it is read, moved, or borrowed. The assignment to `pair.1` drops the old initialized field then stores the new value.

### 2. Partial move repair

Destructure the entire value:

```rust
fn dismantle(record: Record) -> (u64, Vec<u8>) {
    let Record { id, payload } = record;
    (id, payload)
}
```

The original struct is consumed and no longer usable. This is stronger and clearer than moving one field then trying to reuse a partially initialized aggregate.

### 3. `Drop` extraction

```rust
struct Packet {
    payload: Option<Vec<u8>>,
}

impl Packet {
    fn take_payload(&mut self) -> Option<Vec<u8>> {
        self.payload.take()
    }
}

impl Drop for Packet {
    fn drop(&mut self) {
        // cleanup can inspect a valid Option, present or absent
    }
}
```

`take` replaces the field with `None`, leaving a valid `Packet` for its destructor.

### 4. Two mutable elements

Use `split_at_mut` at the larger index and select the other from the left half. Return references in caller-requested order. Equal indices must fail because two mutable references would alias.

### 5. Borrow shortening

Capture only the information required for later logging before mutation. If the later log needs a small `Copy` ID, copy it. If it needs owned text after the owner may change, clone only that text with an explicit name. Do not clone the entire item.

### 6. Split `self`

Destructure the receiver:

```rust
let Self { queue, completed, metrics } = self;
let Some(job) = queue.pop() else { return Ok(None) };
let duration = job.duration();
completed.push(job);
metrics.record(duration);
```

Each field is borrowed separately, and the job is moved rather than referenced across mutation.

### 7. Read–validate–write phases

Read quantities through shared access, validate indices, inequality, availability, and target overflow, then acquire disjoint mutable references and perform only infallible arithmetic. Any design that mutates the source before checking the target is incomplete.

### 8. Reborrow trace

Each helper call receives a shorter `&mut *text`. The original mutable reference remains reserved for the outer function but becomes usable again after each call. Explicit `&mut *text` can make the sequence visible.

### 9. Receiver audit

The correct answer depends on required fields. A helper that formats metrics should take `&Metrics`; one that calculates a summary should return an owned summary; one that swaps two queue entries should take `&mut [Job]`; a state transition consuming the object may take `self`.

### 10. Clone audit

A valid solution removes clones whose only purpose is to retain access across a borrow. Required duplication remains and is documented. `Rc::clone` must be described as another owner, not a deep copy.

### Post-key transfer

Diagnose a composite-store transfer whose lookup and mutation overlap, then derive a failure-atomic split-borrow implementation.

## Reference implementation comparison

The complete laboratory implementation is in [`module-01-borrow-surgery/solution`](../../labs/module-01-borrow-surgery/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Places, Move Paths, and Advanced Borrowing**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Distinguish values from places and trace projections, move paths, partial initialization, and later destruction obligations.
- Model loans over places and explain when fields, indices, slices, and method receivers can or cannot be borrowed disjointly.
- Use reborrowing, non-lexical lifetime shortening, two-phase borrowing, and split APIs without relying on folklore.
- Sequence validation and mutation so failure does not expose prohibited partial state.
- Repair ownership conflicts by changing topology or phases before considering Clone, RefCell, or unsafe code.

A complete explanation of **Places, Move Paths, and Advanced Borrowing** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.

## Deep reasoning and transfer

### Decisive model

> Which places, projections, move paths, and loans are active at each program point, and how can access be decomposed safely?

Build a **place and move-path map**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Distinguish values from places and trace projections, move paths, partial initialization, and later destruction obligations.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Model loans over places and explain when fields, indices, slices, and method receivers can or cannot be borrowed disjointly.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Use reborrowing, non-lexical lifetime shortening, two-phase borrowing, and split APIs without relying on folklore.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Sequence validation and mutation so failure does not expose prohibited partial state.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Repair ownership conflicts by changing topology or phases before considering Clone, RefCell, or unsafe code.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Distinguish values from places and trace projections, move paths, partial initialization, and later destruction obligations.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the place and move-path map.

### Laboratory transfer review

For [Borrow Surgery](../../labs/module-01-borrow-surgery/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In Memory Workspace, Module 11 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Places, Move Paths, and Advanced Borrowing**, which relationship decides this question: “Which places, projections, move paths, and loans are active at each program point, and how can access be decomposed safely?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to Memory Workspace?
