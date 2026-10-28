---
module_id: SEPAT-067
program: Software Engineering: Patterns
level: 2
module_number: 67
title: Competing Consumers
status: complete
last_verified: 2026-08-29
---

# Competing Consumers

## One-Page Review

### Governing question

How can several replaceable workers share one logical stream of work to increase throughput and availability while preserving bounded concurrency, scoped ordering, recoverable ownership, effect idempotency, fairness, security, and an auditable terminal outcome for every message?

### Essential definitions

- **Competing Consumers** are multiple consumer instances eligible to process work from one logical point-to-point channel or subscription; one delivery attempt is assigned to one instance.
- A **logical subscription** is the business obligation and progress state shared by the workers. Adding a worker scales that obligation; adding another subscription creates another obligation.
- An **in-flight delivery** has been assigned but has not reached a broker-recognized terminal state.
- An **acknowledgement** transfers or confirms responsibility after the consumer has satisfied its processing contract; an automatic acknowledgement may occur too early for durable effects.
- A **lease** or **visibility timeout** grants temporary processing ownership. Expiry makes unfinished work eligible for another attempt.
- A **delivery attempt** is not a business effect. A crash after effect commit but before acknowledgement can produce several attempts for one intended effect.
- **prefetch** bounds messages delivered but unacknowledged to a consumer; it changes throughput, memory, fairness, and failure blast radius.
- A **partition** or **message group** is an ordering and parallelism unit. It can preserve per-key order while preventing arbitrary workers from sharing a hot unit.
- A **fencing token** is a monotonically increasing claim generation checked by the effect store so an expired worker cannot commit after a successor.
- A **terminal outcome** is acknowledged success, explicit cancellation/expiry, or owned quarantine/dead-letter disposition—not disappearance from a dashboard.

### Central model, mechanism, or theorem

For arrival rate $\lambda$, $k$ homogeneous consumers, and mean service rate $\mu$ per consumer, an idealized queue is stable only if

$$
\lambda < k\mu.
$$

Real capacity is bounded by broker partitions, serial work, and downstream capacity $C_d$:

$$
C_{effective}\le \min(k\mu,\;p\mu_p,\;C_d).
$$

If fraction $f$ is inherently serial, Amdahl's bound gives

$$
S(k)\le\frac{1}{f+(1-f)/k}.
$$

For message $m$, at-least-once recovery permits delivery attempts $D_m\ge1$, while the business contract may require committed effect $E_m=1$. Stable message/operation identity, an atomic idempotency boundary, and—when leases can overlap—a current fencing generation establish the latter; the queue alone does not.

### Critical invariants

- All workers share one named logical responsibility, schema contract, authorization policy, retry policy, and terminal-outcome ledger.
- A message is acknowledged only after its required durable effect and any outgoing work are safely recorded, or after a documented atomic broker transaction covers them.
- Every effect is idempotent by stable message and operation identity; a delivery tag, receipt handle, process ID, or worker name is not that identity.
- In-flight work is bounded per worker and globally against memory, downstream connections, quotas, and failure recovery capacity.
- Lease renewal proves liveness, not exclusive authority; effect commits reject stale generations or conflicting entity versions.
- Ordering claims identify their key/partition scope. Concurrency never implies global completion order.
- Retry is bounded, classified, delayed, and observable; poison work cannot consume all workers indefinitely.
- Scaling decisions incorporate oldest age, arrival and service rates, skew, downstream saturation, and cost—not queue depth alone.
- Deployment drains/cancels workers deliberately while accounting for deliveries already in flight and possible rebalances.
- Every message reaches an auditable terminal outcome without weakening tenant, purpose, or current-authority checks on retry.

### Common failures

Common failures include confusing another worker with another subscriber, scaling past partition or database capacity, acknowledging before effect commit, treating at-least-once delivery as exactly-once effects, using unbounded prefetch, assuming round-robin is fair under unequal service times, setting leases below tail latency, accepting stale completions, preserving queue order while effects finish out of order, partitioning on a hot key, retrying permanent errors immediately, letting poison messages monopolize the pool, autoscaling into downstream collapse, counting only depth, losing work during abrupt deployment, mixing incompatible worker versions, sharing overpowered credentials, and deleting or dead-lettering work merely to restore a green metric.

### Compact example

Worker A claims `job-1` with generation 1, performs slowly, and loses its lease. Worker B claims the same stable job with generation 2. A's late completion is rejected because generation 1 is stale; B commits the idempotent effect and acknowledges. There were two delivery attempts but one accepted effect. The lease recovered availability, while the effect store—not elapsed time—preserved correctness.

### Connections

