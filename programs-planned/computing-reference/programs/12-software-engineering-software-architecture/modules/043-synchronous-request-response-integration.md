---
module_id: SARCH-043
program: Software Engineering: Software Architecture
level: 1
module_number: 43
title: Synchronous Request-Response Integration
status: complete
last_verified: 2026-09-06
---

# Synchronous Request-Response Integration

## One-Page Review

### Governing question

When should one system wait for another system's response inside a user or machine operation, and how should the architecture bound latency, load, failure, authority, compatibility, and ambiguous outcomes across the resulting dependency graph?

### Essential definitions

- A **synchronous dependency** exists when a caller's progress waits for a callee outcome within the same operation, even if nonblocking I/O implements the wait.
- A **request** communicates intent, target, identity, parameters, context, and sometimes content; a **response** reports a protocol and application outcome.
- A **logical operation** is the caller's intended business action; an **attempt** is one transmission or execution try.
- A **deadline** is the latest useful completion time for an operation; a **timeout** is one participant's local decision to stop waiting.
- **fan-out** occurs when one operation calls several dependencies; **call depth** is the longest nested synchronous path.
- A **hard dependency** must succeed for the caller's required outcome; a **soft dependency** can fail, use a cache, or be omitted under declared policy.
- **idempotency** means repeated execution under the same operation identity has the same relevant intended effect as one execution.
- An **aggregator** combines several provider results; a **gateway** mediates access; an **orchestrator** owns progress of a multi-step process. These roles may coexist but have different authority.
- **backpressure** communicates or enforces that downstream demand must slow; **load shedding** rejects work before overload becomes unstable.
- An **unknown outcome** means available evidence cannot determine whether the remote effect committed.

### Central model, mechanism, or theorem

Model the synchronous integration graph as $G=(V,E)$. Each edge $e$ records provider, contract, hard or soft requirement, deadline budget $b_e$, attempt policy, capacity, identity, authority, and fallback.

For a sequential path $P$, a necessary budget is

$$
\sum_{e\in P}b_e+b_{local}+b_{overhead}\le B.
$$

For parallel required branches, completion waits for the slowest required branch plus aggregation; percentile values do not generally add or take maxima without their joint distribution. A timeout after send maps to several remote states—nonreceipt, queued, executing, committed, or response lost—so retry safety follows from operation identity and effect semantics, not the error label.

### Critical invariants

- require synchronous integration only when the caller needs a current authoritative answer before proceeding;
- distinguish logical operation, attempt, request, connection, trace, session, resource, and effect identity;
- allocate and propagate one end-to-end deadline rather than resetting full timeouts at each hop;
- bound call depth, fan-out, retries, concurrency, queues, payloads, connections, and per-principal work;
- classify hard and soft dependencies by user outcome and define safe degradation;
- treat timeout, disconnect, and cancellation as ambiguous unless the protocol establishes a terminal outcome;
- retry only safe transient failures under stable identity, bounded attempts, backoff, jitter, and server pushback;
- preserve authentication, authorization, data minimization, and trust through every intermediary;
- version request, response, error, policy, and behavior for mixed deployments and rollback;
- place aggregation and orchestration authority explicitly; do not let gateways become hidden domain owners;
- observe phase latency, saturation, attempts, provider outcomes, committed effects, and user outcomes separately;
- test overload, slow and failed dependencies, lost responses, version skew, retry amplification, and recovery.

### Common failures

Common failures include using synchronous calls for notifications or independent reactions; translating every local function into a remote endpoint; resetting timeouts per hop; retrying all failures at every layer; using trace IDs as idempotency keys; treating disconnect as rollback; requiring every optional panel to succeed; making one aggregator a distributed database join; using average latency for tail objectives; trusting all internal callers; forwarding identity through untrusted headers; hiding business policy in a gateway; allowing unbounded connection pools; returning generic errors; and counting attempts as successful user operations.

### Compact example

Checkout has a 700 ms deadline. Local work and edge overhead reserve 120 ms. Price and inventory run in parallel with 250 ms budgets; payment then has 300 ms. The necessary path budget is $120+250+300=670$ ms, leaving 30 ms margin. Recommendations are soft and omitted after 100 ms. If payment times out after send, checkout queries by the same payment operation ID; it neither submits a new charge nor declares rollback.

### Connections

