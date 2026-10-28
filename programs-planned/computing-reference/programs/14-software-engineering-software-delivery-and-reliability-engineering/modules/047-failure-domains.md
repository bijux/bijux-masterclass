---
module_id: SDRE-047
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 47
title: Failure Domains
status: complete
last_verified: 2026-09-06
---

# Failure Domains

## One-Page Review

### Governing question

How can engineers discover, model, validate, and constrain the sets of resources that can fail together, instead of mistaking replica count or location labels for independent resilience?

### Essential definitions

- a **fault** is an adjudged or hypothesized cause of an error;
- an **error** is a system state that can lead to externally visible failure;
- a **failure** occurs when delivered service deviates from its specified behavior;
- a **failure domain** is a set of resources exposed to a shared cause, mechanism, control, or event that can make them unavailable or incorrect together;
- **shared fate** means resources can experience a common outcome through a shared dependency or action;
- a **fault-isolation boundary** constrains propagation or impact so failure inside need not affect resources outside;
- a **common-mode failure** defeats multiple nominally redundant elements through the same cause or mechanism;
- a **common-cause failure** is correlated failure attributable to a shared initiating cause;
- **blast radius** is the affected resource or user scope under a specified failure scenario;
- a **dependency graph** represents components and the services, controls, paths, people, and infrastructure they require;
- a **cut set** is a set of component or domain failures whose joint occurrence prevents the system from meeting a property;
- a **minimal cut set** is a cut set with no proper subset that is also a cut set;
- a **cell** is a bounded service partition with its own serving resources and constrained dependencies;
- an **update domain** groups resources exposed to the same planned change event;
- **independence evidence** supports a bounded claim that one failure does not materially change the probability of another under stated conditions.

### Central model, mechanism, or theorem

Let resources be $R$, candidate failure causes or domains be $D$, and incidence relation $E\subseteq R\times D$, where $(r,d)\in E$ means resource $r$ is exposed to domain $d$. The affected set and blast radius of $d$ are

$$
A(d)=\{r\in R:(r,d)\in E\},\qquad \beta(d)=|A(d)|.
$$

Placing replicas in distinct named zones separates the zone-domain edges; it does not remove shared edges for identity, control plane, network path, software version, deployment wave, operator, quota, data source, or region. Survival must be evaluated against explicit scenarios and required capacity, not inferred from labels.

### Critical invariants

- define the service property and user population whose survival is being evaluated;
- enumerate physical, logical, dependency, control-plane, data, change, security, and organizational domains;
- trace transitive dependencies and shared management paths, not only direct compute placement;
- treat provider labels as claims with documented scope, not universal independence guarantees;
- separate fault prevention, isolation, detection, masking, recovery, and adaptation;
- place enough capacity outside each assumed domain to meet degraded-service requirements;
- include state, quorum, traffic steering, observability, credentials, and operators in the model;
- model simultaneous and sequential failures, including repair and failover delay;
- validate assumptions with inventory evidence, change records, fault injection, and real incidents;
- revise the map when architecture, ownership, deployment, or providers change.

### Common failures

Failures include counting replicas without locating them, equating zone labels with total independence, multiplying availability percentages without testing correlation, ignoring global identity or DNS, separating compute while sharing storage, placing a quorum majority in one domain, using one deployment wave everywhere, treating planned changes as unrelated to failure, overlooking control-plane and observability dependencies, trusting documentation without workload configuration checks, testing one node rather than a domain, failing over into insufficient capacity, and assuming geographic distance eliminates software, credential, operator, or supplier common modes.

### Compact example

Three service replicas occupy three zones and three power feeds. All require one global identity service; replicas 1 and 3 also receive the same deployment wave. A zone failure affects one replica, but identity failure affects all three, and a defective deployment can affect two. The placement is diverse for the declared zone and power scenarios, not for identity or change. The next design actions are to bound identity dependence, stagger releases across serving capacity, verify failover capacity, and test each scenario.

### Connections

[SDRE-046](046-toil-and-automation.md) requires automation blast radius to follow real domain boundaries. [SDRE-048](../ROADMAP.md) next uses redundancy and diversity to tolerate the domains discovered here. [SDRE-049](../ROADMAP.md) then preserves bounded service when some domains are unavailable.

## Governing Question

