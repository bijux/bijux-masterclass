---
module_id: SARCH-056
program: Software Engineering: Software Architecture
level: 2
module_number: 56
title: Cell-Based Architecture
status: complete
last_verified: 2026-09-06
---

# Cell-Based Architecture

## One-Page Review

### Governing question

How should a system repeat bounded, independently operable serving units and assign workloads to them so that growth, failure, overload, deployment, and recovery have limited blast radius without creating unsafe shared dependencies or an unmanageable fleet?

### Essential definitions

- A **cell** is a bounded deployment and failure-isolation unit containing the compute, state, dependencies, capacity, and controls needed for a declared workload slice.
- A **stamp** is a repeatable deployable instance of an architectural stack; a stamp becomes a useful cell only when ownership and failure are meaningfully isolated.
- A **cell key** maps a tenant, account, resource, or request to its home cell.
- A **cell directory** is authoritative metadata resolving cell keys to current cells and epochs.
- A **blast radius** is the users, data, capabilities, or operations one fault or change can affect.
- A **noisy neighbor** consumes shared resources enough to harm another workload.
- **shuffle sharding** assigns each workload a small subset selected from a larger pool so unrelated workloads overlap only partially.
- A **global service** is shared across cells; a **regional service** is shared within a location; a **cell-local service** belongs to one cell.
- **evacuation** moves or rejects a cell's workload after danger; **rebalancing** changes assignments for capacity or policy.
- **fleet drift** is unintended divergence among cells in software, configuration, data schema, policy, or operation.

### Central model, mechanism, or theorem

If $M$ equally weighted tenants are assigned evenly to $C$ independent cells, one complete cell loss affects approximately $M/C$ tenants, or fraction $1/C$. This is only a planning model: correlated shared services, whale tenants, cross-cell workflows, and routing failure can enlarge impact.

For shuffle sharding that assigns each tenant $r$ distinct workers from a pool of $C$, there are

$$
\binom{C}{r}
$$

possible subsets. Under uniform independent assignment, the probability that another tenant receives exactly the same subset is $1/\binom{C}{r}$. The expected overlap size between two subsets is $r^2/C$. These combinatorial properties reduce shared fate probabilistically; they do not prove capacity, independence, or application correctness.

### Critical invariants

- every tenant or key resolves to one authoritative home cell and routing epoch for each operation requiring unique ownership;
- the declared cell boundary includes every dependency needed for the isolation claim, or shared dependencies are named explicitly;
- one cell cannot exhaust another's bounded compute, state, connection, queue, quota, or operator capacity;
- cell placement satisfies failure-domain, residency, encryption, and tenant-isolation policy;
- global services have narrower responsibilities, bounded data, and failure behavior under cell autonomy;
- cell templates are immutable or versioned, reproducible, observable, and tested from empty bootstrap;
- deployment, configuration, schema, and policy versions can be identified per cell;
- moves preserve business identity, state, authority, fencing, in-flight work, and deletion semantics;
- evacuation load fits tested destinations or degrades explicitly without collapsing healthy cells;
- a whale tenant receives dedicated or subcell treatment before it destroys balance assumptions;
- cross-cell workflows expose consistency, partial failure, and reconciliation semantics;
- fleet automation limits concurrency and has independent stop conditions;
- cell health is capability-specific and external to the failed cell where necessary;
- recovery is complete only when tenant and business outcomes reconcile.

### Common failures

Common failures include calling namespaces cells while all share one database; routing by current hostname; assigning tenants randomly without workload weights; letting one large tenant dominate a cell; centralizing identity, keys, configuration, artifacts, queues, or telemetry into an undeclared single failure domain; failing over one cell into every healthy cell without reserve; deploying a bad version to all cells at once; allowing fleet drift to become a permanent fork; performing cross-cell transactions through ad hoc retries; copying regulated data into an ineligible evacuation cell; and declaring cell recovery when infrastructure is green but tenant workflows remain duplicated or missing.

### Compact example

A service places 12,000 equal tenants across 24 cells, about 500 per cell. A single isolated cell nominally affects 4.17% rather than the whole fleet. Yet one payment gateway and one global tenant directory serve every cell; if either fails, the blast radius returns to 100%. The design therefore gives the directory a small cached read path with epochs, scopes payment degradation explicitly, and never claims full cell independence.

