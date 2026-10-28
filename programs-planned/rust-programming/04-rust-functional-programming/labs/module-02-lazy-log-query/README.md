# Laboratory 32 — Lazy Log Query

This is the independent product for **Course 4, Module 32: The Iterator Model**. Read the [module chapter](../../course-book/module-32-the-iterator-model/index.md) and complete its [workbook](../../course-book/module-32-the-iterator-model/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> What state does an iterator own, when does work happen, and what is consumed by each call to next?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

The executable contract is in `labs/module-02-lazy-log-query/README.md`. This laboratory is about pull behavior, not just filtering syntax.

### Product problem

An in-memory log needs borrowed read-only queries and two different prefix operations. One prefix operation may consume the boundary item while discovering that it should stop. The other must preserve that boundary for the caller. Those are different contracts and must not share a misleading name.

### Pull trace before code

For the source below, write the exact sequence of `next` and predicate calls for each consumer:

```text
Debug("boot"), Info("ready"), Error("disk"), Error("network")
```

Trace:

- constructing the query and never consuming it;
- `.take(1).collect()` with minimum `Warn` and term `"disk"`;
- `.count()` with minimum `Info` and term `"e"`;
- a `take_while` prefix through marker `STOP`;
- the preserving `Peekable` variant through the same marker.

A result list without the pull trace is incomplete evidence.

### Implementation obligations

#### Borrowed query

Return `impl Iterator<Item = &LogEntry> + '_`. The query must borrow the source, retain source order, and allocate no result collection by itself. Add a test that uses the source again after the query has been consumed.

#### Consuming prefix

Accept `&mut I` where `I: Iterator<Item = &str>`. Document that `take_while` consumes the first rejected item. Prove the contract with `['a', 'STOP', 'b']`: the result is `['a']`, and the remaining iterator begins at `'b'`.

#### Preserving prefix

Accept `&mut Peekable<I>`. Inspect the next item before deciding whether to consume it. The same source must leave `STOP` available as the next item.

#### Laziness proof

Instrument the query predicate with `Cell<usize>`. Assert zero calls after construction, the exact number after `.take(1)`, and no inspection of later entries once the consumer has enough output.

### Failure modes to expose

Reject implementations that:

- accept `Vec<LogEntry>` and consume the catalog;
- return `Vec<&LogEntry>` by default and call that “lazy”;
- allocate lowercase copies of every message before a case-sensitive query;
- use `take_while` while promising boundary preservation;
- hide delimiter consumption in documentation rather than a test;
- claim zero work without measuring predicate calls.

### Transfer task

Add `first_n_matching`, still as a lazy borrowed view. Use a predicate ledger to prove that matching stops after `n` retained entries, not after `n` source entries. Define `n = 0` explicitly and test it.

### Defense

Explain where iterator state lives, why `next` needs `&mut self`, how `by_ref` changes ownership of the iterator value, and why “adapter construction is lazy” does not mean “the eventual query is free.”

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

> What state does an iterator own, when does work happen, and what is consumed by each call to next?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Lazy Log Query**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
