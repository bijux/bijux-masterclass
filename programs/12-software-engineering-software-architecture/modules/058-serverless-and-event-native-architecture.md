---
module_id: SARCH-058
program: Software Engineering: Software Architecture
level: 2
module_number: 58
title: Serverless and Event-Native Architecture
status: complete
last_verified: 2026-09-06
---

# Serverless and Event-Native Architecture

## One-Page Review

### Governing question

Which responsibilities can safely move into event-triggered, provider-managed execution and services while the architecture retains explicit control over identity, state, delivery, concurrency, cost, security, observability, and recovery?

### Essential definitions

- **serverless** is an operating model in which a provider allocates and manages much of the runtime capacity and infrastructure while the consumer supplies code, configuration, data, and policy; servers and operational responsibility do not disappear.
- **function as a service (FaaS)** runs bounded handlers on demand; serverless also includes managed event, workflow, data, identity, and integration services.
- An **event** is an immutable statement that something occurred; a **command** requests an action; a **notification** merely signals that information may be available.
- An **event envelope** carries identity, source, type, subject, time, schema, and correlation metadata around domain data.
- A **trigger** maps an occurrence or delivery source to execution; it does not by itself establish exactly-once effect.
- A **cold start** is activation work before a runtime can handle an invocation; **warm reuse** is an optimization and must not be required for correctness.
- **reserved concurrency** bounds or guarantees execution capacity for a workload; **fan-out** creates multiple downstream deliveries or executions.
- **eventual completion** means a workflow may finish after the initiating response; it requires visible states, deadlines, and reconciliation.
- **event-native architecture** treats durable events, asynchronous state transitions, and event-driven scaling as first-class boundaries rather than adapters around an implicit synchronous transaction.
- **provider limit** is an enforced quota, size, duration, concurrency, rate, or feature boundary that forms part of the deployed system and must be verified for the selected service and version.

### Central model, mechanism, or theorem

For stable executions with arrival rate $\lambda$ and mean execution time $W$, Little's law gives mean concurrent executions

$$
L=\lambda W.
$$

At 250 invocations/s and mean duration 0.4 s, mean concurrency is 100 before burst, retry, cold-start, and tail allowances. Concurrency is a capacity and downstream-pressure quantity, not merely a billing setting.

If every event produces $b$ new events for $d$ generations without deduplication or termination, total events including the original are

$$
E=\sum_{k=0}^{d}b^k=\frac{b^{d+1}-1}{b-1}\quad(b\ne1).
$$

This simple branching model reveals amplification risk. Real graphs have unequal branching, filtering, cycles, failures, and retries; every event chain needs bounded identity, depth, work, and termination.

### Critical invariants

- every trigger carries a durable event or command identity across redelivery and retry;
- handler correctness never depends on warm process memory, one invocation, or stable local disk;
- admission or trigger acknowledgement is not presented as completed business effect;
- concurrency and fan-out stay within downstream, tenant, region, and cost budgets;
- duplicate, delayed, reordered, missing, and replayed events preserve domain invariants;
- event type and schema evolve under explicit compatibility and ownership rules;
- event time, observation time, publication time, and processing time are not conflated;
- retries distinguish transient failure, permanent rejection, poison data, expiry, and ambiguous external effect;
- workflows expose pending, completed, rejected, expired, compensating, and unknown outcomes;
- secrets, identity, network access, data residency, and least privilege are explicit despite managed infrastructure;
- provider limits and failure behavior are verified at authoring and deployment time, not assumed from a generic pattern;
- observability correlates one business intent across asynchronous hops and sampled traces;
- portability claims distinguish source portability from semantic and operational portability;
- recovery reconciles state and external effects before replay or closure.

### Common failures

Common failures include equating serverless with stateless business behavior; keeping correctness-critical state in a warm global variable; assuming one event causes one invocation; scaling functions until the database collapses; retrying non-idempotent payments; treating event order as global; publishing internal database rows as stable domain contracts; changing schemas without old consumers; chaining dozens of functions synchronously; creating recursive trigger loops; ignoring dead letters and expired work; placing secrets in event payloads or logs; trusting default public network reachability; estimating cost from average duration alone; and claiming cloud portability because code uses a common language.

