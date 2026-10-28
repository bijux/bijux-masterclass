# Exercises — Module 02: Benchmark Design and Statistical Interpretation

Work through all twelve problems before opening the answers. In **Benchmark Design and Statistical Interpretation**, every response must settle this question: **How do open and closed demand, warmup, sample size, missing outcomes, variation, and statistical uncertainty change benchmark meaning?** Treat each problem as a design review: state the rule, construct the smallest counterexample, and select an oracle capable of rejecting your own answer.

## 1. For samples [2, 4, 4, 8, 20], calculate nearest-rank p50 and p90.


## 2. An open schedule targets 200 requests/s for 30 seconds but starts 5,700 attempts. What must the report say?


## 3. A closed workload has 40 users, 300 ms response time, and 200 ms think time. Estimate throughput.


## 4. Why randomize or alternate baseline and candidate run order?


## 5. When is a cold-start workload valid?


## 6. Explain why merging request samples from five runs can overstate confidence.


## 7. Baseline p95 values are 100, 113, and 96 ms. Candidate values are 98, 95, and 94 ms. Can you claim a regression improvement?


## 8. What does coordinated omission do to a latency histogram?


## 9. Why record both server and client latency?


## 10. Which clock is appropriate for duration and why?


## 11. A candidate improves throughput by 20% but increases CPU per request by 35%. What is the decision?


## 12. Design a falsifiable claim for a serialization optimization.


## Submission format

Submit Module 02 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
