# Capstone — API Performance, Capacity, and Traffic Engineering

## One continuing platform

The capstone is the Analysis Runs Platform. Principals create projects, register datasets, submit analysis runs, observe progress, retrieve verified artifacts, and receive or consume completion facts. Course 5 does not replace the platform; it adds the responsibility **sustain the promise under pressure**.

## Starting state

The Course 4 observable and recoverable API 1.2 service with Security and Reliability Profiles 1.0 and migrations 001–008.

## Course increments

| Module | Platform increment |
|---:|---|
| 1 | Freeze six critical workloads, measurement envelopes, outcome populations, evidence classes, and comparable baselines. |
| 2 | Build reproducible benchmark profiles, repeated runs, quantile and interval summaries, and accepted/rejected/inconclusive comparisons. |
| 3 | Optimize artifact and metadata delivery while preserving authorization, ETags, ranges, and bounded memory. |
| 4 | Capture before/after plans, add evidence-backed indexes, size database connections, and preserve owner-aware query semantics. |
| 5 | Profile named phases, detect blocking work, bound profiling overhead, and prove mechanism-level improvements. |
| 6 | Implement bounded admission, per-operation limits, queue accounting, permit release, and recovery after pressure. |
| 7 | Build authorization-aware keys, TTL/capacity policy, source-version invalidation, single-flight fills, and failure semantics. |
| 8 | Implement multi-dimensional fixed-point budgets, tenant isolation, staged shedding, and rollback of partial reservations. |
| 9 | Model CPU, connections, workers, queues, storage, egress, cost, headroom, and scaling decisions. |
| 10 | Build correctness-first regression gates, environment comparability, accepted/rejected/inconclusive candidates, and a performance dossier. |


## Language tracks

Choose one primary implementation track. Compare measurement identity, arithmetic, and externally visible traffic decisions across both languages.

Shared fixtures, vectors, operation maps, releases, and black-box scenarios define parity. Identical class names or directory shape do not.

## Capstone reading order

1. read the module chapter and identify the owning mechanism;
2. inspect the narrow source path named by the chapter;
3. inspect the corresponding test or vector;
4. run the focused proof;
5. perform the lab modification in a working branch;
6. return to the chapter and explain how the implementation realizes the model.

## Handoff discipline

The predecessor material is read-only evidence. The current course may add a compatible public interface, migration, or profile only when its release rules permit it. It must not rewrite earlier history to simplify the present implementation.

**Outgoing handoff:** Performance Profile 1.0, migration 009, workload identities, benchmark evidence, HTTP and query optimizations, concurrency and cache policy, traffic controls, capacity models, and performance release gates.

## Final capstone question

Can you trace one accepted case and one rejected, failed, overloaded, or duplicated case from the public boundary to the authoritative outcome, then name the proof and limitation at every layer this course owns?