[SEPAT-066](066-publish-subscribe-channel.md) distinguishes subscriptions from the workers inside one subscription; [SEPAT-068](../ROADMAP.md) develops the Message Dispatcher that can assign work explicitly. Competing consumers also connects to [Database Engineering](../../18-database-engineering/ROADMAP.md), [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md), [Security Engineering](../../25-security-engineering/ROADMAP.md), [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md), and [Platform Engineering](../../29-platform-engineering/ROADMAP.md).

## Governing Question

When demand exceeds one consumer's safe service rate, how should multiple workers share one obligation so that additional concurrency improves useful throughput without converting failures, retries, skew, or overload into duplicate effects and invisible loss?

The decisive word is *one*. Competing Consumers scales one logical responsibility. The workers may be processes, threads, containers, machines, or functions, but they do not each own a copy of every message. Product APIs differ: a broker queue may dispatch individual messages, a log consumer group may assign partitions, and a leased work service may return receipt handles. The design must state which resource owns progress and what failure makes work eligible again.

## Why This Matters

A single consumer creates a throughput ceiling and a recovery dependency. A pool can process independent jobs concurrently, survive instance loss, and scale with demand. The pattern is therefore central to payment posting, media transformation, indexing, notification preparation, batch imports, and background workflow steps.

Concurrency also multiplies uncertainty. Two attempts can overlap after a lost acknowledgement or expired lease. Ten workers can overload a database that one worker never stressed. A single hot partition can remain late while the aggregate queue appears healthy. Faster completion can violate entity order, and a rolling deployment can combine code versions against the same data. Production quality comes from explicitly governing these effects, not from increasing replica count.

## Prerequisites and Retrieval

You should understand point-to-point and publish-subscribe channels, acknowledgements, idempotency, transactions, queueing basics, partitions, optimistic concurrency, backpressure, schemas, retry, authorization, and observability. Retrieve these facts:

1. Worker instances in one group compete; independent groups each own a logical delivery stream.
2. Broker delivery and acknowledgement delimit transport responsibility, not necessarily the transaction boundary of a database or remote effect.
3. Failure after an effect but before acknowledgement produces a valid reason for redelivery.
4. Queue order does not guarantee concurrent completion order.
5. A timeout indicates missing timely evidence; it does not prove the former worker stopped.
6. Parallel capacity is limited by serial sections, partition count, skew, downstream capacity, and coordination overhead.
7. Depth, lag, and oldest age describe different operational risks.

## Learning Objectives

After completing this module, you should be able to:

- distinguish competing consumers from pub/sub, exclusive consumers, dispatchers, and independent subscriptions;
- model arrivals, service, utilization, in-flight work, attempts, effects, leases, and terminal outcomes;
- derive useful capacity bounds and explain why replica count alone is insufficient;
- choose push/pull, prefetch, batch size, concurrency, lease, heartbeat, and acknowledgement policies;
- design idempotency and fencing boundaries that tolerate redelivery and overlapping attempts;
- preserve required per-key ordering without claiming global order;
- govern retry, poison work, dead letters, cancellation, deployment draining, and reconciliation;
- scale from age/lag and measured service capacity without overwhelming downstream systems;
- secure shared work by workload identity, tenant/purpose checks, least privilege, and current authorization;
- test the design through crash points, expired leases, rebalances, skew, overload, incompatible versions, and recovery.

## Core Exposition

### Name the shared obligation

Start with a business responsibility: `post-authorized-payment`, `render-upload`, or `index-catalog-change`. Bind it to one queue or group, owner, input contract, effect, service objective, authorization policy, retry policy, and terminal-outcome policy. Deployment replicas are implementation members, not new responsibilities.

This naming prevents a common topology error. Two consumer groups attached to a topic normally mean two independently progressing subscribers; each record may be processed once per group. Two members inside one group share that group's records. A queue with two competing endpoints is likewise one work stream. The exact broker language matters less than documenting this cardinality.

### Establish the assignment mechanism

In broker-push systems, the broker selects an eligible consumer and may distribute deliveries roughly round-robin, subject to credit, priority, locality, and availability. In pull systems, workers request work when ready. In partitioned logs, a group coordinator assigns partitions to members, so competition is mediated by partition ownership rather than per-record races.

Assignment is temporary responsibility, not proof of completion. Record stable message ID, logical operation, group/subscription, partition/key, attempt, assignment/lease generation, worker identity, code/schema version, start time, and trace context. Do not use mutable delivery handles as business deduplication keys.

### Separate delivery attempts from effects

