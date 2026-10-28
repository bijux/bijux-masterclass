# Exercises — Module 08: Traffic Shaping, Quotas, and Load Shedding

Work through all twelve problems before opening the answers. In **Traffic Shaping, Quotas, and Load Shedding**, every response must settle this question: **How should quotas, priorities, cost budgets, and load shedding preserve fairness and truthful 429/503 outcomes?** Use the cumulative platform, not an invented toy system. Preserve inherited guarantees and make every new assumption explicit and falsifiable.

## 1. A bucket capacity is 100 tokens, refill 20/s, current 10, cost 50. How long until admission?


## 2. Why use integer microtokens?


## 3. How do rate and concurrency limits differ for long downloads?


## 4. Design a cost for uploads.


## 5. What is an atomic multi-budget decision?


## 6. When is 429 appropriate?


## 7. Why reserve capacity for cancellation/status?


## 8. Three instances each enforce 100 requests/s locally. What is the possible aggregate?


## 9. How can borrowing improve fairness and utilization?


## 10. What must a shedding ladder never do?


## 11. How should limiter keys be bounded?


## 12. Design a mixed-tenant traffic experiment.


## Submission format

Submit Module 08 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
