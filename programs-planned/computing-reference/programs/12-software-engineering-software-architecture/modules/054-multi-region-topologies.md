---
module_id: SARCH-054
program: Software Engineering: Software Architecture
level: 2
module_number: 54
title: Multi-Region Topologies
status: complete
last_verified: 2026-09-06
---

# Multi-Region Topologies

## One-Page Review

### Governing question

Which authorities, data, requests, and recovery capabilities should exist in each region so that locality, consistency, resilience, sovereignty, capacity, and operating complexity form an explicit contract rather than an “active-active” label?

### Essential definitions

- A **region** is a geographically and operationally bounded deployment location; its true failure independence depends on power, network, identity, software, provider, and control dependencies.
- A **topology** is the arrangement of request ingress, compute, state authority, replicas, control planes, and inter-region flows.
- **active-passive** normally serves writes from one region while another prepares for promotion; **active-active** permits useful serving in more than one region but says nothing precise about write authority or consistency.
- **home region** is the normal authority or locality assigned to a tenant, key, or workflow.
- **failover** moves serving or authority after failure; **failback** deliberately returns or redistributes it later.
- **fencing** prevents an old or isolated authority from continuing after a newer epoch exists.
- **recovery point objective (RPO)** is the maximum targeted data-loss interval for a disruption class; **recovery time objective (RTO)** is the maximum targeted restoration interval.
- **traffic steering** selects a destination using health, identity, policy, locality, and capacity; DNS is one possible mechanism, not an authority protocol.
- **regional evacuation** moves or rejects workload before or during a regional threat.
- **degraded mode** provides a narrower explicitly safe service when the ordinary topology cannot.

### Central model, mechanism, or theorem

Suppose $n$ equal active regions each carry utilization $u$ of its safe regional capacity. If one region fails and its work redistributes evenly with no shedding or spare pool, each survivor receives utilization

$$
u'=u\frac{n}{n-1}.
$$

Survival requires $u'\le1$, hence $u\le(n-1)/n$. With three regions, normal utilization must be at most $2/3$ before accounting for skew, failover inefficiency, recovery work, dependency limits, and safety margin. Redundancy without reserved capacity can preserve copies while losing service.

A synchronous inter-region commit must wait for the acknowledgement set required by its protocol. Its latency is therefore lower-bounded by the relevant communication path plus processing; topology cannot promise local-write latency and remote synchronous confirmation simultaneously when distance dominates.

### Critical invariants

- every operation names its current write authority, consistency, residency, and degraded behavior;
- a region label never substitutes for an enumerated fault model and dependency map;
- at most one authority epoch may make mutually exclusive decisions where the invariant requires it;
- failover traffic fits tested destination capacity after skew, retries, repair, and control traffic;
- routing health represents the capability required by the request, not process liveness alone;
- replication state, promotion eligibility, fencing, and cutover evidence are distinct;
- RPO and RTO are defined per disruption, data class, and business capability and are tested;
- asynchronous replication never receives a zero-data-loss claim without evidence that closes the gap;
- residency, encryption, identity, audit, backup, and deletion constraints survive failover and repair;
- external effects and ambiguous operations are reconciled before recovery is declared complete;
- failback is treated as another migration with capacity, compatibility, and authority checks;
- common global dependencies appear in the topology and have failure behavior;
- operators can stop automated movement and exercise bounded manual authority;
- exercises test isolation, delay, stale routes, split authority, capacity loss, restoration, and compromise.

### Common failures

Common failures include calling two read replicas “active-active”; multiplying regional availability as if failures were independent; routing all displaced traffic into regions without reserve; promoting a lagging replica while claiming RPO zero; using DNS expiry as write fencing; letting both sides of a partition elect themselves; measuring replication bytes but not business effects; depending globally on one identity, key, configuration, artifact, or routing service; violating residency during evacuation; keeping write-capable disaster credentials untested or overprivileged; failing over compute while a state authority remains unreachable; and automatically failing back into mixed versions or an unreconciled backlog.

### Compact example

Three regions each serve 55% of safe capacity. Losing one raises the even-share load to $0.55(3/2)=0.825$ before retries and repair, leaving some reserve. At 75%, loss raises it to $1.125$, so the topology is predictably overloaded even if routing is perfect. The design must reserve capacity, shed optional work, use a warm pool, or narrow the failover promise.