Suppose the consumer writes a charge ledger row and then crashes before acknowledgement. Redelivery is correct because the broker lacks proof. Repeating the charge is not correct. The effect boundary should claim a stable key such as `(subscription_id, message_id, operation)` in the same transaction as the effect, or apply an entity transition conditional on the expected version.

If an external service is involved, pass a stable idempotency key when supported and reconcile ambiguous results. If it is not supported, introduce a durable workflow with explicit state rather than pretending the queue makes the remote call exactly once.

### Acknowledge at the semantic boundary

Automatic acknowledgement on receipt maximizes apparent throughput but can lose work if the process fails before the effect. Manual acknowledgement after a durable local transaction supports recovery. When the effect, outgoing publication, and input checkpoint span systems, use an inbox/outbox, product-specific transaction within its stated scope, or reconciliation.

Batch acknowledgements amortize overhead but increase the ambiguity and redelivery set after failure. Acknowledgement ordering rules are broker-specific; review whether one cumulative acknowledgement can accidentally confirm work still running concurrently.

### Bound in-flight work

Prefetch or receive batch size controls how many messages become assigned but unfinished. Too little wastes bandwidth and worker capacity; too much hoards work on slow instances, consumes memory, increases lease churn, and enlarges the set redelivered after a crash.

Choose a bound from measured service-time distribution, memory per job, downstream connection limits, acknowledgement latency, and desired fairness. Apply both per-worker and group/global admission limits where needed. A worker can internally process several jobs, but that concurrency must remain below the weakest downstream quota.

### Treat leases as recoverability, not locks

A visibility timeout hides work for a period. If the worker fails to finish and acknowledge/delete, the job becomes eligible again. Long work may renew the lease with heartbeat. A long lease slows recovery; a short lease creates overlap under legitimate tail latency, pauses, or partitions.

An expired worker may still be alive and able to write. Therefore a lease alone cannot protect a non-idempotent effect. Allocate an increasing generation when ownership changes and require the state store to accept a completion only if its generation is current. Optimistic entity versions can provide a related fence. Heartbeats extend availability evidence but cannot establish uniqueness across an asynchronous network.

### Understand capacity and stability

For homogeneous independent jobs, $k\mu$ is an optimistic service bound. Sustainable operation needs headroom: at utilization near one, latency and backlog become highly sensitive to variability. Account for arrival bursts, tail service times, retry amplification, maintenance, and degraded workers.

Downstream capacity often binds first. If each job holds one database connection for 200 ms and only 50 connections are safely available, the effect tier caps near 250 jobs/s even if worker CPU capacity is 1,000 jobs/s. Scaling workers beyond that point increases contention and timeouts, which generate retries and reduce useful throughput.

### Partition for order and locality

Concurrent queue consumers can receive messages in queue order yet complete effects in another order. If transitions for one entity require order, route that entity key to one partition/message group and process it serially or use version checks that detect gaps and conflicts.

Partitions cap parallelism: traditional consumer-group membership beyond partition count may be idle. Skew matters more than count; a celebrity tenant or default key can overload one partition. Choose a stable, sufficiently dispersed key while honoring semantic serialization. Repartitioning changes mapping and requires a migration protocol if order crosses old/new partitions.

### Design retry as admission control

Classify transient infrastructure failure, throttling, optimistic conflict, malformed input, unsupported schema, unauthorized request, expired work, and permanent domain rejection. Immediate requeue can create a tight loop in which poison work consumes every worker. Use bounded attempts, exponential backoff with jitter, retry deadlines, separate delayed tiers where appropriate, and a quarantine/dead-letter destination with owner and evidence.

Redrive retains stable identity and rechecks current applicability and authorization. It is a controlled new attempt, not a way to erase an incident. Fairness controls should prevent one tenant, key, or poison family from occupying the pool.

### Autoscale on useful signals

Queue depth alone ignores arrival rate, job duration, skew, in-flight work, and business urgency. Combine oldest unfinished age, lag/depth, arrival and completion rates, service-time quantiles, utilization, partition skew, retry amplification, and downstream saturation. Scale down slowly enough to drain leases and avoid oscillation.

Set a maximum concurrency derived from downstream budgets. If the database is saturated, adding workers is harmful; throttle intake or shed only work whose contract explicitly permits it. Capacity tests should include catch-up after outage, not only steady state.

### Deploy and rebalance deliberately

On shutdown, stop accepting assignments, finish or explicitly abandon in-flight work, acknowledge only completed effects, and expose drain progress. A cancelled consumer may still hold previously delivered messages depending on the broker. A forced termination must be expected to cause redelivery.

