---
module_id: SARCH-038
program: Software Engineering: Software Architecture
level: 1
module_number: 38
title: Service-Oriented Architecture
status: complete
last_verified: 2026-09-06
---

# Service-Oriented Architecture

## One-Page Review

### Governing question

How should an organization expose business and technical capabilities as governed services so independently evolving consumers can collaborate across ownership, technology, and deployment boundaries?

### Essential definitions

- A **service** is an explicitly bounded capability offered through a contract to consumers outside its implementation boundary.
- **Service-oriented architecture (SOA)** organizes a system or enterprise around such services, their contracts, compositions, policies, and governance. It is broader than web services and does not imply microservices.
- A **service consumer** requests or subscribes to a capability; a **service provider** supplies it. These are roles for an interaction.
- A **service contract** defines operations or messages, semantics, policies, compatibility, and observable outcomes.
- A **service boundary** separates implementation and authority from consumers; only the contract is a supported dependency.
- **Service autonomy** is the provider's meaningful control over its logic, resources, lifecycle, and change—not absolute independence.
- **Service composition** combines capabilities to achieve a larger outcome.
- **Orchestration** places process coordination in an explicit controller; **choreography** coordinates through participant rules and exchanged messages without one controller owning the entire flow.
- A **service inventory** is a governed set of services within a domain or enterprise, including owners, contracts, dependencies, versions, and lifecycle.
- An **enterprise service bus (ESB)** is an integration infrastructure pattern that may route, transform, mediate, and enforce policy; it is neither required for SOA nor proof of service orientation.

### Central model, mechanism, or theorem

Let consumer $c$ depend on service capability $s$ only through versioned contract $C_s$. An interaction is admissible when

$$
Admit(c,s,r)=Compatible(c,C_s)\land Authenticated(c)\land Authorized(c,r)\land PolicySatisfied(c,s,r)\land CapacityAvailable(s).
$$

For a composite business outcome, build a dependency graph whose vertices are service operations and whose edges denote required outcomes or messages. The graph exposes sequential latency, fan-out, cycles, ownership, failure propagation, and recovery obligations. A service boundary localizes implementation decisions only when consumers do not depend on private schemas, deployment topology, timing accidents, or shared mutable state.

### Critical invariants

- define services around coherent capabilities and authority, not tables, screens, protocols, or organization-chart fragments alone;
- expose supported contracts while hiding provider implementation and private data representation;
- give every service and contract a durable owner, lifecycle, compatibility policy, and support boundary;
- distinguish consumer, provider, broker, gateway, orchestrator, system of record, and message authority;
- treat remote calls as partial-failure interactions, not local procedure calls;
- keep transactions local where possible and define idempotency, compensation, reconciliation, and unknown outcomes across services;
- version semantics, schemas, policies, errors, events, and persisted process state for coexistence and rollback;
- authenticate participants, authorize each action, minimize data, and preserve end-to-end trust through intermediaries;
- bound retries, fan-out, queues, payloads, deadlines, concurrency, and dependency depth;
- make mediation explicit; avoid hiding business policy inside generic integration infrastructure;
- observe consumer-visible outcomes, not only bus, endpoint, or message activity;
- govern deprecation, discovery, reuse, exceptions, and retirement without central approval becoming a delivery bottleneck.

### Common failures

Common failures include equating SOA with SOAP or an ESB; wrapping every legacy function without improving boundaries; defining services per database table; sharing one enterprise database; exposing provider-internal schemas; centralizing all business rules in a bus; assuming location transparency removes latency and partial failure; creating chatty fine-grained services; building one universal canonical data model; using distributed transactions as the default; confusing message delivery with business completion; versioning syntax but changing semantics; allowing cascading synchronous dependencies; measuring reuse without consumer outcomes; and calling any collection of APIs a service-oriented architecture.

### Compact example

An order capability requests payment authorization from a payment service using an order-scoped operation identity. Payment owns authorization policy and returns a durable authorization reference. If the response is lost, order queries by the same identity rather than issuing a new charge. Inventory reservation remains a separate authority. An orchestrated process records each outcome and applies explicit release or refund compensation if later steps fail; no shared database transaction pretends the three authorities are one component.

### Connections

[SARCH-035](035-event-driven-architecture.md) supplies asynchronous coordination; [SARCH-036](036-client-server-architecture.md) supplies remote interaction semantics; and [SARCH-037](037-microkernel-and-plugin-architecture.md) contrasts host-controlled extensions with independently provided services. [SARCH-039](../ROADMAP.md) next examines microservices. API and Service Engineering owns detailed interface protocols; Data Architecture owns enterprise data integration patterns.

## Governing Question

Large organizations rarely replace all systems together. Capabilities live in packages, mainframes, databases, departmental applications, partner platforms, and new products. Consumers need stable access without learning every implementation or coordinating every release. Service orientation offers a way to expose capabilities across these boundaries through explicit contracts and governance.

