# Laboratory 42 — Typed Map Macro

**Course 5 · Module 42: Declarative Macros: Matchers, Fragments, and Repetition**

[Chapter](../../course-book/module-42-declarative-macros-matchers-fragments-and-repetition/index.md) · [Workbook](../../course-book/module-42-declarative-macros-matchers-fragments-and-repetition/workbook.md) · [CommandForge guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Declarative Macros: Matchers, Fragments, and Repetition**: How do you design a `macro_rules!` invocation as a precise grammar while preserving ownership, evaluation order, and expression semantics? The product must make **Read a matcher as a grammar rather than as textual substitution** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **matcher and fragment trace** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> How do you design a `macro_rules!` invocation as a precise grammar while preserving ownership, evaluation order, and expression semantics?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Implement an expression macro that constructs a `BTreeMap` with explicit key and value types:

```rust
typed_map! {
    String => u64;
    make_key("alpha") => read_value(),
    "beta".to_owned() => 2,
}
```

This laboratory is about grammar and semantics, not map convenience. The invocation must have one grammar, expand to one block expression, evaluate each caller expression exactly once in source order, and document duplicate-key behavior.

## Required behavior

- Syntax is `KEY_TYPE => VALUE_TYPE; entries`.
- Entries use `key_expr => value_expr`, comma separation, and an optional trailing comma.
- Empty maps are allowed and retain explicit types.
- Every key and value expression is evaluated once.
- Insertion follows source order.
- Duplicate keys use `BTreeMap::insert` semantics: the last value replaces the earlier value.
- The expansion does not depend on caller imports.

## Adversarial cases

Use counters and a call ledger to detect double evaluation and reordering. Test an empty invocation, a trailing comma, owned `String` keys, expressions with blocks, and a duplicate key. Preserve compile-fail examples for missing type separator and malformed entries in the course compiler laboratory.

## Build sequence

Write the invocation grammar in one line. Choose `ty` and `expr` fragments deliberately. Expand to a block with explicit local bindings. Add behavior tests before reading the reference.

## Transfer

Design a set-building sibling macro. State what grammar and duplicate policy changes, and which implementation logic should remain ordinary Rust rather than being copied into another macro.

## Semantic proof

Test the macro with side-effecting key and value constructors that append labels to a log. The observed order must match source order, and each expression must run exactly once. This proves more than final map equality: it proves that the expansion does not duplicate, reorder, or pre-evaluate caller expressions.

Also test an empty invocation, a trailing comma, a key expression containing a comma inside parentheses, and duplicate keys. Document the duplicate policy explicitly. `BTreeMap::insert` naturally makes the last value win, but the macro must not pretend to reject duplicates when arbitrary key expressions cannot be compared during matching.

Inspect the expansion by hand. It should be a block expression with a private temporary, a sequence of insertions, and the final map value. Any expansion that leaks a fixed local name into caller scope or evaluates an entry twice fails the contract even if the simple tests pass.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Typed Map Macro**.
2. Draw the smallest **matcher and fragment trace** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to CommandForge so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 42 — Typed Map Macro**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Typed Map Macro**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Read a matcher as a grammar rather than as textual substitution.
- Choose fragment specifiers according to the accepted public language.
- Design unambiguous separators, delimiters, optional clauses, and cardinality.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 42 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **matcher and fragment trace**. Defend why your design is simpler than one plausible alternative under the new requirements.
