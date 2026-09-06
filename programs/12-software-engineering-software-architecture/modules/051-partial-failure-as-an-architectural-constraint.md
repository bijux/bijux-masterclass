---
module_id: SARCH-051
program: Software Engineering: Software Architecture
level: 2
module_number: 51
title: Partial Failure as an Architectural Constraint
status: complete
last_verified: 2026-09-06
---

# Partial Failure as an Architectural Constraint

## One-Page Review

### Governing question

How should an architecture preserve bounded, diagnosable outcomes when some participants, links, control planes, regions, or observations fail while the rest of the system continues—and the caller cannot always know whether a remote effect occurred?

### Essential definitions

- A **fault** is an hypothesized cause, an **error** is an incorrect internal state, and a **failure** is externally observable deviation from the promised service.
- **partial failure** means some components or communications fail while others remain active; it creates disagreement and uncertainty, not merely reduced capacity.
- A **failure model** states which faults and timing behaviors a design claims to tolerate.
- **omission failure** loses a send, receive, or response; **crash failure** stops a participant; **timing failure** violates a required time bound; **Byzantine failure** permits arbitrary or malicious behavior.
- **failure detector** means evidence used to suspect failure; a timeout observes elapsed time, not cause or remote state.
- **ambiguous outcome** means the caller cannot distinguish whether an externally visible effect occurred.
- An **end-to-end deadline** is the remaining time budget for a whole operation; a per-attempt timeout bounds only one attempt.
- **idempotency identity** lets repeated delivery refer to one intended effect; idempotent transport does not automatically make business semantics idempotent.
- A **retry storm** is self-amplifying work caused by retries during degraded capacity.
- **containment boundary** limits resource exhaustion, failure propagation, authority, or recovery scope.
- **degraded mode** deliberately provides a narrower service under stated safety and freshness limits.

### Central model, mechanism, or theorem

For a series path of $n$ independently modeled required components with availabilities $a_i$, simplified path availability is

$$
A_{path}=\prod_{i=1}^{n} a_i.
$$

Eight required components each at $0.999$ yield $0.999^8\approx0.99203$, not $0.999$. Real faults are correlated and requests use different paths, so this is an exposure model, not a production forecast.

If each attempt independently needs retry with probability $q<1$ and retries are unbounded, expected attempts are $1/(1-q)$. At $q=0.2$, expected work is $1.25$ attempts per original request. Independence, infinite patience, and stable capacity fail during incidents; bounded retry budgets, deadlines, jitter, admission, and recovery are required.

### Critical invariants

- every remote call admits success, explicit rejection, known non-execution, ambiguous outcome, and invalid-response reasoning where applicable;
- timeouts and connection errors never prove that a remote effect did not occur;
- retry identity represents one business intent across all attempts and hops;
- an end-to-end deadline bounds queueing, attempts, backoff, and downstream work;
- retry, hedge, fan-out, and replay load fit a declared capacity and amplification budget;
- concurrency and state invariants remain valid when messages are delayed, duplicated, reordered, or redelivered;
- containment prevents one dependency from consuming all threads, connections, memory, queue space, or recovery attention;
- degraded behavior states which guarantees, data ages, features, and authorities remain;
- control-plane loss is separated from serving-plane behavior;
- detection, containment, recovery, and reconciliation have owners and durable identities;
- recovery from backup or failover preserves fencing, authority, compatibility, and evidence;
- common-mode and correlated failures are modeled, not multiplied away as independent probabilities;
- safety and security policy cannot silently weaken because a dependency is unavailable;
- tests inject failure at boundaries and verify user and domain outcomes, not only process survival.

### Common failures

Common failures include treating timeout as non-execution; retrying with a new identity; multiplying retries at every layer; giving each hop the full user deadline; waiting forever to preserve consistency; using circuit breakers without capacity or recovery design; sharing one connection pool across unrelated dependencies; declaring “read-only mode” while writes leak through another path; failing open on authorization outage without policy; promoting two regional writers without fencing; restoring stale configuration with new data; letting poison messages block a partition; and calling a process healthy while its capability cannot reach a terminal outcome.

### Compact example

