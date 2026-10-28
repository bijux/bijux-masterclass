# Module 33 — Iterator Algebra and Pipeline Shape

**Course 4 · Day 3 · Module 33 of 100**
`████████░░░░░░░░░░░░░░░░░` **33/100**

[Program](../../../README.md) · [Course 4](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-03-record-shaping-pipeline/README.md) · [LedgerFlow guide](../capstone.md)

[← Module 32: The Iterator Model](../module-32-the-iterator-model/index.md) · [Module 34: Folds, Scans, and Short-Circuiting →](../module-34-folds-scans-and-short-circuiting/index.md)

## The question

> How do adapters change item type, cardinality, order, ownership, and stopping behavior across a pipeline?

## Why this comes now

Once the pull model is clear, adapters can be composed without treating a chain as decorative syntax. You track item type, cardinality, ordering, borrowing, allocation, and stopping behavior stage by stage. Pipeline readability is judged by whether those changes remain visible.

### Prerequisite bridge

Module 32 established **The Iterator Model**. Before continuing, verify that you can treat `size_hint`, `exactsizeiterator`, and `fusediterator` as contracts rather than optimization decoration. This module preserves that capability and adds the ability to derive the item type and cardinality effect of common iterator adapters. Module 34, **Folds, Scans, and Short-Circuiting**, will rely on both when it asks: *What invariant does an accumulator maintain, and when should a traversal continue, emit intermediate state, or stop early?*

### Scope boundary

This module owns the reasoning for **iterator algebra and pipeline shape** inside Course 4. The course uses ordinary functions, closures, iterators, and immutable public models. It does not treat mutation as forbidden, and it postpones macro construction, parallel iteration, async streams, and benchmark-driven optimization. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- Derive the item type and cardinality effect of common iterator adapters.
- Choose correctly among `filter`, `map`, `filter_map`, `flatten`, and `flat_map`.
- Reason about order and truncation in `chain`, `zip`, `take`, and stopping adapters.
- Use `inspect` for observation without embedding required effects into a transformation.
- Refactor long chains into named semantic stages without forcing premature collection.

The three adapters express different cardinality and error semantics.

## Core model

### `map`: exactly one output per input

```rust
let lengths = names.iter().map(|name| name.len());
```

If the source yields `A`, `map` applies `A -> B` and yields one `B` for every source item pulled. It does not skip.

### `filter`: keep or discard the original item

```rust
let active = records.iter().filter(|record| record.active);
```

The predicate receives `&Self::Item`, which can create double references when the source item is already a reference. The output item type is unchanged.

### `filter_map`: zero or one transformed output

```rust
let integers = fields.iter().filter_map(|field| field.parse::<i64>().ok());
```

This code discards every parse error. It is correct only when malformed fields are semantically equivalent to absent values. In an import pipeline, that is often data loss.

A better partial transformation might use an explicitly optional field:

```rust
let labels = records
    .iter()
    .filter_map(|record| record.label.as_deref());
```

Absence is already part of the domain.

### `map` to `Result` preserves failure

```rust
let parsed = fields.iter().map(|field| field.parse::<i64>());
```

The iterator item is now `Result<i64, ParseIntError>`. A later consumer decides whether to fail fast, accumulate, or partition.

### Combining predicate and projection

`filter_map` can replace a `filter` followed by `map` when the partial output is one coherent decision:

```rust
fn positive_amount(text: &str) -> Option<u64> {
    let value = text.parse::<i64>().ok()?;
    u64::try_from(value).ok()
}
```

But if rejection reasons matter, return a result or a richer enum.

### Algebra table

| Adapter | Closure | Output item | Per-input outputs |
|---|---|---|---|
| `map` | `A -> B` | `B` | exactly one |
| `filter` | `&A -> bool` | `A` | zero or one |
| `filter_map` | `A -> Option<B>` | `B` | zero or one |

The source may still be pulled multiple times before the outer iterator yields because filtered items are consumed and discarded.

### Decision rule — Algebra table

Choose from the product meaning: transform every item, select original items, or perform an explicitly optional transformation. Never use `filter_map(Result::ok)` as a generic way to make errors disappear.

`flatten` removes one iterable layer. `flat_map` maps each source item to an iterable and then removes that layer.

```rust
let groups = vec![vec![1, 2], vec![], vec![3]];
let values: Vec<_> = groups.into_iter().flatten().collect();
assert_eq!(values, [1, 2, 3]);
```

The source item is `Vec<i32>`, which implements `IntoIterator<Item = i32>`. `flatten` consumes each inner vector in this owned path.

### `flat_map`

```rust
let words = ["red blue", "green"];
let tokens: Vec<_> = words
    .iter()
    .flat_map(|line| line.split_whitespace())
    .collect();
```

