# 40 — Functional Architecture Synthesis

**Course 4, day 10 · Module 40 of 90**  
`█████████████░░░░░░░` **40/90**

[← Module 39: Combinator Laws and Cost Models](../module-39-combinator-laws-and-cost-models/index.md) · [Course 4 overview](../index.md) · [Ninety-module map](../../../COURSE_MAP.md) · [Module 41: Metaprogramming Boundaries and the Expansion Model →](../../../05-rust-metaprogramming/course-book/module-41-metaprogramming-boundaries-and-expansion-model/index.md)

## The question

> How do closure, iterator, error, reduction, structural-sharing, and effect decisions compose into a readable whole system?

## Why this comes now

The final module removes the last local boundary. Closures, lazy traversal, fallible parsing, reductions, structural sharing, reporting, and effects must form one readable system. An unseen requirement tests whether you can revise the dataflow without destroying determinism or hiding failure.

## What you will be able to do

- Produce a transformation map that identifies source, shape, ownership, failure, state, and effect boundaries.
- Integrate closures, iterators, folds, error traversal, custom protocols, and effect isolation coherently.
- Refactor between loops and combinators without changing observable behavior.
- Implement an unseen feature across parser, transformation core, reducer, report, CLI, and tests.
- Defend the architecture, its rejected alternatives, and its remaining limits under oral review.

For an unfamiliar problem, map the stages before choosing syntax.

Example batch analysis:

```text
bytes
  -> decoded lines
  -> parsed records / parse diagnostics
  -> normalized records
  -> duplicate partition
  -> ordered accepted events
  -> state reduction / transition diagnostics
  -> lazy queries
  -> materialized report
  -> rendered text
  -> shell effects and exit code
```

For each arrow, record:

- input and output type;
- ownership transfer or borrow;
- cardinality;
- order;
- failure policy;
- effects;
- materialization;
- reusable law.

## Core model

### Stage boundaries must earn names

Parsing and validation often deserve separate stages because syntax failure and domain invalidity differ. Normalization may precede duplicate detection if identifiers have canonical form. Sorting before validation can change which duplicate is considered first.

### Avoid one universal pipeline type

Different stages need different semantics: borrowed iterators, owned vectors, result items, diagnostic batches, maps, and reports. Wrapping every stage in one custom `Pipeline<T>` can erase useful distinctions.

### Decision record

Write why a stage is lazy or eager, why it fails fast or accumulates, and why order is preserved or changed. These decisions are more important than adapter selection.

A stage contract should be reviewable without reading implementation.

```text
Stage: parse lines
Input: Iterator<Item = (usize, &str)>
Output: Iterator<Item = Result<RawEvent, ParseDiagnostic>>
Ownership: borrows input text; RawEvent may borrow or own according to boundary
Cardinality: exactly one result per non-header line
Order: source order
Failure: represented per item; traversal continues
Effects: none
```

A later stage may materialize:

```text
Stage: detect duplicate IDs
Input: Vec<Event>
Output: Batch<Event, Diagnostic>
Ownership: consumes events
Cardinality: every event appears in accepted or rejected exactly once
Order: accepted and diagnostics preserve source order
Effects: none
```

### Contract tests

Tests should distinguish:

- zero/one/many cardinality;
- stable order;
- duplicate policy;
- short-circuit versus continuation;
- borrowed versus owned lifetime behavior where compile-fail evidence is useful;
- absence of external effects in the core.

### Stage leakage

A parser that reads files, a validator that prints, or a renderer that mutates domain state violates separation. Merge stages only when the combined contract remains coherent.

### Decision rule

Write stage contracts in types and prose before implementation. If a stage requires several unrelated failure policies or effects, split it.

A complete architecture uses mechanisms for distinct pressures.

- closures capture local policy;
- generic callable bounds preserve static type and ownership contracts;
- iterators expose lazy views and one-pass sources;
- adapters shape item streams;
- folds reduce ordered events into state;
- `Result` and diagnostics encode different failure topologies;
- custom iterators protect representation while exposing domain traversal;
- persistent structures retain versions where required;
- the shell performs external effects.

### Do not force uniformity

A capstone may use an explicit loop for parse accumulation, an iterator chain for a query, `try_fold` for all-or-nothing state application, and local mutation inside owned maps. Coherence comes from contracts, not one syntax.

### Mechanism conflicts

A lazy borrowed query cannot outlive its report. A persistent snapshot may keep large substructures alive. A closure stored in a long-lived object may prolong borrows. A fail-fast consumer may prevent later diagnostics. Integration requires resolving these constraints explicitly.

### Phase ordering

Normalize before laws that assume canonical data. Validate before state reduction. Materialize before sorting. Render after deterministic ordering. Execute effects after the core result is complete enough to justify them.

### Decision rule

Use each mechanism at the pressure it solves. Review cross-stage ownership and failure interactions, especially where laziness or stored closures extend lifetimes.

A syntax rewrite is correct only if observable behavior remains stable.

### Preserve more than output values

Check:

- item order;
- number and order of callback invocations;
- short-circuit point;
- boundary-item consumption;
- error selected first;
- diagnostics accumulated;
- side effects and their order;
- overflow behavior;
- source usability afterward.

### Loop to chain example

A loop that parses every line and accumulates all errors cannot be replaced by `collect::<Result<Vec<_>, _>>()`; that changes continuation to fail-fast.

A loop that stops at the first matching record can often become `find`, provided predicate effects and borrow semantics match.

### Chain to loop example

Expand a complex fold into a loop to name intermediate states. Keep tests fixed. If the loop reveals hidden error loss, repair the product contract before compressing again.

### Differential tests