The promise is often reduced to technology: publish a web-service endpoint, introduce a bus, or split an application. None is sufficient. The architectural question is how to define capability, authority, contract, ownership, composition, policy, failure, and evolution so collaboration remains possible as systems and organizations change.

## Why This Matters

SOA can reduce point-to-point coupling, provide consistent access to authoritative capabilities, integrate heterogeneous systems, enable multi-channel reuse, and make dependencies visible. It can support gradual modernization because a service contract may remain stable while its implementation moves from a package or mainframe to a new system.

It can also create a distributed monolith, a central integration bottleneck, or a catalog of thin wrappers. Remote interactions add latency and ambiguity. Shared schemas spread change. Central orchestration can accumulate business logic without domain ownership. Enterprise governance can protect compatibility yet stall teams if every change needs a committee.

The enduring value of SOA is not a product stack. It is disciplined boundary design across independent consumers and providers. The techniques remain relevant whether messages use SOAP, HTTP, RPC, queues, files, or event streams.

## Prerequisites and Retrieval

Retrieve capability, component, interface, contract, schema, policy, consumer, provider, authority, interoperability, coupling, cohesion, autonomy, composition, orchestration, choreography, workflow, message, event, request, response, idempotency, transaction, compensation, partial failure, timeout, retry, version, registry, gateway, broker, system of record, service-level objective, and governance.

From SARCH-017 retrieve interoperability; SARCH-023 and SARCH-024 distinguish connectors and runtime interactions; SARCH-034 provides pipes and filters; SARCH-035 provides event semantics; SARCH-036 provides client-server failure reasoning; and SARCH-037 provides contract, lifecycle, and composition lessons at a host-plugin boundary.

## Learning Objectives

After completing this module, you should be able to:

1. define SOA without equating it with one protocol, vendor, or deployment size;
2. identify candidate services from business capability, authority, change, and consumer needs;
3. specify contracts that hide implementation while preserving semantic precision;
4. distinguish service autonomy, stateless interaction, loose coupling, reuse, and composability;
5. compare direct integration, mediation, orchestration, and choreography;
6. reason about remote transactions, compensation, idempotency, and unknown outcomes;
7. govern service identity, discovery, policy, compatibility, deprecation, and retirement;
8. place security and data authority across provider, consumer, and intermediary boundaries;
9. diagnose chatty, cyclic, centrally coupled, and shared-data service designs;
10. distinguish classical SOA from microservices while recognizing their shared principles.

## Core Exposition

**Define service by capability and boundary.** A service offers a coherent outcome to consumers through a supported contract. “Check customer credit,” “reserve inventory,” and “produce a shipping label” name capabilities. “Customer table CRUD,” “screen 17 backend,” and “call stored procedure X” reveal implementation structure rather than a durable boundary.

The OASIS Reference Model describes SOA through concepts including service, visibility, interaction, real-world effect, contract, policy, execution context, and description [1]. The useful lesson is that a service is not merely an endpoint. A consumer needs visibility and a shared basis for interaction, and an invocation matters because it can create an effect.

**Treat service orientation as an architectural style.** SOA applies constraints and principles to a collection of capabilities: explicit contracts, bounded implementation, interoperability, autonomy, discoverability, composition, and governed evolution. Specific systems vary. Some use coarse enterprise services; others use domain services, external partner services, or infrastructure services.

SOAP and the WS-* specifications were prominent mechanisms in historical enterprise SOA, but service orientation can use other protocols. The W3C Web Services Architecture explicitly describes roles, messages, service descriptions, policies, discovery, and interaction within its web-service scope [2]. Web services are one realization; SOA is the broader architectural organization.

**Start from consumers and outcomes.** Identify who needs the capability, what outcome they require, which authority can decide it, what data and policy are involved, and how it changes. A service with no meaningful consumer need is a speculative abstraction. A service copied directly from one existing application may preserve accidental boundaries.

Use business capability maps, domain models, process analysis, system-of-record ownership, change patterns, regulatory boundaries, and operational needs as evidence. No single method mechanically yields the right service. Validate candidates against cohesion, authority, release impact, data ownership, latency, failure consequence, and likely consumer diversity.

**Make ownership durable.** Every service needs an accountable owner for semantics, implementation, operations, security, compatibility, documentation, support, and retirement. A central integration team can operate shared infrastructure but should not become the owner of every domain decision. If ownership is split, name decision rights explicitly.

Autonomy means the owner can make meaningful internal changes without negotiating every consumer release. It is constrained by contracts, shared policies, dependencies, regulation, and resources. Absolute autonomy is neither possible nor desirable in an enterprise.

**Design the service boundary around authority.** A service should control the decisions it promises. A credit service that exposes only a replicated table but relies on another application's hidden rules is not authoritative. A service may delegate work, but consumers need a clear source of truth and outcome semantics.

