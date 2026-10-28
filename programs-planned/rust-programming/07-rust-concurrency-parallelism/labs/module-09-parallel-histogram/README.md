# Laboratory 69 — Parallel Histogram

This is the independent product for **Course 7, Module 69**. Read the [module chapter](../../course-book/module-69-rayon-work-stealing-and-deterministic-parallelism/index.md) and complete its [workbook](../../course-book/module-69-rayon-work-stealing-and-deterministic-parallelism/workbook.md) before consulting the reference implementation.

## Learning target

> How do local accumulation, reduction laws, indexed identity, deterministic rendering, and a cost hypothesis turn Rayon scheduling into predictable product meaning?

By the end, the answer must be visible in the public API, protocol diagram, failure behavior, causal tests, and explanation—not merely in a successful run.

## Product

Build sequential and Rayon histograms over labels. A caller-owned custom pool controls parallel resources. Parallel tasks accumulate locally and reduce into a deterministic ordered map.

## Why this laboratory exists

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

> How do local accumulation, reduction laws, indexed identity, deterministic rendering, and a cost hypothesis turn Rayon scheduling into predictable product meaning?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```
