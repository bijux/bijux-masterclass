# Reference Answers — Module 02: Module 02 exercise answers — Benchmark Design and Statistical Interpretation

Read after attempting all twelve Benchmark Design and Statistical Interpretation exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. For samples [2, 4, 4, 8, 20], calculate nearest-rank p50 and p90.

After sorting, `n=5`. p50 rank is `ceil(0.5×5)=3`, value 4. p90 rank is `ceil(0.9×5)=5`, value 20. Record `nearest-rank`; an interpolating method may differ.

## 2. An open schedule targets 200 requests/s for 30 seconds but starts 5,700 attempts. What must the report say?

Offered work is 6,000. Three hundred scheduled arrivals were not started or were dropped/delayed beyond the run. The report must expose 95% schedule coverage, count the 300 outcomes, inspect client saturation, and not call 5,700 requests the offered load.

## 3. A closed workload has 40 users, 300 ms response time, and 200 ms think time. Estimate throughput.

Cycle time is approximately 0.5 s, so each user generates 2 requests/s. Forty users generate about 80 requests/s, subject to client overhead and distribution effects.

## 4. Why randomize or alternate baseline and candidate run order?

Temperature, background load, cache state, and time-dependent drift can correlate with order. Alternating or randomized order reduces the risk that the later build inherits a systematically warmer or quieter environment.

## 5. When is a cold-start workload valid?

When startup or first-request behavior is user-visible and operationally important. It should be a separate named workload with its own setup and reset, not mixed opportunistically into steady-state measurements.

## 6. Explain why merging request samples from five runs can overstate confidence.

Requests within a run share environment state and are correlated. Treating all as independent ignores run-level variation. Preserve run summaries and use independent runs as the unit for reproducibility inference.

## 7. Baseline p95 values are 100, 113, and 96 ms. Candidate values are 98, 95, and 94 ms. Can you claim a regression improvement?

The candidate appears lower, but three runs are sparse and baseline variability is large. Apply the predeclared practical threshold and run-level interval. A cautious conclusion may be promising but insufficient, especially if environment noise is uncontrolled.

## 8. What does coordinated omission do to a latency histogram?

It underrepresents requests that would have arrived during slow service. Instead of recording their queueing delay or rejection, the generator waits and produces fewer samples, making the tail and offered-load behavior look better.

## 9. Why record both server and client latency?

Client latency includes network, connection, and client queue delay; server latency focuses on admitted request processing. Their difference can reveal client saturation or network cost. Neither alone explains the full journey.

## 10. Which clock is appropriate for duration and why?

A monotonic high-resolution clock because it cannot move backward due to wall-clock synchronization. Wall-clock timestamps remain useful for correlation, not elapsed duration.

## 11. A candidate improves throughput by 20% but increases CPU per request by 35%. What is the decision?

It depends on the predeclared resource budget and capacity objective. If throughput comes from consuming proportionally more CPU, it may reduce headroom or cost efficiency. The report must compare service demand, not accept throughput alone.

## 12. Design a falsifiable claim for a serialization optimization.

Example: under `WL-RUN-LIST` with identical workload/environment, the candidate reduces median serialization CPU time by at least 15% and response bytes are unchanged, while full response conformance, p95 end-to-end latency, and memory peak do not regress beyond declared thresholds. Profiling and envelope comparison can disprove it.