Avoid multiple services writing the same records without coordination. Shared databases let teams bypass contracts, create invisible coupling, and make rollback or auditing ambiguous. Shared reference data can be governed, but ownership, freshness, write authority, and schema compatibility must remain explicit.

**Write semantic contracts.** A contract defines operation intent, inputs, outputs, effects, errors, identity, authorization, preconditions, concurrency, idempotency, deadlines, ordering, privacy, and compatibility. A schema validates representation shape; it cannot alone say whether an amount includes tax, whether a reservation is durable, or whether retry can duplicate an effect.

Separate canonical domain meaning from transport representation. A service can expose request-response operations, commands, facts, subscriptions, bulk files, or streaming exchanges. Each needs its own acceptance and outcome model. API and Service Engineering develops these mechanics in depth; architecture establishes ownership and dependency consequences.

**Prefer explicit coarse outcomes over chatty access.** A remote boundary has latency, serialization, capacity, and partial-failure costs. A consumer that calls `getCustomer`, `getAddress`, `getCreditLimit`, and `getBalance` for every order may depend on provider internals and multiply failure points. A capability such as `assessOrderCredit` can place policy with its owner and return the information the consumer needs.

Coarse-grained does not mean giant universal operations. Inputs and effects still need bounded scope. Choose granularity from business coherence, authority, independent change, workload, and failure recovery rather than a fixed line-count or entity rule.

**Understand loose coupling precisely.** Loose coupling reduces consumer knowledge of provider implementation and limits coordinated change. It does not mean no dependency. A consumer still depends on contract semantics, availability, capacity, policy, and business authority.

Coupling hides in shared schemas, timing assumptions, call order, deployment topology, error interpretation, identity formats, and operational support. Passing through a broker does not remove semantic coupling. Measure which changes cross boundaries and which failures propagate.

**Separate stateless interaction from state-free service.** A stateless interaction contains enough explicit context to be handled without hidden conversational memory from earlier calls. The service still owns durable business state, caches, credentials, and process information. Stateful conversations may be justified for long transfers, protocols, or processes, but need identity, expiry, failover, and recovery.

Avoid storing a long-lived business process only in a short-lived session. Persist process state under a domain identity with version and audit semantics. Then retries, failover, and support can reason about it.

**Choose direct interaction or mediation deliberately.** Direct consumer-to-provider calls keep ownership and latency visible. A gateway can authenticate, route, limit, and adapt at an edge. A broker can buffer and fan out messages. An ESB can mediate protocols, transform representations, route content, and enforce common policy.

Mediation can reduce repeated technical adapters and isolate protocol differences. It also introduces another availability, capacity, security, compatibility, and ownership boundary. If business rules, canonical data mutation, and workflow decisions accumulate in the bus, domain behavior becomes centrally coupled and hard to test. Enterprise Integration Patterns catalog message channels, routing, transformation, endpoints, and system-management patterns without claiming that one bus is always appropriate [3].

**Distinguish translation from semantic ownership.** An adapter can translate wire formats, field names, or protocol operations. It cannot safely invent domain meaning that neither endpoint owns. If one system uses “customer” for a billing account and another for a legal party, renaming fields into one canonical schema does not resolve identity or policy.

Canonical message models reduce pairwise syntactic mappings when a stable shared concept exists. A single enterprise-wide model often becomes enormous, political, and slow to evolve. Prefer bounded canonical models owned by domains, with explicit translation at boundaries where meanings differ.

**Use registries for governance, not magical discovery.** A service catalog records identity, owner, purpose, contract, environment, endpoints, dependencies, policies, versions, support, data classification, and lifecycle. Runtime discovery maps logical identity to reachable endpoints. Design-time discovery helps people find and evaluate capabilities.

A registry entry can be stale, incomplete, or misleading. Registration does not prove quality, authority, compliance, or availability. Automate synchronization where possible and assign ownership. Consumers should select a service from verified semantics and support, not keyword coincidence.

**Compose services with explicit control.** Orchestration uses a coordinator that commands steps and records process state. It provides visible sequence, timeout, retry, and compensation policy but can become a central business bottleneck or single coupling hub. Choreography lets participants respond to facts or messages under local rules. It reduces central control but makes end-to-end progress, ownership, and debugging harder.

Choose from process authority and failure recovery. A legally defined claims process may benefit from an explicit orchestrator. Independent reactions to “shipment dispatched” may fit choreography. Many systems combine them: orchestration inside a bounded process and events for external observations.

**Model composite latency and availability.** A synchronous chain accumulates time. If calls are sequential, a necessary latency budget is the sum of phase budgets; fan-out is limited by the slowest required branch plus coordination overhead. Percentiles do not generally add as independent scalars, so measure the composition.

