---
module_id: SARCH-057
program: Software Engineering: Software Architecture
level: 2
module_number: 57
title: Queue-Based Load Leveling
status: complete
last_verified: 2026-09-06
---

# Queue-Based Load Leveling

## One-Page Review

### Governing question

When can a bounded queue decouple arrival bursts from processing capacity without turning overload into hidden latency, stale work, duplicate effects, unfairness, or an unrecoverable backlog?

### Essential definitions

- A **queue** stores admitted work until a consumer can attempt it; admission is not business completion.
- **arrival rate** $\lambda$ is work arriving per unit time; **service rate** $\mu$ is completed attempts per unit time under stated conditions.
- **utilization** $\rho=\lambda/\mu$ in a one-server constant-rate abstraction; sustained $\rho\ge1$ has no stable finite backlog without shedding or changing rates.
- **queueing delay** is time waiting before service; **sojourn time** includes waiting and service.
- **backpressure** communicates reduced acceptance upstream; **load shedding** rejects or expires work deliberately to protect useful service.
- A **bounded queue** has an explicit item, byte, age, or cost limit; a nominal item limit alone may not bound memory or work.
- **visibility timeout** or **lease** temporarily grants delivery ownership; expiration may cause redelivery.
- A **dead-letter path** isolates repeatedly unprocessable items for owned diagnosis and repair; it is not a disposal bin.
- A **poison message** deterministically fails a consumer or invariant; a **retry storm** amplifies work through repeated attempts.
- **freshness budget** is the maximum age at which work remains useful or safe.

### Central model, mechanism, or theorem

For a stable system observed over a suitable interval, Little's law relates average number in system $L$, effective throughput $\lambda$, and average sojourn time $W$:

$$
L=\lambda W.
$$

It is an accounting relation under stability and consistent boundaries, not a latency guarantee. At effective throughput 200 jobs/s and average sojourn 5 s, average in-system work is 1,000 jobs.

If arrivals exceed service by $\lambda-\mu>0$ for duration $T$, a fluid approximation gives backlog growth $B=(\lambda-\mu)T$. After arrivals return to $\lambda_r<\mu$, ideal drain time is $B/(\mu-\lambda_r)$. Queueing moves work in time; it does not create processing capacity.

### Critical invariants

- an enqueue response states durable acceptance scope and never implies final business success;
- every work item has durable identity, authenticated origin, schema/version, priority, deadline or freshness policy, and terminal outcome;
- queue bounds cover count, bytes, age, cost, tenant, partition, and downstream amplification where relevant;
- admission occurs before irreversible overload and propagates honest backpressure;
- consumers preserve idempotent business effect or record deduplication and outcome durably;
- visibility timeout exceeds or renews around legitimate processing without hiding stuck work indefinitely;
- retry count, elapsed time, backoff, and fleet-wide amplification are bounded;
- poison items cannot block unrelated work, and dead-letter handling has ownership, authorization, and safe redrive;
- ordering is promised only within the actual partition, consumer, and retry semantics;
- priority cannot starve lower classes indefinitely unless policy explicitly permits it;
- backlog age and business deadline, not depth alone, determine urgency;
- scaling and drain models include downstream capacity and cold-start effects;
- recovery reconciles external effects and ambiguous acknowledgements;
- tests cover bursts, sustained overload, duplicates, expiry, poison, partition skew, dependency failure, and restoration.

### Common failures

Common failures include treating `202 Accepted` as completed; using an unbounded queue to “absorb” sustained overload; alerting only on depth; counting items without bytes or cost; retrying poison messages forever; setting a visibility timeout shorter than normal work and duplicating effects; claiming exactly-once business behavior from broker delivery; preserving FIFO globally across partitions; letting one tenant fill every partition; autoscaling consumers past database capacity; replaying expired notifications; starving bulk work behind an endless urgent stream or vice versa; deleting dead letters without domain review; and declaring recovery when the queue is empty but downstream effects disagree.

### Compact example

