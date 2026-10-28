---
module_id: PLAT-009
program: Platform Engineering
level: 1
module_number: 9
title: Platform Team Boundaries
status: complete
last_verified: 2026-09-02
---

# Platform Team Boundaries

## One-Page Review

### Governing question

What should a platform team decide, build, operate, coordinate, and explicitly leave to consumer, provider, enabling, and governing teams so that the platform reduces repeated burden without becoming a central queue, universal owner, or detached infrastructure authority?

### Essential definitions

- A **team boundary** is a reviewed allocation of mission, decisions, capabilities, responsibilities, interactions, dependencies, and lifecycle ownership—not merely a reporting line.
- A **platform team** owns an internal product that helps defined consumers perform recurring jobs through coherent, supported capabilities.
- A **stream-aligned team** owns an end-to-end flow of change and its domain outcomes. Platform use does not transfer application or business-domain accountability.
- A **capability provider team** builds or operates a backing service offered through the platform; it may be internal or external and need not own the platform experience.
- An **enabling team** temporarily helps another team acquire capability, discover obstacles, or improve practice without becoming the permanent executor.
- A **governing authority** has legitimate decision rights for policy, risk, finance, privacy, records, safety, or another obligation; the platform may automate its rules but does not acquire its mandate.
- A **team interaction mode** states why two teams interact and whether the intended relationship is time-bounded collaboration, low-coordination service consumption, or temporary facilitation.
- A **boundary debt** is a recurring mismatch among responsibility, authority, knowledge, capacity, and system interfaces that creates waits, handoffs, shadow ownership, or unsafe gaps.

### Central model, mechanism, or theorem

Define a platform-team boundary as $B=(M,U,C,D,R,I,E,L)$: mission $M$, consumers $U$, owned capabilities $C$, decision rights $D$, responsibility contracts $R$, interaction modes $I$, evidence $E$, and lifecycle $L$. Place a decision with a team only when it has legitimate authority, relevant context, execution capability, feedback from consequences, and lifecycle capacity. Treat the boundary as a product hypothesis that evolves with work and evidence, not as a permanent component inventory.

### Critical invariants

- Every capability, decision, incident role, change path, and retirement action has one accountable owner, even when execution is federated.
- Platform ownership does not absorb consumer domain truth, application behavior, provider internals, or independent policy authority.
- Routine platform consumption is available through a supported product contract rather than personal access to platform engineers.
- Collaboration and facilitation name a purpose, participants, time horizon, success evidence, and exit condition.
- Provider teams can evolve their internals without breaking the platform contract; the platform can evolve its experience without silently transferring work downstream.
- Consumers can identify where the platform promise ends, who owns the next boundary, and how to escalate a gap.
- Boundary changes preserve service continuity, state, evidence, and support while responsibility moves.

### Common failures

Renaming an infrastructure queue “the platform team”; making the platform owner of every shared component; centralizing decisions without domain context; distributing execution without authority; using “shared ownership” to avoid accountability; running permanent high-bandwidth collaboration; treating security or SRE as final approval queues; building a single giant platform team for unrelated capabilities; assigning repositories instead of outcomes; and changing an org chart without migrating services, on-call, knowledge, budgets, or consumer contracts.

### Compact example

A deployment platform owns the declaration schema, build/deploy journey, stable states, diagnostics, supported workload classes, provider integration, platform SLO, lifecycle, and consumer support. A runtime provider team owns cluster operation and its service contract. Application teams own code, data, release intent, application objectives, and recovery validation. Security owns policy meaning and exceptions; the platform implements explainable enforcement. The teams collaborate for six weeks to introduce progressive delivery, then return to versioned service interfaces. An incident record names both runtime technical lead and platform consumer-communication lead.

### Connections