### Compact example

An object-created event invokes an image processor. Delivery is repeated after acknowledgement loss, and two handlers race. Both use the same object version and derived-output identity, conditionally create the result, and record the terminal outcome. Concurrency is capped below storage and database limits; oversized or unsupported input is rejected to an owned dead-letter workflow. The trigger provides elastic attempts, not exactly-once transformation.

### Connections

[SARCH-044](044-asynchronous-messaging-integration.md) supplies delivery semantics, [SARCH-055](055-control-plane-and-data-plane-architecture.md) supplies managed control boundaries, and [SARCH-057](057-queue-based-load-leveling.md) supplies load leveling. [SARCH-059](../ROADMAP.md) next examines service meshes and traffic policy. Cloud Engineering owns provider-specific services; this module owns architectural contracts and consequences.

## Governing Question

Serverless systems remove direct responsibility for provisioning many individual hosts and can align capacity with demand. Event triggers let components react independently and turn long workflows into explicit state transitions. These benefits are substantial when work is bursty, bounded, and naturally asynchronous.

The provider still operates physical and virtual servers, and the application still owns domain correctness. Delivery semantics, quotas, cold starts, concurrency, data authority, security, schema, cost, and recovery cross managed-service boundaries. The question is which responsibilities are delegated and which evidence remains necessary.

## Why This Matters

An event can travel farther and duplicate more easily than a direct call. Automatic scaling can convert one malformed object or attack into thousands of executions and downstream writes. A low idle bill can become high incident cost. A small function can participate in a legally or financially significant workflow.

Architecture must make asynchronous state and managed constraints visible. Otherwise local simplicity produces global opacity: no owner sees the whole workflow, retries are inconsistent, and provider dashboards cannot explain the customer's terminal outcome.

## Prerequisites and Retrieval

Retrieve event, command, message, queue, stream, trigger, handler, idempotency, deduplication, retry, backoff, concurrency, fan-out, cold start, state machine, transaction, outbox, schema, version, deadline, dead letter, least privilege, quota, cost allocation, tracing, replay, and reconciliation.

From SARCH-035 and SARCH-044 retrieve event and asynchronous integration; SARCH-045 provides workflow state; SARCH-051 provides partial failure; SARCH-055 provides control/data separation; and SARCH-057 provides queue bounds and downstream capacity.

## Learning Objectives

After completing this module, you should be able to:

1. define serverless and event-native architecture without implying absent infrastructure or responsibility;
2. distinguish event, command, notification, trigger, invocation, effect, and workflow outcome;
3. derive simple concurrency and event-amplification estimates with explicit limitations;
4. design handlers for redelivery, cold starts, concurrency, and ambiguous effects;
5. model workflow state, compensation, expiry, and human resolution;
6. evolve event envelopes and schemas without coupling consumers to private storage;
7. bound fan-out, recursive triggers, downstream pressure, and cost;
8. design identity, secrets, network, residency, and supply-chain controls across managed services;
9. evaluate portability, lock-in, and operational responsibility precisely;
10. verify current provider limits while keeping the architecture durable beyond one service.

## Core Exposition

**Define the delegation boundary.** Serverless delegates infrastructure allocation, patching, runtime scheduling, and some availability mechanics to a provider under a service contract. The consumer still owns code, dependencies, configuration, identity, data, access, domain invariants, observability, and usage.

Write a responsibility map per service. A managed queue may replicate messages but not validate business identity. A function runtime may retry but not know whether an external payment occurred. A workflow service may persist steps but not decide compensation legality.

**Distinguish events and commands.** An event says `OrderPlaced`; a command says `ReserveInventory`; a notification says `OrderChanged` and asks consumers to fetch authority. Events are facts owned by a domain and should not be renamed commands merely to hide coupling.

Commands have an intended receiver and rejection semantics. Events may have unknown consumers. Notifications minimize payload coupling but add read dependency. Choose from authority, privacy, latency, retention, and consumer autonomy.