A processor serves 800 jobs/s. A two-minute burst arrives at 1,100 jobs/s, growing backlog by $(1{,}100-800)120=36{,}000$ jobs. After the burst, arrivals fall to 500 jobs/s, leaving 300 jobs/s drain capacity, so the ideal drain takes 120 seconds. If jobs expire after 90 seconds, capacity mathematics alone is insufficient: admission, priority, or shedding must protect useful outcomes.

### Connections

[SARCH-044](044-asynchronous-messaging-integration.md) supplies message semantics, [SARCH-051](051-partial-failure-as-an-architectural-constraint.md) supplies ambiguous outcomes, and [SARCH-056](056-cell-based-architecture.md) supplies isolation. [SARCH-058](../ROADMAP.md) next studies serverless and event-native systems. Data Engineering owns streaming engines; this module owns architectural load leveling and consequences.

## Governing Question

Direct synchronous work couples producer arrival to consumer capacity and latency. A queue can let producers finish admission quickly while consumers process at a sustainable rate. That temporal decoupling is valuable for bursts, maintenance, rate-limited dependencies, and independently scaled stages.

But a queue is stored demand. If demand exceeds capacity for too long, delay and storage grow. Work may become useless, unsafe, duplicated, or unfair before it is processed. Architecture must define admission, bounds, deadlines, identity, ordering, retries, and terminal outcomes, not simply insert a broker.

## Why This Matters

Queues often keep front doors responsive during incidents while moving failure out of immediate sight. Dashboards can show successful enqueue and healthy consumers even as customers wait hours, recalls arrive late, or retries amplify a failed dependency.

Correct queue-based leveling coordinates product semantics with capacity. Some work can wait; some should be rejected immediately; some must supersede older work; some must never execute after expiry. These policies determine whether the queue protects the system or accumulates liability.

## Prerequisites and Retrieval

Retrieve throughput, latency, percentile, capacity, arrival, service, utilization, burst, queue, partition, ordering, idempotency, deduplication, retry, backoff, visibility timeout, dead letter, backpressure, admission, load shedding, deadline, freshness, priority, fairness, autoscaling, partial failure, and reconciliation.

From SARCH-011 retrieve availability and recovery; SARCH-043 and SARCH-044 provide synchronous and asynchronous integration; SARCH-045 provides workflow state; SARCH-051 provides ambiguous effects; and SARCH-055 through SARCH-056 provide control capacity and isolation.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish admission, durable enqueue, delivery, processing, effect, and terminal business outcome;
2. apply Little's law and fluid backlog models within their assumptions;
3. design queue bounds in count, bytes, age, cost, tenant, and downstream work;
4. select backpressure, shedding, expiry, coalescing, and priority policies;
5. preserve identity and idempotent effects under redelivery and ambiguous acknowledgement;
6. scope ordering and partitioning without creating hidden serialization or skew;
7. configure visibility, retry, dead-letter, and redrive as one lifecycle;
8. scale consumers against end-to-end bottlenecks and recovery headroom;
9. protect fairness, security, privacy, and safety under overload;
10. validate load-leveling claims through workload and failure evidence.

## Core Exposition

**Name the acceptance contract.** Enqueue may mean accepted in process memory, replicated durably, retained until a deadline, or merely handed to an external provider. State which failures it survives and how clients query outcome.

Admission is a domain transition. `accepted`, `scheduled`, `processing`, `completed`, `rejected`, `expired`, `cancelled`, `compensating`, and `outcome_unknown` should not collapse into one success. Preserve a durable business identity across producer retries and consumer deliveries.

**Use queues for temporal decoupling.** A queue is effective when peak arrivals exceed service temporarily but average admitted demand remains supportable and deadlines tolerate waiting. It can also isolate maintenance windows and smooth calls to a constrained downstream.

It cannot solve sustained excess demand. If long-run effective arrival is at or above service, backlog has no stable bound. Increase safe capacity, reduce work, coalesce, prioritize, reject, or change the product contract.

**Apply Little's law with one boundary.** Count the same population for $L$, $\lambda$, and $W$. If $L$ includes queued plus in-service jobs, $W$ includes waiting plus service. Use effective completed throughput in a stable interval.