[SARCH-036](036-client-server-architecture.md) establishes generic client-server roles; [SARCH-039](039-microservices-architecture.md) supplies service dependency costs; [SARCH-041](041-system-of-record-boundaries.md) and [SARCH-042](042-shared-database-versus-database-per-service.md) locate authority and data. [SARCH-044](../ROADMAP.md) next examines asynchronous messaging integration. API Engineering owns protocol-level implementation detail.

## Governing Question

Synchronous request-response is the most direct way to ask another boundary for a decision. It fits authentication, current price, inventory reservation, command acceptance, and interactive queries because the caller needs an answer now. Its apparent simplicity hides a dependency: caller latency and availability now include provider, network, intermediaries, identity, and every required downstream call.

The architectural task is to decide which answers must be current, minimize and bound the synchronous graph, preserve authority and identity, and make uncertain outcomes recoverable. The choice is not equivalent to selecting HTTP, RPC, or a blocking thread. It is a causal commitment inside an end-to-end operation.

## Why This Matters

Uncontrolled synchronous integration produces cascading failure. A slow provider fills caller threads and connections; callers time out and retry; retries increase provider load; queues grow; more deadlines expire. Deep chains make every service's maintenance a product outage. Large fan-out turns rare local failures into common user failure.

Correctness also changes. A remote timeout does not reveal whether a payment, booking, or command committed. Mixed versions coexist. Gateways transform requests. Identity and authorization cross trust boundaries. A successful response can arrive after its result is no longer useful.

Well-designed synchronous integration remains valuable. It gives direct authority checks, immediate feedback, simple causal sequence, and bounded contracts. The goal is not to eliminate it but to use it only where its temporal coupling matches the business need.

## Prerequisites and Retrieval

Retrieve client, server, service, request, response, operation, attempt, endpoint, contract, authority, deadline, timeout, cancellation, retry, idempotency, fan-out, call depth, queue, concurrency, backpressure, admission, partial failure, cache, consistency, gateway, aggregator, orchestrator, authentication, authorization, trace, saturation, and service-level objective.

From SARCH-017 retrieve interoperability; SARCH-018 provides observability; SARCH-024 provides runtime interaction views; SARCH-035 provides asynchronous alternatives; SARCH-036 provides client-server semantics; SARCH-039 provides distributed ownership; and SARCH-041 through SARCH-042 provide current authority and data placement.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish synchronous architectural dependency from blocking implementation;
2. decide when a current authoritative response is required;
3. model sequential depth, parallel fan-out, hard and soft edges, and end-to-end budgets;
4. preserve logical operation identity and reason about timeout ambiguity;
5. design bounded retries, deadlines, cancellation, admission, and load shedding;
6. compare direct calls, gateways, aggregators, orchestration, caching, and asynchronous alternatives;
7. preserve security, privacy, authority, and compatibility across hops;
8. design graceful degradation and partial result semantics;
9. observe and test phase, dependency, saturation, effect, and user outcomes;
10. refactor a fragile synchronous graph without hiding consistency or freshness changes.

## Core Exposition

**Define synchrony by progress dependency.** A caller is synchronously coupled when it cannot complete its operation until another participant responds. The implementation can use threads, futures, callbacks, or an event loop; nonblocking I/O changes resource use but not the architectural wait.

Conversely, a caller can synchronously submit a message to a broker yet be asynchronous with respect to business processing. Broker acceptance is not the final business outcome. Name which outcome is awaited.

**Require a current answer for a reason.** Synchronous integration is strongest when a decision must use current authority: authorize access, reserve scarce stock, validate a precondition, or obtain a bounded result the user needs immediately. It is weak for notifications, independent side effects, large processing, or data that can use a projection.

For each call ask: what would be incorrect if the answer were delayed, cached, omitted, or reconciled later? If no concrete consequence exists, asynchronous propagation or a read model may reduce temporal coupling.

**Design coarse operations.** A local object can expose getters cheaply. A remote service should expose meaningful capability. Calling customer, address, limit, balance, and status endpoints sequentially to assess credit leaks provider structure and multiplies failure. `assessOrderCredit` can keep policy with its owner.

Coarse does not mean unbounded. Limit input, output, work, and duration. Use bulk operations for many similar items under one bounded contract instead of repeated chatty calls, while defining partial and per-item outcomes.

**Map the synchronous graph.** Draw callers, providers, gateways, identity, storage, and nested calls. Annotate hard or soft requirement, deadline, timeout, concurrency, retry owner, capacity, authority, version, and fallback. Static source dependencies cannot reveal runtime calls inserted by configuration or intermediaries.