**Use a stable envelope.** Include globally unique event identity, source, type, subject, schema/version, time semantics, correlation or causation identity, and content type. Keep transport metadata distinct from domain payload.

Identity supports deduplication and trace. Source and type support authorization and routing. Schema enables compatibility. Do not include secrets or unrestricted personal data merely because a bus is private. Sign or authenticate where trust crosses boundaries.

**Treat delivery as attempts.** Triggers may duplicate after timeout, consumer crash, broker retry, or control failure. They may delay and reorder across partitions. Even a platform feature named exactly-once has a documented scope that may exclude external side effects.

Handlers record one business identity and use conditional transitions, transactional inbox/outbox, or idempotent provider operations. Deduplication retention covers replay and disaster recovery. Reuse with different payload is rejected.

**Design for cold and warm execution.** Initialization loads runtime, code, configuration, connection, and caches. Cold-start distribution depends on platform, language, package, network, traffic, and configuration. Current values must be measured for the deployed environment.

Warm memory can cache immutable or version-checked data, but correctness starts from empty or reused state. Clear tenant-specific state between invocations. Local temporary storage is bounded and ephemeral unless the selected service explicitly guarantees otherwise.

**Model concurrency from demand.** Mean concurrency follows arrival times mean duration under stable boundaries. Tail duration, bursts, retry, batch size, and cold initialization require reserve. One event may create multiple concurrent records depending on trigger batching.

Concurrency pushes downstream. A function fleet that can start 10,000 executions should not open 10,000 database connections. Use reserved concurrency, semaphore or pool limits, queueing, admission, and per-tenant fairness. Scale the bottleneck.

**Bound fan-out and recursion.** Event routers, object notifications, change streams, and workflow steps can multiply work. Cycles arise when a handler writes to its own trigger source or two services republish each other's events.

Carry causation identity and bounded depth where useful, filter narrowly, separate input/output locations, cap concurrency and rate, and alarm on amplification ratios. A stop switch must not depend only on the runaway path.

**Model asynchronous workflow state.** A chain of functions is not automatically a workflow. Durable business state names steps, attempts, deadlines, compensation, manual decisions, and terminal outcomes. A workflow engine is a mechanism; the domain state remains explicit.

Compensation is a new action and can fail. Some effects are irreversible. Avoid long synchronous chains that pay cumulative cold starts and make partial failure opaque. Return pending with a status resource when the business permits.

**Use queues for pressure, not only wiring.** Direct triggers can transmit bursts immediately. A queue between source and handler supports buffering, retry ownership, concurrency bounds, and inspection. It also adds age, retention, duplicate, and dead-letter concerns.

Size from arrival, service, downstream capacity, deadlines, payload, and cost. Expire or coalesce only under domain rules. One queue for all tenants and priorities can reconnect failures that functions otherwise isolate.

**Choose streams for ordered histories deliberately.** Streams retain ordered partitions and support multiple consumers and replay. Partition key determines order and heat. Reprocessing can rebuild projections when source events are complete and compatible.

An event log is not automatically a system of record for every domain. Retention, compaction, deletion, privacy, schema, and authority matter. Replaying commands may repeat effects; replay facts into a projection or use explicit repair logic.

**Evolve schemas conservatively.** Producers and consumers deploy independently. Prefer additive compatible evolution, defaults with domain meaning, stable identifiers, and explicit new event types when semantics change. Test old producer/new consumer and new producer/old consumer combinations.

Do not expose internal table shape as a public event contract. A database change event may support integration but couples consumers to storage lifecycle and can leak fields. Translate at the owning domain boundary.

**Handle poison and dead letter.** Validate envelope, size, schema, authorization, and decompression cost before expensive work. Classify permanent invalid input separately from transient dependency failure. Retry budgets include attempts and elapsed deadline.

Dead-letter work retains an unresolved obligation and perhaps sensitive data. Assign owner, retention, access, correction, compensation, and redrive semantics. Redrive preserves original identity and does not assume old events remain valid.