### Connections

[SARCH-053](053-partitioning-and-data-placement.md) supplies placement, [SARCH-054](054-multi-region-topologies.md) supplies regional capacity, and [SARCH-055](055-control-plane-and-data-plane-architecture.md) supplies fleet control. [SARCH-057](../ROADMAP.md) next studies queue-based leveling. Platform Engineering owns cell provisioning and fleet operation; this module owns architectural boundaries and isolation contracts.

## Governing Question

Large shared clusters use capacity efficiently, but every shared resource can connect otherwise unrelated failures. A bad deployment, hot tenant, corrupt queue, exhausted connection pool, or operator mistake may affect the entire population. Cell architecture trades some pooling efficiency for bounded repetition and independent operation.

The central question is not how many identical stacks can be deployed. It is what belongs inside the cell, what must remain shared, how identities map to cells, how capacity and policy are balanced, and how the fleet evolves without simultaneous exposure.

## Why This Matters

At scale, percentage reliability can hide concentrated harm. A one-percent fleet failure may mean every operation for a fixed group of customers fails for hours. Conversely, a globally shared outage can defeat hundreds of apparently independent deployments.

Cells make blast radius an architectural quantity, but they introduce a fleet: directories, templates, version skew, movement, spare capacity, tenant fairness, observability, and repeated operational cost. Isolation that cannot be deployed, tested, and repaired consistently becomes fragmentation.

## Prerequisites and Retrieval

Retrieve partition, shard, tenant, workload, failure domain, blast radius, noisy neighbor, routing, directory, epoch, fencing, replica, region, capacity, headroom, quota, bulkhead, deployment unit, control plane, data plane, schema, residency, idempotency, evacuation, reconciliation, and SLO.

From SARCH-011 retrieve bulkheads and recovery; SARCH-025 and SARCH-048 provide deployment and release independence; SARCH-051 provides partial failure; SARCH-053 provides partitioning and movement; SARCH-054 provides regional topology; and SARCH-055 provides control-plane scope.

## Learning Objectives

After completing this module, you should be able to:

1. define a cell boundary from failure, capacity, data, and operating requirements;
2. distinguish a repeatable stamp from an independently useful cell;
3. classify dependencies as global, regional, or cell-local and expose residual shared fate;
4. design cell keys, directories, epochs, and stale-route behavior;
5. quantify elementary blast-radius and shuffle-shard overlap while stating assumptions;
6. handle whale tenants, noisy neighbors, cross-cell operations, and uneven growth;
7. design progressive cell rollout and fleet drift control;
8. migrate and evacuate tenants with authority, residency, and reconciliation;
9. allocate reserve without cascading overload into healthy cells;
10. evaluate cell evidence without treating instance count as independence proof.

## Core Exposition

**Define the isolation claim first.** A cell might isolate tenant traffic, data corruption, overload, deployment, operator action, region loss, or security compromise. One boundary rarely isolates every cause. State the protected population, capability, and fault set.

A cell can be application-wide for a tenant cohort, data-specific for one shard, or capability-specific for a high-risk path. Avoid making one term cover incompatible scopes. Draw which components and state live inside and outside.

**Distinguish stamp from cell.** A deployment stamp is repeatable infrastructure and software. It may still depend on one global database, queue, identity service, or key. Repetition improves delivery consistency but not necessarily failure isolation.

A cell owns bounded capacity, state, and failure behavior for its declared slice. Some shared dependencies may remain, but the architecture records their blast radius and degraded behavior. Honest partial isolation is better than a fictional cell boundary.

**Choose the cell key from domain identity.** Tenant, account, organization, geographic resource, device fleet, or another stable identity can map work to a home cell. The key should preserve important locality and authority while avoiding sensitive information in routes and logs.

Do not bind public identity to a cell name. An authoritative directory maps stable identity to current cell and epoch, permitting movement. Clients may cache hints, but a trusted ingress resolves or validates current ownership.

