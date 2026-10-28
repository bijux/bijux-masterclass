---
module_id: SDRE-048
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 48
title: Redundancy and Diversity
status: complete
last_verified: 2026-09-06
---

# Redundancy and Diversity

## One-Page Review

### Governing question

How should engineers choose, place, coordinate, and verify surplus and deliberately different resources so the system preserves a declared property under failure without creating hidden common modes, unsafe disagreement, or unaffordable complexity?

### Essential definitions

- **redundancy** supplies more resources, information, paths, capacity, or time than normal success minimally requires;
- **diversity** deliberately varies implementations, technologies, suppliers, locations, authorities, or procedures to reduce selected common-mode exposure;
- **replication** maintains multiple representations or executors of nominally the same function or state;
- **spare capacity** is provisioned capability not required by normal load but available after loss or during maintenance;
- **active-active** resources serve concurrently; **active-passive** designs keep one or more resources in standby;
- **hot**, **warm**, and **cold** standby describe decreasing readiness and increasing activation work, but require project-specific definitions;
- **$N+1$ redundancy** provides one unit beyond the $N$ units required under the stated load and unit capacity;
- a **$k$-of-$n$ system** succeeds when at least $k$ of $n$ relevant elements provide acceptable results;
- a **quorum** is a threshold of participants required for an operation or decision;
- a **voter** chooses or validates an output among redundant channels;
- **failover coverage** is the probability or observed fraction that detection, decision, switching, and recovery work correctly when required;
- **state divergence** means nominal replicas no longer represent compatible state;
- **split brain** occurs when separated participants act as concurrent authorities in a way the design forbids;
- **common-mode failure** defeats several redundant elements through the same mechanism;
- **defense in depth** layers different controls so one control failure need not defeat the protected objective; it is related to but not identical with service redundancy.

### Central model, mechanism, or theorem

For independent component-failure probability $p$, an idealized $k$-of-$n$ system fails when fewer than $k$ components remain available:

$$
P_{fail}=\sum_{i=0}^{k-1}\binom{n}{i}(1-p)^i p^{n-i}.
$$

If a common cause occurs with probability $c$ and defeats the system, while the independent model applies only when it does not occur, then

$$
P_{fail,total}=c+(1-c)P_{fail}.
$$

The equations are conditional models. Real benefit also requires correct placement, sufficient survivor capacity, valid state, reliable detection and switching, a sound voter or coordinator, and evidence that diversity addresses the modeled cause.

### Critical invariants

- name the user-visible property and exact failure scenarios before selecting redundancy;
- map every copy and spare to the failure domains from SDRE-047;
- reserve enough usable capacity and state outside each tolerated domain;
- include detection, routing, control plane, identity, quorum, voter, and operator paths;
- prevent multiple authorities with fencing, consensus, leases, or another justified mechanism;
- keep replicas compatible while avoiding simultaneous change across all serving capacity;
- choose diversity against a specific common mode and test that the difference is real;
- account for dormant drift, activation delay, repair, replenishment, and repeated failures;
- progressively test failover and failback under representative load and degraded dependencies;
- include lifecycle cost, security surface, cognitive load, data correctness, and decommissioning.

### Common failures

Failures include counting idle copies as ready capacity, placing redundant voters in one domain, assuming independence from labels, replicating corrupted state, sharing a voter or control plane, failing over into overload, letting passive systems drift, retrying non-idempotent work, accepting split brain, using two products built on the same vulnerable dependency, deploying one bad version everywhere, adding diversity without operational competence, testing failover but not failback, leaving lost redundancy unreplenished, and treating replication as backup or proven recoverability.

### Compact example

Three identical voters require a quorum of two. Under independent 1% component-failure probability, modeled system failure is $3(0.99)(0.01)^2+(0.01)^3=0.000298$, or 0.0298%. If a shared control-plane defect defeats the system with probability 0.2%, the conditional model yields $0.002+0.998(0.000298)=0.002297404$, or about 0.2297404%. Added copies reduce the residual independent term but do not remove the common cause. The design must separate the control path or tolerate its loss, not merely add another identical voter.

### Connections

[SDRE-047](047-failure-domains.md) supplies the exposure map that gives redundancy meaning. [SDRE-049](../ROADMAP.md) next defines useful degraded service when redundancy cannot preserve full capability. [SDRE-050](../ROADMAP.md) reviews whether these assumptions are production-ready.

## Governing Question