### Connections

[SARCH-051](051-partial-failure-as-an-architectural-constraint.md) supplies partial failure, [SARCH-052](052-consistency-and-availability-trade-offs.md) supplies consistency choices, and [SARCH-053](053-partitioning-and-data-placement.md) supplies placement. [SARCH-055](../ROADMAP.md) next separates control and data planes. Platform Engineering owns deployment machinery; this module owns topology contracts and cross-region consequences.

## Governing Question

Adding a second region creates more than another copy. It adds distance, asynchronous state, authority transfer, traffic steering, capacity reservation, jurisdiction, new control dependencies, and recovery paths. The same deployment can improve one failure mode while worsening consistency, latency, cost, or operator risk.

Architecture must therefore name who serves what before, during, and after disruption. “Multi-region” is a location count; “active-active” is an aspiration. Neither specifies writable objects, conflict rules, routing convergence, promotion evidence, or user outcomes.

## Why This Matters

Regional incidents are often compound: network isolation creates stale health, retries raise load, operators initiate failover, replicas repair, and a control plane is itself degraded. The recovery action can cause the second failure. A diagram with arrows but no states, capacities, or invariants is not a resilience design.

Multi-region choices also shape daily behavior. Synchronous writes pay distance continuously. Home-region ownership improves locality but complicates travel and tenant movement. Global replicas can cross legal boundaries. The normal path and the emergency path must be one coherent architecture.

## Prerequisites and Retrieval

Retrieve region, zone, failure domain, partial failure, consistency model, quorum, leader, replica, partition, routing, DNS, health check, lease, epoch, fencing, idempotency, RPO, RTO, backup, restore, traffic capacity, tail latency, data residency, control plane, data plane, degraded mode, reconciliation, and runbook.

From SARCH-011 retrieve availability and recovery tactics; SARCH-025 and SARCH-049 provide deployment and environment topology; SARCH-041 provides system-of-record authority; SARCH-051 through SARCH-053 provide partial failure, consistency, partitioning, and placement.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish active-passive, active-read, partitioned-active, multi-leader, quorum, and cell-based regional topologies;
2. state write authority and consistency per operation rather than per diagram;
3. derive elementary failover-capacity and latency constraints and identify their assumptions;
4. separate routing, replication, promotion eligibility, and fencing;
5. design RPO and RTO claims per failure and data class;
6. identify global dependencies that defeat regional independence;
7. preserve residency, identity, encryption, audit, and deletion through evacuation;
8. design controlled failover, reconciliation, and failback state machines;
9. choose degraded regional behavior from business and safety obligations;
10. evaluate game-day evidence without generalizing beyond tested scenarios.

## Core Exposition

**Start with capabilities and fault sets.** Name the business capability, actors, state authorities, dependencies, and terminal outcomes. Then state disruptions: one zone lost, whole region unreachable, inter-region delay, control-plane loss, corrupt rollout, credential compromise, provider-wide dependency failure, or evacuation order.

Different faults require different responses. A network-isolated region may still have working compute and stale credentials; a corrupted region should not automatically receive authority elsewhere while continuing to write. A natural disaster, software defect, and malicious administrator do not share one independence model.

**Define region honestly.** A provider region may contain several zones, but independence is bounded by documented and observed dependencies. Cross-region deployments can still share identity, DNS, certificates, source artifacts, libraries, operator access, quotas, or a global database.

Map these dependencies. For each claim, ask what cause could defeat all sites. Diversity may reduce common mode but increases integration, skill, drift, and recovery complexity. Independence is engineered and tested, not inferred from geography.

**Distinguish topology families.** In active-passive, one region normally owns writes and another maintains recovery state. Cold standby requires provisioning and restoration; warm standby runs partial capacity; hot standby maintains near-serving capability. These are capacity and readiness claims, not marketing tiers.

Active-read serves safe reads in additional regions while writes remain authoritative elsewhere. Partitioned-active assigns each tenant or key a home region, so all regions serve useful traffic but each object may still have one writer. Multi-leader permits several write authorities and needs explicit conflict semantics. Global quorum or consensus coordinates an acknowledgement set across placements. Cells repeat a bounded stack and route identities to cells.

