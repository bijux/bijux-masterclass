---
module_id: SARCH-055
program: Software Engineering: Software Architecture
level: 2
module_number: 55
title: Control-Plane and Data-Plane Architecture
status: complete
last_verified: 2026-09-06
---

# Control-Plane and Data-Plane Architecture

## One-Page Review

### Governing question

How should an architecture separate policy, desired state, placement, configuration, identity, and lifecycle decisions from serving traffic so that control failure, delay, compromise, or overload has explicit bounded consequences for the data plane?

### Essential definitions

- The **data plane** executes ordinary workload operations using an installed configuration, such as forwarding, serving, enforcing, reading, writing, or scheduling already admitted work.
- The **control plane** decides or reconciles desired state, authority, routing, placement, policy, membership, and configuration consumed by the data plane.
- The **management plane** exposes human or administrative intent, approval, audit, and lifecycle interfaces; it may invoke but is not identical to the control plane.
- **desired state** describes intended configuration; **observed state** describes measured reality; a **reconciler** repeatedly acts to reduce their difference.
- A **snapshot** is a coherent configuration version; a **delta** is an incremental change that depends on a known base or version.
- A **lease** is time-bounded authority requiring renewal; an **epoch** is an ordered generation used to reject obsolete decisions.
- **fail-static** continues with last validated state; **fail-closed** refuses an operation; **fail-open** permits it; each is a policy choice scoped to a capability and threat.
- **blast radius** is the bounded set of users, resources, or capabilities one control decision can affect.
- **control-loop stability** means feedback converges without harmful oscillation, overshoot, or amplification under its operating assumptions.
- **bootstrap dependency** is required to start or recover a component, even if normal serving can continue without it.

### Central model, mechanism, or theorem

A reconciler observes state $O_t$, compares it with desired state $D_t$, and issues bounded actions $a_t$ so later state approaches the target:

$$
a_t=\pi(D_t,O_t), \qquad O_{t+1}=F(O_t,a_t,e_t),
$$

where policy $\pi$, plant behavior $F$, and disturbance $e_t$ must be understood. Reconciliation is level-triggered and retryable; an event notification may prompt observation but is not itself current truth.

If updates arrive at rate $\lambda$ during a control outage of duration $T$, backlog is approximately $B=\lambda T$. A recovered plane processing at rate $\mu>\lambda$ drains that backlog no faster than

$$
t_{drain}=\frac{\lambda T}{\mu-\lambda}
$$

under a simple constant-rate model. If $\mu\le\lambda$, it never catches up without shedding, coalescing, prioritization, or more capacity.

### Critical invariants

- every control decision has identity, scope, version, authority, validation, and audit evidence;
- data-plane behavior under control loss is specified per operation, including expiry and safe degradation;
- last-known-good state is coherent, authenticated, compatible, and bounded in age or epoch;
- stale controllers, agents, and configurations cannot regain authority after a newer epoch;
- serving health is not coupled blindly to transient management or control-plane health;
- bootstrap and steady-state dependencies are modeled separately and tested from zero;
- reconcilers are idempotent, restartable, bounded, and safe under duplicate, missing, delayed, and reordered observations;
- rollout limits blast radius and preserves a stop, rollback, or forward-repair path;
- policy enforcement states whether stale allow and stale deny are acceptable;
- secrets and credentials have scoped distribution, rotation, revocation, expiry, and degraded behavior;
- control traffic receives capacity, admission, priority, and recovery budgets distinct from workload traffic;
- control-plane compromise is considered separately from unavailability;
- emergency human authority is authenticated, bounded, expiring, and reviewed;
- recovery validates resulting workload and business outcomes, not only configuration delivery.

### Common failures

Common failures include restarting healthy workers because the controller is down; making every request query a central policy service; serving an unbounded stale allow decision; applying partial configuration as if it were one snapshot; using wall-clock timestamps as authority epochs; allowing two reconcilers to fight; retrying every queued update simultaneously after recovery; scaling on delayed metrics until the fleet oscillates; granting a global administrator credential to regional agents; making artifact, identity, DNS, or certificate services invisible bootstrap dependencies; declaring a rollout complete when agents acknowledged but behavior was not probed; and coupling the emergency stop to the failed control plane.

### Compact example