Retries, abandonment, batching, class mixtures, and nonstationarity complicate measurement but do not make accounting optional. Segment by class and report distributions. Average $W$ can hide deadline misses and a stuck partition.

**Model bursts and drain.** The integral of arrival minus service over time approximates backlog change while capacity is available. A short burst may be safe if storage and freshness budgets cover both accumulation and drain.

Drain competes with continuing traffic. A 1,000-job/s consumer with 900 new jobs/s has only 100 jobs/s for old backlog. Recovery work, cold caches, retries, and downstream throttles further reduce net drain.

**Bound the queue multidimensionally.** Item count ignores payload size and processing cost. Bound bytes, age, tenant share, partition depth, retry attempts, downstream calls, and high-cost classes. Apply limits at producer, broker, consumer, and dependency boundaries as appropriate.

Disk capacity is not a safe queue limit. Retention increases recovery time and data exposure. A full queue needs explicit response: reject, shed, replace older coalescible state, spill to governed storage, or pause upstream.

**Propagate backpressure.** Backpressure tells upstream that useful capacity is exhausted. It may be a rejected enqueue, reduced credit, smaller concurrency, slower polling, quota signal, or explicit retry time.

Upstream components must honor it with bounded behavior. Retrying immediately converts backpressure into amplification. Human-facing clients need honest pending or unavailable outcomes rather than infinite spinners.

**Choose load shedding by value and deadline.** Shed work that is expired, redundant, superseded, low priority under policy, or too costly for current reserve. Do not discard randomly when safety, fairness, or legal obligation differs.

Coalescing is valid for state such as “set thermostat target to latest value” but not for additive payments or audit history. Preserve an audit of supersession where required. Admission policy is business policy.

**Define freshness.** Age from enqueue is not always the right clock; a job may refer to source data already stale. Record source version, event time, enqueue time, deadline, policy epoch, and dependency state as needed.

At dequeue, revalidate whether the action remains authorized and useful. Sending yesterday's “your train is delayed” notification today is worse than dropping it. An expired financial instruction may require human resolution rather than execution or deletion.

**Make delivery identity explicit.** Most practical queues may redeliver after consumer crash, lease expiry, or ambiguous acknowledgement. Exactly-once broker delivery, where offered under a specific scope, does not prove exactly-once external business effect.

Use stable operation identity, transactional inbox/outbox patterns where appropriate, conditional state transitions, and durable outcome records. Reject reuse with different payload. Retain deduplication long enough for delayed redelivery and disaster recovery.

**Set visibility timeout from work behavior.** Too short causes concurrent duplicate processing; too long hides crashed work. Renew a lease for legitimate long work, but bound renewal and expose progress. Split very long work into resumable stages where semantics permit.

Cancellation and lease loss must be checked before irreversible effects. An old worker waking after pause may need a fencing token so the new owner and old owner cannot both complete exclusively.

**Bound retries globally.** Retry transient failures with randomized backoff, maximum attempts, elapsed deadline, and fleet-wide retry budget. Distinguish validation, authorization, permanent domain rejection, unavailable dependency, timeout, and unknown effect.

Do not retry a poison message on every worker forever. Isolate it after evidence, preserve context safely, alert an owner, and keep unrelated partitions moving. A changed consumer version may make redrive valid; blind redrive may repeat harm.

**Design dead-letter lifecycle.** Dead-letter storage needs schema, retention, encryption, access, privacy deletion, inspection, repair, replay identity, and audit. The item may contain sensitive payload and evidence of an uncompleted obligation.

Define who decides discard, correct, compensate, or redrive. Replay into the original position may be impossible; explain ordering consequences. Track terminal business resolution beyond broker deletion.

**Scope ordering.** Total FIFO limits parallelism and may let one stuck item block all work. Partition ordering by account, aggregate, device, or workflow when that is the true invariant. A key with extreme load becomes a serial hotspot.

Retries can reorder even within a partition if later items bypass a failing predecessor. Decide whether to block, isolate the key, process commutative work, or record a gap. “Ordered queue” must name send, broker, delivery, attempt, or effect order.