Availability dependencies also compose. If three strictly required independent services each have availability $0.999$, the simple product model yields $0.999^3\approx0.997003$. Independence and constant rates are strong assumptions; common infrastructure and correlated failures can make reality worse. Use the calculation to expose dependency cost, not promise a production SLO.

**Bound fan-out and dependency depth.** One request that synchronously calls ten services can amplify load and failure. Nested retries multiply attempts. Cycles create deadlock, recursion, and ownership ambiguity. Map runtime dependencies and set deadlines, concurrency limits, circuit policies, admission, and degradation at meaningful boundaries.

Denormalize read models or use asynchronous propagation where freshness policy permits. Do not turn every page render into a distributed join across systems of record. The consumer should know whether data is current, cached, replicated, or reconciled.

**Keep transactions local where possible.** One ACID transaction across independent services couples availability, resources, and implementation. Distributed transaction protocols can be appropriate within controlled participants, but they are not a universal enterprise default. Many business processes use a sequence of local commits with durable process state and compensating actions.

Compensation is a new domain action, not time travel. Refunding a charge does not erase the original charge, fees, notification, or audit history. Some effects are irreversible. Define idempotency, duplicate detection, outcome query, compensation eligibility, manual intervention, and reconciliation before failure.

**Reason about ambiguous remote outcomes.** If a consumer times out after sending a command, the provider may not have received it, may be processing, or may have committed with a lost response. Use stable operation identity and authoritative outcome lookup. Retrying with a new identity can duplicate effects; treating timeout as failure can trigger incorrect compensation.

Events also require outcome precision. Broker acknowledgment may prove message acceptance under one durability policy; it does not prove every consumer processed the message or the business objective completed. Observe delivery, processing, domain effect, and composite outcome separately.

**Design compatibility for coexistence.** Providers and consumers deploy at different times. Contracts, schemas, policy documents, credentials, process state, cached responses, and messages may persist. Compatibility must cover old consumer/new provider and rollback to old provider with new state or messages.

Prefer additive changes when defaults are semantically safe. Never reuse fields or error codes for new meaning. Treat stricter validation, unit changes, ordering changes, and new required authorization as compatibility changes even if the schema remains valid. Maintain a supported matrix and test representative real consumers.

**Use policy with clear enforcement.** Policies may address identity, authorization, encryption, retention, residency, rate limits, versions, or support. State who authors, evaluates, enforces, and audits each policy. A policy document nobody enforces is aspiration; a gateway check cannot enforce what happens inside a provider.

Central technical policy can reduce inconsistency. Domain policy belongs with the authority that understands it. Avoid embedding pricing, eligibility, or safety decisions in generic routing rules merely because the bus sees every message.

**Preserve end-to-end security.** Authenticate the intended service and caller. Authorize every capability and resource. Intermediaries that terminate encryption, transform messages, or forward identity become trusted components. Strip untrusted forwarding metadata and propagate identity only through governed, integrity-protected context.

Minimize data shared across service boundaries. Classify fields, restrict purposes, redact logs, protect queues and backups, and define deletion propagation. A canonical enterprise message containing every known customer attribute increases breach impact and policy coupling.

**Plan legacy integration honestly.** A facade can expose a stable service contract while isolating a legacy protocol. It creates room for strangled replacement, but only if the contract represents a durable capability rather than mirroring private screens, tables, or batch formats. The facade owns translation and must report legacy limitations.

Do not label a wrapper “modernized” while it retains unbounded operations, shared credentials, hidden sessions, or nightly consistency without documenting them. Some constraints cannot be abstracted away. Consumers need truthful deadlines, availability, freshness, and outcome semantics.

**Govern for enablement.** Governance defines naming, identity, ownership, contract review, security baselines, version support, telemetry, exception handling, deprecation, and retirement. Automate conformance checks and offer reusable paved paths. Reserve human review for semantic, risk, and ownership questions that automation cannot decide.

Metrics should include time to integrate, compatibility incidents, consumer outcomes, dependency risk, policy exceptions, support burden, and retirement progress. Raw service count or reuse count can reward fragmentation and inappropriate shared services.

**Operate services as dependencies.** Publish availability and latency objectives only with scope, measurement point, exclusions, and dependency assumptions. Define incident ownership, escalation, maintenance, capacity, disaster recovery, and consumer notification. A contract without an operational support model is incomplete for production use.

Observe logical operation, consumer, provider, contract version, attempts, route, queue, downstream dependencies, authoritative effect, and composite outcome. Avoid central traces containing sensitive payloads. Sampling helps diagnosis but is not a transaction ledger.

**Distinguish SOA from microservices.** Both emphasize services, explicit boundaries, independent evolution, and remote interaction. Classical enterprise SOA often uses broader business services, centralized governance, shared integration infrastructure, and heterogeneous legacy integration. Microservices commonly emphasize small independently deployable services, decentralized ownership, automation, and product-team operation.

