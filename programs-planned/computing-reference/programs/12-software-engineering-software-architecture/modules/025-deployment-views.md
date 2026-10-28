---
module_id: SARCH-025
program: Software Engineering: Software Architecture
level: 1
module_number: 25
title: Deployment Views
status: complete
last_verified: 2026-09-06
---

# Deployment Views

## One-Page Review

### Governing question

How can an architecture description map immutable artifacts and runtime instances onto execution environments, physical or virtual nodes, communication paths, and failure domains so that stakeholders can reason about capacity, availability, latency, security, operations, change, and conformance?

### Essential definitions

- A **deployable artifact** is a versioned unit prepared for installation or execution, such as an executable, package, image, firmware bundle, configuration bundle, or static asset.
- A **runtime instance** is one executing realization of an artifact or component at a particular time.
- A **node** is a computational resource that hosts execution environments or artifacts; it may represent physical hardware, a virtual machine, a device, or another declared infrastructure unit.
- An **execution environment** supplies runtime services and constraints, such as an operating system process space, language runtime, container, function environment, or device firmware context.
- A **placement** maps an artifact or runtime instance to a compatible execution environment and node.
- A **communication path** is a deployed route with protocol, direction, addressing, trust, capacity, latency, and failure properties.
- A **failure domain** is a set of resources that may fail together because they share a cause or authority.
- A **deployment unit** is the smallest artifact set independently released, installed, activated, rolled back, or scaled under the declared process.
- **desired state** is the authorized intended deployment; **observed state** is what evidence reports currently exists.
- **drift** is a material difference between desired and observed deployment state.

### Central model, mechanism, or theorem

Represent a deployment configuration as

$$
D=(N,X,A,R,\pi,L,F,Q),
$$

where $N$ is nodes, $X$ execution environments, $A$ immutable artifacts, $R$ runtime instances, $\pi$ maps environments, artifacts, and instances to hosts, $L$ is communication paths, $F$ is failure-domain membership, and $Q$ is placement and quality constraints.

For resource dimension $k$, feasible placement requires

$$
\sum_{r:\pi(r)=n} demand_k(r) + reserve_k(n) \le capacity_k(n)
$$

for every node $n$. This is a necessary static constraint, not a performance guarantee: burst, interference, fragmentation, throttling, failure, and measurement error remain.

### Critical invariants

- declare environment, lifecycle state, scenario, resolution, and notation;
- distinguish source modules, artifacts, execution environments, runtime instances, nodes, and locations;
- bind deployed artifacts to immutable version and integrity identities;
- state compatibility for operating system, architecture, runtime, device, accelerator, and dependency assumptions;
- expose replica count, placement, routing, state, and failure-domain independence;
- budget compute, memory, storage, network, startup, and operational reserve;
- show data locality, persistence, backup, recovery, and authority;
- expose trust zones, identities, secrets, administrative paths, and supply-chain boundaries;
- model normal, degraded, maintenance, rollout, rollback, recovery, and disaster configurations;
- reconcile deployment with runtime, interaction, data, security, build, and operational views;
- compare desired state with observed, versioned evidence and record uncertainty.

### Common failures

Common failures include drawing a vendor inventory instead of architectural placement; equating a component with a container or machine; omitting artifact identity and configuration; showing replica count without failure domains; assuming zones, nodes, racks, accounts, or clusters are independent without evidence; ignoring shared control planes and network dependencies; treating requests as capacity guarantees; omitting persistent state and data gravity; hiding administrative access and secrets; showing only steady state; confusing scheduled with ready or serving; and claiming declared deployment proves observed production state.

### Compact example

Three API replicas satisfy a “three copies” count, but all three on one physical host share one failure domain. A deployment view that maps each replica to a distinct node and each node to a distinct qualified zone makes the availability assumption reviewable. It must still expose their shared database, identity provider, load balancer, network, and control plane.

### Connections