**Plan state deliberately.** Functions can access managed databases, durable objects, caches, object stores, or workflow state. Choose ownership and consistency as in any architecture. Stateless compute does not make the business stateless.

Avoid hidden shared mutable globals and unbounded per-invocation connections. Use conditional writes and transactions for invariants. Cache with version and expiry. Model regional placement, backup, deletion, and recovery across managed stores.

**Secure every event path.** Authenticate source, authorize publish/subscribe/trigger/configuration actions, scope runtime identity, and isolate tenants. Use least-privilege network paths and egress controls. Managed service defaults must be verified, not assumed.

Protect build artifacts and dependencies. A small function often has broad data access. Sign artifacts where supported, pin and scan dependencies, keep secrets out of packages and events, rotate credentials, and audit control-plane changes.

**Treat observability as distributed state.** One request may yield delayed executions in several services. Propagate business, event, causation, correlation, attempt, workflow, and tenant-safe identities. Record event age, queue, trigger, runtime version, cold/warm classification where observable, concurrency, downstream call, and terminal outcome.

Sampling can drop the one failed branch. Retain durable domain audit for critical workflows rather than depending on traces alone. Provider metrics show platform behavior; join them to business authority.

**Model cost from work, not labels.** Cost may include invocations, duration, configured memory or compute, provisioned concurrency, events, queue operations, workflow transitions, logs, network, storage, secrets, builds, and support. Pricing changes, so verify current rates for decisions.

Estimate distributions and amplification, not only average handler duration. High-cardinality logs, retry loops, cross-region egress, and fan-out can dominate. Set tenant and workflow budgets, alarms, quotas, and automatic containment.

**Evaluate portability precisely.** Source code in a portable language may still depend on trigger semantics, identity, event envelope, retry rules, limits, network, deployment, observability, workflow, and data services. Abstraction layers can reduce coupling but may hide valuable capabilities or create another runtime.

Decide which portability is valuable: source, build, interface, event schema, data, operational procedure, or recovery. Maintain an exit or coexistence plan proportional to business risk. Avoid a lowest-common-denominator design without evidence.

**Design regional behavior.** A provider-managed function and trigger still have regions and control planes. Place event sources, handlers, state, keys, logs, and dead letters according to latency, residency, and recovery. Cross-region retry can duplicate and reorder.

Define failover authority and event ownership. Replicating a queue does not decide which region consumes. Preserve routing epochs, idempotency, and reconciliation. Verify provider-specific recovery semantics at deployment time.

**Test current limits and failure.** Providers impose payload, duration, concurrency, rate, retention, environment, and networking limits that change. Record selected service, region, runtime, dependency, configuration, and retrieval date. Test boundary behavior rather than copying a stale number into durable design.

Inject duplicate, reorder, delay, poison, cold burst, downstream throttle, timeout after effect, control-plane loss, quota exhaustion, recursive event, old schema, key revocation, region isolation, and replay. Claims remain bounded to the tested environment.

## Definitions and Notation

Let:

- $\lambda$ be effective invocation arrivals per second and $W$ mean execution time in seconds;
- $L=\lambda W$ be mean concurrent executions under stable consistent boundaries;
- $b$ be mean or modeled branch count per event generation and $d$ maximum generation depth;
- $E_d=\sum_{k=0}^{d}b^k$ be total events in the idealized branching tree;
- $p_i$ be per-invocation charge, $p_t$ time/resource charge, and $x_j$ other metered units;
- $C=p_iN+p_t\sum_i r_it_i+\sum_j p_jx_j$ be a simplified workload cost model;
- $k$ be durable business intent, $e$ event identity, and $a$ attempt identity;
- $t_e,t_p,t_o$ be event, publication, and observation times;
- **cold start** mean initialization before useful handler execution;
- **event age** mean current time minus the explicitly selected source or publication time;
- **amplification ratio** mean downstream attempts or events divided by original admitted intents.

Pricing units and service limits are provider-specific and time-varying. The formulas organize evidence but do not replace current official documentation and measured workloads.

## Mechanisms, Invariants, or Proof Structure