These are tendencies, not mutually exclusive definitions. A microservice estate can reproduce centralized ESB coupling; a classical SOA service can be independently deployable and well bounded. SARCH-039 examines the forces and operational demands of the microservices style. Do not rename SOA to follow fashion or use “micro” as evidence of quality.

**Know when not to distribute.** A modular monolith may preserve capability boundaries with simpler transactions, latency, deployment, and debugging. Extract a service when independent ownership, technology, security, scaling, regulatory separation, integration reach, or lifecycle justifies the distributed boundary.

Architecture can expose a modular monolith through a few coarse services and use events for selected integrations. The aim is not maximum service count; it is controlled collaboration across real boundaries.

## Definitions and Notation

Let service inventory $S=\{s_1,\ldots,s_n\}$, consumers $U=\{u_1,\ldots,u_m\}$, and versioned contract of service $s$ be $C_s^v$. Edge $(u,s)$ in dependency graph $D$ means consumer $u$ relies on an observable outcome of $s$. Edges can be annotated with synchronous, asynchronous, batch, optional, or required semantics.

For request $r$, `Compatible(u,C_s^v)` covers the declared semantic and representation version. `PolicySatisfied` includes applicable identity, data, region, time, and rate policies. `CapacityAvailable` is an admission decision, not a claim of future completion.

For a composite process $q$, let steps $Q=\{q_1,\ldots,q_k\}$. Each step has state in $\{not\_started,accepted,committed,rejected,unknown,compensated,manual\}$. Process completion is a predicate over authoritative step outcomes, not over message counts.

For strictly sequential phase budgets $b_i$, a necessary end-to-end bound is $\sum_i b_i\le B$. For independent mandatory components with availability $a_i$, a simplified series estimate is $A=\prod_i a_i$. Both models require their stated assumptions and do not substitute for measured distributions or correlated-failure analysis.

## Mechanisms, Invariants, or Proof Structure

**Capability invariant.** Each service contract offers a coherent outcome whose authority and owner are named. It does not merely expose provider storage or internal procedures.

**Boundary invariant.** Consumers depend only on supported contract, policy, and observable behavior. Private schema, topology, implementation language, and operational accident remain hidden.

**Ownership invariant.** Service semantics, data authority, compatibility, operation, security, and retirement have accountable decision rights. Shared infrastructure does not silently inherit domain ownership.

**Admission derivation.** Compatibility alone permits unauthorized calls; authentication alone does not grant resource authority; authorization without applicable policy or capacity can violate compliance or stability. Admissible work therefore requires the conjunction stated in the central model. Admission still does not guarantee completion.

**Ambiguous-outcome argument.** After a command is transmitted but before a terminal authoritative response is observed, executions with no receipt and committed effect can be indistinguishable to the consumer. Therefore timeout alone cannot select retry, compensation, or success; stable identity and outcome inquiry are required.

**Composition invariant.** A composite result is declared complete only from authoritative required-step outcomes. Broker acceptance, transport success, and orchestrator activity are intermediate evidence.

**Transaction invariant.** Each local commit has one authority. Cross-service recovery uses an explicitly justified coordination protocol, compensation, or reconciliation; no design assumes an implicit global rollback.

**Compatibility invariant.** Supported old/new consumers, providers, messages, policies, and persisted process states are tested as a declared finite matrix. Syntactic validity is not equated with semantic compatibility.

**Mediation invariant.** Routing and representation translation may be centralized; business meaning and domain policy remain with named owners. An intermediary's transformations and trust are observable.

**Evidence invariant.** Catalog presence, schema validation, message delivery, availability arithmetic, and passing tests each support bounded claims. None proves universal service correctness, availability, or business completion.

## Alternatives and Trade-Offs

| Choice | Advantages | Costs and risks | Prefer when |
|---|---|---|---|
| Modular monolith | local transactions, low latency, simpler debugging and deployment | coordinated scaling and release; less external isolation | boundaries are mainly internal and one owner can govern change |
| Coarse business service | stable capability, fewer remote calls, clear policy owner | larger change surface; risk of broad scope | outcome and authority are cohesive |
| Fine-grained service | narrow responsibility and targeted scaling | chatty calls, more operations, distributed joins | independent lifecycle and workload justify the boundary |
| Direct integration | visible dependency and ownership; fewer intermediaries | repeated adapters and policy implementation | consumer and provider share compatible protocol and policy |
| Gateway or ESB mediation | protocol bridging, routing, shared controls, reduced syntactic duplication | central availability, latency, governance, and business-logic gravity | common technical mediation is real and bounded |
| Orchestration | explicit process state, sequence, timeout, compensation, and audit | coordinator coupling and bottleneck risk | one authority owns the end-to-end process |
| Choreography | participant autonomy and extensible reactions | emergent flow, harder progress and failure diagnosis | participants own independent reactions to durable facts |
| Shared canonical model | fewer mappings for genuinely common concepts | broad coordination and semantic lowest-common-denominator | scope is bounded and one owner can evolve meaning |
| Boundary translation | local domain models and independent evolution | more adapters and mapping tests | domains use legitimately different meanings |
| Distributed transaction | strong atomic coordination for supported participants | availability, locks, operational and technology coupling | failure model and participants justify it |
| Local commits plus compensation | autonomy and long-running workflows | intermediate states, irreversible effects, complex recovery | business semantics permit correction rather than erasure |

