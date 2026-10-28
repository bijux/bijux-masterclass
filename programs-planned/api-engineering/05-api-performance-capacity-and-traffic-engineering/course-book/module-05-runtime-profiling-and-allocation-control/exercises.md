# Exercises — Module 05: Runtime Profiling and Allocation Control

Work through all twelve problems before opening the answers. In **Runtime Profiling and Allocation Control**, every response must settle this question: **Which Python or Node.js runtime phase consumes wall time, CPU, allocations, event-loop capacity, or serialization effort?** A useful solution connects semantics to mechanism: who owns the decision, what can go wrong, and which retained artifact proves the claimed outcome.

## 1. A function has 100 ms wall time and 4 ms CPU time. What is the first hypothesis?


## 2. A function has 80 ms wall time and 78 ms CPU time. What does that suggest?


## 3. Explain `tottime` versus cumulative time in cProfile.


## 4. Why run an unprofiled baseline?


## 5. How would you detect event-loop blocking in Node?


## 6. What can tracemalloc prove and not prove?


## 7. Why can offloading every CPU task to an unbounded thread pool fail?


## 8. A response mapping creates three copies of a 1 MB list. What should you measure?


## 9. When is custom JSON encoding unjustified?


## 10. Why can an API optimization overload PostgreSQL?


## 11. Design a blocking experiment for artifact checksum.


## 12. A candidate lowers allocations 40% but p95 and CPU do not change. Accept?


## Submission format

Submit Module 05 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
