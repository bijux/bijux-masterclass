# Workbook — Module 40: Functional Architecture Synthesis

[Chapter](index.md) · [Laboratory](../../labs/module-10-route-analysis-engine/README.md) · [LedgerFlow guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Functional Architecture Synthesis** has become a usable model rather than remembered vocabulary. Its governing question is: *How do closure, iterator, error, reduction, structural-sharing, and effect decisions compose into a readable whole system?* Preserve your first prediction and record decisive facts in a **whole-pipeline architecture map**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 39 — Combinator Laws and Cost Models that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **How do closure, iterator, error, reduction, structural-sharing, and effect decisions compose into a readable whole system?**
3. Draw the smallest **whole-pipeline architecture map** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Functional Architecture Synthesis** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`case-01.rs`](../../compiler-labs/module-10/case-01.rs) | Pass or fail? What exact rule decides? |
| 2 | [`case-02.rs`](../../compiler-labs/module-10/case-02.rs) | Pass or fail? What exact rule decides? |
| 3 | [`case-03.rs`](../../compiler-labs/module-10/case-03.rs) | Pass or fail? What exact rule decides? |
| 4 | [`case-04.rs`](../../compiler-labs/module-10/case-04.rs) | Pass or fail? What exact rule decides? |
| 5 | [`case-05.rs`](../../compiler-labs/module-10/case-05.rs) | Pass or fail? What exact rule decides? |
| 6 | [`case-06.rs`](../../compiler-labs/module-10/case-06.rs) | Pass or fail? What exact rule decides? |
| 7 | [`case-07.rs`](../../compiler-labs/module-10/case-07.rs) | Pass or fail? What exact rule decides? |
| 8 | [`case-08.rs`](../../compiler-labs/module-10/case-08.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 04-rust-functional-programming
```

## Part 2 — Diagnose and repair

The final program contains one seventy-line chain with five `filter_map(Result::ok)` calls, nested boxed closures, output in `inspect`, a tuple fold, three unexplained `collect`s, and a final `.unwrap_or_default()`.

No individual adapter is inherently wrong. The failure is architectural: data, ownership, diagnostics, effects, and materialization are interleaved so thoroughly that no reviewer can state the product contract.

### Stabilize behavior before refactoring

Capture fixtures for valid input, malformed rows, duplicates, arithmetic rejection, empty input, and output ordering. Record the current observed behavior, including behavior that is wrong but relied upon by no contract. Do not refactor a system whose semantics are still implicit.

### Expand the chain

Rewrite the path as an explicit loop with named values. Recover every point where an error was discarded, a collection was created, or an effect occurred. Attach physical source positions before filtering. Replace the tuple accumulator with a named state. Return output actions as data.

Only then draw the four-flow map:

- data shape;
- ownership and borrowing;
- failure and diagnostics;
- effects and exit status.

### Reintroduce abstraction selectively

Use standard adapters where one adapter names one coherent stage. Keep a loop when several outputs, diagnostic accumulation, or complex control flow would become less visible in a chain. Retain necessary collection boundaries for sorting or replay and remove accidental ones.

### Proof obligations

- no malformed input disappears;
- stable output order is explicit;
- a rejected transition cannot partially commit;
- the pure core runs in memory;
- every `collect` has a named downstream requirement;
- every boxed callable corresponds to runtime heterogeneity;
- no fallback turns failure into a plausible empty success.

### Clinic: Architecture transfer exercise

After repair, add an account-prefix query. Update the transformation map first, then implementation and tests. If you cannot locate the affected stages without reading every line of code, the architecture is still insufficiently explicit.

The clinic is complete when removing complexity has increased visible semantics rather than merely reduced line count.

## Part 3 — Focused exercises

### Exercise 1 — Build the transformation map

For an unseen inventory import, map bytes/text, physical lines, parsed rows, normalized records, deduplicated events, state reduction, lazy queries, report model, rendered bytes, and exit status. Include ownership, cardinality, order, failure, and effects.

### Exercise 2 — Review a stage contract

A stage named `valid_rows` returns `impl Iterator<Item=Row>` but silently drops malformed input and logs to stderr inside `filter_map`. Identify every contract defect and redesign it.

### Exercise 3 — Implement an unseen feature method

Describe the exact workflow for adding “ignore events after a per-account accepted-event limit” without writing code. Include questions that must be settled before implementation.

### Exercise 4 — Detect semantic drift

A refactor replaces an explicit accumulation loop with `collect::<Result<Vec<_>, _>>()`. The tests still pass. What behavior may have changed, and what evidence should be added?

### Exercise 5 — Architecture rejection record

Write three rejection records: boxing every iterator, collecting after every stage, and abstracting every effect behind one large trait.

### Exercise 6 — Course handoff

Identify what Course 5 may automate with macros and what must remain conceptually explicit after metaprogramming.

### Interleaved reasoning pass

1. For **Produce a transformation map that identifies source, shape, ownership, failure, state, and effect boundaries**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the whole-pipeline architecture map.
2. For **Integrate closures, iterators, folds, error traversal, custom protocols, and effect isolation coherently**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the whole-pipeline architecture map.
3. For **Refactor between loops and combinators without changing observable behavior**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the whole-pipeline architecture map.
4. For **Implement an unseen feature across parser, transformation core, reducer, report, CLI, and tests**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the whole-pipeline architecture map.

5. Identify one guarantee from an earlier course that a careless implementation of **Functional Architecture Synthesis** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

The executable crate is `labs/module-10-route-analysis-engine/README.md`. This is an independent transfer laboratory. It uses Course 4 mechanisms but does not copy LedgerFlow’s domain or architecture mechanically.

### Product contract

Input rows have the form:

```text
route|from|to|distance
```

The core parses rows, supports fail-fast and accumulating inspection, groups valid legs by route, validates continuity in source order, computes checked distance, exposes lazy summary queries, renders deterministic text, and produces an exit classification. It performs no filesystem access.

### Architecture record before implementation

Create a transformation map with separate rows for:

1. physical line enumeration;
2. row parsing;
3. fail-fast traversal;
4. accumulated inspection;
5. route grouping;
6. route-local continuity reduction;
7. checked distance aggregation;
8. accepted/diagnostic result assembly;
9. lazy query;
10. deterministic rendering.

For each row, state item type, ownership, cardinality, order, failure policy, and materialization. This map is graded before code.

### Critical policy decisions

- Route leg order is source order, not lexical endpoint order.
- Group order and final report order are deterministic by route key.
- A disconnected route yields no partial summary.
- Parse errors can accumulate independently from route-validation errors.
- Overflow is a typed route diagnostic.
- An empty route group is representable in the reducer API even if grouping normally cannot create one.
- Queries borrow accepted summaries and allocate nothing by default.

### Milestone proofs

#### Parsing

Prove one-based physical line context and distinguish field-count from distance errors. `parse_all` stops at first failure; `inspect_all` continues.

#### Reduction

Trace a three-leg route. At each step record expected origin, current destination, leg count, and checked total. Then inject a disconnected middle leg and prove no accepted summary is emitted.

#### Integration

Combine accumulated parse diagnostics with route diagnostics without losing either order contract. Use a deterministic map for group traversal or sort explicitly with a documented key.

#### Query and rendering

Query by route prefix and optional maximum distance through a borrowed iterator. Render accepted summaries and diagnostics deterministically. Repeated rendering of the same `Analysis` must be byte-identical.

### Laboratory: Architecture transfer exercise

Add a maximum-leg filter across analysis, query, rendering, and tests. Decide whether it filters accepted summaries or rejects routes during reduction; justify the selected product semantics. Do not copy LedgerFlow command code.

### Defects to hunt

- `filter_map(Result::ok)` dropping bad rows;
- `HashMap` report order assumed stable;
- sorting legs and thereby fabricating connectivity;
- partial summary retained after a disconnected leg;
- unchecked distance arithmetic;
- query returning cloned summaries;
- filesystem reads inside the analysis function;
- one 70-line chain with no named stage contracts.

### Final checks and explanation
Submit the transformation map, parser visitation tests, reducer trace, deterministic report proof, lazy query evidence, transfer feature, and a comparison with LedgerFlow identifying at least three deliberate architectural differences. Defend every materialization point and every error-policy boundary. A green suite without a coherent map does not pass.

The executable starter and reference implementation are in [module-10-route-analysis-engine](../../labs/module-10-route-analysis-engine/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

### Laboratory acceptance trace

Before opening the reference implementation for **Route Analysis Engine**, record:

- the public behavior that demonstrates **Produce a transformation map that identifies source, shape, ownership, failure, state, and effect boundaries**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Day 10 is not a feature roundup. It is the proof that you can reason across callable contracts, iterator state, fallible traversal, reducers, persistent structure, effect boundaries, laws, and materialization choices without following a tutorial sequence.

### Freeze the four-flow map

Produce a final architecture map with four parallel flows:

1. **data** — raw text to accepted events to ledger state to report values;
2. **ownership** — borrowed source slices, owned events, persistent shared history, and materialized reports;
3. **failure** — operational errors, row diagnostics, duplicate conflicts, transition rejection, and exit classification;
4. **effects** — file reads, writes, terminal output, and process status.

For every stage, record item types, cardinality, order, laziness, and allocation. A single arrow labeled “process” is not acceptable.

### Architecture council

Review the complete system against these questions:

- Is any diagnostic silently discarded?
- Is any `Option` standing in for an unexplained failure?
- Does any lazy view outlive the owner it borrows?
- Is any collection created only to satisfy the next line of code?
- Is any closure boxed without runtime heterogeneity?
- Does any reducer expose partially committed state after failure?
- Is any output order derived from an unordered collection without sorting?
- Does the core perform hidden I/O or consult global state?
- Is any law stated without preconditions or counterexamples?
- Is any performance statement stronger than the evidence?

Record every finding as keep, repair, or explicitly accepted limitation.

### Unseen feature

Implement one cross-cutting requirement provided only as behavior, such as:

- account-prefix selection for queries and reports;
- a maximum accepted-event bound that still reports later physical-row diagnostics according to a specified policy;
- balance checkpoints emitted every `n` accepted events;
- a report mode that groups diagnostics by source line while preserving stable order within a line.

The feature must update the transformation map before code. Identify every affected stage, then add tests first at the pure core and finally at the CLI boundary. Copying a reference implementation is not permitted.

### Refactoring defense

Select and defend three rejected designs:

1. one long iterator chain replaced by named stages or a loop;
2. one premature `collect` removed or one necessary materialization retained;
3. one effect abstraction rejected in favor of an explicit value or narrow shell function.

The defense must discuss semantics, not taste.

### Final proof route

From a clean checkout, run the published verification route. Save:

- formatting, checking, lint, test, rustdoc, and release-build output where available;
- compiler-prediction results;
- capstone demonstration output;
- the final evidence-ledger verification;
- one intentionally failing test or specimen and the diagnosis used to repair it.

Tool unavailability must be recorded as unavailable, not passed.

### Oral defense

Without opening the implementation, explain:

- why parsing preserves physical line identity;
- why fail-fast and accumulation modes have different types;
- where laziness ends and why;
- how failure atomicity is enforced;
- what audit versions share;
- why the core is deterministic;
- which combinator laws are conditional;
- which cost claims are observations versus contracts.

### Capstone invariant trace

For the Module 40 LedgerFlow increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Do not advance because the calendar day ended. Advance when all hard evidence is present.

### Advancement decision

Advance only when you can redraw the whole system from source bytes to rendered output, locate every materialization and effect, and explain each failure policy and order guarantee.

### Closed-book retrieval

1. Can you reconstruct LedgerFlow’s full transformation map from memory?
2. Where does every materialization occur, and why?
3. Which stages are lazy, and what triggers them?
4. Where are diagnostics accumulated rather than short-circuited?
5. What makes state reduction failure-atomic?
6. Which order guarantees are product contracts?
7. Which operations are deterministic core and which are shell effects?
8. What persistent structure is retained, and what does sharing cost?
9. Which reusable combinator laws are actually claimed?
10. How would you add a feature without semantic drift?

### Reconstruction task

Recreate LedgerFlow’s stage map from memory, then implement one thin vertical slice—parse, validate, reduce, query, render—without consulting the capstone guide.

### Transfer task

Add a cross-account transfer event with two-sided validation and failure-atomic reduction. Show how the change crosses parsing, diagnostics, state, audit history, queries, rendering, and tests. Produce:

- whole-system dataflow from source to report;
- ownership, failure, ordering, and effect boundary at each stage;
- one architectural alternative rejected with reason;
- cross-layer regression test for the unseen feature;

### Spaced review

Repeat questions 2, 4, 7, and 10 after 24 hours. Repeat the reconstruction after seven days with a different domain.

### Closed-book defense

In five minutes, answer “How do closure, iterator, error, reduction, structural-sharing, and effect decisions compose into a readable whole system?” using the **whole-pipeline architecture map**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside LedgerFlow. A list of APIs without the deciding relationship is incomplete.