“We have three replicas” is a count, not a resilience argument. The replicas may share a rack power unit, storage array, network conduit, region-level control plane, credential authority, configuration source, software defect, deployment wave, quota, or operator. A single event can therefore remove all three even when monitoring reports three distinct processes.

A failure-domain analysis asks what can fail together and why. It begins with a user-visible property—such as successful reads, accepted writes, or correct authorization—then traces every resource and control needed to deliver that property. It also asks whether boundaries actually contain propagation and whether surviving resources have enough state and capacity. The objective is not to predict every failure but to expose assumptions and bound plausible correlated harm.

## Why This Matters

The Google SRE Workbook warns against multiplying nominal availability values for replicated instances because common dependencies, common failure domains, shared fate, and global control planes violate independence [1]. This is the central corrective: probability arithmetic is only as valid as its dependency model.

AWS's current Reliability Pillar describes fault isolation as limiting failure impact to a defined boundary and recommends distributing workloads across locations and using bulkhead architectures [2]. Microsoft's current Azure documentation distinguishes hardware fault domains from availability zones and explicitly notes that availability sets remain susceptible to shared datacenter-level failures [3]. These are vendor-specific capability descriptions checked on 2026-09-06, not evidence that any particular workload is configured correctly or immune to wider causes.

NIST SP 800-160 Volume 2 Revision 1 treats segmentation, isolation, redundancy, diversity, and coordinated protection as adaptable cyber-resiliency techniques within a systems-engineering lifecycle [4]. Security compromise belongs in failure-domain analysis because shared credentials, management planes, build systems, and trust roots can correlate failure across otherwise separate physical locations.

Google's treatment of cascading failure adds a dynamic dimension: overload, retries, resource exhaustion, and recovery traffic can propagate beyond the component where a fault began [5]. A static location map is therefore insufficient. Engineers need both exposure domains—what can share an initiating cause—and containment mechanisms—what stops errors and load from crossing boundaries.

## Prerequisites and Retrieval

Retrieve fault, error, failure, reliability property, SLI, dependency, redundancy, replica, quorum, capacity, overload, timeout, retry, control plane, data plane, blast radius, deployment, credential, region, zone, rack, network path, storage, recovery, and evidence.

From SDRE-041 retrieve property-specific failure semantics. From SDRE-042 and SDRE-043 retrieve user populations and target conditions. From SDRE-045 retrieve tolerated bad service. From SDRE-046 retrieve automation scope, concurrency, and blast radius. Keep redundancy mechanisms and diversity trade-offs for SDRE-048, while using enough of them here to test whether domain separation is meaningful.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish fault, error, failure, exposure domain, and isolation boundary;
2. construct a multi-layer failure-domain inventory for a user-visible property;
3. model resource-to-domain incidence and calculate scenario blast radius;
4. identify transitive shared dependencies and common control paths;
5. explain why replica and location counts do not establish independence;
6. analyze quorum, capacity, and state placement against domain loss;
7. model change, credential, operator, and time as correlation sources;
8. derive and challenge probabilistic claims involving common cause;
9. design tests that validate domain and containment assumptions;
10. maintain a failure-domain model as governed operational evidence.

## Core Exposition

**Begin with the property, not the inventory.** A domain matters relative to behavior. Loss of a read cache may affect latency but not correctness; loss of a write quorum may prevent availability to protect consistency; compromise of a signing key may make correct authorization impossible while processes remain up. State the SLI or property, population, acceptable degraded mode, evaluation interval, and threat or hazard scope.

Use precise failure language. A disk sector fault may create corrupt state—an error—that becomes failure when a read returns incorrect data. Detection and correction can prevent the failure from reaching users. A failure domain names shared exposure, while an isolation boundary names containment. The same rack can be a power-failure domain and still have process isolation that contains one crash.

**Inventory domain layers.** Physical domains include device, chassis, rack, power distribution, cooling loop, room, datacenter, conduit, zone, floodplain, and region. Geographic separation reduces some correlated hazards but may add latency, replication lag, regulatory boundaries, and operational complexity.

Logical infrastructure domains include host kernel, hypervisor, cluster scheduler, service mesh, network control, storage control, quota, namespace, account, and provider service. Tenants isolated for data may still share a capacity pool. Separate data planes can still depend on one control plane for configuration or failover.

