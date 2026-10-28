# Module 35 — Option, Result, and Fallible Traversal

**Course 4 · Day 5 · Module 35 of 100**
`█████████░░░░░░░░░░░░░░░░` **35/100**

[Program](../../../README.md) · [Course 4](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-05-resilient-import/README.md) · [LedgerFlow guide](../capstone.md)

[← Module 34: Folds, Scans, and Short-Circuiting](../module-34-folds-scans-and-short-circuiting/index.md) · [Module 36: Custom Iterators and Collection Protocols →](../module-36-custom-iterators-and-collection-protocols/index.md)

## The question

> Should a fallible traversal skip, fail fast, recover, accumulate diagnostics, or continue with an explicit default?

## Why this comes now

A pipeline over valid values is incomplete when parsing or validation can fail. `Option` and `Result` now become traversal policies: skip, stop, recover, default, or collect diagnostics. The essential decision is not which combinator is shortest but what information the product is allowed to lose.

### Prerequisite bridge

Module 34 established **Folds, Scans, and Short-Circuiting**. Before continuing, verify that you can use `controlflow` for domain-specific early exit without inventing an error. This module preserves that capability and adds the ability to compose optional and fallible transformations while preserving ownership and error meaning. Module 36, **Custom Iterators and Collection Protocols**, will rely on both when it asks: *What laws must a custom traversal obey, and who owns the collection when iteration begins?*

### Scope boundary

This module owns the reasoning for **option, result, and fallible traversal** inside Course 4. The course uses ordinary functions, closures, iterators, and immutable public models. It does not treat mutation as forbidden, and it postpones macro construction, parallel iteration, async streams, and benchmark-driven optimization. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- Compose optional and fallible transformations while preserving ownership and error meaning.
- Use `transpose`, `flatten`, and `collect` to change container shape deliberately.
- Distinguish fail-fast traversal from diagnostic accumulation and implement both honestly.
- Choose eager and lazy defaults with awareness of evaluation and side effects.
- Stop combinator chains when explicit control flow communicates the error topology more clearly.

`Option` and `Result` provide combinators that preserve one branch while transforming another.

## Core model

### `map`

```rust
let length = maybe_name.as_deref().map(str::len);
```

`Option::map` transforms `Some(T)` and leaves `None`. `Result::map` transforms `Ok(T)` and leaves `Err(E)`.

### `and_then`

Use `and_then` when the next function already returns the same container shape:

```rust
fn positive(value: i64) -> Option<u64> {
    u64::try_from(value).ok().filter(|value| *value > 0)
}

let parsed_positive = text.parse::<i64>().ok().and_then(positive);
```

Using `map(positive)` would produce `Option<Option<u64>>`.

For results:

```rust
let event = parse(line).and_then(validate);
```

The first error stops the chain.

### `or_else`

`or_else` runs a recovery function only on absence or error:

```rust
let config = read_primary().or_else(|primary_error| {
    read_fallback().map_err(|fallback_error| Error::Both {
        primary: primary_error,
        fallback: fallback_error,
    })
});
```

Recovery should preserve relevant context rather than replacing every error with a generic message.

### Borrow before consuming

Because many combinators take `self` by value, use `as_ref`, `as_mut`, `as_deref`, or `as_deref_mut` to transform borrowed contents while retaining the container.

```rust
let name: Option<String> = Some(String::from("Ada"));
let length = name.as_ref().map(String::len);
assert!(name.is_some());
```

### Combinator names are control flow

- `map`: success value changes, shape remains.
- `and_then`: success value chooses the next same-shaped computation.
- `map_err`: error value changes, success remains.
- `or_else`: error chooses a recovery computation.

### Decision rule — Combinator names are control flow

Use combinators when each step has one clear branch responsibility. Switch to `match` when several branches interact, when context must be assembled from both sides, or when the chain obscures evaluation order.

Nested containers often arise from mapping a fallible or optional function. `flatten` removes one same-kind layer. `transpose` swaps `Option` and `Result`.

### Flattening

```rust
let nested: Option<Option<u64>> = Some(Some(7));
assert_eq!(nested.flatten(), Some(7));
```

For results with the same error type:

```rust
let nested: Result<Result<u64, Error>, Error> = Ok(Ok(7));
assert_eq!(nested.flatten(), Ok(7));
```

