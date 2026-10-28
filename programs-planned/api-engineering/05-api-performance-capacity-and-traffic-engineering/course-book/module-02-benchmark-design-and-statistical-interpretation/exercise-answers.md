# Worked Answers — Module 02: Benchmark Design and Statistical Interpretation

Use these solutions to audit your reasoning for **Benchmark Design and Statistical Interpretation**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. For samples [2, 4, 4, 8, 20], calculate nearest-rank p50 and p90.

After sorting, `n=5`. p50 rank is `ceil(0.5×5)=3`, value 4. p90 rank is `ceil(0.9×5)=5`, value 20. Record `nearest-rank`; an interpolating method may differ.

The chapter’s decisive distinction is this: Given the same samples and algorithm, both tracks produce the same count, minimum, maximum, mean within a defined tolerance, and nearest-rank quantiles. Shared vectors include ties, tiny samples, large values, and invalid input.

## 2. An open schedule targets 200 requests/s for 30 seconds but starts 5,700 attempts. What must the report say?

Offered work is 6,000. Three hundred scheduled arrivals were not started or were dropped/delayed beyond the run. The report must expose 95% schedule coverage, count the 300 outcomes, inspect client saturation, and not call 5,700 requests the offered load.

In the cumulative capstone, the rule becomes concrete: Coordinated omission occurs when a generator waits through a slow period and therefore fails to record requests that should have arrived during that period. A closed loop naturally records one long request, while an open schedule would have offered several requests and observed queueing or rejection.

## 3. A closed workload has 40 users, 300 ms response time, and 200 ms think time. Estimate throughput.

Cycle time is approximately 0.5 s, so each user generates 2 requests/s. Forty users generate about 80 requests/s, subject to client overhead and distribution effects.

A useful way to reason about the boundary is: A statistically detectable change may be operationally irrelevant. A 0.5 ms improvement on a 200 ms budget may not justify complexity. Conversely, a 5% p99 regression near an SLO boundary may be important even with limited statistical power.

## 4. Why randomize or alternate baseline and candidate run order?

Temperature, background load, cache state, and time-dependent drift can correlate with order. Alternating or randomized order reduces the risk that the later build inherits a systematically warmer or quieter environment.

The implementation consequence is: Plot or inspect rolling throughput, latency, CPU, memory, pool use, and cache state. Define warmup completion by a stated condition or a fixed policy justified by evidence. Then separate warmup data from the measurement window rather than deleting it.

## 5. When is a cold-start workload valid?

When startup or first-request behavior is user-visible and operationally important. It should be a separate named workload with its own setup and reset, not mixed opportunistically into steady-state measurements.

The important nuance is: Early measurements may include process startup, connection establishment, JIT or adaptive runtime effects, filesystem cache population, database buffer warming, and lazy imports. Blindly discarding the first minute is no better than blindly retaining it.

**Evidence.** Use a correctness-gated baseline/candidate comparison that attributes CPU, wall time, allocations, event-loop delay, and downstream work to one hypothesis.

## 6. Explain why merging request samples from five runs can overstate confidence.

Requests within a run share environment state and are correlated. Treating all as independent ignores run-level variation. Preserve run summaries and use independent runs as the unit for reproducibility inference.

Under concurrency or failure, the distinction becomes: A latency distribution within one run describes requests under that run’s conditions. Variation across independent runs describes reproducibility and environmental noise. Do not merge ten runs into one giant sample and pretend they were one continuous population.

## 7. Baseline p95 values are 100, 113, and 96 ms. Candidate values are 98, 95, and 94 ms. Can you claim a regression improvement?

The candidate appears lower, but three runs are sparse and baseline variability is large. Apply the predeclared practical threshold and run-level interval. A cautious conclusion may be promising but insufficient, especially if environment noise is uncontrolled.

The design remains honest only if: For a release comparison, compute each run’s summary, then compare run summaries. A deterministic bootstrap over independent run-level p95 or throughput values can provide an interval for the difference, but it does not rescue a biased workload or correlated runs.

## 8. What does coordinated omission do to a latency histogram?

It underrepresents requests that would have arrived during slow service. Instead of recording their queueing delay or rejection, the generator waits and produces fewer samples, making the tail and offered-load behavior look better.

The consumer-facing consequence is: Coordinated omission occurs when a generator waits through a slow period and therefore fails to record requests that should have arrived during that period. A closed loop naturally records one long request, while an open schedule would have offered several requests and observed queueing or rejection.

## 9. Why record both server and client latency?

Client latency includes network, connection, and client queue delay; server latency focuses on admitted request processing. Their difference can reveal client saturation or network cost. Neither alone explains the full journey.

The operational consequence is: The client can saturate before the server. DNS, connection creation, TLS, serialization, logging, and result storage can consume time and CPU. A trustworthy report records client-side resource use and checks whether scheduled work was actually started.

## 10. Which clock is appropriate for duration and why?

A monotonic high-resolution clock because it cannot move backward due to wall-clock synchronization. Wall-clock timestamps remain useful for correlation, not elapsed duration.

The strongest engineering interpretation is: Each stage has its own timestamp. The harness should use a monotonic clock for durations and wall-clock time only for correlation. It must not generate request identifiers or payloads inside the timed region unless that cost is intentionally part of the workload.

**Evidence.** Use a correctness-gated baseline/candidate comparison that attributes CPU, wall time, allocations, event-loop delay, and downstream work to one hypothesis.

## 11. A candidate improves throughput by 20% but increases CPU per request by 35%. What is the decision?

It depends on the predeclared resource budget and capacity objective. If throughput comes from consuming proportionally more CPU, it may reduce headroom or cost efficiency. The report must compare service demand, not accept throughput alone.

The defect-oriented view is: A summarized report should be derivable from retained events or histograms. Store tool version, command, scenario, random seed, environment, time windows, and dropped work. If raw request data contains sensitive identifiers, pseudonymize or aggregate it before retention.

## 12. Design a falsifiable claim for a serialization optimization.

Example: under `WL-RUN-LIST` with identical workload/environment, the candidate reduces median serialization CPU time by at least 15% and response bytes are unchanged, while full response conformance, p95 end-to-end latency, and memory peak do not regress beyond declared thresholds. Profiling and envelope comparison can disprove it.

Across the Python and TypeScript tracks, the invariant is: A benchmark that cannot be rerun is a demonstration, not a regression gate. The capstone harness emits a stable envelope format independent of k6, Locust, Python, or Node. Tool adapters map their output into that format.