**Design the directory as critical metadata.** The directory needs durability, consistency, versioning, bootstrap, cache, recovery, and security. It should contain minimal mapping and policy metadata, not become another global operational database.

Under directory loss, existing validated mappings may continue within bounds while new tenant creation and movement stop. Stale writes are rejected through cell epochs. A directory cache accelerates lookup but cannot independently grant ownership.

**Bound resources, not just processes.** Cells require isolation for CPU, memory, storage I/O, network, connections, threads, queues, caches, quotas, third-party calls, maintenance bandwidth, and operational attention. Shared node pools can retain hardware efficiency only if reservations and enforcement preserve the cell claim.

One global connection pool or queue can reconnect blast radii. Track per-cell and per-tenant consumption. Admission and backpressure act before exhaustion, and essential work receives protected capacity.

**Size from weighted workload.** Tenant count is a weak proxy. Model request rate, bytes, CPU, working set, storage operations, egress, growth, burst, and special operations. Assign by multiple constrained dimensions and measure tail behavior.

Packing cells tightly raises utilization but leaves little failure or movement reserve. Small cells limit impact and ease movement but increase fixed cost and fleet overhead. Choose maximum cell size from acceptable impact and recovery time, then validate cost.

**Handle whale tenants explicitly.** A tenant larger than ordinary cell capacity invalidates equal-assignment reasoning. Split the tenant by a subordinate stable key when invariants permit, provide a dedicated cell, or establish a larger class with separate objectives.

Do not let a whale share silently with small tenants. Dedicated capacity improves isolation but creates a unique topology and recovery path. Keep the same interfaces, controls, and evidence where possible.

**Use shuffle sharding where partial sharing is appropriate.** Rather than assign each tenant to one shared worker pool, choose a small subset. Failures or overload in one subset overlap with fewer other tenants. The combinations grow rapidly.

The benefit is probabilistic and workload-sensitive. Nonuniform selection, unequal workers, shared downstreams, and correlated faults reduce it. The subset must have capacity for the assigned tenants, and routing must be stable and observable.

**Minimize global services.** Truly global functions may include identity namespace, tenant directory, artifact provenance, policy roots, or aggregate billing. Keep their synchronous serving role narrow. Replicate or cache bounded verified state locally where semantics allow.

Global does not mean one deployment. It means fleet-wide scope. A replicated global service can still be a common semantic dependency or accept a bad global change. Apply its own cells, quorum, controls, and blast-radius limits.

**Place state with ownership.** Cell-local databases and queues prevent a hot or corrupt tenant cohort from consuming the whole fleet. Shared storage with cell partitions can be valid if resource and failure isolation are demonstrated.

Cross-cell secondary indexes and analytics should be asynchronous where possible and expose freshness. Global uniqueness may need a small coordinated authority. Do not copy every transactional join into a global store merely for convenience.

**Define cross-cell operations.** Transfers, collaboration, messaging, search, and reporting may cross cells. Choose a coordinator, distributed transaction, workflow, immutable event, projection, rights allocation, or explicit unsupported boundary.

Preserve one business identity across retries. A timeout between cells creates ambiguous outcomes. Reconciliation and compensation have owners. Cell isolation must not turn correctness into two unrelated local writes.

**Design deployment rings across cells.** Cells provide natural cohorts for progressive delivery: internal, canary, small production, representative risk classes, region groups, then broader fleet. Do not update every cell simultaneously merely because templates are identical.

Canaries must represent tenant size, region, data shape, workload, and dependencies. Define stop conditions from user capabilities and resource behavior. A cell acknowledgement does not prove every tenant path.

**Control fleet drift.** Some version skew is intentional during rollout; unmanaged skew becomes permanent forks. Inventory software, schema, configuration, policy, artifacts, and migrations by cell. Set compatibility windows and remediation ownership.

Emergency exceptions are explicit, expiring, and audited. Reproducible templates and declarative desired state reduce variation, but observed behavior and local state still require validation.

**Move tenants as authority migrations.** Provision target capacity and policy, copy a versioned snapshot, stream changes, verify data and indexes, fence old ownership, advance directory epoch, drain stale routes, reconcile in-flight work, and retain governed rollback state.