Cycles are especially dangerous. A calls B for authorization while B calls A for profile data. Under load or failure, their pools can wait on each other. Break cycles by relocating policy, publishing stable facts, using a lower-level authority, or changing the boundary.

**Distinguish hard and soft edges.** A dependency is hard relative to a named outcome. Payment authorization can be hard for completing checkout; recommendations are soft. The same provider can be hard for one action and optional for another.

Define degradation before incidents. Omit a panel, use a bounded-stale value, queue intent, restrict an operation, or fail closed. A fallback must be simpler and safe under the same failure; calling another chain with identical dependencies is not resilient.

**Budget from the outside inward.** Begin with the user's or machine's latest useful completion time $B$. Reserve edge, local, serialization, queue, and response overhead. Allocate remaining budget to calls. Propagate the absolute deadline or remaining duration so downstream work stops when no longer useful.

Resetting a full timeout at every hop permits actual work far beyond the objective. A caller with 1 s timeout invoking a provider that starts three 1 s dependencies sequentially can occupy resources for several seconds after the caller leaves.

**Do not add percentiles naively.** Mean sequential times add under compatible definitions. Tail percentiles depend on joint distributions and correlation. Parallel required fan-out waits for the maximum branch, but the percentile of that maximum is not simply the maximum of branch percentiles.

Allocate budgets as engineering constraints, then measure the end-to-end distribution under representative load and failure. Record queue time separately from service time so overload is visible.

**Model fan-out amplification.** One logical operation can produce many calls. If all $n$ independent equal-availability dependencies are required, simplified success is $a^n$. With $a=0.995$ and $n=12$, $a^{12}\approx0.94162$. Correlation and shared infrastructure can make the model optimistic or change it unpredictably.

Fan-out also multiplies connections, authentication, logs, traces, retries, and provider work. Reduce it with aggregation at the correct authority, batch APIs, projections, caches, and optional results.

**Separate logical operation and attempt.** One checkout can cause several payment attempts through retries or hedges. Give the business action a stable identity and each attempt its own transport and trace identity. The provider scopes deduplication by principal, operation, request fingerprint, and retention window.

A trace ID supports observation but is not automatically unique under business rules, retained long enough, or protected from caller reuse. Do not substitute it for an idempotency contract.

**Reason about timeout ambiguity.** A request passes resolution, connection, authentication, send, admission, queue, processing, commit, and response. If the caller stops observing after send, the provider could be at any later state. Timeout proves only that the caller's wait ended.

For read-only queries, retry may be safe but can return a newer result and add load. For effects, use stable identity, atomic deduplication with commit, outcome query, or reconciliation. Never retry a charge under a fresh identity simply because a library labels the error transient.

Birrell and Nelson's RPC work showed how remote calls can resemble procedures while needing binding, retransmission, and failure semantics [1]. The resemblance is useful; pretending remoteness disappears is not.

**Propagate cancellation honestly.** Cancellation tells downstream work it may stop. It does not guarantee interruption, rollback, or removal of external effects. A provider may already have committed or may require cleanup. Define terminal outcome inquiry.

Cooperative cancellation can save resources. Providers check it at safe points and release reservations. A closed socket is a transport observation, not a domain transaction instruction.

**Retry only bounded safe work.** Classify errors into caller-correctable, permanent domain rejection, authentication or authorization, conflict, resource exhaustion, transient unavailability, deadline, cancellation, and unknown outcome. Retry only categories whose contract permits it.

Use capped attempts, one end-to-end deadline, exponential or otherwise justified backoff, jitter, and server pushback. Retry at one coordinated layer. Nested retries multiply. If four layers each make three attempts, the deepest service can see $3^4=81$ attempts for one operation.

**Treat hedging as deliberate duplication.** A hedge sends another attempt before the first finishes to reduce tail latency. It increases load and duplicate risk. Use only for safe idempotent work, after measuring tail behavior, with cancellation, identity, and capacity.

Hedging during overload can worsen the tail it targets. Restrict it to sufficient spare capacity and selected operations, and measure attempts per logical outcome.

**Apply admission before queues collapse.** Every server has finite connections, threads or tasks, memory, CPU, file descriptors, and dependency capacity. Bound request size, concurrency, queue, and per-principal use. Reject early with a stable error and retry guidance only when useful.