**Partition for load and locality.** Hashing distributes ordinary keys but can hide hot tenants. Range partitioning supports scans but may hotspot. Maintain enough partitions for parallelism without creating excessive consumers, connections, and metadata.

Use per-partition age and throughput. Global depth can look healthy while one partition is stuck. Repartitioning live work needs ownership epochs, offset/state transfer, and duplicate protection.

**Protect fairness.** One tenant can fill shared storage or dominate consumers. Use per-tenant quotas, weighted fair scheduling, separate priority classes, cells, and admission. Priority queues require aging or reserved shares if starvation is unacceptable.

Do not let low-value bulk work block safety commands. Also prevent an endless “urgent” stream from eliminating contractual background work. Validate priority claims and authorize who may set them.

**Scale the bottleneck, not the queue.** Consumer autoscaling based on depth or age can help only if downstream databases, providers, locks, and quotas can absorb concurrency. Scaling past them increases timeout and retry load.

Use backlog age, arrival/service rates, cost, deadlines, and downstream saturation. Cap concurrency per dependency and tenant. Scale-out delay belongs in the model; preserve headroom for drain after failure.

**Separate queue durability from business durability.** Replicated broker storage protects queued bytes under its fault model. It does not prove producer intent was committed, the schema remains processable, the consumer effect is durable, or the outcome reached the user.

Trace end to end. A message may be acknowledged then expire, enter dead letter, or produce an ambiguous external effect. Product state should reveal this rather than reporting generic success.

**Design multi-stage pipelines.** Each queue creates another buffer, retry policy, ordering boundary, and amplification point. If every stage buffers freely, total latency and storage can be enormous while each local depth appears acceptable.

Carry end-to-end identity, deadline, priority, and trace context. Allocate budgets across stages and stop stale work early. Avoid multiplying retries at producer, broker, consumer, and downstream client.

**Preserve security and privacy.** Authenticate producers and authorize topics, partitions, tenant keys, priority, and redrive. Encrypt payload and metadata as required. Minimize sensitive content and prevent one tenant from observing another's timing or identifiers.

Deletion and retention rules include queued, retried, dead-lettered, backed-up, and replayed copies. Treat malformed and oversized messages as hostile inputs. Limit decompression, parsing, and fan-out cost before expensive work.

**Observe useful outcomes.** Measure effective arrival and service rates, depth, bytes, oldest age, age percentiles, attempts, lease expiry, duplicates, poison rate, dead letters, per-tenant and per-partition skew, downstream saturation, and terminal outcomes.

Lag alone does not show harm. Join age to deadlines and value. Empty queue can mean healthy completion, data loss, or consumers accepting and failing later. Reconcile business authorities.

**Test load and failure.** Generate burst, sustained overload, heavy tenant, large payload, slow consumer, stopped partition, downstream throttle, crash before and after effect, lost acknowledgement, duplicate, reorder, poison, expired item, broker failover, and recovery replay.

Record workload, tool and broker versions, topology, expected invariant, actual output, and limitation. Passing one synthetic burst does not prove behavior under different payload cost, skew, downstream failure, or duration.

## Definitions and Notation

Let:

- $A(t)$ be cumulative admitted arrivals by time $t$;
- $S(t)$ be cumulative completed service by time $t$;
- $Q(t)=Q(0)+A(t)-S(t)$ be queued plus in-service work under consistent accounting;
- $\lambda$ be effective arrival or throughput rate and $\mu$ service capacity under stated conditions;
- $\rho=\lambda/\mu$ be utilization in a simplified one-server model;
- $L$ be average number in system and $W$ average sojourn time;
- $d_i$ be item deadline and $a_i(t)$ its age at time $t$;
- $k_i$ be durable business identity and $n_i$ attempt count;
- $p(i)$ be queue partition for item $i$;
- **net drain rate** mean service rate minus continuing admitted arrival rate;
- **work amplification** mean total attempts or downstream actions per original admitted intent.

Little's law requires a stable observation with consistent population boundaries. The fluid backlog equations approximate aggregate work and do not model stochastic tail latency, scheduling, payload cost, or failure correlation.

## Mechanisms, Invariants, or Proof Structure