Flattening is appropriate when both layers represent the same control meaning. If outer and inner absence have different meanings, use a domain enum instead of erasing the distinction.

### Transpose

An optional field may be present but fallible to parse:

```rust
fn parse_limit(text: Option<&str>) -> Result<Option<u64>, ParseIntError> {
    text.map(str::parse).transpose()
}
```

Shape trace:

```text
Option<&str>
  map(str::parse)
Option<Result<u64, ParseIntError>>
  transpose()
Result<Option<u64>, ParseIntError>
```

The final type says: parsing may fail; if it succeeds, the value may be absent.

The reverse direction can be useful when an operation may fail to produce an optional continuation, though explicit control flow is often clearer.

### Shape before syntax

Write the desired type first. For example:

- “failure stops the whole operation; successful output may be absent” → `Result<Option<T>, E>`;
- “the operation itself may be absent; if present it may succeed or fail” → `Option<Result<T, E>>`.

These are not interchangeable.

### Preserve semantic layers

`None` might mean not configured, not found, filtered out, end of input, or invalid-but-discarded. Combining different meanings into nested options is a signal to introduce a domain type.

### Decision rule — Preserve semantic layers

Use `flatten` and `transpose` when the resulting shape accurately states the control semantics. Do not remove layers merely because nested types look inconvenient.

The standard library implements collection from an iterator of results:

```rust
let parsed: Result<Vec<u64>, _> = fields
    .iter()
    .map(|field| field.parse::<u64>())
    .collect();
```

If every item is `Ok`, the target collection is built. At the first `Err`, collection stops and returns that error. Later items are not parsed.

### This is traversal, not magic

The target type directs `collect` through `FromIterator`. `Result<V, E>` can collect `Result<A, E>` when `V` can collect `A`. The result wrapper supplies fail-fast behavior.

### Preserve line context

```rust
let parsed: Result<Vec<_>, ImportError> = lines
    .enumerate()
    .map(|(index, line)| {
        parse_line(line).map_err(|source| ImportError::Line {
            number: index + 1,
            source,
        })
    })
    .collect();
```

The first failure retains its line number.

### Partial allocation

The target may have accumulated values before failure, but the partially built collection is not returned by this interface. If partial success must survive, use a different result type.

### Collecting `Option`

An iterator of `Option<T>` can similarly collect into `Option<Vec<T>>`, stopping at the first `None`. This is useful when every element is required but there is no error reason.

### `collect::<Result<(), E>>()`

When each operation returns `Result<(), E>`, collecting can drive all operations until the first failure while discarding unit successes:

```rust
let result: Result<(), Error> = records.iter().map(validate_record).collect();
```

An explicit `try_for_each` may communicate intent more directly.

### Decision rule — collect::<Result<(), E>>()

Use result collection when the product contract is “all values or the first error.” Do not describe it as error accumulation or partial import.

Fail-fast parsing answers: “Can I produce the complete value?” Batch validation often asks: “What can I accept, and what is wrong with the rest?” These are different contracts.

### Partition results explicitly

```rust
#[derive(Debug)]
struct Batch<T, E> {
    accepted: Vec<T>,
    errors: Vec<E>,
}

impl<T, E> Batch<T, E> {
    fn from_results<I>(items: I) -> Self
    where
        I: IntoIterator<Item = Result<T, E>>,
    {
        items.into_iter().fold(
            Self { accepted: Vec::new(), errors: Vec::new() },
            |mut batch, item| {
                match item {
                    Ok(value) => batch.accepted.push(value),
                    Err(error) => batch.errors.push(error),
                }
                batch
            },
        )
    }
}
```

This traverses every item. The return type makes partial acceptance explicit.

### Parse errors and domain rejections may differ

A line that cannot be decoded is not the same as a valid event rejected by business state. Preserve separate diagnostic variants so callers can decide whether to repair input, change policy, or inspect account history.

### Cross-record validation

Some errors are not visible per record: duplicate identifiers, inconsistent totals, or order-dependent transitions. Accumulation may require phases:

1. parse each record;
2. normalize;
3. detect duplicates;
4. order events;
5. reduce state and collect transition rejections.

A single `partition(Result::is_ok)` is not enough.

### Accepted-with-warnings

Sometimes a record is usable but has warnings. Model this directly:

