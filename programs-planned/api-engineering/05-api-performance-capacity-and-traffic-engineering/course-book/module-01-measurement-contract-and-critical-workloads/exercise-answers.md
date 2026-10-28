# Reference Answers — Module 01: Module 01 exercise answers — Measurement Contract and Critical Workloads

Read after attempting all twelve Measurement Contract and Critical Workloads exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Write a measurement requirement for idempotent run submission.

A complete requirement names `WL-RUN-SUBMIT`, an arrival model and rate, environment and dataset, the idempotency correctness oracle, latency or admission bounds, and resource limits. Example: under an open 40 submissions/s schedule in `ENV-4CPU`, 100% of duplicate keys must map to one logical run; at least 99.5% of eligible unique submissions must be admitted or receive the documented overload response; p95 admitted-response latency must be at most 220 ms. The exact numbers are policy, but the structure is non-negotiable.

## 2. A closed test has 100 users, 250 ms average response time, and no think time. What approximate throughput can it generate?

At steady state, each user completes about `1 / 0.25 = 4` requests/s, so 100 users can generate roughly 400 requests/s. This is an upper approximation; client overhead and variability reduce it. If response time rises to 500 ms, the same closed population generates roughly 200 requests/s, demonstrating self-throttling.

## 3. Why is a p99 from 50 observations weak evidence?

Nearest-rank p99 selects rank `ceil(0.99 × 50) = 50`, the maximum observation. One sample determines the result, and repeated runs can vary greatly. The report should retain the sample count, avoid overinterpreting p99, and use a larger population or a longer window.

## 4. Classify offered=1000, started=980, completed=950, rejected=20, failed=10, missing=20.

The counts need precise definitions. If rejected and failed are among completed outcomes, then completed categories must reconcile to 950 and 30 scheduled starts remain unresolved: 20 were never started and 10 started but did not terminate, or another allocation. The answer cannot be accepted without a conservation equation. The harness should explicitly define whether rejected is a terminal completed result.

## 5. Which fields belong in a workload hash?

Arrival model, rate or user count, duration, request mix, payload/data distribution, dataset ID, think time, retry behavior, correctness policy, and relevant headers belong. A human description or report note can be excluded. Changing any semantic field requires a new hash even if the display ID is unchanged.

## 6. Can two runs on different CPUs ever be compared?

They cannot support a direct code-regression claim without controlling the CPU difference. They may support a capacity comparison if the CPU configuration is the intended variable and all other relevant fields are controlled. The report must label the comparison accordingly rather than calling it a code improvement.

## 7. Why must errors remain outside the latency quantile but inside the decision?

A latency value may be undefined for a rejected request or known only at a timeout bound. Mixing unlike durations can obscure meaning. However, excluding errors from the decision would reward failure. Store latency for its defined population and evaluate error, rejection, timeout, and missing-outcome budgets alongside it.

## 8. Derive one critical workload from the artifact retrieval journey.

Use `WL-ARTIFACT-DOWNLOAD` with authorized principals, a declared object-size distribution, conditional and range request mix, open arrival schedule for independent downloads, storage state, checksum/byte/range authorization oracle, and measurements for first-byte latency, completion latency, bytes sent, memory, and storage reads.

## 9. What makes a baseline accepted rather than merely recorded?

Its predecessor integrity and correctness pass; workload and environment identities are complete; warmup and measurement windows are declared; outcome counts reconcile; repeated runs are stable enough for the intended threshold; and the evidence class matches the claim.

## 10. A candidate drops tracing and gains 8% throughput. Is it valid?

Not automatically. Course 4 requires a reliability telemetry profile. If the candidate changes required signal populations or sampling, it changes the inherited reliability profile. The change must be separately versioned and justified; otherwise the candidate is rejected before performance comparison.

## 11. Why store source revision and build flags?

The same source can produce different machine code or runtime behavior under different optimization flags, dependency locks, or feature flags. Without build identity, another engineer cannot reproduce the binary or isolate the cause.

## 12. Give one claim a local dependency-light benchmark can support and one it cannot.

It can support: candidate X is slower than baseline Y for the same deterministic workload on this machine, or a queue policy bounds admitted concurrency in the model. It cannot support: the production deployment can handle 5,000 requests/s with its actual database, network, and data distribution.