Unbounded queues convert overload into latency and memory failure. Little's Law $N=\lambda W$ relates mean in-system work, completed rate, and mean time in a stable system [2]. It does not prescribe queue size or apply unchanged during collapse.

**Coordinate pool budgets.** A service can admit more work than a dependency pool supports, moving the queue to connection acquisition. Thirty caller instances with 40 connections each create potential 1,200 downstream sessions. Capacity planning follows the whole fan-in, not one instance default.

Use bulkheads where workloads need isolation, but avoid tiny pools that cause head-of-line blocking. Measure active, queued, rejected, cancelled, and timed-out work.

**Choose direct calls and intermediaries deliberately.** Direct calls keep dependency ownership visible. Gateways can authenticate, route, limit, translate, and observe. Aggregators can combine results. Orchestrators can own a process. Each adds latency, capacity, failure, security, and compatibility surfaces.

Keep domain decisions with their authority. A gateway may validate a token but should not invent credit or safety policy. An aggregator that joins every private entity becomes a new coupled data layer. State its own contract and failure semantics.

**Design partial results.** Fan-out queries can return complete, partial, stale, or unavailable results. Define which fields are required, source and freshness, error placement, and cache behavior. A top-level 200 response can still contain missing components; clients need machine-readable completeness.

Do not return partial authorization or financial decisions unless the domain explicitly permits it. Partial success is a product semantic, not a generic resilience tactic.

**Cache under authority and freshness rules.** Caches reduce latency and dependency load. Define keys, tenant and authorization variation, validators, expiry, invalidation, stale use, negative caching, and failure. A cache hit is not current authority.

Never share personalized or permission-sensitive responses under an incomplete key. A stale safety or revocation decision can be worse than unavailability. Use current authoritative calls where consequence requires them.

**Version for independent deployment.** Caller, gateway, provider, and dependencies roll at different times. Test old/new combinations and rollback. Add fields with safe defaults, preserve unknown fields where appropriate, and avoid changing units, side effects, error meanings, or validation silently.

Compatibility includes time behavior. A provider that changes a 50 ms operation into a 2 s workflow can break callers without schema change. Publish support windows and observe actual versions, while treating unknown consumers as uncertainty.

**Preserve security end to end.** Authenticate the intended provider and caller workload; preserve the end principal where delegated authorization needs it. Restrict token audience, scope, lifetime, and forwarding. Do not trust arbitrary forwarding headers.

Authorize each operation and resource at the owner. An internal network or mutual channel does not grant business access. NIST SP 800-207 describes zero-trust principles that avoid implicit trust from network location [3].

Minimize request, response, error, log, and trace data. Intermediaries that terminate encryption or inspect content become trust boundaries. Protect credentials and rotate them without breaking mixed deployments.

**Make errors architectural contracts.** Distinguish malformed input, unauthenticated, unauthorized, absent, conflict, precondition failure, rate limit, overload, unavailable dependency, deadline, cancellation, internal failure, and unknown effect. Callers need stable semantics to decide correct action.

Do not expose internal stack traces or provider topology. Preserve enough correlation for support without turning implementation detail into API behavior.

**Observe the operation at several layers.** Record logical operations separately from attempts. Capture resolution, connection, authentication, queue, processing, dependencies, commit, and response where useful. Include provider version, route, deadline remaining, rejection, saturation, and effect identity without secrets.

Distributed traces show sampled paths; they are not an authoritative ledger. A missing span does not prove a call did not occur. Reconcile committed effects by domain identity where correctness matters.

**Test slow, not only failed.** A dependency that fails immediately releases resources; one that responds just after every timeout can cause maximum occupancy and retries. Test delay before receipt, during queue, before and after commit, and during response. Test malformed large responses and slow streaming peers.

Inject overload, connection exhaustion, DNS staleness, credential rotation, gateway change, mixed versions, cancellation, retry storms, and lost responses. Verify user outcomes and resource recovery. A handled exception is insufficient if queues remain full.

**Refactor fragile synchronous graphs.** Start by classifying hard and soft edges and removing calls not needed for the outcome. Coarsen chatty APIs at domain boundaries. Replace stable descriptive reads with projections under freshness contracts. Move independent side effects to durable messages.

Do not convert a hard current-authority decision to asynchronous behavior without changing product semantics. If the user must know whether stock is reserved, return pending with outcome tracking or continue a bounded synchronous reservation; do not report success on message acceptance.

