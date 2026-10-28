# Module 09 — Capacity Modeling and Scaling Decisions

> **Program stage:** Course 5 of 10 — Sustain the promise under pressure.

> **Central question:** What capacity does the current system have, what uncertainty surrounds it, and which resource becomes the first bottleneck as demand grows?

## Where this module fits

Module 08 produced **Implement multi-dimensional fixed-point budgets, tenant isolation, staged shedding, and rollback of partial reservations**. This module extends that result by asking: **What capacity does the current system have, what uncertainty surrounds it, and which resource becomes the first bottleneck as demand grows?**

The new capstone increment is **Model CPU, connections, workers, queues, storage, egress, cost, headroom, and scaling decisions**. It becomes the prerequisite for **Performance Regression and Release Engineering**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Translate workload forecasts into resource demand.
- Calculate service demand from utilization and throughput.
- Identify the first bottleneck across CPU, database, memory, storage, network, and worker capacity.
- Apply headroom and failure/maintenance assumptions.
- Model queue drain and recovery capacity.
- Represent uncertainty with ranges and scenarios.
- Compare vertical, horizontal, optimization, and demand-shaping options.
- Include stateful dependency and connection limits.
- Estimate cost per useful completed unit.
- Define trigger metrics and remeasurement conditions.

## Capstone increment

Model CPU, connections, workers, queues, storage, egress, cost, headroom, and scaling decisions.

## Core performance model

### 1. Capacity is conditional


A capacity statement must name:

```text
workload mix
data scale and distribution
service objectives
environment/topology
software versions
failure assumptions
headroom policy
```

“Handles 2,000 requests/s” is incomplete. Which requests? With what artifact sizes, database state, worker mix, and latency/error bounds?

The capstone model reports capacity per scenario, not one universal maximum. It preserves workload identities from Module 1 and uses measured service demand from earlier modules.


### 2. From throughput and utilization to service demand


For a resource over a stable interval:

```text
resource service demand per completion
≈ resource busy time / completed work
```

If four CPU cores are 60% utilized for 60 seconds while 12,000 requests complete:

```text
busy CPU seconds = 4 × 0.60 × 60 = 144
CPU demand/request = 144 / 12,000 = 0.012 s = 12 ms
```

At that demand, theoretical CPU throughput at 100% is about `4 / 0.012 ≈ 333 requests/s`. Operating capacity must apply headroom and account for workload mix.

This estimate assumes utilization and completed-work populations align. CPU consumed by background jobs must be attributed or included.


### 3. Multi-class workload model


Let workload class `i` have forecast rate `λᵢ` and resource demand `Dᵢ,r` at resource `r`. Total utilization contribution is approximately:

```text
U_r = Σ λᵢ × Dᵢ,r / capacity_units_r
```

For CPU measured in core-seconds, capacity units are cores. For database connections, use active service demand and concurrency rather than treating a connection as CPU. For network, use bytes per second plus protocol overhead and burst behavior.

The model file stores each class separately. This lets a change in mix alter the result without inventing one average request.


### 4. Headroom and failure capacity


Running at measured maximum is not a production plan. Headroom absorbs bursts, skew, maintenance, noisy neighbors, model error, and recovery work. Define target utilization per resource, such as 60–75%, from operational evidence rather than copying a universal number.

Failure assumptions matter. If one of three API instances may be unavailable during deployment, remaining instances must serve critical load within objectives or the release process must reduce traffic. If database failover temporarily lowers capacity, queue and shedding policies must protect durable work.

Record both normal and degraded capacity. Course 4 runbooks and alerts supply the failure scenarios.


### 5. Stateful bottlenecks


Stateless API instances may scale horizontally, but PostgreSQL, durable queues, and artifact storage have state and coordination limits. Adding API instances also adds:

- database pool connections;
- cache copies or shared-cache demand;
- outbound sockets;
- telemetry volume;
- limiter state divergence;
- worker claim pressure.

The capacity model therefore computes aggregate connections and downstream demand for each scale step. Horizontal API scaling can worsen a database bottleneck.


### 6. Queue drain and recovery


After an outage, the system must serve new arrivals and drain backlog. If completion capacity is `μ` and new arrival rate is `λ`, net drain rate is `μ - λ` when positive.

For backlog `B`:

```text
drain time = B / (μ - λ)
```

If `μ <= λ`, the backlog never drains without reducing arrivals or increasing capacity. Recovery capacity may need additional temporary headroom, but aggressive drain can overload storage or webhook receivers.