### Event-native design procedure

1. Name domain facts, requested actions, authorities, terminal outcomes, deadlines, and compensation.
2. Define envelope identity, source, type, subject, schema, time, causation, privacy, and trust.
3. Select trigger, queue, stream, workflow, state store, partition, region, and delivery contract.
4. Design duplicate, reorder, delay, missing, poison, replay, and ambiguous-effect behavior.
5. Model arrival, duration, concurrency, batch, fan-out, downstream capacity, and cost bounds.
6. Define cold-start, configuration, local-state, connection, and runtime-version behavior.
7. Protect identities, events, secrets, artifacts, network, data, control plane, and tenant boundaries.
8. Observe intent through terminal business outcome and preserve durable audit where needed.
9. Verify current limits and exercise failure, quota, compromise, region, and recovery paths.

### Amplification derivation

With constant branch factor $b$, generation $k$ contains $b^k$ events, so through depth $d$ the geometric sum is $(b^{d+1}-1)/(b-1)$ for $b\ne1$ and $d+1$ for $b=1$. A cycle without a depth or state termination can grow until quota or failure intervenes; retries multiply attempts beyond this event count.

### Architectural invariants

- no platform acknowledgement masquerades as completed domain effect;
- no handler requires warm state or single delivery for correctness;
- no event can create unbounded downstream depth, width, retries, or cost;
- no schema change silently changes the meaning consumed by older handlers;
- no replay repeats commands or external effects without explicit repair semantics;
- no serverless delegation removes named ownership for security, data, and recovery.

## Alternatives and Trade-Offs

| Choice | Strength | Cost or risk | Required evidence |
|---|---|---|---|
| direct synchronous service | immediate outcome and simple trace | coupling and idle capacity | latency and failure contract |
| direct event trigger | low wiring and fast reaction | burst transfer and retry opacity | delivery and concurrency test |
| queued trigger | backpressure and retry ownership | added age and dead-letter lifecycle | capacity and freshness |
| retained stream | order partitions, replay, many consumers | schema, retention, hot keys | offsets and replay safety |
| managed workflow | durable step state | transition cost and platform semantics | compensation and history |
| FaaS handler | elastic bounded execution | cold start, limit, runtime coupling | distributions and quotas |
| long-running service | stable connections and runtime control | capacity operation and idle cost | scaling and patching |
| provisioned concurrency | lower activation variability | reserved cost | workload-tail benefit |
| provider-native integration | deep managed capability | semantic lock-in | explicit dependency and exit plan |
| portable abstraction | common interfaces | hidden features and extra layer | recovery and operational parity |

## Failure Modes and Misconceptions

1. **“Serverless has no servers.”** infrastructure exists; responsibility is redistributed.
2. **“Functions are stateless.”** runtime instances and business workflows can carry state.
3. **“One event invokes once.”** duplicate and retry are normal possibilities.
4. **“Automatic scale means infinite capacity.”** quotas and downstreams remain finite.
5. **“Cold start is one number.”** it is a workload and environment distribution.
6. **“Warm reuse is reliable.”** reuse is an optimization, not a correctness premise.
7. **“Event means command.”** facts and requested actions have different ownership.
8. **“A bus decouples semantics.”** schemas, identity, and domain meaning still couple.
9. **“Exactly-once covers the workflow.”** documented scope may end before external effects.
10. **“Replay repairs everything.”** commands, old schemas, and irreversible effects may repeat harm.
11. **“Scaling consumers drains safely.”** downstream capacity can collapse.
12. **“Managed means secure by default.”** identity, network, data, and configuration remain owned.
13. **“Small functions have small blast radius.”** broad roles and fan-out can be fleet-wide.
14. **“Average cost predicts spend.”** tails, retries, logs, events, and egress matter.
15. **“Portable language means portable system.”** trigger and managed-service semantics remain.
16. **“Provider success means business completion.”** asynchronous and external outcomes still reconcile.

## Worked Examples

### Example 1

**Situation.** A workload receives 250 invocations/s with mean duration 0.4 seconds.

