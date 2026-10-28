# Module 06 — Queueing, Concurrency, and Backpressure

> **Program stage:** Course 5 of 6 — Sustain the promise under pressure.

> **Central question:** How do arrival rate, service time, queue depth, concurrency, fairness, and backpressure determine overload behavior?

## Where this module fits


Performance collapse is often a queueing problem rather than a slow-function problem. When work arrives faster than a limiting stage can complete it, the difference accumulates as waiting, memory, open connections, database sessions, job rows, or retry pressure. Latency grows before throughput visibly falls.

This module gives the learner a practical queueing model. Little’s Law connects average work in the system, throughput, and average time. Utilization explains why operating near theoretical maximum produces unstable waiting. Bounded admission and backpressure turn unbounded delay into explicit, observable decisions.

The capstone has several queues: HTTP admission, database pool waiters, durable analysis jobs, active artifact streams, webhook deliveries, and client-side retry attempts. They must not be tuned independently. Increasing one concurrency limit can merely move overload to PostgreSQL, storage, or an external receiver.


## Capstone result

Implement bounded admission, per-operation limits, queue accounting, permit release, and recovery after pressure.

Implement bounded concurrency, queue capacity, admission deadlines, fair permits, and backpressure evidence for run submission, worker execution, artifact streaming, and webhook delivery.

## Learning outcomes

By the end of this module, you can:

- identify every implicit and explicit queue in a request journey
- apply Little’s Law with compatible populations and intervals
- distinguish service time, waiting time, response time, and service demand
- explain why tail latency rises rapidly near saturation
- size concurrency from a limiting resource rather than CPU count folklore
- bound queue length and waiting time
- propagate cancellation without undoing committed work
- design backpressure across API, worker, storage, and outbound stages
- preserve fairness and avoid starvation
- separate admission rejection from internal failure

## Core performance model

### 1. Every wait is a queue


A queue can be visible as a table or hidden inside a runtime:

- socket accept backlog;
- web-server request queue;
- application semaphore waiters;
- database connection-pool waiters;
- row-lock waiters;
- durable job table;
- executor work queue;
- storage read queue;
- outbound connection pool;
- client retries.

Inventory each queue with owner, capacity, ordering, timeout, cancellation behavior, and observable depth. An “unbounded async task list” is an unbounded queue even if it has no queue class.

The same unit must be used when comparing arrival and service rates. HTTP requests, analysis jobs, and artifact chunks are different work units.


### 2. Little’s Law


For a stable system over a compatible interval:

```text
L = λW
```

`L` is average work in the system, `λ` is average throughput, and `W` is average time in the system.

If a worker plane completes 20 jobs/s and jobs spend an average of 5 s from admission to completion, about 100 jobs are in the system on average. If the measured queue plus active jobs is 500, either the interval is not stable, the populations differ, or the time estimate is wrong.

Little’s Law is a conservation relationship, not a capacity formula. It does not assume a particular arrival distribution, but it requires stable averages and consistent boundaries.


### 3. Service time, response time, and service demand


**Service time** at a stage is time actively receiving service there. **Waiting time** is time queued before service. **Response time** for a journey includes both across stages. **Service demand** is resource time consumed per completed unit, such as CPU-seconds per request or database-seconds per query.

A connection-pool wait can dominate response time even when query service time is low. Increasing connections reduces one wait only until database contention raises service time.

The benchmark envelope stores queue wait and active service separately where possible. This permits a decision between faster service and stricter admission.


### 4. Saturation and the utilization knee


In simple queueing models, waiting grows sharply as utilization approaches 1. For an M/M/1 approximation:

```text
W = 1 / (μ - λ)
ρ = λ / μ
```

where `μ` is service rate and `λ < μ`. Real API systems are not M/M/1: arrivals, service times, multiple servers, priorities, and retries differ. Use the formula to build intuition, not to publish exact predictions.

The practical objective is headroom. A resource at 95% average utilization may have no capacity for bursts, skew, maintenance, or failure. Tail latency and queue depth reveal the knee more reliably than average utilization alone.


### 5. Bounded admission


Admission control decides before expensive work consumes scarce resources. It can bound:

- active requests;
- outstanding database operations;
- active uploads/downloads;
- queued analysis jobs per tenant;
- concurrent webhook attempts.

A permit has an acquisition deadline. When no permit is available, the service returns a documented overload response or declines work before creating partial effects. Waiting forever is not reliability.

