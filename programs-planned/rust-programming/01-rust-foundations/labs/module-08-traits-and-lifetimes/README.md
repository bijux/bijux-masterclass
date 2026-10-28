# Laboratory 8 — Trait and Lifetime Boundary

**Course 1 · Module 8: Generics, Traits, Conversions, and Lifetime Basics**

[Chapter](../../course-book/module-08-generics-traits-conversions-and-lifetime-basics/index.md) · [Workbook](../../course-book/module-08-generics-traits-conversions-and-lifetime-basics/workbook.md) · [Taskboard guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Generics, Traits, Conversions, and Lifetime Basics**: What behavior is genuinely shared, what constraints make it valid, and what borrow relationship must a signature expose? The product must make **Write generic functions and types whose bounds correspond to operations actually performed** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **trait and lifetime contract** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> What behavior is genuinely shared, what constraints make it valid, and what borrow relationship must a signature expose?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

### Purpose

Build a reusable but bounded report system. The lab tests whether you can distinguish justified genericity from abstraction for its own sake.

### Domain

```rust
struct Metric {
    name: String,
    value: i64,
}

struct Report {
    title: String,
    metrics: Vec<Metric>,
}
```

Invariants:

- titles and metric names are trimmed, nonempty, and at most 80 bytes;
- names contain no tabs or line breaks;
- metric names are unique within a report;
- canonical output sorts metrics by name.

### Required traits

Implement standard traits where justified:

- `Display` for a compact `Metric` view;
- `FromStr` for one metric line;
- `TryFrom<(String, i64)>` for validated `Metric` construction;
- `Default` for an empty `Report` only if the title policy gives it a meaningful title; otherwise do not implement it.

Define at most one custom trait. If you define one, the design document must show at least two meaningful implementations and one generic caller. No custom trait is also a valid and likely outcome.

### Required generic functions

```rust
fn load_report<R: BufRead>(reader: R) -> Result<Report, ReportError>;
fn write_report<W: Write>(writer: &mut W, report: &Report) -> Result<(), ReportError>;
fn extrema<T: Ord>(values: &[T]) -> Option<(&T, &T)>;
```

### Lifetime task

Implement:

```rust
fn choose_metric<'a>(left: &'a Metric, right: &'a Metric) -> &'a Metric;
```

Then implement a function that always returns from the first report while accepting an unrelated second borrow, using separate lifetimes.

### Tests

- all standard-trait round trips;
- invalid names and duplicate metrics;
- generic in-memory read/write;
- exact deterministic bytes;
- write failure using a small custom writer that fails after a byte limit;
- lifetime functions exercised with nested scopes;
- generic extrema for integers and strings;
- a compile-fail explanation for a returned local reference.

### Design document

Explain:

- each generic parameter and bound;
- where monomorphization occurs conceptually;
- every owned versus borrowed field;
- why each standard trait matches its semantic law;
- whether a custom trait survived review;
- which allocations canonical sorting performs;
- why the codec does not know filesystem paths.

### Acceptance

The lab passes only when removing any bound either makes a body operation illegal or broadens semantics incorrectly. Redundant bounds and artificial traits are defects, not extra credit.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Trait and Lifetime Boundary**.
2. Draw the smallest **trait and lifetime contract** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to Taskboard so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 8 — Trait and Lifetime Boundary**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Trait and Lifetime Boundary**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Write generic functions and types whose bounds correspond to operations actually performed.
- Define and implement small traits as behavioral contracts without abstraction theater.
- Use Display, Error, From, FromStr, Read, BufRead, and Write at natural boundaries.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 8 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **trait and lifetime contract**. Defend why your design is simpler than one plausible alternative under the new requirements.