[SARCH-022](022-module-and-code-views.md) supplies implementation structure; [SARCH-023](023-component-and-connector-views.md) supplies runtime topology; [SARCH-024](024-runtime-interaction-views.md) supplies causal paths. [SARCH-026](../ROADMAP.md) next develops data and information views. Platform, Cloud, Systems, Networks, Security, and Reliability Engineering deepen deployment mechanisms.

## Governing Question

Logical architecture can be sound while its deployment defeats the intended qualities. Redundant processes placed on one host are not resilient to host failure. A low-latency service placed far from its data pays network delay and transfer cost. An image built for one processor architecture cannot run on an incompatible node. A secure application with an exposed administrative path is not securely deployed.

The governing problem is to show where executable things can and do run, what connects them, which resources and authorities they share, how configurations change, and what evidence supports the claims. A useful deployment view is more than an asset list: it explains placement decisions and their consequences.

## Why This Matters

Deployment determines concrete failure, performance, security, and operational behavior. CPU scheduling, memory limits, storage media, network paths, locality, device capabilities, trust zones, and update mechanisms constrain the running system. Configuration transitions create mixed versions and temporarily reduced capacity. Recovery depends on artifacts, state, credentials, control planes, and people being available together.

Modern infrastructure adds indirection rather than eliminating placement. A scheduler may decide the exact node late, but architecture still declares eligible pools, affinities, anti-affinities, topology domains, resources, identities, and constraints. “Serverless” still executes on provider-managed nodes; it changes which placement decisions the consumer controls and what evidence is available.

A deployment view enables capacity review, threat modeling, failure analysis, rollout planning, cost reasoning, incident diagnosis, and conformance checks. It should remain intelligible even when a product or provider changes.

## Prerequisites and Retrieval

Retrieve artifact, package, image, executable, configuration, node, host, device, virtual machine, process, container, runtime, instance, replica, scheduler, placement, affinity, anti-affinity, topology, zone, region, failure domain, communication path, capacity, demand, reserve, persistence, state, identity, secret, desired state, observed state, drift, rollout, rollback, and recovery.

From prior modules, retrieve stakeholders and concerns, quality scenarios, availability, performance, scalability, security, interoperability, observability, context views, module/code views, component-and-connector views, and runtime interactions. Distinguish logical responsibility, built artifact, executing instance, infrastructure resource, and organization owner.

## Learning Objectives

After completing this module, you should be able to:

1. define artifacts, nodes, execution environments, instances, placements, paths, and failure domains;
2. select logical, physical, and environment-specific deployment resolutions;
3. map components through artifacts and instances to compatible hosts;
4. check resource feasibility and explain why it does not guarantee performance;
5. reason about replica independence, shared dependencies, locality, and state;
6. expose trust zones, workload identities, secrets, administrative paths, and integrity;
7. model rollout, rollback, scaling, recovery, and degraded configurations;
8. compare static placement, scheduler constraints, and observed placement evidence;
9. detect cross-view mismatch and deployment drift;
10. evaluate a deployment design against quality scenarios and evidence limits.

## Core Exposition

**Frame the deployment concern.** State stakeholders, environment, lifecycle state, scenario, resolution, and time. A logical deployment view may show zones and workload classes. A physical view may show sites, racks, devices, and network segments. An environment-specific view may show exact clusters, node pools, and artifact digests. Production, test, disaster recovery, and edge installations may need separate views.

ISO/IEC/IEEE 42010:2022 remains the current published architecture-description edition as checked on 2026-09-06 and requires architecture models to be governed by concerns, viewpoints, model kinds, and correspondences [1]. UML 2.5.1 provides nodes, execution environments, artifacts, deployment relationships, and communication paths as one available notation [2]. The notation does not choose the right failure domains or prove the deployed state.

**Separate conceptual layers.** A source module is built into an artifact. An artifact is installed or made available to an execution environment. A runtime instance realizes behavior from an artifact. An execution environment is hosted on a node. Nodes exist within physical, administrative, network, and failure locations.

These relations are many-to-many. One image can create many instances; one process can load several artifacts; one node can host many environments; one logical component can be realized by several artifacts; and one deployment unit can package multiple components. Record the correspondence that matters rather than assuming identical boxes across views.