The permit implementation must release on success, error, timeout, and cancellation. Metrics expose active, waiting, rejected, and wait duration.


### 6. Backpressure across stages


Backpressure communicates downstream limits upstream. For durable jobs:

```text
API admission
→ durable job depth budget
→ worker claim concurrency
→ storage publication capacity
→ webhook outbox/drain capacity
```

If artifact storage slows, workers may finish computation but block publication. Claiming more jobs increases memory and lease pressure. Worker claim rate should respond to active work and downstream capacity, not simply queue depth.

Backpressure does not require one protocol. It may be a bounded channel, semaphore, queue depth check, poll interval, or explicit rejection. Its semantics must be observable and race-safe.


### 7. Cancellation and committed work


A client disconnect before admission can cancel waiting. After a run submission transaction commits, disconnecting the HTTP request must not erase durable work. The API may stop waiting for a response, but the job remains.

For downloads, cancellation should stop storage reads and release stream permits promptly. For outbound webhook attempts, cancellation during process shutdown returns the claim safely according to lease semantics.

Define cancellation at each boundary. Treating one cancellation token as global can undo work that has already crossed a durable boundary.


### 8. Fairness and starvation


A global FIFO queue can be dominated by one tenant. Strict per-tenant queues can leave capacity idle. Fair scheduling combines a global resource cap with tenant or class limits and a deliberate ordering policy.

The capstone fair admission model uses global permits plus per-principal or per-tenant limits. It records rejection reason and remaining budget without exposing another tenant’s use.

Priority can be justified for operational control or critical journeys, but it can starve low-priority work. Every priority scheme needs starvation evidence and a maximum wait or aging policy.


### 9. Overload should be truthful


Overload is not an internal 500. The service should reject before partial effects and use documented 429 or 503 behavior according to policy. `Retry-After` must align with the system’s actual recovery model; a precise value invented without capacity evidence can amplify retries.

Accepted `202` work counts against durable queue capacity. It is dishonest to accept unlimited jobs and later miss every freshness objective. Admission ties API behavior to worker capacity and capacity planning.

Course 3 abuse controls and Course 4 reliability alerts remain active. Performance controls refine their numerical budgets and fairness behavior.


## Course requirements

| Rule | Required behavior | Failure if omitted | Decisive evidence |
|---|---|---|---|
| Queue inventory complete | Every wait boundary has owner, capacity, timeout, cancellation, and metric. | Hidden unbounded queue absorbs overload. | Queue catalogue |
| Populations compatible | Little’s Law uses same work unit and interval. | Plausible arithmetic hides mismatched stages. | Model review |
| Admission bounded | Active and waiting work have explicit caps and deadlines. | Memory and latency grow without bound. | Concurrency tests |
| Permits always released | All terminal paths release capacity exactly once. | Capacity leaks after errors/cancellation. | State-machine tests |
| Durable boundary respected | Client cancellation cannot roll back committed job intent. | Accepted work disappears. | Restart/cancellation proof |
| Downstream-aware claims | Worker/outbound concurrency respects downstream capacity. | Queue is drained into a slower resource. | Mixed fault test |
| Fairness explicit | Global and tenant/class limits prevent monopoly and starvation. | One tenant consumes service. | Mixed-tenant test |
| Overload documented | Rejection is observable and preserves response contract. | 500s or timeouts replace explicit policy. | Conformance and traffic report |

## Worked failures

### Case 1 — The unbounded semaphore wait

**Initial condition.** Requests wait indefinitely for a database permit. Error rate is low, but p99 climbs to minutes.

**Analysis.** The queue hides overload and consumes sockets/memory. Low errors do not mean acceptable service.

**Correct response.** Bound waiters and acquisition time; reject with documented overload and protect admitted work.

**Lesson.** Queueing delay is a resource and a failure mode.

### Case 2 — The worker concurrency increase

**Initial condition.** Queue depth rises, so worker concurrency doubles. Artifact storage is already saturated.

**Analysis.** More jobs leave the durable queue and pile up at storage, increasing lease renewals and memory.

**Correct response.** Limit claims by downstream publication capacity and improve or scale the actual bottleneck.

**Lesson.** Draining one queue can overload the next stage.

### Case 3 — The cancellation rollback

**Initial condition.** A client disconnects after the submission transaction commits; handler cancellation deletes the job.