**Know when synchrony is best.** A small, shallow call to a reliable authority with clear timeout, capacity, idempotency, and error semantics is often simpler than asynchronous workflow. Asynchrony adds state, messages, duplicates, and progress handling. Choose based on temporal need and failure consequence.

Architectures can combine: synchronous command acceptance, asynchronous processing, and synchronous outcome query. Name each boundary and what its response establishes.

## Definitions and Notation

Let synchronous integration graph be $G=(V,E)$. Edge $e=(u,v)$ means caller $u$ waits for provider $v$ within the operation. Attributes include $hard(e)$, deadline budget $b_e$, maximum attempts $k_e$, maximum concurrency $c_e$, authority, contract version, and fallback.

For path $P$, necessary allocated time is $B_P=\sum_{e\in P}b_e+b_{local}+b_{overhead}$. It is an allocation model; actual latency distributions, parallelism, queueing, and correlation need measurement.

Logical operation $o$ has attempts $A(o)=\{a_1,\ldots,a_k\}$. Every attempt has transport identity and trace context; all share a stable effect identity only when the contract defines that scope. Remote state belongs to $\{not\_received,queued,executing,committed,rejected,unknown\}$ under an authoritative observer.

For $n$ equally available independent required dependencies with availability $a$, simplified success is $a^n$. When branches are optional, correlated, cached, or degraded, the structure and result differ.

## Mechanisms, Invariants, or Proof Structure

**Need invariant.** Every synchronous edge corresponds to a current result required before the named outcome can proceed. Otherwise its temporal coupling requires separate justification.

**Deadline invariant.** One end-to-end deadline bounds useful work. Each hop receives remaining budget, and local queues or retries do not reset it.

**Identity invariant.** Logical operation, attempt, request, trace, connection, session, principal, resource, and committed effect identities remain typed and mapped explicitly.

**Ambiguous-outcome argument.** After transmission and before a terminal authoritative response, executions with nonreceipt and commit can be observationally identical to the caller. Therefore timeout alone cannot justify a fresh effect, success, failure, or compensation.

**Capacity invariant.** Every queue, pool, payload, fan-out, attempt count, and per-principal workload is bounded. Recovery traffic cannot expand without limit.

**Fan-out derivation.** Under independent equal availability and all-required success, joint success is the product $a^n$. Relaxing any premise changes the calculation.

**Authority invariant.** Gateways, aggregators, caches, and callers cannot silently take over domain decisions owned by providers. Partial or stale results state their authority.

**Compatibility invariant.** Supported caller, intermediary, provider, error, policy, and state versions coexist and roll back under tested semantics.

**Security invariant.** Workload and end-principal identity, authorization, audience, purpose, and delegation survive each trusted hop; location provides no blanket authority.

**Evidence invariant.** Response success, trace completion, retry count, and service SLOs are intermediate observations. The user and business outcome need their own evidence.

## Alternatives and Trade-Offs

| Choice | Advantages | Costs and risks | Prefer when |
|---|---|---|---|
| Direct synchronous call | immediate authority, simple causal path | latency and availability coupling | one bounded current answer is required |
| Gateway-mediated call | common edge security, routing, limits, translation | added hop, trust, capacity, and policy gravity | shared technical mediation is coherent |
| Aggregator | consumer-oriented result and hidden fan-out | bottleneck, partial results, distributed join | several bounded reads form one view |
| Synchronous orchestration | visible sequence and immediate progress | deep dependency and resource holding | short workflow needs immediate decisions |
| Asynchronous workflow | temporal decoupling and durable progress | state, duplicates, lag, and outcome query | work is long or can be pending |
| Cached/projection read | low latency and provider isolation | staleness, invalidation, rebuild | purpose accepts bounded freshness |
| Batch operation | fewer round trips and bounded set processing | larger payload and partial-item semantics | many similar items share authority |
| Retry | recovery from selected transient faults | load amplification and duplicate risk | operation semantics and capacity permit |
| Hedge | tail reduction from redundant attempt | extra load and cancellation complexity | safe reads have measured tail outliers |
| Fail closed | protects high-consequence decisions | reduced availability | missing authority must prevent action |
| Graceful partial result | preserves useful experience | completeness and cache complexity | omitted fields are genuinely optional |

## Failure Modes and Misconceptions