Partitioned groups rebalance when membership changes. Pause new work, commit/checkpoint at the documented boundary, revoke ownership, and fence late writes. Rolling versions must share compatible message and state schemas and the same idempotency semantics. If that cannot be guaranteed, drain the old population before activating the new one.

### Secure every attempt

Give each workload a verifiable identity and least-privilege consume/ack permissions for its group and tenant scope. Shared long-lived credentials make attribution and revocation weak. Validate signed/provenance metadata and message schema before using payload fields for authorization decisions.

Authorization can change while work waits or retries. High-impact work should recheck current account, consent, sanctions, clinical status, or tenancy at effect time. Protect queue administration, redrive, dead-letter content, traces, and metrics; these surfaces often expose sensitive payload or enable replayed authority.

### Observe obligations, not just processes

Measure queued/ready depth, oldest age, in-flight count, arrival/completion/useful-effect rate, service and queueing latency, acknowledgement latency, redelivery, lease expiry/renewal, deduplication hit, stale-fence rejection, retry class, dead-letter age, per-key/tenant skew, worker version, downstream saturation, and autoscaling decisions.

Trace one stable message across attempts and effect identity without placing secrets in labels. Reconcile broker terminal state against the effect ledger. “All workers healthy” does not show that old work is progressing; “queue empty” may mean premature acknowledgement or unauthorized deletion.

## Definitions and Notation

| Symbol or term | Meaning |
| --- | --- |
| $\lambda$ | Mean arrival rate into the logical subscription |
| $k$ | Number of eligible consumer instances |
| $\mu_i$ | Mean service rate of consumer $i$ under stated workload |
| $p$ | Number of independently assignable partitions/groups |
| $C_d$ | Safe downstream effect capacity |
| $U$ | Utilization; idealized as $\lambda/\sum_i\mu_i$ |
| $D_m$ | Number of delivery attempts for message $m$ |
| $E_{m,o}$ | Accepted effects for message $m$, operation $o$ |
| $g$ | Monotone ownership/lease generation used as a fence |
| in-flight | Assigned but not terminally acknowledged/deleted work |
| prefetch/credit | Maximum deliveries made available ahead of acknowledgement |
| lease | Time-bounded processing claim whose expiry enables recovery |
| poison message | Work that predictably fails ordinary processing and retry |
| hot key | Key whose rate/cost dominates its partition or fairness share |

The simple $M/M/k$-like capacity notation is a model, not a product guarantee. It assumes stationary arrivals, independent homogeneous service, no retry amplification, and no external bottleneck. Measurements from a real workload are empirical evidence and must report distributions and conditions.

## Mechanisms, Invariants, or Proof Structure

### Safety argument for one accepted effect

Assume every logical operation has stable key $q=(subscription,m,o)$. The effect store atomically enforces either a unique committed row for $q$, or a conditional state transition from the expected entity version. Any number of attempts can race; at most one commits the guarded effect. Completed retries observe the prior result. Thus $E_{m,o}\le1$. If policy and recovery ensure some valid attempt eventually executes and the store remains available, then $E_{m,o}\ge1$, giving $E_{m,o}=1$. The liveness premise is separate from safety.

### Fencing argument for expired ownership

Each reassignment allocates a larger generation $g$. The effect store records the current generation and accepts a completion only when the presented generation equals it. If worker A holds $g=1$, expires, and worker B receives $g=2$, A's late write fails the predicate. This protects guarded effects even though the workers overlap. The proof does not cover an unguarded external side effect; that needs its own idempotency/fencing protocol.

### Capacity bound

No pool can complete faster than aggregate worker service, assignable partitions, or downstream effects. Therefore the minimum of those capacities is an upper bound. A serial fraction yields Amdahl's stricter speedup bound. Queue stability requires sustainable useful completion above arrivals, including retry load and safety headroom. These are algebraic bounds, not latency predictions.

### Executable finite-state model

The following deterministic model reassigns an expired job with a higher token. It rejects the stale completion and admits one current effect. It abstracts durable storage, clocks, broker replication, concurrent races, and external I/O; those require integration and fault-injection tests.

