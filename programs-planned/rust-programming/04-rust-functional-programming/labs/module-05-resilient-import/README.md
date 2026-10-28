# Laboratory 35 — Resilient Import

**Course 4 · Module 35: Option, Result, and Fallible Traversal**

[Chapter](../../course-book/module-35-option-result-and-fallible-traversal/index.md) · [Workbook](../../course-book/module-35-option-result-and-fallible-traversal/workbook.md) · [LedgerFlow guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Option, Result, and Fallible Traversal**: Should a fallible traversal skip, fail fast, recover, accumulate diagnostics, or continue with an explicit default? The product must make **Compose optional and fallible transformations while preserving ownership and error meaning** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **failure-policy matrix** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> Should a fallible traversal skip, fail fast, recover, accumulate diagnostics, or continue with an explicit default?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

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

## Working route

1. Read the product contract and run the starter’s baseline checks for **Resilient Import**.
2. Draw the smallest **failure-policy matrix** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to LedgerFlow so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 35 — Resilient Import**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Resilient Import**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Compose optional and fallible transformations while preserving ownership and error meaning.
- Use `transpose`, `flatten`, and `collect` to change container shape deliberately.
- Distinguish fail-fast traversal from diagnostic accumulation and implement both honestly.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 35 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **failure-policy matrix**. Defend why your design is simpler than one plausible alternative under the new requirements.