A payment request reaches the provider, which commits the charge, but the response is lost. The caller's 800-ms timeout expires. Retrying with a new payment ID can double-charge; reporting failure can trigger another user attempt. The system records one payment intent and attempt identity before sending, returns `outcome_unknown`, queries or reconciles under the same identity, and permits only authorized repair. The timeout bounded waiting; it did not reveal provider state.

### Connections

[SARCH-011](011-availability-and-recovery-tactics.md) supplies foundational tactics; [SARCH-043](043-synchronous-request-response-integration.md) and [SARCH-044](044-asynchronous-messaging-integration.md) supply connector semantics; [SARCH-048](048-deployment-units-and-release-independence.md) supplies mixed-version recovery. [SARCH-052](../ROADMAP.md) next examines consistency and availability trade-offs. Distributed Systems Engineering owns formal distributed algorithms; this module owns architectural consequences.

## Governing Question

Inside one process, failure often stops the computation and returns control to one runtime. Across processes and authorities, one participant can continue after another times out, a request can arrive after its caller gives up, and observers can disagree about which state is current. The system must act before perfect knowledge is available.

Partial failure is therefore an architectural constraint, not an exception-handler detail. It shapes interfaces, state machines, deadlines, identities, capacity, data authority, deployment, security, observability, recovery, and human operation.

## Why This Matters

Distributed systems usually spend most of their time on normal paths, but their worst incidents emerge from combinations: slow dependency plus retries, partial rollout plus stale schema, control-plane outage plus cold restart, regional isolation plus duplicate authority. Mechanisms intended to improve reliability can amplify the incident.

Users care about terminal outcomes. “The request timed out” is not enough when money moved, an order shipped, a medication was administered, or a command reached machinery. Architecture must preserve durable intent, honest uncertainty, and a path to reconciliation.

## Prerequisites and Retrieval

Retrieve availability, reliability, latency, deadline, timeout, retry, queue, idempotency, concurrency, transaction, replication, failover, recovery point, recovery time, load shedding, backpressure, circuit breaker, bulkhead, region, control plane, data plane, trust boundary, and evidence.

From SARCH-011 through SARCH-018 retrieve quality tactics; SARCH-024 through SARCH-028 provide runtime, deployment, data, and operational views; SARCH-041 through SARCH-047 provide authority and integration failure; and SARCH-048 through SARCH-050 provide release, configuration, and end-to-end capability tracing.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish fault, error, failure, suspicion, and partial failure;
2. state crash, omission, timing, arbitrary, and correlated failure assumptions;
3. model ambiguous remote outcomes without equating timeout with failure;
4. allocate end-to-end deadlines and bounded retry budgets;
5. design business idempotency across delivery attempts and hops;
6. reason about retry, hedge, fan-out, and recovery amplification;
7. choose containment and degraded modes from domain and safety obligations;
8. separate control-plane availability from data-plane continuity;
9. design failover, fencing, reconciliation, and restoration under partial knowledge;
10. review evidence and failure-injection results without claiming universal resilience.

## Core Exposition

**Begin with a failure model.** “Highly available” says little unless the design states which failures it handles. Crash-stop assumes a failed process stops and does not return. Crash-recovery permits return with durable state. Omission loses communication. Timing faults make correct answers too late. Byzantine behavior may be arbitrary or malicious.

Choose models per boundary. A managed database might be modeled for crash and failover in normal design while its administrative plane is treated as a compromise boundary. A third-party response may be authenticated yet semantically wrong. Do not pay Byzantine-tolerance cost without a threat, and do not assume honest crash behavior across hostile boundaries.

**Separate fault, error, and failure.** A corrupted memory bit is a fault; an invalid in-memory balance is an error; returning the wrong balance is a failure. Detection can interrupt this chain. Conversely, an internal exception that is contained and retried within contract may not be an externally visible failure.

This distinction directs evidence. Hardware telemetry may expose faults, invariant checks expose errors, and service-level measures expose failures. One metric cannot substitute for the others.

**Treat failure detection as suspicion.** A timeout states that a result did not arrive before a local deadline. Causes include lost request, lost response, slow queue, overloaded callee, network partition, scheduler pause, clock issue, or caller overload. The callee may have completed.