### Queue-design procedure

1. Name business intent, acceptance durability, terminal outcomes, deadlines, and cancellation semantics.
2. Measure arrival, service, payload cost, burst, skew, and downstream limits by class and tenant.
3. Define queue boundaries in count, bytes, age, cost, partition, tenant, retry, and amplification.
4. Choose partition key, ordering scope, priority, fairness, coalescing, shedding, and backpressure.
5. Define business identity, deduplication, visibility lease, fencing, retry classification, and outcome record.
6. Define poison isolation, dead-letter ownership, repair, retention, privacy, and safe redrive.
7. Scale within downstream capacity and reserve drain headroom.
8. Observe age and terminal business outcomes end to end.
9. Test bursts, sustained overload, partial failure, recovery, and adversarial payloads.

### Backlog derivation

During a constant-rate overload interval, $Q(T)-Q(0)=(\lambda-\mu)T$ when $\lambda>\mu$. If later arrivals fall to $\lambda_r<\mu$, net drain is $\mu-\lambda_r$, so the ideal time to remove excess $B$ is $B/(\mu-\lambda_r)$. At equality backlog does not shrink; below capacity but with deadlines, work can still expire before drain.

### Architectural invariants

- no admission response masquerades as completed effect;
- no queue grows without declared multidimensional bounds and full behavior;
- no retry loses original business identity or exceeds its time/work budget;
- no expired or superseded work executes without current domain revalidation;
- no poison or tenant can consume unbounded unrelated capacity;
- no empty-queue recovery claim precedes business-outcome reconciliation.

## Alternatives and Trade-Offs

| Choice | Strength | Cost or risk | Required evidence |
|---|---|---|---|
| synchronous rejection | immediate truth and backpressure | lower burst acceptance | client behavior and retry bound |
| durable queue | temporal leveling and decoupling | delayed/ambiguous completion | durability and outcome tracking |
| unbounded retention | fewer immediate rejects | uncontrolled latency, cost, exposure | generally unacceptable without outer bound |
| coalescing | reduces superseded state work | invalid for additive/history semantics | domain merge proof |
| strict FIFO | simple order | head-of-line blocking and low parallelism | actual invariant scope |
| keyed partitions | local order and parallelism | hot keys and rebalancing | per-key heat and epochs |
| priority queue | protects urgent work | starvation and priority abuse | aging, shares, authorization |
| retry with backoff | recovers transient faults | amplification and stale work | classification and budgets |
| dead-letter isolation | protects unrelated work | hidden obligations and sensitive retention | ownership and resolution |
| autoscaled consumers | faster drain | downstream overload and cold-start lag | end-to-end capacity tests |

## Failure Modes and Misconceptions

1. **“A queue adds capacity.”** it stores demand and shifts processing time.
2. **“Average arrival below capacity is enough.”** bursts and deadlines can still fail.
3. **“Successful enqueue means success.”** only the stated admission transition occurred.
4. **“Depth measures health.”** bytes, age, skew, cost, and outcomes also matter.
5. **“Disk size is a safe bound.”** recovery time, privacy, and usefulness constrain retention.
6. **“Exactly-once delivery means exactly-once effect.”** external state and failure boundaries differ.
7. **“Long visibility prevents duplicates.”** it delays recovery and cannot eliminate ambiguous effects.
8. **“Retry all errors.”** permanent, poison, unauthorized, expired, and unknown outcomes differ.
9. **“Dead letter means handled.”** it marks unresolved work requiring ownership.
10. **“FIFO is global.”** partitioning, retries, and effect order limit scope.
11. **“More consumers always drain faster.”** downstream bottlenecks can worsen.
12. **“Priority protects important work.”** misclassification and starvation require policy.
13. **“Backpressure is an implementation detail.”** it changes client and product behavior.
14. **“Old work should eventually run.”** expiry or supersession can make execution harmful.
15. **“Empty queue means recovered.”** loss or divergent effects may remain.
16. **“One load test proves leveling.”** cost, skew, faults, duration, and versions bound evidence.

## Worked Examples

### Example 1