Each line produces an iterator of borrowed tokens. Cardinality is zero-to-many.

### `Option` and `Result` are iterable too

`Option<T>` yields zero or one item. `Result<T, E>` yields one item for `Ok` and zero for `Err`. Flattening them can silently discard information:

```rust
let results: Vec<Result<i32, &str>> = vec![Ok(1), Err("bad"), Ok(2)];
let values: Vec<i32> = results.into_iter().flatten().collect();
assert_eq!(values, [1, 2]);
```

The error vanished. This may be useful for a deliberately best-effort view, but it is not validation.

### Nested cardinality and order

`flat_map` preserves outer order and, for each outer item, inner order. If outer items produce large inner sequences, output may expand dramatically. Record the cardinality bound when it matters.

### Borrowed inner iterators

A `flat_map` closure may return an iterator borrowing from its input item only when the ownership and lifetime relationships permit it. Borrowed slice items work naturally:

```rust
fn all_tags(records: &[Record]) -> impl Iterator<Item = &str> + '_ {
    records.iter().flat_map(|record| record.tags.iter().map(String::as_str))
}
```

Returning references into a temporary inner value does not work because the owner disappears.

### `map(...).flatten()` or `flat_map(...)`

Use whichever communicates the domain. `flat_map` emphasizes one-to-many transformation. Separate `map` and `flatten` can expose an important intermediate nested structure for debugging or reuse.

### Decision rule — map(...).flatten()` or `flat_map(...)

Use flattening only when removing one level of iterable structure is the intended semantic operation. Audit whether `Option` or `Result` information is being discarded and state the zero-to-many growth explicitly.

### `chain`: first sequence, then second

```rust
let all = primary.into_iter().chain(fallback);
```

Both iterators must yield the same item type. `chain` preserves the full order of the first, followed by the full order of the second. It does not merge or sort.

A chained fallback may be clearer than conditional collection when the policy is “try every primary source, then every secondary source.”

### `zip`: pair until either side ends

```rust
let labeled: Vec<_> = names.iter().zip(scores.iter()).collect();
```

The output cardinality is the minimum remaining length. Extra elements on the longer side are not represented.

If unequal lengths indicate invalid data, `zip` alone is dangerous. Validate lengths first or use a protocol that reports mismatch.

```rust
if names.len() != scores.len() {
    return Err(Error::LengthMismatch);
}
let pairs = names.into_iter().zip(scores);
```

### `enumerate`: position in this traversal

```rust
let numbered = lines.iter().enumerate();
```

The index counts yielded source items from zero. If `enumerate` appears after `filter`, it numbers retained items. If it appears before `filter`, it preserves original source positions.

```rust
let original_positions = lines
    .iter()
    .enumerate()
    .filter(|(_, line)| !line.trim().is_empty());
```

Adapter order changes meaning.

### `unzip` and tuple collection

An iterator of pairs can be separated into two collections:

```rust
let (names, scores): (Vec<_>, Vec<_>) = pairs.into_iter().unzip();
```

This traverses once but materializes two targets. Keep pairs together when positional association is an invariant; unzipping can make later mismatches possible.

### Pairing is not joining

`zip` pairs by position, not by key. A relational join requires a key-indexing or merge algorithm and explicit duplicate policy. Calling `zip` a join hides incorrect semantics.

### Decision rule — Pairing is not joining

Use `chain` for ordered concatenation, `zip` for positional pairing under an explicit truncation or equal-length policy, and `enumerate` at the stage whose positions you intend to expose.

`take`, `skip`, `take_while`, `skip_while`, and `map_while` describe prefixes and suffixes, but their boundary semantics differ.

### Count-based prefixes

```rust
let first_three = iter.take(3);
let after_three = iter.skip(3);
```

`take` yields at most the requested count. `skip` consumes and discards the requested count before yielding.

### Predicate-based prefixes

`take_while` yields while the predicate is true. The first false item is consumed to discover the boundary and not yielded.

`skip_while` discards while true. Once false occurs, that item and all remaining items are yielded without calling the predicate again.

### `map_while`

```rust
let parsed_prefix = fields
    .into_iter()
    .map_while(|field| field.parse::<u64>().ok());
```

This yields parsed values until the first parse failure. Later fields are not part of the defined prefix. Unlike a general fail-fast `Result`, the failure itself is discarded.

The standard-library contract does not specify useful repeated behavior after the first `None` for `MapWhile`; use `.fuse()` when callers depend on permanent exhaustion.

### Prefix semantics are domain semantics

A log reader may legitimately stop at the first sentinel. An import validator usually should not stop at the first blank field unless the format defines blank as end-of-record.

### `skip_while` is not `filter`

```rust
let values = [-2, -1, 3, -4, 5];
```