**Identify artifacts immutably.** Use content digest, signed version, build provenance, configuration identity, and compatibility metadata where applicable. A mutable tag such as `latest` is a locator, not an immutable identity. Rollback requires the exact prior artifacts and compatible configuration, schema, credentials, and runtime environment—not merely an old application binary.

The current Open Container Initiative image specification, checked 2026-09-06, defines an image using a manifest, optional index, filesystem layers, and configuration, with content-addressable descriptors [5]. Its runtime specification defines the runtime bundle and container lifecycle [6]. These standards are useful current examples of artifact and execution contracts, not a reason to model every deployment as a container.

**Model nodes and execution environments.** Nodes can represent devices, physical hosts, hypervisors, virtual machines, managed compute units, or trusted execution environments. Execution environments provide processes, runtimes, isolation, namespaces, libraries, accelerators, filesystems, clocks, and lifecycle behavior. Declare which layer owns scheduling, restart, update, telemetry, and resource enforcement.

Compatibility includes processor architecture, operating system and ABI, runtime and library versions, device features, accelerators, storage and network capabilities, regulatory location, and security posture. “Runs on Linux” is too weak when the artifact needs a specific instruction set, kernel feature, device, or mount behavior.

**Represent placement as constraints and instances.** At design time, a scheduler-managed system often specifies eligible placement rather than an exact host. Record selectors, affinities, anti-affinities, topology spread, resource requests, limits, priorities, disruption rules, and state locality as durable concepts. Then link to configuration carrying tool-specific syntax.

Kubernetes documentation retrieved 2026-09-06 describes topology spread constraints across domains such as regions, zones, nodes, and user-defined domains, while also documenting limitations: domains derive from eligible nodes and constraints need not remain satisfied after removals [7]. This illustrates why a declared scheduler rule is neither permanent balance nor proof of failure independence.

**Define failure domains from causes.** A failure domain is concern-relative. A host power loss, rack switch failure, zone outage, regional dependency failure, account lockout, bad rollout, certificate expiry, identity-provider failure, and operator error cut the deployment differently. Geographic separation does not protect against a shared control plane or globally distributed bad configuration.

For each quality scenario, identify common causes and administrative authorities. Then express separation constraints. If replicas must survive one node failure, they need distinct qualified node domains and enough remaining capacity. If they must survive a zone failure, dependencies and quorum placement must also span qualified zones.

**Check resources in several dimensions.** Map CPU, memory, accelerators, ephemeral storage, persistent storage, I/O, file descriptors, connections, bandwidth, address space, quotas, and startup demand. Reserve capacity for system services, telemetry, failover, rollout overlap, and uncertainty. Average demand cannot establish safe placement.

For resource $k$ on node $n$, require $\sum demand_k(r)+reserve_k(n)\le capacity_k(n)$. Check every relevant dimension; feasible CPU placement can still exhaust memory or network. Dynamic interference, burst, fragmentation, throttling, garbage collection, cache effects, and hardware variability require tests and observations.

**Map communication paths.** Show source and destination placements, protocol, routing, discovery, intermediary, trust crossing, encryption, identity, address family, bandwidth, latency, loss, and failure ownership. A logical connector may traverse client libraries, proxies, DNS, gateways, firewalls, load balancers, meshes, and provider networks.

Avoid drawing a single direct line when consequential intermediaries or shared paths exist. Separate data, control, management, replication, backup, and telemetry paths. An apparently independent pair of zones may depend on one interconnect, name service, certificate authority, or routing control plane.

**Place state deliberately.** Identify ephemeral, cached, authoritative, replicated, checkpointed, and externally stored state. Record volume attachment rules, locality, consistency, replication, encryption, backup, restore, retention, and deletion. A stateless process can still depend on stateful queues, identity, configuration, and databases.

Data gravity changes performance and recovery. Moving computation closer can reduce transfer and latency but increase operational diversity or failure coupling. Replicating state improves read locality or availability only under a defined consistency, lag, conflict, and recovery model. SARCH-026 deepens the information semantics.