Large tenants may move in parts only if subordinate authority boundaries exist. Respect residency, encryption keys, audit, backups, tombstones, and queue state. DNS or load-balancer change alone is not a state migration.

**Design evacuation policy.** A cell may be isolated, overloaded, corrupt, compromised, or located in a threatened region. Not all cases permit moving its state. Corruption may require restore; compromise may require new trust roots; overload may require shedding rather than spreading.

Predeclare eligible destinations and reserve. Moving a failed cell's full load into tightly packed healthy cells can cascade. Prioritize essential capabilities and tenants, cap movement, and allow isolation to remain an intentional failure boundary.

**Choose failure containment over indiscriminate failover.** If every cell automatically accepts every other cell's traffic, overload becomes fleet-wide. Some architectures prefer one cohort unavailable while preserving the rest, with recovery into dedicated spare capacity.

Business criticality may require evacuation. Then hold warm empty cells, maintain spare fraction, or reduce normal utilization. Exercise actual tenant and data movement within RTO/RPO and policy constraints.

**Protect tenant and security boundaries.** Cell routing must authenticate the tenant; never trust a caller-supplied cell key alone. Scope service identities, keys, network access, administrative roles, and audit by cell and tenant where warranted.

A compromised global controller can still affect all cells. Agent-side policy limits, progressive rollout, multi-party approval, and independent stop controls reduce harm. A compromised cell should not obtain credentials for its neighbors.

**Observe locally and globally.** Record tenant, cell, directory and authority epoch, version, capacity, queue, latency, error, dependency, deployment, migration state, and business outcome without leaking private keys or sensitive tenant identifiers.

Keep local evidence when central telemetry fails. Fleet aggregation identifies patterns, but per-cell SLOs reveal concentrated harm hidden by global averages. Weight both tenant count and criticality.

**Operate the fleet as a product.** Templates, directory, provisioning, upgrade, compliance, capacity, evacuation, backup, restore, and retirement need owners and service objectives. Automation should be idempotent, rate-limited, resumable, and independently stoppable.

Measure time to create a cell, place a tenant, move it, restore from zero, patch a vulnerability, and remove a cell safely. Fleet toil can erase reliability gains if exceptional cells require bespoke action.

**Test isolation and recovery.** Saturate one cell, corrupt one queue, remove a database, break its control plane, deploy a bad version, expire credentials, lose the directory, misroute a tenant, and return an old cell after movement.

Verify unaffected cells, shared dependencies, capacity reserve, tenant outcomes, stale-route rejection, evidence, and operator control. Tests support only the exercised topology, load, and version; look for common causes after every breach.

## Definitions and Notation

Let:

- $C$ be the number of cells and $M$ the tenant population;
- $w_i^{(d)}$ be tenant $i$'s workload weight in dimension $d$;
- $L_c^{(d)}$ be load assigned to cell $c$ and $K_c^{(d)}$ its safe capacity;
- $U_c^{(d)}=L_c^{(d)}/K_c^{(d)}$ be normalized cell utilization;
- $H(i)$ be tenant $i$'s home cell and $e_i$ its current routing/authority epoch;
- $r$ be shuffle-shard subset size selected from a pool of $C$ workers;
- $I(A,B)=|A\cap B|$ be overlap between two assigned subsets;
- $F$ be the declared faults the cell boundary isolates;
- **residual shared fate** mean dependencies outside cells that can affect several or all cells;
- **fleet drift** mean unplanned divergence from governed cell versions;
- **evacuation capacity** mean eligible reserved capacity available without violating policy or harming healthy workloads.

Equal tenant counts imply neither equal $L_c^{(d)}$ nor equal consequences. Blast-radius claims must include weight, criticality, shared dependencies, and cross-cell propagation.

## Mechanisms, Invariants, or Proof Structure

### Cell-design procedure