```rust
enum Validation<T, E> {
    Valid(T),
    ValidWithWarnings { value: T, warnings: Vec<E> },
    Invalid(Vec<E>),
}
```

Do not overload `Result` if success and diagnostics must coexist.

### Product policy

Accumulating errors can expose more feedback but may perform more work and hold more memory. It may also be unsafe when later validation depends on secrets or expensive resources. Choose from the product contract.

### Decision rule — Product policy

Use fail-fast `Result` for all-or-nothing construction and diagnostic accumulation for batch review or partial acceptance. Represent their difference in the return type and test cross-record phases.

Methods ending in `_else` usually accept a closure and evaluate it only on the fallback path. Their eager counterparts receive an already evaluated value.

```rust
let value = option.unwrap_or(expensive_default());
```

`expensive_default()` runs before `unwrap_or`, even if `option` is `Some`.

```rust
let value = option.unwrap_or_else(expensive_default);
```

The function runs only for `None`.

### Error construction

```rust
let item = maybe_item.ok_or_else(|| Error::Missing {
    key: key.to_owned(),
})?;
```

Lazy error construction avoids allocation on success.

### Laziness changes effects

If the fallback reads a file, increments a counter, or can fail, choosing eager or lazy evaluation changes observable behavior. Do not treat `_else` as a micro-optimization only.

### Defaults can hide invalid states

```rust
let amount = parsed.unwrap_or_default();
```

Turning a malformed amount into zero may corrupt a ledger. A default is valid only when it is an actual domain default, not merely a convenient value of the type.

### `map_or` and `map_or_else`

These collapse the container into a plain value. The eager default in `map_or` is evaluated regardless of branch; `map_or_else` computes branch-specific outputs lazily.

### Recovery can be fallible

`map_or_else` is useful when an optional value falls back to a fallible operation by returning `Result` from both closures. Keep the resulting nested shapes readable; an explicit match may be better.

### Decision rule — Recovery can be fallible

Choose eager or lazy forms based on evaluation semantics. Use defaults only when the domain defines them. Record fallback effects and failure timing in the four-flow ledger.

An error is not an afterthought attached to a happy-path chain. It changes item type, stopping behavior, and ownership.

```rust
let parsed = lines.map(parse_line);
```

The item type is `Result<Record, ParseError>`. From here, the pipeline has several honest choices:

- collect into `Result<Vec<_>, _>` and fail fast;
- map errors into richer context;
- fold into accepted values and diagnostics;
- retry or recover selected errors;
- expose the result iterator to a caller;
- deliberately discard errors under a documented best-effort policy.

### Preserve the source error

A domain error should often retain the lower-level error:

```rust
enum ImportError {
    Line {
        number: usize,
        source: ParseError,
    },
}
```

Stringifying early destroys structured inspection and source chaining.

### Error ordering

In accumulation mode, diagnostics should have deterministic order, commonly source order and then validation-rule order. A hash-based grouping can make output nondeterministic unless sorted.

### Recovery boundaries

Recovery should be narrow. Retrying every error, defaulting every missing field, or treating every parse failure as absence creates a pipeline that produces output but cannot be trusted.

### Side-channel errors are weak

A function that returns successful records while writing errors to stderr has split semantics and is difficult to test. Return diagnostics as data; let the shell decide how to render them.

### Panics are not a combinator strategy

`unwrap` inside a mapping closure moves failure out of the type and into process termination. Use panic only for genuine unrecoverable invariant violations, not ordinary input.

### Decision rule — Panics are not a combinator strategy

Draw the failure path alongside the data path. Every conversion from `Result` to `Option`, string, default, log message, or panic must have a product justification.

There is no prize for expressing an entire error flow through methods.

### Combinators for one-branch transformations

```rust
let amount = text
    .parse::<i64>()
    .map_err(Error::Amount)
    .and_then(NonNegative::try_from);
```

Each stage transforms one branch and leaves the other intact.

### `?` for linear propagation

```rust
fn parse_event(line: &str) -> Result<Event, Error> {
    let mut fields = line.split('\t');
    let id = fields.next().ok_or(Error::MissingId)?.parse()?;
    let account = fields.next().ok_or(Error::MissingAccount)?;
    let amount = fields.next().ok_or(Error::MissingAmount)?.parse()?;
    Event::new(id, account, amount)
}
```