**Expose security and administrative placement.** Mark trust zones, workload identity issuers, authentication and authorization points, secret delivery, key custody, certificate rotation, debug access, update channels, registries, and management networks. A workload network policy does not protect a privileged control plane with broader reach.

Artifact integrity and provenance are necessary but not sufficient. The node, runtime, configuration, secrets, and admission path must also be trustworthy for the claim. NIST SP 800-190 separates container image, registry, orchestrator, container, and host risks and emphasizes that isolation boundaries and operational controls require explicit treatment [8].

**Model configuration transitions.** Deployment is a state machine, not one snapshot. Show desired versions, old and new populations, admission of traffic, health and readiness gates, draining, schema compatibility, capacity overlap, rollback boundary, and terminal failure states. During a rolling change, mixed versions may communicate and share data.

“Scheduled,” “started,” “ready,” “serving,” and “healthy for this scenario” are distinct. A process can be running while dependencies are unavailable, caches cold, migrations incomplete, or traffic still routed elsewhere. Name the evidence and authority for each state.

**Plan degraded and recovery configurations.** Model node loss, zone loss, network partition, storage loss, control-plane loss, credential failure, capacity shortage, bad artifact, and operator lockout. Specify what relocates, what remains pinned, how state is recovered, and what reduced service is acceptable.

Recovery time includes detection, decision, provisioning, artifact retrieval, identity issuance, state restoration, warm-up, validation, and traffic shift. Recovery-point claims depend on state replication and backup evidence. A dormant recovery environment can drift even when its diagram remains attractive.

**Distinguish desired and observed state.** Infrastructure declarations, scheduler constraints, and release records express intent. Inventory, attestation, runtime APIs, telemetry, and direct inspection provide observations. Each can be stale, partial, or compromised. Record collection time, permissions, versions, and exclusions.

Conformance compares a normalized observed deployment with explicit constraints, not with pixel positions. Examples include allowed artifact digests, minimum replicas, prohibited co-placement, approved regions, compatible runtimes, required path encryption, and resource reserve. Passing a snapshot does not prove continuous conformance.

**Reconcile adjacent views.** Map source modules to artifacts; runtime components to instances; connectors to deployed paths; interactions to routes and latency boundaries; data authorities to storage; security decisions to trust zones; and operational responsibilities to control surfaces. A component with no artifact, artifact with no build owner, instance with no eligible node, or path with no connector is a review finding.

## Definitions and Notation

Define a deployment configuration

$$
D=(N,X,A,R,\pi,L,F,Q),
$$

where $N$ is nodes, $X$ execution environments, $A$ immutable artifacts, $R$ runtime instances, $\pi$ is the host/placement relation, $L$ is deployed communication paths, $F$ maps resources into concern-specific failure domains, and $Q$ is the set of compatibility, capacity, separation, locality, security, and lifecycle constraints.

For resource dimensions $K$ define capacity $capacity_k(n)$, reserved headroom $reserve_k(n)$, and demand $demand_k(r)$. Static feasibility is

$$
Feasible(D)\iff \forall n\in N,\forall k\in K:\
\sum_{r:\pi(r)=n} demand_k(r)+reserve_k(n)\le capacity_k(n).
$$

For replicas $r_i,r_j$ required to tolerate one domain failure under domain function $f\in F$, a separation constraint is

$$
i\ne j\implies f(\pi(r_i))\ne f(\pi(r_j)).
$$

This is meaningful only if $f$ reflects the relevant common cause and dependencies also satisfy the scenario.

Let $Desired$ be the authorized normalized deployment state and $Observed_t$ evidence collected at time $t$. Define concern-relative drift as a predicate $Drift_Q(Desired,Observed_t)$ over the constraints in $Q$. Absence of detected drift means only that available evidence satisfied the encoded constraints at $t$.

## Mechanisms, Invariants, or Proof Structure

Use this deployment-review mechanism.