<!-- bijux-verify: {"id":"competing-consumers-fencing","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"worker-a claimed=job-1 token=1 attempt=1\nworker-b claimed=job-1 token=2 attempt=2\nstale=rejected current=accepted effects=1\nworker-a claimed=job-2 token=1 effects=2 queued=0 in_flight=0\n","stderr":""}} -->
```python
class WorkQueue:
    def __init__(self, jobs):
        self.ready = list(jobs)
        self.in_flight = {}
        self.generations = {}
        self.attempts = {}

    def claim(self, worker):
        job = self.ready.pop(0)
        job_id = job["id"]
        token = self.generations.get(job_id, 0) + 1
        self.generations[job_id] = token
        self.attempts[job_id] = self.attempts.get(job_id, 0) + 1
        self.in_flight[job_id] = {"job": job, "worker": worker, "token": token}
        return job, token, self.attempts[job_id]

    def expire(self, job_id):
        claim = self.in_flight.pop(job_id)
        self.ready.insert(0, claim["job"])

    def complete(self, job_id, worker, token, effects):
        claim = self.in_flight.get(job_id)
        if claim is None or claim["worker"] != worker or claim["token"] != token:
            return "rejected"
        effects.add((job_id, "apply"))
        self.in_flight.pop(job_id)
        return "accepted"


queue = WorkQueue([{"id": "job-1"}, {"id": "job-2"}])
effects = set()

job, token_a, attempt = queue.claim("worker-a")
print(f"worker-a claimed={job['id']} token={token_a} attempt={attempt}")
queue.expire(job["id"])

job, token_b, attempt = queue.claim("worker-b")
print(f"worker-b claimed={job['id']} token={token_b} attempt={attempt}")
stale = queue.complete(job["id"], "worker-a", token_a, effects)
current = queue.complete(job["id"], "worker-b", token_b, effects)
print(f"stale={stale} current={current} effects={len(effects)}")

job, token, _ = queue.claim("worker-a")
queue.complete(job["id"], "worker-a", token, effects)
print(
    f"worker-a claimed={job['id']} token={token} effects={len(effects)} "
    f"queued={len(queue.ready)} in_flight={len(queue.in_flight)}"
)
```

## Alternatives and Trade-Offs

| Design | Advantage | Cost or limitation | Best fit |
| --- | --- | --- | --- |
| Single/exclusive consumer | Simple order and low coordination | Throughput and availability ceiling | Low-rate globally serialized work |
| Broker-dispatched competing consumers | Fine-grained balancing across ready workers | Completion order and lease overlap need control | Independent jobs with queue semantics |
| Partitioned consumer group | Per-partition order and scalable replay | Parallelism capped by partitions; hot-key skew | Keyed event streams |
| Explicit Message Dispatcher | Capability/priority-aware assignment | Dispatcher state and availability become critical | Heterogeneous workers or special scheduling |
| Database work claiming | Transactional proximity to state | Polling/lock contention and weak broker features | Moderate internal workloads already bound to one database |
| Static sharding | Predictable ownership/locality | Rebalancing and failed-shard recovery are operational work | Stable keys and long-lived locality |
| Serverless queue trigger | Rapid elastic operation | Platform concurrency, lease, cost, and runtime limits | Bursty bounded-duration jobs |
| Workflow engine | Durable multi-step state, timers, cancellation | Higher semantic and operational complexity | Long-running coordinated work, not one atomic job |

Push delivery reduces polling latency but needs credit/backpressure. Pull lets workers request at their pace but can add polling overhead and unfairness. Large batches amortize calls but increase latency, hoarding, and ambiguous retry sets. Priority queues serve urgent work but can starve ordinary work; separate capacity reservations or aging may be safer.

## Failure Modes and Misconceptions

- **“Each consumer receives each message.”** That describes separate pub/sub subscriptions, not competition within one logical stream.
- **“The broker guarantees exactly once.”** Transport features cannot generally make arbitrary database, payment, email, or HTTP effects unique.
- **“More replicas always increase throughput.”** Partitions, serial fractions, downstream quotas, contention, and skew impose hard or practical ceilings.
- **“Round-robin means equal work.”** It may equalize deliveries, not service cost; prefetch can let a slow worker hoard expensive jobs.
- **“A lease prevents overlap.”** Expiry and network delay can leave the former worker running; fence or deduplicate effects.
- **“Queue FIFO means effects are FIFO.”** Concurrent service, retry, and variable duration reorder completion.
- **“A long visibility timeout is safer.”** It reduces premature overlap but delays recovery and keeps work in flight longer.
- **“Immediate retry is resilient.”** It can create a redelivery loop and crowd out healthy work.
- **“Depth is the autoscaling target.”** Oldest age, rate, service time, partition skew, retry amplification, and downstream health are also required.
- **“A healthy worker pool means healthy processing.”** Workers may acknowledge early, loop on poison work, or make no useful effects.
- **“Scale-to-zero is free.”** Cold starts can violate latency, cause lease expiry, and increase burst concurrency downstream.
- **“Killing a pod returns all work instantly.”** Failure detection and lease/connection expiry take time; already committed effects may still lack acknowledgement.
- **“All workers can deploy independently.”** Concurrent versions must share schema, state-transition, and idempotency compatibility.
- **“Dead-lettering completes the business obligation.”** It creates an owned unresolved outcome unless policy explicitly permits abandonment.
- **“One shared credential is operationally simpler.”** It weakens attribution, tenant isolation, rotation, and revocation.

## Worked Examples

### Example 1

**Situation.** A render queue receives $\lambda=180$ jobs/s. One worker completes $\mu=30$ jobs/s; downstream storage safely accepts 240 results/s. How many workers are minimally stable in the idealized model?

**Reasoning.** Stability requires $180<30k$, so $k>6$. Six workers equal arrivals and provide no headroom; seven provide ideal capacity 210 jobs/s, below the downstream bound. Tail latency, maintenance, and retries require measured additional headroom.

**Conclusion.** Seven is the mathematical minimum under the assumptions, not a production sizing recommendation; validate a larger bounded pool empirically.

### Example 2

**Situation.** Billing and search must both react to `OrderPlaced`. Each has four replicas. Is this eight competing consumers on one obligation?

**Reasoning.** Billing and search have different effects, owners, progress, retry, and terminal outcomes, so they are two logical subscriptions. Four billing replicas compete within billing; four search replicas compete within search. A billing acknowledgement cannot satisfy search.

**Conclusion.** Subscriber cardinality is two and worker cardinality is eight; model two obligations, each with four competitors.

### Example 3

**Situation.** Worker A inserts invoice `inv-9`, commits, and crashes before acknowledging message `m-9`. Worker B receives `m-9`.

**Reasoning.** Redelivery is required because the broker did not observe completion. If the database transaction uniquely claims `(invoice-subscription,m-9,create-invoice)`, B finds the completed claim and acknowledges without inserting again. A worker-specific receipt would not match the second attempt.

**Conclusion.** Stable operation identity makes at-least-once delivery compatible with one invoice effect.

### Example 4

**Situation.** Two workers have prefetch 50. A becomes slow after receiving 50 large media jobs while B finishes its small jobs and goes idle.

**Reasoning.** Delivery counts were initially balanced, but assigned work cannot immediately migrate while it remains in flight. Lower prefetch or pull-on-capacity improves fairness, at the cost of more delivery round trips. Cost-aware queues or dispatching may be needed when job sizes vary greatly.

**Conclusion.** Tune credit from service distribution and fairness, not from average throughput alone.

### Example 5

**Situation.** A 60-second job has a 45-second lease. Worker A pauses, the lease expires, and B receives generation 12 while A resumes with generation 11.

**Reasoning.** Both workers can now run. Lease renewal may reduce overlap but cannot retract B's valid claim. The effect store compares the presented generation with current generation 12: A is rejected; B may commit. If the external effect cannot check a token, it needs stable idempotency or a compensating workflow.

**Conclusion.** A lease recovers work; fencing decides which overlapping owner may mutate guarded state.

### Example 6

**Situation.** A topic has 12 partitions and 20 consumer-group members. Forty percent of traffic uses tenant key `global`.

**Reasoning.** At most 12 traditional group members can own partitions concurrently, leaving eight without partition work. The `global` key maps to one partition, which receives at least 40% of traffic and bounds overall age. Adding members cannot split that key while preserving its partition order.

**Conclusion.** Fix key semantics or shard the hot logical stream with an ordering strategy; replicas alone cannot solve the bottleneck.

### Example 7

**Situation.** Queue age rises, so autoscaling grows from 20 to 200 workers. Database connection saturation causes timeouts, which are retried.

**Reasoning.** Worker capacity rose above downstream capacity. Timeouts amplify arrivals, hold leases longer, and reduce useful completions, a positive feedback loop. Cap concurrency by database budget, back off retries, and scale only while useful throughput improves.

**Conclusion.** Autoscaling must be constrained by the effect tier and measured in accepted effects, not process count.

### Example 8

**Situation.** One malformed message is immediately requeued. Eight workers repeatedly receive it while normal messages age.

**Reasoning.** The error is deterministic, so immediate retry offers no new condition. Track attempts/error class, quarantine after a small bound, preserve payload/provenance securely, alert the owner, and continue healthy work. Redrive only after parser or data remediation and under the same stable identity.

**Conclusion.** Bounded quarantine preserves pool capacity while retaining an auditable unresolved obligation.

### Example 9

**Situation.** Version A interprets missing `currency` as USD; version B rejects missing currency. Both run during a rolling deployment.

**Reasoning.** Assignment timing now changes semantics. Either make both versions accept the same contract during the overlap, translate at a governed boundary, or drain A before activating B. Idempotency results must remain readable across versions, and retry must not change meaning.

**Conclusion.** A competing pool needs a deployment compatibility contract, not merely individually healthy binaries.

### Example 10

**Situation.** Workers process clinical follow-up jobs. A job was authorized yesterday, but the patient withdrew consent while it waited; a worker now claims it.

**Reasoning.** Queue possession proves neither current consent nor clinical applicability. Before effect, validate patient identity, current consent, order/version, practitioner authority, and expiry. Record an auditable cancellation outcome rather than contacting the patient. Redelivery repeats the current-state check.

**Conclusion.** High-stakes consumers treat the message as a request for reevaluation under current authority, not as timeless authorization.

## Cross-Program Connections

- [Database Engineering](../../18-database-engineering/ROADMAP.md): unique claims, conditional updates, transactions, connection budgets, and hot rows establish the effect boundary.
- [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md): crash-point tests, model-based schedules, duplicate injection, lease expiry, and invariant oracles expose concurrency defects.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): workload identity, tenant isolation, current authorization, redrive controls, and protected dead letters constrain shared workers.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): leases, failure detection, fencing, partitions, retries, and ambiguous outcomes explain why overlap is unavoidable.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): autoscaling, deployment draining, quotas, observability, and capacity governance make the pool operable.
- [SEPAT-066](066-publish-subscribe-channel.md) supplies the logical-subscription boundary; [SEPAT-068](../ROADMAP.md) adds explicit dispatch policy when eligibility is heterogeneous.