Retrieve product scope from [PLAT-004](004-platform-as-product.md), self-service boundaries from [PLAT-005](005-self-service-and-guardrails.md), capability/provider separation from [PLAT-007](007-platform-capabilities-versus-tool-catalogs.md), and external-service responsibility from [PLAT-008](008-internal-platforms-and-external-cloud-services.md). The next module defines the [platform value proposition](../roadmap.md#block-01--platform-engineering-foundations). Later modules own platform architecture, metadata ownership, service brokers, policy, reliability, dependency mapping, support models, and platform monopolies in depth.

## Governing Question

How should an organization place platform responsibilities and team interactions so that stream-aligned teams can deliver domain value independently while the platform remains coherent, operable, user-centered, and small enough to sustain?

A component list cannot answer this question. “The platform team owns Kubernetes, CI, identity, databases, and observability” says little about consumer outcomes, policy authority, incident coordination, or what each provider actually operates. It can also make one team responsible for a collection too large to understand.

The boundary must follow the flow of work and feedback. A team should be able to make and verify the decisions it owns, operate the resulting service through change and failure, and learn from consumers. When authority, knowledge, execution, and consequences sit in different teams, the interface must reunite them or the boundary must change.

## Why This Matters

Platform engineering deliberately redistributes work. It moves repeated integration and operation away from many application teams and into reusable product capabilities. Done well, this reduces coordination and cognitive load. Done poorly, it creates a central dependency through which every delivery change, exception, incident, and approval must pass.

Current CNCF guidance makes the dual relationship explicit: platform teams work with infrastructure and supporting-service providers to create coherent experiences, and with product/user teams to learn whether those experiences meet needs. It identifies user research, roadmapping, advocacy, and interfaces among platform-team jobs while warning that the platform team itself has finite cognitive capacity. The same guidance allows provider teams or managed services to operate backing implementations.

Team Topologies supplies a useful interaction vocabulary. Stream-aligned teams own flows of value; platform teams offer an internal product; complicated-subsystem teams hold specialized technical work; enabling teams facilitate learning. Collaboration is high-bandwidth and time-bounded, X-as-a-Service is a stable consumption relationship, and facilitation is temporary help. The vocabulary is a reasoning aid, not permission to relabel an existing silo without changing work.

DORA's current platform guidance treats the platform as a sociotechnical product, warns against ivory-tower, ticket-operations, one-size-fits-all, and central bottleneck patterns, and recommends extensibility because a central team cannot build everything. Google SRE guidance similarly makes service health an operating responsibility that includes monitoring, capacity, incidents, and correcting causes; its engagement guidance shows that scarce specialist teams must bound what they accept. These ideas converge on explicit scope and sustainable ownership.

Without a boundary contract, common work becomes everyone’s problem and therefore no one’s product. Consumers learn platform internals because the platform has no coherent interface. Platform engineers become embedded in every application project. Provider teams change dependencies without consumer impact analysis. Policy teams approve routine cases manually. Incidents bounce among teams. A boundary contract makes these failure paths discussable and testable.

## Prerequisites and Retrieval

Retrieve from PLAT-001 the system boundary and complexity-transfer model. Retrieve consumer segments and decision authorities from PLAT-002, team-relative cognitive load from PLAT-003, product lifecycle from PLAT-004, self-service and exception boundaries from PLAT-005, paved-road ownership from PLAT-006, capability/provider distinction from PLAT-007, and three-layer external-service responsibilities from PLAT-008.

You should understand service ownership, domain boundaries, APIs, support, on-call, incident response, product discovery, cognitive load, dependency management, policy, and organizational change. The chapter uses Team Topologies terminology where helpful but does not require a particular reporting structure or team name.

## Learning Objectives

After completing this module, you should be able to:

1. write a platform-team boundary in terms of mission, consumers, capabilities, decisions, responsibilities, interactions, evidence, and lifecycle;
2. distinguish platform product ownership from provider, consumer, enabling, specialist, and governing-authority ownership;
3. place decisions using authority, context, capability, feedback, and lifecycle criteria;
4. design time-bounded collaboration, service consumption, and facilitation with explicit exit conditions;
5. structure a federated platform grouping without losing one coherent consumer contract;
6. allocate support, incident, change, contribution, and retirement responsibilities across team boundaries; and
7. detect boundary debt through waits, escalations, shadow work, overload, and consumer outcomes.

## Core Exposition

### Define the boundary by mission and consumer outcome

Start with the platform's mission and bounded consumers, not technologies. “Enable eligible application teams to deploy and operate stateless services with governed identity, delivery, and telemetry” can guide ownership. “Own Kubernetes and Jenkins” cannot say which consumer outcome or lifecycle the team accepts.

Model the boundary as

$$
B=(M,U,C,D,R,I,E,L),
$$

where $M$ is mission, $U$ consumer segments, $C$ owned capabilities, $D$ decision rights, $R$ responsibility contracts, $I$ interaction modes, $E$ evidence about flow and outcomes, and $L$ change and retirement. Record explicit non-responsibilities alongside the tuple.

A team boundary is not a claim of isolation. Platform work crosses consumer, provider, security, reliability, finance, and leadership concerns. The boundary identifies stable ownership and the interfaces through which those concerns meet. It should reduce repeated coordination while preserving high-bandwidth collaboration for discovery and exceptional change.

### Separate platform product ownership from implementation ownership

The platform team owns the coherence of the platform product: research, supported journeys, interfaces, capability composition, status semantics, documentation, adoption experience, support entry, cross-capability evidence, product objectives, change, and retirement. It is accountable when the platform contract is confusing or its composed journey fails, even if a provider caused the underlying defect.

A capability provider team owns its service contract, implementation, operation, capacity, reliability, security duties, change, evidence, and escalation. It can be a database, identity, runtime, delivery, telemetry, or cloud team. The platform may consume several providers and should not duplicate their internal expertise without reason.

A stream-aligned consumer team owns its domain decisions, application code and data, declared intent, use of the capability, application-level objectives, incident participation, and validation that platform outcomes fit its product. A platform can automate a database but cannot choose whether a business record is truthful or whether an application recovery is acceptable.

Governing authorities retain policy meaning and exception authority. The platform can turn supported policy into automated decisions and evidence. It must not invent a legal, privacy, security, safety, financial, or records mandate because centralization is convenient.

### Place decisions, not just tasks

For each consequential decision $d$ and candidate owning team $t$, test five conditions:

$$
\operatorname{fit}(d,t)=A_t(d)\land K_t(d)\land C_t(d)\land F_t(d)\land L_t(d),
$$

where $A$ is legitimate authority, $K$ contextual knowledge, $C$ execution capability, $F$ feedback from consequences, and $L$ lifecycle capacity. This is a decision checklist, not a numerical score. A missing term identifies an interface or boundary problem.

For example, an application team has context to choose its recovery objective but may lack authority to waive a records obligation. A security team has policy authority but may lack workload context to choose a release window. The platform can validate declarations and execute controls while preserving those decision rights.

Distinguish deciding, executing, verifying, coordinating, and hearing an appeal or exception. One team need not perform all five, but one accountable decision owner must be visible. RACI-style labels can help communication, yet they do not replace a product contract, execution interface, evidence, or recovery plan.

The following synthetic register checks only that five decision records contain all five roles. It does not prove that the selected teams possess the required authority or competence.

<!-- bijux-verify: {"id":"platform-boundary-register","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"decisions=5\nassignments=25\nunique-deciders=4\nplatform-decides=2\nconsumer-decides=1\nuncovered=0\n","stderr":""}} -->
```python
register = {
    "platform-interface": ("platform", "platform", "platform", "platform", "product-council"),
    "application-release": ("consumer", "consumer", "consumer", "platform", "incident-command"),
    "security-policy": ("security-authority", "platform", "security-authority", "platform", "risk-owner"),
    "provider-upgrade": ("provider", "provider", "platform", "platform", "service-owner"),
    "platform-retirement": ("platform", "platform", "consumer", "platform", "portfolio-owner"),
}

uncovered = [name for name, roles in register.items() if len(roles) != 5 or not all(roles)]
deciders = [roles[0] for roles in register.values()]
print(f"decisions={len(register)}")
print(f"assignments={sum(len(roles) for roles in register.values())}")
print(f"unique-deciders={len(set(deciders))}")
print(f"platform-decides={deciders.count('platform')}")
print(f"consumer-decides={deciders.count('consumer')}")
print(f"uncovered={len(uncovered)}")
```

### Choose an interaction mode deliberately

Use collaboration when teams must discover a boundary, capability, API, operating model, or unfamiliar technology together. It has high bandwidth and interrupts both roadmaps, so define the question, participants, decision owner, duration, artifacts, evidence, and exit. Permanent “collaboration” for every routine change is a dependency, not successful teamwork.

Use X-as-a-Service for steady consumption. The provider publishes a contract, interface, quality, status, support, lifecycle, and feedback channel; the consumer acts without recurring coordination. For a platform, this is the normal target for mature routine journeys. It does not mean interpersonal relationships disappear; it means ordinary work does not require them.

Use facilitation when an enabling team helps another team learn, remove an obstacle, or adopt a practice. Define the capability the recipient should acquire and when the helper exits. If the facilitating team keeps executing the work, it has become a provider or shadow owner.

Interaction modes can change. Two teams may collaborate to discover a deployment contract, consume it as a service after stabilization, and briefly use facilitation for migration. Record the transition rather than treating all cross-team communication as one vague dependency.

### Publish a team-facing contract

A useful team contract—often called a Team API—states:

- mission, consumers, owned outcomes, capabilities, and non-responsibilities;
- interfaces, supported requests, prerequisites, states, service objectives, and limits;
- decisions the team owns and decisions it requires from others;
- providers and dependencies, with normal and incident escalation;
- interaction modes, collaboration entry criteria, and facilitation exit criteria;
- contribution model, review authority, maintenance ownership, and support;
- roadmap, change, compatibility, deprecation, migration, and retirement;
- operating hours, on-call, incident roles, and consumer communication;
- feedback channels and evidence used to review the boundary; and
- team capacity constraints and how unsupported demand is handled.

The contract should be versioned and easy to discover, but it is not a substitute for working interfaces or relationships. A beautiful ownership page with a ticket queue behind every action still creates coordination. An API without a responsible team creates abandonment.

### Design a platform grouping rather than a giant team

A broad platform usually exceeds one small team's cognitive and operational capacity. Current Team Topologies guidance distinguishes a platform grouping from one platform team: several teams can own distinct platform products or capabilities around a shared purpose. Use this shape when a single consumer experience depends on specialized delivery, runtime, data, identity, or observability domains.

Federation requires cohesion. Define a platform product or architecture council only for cross-capability semantics and investment decisions, not as an approval queue. Each provider team owns a bounded service. Shared conventions cover identity, metadata, lifecycle state, errors, telemetry, support routing, compatibility, and change. A product function integrates research and priorities across journeys.

Avoid a portal team becoming the accidental owner of everything it displays. The portal composes views and actions; capability teams remain authoritative for behavior and state. Similarly, a central platform product manager cannot make every domain decision. Product coherence depends on explicit provider contracts and shared evidence, not hierarchical control.

### Allocate support and incidents end to end

Consumers need one intelligible entry point for platform problems. The platform can triage and route without pretending it can repair every provider. Define severity, expected response, information required, status source, handoff acknowledgment, escalation, and closure. Preserve the consumer's case identifier across provider systems.

During an incident, distinguish technical control and consumer accountability. The provider closest to the fault may lead diagnosis and repair. The platform owns impact assessment for its contract, consumer communication, workaround integration, and verification of the platform journey. Application teams own application impact, domain mitigation, and recovery acceptance.

Never bounce a consumer among teams to locate the fault. Internal routing is a platform responsibility when the consumer used the platform contract. Conversely, do not assign every application incident to the platform merely because the application runs there. Evidence should show whether the platform promise, provider service, consumer use, or several layers failed.

### Govern change and contributions

Boundaries are tested by change. A provider must announce breaking changes early enough for the platform to assess and migrate. The platform must not transfer new declarations, operations, or failure handling to consumers without a contract change. Consumers need a route to propose missing capabilities and challenge invalid defaults.

Extensibility prevents central bottlenecks only when contribution ownership is explicit. Define eligible extension types, interface and quality requirements, security and licensing checks, review authority, test evidence, documentation, telemetry, support, compatibility, and retirement. Decide whether the contributor becomes the long-term provider or transfers ownership with capacity and knowledge.

“Open a pull request” is not a contribution model if the platform team must maintain an unbounded set of integrations. A plugin marketplace can distribute creation while centralizing every incident. Count lifecycle ownership, not merged code.

### Evolve boundaries with evidence

Review the boundary when queues, repeated escalations, recurring collaboration, shadow tools, unclear incidents, contribution backlog, provider drift, or overload appear. Segment evidence by consumer and journey. A high ticket count may signal missing self-service, unclear documentation, a defective provider, or a capability outside platform scope.

Measure wait and handoff time, task success, unresolved ownership, escalation depth, support recurrence, interrupt load, on-call burden, roadmap displacement, dependency change failures, consumer workarounds, contribution aging, and recovery. Combine operational evidence with observation and interviews. Low contact can mean excellent self-service or silent abandonment.

Boundary changes require migration. Move authority, people where appropriate, service state, source, access, on-call, budgets, objectives, documentation, consumers, incidents, and knowledge. Run a period of paired operation with an explicit end. An org-chart announcement without transfer mechanics creates nominal ownership and practical orphaning.

## Definitions and Notation

$B=(M,U,C,D,R,I,E,L)$ is a platform-team boundary: mission, consumers, capabilities, decisions, responsibilities, interactions, evidence, and lifecycle. Non-responsibilities constrain $C$, $D$, and $R$ even though they are written as an explicit companion list rather than another tuple element.

$\operatorname{fit}(d,t)=A_t(d)\land K_t(d)\land C_t(d)\land F_t(d)\land L_t(d)$ is a conjunctive checklist for placing decision $d$ with team $t$: authority, contextual knowledge, execution capability, consequence feedback, and lifecycle capacity must all be credible. It is not a measured probability or proof of correct organization design.

For teams $a$ and $b$, an interaction record can be written $I_{ab}=(m,p,h,o,x,e)$: mode $m$, purpose $p$, horizon $h$, owners $o$, exit condition $x$, and evidence $e$. Modes are collaboration, X-as-a-Service, or facilitation. The model describes intended interaction and must be compared with observed work.

## Mechanisms, Invariants, or Proof Structure

Create the boundary from observed journeys. Map consumer work, decisions, waits, providers, failures, and authorities. Cluster repeated undifferentiated work into candidate capabilities. For each candidate, write $B$, explicit exclusions, provider contracts, decision registers, and interaction records. Test ordinary use, change, incident, exception, contribution, and retirement before declaring ownership stable.

The core mechanism is alignment: responsibility must meet authority, knowledge, capability, feedback, and capacity. If a platform team is accountable for recovery but cannot inspect or change the provider, the boundary lacks capability. If it can execute policy but no authority owns policy meaning, the boundary lacks authority. If a central team decides application semantics, it lacks context and feedback.

The accountability invariant requires one visible owner for each contract and decision while allowing federated execution. The autonomy invariant requires routine consumers to act through stable interfaces. The learning invariant requires temporary high-bandwidth modes to produce a durable boundary or capability. The lifecycle invariant requires ownership during change and retirement, not only creation.

Test adversarial cases: a provider fails while the platform is healthy; a consumer misuses a valid capability; policy authorities disagree; a contributor leaves; a platform team reaches on-call saturation; two teams claim the same service; no team accepts an old component; a mandated platform loses voluntary feedback; and a reorganization moves people but not production access. Each case should resolve through named owners and evidence rather than hierarchy alone.

## Alternatives and Trade-Offs

**One centralized platform team** can create early coherence and fast shared decisions. It becomes fragile when capabilities, consumers, and operations exceed its cognitive or on-call capacity. Split by durable capability and consumer boundaries before creating internal queues.

**Federated capability teams** preserve expertise and scale ownership. They can expose inconsistent states, support, and lifecycle. Use shared platform contracts and product evidence without forcing one implementation team.

**Embedded platform engineers** provide rich context during discovery or migration. Permanent embedding can hide a missing product interface and fragment platform priorities. Define purpose, duration, home ownership, outputs, and exit.

**Consumer-owned infrastructure** maximizes local control and can fit specialist domains. It repeats undifferentiated integration and increases operating load. Keep it for independent paths with cross-cutting obligations, or use its repeated pain as platform discovery evidence.

**Central governance gates** provide explicit review for judgment-heavy exceptions. They create waits when deterministic routine cases remain manual. Authorities should define rules and exception criteria; the platform can automate supported decisions while preserving appeal.

**Shared component ownership** can enable cooperation during transition. Long-lived co-ownership obscures roadmap, on-call, and retirement. Prefer one accountable service owner plus explicit contributors and dependent teams.

## Failure Modes and Misconceptions

- **“The platform team owns all infrastructure.”** Platform scope follows consumer jobs and product contracts, not an administrative technology category.
- **“Stream-aligned teams own everything they run on.”** They own domain outcomes but can consume operated platform capabilities without learning provider internals.
- **“Shared ownership improves collaboration.”** It often hides who prioritizes, responds, changes, and retires.
- **“A ticket queue is a team interface.”** A queue can support exceptions; routine delivery through it creates coordination and wait.
- **“Embedding proves customer focus.”** Permanent platform staffing inside consumer teams may conceal a missing product and split ownership.
- **“Security decides platform design.”** Security owns legitimate policy and risk decisions; platform and consumer teams retain product and domain decisions.
- **“SRE owns reliability after handoff.”** Reliability needs service ownership, design authority, feedback, and sustainable engagement, not transfer to a cleanup team.
- **“A portal team owns every displayed capability.”** Presentation composition does not transfer authoritative state or operation.
- **“More contributors remove the bottleneck.”** Without maintenance and support ownership, contribution increases platform load.
- **“Reorganization changes the boundary.”** Production responsibility moves only when authority, access, knowledge, state, capacity, and consumer contracts move.

## Worked Examples

### Example 1

A platform team receives tickets to create every namespace. Its stated boundary says “Kubernetes ownership,” but consumers wait for routine execution. The team changes the mission to a governed environment capability, publishes declarations and states, automates eligible cases, and retains tickets for exceptions. Boundary evidence shifts from ticket closure to successful independent journeys and operator load.

### Example 2

A database platform is backed by three engine teams. The platform owns common intent, identity, provisioning state, evidence, support entry, and retirement. Each engine team owns engine semantics, capacity, upgrades, backups, and technical incident response. Application teams retain schema and recovery validation. The grouping is federated without becoming three unrelated products.

### Example 3

Security authors a workload-identity policy. The platform implements deterministic evaluation and explanations. Application teams declare workload and data context. Security hears exceptions and validates control evidence. The platform does not invent risk acceptance, and security does not manually approve ordinary valid requests.

### Example 4

An enabling team helps five application teams adopt service objectives. The engagement lasts four weeks, produces examples and diagnostic gaps, and ends when each team can define and review an objective. Recurrent tooling needs become platform backlog evidence. The enabling team does not become permanent author of application objectives.

### Example 5

A runtime provider changes an upgrade API. Its provider contract requires advance notice and conformance evidence. The platform team adapts the provider integration while keeping consumer declarations stable, publishes affected conditions, and coordinates migrations. Consumers participate only where application behavior or downtime decisions require their authority.

### Example 6

During a cluster failure, the runtime team leads technical recovery, the platform team owns capability status and cross-consumer communication, and application teams validate domain recovery. One incident commander coordinates priorities. The shared incident does not erase distinct service ownership.

### Example 7

A platform engineer is embedded with a data-science team for six weeks to discover GPU workload needs. The artifact is a workload profile, responsibility map, prototype, and decision that accelerator tuning remains consumer-owned while account, identity, budget, and audit become platform enablement. The engineer returns to the platform team after the exit review.

### Example 8

A portal displays deployment, database, and observability actions. Each capability publishes authoritative state and support. The portal team owns navigation, accessibility, identity of the user session, and composition errors, but not database recovery or telemetry retention. Routing preserves one consumer case while involving the correct provider.

### Example 9

An acquired business has a specialist deployment system. Forcing immediate platform migration would destroy domain knowledge. Teams collaborate to map contracts and risk, then use a time-bounded adapter while deciding whether to migrate, contribute a new provider, or retain an independent path. Acquisition status does not determine technical ownership.

### Example 10

A platform grouping splits one overloaded team into delivery, runtime, and developer-experience teams. The migration transfers repositories, services, access, on-call, budgets, objectives, incident history, and consumer contracts. Paired operation ends after two rehearsed incidents and one change cycle. The split is complete only when consumers can predict the new boundaries.

## Cross-Program Connections

Organizational design supplies authority, incentives, reporting, staffing, and team evolution; platform engineering supplies the internal product and interaction contracts. Domain-driven design helps align application ownership with business context. Systems engineering contributes boundary, interface, feedback, dependency, and lifecycle reasoning.

Reliability engineering contributes service objectives, on-call sustainability, incident command, and operational readiness. Security and privacy engineering supply governing authorities and control expertise without owning every product decision. API engineering makes team boundaries executable through stable interfaces and compatibility. Cloud engineering owns provider topology while platform teams own the consumer-facing composition.

Product management contributes discovery, segmentation, value hypotheses, roadmaps, and retirement. FinOps connects allocation and budget authority to capability use. Socio-technical review must examine affected people: team independence is not valuable if it merely hides unsafe workload, inaccessible processes, or externalized support labor.

## References

- CNCF TAG App Delivery, [*CNCF Platforms White Paper*](https://tag-app-delivery.cncf.io/whitepapers/platforms/), 2023. Current platform-team responsibilities, provider relationships, product partnership, cognitive-load limits, thinnest viable platform guidance, and outcome orientation.
- CNCF TAG App Delivery, [*Platforms Working Group Glossary*](https://tag-app-delivery.cncf.io/wgs/platforms/glossary/), current version retrieved 2026. Current definitions of platform engineering, platform teams, capability providers, platform qualities, and thinnest viable platforms.
- DORA, [*Platform Engineering*](https://dora.dev/capabilities/platform-engineering/), updated January 12, 2026. Current sociotechnical product framing, extensibility guidance, clear-feedback evidence, and central bottleneck, ticket-operations, and ivory-tower failure patterns.
- Matthew Skelton and Manuel Pais, *Team Topologies: Organizing Business and Technology Teams for Fast Flow*, IT Revolution, 2019. Practitioner foundation for stream-aligned, platform, enabling, and complicated-subsystem teams; cognitive load; Team APIs; and interaction modes.
- Team Topologies, [*Key Concepts*](https://teamtopologies.com/key-concepts), current guidance retrieved 2026. Current summary of fundamental team types, platform internal products, stream-aligned ownership, interaction modes, cognitive load, and dynamic boundaries.
- Team Topologies, [*Team Interaction Modeling with Team Topologies*](https://teamtopologies.com/key-concepts-content/team-interaction-modeling-with-team-topologies), current guidance retrieved 2026. Current definitions and temporal expectations for collaboration, X-as-a-Service, and facilitation.
- Team Topologies, [*Groupings*](https://teamtopologies.com/key-concepts-content/groupings), current second-edition guidance retrieved 2026. Platform groupings as multiple teams around a coherent purpose rather than one monolithic team.
- Google, [*Site Reliability Engineering, Part III: Practices*](https://sre.google/sre-book/part-III-practices/), 2016. Service-health ownership spanning monitoring, capacity, incidents, and correction of outage causes.
- Google, [*Continuous Improvement for Reliable Service*](https://sre.google/workbook/engagement-model/), *Site Reliability Workbook*, 2018. Bounded specialist engagement, service readiness, scarce SRE capacity, shared goals, and ownership realignment.

## Exercises

### Exercise 1

Write a boundary contract $B$ for a deployment platform. Include explicit non-responsibilities and allocate release intent, runtime upgrade, security policy, application recovery, platform status, and retirement decisions.

### Exercise 2

A platform team has permanent engineers embedded in twelve application teams. Diagnose whether the interactions are collaboration, facilitation, service consumption, or undefined dependency, and design a transition with evidence and exit criteria.

### Exercise 3

Design a federated platform grouping for identity, runtime, delivery, data services, and a portal. State the authoritative contract of each team and the minimum shared semantics needed for one coherent consumer journey.

### Exercise 4

During an outage, an application team, platform team, and cloud team each claim the fault belongs elsewhere. Define incident roles, evidence, status, escalation, consumer communication, recovery validation, and post-incident boundary review.

### Exercise 5

Transfer the boundary model to a regional hospital platform that composes identity, laboratory results, medication decision support, and messaging. Identify platform, clinical, provider, security, privacy, and patient-facing decision rights.

## Answers to the Exercises

### Answer 1

Mission: enable eligible application teams to release supported workload classes safely and independently. Consumers are application and operations teams. Capabilities include build binding, deployment intent, policy evaluation, rollout state, diagnostics, rollback orchestration, and evidence. The platform owns interface semantics, supported profiles, platform status, provider integration, support, compatibility, and capability retirement. Application teams own code, domain correctness, release intent within policy, application objectives, data, and recovery acceptance. Runtime providers own substrate upgrades and service operation; security owns policy meaning and exceptions. The platform coordinates runtime change and exposes impact but does not decide application release timing without a declared emergency authority. Interactions are steady service consumption, bounded collaboration for new profiles, and facilitation for adoption. Evidence covers independent task success, waits, incidents, recovery, consumer effort, and operator load.

### Answer 2

If embedded engineers must participate in routine delivery indefinitely, the relationship is an undefined dependency, even if called collaboration. If they are discovering a new interface for a few weeks, it is collaboration; if teaching an existing practice, facilitation; if consumers act through a stable contract, service consumption. Inventory what embedded engineers actually decide and execute, cluster repeated needs, and assign provider or consumer ownership. Build stable interfaces and diagnostics for routine cases. Retain bounded collaboration for unresolved workloads and temporary facilitation for learning. Transition team by team with a named capability, independent completion test, support path, consumer and operator workload evidence, and exit date. Do not withdraw people until recovery and exception paths work.

### Answer 3

Identity owns federation, workload credentials, revocation, and identity evidence; runtime owns execution environments, capacity, isolation, upgrades, and runtime health; delivery owns build/release orchestration and provenance; data-service teams own engine-specific provisioning, protection, recovery mechanisms, and lifecycle; the portal owns accessible discovery and composition, not underlying authoritative state. A platform product function owns end-to-end journeys, shared research, prioritization, and cross-capability outcomes. Shared semantics include stable consumer/team/resource identity, declarations and provenance, operation identifiers, lifecycle conditions, error/problem forms, support correlation, telemetry, policy-decision links, compatibility, deprecation, and incident routing. Each capability exposes authoritative status. The portal and composite journeys reference rather than duplicate it.

### Answer 4

Appoint one incident commander for coordination, a platform lead for capability impact and consumer communication, a cloud/provider lead for substrate diagnosis and recovery, and an application lead for domain impact and validation. Preserve correlated request, platform operation, provider resource, deployment, telemetry, and change identifiers. Publish separate provider, platform, and application conditions with freshness and uncertainty. Escalate through documented service contracts; consumers should not route themselves among owners. Recovery requires provider mechanism health, platform journey tests, reconciliation of partial operations, and application acceptance. The review asks whether the platform promise failed, routing worked, authority matched responsibility, dependency signals were sufficient, and recurring collaboration or access gaps require a boundary change.

### Answer 5

The hospital platform owns coherent identity binding, interfaces, message routing, status, audit correlation, provider integration, support, and technical lifecycle for supported clinical journeys. Identity providers own authentication mechanisms; laboratories own result production, provenance, correction, and reference context; medication-system providers own stated computation and technical evidence; messaging providers own delivery mechanisms. Clinicians retain diagnosis, interpretation, prescribing, override, and patient-context decisions. Pharmacy and clinical-safety authorities own medication policy and validation; security owns control policy; privacy and records authorities own permissible access, disclosure, retention, and correction routes. Patients need accessible notification, consent or objection where applicable, provenance, and human recourse. The platform must not convert successful message delivery or a decision-support output into a claim of clinical truth, authorization, informed consent, or safe treatment.
