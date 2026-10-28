# API Performance, Capacity, and Traffic Engineering

**Course 5 of 10 — Sustain the promise under pressure**

## Course promise

Measure, model, and control latency, throughput, resource use, fairness, and overload behavior with comparable evidence.

> **Governing question:** Where do time and capacity go, what is the first limiting resource, and which measured change improves the system without weakening correctness?

## Place in the program

**Incoming boundary:** The Course 4 observable and recoverable API 1.2 service with Security and Reliability Profiles 1.0 and migrations 001–008.

**Outgoing boundary:** Performance Profile 1.0, migration 009, workload identities, benchmark evidence, HTTP and query optimizations, concurrency and cache policy, traffic controls, capacity models, and performance release gates.

Course 5 treats its incoming handoff as historical evidence, not editable scaffolding. It may add only the sustain the promise under pressure mechanisms governed here; any public or durable change requires an explicit compatibility and release decision.

## What you will add

- measurement contracts and representative workload models;
- valid benchmark design and statistical interpretation;
- HTTP, database, and runtime profiling;
- queueing, backpressure, caching, quotas, and load shedding;
- capacity, cost, and regression release decisions;

## Course-level learning outcomes

- Distinguish performance requirements from reliability objectives and capacity claims.
- Distinguish load generation, timing, outcome collection, and analysis.
- Separate resource state, selected representation, and transferred message.
- Separate client wait, pool wait, lock wait, planning, execution, and transfer.
- Separate wall-clock, process CPU, and allocation measurements.
- Identify every implicit and explicit queue in a request journey.
- Distinguish HTTP, process-local, shared application, database, and client caches.
- Distinguish rate limits, quotas, concurrency limits, and capacity admission.
- Translate workload forecasts into resource demand.
- Design a tiered performance verification pipeline.

## Module map

| Day | Chapter | Governing question | Capstone increment |
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

## Deliberate boundaries

This course does not claim or teach the following as part of its completion:

- language benchmark contests;
- automatic Redis or Kubernetes prescriptions;
- production capacity claims from laptop evidence;
- optimization that weakens correctness or security;

Those boundaries prevent the course from becoming a survey of adjacent tools and make its completion claims defensible.

## How to study

Begin with [Start here](start-here.md). In Course 5, read each chapter around the question **Where do time and capacity go, what is the first limiting resource, and which measured change improves the system without weakening correctness?**; then use the exercises, controlled lab, and checkpoint to turn the explanation into evidence. [Language strategy](language-strategy.md) and [Evidence model](evidence-model.md) define how implementation and proof support—not replace—the course book.

## Completion

Complete all ten checkpoints, the capstone release or defense, and the outgoing handoff. A green command without a defensible claim and evidence boundary is not sufficient.