**Specify per-operation authority.** A product may use regional catalog reads, home-region account writes, globally coordinated uniqueness, asynchronous analytics, and local emergency operations. Put this matrix in the design.

Authority includes epoch and scope. “Region A is primary” is incomplete when some partitions have moved, workflows are pending, or a control-plane lease expired. Storage must reject obsolete authority, not rely only on routers behaving correctly.

**Model distance.** Information cannot be synchronously confirmed across regions without communication. A protocol needing remote acknowledgement incurs at least the relevant network path and processing; tail latency and retransmission matter. Local acknowledgement can be faster but leaves a replication gap or changes the commit definition.

Choose from the invariant and user deadline. Strongly ordered money reservation may pay coordination; a product-view counter may replicate asynchronously. Do not make all fields pay the strictest operation's latency by accidental shared transaction scope.

**Model failover capacity.** Capacity is multidimensional: requests, compute, memory, storage operations, network, connections, quotas, third-party calls, and operator throughput. Normalize by safe, tested capacity, not theoretical maximum.

For equal active regions and even redistribution, one-loss utilization scales by $n/(n-1)$. Real traffic is skewed and sticky. Cache coldness, retries, replica repair, queue replay, and connection churn consume reserve. Model each constrained dependency and apply admission before overload destroys recovery.

**Choose traffic steering as policy.** Anycast, global proxy, DNS, client selection, and service routing have different observation and convergence. Health must represent the requested capability. A region may serve cached browsing but not account writes.

Routing and authority are separate. DNS can direct traffic but cannot fence an old writer. Clients may cache beyond intended TTL, reuse connections, or retry another region. Requests carry durable identity and resolve current authority at a trusted boundary.

**Design active-passive promotion.** Define replication mode, lag measures, promotion eligibility, decision authority, fencing, endpoint change, dependency readiness, capacity, validation, and rollback. Promotion converts a replica into authority; copy presence alone is insufficient.

Automatic promotion reduces delay but can amplify false suspicion or corruption. Manual promotion adds human latency and error. Use automation for verified mechanics and bounded policy; require explicit approval where ambiguity or harm demands it.

**Design partitioned-active ownership.** Assign tenants, keys, or jurisdictions a home region. Requests route to home authority, while replicas elsewhere support reads or recovery. This avoids concurrent writes for many operations and keeps latency local to the owner.

Traveling users pay remote latency unless a safe local projection or ownership move exists. Home moves are migrations: copy, catch up, fence, change routing epoch, validate, and reconcile. Large tenants and uneven geography require capacity-aware placement.

**Design multi-leader only with conflict semantics.** Local writes improve availability and latency under partition, but concurrent state must merge, reject, compensate, or reach human resolution. Last-write-wins is a selection rule, not a universal business policy.

Preserve causal context and durable operation identity. Test deletion, uniqueness, monetary bounds, authorization, and older clients. Some data can use multi-leader while invariant-sensitive commands retain one authority.

**Design global quorum placement.** A quorum can tolerate some replica loss while preserving protocol intersection. Place voters so the desired failure can lose a subset without losing progress, and understand which region combinations can form authority.

An even voter count may not add failure tolerance. Witnesses can participate in authority without storing full data, but their exact protocol role matters. Avoid a topology where two regions depend on a third region's tiny voter and untested network path for every commit.

**Define RPO and RTO per scope.** RPO zero for acknowledged writes requires that the acknowledgement definition and recovery path preserve them under the named fault. Asynchronous replication ordinarily permits a nonzero gap if authority disappears before transfer. Backups may address corruption but have longer recovery.

RTO starts at a declared event and ends at a declared useful capability, not when a process launches. Separate detection, decision, fencing, provisioning, restore/catch-up, routing, cache warm-up, validation, and reconciliation. State excluded disasters and dependencies.

**Separate availability from disaster recovery.** A continuously available topology handles some faults without a recovery event. Disaster recovery restores service after loss. High availability within one region may not cover regional destruction; a remote backup may preserve data but not meet a short serving RTO.

Use both where required. Test restore independently from replica failover because logical corruption and deletion can replicate everywhere. Preserve isolated recovery copies and credentials according to threat and policy.