## Failure Modes and Misconceptions

1. **“SOA means SOAP.”** SOAP is one message protocol family; service orientation is an architectural organization.
2. **“SOA requires an ESB.”** Mediation is optional and must be justified from integration forces.
3. **“A catalog entry makes a service reusable.”** Consumers need suitable semantics, support, compatibility, and economics.
4. **“Loose coupling means no dependency.”** Contract meaning, availability, policy, and authority remain dependencies.
5. **“A schema is the contract.”** It omits effects, errors, time, identity, ordering, and policy.
6. **“Table CRUD is a business service.”** It exposes storage shape and often moves invariants to consumers.
7. **“One canonical enterprise model eliminates integration.”** It often relocates semantic conflict into central governance.
8. **“The bus should contain shared business logic.”** That obscures domain ownership and creates central release coupling.
9. **“Location transparency makes remote calls local.”** Latency, ambiguity, serialization, and partial failure remain.
10. **“Stateless service means no stored state.”** It usually describes interaction context, not absence of durable domain state.
11. **“Every process needs a central orchestrator.”** Independent reactions may fit choreography; explicit processes may not.
12. **“Compensation is rollback.”** It is a new effect and may not undo external consequences.
13. **“Delivered message means completed business action.”** Acceptance, delivery, processing, commit, and composite completion differ.
14. **“Three 99.9% dependencies guarantee 99.7%.”** The product is only a simplified model under independence and series assumptions.
15. **“More services means more agility.”** Excess boundaries create coordination and operational load.
16. **“Microservices replaced SOA.”** They share service-orientation ideas and emphasize a particular organizational and deployment style.

## Worked Examples

### Example 1

**Situation.** A retailer proposes one service for every table in its order database.

**Reasoning.** `OrderHeaderService`, `OrderLineService`, and `OrderStatusService` force consumers to reconstruct an order and its invariants through several remote calls. The database schema becomes the public model. A coherent `Order` capability instead accepts operations such as place, revise under preconditions, cancel, and query summary while the provider owns line consistency, totals, and state transitions. Separate payment and inventory services remain independent authorities.

**Conclusion.** Service boundaries follow coherent capability and authority, not table count.

### Example 2

**Situation.** Four channels need customer eligibility, but the legacy system exposes only an interactive screen and nightly file.

**Reasoning.** A facade service defines `assessEligibility` with explicit inputs, decision timestamp, evidence reference, errors, and freshness. Initially it adapts the legacy screen for bounded synchronous use and reports nightly-data limitations. The contract avoids screen field names so a replacement rules engine can later implement it. Capacity limits prevent new channels from overwhelming the legacy host.

**Conclusion.** A truthful capability facade can enable gradual replacement; a screen-shaped wrapper would freeze the legacy design.

### Example 3

**Situation.** A central bus transforms every department's `customer` record into one 240-field enterprise message.

**Reasoning.** Billing means account holder, healthcare means patient, and logistics means delivery party. Matching field names do not resolve identity, consent, or authority. Most consumers receive unnecessary sensitive fields, and every change needs central coordination. The organization defines smaller domain-owned contracts and explicit cross-domain mappings for the few shared purposes, with provenance and data minimization.

**Conclusion.** Canonicalization is valuable only within a bounded semantic scope; universal schemas can increase coupling and risk.

### Example 4

**Situation.** Checkout sequentially requires pricing, inventory, and payment, each modeled as independently available with $a=0.999$.

**Reasoning.** Under the simplified assumptions that all three are strictly required and failures are independent, series availability is $0.999^3=0.997002999$, about $99.7003\%$. This exposes a dependency cost. It is not an SLO prediction: shared networks, identity providers, deployments, and load create correlated failures, while caching or degradation can make some dependencies nonmandatory.

**Conclusion.** Composition arithmetic is a diagnostic model whose assumptions must accompany the number.

### Example 5

**Situation.** An order service requests payment, times out, and is about to request payment again with a new identifier.

**Reasoning.** The first request may have committed. A new identifier can create a second charge. The order process retains the original operation identity and queries the payment authority. If the outcome remains unknown, it records manual or delayed reconciliation rather than marking failure. Compensation begins only from a known committed authorization and uses a distinct idempotent refund identity.

**Conclusion.** Stable operation identity and outcome inquiry are prerequisites for safe retry and compensation.