Failure detectors trade speed against false suspicion. A short timeout contains latency but can retry healthy slow work. A long timeout consumes resources and violates the user deadline. Use observed latency distributions and business consequences, then test degradation; do not derive semantic truth from elapsed time.

**Enumerate remote-call outcomes.** Before send, the caller may know no request left. After accepted send, it may receive success, explicit rejection, invalid response, or no usable response. Once an effect-capable request might have reached the callee, non-execution is not generally knowable from silence.

Represent ambiguity as domain state. Preserve intent and attempt identity, expose a status query or reconciliation path, and define who may decide. Hiding ambiguity behind `500` invites duplicate human or automated action.

**Use end-to-end deadlines.** A user or upstream workflow owns a total time budget. Propagate remaining deadline, subtract local work and safety margin, and reject work that cannot finish usefully. Each hop must not reset the original budget.

Per-attempt timeout, maximum attempts, backoff, queue wait, and processing must fit. Cancellation is advisory across remote boundaries: a timed-out caller cannot assume downstream work stopped. Downstream components should check deadline before starting expensive or irreversible work when semantics allow.

**Make retries bounded and owned.** Retry only transient conditions for operations safe under repeated delivery. Bound attempts and elapsed time, add randomized backoff, respect server overload signals, and enforce a system-wide retry budget.

Retries at client, gateway, service, library, and queue can multiply. Three layers with three attempts can create up to $3^3=27$ downstream attempts for one original request. Choose one owning layer where possible and expose attempt counts.

**Design idempotency at the business boundary.** HTTP method labels, message delivery modes, or database upserts do not automatically prevent duplicate business effects. Use an identity representing one intent, bind it to authenticated principal and normalized request, and durably record result or state.

Reject reuse with different parameters. Retain identity long enough to cover retries, delayed delivery, recovery, and user resubmission. Downstream providers need the same or safely mapped identity; otherwise one idempotent hop can feed a non-idempotent next hop.

**Budget amplification.** Fan-out, retries, hedging, cache miss, replay, and failover all add work precisely when capacity may be reduced. Model upper bounds and expected work, then test correlated degradation.

Admission control, load shedding, queue limits, and per-tenant fairness protect essential work. Unlimited queues convert overload into latency and stale work. Reject or degrade before resource exhaustion destroys recovery.

**Contain failure.** Bulkheads separate thread, connection, memory, queue, and deployment capacity. A dependency-specific pool prevents one slow provider from consuming every worker. Cells or regions limit blast radius. Separate credentials and configuration constrain compromise.

Containment costs idle reserve and complexity. A shared pool can use capacity efficiently in normal operation; partitioned pools preserve independence. Size from criticality, traffic, and failure scenarios, and allow controlled borrowing only if it cannot starve essential paths.

**Use circuit breakers as stateful admission.** A breaker stops some calls after evidence of likely failure, probes recovery, and prevents repeated expensive waits. It does not repair the dependency, guarantee fast recovery, or make fallback correct.

Choose thresholds, sampling, scope, open duration, probe concurrency, and observability. Fleet-wide synchronized breakers can produce oscillation. Per-instance breakers can overload a recovering dependency with simultaneous probes. Randomization and centralized or dependency-provided admission may help.

**Design degraded modes semantically.** A fallback must be valid for the operation. Cached catalog data may support browsing while stale authorization cannot safely permit payment. Read-only mode must identify every write path and the freshness of reads.

State which features remain, which data may be stale, which users are included, which guarantees weaken, who authorizes entry, how mode is visible, and how exit reconciles state. Silent degradation is deceptive and hard to recover.

**Separate control and data planes.** A serving process may continue with locally validated routes and configuration during control-plane loss. Cold starts, scale-out, certificate rotation, or policy expiry may still fail. “Existing traffic continues” is narrower than “the system is available.”

Map bootstrap and lease dependencies. Test loss while warm and restoration from zero. Prevent a recovering control plane from overwhelming every consumer with simultaneous refresh.