**Preserve governance across regions.** Data residency can constrain primary state, replicas, backups, logs, caches, queues, analytics, support access, key custody, and repair transit. Regional failure does not silently suspend law or contract.

Predefine legal failover destinations and degraded behavior. If no compliant destination exists, reject or provide a narrower local service. Record which authority approved emergency access, expiry, and subsequent review.

**Design identity and keys for isolation.** A globally central identity or key service can make every region depend on one location. Replicating credentials introduces revocation, compromise, and clock issues. Use scoped credentials, bounded cache, regional verification material, explicit policy epochs, and protected emergency paths.

Key placement may be part of sovereignty. Rotation, revocation, restore, and failover must work without granting every region universal decryption. Audit emergency use and make it expire.

**Treat replication lag as multidimensional.** Time lag, byte lag, operation lag, commit position, and business-state lag answer different questions. A replica can be seconds behind yet miss a critical revocation, or hours behind on cold data without affecting service.

Expose eligibility based on the capability's requirements. Before promotion, verify schema, configuration, indexes, encryption, policy epoch, change-stream position, and external dependencies, not only byte count.

**Handle ambiguous in-flight work.** During steering or authority loss, clients retry and responses disappear. A completed effect in the old region may be unknown to the new. Preserve one business identity across attempts, reject stale epochs, query status, and reconcile.

Queues and workflows cross regions too. Duplicate delivery, reorder, backlog, and schema skew must be bounded. A green database does not prove shipments, payments, messages, or physical commands agree.

**Design failback deliberately.** The former region may contain stale data, old code, queued work, expired credentials, and changed topology. Reintroduce it as a new deployment and data movement, not a reverse DNS switch.

Verify compatibility, copy direction, authority, capacity, and policy. Shift traffic gradually, observe, and preserve rollback. Sometimes the new topology should remain; recovery objectives need not imply returning immediately.

**Control automation and humans.** Automated steering can react faster than operators but can oscillate on partial health or spread corruption. Add hysteresis, minimum evidence, movement budgets, maximum blast radius, and a stop control.

Runbooks state decision rights and evidence. Practice with realistic access controls. Break-glass credentials that are never tested may fail; permanently broad credentials create another disaster.

**Observe end-to-end regional state.** Record request identity, chosen region, home region, route decision, routing and authority epochs, consistency mode, data version, replication position, capacity, degraded mode, promotion state, recovery objective, and reconciliation outcome without leaking secrets.

Synthetic probes should exercise user capabilities from outside each region. Internal health misses global routing, certificates, identity, and last-mile reachability. Keep regional and global views so a global aggregator outage does not erase local evidence.

**Test the transitions.** Exercise one-way isolation, total region loss, control-plane loss, stale route, lagging replica, full destination, shared dependency loss, corrupt write, credential revocation, schema skew, queue backlog, and return of the old region.

Measure user outcomes, RPO, RTO components, lost or duplicated effects, capacity, and manual decisions. A successful game day supports only the exercised fault, scale, version, and environment; expand when a defect indicates a broader class.

## Definitions and Notation

Let:

- $G=\{g_1,\ldots,g_n\}$ be regions and $F$ the declared disruption set;
- $A_e(k)$ be the write authority for key $k$ under authority epoch $e$;
- $u_i^{(d)}$ be region $i$'s utilization in resource dimension $d$ relative to safe capacity;
- $x_{ij}$ be traffic shifted from failed region $i$ to surviving region $j$;
- $H_j^{(d)}$ be reserved headroom in region $j$ and resource dimension $d$;
- $\ell_{ij}$ be an observed latency distribution between regions $i$ and $j$;
- $q$ be the acknowledgement set required for an operation;
- $\delta$ be replication position gap under an explicitly named metric;
- $t_d,t_a,t_f,t_p,t_c,t_r,t_v$ be detection, authorization, fencing, provisioning, catch-up, routing, and validation durations;
- **RPO** mean the targeted maximum loss point under a named disruption;
- **RTO** mean the targeted time to a named useful capability under that disruption.

A decomposed recovery model can use

$$
T_{restore}=t_d+t_a+t_f+t_p+t_c+t_r+t_v,
$$

when stages are sequential. Parallel work changes the critical path, and uncertainty, retries, and manual delay require measured distributions rather than a single guaranteed sum.

