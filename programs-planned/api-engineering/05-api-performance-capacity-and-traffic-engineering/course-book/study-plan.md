# Ten-Day Study Plan — API Performance, Capacity, and Traffic Engineering

This is a dense two-week course with one numbered module per weekday. Orientation is required before Day 1 and is not counted as a teaching module. The middle weekend contains no hidden new curriculum.

| Day | Module | Main intellectual move | Required result |
|---:|---|---|---|
| 1 | [Measurement Contract and Critical Workloads](module-01-measurement-contract-and-critical-workloads/index.md) | What exactly is being measured, under which workload and environment identity, and which correctness oracle still applies? | Freeze six critical workloads, measurement envelopes, outcome populations, evidence classes, and comparable baselines. |
| 2 | [Benchmark Design and Statistical Interpretation](module-02-benchmark-design-and-statistical-interpretation/index.md) | How do open and closed demand, warmup, sample size, missing outcomes, variation, and statistical uncertainty change benchmark meaning? | Build reproducible benchmark profiles, repeated runs, quantile and interval summaries, and accepted/rejected/inconclusive comparisons. |
| 3 | [HTTP Efficiency and Representation Cost](module-03-http-efficiency-and-representation-cost/index.md) | Where do HTTP connections, representations, compression, conditional requests, range delivery, and streaming consume time and bytes? | Optimize artifact and metadata delivery while preserving authorization, ETags, ranges, and bounded memory. |
| 4 | [PostgreSQL Query and Persistence Performance](module-04-postgresql-query-and-persistence-performance/index.md) | Which query plan, index, lock, pool, or pagination behavior is the first persistence bottleneck for a declared workload? | Capture before/after plans, add evidence-backed indexes, size database connections, and preserve owner-aware query semantics. |
| 5 | [Runtime Profiling and Allocation Control](module-05-runtime-profiling-and-allocation-control/index.md) | Which Python or Node.js runtime phase consumes wall time, CPU, allocations, event-loop capacity, or serialization effort? | Profile named phases, detect blocking work, bound profiling overhead, and prove mechanism-level improvements. |
| 6 | [Queueing, Concurrency, and Backpressure](module-06-queueing-concurrency-and-backpressure/index.md) | How do arrival rate, service time, queue depth, concurrency, fairness, and backpressure determine overload behavior? | Implement bounded admission, per-operation limits, queue accounting, permit release, and recovery after pressure. |
| 7 | [Caching, Freshness, and Invalidation](module-07-caching-freshness-and-invalidation/index.md) | Which data is safe to cache, for whom, for how long, and who owns invalidation after mutation or failure? | Build authorization-aware keys, TTL/capacity policy, source-version invalidation, single-flight fills, and failure semantics. |
| 8 | [Traffic Shaping, Quotas, and Load Shedding](module-08-traffic-shaping-quotas-and-load-shedding/index.md) | How should quotas, priorities, cost budgets, and load shedding preserve fairness and truthful 429/503 outcomes? | Implement multi-dimensional fixed-point budgets, tenant isolation, staged shedding, and rollback of partial reservations. |
| 9 | [Capacity Modeling and Scaling Decisions](module-09-capacity-modeling-and-scaling-decisions/index.md) | What capacity does the current system have, what uncertainty surrounds it, and which resource becomes the first bottleneck as demand grows? | Model CPU, connections, workers, queues, storage, egress, cost, headroom, and scaling decisions. |
| 10 | [Performance Regression and Release Engineering](module-10-performance-regression-and-release-engineering/index.md) | How does a performance change become a reproducible release decision rather than a favorable chart? | Build correctness-first regression gates, environment comparability, accepted/rejected/inconclusive candidates, and a performance dossier. |


## Daily rhythm

A productive day uses four blocks:

- **Model:** read the chapter and reconstruct the governing diagram or state machine;
- **Transfer:** answer the exercises and compare with the reasoned answers;
- **Experiment:** perform the lab, including the failure or pressure condition;
- **Defense:** complete the checkpoint and preserve evidence.

Do not treat “morning to night” as uninterrupted screen time. Use deliberate breaks. Stop blind copying when fatigue removes your ability to predict outcomes.

## Middle weekend

Use Saturday for at most one focused repair cycle per failed checkpoint and for a cross-module synthesis note. Sunday contains no required implementation. Rerun predecessor and accumulated course proofs before Week 2.

## Recovery rule

When behind, reduce breadth before reducing evidence. Complete one language track deeply, keep the comparison focused, and do not skip the failure experiment. A copied second implementation is less valuable than one defended invariant.