## References

1. Hohpe, Gregor, and Bobby Woolf. *Enterprise Integration Patterns*. Addison-Wesley, 2003. Competing Consumers, Idempotent Receiver, Transactional Client, and related messaging patterns.
2. Hohpe, Gregor. “Competing Consumers.” *Enterprise Integration Patterns* website, copyright 2003–2023. <https://www.enterpriseintegrationpatterns.com/patterns/messaging/CompetingConsumers.html>. Accessed 2026-08-29.
3. RabbitMQ. “Consumers.” Current documentation. <https://www.rabbitmq.com/docs/consumers>. Accessed 2026-08-29.
4. RabbitMQ. “Consumer Acknowledgements and Publisher Confirms.” Current documentation. <https://www.rabbitmq.com/docs/confirms>. Accessed 2026-08-29.
5. RabbitMQ. “Consumer Prefetch,” version 4.3 documentation. <https://www.rabbitmq.com/docs/consumer-prefetch>. Accessed 2026-08-29.
6. Apache Kafka. “Introduction” and “Design,” current 4.3 documentation. <https://kafka.apache.org/documentation/> and <https://kafka.apache.org/design/>. Accessed 2026-08-29.
7. Amazon Web Services. “Amazon SQS visibility timeout.” *Amazon Simple Queue Service Developer Guide*. <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html>. Accessed 2026-08-29.
8. Amazon Web Services. “FIFO queue delivery logic in Amazon SQS.” *Amazon Simple Queue Service Developer Guide*. <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-understanding-logic.html>. Accessed 2026-08-29.
9. Kleppmann, Martin. *Designing Data-Intensive Applications*. O'Reilly, 2017. Chapters 8 and 11 on distributed-system faults and stream processing.
10. Harchol-Balter, Mor. *Performance Modeling and Design of Computer Systems*. Cambridge University Press, 2013. Queueing, scheduling, variability, and capacity foundations.
11. Goetz, Brian, et al. *Java Concurrency in Practice*. Addison-Wesley, 2006. Task execution, cancellation, sizing, and liveness foundations.
12. Gray, Jim, and Andreas Reuter. *Transaction Processing: Concepts and Techniques*. Morgan Kaufmann, 1992. Recovery, idempotence, and transaction-processing foundations.

