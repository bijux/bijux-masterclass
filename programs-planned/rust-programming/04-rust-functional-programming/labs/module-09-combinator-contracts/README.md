# Laboratory 39 — Combinator Contracts

This is the independent product for **Course 4, Module 39: Combinator Laws and Cost Models**. Read the [module chapter](../../course-book/module-39-combinator-laws-and-cost-models/index.md) and complete its [workbook](../../course-book/module-39-combinator-laws-and-cost-models/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> What semantic laws should a combinator preserve, and what can honestly be claimed about evaluation and cost?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

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

> What semantic laws should a combinator preserve, and what can honestly be claimed about evaluation and cost?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Combinator Contracts**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
