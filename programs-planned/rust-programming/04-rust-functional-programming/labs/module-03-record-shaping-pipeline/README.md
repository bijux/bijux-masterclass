# Laboratory 33 — Record-Shaping Pipeline

This is the independent product for **Course 4, Module 33: Iterator Algebra and Pipeline Shape**. Read the [module chapter](../../course-book/module-33-iterator-algebra-and-pipeline-shape/index.md) and complete its [workbook](../../course-book/module-33-iterator-algebra-and-pipeline-shape/workbook.md) before consulting the reference implementation.

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

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/`, add the first adversarial test before the design-changing repair, and complete the workbook’s transfer problem before reading the reference implementation.

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

> How do adapters change item type, cardinality, order, ownership, and stopping behavior across a pipeline?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Record-Shaping Pipeline**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
