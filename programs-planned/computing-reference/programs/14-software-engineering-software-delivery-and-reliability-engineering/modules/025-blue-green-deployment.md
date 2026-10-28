---
module_id: SDRE-025
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 25
title: Blue-Green Deployment
status: complete
last_verified: 2026-09-06
---

# Blue-Green Deployment

## One-Page Review

### Governing question

How can two production-capable environments provide a controlled cutover and credible return path without hiding traffic, state, capacity, or compatibility risk?

### Essential definitions

- **blue-green deployment** maintains an active environment and a separately prepared candidate environment, then changes traffic authority;
- an **environment** includes runtime, configuration, identity, dependencies, capacity, network policy, and observability—not only compute instances;
- **cutover** changes which environment receives authoritative work;
- **switching plane** is the load balancer, gateway, service-discovery, DNS, queue, scheduler, or client mechanism that routes work;
- **draining** stops admitting new work while allowing bounded in-flight work to finish or terminate safely;
- **quiescence** is a proved state in which a component can no longer create relevant effects;
- **warm-up** establishes caches, connections, code paths, and capacity before relying on candidate latency;
- **split brain** occurs when two environments independently believe they are authoritative for work that requires one authority;
- **rollback window** is the bounded interval during which the former environment remains safe and ready to resume authority;
- **state compatibility** means both application versions interpret and update shared persistent state safely;
- **parity** means equality of properties relevant to a claim, not literal duplication;
- **switch record** binds subject, route state, evidence, policy, actor, time, observations, and outcome.

### Central model, mechanism, or theorem

Let $B$ and $G$ be blue and green deployment subjects and let routing weights be $w_B,w_G\in[0,1]$ with $w_B+w_G=1$. A cutover at time $t$ is permitted only when

$$
Ready(G,t)\land Compatible(B,G,S_t)\land Capacity(G,t)\land Observe(G,t)\land Recover(B,G,t)\land ExclusiveAuthority(t).
$$

Changing desired weight to $(0,1)$ does not prove all work moved. Cached DNS, persistent connections, queued messages, scheduled work, retries, and control-plane propagation can continue sending effects to blue. Drain and observe every work path before declaring blue quiescent.

### Critical invariants

- blue and green are identified by immutable deployment subjects, never ambiguous color labels alone;
- the candidate is production-capable under declared traffic and failure assumptions;
- route changes are authenticated, serialized, idempotent, recorded, and reconciled with observed state;
- every request, job, message, and write has one authoritative handling rule;
- shared data remains compatible with both environments throughout the rollback window;
- candidate warm-up and probes do not create uncontrolled production side effects;
- missing or adverse signals halt impact expansion;
- blue remains patched, credential-valid, capacity-ready, and data-compatible until retirement;
- draining has explicit admission, completion, timeout, retry, and cancellation semantics;
- rollback is allowed only while the former environment and current state remain compatible.

### Common failures

Failures include calling two instance groups two environments, rebuilding green after approval, switching by mutable tag, assuming DNS changes are immediate, forgetting WebSockets or queues, allowing both schedulers to run singleton work, testing green with production writes, sharing mutable local state, warming only happy paths, omitting capacity headroom, comparing untagged telemetry, deallocating blue too soon, changing the database destructively, and calling route reversal a rollback after state compatibility has expired.

### Compact example

Blue serves digest `A7`; green contains approved digest `A8` plus production configuration `C5`. Green receives synthetic probes and read-only mirrored requests, warms caches, and passes capacity checks. A gateway atomically moves new HTTP admissions to green. Blue stops scheduled work, drains bounded connections, and remains ready. Version-tagged signals confirm green health and no new blue admissions. Only after the rollback window and shared-schema compatibility gate does the controller retire blue.

### Connections

[SDRE-024](024-database-change-delivery.md) supplies shared-state compatibility. [SDRE-026](../ROADMAP.md) next develops incremental canary exposure. Platform Engineering owns routing implementations; Distributed Systems owns authority, ordering, and partial failure.

## Governing Question

Blue-green deployment is often presented as a diagram with two boxes and one arrow. The diagram omits the difficult parts: whether the boxes are truly independent, where persistent state lives, what “switch” means for each traffic class, how old work drains, which signals authorize the change, and whether returning traffic preserves data semantics.

The technique reduces the time required to replace compute and offers a prepared return target. It does not make a release safe by topology alone. A rigorous design treats cutover as a distributed state transition over deployment identity, routing authority, application compatibility, work already in flight, and shared resources.