### Example 6

**Situation.** A shipment workflow has authorize order, reserve stock, book carrier, and notify customer steps. Who should coordinate it?

**Reasoning.** The sales domain owns the promise to the customer and the ordered recovery policy, so a durable orchestrator records each step. Stock and carrier remain authoritative for their local outcomes. After booking failure, the orchestrator releases a known reservation; after an unknown booking outcome, it queries before compensating. `ShipmentBooked` is then published for independent analytics and notifications that do not determine process success.

**Conclusion.** Orchestration fits one owned business process, while choreography serves independent reactions to established facts.

### Example 7

**Situation.** A provider adds a required `jurisdiction` field and calls the change backward compatible because the response schema is unchanged.

**Reasoning.** Old consumers do not send the field, so their previously valid requests fail. The change is behaviorally breaking. A compatible rollout first makes the field optional with a safe, documented derivation where valid, observes adoption, updates consumers, then introduces a new contract version if explicit jurisdiction is semantically required. Rollback tests cover messages produced during the transition.

**Conclusion.** Compatibility includes request acceptance and meaning, not only response syntax.

### Example 8

**Situation.** One user request makes two sequential calls; the first has 180 ms budget and the second 260 ms, with 40 ms local work and 70 ms total mediation allowance. The end-to-end budget is 500 ms.

**Reasoning.** The necessary sequential budget is $180+260+40+70=550$ ms, already 50 ms above the objective before unmodeled overhead. Resetting 500 ms at each hop could permit much longer execution. The design must reduce work, parallelize only independent steps, use cached or asynchronous data with declared freshness, degrade, or revise the objective.

**Conclusion.** End-to-end budgets expose impossible synchronous compositions before production timeouts do.

### Example 9

**Situation.** An ESB routes claims, but over time it also decides coverage, pricing exceptions, and fraud holds.

**Reasoning.** Technical mediation now owns domain decisions from three authorities. Changes queue behind one integration team, tests require the entire bus, and services become data stores behind central logic. Move coverage, pricing, and fraud policy to their accountable services. Keep bounded routing, protocol adaptation, identity propagation, and common telemetry in the integration layer, with every transformation visible.

**Conclusion.** An integration bus should not become an anonymous enterprise domain model.

### Example 10

**Situation.** A regional emergency network must coordinate shelters, hospitals, and transport providers despite intermittent connectivity and different systems.

**Reasoning.** Define coarse services for capacity declaration, assistance request, assignment, and status, with agency authority and signed identities. Use locally durable messages, stable operation IDs, bounded payloads, replay protection, and reconciliation after reconnect. A regional orchestrator may coordinate an assigned evacuation, but each agency commits its resources locally. Read models expose timestamp and provenance so stale capacity is never mistaken for current truth. Offline safe procedures remain available when the network cannot establish an outcome.

**Conclusion.** Service orientation can integrate autonomous organizations, but contracts must expose connectivity, freshness, authority, and unknown outcomes rather than hide them.

## Cross-Program Connections

- **API and Service Engineering:** owns detailed HTTP, RPC, GraphQL, event API, schema, security, testing, gateway, and developer-experience mechanics behind service contracts.
- **Distributed Systems Engineering:** owns time, failure models, replication, consistency, consensus, distributed transactions, and coordination mechanisms.
- **Data Architecture Engineering:** owns system-of-record, hub-and-spoke, ESB, canonical data, API-led access, and enterprise data-integration consequences.
- **Software Engineering Patterns:** adapters, facades, gateways, message routers, process managers, sagas, and anti-corruption layers implement bounded portions of SOA.
- **Security Engineering:** identity federation, delegation, authorization, least privilege, audit, confidentiality, and cross-boundary trust govern service interaction.
- **Software Delivery and Reliability Engineering:** deployment, SLOs, capacity, incident ownership, observability, rollback, and dependency management determine operability.
- **Systems Engineering:** stakeholder authority, interface control, verification, configuration baselines, and lifecycle governance apply across organizational services.
- **Database Engineering:** local transactions, schema ownership, replication, outbox, migration, and recovery support service data authority.

## References

1. OASIS, *Reference Model for Service Oriented Architecture 1.0*, OASIS Standard, 12 October 2006. <https://docs.oasis-open.org/soa-rm/v1.0/soa-rm.html>
2. W3C Web Services Architecture Working Group, *Web Services Architecture*, W3C Working Group Note, 11 February 2004. <https://www.w3.org/TR/ws-arch/>
3. Gregor Hohpe and Bobby Woolf, *Enterprise Integration Patterns: Designing, Building, and Deploying Messaging Solutions*, Addison-Wesley, 2003. <https://www.enterpriseintegrationpatterns.com/>
4. OASIS, *Reference Architecture Foundation for Service Oriented Architecture Version 1.0*, OASIS Committee Specification 01, 4 December 2012. <https://docs.oasis-open.org/soa-rm/soa-ra/v1.0/soa-ra.html>
5. The Open Group, *SOA Reference Architecture*, Technical Standard C119, 2011. <https://publications.opengroup.org/c119>
6. Mike P. Papazoglou, *Web Services: Principles and Technology*, Pearson, 2007.
7. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021.
8. Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2002.