Redundancy is often summarized as “have more than one.” That advice omits what is duplicated, which property the copies protect, how many are required, where they are placed, how state stays valid, who selects an answer, and what happens when the selector or recovery path fails. Two processes sharing one host are redundant against one process crash but not against host loss. Two databases can improve read availability while propagating the same destructive write.

Diversity answers a different problem. Identical copies intentionally share behavior, which also means they can share defects. Different implementations, suppliers, versions, locations, or operational paths may reduce a chosen common mode. They can also disagree, interact unexpectedly, expand attack surface, and exceed the team's ability to operate them. The governing question is therefore not “how much redundancy is good?” It is which surplus and differences create evidence-backed tolerance for a declared failure model at acceptable total cost.

## Why This Matters

NIST SP 800-160 Volume 2 Revision 1 treats redundancy and diversity as complementary cyber-resiliency techniques. It emphasizes protected surplus, analysis of shared resources, multiple layers, manageability, and the trade-off that diversity and redundancy can add complexity and attack surface [1]. The guidance is adaptable rather than a universal architecture prescription.

Google's SRE treatment of data integrity warns that replication and redundancy are not recoverability: a software defect or destructive operation can propagate across replicas, while recovery needs appropriately diverse and tested historical copies [2]. Its SLO guidance likewise warns that common dependencies and global control planes invalidate simple multiplication of nominal availability [3]. These distinctions keep copy count from becoming false assurance.

Current AWS reliability guidance describes static stability as pre-provisioning the resources needed after a failure rather than depending on successful resource creation during the failure [4]. This is source-specific cloud guidance, but the durable principle is broader: a recovery path that introduces a new untested mode, quota need, image fetch, credential, or control dependency may fail exactly when needed.

Google's reliability-testing chapter argues that confidence must account for system change and be supported by tests appropriate to production mechanisms [5]. Redundancy is latent behavior until loss, switching, degraded load, repair, and failback have been exercised. A successful diagram review does not show that state is current, routing converges, or operators can recover without compounding the incident.

## Prerequisites and Retrieval

Retrieve reliability property, fault, error, failure, failure domain, common cause, common mode, capacity, state, replica, quorum, consistency, partition, recovery, latency, availability, durability, control plane, data plane, deployment wave, idempotency, fencing, and evidence.

From SDRE-041 retrieve property distinctions. From SDRE-045 retrieve tolerated failure. From SDRE-046 retrieve safe automation and reconciliation. From SDRE-047 retrieve transitive failure domains, capacity survival, quorum placement, common-cause probability, and validation boundaries. This chapter develops surplus and difference choices; detailed backup recovery, regional evacuation, consensus, and overload mechanisms appear later.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish redundancy, replication, spare capacity, diversity, and defense in depth;
2. choose a redundancy form for a declared property and failure scenario;
3. derive idealized parallel and $k$-of-$n$ reliability expressions;
4. expose independence, coverage, state, voter, and survivor-capacity assumptions;
5. compare active-active with hot, warm, and cold standby designs;
6. reason about quorum placement, fencing, and split-brain prevention;
7. select diversity against a specific physical, software, supplier, or operational common mode;
8. identify when diversity increases semantic, security, and operational risk;
9. design representative failover, failback, and replenishment validation;
10. judge redundancy as a lifecycle system rather than an inventory count.

## Core Exposition

**Specify the protected property.** Redundancy can preserve availability, capacity, integrity, durability, decision correctness, or recovery options, but the mechanism differs. Extra stateless servers can preserve throughput. Mirrored storage can survive device loss. Erasure coding stores sufficient information to reconstruct data. A voting arrangement can mask some erroneous outputs. Historical backups preserve recovery points that live replication cannot.

State scope and failure scenario. “The API remains available after loss of any one zone at 60% of peak admission” is testable. “Highly redundant” is not. State whether maintenance, overload, partition, corruption, credential compromise, software defect, and operator error are included. No finite architecture tolerates every combination.

**Choose the unit of surplus.** Hardware redundancy adds devices or paths. Software replication adds executing instances. Information redundancy adds parity, checksums, or coded fragments. Temporal redundancy repeats an operation. Capacity redundancy reserves headroom. Procedural redundancy preserves alternate people or recovery methods. These forms address different causes and can be layered.

An $N+1$ design requires $N$ units for declared demand and holds one equivalent unit beyond that need. It tolerates one unit loss only if the spare is in another relevant domain, can assume load in time, has compatible configuration and state, and does not depend on the failed resource. If units differ in capacity, count is misleading; calculate usable capacity.

