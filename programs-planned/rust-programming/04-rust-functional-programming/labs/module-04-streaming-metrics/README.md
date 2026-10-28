# Laboratory 34 — Streaming Metrics

This is the independent product for **Course 4, Module 34: Folds, Scans, and Short-Circuiting**. Read the [module chapter](../../course-book/module-34-folds-scans-and-short-circuiting/index.md) and complete its [workbook](../../course-book/module-34-folds-scans-and-short-circuiting/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> What invariant does an accumulator maintain, and when should a traversal continue, emit intermediate state, or stop early?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

The crate in `labs/module-04-streaming-metrics/README.md` asks for four related but different traversals. Treat them as separate contracts.

### Prefix invariant first

For `Metrics`, state the invariant after consuming exactly `k` values:

- `count` equals `k`;
- `total` equals the checked sum of the first `k` values;
- `minimum` and `maximum` are `None` exactly when `k == 0`;
- otherwise extrema describe precisely that prefix.

Do not begin with a tuple accumulator. The named state is part of the proof surface.

### Four traversal modes

#### Final summary

Implement `summarize` with `try_fold`. Overflow must return `MetricError::Overflow` and no partial final `Metrics`. Test empty input, mixed signs, and overflow at both the first and a later step.

#### Running totals

Implement a lazy `scan` that yields each checked prefix total. Decide what happens after overflow. The published contract emits exactly one error item and then remains exhausted. A scan that repeatedly emits errors is wrong even if the first error is correct.

#### First threshold crossing

Use `ControlFlow` to return the first `(index, prefix_total)` above a limit. Crossing is an ordinary discovery, not a domain error. Checked addition can still produce an error. Your type shape must preserve that distinction.

#### Sign-change transfer reducer

Define whether zero is its own sign class or ignored. State the policy before coding, encode it in a named accumulator, and write a counterexample that distinguishes the two interpretations.

### Diagnostic experiment

For `[2, 4, 8]` and limit `5`, record accumulator state before and after every closure call. For `[i64::MAX, 1, 2]`, record which items are pulled by each traversal. This is evidence about short-circuiting, not merely output.

### Rejected implementations

- minimum initialized to zero;
- wrapping or saturating arithmetic without product authorization;
- an external mutable diagnostics vector captured by a fold;
- one Boolean used for both “error seen” and “stop requested”;
- `reduce` for an operation that requires an explicit empty identity;
- a five-field anonymous tuple whose positions have no reviewable names.

### Defense

You must explain why `try_fold` failure is not transactionality for external effects, why `scan` can remain lazy while carrying state, and why a readable loop would be preferable if the accumulator update required several independently fallible substeps.

## Working route

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/`, add the first adversarial test before the design-changing repair, and complete the workbook’s transfer problem before reading the reference implementation.

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

> What invariant does an accumulator maintain, and when should a traversal continue, emit intermediate state, or stop early?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Streaming Metrics**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