Application and data domains include process, shard, partition, cell, queue, database, schema, cache, keyspace, and source of truth. Ask where state lives, how many copies are needed, which copies acknowledge writes, and whether a corrupted value replicates. Replication preserves a defect as efficiently as correct data unless validation or version recovery provides a boundary.

Change domains include artifact, library version, feature flag, configuration bundle, migration, deployment controller, rollout wave, and maintenance window. Simultaneously updating every replica makes the release a common-mode domain even when hardware is separate. Stagger by domain and preserve known-good serving capacity.

Security domains include identity provider, certificate authority, signing root, secrets system, administrator role, network trust zone, build pipeline, and policy engine. A globally shared credential can give one compromise global blast radius. Multiple cloud regions under one compromised control account are not independent for that threat.

Human and organizational domains include on-call team, access group, vendor, support escalation, change authority, knowledge owner, timezone, and communication channel. One mistaken bulk command, unavailable specialist, supplier incident, or coordinated maintenance decision can correlate technical resources. Avoid blaming individuals; design authority and review boundaries that constrain error.

**Build an incidence map.** Represent each serving resource and every domain to which it is exposed. Include transitive dependencies: if application A requires gateway G and G requires identity I, then A is exposed to I even without a direct API call. Distinguish normal serving dependencies from dependencies needed only for change, scale, failover, or recovery.

The controlled script below finds pairwise shared exposures in a fictional three-replica placement. It proves only set intersection for declared input; a real inventory needs authoritative topology and dependency evidence.