Model separate stages: analysis jobs, artifact publication, and webhook deliveries.


### 7. Storage and data growth


Capacity includes:

- primary data;
- indexes;
- WAL and replication;
- backups;
- temporary files;
- artifacts;
- cache;
- telemetry retention.

Use daily creation rate, retention, replication factor, compression, and cleanup lag. Index changes from Module 4 increase storage and write demand. Artifact ranges and caching from Modules 3 and 7 may reduce network but not stored bytes.

Storage capacity has both space and throughput/IOPS dimensions. Reaching I/O saturation before disk fullness is common.


### 8. Uncertainty and scenarios


Forecasts are uncertain. Avoid a single precise number. Define:

- expected scenario;
- high-growth/high-payload scenario;
- degraded-capacity scenario;
- optional low-growth scenario.

Use ranges for arrival rates, payload sizes, service demand, and growth. Sensitivity analysis asks which uncertain input most changes the first bottleneck. That input deserves better measurement.

The capstone uses Decimal arithmetic and records assumptions with source/evidence dates.


### 9. Scaling options


For each bottleneck, compare:

1. **optimize demand** — reduce service demand through query/runtime/HTTP changes;
2. **shape demand** — quotas, batching, scheduling, compression, retention;
3. **vertical scale** — more capacity per instance;
4. **horizontal scale** — more independent service capacity;
5. **partition or isolate** — only when ownership and operational costs justify it;
6. **change objective/product policy** — explicit business decision, not silent degradation.

Microservices are not a capacity primitive. Distribution adds overhead and should be considered in Course 8 only after a bounded service demonstrates a justified boundary.


### 10. Cost and efficiency


Track cost per useful completed outcome, not cost per request regardless of correctness:

```text
cost per completed analysis
cost per GiB artifact delivered
cost per 1,000 eligible metadata reads
```

A candidate that doubles instances and improves throughput 20% may reduce efficiency. Cost is not only infrastructure price; operational complexity, migration risk, and engineering maintenance matter.

The capacity decision states expected headroom gained, cost, failure mode, implementation effort, and trigger for the next step.


### 11. Validate model against reality


A model is not complete when the spreadsheet balances. Compare predicted utilization and queueing with a controlled workload at one or more points. Calibrate service demand when error is systematic.

Store model version and actual-versus-predicted observations. When software, workload, topology, or data distribution changes materially, remeasure. A capacity model decays.

The final handoff gives Course 6 the measured worker/queue budgets needed to design asynchronous contracts without inventing broker capacity.

## Course requirements

| Rule | Required behavior | Failure if omitted | Decisive evidence |
|---|---|---|---|
| Conditioned claim | Capacity statement names workload, environment, objectives, and failure mode. | One universal RPS number is published. | Scenario report |
| Multi-class demand | Critical workloads remain separate in resource arithmetic. | Average request hides expensive mix. | Model schema |
| Headroom explicit | Target utilization and rationale are versioned. | Theoretical maximum becomes operating plan. | Capacity profile |
| Downstream included | Scale steps include database, storage, network, and telemetry effects. | Stateless tier scaling overloads stateful tier. | Aggregate model |
| Recovery modeled | Backlog drain under new arrivals is calculated. | Outage ends but backlog never recovers. | Drain scenario |
| Uncertainty visible | Inputs have ranges/source dates and sensitivity. | Forecast precision is fabricated. | Scenario/sensitivity report |
| Cost useful-outcome based | Efficiency uses correct completed outcomes. | Failures improve cost/request metric. | Cost model |
| Model calibrated | At least one predicted point is compared with measured behavior. | Spreadsheet is treated as proof. | Validation run |

## Worked failures

### Case 1 — The linear instance forecast

**Initial condition.** Traffic is expected to triple, so API instances are tripled.

**Analysis.** The database is already the first bottleneck and each instance adds pool connections. API CPU has headroom.

**Correct response.** Optimize or scale the database/query path and cap aggregate connections before adding API instances.

**Lesson.** Scale the limiting resource, not the visible tier.

### Case 2 — The no-failure plan

**Initial condition.** Normal demand fits three instances at 85% utilization, but deployment removes one instance.

**Analysis.** Remaining instances exceed capacity and overload during every rollout.

**Correct response.** Plan N-1 or use traffic reduction/deployment sequencing with explicit objective impact.

**Lesson.** Maintenance is a capacity scenario.

### Case 3 — The backlog that never drains

**Initial condition.** After outage, workers complete 100 jobs/s while new arrivals are 110 jobs/s.

