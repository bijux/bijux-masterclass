# API Performance, Capacity, and Traffic Engineering

**Course 5 of 6 — Sustain the promise under pressure**

Preserve correctness, latency, throughput, fairness, and bounded resource use as demand and data volume grow.

> Where does time and capacity go, what is the first limiting resource, and which measured change improves the system without weakening its promise?

## Begin with the course book

1. Read [Course introduction](course-book/index.md).
2. Complete [Start here](course-book/start-here.md) and [orientation](course-book/module-00-orientation/index.md).
3. Follow the ten modules in order.
4. Use the capstone and implementation tracks only through the reading routes named in each chapter.
5. Preserve checkpoint evidence before progressing.

## Modules

01. [Measurement Contract and Critical Workloads](course-book/module-01-measurement-contract-and-critical-workloads/index.md)
02. [Benchmark Design and Statistical Interpretation](course-book/module-02-benchmark-design-and-statistical-interpretation/index.md)
03. [HTTP Efficiency and Representation Cost](course-book/module-03-http-efficiency-and-representation-cost/index.md)
04. [PostgreSQL Query and Persistence Performance](course-book/module-04-postgresql-query-and-persistence-performance/index.md)
05. [Runtime Profiling and Allocation Control](course-book/module-05-runtime-profiling-and-allocation-control/index.md)
06. [Queueing, Concurrency, and Backpressure](course-book/module-06-queueing-concurrency-and-backpressure/index.md)
07. [Caching, Freshness, and Invalidation](course-book/module-07-caching-freshness-and-invalidation/index.md)
08. [Traffic Shaping, Quotas, and Load Shedding](course-book/module-08-traffic-shaping-quotas-and-load-shedding/index.md)
09. [Capacity Modeling and Scaling Decisions](course-book/module-09-capacity-modeling-and-scaling-decisions/index.md)
10. [Performance Regression and Release Engineering](course-book/module-10-performance-regression-and-release-engineering/index.md)

## Program boundary

**Incoming:** The Course 4 observable and recoverable API 1.2 service with Security and Reliability Profiles 1.0 and migrations 001–008.

**Outgoing:** Performance Profile 1.0, migration 009, workload identities, benchmark evidence, HTTP and query optimizations, concurrency and cache policy, traffic controls, capacity models, and performance release gates.

## Implementation strategy

Choose one primary implementation track. Compare measurement identity, arithmetic, and externally visible traffic decisions across both languages.

## Verification

```bash
make doctor
make core-proof
make manifest-proof
```

Environment-dependent routes are reported separately. Missing infrastructure is never represented as a passing live proof.