$N+2$ can tolerate two unit losses under corresponding assumptions, support one failure during maintenance, or reserve uncertainty. It does not imply two-domain tolerance if both surplus units share a domain or common control. The notation always needs load, unit, placement, and activation semantics.

**Compare active and standby modes.** Active-active resources handle normal work together. They are exercised continuously and can use provisioned capacity, but load rebalancing, state coordination, and correlated traffic can complicate failure. Removing one active resource increases load on survivors immediately.

Active-passive resources keep a designated authority or serving set. A hot standby continuously maintains near-ready state; warm standby needs bounded activation or scale; cold standby requires substantial provisioning or restoration. These terms are not standardized performance guarantees. Define state lag, activation steps, dependencies, capacity, and recovery objective for the project.

Standby reduces some concurrency complexity but creates dormancy risk. Credentials expire, images disappear, schemas diverge, quotas change, routes rot, and operators forget. Periodic activation and rotation make readiness observable. A standby never exercised under load is an assertion, not capacity evidence.

**Require sufficient survivor capacity.** Let required degraded load be $L$ and usable capacity outside failed domain $d$ be $K_{survive}(d)$. The necessary condition is $K_{survive}(d)\ge L$. Apply derating for failover overhead, uneven sharding, state warmup, cache misses, network bottlenecks, and dependency quotas. Nominal CPU totals alone are not usable capacity.

Static stability pre-provisions the capacity required for the failure mode [4]. Dynamic recovery can be economical, but it relies on control planes, quotas, images, networks, credentials, scheduling, and time. If dynamic creation is part of the design, test those dependencies during the same scenario and define what happens when creation is delayed or unavailable.

**Coordinate state and authority.** Stateless replication still depends on configuration and downstream state. Stateful replication must define write acknowledgement, ordering, consistency, lag, conflict, corruption, and recovery. Synchronous replication can bound acknowledged-state loss but adds latency and partition trade-offs. Asynchronous replication lowers coupling but admits lag and possible loss during failover.

Quorum protocols use overlapping participant sets so conflicting decisions cannot both gather sufficient support under stated assumptions. Count alone is insufficient: voters must occupy appropriate failure domains and communicate. A five-voter quorum of three fails under one domain loss if three voters share that domain.

Fencing prevents a stale former primary from continuing to mutate shared state after a new primary is chosen. Mechanisms include monotonically increasing epochs, lease tokens enforced by the storage target, or consensus-owned authority. A timestamp or operator belief is not fencing unless every effect receiver rejects stale authority.

Split brain can preserve apparent availability while violating correctness. Network partition, delayed control messages, and failed demotion can produce two writers. Choose which property yields under partition, make authority externally enforceable, and test rejoin and conflict handling. Do not count two writable primaries as useful redundancy without a consistency model.

**Model component reliability cautiously.** For two independent components in parallel where either suffices, system failure is $p_1p_2$. For identical independent $p$, it is $p^2$. For a $k$-of-$n$ system, sum binomial terms with fewer than $k$ successes. Independence, identical probability, stable windows, complete coverage, and correct switching are strong assumptions.

Failover coverage can dominate. If component failure occurs and recovery succeeds with probability $q$, a spare does not make all those failures harmless; detection, decision, activation, state, and routing must succeed. Model those mechanisms as components or scenarios rather than applying a ceremonial “redundancy factor.”

Common cause adds a floor that more identical copies cannot remove. With system-defeating common-cause probability $c$ and independent residual system failure $P_I$, a simple conditional model is $c+(1-c)P_I$. It is useful for sensitivity, not a comprehensive distribution: causes can overlap and probabilities vary with conditions.

The following controlled calculation compares a fictional three-component, two-required system under independence with a simple common-cause model, then checks an $N+1$ capacity state.

