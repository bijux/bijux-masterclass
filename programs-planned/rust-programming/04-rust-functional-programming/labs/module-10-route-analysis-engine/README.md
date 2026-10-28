# Laboratory 40 — Route Analysis Engine

**Course 4 · Module 40: Functional Architecture Synthesis**

[Chapter](../../course-book/module-40-functional-architecture-synthesis/index.md) · [Workbook](../../course-book/module-40-functional-architecture-synthesis/workbook.md) · [LedgerFlow guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Functional Architecture Synthesis**: How do closure, iterator, error, reduction, structural-sharing, and effect decisions compose into a readable whole system? The product must make **Produce a transformation map that identifies source, shape, ownership, failure, state, and effect boundaries** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **whole-pipeline architecture map** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> How do closure, iterator, error, reduction, structural-sharing, and effect decisions compose into a readable whole system?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

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

### Independent transfer

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

## Working route

1. Read the product contract and run the starter’s baseline checks for **Route Analysis Engine**.
2. Draw the smallest **whole-pipeline architecture map** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to LedgerFlow so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 40 — Route Analysis Engine**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Route Analysis Engine**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Produce a transformation map that identifies source, shape, ownership, failure, state, and effect boundaries.
- Integrate closures, iterators, folds, error traversal, custom protocols, and effect isolation coherently.
- Refactor between loops and combinators without changing observable behavior.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Transfer defense

Rebuild the decisive relationship from Module 40 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **whole-pipeline architecture map**. Defend why your design is simpler than one plausible alternative under the new requirements.