1. **Frame:** name environment, time, lifecycle state, concern, scenario, resolution, and omissions.
2. **Resolve artifacts:** bind source responsibilities to immutable artifacts, configuration, provenance, and compatibility.
3. **Resolve runtime:** distinguish component roles, instances, execution environments, and lifecycle states.
4. **Map nodes:** identify physical, virtual, device, location, administrative, and topology properties.
5. **Place:** specify eligible hosts, exact instances where needed, multiplicity, affinity, anti-affinity, and locality.
6. **Budget:** check multidimensional demand, reserve, failover, rollout overlap, burst, and measurement uncertainty.
7. **Connect:** map data, control, management, backup, and telemetry paths with trust and failure properties.
8. **Challenge:** remove domains, paths, storage, control planes, credentials, capacity, and artifacts; examine recovery.
9. **Transition:** model rollout, rollback, scaling, maintenance, degraded operation, and disaster recovery.
10. **Reconcile and verify:** compare desired and observed state and map to runtime, interaction, data, security, build, and operations.

The governing invariants are immutable artifact identity, compatible placement, multidimensional feasibility, declared failure independence, explicit state locality, protected administrative authority, safe configuration transitions, cross-view correspondence, and evidence-bounded conformance.

If each replica occupies a different domain under $f$, removal of one such domain removes at most one replica. This follows directly from the separation constraint. It does not prove service availability: the remaining replicas may lack capacity, quorum, data, routing, credentials, or independent dependencies.

## Alternatives and Trade-Offs

**Exact placement versus scheduler constraints.** Exact placement aids appliances, regulated equipment, and incident records but can be brittle. Constraint-based placement supports dynamic scheduling but requires observable conformance and a precise topology vocabulary.

**Packing versus spreading.** Packing can improve utilization, locality, and cost. Spreading can reduce some correlated failures but adds network latency, transfer, coordination, and idle reserve. Choose against scenarios, not slogans.

**Virtual machines versus containers versus processes.** Each offers different packaging, isolation, startup, density, portability, and operational boundaries. The underlying host and control plane still matter. Do not infer security or failure independence from a label.

**Mutable hosts versus immutable replacement.** In-place change can be efficient for stateful or constrained devices but accumulates state and drift. Replacement improves reproducibility but requires externalized state, compatible transitions, artifact availability, and safe cutover.

**Centralized versus edge placement.** Centralization simplifies governance and aggregation. Edge placement reduces latency and supports offline operation but increases hardware diversity, physical exposure, limited capacity, delayed updates, and reconciliation needs.

**Active-active versus active-passive.** Active-active uses capacity continuously and can reduce failover time but needs routing, data, and conflict semantics. Active-passive can simplify authority but risks drift and untested recovery while reserving idle capacity.

**One detailed view versus layered projections.** A single inventory is compact but mixes abstraction and concerns. Linked logical, physical, security, network, and rollout projections preserve clarity if their correspondences are governed.

## Failure Modes and Misconceptions

- **A component is a container.** Logical responsibility, artifact, environment, instance, and host are different layers.
- **Three replicas mean high availability.** Co-placement and shared dependencies can make them one failure unit.
- **A zone label proves independence.** Labels describe topology; common causes and provider guarantees need evidence.
- **Resource requests guarantee performance.** Static feasibility omits burst, contention, throttling, and workload shape.
- **Stateless means no state dependency.** Configuration, identity, queues, caches, and databases remain stateful.
- **A mutable tag identifies an artifact.** It can resolve to different content; use an immutable digest or equivalent.
- **Encrypted application traffic secures deployment.** Administrative, registry, secret, backup, and control paths also matter.
- **Scheduled means serving.** Placement, startup, readiness, routing, and scenario health are distinct.
- **Rollback restores the old system.** Data, configuration, credentials, dependencies, and irreversible effects may have changed.
- **Desired state is actual state.** Declarations express intent; observation provides bounded evidence.
- **Separate regions remove common cause.** Global control planes, identities, releases, and operators may remain shared.
- **The deployment diagram is inventory.** A useful view explains constraints, qualities, transitions, and evidence.

## Worked Examples

