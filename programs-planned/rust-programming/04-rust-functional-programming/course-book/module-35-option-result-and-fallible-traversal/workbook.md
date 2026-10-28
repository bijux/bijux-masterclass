# Workbook — Module 35: Option, Result, and Fallible Traversal

[Chapter](index.md) · [Laboratory](../../labs/module-05-resilient-import/README.md) · [LedgerFlow guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Option, Result, and Fallible Traversal** has become a usable model rather than remembered vocabulary. Its governing question is: *Should a fallible traversal skip, fail fast, recover, accumulate diagnostics, or continue with an explicit default?* Preserve your first prediction and record decisive facts in a **failure-policy matrix**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 34 — Folds, Scans, and Short-Circuiting that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **Should a fallible traversal skip, fail fast, recover, accumulate diagnostics, or continue with an explicit default?**
3. Draw the smallest **failure-policy matrix** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Option, Result, and Fallible Traversal** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`case-01.rs`](../../compiler-labs/module-05/case-01.rs) | Pass or fail? What exact rule decides? |
| 2 | [`case-02.rs`](../../compiler-labs/module-05/case-02.rs) | Pass or fail? What exact rule decides? |
| 3 | [`case-03.rs`](../../compiler-labs/module-05/case-03.rs) | Pass or fail? What exact rule decides? |
| 4 | [`case-04.rs`](../../compiler-labs/module-05/case-04.rs) | Pass or fail? What exact rule decides? |
| 5 | [`case-05.rs`](../../compiler-labs/module-05/case-05.rs) | Pass or fail? What exact rule decides? |
| 6 | [`case-06.rs`](../../compiler-labs/module-05/case-06.rs) | Pass or fail? What exact rule decides? |
| 7 | [`case-07.rs`](../../compiler-labs/module-05/case-07.rs) | Pass or fail? What exact rule decides? |
| 8 | [`case-08.rs`](../../compiler-labs/module-05/case-08.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 04-rust-functional-programming
```

## Part 2 — Diagnose and repair

A parser tries to be “resilient”:

```rust
let records: Vec<Record> = lines
    .filter_map(|line| parse(line).ok())
    .filter_map(|record| authorize(record).then_some(record))
    .filter_map(|record| (!seen_before(&record)).then_some(record))
    .collect();
```

The CLI then prints `0 records` and exits successfully. Missing input, malformed syntax, unauthorized records, duplicates, and an actually empty file have become observationally identical.

### Identify the information destruction

`Option` can represent an optional memo or a search miss. It cannot explain why a required input row vanished. Converting `Result` to `Option` discards the error; `then_some` discards the failed predicate's reason; duplicate filtering discards both conflict locations.

The problem is not only user messaging. The program can no longer select a correct exit status or decide whether partial results are trustworthy.

### Rebuild the topology

Create typed variants for parse, validation, authorization, duplicate identity, and transition diagnostics. Preserve physical line and stable record identity. Define two APIs:

- `parse_all`: fail fast with the first structured error;
- `inspect_all`: visit every line and return accepted records plus ordered diagnostics.

Use `Option` only for fields whose absence is itself an ordinary valid state. Use `transpose` when an optional field can fail to parse if present.

### Prove traversal policy

Add a visit probe. In fail-fast mode, later lines must not be visited. In inspection mode, every physical line is visited once. Add a duplicate fixture that reports the first and later source positions rather than silently keeping one.

### Reject seductive fixes

- replacing every error with a formatted `String` at the parser boundary;
- returning `(Vec<Record>, bool)` where the Boolean means “something went wrong”;
- collecting successes and calling rejected rows warnings;
- choosing exit status from vector length.

The repaired API should make it impossible to mistake partial success for complete success without deliberately ignoring a field.

## Part 3 — Focused exercises

### Exercise 1 — Draw nested shapes

For each type—`Option<Result<T,E>>`, `Result<Option<T>,E>`, `Result<Result<T,E1>,E2>`, and `Option<Option<T>>`—state what each layer means and which operation can change the shape without losing information.

### Exercise 2 — Prove fail-fast evaluation

Parse a list of strings with `map(parse).collect::<Result<Vec<_>, _>>()`. Design a test proving that items after the first error are not parsed.

### Exercise 3 — Accumulate without erasing order

Design a result type for an import that must return accepted records, warnings, and errors in source order while retaining each physical line number.

### Exercise 4 — Eager versus lazy defaults

A fallback allocates a large default report and increments a metric. Compare `unwrap_or(default())` and `unwrap_or_else(default)` on the `Some` path.

### Exercise 5 — Preserve source errors

A parser currently uses `map_err(|e| e.to_string())` at every stage. Replace this with a structured error that preserves source and context.

### Exercise 6 — Choose explicit control flow

Rewrite a dense chain that trims a field, treats empty as missing, parses a present number, applies a range check, emits a warning for a deprecated value, and accumulates diagnostics. Explain where combinators stop helping.

### Interleaved reasoning pass

1. For **Compose optional and fallible transformations while preserving ownership and error meaning**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the failure-policy matrix.
2. For **Use `transpose`, `flatten`, and `collect` to change container shape deliberately**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the failure-policy matrix.
3. For **Distinguish fail-fast traversal from diagnostic accumulation and implement both honestly**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the failure-policy matrix.
4. For **Choose eager and lazy defaults with awareness of evaluation and side effects**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the failure-policy matrix.

5. Identify one guarantee from an earlier course that a careless implementation of **Option, Result, and Fallible Traversal** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

The executable package is `labs/module-05-resilient-import/README.md`. This laboratory separates optional data from invalid data and fail-fast policy from accumulation policy.

### Failure topology

The line format is:

```text
id|amount|optional-note
```

Construct a topology table before coding:

| Condition | Shape | Policy |
|---|---|---|
| note absent | `Option` | valid record |
| note present and valid | `Some` | valid record |
| note present but invalid | `Result::Err` | reject line |
| invalid id/amount | `Result::Err` | reject line |
| surrounding note whitespace | warning | accept with evidence |
| duplicate id | second-phase diagnostic | retain first valid declaration |

This table is the core of the lab. Converting every row problem to `None` destroys distinctions the product needs.

### Two public batch contracts

#### `parse_all`

Return `Result<Vec<Accepted<Record, Diagnostic>>, Diagnostic>`. Collection stops at the first rejected row. Instrument the parser to prove later rows are not visited.

#### `inspect_all`

Visit every row exactly once. Return accepted values and row diagnostics in source order. A successful row can carry warnings without becoming an error.

The two functions may share a row parser, but they must not pretend to share batch policy.

### Optional-but-fallible note

Use the actual shape transformation:

```text
Option<&str>
→ Option<Result<String, Diagnostic>>
→ Result<Option<String>, Diagnostic>
```

Explain where `transpose` acts. A solution that manually duplicates the branches may compile, but it misses the lesson and is harder to audit.

### Duplicate phase

Run duplicate detection only after syntactic acceptance. The first accepted ID reserves identity. A later duplicate reports its real physical line. Do not renumber accepted records after parse errors. Because duplicate findings are produced in a later phase, merge them back with parse diagnostics by physical line using a stable ordering rule; appending them blindly can violate the public source-order contract.

### Required adversarial tests

- malformed first row prevents later visitation in fail-fast mode;
- malformed middle row does not prevent later inspection in accumulation mode;
- blank note is valid `None`;
- a note containing the prohibited character is an error, not absence;
- whitespace trimming yields one warning and the trimmed value;
- duplicate diagnostics identify the later source line;
- parse diagnostics are unchanged by adding duplicate detection;
- an earlier duplicate diagnostic is rendered before a later parse diagnostic even though detection happens in a second phase.

### Defense

Explain why `collect::<Result<Vec<_>, _>>()` is deliberately fail-fast, why `filter_map(Result::ok)` is unacceptable here, and when a separate two-channel `FromIterator` type would be a justified reusable abstraction rather than a one-off wrapper.

The executable starter and reference implementation are in [module-05-resilient-import](../../labs/module-05-resilient-import/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

### Laboratory acceptance trace

Before opening the reference implementation for **Resilient Import**, record:

- the public behavior that demonstrates **Compose optional and fallible transformations while preserving ownership and error meaning**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Day 5 separates forms of absence and failure that are easy to collapse into `None`, strings, or silent filtering. LedgerFlow must distinguish at least optional input, row rejection, nonfatal warning, duplicate identity, illegal state transition, and operational I/O failure.

### Draw the failure-topology table

Before changing code, classify each condition:

| Condition | Domain meaning | Local representation | Continue? | Appears in final report? | Exit consequence |
|---|---|---|---|---|---|

Examples include a missing optional memo, an invalid amount, a duplicate event ID, a warning about normalized whitespace, a transition rejected by the ledger, and failure to read the input file.

Do not choose `Option` merely because processing may continue. `Option` represents presence or absence; it does not explain why a required row vanished.

### Define row outcomes

Create a row result capable of representing:

- an accepted event with zero or more warnings;
- a rejected row with one or more structured diagnostics;
- an ignorable physical line whose status is intentional rather than erroneous.

Preserve physical line number and enough field context to explain the rejection. Avoid converting source errors into strings before the shell renders them.

### Implement both traversal policies

#### Fail-fast mode

Use `collect::<Result<Vec<_>, _>>()`, `try_fold`, or an explicit equivalent to stop at the first rejected row. Add a probe proving that later rows are not visited. Document the returned error and whether already parsed values survive.

#### Inspection mode

Visit every physical line exactly once. Accumulate accepted events, warnings, and rejection diagnostics in stable source order. The final type must make partial success visible; returning only `Vec<Event>` is insufficient.

The two modes may share a row parser but must not share a return type that lies about their policy.

### Shape transformations

Use and explain at least two of these transformations where they naturally arise:

- `Option<Result<T, E>>::transpose()` for an optional field whose present text can fail to parse;
- `Result<Option<T>, E>` when lookup may fail operationally but absence is otherwise normal;
- `collect::<Result<Vec<T>, E>>()` for fail-fast traversal;
- `partition` or an explicit accumulator when all outcomes must be retained.

Do not use `flatten` to erase errors.

### Duplicate identity policy

Define whether the first or later duplicate is authoritative, whether both source locations are reported, and whether a duplicate prevents ledger reduction. Add a fixture with three appearances of the same ID. Diagnostics must contain enough information to reconstruct the conflict.

### Capstone invariant trace

For the Module 35 LedgerFlow increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Do not advance because the calendar day ended. Advance when all hard evidence is present.

### Advancement decision

Advance only when each absence or failure has an explicit continuation policy and source-order behavior remains predictable under accumulation.

### Closed-book retrieval

1. What semantic difference separates `None` from `Err`?
2. What shapes do `flatten` and `transpose` change?
3. How does `collect::<Result<Vec<_>, E>>()` traverse?
4. Why is validation accumulation not just a different spelling of `Result`?
5. When is `unwrap_or_else` preferable to `unwrap_or`?
6. What information is destroyed by `.ok()`?
7. Where should line number context be attached?
8. Why can `?` improve clarity in one stage and hide topology in a long chain?
9. How do warnings coexist with an accepted value?
10. What rule decides whether processing continues after an error?

### Reconstruction task

Implement the same row import twice: once fail-fast with `collect::<Result<_, _>>()`, once accumulating structured diagnostics while retaining valid rows. Compare their public result types.

### Transfer task

Design a configuration importer with required fields, optional fields, warnings, row-local errors, and one global uniqueness check. Produce:

- failure-policy matrix for skip, default, recover, fail-fast, and accumulate;
- source-order rule for accepted values and diagnostics;
- error context retained at the row or field boundary;
- test proving that one rejected record cannot corrupt accepted state;

### Spaced review

Repeat questions 2, 4, 7, and 10 after 24 hours. Repeat the reconstruction after seven days with a different domain.

### Closed-book defense

In five minutes, answer “Should a fallible traversal skip, fail fast, recover, accumulate diagnostics, or continue with an explicit default?” using the **failure-policy matrix**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside LedgerFlow. A list of APIs without the deciding relationship is incomplete.