<!-- bijux-verify: {"id":"evaluate-redundancy-assumptions","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"independent_system_failure=0.029800%\nwith_common_cause=0.229740%\nsurvivor_capacity=300 required=300 margin=0\n","stderr":""}} -->
```python
from decimal import Decimal
from math import comb

p = Decimal("0.01")
n = 3
k = 2
independent_failure = sum(
    Decimal(comb(n, available))
    * (Decimal(1) - p) ** available
    * p ** (n - available)
    for available in range(k)
)

common_cause = Decimal("0.002")
total_failure = common_cause + (Decimal(1) - common_cause) * independent_failure

print(f"independent_system_failure={independent_failure:.6%}")
print(f"with_common_cause={total_failure:.6%}")

unit_capacity = 100
units_after_one_failure = 3
required = 300
survivor_capacity = unit_capacity * units_after_one_failure
print(
    f"survivor_capacity={survivor_capacity} required={required} "
    f"margin={survivor_capacity - required}"
)
```

Zero modeled margin means any derating breaks the capacity condition. It is not evidence of a safe design merely because equality holds.

**Use diversity against named common modes.** Location diversity addresses selected physical hazards. Supplier diversity can reduce one provider's defect or business failure. Implementation diversity can reduce a shared software bug. Version diversity can preserve a known-good path during rollout. Operational diversity can provide out-of-band access or an alternate recovery procedure.

Verify the difference. Two network carriers may lease the same conduit. Two products may embed the same library or depend on one identity provider. Two implementations may follow one ambiguous specification and reproduce the same error. Two clouds may share one deployment artifact, DNS provider, and operator credential. A procurement boundary is not automatically a failure boundary.

Intentional diversity creates costs. Different databases have different consistency and query semantics. Multiple clouds vary in identity, networking, limits, telemetry, and failure behavior. Separate implementations can disagree, making the voter or adjudicator critical. Teams must patch, test, monitor, and practice every variant; neglected diversity becomes unsafe drift.

Avoid false diversity through ornamental differences. Different programming languages on the same runtime, shared generated code, identical algorithm, or common package may not address the target defect. Conversely, modest diversity—staggered versions, independent validation, immutable historical copies, or a manual out-of-band path—may address the dominant cause without duplicating an entire stack.

**Design the selector and voter.** Redundant outputs require a rule. A load balancer selects a healthy server based on potentially imperfect health evidence. A majority voter masks one disagreeing channel only if failures are sufficiently independent and the voter itself is trustworthy. Semantic disagreements may have no obvious majority truth.

Health checks can create correlated removal: a shared dependency becomes slow, every instance fails the same check, and routing removes all capacity. Use user-relevant checks, hysteresis, bounded eviction, and last-known-good behavior where appropriate. Distinguish component health from eligibility to receive a particular workload.

Voting adds latency and resources. Triple modular redundancy can mask one arbitrary result under stated voter and independence assumptions, but identical deterministic bugs produce the same wrong answer and pass the vote. Independent specification, diverse implementation, input validation, and external plausibility checks address different layers.

**Use temporal redundancy carefully.** Retrying can overcome a transient fault, making time the surplus dimension. It can also duplicate a committed non-idempotent effect, amplify overload, synchronize clients, and consume deadlines. Use stable operation identity, idempotency or deduplication, bounded attempts, backoff, jitter, and a retry budget. A retry against the same failed domain is not meaningful diversity.

Hedged requests send another attempt before the first completes and select an acceptable result. They can reduce tail latency but multiply load and complicate cancellation and side effects. Restrict them to safe operations, cap extra traffic, and observe whether both attempts share the slow dependency.

**Separate live replication from recovery copies.** Live replicas optimize current serving and can propagate deletion, corruption, ransomware, or software defects. Backups and point-in-time history preserve older states under separate retention and authority. They need their own redundancy and diversity, but their essential property is verified restoration, not mere presence [2].

Checksums add information redundancy for detection; parity or erasure codes can reconstruct bounded loss. They do not prove semantic correctness of the original data. Store integrity metadata and fragments across relevant domains, scrub them, and test reconstruction before loss exceeds tolerance.

**Stagger change and preserve compatibility.** Do not update every redundant element simultaneously. Partition rollout by failure domain and user blast radius, preserve sufficient known-good capacity, and gate on property-specific evidence. Configuration, feature flags, schemas, certificates, and firmware need the same treatment as binaries.

Version diversity requires compatibility. Old and new nodes may exchange messages, read shared data, or contend for leadership. Define rolling protocol and schema windows, reversible steps, and minimum compatible versions. Diversity that cannot interoperate can reduce availability during ordinary change.

**Test the whole lifecycle.** Inventory placement and shared dependencies. Test loss under representative load, including state lag, failover detection, routing convergence, cache warmup, survivor saturation, correctness, and user SLIs. Then test failback: stale primaries, replay, reconciliation, duplicate work, and restored capacity can cause a second incident.

Test maintenance while already degraded, because one failure plus planned work is a common reason for $N+2$ or extra headroom. Test replenishment and repair time. A design that tolerates one loss for ten minutes may not tolerate a second failure during a six-hour rebuild.

Record evidence scope. One zone exercise does not prove region, software, credential, or corruption tolerance. A simulated dependency failure may not reproduce provider control-plane behavior. Expand from incidents and surprises, and keep unresolved assumptions visible.

**Govern cost and complexity.** Include hardware or service cost, cross-domain transfer, replication traffic, write latency, consistency limits, software licenses, security review, operational skills, testing, patching, incident diagnosis, and decommissioning. Redundancy can improve maintenance flexibility and reliability while also increasing the number of things that fail.

Choose the smallest coherent design that meets the target failure model with evidence and margin. Review when load, topology, vendors, threats, state, or objectives change. Remove obsolete copies and variants deliberately; forgotten redundant resources retain credentials, data, cost, and attack surface.

## Definitions and Notation

Let $X_i=1$ mean component $i$ succeeds for property $P$ in window $W$. A $k$-of-$n$ system succeeds when $\sum_{i=1}^nX_i\ge k$. If components are independent and identically fail with probability $p$, then

$$
P_{fail}=P\!\left(\sum X_i<k\right)=\sum_{i=0}^{k-1}\binom{n}{i}(1-p)^ip^{n-i}.
$$

For two nonidentical independent parallel elements where either suffices, $P_{fail}=p_1p_2$. Without independence, $P(F_1\cap F_2)$ must be modeled or bounded directly.

Let $c$ be probability of an exhaustive system-defeating common cause, and let $P_I$ be conditional system-failure probability given no such cause. Then $P_{total}=c+(1-c)P_I$. This simple partition assumes the common-cause event and its complement cover the model.

For domain $d$, usable surviving capacity is

$$
K_d=\sum_{r\notin A(d)}\alpha_r k_r,
$$

where nominal capacity is $k_r$ and scenario derating $0\le\alpha_r\le1$ accounts for usable state, routing, warmup, or other declared limits. A necessary capacity condition is $K_d\ge L_d$ for degraded demand $L_d$.

For an $(n,k)$ erasure code, any $k$ valid fragments reconstruct the encoded object under the code's assumptions, so up to $n-k$ fragment losses are tolerated. Placement and integrity determine whether domain failure or correlated corruption respects that bound.

Failover time can be decomposed as $T_f=T_d+T_a+T_s+T_v$, covering detection, authority decision, switching or activation, and verification. Overlap can make this sum an upper model rather than exact elapsed time; define measurement points.

## Mechanisms, Invariants, or Proof Structure

**Parallel-system derivation.** When either of two elements suffices, the system fails exactly on $F_1\cap F_2$. Under independence this is $p_1p_2$. Removing independence removes the product equality, not merely its numerical precision.

**$k$-of-$n$ derivation.** Exactly $i$ successes among independent identical components has probability $\binom ni(1-p)^ip^{n-i}$. System failure includes mutually exclusive cases $i=0$ through $k-1$, so their probabilities sum. A shared voter or domain is outside that component-only model unless included explicitly.

**Common-cause floor.** Since $P_{total}=c+(1-c)P_I\ge c$, reducing $P_I$ with more identical copies cannot push modeled system failure below $c$. Addressing the shared cause or tolerating it is necessary to cross that floor.

**Quorum intersection.** In a universe of $N$ voters, any two quorums of size $Q$ intersect when $2Q>N$. Intersection supports consistency only when common members cannot approve conflicting decisions under the protocol and failure model.

**Capacity necessity.** If surviving usable capacity $K_d<L_d$, no routing algorithm can serve all declared degraded demand without exceeding the capacity model. Queuing, shedding, or reduced service must change the requirement or the design.

**Fencing invariant.** Once authority epoch $e+1$ is accepted, effect receivers must reject commands from every epoch $e'\le e$. Otherwise a delayed former primary can mutate state after failover and redundancy creates concurrent authority.

**Diversity limitation.** Difference reduces a common mode only if the causal mechanism does not cross the difference. Diverse brands sharing one vulnerable dependency remain homogeneous for that vulnerability; operational complexity can add new common modes.

## Alternatives and Trade-Offs

**Active-active versus active-passive.** Active-active continuously exercises capacity and can distribute load but complicates coordination. Active-passive simplifies authority while adding activation delay and drift. Choose from state, latency, capacity, and failure semantics.

**Hot versus warm versus cold standby.** Hot standby minimizes activation time at higher cost and coupling. Cold standby lowers steady cost but maximizes recovery dependencies and uncertainty. Define readiness quantitatively rather than relying on labels.

**Replication versus erasure coding.** Replication gives simple reads and repairs at higher storage overhead. Erasure coding reduces overhead for a failure tolerance but increases reconstruction computation, fragment coordination, and degraded-read cost.

**Homogeneity versus diversity.** Homogeneity simplifies compatibility, patching, and diagnosis. Diversity may reduce a chosen common mode but increases integration, skills, and security burden. Match difference to evidence.

**Static capacity versus dynamic recovery.** Pre-provisioned capacity reduces failure-time dependencies and costs more continuously. Dynamic creation can reduce normal cost but adds activation delay and control-plane risk.

**Synchronous versus asynchronous state.** Synchronous replication can protect acknowledged state under declared quorum assumptions but adds latency and availability trade-offs. Asynchronous replication lowers write coupling but permits lag and loss.

**Automatic versus human-authorized failover.** Automation reacts consistently and quickly for well-modeled states. Human authorization can manage ambiguity but adds delay and toil. Automate bounded mechanics and retain judgment where evidence does not justify autonomy.

## Failure Modes and Misconceptions

- **“More copies always improve reliability.”** Shared causes, voters, controls, and propagated corruption can dominate.
- **“$N+1$ is self-explanatory.”** Required load, unit capacity, placement, derating, and activation must be defined.
- **“Passive means safe.”** Dormant state, credentials, routes, quotas, and skills drift.
- **“Different vendors are independent.”** They may share infrastructure, dependencies, protocols, operators, or vulnerabilities.
- **“Diverse means better.”** Unmanaged differences add defects, attack surface, incompatibility, and recovery burden.
- **“Replication is backup.”** Live copies can replicate destructive change; recoverability needs historical, protected, tested state.
- **“Quorum count guarantees correctness.”** Placement, communication, protocol, voter behavior, and fencing remain necessary.
- **“Failover success ends the exercise.”** Failback, reconciliation, replenishment, and second-failure exposure can fail later.
- **“A health check knows truth.”** Shared or poorly chosen checks can remove healthy capacity or retain unsafe nodes.
- **“Retries are free redundancy.”** They consume capacity and can duplicate effects or amplify overload.
- **“Equal nominal capacity is usable capacity.”** Warmup, state, routing, dependencies, and uneven partitions derate it.
- **“Probability replaces testing.”** Equations expose assumptions; tests and incidents supply bounded evidence.
- **“Geography handles software defects.”** Identical artifacts and flags cross locations.
- **“Redundant resources can be forgotten.”** Unowned copies retain cost, data, privilege, and vulnerabilities.

## Worked Examples

### Example 1

**Situation.** A workload needs 300 units of capacity. Four instances each provide 100; one is nominal $N+1$ surplus.

**Reasoning.** After one failure, nominal survivor capacity is exactly 300, leaving zero margin. If cache warmup derates survivors to 95%, usable capacity is $3(95)=285$, below demand. Placement in one domain would make even the count invalid.

**Conclusion.** The design is nominal $N+1$ but needs derating, domain placement, or degraded admission before it is defensible.

### Example 2

**Situation.** Three components require two successes and each independently fails with probability 1%.

**Reasoning.** Failure means exactly zero or one success: $p^3+3(1-p)p^2=0.000001+0.000297=0.000298$, or 0.0298%. Adding a 0.2% system-defeating common cause gives 0.2297404% in the simple conditional model.

**Conclusion.** Redundancy reduces the residual independent term; the common cause sets the dominant floor.

### Example 3

**Situation.** A warm database standby receives asynchronous changes and has never served production traffic. Primary loss occurs after replication lag reaches eight minutes.

**Reasoning.** Compute readiness does not imply state readiness. Promotion may violate the acknowledged-data objective, routes and credentials may be stale, and caches are cold. Recovery must compare the eight-minute exposure with the RPO, validate authority, and test actual serving capacity.

**Conclusion.** Classify readiness by measured state, activation, and service evidence, not “warm” as a label.

### Example 4

**Situation.** A five-voter service uses quorum three, with voters placed 2-2-1 across three failure domains.

**Reasoning.** Losing either two-voter domain leaves three voters; losing the one-voter domain leaves four. Quorum count survives each single domain. Shared network, software, and control dependencies can still defeat voting.

**Conclusion.** Placement satisfies the single-domain count condition but not the complete service proof.

### Example 5

**Situation.** A storage code creates ten fragments and requires any six to reconstruct data.

**Reasoning.** It tolerates up to four fragment losses. If five fragments occupy one failure domain, loss of that domain leaves five and reconstruction fails. Spreading at most four per tolerated domain preserves the count condition, subject to integrity and reachability.

**Conclusion.** Coding tolerance applies to fragment loss, so placement must translate domain loss into no more than four unavailable valid fragments.

### Example 6

**Situation.** Two independently implemented authorization engines both interpret an ambiguous policy sentence as allowing an unsafe action.

**Reasoning.** Implementation diversity does not address specification common mode. Majority agreement between two or three engines can reproduce the same wrong interpretation. Formalized policy semantics, independent review, negative tests, and fail-safe constraints target the cause.

**Conclusion.** Choose diversity at the layer containing the fault; different code is insufficient for a shared specification error.

### Example 7

**Situation.** A payment client times out and sends three identical charge requests to the same endpoint.

**Reasoning.** Temporal redundancy may overcome a transient packet loss, but it can create four charges if the operation lacks a stable identity and deduplication. It also adds load to the same failure domain. The deadline and retry budget must bound attempts.

**Conclusion.** Make the operation idempotent or deduplicated and diversify only when another path avoids the suspected cause.

### Example 8

**Situation.** Two network providers advertise diverse circuits, but a site survey shows both fibers share the building entrance.

**Reasoning.** Provider diversity reduces some supplier and backbone failures, but excavation or fire at the shared entrance defeats both. A separate physical entrance targets that common mode; it may still share power or upstream conduit.

**Conclusion.** Verify diversity against the named hazard through physical and contractual evidence.

### Example 9

**Situation.** A service keeps old and new versions active during rollout, but a database migration removes a column the old version reads.

**Reasoning.** Version diversity would permit rollback only if data and protocol remain compatible. The destructive migration converts the old version from known-good capacity into broken capacity. Expand-contract sequencing preserves the compatibility window.

**Conclusion.** Software-version redundancy requires compatible shared state and reversible rollout design.

### Example 10

**Situation.** Live storage has three replicas across zones, and an operator deletes a customer record through the supported API.

**Reasoning.** Replication faithfully propagates the valid command. Device and zone redundancy remain healthy while historical state disappears. A protected point-in-time copy under separate deletion authority may permit recovery, but only a restore test establishes usable recovery.

**Conclusion.** Replication protects selected component loss; historical and authority diversity protect different data-loss causes.

## Cross-Program Connections

- **Algorithms:** combinatorics, probability, coding, voting, and bounds formalize selected redundancy claims.
- **Data structures:** checksums, parity, erasure codes, logs, and immutable versions add information redundancy.
- **Operating systems:** process, host, scheduler, and device replication inherit kernel and control-plane common modes.
- **Databases:** quorum, replication mode, consistency, fencing, backup, and point-in-time recovery protect distinct properties.
- **Distributed systems:** partitions, consensus, failure detection, leases, and retries govern authority under uncertainty.
- **Networks:** path, carrier, conduit, routing, and naming diversity must be established at the relevant layer.
- **Security:** diverse controls and trust roots can reduce common mode while increasing attack surface and key-management complexity.
- **Platform engineering:** zones, cells, clusters, rollout waves, quotas, and static capacity operationalize placement.
- **Systems engineering:** common-cause analysis, cut sets, coverage, derating, repair, and lifecycle cost connect architecture to mission risk.

## References

1. Ron Ross, Victoria Pillitteri, Richard Graubart, Deborah Bodeau, and Rosalie McQuaid, *Developing Cyber-Resilient Systems: A Systems Security Engineering Approach*, NIST SP 800-160 Volume 2 Revision 1, December 2021. [Official publication record](https://csrc.nist.gov/pubs/sp/800/160/v2/r1/final). Accessed 2026-09-06.
2. Raymond Blum and Rhandeev Singh, “Data Integrity: What You Read Is What You Wrote,” in *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly Media, 2016. [Official online edition](https://sre.google/sre-book/data-integrity/). Accessed 2026-09-06.
3. Alex Hidalgo et al., “Implementing SLOs,” in *The Site Reliability Workbook*, O'Reilly Media, 2018. [Official online edition](https://sre.google/workbook/implementing-slos/). Accessed 2026-09-06.
4. Amazon Web Services, “REL11-BP05 Use static stability to prevent bimodal behavior,” *AWS Well-Architected Framework: Reliability Pillar*, current online edition. [Official documentation](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_withstand_component_failures_static_stability.html). Accessed 2026-09-06.
5. Alex Perry and Max Luebbe, “Testing for Reliability,” in *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly Media, 2016. [Official online edition](https://sre.google/sre-book/testing-reliability/). Accessed 2026-09-06.
6. Amazon Web Services, “Use fault isolation to protect your workload,” *AWS Well-Architected Framework: Reliability Pillar*, current online edition. [Official documentation](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/use-fault-isolation-to-protect-your-workload.html). Accessed 2026-09-06.

Current vendor claims are source-specific and were checked on 2026-09-06. The probability, coding, quorum, and capacity examples are educational models with declared assumptions, not production guarantees.

## Exercises

### Exercise 1

A service needs 480 requests/second after one instance failure. It has four active instances rated at 160 each, but degraded-operation tests support a 90% derating. Determine whether the design meets the requirement after one loss and calculate its usable margin.

### Exercise 2

For four independent components where at least three must succeed and each fails with probability 2%, derive system-failure probability. Then add a 0.1% exhaustive common-cause probability using the chapter model.

### Exercise 3

A primary times out during a lease renewal, a standby obtains a higher epoch, and the old primary can still reach storage. Specify the fencing rule, effect-receiver behavior, retry handling, and evidence needed to prevent split brain.

### Exercise 4

Compare two identical regional stacks with two stacks implemented on different vendors. Identify three common modes diversity might reduce, four it might retain, and the operational evidence required before choosing.

### Exercise 5

A company has live multi-zone replication, daily immutable backups in the same administrative account, a quarterly restore test, and one global deployment pipeline. Design a layered improvement against zone loss, destructive credentials, bad software rollout, and long-dormant recovery failure without claiming that unlimited duplication is optimal.

## Answers to the Exercises

### Answer 1

After one loss, three instances remain. Each has usable capacity $160(0.9)=144$, so total usable capacity is $3(144)=432$ requests/second. This is below 480 by 48 requests/second; margin is $432-480=-48$. Nominal capacity would equal 480, but the tested derating disproves that optimistic condition. Add capacity, reduce degraded demand through admission or feature shedding, or improve and revalidate the limiting behavior.

### Answer 2

Failure means zero, one, or two successes; equivalently, at least two component failures. With success probability 0.98 and failure probability 0.02,

$$
P_I=\binom40(0.02)^4+\binom41(0.98)(0.02)^3+\binom42(0.98)^2(0.02)^2.
$$

This is $0.00000016+0.00003136+0.00230496=0.00233648$, or 0.233648%. With $c=0.001$, total is $0.001+0.999(0.00233648)=0.00333414352$, or about 0.333414352%. The result depends on independent identical residual failures and an exhaustive common-cause partition.

### Answer 3

The standby must obtain a monotonically higher epoch from an authority that cannot grant overlapping valid epochs under the model. Every storage mutation carries that epoch, and storage durably rejects commands from any epoch below the highest accepted value. The old primary's network access then cannot preserve write authority. A renewal timeout is indeterminate: query authoritative lease or epoch state rather than assuming renewal failed. Persist operation identity, record grants and rejections, test delayed old-primary writes, and verify that all effect receivers enforce fencing. Merely notifying the old primary or comparing wall clocks is insufficient.

### Answer 4

Vendor diversity might reduce one provider's facility design defect, regional control-plane defect, or product-specific software vulnerability. It can retain the same application artifact, deployment system, DNS, identity, source repository, specification defect, operator group, and physical geography; any four with causal explanation suffice. Evidence includes transitive dependency and physical-path maps, provider scope documentation, shared-library and artifact inventories, failure histories, representative failover tests, state compatibility, capacity tests, security review, recovery time, team competence, patch performance, and full lifecycle cost. Choose only if the reduced modeled risk exceeds integration and operational risk.

### Answer 5

Keep multi-zone serving placement and test zone loss under degraded load. Move or copy recovery data under a separately scoped administrative and deletion authority, retain multiple recovery points, and verify integrity. Stagger deployment by zone or cell, preserve known-good compatible capacity, gate rollout on user and data signals, and protect pipeline credentials. Increase restore-test frequency according to recovery objectives, automate validation safely, and rehearse loss of the primary account and control plane. Track replication, backup, deployment, identity, and operator domains separately. The plan targets four named causes; further copies are justified only by additional requirements, evidence, and lifecycle trade-offs.