### Example 1

**Situation.** A three-tier system has web, application, and database source modules.

**Reasoning.** Build web assets into artifact digest `w7`, application code into executable image `a12`, and database migrations into signed bundle `m4`. Deploy web assets through an edge cache, two `a12` instances in a managed runtime, and apply `m4` through a controlled migration environment to the database authority. The module names alone do not identify instances or placement.

**Conclusion.** Deployment views require explicit module-to-artifact-to-environment-to-node correspondences.

### Example 2

**Situation.** Three API replicas are scheduled on one 64-core host.

**Reasoning.** Replica count is three, but host failure removes all three. Under host-domain function $f_h$, every replica has the same value, violating pairwise separation. Place them on three qualified hosts and verify shared router, identity, storage, power, and control-plane dependencies separately.

**Conclusion.** Multiplicity without concern-specific failure separation does not establish resilience.

### Example 3

**Situation.** A node has 16 GiB allocatable memory and requires 2 GiB reserve. Three workers request 5 GiB each.

**Reasoning.** Total planned use is $3(5)+2=17$ GiB, exceeding 16 GiB; the placement is statically infeasible. Two workers use $2(5)+2=12$ GiB and leave 4 GiB within the model. Actual safety still depends on demand accuracy, limits, burst, and other workloads.

**Conclusion.** Capacity inequalities reject impossible placements but do not predict runtime behavior.

### Example 4

**Situation.** A 150 ms request budget crosses client edge, application, and database paths.

**Reasoning.** Allocate 35 ms edge-to-app, 55 ms application work, 40 ms database round trip, and 20 ms margin: $35+55+40+20=150$ ms. Moving the application to another region adds an estimated 45 ms to the database path, violating the budget unless work, data, or response semantics change. These are allocations pending measurement.

**Conclusion.** Deployment and data locality constrain achievable latency budgets.

### Example 5

**Situation.** A stateful worker using a locally attached volume is rescheduled to another node after failure.

**Reasoning.** The new node can run the artifact but cannot see the old local volume. Recovery must attach a replicated volume, restore a checkpoint, replay a durable log, or declare the local state disposable. Placement eligibility must include storage topology and recovery time, not CPU compatibility alone.

**Conclusion.** Executable portability does not imply state portability.

### Example 6

**Situation.** A rolling update replaces four server instances one at a time while clients remain on two versions.

**Reasoning.** During transition, old clients call new servers and new clients call old servers. The deployment view adds mixed-version paths, minimum serving capacity, readiness gates, drain, and rollback. A destructive schema migration before the compatibility window closes can make rollback impossible.

**Conclusion.** Deployment transitions are configurations with distinct compatibility and capacity obligations.

### Example 7

**Situation.** A tag `payments:stable` moves from image digest `d1` to `d2`; one node has a stale cache.

**Reasoning.** A deployment recorded only by tag cannot establish which content runs. Bind desired instances to digest `d2`, verify platform compatibility and signature policy, and observe runtime image identity. The stale node running `d1` is drift even though its tag text matches.

**Conclusion.** Mutable locators are insufficient for artifact identity and conformance.

### Example 8

**Situation.** Workloads are isolated by network policy, but a shared deployment controller can mount every secret.

**Reasoning.** The data-plane paths appear restricted, yet controller compromise can alter artifacts, identities, and secret delivery across workloads. Show the administrative trust zone, credential scope, admission policy, audit path, and break-glass controls. Reduce privileges or split authority where the threat model requires it.

**Conclusion.** Control-plane placement and authority can dominate data-plane isolation.

### Example 9

**Situation.** Application instances keep serving when the scheduler control plane becomes unreachable.

**Reasoning.** Existing data-plane work may continue, but failed instances cannot be replaced, desired changes cannot be reconciled, credentials may not rotate, and scale-out may stop. The deployment view separates current-serving behavior from management and recovery capability and defines a maximum safe control-plane isolation interval.

**Conclusion.** Control-plane failure can preserve current traffic while degrading change and recovery.

### Example 10

