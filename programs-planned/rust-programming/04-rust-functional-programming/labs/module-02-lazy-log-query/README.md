# Laboratory 32 — Lazy Log Query

**Course 4 · Module 32: The Iterator Model**

[Chapter](../../course-book/module-32-the-iterator-model/index.md) · [Workbook](../../course-book/module-32-the-iterator-model/workbook.md) · [LedgerFlow guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **The Iterator Model**: What state does an iterator own, when does work happen, and what is consumed by each call to next? The product must make **Explain the distinct roles of `IntoIterator`, `Iterator`, adapters, and consumers** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **iterator state trace** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

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

1. Read the product contract and run the starter’s baseline checks for **Lazy Log Query**.
2. Draw the smallest **iterator state trace** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to LedgerFlow so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 32 — Lazy Log Query**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Lazy Log Query**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Explain the distinct roles of `IntoIterator`, `Iterator`, adapters, and consumers.
- Trace the state changes caused by repeated calls to `next`.
- Predict whether an iteration path borrows, mutably borrows, or consumes its source.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 32 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **iterator state trace**. Defend why your design is simpler than one plausible alternative under the new requirements.
