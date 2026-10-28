# Reference Answers — Module 06: Metrics and Service-Level Indicators

Read after attempting all twelve Metrics and Service-Level Indicators exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. When should a counter be used?

**Answer.** For monotonically accumulating events such as requests, failures, retries, and dropped telemetry. Export/query logic handles process resets.

## 2. When should a gauge be used?

**Answer.** For current state such as queue depth, permits in use, or lifecycle state, with explicit collection and aggregation ownership.

## 3. Why use histograms for latency?

**Answer.** They preserve a distribution and allow threshold proportions and approximate quantiles; an average cannot expose the tail.

## 4. May operation ID be a metric label?

**Answer.** Yes when the operation set is fixed and reviewed. Raw paths or resource identifiers are not bounded.

## 5. Why is run ID forbidden as a label?

**Answer.** It grows with every run, creates unbounded series, increases cost, and may leak sensitive identifiers.

## 6. How should 401 responses affect availability?

**Answer.** Correct rejection of invalid credentials is normally excluded; rejection of valid credentials due to service regression is bad and requires classified valid-credential test traffic.

**Common mistake.** Describing a procedure for “How should 401 responses affect availability?” without a falsifiable completion condition.

## 7. What is the SLI for run-start freshness?

**Answer.** The proportion of durably accepted eligible runs with a first running event within the threshold, measured from durable acceptance time.

## 8. Why can a queue-depth gauge be misleading?

**Answer.** A small backlog may still contain very old work; combine depth with oldest-age or freshness indicators.

## 9. What does a counter reset mean?

**Answer.** Usually process lifecycle, not negative work. Rate queries must detect resets and aggregate per-series increments.

## 10. Why version recording rules?

**Answer.** They encode indicator semantics used by dashboards and alerts; silent changes invalidate historical comparisons.

## 11. Trace metrics and SLI populations in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_reliability/metrics.py` and `capstone/tracks/typescript-fastify/src/reliability/metrics.ts`. The required invariant is that instrument type, labels, eligibility, good/bad classification, and reset handling are explicit and bounded.

## 12. Compare metrics and SLI populations across Python and TypeScript

Both tracks must preserve this invariant: instrument type, labels, eligibility, good/bad classification, and reset handling are explicit and bounded. The intentional difference is that metric libraries differ; descriptors and resulting counts/histograms must match shared vectors.