**Situation.** Effective throughput is 200 jobs/s and average sojourn is five seconds in a stable interval.

**Reasoning.** Little's law gives $L=200(5)=1{,}000$ average jobs in system. If monitoring shows only 600, boundaries differ: perhaps it excludes in-service work, samples another class, or uses offered rather than completed rate.

**Conclusion.** Little's law diagnoses inconsistent measurement as well as capacity relationships.

### Example 2

**Situation.** Arrival is 1,100 jobs/s and service 800 for 120 seconds; afterward arrival is 500.

**Reasoning.** Excess grows by $300(120)=36{,}000$. Later net drain is $800-500=300$ jobs/s, so ideal drain is 120 seconds. Retry and cold-cache costs lengthen it, and a 90-second freshness budget causes some work to expire.

**Conclusion.** A survivable storage burst can still violate business freshness.

### Example 3

**Situation.** An email endpoint returns `202 Accepted` after durable enqueue.

**Reasoning.** The response means the intent survived the broker's declared faults, not that delivery occurred. Expose a message identity and status. Later states may be sent, provider-rejected, expired, suppressed, or unknown; client text must not say “delivered.”

**Conclusion.** Admission and terminal outcome need separate API semantics.

### Example 4

**Situation.** Processing normally takes 90 seconds but visibility timeout is 60.

**Reasoning.** A second consumer may receive the item while the first still acts, causing concurrent duplicate effect. Renew a bounded lease or split resumable work; record identity and conditionally commit the domain outcome. A three-hour timeout would delay genuine crash recovery.

**Conclusion.** Visibility balances duplicate exposure and recovery delay but never replaces idempotent effect design.

### Example 5

**Situation.** One malformed item crashes every consumer at the head of a strict FIFO partition.

**Reasoning.** Classify deterministic failure, isolate after bounded attempts, preserve its sequence gap and evidence, alert an owner, and continue only if later work is semantically safe. Redrive after corrected schema or consumer validation under the same identity.

**Conclusion.** Poison isolation needs ordering policy and owned business resolution.

### Example 6

**Situation.** Consumer autoscaling doubles concurrency while the database is already at its connection limit.

**Reasoning.** Extra consumers wait, time out, and retry, reducing effective service. Cap database concurrency, shed or slow intake, optimize service cost, and scale the actual bottleneck. Use backlog age and downstream saturation, not depth alone.

**Conclusion.** Scaling the wrong stage amplifies overload.

### Example 7

**Situation.** Tenant A contributes 70% of a shared queue and delays 500 smaller tenants.

**Reasoning.** Partition and account capacity by tenant, reserve fair shares, cap A, and isolate its heavy work in a cell or separate class. Weighted scheduling lets unused capacity be borrowed without allowing permanent starvation.

**Conclusion.** Load leveling requires tenant-aware admission and scheduling.

### Example 8

**Situation.** A queue contains one million location updates, but only each device's latest target matters.

**Reasoning.** If updates mean set-state rather than additive history, coalesce by authenticated device identity while preserving required audit. Do not coalesce payments or incremental counters. Revalidate the latest target and expiry before actuation.

**Conclusion.** Domain-valid supersession can reduce backlog more safely than brute-force drain.

### Example 9

**Situation.** A consumer charges a card, then crashes before acknowledging the message.

**Reasoning.** Redelivery is expected. Reuse one payment intent with the provider, inspect the durable outcome, and reconcile if response was ambiguous. A broker's delivery mode cannot undo the external charge.

**Conclusion.** Exactly-once business effect crosses broker, consumer, and provider authorities.

### Example 10

**Situation.** A restored queue is empty after an incident, but 200 orders lack shipment status.

**Reasoning.** Messages may have expired, been lost, dead-lettered, or produced effects without callbacks. Compare order authority, queue audit, carrier identities, and warehouse state; repair or compensate through authorized workflows before closing recovery.

**Conclusion.** Queue state is evidence, not the business system of record.

## Cross-Program Connections

