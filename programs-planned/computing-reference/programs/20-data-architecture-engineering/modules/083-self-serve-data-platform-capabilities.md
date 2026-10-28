---
module_id: DARCH-083
program: Data Architecture Engineering
level: 2
module_number: 83
title: Self-Serve Data Platform Capabilities
status: complete
last_verified: 2026-09-03
---

# Self-Serve Data Platform Capabilities

## One-Page Review

### Governing question

How should a data platform expose safe, comprehensible, reliable, and economical self-service capabilities that let domain teams create and operate governed data products without mastering every infrastructure layer, waiting in hidden ticket queues, or surrendering the ability to meet legitimate specialized needs?

### Essential definitions

- A **self-serve data platform** is an owned internal product that supplies reusable capabilities and paved journeys for building, operating, governing, discovering, and retiring data products.
- A **platform user** is a domain engineer, analyst, scientist, steward, owner, operator, consumer, or automation principal with a defined job and context.
- A **capability** is a supported outcome-oriented service, such as publishing a governed stream, rather than an uncomposed infrastructure component.
- A **user journey** is an end-to-end path from intent to verified outcome, including prerequisites, decisions, waiting, failures, support, and lifecycle.
- A **paved path** is a curated, supported combination of capabilities and defaults for a common class of work.
- A **platform contract** defines a capability's inputs, outputs, semantics, service expectations, policy, support, compatibility, cost, evidence, and lifecycle.
- A **platform API** is the stable machine interface through which users and automation request, inspect, change, or retire capabilities; a portal or CLI is one client of it.
- A **control plane** manages desired state, identity, policy, orchestration, metadata, status, evidence, and reconciliation for platform resources.
- A **data plane** executes storage, compute, transport, query, serving, and data processing under control-plane intent.
- A **composition** assembles lower-level resources and controls into a higher-level product capability through a versioned implementation.
- An **escape contract** permits a justified alternative while preserving product identity, interoperability, security, governance, evidence, support, cost, and lifecycle responsibility.
- **Progressive disclosure** exposes simple safe defaults first and reveals advanced choices only when user needs justify additional cognitive load.
- **Platform cognitive load** is the infrastructure, policy, operational, and interface knowledge a user must hold to accomplish a supported job safely.
- **Golden-path adoption** measures eligible work using supported journeys; it is evidence of fit only when use is voluntary enough to reveal alternatives and outcomes.
- A **capability receipt** records request, identity, product, profile, policy, implementation version, resources, status, evidence, costs, obligations, and limitations.
- **Closure** retires capability instances, identities, dependencies, data, policy, secrets, metadata, costs, and recovery paths while preserving required evidence.

### Central model, mechanism, or theorem

Represent a self-serve platform as:

`S = (U, J, C, X, P, G, O, E, M, L)`

where `U` is users and researched needs, `J` supported journeys, `C` composed capabilities and contracts, `X` experience and interfaces, `P` control and data planes, `G` governed defaults and escape contracts, `O` operations and reliability, `E` evidence, security, and compliance, `M` measurement, economics, and learning, and `L` lifecycle and closure. Self-service exists when an authorized user can achieve a supported outcome through stable interfaces with bounded waiting and cognitive load while controls and evidence operate automatically. A button that creates a ticket does not meet that condition.

### Critical invariants

- User, team, product, journey, capability, profile, request, desired state, implementation, resource, policy, status, receipt, and outcome have separate stable identities.
- Every capability begins with a researched user job and publishes a supported contract, not merely a provider service or reusable script.
- Portal, CLI, SDK, workflow, and automation share stable APIs and state semantics; no interface becomes the only source of truth.
- Desired state is declarative and versioned; controllers reconcile idempotently, expose conditions, and never hide partial or unknown state behind `ready`.
- Paved paths apply identity, isolation, contracts, quality, lineage, security, privacy, retention, deletion, observability, cost, and recovery by default.
- Domain teams retain accountability for data-product meaning and consumers; the platform owns capability usability, reliability, compatibility, and shared controls.
- Progressive abstraction cannot hide evidence, cost, ownership, or failure behavior needed for responsible operation.
- Escape paths are explicit and supported or clearly self-owned; they cannot silently bypass nondelegable policy or interoperability.
- Multi-tenant isolation covers identities, control state, data, compute, network, secrets, metadata, logs, quotas, support, and recovery.
- Metrics distinguish requests, automation, waiting, success, time to value, adoption, abandonment, escapes, cognitive load, reliability, cost, risk, and user outcomes.
- Upgrades and rollbacks preserve product contracts and current policy, deletion, holds, and identity; implementation changes do not silently rewrite user intent.
- Recovery restores trusted control state, identity, policy, secrets, metadata, tombstones, and reconciliation before data-plane service.

### Common failures

Common failures include calling a portal a platform; placing manual approvals behind an API; exposing buckets, clusters, and topics as user outcomes; choosing capabilities without user research; making every option configurable; forcing one path on every workload; allowing invisible bypasses; coupling product contracts to provider resources; storing desired state only in scripts; reporting provisioned before controls are ready; hiding partial failures; centralizing all data-product meaning in the platform team; omitting cost and quotas; treating platform uptime as user success; measuring adoption under a mandate; ignoring support and documentation; upgrading all tenants simultaneously; letting rollback restore revoked access; and recovering data planes before control context.

### Compact example

Ten invented user journeys are evaluated against six declared platform requirements. Four qualify; one each lacks a validated user need, requires a manual ticket, lacks embedded policy, lacks observability, lacks recovery, or uses an unsupported escape. Seven user teams, nine capabilities, three service profiles, ten receipts, and ten decisions are counted. Executable evidence confirms only those declarations and counts. It proves no real user need, self-service, platform usability, policy enforcement, isolation, reliability, cost efficiency, recovery, or beneficial outcome.

### Connections

[DARCH-026](026-data-products-and-service-expectations.md), [DARCH-049](049-self-service-analytics-boundaries.md), [DARCH-050](050-mapping-data-workloads-to-platforms-and-serving-systems.md), [DARCH-064](064-lineage-architecture.md), [DARCH-072](072-policy-as-code-for-data.md), [DARCH-081](081-data-mesh-principles.md), and [DARCH-082](082-domain-oriented-decentralization.md) establish product contracts, self-service boundaries, workload placement, provenance, executable policy, mesh principles, and domain ownership. [DARCH-084](../ROADMAP.md) next develops federated computational governance.

## Governing Question

A platform can offer a polished form that opens an operations ticket, creates an ungoverned bucket after three days, and leaves the domain team to configure schemas, lineage, policy, alerts, cost, retention, and recovery. The interaction is digital but the outcome is neither self-service nor a product capability.