Product behavior changes across versions and configurations. The RabbitMQ, Kafka, and Amazon SQS claims above were checked against official documentation on 2026-08-29; deployments must verify the exact service version, queue type, client, and settings they operate.

## Exercises

### Exercise 1

Define the difference among a logical subscription, a consumer instance, a delivery attempt, and a committed effect. Explain why four workers do not imply four effects.

### Exercise 2

A queue receives 320 jobs/s. Each worker can process 50 jobs/s, there are eight partitions, the downstream service permits 360 effects/s, and 20% of work is serial. Compute the ideal minimum worker count for stability, the worker/partition/downstream capacity at eight workers, and Amdahl's maximum speedup at eight workers. State what the arithmetic cannot prove.

### Exercise 3

Design the processing transaction for `ReserveInventory(message_id, sku, quantity, expected_version)`. It must tolerate a crash after database commit but before acknowledgement and reject a stale leased worker. Specify keys, predicates, writes, acknowledgement point, and retry behavior.

### Exercise 4

A pool has 40 workers, prefetch 100, and a database limit of 80 safe concurrent effects. Oldest age grows while CPU is low; redeliveries and database timeouts spike during autoscaling. Diagnose the mechanism and propose configuration, telemetry, retry, and deployment tests.

### Exercise 5

Design a competing-consumer system for issuing time-sensitive medication reminders across tenants. Address ordering, current consent/clinical state, fairness, identity and authorization, leases, duplicate effects, poison messages, autoscaling, audit, and human escalation.