A routing controller becomes unavailable. Existing proxies retain an authenticated snapshot version 87 for thirty minutes and continue routes whose certificates and policy epochs remain valid. New routes and privilege grants stop; revocations arrive through a separately protected urgent channel. Cold starts use a local sealed snapshot or fail explicitly. Recovery sends a current snapshot, not every obsolete delta, and canaries behavior before fleet rollout.

### Connections

[SARCH-049](049-configuration-and-environment-topology.md) supplies configuration structure, [SARCH-051](051-partial-failure-as-an-architectural-constraint.md) supplies control loss, and [SARCH-054](054-multi-region-topologies.md) supplies regional dependencies. [SARCH-056](../ROADMAP.md) next bounds stacks into cells. Platform Engineering owns control implementations; this module owns separation, contracts, and failure consequences.

## Governing Question

Modern systems continuously decide where work runs, which routes exist, what policy permits, which certificate is current, and how desired state becomes reality. If every serving operation depends synchronously on those decisions, the controller becomes part of every data path. If serving ignores control indefinitely, stale policy and unsafe authority accumulate.

The architectural problem is to define the boundary: which state can be precomputed and enforced locally, which decisions require fresh coordination, how long installed state remains valid, and how the system bootstraps and recovers when control is absent or hostile.

## Why This Matters

Control planes concentrate leverage. A small configuration error can affect an entire fleet faster than ordinary workload traffic. A compromised controller can distribute trusted malicious state. Conversely, overcoupling health to control availability can turn a recoverable control outage into a serving outage.

The separation also determines operability. Desired state, observation, reconciliation, rollout, and audit need explicit versions and ownership. Without them, operators cannot tell whether a decision was intended, delivered, activated, effective, or safely reversible.

## Prerequisites and Retrieval

Retrieve desired state, observed state, feedback, controller, agent, policy, authority, lease, epoch, fencing, snapshot, delta, cache, bootstrap, idempotency, retry, backpressure, health, rollout, canary, circuit breaker, fail-open, fail-closed, availability, consistency, region, threat model, and audit.

From SARCH-023 retrieve runtime components; SARCH-025 and SARCH-048 provide deployment and release units; SARCH-049 provides configuration topology; SARCH-051 provides partial failure; and SARCH-053 through SARCH-054 provide placement and regional topology.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish management, control, and data planes by responsibility rather than process name;
2. model desired-state reconciliation and its convergence assumptions;
3. specify data-plane behavior under controller loss, stale state, and compromise;
4. separate snapshot, delta, delivery, activation, and observed-effect semantics;
5. design versioning, epochs, leases, and fencing for control authority;
6. calculate simple outage backlog and drain constraints while stating limitations;
7. design bootstrap independently from warm steady-state serving;
8. bound rollout and reconciliation blast radius;
9. protect policy, identity, secrets, audit, and emergency operation;
10. review control-plane evidence without equating acknowledgement with correct behavior.

## Core Exposition

**Classify by responsibility, not host.** A process can perform both control and data work; separate processes can still form one logical plane. Ask whether an operation decides desired behavior or executes already installed behavior. Administrative intent and approval form a management surface even when one API handles all three.

Examples vary by domain. A network controller computes routes while switches forward packets. A scheduler chooses placement while workers run tasks. A policy compiler creates decisions while local agents enforce them. A database membership service assigns replicas while storage serves reads and writes.

**Keep the data path bounded.** Local enforcement can preserve serving when the controller is slow or unavailable and reduce request latency. It requires a coherent installed state, provenance, expiry, and behavior when freshness bounds are crossed.

Not every decision can be cached safely. A rapidly changing fraud hold or credential revocation may require fresh authority. Split policy: immutable or slow-changing rules can be compiled; urgent denies need a protected low-latency invalidation path; high-risk grants may require online confirmation.

**Model desired and observed state.** Desired state expresses intent, not fact. A successful API write proves acceptance by the management boundary, not activation everywhere. Observed state may be delayed, incomplete, or incorrect.

Use stable resource identities, versions, conditions, and ownership. Distinguish accepted, validated, scheduled, delivered, acknowledged, activated, effective, converged, and failed. User interfaces and automation should not collapse these states into “deployed.”