**Reasoning.** Little's law estimates mean concurrency $250(0.4)=100$. A burst at 800/s, 99th-percentile duration 1.2 s, or retries can require much more. Reserve and cap concurrency against the database, not only the function platform.

**Conclusion.** Mean concurrency is a baseline, not a safe configured maximum.

### Example 2

**Situation.** Every event emits three new events for four generations.

**Reasoning.** Including the original, total is $1+3+9+27+81=121$. One hundred original events can cause 12,100 events before retries. Add causation depth, filters, output separation, budgets, and an independent stop.

**Conclusion.** Modest branch factors create large event amplification quickly.

### Example 3

**Situation.** Two image handlers receive the same object-created event.

**Reasoning.** Both derive one result identity from source object and immutable version. A conditional write elects one output; the loser observes completion. Unsupported input enters an owned terminal state. Neither relies on one delivery or warm memory.

**Conclusion.** Durable identity and conditional effect make redelivery safe within the stated store boundary.

### Example 4

**Situation.** A function charges a payment provider and times out before recording success.

**Reasoning.** Runtime retry may repeat the charge unless the same payment intent reaches the provider. Record intent before dispatch, reuse it, query provider status, and expose outcome unknown until reconciled. Increasing timeout changes waiting, not remote truth.

**Conclusion.** Managed retry cannot resolve ambiguous external effect without end-to-end identity.

### Example 5

**Situation.** A warm runtime retains the previous tenant's profile in a global cache.

**Reasoning.** The platform may reuse the process for a different tenant. Key cache entries by authenticated tenant and data version, clear unsafe request state, and make cache misses correct. Never place secrets or mutable authorization decisions in unbounded globals.

**Conclusion.** Warm reuse is a performance opportunity and a data-isolation risk.

### Example 6

**Situation.** A schema producer renames `customer_id` to `account_id` and removes the old field immediately.

**Reasoning.** Older consumers fail or misroute. Add the new field with defined equivalence, deploy tolerant consumers, measure use, then publish a new semantic version if meaning differs. Keep private database naming out of the public event.

**Conclusion.** Independent deployment requires compatibility and semantic ownership, not parser tolerance alone.

### Example 7

**Situation.** A queue launches 5,000 handlers against a database limited to 400 safe concurrent operations.

**Reasoning.** Unbounded concurrency causes connection exhaustion, timeouts, and retries. Reserve handler concurrency below the tested database budget, batch where valid, partition fairly, and let queue age expose the capacity gap.

**Conclusion.** Elastic execution must be shaped by the narrowest downstream capacity.

### Example 8

**Situation.** An expired evacuation alert is redriven from dead letter six hours later.

**Reasoning.** Original identity prevents duplicate classification but does not make the alert current. Revalidate incident authority, supersession, geography, and expiry; resolve it as expired or replace it with a new authorized message. Preserve audit.

**Conclusion.** Replayability is not continued business validity.

### Example 9

**Situation.** Two architectures run 10 million requests: one at 100 ms and one at 500 ms mean duration with equal configured resource.

**Reasoning.** In the simplified duration-metered term, the second consumes five times the execution resource-time before considering request, logging, event, or egress charges. Tail retries and provisioned capacity can alter the comparison; current prices must be applied separately.

**Conclusion.** Architectural cost follows total metered work and amplification, not an invocation label.

### Example 10

**Situation.** A region fails after replicating events but before marking which region owns consumption.

**Reasoning.** Both regions may process the same identities. Advance a consumption authority epoch, fence stale handlers where exclusive effects require it, preserve deduplication across regions, and reconcile in-flight external actions before broad replay.

**Conclusion.** Multi-region event storage does not itself establish one processing authority.

## Cross-Program Connections