**Situation.** A remote flood-warning station has intermittent satellite connectivity, solar power, local sensors, and a siren.

**Reasoning.** Place signed firmware, local rules, sensor acquisition, bounded storage, monotonic operation log, and alarm control on the station. Place fleet analytics and update approval centrally. Model power reserve, physical tampering, stale configuration, offline alarm authority, store-and-forward telemetry, safe update rollback, and later reconciliation. A central service timeout must not suppress locally justified warning.

**Conclusion.** Edge deployment views must cover physical resources, offline authority, security, update, and reconciliation.

## Cross-Program Connections

- **Platform Engineering:** schedulers, workload abstractions, policies, and developer platforms implement placement constraints.
- **Cloud Engineering:** regions, zones, managed services, elasticity, shared responsibility, and cost specialize cloud deployment.
- **Systems Engineering:** physical environments, devices, power, hazards, maintenance, and assurance bound whole-system placement.
- **Operating Systems:** processes, virtual memory, isolation, filesystems, scheduling, and devices implement execution environments.
- **Computer Architecture:** instruction sets, memory hierarchy, accelerators, and NUMA determine hardware compatibility and performance.
- **Networks:** routing, addressing, bandwidth, loss, segmentation, and control planes determine deployed communication paths.
- **Security:** workload identity, isolation, artifact integrity, secrets, administration, and physical exposure shape trust.
- **Software Delivery and Reliability Engineering:** build provenance, rollout, observability, incident response, and recovery supply evidence.
- **Database Engineering:** storage topology, durability, replication, consistency, backup, and restore determine state placement.

## References

1. ISO/IEC/IEEE, *ISO/IEC/IEEE 42010:2022 Software, systems and enterprise — Architecture description*, 2nd ed., November 2022. Official catalogue; current edition checked 2026-09-06. https://www.iso.org/standard/74393.html
2. Object Management Group, *OMG Unified Modeling Language (OMG UML), Version 2.5.1*, formal/2017-12-05, December 2017, Clause 19, Deployments. Official specification and current formal version checked 2026-09-06. https://www.omg.org/spec/UML/2.5.1/PDF
3. Paul Clements et al., *Documenting Software Architectures: Views and Beyond*, 2nd ed., Addison-Wesley, 2010.
4. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021.
5. Open Container Initiative, *OCI Image Format Specification*, Standards Track, published November 2025. Current specification checked 2026-09-06. https://specs.opencontainers.org/image-spec/
6. Open Container Initiative, *OCI Runtime Specification*, Standards Track, published November 2025. Current specification checked 2026-09-06. https://specs.opencontainers.org/runtime-spec/runtime/
7. Kubernetes Authors, “Pod Topology Spread Constraints,” official documentation. Retrieved 2026-09-06. https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/
8. National Institute of Standards and Technology, *Application Container Security Guide*, NIST SP 800-190, September 2017. https://doi.org/10.6028/NIST.SP.800-190
9. Brendan Burns, Joe Beda, Kelsey Hightower, and Lachlan Evenson, *Kubernetes: Up and Running*, 3rd ed., O’Reilly Media, 2022.

## Exercises

### Exercise 1

Precisely distinguish a source module, deployable artifact, deployment unit, execution environment, runtime instance, node, location, and failure domain. Give one many-to-many relationship among them.

### Exercise 2

Nodes $n_1$ and $n_2$ each provide 12 GiB memory. Each needs 2 GiB reserve. Replicas $r_1,r_2,r_3$ each demand 4 GiB, and $r_1$ and $r_2$ must occupy different host failure domains. Determine feasible placements and remaining modeled headroom.

### Exercise 3

Diagnose a deployment with four replicas across two zones where all persistent volumes, DNS, and workload identities depend on one regional control service. Which claims are supported by replica spread, and which are not?

### Exercise 4

Compare exact static placement with scheduler-constrained placement for a payment service. Address capacity, locality, failure separation, rollout, drift, observability, and emergency operation.

### Exercise 5

