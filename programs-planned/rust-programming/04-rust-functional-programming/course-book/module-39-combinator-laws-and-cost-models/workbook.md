# Workbook — Module 39: Combinator Laws and Cost Models

[Return to the chapter](index.md) · [Open the LedgerFlow engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether you can use **Combinator Laws and Cost Models** without relying on surface syntax. Keep the module question in view: *What semantic laws should a combinator preserve, and what can honestly be claimed about evaluation and cost?* For every task, identify the program point where the decisive type, ownership, dispatch, failure, or cost relationship is established. Compile only after committing to a prediction, and preserve the smallest counterexample that changes your model.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Combinator Laws and Cost Models** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`case-01.rs`](../../compiler-labs/module-09/case-01.rs) | Pass or fail? What exact rule decides? |
| 2 | [`case-02.rs`](../../compiler-labs/module-09/case-02.rs) | Pass or fail? What exact rule decides? |
| 3 | [`case-03.rs`](../../compiler-labs/module-09/case-03.rs) | Pass or fail? What exact rule decides? |
| 4 | [`case-04.rs`](../../compiler-labs/module-09/case-04.rs) | Pass or fail? What exact rule decides? |
| 5 | [`case-05.rs`](../../compiler-labs/module-09/case-05.rs) | Pass or fail? What exact rule decides? |
| 6 | [`case-06.rs`](../../compiler-labs/module-09/case-06.rs) | Pass or fail? What exact rule decides? |
| 7 | [`case-07.rs`](../../compiler-labs/module-09/case-07.rs) | Pass or fail? What exact rule decides? |
| 8 | [`case-08.rs`](../../compiler-labs/module-09/case-08.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 04-rust-functional-programming
```

## Part 2 — Diagnose and repair

The library advertises “composable zero-cost validators.” Internally it boxes every closure, collects after every stage, converts every error to `String`, and claims validator composition is associative.

One validator increments a counter, another writes an audit record, and a third can panic. Re-grouping them changes call order, effect count, and which failure is observed.

### Repair the API

- keep generic callable types when a pipeline carries one concrete type;
- use dynamic dispatch only for a runtime heterogeneous registry;
- preserve typed errors and source context;
- materialize only where sorting, replay, or ownership requires it;
- split pure predicates from effectful validation commands;
- publish laws only with explicit preconditions and counterexamples.

### Cost dossier

For one repaired combinator, record traversals, allocations, closure captures, short-circuit behavior, and dispatch. Label these as qualitative model claims. Defer measured latency or throughput to Course 9 with a benchmark protocol.

### Counterexample test

Create stateful predicates whose call logs differ under two supposedly equivalent compositions. The test should fail the overbroad law and then pass once the law is restricted to pure predicates and value observation.

### Abstraction restraint

Delete at least one combinator whose local use is clearer as an ordinary `if` or loop. A smaller law-bearing API is stronger than a catalog of wrappers around standard adapters.

## Part 3 — Focused exercises

### Exercise 1 — State a law honestly

Propose an idempotence law for whitespace normalization. Define domain, observation, and counterexamples that would break the law.

### Exercise 2 — Compose predicates with effects

Compare `filter(p).filter(q)` with `filter(|x| p(x) && q(x))` when `p` and `q` increment counters or may fail.

### Exercise 3 — Design lazy and eager names

A search API can return borrowed matches lazily or cloned matches in an owned vector. Design both signatures and explain the tradeoff.

### Exercise 4 — Preserve context through composition

Design a combinator that attaches stage context to `Result<T,E>` without converting `E` to text.

### Exercise 5 — Write a cost ledger

Compare three ways to normalize and filter records: one lazy chain, collect after normalization then filter, and clone into a boxed iterator pipeline. Record traversals, allocations, clones, storage, and lifetime consequences.

### Exercise 6 — De-combinatorize

A function returns a deeply nested `impl Iterator<Item=Result<...>>` with six closure layers, mutable diagnostic capture, and branch-specific boxing. Refactor toward readable stage contracts.



## Part 4 — Independent laboratory

The executable package is `labs/module-09-combinator-contracts/README.md`. The objective is not to create a large helper library. It is to admit only combinators with stable semantics, bounded claims, and a real reuse case.

### Combinator dossiers

For each of `both`, `either`, `negate`, `compose`, and `on_field`, prepare a dossier containing:

- the public callable bound;
- call order and short-circuit behavior;
- captured state;
- output and error type;
- one law candidate;
- the law’s preconditions;
- one counterexample outside those preconditions;
- qualitative allocation, cloning, and dispatch costs.

A signature without the dossier is not complete work.

### Predicate order

`both(p, q)` must call `q` only when `p` returns true. `either(p, q)` must call `q` only when `p` returns false. Instrument both predicates. Equal Boolean outputs are insufficient because reordered side effects can violate the contract.

Use `FnMut`, not `Fn`, because the combinators are intentionally capable of composing stateful callables. That choice also narrows which algebraic laws are valid.

### Composition and context

`compose(first, second)` passes the output of the first function into the second and preserves their invocation order. `on_field` maps only the error channel and retains the concrete source error in `FieldError<E>`. Stringification belongs at a reporting boundary, not in the reusable adapter.

### Law experiment

Normalization collapses whitespace and lowercases text. Test idempotence over a bounded exhaustive sample:

```text
normalize(normalize(x)) == normalize(x)
```

State why this is a claim about the published normalizer, not about arbitrary text transforms.

For pure total predicates, evaluate a candidate equivalence between `both(p, q)` and successive filters. Then construct a stateful `q` whose call ledger demonstrates the missing purity/observational-equivalence precondition.

### Lazy and eager surfaces

Keep `matching` as a borrowed lazy iterator and `collect_matching` as an explicitly allocating, cloning convenience. Their names and return types must not hide ownership policy.

### Rejection threshold

Do not add a combinator merely because it can be written generically. Reject:

- boxed callables where one concrete type flows;
- a global `Pipe` extension trait used once;
- string-only error wrappers;
- laws stated without a domain;
- “zero-cost” claims without measurement;
- combinators that obscure required effects or evaluation order.

Submit all dossiers, call-order tests, the bounded law test, the stateful counterexample, and the lazy/eager ownership comparison. Defend one combinator you kept and one you deliberately removed. Explain what future evidence would be required before promoting this small module into a stable public library.

The executable starter and reference implementation are in [module-09-combinator-contracts](../../labs/module-09-combinator-contracts/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

## Part 5 — Capstone transfer

Day 9 extracts reusable LedgerFlow operations only after their semantics have stabilized. A short function is not automatically a useful combinator. Each published operation must improve the domain vocabulary and carry an explicit contract for order, ownership, failure, materialization, and cost.

### Select three candidates

Choose three operations from different categories:

- a predicate combinator for queries;
- a transformation or normalization combinator;
- a reducer/report combinator.

For each candidate, write a dossier:

| Question | Answer |
|---|---|
| Domain meaning | |
| Input/output types | |
| Borrowed or owned | |
| Lazy or eager | |
| Order behavior | |
| Failure behavior | |
| Law with preconditions | |
| Counterexample boundary | |
| Allocation/clone/traversal cost | |

Do not publish a combinator whose only description is its implementation.

### State laws precisely

Possible laws include identity, associativity, idempotence, or distributivity, but only under stated observation and preconditions. For example, predicate conjunction may be truth-functionally associative for pure predicates, while evaluation count and side effects make differently grouped stateful predicates observably different.

Every claimed law needs:

1. a quantified domain statement;
2. preconditions such as purity, totality, or normalized input;
3. the observation under which values are considered equal;
4. property-style tests over representative cases;
5. at least one counterexample outside the preconditions.

Do not write algebraic slogans without the boundary that makes them true.

### Distinguish lazy and eager APIs

When both are valuable, use names and return types that make the boundary visible. A borrowed lazy account query may return `impl Iterator<Item = &Event> + '_`; a sorted report must materialize because sorting requires ownership of an orderable collection or index.

Do not hide a `collect` inside a function named like a view. Do not expose a lazy iterator when the operation must retain a temporary owner that would be dropped on return.

### Cost ledger

For each combinator, record qualitative costs:

- traversals of the source;
- allocation points;
- payload clones;
- closure captures and their sizes conceptually;
- dynamic dispatch, if any;
- short-circuit behavior;
- materialization boundaries.

This is not benchmark evidence. Avoid “zero cost,” “faster,” or “optimized” unless a later measurement course supplies data and methodology.

### Error preservation

Combinators that operate on fallible stages must preserve structured error types and useful context. Reject designs that convert every error to `String`, drop diagnostics with `filter_map`, or make partial success indistinguishable from complete success.

## Part 6 — Reconstruct and defend

Do not advance because the calendar day ended. Advance when all hard evidence is present.

### Advancement decision

Advance only when every claimed law has explicit preconditions, a counterexample is known for one tempting false law, and each cost statement names its operation and data shape.

### Closed-book retrieval

1. What makes a domain combinator more than a short helper?
2. What preconditions support predicate-composition laws?
3. How can side effects invalidate an algebraic-looking rewrite?
4. Why does law testing not prove an infinite domain?
5. What does a cost model state without benchmarks?
6. When should an API return `impl Iterator`?
7. When is an owned `Vec` the better public result?
8. How can error context be preserved through composition?
9. Why do two closure expressions resist one return-position `impl Fn`?
10. What symptoms indicate over-combinatorization?

### Reconstruction task

Implement predicate conjunction and result-preserving mapping, state their laws, and write a counterexample showing how hidden effects invalidate a rewrite.

### Transfer task

Create reusable query combinators for a document search domain, including one fallible combinator and one ordering-sensitive operation. Produce:

- law stated for all valid inputs;
- smallest counterexample for one false law;
- cost claim tied to a named operation and data shape;
- test showing that a superficially equivalent combinator changes order, duplication, or failure;

### Spaced review

Repeat questions 2, 4, 7, and 10 after 24 hours. Repeat the reconstruction after seven days with a different domain.