1. State protected population, capabilities, faults, maximum blast radius, and recovery objectives.
2. Draw the complete request, state, control, identity, key, artifact, queue, telemetry, and operator dependencies.
3. Choose stable cell key, directory, authority epoch, routing, and stale-route rejection.
4. Define cell-local, regional, and global services and residual shared fate.
5. Size cells from multidimensional workload, tenant criticality, movement, and failure reserve.
6. Define whales, noisy neighbors, cross-cell operations, residency, and security isolation.
7. Build reproducible templates, progressive deployment rings, drift bounds, and independent stop controls.
8. Specify tenant move, cell evacuation, restore, reconciliation, and retirement states.
9. Test isolation, shared dependencies, capacity, policy, and tenant outcomes.

### Shuffle-shard derivation

There are $\binom{C}{r}$ unordered subsets of size $r$. With uniform independent assignment, exact-subset collision probability is its reciprocal. For expected overlap, each of the $r$ members in subset $A$ is in independently sampled subset $B$ with marginal probability $r/C$, so linearity of expectation gives $\mathbb{E}[I(A,B)]=r(r/C)=r^2/C$. Membership events within one subset are dependent, but independence among indicators is not required for linearity.

### Architectural invariants

- no cell claim without explicit local and shared dependencies;
- no tenant write without current home-cell authority or an explicit cross-cell protocol;
- no cell failure may consume unbounded healthy-cell capacity;
- no fleet change exposes every cell simultaneously without a separately justified necessity;
- no cell move omits fencing, in-flight work, deletion, policy, and business reconciliation;
- no global aggregate hides a persistently failed tenant cohort.

## Alternatives and Trade-Offs

| Choice | Strength | Cost or risk | Required evidence |
|---|---|---|---|
| large shared cluster | pooling efficiency | broad resource and change blast radius | quotas and failure tests |
| small full-stack cells | bounded failure and movement | fixed cost and fleet size | bootstrap and fleet automation |
| shared storage partitions | storage efficiency | residual contention and corruption scope | enforced resource isolation |
| cell-local storage | strong data isolation | cross-cell query and movement complexity | backup, restore, reconciliation |
| tenant home cell | locality and accountability | skew and movement | weighted placement and directory |
| shuffle sharding | combinatorial partial isolation | probabilistic overlap and routing | assignment and capacity simulation |
| global service | uniform fleet semantics | common dependency and change risk | local degradation and blast limits |
| dedicated whale cell | protects small tenants | lower utilization and special recovery | consistent interfaces and exercises |
| automatic evacuation | shorter outage | cascade, corruption, policy risk | reserve and fault classification |
| containment-first | protects healthy cells | affected cohort remains unavailable | recovery objectives and communication |

## Failure Modes and Misconceptions

1. **“A repeated stack is a cell.”** repetition does not establish isolation.
2. **“One cell failure affects exactly one over C.”** skew and shared dependencies change impact.
3. **“Cells remove global services.”** some global scope remains and must be bounded.
4. **“Namespaces isolate resources.”** underlying pools and quotas determine contention.
5. **“Random tenant placement balances load.”** tenant weights and correlations differ.
6. **“A whale is just several tenants.”** one identity and invariant boundary may remain serial.
7. **“Shuffle sharding prevents collisions.”** it reduces exact and partial overlap probabilistically.
8. **“The directory may be eventually right.”** stale write ownership can create split authority.
9. **“Cross-cell means asynchronous.”** distributed coordination remains possible at a cost.
10. **“Every cell should fail over everywhere.”** that can spread overload or corruption.
11. **“Canary one cell and deploy all.”** representativeness and fleet concurrency still matter.
12. **“Identical templates prevent drift.”** local state, policy, and emergency changes diverge.
13. **“Cell-local telemetry proves fleet health.”** global paths and shared services remain.
14. **“Global averages show customer impact.”** one cohort can disappear inside the mean.
15. **“Tenant movement is routing.”** state, authority, policy, and in-flight work move too.
16. **“More cells always improve reliability.”** operational complexity can exceed control capability.

## Worked Examples

### Example 1

**Situation.** Twelve thousand equal tenants are placed across 24 independent cells.

**Reasoning.** Even assignment gives 500 tenants per cell and nominal loss fraction $1/24\approx4.17\%$. If all cells synchronously require one global identity service, its loss still affects 100%. Report both the cell-local and residual global blast radii.

**Conclusion.** Cell count bounds only faults actually contained by the boundary.