## Mechanisms, Invariants, or Proof Structure

### Topology-design procedure

1. Name capabilities, state authorities, users, locations, and terminal outcomes.
2. Declare disruption, consistency, latency, RPO, RTO, residency, and security requirements per operation and data class.
3. Draw ingress, compute, state, replica, control, identity, key, artifact, observability, backup, and external-dependency flows.
4. Choose active-passive, active-read, partitioned-active, multi-leader, quorum, cell, or mixed ownership deliberately.
5. Model normal and failed capacity in every constrained resource, including repair and retry amplification.
6. Define routing, health, epochs, promotion eligibility, fencing, and in-flight identity.
7. Define degraded service, admission, evacuation, reconciliation, and manual authority.
8. Define restoration and failback as versioned migrations.
9. Exercise transitions and record evidence bounded to the tested fault and environment.

### Capacity derivation

If $n$ equal regions each serve load $uC$, total load is $nuC$. After one loss, $n-1$ regions share it, so each receives $nuC/(n-1)$ and utilization $u'=un/(n-1)$. Requiring $u'\le1$ yields $u\le(n-1)/n$. This is necessary only under the simplified even, equal-capacity, no-overhead model; real designs need more reserve.

### Architectural invariants

- no topology label without per-operation authority and failure semantics;
- no promotion without current evidence, explicit decision authority, and fencing;
- no failover promise without capacity and dependency proof for the destination;
- no RPO/RTO claim without failure scope, start/end boundary, and exercise evidence;
- no regional recovery declaration before business effects and in-flight ambiguity reconcile;
- no emergency topology that silently violates jurisdiction or security policy.

## Alternatives and Trade-Offs

| Topology | Primary strength | Cost or risk | Required evidence |
|---|---|---|---|
| cold standby | lower steady cost | long provisioning/restore RTO | reproducible build and restore |
| warm standby | faster recovery | drift and uncertain capacity | promotion and load exercise |
| hot active-passive | short promotion path | idle cost and split authority risk | lag, fencing, routing test |
| active-read | local read latency | stale reads and remote writes | freshness and session behavior |
| partitioned-active | local home writes | uneven placement and home moves | directory, capacity, migration |
| multi-leader | local write continuity | domain conflicts and reconciliation | causal/conflict histories |
| global quorum | strong coordinated authority | distance latency and quorum loss | voter placement and partitions |
| cell-based regions | bounded blast radius | fleet and routing complexity | cell independence and evacuation |
| multi-provider | reduced provider common mode | operational and semantic divergence | portability and joint recovery |
| compliant local degrade | preserves lawful essential service | narrower functionality | policy, expiry, and audit |

## Failure Modes and Misconceptions

1. **“Multi-region means region-resilient.”** shared dependencies or insufficient capacity may defeat it.
2. **“Active-active means every region can write everything.”** the label does not specify authority.
3. **“Three regions provide three times availability.”** failures are correlated and service paths differ.
4. **“A replica is promotable.”** lag, version, policy, indexes, capacity, and fencing remain.
5. **“DNS performs failover.”** it steers some traffic and cannot revoke write authority.
6. **“RPO zero means no loss ever.”** the claim must name acknowledgement and disruption scope.
7. **“RTO ends when hosts start.”** useful business capability and reconciliation are later boundaries.
8. **“Asynchronous means eventually safe.”** invariant violations and external effects may persist.
9. **“All regions should use the same topology.”** operations and jurisdictions differ.
10. **“Global quorum always survives one region.”** voter distribution determines progress.
11. **“Failover capacity equals normal spare CPU.”** caches, retries, repair, quotas, and dependencies constrain it.
12. **“Automatic is safer.”** automation can amplify false suspicion, corruption, or overload.
13. **“Residency pauses during disaster.”** emergency behavior must remain authorized.
14. **“Global identity is outside the topology.”** it can be the common point of failure.
15. **“Replication replaces backup.”** corruption and deletion can replicate.
16. **“Failback is just reverse routing.”** it is a migration across changed state and versions.

## Worked Examples

### Example 1

**Situation.** Three equal regions normally run at 75% of safe capacity and promise survival of any one loss.