**Analysis.** Net drain is negative. Backlog grows despite recovery.

**Correct response.** Increase completion capacity, shape arrivals, or shed new work until `μ > λ`.

**Lesson.** Recovery needs surplus capacity.

### Case 4 — The precise five-year number

**Initial condition.** A model predicts 47.382 instances in 2031 from one week of traffic.

**Analysis.** Input uncertainty dominates decimal precision; workload mix and software will change.

**Correct response.** Use near-term scenarios, ranges, sensitivity, trigger metrics, and periodic recalibration.

**Lesson.** Precision is not accuracy.

## Python implementation

### Mechanism

The Python capacity module uses `Decimal` for auditable rates and service demand, computes resource utilization/headroom, backlog drain, storage growth, first bottleneck, and scenario sensitivity.

### Repository paths

- `capstone/tracks/python-fastapi/src/api_performance/capacity.py`
- `capstone/tracks/python-fastapi/src/api_performance/cost.py`
- `capstone/tracks/python-fastapi/tests_performance/test_capacity_cost.py`

### Focused example

```python
from decimal import Decimal
from api_performance.capacity import cpu_demand

demand = cpu_demand(
    cores=Decimal("4"),
    utilization=Decimal("0.60"),
    interval_seconds=Decimal("60"),
    completions=Decimal("12000"),
)
assert demand == Decimal("0.012")
```

Decimal preserves reviewable arithmetic and serialized values. The model validates non-negative rates, utilization bounds, compatible units, and positive capacity before calculating headroom.

### Python-specific failure to avoid

Do not mix binary floats and Decimal implicitly. Parse decimal strings from model files and quantize only for presentation, not during intermediate calculations.

## TypeScript implementation

### Mechanism

The TypeScript capacity model uses fixed-scale decimal integers for cross-language vectors. Rates and demands are serialized as decimal strings and converted through a small exact decimal helper.

### Repository paths

- `capstone/tracks/typescript-fastify/src/performance/capacity.ts`
- `capstone/tracks/typescript-fastify/src/performance/cost.ts`
- `capstone/tracks/typescript-fastify/test-performance-core/capacity-cost.test.mjs`

### Focused example

```typescript
const demand = cpuDemand({
  cores: decimal("4"),
  utilization: decimal("0.60"),
  intervalSeconds: decimal("60"),
  completions: decimal("12000"),
});
if (formatDecimal(demand) !== "0.012") {
  throw new Error("unexpected CPU demand");
}
```

The helper stores scaled bigint values and refuses silent rounding. Model output is human-readable decimal text with an explicit scale.

### TypeScript-specific failure to avoid

JavaScript number arithmetic can display small binary rounding errors and lose integer precision. Use the provided fixed-scale representation for decision records.

## Cross-language invariant

Both tracks agree on service demand, utilization, headroom, drain time, storage growth, first-bottleneck ordering, and cost vectors at the declared decimal scale.

## Failure patterns

- **Universal capacity number.** Workload and objectives are omitted. **Decisive check:** conditioned scenario.
- **Stateless-only scaling.** Downstream stateful demand ignored. **Decisive check:** aggregate connection/resource model.
- **No headroom.** Measured maximum becomes target. **Decisive check:** degraded/maintenance scenario.
- **Average request.** Expensive class disappears into mix. **Decisive check:** multi-class table.
- **Backlog amnesia.** Recovery serves new load but never drains old work. **Decisive check:** net drain calculation.
- **Forecast pseudoprecision.** Uncertain inputs yield precise output. **Decisive check:** ranges and sensitivity.

## Evidence and design review

Before accepting the module increment, answer:

1. Which workload class contributes most to each resource?
2. Which resource reaches target utilization first?
3. What happens under one-instance or dependency degradation?
4. Can the system drain backlog while serving new arrivals?
5. Which uncertain input most changes the decision?
6. What is the cheapest reversible step that adds useful headroom?

## Module synthesis

You are ready to leave this module when you can **translate workload forecasts into resource demand, calculate service demand from utilization and throughput, and identify the first bottleneck across CPU, database, memory, storage, network, and worker capacity** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **the lab introduces its declared planted defect** and requiring the following oracle: **all resource arithmetic has units; workload classes remain separate; normal and degraded headroom are reported; backlog drains only when completion exceeds arrivals.**

The cumulative platform now includes **Model CPU, connections, workers, queues, storage, egress, cost, headroom, and scaling decisions**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Performance Regression and Release Engineering](../module-10-performance-regression-and-release-engineering/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