### Example 2

**Situation.** A namespace-per-cell deployment shares one database connection pool.

**Reasoning.** One cell's slow queries consume every connection, so the supposed boundary does not isolate the constrained resource. Allocate per-cell pools and database budgets, or narrow the isolation claim and add admission before shared exhaustion.

**Conclusion.** Resource enforcement, not naming, establishes noisy-neighbor isolation.

### Example 3

**Situation.** One tenant generates 45% of fleet writes while all others are assigned evenly.

**Reasoning.** No ordinary cell can host it under the equal-tenant model. Partition it by a subordinate domain key if invariants permit, or give it a dedicated capacity class. Keep its directory identity stable and test its distinct recovery path.

**Conclusion.** Whale handling is part of the architecture, not an exceptional placement script.

### Example 4

**Situation.** Each tenant receives two workers from a pool of ten through shuffle sharding.

**Reasoning.** There are $\binom{10}{2}=45$ subsets, so exact-subset collision probability is $1/45\approx2.22\%$. Expected pairwise overlap is $2^2/10=0.4$ workers. Unequal selection or a shared database can dominate these benefits.

**Conclusion.** Combinatorial assignment reduces shared fate under explicit uniformity and independence assumptions.

### Example 5

**Situation.** The tenant directory is unavailable but cells and ingress caches remain healthy.

**Reasoning.** Existing authenticated mappings continue within epoch and expiry bounds; storage rejects stale epochs. New tenant creation and moves stop. Cache miss returns explicit unavailability rather than guessing a cell. Recovery validates directory history before new assignments.

**Conclusion.** A bounded cached lookup path can preserve existing service without decentralizing authority.

### Example 6

**Situation.** A release succeeds in a tiny internal cell and is scheduled for all 80 production cells.

**Reasoning.** The canary lacks whale tenants, old schemas, and one jurisdictional policy. Add representative cohorts, limit concurrent cells, probe user capabilities, and stop automatically on weighted error, latency, or invariant evidence. Preserve mixed-version compatibility.

**Conclusion.** Cells enable progressive delivery only when exposure reflects risk and concurrency is bounded.

### Example 7

**Situation.** Cell A is saturated and automation redistributes its work across nine cells at 92% utilization.

**Reasoning.** Even spreading adds roughly $0.92/9\approx10.2$ percentage points if A had equal load, pushing survivors above capacity before retry and cache costs. Contain A, shed optional work, or use reserved evacuation capacity; indiscriminate failover causes cascade.

**Conclusion.** Healthy-cell protection may require leaving one cohort degraded.

### Example 8

**Situation.** A regulated tenant moves to a new cell in another region.

**Reasoning.** Verify destination residency and key policy, provision capacity, copy snapshot, stream changes, validate indexes and tombstones, fence old epoch, advance directory, drain stale routes, reconcile queues and external effects, and retain compliant rollback evidence.

**Conclusion.** Cell movement is governed authority and state migration.

### Example 9

**Situation.** Search combines results from 60 cells and one cell times out.

**Reasoning.** Returning 59/60 results may be acceptable only if the API marks incompleteness and the missing cohort's harm is understood. A global index can reduce fan-out but becomes another shared data path. Deadlines, partial ordering, privacy, and retry work need contracts.

**Conclusion.** Cross-cell aggregation trades isolation for completeness, latency, and global dependency.

### Example 10

**Situation.** A cell returns after a tenant moved away during its partition.

**Reasoning.** Its old epoch cannot resume writes. Quarantine it, compare durable operation identities and change positions, reconcile ambiguous effects with the new authority, retain required evidence, and retire or rebuild it from current templates.

**Conclusion.** Returning cells are stale actors until authority and business state are reconciled.

## Cross-Program Connections