**Reasoning.** Even redistribution produces $0.75(3/2)=1.125$, already 112.5% before retries, cold caches, and repair. Routing cannot satisfy the promise. Reduce normal load below a tested reserve, add failover capacity, or explicitly shed lower-priority work.

**Conclusion.** Replica and region counts do not replace failed-state capacity arithmetic.

### Example 2

**Situation.** Two regions synchronously acknowledge a payment reservation across an observed 90-ms round-trip path.

**Reasoning.** Any commit requiring the remote acknowledgement cannot complete before the required communication and processing. Local response below that path bound would mean the remote acknowledgement was not on the commit critical path or the measurement/scope differs. Batch, pipeline, or place authority nearer users, but do not promise contradictory semantics.

**Conclusion.** Distance constrains synchronous confirmation; topology must choose latency and acknowledgement scope honestly.

### Example 3

**Situation.** A passive replica is 45 seconds behind when its primary region disappears.

**Reasoning.** Promotion may lose acknowledged state within the gap unless acknowledgements had already included durable remote storage. If payment loss is unacceptable, pause, recover another copy, or reconcile with external authorities. The UI reports recovery, not an unsupported RPO-zero claim.

**Conclusion.** Promotion availability and accepted data loss are separate decisions.

### Example 4

**Situation.** DNS points writes to region B, but a client keeps its connection to isolated region A.

**Reasoning.** DNS convergence does not fence A. Advance the authority epoch through a protocol A cannot satisfy; B accepts the new epoch and storage rejects A's old token. Preserve operation identity because the client may retry an ambiguous write at B.

**Conclusion.** Traffic steering changes destination; fencing changes authority.

### Example 5

**Situation.** European and North American tenants have home regions, and one customer relocates.

**Reasoning.** Copy the tenant to a permitted target, stream changes, validate policy and state, fence the old epoch, update the authoritative directory, drain stale routes, and retain governed rollback evidence. During the move, define read freshness and write routing rather than allowing both homes.

**Conclusion.** Home-region reassignment is an online authority migration.

### Example 6

**Situation.** Two leaders accept concurrent edits to a profile color and a medication order.

**Reasoning.** Profile color may use a declared deterministic winner while preserving audit. Medication orders cannot discard one clinician's intent by timestamp; use one authority, a domain conflict requiring review, or a protocol preserving the clinical invariant. The same topology can choose differently per field.

**Conclusion.** Multi-leader acceptability is determined by domain conflict semantics.

### Example 7

**Situation.** Five voters are placed three in region A and one each in B and C.

**Reasoning.** A majority needs three. Loss of A leaves two and stops progress; loss of B or C leaves four. The topology tolerates some single-region losses but not any single-region loss. Reposition voters according to the intended fault set and latency path.

**Conclusion.** Quorum resilience follows voter geometry, not total replica count.

### Example 8

**Situation.** A regional evacuation sends health records to the nearest unconstrained region.

**Reasoning.** If residency and key-custody rules forbid that destination, urgency does not silently authorize the copy. Predeclare compliant recovery regions or provide a narrower local mode. Record emergency authority, scope, expiry, and review if policy permits an exception.

**Conclusion.** Resilience behavior must remain inside governance or explicitly enter an authorized emergency policy.

### Example 9

**Situation.** Restoration stages take 2, 5, 1, 12, 20, 4, and 6 minutes sequentially.

**Reasoning.** The simple sum is 50 minutes. If the RTO is 45, optimism about a 12-minute host start is irrelevant. Parallelizing safe stages may shorten the critical path; otherwise reduce stages or change the objective, then measure distributions in exercises.

**Conclusion.** RTO engineering follows the end-to-end critical path to useful service.

### Example 10

**Situation.** After failover, automation shifts traffic back as soon as region A reports healthy.

**Reasoning.** A may have stale data, old binaries, cold caches, queued work, and expired policy. Rebuild and validate it, reconcile old effects, introduce read traffic, then bounded writes under a new epoch. Hysteresis prevents route oscillation if health flaps.

**Conclusion.** Failback is controlled reintegration, not the inverse of failover.

## Cross-Program Connections