During refactoring, run old and new implementations on generated small inputs and compare structured results. Include malformed and boundary cases.

### Cost changes

A semantically equivalent rewrite may allocate or traverse differently. Record cost changes separately and measure before claiming improvement.

### Decision rule

Define observable equivalence before refactoring. Use differential tests and preserve failure, effect, and consumption semantics—not just final happy-path values.

An independent feature proves transfer because no chapter provides its exact implementation.

### Method

1. Restate the requirement as observable behavior.
2. Mark affected stages in the transformation map.
3. Add failing public tests.
4. Decide whether the feature changes item shape, order, failure, state, effects, or all five.
5. Implement the smallest coherent stage changes.
6. Add law and counterexample tests.
7. Run the complete proof route.
8. Defend rejected alternatives.

### Example: account prefix query

A new CLI query may require:

- parser support for the command;
- normalization of the prefix;
- a lazy account iterator;
- deterministic sort policy;
- renderer changes;
- exit behavior for no matches;
- process tests.

It should not require changing event reduction if the query is read-only.

### Prevent feature leakage

Do not add query-specific fields to core state unless they represent stable domain data. Derived indexes may be justified for performance later, but first implement correct semantics.

### Decision rule

Treat unseen work as a contract change across named stages. Do not begin by searching for an adapter that resembles the feature.

A review should challenge both correctness and unnecessary cleverness.

### Dataflow

- Are stage types explicit?
- Is cardinality change deliberate?
- Is order stable where required?
- Are grouping and sorting policies deterministic?

### Ownership

- Can borrowed outputs outlive their owners?
- Is consuming iteration used when sources are no longer needed?
- Are clones and `Rc` edges justified?
- Do stored closures prolong borrows or retain large data?

### Failure

- Is `None` distinct from invalid data?
- Which paths fail fast?
- Which accumulate?
- Are source errors retained?
- Are partial effects reported?

### Effects

- Does the core print, read environment, or access time?
- Are required effects hidden in `inspect` or callbacks?
- Can plans become stale?
- Are retries idempotent?

### Laws and costs

- Are laws scoped and counterexamples tested?
- Are size hints and stronger iterator traits truthful?
- Are cost statements measured or labeled as models?
- Would a loop be clearer?

### Public API

- Is laziness valuable to callers?
- Are opaque iterator lifetimes understandable?
- Does a custom combinator earn its vocabulary?
- Can future courses add parallel or async execution without breaking semantics?

### Decision rule

Approve architecture only when a reader can trace all four flows and the abstraction count is proportional to real variation and reuse.

Course 4 ends with handwritten mechanisms because their semantics must be understood before automation.

You should now be able to:

- derive closure capture and callable bounds;
- trace lazy iterator state and ownership;
- design adapter chains from type and cardinality algebra;
- write folds with prefix invariants;
- distinguish fail-fast and accumulated validation;
- implement lawful custom iterators and collections;
- transform recursive and persistent structures;
- isolate effects and review combinator laws;
- build and defend a complete dataflow architecture.

Course 5 may automate repetitive declarations, derive implementations, and generate code. It must not use macros to conceal unclear semantics.

### Suitable future automation

- repetitive enum-to-string mappings with a clear source of truth;
- validated derives that preserve documented laws;
- declarative construction of repeated parser or visitor forms;
- compile-time generation from stable schemas.

### Unsuitable automation

- hiding ownership errors;
- generating opaque iterator pipelines nobody can review;
- replacing a small explicit match with a macro language;
- deriving a trait whose semantic laws are undefined;
- claiming performance because code is generated.

### Exit standard

Before moving on, complete the final written examination, practical transfer, LedgerFlow extension, and oral defense. The course is not complete because every page was read.

### Unseen requirement: explain rejected ledger events by account

Transformation map changes:

1. parsing unchanged;
2. normalization unchanged;
3. duplicate diagnostics already carry account when available;
4. transition reducer must retain account in rejection;
5. report gains a lazy `rejections_for(account)` view;
6. renderer gains deterministic account section;
7. CLI parser gains `rejected <file> <account>`;
8. process tests distinguish no matches, rejected matches, and operational failure.

No new effect belongs in the core. No boxed closure is required. The query can return `impl Iterator<Item = &Diagnostic> + '_`.

### Semantic regression check

The feature must not change accepted event order, balance calculation, fail-fast mode, or summary rendering. Differential tests compare old and new results on prior fixtures.

### Defense

A precomputed rejection index was rejected because correctness and API shape can be proved without it. Course 9 may benchmark if repeated queries justify indexing.

## Use the idea in a complete program

The course capstone is **LedgerFlow**, a deterministic event-analysis pipeline with diagnostics, audit history, queries, and reports. Add an unseen cross-cutting analysis or reporting requirement while preserving deterministic output, audit history, and explicit failure. Defend the revised dataflow end to end. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-10-route-analysis-engine/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 40 when you can:

- answer the module question—“How do closure, iterator, error, reduction, structural-sharing, and effect decisions compose into a readable whole system?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Produce a transformation map that identifies source, shape, ownership, failure, state, and effect boundaries;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [The Rust Book: Closures and Iterators](https://doc.rust-lang.org/book/ch13-00-functional-features.html)
- [Iterator](https://doc.rust-lang.org/std/iter/trait.Iterator.html)

[← Module 39](../../../04-rust-functional-programming/course-book/module-39-combinator-laws-and-cost-models/index.md) · [ninety-module map](../../../COURSE_MAP.md)

## Continue

1. Complete the [Module 40 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 40 — Route Analysis Engine](../../labs/module-10-route-analysis-engine/README.md) from its public contract.
3. Apply the Module 40 increment in the [LedgerFlow engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
