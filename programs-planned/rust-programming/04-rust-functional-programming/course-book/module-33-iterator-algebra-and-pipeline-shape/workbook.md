# Workbook — Module 33: Iterator Algebra and Pipeline Shape

[Return to the chapter](index.md) · [Open the LedgerFlow engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether you can use **Iterator Algebra and Pipeline Shape** without relying on surface syntax. Keep the module question in view: *How do adapters change item type, cardinality, order, ownership, and stopping behavior across a pipeline?* For every task, identify the program point where the decisive type, ownership, dispatch, failure, or cost relationship is established. Compile only after committing to a prediction, and preserve the smallest counterexample that changes your model.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Iterator Algebra and Pipeline Shape** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`case-01.rs`](../../compiler-labs/module-03/case-01.rs) | Pass or fail? What exact rule decides? |
| 2 | [`case-02.rs`](../../compiler-labs/module-03/case-02.rs) | Pass or fail? What exact rule decides? |
| 3 | [`case-03.rs`](../../compiler-labs/module-03/case-03.rs) | Pass or fail? What exact rule decides? |
| 4 | [`case-04.rs`](../../compiler-labs/module-03/case-04.rs) | Pass or fail? What exact rule decides? |
| 5 | [`case-05.rs`](../../compiler-labs/module-03/case-05.rs) | Pass or fail? What exact rule decides? |
| 6 | [`case-06.rs`](../../compiler-labs/module-03/case-06.rs) | Pass or fail? What exact rule decides? |
| 7 | [`case-07.rs`](../../compiler-labs/module-03/case-07.rs) | Pass or fail? What exact rule decides? |
| 8 | [`case-08.rs`](../../compiler-labs/module-03/case-08.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 04-rust-functional-programming
```

## Part 2 — Diagnose and repair

The import pipeline looks concise:

```rust
let rows = text
    .lines()
    .filter(|line| !line.trim().is_empty())
    .filter_map(|line| parse_row(line).ok())
    .enumerate()
    .zip(scores)
    .inspect(|(row, _)| write_audit(row))
    .collect::<Vec<_>>();
```

It is also wrong in four independent ways.

### Reconstruct the real stage behavior

1. Blank-line filtering occurs before numbering, so `enumerate` produces post-filter positions rather than physical line numbers.
2. `filter_map(Result::ok)` converts every parse failure into absence. The final count cannot distinguish invalid input from a genuinely empty file.
3. `zip` silently ends with the shorter input. Extra rows or scores disappear unless equal length was proved beforehand.
4. `inspect` performs required I/O. Because the pipeline is lazy, audit writes occur only when and as far as a consumer pulls, and a later failure may leave partial effects.

### Repair from semantics outward

First rewrite the operation as a loop. Attach source positions at the boundary. Keep `Result` or a row-outcome enum. Validate pairing cardinality. Return audit actions as data instead of executing them during traversal. Only after equivalence tests pass should you reintroduce adapters for stages that remain one coherent transformation.

A readable repaired outline might have named streams:

```rust
let source_lines = attach_positions(text.lines());
let classified = classify_lines(source_lines);
let parsed = parse_classified(classified);
let paired = pair_with_validated_scores(parsed, scores)?;
```

The names expose stage boundaries; they do not require intermediate collections.

### Prove no evidence disappeared

Use a fixture containing a comment, a malformed row, a blank line, and a valid later row. Assert physical positions, retained diagnostics, later-row visitation, and zero audit writes before the shell executes a completed plan.

### Transfer question

When would `filter_map` be correct here? It is appropriate for a stage whose explicit contract is “yield zero or one value,” such as ignoring comment lines after they have already been classified and counted. It is not an error policy.

## Part 3 — Focused exercises

### Exercise 1 — Pipeline shape ledger

For `rows.iter().enumerate().filter(|(_, r)| !r.starts_with('#')).filter_map(|(i, r)| parse(r).ok().map(|x| (i, x))).flat_map(expand)`, record the item type after every stage, cardinality behavior, ordering, and what information is lost.

### Exercise 2 — Choose the adapter

Choose among `map`, `filter`, `filter_map`, `flatten`, and `flat_map` for: converting every amount to cents; retaining active records; parsing optional notes; yielding every tag from every record; removing one `Option` layer. Justify each choice by cardinality and item type.

### Exercise 3 — Find the truncation bug

An implementation zips invoice rows with tax rates loaded from another source. It produces plausible output when one source has fewer rows. Design a repair that makes length mismatch explicit.

### Exercise 4 — Position before or after filtering

A report must show physical source line numbers and also rank accepted records from zero. Construct one pipeline that preserves both numbers and explain where each `enumerate` belongs.

### Exercise 5 — Remove required effects from `inspect`

A pipeline uses `inspect(|row| audit_file.write_all(...))` to satisfy a legal audit requirement. Explain why this is fragile and redesign the boundary.

### Exercise 6 — Refactor a long chain

Take a chain with parsing, normalization, filtering, expansion, sorting, and rendering. Identify where laziness must end and split it into semantic stages without collecting after every adapter.



## Part 4 — Independent laboratory

Use `labs/module-03-record-shaping-pipeline/README.md` for the executable package. The purpose is to make every shape change reviewable.

### Input and output model

Each survey may omit its payload. A present payload contains comma-separated labels. A separate score string contains comma-separated integers. Successful output is a sequence of observations carrying the original record index, original field index, normalized label, and parsed score.

Before implementation, write a stage table:

| Stage | Item type | Cardinality per input | Order | Ownership | Failure channel |
|---|---|---|---|---|---|
| source | | | | | |
| optional payload selection | | | | | |
| field expansion | | | | | |
| empty-field removal | | | | | |
| score parsing | | | | | |
| pairing | | | | | |
| materialization | | | | | |

The table must reveal two semantic traps: filtering before `enumerate` changes identity, and `zip` truncates silently unless equal length is proven first.

### Construction

1. Implement a borrowed `fields` view. Enumerate surveys before optional selection and fields before empty-field removal so retained positions remain original positions.
2. Split labels and scores into temporary borrowed **raw slot** slices without filtering. Materialization at this boundary is justified because slot counts must be compared before pairing.
3. Reject unequal raw slot counts with `ShapeError::LengthMismatch`; do not let `zip` define policy.
4. After positions are paired, omit a slot only when both sides are empty. Report `MissingLabel` or `MissingScore` for one-sided emptiness. This prevents compaction from pairing unrelated positions.
5. Parse scores into typed errors containing the original field position. Do not use `filter_map(Result::ok)`.
6. Normalize labels only after a successful positional pair exists, and materialize the final `Vec<Observation>` once the validated batch is complete.

### Semantic mutation tests

Write tests that would fail if a maintainer performed each of these apparently harmless reorderings:

- move `enumerate` after `filter_map`;
- move field `enumerate` after empty filtering;
- filter empty slots independently before length validation or pairing;
- call `zip` before length validation;
- parse scores through `.ok()`;
- sort labels before pairing;
- use `inspect` to perform required output writes.

The test names should state the preserved contract, not the adapter used.

### Transfer: aliases with provenance

Chain an optional alias stream after primary labels. Every yielded pair must carry `"primary"` or `"alias"` provenance. Do not merge the collections and rediscover origin by index. Preserve primary order followed by alias order.

### Defense

Explain why optional payload absence is not a parse error, why an iterator chain can compile while changing identity semantics, and why `zip` is a mechanism rather than a validation policy. Be able to replace the pipeline with a loop and show that both implementations preserve the same stage contract.

The executable starter and reference implementation are in [module-03-record-shaping-pipeline](../../labs/module-03-record-shaping-pipeline/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

## Part 5 — Capstone transfer

Day 3 turns the physical input stream into named lazy stages. The primary risk is not syntax. It is changing cardinality, order, or source positions without noticing. The increment therefore begins with a **transformation-shape map**, then implements only the stages whose contracts are explicit.

### Preserve physical evidence first

LedgerFlow diagnostics refer to physical input lines. Attach line numbers before removing comments, blank rows, or headers. An `enumerate` placed after filtering gives logical positions, not source positions, and would make every later diagnostic misleading.

Write the first stage as a stream of source records equivalent to:

```rust
struct SourceLine<'a> {
    number: usize,
    text: &'a str,
}
```

The representation may differ, but line identity must survive through parsing and rejection.

### Build the transformation-shape map

Fill one row for every stage:

| Stage | Input item | Output item | Cardinality | Order | Borrowed/owned | Failure channel | Lazy/eager |
|---|---|---|---|---|---|---|---|

Include at least:

1. physical line attachment;
2. header recognition;
3. ignorable-line classification;
4. field splitting;
5. event parsing;
6. optional expansion or normalization;
7. accepted-event selection.

If a stage can produce zero, one, or many outputs, write that explicitly. Do not use “iterator” as an item description.

### Implementation constraints

- `filter` may remove only lines whose removal is the declared product behavior.
- `filter_map` may express a real zero-or-one transformation, but may not turn `Err` into disappearance.
- `flat_map` must be justified by one-to-many semantics, not used to avoid naming a nested structure.
- `zip` is permitted only after proving equal length or accepting truncation as the contract.
- `inspect` may observe for diagnostics during development but must not perform required writes or state transitions.
- Do not collect merely to make the next adapter easier. Materialize only where a later stage requires ownership, sorting, replay, or random access.

### Readability refactor

Implement the import first as an explicit loop that preserves all outputs and diagnostics. Use it as the semantic baseline. Then refactor selected stages to adapters. Compare results on the same fixture. Any semantic difference is a defect in the refactor, not evidence that the chain is “more functional.”

Name intermediate iterators when a chain crosses more than one semantic boundary. A reader should see parsing, validation, and selection as distinct operations even if all remain lazy.

### Adversarial cases

Add fixtures for:

- comments before and after malformed rows;
- a malformed first data row;
- adjacent blank lines;
- an expansion that yields two events from one source row, if supported;
- two collections of unequal length presented to any pairing operation;
- a valid row after an invalid row, proving later evidence is not erased in accumulation mode.

## Part 6 — Reconstruct and defend

Do not advance because the calendar day ended. Advance when all hard evidence is present.

### Advancement decision

Advance only when you can annotate every adapter with item type, cardinality, order, ownership, stopping behavior, and materialization.

### Closed-book retrieval

1. How do `filter` and `filter_map` differ in output type and failure risk?
2. What one nesting layer does `flatten` remove?
3. What order does `flat_map` preserve?
4. When does `zip` silently truncate?
5. Why does the position of `enumerate` change meaning?
6. What does `take_while` do with the first item that fails the predicate?
7. Why must `inspect` not carry required business effects?
8. How do you calculate a pipeline cardinality range?
9. When does naming a stage improve type errors?
10. What evidence shows an intermediate `collect` is necessary rather than convenient?

### Reconstruction task

Rebuild a pipeline that parses comma-separated rows, preserves empty fields, expands nested tags, and reports original row numbers. Name every stage before writing the chain.

### Transfer task

Transform nested invoice lines into a stable flat report without losing source association or silently truncating mismatched sequences. Produce:

- stage map with item type, cardinality, order, and ownership after every adapter;
- justification for the placement of `collect`;
- one edge case involving zero, one, or many outputs;
- test detecting accidental compaction, reordering, or eager allocation;

### Spaced review

Repeat questions 2, 4, 7, and 10 after 24 hours. Repeat the reconstruction after seven days with a different domain.