**Handle asynchronous partial failure.** Queues preserve work across consumer failure but introduce duplicates, delay, reordering, poison messages, redelivery, retention, and uncertain producer acknowledgement. Durable publish may be ambiguous unless producer and broker share a transaction or reconciliation protocol.

Consumers record business identity and outcome durably. Dead-letter handling needs ownership and safe redrive. A poison message should not block unrelated partitions indefinitely; skipping it must not silently violate ordering invariants.

**Protect state transitions.** Partial failure can split a workflow between authorities. Prefer local transactions for local invariants, explicit state machines, conditional writes, outbox/inbox patterns where appropriate, and reconciliation for cross-authority gaps.

Compensation is a new business action, not time reversal. It can fail and may not restore the original world. Record compensating authority, financial or legal meaning, and user-visible outcome.

**Design failover with authority.** Redundant replicas improve availability only when routing, data, identity, configuration, capacity, and operator authority can move safely. Two sites accepting conflicting writes can be worse than one unavailable site.

Use leases, epochs, fencing tokens, quorum rules, or external authority appropriate to the design. Account for stale clients and isolated old leaders. Failback is another migration requiring evidence, not an automatic return to normal.

**Model correlated and common-mode failure.** Independence assumptions fail when services share region, network, identity, DNS, artifact, library, configuration, operator, quota, or provider. A product of individual availability numbers can understate common exposure.

Draw common dependencies and fault domains. Test provider-wide throttling, certificate expiry, bad configuration, shared rollout, and operator error. Diversity can reduce common mode but increases compatibility and operational cost.

**Preserve security under failure.** Authorization, revocation, key, time, and audit services can fail partially. Decide which operations fail closed, use bounded cached decisions, or enter delegated emergency authority. Scope by harm, identity, data sensitivity, and reversibility.

Attackers can trigger expensive retries, force fallback, fill queues, or exploit recovery credentials. Authenticate failure signals where possible, rate-limit identities, protect break-glass access, and audit degraded operation. Availability tactics are part of the threat surface.

**Observe causal state, not just health.** Record request and business identity, attempt, deadline, dependency, revision, queue age, breaker state, outcome class, and reconciliation state without leaking secrets. Distinguish caller cancellation, local rejection, remote decline, timeout, and unknown effect.

Health endpoints should reflect declared serving capability. A process can be alive while unable to complete essential work. Avoid making every dependency failure mark every instance unready and trigger a restart storm.

**Recover deliberately.** Recovery order follows authority and dependency, not convenience. Restore identity and configuration foundations, authoritative data, essential control, and serving paths with capacity limits. Validate versions and fencing before admitting writes.

Reconcile work created before, during, and after failure. Drain retries and queues gradually. Preserve incident evidence. Declare recovery only when business state and user outcomes are understood, not merely when dashboards turn green.

**Test partial failure as combinations.** Inject delay, omission, reset, duplicate, reordering, crash, disk full, stale configuration, expired credential, quota, corrupt response, region isolation, and recovery. Combine failures with load and deployment skew.

State the experiment boundary, tool versions, expected invariant, observed behavior, and limitations. Passing one injected case proves only that case in the tested environment. Expand tests when a defect suggests a class.

## Definitions and Notation

Let:

- $a_i$ be modeled availability of required path component $i$;
- $A_{path}$ be simplified availability of a series path under independence;
- $q$ be independent retry probability per attempt in a geometric model;
- $N$ be attempt count, with $\mathbb{E}[N]=1/(1-q)$ under the model;
- $D$ be end-to-end deadline and $d_i$ the budget allocated to activity $i$;
- $F$ be a declared set of faults covered by a failure model;
- **ambiguous outcome** mean effect occurrence cannot be determined from current evidence;
- **fencing token** mean a monotonically ordered authority token used to reject stale actors;
- **load shedding** mean deliberate rejection of lower-priority work to preserve bounded essential service;
- **reconciliation** mean comparing authorities and evidence to identify and repair divergent outcomes;
- **common-mode failure** mean one cause defeats multiple supposedly redundant elements.

The inequality $\sum_i d_i\le D$ is necessary for a deterministic budget allocation but not sufficient for the deadline: queueing, scheduling, network variation, and unmodeled work still matter.

