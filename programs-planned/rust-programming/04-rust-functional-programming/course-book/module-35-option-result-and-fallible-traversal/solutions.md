# Reasoned solutions — Module 35: Option, Result, and Fallible Traversal

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the LedgerFlow engineering guide](../capstone.md)

Use these explanations to review your reasoning about **Option, Result, and Fallible Traversal**, not to substitute for an attempt. The decisive question is: *Should a fallible traversal skip, fail fast, recover, accumulate diagnostics, or continue with an explicit default?* When your design differs, separate three possibilities: a Rust rule was applied incorrectly, the product contract changed, or two architectures satisfy the same contract with different trade-offs.

## Compiler specimen reasoning

### 1. `case-01.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** collect over Result performs fail-fast traversal.
- **Causal explanation:** The specimen compiles because collect over Result performs fail-fast traversal.
- **Principled repair:** use this shape when partial output has no value
- **Weak repair to reject:** silently filter out errors

### 2. `case-02.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** a Vec of values cannot collect an iterator of Result items.
- **Causal explanation:** The compiler rejects the specimen because a Vec of values cannot collect an iterator of Result items.
- **Principled repair:** collect into Result<Vec<_>, _> or handle each residual
- **Weak repair to reject:** call unwrap in the mapper

### 3. `case-03.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** transpose swaps Option<Result<T,E>> into Result<Option<T>,E>.
- **Causal explanation:** The specimen compiles because transpose swaps Option<Result<T,E>> into Result<Option<T>,E>.
- **Principled repair:** use transpose for optional fallible fields
- **Weak repair to reject:** convert parse errors to None

### 4. `case-04.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Result residuals cannot be propagated from an Option-returning function.
- **Causal explanation:** The compiler rejects the specimen because result residuals cannot be propagated from an Option-returning function.
- **Principled repair:** use .ok()? only if failure legitimately means absence, otherwise return Result
- **Weak repair to reject:** replace every error with None

### 5. `case-05.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** map_err adds typed context without losing success.
- **Causal explanation:** The specimen compiles because map_err adds typed context without losing success.
- **Principled repair:** retain structured error data
- **Weak repair to reject:** format the error into a String at the parser boundary

### 6. `case-06.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** accumulation requires an explicit two-channel collector.
- **Causal explanation:** The specimen compiles because accumulation requires an explicit two-channel collector.
- **Principled repair:** use an explicit Batch or partition helper
- **Weak repair to reject:** pretend Result collect accumulates all errors

### 7. `case-07.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** unwrap_or_else evaluates fallback lazily.
- **Causal explanation:** The specimen compiles because unwrap_or_else evaluates fallback lazily.
- **Principled repair:** prefer lazy fallback for work or consuming captures
- **Weak repair to reject:** use unwrap_or with an expensive eager expression

### 8. `case-08.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** question mark does not automatically convert unrelated error types.
- **Causal explanation:** The compiler rejects the specimen because question mark does not automatically convert unrelated error types.
- **Principled repair:** map_err with contextual String or use a typed enum with From
- **Weak repair to reject:** erase all errors before the function boundary

## Exercise reasoning

### Exercise 1 — Draw nested shapes

`Option<Result<T,E>>` means the value may be absent, and if present its production may fail; `transpose` produces `Result<Option<T>,E>`, making failure outermost. `Result<Result<T,E1>,E2>` represents two distinct failure stages; `flatten` is unavailable because error types differ, and explicit mapping or a common error type is required. `Option<Option<T>>` can be flattened when the two kinds of absence have the same meaning; if they mean different things, flattening destroys semantic distinction.

### Exercise 2 — Prove fail-fast evaluation

Use a parser closure that appends each visited index to a ledger before returning. Supply valid, invalid, then valid input. Assert the result is the first error and the ledger contains only indices through the invalid element. Output alone is insufficient because an implementation could parse all rows and still return the first error.

### Exercise 3 — Accumulate without erasing order

One design is `Inspection { accepted: Vec<Accepted>, diagnostics: Vec<Diagnostic> }`, where every accepted record and diagnostic carries its source line. If a consumer needs one total ordering across accepted and rejected outcomes, keep `Vec<RowOutcome>` and derive channels later. The iteration should visit each line once and append outcomes deterministically. Do not model parse failure as `None`, and do not use a `HashMap` when source order is part of the contract.

### Exercise 4 — Eager versus lazy defaults

`unwrap_or(default())` evaluates `default()` before the method call, so allocation and metric mutation happen even when the option is `Some`. `unwrap_or_else(default)` stores the callable and invokes it only for `None`; it accepts a one-shot fallback. When the fallback is a cheap constant, eager syntax may be clearer. The decision includes evaluation and effect semantics, not only runtime cost.

### Exercise 5 — Preserve source errors

Define variants such as `InvalidAmount { line, text, source: ParseIntError }` or a context wrapper retaining the source error. Add context at the boundary that knows line and field. Implement `Display` for the user message and `Error::source` when appropriate. Early stringification prevents callers from inspecting categories or chains and makes later reporting brittle.

### Exercise 6 — Choose explicit control flow

Small shape changes can remain compositional: trim, convert empty to `None`, then `map(parse).transpose()`. Once one accepted value may coexist with warnings and range errors must join an accumulation channel, an explicit `match` or row-inspection function is clearer. It names every outcome and prevents `and_then` nesting from hiding whether a branch stops, skips, warns, or rejects.



## Laboratory comparison

The complete laboratory implementation is in [`module-05-resilient-import/solution`](../../labs/module-05-resilient-import/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Option, Result, and Fallible Traversal**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Compose optional and fallible transformations while preserving ownership and error meaning.
- Use `transpose`, `flatten`, and `collect` to change container shape deliberately.
- Distinguish fail-fast traversal from diagnostic accumulation and implement both honestly.
- Choose eager and lazy defaults with awareness of evaluation and side effects.
- Stop combinator chains when explicit control flow communicates the error topology more clearly.

A complete explanation of **Option, Result, and Fallible Traversal** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.