Transfer the method to a small Earth-observation satellite fleet. Design deployment views for signed flight software, onboard compute, ground stations, delayed communication, limited power and storage, safe mode, staged update, rollback, and fleet-version reconciliation.

## Answers to the Exercises

### Answer 1

A **source module** organizes implementation code. A **deployable artifact** is an immutable built unit. A **deployment unit** is the artifact set independently released or rolled back. An **execution environment** supplies runtime services. A **runtime instance** is one execution of artifact behavior. A **node** hosts environments or artifacts. A **location** describes physical, network, jurisdictional, or administrative placement. A **failure domain** groups resources exposed to one concern-specific common cause.

Relationships are not one-to-one. One artifact can create many instances; one instance can load several artifacts; one node hosts many environments; one deployment unit can contain several components; and one logical component can be realized by several artifacts.

### Answer 2

Usable modeled capacity per node is $12-2=10$ GiB. Two 4 GiB replicas fit on one node with 2 GiB headroom; three do not because $3(4)+2=14>12$ GiB. A feasible placement puts $r_1$ on $n_1$, $r_2$ on $n_2$, and $r_3$ on either node. The chosen node then uses $2(4)+2=10$ GiB and has 2 GiB total capacity unallocated; the other uses $4+2=6$ GiB and has 6 GiB unallocated.

The separation rule for $r_1,r_2$ holds only if $n_1,n_2$ are distinct qualified host domains. This static result says nothing about CPU, burst memory, interference, failover capacity, or shared dependencies.

### Answer 3

The spread supports a narrow claim: loss of one qualified zone need not remove every compute replica, assuming routing reaches survivors. It does not establish service availability. The one regional control service remains a common dependency for volumes, name resolution, and identities. Its failure may make data unavailable, prevent discovery, block authentication, stop replacement, or prevent recovery even while processes run.

Document current-serving and recovery behavior separately. Either remove the common cause through independently recoverable data, identity, DNS, and control paths, or narrow the availability claim and define degraded behavior, maximum isolation time, recovery ownership, and evidence.

### Answer 4

Exact placement names hosts and is predictable for licensing, fixed appliances, tightly coupled devices, and some audited environments. It can encode locality and separation directly, but host loss or maintenance needs explicit reassignment and it can waste capacity. Every change risks configuration drift.

Scheduler constraints declare eligible pools, resources, affinity, topology separation, disruption policy, and priorities. They adapt to failure and scaling, but actual placement varies and requires observation. Constraints can be unsatisfiable, use incorrect labels, or degrade after removal. Payment state locality, immutable artifact identity, workload authority, and failover reserve remain explicit in either design.

A sound comparison models normal placement, rollout overlap, zone loss, control-plane isolation, and emergency intervention. Exact placement needs validated replacement procedures; scheduled placement needs constraint validation, placement evidence, and a bounded plan for loss of scheduling. Neither approach alone proves capacity, integrity, or availability.

### Answer 5

Use flight-computer hardware, redundant storage, power subsystem, radios, sensors, actuators, ground stations, update authority, and mission-control services as nodes or external resources at appropriate resolution. Bind flight software, bootloader, configuration, and models to signed immutable identities with processor, memory, sensor, and boot compatibility. Each spacecraft has an observed version and health state; the fleet view records variation intentionally.

Onboard placement reserves compute, memory, storage, and energy for control and safe mode before payload processing. Logs and observations use bounded storage and priority-aware deletion. Commands carry spacecraft, operation, version, validity, and replay-resistant identity. Loss of ground contact leaves explicitly bounded onboard authority; stale commands are rejected.

Stage an update to a qualified subset, verify boot, control, power, communications, and telemetry, then expand. Preserve a known-compatible rollback image and configuration in protected storage, but recognize that irreversible state or hardware changes can limit rollback. Ground-station diversity must include geography, spectrum, network, identity, and operator common causes. After delayed contact, reconcile commands, installed digests, configuration, safe-mode entries, and physical effects without assuming fleet uniformity. Acceptable alternatives must preserve power safety, authenticated control, immutable evidence, delayed-operation semantics, and recovery ownership.