## Mechanisms, Invariants, or Proof Structure

### Remote-effect protocol

1. Authenticate the caller and validate one durable business intent identity.
2. Record intent and current state before effect-capable dispatch where the design requires it.
3. Send the same downstream identity with bounded deadline and attempt metadata.
4. Treat explicit valid response according to contract.
5. On silence after possible send, record ambiguous outcome rather than inferred rejection.
6. Query, consume callback, or reconcile with the remote authority under the same identity.
7. Permit retry only when identity semantics prevent duplicate intended effect.
8. Reach a terminal state or escalate to bounded authorized manual repair.

### Retry-amplification derivation

If each attempt independently succeeds with probability $1-q$, then $P(N=k)=q^{k-1}(1-q)$ for $k\ge1$. The geometric expectation is $1/(1-q)$. At $q=0.2$, this gives $1.25$. During overload, $q$ rises as retries add work, violating independence and fixed $q$; the formula warns about amplification but cannot predict the feedback loop.

### Partial-failure review

1. State actors, business invariants, terminal outcomes, and tolerable degraded states.
2. Draw required dependency paths, authorities, failure and trust domains.
3. Assign a failure model to every connector and participant.
4. Enumerate known success, known rejection, ambiguity, invalid response, and lost progress.
5. allocate deadline, capacity, queue, and retry budgets end to end;
6. define identity, deduplication, ordering, concurrency, fencing, and reconciliation;
7. define containment, admission, fallback, and security behavior;
8. define observability, owner, operator authority, and recovery sequence;
9. test failures with load, skew, rollout, cold start, and restoration;
10. record evidence scope and unresolved risks.

### Invariants

- no silence-to-non-execution inference;
- no new business identity for a retry of the same intent;
- no retry or queue policy without a bounded capacity consequence;
- no failover writer without current authority and stale-writer fencing;
- no degraded mode without explicit guarantee and exit semantics;
- no recovery declaration before reconciliation of durable business outcomes.

## Alternatives and Trade-Offs

| Mechanism | Benefit | Failure cost | Evidence needed |
|---|---|---|---|
| immediate failure | releases resources | rejects recoverable work | explicit outcome and client behavior |
| bounded retry | masks transient omission | amplification and duplicate effects | identity, attempts, deadline, load |
| queue | durable decoupling and leveling | delay, duplicates, poison work | age, redelivery, outcome, redrive |
| circuit breaker | avoids repeated waits | false opens, oscillation, probe surge | state, dependency recovery, user result |
| bulkhead | contains exhaustion | stranded capacity | pool saturation and priority behavior |
| cached fallback | serves during dependency loss | stale or unauthorized result | age, policy, provenance, scope |
| fail closed | protects forbidden action | loss of essential service | harm and emergency-authority analysis |
| degraded operation | preserves essential subset | weaker guarantees and reconciliation | visible mode, outcomes, exit test |
| active-passive failover | simpler write authority | promotion time and idle cost | fencing, capacity, restoration |
| active-active | low regional failover latency | conflict and common-control complexity | partition and convergence tests |

Mechanisms compose and interact. Review the combined feedback loops, not a checklist of individually fashionable tactics.

## Failure Modes and Misconceptions

1. **“Timeout means failure.”** It means no acceptable response arrived before a local limit.
2. **“Retry means resilience.”** It can duplicate effects and overload reduced capacity.
3. **“Idempotent HTTP method means idempotent business action.”** Application identity and state still decide effects.
4. **“Exactly once removes duplicates.”** Delivery labels do not erase crash boundaries or external side effects.
5. **“A queue makes work reliable.”** Poison, expiry, duplicate, and unowned backlog remain.
6. **“Circuit breaker is a fallback.”** It is admission state; fallback correctness is separate.
7. **“Bulkheads always improve utilization.”** Reserve can sit idle; containment is the purchased property.
8. **“Health means capability.”** A live process may be unable to achieve essential terminal outcomes.
9. **“Fail closed is universally safe.”** Service loss can create clinical or physical harm.
10. **“Control-plane loss leaves service unaffected.”** cold start, scale, lease, identity, or policy expiry may fail.
11. **“Two regions double availability.”** shared dependencies and unsafe authority can defeat redundancy.
12. **“Failover is routing.”** data currency, fencing, identity, configuration, and capacity determine safety.
13. **“Compensation rolls back.”** it is a fallible new action with its own semantics.
14. **“Independent probabilities describe incidents.”** common causes dominate many large failures.
15. **“Green infrastructure metrics mean recovery.”** business ambiguity and queued work may remain.
16. **“One chaos test proves resilience.”** evidence is bounded to injected conditions and observed outcomes.