The sequence is easier to read as statements because each value feeds the next construction.

### `match` for interacting branches

```rust
match (primary(), fallback()) {
    (Ok(value), _) => Ok(value),
    (Err(primary), Ok(value)) => Ok(value),
    (Err(primary), Err(fallback)) => Err(Error::Both { primary, fallback }),
}
```

A match exposes relationships between outcomes that `or_else` may obscure or evaluate differently.

### Avoid combinator tunneling

A long chain can hide where ownership moves, which errors are transformed, and when fallbacks run. Introduce named values when the type changes meaningfully.

### Review heuristic

Use a combinator when it names the branch operation directly. Use `?` for linear success-path construction. Use `match` when multiple branches interact or when evaluation order must be obvious.

### Decision rule — Review heuristic

Select control syntax from error topology, not stylistic identity. A functional Rust programmer is fluent in all three and refuses to erase diagnostics for chain aesthetics.

### Optional but fallible field

```rust
fn parse_limit(field: Option<&str>) -> Result<Option<u64>, Diagnostic> {
    field
        .map(|text| text.parse::<u64>().map_err(Diagnostic::invalid_limit))
        .transpose()
}
```

Shape: `Option<&str>` → `Option<Result<u64, Diagnostic>>` → `Result<Option<u64>, Diagnostic>`.

### Fail-fast batch

```rust
fn parse_all(lines: &[String]) -> Result<Vec<Event>, Diagnostic> {
    lines
        .iter()
        .enumerate()
        .map(|(index, line)| parse_line(line).map_err(|e| e.at_line(index + 1)))
        .collect()
}
```

Stops at first error.

### Accumulating batch

```rust
fn inspect_all(lines: &[String]) -> Batch<Event, Diagnostic> {
    lines
        .iter()
        .enumerate()
        .map(|(index, line)| parse_line(line).map_err(|e| e.at_line(index + 1)))
        .fold(Batch::default(), Batch::push_result)
}
```

Traverses every line and returns accepted values plus diagnostics. The product chooses which mode.

### Rejected shortcut

`filter_map(|line| parse_line(line).ok())` is rejected because malformed lines disappear and the caller cannot distinguish valid omission from corruption.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For compose optional and fallible transformations while preserving ownership and error meaning, construct one positive and one causal negative example. Mark the first decisive fact in the **failure-policy matrix** and state which evidence could falsify the claim.

2. **Outcome 2.** For use `transpose`, `flatten`, and `collect` to change container shape deliberately, construct one positive and one causal negative example. Mark the first decisive fact in the **failure-policy matrix** and state which evidence could falsify the claim.

3. **Outcome 3.** For distinguish fail-fast traversal from diagnostic accumulation and implement both honestly, construct one positive and one causal negative example. Mark the first decisive fact in the **failure-policy matrix** and state which evidence could falsify the claim.

4. **Outcome 4.** For choose eager and lazy defaults with awareness of evaluation and side effects, construct one positive and one causal negative example. Mark the first decisive fact in the **failure-policy matrix** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

The course capstone is **LedgerFlow**, a deterministic event-analysis pipeline with diagnostics, audit history, queries, and reports. Separate row-local diagnostics, fatal stream failures, warnings, and duplicate policy. Preserve physical source order when diagnostics from multiple phases are combined. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-05-resilient-import/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 36 when you can:

- answer the module question—“Should a fallible traversal skip, fail fast, recover, accumulate diagnostics, or continue with an explicit default?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Compose optional and fallible transformations while preserving ownership and error meaning;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [Option](https://doc.rust-lang.org/std/option/enum.Option.html)
- [Result](https://doc.rust-lang.org/std/result/enum.Result.html)
- [FromIterator for Result](https://doc.rust-lang.org/std/result/enum.Result.html#impl-FromIterator%3CResult%3CA,+E%3E%3E-for-Result%3CV,+E%3E)

[← Module 34](../module-34-folds-scans-and-short-circuiting/index.md) · [one-hundred-module map](../../../COURSE_MAP.md) · [Module 36 →](../module-36-custom-iterators-and-collection-protocols/index.md)

## Continue

Continue to [Module 36 — Custom Iterators and Collection Protocols](../module-36-custom-iterators-and-collection-protocols/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