**Use level-triggered reconciliation.** A reconciler repeatedly compares current observation with desired state and acts toward the target. If an event is lost, later observation still reveals the difference. An edge-triggered sequence that depends on receiving every event is fragile unless the log and offsets provide that guarantee.

Actions should be idempotent or carry durable identity. Re-read after action because the world may change between observation and write. Bound work, use backoff, and preserve fairness so one broken resource cannot starve all reconciliation.

**Understand feedback stability.** Delayed measurements and actions can make controllers overshoot. An autoscaler observes old load, adds capacity that takes minutes, observes another high sample, and adds again. When capacity arrives, it removes too quickly and repeats.

Use deadbands, rate limits, stabilization windows, predictive knowledge, and explicit actuator delay. These mechanisms trade responsiveness for stability. Test step changes, noise, saturation, partial actuator failure, and recovery rather than tuning on one smooth trace.

**Version complete meaning.** Configuration versioning needs identity, schema, dependencies, authority, and compatibility. A monotonic epoch orders authority changes; a content digest verifies bytes; neither replaces semantic validation.

Apply a coherent snapshot atomically at the agent boundary when rules interact. If deltas are used, include base version, ordering, idempotency, gap detection, and snapshot recovery. Reject unknown schema or missing dependency rather than partially interpreting it.

**Choose push, pull, or hybrid delivery.** Push reduces notification delay but needs connection, retry, fan-out, and backpressure. Pull makes agents control load and recover missed notifications but adds polling delay. A hybrid notification followed by versioned fetch often combines both.

Delivery is not activation. Agents validate, stage, activate, probe, and report. The controller records uncertainty when acknowledgements are missing; it does not infer absence or success from silence.

**Define fail-static, closed, and open by capability.** During control loss, a proxy might continue last-known routes, refuse new privilege, retain explicit denies, and permit low-risk cached reads. One global failure posture is rarely correct.

State validity duration and expiry behavior. Fail-static can become unsafe when membership, certificates, revocations, or destinations change. Fail-closed protects some security invariants but may harm safety or availability. Emergency policy must be preauthorized, not improvised silently.

**Separate leases from local clocks carefully.** A lease bounds authority in time under assumptions about clocks, renewal, and storage. Clock error and process pause can break naive use. Epoch fencing at the resource provides an ordered rejection mechanism even when an old controller wakes.

Define who issues epochs and how that authority survives failure. A timestamp is not automatically unique or monotonic across actors. Old agents must reject state below their accepted epoch and persist enough state across restart.

**Design last-known-good state.** Persist only validated, authenticated, compatible snapshots and their provenance. Keep previous known-good state for rollback when policy permits. A local cache of arbitrary last-seen bytes is not a recovery asset.

Bound use by time, epoch, certificate life, data sensitivity, and capability. State what happens at expiry. A route may remain usable while a privilege grant does not. Monitor age locally even if global telemetry is unavailable.

**Design bootstrap separately.** A warm worker may serve for hours from installed state, yet a restarted worker may require identity, certificates, DNS, artifact, time, configuration, placement, and policy services. Region evacuation and fleet restart expose this gap.

Create a minimal trust and configuration root appropriate to the threat model: sealed local snapshot, regional mirror, embedded trust anchor, or explicitly unavailable cold start. Test restoration from zero, not only control loss while warm.

**Partition control scope.** One global plane simplifies policy but creates large blast radius and latency. Regional, tenant, shard, or cell controllers contain failure and scale metadata. Hierarchy can distribute global constraints and local decisions.

Partitioning creates consistency questions. Two regional controllers must not both grant unique ownership. Global desired state may be unavailable while local reconcilers continue within leased scope. Define delegation, conflict, and reassignment explicitly.

**Bound rollout blast radius.** Validate syntax, schema, references, policy, and invariants before delivery. Roll out through a representative canary, small cohort, region, or cell, with automatic stop conditions based on capability behavior.

Acknowledgements prove receipt or activation only as defined. Probe routes, authorization, workload health, and business outcomes. Preserve version comparison and rollback, but recognize that stateful effects may require forward repair rather than reversal.

**Give control traffic its own capacity model.** Configuration distribution, heartbeats, reconciliation, logs, metrics, certificate rotation, repair, and operator queries compete for CPU, network, storage, and quotas. A data-plane incident can flood the controller with status changes exactly when it is least able to respond.