- **Data Engineering:** owns stream partitions, offsets, watermarks, windows, replay, and processing engines.
- **API and Service Engineering:** exposes accepted, pending, rejected, expired, and completed states and backpressure.
- **Distributed Systems Engineering:** owns replicated logs, delivery protocols, leases, ordering, and fault tolerance.
- **Database Engineering:** owns transactional outbox/inbox, deduplication state, conditional effects, and recovery.
- **Platform Engineering:** owns broker fleets, autoscaling, quotas, partitions, capacity, and tenant isolation.
- **Software Delivery and Reliability Engineering:** owns SLOs, overload tests, alerts, dead-letter operation, and incident reconciliation.
- **Security Engineering:** owns producer identity, topic authorization, sensitive payload, hostile input, and redrive authority.
- **Systems Engineering:** connects queued commands to deadlines, people, physical actuators, and safety.

## References

1. John D. C. Little, “A Proof for the Queuing Formula: $L=\lambda W$,” *Operations Research* 9(3), 1961. <https://doi.org/10.1287/opre.9.3.383>
2. Leonard Kleinrock, *Queueing Systems, Volume 1: Theory*, Wiley, 1975.
3. Mor Harchol-Balter, *Performance Modeling and Design of Computer Systems*, Cambridge University Press, 2013. <https://doi.org/10.1017/CBO9781139226424>
4. Matt Welsh, David Culler, and Eric Brewer, “SEDA: An Architecture for Well-Conditioned, Scalable Internet Services,” *SOSP 2001*. <https://doi.org/10.1145/502034.502057>
5. Gregor Hohpe and Bobby Woolf, *Enterprise Integration Patterns*, Addison-Wesley, 2003.
6. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly Media, 2017.
7. Jeffrey Dean and Luiz André Barroso, “The Tail at Scale,” *Communications of the ACM* 56(2), 2013. <https://doi.org/10.1145/2408776.2408794>
8. Betsy Beyer et al., eds., *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly Media, 2016. <https://sre.google/sre-book/table-of-contents/>

## Exercises

### Exercise 1

Define queue, admission, arrival rate, service rate, utilization, queueing delay, sojourn time, backpressure, load shedding, bounded queue, visibility timeout, dead letter, poison message, freshness budget, net drain, and work amplification.

### Exercise 2

A stable system completes 300 jobs/s with average sojourn 8 seconds. Calculate average jobs in system. Then a 10-minute interval admits 450 jobs/s while service remains 300; afterward arrivals fall to 180. Calculate excess backlog and ideal drain time, and state why deadlines and variance still matter.

### Exercise 3

Diagnose a broker pipeline with unbounded retention, new identity on each retry, 30-second visibility for five-minute jobs, global FIFO, unlimited consumer autoscaling, and dead letters deleted weekly. Provide a safe lifecycle and evidence.

### Exercise 4

Compare synchronous rejection, bounded durable queueing, coalescing, priority classes, keyed ordering, and autoscaling for payment, telemetry, email, inventory reservation, and physical commands. Explain acceptance, expiry, idempotency, fairness, and recovery.

### Exercise 5

Design queue-based load leveling for an international wildfire-response network carrying sensor telemetry, evacuation alerts, aircraft requests, volunteer updates, medical supplies, public subscriptions, and intermittent field commands. Cover capacity, identity, priority, freshness, ordering, fairness, offline behavior, security, poison work, shedding, scaling, evidence, and physical reconciliation.

## Answers to the Exercises

### Answer 1

A **queue** stores admitted work before a consumer attempt. **Admission** accepts work under a stated durability and retention contract. **Arrival rate** is admitted work per time; **service rate** is completed attempts per time; **utilization** is their ratio in the simplified model. **Queueing delay** is waiting; **sojourn** includes waiting and service. **Backpressure** signals reduced upstream acceptance; **load shedding** deliberately rejects or expires work. A **bounded queue** limits count, bytes, age, cost, or another resource. A **visibility timeout** is a temporary delivery lease. A **dead letter** is isolated unresolved work; a **poison message** deterministically fails processing. A **freshness budget** bounds useful age. **Net drain** is service minus continuing arrivals. **Work amplification** is attempts or downstream actions per original intent.

### Answer 2