- **Platform Engineering:** owns cell provisioning, directories, schedulers, quotas, topology, and fleet automation.
- **Cloud Engineering:** owns regional resources, provider limits, identity, networking, cost, and shared-responsibility boundaries.
- **Distributed Systems Engineering:** owns sharding, membership, epochs, consensus, replication, and reconfiguration protocols.
- **Database Engineering:** owns cell-local data, distributed transactions, indexes, backup, restore, and movement mechanisms.
- **Security Engineering:** owns tenant isolation, cell credentials, key scope, compromise containment, and emergency authority.
- **Software Delivery and Reliability Engineering:** owns rollout rings, SLOs, evacuation exercises, drift remediation, and incidents.
- **Data Architecture Engineering:** owns tenant authority, residency, lineage, retention, deletion, and cross-cell analytical data.
- **Systems Engineering:** connects cell failure and recovery to capacity, people, physical processes, and safety.

## References

1. Michael T. Nygard, *Release It! Design and Deploy Production-Ready Software*, 2nd ed., Pragmatic Bookshelf, 2018.
2. David Karger et al., “Consistent Hashing and Random Trees: Distributed Caching Protocols for Relieving Hot Spots on the World Wide Web,” *STOC 1997*. <https://doi.org/10.1145/258533.258660>
3. Atul Adya et al., “Slicer: Auto-Sharding for Datacenter Applications,” *OSDI 2016*. <https://www.usenix.org/conference/osdi16/technical-sessions/presentation/adya>
4. Abhishek Verma et al., “Large-scale Cluster Management at Google with Borg,” *EuroSys 2015*. <https://doi.org/10.1145/2741948.2741964>
5. Amazon Web Services, “REL10-BP04 Use bulkhead architectures to limit scope of impact,” *AWS Well-Architected Framework*, retrieved 2026-09-06. <https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_fault_isolation_multiaz_region_system.html>
6. Amazon Web Services, “Shuffle Sharding: Massive and Magical Fault Isolation,” *AWS Architecture Blog*, 2014. <https://aws.amazon.com/blogs/architecture/shuffle-sharding-massive-and-magical-fault-isolation/>
7. Microsoft, “Deployment Stamps pattern,” *Azure Architecture Center*, retrieved 2026-09-06. <https://learn.microsoft.com/azure/architecture/patterns/deployment-stamp>
8. Betsy Beyer et al., eds., *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly Media, 2016. <https://sre.google/sre-book/table-of-contents/>

## Exercises

### Exercise 1

Define cell, stamp, cell key, cell directory, blast radius, noisy neighbor, shuffle sharding, global service, regional service, cell-local service, evacuation, rebalancing, fleet drift, residual shared fate, and evacuation capacity.

### Exercise 2

For shuffle shards of size 3 selected uniformly from 20 workers, compute the number of possible subsets, exact-subset collision probability, and expected pairwise overlap. Explain what the results do not prove.

### Exercise 3

Diagnose a “cell-based” service whose cells share one writable database, global queue, unscoped credential, and deployment wave; whose client chooses a cell name; and whose failover spreads load to all cells. Propose a coherent redesign and evidence.

### Exercise 4

Compare a large shared cluster, full-stack tenant cells, shared-storage cells, dedicated whale cells, and shuffle-sharded worker pools for cost, locality, isolation, global operations, movement, deployment, and recovery.

### Exercise 5

Design cell architecture for an international disaster-response platform serving emergency agencies, shelters, medical teams, public alerts, volunteers, supply depots, and intermittently connected field devices. Include cell keys, state, shared services, residency, uneven disasters, authority, capacity, rollout, cross-cell workflows, evacuation, security, recovery, evidence, and human command.

## Answers to the Exercises

### Answer 1

A **cell** is a bounded independently operable serving and failure unit; a **stamp** is a repeatable deployed stack that may lack true isolation. A **cell key** maps stable domain identity to a home cell; a **cell directory** authoritatively stores that mapping and epoch. **Blast radius** is affected scope. A **noisy neighbor** harms others through shared consumption. **Shuffle sharding** assigns small subsets from a larger pool to reduce overlap. **Global**, **regional**, and **cell-local services** have fleet-wide, location-wide, and one-cell scope. **Evacuation** moves or rejects work after danger; **rebalancing** changes assignment for capacity or policy. **Fleet drift** is unintended cell-version divergence. **Residual shared fate** is cross-cell dependency exposure. **Evacuation capacity** is eligible reserved destination capacity that preserves policy and healthy service.

### Answer 2

