---
module_id: PLAT-008
program: Platform Engineering
level: 1
module_number: 8
title: Internal Platforms and External Cloud Services
status: complete
last_verified: 2026-09-02
---

# Internal Platforms and External Cloud Services

## One-Page Review

### Governing question

How can an internal platform compose external cloud services into a coherent product without confusing provider operation with organizational accountability, hiding consequential provider semantics, or creating an untested dependency and exit boundary?

### Essential definitions

- An **internal platform** is defined by its bounded organizational consumers and accountable product contract, not by whether its implementation runs on premises or was written by employees.
- An **external cloud service** is a provider-operated capability consumed across an organizational boundary under technical, operational, commercial, legal, and lifecycle terms.
- A **provider adapter** translates platform intent, state, errors, identity, policy, evidence, and lifecycle operations to one provider contract. It is not automatically a portable abstraction.
- **Shared responsibility** allocates distinct duties among provider, platform team, workload team, and other authorities. “Shared” is incomplete unless decision, execution, evidence, escalation, and recovery are assigned.
- **Residual responsibility** is an obligation the organization retains even when a provider performs part of the work—for example data classification, access decisions, lawful use, workload design, or acceptance of risk.
- **Provider exposure** is the provider detail a consumer must know because it changes compatibility, cost, data location, failure behavior, or an owned decision.
- **Exit readiness** is evidenced ability to stop or replace a service while preserving required data, identity, operation, audit, and deletion outcomes within stated bounds.

### Central model, mechanism, or theorem

Represent an external service as $E=(F,Q,A,D,C,L,X)$: functions $F$, qualities and limits $Q$, responsibility allocation $A$, data behavior $D$, commercial terms $C$, lifecycle $L$, and exit contract $X$. The internal platform composes one or more such services behind a consumer contract $P=(U,J,I,O,S,G,R,V)$ for users $U$, jobs $J$, intent $I$, outcomes $O$, states $S$, guarantees $G$, responsibilities $R$, and evidence $V$. Delegating mechanisms can reduce work, but it does not erase any responsibility promised by $P$ or retained by the organization.

### Critical invariants

- Every consumer-visible promise has an accountable internal owner and provider evidence sufficient to support it.
- Responsibility is assigned per service, configuration, lifecycle state, and failure mode; service-model labels alone are not accepted as contracts.
- The platform exposes provider facts whenever they change a consumer-owned decision or material risk.
- Provider status, platform status, and workload status remain distinguishable and are correlated through stable identifiers.
- Quotas, regions, identity, data handling, support, cost, change, deprecation, recovery, and deletion are part of integration—not procurement footnotes.
- Portability claims name the exact artifact, behavior, target, cost, and tested recovery objective.
- An exit plan includes rehearsal evidence and authoritative deletion, not only an export format.

### Common failures

Calling a vendor console an internal platform; treating “managed” as “no customer operation”; repeating a generic shared-responsibility diagram without service-level ownership; hiding provider limits behind a leaky lowest-common-denominator API; promising multi-cloud without testing a second target; coupling identity and audit irreversibly to one account hierarchy; ignoring quotas, commitments, egress, deprecation, and support; and discovering during an outage that nobody owns coordination or consumer communication.

### Compact example

An internal database capability accepts owner, data class, region, recovery objectives, and compatibility profile. A cloud provider operates hosts, storage machinery, and database binaries. The platform team provisions approved configurations, binds workload identity, verifies backups, normalizes lifecycle state, monitors provider notices, coordinates incidents, allocates cost, and rehearses export and restore. The application team owns schema, query behavior, data minimization, client retries, and recovery validation. The data authority owns classification and retention. The provider is external; the capability remains an accountable internal product.

### Connections