- **Cloud Engineering:** owns provider runtime, event, data, identity, regional, quota, and cost mechanics.
- **Platform Engineering:** owns deployment, runtime policy, concurrency, observability, developer interfaces, and guardrails.
- **API and Service Engineering:** owns synchronous/pending contracts, idempotency, status resources, and client behavior.
- **Data Engineering:** owns streams, partitions, replay, event time, watermarks, and pipeline semantics.
- **Distributed Systems Engineering:** owns delivery, consensus, replication, clocks, and failure models.
- **Security Engineering:** owns trigger identity, runtime roles, secrets, network, supply chain, and compromise containment.
- **Software Delivery and Reliability Engineering:** owns releases, SLOs, load tests, cost incidents, recovery, and evidence.
- **Database Engineering:** owns state, transactions, conditional effects, outbox/inbox, deduplication, and recovery.

## References

1. Eric Jonas et al., “Cloud Programming Simplified: A Berkeley View on Serverless Computing,” 2019. <https://arxiv.org/abs/1902.03383>
2. Paul Castro et al., “The Rise of Serverless Computing,” *Communications of the ACM* 62(12), 2019. <https://doi.org/10.1145/3368454>
3. Ioana Baldini et al., “Serverless Computing: Current Trends and Open Problems,” in *Research Advances in Cloud Computing*, Springer, 2017. <https://doi.org/10.1007/978-981-10-5026-8_1>
4. Cloud Native Computing Foundation, “CloudEvents Specification,” version 1.0.2, 2022. <https://github.com/cloudevents/spec/tree/v1.0.2>
5. Cloud Native Computing Foundation, *CNCF Serverless Whitepaper*, version 1.0, 2018. <https://github.com/cncf/wg-serverless/tree/master/whitepapers/serverless-overview>
6. Gregor Hohpe and Bobby Woolf, *Enterprise Integration Patterns*, Addison-Wesley, 2003.
7. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly Media, 2017.
8. Betsy Beyer et al., eds., *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly Media, 2016. <https://sre.google/sre-book/table-of-contents/>

## Exercises

### Exercise 1

Define serverless, FaaS, event-native architecture, event, command, notification, envelope, trigger, cold start, warm reuse, reserved concurrency, fan-out, eventual completion, provider limit, event age, and amplification ratio.

### Exercise 2

A handler receives 600 events/s with mean duration 0.25 s. Estimate mean concurrency. Then each original event emits two events per generation for five generations. Calculate total events including the original and work for 1,000 originals before retries. State the model limitations.

### Exercise 3

Diagnose an event workflow that relies on warm globals, uses a new ID per retry, has unlimited concurrency, writes back into its own trigger bucket, logs full payloads, exposes no status, and redrives dead letters blindly. Provide a safe design and evidence.

### Exercise 4

Compare a long-running synchronous service, direct event-triggered functions, queued functions, retained streams, and managed workflows for image processing, payments, telemetry, document conversion, and approval. Address state, latency, duplicate effects, scaling, cost, security, and recovery.

### Exercise 5

Design a serverless and event-native architecture for an international organ-transport coordination system spanning donor hospitals, laboratories, aircraft, couriers, customs, recipient teams, location and temperature sensors, consent, and strict time windows. Cover authorities, events and commands, identity, workflow, ordering, concurrency, privacy, residency, expiry, external effects, offline links, security, recovery, evidence, and human control.

## Answers to the Exercises

### Answer 1

**Serverless** delegates much runtime capacity operation to a provider while application responsibility remains. **FaaS** executes bounded handlers on demand. **Event-native architecture** makes durable asynchronous events and state transitions primary boundaries. An **event** states a fact, a **command** requests action, and a **notification** signals information. An **envelope** carries identity and routing/schema metadata. A **trigger** connects delivery to execution. A **cold start** initializes execution; **warm reuse** reuses an instance. **Reserved concurrency** bounds or guarantees execution capacity. **Fan-out** creates multiple downstream actions. **Eventual completion** finishes after initiation through visible state. A **provider limit** is an enforced current service boundary. **Event age** measures age from a declared time. **Amplification ratio** compares downstream work with original intents.

### Answer 2