1. **“Async I/O makes the architecture asynchronous.”** The caller still waits for the result.
2. **“HTTP means request-response is appropriate.”** Protocol does not establish temporal need.
3. **“Remote calls are local calls with latency.”** Partial failure and ambiguous effects differ fundamentally.
4. **“Timeout means the provider failed.”** It means the caller stopped observing.
5. **“Cancellation rolls back work.”** It requests stopping and may arrive after commit.
6. **“Retries always improve availability.”** They can amplify overload or duplicate effects.
7. **“Trace ID is an idempotency key.”** Scope, fingerprint, retention, and effect semantics differ.
8. **“Parallel fan-out removes latency.”** Completion still waits for required tails and adds load.
9. **“Average latency predicts user experience.”** Queues and tail distributions control many objectives.
10. **“A gateway owns authorization.”** Edge checks do not replace resource-owner decisions.
11. **“Partial results are always resilient.”** Some decisions are unsafe when incomplete.
12. **“Caches remove dependencies.”** Freshness, invalidation, and authority remain.
13. **“Every service should retry its dependencies.”** Nested policies multiply attempts.
14. **“Health checks prove readiness for every operation.”** Capacity and dependency paths vary.
15. **“A successful response proves the business process completed.”** It proves only the contract's stated outcome.
16. **“Asynchronous replacement preserves semantics.”** Pending state and later failure change the product contract.

## Worked Examples

### Example 1

**Situation.** Checkout has 700 ms total budget. Edge and local work reserve 120 ms; price and stock run in parallel with 250 ms each; payment follows with 300 ms.

**Reasoning.** The necessary longest path is $120+250+300=670$ ms, leaving 30 ms allocation margin. Because price and stock run in parallel, their budgets are not summed, but actual joint tails and aggregation overhead still need measurement. Recommendations are soft and omitted at 100 ms. Payment receives the remaining absolute deadline, not a new 700 ms.

**Conclusion.** The graph fits the allocation narrowly; representative tail and overload tests decide whether the margin is adequate.

### Example 2

**Situation.** A profile page synchronously calls 15 services, all required and independently modeled at availability 0.995.

**Reasoning.** Simplified success is $0.995^{15}\approx0.92757$, or 92.757%. The model omits the page service and shared failures. Classify fields: identity summary may be hard, while badges and recommendations are optional. Build a profile projection for stable descriptive data and query only current authoritative facts that require it.

**Conclusion.** Required fan-out converts strong local availability into weak product availability; reduce the hard graph.

### Example 3

**Situation.** A payment request times out after the server may have committed.

**Reasoning.** The caller retains operation ID `pay-55` and request fingerprint. It queries payment authority or retries the identical request under `pay-55`; the provider atomically returns the stored outcome or applies it once. The caller records `unknown` until authoritative evidence arrives. A new ID could double-charge, and immediate refund could act before any charge exists.

**Conclusion.** Timeout recovery depends on stable effect identity and outcome inquiry, not transport error categories.

### Example 4

**Situation.** Four layers each retry a downstream request up to three total attempts.

**Reasoning.** Worst-case deepest demand is $3^4=81$ attempts per logical operation. During provider overload this delays recovery. Assign retries to one boundary, limit total elapsed time, add jitter, honor overload pushback, and measure attempt amplification. Other layers propagate the failure rather than restarting full budgets.

**Conclusion.** Retry policy must be composed across the call graph as load.

### Example 5

**Situation.** A dashboard waits for sales, inventory, logistics, and recommendations; logistics is slow.

**Reasoning.** Sales and inventory are required for the chosen operational view. Logistics can use a versioned projection up to five minutes old and display its timestamp. Recommendations are omitted. The aggregator returns completeness metadata per section, source version, and stable errors. A later dispatch action calls logistics authority directly and cannot use the stale view.

**Conclusion.** Partial results are safe only when requiredness and authority are defined per user action.

### Example 6

**Situation.** A request has 1 s user deadline, but gateway, service A, and service B each reset a 1 s timeout.

**Reasoning.** Queueing and sequential calls can continue for roughly several seconds, wasting work after the user leaves. Propagate an absolute deadline. Each component subtracts elapsed time and its local reserve; if insufficient time remains, it rejects before starting. Cleanup can continue under a separate bounded lifecycle where correctness requires it.

**Conclusion.** Per-hop timeout resets violate the end-to-end objective even if each local configuration seems reasonable.

### Example 7

**Situation.** An internal gateway authenticates a workload and forwards `X-User: admin` from the original request unchanged.

**Reasoning.** Any caller able to set the header can impersonate an administrator. The trusted edge strips untrusted identity headers, authenticates the principal, creates integrity-protected audience- and scope-bound context, and forwards only necessary claims. Each service authorizes the resource and operation. Logs avoid raw credentials and sensitive attributes.

