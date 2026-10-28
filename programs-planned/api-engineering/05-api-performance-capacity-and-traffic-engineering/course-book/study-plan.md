# Two-Week Study Plan — API Performance, Capacity, and Traffic Engineering

## Rhythm

Course 5 uses ten teaching days over two weeks. Orientation freezes the incoming boundary before Day 1; each day moves from the sustain the promise under pressure model to transfer problems, a controlled experiment, and an evidence defense. The middle weekend is for repairing failed checkpoints, not adding features.

| Day | Module | Required result |
|---:|---|---|
| 1 | [Measurement Contract and Critical Workloads](module-01-measurement-contract-and-critical-workloads/index.md) | Freeze six critical workloads, measurement envelopes, outcome populations, evidence classes, and comparable baselines. |
| 2 | [Benchmark Design and Statistical Interpretation](module-02-benchmark-design-and-statistical-interpretation/index.md) | Build reproducible benchmark profiles, repeated runs, quantile and interval summaries, and accepted/rejected/inconclusive comparisons. |
| 3 | [HTTP Efficiency and Representation Cost](module-03-http-efficiency-and-representation-cost/index.md) | Optimize artifact and metadata delivery while preserving authorization, ETags, ranges, and bounded memory. |
| 4 | [PostgreSQL Query and Persistence Performance](module-04-postgresql-query-and-persistence-performance/index.md) | Capture before/after plans, add evidence-backed indexes, size database connections, and preserve owner-aware query semantics. |
| 5 | [Runtime Profiling and Allocation Control](module-05-runtime-profiling-and-allocation-control/index.md) | Profile named phases, detect blocking work, bound profiling overhead, and prove mechanism-level improvements. |
| 6 | [Queueing, Concurrency, and Backpressure](module-06-queueing-concurrency-and-backpressure/index.md) | Implement bounded admission, per-operation limits, queue accounting, permit release, and recovery after pressure. |
| 7 | [Caching, Freshness, and Invalidation](module-07-caching-freshness-and-invalidation/index.md) | Build authorization-aware keys, TTL/capacity policy, source-version invalidation, single-flight fills, and failure semantics. |
| 8 | [Traffic Shaping, Quotas, and Load Shedding](module-08-traffic-shaping-quotas-and-load-shedding/index.md) | Implement multi-dimensional fixed-point budgets, tenant isolation, staged shedding, and rollback of partial reservations. |
| 9 | [Capacity Modeling and Scaling Decisions](module-09-capacity-modeling-and-scaling-decisions/index.md) | Model CPU, connections, workers, queues, storage, egress, cost, headroom, and scaling decisions. |
| 10 | [Performance Regression and Release Engineering](module-10-performance-regression-and-release-engineering/index.md) | Build correctness-first regression gates, environment comparability, accepted/rejected/inconclusive candidates, and a performance dossier. |

## Suggested day

```text
08:30  retrieval practice and checkpoint repair
09:00  chapter reading and diagram reconstruction
11:00  worked examples and standards review
13:00  primary-track implementation reading
15:00  exercises before answers
17:00  controlled lab
19:30  evidence package and checkpoint defense
```

The two-week schedule is subordinate to evidence. If the sustain the promise under pressure argument becomes unclear, stop at the last green checkpoint, reduce the counterexample, and resume only after the owning mechanism is understood.

## Weekend synthesis

At the Week 1 boundary, reconstruct how Modules 1–5 change the platform while preserving this incoming state: The Course 4 observable and recoverable API 1.2 service with Security and Reliability Profiles 1.0 and migrations 001–008. Rerun those checkpoints and postpone every feature that does not serve the Course 5 responsibility.

## Recovery route

When a checkpoint fails:

1. isolate the first broken invariant;
2. restore the predecessor baseline if necessary;
3. reduce the failing case;
4. repair the owning mechanism;
5. retain the case as a regression;
6. update your explanation before continuing.