Mean concurrency is $L=600(0.25)=150$. With branch factor 2 and depth 5, total per original is $1+2+4+8+16+32=63$, so 1,000 originals cause 63,000 events before retries. The model assumes stable arrival and mean duration for concurrency, constant branching, no filtering, no cycles beyond depth, and one unit of work per event. Bursts, duration tails, cold starts, batches, duplicate delivery, retries, unequal handlers, downstream limits, and quota behavior require additional evidence.

### Answer 3

Make correctness begin from an empty or reused runtime; key any safe cache by tenant and version and clear request state. Assign one durable event and business identity, preserve it across trigger and downstream retries, and conditionally record terminal effects. Separate input and output locations, carry causation and depth, cap fan-out, and provide an independent stop for recursion. Insert a bounded queue and reserve concurrency below downstream capacity with tenant fairness and cost alarms.

Minimize and protect payloads; logs carry safe identifiers, not full private content. Expose accepted, pending, completed, rejected, expired, compensating, and unknown states. Validate envelope, schema, size, authorization, and expiry. Dead letters have scoped access, retention, an owner, correction/compensation, and same-identity redrive only after current validity checks. Evidence joins event, cause, attempt, runtime/artifact version, cold/warm observation where available, concurrency, downstream call, cost unit, control change, dead-letter decision, and business outcome. Test duplicate, lost acknowledgement, cold burst, poison, recursion, compromise, quota, old schema, and regional recovery.

### Answer 4

A long-running service suits stable connections, low-latency synchronous outcomes, and controlled runtimes but requires provisioned capacity. Direct event functions minimize wiring for bounded reactions but transmit bursts and obscure retry ownership. Queued functions add backpressure and concurrency shaping at the cost of age and dead-letter lifecycle. Retained streams suit ordered partitions, replay, and many projections but demand schema, privacy, retention, and replay discipline. Managed workflows persist multi-step state and compensation but add transition cost and provider semantics.

Image conversion often fits queued functions; payments need durable intent and external reconciliation regardless of compute; telemetry fits retained streams and bounded functions; document conversion needs size/duration checks and may require a service for long jobs; approval needs durable workflow and human states. Evaluate cold and tail latency, state authority, duplicate effects, downstream capacity, workload cost, identity and secrets, schema, regional behavior, portability, and recovery—not just code size.

### Answer 5

Consent, donor and recipient clinical eligibility, allocation, and custody each have named authorities. Publish immutable versioned facts such as test result accepted, package sealed, custody transferred, and temperature observation; send commands such as request aircraft, acknowledge handoff, or prepare theatre to intended authorities. Every envelope carries case-safe identity, source, type, subject, schema, causation, event/publication time, authority epoch, privacy class, and signature without unnecessary patient identity.

A durable workflow records offers, acceptance, deadlines, laboratory prerequisites, customs, transport legs, custody, recipient readiness, cancellation, exception, and terminal outcome. One business identity survives provider and handler retry. Queues isolate each constrained organization and cap concurrency; strict order applies per organ/custody chain, while sensor telemetry partitions by device and time. Cold execution retrieves current authenticated state; no warm cache grants consent or custody. Expired offers and commands cannot execute after deadline without new clinical authority.

Sensitive data remains in compliant regional stores; events carry minimal references and scoped access. Offline couriers and aircraft gateways retain signed bounded commands and observations, then deduplicate on reconnect. Temperature events may arrive late but cannot overwrite a newer validated chain silently. External calls to airlines, customs, laboratories, and messaging preserve identity and outcome-unknown reconciliation. Fan-out to candidate teams is bounded and revoked explicitly when allocation closes.

Runtime roles, event publishers, subscribers, keys, artifacts, egress, and dead-letter access use least privilege. Compromised events face signature, schema, case, range, and authority checks. Evidence records workflow and event identities, authority/policy/schema versions, deadlines, event age, handler attempt and artifact, queue/concurrency, custody signatures, sensor provenance, external outcome, human decision, and terminal clinical/logistical state. Tests cover duplicate offer, consent withdrawal, late lab result, cold burst, lost handoff response, sensor flood, stale aircraft command, customs outage, region loss, key compromise, and replay. Named transplant coordinators and clinicians retain scoped, time-bounded manual authority and an independent stop path.