## Worked Examples

### Example 1

**Situation.** Eight required components are each modeled at availability 0.999.

**Reasoning.** Under independent series assumptions, $A_{path}=0.999^8\approx0.99203$. A shared identity outage may fail all eight together, invalidating independence. Reduce required synchronous path, provide valid degradation, and measure actual request paths and common dependencies.

**Conclusion.** Component availability does not transfer unchanged to an end-to-end capability.

### Example 2

**Situation.** A charge request times out after it may have reached the provider.

**Reasoning.** Record `outcome_unknown` under the original payment identity. Query or reconcile the provider. A retry uses the same identity only if the provider contract deduplicates it. Do not report decline or create a new intent.

**Conclusion.** Silence after possible dispatch creates ambiguity, not known failure.

### Example 3

**Situation.** Three layers each permit three total attempts.

**Reasoning.** In the worst nested case one user request creates $3\times3\times3=27$ downstream attempts. Centralize retry ownership, propagate attempt and deadline budgets, shed overload, and honor dependency backpressure.

**Conclusion.** Locally bounded retries can still multiply globally.

### Example 4

**Situation.** Each independent attempt needs retry with probability 0.2.

**Reasoning.** The geometric model gives expected attempts $1/(1-0.2)=1.25$, a 25% work increase. During incident load, retry traffic can raise the failure probability, so the fixed independent model becomes optimistic.

**Conclusion.** Expected retry cost is useful for budgeting but not a stable-overload forecast.

### Example 5

**Situation.** One thread pool serves inventory, recommendations, and authentication calls; recommendations become slow.

**Reasoning.** Blocked recommendation calls exhaust all threads and prevent authentication. Give critical dependencies bounded pools and queues, enforce deadlines, degrade recommendations, and reserve authentication capacity. Observe rejected and saturated work.

**Conclusion.** Resource bulkheads prevent a low-criticality dependency from consuming essential capacity.

### Example 6

**Situation.** Authorization service is unavailable during emergency dispatch.

**Reasoning.** Public administrative actions fail closed. Authenticated field commanders may receive short-lived, scoped offline authority for defined emergency commands, with local audit and later reconciliation. Anonymous or expired identity never inherits that path.

**Conclusion.** Failure policy follows harm, identity, scope, and reversibility—not one global slogan.

### Example 7

**Situation.** A queue consumer crashes after shipping an order but before acknowledging the message.

**Reasoning.** Redelivery is expected. Use one shipment intent identity and record the carrier result. On redelivery, return or reconcile the existing outcome rather than creating another shipment. A database dedupe row alone is insufficient if the carrier received a different identity.

**Conclusion.** End-to-end idempotency must cross the external-effect boundary.

### Example 8

**Situation.** A region is isolated and both sides attempt to become the sole writer.

**Reasoning.** Reachability cannot establish uniqueness. A current epoch or fencing authority must reject the stale writer; if no safe authority is available, restrict one side to read-only or separately scoped work. Reconcile before failback.

**Conclusion.** Redundant capacity without fenced authority can corrupt state.

### Example 9

**Situation.** The configuration plane fails while warm instances serve normally.

**Reasoning.** Existing instances use validated snapshots, but scale-out lacks bootstrap and a certificate expires in two hours. Declare the precise continuity window, preserve capacity, repair control plane, and test cold restoration. Do not claim full availability from current traffic alone.

**Conclusion.** Warm data-plane continuity can hide a shrinking recovery margin.

### Example 10

**Situation.** After recovery, dashboards are green but 4,000 payment intents remain unknown.