<!-- bijux-verify: {"id":"find-shared-failure-domains","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"replica_pair=r1,r2 shared=identity-global\nreplica_pair=r1,r3 shared=deploy-blue,identity-global\nreplica_pair=r2,r3 shared=identity-global\nall_replicas_common=identity-global\ndomain=identity-global affected=3\n","stderr":""}} -->
```python
from itertools import combinations

exposures = {
    "r1": {"zone-a", "power-a", "identity-global", "deploy-blue"},
    "r2": {"zone-b", "power-b", "identity-global", "deploy-green"},
    "r3": {"zone-c", "power-c", "identity-global", "deploy-blue"},
}

for left, right in combinations(exposures, 2):
    shared = ",".join(sorted(exposures[left] & exposures[right]))
    print(f"replica_pair={left},{right} shared={shared}")

common = set.intersection(*exposures.values())
print(f"all_replicas_common={','.join(sorted(common))}")

affected = {
    domain: sum(domain in domains for domains in exposures.values())
    for domain in set.union(*exposures.values())
}
largest = max(affected, key=lambda domain: (affected[domain], domain))
print(f"domain={largest} affected={affected[largest]}")
```

An incidence map is a hypothesis. Resource tags can be wrong, managed-service internals may be undisclosed, and dependencies can activate only during failure. Record source, confidence, owner, and last verification for each edge. Mark unknowns rather than treating missing edges as independence.

**Evaluate scenario survival.** For each domain failure, remove or corrupt the exposed resources and ask whether the required property still holds. Check serving capacity, quorum, routing, state freshness, authorization, observability, and operator access. “One instance remains” is insufficient if it cannot accept load or lacks current data.

Define a degraded requirement. A checkout service might need 60% of peak admission with nonessential recommendations disabled. A database might require read-only operation with bounded staleness. A safety service may choose fail-closed behavior. The survival criterion must say what users receive, not only which components stay green.

Quorum systems make placement constraints concrete. A three-voter majority requires two available voters. If two voters share one power domain, loss of that domain removes quorum despite three nominal copies. Separate voters across the modeled domains, then include shared network, identity, software, and control dependencies that can still prevent voting.

Capacity is part of isolation. If each of three zones normally runs at 45% and traffic spreads evenly, losing one sends half of its load to each survivor; each approaches 67.5% before failover overhead, which may be viable. If normal utilization is 75%, survivors would need about 112.5% each, so domain separation cannot provide service at the same demand. Admission control or graceful degradation may define a lower survival target.

**Do not assume statistical independence.** If replicas fail independently with probability $p$, two simultaneous failures have probability $p^2$. This is a conditional model, not a property of “different zones.” Measure joint behavior and seek mechanisms that explain separation.

A simple common-cause model illustrates the danger. Let domain-wide cause $C$ occur with probability $c$. Conditional on no $C$, suppose two replicas independently fail with probability $p$. Then

$$
P(F_1\cap F_2)=c+(1-c)p^2.
$$

With $c=0.005$ and $p=0.01$, the joint probability is $0.005+0.995(0.0001)=0.0050995$, not $0.0001$. The example is illustrative; real causes overlap, probabilities change with load and time, and evidence is rarely sufficient for such a simple distribution.

Conditional probability reveals correlation: independence requires $P(F_2\mid F_1)=P(F_2)$ under the modeled conditions. Incident coincidence, shared dependencies, and common changes can make the conditional probability much larger. Sparse catastrophic events make empirical estimation uncertain, so combine data with causal architecture analysis and conservative scenarios.

**Analyze propagation as well as exposure.** A fault in one component can produce retries, queue growth, synchronized failover, cache misses, lock contention, or recovery traffic that overloads healthy domains. Timeouts and retry budgets, backpressure, load shedding, circuit breaking, and capacity reservation constrain propagation. Their detailed design arrives later in Level II; here, record the crossing paths and containment assumptions.

A boundary needs an enforcement mechanism. Separate queues limit backlog sharing only if workers and storage do not rejoin at a smaller shared pool. Per-tenant quotas constrain demand only if administrative bypasses are bounded. Network segmentation constrains reachability but not a globally distributed bad artifact. Layer boundaries for distinct mechanisms.

Cells can bound application blast radius by partitioning users and serving dependencies. A cell should minimize global synchronous dependencies and have clear routing, state, capacity, deployment, and recovery ownership. Global discovery or identity may remain necessary; model it explicitly, cache or degrade safely where possible, and avoid calling the architecture cell-isolated when global dependencies can stop every cell.

**Treat planned change as a failure scenario.** Map which resources receive a release, configuration, certificate rotation, schema migration, or provider maintenance event together. Stagger waves across capacity needed for service. Canarying one instance in every cell can still expose every cell to the same defect; a canary strategy must consider both detection quality and user blast radius.

Feature flags create logical change domains. One global flag can activate a defect everywhere even if binaries were deployed gradually. Segment activation, validate default behavior, retain a safe disable path, and guard the control system itself. Schema changes can cross versions and data replicas; compatibility windows determine whether rollback remains possible.

**Distinguish data plane and control plane.** A service may continue serving from existing configuration when its control plane is unavailable. It may be unable to scale, rotate credentials, accept new tenants, or fail over. State both steady-state and recovery dependencies. A dormant secondary that needs the failed primary control plane for activation is not an independent recovery path.

Observability can share fate too. If telemetry exits through the failed network or one monitoring account is inaccessible, operators lose evidence precisely during the scenario. Maintain scenario-appropriate local signals, independent health paths, and tested access. Do not infer service survival from a dashboard that stopped receiving data.

**Validate boundaries.** Inspect placement, provider capability, wiring, route, dependency, IAM, artifact, rollout, and ownership records. Compare declared topology with runtime telemetry. Review historical incidents and near misses for unexpected co-failure. Use architecture review to find edges that instrumentation cannot see.

Test one domain at a time under controlled conditions: process, host, rack-equivalent, zone, dependency, control-plane, credential, change wave, and operator-access loss where safe. Observe user SLIs, failover time, capacity, data correctness, queue growth, automation, alerts, and recovery. Fault injection validates the tested scenario and environment; it does not certify all future failures.

Test combinations selected from risk, cut sets, and incident evidence. A minimal cut set focuses attention on the smallest joint failures that defeat the property. Exhaustive combinations are usually infeasible, so document selection, exclusions, safeguards, and residual uncertainty.

**Govern the model.** Store domain identifiers and constraints with architecture or deployment specifications where possible. Validate placement and rollout policy automatically. Require an exception record when intended diversity cannot be achieved. Link each assumption to an owner, evidence, review date, and recovery test.

Review after provider changes, topology changes, new global dependencies, migrations, mergers of control systems, credential redesign, and incidents. Detect drift: three replicas can gradually collapse into one domain after rescheduling or capacity shortage. A diagram without current evidence is historical documentation, not a reliability control.

## Definitions and Notation

Let $R=\{r_1,\ldots,r_n\}$ be resources relevant to property $P$, $D=\{d_1,\ldots,d_m\}$ be modeled failure domains, and $E\subseteq R\times D$ be exposure. The affected set and resource-count blast radius are

$$
A(d)=\{r\in R:(r,d)\in E\},\qquad \beta(d)=|A(d)|.
$$

For resource capacity $k(r)\ge0$, capacity lost under $d$ is $K_{lost}(d)=\sum_{r\in A(d)}k(r)$. Surviving capacity is $K_{survive}(d)=\sum_{r\notin A(d)}k(r)$. A capacity survival condition for required degraded demand $L_d$ is $K_{survive}(d)\ge L_d$, subject to state and routing feasibility.

Let $S\subseteq D$ be a scenario containing several failed domains. Its affected resources are $A(S)=\bigcup_{d\in S}A(d)$. A set $S$ is a cut set for property $P$ when removing or corrupting $A(S)$ causes $P$ to fail. It is minimal when no proper subset of $S$ is also a cut set.

For replica failure events $F_1$ and $F_2$, independence under conditions $H$ means

$$
P(F_1\cap F_2\mid H)=P(F_1\mid H)P(F_2\mid H).
$$

Labels do not establish this equality. Evidence must define $H$, observation windows, failure predicates, and uncertainty.

For a quorum system with $N$ voters and required quorum $Q$, domain scenario $S$ preserves quorum only if $N-|A(S)\cap V|\ge Q$, where $V$ is the voter set. This count is necessary but not sufficient: surviving voters must communicate and hold valid state.

## Mechanisms, Invariants, or Proof Structure

**Transitive-exposure argument.** If resource $r$ requires dependency $x$ for property $P$, and $x$ is exposed to domain $d$, then failure of $d$ can prevent $r$ from contributing to $P$. Therefore a direct-resource placement map that omits dependency edges understates $A(d)$.

**Replica-count counterexample.** Place three voters $v_1,v_2,v_3$ so $v_1,v_2$ share domain $d$. Majority requires two. Failure of $d$ leaves only $v_3$, so quorum fails. Three copies do not imply tolerance of one domain failure.

**Independence counterexample.** In the common-cause model, any $c>0$ adds $c$ to joint failure before independent residual failure. Thus $p^2$ understates joint risk whenever the modeled common cause is ignored. The simple equation does not enumerate all real common causes.

**Capacity invariant.** Domain separation preserves process count but not service if surviving usable capacity is below degraded demand. Routing delay, recovery work, dependency limits, and state availability reduce usable capacity further; raw nominal capacity is an upper bound.

**Change-domain argument.** Hardware placement cannot isolate a deterministic defect activated by the same artifact and input on all replicas. Version diversity, staggered activation, input containment, or a safe fallback changes that domain; another hardware copy does not.

**Control-plane distinction.** If data-plane operation does not synchronously require control-plane availability, existing traffic may survive control loss. Any operation requiring fresh configuration, scale, credential, routing, or activation still depends on it. Survival claims must name the operational mode.

**Containment invariant.** A claimed isolation boundary must have a mechanism that limits propagation, a measurable outside property, and a test showing the property remains within bounds for the scenario. Drawing a box is not containment evidence.

## Alternatives and Trade-Offs

**Physical separation versus latency.** Greater distance reduces shared local hazards but increases network delay, replication lag, cost, and partition exposure. Choose distances from the failure scenarios and property, not maximum geography by default.

**Shared platform versus isolated stacks.** Shared services improve efficiency and consistent control but introduce common dependencies. Isolated stacks reduce some blast radius while multiplying maintenance and drift. Cells often share bounded global functions while isolating serving paths.

**Homogeneity versus diversity.** Identical replicas simplify operation and reduce accidental variance. They share software and configuration failure modes. Diversity can reduce common mode but increases complexity and is developed in SDRE-048.

**Active versus standby capacity.** Active capacity is continuously exercised and costly. Standby capacity can isolate normal load but may drift or fail activation. Test the exact failover and state path.

**Fine versus coarse domains.** Fine domains expose precise blast radius and support targeted placement but increase metadata and policy complexity. Coarse domains are manageable but can hide correlated substructure. Model at the smallest granularity that changes a decision.

**Static versus dynamic mapping.** Static architecture records capture intent and hidden dependencies. Runtime discovery captures current placement but may miss dormant recovery and administrative paths. Reconcile both and preserve provenance.

**Probabilistic versus scenario analysis.** Probability supports comparisons when data and assumptions are credible. Scenario analysis remains useful for rare or adversarial causes with sparse data. Use both without converting either into certainty.

## Failure Modes and Misconceptions

- **“Three replicas means two-failure tolerance.”** Placement, quorum, dependencies, and capacity determine tolerance.
- **“Different zones are independent.”** They may share region, control, identity, network, software, deployment, supplier, and operator domains.
- **“Regions eliminate common mode.”** Global credentials, DNS, build systems, policies, and code can span regions.
- **“Availability percentages multiply.”** Multiplication requires a defensible conditional independence model and compatible failure definitions.
- **“A provider label proves workload resilience.”** Capability, product configuration, dependency behavior, and failover must all be verified.
- **“Only unplanned faults matter.”** Releases, migrations, maintenance, certificate rotation, and operator actions create change domains.
- **“Separate compute is enough.”** Shared storage, state, routing, quota, and identity can still remove service.
- **“A surviving replica means survival.”** It may lack quorum, data, capacity, reachability, or authorization.
- **“Control-plane loss equals immediate data-plane loss.”** Sometimes serving continues; scale, change, and recovery may still fail. Specify the mode.
- **“A boundary is a diagram box.”** Containment needs enforcement and observed outside behavior.
- **“Fault injection proves independence.”** It supports only the tested scenario, configuration, and evidence window.
- **“Farther is always safer.”** Distance trades local correlation against latency, partitions, cost, and operational complexity.
- **“Monitoring is outside the model.”** Shared telemetry or access failure can make diagnosis and recovery fail together.
- **“The map is finished.”** Scheduling, suppliers, control systems, ownership, and software change continuously.

## Worked Examples

### Example 1

**Situation.** Four application processes run on four virtual machines but all virtual machines occupy one physical rack and one power feed.

**Reasoning.** Process and virtual-machine faults may be isolated, but rack power loss affects all four. The resource count gives protection against some software and host failures, not the rack-power scenario.

**Conclusion.** Record four process domains and one shared rack-power domain; place required surviving capacity outside that domain if the property requires rack tolerance.

### Example 2

**Situation.** Three zonal replicas have independent power and cooling, but every request synchronously checks one regional identity endpoint.

**Reasoning.** Zone loss can leave two replicas. Identity failure prevents all from authorizing requests, so the identity service is a transitive shared domain. Cached authorization might preserve bounded reads, subject to expiry and security policy.

**Conclusion.** The service is zone-diverse but not independent of regional identity; define and test the acceptable control-loss mode.

### Example 3

**Situation.** Two replicas each have residual failure probability 1% when no common cause occurs, while a common cause occurs with probability 0.5%.

**Reasoning.** Independent-only arithmetic gives $0.01^2=0.0001=0.01\%$. The common-cause model gives $0.005+0.995(0.0001)=0.0050995=0.50995\%$, nearly 51 times larger.

**Conclusion.** Small common-cause probability can dominate joint failure; the numerical model remains illustrative until its assumptions have evidence.

### Example 4

**Situation.** A service deploys the same new binary to one canary in each of 20 cells simultaneously.

**Reasoning.** Serving state is cell-partitioned, but the canary wave touches every cell. If the defect corrupts cell-local state before detection, every cell can be affected. Canary count is small while geographic and tenant blast radius is global.

**Conclusion.** Stage cells as well as instances, use health and data-integrity gates, and preserve untouched cells for comparison and service.

### Example 5

**Situation.** Two regions use separate compute, databases, and networks but share one administrator role and artifact-signing key.

**Reasoning.** A credential compromise or signed malicious artifact can affect both regions. Geographic separation does not isolate the security control domain. Separate authority, threshold approval, scoped credentials, and recovery roots may reduce the shared fate.

**Conclusion.** Include trust and management domains in multi-region claims.

### Example 6

**Situation.** A three-voter database places two voters in zone A and one in zone B; majority quorum is two.

**Reasoning.** Loss of zone A removes two voters, leaving one. The system correctly refuses writes if consistency requires majority, so user-visible write availability fails. Three data copies did not yield zone-failure tolerance.

**Conclusion.** Place no quorum majority inside an assumed single-failure domain and verify communication and state of survivors.

### Example 7

**Situation.** Two datacenters use different routers but both fiber paths cross one physical conduit.

**Reasoning.** Logical route diversity does not imply physical path diversity. Excavation damage at the conduit can cut both. Provider path records, diverse entrances, and controlled tests provide better evidence than different interface identifiers.

**Conclusion.** Map the shared conduit as a network failure domain and verify actual path diversity.

### Example 8

**Situation.** Existing service instances can serve for six hours without the configuration control plane, but autoscaling and regional failover require it.

**Reasoning.** The data plane survives steady traffic while cached configuration is valid and capacity is sufficient. A load spike, credential expiry, or region loss during the outage can require unavailable control functions.

**Conclusion.** State the bounded steady-state survival claim and separately model scale, change, expiry, and failover dependencies.

### Example 9

**Situation.** Each of three cells has 1,000 requests/second capacity and normally receives 700. One cell fails and routing divides its load equally.

**Reasoning.** Each survivor receives $700+350=1{,}050$ requests/second, exceeding nominal capacity before recovery overhead. Isolation limits which resources failed but cannot meet full demand. Shedding at least 100 aggregate requests/second or reserving more headroom is required.

**Conclusion.** Domain separation without degraded-capacity planning does not preserve the service target.

### Example 10

**Situation.** A zone-loss exercise succeeds, but the next real incident removes the zone and the telemetry account used by the on-call team.

**Reasoning.** The exercise validated serving failover but omitted an observability and access domain. Operators cannot confirm state or safely intervene. Independent signals and tested emergency access belong to the recovery property.

**Conclusion.** Expand the domain map and future exercises from the escaped dependency; do not generalize beyond the tested scenario.

## Cross-Program Connections

- **Computer architecture:** power, memory, bus, cache, and device boundaries define physical common causes below software placement.
- **Operating systems:** process isolation, namespaces, kernels, hosts, and schedulers contain some faults while sharing others.
- **Networks:** logical routes, physical conduits, control planes, naming, and traffic steering create layered fate sharing.
- **Database engineering:** replica placement, quorum, corruption propagation, recovery logs, and state freshness determine data survival.
- **Distributed systems:** partitions, failure detectors, consensus, retries, and recovery traffic make failure dynamic and partially observed.
- **Security engineering:** trust roots, credentials, identity, build systems, and administrative authority are correlation domains.
- **Platform engineering:** cells, clusters, accounts, zones, quotas, and rollout controllers expose placement and policy boundaries.
- **Systems engineering:** fault trees, cut sets, hazards, redundancy, and lifecycle evidence connect component causes to mission effects.
- **Software delivery:** artifacts, flags, schemas, controllers, and rollout waves create temporal and logical domains across locations.

## References

1. Alex Hidalgo et al., “Implementing SLOs,” in *The Site Reliability Workbook*, O'Reilly Media, 2018. [Official online edition](https://sre.google/workbook/implementing-slos/). Accessed 2026-09-06.
2. Amazon Web Services, *AWS Well-Architected Framework: Reliability Pillar*, current online edition. [Use fault isolation to protect your workload](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/use-fault-isolation-to-protect-your-workload.html). Accessed 2026-09-06.
3. Microsoft, “Availability sets overview,” Azure Virtual Machines documentation. [Official documentation](https://learn.microsoft.com/en-us/azure/virtual-machines/availability-set-overview). Accessed 2026-09-06.
4. Ron Ross, Victoria Pillitteri, Richard Graubart, Deborah Bodeau, and Rosalie McQuaid, *Developing Cyber-Resilient Systems: A Systems Security Engineering Approach*, NIST SP 800-160 Volume 2 Revision 1, December 2021. [Official publication record](https://csrc.nist.gov/pubs/sp/800/160/v2/r1/final). Accessed 2026-09-06.
5. Mike Ulrich and K. V. Vishwanath, “Addressing Cascading Failures,” in *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly Media, 2016. [Official online edition](https://sre.google/sre-book/addressing-cascading-failures/). Accessed 2026-09-06.
6. Microsoft, “What are Azure availability zones?”, Azure reliability documentation. [Official documentation](https://learn.microsoft.com/en-us/azure/reliability/availability-zones-overview). Accessed 2026-09-06.

Current vendor claims are deliberately source-specific and were checked on 2026-09-06. No provider documentation proves the configuration or independence of a particular workload. Probability and capacity examples are educational models with stated assumptions.

## Exercises

### Exercise 1

A service has four replicas across two zones. Each zone has two replicas. All replicas use one database, one identity service, two artifact waves, and a shared on-call role. Construct a domain inventory and state what additional facts are required before claiming tolerance of one zone failure.

### Exercise 2

Under a simple model, a common cause occurs with probability 0.2%. Conditional on its absence, each of two replicas independently fails with probability 2%. Compute joint failure probability and compare it with naive $p^2$. Explain the model's limits.

### Exercise 3

A five-voter system requires quorum three. Voters 1–3 share power domain A; voters 4–5 are in distinct domains B and C. Analyze each single-domain loss and propose a placement that tolerates any one of A, B, or C, assuming communication and state remain valid.

### Exercise 4

Design a controlled validation for the loss of one service cell. Include user-visible property, steady-state setup, safeguards, failure action, observations, capacity, propagation checks, recovery, and limits on the conclusion.

### Exercise 5

A company plans two-cloud deployment for geographic resilience. Both sides use the same source repository, continuous-delivery controller, DNS provider, identity provider, incident chat, and primary operator team. Evaluate the independence claim and propose a proportionate plan that avoids pretending every dependency can or should be duplicated.

## Answers to the Exercises

### Answer 1

Inventory at least replica/process, host, zone, database, identity, artifact wave, deployment controller, account or credential, network path, traffic steering, observability, and on-call authority domains. A zone scenario removes its two replicas, but survival also requires database and identity availability from the survivor zone, routable capacity for full or declared degraded demand, current state, functioning traffic steering, usable telemetry, and operator access. Determine whether the database and identity are zonal or regional, how artifact waves map to zones, whether network and power paths are distinct, how failover occurs, and whether tests observed the user SLI. Until then, “two zones” is placement evidence, not a complete tolerance claim.

### Answer 2

Here $c=0.002$ and $p=0.02$. The model gives $c+(1-c)p^2=0.002+0.998(0.0004)=0.0023992$, or 0.23992%. Naive independence gives $0.0004$, or 0.04%, so the modeled common cause makes joint failure about $0.0023992/0.0004=5.998$ times as likely. The model assumes one exhaustive common-cause event, stable probabilities, conditional independence outside it, compatible windows, and precise failure predicates. Real causes overlap, vary with time and load, and are sparsely observed; use the calculation to expose sensitivity, not claim a forecast.

### Answer 3

Loss of A removes voters 1–3 and leaves two, below quorum. Loss of B removes voter 4 and leaves four; loss of C removes voter 5 and leaves four. To tolerate any one domain with quorum three, no domain may contain more than $5-3=2$ voters. One placement is two voters in A, two in B, and one in C. After loss of A or B, three remain; after loss of C, four remain. This count is necessary, not sufficient: remaining voters must communicate, hold valid state, and avoid shared control, software, and network failures.

### Answer 4

Define a user SLI and degraded target, such as successful correct requests with at least 60% admitted peak load. Establish representative traffic, verified state replication, headroom, and healthy telemetry. Limit the exercise to a named noncritical cohort or bounded window, name abort authority, and verify a recovery path. Remove or isolate the cell through the same mechanism modeled, then observe routing, latency, errors, data correctness, survivor saturation, queues, retries, dependency load, automation decisions, alerts, and operator access. Restore deliberately and check reconciliation and data integrity. The result supports only this configuration, load, fault mechanism, duration, and observation set; record unknowns and escaped behavior.

### Answer 5

The clouds reduce some facility, regional, and provider-specific domains, but source, delivery, DNS, identity, communication, and human authority remain shared. A bad artifact or compromised identity can cross both; DNS failure can make both unreachable; one team can repeat the same action. Prioritize dependencies by whether steady serving or recovery synchronously requires them and by consequence. For example, preserve last-known-good serving without delivery, use staged per-cloud waves, protect signing and deployment authority with scoped credentials and independent approval, provide bounded DNS contingency, cache or degrade identity only where security policy permits, maintain an independent emergency communication path, and cross-train recovery. Test scenarios. Duplicate a dependency only when reduced correlated risk justifies the added complexity and new failure modes; document accepted shared domains explicitly.