Use bounded queues, coalescing, priority, sampling, admission, sharding, and per-tenant fairness. Preserve urgent revocation and safety commands. Do not discard state transitions whose loss invalidates authority; coalesce only when current desired state makes intermediates irrelevant.

**Plan outage recovery.** If updates accumulate at rate $\lambda$ for time $T$, recovered capacity must exceed ongoing arrival rate to catch up. Replaying every obsolete delta wastes capacity; a current snapshot can collapse superseded desired state if audit and semantics permit.

Avoid a thundering herd of agents reconnecting, renewing leases, fetching artifacts, and reporting state. Randomize, stage, and prioritize. Maintain enough data-plane reserve for recovery traffic.

**Protect security boundaries.** Authenticate management intent, authorize by scope, sign or authenticate distributed state, encrypt sensitive content, and audit creation through effect. Regional agents should not hold global power merely for convenience.

Treat control compromise differently from outage. A compromised signed channel can distribute harmful valid-looking state. Use multi-party approval for high-impact change, policy constraints at agents, blast-radius limits, immutable audit, and revocation or trust-root rotation paths.

**Design secret and certificate control.** Short-lived credentials reduce exposure but increase renewal dependency. Long-lived caches improve outage tolerance but increase compromise and revocation windows. Choose by threat and capability.

Agents validate subject, audience, scope, issuer, version, time bounds, and revocation policy. Never log secrets in control evidence. Test expiry during partition and replacement after controller compromise.

**Separate health layers.** Process liveness, agent readiness, data-plane capability, controller reachability, and end-to-end user outcome are different signals. Removing every worker because it cannot reach control can erase a healthy fail-static service.

Routing health should match the request capability. A node may serve existing routes but reject configuration-dependent new tenants. Expose degraded status without triggering destructive automated replacement.

**Design management and emergency operation.** Human interfaces need strong identity, least privilege, preview, diff, approval, rate limit, dry-run where meaningful, audit, and clear state transitions. Operators need a locally reachable stop for runaway automation.

Break-glass authority is scoped by resource, action, duration, and incident; it produces visible evidence and retrospective review. If it depends on the failed global plane, it is decorative. If it bypasses every guard indefinitely, it is a standing compromise path.

**Observe causally.** Record intent ID, actor, desired version, policy decision, target cohort, delivery and activation version, observed state, reconcile attempt, authority epoch, lease, last-known-good age, error class, rollout state, and user effect without leaking protected configuration.

Preserve regional evidence when the global collector fails. Trace one change from approval to actual behavior. Metrics such as “99% agents connected” do not reveal whether the missing 1% owns critical traffic.

**Test failure and compromise.** Drop control messages, reorder deltas, lose a snapshot, pause an agent, skew clocks, duplicate reconcilers, partition regions, exhaust queues, corrupt desired state, revoke the signer, restart from zero, and restore at fleet scale.

Check authority, policy, serving continuity, expiry, backpressure, convergence, business outcomes, and human controls. Tests show observed behavior for their versions and loads; model untested schedules and expand sampling after defects.

## Definitions and Notation

Let:

- $D_t$ be desired state at observation time $t$ and $O_t$ observed state;
- $\pi(D_t,O_t)$ be reconciliation policy producing bounded action $a_t$;
- $F(O_t,a_t,e_t)$ be system evolution under action and disturbance $e_t$;
- $v$ be a configuration version, $e$ an authority epoch, and $\tau$ a validity deadline;
- $\lambda$ be average arriving control updates per second;
- $\mu$ be average recovery processing capacity per second;
- $T$ be control outage duration and $B=\lambda T$ the simple accumulated backlog;
- $c$ be rollout cohort size and $N$ eligible targets;
- **activation** mean an agent has installed a version for use;
- **effectiveness** mean observed behavior satisfies the version's intended capability;
- **last-known-good** mean a previously validated and authenticated snapshot approved for bounded reuse;
- **control debt** mean desired state accepted but not yet effectively reconciled.

The constant-rate backlog model ignores bursts, coalescing, dependencies, failed items, retry cost, priority, heterogeneous work, and changing capacity. It is a feasibility screen, not a recovery forecast.

## Mechanisms, Invariants, or Proof Structure

### Control-plane design procedure