**Conclusion.** Intermediaries must establish and constrain identity; network placement and forwarded strings are not authority.

### Example 8

**Situation.** Thirty application instances each allow 40 calls to a dependency whose safe concurrency is 300.

**Reasoning.** Potential fan-in is $30\times40=1{,}200$, four times the safe concurrency before retries. Allocate caller budgets whose aggregate respects provider capacity, enforce provider admission, and keep administrative reserve. Queueing at caller can smooth short bursts but must be bounded by deadline. Measure work cost because equal concurrency does not imply equal load.

**Conclusion.** Instance-local pool settings must satisfy an end-to-end capacity model.

### Example 9

**Situation.** A notification email is sent synchronously before an order response can complete.

**Reasoning.** Email does not determine whether the order is valid, and provider delay turns a soft side effect into a hard dependency. Commit the order and publication obligation locally, respond with the order outcome, then let a consumer send email idempotently. Expose notification status separately if users need it. If regulation requires confirmed delivery before completion, that requirement must be explicit and the workflow may remain pending.

**Conclusion.** Independent side effects usually belong outside the synchronous critical path.

### Example 10

**Situation.** A hospital medication service requests current allergy status but the identity and allergy service is unavailable.

**Reasoning.** A stale generic cache could cause harm. The architecture defines a signed bounded local clinical summary with source, patient identity, version, update time, and explicit permitted emergency use. If freshness exceeds the clinical threshold or identity is uncertain, administration fails closed and invokes a human emergency protocol. Calls use one deadline and never infer “no allergy” from timeout or absence.

**Conclusion.** High-consequence synchronous integration needs explicit safe-unavailable behavior, not optimistic degradation.

## Cross-Program Connections

- **API and Service Engineering:** owns HTTP/RPC mechanics, schema, errors, idempotency, resilience, gateways, testing, and observability in depth.
- **Distributed Systems Engineering:** owns partial failure, time, coordination, consistency, failure detectors, and retry consequences.
- **Network Engineering:** owns connection, transport, congestion, loss, DNS, TLS, and path behavior beneath calls.
- **Security Engineering:** identity, delegation, authorization, least privilege, trust boundaries, and data minimization govern every hop.
- **Software Delivery and Reliability Engineering:** SLOs, capacity, load shedding, observability, incident response, rollout, and recovery validate the graph.
- **Database Engineering:** local commit, locks, isolation, idempotency storage, and authoritative outcome queries support service effects.
- **Data Architecture Engineering:** systems of record, projections, freshness, and consumer data contracts determine which reads can leave the critical path.
- **Platform Engineering:** service discovery, identity bootstrap, routing, telemetry, policy, and safe defaults reduce repeated implementation cost.

## References

1. Andrew D. Birrell and Bruce Jay Nelson, “Implementing Remote Procedure Calls,” *ACM Transactions on Computer Systems* 2(1), 1984. <https://doi.org/10.1145/2080.357392>
2. John D. C. Little, “A Proof for the Queuing Formula: L = λW,” *Operations Research* 9(3), 1961. <https://doi.org/10.1287/opre.9.3.383>
3. NIST, *SP 800-207: Zero Trust Architecture*, August 2020. <https://csrc.nist.gov/pubs/sp/800/207/final>
4. IETF, *RFC 9110: HTTP Semantics*, June 2022. <https://www.rfc-editor.org/rfc/rfc9110>
5. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly Media, 2017.
6. Michael T. Nygard, *Release It! Design and Deploy Production-Ready Software*, 2nd ed., Pragmatic Bookshelf, 2018.
7. Betsy Beyer, Chris Jones, Jennifer Petoff, and Niall Richard Murphy, eds., *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly Media, 2016. <https://sre.google/sre-book/table-of-contents/>
8. Gregor Hohpe and Bobby Woolf, *Enterprise Integration Patterns: Designing, Building, and Deploying Messaging Solutions*, Addison-Wesley, 2003. <https://www.enterpriseintegrationpatterns.com/>

## Exercises

### Exercise 1

Define synchronous dependency, logical operation, attempt, deadline, timeout, hard dependency, soft dependency, fan-out, call depth, and unknown outcome. Explain why nonblocking I/O does not remove synchronous architecture.

### Exercise 2

