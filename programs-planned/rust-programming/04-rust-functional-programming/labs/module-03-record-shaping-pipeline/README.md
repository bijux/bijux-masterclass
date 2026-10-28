# Laboratory 33 — Record-Shaping Pipeline

**Course 4 · Module 33: Iterator Algebra and Pipeline Shape**

[Chapter](../../course-book/module-33-iterator-algebra-and-pipeline-shape/index.md) · [Workbook](../../course-book/module-33-iterator-algebra-and-pipeline-shape/workbook.md) · [LedgerFlow guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Iterator Algebra and Pipeline Shape**: How do adapters change item type, cardinality, order, ownership, and stopping behavior across a pipeline? The product must make **Derive the item type and cardinality effect of common iterator adapters** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **pipeline shape table** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> How do adapters change item type, cardinality, order, ownership, and stopping behavior across a pipeline?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

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

## Working route

1. Read the product contract and run the starter’s baseline checks for **Record-Shaping Pipeline**.
2. Draw the smallest **pipeline shape table** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to LedgerFlow so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 33 — Record-Shaping Pipeline**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Record-Shaping Pipeline**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Derive the item type and cardinality effect of common iterator adapters.
- Choose correctly among `filter`, `map`, `filter_map`, `flatten`, and `flat_map`.
- Reason about order and truncation in `chain`, `zip`, `take`, and stopping adapters.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 33 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **pipeline shape table**. Defend why your design is simpler than one plausible alternative under the new requirements.