**Reasoning.** Pause blind retries, reconcile by durable provider identity, classify success, absence, decline, and unresolved cases, post missing ledger effects idempotently, and authorize manual repair for the remainder. Communicate user outcomes and preserve evidence.

**Conclusion.** Technical recovery is incomplete until ambiguous business state is reconciled.

## Cross-Program Connections

- **Distributed Systems Engineering:** owns failure detectors, consensus, replication, partitions, and formal safety/liveness in depth.
- **Software Delivery and Reliability Engineering:** owns SLOs, incident response, progressive delivery, observability, and recovery practice.
- **API and Service Engineering:** owns deadlines, status semantics, idempotency contracts, rate limits, and client behavior.
- **Database Engineering:** owns transactions, concurrency, durability, replication, backup, and recovery mechanisms.
- **Platform Engineering:** supplies workload isolation, routing, configuration, identity, health, rollout, and failure injection.
- **Security Engineering:** owns degraded authorization, credential failure, adversarial behavior, recovery access, and audit integrity.
- **Network Engineering:** owns loss, delay, reordering, reachability, congestion, routing, and partition mechanisms.
- **Systems Engineering:** extends partial-failure analysis to people, hardware, facilities, and physical safety.

## References

1. Algirdas Avizienis, Jean-Claude Laprie, Brian Randell, and Carl Landwehr, “Basic Concepts and Taxonomy of Dependable and Secure Computing,” *IEEE Transactions on Dependable and Secure Computing* 1(1), 2004. <https://doi.org/10.1109/TDSC.2004.2>
2. Jim Gray, “Why Do Computers Stop and What Can Be Done About It?” Tandem Computers Technical Report 85.7, 1985. <https://jimgray.azurewebsites.net/JimGrayPublications.htm>
3. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly Media, 2017.
4. Michael T. Nygard, *Release It!*, 2nd ed., Pragmatic Bookshelf, 2018.
5. Betsy Beyer, Chris Jones, Jennifer Petoff, and Niall Richard Murphy, eds., *Site Reliability Engineering*, O'Reilly Media, 2016. <https://sre.google/sre-book/table-of-contents/>
6. IETF, *HTTP Semantics*, RFC 9110, June 2022. <https://www.rfc-editor.org/rfc/rfc9110>
7. Pat Helland, “Life beyond Distributed Transactions: An Apostate's Opinion,” *CIDR 2007*. <https://www.cidrdb.org/cidr2007/papers/cidr07p15.pdf>
8. Jeffrey C. Mogul, “Emergent (Mis)behavior vs. Complex Software Systems,” *EuroSys 2006*. <https://doi.org/10.1145/1218063.1217964>

## Exercises

### Exercise 1

Define fault, error, failure, partial failure, failure model, omission, crash-recovery, timing failure, Byzantine failure, failure detector, ambiguous outcome, end-to-end deadline, idempotency identity, retry storm, containment boundary, degraded mode, fencing, and reconciliation.

### Exercise 2

A required series path has five independently modeled components at availability 0.9995. Compute simplified path availability. A retry policy independently retries with probability 0.1; compute expected attempts. State why neither result forecasts an overload incident.

### Exercise 3

Diagnose an order workflow whose mobile client, gateway, order service, and payment library each retry three times; every retry creates a new payment ID; and a timeout is returned as “declined.” Design corrected identity, deadline, retry ownership, outcome states, admission, and reconciliation.

### Exercise 4

Compare immediate failure, bounded retry, queueing, cached fallback, circuit breaker, bulkhead, and regional failover for a clinical scheduling capability. State which combinations you would use for reads, new appointments, authorization, and emergency access, with evidence and limits.

### Exercise 5

Design partial-failure behavior for a flood-control network with central forecasts, regional control rooms, river sensors, intermittently connected gates, local operators, expiring safety rules, and two communication providers. Cover failure models, authority, deadlines, identities, duplicates, stale data, degraded modes, security, containment, failover, recovery, evidence, reconciliation, and manual action.

## Answers to the Exercises

### Answer 1