$\binom{20}{3}=20\cdot19\cdot18/(3\cdot2\cdot1)=1{,}140$ subsets. Exact-subset collision probability is $1/1{,}140\approx0.000877$, or about 0.0877%. Expected overlap is $3^2/20=0.45$ workers. These results assume uniform independent subset assignment and say nothing about worker capacity, tenant weights, partial-overlap harm distribution, correlated infrastructure, shared databases, routing correctness, security, or application invariants.

### Answer 3

The design repeats compute but retains global data, queue, credential, change, and overload blast radii. Choose a stable authenticated tenant key; resolve it through an authoritative minimal directory and route via trusted ingress. Give each cell bounded data partitions or demonstrate enforced storage isolation, cell-local queues or quotas, scoped credentials, and resource admission. Storage accepts only current directory/authority epochs; callers cannot choose ownership.

Progress releases through representative cells with bounded concurrency and independent stop conditions. Keep necessary global services narrow and define cached or degraded behavior. Fail a cell into dedicated reserve or shed optional work according to priority rather than overloading every neighbor. Test database and queue contention, credential compromise, stale route, directory loss, whale load, bad rollout, cell loss, destination saturation, and restoration. Evidence includes tenant/cell/epoch, weighted capacity, local and shared dependency outcome, version, migration state, business result, and unaffected-cell verification.

### Answer 4

A large shared cluster maximizes pooling and simplifies global queries but broadens resource, change, and corruption impact. Full-stack tenant cells isolate compute and state strongly and make tenant outcomes legible, at fixed-cost, cross-cell-query, directory, and fleet complexity. Shared-storage cells reduce storage overhead but retain contention, maintenance, and corruption exposure unless partitions and budgets are enforced. Dedicated whale cells protect small tenants and tune capacity, but create lower utilization and uncommon recovery paths. Shuffle-sharded workers gain combinatorial partial isolation with less full-stack duplication, but assignment is probabilistic and downstream dependencies may reconnect fate.

Choose by acceptable blast radius, workload weights, transaction locality, residency, movement time, global-index requirements, deployment independence, reserve, and operator capacity. Mixing is normal: full-stack cells for regulated transaction paths, dedicated cells for whales, shared asynchronous analytics, and shuffle-sharded stateless processing. State residual shared fate and test it.

### Answer 5

Use stable agency or jurisdiction identity as the top-level cell key, with subordinate incident cells only when command and data authority are explicit. Each cell owns agency operations, shelter state, scoped medical coordination, volunteer assignments, local alert drafts, supply rights, queues, and bounded offline synchronization. A minimal global directory maps agencies and public regions to cells by epoch. Global functions are limited to federation trust, signed alert namespace, artifact provenance, and aggregate public discovery; cells retain validated bounded state when these are unavailable.

Residency and medical privacy cover replicas, backups, logs, repair, support, and evacuation. Disaster intensity creates whale incidents: allocate dedicated incident capacity or split by operational sector while one named command authority coordinates safety invariants. Supply depots allocate conserved rights to disconnected field units. Public alerts carry signed identity, geographic scope, supersession, expiry, and retraction; stale drafts cannot override a newer command epoch. Cross-cell mutual aid uses durable request identities, explicit acceptance, resource transfer, and reconciliation rather than two local best-effort updates.

Reserve eligible cells by region and jurisdiction; protect healthy agencies through admission and safety priorities. Evacuation classifies overload, physical region threat, corruption, and compromise before moving. A compromised cell receives new trust roots and cannot authenticate as neighbors. Releases progress through representative quiet and disaster-load cells with stop controls. Field devices bootstrap from sealed trust and cached policy, expose staleness, and reconcile after links return.

Evidence records agency, incident, cell and authority epoch, policy and artifact versions, data freshness, capacity, queue age, supply rights, alert state, cross-cell commitment, operator decision, degraded mode, physical confirmation, and terminal outcome. Exercises include whale disaster, directory loss, false global alert, stale device, cell compromise, region evacuation, shared identity loss, bad rollout, saturated reserve, and returning old cell. Named incident commanders, medical officers, security leaders, and public authorities hold scoped expiring emergency powers and independent stop channels.