A 900 ms operation reserves 140 ms for local and edge work. Two required parallel calls have 280 ms budgets; a following sequential authority call has 420 ms. Compute the necessary longest-path budget and margin. State four reasons the arithmetic does not prove the percentile objective.

### Exercise 3

A caller retries every timeout three times, its gateway retries twice, and a client library retries twice. Diagnose worst-case attempt amplification and design a coordinated policy for a mutating operation.

### Exercise 4

Compare direct calls, gateway mediation, aggregation, a cached projection, and asynchronous workflow for a travel-booking page that needs fare, seat, payment, reviews, and loyalty information. Define authority, requiredness, freshness, and failure.

### Exercise 5

Design synchronous integration for a wildfire-response system linking dispatch, crews, weather, road closures, aircraft, and public alerts. Bound the call graph and deadlines, define offline and unknown outcomes, identity and authorization, degradation, capacity, asynchronous boundaries, and evidence. Identify a response that must never be inferred from timeout.

## Answers to the Exercises

### Answer 1

A **synchronous dependency** makes caller progress wait for a provider outcome in the same operation. A **logical operation** is intended business work; an **attempt** is one try. A **deadline** is latest useful completion; a **timeout** ends one observer's wait. A **hard dependency** is required for the named outcome; a **soft dependency** may degrade or be omitted. **Fan-out** is the number of downstream branches; **call depth** is the longest nested path. An **unknown outcome** lacks evidence of the remote terminal effect. Futures, callbacks, and event loops avoid blocking a thread, but if the product operation cannot finish before the response, temporal and failure coupling remain synchronous.

### Answer 2

The parallel pair contributes the maximum allocated branch, 280 ms, not twice that value. Necessary longest path is $140+280+420=840$ ms, leaving $900-840=60$ ms margin. This does not prove the percentile objective because branch distributions and correlation are unknown; queueing and unmodeled serialization or network overhead can consume margin; percentile values do not compose by simple addition or maximum; actual work can exceed allocation; retries and contention change distributions; and clock or measurement boundaries may differ. Any four with correct arithmetic earn full credit.

### Answer 3

Interpreting counts as total attempts, worst-case multiplication is $3\times2\times2=12$ attempts for one logical operation. If the numbers meant retries in addition to the first attempt, the contract would need to clarify and the product would be larger. For a mutation, assign one layer retry ownership, propagate one absolute deadline, retry only contract-declared transient failures, use stable operation identity and request fingerprint, store effect and outcome atomically with deduplication, cap attempts and elapsed time, back off with jitter, honor overload signals, and query unknown outcomes. Other layers must not independently retry. Observe logical operations separately from attempts and prevent a new identity after timeout.

### Answer 4

Fare and seat needed for booking come from their current authorities through coarse bounded calls; seat reservation uses stable identity and unknown-outcome inquiry. Payment is a separate authoritative effect and belongs in a durable booking process rather than a deep page-render chain. A gateway can establish identity, rate limits, and routing but does not decide fare or payment. An aggregator can assemble fare and seat options with explicit completeness. Reviews and loyalty display can use timestamped projections or caches; reviews are soft, while loyalty may be soft for display but authoritative for spending points. Long-running confirmation and ticketing proceed asynchronously with a pending booking identity and synchronous outcome query. Failure omits reviews, labels stale loyalty, prevents commitment without known fare/seat, and never treats payment timeout as failure or success.

### Answer 5

Dispatch owns incident and assignment decisions. Crew systems own acknowledgment and local status; aviation authority owns aircraft commitment; road and weather providers own timestamped observations; public alerts require authorized message approval. Keep the immediate dispatch graph shallow: query a local replicated weather/road view under freshness bounds, send idempotent assignment commands to selected resources under one end-to-end deadline, and record accepted, rejected, or unknown outcomes. Never infer that a crew or aircraft is assigned, safe, or unavailable merely from timeout. During disconnection, local incident commanders operate under explicitly delegated authority and later reconcile stable operation IDs and signed logs. Alerts publish asynchronously after an authorized decision, with urgent local channels independent of regional network failure. Workload and end-principal identity, scopes, and jurisdiction are preserved; untrusted forwarding headers are stripped. Bound fan-out, retries, queues, radio/network use, and per-incident resources; shed informational work before safety work. Test partitions, delayed response after commit, duplicate assignment, stale weather, identity rotation, overload, gateway loss, recovery, and manual procedures. Full credit requires current authority for irreversible allocation and honest unknown states.