- **Distributed Systems Engineering:** owns consensus, replication, clocks, leases, failure detectors, and formal progress/safety analysis.
- **Platform Engineering:** owns regional substrate, routing, deployment, capacity, topology enforcement, and evacuation mechanisms.
- **Cloud Engineering:** owns provider-region services, network and identity design, cost, portability, and shared-responsibility evidence.
- **Database Engineering:** owns replication mode, commit semantics, promotion, backup, restore, and database recovery.
- **Security Engineering:** owns credential scope, key custody, compromise response, emergency authority, and cross-region audit.
- **Data Architecture Engineering:** owns residency, lifecycle, authority, lineage, deletion, and governed movement.
- **Software Delivery and Reliability Engineering:** owns RPO/RTO validation, game days, incident command, SLOs, and restoration evidence.
- **Systems Engineering:** connects regional degradation and recovery to physical operations, people, and safety.

## References

1. Giuseppe DeCandia et al., “Dynamo: Amazon's Highly Available Key-value Store,” *SOSP 2007*. <https://doi.org/10.1145/1294261.1294281>
2. James C. Corbett et al., “Spanner: Google's Globally-Distributed Database,” *OSDI 2012*. <https://www.usenix.org/conference/osdi12/technical-sessions/presentation/corbett>
3. Wyatt Lloyd et al., “Don't Settle for Eventual: Scalable Causal Consistency for Wide-Area Storage with COPS,” *SOSP 2011*. <https://doi.org/10.1145/2043556.2043593>
4. Jason Baker et al., “Megastore: Providing Scalable, Highly Available Storage for Interactive Services,” *CIDR 2011*. <https://www.cidrdb.org/cidr2011/Papers/CIDR11_Paper32.pdf>
5. Tim Kraska et al., “MDCC: Multi-Data Center Consistency,” *EuroSys 2013*. <https://doi.org/10.1145/2465351.2465363>
6. Jeffrey Dean and Luiz André Barroso, “The Tail at Scale,” *Communications of the ACM* 56(2), 2013. <https://doi.org/10.1145/2408776.2408794>
7. Betsy Beyer et al., eds., *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly Media, 2016. <https://sre.google/sre-book/table-of-contents/>
8. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly Media, 2017.

## Exercises

### Exercise 1

Define region, topology, active-passive, active-read, partitioned-active, multi-leader, home region, failover, failback, fencing, traffic steering, RPO, RTO, regional evacuation, and degraded mode.

### Exercise 2

Four equal active regions run at utilization 0.68. Derive utilization after one evenly redistributed loss and after two losses. State the maximum normal utilization permitted by the simple model for one-loss and two-loss survival, and identify missing real-world costs.

### Exercise 3

Diagnose a failover system that promotes on a 20-second health timeout, changes DNS, has unknown replica lag, reuses one global administrator credential, assumes destination capacity, retries writes with new IDs, and automatically fails back on process health. Provide a safe state machine and evidence.

### Exercise 4

Compare hot active-passive, partitioned-active home regions, multi-leader, and global quorum for payment authorization, collaborative documents, product catalog, access revocation, and analytics. Explain latency, consistency, partition behavior, capacity, conflicts, and recovery.

### Exercise 5

Design a multi-region topology for an international rail-control and passenger system spanning signaling, train telemetry, ticketing, payments, timetables, maintenance, national regulation, intermittent cross-border links, and public-safety emergencies. Cover authorities, latency, consistency, residency, capacity, routing, degraded modes, RPO/RTO, fencing, external effects, recovery, failback, evidence, and human control.

## Answers to the Exercises

### Answer 1

A **region** is a geographically and operationally bounded location whose independence must be demonstrated. A **topology** arranges ingress, compute, state, replicas, controls, and flows. **Active-passive** keeps normal authority in one region and prepares another; **active-read** serves selected reads elsewhere; **partitioned-active** gives different keys home authorities; **multi-leader** permits concurrent regional writes. A **home region** is a key's normal authority or locality. **Failover** moves service or authority; **failback** reintegrates or returns it. **Fencing** rejects obsolete authority. **Traffic steering** chooses a destination but does not grant authority. **RPO** targets maximum loss point and **RTO** targets time to a defined useful service for a named disruption. **Regional evacuation** moves or rejects workload around a threat. A **degraded mode** is narrower explicitly safe service.

### Answer 2