1. Classify management intent, control decisions, and data-plane execution per capability.
2. Define desired, observed, accepted, delivered, activated, effective, converged, and failed states.
3. Choose authoritative identity, version, epoch, lease, snapshot, and delta semantics.
4. Specify control-loss, stale-state, expiry, bootstrap, and compromise behavior per operation.
5. Design idempotent bounded reconciliation and stable feedback under delay, noise, saturation, and partial actuation.
6. Partition controller scope and preserve global invariants through delegation and fencing.
7. Bound rollout, capacity, queue, retry, and recovery amplification.
8. Protect identity, policy, secrets, audit, emergency authority, and local stop controls.
9. Validate effect through capability probes and adversarial transition tests.

### Backlog derivation

An outage lasting $T$ at constant arrival rate $\lambda$ creates $B=\lambda T$. After recovery, new work continues at $\lambda$ while total service is $\mu$, leaving net drain rate $\mu-\lambda$. For $\mu>\lambda$, drain time is $B/(\mu-\lambda)=\lambda T/(\mu-\lambda)$. At equality no spare rate drains old work; below equality backlog grows.

### Architectural invariants

- no accepted-intent status is presented as effective state;
- no installed configuration lacks authenticated provenance, compatibility, and version;
- no stale authority can act after a later fenced epoch;
- no control outage automatically destroys valid data-plane serving;
- no recovery replay exceeds bounded capacity or starves urgent controls;
- no high-blast-radius change lacks progressive exposure and an independent stop path.

## Alternatives and Trade-Offs

| Choice | Strength | Cost or risk | Evidence needed |
|---|---|---|---|
| synchronous per-request control | freshest central decision | latency and shared outage path | deadline and failure behavior |
| compiled local policy | fast autonomous enforcement | staleness and distribution | version, expiry, revocation |
| push delivery | low notification delay | fan-out, retry, backpressure | fleet loss and reconnect |
| pull delivery | agent-owned load and recovery | polling delay and source load | freshness distribution |
| snapshot | coherent recovery and bootstrap | larger transfer | digest and atomic activation |
| delta stream | efficient incremental change | gap, order, and base coupling | offsets and snapshot fallback |
| global controller | simple global invariants | blast radius and latency | regional/control isolation |
| partitioned controllers | scale and containment | delegation conflicts | scope, epoch, reassignment |
| fail-static | serving continuity | stale policy or topology | bounded validity and expiry |
| fail-closed/open | protects selected harm model | availability or security loss | operation-specific policy |

## Failure Modes and Misconceptions

1. **“Control plane means one service.”** it is a responsibility boundary, not a process count.
2. **“Data planes need no control.”** they consume installed decisions and trust roots.
3. **“Desired state is actual state.”** acceptance, activation, and effect differ.
4. **“An event stream guarantees reconciliation.”** loss or gaps require current-state observation.
5. **“Idempotent means harmless.”** repeating a wrong desired state is still harmful.
6. **“Last known means last known good.”** validation, authentication, and compatibility are required.
7. **“Fail-open or fail-closed is global.”** the correct posture varies by operation and harm.
8. **“A timestamp is a fencing token.”** clock order may not represent authority.
9. **“Agent acknowledgement proves behavior.”** it may prove only receipt or activation.
10. **“Warm survival proves recoverability.”** bootstrap dependencies appear from zero.
11. **“More reconcilers converge faster.”** competing actors can oscillate or duplicate load.
12. **“Control traffic is negligible.”** incident status and recovery can dominate it.
13. **“Replay catches up eventually.”** not when service rate is at or below arrivals.
14. **“Global policy requires global synchronous serving.”** compiled bounded local enforcement may suffice.
15. **“Signed configuration is safe.”** a compromised authorized signer can distribute harm.
16. **“Emergency access always improves resilience.”** unbounded bypass creates security and integrity failure.

## Worked Examples

### Example 1

**Situation.** A routing controller fails while proxies have authenticated snapshot 87.

**Reasoning.** Existing routes continue within a thirty-minute validity bound; new routes and privilege grants stop. Agents retain explicit denies and receive urgent revocations through a separate protected path. At expiry they degrade by capability rather than accepting arbitrary stale state.

**Conclusion.** Fail-static continuity requires validated snapshots and operation-specific expiry behavior.

### Example 2

