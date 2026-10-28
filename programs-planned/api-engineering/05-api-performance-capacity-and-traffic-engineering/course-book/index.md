# API Performance, Capacity, and Traffic Engineering

**Course 5 of 6 — Sustain the promise under pressure**

> **Central question:** Where does time and capacity go, what is the first limiting resource, and which measured change improves the system without weakening its promise?

## Course responsibility

Preserve correctness, latency, throughput, fairness, and bounded resource use as demand and data volume grow. The course inherits earlier guarantees rather than restating them as new work. Its purpose is to add one mature engineering responsibility to the same Analysis Runs Platform.

## Incoming and outgoing boundaries

**Incoming boundary:** The Course 4 observable and recoverable API 1.2 service with Security and Reliability Profiles 1.0 and migrations 001–008.

**Outgoing boundary:** Performance Profile 1.0, migration 009, workload identities, benchmark evidence, HTTP and query optimizations, concurrency and cache policy, traffic controls, capacity models, and performance release gates.

## What you will be able to do

After completing the course, you can:

- freeze six critical workloads, measurement envelopes, outcome populations, evidence classes, and comparable baselines.
- build reproducible benchmark profiles, repeated runs, quantile and interval summaries, and accepted/rejected/inconclusive comparisons.
- optimize artifact and metadata delivery while preserving authorization, ETags, ranges, and bounded memory.
- capture before/after plans, add evidence-backed indexes, size database connections, and preserve owner-aware query semantics.
- profile named phases, detect blocking work, bound profiling overhead, and prove mechanism-level improvements.
- implement bounded admission, per-operation limits, queue accounting, permit release, and recovery after pressure.
- build authorization-aware keys, TTL/capacity policy, source-version invalidation, single-flight fills, and failure semantics.
- implement multi-dimensional fixed-point budgets, tenant isolation, staged shedding, and rollback of partial reservations.
- model CPU, connections, workers, queues, storage, egress, cost, headroom, and scaling decisions.
- build correctness-first regression gates, environment comparability, accepted/rejected/inconclusive candidates, and a performance dossier.

## Ten-module learning path

| Day | Module | Governing question | Capstone result |
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


## How the book is organized

Each numbered module has five learner-facing files:

1. `index.md` — the complete explanation, worked designs, implementation reading, failure analysis, and transition;
2. `exercises.md` — twelve transfer questions;
3. `exercise-answers.md` — matching reasoned reference answers;
4. `lab.md` — one controlled failure, pressure, or release experiment;
5. `checkpoint.md` — the evidence required before progression.

The course book is authoritative. Capstone source, fixtures, reports, and proof scripts make the material executable; they do not replace the explanation.

## Completion standard

You complete the course only when every module checkpoint, the capstone proof, and the final defense pass. A strong result states not only what worked but which claim was established, which evidence class supports it, and what remains unexecuted.

Continue with [Start here](start-here.md).