## Exercises

### Exercise 1

Define service, service contract, service autonomy, service inventory, orchestration, and choreography. Explain why SOAP and an ESB are neither necessary nor sufficient for SOA.

### Exercise 2

A synchronous operation requires four independent components with modeled availabilities 0.998, 0.999, 0.997, and 0.9995. Compute the simplified series availability and state why the result is not a production SLO guarantee.

### Exercise 3

A customer portal makes twelve synchronous entity-level calls to render one page and fails whenever any call fails. Diagnose the architectural problems and propose a bounded redesign without assuming microservices.

### Exercise 4

Compare orchestration and choreography for an insurance claim spanning coverage validation, damage assessment, payment, and notification. Recommend a split and define failure evidence.

### Exercise 5

Design a service-oriented integration for a university consortium that must recognize cross-institution course completion while each institution retains student-record authority. Cover capability boundaries, contracts, identity, data minimization, composition, offline or delayed exchange, compatibility, governance, and dispute recovery.

## Answers to the Exercises

### Answer 1

A **service** offers an explicitly bounded capability to external consumers. Its **service contract** defines interaction semantics, representations, policies, compatibility, and outcomes. **Service autonomy** is the provider's meaningful control over implementation, resources, lifecycle, and change subject to contracts and obligations. A **service inventory** is the governed set of service identities, owners, contracts, dependencies, versions, and lifecycles. **Orchestration** uses an explicit controller for process progress; **choreography** coordinates participants through distributed interaction rules and messages. SOAP can carry service messages but says little about capability boundaries, authority, ownership, or governance. An ESB can mediate interactions but can connect poorly bounded procedures or centralize domain logic. SOA can use neither, either, or both; the architectural properties decide.

### Answer 2

Under the stated independent, strictly required series model,

$$
A=0.998\times0.999\times0.997\times0.9995=0.993513988503,
$$

or about $99.3511\%$. It is not a production guarantee because failures may be correlated, availability varies over time and workload, measurement definitions may differ, retries or degradation may change requirement structure, and shared infrastructure may dominate. The arithmetic is useful for exposing dependency cost only under its assumptions.

### Answer 3

The portal performs a distributed join, exposes entity granularity, multiplies latency and failure points, and probably depends on provider schemas and call order. Map which data belongs together, its authority, required freshness, and whether every field is mandatory. Introduce a coarse consumer-oriented query capability or a materialized read model populated asynchronously under explicit freshness and provenance. Keep critical write decisions at authoritative services, bound fan-out and deadlines, cache safe data, and degrade optional panels independently. A modular monolith or existing coarse service can implement the redesign; splitting into more deployments is not required. Tests should cover partial data, stale read models, timeout, provider change, and authorization per field.

### Answer 4

Claims adjudication has an accountable process owner, ordered state, deadlines, manual steps, and compensation, so a durable orchestrator should record coverage validation, assessment acceptance, payment identity and outcome, and terminal claim state. Coverage, assessment, and payment services remain authoritative for their local decisions. Notifications and analytics can react choreographically to durable claim-state facts because they should not decide claim completion. Evidence distinguishes message accepted, participant outcome committed, orchestrator state persisted, compensation committed, and human review. Unknown payment outcome triggers inquiry, not a duplicate payment or premature claim failure. An alternative all-choreography design is acceptable only if it names who determines completion and demonstrates equivalent progress, recovery, and audit semantics.

### Answer 5

Each institution exposes a `LearningRecord` service that can attest completion, revoke or correct an attestation, and answer status by stable record identity. A consortium recognition service owns mapping external completion to consortium rules; it does not write institutional transcripts. Contracts include institution, learner-scoped pseudonymous identity, course or outcome identifier, credits and level, completion time, grading interpretation, provenance, signature, correction status, purpose, and version. Federated identity binds institutions and authorized registrars; disclose only fields required for recognition and restrict reuse. Recognition is an orchestrated case with durable states for request, attestation, mapping, decision, appeal, and correction; notifications are choreographed facts. Signed bounded messages can queue during disconnection, with replay protection, expiry, acknowledgment, and later reconciliation. Governance assigns contract and vocabulary owners, supported versions, key rotation, conformance tests, privacy rules, service objectives, and retirement. A dispute preserves both the institution's authoritative attestation and consortium decision evidence, enters manual review, and issues append-only correction or revocation rather than silently overwriting history. Full credit requires retaining institutional record authority and exposing delayed or unknown outcomes honestly.