## Answers to the Exercises

### Answer 1

A logical subscription is one owned business obligation and its progress state. A consumer instance is a replaceable executor eligible for that obligation. A delivery attempt is one assignment of a message to an instance and can repeat after failure. A committed effect is the accepted business state change or external action. Four workers provide up to four-way execution concurrency; the broker assigns a given attempt to one worker, and stable idempotency/conditional state ensures all attempts for the same operation produce at most one accepted effect.

### Answer 2

Ideal stability requires $320<50k$, so $k>6.4$ and the minimum integer is seven. At eight workers, raw worker capacity is $8\times50=400$ jobs/s. Eight partitions do not reduce that bound if each can feed one worker at 50 jobs/s, but no ninth traditional group member could add partition parallelism. Downstream capacity reduces useful capacity to $\min(400,400,360)=360$ effects/s. With serial fraction $f=0.2$,

$$
S(8)\le\frac{1}{0.2+0.8/8}=\frac{1}{0.3}\approx3.33.
$$

The calculations do not prove stability under bursty arrivals, skew, heterogeneous service times, retries, coordination overhead, failures, or a particular latency SLO. Measurements and fault/load tests must validate headroom.

### Answer 3

Use stable operation key `(inventory-subscription,message_id,reserve)` and a monotone lease generation $g$. In one database transaction: authenticate/validate the message; read the current claim and SKU row; require presented $g$ to equal the current claim generation; insert the operation key if absent; require SKU version to equal `expected_version` and available quantity to cover the request; decrement quantity and advance version; record result and outgoing outbox event. A unique constraint prevents a second operation key, and conditional version/generation predicates reject stale workers. Commit, then acknowledge. After a crash before acknowledgement, retry reads the completed operation result and acknowledges without decrementing again. Conflicts, insufficient inventory, malformed input, and transient storage failure receive distinct terminal/retry policies.

### Answer 4

The pool can hold up to 4,000 unacknowledged deliveries and potentially drive far more than 80 concurrent effects. Scaling increases database contention; timeouts lengthen service, leases expire, redeliveries amplify demand, and CPU remains low because workers wait on I/O. Cap group effect concurrency at or below the database budget with headroom; substantially reduce prefetch based on job duration/memory; use backoff and bounded retry for throttling/timeouts; and stop scaling when downstream saturation rises without useful completions. Measure ready/in-flight/oldest age, service quantiles, useful effect rate, DB connections/latency, attempt classes, lease expiry, dedupe, and per-key skew. Test outage catch-up, slow queries, worker death at each transaction point, lease expiry, autoscale oscillation, drain, and rolling-version compatibility.

### Answer 5

Use one governed reminder obligation per appropriate tenant/security boundary, with stable reminder operation ID and partition/message group by patient or medication plan when per-patient order matters. Workers authenticate with individual workload identities and receive least-privilege tenant-scoped access. At effect time they recheck patient identity, current consent, active medication/order version, quiet-hour/expiry policy, and clinician authority; the queued payload is not timeless authorization. The delivery claim carries a monotone generation, while a transactional effect ledger uniquely records `(subscription,reminder_id,channel)` before an idempotent notification request. Expired workers are fenced and retries reuse the same operation identity.

Bound per-tenant concurrency and use fair scheduling so a large tenant cannot starve others. Set leases from service-time tails with heartbeat, but rely on fencing/idempotency for safety. Classify temporary channel failure separately from withdrawn consent, expired order, malformed data, and unsupported schema. Quarantine poison work with encrypted evidence, an owner, and clinically appropriate human escalation; never repeatedly notify. Autoscale from oldest clinically valid age, arrival/completion rate, tenant skew, and downstream notification/provider capacity. Audit attempts, current-state decisions, accepted effect, acknowledgement, cancellation, redrive, and human override without exposing health data in metric labels. Validate with duplicate/overlap, consent withdrawal during wait, hot tenant, provider outage, stale worker, clock boundary, poison payload, and disaster-recovery exercises before any safety claim.