## Why This Matters

Martin Fowler describes blue-green deployment as keeping two production environments as identical as practicable and switching routing between them [1]. Humble and Farley place the pattern in a broader deployment-pipeline and release discipline [2]. The durability of the idea lies in separating preparation from authority: green can be built and checked before receiving production work.

Switching remains mechanism-specific. RFC 9199 explains that DNS TTLs influence transition delay and that cached records cannot be remotely removed [3]. RFC 8767 permits resolvers to serve stale DNS data in exceptional conditions [4]. Therefore a DNS update is desired routing state, not proof that all clients stopped using blue.

Current AWS RDS guidance warns that writes to a green database replica can cause conflicts and that schema changes must remain compatible with the replication method [5]. This vendor example illustrates a general rule: duplicating compute is easy compared with coordinating mutable state. SDRE-024's expand–migrate–contract discipline remains necessary.

## Prerequisites and Retrieval

Retrieve artifact digest, environment, promotion, configuration, secret, readiness, health, load balancer, DNS, connection, queue, session, idempotency, capacity, latency, persistent state, replication, compatibility, rollback, recovery, and audit.

From SDRE-022 retrieve immutable subjects and target evidence; from SDRE-023 retrieve environment-scoped secrets; from SDRE-024 retrieve mixed-version database compatibility. Blue-green is a deployment strategy, not an alternative to those controls.

## Learning Objectives

After completing this module, you should be able to:

1. define the complete blue and green environment boundary;
2. distinguish desired route state from observed traffic;
3. inventory synchronous, asynchronous, scheduled, and long-lived work paths;
4. design readiness, warm-up, cutover, drain, observation, rollback, and retirement;
5. maintain exclusive authority for singleton work and writes;
6. reason about shared-state compatibility and rollback-window expiry;
7. calculate capacity and bounded drain requirements;
8. distinguish blue-green from canary, rolling, shadow, and active-active designs;
9. test switching-plane failures and stale routing;
10. construct an auditable, idempotent cutover controller.

## Core Exposition

**Define the environments.** Each color is a deployment subject: artifact, effective configuration, secret references, infrastructure, identity, network policy, dependencies, and schema assumptions. If both colors share a host, process namespace, writable filesystem, credentials, or failure-prone gateway, that resource is outside the redundancy boundary. Record shared components and their failure impact.

Parity is claim-specific. Green needs the production architecture, policies, dependencies, and capacity required for the release, but should not copy production credentials or personal data casually. A smaller green may be acceptable only if scaling time and headroom are included in the cutover proof. Compare rendered configuration and policy rather than trusting color names.

**Preserve subject identity.** Build once, identify by digest, and promote exact bytes. Bind production configuration, secret references, migrations, and infrastructure declarations. Approving `green` or `release-latest` is insufficient because labels move. The switch record names both source and target subjects.

**Inventory every work path.** HTTP traffic may enter through a gateway, but systems also receive gRPC streams, WebSockets, DNS-resolved direct connections, queues, event subscriptions, cron jobs, webhooks, file drops, administrative calls, and retries. Each path needs a routing and drain rule. A gateway switch cannot stop a blue scheduler from issuing invoices.

Separate admission from completion. At cutover, stop new blue admissions. Existing bounded work can finish, be canceled safely, or be reissued with idempotency keys. Long-lived streams require a maximum lifetime, server-directed reconnect, or explicit termination policy. Without a bound, there is no finite proof that blue has drained.

If propagation takes at most $P$, admitted work lasts at most $L$, and queued delay is at most $Q$, a conservative observation bound is

$$
T_d\ge P+\max(L,Q),
$$

under those enforced assumptions. It is not a universal timeout; retries or work that creates later work need their own bounds.

**Prepare green safely.** Provision independently, resolve target secrets through green identity, run structural and dependency checks, and verify exact subject identity. Readiness means capable of serving a new request now; liveness means the process should remain running. Neither proves sustained capacity or correct business effects.

Warm caches, connection pools, just-in-time code, models, and storage. Synthetic probes use isolated tenants or reversible operations. Mirrored traffic is read-only or has effects suppressed. A shadow response cannot become authoritative accidentally. Compare output with privacy controls and semantic tolerances.

Capacity includes shared dependencies. If arrival rate is $\lambda$ and green's demonstrated sustainable service capacity is $\mu_G$, require $\lambda<\mu_G$ plus explicit headroom for uncertainty and failures. Keeping blue warm consumes compute but a shared database, gateway, or quota can still saturate when both environments warm simultaneously.