Retrieve capability-versus-provider separation from [PLAT-007](007-platform-capabilities-versus-tool-catalogs.md), road and escape ownership from [PLAT-006](006-paved-roads-and-escape-hatches.md), and product lifecycle from [PLAT-004](004-platform-as-product.md). The next module defines [platform team boundaries](../roadmap.md#block-01--platform-engineering-foundations). Later modules own service brokering, identity, multi-tenancy, reliability, dependency mapping, regional design, cost allocation, build-versus-buy, and capability retirement in depth.

## Governing Question

Which parts of an internal platform should be implemented by external cloud services, which responsibilities must remain inside the organization, and how should the platform translate the boundary so that consumers receive a coherent and truthful contract?

“Internal” and “external” describe different dimensions. Internal identifies the platform's product audience and organizational accountability. External identifies an implementation and control boundary. A platform can be internal while composing public-cloud compute, managed databases, identity services, source control, observability, or software-as-a-service. Conversely, software operated on the organization's own infrastructure is not automatically an internal platform; it may lack a user-centered product contract entirely.

The design problem is therefore not where the machines sit. It is how responsibility, authority, evidence, failure, change, cost, data, and exit cross several independently operated systems. A sound platform takes responsibility for the consumer experience it promises while preserving provider facts that consumers and organizational authorities genuinely need.

## Why This Matters

External services can transfer undifferentiated operation to specialists, provide rapid capacity, expose mature capabilities, and shorten platform delivery. Current CNCF platform guidance explicitly allows capability providers to be internal teams or third parties and recommends using existing managed providers where they fit. NIST's cloud definition grounds the familiar service models in on-demand self-service, resource pooling, elasticity, network access, and measured service. These properties can supply powerful substrate for an internal product.

Transfer is never total. Cloud providers operate particular layers and publish particular promises; customers still choose configurations, identities, data, workload architecture, regions, recovery, use, and risk. Current Azure guidance, for example, shows responsibility shifting across IaaS, PaaS, and SaaS while customer data, accounts, and access decisions remain customer concerns. Its reliability guidance also separates core provider reliability from provider-offered reliability features that customers must select and use, and from application reliability. AWS similarly states that its responsibility covers security of its cloud infrastructure while customer duties depend on the services selected and their use.

An internal platform inserts another accountable layer between provider and workload team. It may assume configuration, provisioning, policy, observability, support, upgrade, and recovery duties that would otherwise fall to each workload team. If it only forwards a provider API, it can add failure and ambiguity without reducing meaningful burden. If it hides every provider fact, it can prevent consumers from meeting compatibility, residency, cost, and recovery obligations.

External concentration also changes systemic risk. One provider identity outage, quota, regional failure, API change, commercial dispute, or control-plane defect can affect many platform consumers. Diversifying every service is usually expensive and may make both copies weak. Accepting concentration can be rational, but only as an explicit decision with bounded blast radius, provider evidence, response paths, and recovery or exit choices.

## Prerequisites and Retrieval

Retrieve from PLAT-001 the total-system complexity and central blast-radius model. Retrieve consumer jobs and authorities from PLAT-002, bounded cognitive-load claims from PLAT-003, product evidence and lifecycle from PLAT-004, self-service state and guardrails from PLAT-005, road and escape ownership from PLAT-006, and capability/provider separation from PLAT-007.

You should understand cloud service and deployment models, APIs, identity, networking, data lifecycle, observability, service objectives, incident response, configuration, procurement, cost, compatibility, backup, restore, and migration. This chapter establishes the product and responsibility boundary; later modules own detailed cloud architecture, platform reliability, and build-versus-buy analysis.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish an internal platform product from its internal and external implementation providers;
2. model an external service beyond its feature list, including qualities, responsibility, data, commercial, lifecycle, and exit terms;
3. allocate provider, platform, workload, and authority responsibilities for normal operation and failure;
4. decide which provider semantics to translate, preserve, or expose to platform consumers;
5. design evidence propagation, incident coordination, provider-change handling, and truthful platform status;
6. bound portability and multi-provider claims with named artifacts, targets, costs, and tests; and
7. evaluate external composition through total lifecycle burden rather than acquisition speed or unit price alone.

## Core Exposition

### Separate product boundary from implementation boundary

An internal platform is a product for a known organizational population. It owns research, interfaces, supported journeys, documentation, support, evidence, change, and retirement. None of those properties requires the platform team to operate every backing mechanism. CNCF guidance describes platforms as bridges between users and capability providers and states that providers can be third parties or other internal teams.

Draw three layers: consumer, internal platform, and provider. The consumer declares domain intent and receives a platform outcome. The platform translates and operates the product contract. The provider supplies one or more underlying services. Other authorities—security, privacy, finance, legal, data governance, incident command—cut across these layers and retain their own decisions.

Do not collapse the platform into a portal over vendor consoles. A coherent platform may deliberately link consumers to a provider-native interface when direct expertise is required, but it must say where its promise ends. Conversely, do not rebuild an external service merely to make the implementation appear internal. Ownership quality, not code provenance, determines whether the platform is real.

### Specify the external service as a dependency contract

Model candidate service $e$ as

$$
E_e=(F,Q,A,D,C,L,X),
$$

where $F$ is functionality and interfaces; $Q$ is performance, availability, durability, quotas, regions, and other limits; $A$ allocates responsibilities and authorities; $D$ covers data location, protection, access, retention, export, and deletion; $C$ covers price, metering, commitments, licenses, support, and termination; $L$ covers versions, changes, deprecations, incidents, and support lifecycle; and $X$ is the migration and exit contract.

A feature comparison covers mostly $F$. Platform fitness depends on the whole tuple. A database can support the required query model yet fail residency, recovery, identity, observability, quota, or export needs. A service can have a strong availability objective while providing no application-level recovery. A cheap unit rate can be dominated by integration, premium support, cross-region transfer, unused commitments, or exit.

Record claims with source, scope, effective time, and verification method. Marketing pages, contractual terms, service documentation, observed tests, audit reports, and incident history are different evidence classes. The platform must not silently upgrade one into another.

### Define the internal platform contract independently

For a platform capability, define

$$
P=(U,J,I,O,S,G,R,V),
$$

where $U$ is eligible consumers and workloads, $J$ jobs, $I$ declared intent, $O$ outcomes, $S$ observable lifecycle states, $G$ guarantees and limits, $R$ responsibility allocation, and $V$ evidence. Map $P$ to one or more provider contracts without making current provider nouns the default consumer language.

The platform may promise less than the provider in order to reserve recovery margin, support heterogeneous implementations, or avoid exposing an unstable feature. It must never promise more without an additional mechanism and evidence. If the provider promises regional service availability but the platform's identity broker is single-region, the end-to-end platform promise is bounded by the broker. If the provider can restore a database but the platform never captures the application-consistent inputs, the capability cannot claim application recovery.

Provider replacement is not required for a useful abstraction. Stable intent, lifecycle state, identity, evidence, and support can reduce consumer burden even when data-plane APIs remain provider-specific. Truthful partial abstraction is better than fictitious portability.

### Allocate responsibility at operational resolution

Generic IaaS, PaaS, and SaaS diagrams are useful orientation, not service contracts. Responsibility changes by selected service, feature, configuration, region, lifecycle state, and incident. Add the platform and workload layers explicitly.

For every material responsibility $r$, allocate five aspects:

$$
A(r)=(d,e,v,c,q),
$$

where $d$ decides, $e$ executes, $v$ verifies, $c$ communicates and coordinates, and $q$ owns recovery or residual risk. These roles may differ. A provider may execute host patching; the platform verifies service notices and coordinates impact; the workload team validates application behavior; a risk authority accepts a temporary exposure.

Avoid the bare label “shared.” It often means no one knows who acts. Assign named roles for identity, configuration, encryption, keys, backups, restore tests, capacity, quotas, telemetry, incidents, support escalation, data requests, retention, deletion, cost, changes, and exit. Revisit the allocation when service tier or feature changes.

The following synthetic checker verifies that a small responsibility register has an accountable decision owner, executor, verifier, coordinator, and recovery owner. It demonstrates schema completeness only; it cannot prove that the chosen owners have authority or capacity.

<!-- bijux-verify: {"id":"cloud-responsibility-register","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"responsibilities=4\nassignments=20\nprovider-executes=2\nplatform-coordinates=4\nconsumer-decides=1\nuncovered=0\n","stderr":""}} -->
```python
register = {
    "host-patching": ("provider", "provider", "platform", "platform", "provider"),
    "service-configuration": ("platform", "platform", "platform", "platform", "platform"),
    "data-retention": ("data-authority", "platform", "platform", "platform", "data-authority"),
    "schema-recovery": ("consumer", "provider", "consumer", "platform", "consumer"),
}

required_positions = 5
uncovered = [name for name, owners in register.items() if len(owners) != required_positions or not all(owners)]
print(f"responsibilities={len(register)}")
print(f"assignments={sum(len(owners) for owners in register.values())}")
print(f"provider-executes={sum(owners[1] == 'provider' for owners in register.values())}")
print(f"platform-coordinates={sum(owners[3] == 'platform' for owners in register.values())}")
print(f"consumer-decides={sum(owners[0] == 'consumer' for owners in register.values())}")
print(f"uncovered={len(uncovered)}")
```

### Translate semantics without concealing consequences

The platform should normalize repetitive mechanics: account placement, naming, identity binding, approved encryption, baseline telemetry, tags, cost attribution, request status, audit links, and routine lifecycle operations. It should expose provider detail when it changes a consumer-owned decision.

Provider exposure commonly includes engine or API compatibility, region and failure domain, consistency semantics, quotas, irreversible features, data location, cost dimensions, recovery limits, maintenance behavior, preview status, and unsupported operations. Expose these as typed capability profiles rather than dumping every provider option into one untestable form.

Separate intent from resolution. A consumer might request a region class, recovery objective, data class, and compatibility profile. The platform resolves those declarations to a provider, region, tier, and configuration, then records the resolution and reasons. If the consumer directly depends on a provider API, record that dependency rather than claiming it is hidden.

### Integrate identity, data, and evidence end to end

External service integration begins before provisioning. Establish organization, account, project, subscription, region, network, identity, key, logging, and billing boundaries. Prefer workload identity and federation over long-lived copied credentials. Define emergency access, revocation, provider support access, and separation of duties.

Trace data through collection, transit, processing, replicas, backups, telemetry, support artifacts, export, retention, and deletion. A provider deletion acknowledgement may not cover backups, derived indexes, logs, or externally copied exports. The platform needs a deletion state model and evidence that matches the actual service contract.

Evidence must remain attributable. Correlate consumer request, platform operation, provider resource, policy decision, configuration version, incident, cost record, and deletion evidence with stable identifiers. Provider logs alone may omit platform intent; platform logs alone cannot prove provider behavior. Preserve clocks, retention, access, and gaps explicitly.

### Engineer provider failure and change

Provider operation can remove host-level toil, but it creates a dependency that the platform must operate. Monitor provider health and notices, yet do not equate a green provider dashboard with a healthy consumer capability. Use synthetic checks and consumer-impact signals. Keep provider, platform, and workload conditions separate so responders know which layer made each claim.

Define incident roles before failure: detection, provider escalation, internal incident command, consumer communication, technical mitigation, recovery validation, evidence retention, and review. Provider support response is an input to the platform response objective, not the same promise. Test degraded provider APIs, throttling, stale status, region loss, identity failure, delayed support, partial recovery, and inconsistent deletion.

Provider changes include new defaults, API versions, pricing, quotas, regions, certificates, root authorities, maintenance, feature retirement, ownership changes, and contract termination. Ingest notices into an owned change workflow. Inventory affected resources, test compatibility, communicate impact, migrate within a bounded window, and verify completion. Email sent to an unowned account is not a lifecycle system.

### Make portability a bounded claim

“Portable” must identify what moves. Source code may be portable while identity, data, network, telemetry, policy, and operating procedures are not. A container image does not make a stateful system portable. An infrastructure declaration may reproduce resources while losing managed-service semantics or historical evidence.

Specify a portability claim as

$$
X=(a,s,t,\tau,\kappa,\delta,v),
$$

where $a$ is the artifact or state, $s$ source, $t$ target, $\tau$ maximum elapsed time, $\kappa$ acceptable cost and effort, $\delta$ tolerated data or behavior difference, and $v$ verification evidence. A claim without a named target and rehearsal is a design intention.

Use provider-neutral intent where it reduces real burden, but retain provider profiles for meaningful differences. Supporting two providers doubles neither reliability nor freedom automatically. It introduces adapter behavior, conformance tests, operational skills, routing, data replication, support, and weakest-common-contract pressures. Choose multiple providers only for evidenced regulatory, market-access, acquisition, resilience, bargaining, or product needs.

### Design exit as a lifecycle operation

Exit may mean replacing a service, moving a workload, separating a business unit, responding to provider termination, or retiring the capability. Inventory data, schemas, identity, configuration, keys, dependencies, certificates, network names, policies, logs, evidence, commitments, and consumers. Define export consistency, validation, dual-run or outage, cutover, rollback, retained records, revocation, deletion, and financial closeout.

Rehearse the risky path. Small sample exports do not prove production throughput or application-consistent recovery. Measure export rate, transformation, target import, verification, cutover, rollback, egress charge, staff effort, and deletion delay. If full rehearsal is too costly, state the residual uncertainty and test components on a justified schedule.

Avoid both extremes. Building every service internally to avoid dependency can consume vast effort and produce weaker operation. Adopting a service with no exit work can be rational for low-consequence, replaceable use. Match exit investment to criticality, irreversibility, concentration, contract horizon, and plausible triggers.

### Evaluate total lifecycle burden

Compare options using total burden, not license price or implementation headcount:

$$
B_{total}=B_{acquire}+B_{integrate}+B_{operate}+B_{assure}+B_{change}+B_{incident}+B_{exit}+B_{consumer}.
$$

External services can reduce $B_{operate}$ for underlying machinery while increasing integration, assurance, commercial, incident-coordination, and exit burden. Internal implementation can increase engineering and operational burden while providing authority, fit, or evidence unavailable externally. Estimates should include uncertainty and concentration rather than pretending the terms are precise independent numbers.

Evaluate value as well: lead time, capability depth, reliability, global reach, elasticity, expertise, and opportunity cost. Segment by workload class. One provider may be excellent for ordinary stateless services and unacceptable for a legally constrained or latency-critical workload. Preserve an independent path when the platform contract does not fit.

## Definitions and Notation

Let $U$ denote platform consumers, $J$ their jobs, $P$ an internal platform capability, and $E$ an external service. $E=(F,Q,A,D,C,L,X)$ captures functions, qualities, responsibility, data, commercial terms, lifecycle, and exit. $P=(U,J,I,O,S,G,R,V)$ captures the consumer contract. Mapping $m:P\to 2^E$ associates a capability with one or more services; it does not make provider behavior identical.

For responsibility $r$, $A(r)=(d,e,v,c,q)$ assigns decision, execution, verification, coordination, and recovery or residual-risk ownership. A complete tuple is necessary but not sufficient: each owner also needs authority, capability, evidence, and a reachable escalation path.

$X=(a,s,t,\tau,\kappa,\delta,v)$ bounds a portability or exit claim by artifact, source, target, time, cost/effort, tolerated difference, and verification. $B_{total}$ is an accounting frame for acquisition, integration, operation, assurance, change, incident, exit, and consumer burden; it is not a universal optimization theorem.

## Mechanisms, Invariants, or Proof Structure

Use a provider onboarding gate. First validate the consumer job and platform fit. Then review the complete $E$ tuple, create the $A(r)$ register, map provider states and errors to $P$, integrate identity/data/evidence, exercise failure and recovery, establish change ingestion, quantify cost, and test an exit slice. Approve only the claims supported by evidence.

Maintain three linked records: the consumer-facing capability contract, the provider dependency contract, and the responsibility register. A provider change triggers impact analysis against all three. A platform change cannot silently transfer responsibility to consumers; a provider change cannot silently weaken a platform guarantee.

The central invariant is accountability conservation: delegation can change who executes a mechanism, but every platform promise and residual organizational obligation retains an accountable owner. This is an engineering rule, not a claim that responsibility is mathematically conserved. It prevents “the provider manages it” from ending analysis before configuration, evidence, recovery, and consumer communication have owners.

Review boundary cases: provider healthy/platform broken; provider broken/platform status stale; control plane unavailable/data plane serving; service restored/data inconsistent; export successful/target unusable; resource deleted/backups retained; contract valid/region prohibited; two providers available/identity dependency shared. These cases reveal hidden coupling better than a happy-path provisioning demo.

## Alternatives and Trade-Offs

**Provider-direct use** preserves provider capability and speed for expert teams. It gives each team integration, governance, support, cost, and lifecycle duties. Prefer it for specialist or independently owned work, with cross-cutting organizational obligations explicit.

**Thin enablement** supplies accounts, identity, network, billing, approved configurations, and guidance while leaving service operation with workload teams. This can be more honest and valuable than an abstract API when domains require provider expertise.

**Platform-managed provider composition** offers a stable internal outcome and assumes integration and operational duties. It reduces repeated burden when the platform has authority and capacity. It also concentrates blast radius and requires sustained lifecycle ownership.

**Internally operated implementation** can satisfy unusual control, latency, sovereignty, compatibility, or economic needs. It assumes engineering, capacity, security, reliability, support, and upgrade burden that a provider might otherwise carry.

**Multi-provider composition** may reduce a selected dependency or satisfy placement requirements, but it adds adapter divergence, skills, testing, cost, data movement, and coordination. Active-active, active-passive, portable-at-rebuild, and procurement optionality are different products; name the one actually delivered.

**Managed platform product** may replace part of the internal platform surface. It can accelerate delivery, but the organization still owns consumer fit, integration, retained responsibilities, evidence evaluation, commercial exposure, and exit. Buying a platform does not buy away internal product judgment.

## Failure Modes and Misconceptions

- **“Internal means self-hosted.”** Internal identifies audience and accountability; implementation locality is separate.
- **“Managed means no operations.”** Provider operation changes the work. Configuration, integration, monitoring, incident coordination, recovery validation, cost, change, and exit remain.
- **“The provider SLA becomes our SLO.”** End-to-end experience includes platform and workload dependencies, exclusions, detection, response, and recovery.
- **“Shared responsibility means both teams own it.”** Without named decision, execution, verification, coordination, and recovery roles, it often means neither acts.
- **“Abstraction requires hiding the provider.”** Consequential differences must remain visible to the party that owns the decision.
- **“One API makes it portable.”** Data, semantics, identity, networks, evidence, skills, and operations may remain coupled.
- **“Multi-cloud removes lock-in.”** It can merely move coupling into a custom control plane while doubling weakly operated surface.
- **“Export equals exit.”** Exit includes consistent state, target restoration, cutover, validation, rollback, retained evidence, revocation, deletion, and commercial closure.
- **“Provider green means platform healthy.”** Provider status is only one signal; the platform must observe its own consumer journey.
- **“Cheaper units mean lower cost.”** Commitments, idle capacity, egress, support, integration, incidents, and consumer burden can reverse the comparison.

## Worked Examples

### Example 1

A platform wraps a managed relational database. It keeps provider-native SQL compatibility explicit because applications own query and driver behavior, while normalizing requests, identity, encryption, backups, telemetry, status, cost tags, and deletion. This is a useful partial abstraction: stable organizational intent without pretending engines are interchangeable.

### Example 2

A team uses virtual machines through a platform. The cloud provider operates facilities, physical hosts, and virtualization. The platform owns approved images, account placement, network baseline, identity binding, patch orchestration, inventory, and support coordination. The workload team owns application code and application recovery. Labeling the service “IaaS” alone would not reveal this internal split.

### Example 3

A SaaS source-control provider operates application infrastructure. The platform integrates federation, group synchronization, repository policy, audit export, billing, and offboarding. Engineering teams own repository content and branch decisions; security owns scoped policy; records authorities define retention. The service is highly managed yet still requires an internal operating product.

### Example 4

A provider reports a regional database incident. The platform's synthetic transaction also fails, but its data plane remains partially available. Platform status states `provider_degraded`, affected capability profiles, last successful verification, and known consumer impact. It does not translate the provider page directly into `platform_down` or `healthy`.

### Example 5

A global identity provider backs several platform capabilities. Adding a second compute provider does not remove this shared dependency. Dependency analysis identifies identity, DNS, source control, and the platform control plane as correlated edges. The organization chooses resilient cached workload credentials and a tested emergency path instead of claiming provider diversity solved concentration.

### Example 6

A managed message service introduces a new default retention policy. The provider notice enters a change workflow, which inventories affected topics, compares the platform contract, tests behavior, communicates cost and deletion implications, applies explicit settings, and verifies them. An email to the original account creator would have been insufficient lifecycle ownership.

### Example 7

A platform claims database portability. Its bounded claim covers logical schema and application-owned data from provider A to a named engine on provider B within eight hours for a tested size, with a documented difference in extensions. Identity, monitoring history, and provider-specific procedures are explicitly excluded. The narrower claim is more useful than “cloud agnostic.”

### Example 8

A research team needs a specialized accelerator available from one provider. Rather than forcing it through the standard runtime API, the platform offers thin enablement: account vending, data-class controls, budget, identity, audit, and an owned support boundary. The research team retains accelerator/runtime tuning and reproducibility duties.

### Example 9

A provider-direct object store is inexpensive per unit, but a regulated workload requires private connectivity, dedicated keys, long audit retention, premium support, cross-region replication, restore testing, and verified deletion. Total lifecycle analysis shows that an internally operated alternative remains more expensive, but the decision margin is far smaller than the storage-rate comparison suggested.

### Example 10

An organization retires a hosted build service. It exports repository bindings, build definitions, secrets references, attestations, logs, and retention metadata; recreates identity and runners; dual-runs representative builds; verifies artifact equivalence and provenance; cuts over; revokes provider access; and tracks provider deletion. Successful source export was only the first exit step.

## Cross-Program Connections

Cloud and infrastructure architecture owns regions, accounts, networks, compute, storage, and provider topology; platform engineering owns how those choices become coherent consumer capabilities. API engineering owns interface semantics while the platform owns the product journey and provider adapters. Security engineering supplies identity, control, evidence, and risk mechanisms without replacing workload, platform, or data authority.

Reliability engineering contributes dependency mapping, objectives, incident response, recovery, and failure testing. FinOps contributes allocation, unit economics, commitments, forecasting, and anomaly evidence. Data engineering clarifies schema, lineage, retention, replication, and migration. Procurement and legal functions own contractual and commercial authority, but platform engineers must translate technical consequences into their decisions.

Systems engineering supplies boundary, interface, feedback, emergent-risk, and lifecycle reasoning. Organizational design clarifies which teams can decide, execute, verify, coordinate, and accept residual risk. The model also transfers beyond cloud: an internal clinical platform composing laboratory vendors or a municipal platform composing payment providers faces the same accountability-conservation and exit questions.

## References

- CNCF TAG App Delivery, [*CNCF Platforms White Paper*](https://tag-app-delivery.cncf.io/whitepapers/platforms/), 2023. Current platform definition, external and internal capability providers, provider composition, thinnest reasonable layers, secure defaults, and internal platform-team responsibilities.
- CNCF TAG App Delivery, [*Platforms Working Group Glossary*](https://tag-app-delivery.cncf.io/wgs/platforms/glossary/), current version retrieved 2026. Current definitions of platforms, platform capability providers, platform qualities, provider abstraction, and provider origin.
- NIST, [SP 800-145 — *The NIST Definition of Cloud Computing*](https://csrc.nist.gov/pubs/sp/800/145/final), 2011. Stable baseline for essential cloud characteristics, IaaS/PaaS/SaaS service models, and public/private/community/hybrid deployment models; the taxonomy is descriptive rather than a service-specific responsibility contract.
- NIST, [SP 500-322 — *Evaluation of Cloud Computing Services Based on NIST SP 800-145*](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.500-322.pdf), 2018. Evaluation method for determining whether service claims satisfy the NIST cloud characteristics and models.
- Microsoft, [*Shared Responsibility in the Cloud*](https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility), current documentation retrieved 2026. Current responsibility allocation across on-premises, IaaS, PaaS, and SaaS, including retained customer responsibilities.
- Microsoft, [*Shared Responsibility for Reliability*](https://learn.microsoft.com/en-us/azure/reliability/concept-shared-responsibility), current documentation retrieved 2026. Current distinction among core provider reliability, customer-selected reliability-enhancing capabilities, and application reliability.
- Amazon Web Services, [*AWS Security Documentation: Shared Responsibility Model*](https://docs.aws.amazon.com/security/), current documentation retrieved 2026. Current provider/customer distinction between security of the cloud and security in the cloud, qualified by selected services.
- DORA, [*Platform Engineering*](https://dora.dev/capabilities/platform-engineering/), updated January 12, 2026. Current user-centered platform-product, workflow, self-service, cognitive-load, and balanced-outcome guidance.

## Exercises

### Exercise 1

Create a responsibility register for a managed database capability covering host patching, engine upgrades, service configuration, schema migration, identity, backups, restore validation, incidents, retention, deletion, and cost. Assign decision, execution, verification, coordination, and recovery ownership.

### Exercise 2

Evaluate an internal platform that exposes the raw console and API of one cloud provider through single sign-on. Decide whether it is provider-direct access, enablement, or a platform-managed capability, and specify the smallest honest product improvement.

### Exercise 3

Write a bounded portability claim for moving a stateful service between two named targets. Include artifacts, semantics, identity, data, evidence, time, cost, tolerable differences, validation, cutover, rollback, and deletion.

### Exercise 4

A provider control plane is unavailable while existing data-plane resources continue serving. Design platform state, consumer communication, allowed operations, emergency actions, and recovery verification without turning provider status into the platform's only truth.

### Exercise 5

Transfer the model to a municipal benefits platform that composes an external identity service, payment processor, document store, and notification provider. Identify retained public authorities, provider/platform boundaries, correlated failures, and exit evidence.

## Answers to the Exercises

### Answer 1

One defensible allocation is: provider decides and executes physical-host patching, while the platform verifies provider evidence and coordinates impact. Platform and provider jointly schedule supported engine upgrades; the platform decides the consumer window, executes the platform operation, verifies compatibility, and owns rollback coordination. The platform decides and applies approved service configuration; the application team decides and executes schema migration with platform tooling and validates application behavior. The security authority defines identity policy, the platform binds workload identity, and the application team verifies access. The platform configures and monitors backups; the provider executes storage mechanisms; the application team validates restored data and behavior. Platform incident command coordinates provider escalation and consumers, while application owners validate recovery. Data authorities decide retention; the platform configures and verifies it. Deletion requires platform initiation, provider execution, evidence over replicas/backups, consumer confirmation, and data-authority rules. Finance owns allocation policy, the platform emits attribution, and consumers own budget action. Every “shared” row names the five roles and an escalation.

### Answer 2

Single sign-on plus raw provider interfaces is provider-direct access with useful enablement. It can centralize identity, account placement, and perhaps billing, but it does not by itself define consumer jobs, stable intent, platform lifecycle state, guarantees, support, recovery, or provider translation. The smallest honest improvement is to publish an enablement contract: eligible teams, account and identity behavior, approved regions and configurations, cost ownership, support route, retained workload responsibilities, provider-change notices, offboarding, and evidence. The organization should add a platform-managed capability only for a recurrent job it can operate end to end. Renaming the console or wrapping every API would not create that ownership.

### Answer 3

For example: move logical PostgreSQL schema and application-owned records from a named managed service in region A to a named supported PostgreSQL target in region B for databases up to 2 TB. Preserve documented SQL behavior and recovery point within five minutes; allow listed extension replacements and changed performance within tested bounds. Recreate workload identity through platform declarations rather than exporting provider credentials. Export audit and configuration evidence separately. Complete rehearsed migration within eight hours and a stated labor/egress budget. Validate counts, checksums, constraints, representative queries, authorization, recovery, and application objectives. Use change capture during dual run, freeze writes for bounded cutover, retain source read-only through rollback expiry, then revoke access and obtain deletion evidence under retention terms. This does not claim portability of provider monitoring history or every engine extension.

### Answer 4

Represent at least `provider_control_degraded`, platform reconciliation condition, last observed resource state, data-plane synthetic health, and freshness time. Existing workloads may continue serving; block or queue create/update/delete operations whose outcome cannot be known safely. Preserve read-only inventory from cached evidence with a stale marker. Allow only predeclared emergency operations that do not depend on false state, such as direct credential revocation through an independently tested path or application traffic mitigation. Platform incident command owns provider escalation and gives consumers impact, allowed actions, uncertainty, and update times. After provider recovery, reconcile desired and observed state, detect duplicated or partial operations, verify identity and policy, run consumer-path tests, and only then clear degraded status.

### Answer 5

The municipality retains eligibility policy, lawful-purpose decisions, due process, accessibility, records duties, financial authority, and public accountability. The identity provider proves bounded authentication signals but does not decide benefit eligibility. The payment processor executes transfers under platform-authorized instructions; finance reconciles and handles reversals. The document provider stores and retrieves governed artifacts; records and privacy authorities own classification, retention, disclosure, and deletion rules. The notification provider delivers messages but cannot establish legally effective notice without policy and evidence. The platform owns coherent case identifiers, orchestration, consent and access enforcement, status, evidence correlation, provider escalation, and resident communication. Correlated failures include shared identity, network, DNS, funding accounts, and platform orchestration. Exit evidence includes portable identity links without reusable secrets, payment reconciliation, document integrity and metadata, notification history, target restoration, revoked provider access, retained public records, and verified deletion under lawful schedules.