With four regions, one loss gives $0.68(4/3)\approx0.907$. Two losses give $0.68(4/2)=1.36$, so capacity is insufficient. For one-loss survival the simple bound is $(4-1)/4=0.75$; for two-loss survival it is $(4-2)/4=0.50$. These are necessary under equal capacity and even redistribution. Real reserve must cover geographic skew, sticky sessions, unavailable dependencies, retries, cold caches, connection churn, queue replay, replica repair, control traffic, quotas, background work, and safety margin.

### Answer 3

A timeout is suspicion, DNS is routing, and neither grants or revokes authority. Detect capability loss from multiple scoped signals; query replication position, schema/configuration/policy epoch, index state, destination dependencies, and tested capacity; classify whether corruption or compromise is possible; and obtain the required automated or human decision. Fence the old writer with a new authority epoch before or atomically with promotion. Promote only an eligible copy, expose actual RPO, shift bounded traffic, and preserve the same business identities across ambiguous retries. Use scoped regional and emergency credentials rather than one universal administrator.

Validate business outcomes, external effects, lag, capacity, and degraded behavior. Retain incident evidence. Rebuild the old region as untrusted changed state, reconcile its queues and writes, verify current software and policy, then reintroduce traffic gradually under another controlled epoch. Process health alone cannot trigger failback; hysteresis and a stop control prevent oscillation.

### Answer 4

Payment authorization usually needs one account authority or coordinated quorum; hot standby shortens recovery but requires fencing, while partitioned home regions keep normal writes local. Collaborative documents may use home ownership or causally aware multi-leader operations with domain merge; conflicts and offline behavior remain visible. Catalog reads suit active-read or multi-leader for mergeable fields, with authoritative price and recall rules separated. Access revocation needs strongly ordered policy epochs, bounded caches, and explicit emergency behavior. Analytics can replicate asynchronously and tolerate stated lag.

Hot active-passive simplifies ordering but leaves promotion, remote latency, and reserved-capacity costs. Partitioned-active improves local writes but creates home routing, skew, and migration. Multi-leader improves partition-time acceptance but requires causal context and domain resolution. Global quorum offers coordinated authority under its voter fault model but pays distance and may lose progress for some partitions. Recovery for every option includes ambiguous requests, external effects, data repair, capacity, and governed failback.

### Answer 5

Safety-critical signaling authority remains bounded to each physical control area with authenticated current epochs, local redundant control, and fail-safe behavior; no distant passenger-system region may assume it. Train telemetry can buffer locally with monotonic identity and reconcile later. National timetable and maintenance authorities publish versioned plans; stale data is labeled and cannot override current movement authority. Tickets use passenger or journey home regions, while seat rights are allocated so disconnected sellers cannot oversubscribe. Payments preserve one intent identity and reconcile provider outcomes. Public read-only timetables may be broadly replicated.

Place safety, identity, passenger, payment, and audit data under applicable national residency and key-custody rules, including logs, backup, repair, and support. Cross-border routes carry only necessary signed state. Each region reserves tested capacity for its declared neighbors; optional analytics and browsing shed before dispatch, signaling, emergency communication, and maintenance safety. Routing health is capability-specific. DNS or global proxies steer users, while authority epochs and storage fencing prevent stale writers.

Define RPO/RTO separately: near-zero acknowledged-loss and short restoration for control records under the exact local fault model; bounded gaps for telemetry; explicit payment and ticket reconciliation; longer analytical recovery. Under isolation, signaling fails safe locally, trains use bounded operating rules, clinics—none exist here—are irrelevant, ticketing spends local seat rights or rejects, and passenger displays expose freshness. Promotion requires eligible state, authority, capacity, policy, and manual rail-operations approval where safety demands it.

After restoration, deduplicate commands and payments, reconcile tickets with physical journeys, validate train positions and maintenance states through their authorities, throttle repair, and retain incident evidence. Failback treats the returning region as a changed deployment and advances epochs only after validation. Evidence records route, region, authority/policy versions, data position, capacity, degraded mode, command acknowledgement, physical confirmation, payment state, manual action, RPO/RTO stages, and terminal reconciliation. Named dispatch, security, regulatory, and incident commanders hold scoped, expiring emergency powers and a tested stop control.
