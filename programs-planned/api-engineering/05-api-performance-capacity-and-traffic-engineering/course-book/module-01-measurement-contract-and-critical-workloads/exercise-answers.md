# Worked Answers — Module 01: Measurement Contract and Critical Workloads

Use these solutions to audit your reasoning for **Measurement Contract and Critical Workloads**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Write a measurement requirement for idempotent run submission.

A complete requirement names `WL-RUN-SUBMIT`, an arrival model and rate, environment and dataset, the idempotency correctness oracle, latency or admission bounds, and resource limits. Example: under an open 40 submissions/s schedule in `ENV-4CPU`, 100% of duplicate keys must map to one logical run; at least 99.5% of eligible unique submissions must be admitted or receive the documented overload response; p95 admitted-response latency must be at most 220 ms. The exact numbers are policy, but the structure is non-negotiable.

The chapter’s decisive distinction is this: Each workload names a decisive correctness oracle. For WL-RUN-SUBMIT, the oracle checks that repeated idempotency keys create one logical run and replay the stored public outcome. For WL-ARTIFACT-DOWNLOAD, it checks exact bytes, checksum, authorization, range semantics, and validators.

## 2. A closed test has 100 users, 250 ms average response time, and no think time. What approximate throughput can it generate?

At steady state, each user completes about `1 / 0.25 = 4` requests/s, so 100 users can generate roughly 400 requests/s. This is an upper approximation; client overhead and variability reduce it. If response time rises to 500 ms, the same closed population generates roughly 200 requests/s, demonstrating self-throttling.

In the cumulative capstone, the rule becomes concrete: In a closed model , a fixed population waits for completion or think time before sending the next request. When the service slows, the generated arrival rate falls. Closed models are appropriate for bounded interactive users or worker pools, but they can conceal overload if used for externally driven traffic.

## 3. Why is a p99 from 50 observations weak evidence?

Nearest-rank p99 selects rank `ceil(0.99 × 50) = 50`, the maximum observation. One sample determines the result, and repeated runs can vary greatly. The report should retain the sample count, avoid overinterpreting p99, and use a larger population or a longer window.

A useful way to reason about the boundary is: The denominator for latency quantiles also matters. If timed-out requests disappear from the sample, latency looks better as the service fails. The benchmark envelope stores outcome counts next to latency samples and treats missing terminal observations as failures.

## 4. Classify offered=1000, started=980, completed=950, rejected=20, failed=10, missing=20.

The counts need precise definitions. If rejected and failed are among completed outcomes, then completed categories must reconcile to 950 and 30 scheduled starts remain unresolved: 20 were never started and 10 started but did not terminate, or another allocation. The answer cannot be accepted without a conservation equation. The harness should explicitly define whether rejected is a terminal completed result.

The implementation consequence is: A mixed model is often correct. The capstone models run submissions with an open arrival stream while each virtual client has bounded outstanding idempotent retries. The workload file records the model explicitly; a tool’s default is not accepted as design.

## 5. Which fields belong in a workload hash?

Arrival model, rate or user count, duration, request mix, payload/data distribution, dataset ID, think time, retry behavior, correctness policy, and relevant headers belong. A human description or report note can be excluded. Changing any semantic field requires a new hash even if the display ID is unchanged.

The important nuance is: A workload identity is a stable ID plus a canonical hash of semantic fields. Comments and display labels may be excluded; arrival rate, request mix, payload distribution, duration, and correctness policy are included.

## 6. Can two runs on different CPUs ever be compared?

They cannot support a direct code-regression claim without controlling the CPU difference. They may support a capacity comparison if the CPU configuration is the intended variable and all other relevant fields are controlled. The report must label the comparison accordingly rather than calling it a code improvement.

Under concurrency or failure, the distinction becomes: Fingerprinting does not make unlike environments comparable. It makes the difference visible. The comparison engine rejects mismatched workload hashes and labels environment mismatches as non-comparable unless the report explicitly declares a controlled dimension.

## 7. Why must errors remain outside the latency quantile but inside the decision?

A latency value may be undefined for a rejected request or known only at a timeout bound. Mixing unlike durations can obscure meaning. However, excluding errors from the decision would reward failure. Store latency for its defined population and evaluate error, rejection, timeout, and missing-outcome budgets alongside it.

The design remains honest only if: Repeat the baseline. If two runs in the same controlled environment differ beyond a predeclared noise band, do not optimize yet. First investigate environment noise, data-state drift, thermal throttling, background work, or benchmark errors.

## 8. Derive one critical workload from the artifact retrieval journey.

Use `WL-ARTIFACT-DOWNLOAD` with authorized principals, a declared object-size distribution, conditional and range request mix, open arrival schedule for independent downloads, storage state, checksum/byte/range authorization oracle, and measurements for first-byte latency, completion latency, bytes sent, memory, and storage reads.

The consumer-facing consequence is: A journey is a user outcome across stages. A workload is an executable demand model for that journey. Derive workloads from the Course 4 journey catalogue, then specify request mix, data distribution, arrival process, think time, concurrency, duration, and correctness checks.

## 9. What makes a baseline accepted rather than merely recorded?

Its predecessor integrity and correctness pass; workload and environment identities are complete; warmup and measurement windows are declared; outcome counts reconcile; repeated runs are stable enough for the intended threshold; and the evidence class matches the claim.

The operational consequence is: A baseline is not the first number produced. It is an accepted, reproducible envelope whose workload and environment are suitable for the intended comparison. Store raw samples when practical, summary algorithm names, warmup and measurement windows, start time, source revision, and all outcome counts.

## 10. A candidate drops tracing and gains 8% throughput. Is it valid?

Not automatically. Course 4 requires a reliability telemetry profile. If the candidate changes required signal populations or sampling, it changes the inherited reliability profile. The change must be separately versioned and justified; otherwise the candidate is rejected before performance comparison.

The strongest engineering interpretation is: Performance is not the smallest observed response time. It is behavior under demand while other requirements remain true. For this course, a candidate must preserve the API contract, authorization, durable effects, idempotent replay, error classification, and reliability populations.

## 11. Why store source revision and build flags?

The same source can produce different machine code or runtime behavior under different optimization flags, dependency locks, or feature flags. Without build identity, another engineer cannot reproduce the binary or isolate the cause.

The defect-oriented view is: The environment fingerprint includes runtime versions, CPU and memory limits, process count, worker count, database settings, data scale, source revision, and relevant feature flags. Hostnames and secret values are excluded or pseudonymized.

**Evidence.** Use a correctness-gated baseline/candidate comparison that attributes CPU, wall time, allocations, event-loop delay, and downstream work to one hypothesis.

## 12. Give one claim a local dependency-light benchmark can support and one it cannot.

It can support: candidate X is slower than baseline Y for the same deterministic workload on this machine, or a queue policy bounds admitted concurrency in the model. It cannot support: the production deployment can handle 5,000 requests/s with its actual database, network, and data distribution.

Across the Python and TypeScript tracks, the invariant is: A benchmark harness must execute the oracle during or immediately after the run. “The endpoint returned 2xx” is insufficient. Database and artifact state may be authoritative; telemetry remains evidence, not business truth.