**Control authority.** A controller serializes switch attempts and uses compare-and-swap against an expected route generation. Repeating the same requested subject converges; a stale request cannot overwrite a newer route. Policy binds actor, source, target, evidence, maintenance constraints, and recovery readiness.

Singleton schedulers, queue partitions, leaders, and write primaries use leases or fencing tokens. Merely setting `enabled=false` in blue is unsafe if stale processes continue. The receiver validates the current generation so an old authority cannot produce accepted effects.

**Switch and observe.** A load balancer can move new connections quickly; DNS, clients, proxies, and connection pools may lag. Record desired and observed route weights, connection counts, request counts, message ownership, scheduler generations, and write origins by environment and version.

Evaluate candidate signals against a declared baseline and thresholds: correctness invariants, error ratio, latency distribution, saturation, dependency behavior, business outcomes, and missing telemetry. Tag observations with subject and color. Aggregate service metrics can hide green failure behind healthy blue traffic.

All-at-once switching is the canonical blue-green form; weighted switching overlaps with canary technique. A brief controlled ramp can protect the switching mechanism, but it does not replace the candidate's readiness or capacity evidence. SDRE-026 develops statistical and exposure questions for canaries.

**Coordinate state.** The simplest design shares a backward-compatible database. Green reads and writes the same authoritative state, while schema supports both versions. If green changes data in a way blue cannot understand, the rollback window ends even if blue compute remains present.

Separate databases require replication direction, lag bounds, conflict policy, cutover point, and prevention of independent writes. Bidirectional writes create a distributed consistency problem, not convenient rollback. Prefer one write authority, durable change capture, and verified convergence. Object storage, caches, search indexes, and sessions also contain state.

Keep user sessions portable or force a deliberate reauthentication. Local memory and local disks make the environments behaviorally unequal. Cache keys and serialized values need version compatibility. External side effects—payments, email, device commands—require idempotency and cannot be undone by routing.

**Maintain the return path.** Blue remains patched, observable, credential-valid, capacity-ready, and compatible. Do not let configuration or dependencies drift during the rollback window. Periodically prove it can receive a synthetic request without becoming authoritative.

Rollback criteria are declared before cutover. Route reversal can restore request handling when state and dependencies remain compatible. It cannot undo green's writes or external effects. If compatibility is lost, stop, disable the feature, or roll forward rather than sending traffic to code that misinterprets data.

**Drain and retire.** After green is stable, stop all blue admissions, verify no singleton authority, wait through bounded in-flight work, inspect late traffic, and archive the switch record. Remove blue only after the rollback window closes by policy. Revoke its credentials, detach routes, preserve required forensic evidence, and release capacity.

Never infer quiescence from low traffic alone. A monthly job, delayed webhook, stale DNS resolver, or forgotten administrative path may reappear. Inventory and enforced admission controls provide stronger evidence than silence.

**Test the controller.** Exercise wrong digest, changed configuration, unavailable dependency, insufficient capacity, stale route generation, concurrent switches, partial propagation, missing telemetry, old DNS answer, persistent connection, lost controller, duplicated message, scheduler split brain, database incompatibility, failed drain, rollback after state change, and cleanup failure. Safe failure holds authority or stops expansion; it does not guess.

## Definitions and Notation

Let environment subjects be $B=(a_B,c_B,r_B)$ and $G=(a_G,c_G,r_G)$. Let desired route vector $W=(w_B,w_G)$ satisfy $w_B+w_G=1$. Let observed fraction $\widehat W$ be measured from tagged admissions; $W=\widehat W$ is not assumed during propagation.

Let $S_t$ be persistent and external-effect state. $Compatible(B,G,S_t)$ means both subjects can safely interpret all state reachable during the rollback window. Let authority generation $g$ increase monotonically; a write or singleton action is accepted only when carrying the current fenced generation.

Let $C_G$ be demonstrated green capacity and $D$ declared headroom fraction. A necessary capacity condition is $C_G\ge(1+D)\lambda$, but measurement error, burstiness, dependency ceilings, and failures require further evidence.

## Mechanisms, Invariants, or Proof Structure

**Routing invariant.** Desired weights sum to one, but exclusive authority may require stronger fencing than routing. Duplicate delivery can occur even when admission weights are correct.