The governing question is how to reduce the distance from domain intent to an operated data product while increasing safety and evidence. A durable platform studies users, composes primitives into meaningful capabilities, reconciles declarative state, embeds controls, exposes honest status and cost, supports specialized paths, and learns from adoption, failure, support, and outcomes.

## Why This Matters

Zhamak Dehghani's [Data Mesh Principles and Logical Architecture](https://martinfowler.com/articles/data-mesh-principles.html) describes a self-serve data platform as one of four interdependent mesh principles and frames it as capabilities that lower the cognitive load of domain teams. The platform enables domain ownership; it does not absorb data-product accountability or eliminate federated governance.

Team Topologies' current [key concepts](https://teamtopologies.com/key-concepts) describe platform, stream-aligned, enabling, and complicated-subsystem team types; X-as-a-service, collaboration, and facilitating interaction modes; and cognitive load as a design concern. A platform team's success depends on the flow and experience of its users, not the number of components it owns.

The CNCF Application Delivery Technical Advisory Group's [Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/) treats a platform as a curated collection of capabilities that serves user needs through self-service and reduces cognitive load. It emphasizes platforms as products rather than one-size-fits-all technology layers. The concepts apply to data platforms while data semantics and lifecycle add domain-specific requirements.

Backstage [Software Templates](https://backstage.io/docs/features/software-templates/) can load code skeletons, collect structured input, publish repositories, and register components. Templates can improve repeatability and user experience, but generated artifacts need maintained contracts, secure actions, policy, ownership, upgrades, and lifecycle. A developer portal is one interface, not the platform itself.

Crossplane [Composition](https://docs.crossplane.io/latest/composition/) defines composite resources and compositions that reconcile higher-level APIs into managed resources. The pattern illustrates declarative platform APIs, composition revisions, functions, and status. Crossplane is one implementation option; correct resource models, providers, security, operations, and user contracts remain local responsibilities.

Kubernetes [custom resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) extend an API with declarative resource types and controllers. The documentation distinguishes declarative APIs, controllers, and custom resources from imperative commands and advises considering aggregation and configuration alternatives. A custom resource should represent durable desired state, not every operational action.

Kubernetes [admission controllers](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/) intercept authenticated and authorized API requests before persistence and can mutate or validate them. Admission supports platform guardrails and defaults, with ordering and failure-policy concerns. It cannot govern data-plane activity or external resources by itself.

The Open Policy Agent [Policy Language](https://www.openpolicyagent.org/docs/policy-language) supports declarative policy over structured inputs. Platform capabilities can evaluate shared rules consistently, but must govern input schemas, bundles, availability, enforcement, obligations, evidence, and exceptions. Policy evaluation does not prove target effect.

The OpenTelemetry [specification](https://opentelemetry.io/docs/specs/otel/) defines common telemetry signals, context, resources, semantic conventions, SDKs, and protocols. Standardized traces, metrics, and logs help correlate platform requests, reconciliation, and data-plane outcomes. Instrumentation coverage and domain-specific service evidence remain to be designed.

OpenLineage's [object model](https://openlineage.io/docs/spec/object-model/) defines jobs, runs, datasets, and extensible facets. A platform can make lineage emission a default capability across engines while preserving domain product identity. Exact input and output versions, run completeness, policy, and semantic contracts still require local profiles.

The Bitol [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/) provides a machine-readable community specification for product, schema, service, quality, role, term, and related metadata. A platform can validate and automate a profiled contract envelope without making file presence equivalent to accountable ownership or observed quality.

NIST's [Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework) organizes outcomes across Govern, Identify, Protect, Detect, Respond, and Recover. Its profiles and outcomes reinforce that platform self-service needs governance, protection, observation, response, and recovery rather than provisioning alone.

NIST [SP 800-53 Release 5.2.0](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) provides security and privacy controls spanning access, audit, configuration, contingency, identity, privacy processing, risk, acquisition, integrity, and supply chain. Platform profiles can automate and evidence selected controls, but local tailoring and effectiveness assessment remain necessary.

The FinOps Foundation's [Framework Capabilities](https://www.finops.org/framework/capabilities/) organize practices for understanding, allocating, optimizing, and operating cloud value and cost. A self-serve platform should expose unit economics, ownership, budgets, anomalies, and optimization context without turning chargeback into its only product objective.

AWS [Data Mesh Strategy](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-data-mesh/introduction.html) and Google Cloud [Data Mesh Architecture](https://cloud.google.com/architecture/data-mesh) provide provider-specific mappings for domain products, platform capabilities, and governance. Managed services can accelerate implementation, but provider consoles and landing zones do not prove user-centered self-service.

Together these sources support platforms as products, cognitive-load reduction, declarative APIs, compositions, templates, admission, policy, telemetry, lineage, contracts, controls, cost management, and provider implementations. The architecture must compose them into end-to-end data-product journeys.

## Prerequisites and Retrieval

You should understand data products, platform engineering, APIs, declarative control planes, controllers, distributed systems, infrastructure as code, identity, policy as code, schemas, data quality, lineage, observability, multi-tenancy, cloud cost, security, privacy, retention, deletion, incident response, product management, and recovery.

Retrieve platform, user, persona, journey, job, capability, contract, self-service, paved path, golden path, portal, API, CLI, SDK, template, composition, control plane, data plane, desired state, observed state, reconciliation, idempotency, condition, profile, default, progressive disclosure, escape hatch, cognitive load, tenant, quota, unit cost, adoption, abandonment, deprecation, and closure.

As a retrieval test, inspect a `Create Pipeline` button. Ask which user job it satisfies; which product and contract it creates; which sources, sinks, schemas, identities, policies, quality, lineage, observability, service, cost, retention, deletion, and recovery apply; whether a ticket or controller performs the work; how partial state appears; which implementation version runs; how upgrades and rollback work; and who supports it. The button answers none of these questions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish platforms, portals, infrastructure, tools, templates, capabilities, paved paths, and data products;
2. research platform users, jobs, journeys, cognitive load, failure, waiting, support, and desired outcomes;
3. define stable platform APIs, resource models, contracts, desired state, conditions, reconciliation, and receipts;
4. compose identity, contracts, schemas, ingestion, storage, compute, streaming, quality, lineage, policy, observability, cost, and lifecycle capabilities;
5. design governed defaults, profiles, progressive disclosure, escape contracts, and domain-platform responsibility boundaries;
6. implement multi-tenant isolation, quotas, secrets, supply-chain security, audit, retention, deletion, and recovery;
7. operate capability service levels, dependencies, upgrades, deprecation, incidents, support, and capacity;
8. measure time to value, waiting, success, abandonment, adoption, escape reasons, cognitive load, reliability, cost, risk, and user outcomes;
9. migrate fragmented scripts and ticket queues into productized capabilities without breaking current data products; and
10. verify recovery and closure across control and data planes without restoring stale policy or deleted data.

## Core Exposition

**Begin with platform users.** Identify domain engineers, analysts, scientists, product owners, stewards, application teams, operators, and automation. Their skills, authority, risk, frequency, environment, and preferred interfaces differ. Avoid designing for an abstract “data team.”

**Research jobs and outcomes.** Observe how users ingest a source, publish a stream, build a batch product, run a quality check, grant access, investigate lineage, manage cost, delete subject data, or recover service. Capture current steps, decisions, waiting, workarounds, failure, support, and desired outcomes.

**Map end-to-end journeys.** Start at intent and end at verified operation, not resource creation. A “publish governed stream” journey includes product identity, contract, schema, producer and consumer authentication, policy, lineage, quality, observability, cost, retention, deletion, support, and recovery.

**Choose platform scope from repeated needs.** Productize capabilities that several users need and that benefit from consistent controls or specialist operation. Do not absorb every one-off workflow or domain semantic decision. Publish scope and non-goals.

**Treat the platform as a product.** Give it accountable ownership, user research, strategy, roadmap, capability contracts, service expectations, support, incidents, cost, adoption goals, feedback, and retirement. A technology program with an end date cannot substitute for durable operation.

**Define capability outcomes.** Name capabilities by the result users seek: register a product, ingest governed events, publish a quality-assured table, create a protected workspace, serve a feature, share with a partner, or retire a product. Lower-level resources remain implementation details when safe.

**Separate capabilities from primitives.** Buckets, clusters, queues, identities, keys, networks, and compute jobs are necessary primitives. A capability composes them with product identity, policy, metadata, evidence, operation, cost, and lifecycle into a supported outcome.

**Design stable platform APIs first.** Portals, CLIs, SDKs, Git workflows, and automation call the same versioned APIs and observe the same state. Do not place essential behavior only in UI code or undocumented operator scripts.

**Use declarative desired state where it fits.** Users specify durable intent such as product distribution, service profile, region, retention, and consumers. Controllers compare desired and observed state, take idempotent actions, report conditions, and continue reconciliation after interruptions.

**Keep imperative operations explicit.** Rotation, replay, backfill, restore, failover, emergency access, and irreversible deletion can require commands with authorization, target version, idempotency, evidence, and review. Do not distort every action into long-lived desired state.

**Model platform resources carefully.** Give product, distribution, source, pipeline, stream, workspace, policy binding, quality suite, lineage integration, retention plan, and retirement stable identities and ownership. Avoid one giant resource with hundreds of unrelated options.

**Separate specification, status, and evidence.** Specification records intent. Status records current observed conditions, generation, dependencies, and progress. Evidence records decisions and outcomes. Controllers must not edit user intent to match implementation convenience.

**Use condition-based status.** Represent accepted, validated, policy-ready, dependencies-ready, provisioned, data-ready, observable, recoverable, degraded, blocked, deleting, and closed states with reason, observed generation, transition time, and evidence. One `ready` Boolean hides partial failure.

**Make reconciliation idempotent.** Repeated control-plane actions for the same desired generation should converge without duplicating resources, grants, data, or notifications. Bind effects to immutable target versions and record retries and partial outcomes.

**Handle drift explicitly.** Detect out-of-band changes to resources, policy, schemas, identities, retention, and observability. Decide whether to correct, adopt, quarantine, notify, or grant an exception. Silent overwrite can destroy intentional emergency changes; silent adoption can legitimize bypass.

**Version compositions.** A capability profile resolves to a signed or otherwise governed composition, provider versions, policy, defaults, and migrations. Record which implementation created each instance. Upgrades should change implementation without silently changing the user contract.

**Provide product registration.** Establish stable identity, domain, owner, consumers, purpose, interfaces, contract, policy, support, cost, and lifecycle before broad publication. Registration is an API-backed state transition, not a catalog form detached from operation.

**Provide contract and schema capability.** Store and validate multidimensional data contracts, schemas, semantics, compatibility, quality, policy, and change proposals. Generate client artifacts where useful but preserve the contract as authority rather than generated code.

**Provide ingestion capability.** Authenticate producers, validate contracts and schemas, assign immutable identity, classify, route by location, quarantine ambiguity, emit lineage and metrics, apply retention, and expose replay and failure behavior. Connector creation alone is insufficient.

**Provide batch transformation capability.** Bind source and output product versions, code, dependencies, configuration, compute profile, schedule or trigger, quality gates, atomic publication, lineage, service, cost, retries, backfills, retention, and recovery.

**Provide streaming capability.** Compose topic or stream identity, schema, partitioning, retention, producer and consumer policy, ordering, delivery semantics, dead letters, replay, lineage, observability, quotas, evolution, and deletion. Avoid exposing broker primitives as the entire experience.

**Provide storage and table capability.** Select format, location, partitioning, access, encryption, keys, versioning, catalogs, compaction, quality, retention, deletion, backup, and recovery from the profile and product contract. Let advanced users tune within safe bounds.

**Provide query and serving capability.** Govern identity, purpose, product version, rows, columns, joins, workload isolation, budgets, caching, export, audit, latency, concurrency, and cost. Query availability does not imply every product is safe for every consumer.

**Provide workspace capability.** Create time-bounded notebook, development, or research environments with approved product access, identities, packages, networks, secrets, lineage, query audit, output controls, cost, cleanup, and deletion. Workspaces are consumers, not exceptions.

**Provide quality capability.** Offer reusable metric definitions, test execution, sampling, expectation profiles, measurement storage, lineage, alerts, quarantine hooks, incident creation, and consumer-specific acceptance. The domain defines semantic fitness and response priorities.

**Provide lineage and metadata capability.** Capture product, dataset, job, run, code, schema, policy, quality, and publication identity across supported engines. Normalize into stable envelopes without discarding native evidence or implying complete coverage.

**Provide discovery capability.** Index products, distributions, contracts, owners, consumers, meaning, quality, lineage, policy, samples, support, cost, incidents, and lifecycle with role-aware visibility. Discovery remains separate from access authorization.

**Provide identity and policy capability.** Resolve user and workload principals, delegation, tenant, product, purpose, action, environment, policy version, and obligations. Distribute policy for reliable local decisions where appropriate and record enforcement separately.

**Provide secrets and key capability.** Provision scoped identities, secrets, encryption keys, rotation, revocation, access evidence, backup, and recovery. Prevent domain teams from copying shared credentials into pipelines or logs.

**Provide privacy and classification capability.** Supply classification assertions, purpose profiles, minimization, masking, tokenization, residency, consent context, rights routing, and protected evidence. Domain and authorized privacy roles decide meaning and applicability.

**Provide retention and deletion capability.** Assign schedules and triggers, apply holds, execute disposition, discover subject and object targets, propagate deletion, preserve tombstones, track backups, and verify non-resurrection. Storage TTLs are adapters, not the governance model.

**Provide observability capability.** Correlate platform request, controller reconciliation, provider operations, data-plane health, pipeline runs, quality, lineage, policy, consumer service, cost, and incidents. Expose user-relevant conditions rather than raw infrastructure telemetry alone.

**Provide cost and capacity capability.** Attribute unit cost to products, teams, consumers, environments, and capabilities; offer budgets, forecasts, quotas, anomaly detection, optimization, and capacity signals. Balance cost with value, reliability, risk, and shared-platform externalities.

**Provide incident and support capability.** Route incidents by product, domain, platform capability, provider, policy, and dependency. Preserve severity, impact, ownership, communication, evidence, remedy, and review. Users need responsive support even when the API is self-service.

**Provide recovery capability.** Define control-plane and data-plane recovery dependencies, product and contract state, identity, policy, secrets, metadata, retention, deletion, and validation. Make recovery a testable capability, not a runbook outside the product.

**Design paved paths around journeys.** A path composes capability versions, profiles, defaults, tests, documentation, examples, support, and evidence for a common outcome. Users should see the product intent and important trade-offs, not dozens of provider options.

**Use progressive disclosure.** Begin with domain, product, purpose, consumers, data shape, service and risk profile. Derive safe defaults. Reveal partitioning, engine, network, key, or scheduling choices only when the user demonstrates a need the abstraction cannot express.

**Avoid lowest-common-denominator abstractions.** A universal pipeline form can fit no workload well. Use a small family of capability types and profiles with shared identities and contracts. Preserve composability rather than one enormous platform object.

**Design escape contracts.** Record why the paved path is insufficient, which alternative is used, who operates it, which global interfaces and controls remain, what evidence is supplied, how support works, how costs are owned, and when the decision is reviewed.

**Distinguish supported from self-owned.** The platform can fully support a path, certify interoperability while the domain operates it, or merely register an external system. State service and incident responsibilities explicitly. Do not imply support from catalog visibility.

**Reduce cognitive load, not agency.** Hide accidental infrastructure complexity while exposing product semantics, risk, cost, dependencies, status, and lifecycle decisions. Users need enough model to operate responsibly and challenge defaults.

**Apply governed defaults.** Default to isolated identities, encrypted storage, contract validation, private networking, lineage, quality hooks, telemetry, budgets, retention, backups, and safe deletion. Defaults are versioned policy and can require stronger profiles by data or use.

**Avoid default lock-in.** Users should see capability and contract semantics separate from provider resource names. Maintain exportable product metadata, schemas, lineage, policy references, and data formats where justified. Portability has cost and should match exit risk.

**Design multi-tenancy explicitly.** Isolate control objects, data, compute, network, identities, secrets, metadata, logs, quotas, billing, support, backups, and recovery. Test noisy neighbors, name collisions, confused deputies, cross-tenant search, and administrator access.

**Use least privilege throughout reconciliation.** Controllers receive narrowly scoped identities and cannot become universal administrators by convenience. Separate read, create, modify, delete, policy, secret, and recovery operations. Audit platform and provider administration.

**Secure the platform supply chain.** Govern source, dependencies, actions, templates, images, providers, compositions, bundles, signatures, builds, registries, deployment, and revocation. A compromised template can distribute the same weakness to every domain.

**Validate untrusted input and output.** User specifications, names, schemas, templates, policy data, provider responses, logs, and generated artifacts can contain malicious or ambiguous content. Apply schemas, semantic validation, escaping, limits, provenance, and review.

**Design quota as a product control.** Quotas protect capacity, cost, tenants, and providers, but can block critical workloads. Publish units, scopes, defaults, current use, forecast, request path, priority, override, and incident behavior.

**Set platform service objectives by journey.** Measure request acceptance, reconciliation latency, capability readiness, correctness, data-plane service, recovery, and support for meaningful user outcomes. Control-plane uptime can be green while every provisioning request is stuck.

**Expose dependency health.** A capability can depend on identity, policy, cloud APIs, registries, networks, schemas, metadata, and providers. Show which dependency blocks which condition and whether retry, degradation, or user action is appropriate.

**Plan capacity and backpressure.** Reconciliation queues, provider quotas, telemetry volume, metadata cardinality, build capacity, and support load can saturate. Prioritize safety and recovery work, report waiting honestly, and avoid retry storms.

**Operate safe upgrades.** Inventory capability instances and contracts, test new compositions, canary profiles and tenants, observe semantic and operational differences, support coexistence, migrate cohorts, and stop rollout on user or control harm.

**Constrain rollback.** Previous implementation can contain vulnerable dependencies, obsolete policy, incompatible schemas, expired exceptions, or unsafe deletion behavior. Roll back only the compatible implementation dimensions while retaining current safety and governance state.

**Deprecate capabilities deliberately.** Publish successor, compatibility, dates, affected users and products, migration tools, support, cost, and consequences. Track actual use and remove old paths only after consumers and recovery dependencies move.

**Avoid permanent previews.** Experimental capabilities need named users, scope, service disclaimer, security, policy, data limits, support, evidence, expiry, and decision. A preview handling production-critical data becomes an unsupported product.

**Make documentation executable where useful.** Pair conceptual guidance with templates, examples, test fixtures, API schemas, policy checks, and observable journeys. Generated examples need maintenance and version binding; documentation success still requires user research.

**Design onboarding as a journey.** Establish team and product identity, authority, training, environments, first governed product, support, and feedback. Time to first value includes approvals and learning, not only resource provisioning.

**Design support tiers.** Offer documentation and diagnostics, community help, platform support, specialist enabling, and incident escalation appropriate to capability risk. Record recurring questions as product discovery rather than user failure.

**Measure self-service honestly.** Track automated outcomes, human touch time, queue time, total lead time, retries, failures, abandonment, support, and hidden manual operations. A request completed through an invisible ticket is not self-service.

**Measure adoption with eligible denominators.** Count products and journeys that need a capability, those using paved paths, governed escapes, unmanaged bypasses, and unknown paths. A mandate can make adoption high while satisfaction and outcomes fall.

**Measure user outcomes.** Track time to first operated product, safe change lead time, recovery, cognitive load, satisfaction, contract quality, reliability, incidents, consumer value, and domain capacity. Portal visits and template executions are activity, not outcome.

**Measure platform economics.** Attribute engineering, infrastructure, support, compliance, incident, migration, and opportunity cost. Compare repeated domain work avoided, lead time, reliability, risk, and product value. Shared value may not map cleanly to chargeback.

**Use escapes and support as discovery.** Analyze why users leave paths or need help: missing capability, bad abstraction, latency, cost, documentation, policy, reliability, or skill. Fix platform fit rather than simply blocking alternatives.

**Audit the platform.** Record API requests, desired-state changes, controller actions, policy decisions, provider calls, administrative access, templates, compositions, upgrades, exceptions, recovery, and closure. Protect audit data from platform administrators where risk warrants.

**Support challenge and remedy.** Users can contest defaults, policy, quotas, cost, status, support, or capability fit. Preserve evidence, owner, response, exception or correction, and outcome. A self-service product still needs accountable human paths.

**Respond across control and data planes.** Platform incidents can create wrong identities, open access, missing lineage, lost data, stale policy, runaway cost, or deleted-data resurrection. Contain desired state and execution, identify affected products and consumers, correct, notify, and verify.

**Migrate from tickets incrementally.** Inventory requests, decisions, scripts, manual steps, failure, waiting, owners, data, controls, evidence, and exceptions. Model stable desired state and capability APIs, then automate frequent bounded journeys while preserving expert review where judgment is real.

**Migrate fragmented tooling through contracts.** Wrap existing engines behind common product identity, policy, metadata, status, and evidence before replacing them. Avoid a full platform rewrite that delays user value and loses native capabilities.

**Recover the control plane first.** Restore API identity, desired state, policy bundles, compositions, secrets, metadata, ownership, contracts, exceptions, retention, holds, deletion tombstones, and incident blocks. Reconcile data-plane resources before declaring them ready.

**Avoid circular recovery.** The platform's registry, policy, secrets, telemetry, and storage may depend on capabilities the platform itself manages. Identify bootstrap resources and independent recovery paths, minimize them, and test loss of each dependency.

**Close capability instances completely.** Mark deletion intent, stop use, reconcile dependencies, revoke access, delete or retain data under policy, remove secrets and resources, settle cost, preserve evidence, and verify backups and restore cannot recreate the instance.

**Close platform capabilities and the platform itself.** Migrate users and products, freeze new instances, retire APIs and controllers, revoke providers, preserve schemas and receipts, transfer obligations, delete infrastructure, and test that automation cannot resume from stale desired state.

## Definitions and Notation

Let a self-serve data platform be:

`S = (U, J, C, X, P, G, O, E, M, L)`.

Represent a platform capability as:

`c = (id, users, job, api, contract, profiles, composition, policy, service, support, cost, lifecycle)`.

Represent a capability request as:

`q = (principal, team, product, purpose, capability, profile, specification, generation, policy_context, idempotency)`.

Represent a condition as:

`k = (type, status, observed_generation, reason, message, transition_time, evidence)`.

Represent an escape contract as:

`x = (need, alternative, owner, retained_invariants, evidence, support, cost, risk, review, exit)`.

Define self-service completion as:

`C_s = automated_verified_outcomes / eligible_requests`.

Define golden-path adoption as:

`A_g = supported_path_instances / eligible_capability_instances`.

Define journey lead time as:

`T_j = verified_outcome_time - valid_intent_time`.

Decompose it into active user time, automated execution, human touch, queue, retry, and blocked dependency time. A low API response latency can coexist with a high `T_j`.

## Mechanisms, Invariants, or Proof Structure

Use these assurance gates.

**User gate.** Identify users, jobs, contexts, skills, authority, frequency, risk, current journeys, cognitive load, and desired outcomes.

**Capability gate.** Define outcome, scope, non-goals, contract, users, API, profiles, composition, service, support, cost, evidence, and lifecycle.

**Interface gate.** Give portal, CLI, SDK, Git workflow, and automation consistent versioned API, identity, idempotency, state, error, and status semantics.

**Control-plane gate.** Preserve desired state, generation, controller identity, reconciliation, conditions, dependencies, drift, evidence, and deletion finalization.

**Composition gate.** Bind capability profile to governed templates, providers, policy, defaults, dependencies, implementation versions, tests, and migrations.

**Governance gate.** Embed product identity, contracts, classification, purpose, access, quality, lineage, residency, retention, deletion, audit, and recovery.

**Escape gate.** Require justified need, alternative, owner, retained invariants, evidence, support, cost, risk, review, and exit.

**Tenant gate.** Isolate control, data, compute, network, identities, secrets, metadata, logs, quotas, billing, support, backup, and recovery.

**Operations gate.** Define service objectives, capacity, dependencies, upgrades, rollback, incidents, support, deprecation, and provider failure.

**Evidence gate.** Record requests, decisions, desired and observed state, controller actions, resources, obligations, costs, exceptions, incidents, and outcomes.

**Outcome gate.** Measure self-service, lead time, waiting, failure, abandonment, adoption, escapes, load, reliability, cost, risk, and user value.

**Migration gate.** Inventory manual and fragmented journeys, expose stable APIs, automate bounded work, wrap existing engines, migrate cohorts, and retire bypasses.

**Recovery gate.** Restore trusted identity, desired state, policy, secrets, metadata, contracts, exceptions, holds, deletion, and bootstrap dependencies before reconciliation.

**Closure gate.** Stop use, settle dependencies, revoke identity, apply disposition, remove resources and cost, preserve evidence, and prevent restoration.

**Learning gate.** Turn research, support, escapes, incidents, metrics, and challenges into capability, contract, policy, documentation, and roadmap decisions.

### Executable evidence: self-serve platform journey evaluation

The following program classifies ten invented user journeys against six declared platform requirements.

<!-- bijux-verify: {"id":"self-serve-platform-journey-evaluation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"journeys=10\nqualified=4\nmissing_user_need=1\nmanual_ticket=1\nmissing_policy=1\nmissing_observability=1\nmissing_recovery=1\nunsupported_escape=1\nuser_teams=7\ncapabilities=10\nservice_profiles=3\nevidence_receipts=10\ndecision_events=10\n","stderr":""}} -->
```python
journeys = [
    {"team": "orders", "capability": "batch-product", "profile": "p1", "need": True, "automated": True, "policy": True, "observable": True, "recovery": True, "escape": True},
    {"team": "risk", "capability": "stream-product", "profile": "p2", "need": True, "automated": True, "policy": True, "observable": True, "recovery": True, "escape": True},
    {"team": "science", "capability": "workspace", "profile": "p3", "need": True, "automated": True, "policy": True, "observable": True, "recovery": True, "escape": True},
    {"team": "finance", "capability": "quality-suite", "profile": "p1", "need": True, "automated": True, "policy": True, "observable": True, "recovery": True, "escape": True},
    {"team": "orders", "capability": "unused-cache", "profile": "p1", "need": False, "automated": True, "policy": True, "observable": True, "recovery": True, "escape": True},
    {"team": "marketing", "capability": "partner-export", "profile": "p2", "need": True, "automated": False, "policy": True, "observable": True, "recovery": True, "escape": True},
    {"team": "support", "capability": "query-service", "profile": "p3", "need": True, "automated": True, "policy": False, "observable": True, "recovery": True, "escape": True},
    {"team": "risk", "capability": "feature-product", "profile": "p2", "need": True, "automated": True, "policy": True, "observable": False, "recovery": True, "escape": True},
    {"team": "identity", "capability": "token-service", "profile": "p3", "need": True, "automated": True, "policy": True, "observable": True, "recovery": False, "escape": True},
    {"team": "science", "capability": "special-compute", "profile": "p1", "need": True, "automated": True, "policy": True, "observable": True, "recovery": True, "escape": False},
]

def evaluate(journey):
    if not journey["need"]:
        return "missing_user_need"
    if not journey["automated"]:
        return "manual_ticket"
    if not journey["policy"]:
        return "missing_policy"
    if not journey["observable"]:
        return "missing_observability"
    if not journey["recovery"]:
        return "missing_recovery"
    if not journey["escape"]:
        return "unsupported_escape"
    return "qualified"

results = [evaluate(journey) for journey in journeys]
print(f"journeys={len(journeys)}")
for outcome in ["qualified", "missing_user_need", "manual_ticket", "missing_policy", "missing_observability", "missing_recovery", "unsupported_escape"]:
    print(f"{outcome}={results.count(outcome)}")
print(f"user_teams={len({journey['team'] for journey in journeys})}")
print(f"capabilities={len({journey['capability'] for journey in journeys})}")
print(f"service_profiles={len({journey['profile'] for journey in journeys})}")
print(f"evidence_receipts={len(journeys)}")
print(f"decision_events={len(results)}")
```

The output reports ten journeys, four qualified and one of each declared failure, seven teams, ten capabilities, three service profiles, ten declared receipts, and ten decisions.

The evidence is deliberately narrow. Invented Booleans and strings do not establish user need, automation, policy, observability, recovery, escape support, isolation, reliability, cost, adoption, or outcome. The evaluator trusts declarations, selects the first failure, and performs no platform operation. Production assurance requires user research, real API and controller observations, policy and enforcement evidence, tenant tests, service telemetry, support and escape analysis, cost data, incident learning, and recovery exercises.

## Alternatives and Trade-Offs

**Portal-first design.** Discovery and demos arrive quickly. State and behavior can fragment behind the interface.

**API-first design.** Automation and interface consistency improve. User journeys can remain poor without experience research.

**Git-based workflows.** Review and history are familiar. Feedback and reconciliation latency can be high.

**Interactive APIs.** Feedback is immediate. Durable review, reproducibility, and bulk change need design.

**Declarative desired state.** Reconciliation and recovery improve. One-time operations can be awkward.

**Imperative orchestration.** Operational intent is direct. Retry and drift can become unsafe.

**High-level capabilities.** Cognitive load falls. Abstractions can hide essential trade-offs or fit poorly.

**Low-level primitives.** Flexibility rises. Every domain repeats integration and controls.

**Few paved paths.** Support and reliability concentrate. Workload coverage is narrow.

**Many profiles.** Fit improves. Testing, documentation, upgrades, and choice load grow.

**Strict golden paths.** Control coverage and support are consistent. Legitimate specialized work can be blocked.

**Governed escapes.** Domain fit and learning improve. Operating and assurance responsibility becomes distributed.

**Central evaluation.** Policy rollout and evidence are consistent. Latency and outages become systemic.

**Local policy bundles.** Availability improves. Distribution, revocation, and drift require strong controls.

**Build internal capabilities.** Fit and control can be high. Long-term engineering and support costs grow.

**Use managed services.** Delivery can accelerate. Provider semantics, portability, evidence, and cost constrain choice.

**Uniform provider stack.** Skills and support simplify. Domain fit and exit options narrow.

**Portable contracts over varied engines.** Flexibility improves. Compatibility testing and operations grow.

**Automatic upgrades.** Security and standardization improve quickly. Blast radius and contract surprises rise.

**Tenant-controlled upgrades.** Change is safer locally. Version sprawl and platform burden increase.

**Central platform funding.** Shared adoption is encouraged. Cost ownership and demand signals can weaken.

**Chargeback.** Unit economics become visible. Domains may avoid valuable shared capabilities.

**Strong abstraction.** Provider complexity is contained. Debugging and specialized optimization become harder.

**Transparent implementation.** Expert control improves. Most users face unnecessary cognitive load.

## Failure Modes and Misconceptions

1. **“A portal is a platform.”** It is one interface over capabilities and state.
2. **“A button makes a workflow self-service.”** Hidden tickets and approvals preserve queues.
3. **“Infrastructure primitives are capabilities.”** Users need supported outcomes with controls and lifecycle.
4. **“Every data user has the same journey.”** Roles, skills, frequency, risk, and context differ.
5. **“Platform roadmaps can skip user research.”** Internal users still have alternatives and unmet needs.
6. **“More features mean better platform fit.”** Choice and maintenance can raise cognitive load.
7. **“One universal pipeline supports every workload.”** Batch, streaming, ML, and regulated needs differ.
8. **“A template is a maintained product.”** Generated code, dependencies, upgrades, and support still matter.
9. **“The UI can be the source of truth.”** Automation and recovery require stable APIs and state.
10. **“Every operation should be declarative.”** Some bounded commands need explicit execution semantics.
11. **“Every operation should be imperative.”** Durable intent and drift need reconciliation.
12. **“A ready Boolean describes platform state.”** Partial dependencies and controls remain hidden.
13. **“Provisioned means usable.”** Policy, data, quality, observability, and recovery may be incomplete.
14. **“Retries are automatically safe.”** Effects need immutable targets and idempotency.
15. **“Controllers should overwrite all drift.”** Emergency or external changes may need adoption or review.
16. **“Compositions are implementation details without versions.”** Instances depend on exact behavior and migration.
17. **“Product registration is a catalog form.”** Identity must connect operation, policy, and lifecycle.
18. **“Schema validation is a full data contract.”** Semantics, quality, service, and policy remain.
19. **“A connector completes ingestion.”** Identity, contracts, failure, lineage, and lifecycle remain.
20. **“A topic is a streaming product.”** Producer, consumer, schema, replay, policy, and service remain.
21. **“A bucket is a storage capability.”** Format, access, keys, retention, and recovery remain.
22. **“Query access serves every consumer.”** Purpose, isolation, exports, performance, and cost differ.
23. **“Notebooks are outside platform governance.”** They consume, transform, retain, and export data.
24. **“The platform owns data quality.”** It supplies mechanisms; domains own semantic fitness.
25. **“Lineage emission proves complete provenance.”** Instrumentation and semantic gaps remain.
26. **“Discovery grants access.”** Finding a product and authorization are separate decisions.
27. **“Policy evaluation proves enforcement.”** Target effects and obligations need evidence.
28. **“Secret management is just storage.”** Identity, rotation, revocation, audit, and recovery matter.
29. **“A PII scanner provides privacy governance.”** Purpose, rights, context, and lifecycle remain.
30. **“Storage TTLs provide retention governance.”** Authority, triggers, holds, disposition, and evidence remain.
31. **“Raw telemetry is platform observability.”** Users need journey and product conditions.
32. **“Cost dashboards create efficiency.”** Ownership, value, forecasts, and action paths matter.
33. **“Self-service eliminates support.”** Users still need diagnosis, learning, and escalation.
34. **“Recovery is a separate operations concern.”** It is a capability contract and user outcome.
35. **“Paved paths should expose every option.”** Progressive disclosure protects focus and safety.
36. **“High-level abstractions must fit everything.”** Capability families and escapes handle variation.
37. **“Escape hatches are governance bypasses.”** Good escape contracts preserve invariants and evidence.
38. **“Registered alternatives are platform-supported.”** Service ownership must be explicit.
39. **“Hiding complexity reduces all cognitive load.”** Hidden cost and failure can make operation harder.
40. **“Secure defaults never need versions.”** Threats, policy, providers, and users change.
41. **“Multi-tenancy is namespace separation.”** Identity, network, metadata, logs, and recovery can cross tenants.
42. **“Platform controllers need broad administrator access.”** Least privilege limits systemic compromise.
43. **“Trusted templates need no supply-chain controls.”** Their scale amplifies compromise.
44. **“Quotas are purely financial.”** They protect capacity, tenants, providers, and reliability.
45. **“Control-plane uptime proves user success.”** Requests can remain blocked or wrong.
46. **“Automatic upgrades always reduce risk.”** Blast radius and semantic change can create harm.
47. **“High adoption proves satisfaction.”** Mandates can hide workarounds and abandonment.
48. **“API latency measures time to value.”** Queue, learning, dependencies, and operation dominate journeys.
49. **“Restore data planes first for speed.”** Stale identity and policy can expose data.
50. **“Deleting desired state closes a capability.”** Data, resources, secrets, costs, evidence, and backups remain.

## Worked Examples

### Example 1

A platform team follows an Orders engineer from source registration through a supported streaming product. It discovers five tickets and repeated policy work, then designs one governed journey with explicit owner, contract, schema, consumers, lineage, service, cost, and closure.

### Example 2

A `DataProductDistribution` API accepts product, purpose, interface, service and risk profiles. Controllers compose identity, storage, policy, quality, lineage, telemetry, budget, retention, and recovery and expose separate conditions for each observed generation.

### Example 3

A stream capability creates schemas, producer and consumer identities, partition and retention policy, dead-letter handling, replay controls, lineage, alerts, quotas, and deletion hooks. The user chooses service and data profiles rather than broker parameters initially.

### Example 4

A scientist requests a protected workspace. The platform grants time-bound product access, approved packages and network, secrets, query audit, output controls, cost budget, lineage, cleanup, and deletion. Extension changes desired state and receives a new policy decision.

### Example 5

A geospatial team needs specialized compute. Its escape contract retains product registration, identity, network, policy, contract, lineage, telemetry, cost, retention, recovery, and incident interfaces while the domain owns engine operation and upgrades.

### Example 6

A platform composition upgrade changes object-store provider and table format implementation while preserving the distribution contract. Canary tenants dual-read and reconcile data, policy, lineage, performance, cost, deletion, and recovery before cohort migration.

### Example 7

A control-plane outage uses verified local policy bundles for bounded reads, denies new sensitive exports, queues safe desired-state changes, and exposes degraded status. It never converts missing decisions into universal allow or reports resources current.

### Example 8

Metrics show 90 percent mandated template use but long ticket waits and high notebook exports. Journey analysis separates automation from human touch, discovers a missing exploration capability, and changes the roadmap rather than celebrating adoption.

### Example 9

A provider quota blocks hundreds of reconciliation attempts. Controllers back off, prioritize recovery and security changes, show the dependency and queue age, forecast capacity, and prevent retry storms. Support communicates affected products and workarounds.

### Example 10

Recovery restores product and contract registries, controller desired state, policy, provider identities, secrets, exceptions, holds, deletion tombstones, and evidence. Data-plane resources remain quarantined until reconciliation and tenant isolation pass.

## Cross-Program Connections

**Platform Engineering.** Platform-as-product, APIs, control planes, golden paths, reliability, multi-tenancy, cognitive load, support, and adoption are direct foundations.

**Data Engineering.** Ingestion, batch, streaming, storage, query, quality, lineage, orchestration, backfills, retention, and deletion become platform capabilities.

**API and Service Engineering.** Resource models, declarative and imperative operations, idempotency, conditions, errors, versioning, compatibility, and service objectives define interfaces.

**Distributed Systems Engineering.** Reconciliation, desired and observed state, retries, backpressure, partial failure, dependency health, and recovery shape the control plane.

**Security Engineering.** Identity, least privilege, tenant isolation, secrets, policy, supply chain, audit, incident response, and secure recovery protect shared blast radius.

**Privacy Engineering.** Purpose, classification, minimization, tokenization, residency, rights, retention, deletion, evidence, and affected-party remedy require embedded profiles.

**Product Management.** User research, jobs, journeys, roadmaps, contracts, support, adoption, cost, feedback, outcomes, and deprecation make the platform a product.

**Site Reliability Engineering.** Service-level objectives, capacity, dependencies, observability, incidents, upgrades, rollback, and disaster recovery sustain capabilities.

**FinOps.** Attribution, unit economics, budgets, forecasts, quotas, anomalies, optimization, and value guide platform and product decisions.

**Systems Engineering.** User, team, platform, provider, policy, economics, failure, lifecycle, and emergent bypass interactions need end-to-end analysis.

## References

1. Zhamak Dehghani, [Data Mesh Principles and Logical Architecture](https://martinfowler.com/articles/data-mesh-principles.html), self-serve data-platform principle and logical context.
2. Team Topologies, [Key Concepts](https://teamtopologies.com/key-concepts), team types, interaction modes, flow, and cognitive load.
3. CNCF TAG App Delivery, [Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/), platform capabilities, users, self-service, and product thinking.
4. Backstage, [Software Templates](https://backstage.io/docs/features/software-templates/), parameterized scaffolding, actions, repositories, and catalog registration.
5. Crossplane, [Composition](https://docs.crossplane.io/latest/composition/), composite APIs, managed resources, functions, revisions, and reconciliation.
6. Kubernetes, [Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/), declarative extension APIs and controllers.
7. Kubernetes, [Admission Controllers](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/), mutating and validating admission and failure behavior.
8. Open Policy Agent, [Policy Language](https://www.openpolicyagent.org/docs/policy-language), declarative policy evaluation over structured data.
9. OpenTelemetry, [Specification](https://opentelemetry.io/docs/specs/otel/), traces, metrics, logs, context, resources, and protocols.
10. OpenLineage, [Object Model](https://openlineage.io/docs/spec/object-model/), jobs, runs, datasets, and facets.
11. Bitol, [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/), machine-readable product, schema, quality, service, role, and term metadata.
12. NIST, [Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework), Govern, Identify, Protect, Detect, Respond, and Recover outcomes.
13. NIST, [SP 800-53 Release 5.2.0](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final), security and privacy controls.
14. FinOps Foundation, [Framework Capabilities](https://www.finops.org/framework/capabilities/), cloud value, cost, allocation, optimization, and operations practices.
15. AWS, [Data Mesh Strategy](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-data-mesh/introduction.html), provider-specific platform and domain guidance.
16. Google Cloud, [Data Mesh Architecture](https://cloud.google.com/architecture/data-mesh), provider-specific data-product, governance, and platform guidance.

## Exercises

### Exercise 1

Research and design the journey for a domain team to publish a governed batch data product. Define users, jobs, current pain, capability contract, API, desired state, profiles, conditions, support, evidence, cost, and closure.

### Exercise 2

Design experience, control, and data planes for a platform supporting batch, streaming, query, ML, partner sharing, and regulated products. Define resource types, controllers, dependencies, tenancy, policy, observability, and recovery.

### Exercise 3

Define a paved streaming-product path plus an escape contract for specialized event processing. Include contracts, schemas, identity, policy, lineage, quality, service, cost, incident, retention, deletion, upgrades, and support.

### Exercise 4

Create an evidence and measurement model that distinguishes self-service, adoption, platform reliability, control coverage, cognitive load, cost, product value, incidents, and user outcomes across 300 products.

### Exercise 5

Migrate a platform built from tickets, scripts, cloud consoles, and team-specific pipeline frameworks into stable capabilities. Include inventory, APIs, wrapping, automation, cohorts, rollback, recovery, deprecation, and closure.

## Answers to the Exercises

### Answer 1

Interview product owners and engineers and observe one product from request to supported operation. Capture source authorization, product registration, contract and schema, compute, storage, quality, publication, access, lineage, policy, observability, retention, cost, support, recovery, and current waiting or rework. Define the outcome as an operated batch distribution for named consumers, not a scheduled job.

Publish a capability API with product, owner, purpose, source, consumer, contract, schedule or trigger, service, data, risk, location, retention, and cost profiles. Desired state receives stable identity and generation. Conditions show accepted, contract-valid, policy-ready, source-ready, compute-ready, published, observable, recoverable, degraded, and closed states. A governed composition binds implementation and policy versions. Receipts record decisions and observed resources. Measure end-to-end lead time, human touch, failures, support, cognitive load, reliability, cost, consumer use, and closure; use findings to evolve the path.

### Answer 2

The experience plane provides portal, CLI, SDK, Git workflows, documentation, examples, diagnostics, status, cost, and support over one API. The control plane manages team and product identity, contracts, schemas, capability instances, profiles, compositions, policies, desired state, conditions, metadata, lineage, quality definitions, budgets, exceptions, incidents, upgrades, and finalizers. Data planes provide isolated ingestion, storage, batch and streaming compute, query, serving, workspaces, feature processing, and exchange.

Resource types remain cohesive: product, distribution, pipeline, stream, workspace, policy binding, quality suite, contract, retention plan, and closure. Controllers use least-privilege identities and idempotent reconciliation, publish dependency conditions, and handle drift. Tenant isolation covers all planes and backups. Policy admission validates intent; runtime controls govern execution. Telemetry correlates request to consumer outcome. Recovery bootstraps identity, APIs, desired state, policy, secrets, metadata, exceptions, holds, and tombstones before reconciling data resources.

### Answer 3

The paved path asks for product and stream identity, domain, owner, consumers, purpose, event contract, keys and time, traffic and service profile, classification, location, retention, and replay needs. It composes producer and consumer identities, schemas, broker resources, partition policy, dead letters, quality hooks, lineage, observability, quotas, cost attribution, support, deletion, backup, and recovery. Conditions expose each dependency and verified generation.

The specialized processor escape names the unsupported requirement and alternative engine, domain operator, retained product and contract APIs, event envelope, identity, network, secrets, policy decisions, schemas, lineage facets, telemetry, service evidence, budget, retention, deletion, incident integration, recovery, and review date. The domain owns engine upgrades and on-call; the platform owns shared interfaces. Cross-path compatibility tests and provider events support consumers. The exit plan moves to a future paved profile or renews the exception with evidence.

### Answer 4

Build denominators for eligible user journeys, products needing each capability, requests, capability instances, teams, tenants, controls, escape decisions, and recovery paths. Self-service separates fully automated verified outcomes from invisible tickets and records human touch and queue time. Adoption separates paved, governed escape, unmanaged, abandoned, and unknown instances. Reliability measures meaningful conditions and end-to-end journey objectives, not control-plane uptime alone.

Control evidence links policy decision, enforcement, obligation, resource observation, tenant test, retention, deletion, and recovery. Cognitive-load evidence combines task success, learning time, concepts required, support, errors, and surveys. Cost includes platform engineering, infrastructure, provider, support, incidents, migrations, and domain work, related to lead time, reuse, risk, and consumer value. Track escapes and support causes, false blocks, security and privacy incidents, time to remedy, product adoption, consumer outcomes, and affected-party reports. Preserve uncertainty and avoid one composite score.

### Answer 5

Inventory every request type, ticket, approval, script, template, console action, resource, framework, identity, policy, manual decision, failure, owner, queue, evidence, product dependency, cost, and recovery path. Identify repeated user jobs and separate genuine judgment from clerical work. Define stable capability and resource APIs before replacing implementations. Wrap useful existing engines behind common product identity, contracts, policy, status, lineage, observability, and lifecycle.

Shadow API requests and controller plans against current operator outcomes, correct semantics, then automate bounded high-volume journeys. Migrate teams and products in cohorts, reconcile resources, controls, cost, service, and consumer outcomes, and retain safe rollback without reviving stale access or deletion state. Convert real judgment into explicit review tasks with scope and evidence rather than hidden tickets. Deprecate scripts and frameworks after instance inventory, user migration, provider and credential revocation, final desired-state reconciliation, evidence preservation, and recovery tests. Close cloud resources, data, secrets, costs, and backups rather than deleting only catalog entries.