**Situation.** A controller is down for 600 seconds while 20 updates/s arrive; recovery capacity is 50 updates/s.

**Reasoning.** Backlog is $20(600)=12{,}000$ updates. Net drain is $50-20=30$ updates/s, so the ideal drain time is $12{,}000/30=400$ seconds. Retries and heterogeneous actions make actual time longer; coalescing superseded state may reduce work.

**Conclusion.** Recovery capacity must exceed ongoing arrivals and include a bounded catch-up plan.

### Example 3

**Situation.** Ten configuration deltas arrive out of order and delta 4 is missing.

**Reasoning.** An agent at base version 3 cannot safely apply 5 through 10 when interactions matter. It detects the gap, fetches an authenticated snapshot at version 10, validates dependencies, activates atomically, and reports both activation and capability probe results.

**Conclusion.** Delta efficiency depends on base and order recovery through coherent snapshots.

### Example 4

**Situation.** An autoscaler samples two-minute-old load every thirty seconds while capacity takes five minutes to start.

**Reasoning.** Repeated high observations trigger several actions before any effect is visible, causing overshoot; rapid scale-down can then oscillate. Account for actuator delay, cap step size, use stabilization windows and deadband, and test step loads and failed starts.

**Conclusion.** Feedback delay is part of controller correctness and capacity safety.

### Example 5

**Situation.** A worker remains healthy but cannot contact the deployment controller.

**Reasoning.** If its installed workload and credentials are valid, marking it unready would remove serving capacity and may trigger replacement that cannot bootstrap. Expose controller degradation separately; reject only operations requiring new state and monitor local expiry.

**Conclusion.** Control reachability and data-plane serving health need separate signals.

### Example 6

**Situation.** A stale regional controller assigns a shard after global authority moved it.

**Reasoning.** The resource stores epoch 42 and rejects the regional controller's epoch 41 request even if routing delivers it. The regional controller must reacquire delegated authority before acting. A wall-clock timestamp would not establish legitimate ordering.

**Conclusion.** Fencing is enforced at the controlled resource, not only by controller cooperation.

### Example 7

**Situation.** A policy rollout receives acknowledgements from 99% of agents.

**Reasoning.** The missing 1% may own critical traffic, and acknowledgement may mean bytes received. Select canaries by capability and risk, probe authorization outcomes, inspect errors and business paths, stop on harm, and track activation/effect by workload weight.

**Conclusion.** Fleet percentage and acknowledgement are insufficient rollout evidence.

### Example 8

**Situation.** Short-lived certificates expire during a regional control partition.

**Reasoning.** Continuing forever increases compromise exposure; immediate expiry may stop safety-critical service. Predefine regional renewal or bounded emergency credentials, narrow scope and audience, audit issuance, and fail closed for privilege expansion. Test recovery and revocation after reconnection.

**Conclusion.** Credential lifetime trades outage tolerance against exposure and needs explicit degraded policy.

### Example 9

**Situation.** A recovered fleet of 100,000 agents reconnects simultaneously.

**Reasoning.** Heartbeats, snapshot fetches, lease renewal, and status reports create a thundering herd. Randomize reconnect, serve cached content by digest, prioritize revocations and authorities, limit cohorts, coalesce desired state, and preserve data-plane bandwidth.

**Conclusion.** Control-plane recovery itself must be admitted, staged, and capacity-tested.

### Example 10

**Situation.** A malicious administrator submits a validly signed route sending all payments to a capture service.

**Reasoning.** Signature proves channel authority, not acceptable policy. Agent-side constraints reject destinations outside approved trust domains; high-impact changes require separate approval; rollout is capped; immutable audit and independent stop controls support containment and trust-root response.

**Conclusion.** Control-plane compromise requires policy constraints and blast-radius defenses beyond authentication.

## Cross-Program Connections

- **Platform Engineering:** owns schedulers, controllers, configuration distribution, service routing, and fleet reconciliation.
- **Cloud Engineering:** owns provider control APIs, regional bootstrap, identity, quotas, and shared-responsibility boundaries.
- **Distributed Systems Engineering:** owns leases, epochs, consensus, replicated metadata, failure detectors, and reconfiguration.
- **Security Engineering:** owns management authorization, signing, secret distribution, revocation, compromise, and break-glass controls.
- **Software Delivery and Reliability Engineering:** owns progressive rollout, health, incident control, game days, and recovery evidence.
- **Database Engineering:** owns membership, placement, schema, replica, backup, and failover control for data engines.
- **Systems Engineering:** supplies feedback stability, safety, human authority, and physical actuator consequences.
- **API and Service Engineering:** exposes accepted, pending, active, degraded, and failed control states honestly.

