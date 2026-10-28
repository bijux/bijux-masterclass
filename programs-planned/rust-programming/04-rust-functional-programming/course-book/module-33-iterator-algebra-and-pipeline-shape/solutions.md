# Reasoned solutions — Module 33: Iterator Algebra and Pipeline Shape

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the LedgerFlow engineering guide](../capstone.md)

Use these explanations to review your reasoning about **Iterator Algebra and Pipeline Shape**, not to substitute for an attempt. The decisive question is: *How do adapters change item type, cardinality, order, ownership, and stopping behavior across a pipeline?* When your design differs, separate three possibilities: a Rust rule was applied incorrectly, the product contract changed, or two architectures satisfy the same contract with different trade-offs.

## Compiler specimen reasoning

### 1. `case-01.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** filter_map represents zero-or-one output per input.
- **Causal explanation:** The specimen compiles because filter_map represents zero-or-one output per input.
- **Principled repair:** use filter_map when rejection truly means omission
- **Weak repair to reject:** discard Result errors when diagnostics are required

### 2. `case-02.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** flatten removes one iterator-like nesting layer.
- **Causal explanation:** The specimen compiles because flatten removes one iterator-like nesting layer.
- **Principled repair:** use flatten for the exact nested shape
- **Weak repair to reject:** use flat_map with an unrelated allocation

### 3. `case-03.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** chain requires both iterators to have the same item type.
- **Causal explanation:** The compiler rejects the specimen because chain requires both iterators to have the same item type.
- **Principled repair:** map one side to a common semantic type or use an enum
- **Weak repair to reject:** stringify everything without a boundary reason

### 4. `case-04.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** zip pairs until either input ends.
- **Causal explanation:** The specimen compiles because zip pairs until either input ends.
- **Principled repair:** validate equal lengths first when truncation would be a defect
- **Weak repair to reject:** assume zip reports length mismatch

### 5. `case-05.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** consuming an input in zip moves the collection.
- **Causal explanation:** The compiler rejects the specimen because consuming an input in zip moves the collection.
- **Principled repair:** borrow left with iter when it must remain usable
- **Weak repair to reject:** clone left merely to preserve an accidental later use

### 6. `case-06.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** flat_map performs one-to-many expansion.
- **Causal explanation:** The specimen compiles because flat_map performs one-to-many expansion.
- **Principled repair:** use flat_map when the expansion relationship is explicit
- **Weak repair to reject:** build one temporary Vec per item without need

### 7. `case-07.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** enumerating before filtering preserves original positions.
- **Causal explanation:** The specimen compiles because enumerating before filtering preserves original positions.
- **Principled repair:** place enumerate before filters when source position matters
- **Weak repair to reject:** renumber surviving items and label them source positions

### 8. `case-08.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** take_while predicate receives a reference to the iterator item.
- **Causal explanation:** The compiler rejects the specimen because take_while predicate receives a reference to the iterator item.
- **Principled repair:** dereference to the intended value shape
- **Weak repair to reject:** change all source values to Copy-owned items without considering ownership

## Exercise reasoning

### Exercise 1 — Pipeline shape ledger

`iter` yields `&String` one per row. `enumerate` yields `(usize, &String)` one-to-one with physical positions. `filter` yields zero-or-one tuple per input while preserving order. `filter_map` changes the value to parsed records and drops every parse error; that is the critical information loss. `flat_map` yields zero or more expanded values per accepted record, preserving outer source order and each inner iterable’s order. A better design keeps parse failures as `Result` or a diagnostic channel instead of using `.ok()`.

### Exercise 2 — Choose the adapter

Use `map` for one-to-one amount conversion, `filter` for retaining active records without changing the item type, `filter_map` only when an invalid or absent optional note legitimately means no output, `flat_map` to map each record to its tags and yield all tags, and `flatten` when the nested values already exist. The justification matters: using `filter_map` for mandatory parsing would silently redefine an error as absence.

### Exercise 3 — Find the truncation bug

`zip` intentionally stops at the shorter iterator. If equal length is an invariant, check lengths before zipping when both sources expose length, or use an indexed/peekable loop that reports which side ended first. The test suite needs left-shorter, right-shorter, and equal-length cases. Padding with defaults changes business meaning and is not a neutral repair.

### Exercise 4 — Position before or after filtering

Attach the physical position before any filtering: `rows.iter().enumerate()`. After filtering and successful parsing, enumerate again to assign accepted rank. The output can carry `(source_line, accepted_rank, record)`. One enumerate cannot represent both concepts because filtering changes cardinality. Name the indices to prevent accidental interchange.

### Exercise 5 — Remove required effects from `inspect`

`inspect` is intended for observation while items are pulled. Its call count depends on downstream consumption, short-circuiting, and errors; a pipeline that is never consumed performs no audit. Required effects should be explicit in the shell or represented as data. One redesign has the core produce `(accepted_values, audit_entries)` or an effect plan, and the shell writes the entries under a tested protocol.

### Exercise 6 — Refactor a long chain

Parsing through filtering and expansion can usually remain lazy if downstream consumes once. Sorting requires materialization because global order needs all items. A good split is `normalized_rows`, `parsed_rows`, `accepted_events`, then `let mut events: Vec<_> = accepted_events.collect(); events.sort_by_key(...);`, followed by a rendering iterator or explicit loop. The materialization boundary is justified by the algorithm, not by type inconvenience.



## Laboratory comparison

The complete laboratory implementation is in [`module-03-record-shaping-pipeline/solution`](../../labs/module-03-record-shaping-pipeline/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Iterator Algebra and Pipeline Shape**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Derive the item type and cardinality effect of common iterator adapters.
- Choose correctly among `filter`, `map`, `filter_map`, `flatten`, and `flat_map`.
- Reason about order and truncation in `chain`, `zip`, `take`, and stopping adapters.
- Use `inspect` for observation without embedding required effects into a transformation.
- Refactor long chains into named semantic stages without forcing premature collection.

A complete explanation of **Iterator Algebra and Pipeline Shape** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.
