# Exercises — Module 06: Queueing, Concurrency, and Backpressure

Work through all twelve problems before opening the answers. In **Queueing, Concurrency, and Backpressure**, every response must settle this question: **How do arrival rate, service time, queue depth, concurrency, fairness, and backpressure determine overload behavior?** Answer as though another team must implement and operate the design. Ambiguous ownership, unbounded behavior, and evidence-free claims are defects.

## 1. Use Little’s Law for 50 completed requests/s and 0.4 s average response time.


## 2. A queue contains 300 jobs, 20 are active, throughput is 10 jobs/s. Estimate mean time in system if stable.


## 3. For M/M/1 with service rate 100/s and arrival 80/s, approximate response time.


## 4. What happens to the same approximation at arrival 95/s?


## 5. Why is an asyncio semaphore insufficient as a full admission controller?


## 6. Calculate maximum application chunk buffers for 150 download permits, 128 KiB chunks, two buffers each.


## 7. When should a client disconnect cancel work?


## 8. Why can increasing database pool size reduce throughput?


## 9. Design fair admission for tenants A and B.


## 10. How should queue depth affect worker claims?


## 11. Distinguish 429 and 503 in a traffic policy.


## 12. A system has zero rejections but rising queue wait and missed SLO. Is admission healthy?


## Submission format

Submit Module 06 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