**Analysis.** The durable acceptance boundary was crossed. Deletion violates `202 Accepted` semantics and idempotent replay.

**Correct response.** Release HTTP resources but preserve run/job state; expose status through monitor resource.

**Lesson.** Cancellation scope ends at durable commitment.

### Case 4 — The noisy tenant

**Initial condition.** One tenant submits 90% of jobs and consumes all worker permits. Other tenants time out.

**Analysis.** Global concurrency alone provides no fairness.

**Correct response.** Combine global capacity with tenant limits or fair scheduling; measure wait and starvation.

**Lesson.** Capacity and fairness are separate properties.

## Python implementation

### Mechanism

The Python queueing module implements Little’s Law checks, bounded async admission, fair per-key permits, and a queue-state snapshot. It uses injected clocks for deterministic tests.

### Repository paths

- `capstone/tracks/python-fastapi/src/api_performance/queueing.py`
- `capstone/tracks/python-fastapi/src/api_performance/admission.py`
- `capstone/tracks/python-fastapi/tests_performance/test_queueing_admission.py`

### Focused example

```python
from api_performance.queueing import little_law

model = little_law(throughput_per_second=20.0, mean_time_seconds=5.0)
assert model.mean_in_system == 100.0
```

The model validates non-negative finite inputs and labels the work unit. The admission controller has a bounded waiter count and acquisition deadline; context-manager exit releases exactly once.

### Python-specific failure to avoid

`asyncio.Semaphore` alone does not bound the number of waiting tasks. Wrap it with an explicit waiter cap and timeout, and handle `CancelledError` without leaking a permit.

## TypeScript implementation

### Mechanism

The TypeScript implementation uses an abort-aware permit queue with global and key-specific limits. All resolution paths remove waiters and release permits once.

### Repository paths

- `capstone/tracks/typescript-fastify/src/performance/queueing.ts`
- `capstone/tracks/typescript-fastify/src/performance/admission.ts`
- `capstone/tracks/typescript-fastify/test-performance-core/queueing-admission.test.mjs`

### Focused example

```typescript
const model = littleLaw({
  throughputPerSecond: 20,
  meanTimeSeconds: 5,
  unit: "analysis-jobs",
});
if (model.meanInSystem !== 100) throw new Error("bad Little's Law");
```

The permit queue accepts an `AbortSignal`, removes aborted waiters, and checks invariants after every transition. Tests cover simultaneous release, timeout, and cancellation.

### TypeScript-specific failure to avoid

A pending promise retained in an array is still memory. Remove settled/aborted waiters and avoid resolving the same waiter from both timeout and release callbacks.

## Cross-language invariant

Both tracks agree on queue arithmetic, admission decisions, rejection reasons, fairness order for deterministic vectors, and capacity snapshots.

## Failure patterns

- **Queue invisibility.** Waiting occurs in runtime or pool without metrics. **Decisive check:** queue inventory and wait timer.
- **Little’s Law mismatch.** Arrival, work-in-system, and duration use different populations. **Decisive check:** unit/interval labels.
- **Waiter leak.** Cancelled tasks remain queued. **Decisive check:** terminal-path invariant.
- **Downstream blindness.** Concurrency is raised at upstream stage only. **Decisive check:** stage utilization map.
- **Fairness assumption.** FIFO global queue is called fair. **Decisive check:** tenant wait/rejection distribution.
- **Fake Retry-After.** Precise retry delay has no recovery basis. **Decisive check:** retry policy and queue model.

## Evidence and design review

Before accepting the module increment, answer:

1. Where can work wait in the complete journey?
2. Which queue grows first at the tested arrival rate?
3. Are service and waiting time measured separately?
4. What is the maximum memory/work implied by every queue cap?
5. How does cancellation behave before and after durable commit?
6. Can one tenant monopolize permits or queue positions?

## Module synthesis

Queueing turns excess demand into waiting. Module 6 makes every queue explicit, bounds waiting and active work, preserves durable cancellation semantics, and connects concurrency to the actual limiting resource.

Proceed to [Exercises](exercises.md), then complete the [Lab](lab.md) and [Checkpoint](checkpoint.md).

## Next in the story

The next module, **Caching, Freshness, and Invalidation**, asks: Which data is safe to cache, for whom, for how long, and who owns invalidation after mutation or failure? It builds on the evidence produced here rather than reopening this module's decisions.
