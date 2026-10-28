# Reasoned solutions — Module 36: Custom Iterators and Collection Protocols

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the LedgerFlow engineering guide](../capstone.md)

Use these explanations to review your reasoning about **Custom Iterators and Collection Protocols**, not to substitute for an attempt. The decisive question is: *What laws must a custom traversal obey, and who owns the collection when iteration begins?* When your design differs, separate three possibilities: a Rust rule was applied incorrectly, the product contract changed, or two architectures satisfy the same contract with different trade-offs.

## Compiler specimen reasoning

### 1. `case-01.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** a custom iterator stores exactly the state needed by next.
- **Causal explanation:** The specimen compiles because a custom iterator stores exactly the state needed by next.
- **Principled repair:** encode one lawful state machine
- **Weak repair to reject:** recompute the sequence from the beginning on every next

### 2. `case-02.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** an iterator cannot yield a static reference to a local temporary.
- **Causal explanation:** The compiler rejects the specimen because an iterator cannot yield a static reference to a local temporary.
- **Principled repair:** store the data in the iterator or yield owned String
- **Weak repair to reject:** leak every String to manufacture static references

### 3. `case-03.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** IntoIterator for a shared reference defines borrowed traversal.
- **Causal explanation:** The specimen compiles because intoIterator for a shared reference defines borrowed traversal.
- **Principled repair:** provide owned and borrowed modes only when meaningful
- **Weak repair to reject:** expose the internal Vec publicly

### 4. `case-04.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** two implementations for the same trait/type relationship conflict.
- **Causal explanation:** The compiler rejects the specimen because two implementations for the same trait/type relationship conflict.
- **Principled repair:** keep one implementation and encode alternate behavior as a named method
- **Weak repair to reject:** use conditional compilation to hide accidental overlap

### 5. `case-05.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** FusedIterator promises permanent exhaustion.
- **Causal explanation:** The specimen compiles because fusedIterator promises permanent exhaustion.
- **Principled repair:** implement FusedIterator only after proving the law
- **Weak repair to reject:** add the marker to silence a generic bound

### 6. `case-06.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** FromIterator defines an eager collection target.
- **Causal explanation:** The specimen compiles because fromIterator defines an eager collection target.
- **Principled repair:** implement the exact item relationship users need
- **Weak repair to reject:** accept every item through ToString and hide conversions

### 7. `case-07.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** collect item type must match the target FromIterator implementation.
- **Causal explanation:** The compiler rejects the specimen because collect item type must match the target FromIterator implementation.
- **Principled repair:** map str::to_owned or implement a justified borrowed relationship
- **Weak repair to reject:** add a blanket conversion that obscures allocation

### 8. `case-08.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Extend supports incremental growth from a matching item stream.
- **Causal explanation:** The specimen compiles because extend supports incremental growth from a matching item stream.
- **Principled repair:** implement Extend consistently with FromIterator
- **Weak repair to reject:** rebuild the collection from scratch on every append

## Exercise reasoning

### Exercise 1 — Design `next` from state

Use `current: Option<i64>` and `end: i64`, or a current value plus explicit `done` flag. If `current > end`, return `None` permanently. Yield the current value; if it equals end, mark done. Otherwise use `checked_add(1)` and mark done on impossible overflow. An explicit option state avoids wrapping from `i64::MAX` to a negative number. Tests need empty, singleton, ordinary, maximum-boundary, repeated-`None`, and partial-consumption cases.

### Exercise 2 — Choose receiver implementations

Owned traversal yields `T` and consumes the bag. Shared traversal yields `&T` tied to the borrow. Mutable traversal yields `&mut T` and permits callers to mutate elements. Omit the mutable form when direct element mutation could violate collection invariants, such as uniqueness, sort order, or key consistency. Providing all three forms is not automatically idiomatic; each is a public capability.

### Exercise 3 — Fallible invariants and `FromIterator`

Ordinary `FromIterator<String>` cannot return `Result`, so it cannot honestly report duplicate failure. It could silently keep first/last, panic, or alter the item type to `Result`, but those are different contracts. Prefer `TryFromIterator` as a domain method such as `UniqueNames::try_from_iter`, collect into a neutral vector and validate, or implement `FromIterator` only if duplicates have a documented non-failing policy. Do not hide fallibility to gain `.collect()` syntax.

### Exercise 4 — Extend and partial mutation

`Extend` returns `()`, so it has no channel for the first rejected item and may already have inserted earlier records. An atomic alternative validates the full input into an owned candidate before committing, or exposes `try_extend` returning a typed failure with unchanged state or a surviving candidate. Implement `Extend` only for an infallible subset or a documented best-effort policy.

### Exercise 5 — Validate `size_hint`

Without additional knowledge, at least `lower / 3` complete groups are guaranteed, while the upper bound is `upper.map(|n| n.div_ceil(3))` if the adapter yields the first item of each three-item block. Exact formulas depend on phase state—how many upstream items have already been consumed inside the current block. The lower bound must never exceed actual remaining yields, and the upper bound must never be lower. Tests should compare reported bounds against actual remaining count over many small sequences and partial states.

### Exercise 6 — Custom adapter law review

The adapter owns upstream iterator, predicate, and a `done` flag. On each `next`, it pulls one item; if predicate passes, yield it. If predicate fails, set `done` and return `None`. The failing item is consumed. Because `done` prevents future upstream calls, the adapter is fused regardless of whether upstream is fused. If the product must preserve the failing item, this adapter is the wrong protocol; use peeking or a splitter that returns the remainder.



## Laboratory comparison

The complete laboratory implementation is in [`module-06-custom-cursors/solution`](../../labs/module-06-custom-cursors/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Custom Iterators and Collection Protocols**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Implement a correct custom `Iterator` by defining state and exhaustion behavior.
- Provide owned, shared, and mutable `IntoIterator` implementations only where their semantics are useful.
- Implement `FromIterator` and `Extend` for a domain collection with explicit invariant policy.
- Implement stronger iterator traits only when every required law holds.
- Design `size_hint` as a truthful bound and not as an unsupported performance promise.

A complete explanation of **Custom Iterators and Collection Protocols** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.
