# Capstone — API Performance, Capacity, and Traffic Engineering

## Cumulative system

Course 5 continues the Analysis Runs Platform at the point where the previous course stopped. Its capstone exists to sustain the promise under pressure while preserving the same projects, datasets, runs, artifacts, identities, and user journeys.

## Inherited state

The Course 4 observable and recoverable API 1.2 service with Security and Reliability Profiles 1.0 and migrations 001–008.

The inherited boundary is read-only: The Course 4 observable and recoverable API 1.2 service with Security and Reliability Profiles 1.0 and migrations 001–008. A difficult implementation is not permission to rewrite predecessor contracts, migrations, profiles, or evidence; the current course must solve the problem at its own owning layer.

## Course additions

- measurement contracts and representative workload models;
- valid benchmark design and statistical interpretation;
- HTTP, database, and runtime profiling;
- queueing, backpressure, caching, quotas, and load shedding;
- capacity, cost, and regression release decisions;

## Increment map

| Module | Mechanism | Cumulative result |
|---:|---|---|
| 1 | Measurement Contract and Critical Workloads | Freeze six critical workloads, measurement envelopes, outcome populations, evidence classes, and comparable baselines. |
| 2 | Benchmark Design and Statistical Interpretation | Build reproducible benchmark profiles, repeated runs, quantile and interval summaries, and accepted/rejected/inconclusive comparisons. |
| 3 | HTTP Efficiency and Representation Cost | Optimize artifact and metadata delivery while preserving authorization, ETags, ranges, and bounded memory. |
| 4 | PostgreSQL Query and Persistence Performance | Capture before/after plans, add evidence-backed indexes, size database connections, and preserve owner-aware query semantics. |
| 5 | Runtime Profiling and Allocation Control | Profile named phases, detect blocking work, bound profiling overhead, and prove mechanism-level improvements. |
| 6 | Queueing, Concurrency, and Backpressure | Implement bounded admission, per-operation limits, queue accounting, permit release, and recovery after pressure. |
| 7 | Caching, Freshness, and Invalidation | Build authorization-aware keys, TTL/capacity policy, source-version invalidation, single-flight fills, and failure semantics. |
| 8 | Traffic Shaping, Quotas, and Load Shedding | Implement multi-dimensional fixed-point budgets, tenant isolation, staged shedding, and rollback of partial reservations. |
| 9 | Capacity Modeling and Scaling Decisions | Model CPU, connections, workers, queues, storage, egress, cost, headroom, and scaling decisions. |
| 10 | Performance Regression and Release Engineering | Build correctness-first regression gates, environment comparability, accepted/rejected/inconclusive candidates, and a performance dossier. |

## Implementation route

Build the complete Course 5 increment in one primary track. Use the second track only after the chapter model is clear, then run shared vectors to test whether **sustain the promise under pressure** survives an idiomatic implementation in another runtime.

## Final state

Performance Profile 1.0, migration 009, workload identities, benchmark evidence, HTTP and query optimizations, concurrency and cache policy, traffic controls, capacity models, and performance release gates.

## Handoff discipline

The successor receives only the settled result: Performance Profile 1.0, migration 009, workload identities, benchmark evidence, HTTP and query optimizations, concurrency and cache policy, traffic controls, capacity models, and performance release gates. Local caches, secrets, ad-hoc reports, and environment-specific artifacts remain outside the handoff.