`skip_while(|x| *x < 0)` yields `3, -4, 5`. It stops applying the predicate after the first nonnegative value. `filter(|x| **x >= 0)` yields `3, 5` and tests every item.

### Boundary tests

Test:

- empty input;
- no item satisfies the predicate;
- every item satisfies it;
- boundary at the first item;
- boundary in the middle;
- behavior of the underlying iterator after partial consumption.

### Decision rule — Boundary tests

Use prefix and suffix adapters only when the data has ordered boundary semantics. Account for whether the boundary item is consumed, discarded, yielded, or converted into `None`.

`inspect` calls a closure with a reference to each item and yields the original item unchanged.

```rust
let total: i64 = amounts
    .iter()
    .inspect(|amount| eprintln!("input: {amount}"))
    .copied()
    .sum();
```

It is useful for temporary debugging, metrics that are explicitly best-effort, or tracing that must not affect the transformation result.

### Execution remains lazy

The observation occurs only when downstream consumers pull items. A short-circuiting consumer may inspect only a prefix.

```rust
let found = values
    .iter()
    .inspect(|value| eprintln!("checked {value}"))
    .find(|value| **value == target);
```

Only values through the match are observed.

### Required effects do not belong here

Persisting records, charging accounts, acknowledging messages, or incrementing exact business counters inside `inspect` creates a fragile contract. Removing a diagnostic-looking stage would change the product.

If an effect is required:

- represent it as a command or plan;
- execute it in an explicit loop;
- return a result that records success or failure;
- test its boundary separately.

### `inspect_err`

`Result::inspect_err` is similar: it observes an error while returning the original result. It is useful for diagnostics, but it does not handle, transform, or recover from the error.

```rust
let parsed = text
    .parse::<u64>()
    .inspect_err(|error| eprintln!("invalid amount: {error}"));
```

### Observation can perturb timing

Even diagnostic output can affect timing, ordering with other streams, or tests. Keep assertions about product behavior independent of debug observation.

### Named instrumentation boundary

For stable instrumentation, a narrow observer callback may be clearer than scattered `inspect` calls, especially if the product explicitly documents best-effort event observation. Its call-count and failure policy must still be specified.

### Decision rule — Named instrumentation boundary

Use `inspect` only when deleting it preserves product semantics. If the effect must happen, move it into the effect flow and return or handle failure explicitly.

Before writing a chain, build a stage table.

Suppose records contain optional comma-separated tags:

```rust
struct Record {
    id: u64,
    tags: Option<String>,
}
```

A borrowed tag pipeline might be:

```rust
let tags = records
    .iter()
    .filter_map(|record| record.tags.as_deref())
    .flat_map(|tags| tags.split(','))
    .map(str::trim)
    .filter(|tag| !tag.is_empty());
```

Stage table:

| Stage | Item | Cardinality | Order | Ownership |
|---|---|---|---|---|
| `records.iter()` | `&Record` | one per record | record order | borrows slice |
| `filter_map` | `&str` | zero/one per record | preserved | borrows each string |
| `flat_map` | `&str` | zero/many per present field | outer then inner | borrowed substrings |
| `map` | `&str` | one/one | preserved | same borrowed data |
| `filter` | `&str` | zero/one | preserved | unchanged item |

This table reveals that the output iterator cannot outlive `records` and that no allocation is required by these standard string-slice operations. It does not prove that every called function in an arbitrary pipeline allocates zero times.

### Adapter order is algebra

`map(f).filter(p)` and `filter(p).map(f)` are generally different because `p` may expect different types and because one order executes `f` for rejected items.

`filter(p).filter(q)` yields the same set and order as one predicate `p && q` when both predicates are deterministic and side-effect free. With stateful predicates, even apparently simple laws may fail.

### Cardinality bounds

State bounds:

- `map`: exact preservation;
- `filter`: output no greater than input;
- `flat_map`: depends on inner bounds;
- `zip`: no greater than either side;
- `chain`: sum when finite and known;
- stopping adapters: prefix bounded by source.

Bounds support reasoning about termination and collection capacity, but not exact performance.

### Ownership flow is part of type algebra

Switching from `iter` to `into_iter` changes item ownership and may make returned references impossible or cloning unnecessary. A stage table that omits ownership is incomplete Rust reasoning.

### Decision rule — Ownership flow is part of type algebra

For nontrivial pipelines, derive five properties per stage: item type, cardinality, order, ownership, and stopping. Add failure and effects when present. Only then compress into fluent syntax.

A chain can be locally type-correct and globally unreadable. The repair is usually not comments after every adapter; it is a better boundary.

### Name domain transformations

```rust
fn normalized_tags(record: &Record) -> impl Iterator<Item = &str> {
    record
        .tags
        .as_deref()
        .into_iter()
        .flat_map(|value| value.split(','))
        .map(str::trim)
        .filter(|tag| !tag.is_empty())
}
```