Little's law gives $L=300(8)=2{,}400$ average jobs in system. Ten minutes is 600 seconds; excess rate is $450-300=150$, so excess backlog is $150(600)=90{,}000$ jobs. Later net drain is $300-180=120$ jobs/s, giving ideal drain time $90{,}000/120=750$ seconds, or 12.5 minutes. Stability averages do not bound tail delay. Variable job cost, partition skew, retries, downstream throttling, cold caches, and scale lag change service. Items with deadlines shorter than accumulation plus drain may expire even though the queue eventually empties.

### Answer 3

Define admission durability and terminal domain states; keep one authenticated business identity across producer and consumer retries. Bound count, bytes, age, tenant, partition, cost, attempts, and downstream work. Reject or coalesce only under domain policy when full. For five-minute jobs, use renewable bounded leases with progress or split into resumable stages; conditionally commit effects and fence stale workers. Partition order by the actual aggregate rather than global FIFO, with poison isolation and explicit gap policy.

Scale consumers from arrival/service rate, oldest age, deadline, job cost, and downstream saturation, with hard dependency concurrency caps. Classify failures; retry only transient cases with elapsed and attempt budgets. Dead-letter items retain protected evidence and have an owner who corrects, compensates, safely redrives under the same identity, or authorizes disposal. Measure effective rates, ages, bytes, attempts, duplicates, partition skew, dependency state, and final business outcomes. Test lost acknowledgements, poison, expiry, sustained overload, and restoration.

### Answer 4

Payments favor bounded admission or synchronous rejection when capacity is unavailable, one intent identity, and provider reconciliation; coalescing is invalid. Telemetry can use keyed partitions and may sample or coalesce state readings if historical obligations allow. Email can accept durably and expose pending/sent/rejected/expired states, with tenant fairness. Inventory reservation cannot merely queue beyond offer expiry; reserve rights synchronously or mark pending and revalidate. Physical commands need strict authority, short freshness, per-device order, fencing, and reconciliation with observed physical state.

Synchronous rejection gives immediate backpressure but lower burst acceptance. Bounded queues level temporary bursts while exposing delay. Coalescing removes superseded state only under valid semantics. Priority protects safety work but needs authorization and anti-starvation shares. Keyed order preserves local sequences but creates hot keys. Autoscaling helps within actual downstream capacity. Every design specifies acceptance, deadline, cancellation, duplicate effect, fairness, poison, recovery, and evidence.

### Answer 5

Separate classes: safety alerts and authenticated field commands; aircraft and medical resource requests; sensor telemetry; volunteer updates; and public notifications. Each has distinct queues, reserved shares, deadlines, payload bounds, and shedding. Alerts carry incident, geography, authority epoch, supersession, expiry, and signature; stale alerts are withdrawn rather than delivered. Field commands key by physical asset, preserve order and fencing, expire quickly, and reconcile with physical acknowledgement. Aircraft and supplies use one request identity and an authoritative allocation workflow; enqueue is pending, not allocated.

Telemetry keys by sensor and time window, admits bounded late data, samples under overload according to scientific policy, and never lets a noisy device consume safety capacity. Volunteer and public notifications use tenant/geography quotas and may coalesce latest state. Intermittent field gateways persist scoped work locally, expose freshness, and synchronize identities without creating duplicates. Sensitive medical and location data is minimized, encrypted, residency-bound, retained appropriately, and accessible only to authorized producers, consumers, and redrive operators.

Capacity models burst and sustained fire scenarios, payload/decompression cost, satellite bandwidth, downstream dispatch and hospital limits, and recovery drain. Backpressure reaches agencies; expired and superseded work sheds first under declared policy. Poison payloads isolate with forensic evidence. Consumers retry transient faults with bounded randomized backoff and per-dependency concurrency. Evidence records source, incident, identity, authority and schema version, priority, enqueue/event time, attempts, partition, expiry, consumer effect, physical acknowledgement, manual action, and terminal outcome. Exercises cover region isolation, false sensor flood, compromised producer, aircraft scarcity, duplicate command, lost response, poison alert, queue saturation, reconnect herd, and reconciliation after fire containment.
