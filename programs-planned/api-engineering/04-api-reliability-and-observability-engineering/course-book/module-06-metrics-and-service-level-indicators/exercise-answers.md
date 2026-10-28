# Worked Answers — Module 06: Metrics and Service-Level Indicators

Use these solutions to audit your reasoning for **Metrics and Service-Level Indicators**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. When should a counter be used?

For monotonically accumulating events such as requests, failures, retries, and dropped telemetry. Export/query logic handles process resets.

The chapter’s decisive distinction is this: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=06 TRACK=python and explain why the same public and durable outcome holds in the other language.

## 2. When should a gauge be used?

For current state such as queue depth, permits in use, or lifecycle state, with explicit collection and aggregation ownership.

In the cumulative capstone, the rule becomes concrete: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=06 TRACK=typescript and explain why the same public and durable outcome holds in the other language.

## 3. Why use histograms for latency?

They preserve a distribution and allow threshold proportions and approximate quantiles; an average cannot expose the tail.

A useful way to reason about the boundary is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=06 TRACK=python and explain why the same public and durable outcome holds in the other language.

## 4. May operation ID be a metric label?

Yes when the operation set is fixed and reviewed. Raw paths or resource identifiers are not bounded.

The implementation consequence is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=06 TRACK=typescript and explain why the same public and durable outcome holds in the other language.

**Evidence.** Recompute good, bad, eligible, excluded, and missing populations from durable outcomes; then validate burn-rate windows, alert linkage, and the user-journey dashboard.

## 5. Why is run ID forbidden as a label?

It grows with every run, creates unbounded series, increases cost, and may leak sensitive identifiers.

The important nuance is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=06 TRACK=python and explain why the same public and durable outcome holds in the other language.

**Evidence.** Run a bounded fault experiment with a declared durable-state oracle, correlated telemetry, abort condition, cleanup, and a planted mutant that the proof rejects.

## 6. How should 401 responses affect availability?

Correct rejection of invalid credentials is normally excluded; rejection of valid credentials due to service regression is bad and requires classified valid-credential test traffic.

**Common mistake.** Describing a procedure for “How should 401 responses affect availability?” without a falsifiable completion condition.

Under concurrency or failure, the distinction becomes: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=06 TRACK=typescript and explain why the same public and durable outcome holds in the other language.

## 7. What is the SLI for run-start freshness?

The proportion of durably accepted eligible runs with a first running event within the threshold, measured from durable acceptance time.

The design remains honest only if: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=06 TRACK=python and explain why the same public and durable outcome holds in the other language.

## 8. Why can a queue-depth gauge be misleading?

A small backlog may still contain very old work; combine depth with oldest-age or freshness indicators.

The consumer-facing consequence is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=06 TRACK=typescript and explain why the same public and durable outcome holds in the other language.

**Evidence.** Run a bounded fault experiment with a declared durable-state oracle, correlated telemetry, abort condition, cleanup, and a planted mutant that the proof rejects.

## 9. What does a counter reset mean?

Usually process lifecycle, not negative work. Rate queries must detect resets and aggregate per-series increments.

The operational consequence is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=06 TRACK=python and explain why the same public and durable outcome holds in the other language.

**Evidence.** Run a bounded fault experiment with a declared durable-state oracle, correlated telemetry, abort condition, cleanup, and a planted mutant that the proof rejects.

## 10. Why version recording rules?

They encode indicator semantics used by dashboards and alerts; silent changes invalidate historical comparisons.

The strongest engineering interpretation is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=06 TRACK=typescript and explain why the same public and durable outcome holds in the other language.

**Evidence.** Run a bounded fault experiment with a declared durable-state oracle, correlated telemetry, abort condition, cleanup, and a planted mutant that the proof rejects.

## 11. Trace metrics and SLI populations in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_reliability/metrics.py` and `capstone/tracks/typescript-fastify/src/reliability/metrics.ts`. The required invariant is that instrument type, labels, eligibility, good/bad classification, and reset handling are explicit and bounded.

The defect-oriented view is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=06 TRACK=python and explain why the same public and durable outcome holds in the other language.

## 12. Compare metrics and SLI populations across Python and TypeScript

Both tracks must preserve this invariant: instrument type, labels, eligibility, good/bad classification, and reset handling are explicit and bounded. The intentional difference is that metric libraries differ; descriptors and resulting counts/histograms must match shared vectors.

Across the Python and TypeScript tracks, the invariant is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=06 TRACK=typescript and explain why the same public and durable outcome holds in the other language.