**Rollback argument.** Blue's presence is insufficient. If green writes state outside blue's accepted domain, routing back violates compatibility. Thus rollback requires compute readiness and state compatibility.

**Drain argument.** With enforced bounds $P,L,Q$, no newly admitted blue work after propagation and all earlier work ends within $\max(L,Q)$, giving the stated conservative bound. Without any bound, quiescence must be established by another mechanism.

**Capacity argument.** Two complete environments do not double end-to-end capacity when they share a bottleneck. Candidate testing and concurrent warm-up must include shared dependency demand.

**Executable switch policy.** This deterministic model checks identity, evidence, capacity, compatibility, generation, and drain state. It does not control a network.

<!-- bijux-verify: {"id":"blue-green-switch-policy","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"ready_switch=allowed\nwrong_subject=denied:subject\ninsufficient_capacity=denied:capacity\nincompatible_state=denied:state\nstale_generation=denied:generation\nmissing_signal=denied:observation\nweights_valid=True\nblue_quiescent=False\nrollback_before_state_change=allowed\nrollback_after_state_change=denied:state\n","stderr":""}} -->
```python
approved = "sha256:green-A8-C5"

def switch(subject, capacity, demand, state_compatible=True,
           observed=True, expected_generation=7, actual_generation=7):
    if subject != approved:
        return "denied:subject"
    if capacity < 1.25 * demand:
        return "denied:capacity"
    if not state_compatible:
        return "denied:state"
    if expected_generation != actual_generation:
        return "denied:generation"
    if not observed:
        return "denied:observation"
    return "allowed"

print(f"ready_switch={switch(approved, 1500, 1000)}")
print(f"wrong_subject={switch('sha256:other', 1500, 1000)}")
print(f"insufficient_capacity={switch(approved, 1100, 1000)}")
print(f"incompatible_state={switch(approved, 1500, 1000, state_compatible=False)}")
print(f"stale_generation={switch(approved, 1500, 1000, expected_generation=6)}")
print(f"missing_signal={switch(approved, 1500, 1000, observed=False)}")
weights = (0.0, 1.0)
print(f"weights_valid={sum(weights) == 1.0 and all(0 <= w <= 1 for w in weights)}")
blue = {"new_admissions": 0, "open_streams": 2, "singleton_authority": False}
print(f"blue_quiescent={blue == {'new_admissions': 0, 'open_streams': 0, 'singleton_authority': False}}")
print(f"rollback_before_state_change={'allowed' if True else 'denied:state'}")
print(f"rollback_after_state_change={'allowed' if False else 'denied:state'}")
```

## Alternatives and Trade-Offs

**Blue-green versus rolling.** Blue-green prepares a complete target and offers a retained source, at higher capacity cost. Rolling replaces units gradually but creates longer mixed-version operation.

**Blue-green versus canary.** A cutover exposes most traffic at once after preparation. Canary limits initial exposure and gathers production evidence, but needs representative routing and statistical judgment.

**Load-balancer versus DNS switching.** Load balancers usually control admissions centrally. DNS reaches broader boundaries but caches and clients delay convergence. Neither controls already-open connections.

**Shared versus replicated state.** Shared state avoids data cutover but requires version compatibility and may remain a single failure domain. Replication isolates environments but introduces lag, conflict, and authority transfer.

**Warm versus cold blue.** Warm blue gives faster return and stronger evidence but costs capacity and can create accidental authority. Cold restoration costs less but is disaster recovery, not immediate blue-green rollback.

**Mirroring versus synthetic probes.** Mirroring represents real inputs but risks privacy and side effects. Synthetic probes are controlled but may miss production distributions. Use both within explicit boundaries.

**Atomic versus weighted switch.** Atomic desired state is simple but observed movement is never perfectly instantaneous. Weighted control reduces exposure but becomes a progressive-delivery policy.

## Failure Modes and Misconceptions

- **“Two colors mean two fault domains.”** shared gateways, databases, credentials, or hosts may fail together.
- **“Identical means correct.”** identical misconfiguration duplicates failure.
- **“Readiness proves capacity.”** a probe does not establish sustained service.
- **“The DNS TTL is a deadline.”** stale serving and client caching can extend old routing.
- **“Zero blue requests means drained.”** unobserved jobs or streams may remain.
- **“Traffic weights enforce one writer.”** queues and schedulers need fencing.
- **“Shadow traffic is harmless.”** candidate side effects must be suppressed.
- **“Rollback is instant.”** propagation, draining, warm-up, and state compatibility constrain it.
- **“Old compute guarantees rollback.”** changed data can make old code unsafe.
- **“Separate databases improve safety automatically.”** replication and conflict can be harder.
- **“Double compute means double capacity.”** shared bottlenecks remain.
- **“Green may use staging secrets.”** it needs target-scoped production identity.
- **“Keep blue forever.”** stale environments accumulate vulnerabilities and cost.
- **“Delete blue after a quiet hour.”** retirement follows declared evidence and recovery policy.
- **“Blue-green prevents release defects.”** it bounds replacement mechanics, not correctness.

## Worked Examples

### Example 1

**Find the real boundary.** Blue and green instance groups share one gateway, database, and secret. Compute replacement is independent, but those shared components are outside the blue-green boundary. Conclusion: document the pattern as compute-level blue-green, not full-environment redundancy.

### Example 2

**Calculate capacity.** Peak demand is 800 requests/s and policy requires 30% headroom. Green must demonstrate at least $1.3\cdot800=1040$ requests/s while shared dependencies remain within limits. Conclusion: instance count alone is not capacity evidence.

### Example 3

**Bound draining.** Route propagation is bounded at 20 seconds, requests at 45 seconds, and queued admission at 10 seconds. $T_d\ge20+\max(45,10)=65$ seconds. Conclusion: observe at least 65 seconds under these assumptions, then verify counts; an unbounded stream invalidates the calculation.

### Example 4

**Expose a DNS misconception.** An operator changes an address with TTL 60 seconds and removes blue after one minute. A resolver serving stale data during upstream failure and a client holding a connection still use blue. Conclusion: DNS desired state and connection state require direct observation and a longer retirement policy.

### Example 5

**Fence a scheduler.** Both environments contain a billing cron. The controller grants generation 18 to green, and the database accepts billing effects only with current generation. A delayed blue job carrying 17 is rejected. Conclusion: fencing enforces authority after stale execution.

### Example 6

**Warm safely.** Green needs cache and JIT warm-up. Synthetic tenant requests populate paths without contacting payment providers; mirrored production reads have writes suppressed and outputs protected. Conclusion: warm-up should reproduce resource behavior without becoming an uncontrolled second producer.

### Example 7

**Reject an unsafe rollback.** Green writes a new enum value that blue cannot parse. Error rates rise. Switching back would turn every such row into a blue failure. Conclusion: disable the feature or roll forward; retained compute is not a valid return path.

### Example 8

**Handle a lost controller.** The controller times out after submitting generation 9. Its replacement reads desired route generation, observed backend weights, connection counts, and audit record before acting. It never repeats from assumption. Conclusion: uncertain cutover state requires reconciliation.

### Example 9

**Distinguish aggregate health.** With 90% blue and 10% green, aggregate errors are 0.9%, but green alone errors at 9%. Untagged telemetry appears tolerable. Conclusion: every signal must bind to environment and subject.

### Example 10

**Retire completely.** After the rollback window, the team disables every blue admission path, confirms queues and streams empty, revokes blue credentials, removes routes, archives evidence, and releases resources. Conclusion: retirement is a security and authority transition, not merely deleting instances.

## Cross-Program Connections

- **Distributed Systems:** leases, fencing, retries, partial failure, and convergence govern authority.
- **Database Engineering:** shared-state compatibility and replication determine rollback feasibility.
- **Network Engineering:** DNS, connection lifetimes, gateways, and routing propagation determine switching.
- **Platform Engineering:** environment provisioning, selectors, identity, health, and controllers implement the mechanism.
- **Security Engineering:** credential scope, administrative authority, mirrored data, and retirement affect exposure.
- **Software Architecture:** state ownership, sessions, singleton work, and external effects define coupling.
- **Testing and Quality Engineering:** probes, traffic replay, fault injection, and tagged comparison create evidence.
- **Cloud Engineering:** quotas, regions, managed load balancers, and control-plane behavior shape failure domains.

## References

1. Martin Fowler, [“Blue Green Deployment”](https://martinfowler.com/bliki/BlueGreenDeployment.html), March 2010; retrieved 2026-09-06.
2. Jez Humble and David Farley, *Continuous Delivery*, Addison-Wesley, 2010, Chapters 10 and 12.
3. IETF, [RFC 9199: *Considerations for Large Authoritative DNS Server Operators*](https://www.rfc-editor.org/rfc/rfc9199.html), March 2022; retrieved 2026-09-06.
4. IETF, [RFC 8767: *Serving Stale Data to Improve DNS Resiliency*](https://www.rfc-editor.org/rfc/rfc8767.html), March 2020; retrieved 2026-09-06.
5. Amazon Web Services, [“Best practices for Amazon RDS blue/green deployments”](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/blue-green-deployments-best-practices.html), current documentation retrieved 2026-09-06. Used as vendor-specific evidence about writes and replication-compatible schema changes, not a universal database guarantee.
6. Google, *Site Reliability Engineering*, O'Reilly, 2016, Chapter 8, “Release Engineering.”
7. Michael Nygard, *Release It!*, second edition, Pragmatic Bookshelf, 2018. Used for stability, capacity, and failure-boundary reasoning.
8. IETF, [RFC 9110: *HTTP Semantics*](https://www.rfc-editor.org/rfc/rfc9110.html), June 2022; retrieved 2026-09-06. Used for durable request and connection semantics; specific drain behavior remains implementation-defined.

## Exercises

### Exercise 1

Define cutover, draining, quiescence, switching plane, rollback window, and split brain. Explain why desired route weight zero does not establish quiescence.

### Exercise 2

Green must serve 2,400 requests/s with 35% headroom. Compute required demonstrated capacity. If propagation is bounded at 30 seconds, requests at 50 seconds, and queued delay at 80 seconds, compute the conservative drain observation bound.

### Exercise 3

A cutover moves HTTP traffic, but blue retains WebSockets, consumes a queue, and runs a daily settlement job. Design admission, drain, retry, and authority controls for all paths.

### Exercise 4

Compare shared-database and replicated-database blue-green designs across compatibility, write authority, lag, conflict, rollback, capacity, and recovery.

### Exercise 5

A medical device fleet caches DNS for hours, maintains persistent sessions, and can issue safety-relevant commands. Design a blue-green cutover that preserves one command authority and supports safe return.

## Answers to the Exercises

### Answer 1

Cutover transfers authoritative work; draining refuses new work while bounded in-flight work finishes or terminates; quiescence proves no relevant new effects can originate; the switching plane routes work; the rollback window is the interval during which the former subject remains safe and ready; split brain is concurrent independent authority where one is required. Desired weight zero changes controller intent, but cached DNS, established connections, queues, retries, jobs, and propagation may still reach blue. Observed admissions, bounded completion, and fenced authority are required.

### Answer 2

Required capacity is $2400(1+0.35)=3240$ requests/s. The drain bound is $P+\max(L,Q)=30+\max(50,80)=110$ seconds. These values are necessary under the assumptions, not sufficient proof: shared dependencies, bursts, retries, telemetry gaps, and unbounded work need separate evidence.

### Answer 3

The HTTP gateway sends new connections to green and tags observations. Blue directs WebSocket clients to reconnect with bounded grace, then terminates remaining sessions safely. Queue partitions transfer by lease or consumer generation; messages carry idempotency keys and stale blue acknowledgments or effects are rejected. The settlement scheduler uses a fenced generation stored at the authoritative effect boundary, so only green can settle. Observe new admissions, open streams, queue ownership, outstanding retries, and generation use. Blue is quiescent only when each path satisfies its rule.

### Answer 4

A shared database avoids a data copy and gives one state authority, but both versions must remain schema- and data-compatible and the database remains a shared failure and capacity domain. Replicated databases improve isolation and can support engine upgrades, but require bounded lag, a cutover position, replication-compatible changes, one write authority, conflict handling, and proof that green contains all accepted blue writes. Returning to blue may require reverse replication or may be unsafe after green writes. Choose shared state for ordinary application release when expand–contract supports both versions; choose replication only when isolation or database change justifies the added distributed-state protocol.

### Answer 5

Use a gateway or command broker as the fenced authority rather than relying on DNS alone. Provision green with the exact subject, device protocol compatibility, production identity, full capacity, and read-only replay evidence. Issue a monotonically increasing command-authority generation; devices or the broker reject commands from older generations. Lower DNS TTL well before cutover where possible, but retain blue because device caches and sessions exceed it. New sessions prefer green; existing sessions receive an authenticated reconnect instruction and bounded deadline, while blue loses command authority immediately but can finish safe acknowledgments. Track every device cohort and command generation. Return is allowed only if blue understands current device and server state; otherwise keep authority on green and roll forward. Retire blue only after the maximum offline/cache/session horizon or explicit fleet acknowledgment proves no stale command path remains.