A **fault** is an hypothesized cause, an **error** an incorrect internal state, and a **failure** externally visible deviation from service. **Partial failure** leaves some participants active while others fail. A **failure model** states covered faults. **Omission** loses communication; **crash-recovery** allows a stopped participant to return with durable state; **timing failure** violates a bound; **Byzantine failure** allows arbitrary behavior. A **failure detector** supplies suspicion, not perfect truth. **Ambiguous outcome** means effect occurrence is unknown. An **end-to-end deadline** bounds the whole operation. **Idempotency identity** binds repeats to one intent. A **retry storm** amplifies degraded load. A **containment boundary** limits propagation or exhaustion. A **degraded mode** offers an explicit narrower contract. **Fencing** rejects stale authority. **Reconciliation** compares authoritative facts and repairs divergence.

### Answer 2

Under independent series assumptions, $A_{path}=0.9995^5\approx0.9975025$, or about 99.75025%. The geometric retry model gives $\mathbb{E}[N]=1/(1-0.1)=1.111\ldots$ attempts. Incidents violate fixed independent assumptions: components share causes, requests take different paths, retries consume reduced capacity, and rising load changes failure probability. The values are planning aids requiring common-mode analysis and load testing.

### Answer 3

Create one authenticated order intent and one payment intent identity before dispatch; reuse them across every delivery and map the provider identity durably. Give the client one total deadline and propagate remaining budget. Let one layer—normally the service with business context—own bounded retries for declared transient conditions; disable multiplicative lower-layer retries or share one attempt budget. A timeout after possible provider send becomes `payment_outcome_unknown`, never `declined`. Return durable status, query or reconcile provider by original identity, and reach paid, confirmed absent, declined, or authorized repair. Add jitter, admission, per-tenant limits, dependency bulkheads, and attempt telemetry. Test delayed response, duplicate delivery, provider success with lost response, overload, and client resubmission.

### Answer 4

For schedule reads, use a bounded local cache with age visible and a breaker around the source; do not show stale availability as confirmed. New appointments use an end-to-end deadline, one durable request identity, bounded service-owned retry before ambiguous booking, and a queue only if `accepted` is clearly distinct from booked. Separate pools protect clinical lookup from notification or analytics. Authorization fails closed for ordinary changes, while predesigned short-lived emergency access may operate under authenticated clinician identity, limited scope, local audit, and later review. Regional failover requires current patient and slot data, fenced write authority, capacity, identity, configuration, and reconciliation; otherwise serve read-only guidance. Evidence includes outcome identity, attempts, cache age, breaker and pool state, effective authority, unknown bookings, reconciliation, and patient impact. No tactic proves clinical correctness without workflow and safety review.

### Answer 5

Model sensor omission, delay, corrupt or implausible readings, regional crash-recovery, link partition, control-plane loss, compromised credentials, and gate actuator ambiguity. Central forecast owns basin guidance; regional rooms own delegated plans; each gate accepts commands only from a current scoped authority epoch, while a named local operator has bounded emergency authority during isolation. Commands carry gate, plan, sequence, expiry, and idempotency identity. A lost acknowledgement after actuation becomes unknown: inspect authenticated gate state or local confirmation before retry.

Deadlines reflect hydrological decision time, not generic network timeouts. Use both providers without assuming independence; reserve local radio or physical procedure. Sensors expose age and confidence; stale forecasts cannot silently drive automatic opening past policy. Bulkheads and admission preserve safety telemetry, while nonessential analytics shed load. Local degraded mode uses signed last-known rules, current local observations, conservative bounds, and visible manual control; expired rules trigger the predefined safe authority path rather than an improvised default.

Regional failover requires fenced command authority and compatible state; central loss must not create two commanders. Recovery restores identity, rules, topology, telemetry, then command paths under rate limits. Reconcile every issued command, observed gate position, override, missed sensor interval, and downstream effect before normal authority resumes. Evidence records artifact and rule revisions, opaque credential versions, authority epochs, deadlines, attempts, readings, commands, acknowledgements, physical confirmation, and operator decisions. Exercises inject partition during actuation, conflicting forecasts, provider common-mode failure, clock error, cold restart, and restoration. Full credit requires physical inspection and human safety authority where digital evidence cannot establish gate state.