The caller sees a semantic view:

```rust
let tags = records.iter().flat_map(normalized_tags);
```

The helper remains lazy and borrowed.

### Separate policy from mechanics

```rust
fn is_billable(event: &Event) -> bool { ... }
fn amount(event: &Event) -> i64 { ... }

let total: i64 = events.iter().filter(|e| is_billable(e)).map(amount).sum();
```

Named functions make laws and tests possible. They also prevent one closure from mixing validation, normalization, and observation.

### Introduce a local type for a complex accumulator

Anonymous tuples in folds become positional protocols:

```rust
.fold((0_u64, 0_i64, None), |(count, total, max), item| ...)
```

Use a struct whose fields name the invariant. Local structs are inexpensive design tools.

### Materialize at real phase boundaries

Sorting, grouping, repeated traversal, ownership transfer, or a required stable snapshot may justify `collect`. A page-long chain is not improved by collecting after every third adapter.

### Preserve diagnostic context

If a helper returns `Option` merely to fit `filter_map`, ensure every `None` has the same meaning. When reasons differ, use a result or enum.

### Review at the call site

A reusable helper that makes its own body elegant may produce lifetimes or opaque types that are difficult for callers. Functional API design is judged at both sides.

### The three-line rule is not a law

Some teams limit chain length; others prefer one operation per line. Mechanical limits cannot replace semantic review. A seven-stage chain of uniform transformations may be clearer than a three-stage chain containing nested error and effect logic.

### Decision rule — The three-line rule is not a law

Name stable domain operations, accumulators, and phase boundaries. Keep adapter chains linear in meaning. When a reader must mentally execute branches, mutations, and failure recovery inside closures, expand the code.

### Pipeline

```rust
let values = records
    .iter()
    .enumerate()
    .filter_map(|(index, record)| record.payload.as_deref().map(|p| (index, p)))
    .flat_map(|(index, payload)| {
        payload.split(',').map(move |field| (index, field.trim()))
    })
    .filter(|(_, field)| !field.is_empty());
```

### Stage derivation

- `iter`: `&Record`, exact one per record, borrowed.
- `enumerate`: `(usize, &Record)`, source positions.
- `filter_map`: zero/one `(usize, &str)` per record; absence is a real optional field.
- `flat_map`: zero/many fields; inner closure uses `move` to copy `index` into the returned iterator closure while borrowing `payload`.
- `filter`: retains nonempty `(usize, &str)` items.

Order is record order, then field order. The iterator borrows from `records`. No parse error is hidden because payload absence is optional; malformed field validation belongs later.

### Adapter-order experiment

Moving `enumerate` after `filter_map` renumbers present payloads and loses original source positions. The types still compile; semantics change.

### Rejected pipeline

`flat_map(|text| text.parse::<u64>())` uses `Result` as zero-or-one iteration and discards errors. It is rejected for imports.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For derive the item type and cardinality effect of common iterator adapters, construct one positive and one causal negative example. Mark the first decisive fact in the **pipeline shape table** and state which evidence could falsify the claim.

2. **Outcome 2.** For choose correctly among `filter`, `map`, `filter_map`, `flatten`, and `flat_map`, construct one positive and one causal negative example. Mark the first decisive fact in the **pipeline shape table** and state which evidence could falsify the claim.

3. **Outcome 3.** For reason about order and truncation in `chain`, `zip`, `take`, and stopping adapters, construct one positive and one causal negative example. Mark the first decisive fact in the **pipeline shape table** and state which evidence could falsify the claim.

4. **Outcome 4.** For use `inspect` for observation without embedding required effects into a transformation, construct one positive and one causal negative example. Mark the first decisive fact in the **pipeline shape table** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

The course capstone is **LedgerFlow**, a deterministic event-analysis pipeline with diagnostics, audit history, queries, and reports. Build the ordered event-shaping pipeline and document each stage's item type, cardinality, order, borrowing, and allocation behavior. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-03-record-shaping-pipeline/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 34 when you can:

- answer the module question—“How do adapters change item type, cardinality, order, ownership, and stopping behavior across a pipeline?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Derive the item type and cardinality effect of common iterator adapters;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [Iterator adapters](https://doc.rust-lang.org/std/iter/trait.Iterator.html)
- [std::iter](https://doc.rust-lang.org/std/iter/)

[← Module 32](../../../04-rust-functional-programming/course-book/module-32-the-iterator-model/index.md) · [one-hundred-module map](../../../COURSE_MAP.md) · [Module 34 →](../../../04-rust-functional-programming/course-book/module-34-folds-scans-and-short-circuiting/index.md)

## Continue

Continue to [Module 34 — Folds, Scans, and Short-Circuiting](../module-34-folds-scans-and-short-circuiting/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