## References

1. Nick McKeown et al., “OpenFlow: Enabling Innovation in Campus Networks,” *ACM SIGCOMM Computer Communication Review* 38(2), 2008. <https://doi.org/10.1145/1355734.1355746>
2. Diego Kreutz et al., “Software-Defined Networking: A Comprehensive Survey,” *Proceedings of the IEEE* 103(1), 2015. <https://doi.org/10.1109/JPROC.2014.2371999>
3. Andy Greenberg et al., “A Clean Slate 4D Approach to Network Control and Management,” *ACM SIGCOMM Computer Communication Review* 35(5), 2005. <https://doi.org/10.1145/1096536.1096541>
4. Jeffrey Dean and Sanjay Ghemawat, “MapReduce: Simplified Data Processing on Large Clusters,” *OSDI 2004*. <https://www.usenix.org/legacy/events/osdi04/tech/dean.html>
5. Mike Burrows, “The Chubby Lock Service for Loosely-Coupled Distributed Systems,” *OSDI 2006*. <https://www.usenix.org/legacy/event/osdi06/tech/burrows.html>
6. Abhishek Verma et al., “Large-scale Cluster Management at Google with Borg,” *EuroSys 2015*. <https://doi.org/10.1145/2741948.2741964>
7. RFC 7426, “Software-Defined Networking (SDN): Layers and Architecture Terminology,” IETF, January 2015. <https://www.rfc-editor.org/rfc/rfc7426>
8. Betsy Beyer et al., eds., *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly Media, 2016. <https://sre.google/sre-book/table-of-contents/>

## Exercises

### Exercise 1

Define management plane, control plane, data plane, desired state, observed state, reconciler, snapshot, delta, lease, epoch, fencing, fail-static, fail-open, fail-closed, blast radius, control-loop stability, bootstrap dependency, and control debt.

### Exercise 2

A control plane is unavailable for 15 minutes while 40 updates/s arrive. After recovery it can process 100 updates/s total. Calculate simple backlog and drain time. Repeat for capacity 40 and 30 updates/s, and explain why snapshots, priority, and heterogeneous work alter the result.

### Exercise 3

Diagnose a fleet that reads every authorization decision synchronously from one global controller, applies unordered deltas, uses timestamps for authority, restarts when control is unreachable, and reports deployment success on receipt. Design a safer architecture and evidence chain.

### Exercise 4

Compare global versus regional controllers, push versus pull delivery, snapshot versus delta distribution, and fail-static versus fail-closed behavior for routes, certificate renewal, access revocation, autoscaling, and database placement.

### Exercise 5

Design management, control, and data planes for a distributed municipal water system with pumps, valves, quality sensors, treatment plants, intermittent links, cyber threats, maintenance, environmental limits, and emergency operators. Cover authority, feedback, local autonomy, expiry, bootstrap, configuration, safety, compromise, capacity, recovery, evidence, and human stop controls.

## Answers to the Exercises

### Answer 1

The **management plane** accepts human or administrative intent, approval, and audit. The **control plane** computes or reconciles desired policy, authority, placement, routing, or configuration. The **data plane** executes ordinary work from installed decisions. **Desired state** is intent; **observed state** is measured reality; a **reconciler** repeatedly acts on their difference. A **snapshot** is one coherent version; a **delta** is a base-dependent increment. A **lease** grants time-bounded authority; an **epoch** orders authority generations; **fencing** makes resources reject obsolete generations. **Fail-static** retains validated state, **fail-open** permits, and **fail-closed** refuses under uncertainty. **Blast radius** bounds affected scope. **Control-loop stability** is convergence without harmful oscillation. A **bootstrap dependency** is needed to start or recover even if warm serving tolerates its loss. **Control debt** is accepted desired state not yet effectively reconciled.

### Answer 2

