# Laboratory 69 — Parallel Histogram

**Course 7 · Module 69: Rayon, Work Stealing, and Deterministic Parallelism**

[Chapter](../../course-book/module-69-rayon-work-stealing-and-deterministic-parallelism/index.md) · [Workbook](../../course-book/module-69-rayon-work-stealing-and-deterministic-parallelism/workbook.md) · [BatchWeave guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Rayon, Work Stealing, and Deterministic Parallelism**: How can divisible computation use a work-stealing pool while preserving item meaning, reduction laws, failure policy, result ordering, and a defensible cost model? The product must make **Distinguish task parallelism, data parallelism, and a long-lived message-driven worker service** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **work-partition and reduction map** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

> How do local accumulation, reduction laws, indexed identity, deterministic rendering, and a cost hypothesis turn Rayon scheduling into predictable product meaning?

By the end, the answer must be visible in the public API, protocol diagram, failure behavior, causal tests, and explanation—not merely in a successful run.

## Product

Build sequential and Rayon histograms over labels. A caller-owned custom pool controls parallel resources. Parallel tasks accumulate locally and reduce into a deterministic ordered map.

## Product-specific design pressure

The lab removes I/O and worker lifecycle so the reader can focus on algebra and scheduler-independent meaning. The sequential implementation is the executable oracle.

## Contract

Reject zero pool threads and pool widths above an explicit product limit. Use exactly pinned Rayon 1.12.0. Preserve counts across one, two, and several threads. No global mutex may appear in the per-item path. Count addition must be bounded against input length. A sequential cutoff is documented as a hypothesis, not a benchmark conclusion.

## Required milestones

1. Write identity and associativity laws.
2. Implement sequential oracle.
3. Build reusable custom pool.
4. Implement local fold/reduce.
5. Compare outputs across thread counts and sizes.

## Adversarial cases

- empty labels
- one label
- all unique
- all identical
- large skewed set
- one/two/many threads
- thread count above the product limit
- input near count bound
- cutoff boundary

## Evidence to produce

- reduction-law proof
- oracle equality matrix
- no hot-loop shared lock
- deterministic rendering
- cost hypothesis

## Prohibited shortcuts

- one global mutex map
- floating-point or subtraction reduction without law
- side-effect logging in closures
- new pool per call
- claiming speed without measurement

## Transfer

Transfer the design to source-code statistics with indexed diagnostics. Select the lowest-index error deterministically after parallel validation.

## Comparing with the reference

Compare the algebra and oracle before implementation style. The reference should be correct at every pool width and should keep rendering and external effects outside the parallel closure.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/` and do not open `solution/` until the protocol, adversarial cases, and transfer are implemented or a precise blocker is written.

The laboratory is complete when the tests and documented failure paths pass, and you can answer the governing question without the chapter:

For **Laboratory 69 — Parallel Histogram**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Design record

Before implementation, complete this record for **Parallel Histogram**:

| Question | Required answer |
|---|---|
| Module decision | How does **Rayon, Work Stealing, and Deterministic Parallelism** answer its governing question in this product? |
| Authority | Which type or component decides the main rule? |
| Valid states | Which states may be observed through the public API? |
| Rejection | What exact input or transition is refused, and what remains unchanged? |
| Ownership | Who owns every resource before, during, and after the decisive operation? |
| Order and bounds | Which sequence, capacity, lifetime, or compatibility limit is promised? |
| Evidence | Which test, compiler case, model, trace, or review could falsify the claim? |

Use the **work-partition and reduction map** to answer the table. Then add at least three adversarial cases: one at the smallest boundary, one at the largest accepted or rejected boundary, and one that leaves partial work before failure. For each, state the final observable state before running the test.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Parallel Histogram**.
2. Draw the smallest **work-partition and reduction map** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to BatchWeave so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Distinguish task parallelism, data parallelism, and a long-lived message-driven worker service.
- Explain work stealing without relying on worker identity or execution order.
- Derive closure `Send` and captured-state `Sync` requirements from parallel execution.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 69 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **work-partition and reduction map**. Defend why your design is simpler than one plausible alternative under the new requirements.
