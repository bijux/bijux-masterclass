# Reasoned solutions — Module 34: Folds, Scans, and Short-Circuiting

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the LedgerFlow engineering guide](../capstone.md)

Use these explanations to review your reasoning about **Folds, Scans, and Short-Circuiting**, not to substitute for an attempt. The decisive question is: *What invariant does an accumulator maintain, and when should a traversal continue, emit intermediate state, or stop early?* When your design differs, separate three possibilities: a Rust rule was applied incorrectly, the product contract changed, or two architectures satisfy the same contract with different trade-offs.

## Compiler specimen reasoning

### 1. `case-01.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** fold consumes the source into one accumulator.
- **Causal explanation:** The specimen compiles because fold consumes the source into one accumulator.
- **Principled repair:** state the accumulator invariant
- **Weak repair to reject:** use fold only to make a loop look functional

### 2. `case-02.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** reduce uses the first item as the initial accumulator.
- **Causal explanation:** The specimen compiles because reduce uses the first item as the initial accumulator.
- **Principled repair:** handle the Option result explicitly
- **Weak repair to reject:** unwrap reduce on possibly empty input

### 3. `case-03.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** try_fold short-circuits through Result.
- **Causal explanation:** The specimen compiles because try_fold short-circuits through Result.
- **Principled repair:** use try_fold for genuine stop-on-error traversal
- **Weak repair to reject:** encode overflow as a magic total

### 4. `case-04.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** question mark requires the closure return type to carry the residual.
- **Causal explanation:** The compiler rejects the specimen because question mark requires the closure return type to carry the residual.
- **Principled repair:** return Result items and collect them or handle the parse in the closure
- **Weak repair to reject:** unwrap the parse and replace a type error with a panic

### 5. `case-05.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** scan exposes intermediate state while retaining hidden accumulator state.
- **Causal explanation:** The specimen compiles because scan exposes intermediate state while retaining hidden accumulator state.
- **Principled repair:** use scan for stateful lazy views
- **Weak repair to reject:** collect all prefixes inside a fold then re-iterate

### 6. `case-06.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** every fold branch must return the same accumulator type.
- **Causal explanation:** The compiler rejects the specimen because every fold branch must return the same accumulator type.
- **Principled repair:** choose an accumulator that represents both states
- **Weak repair to reject:** use a sentinel integer for missing state

### 7. `case-07.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** ControlFlow represents an explicit early-break value.
- **Causal explanation:** The specimen compiles because controlFlow represents an explicit early-break value.
- **Principled repair:** use ControlFlow when early success is not an error
- **Weak repair to reject:** abuse Result error for successful discovery

### 8. `case-08.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** sum needs a concrete output type when several implementations are possible.
- **Causal explanation:** The compiler rejects the specimen because sum needs a concrete output type when several implementations are possible.
- **Principled repair:** annotate the intended numeric accumulator
- **Weak repair to reject:** cast values arbitrarily without domain reasoning

## Exercise reasoning

### Exercise 1 — Prove a summary fold

For the empty prefix: `count == 0`, `total == 0`, `min == None`, and `max == None`. After `k` items, count is `k`, total is the checked sum of exactly those items, and min/max are extrema of that prefix. The step increments count with checked arithmetic, updates total with `checked_add`, and combines extrema through `Option`. If arithmetic fails, return an error containing the source position and the prior accumulator rather than silently wrapping.

### Exercise 2 — Choose fold, reduce, or sum

A nonempty GCD can use `reduce` when emptiness is represented as `None`. Optional maximum can also use `max` or `reduce`. Monetary checked total needs `try_fold` because overflow is part of the contract. String concatenation can use `fold(String::new(), ...)` but order matters and repeated allocation behavior should be considered; an explicit loop may make capacity planning clearer. `sum` is appropriate only when its arithmetic semantics and identity match the domain.

### Exercise 3 — Running balance with `scan`

A pure `scan` closure returning `Option<Balance>` uses `None` to end iteration, but it cannot explain why. For a domain failure, a stream of `Result<Balance, Error>` may be clearer, or a custom iterator can retain precise state. If `scan` returns `Some(Err(...))` and then marks itself terminated, the failing event is consumed and emitted as an error. Document this explicitly. The exercise demonstrates that output topology matters as much as adapter availability.

### Exercise 4 — Failure-atomic `try_fold`

Pass owned candidate ledger state as the accumulator: `events.try_fold(initial, |ledger, event| ledger.apply(event))`. `apply` should validate first and return either the new ledger or an error that can include the unchanged prior ledger if recovery requires it. Mutating an outer map exposes partial changes if an error arrives after earlier events, and rollback then becomes an implicit second protocol. Owned candidate state makes commit semantics explicit, although cloning cost must be considered and optimized with local mutation or transaction planning where appropriate.

### Exercise 5 — Early exit is not always failure

The closure carries `(index, total)` in `Continue`; when the updated total reaches the quota it returns `Break((index, total))`. Reaching the quota is the requested successful result, not an exceptional condition. `Result` would label ordinary control flow as error and conflate it with checked-arithmetic failure; those can remain a separate `Result` layer if necessary.

### Exercise 6 — Split accumulator soup

Keep domain state and recoverable diagnostics in a coherent core accumulator if they share one traversal contract. Replace audit text with structured audit entries. Remove progress output and timing from the core; the shell can observe batches or execute a returned plan. If timing must surround the whole operation, it needs no per-item accumulator field. One pass can remain, but the accumulator now has one explainable invariant instead of mixing domain state and effects.



## Laboratory comparison

The complete laboratory implementation is in [`module-04-streaming-metrics/solution`](../../labs/module-04-streaming-metrics/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Folds, Scans, and Short-Circuiting**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Design a fold accumulator with a precise prefix invariant.
- Distinguish `fold`, `reduce`, `sum`, `product`, and explicit loops by semantics rather than style.
- Use `scan` when evolving state must also yield an output stream.
- Use `try_fold` and `try_for_each` for fallible short-circuiting traversal.
- Use `ControlFlow` for domain-specific early exit without inventing an error.

A complete explanation of **Folds, Scans, and Short-Circuiting** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.