Fifteen minutes is 900 seconds, so backlog is $40(900)=36{,}000$ updates. At total capacity 100, net drain is $100-40=60$ updates/s and ideal drain time is $36{,}000/60=600$ seconds, or ten minutes. At capacity 40 the net rate is zero, so old backlog never drains. At 30, ongoing arrivals exceed capacity by ten updates/s and backlog grows. A current snapshot can coalesce superseded desired states but not audit events or actions whose intermediates matter. Priority preserves revocations and authority changes. Validation, retries, dependencies, and unequal action cost invalidate the constant-work assumption, so measured recovery needs more reserve.

### Answer 3

Compile stable policy for authenticated local enforcement and keep a protected fresh path for urgent revocation and high-risk grants; one global request-time dependency should not decide every capability. Distribute coherent authenticated snapshots, or deltas carrying base version, order, identity, and gap recovery. Use an authority service to issue monotonic epochs and enforce fencing at resources; timestamps are evidence, not authority. Separate control reachability from serving readiness: valid installed state continues within operation-specific age, certificate, and policy bounds, while fresh-control operations stop.

Track management acceptance, validation, scheduling, delivery, agent activation, capability probe, observed effect, convergence, and failures separately. Test cold bootstrap, control partition, stale agent, missing delta, revocation, signer compromise, reconnection herd, and mixed versions. Roll out by risk-weighted cohorts with stop conditions. Evidence includes actor and intent, version/digest, epoch, target, agent result, last-known-good age, user behavior, rollback or repair, and audit continuity.

### Answer 4

A global controller simplifies global uniqueness and policy but raises latency and blast radius; regional controllers scale and survive isolation but need delegated scope, epochs, and reassignment. Push reduces notification latency but creates fleet fan-out and reconnect pressure; pull lets agents pace recovery but adds polling delay; hybrid notification plus fetch is often useful. Snapshots give coherent bootstrap and gap repair at transfer cost; deltas save bandwidth but require base, order, idempotency, and snapshot fallback.

Routes can often fail-static within topology and certificate bounds. Certificate renewal needs regional or offline-authorized paths before expiry; privilege expansion fails closed, while selected emergency service uses preauthorized scoped credentials. Revocation favors urgent deny propagation and conservative expiry. Autoscaling can pause control changes while existing capacity serves, with admission if load grows. Database placement continues current fenced ownership but stops unsafe reconfiguration when authority is unavailable. Each choice needs capability-specific freshness, security, capacity, bootstrap, and observed-effect evidence.

### Answer 5

The management plane authenticates engineers, plant operators, safety officers, and emergency commanders; it requires scoped approval, previews changes, preserves immutable audit, and offers an independent physical and local digital stop. The control plane maintains treatment targets, environmental constraints, pump/valve authority epochs, maintenance state, and topology. Regional plant controllers reconcile bounded desired state with local sensor observation. The data plane samples sensors and executes already authorized bounded control locally; remote dashboards do not drive actuators synchronously.

Each safety loop has declared sample age, actuator delay, stable gains or rule bounds, saturation, interlock, and fail-safe state. Loss of central control leaves authenticated last-known-good targets only until capability-specific expiry. Local quality protection and pressure limits remain; nonessential optimization pauses. New remote privilege and broad set-point changes fail closed. Emergency operators use authenticated, two-person where warranted, time-limited local authority with visible audit and physical confirmation.

Snapshots bind plant, schema, dependencies, policy epoch, digest, and validity; deltas require a known base and fall back to snapshot on gaps. Actuators persist the highest epoch and reject stale controllers. Bootstrap uses protected local trust roots and sealed safe configuration, and is tested after total power loss. Control traffic has priority classes for safety stops, revocation, current state, routine optimization, and telemetry; reconnect and backlog are staged and coalesced only where intermediate history is irrelevant.

Threat controls constrain signed commands by physical asset, rate, range, environmental rule, and approved topology, so a compromised signer cannot command every plant. Secrets are scoped and rotatable offline. Evidence records sensor provenance and age, desired/observed state, command identity, controller and actuator epoch, interlock result, physical acknowledgement, operator, degraded mode, queue age, recovery, and environmental outcome. Exercises include delayed/noisy sensors, link loss, stuck valve, duplicate controller, clock error, malicious configuration, expired credentials, plant restart, regional flood, and central restoration. Recovery reconciles digital state with physical reservoir, pressure, chemical, and valve state before ordinary automation resumes.
