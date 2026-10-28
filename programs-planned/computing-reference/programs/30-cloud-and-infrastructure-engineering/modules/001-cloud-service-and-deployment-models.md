---
module_id: CLOUD-001
program: Cloud & Infrastructure Engineering
level: 1
module_number: 1
title: Cloud Service and Deployment Models
status: complete
last_verified: 2026-08-29
---

# Cloud Service and Deployment Models

## One-Page Review

### Governing question

How do service and deployment models describe what a cloud service offers, which capabilities a consumer can control, and for whom the underlying cloud infrastructure is provisioned?

### Essential definitions

- **Cloud computing** is an operating model for on-demand network access to a scalable, elastic pool of shareable physical or virtual resources with self-service provisioning and administration.
- NIST's five **essential characteristics** are on-demand self-service, broad network access, resource pooling, rapid elasticity, and measured service.
- A **cloud service** offers one or more capabilities through cloud computing via a defined interface.
- A **service model** classifies the capability offered and the consumer/provider control boundary: Infrastructure as a Service, Platform as a Service, or Software as a Service.
- **IaaS** gives the consumer fundamental processing, storage, and networking capabilities on which the consumer can deploy and run software, including operating systems and applications, within provider limits.
- **PaaS** gives the consumer a provider-supported environment for deploying consumer-created or acquired applications without managing the underlying infrastructure.
- **SaaS** gives the consumer use of the provider's applications through an interface while the provider manages the underlying application and infrastructure, subject to configurable consumer settings.
- A **deployment model** describes the population and organizational arrangement for which cloud infrastructure is provisioned: private, community, public, or hybrid.
- **Private cloud** is provisioned for exclusive use by one organization; **community cloud** for exclusive use by a community with shared concerns; **public cloud** for open use by the general public; **hybrid cloud** composes two or more distinct cloud infrastructures bound to enable data and application portability.

### Central model, mechanism, or theorem

Service model and deployment model are independent axes. Let (S=\{I,P,A\}) represent IaaS, PaaS, and SaaS, and (D=\{private,community,public,hybrid\}). A basic classification lies in $S\times D$, but the pair is only a starting point. The actual contract (K) must specify controllable resources, retained consumer duties, provider duties, interfaces, tenancy, location, service levels, security, data use, portability, metering, and exit. Calling an offering “public PaaS” does not determine those particulars.

### Critical invariants

A cloud claim is checked against cloud characteristics rather than location or marketing. Service and deployment models are never conflated. Classification follows the offered capability and real control boundary, not the product name. Provider-managed does not mean consumer-unaccountable. Private does not mean on-premises, and public does not mean publicly readable. Hybrid requires distinct clouds and a binding portability mechanism; using two unrelated public providers is not automatically hybrid. Every selection traces workload needs to the exact service contract and verifies security, reliability, data, legal, economic, portability, and exit consequences.

### Common failures

Teams call any hosted VM “cloud”; call virtualization a private cloud without self-service or elasticity; assume SaaS removes identity, data, configuration, legal, or continuity responsibility; choose IaaS for “maximum control” without pricing operations; choose PaaS for “no operations”; treat serverless as literally server-free; label two vendor accounts hybrid; treat multi-cloud as a NIST deployment model; assume public cloud makes customer data public; equate region with deployment model; or compare service categories rather than exact contracts.

### Compact example

An organization can run an IaaS private cloud for one enterprise, consume a public PaaS application runtime, and use a public SaaS collaboration system. If its private cloud and public cloud are bound so workloads or data can move under an integrated arrangement, that portion may be hybrid. The labels do not decide identity design, recovery, residency, cost, or portability; the contracts and architecture do.

### Connections

Operating systems and networks explain the mechanisms below IaaS. Software architecture maps workload requirements to service boundaries. Security and data architecture govern trust and information. Platform engineering creates internal experiences over cloud capabilities. Distributed systems explain remote failure and consistency. Later cloud modules deepen shared responsibility, global infrastructure, control planes, elasticity, managed services, quotas, failure domains, resources, resilience, economics, hybrid, and multi-cloud.

## Governing Question

What exactly is being consumed as a service, who can consume the underlying infrastructure, and what architectural facts remain unspecified by those labels?

Service models answer the first question at a coarse control boundary. Deployment models answer the second at a coarse provisioning and community boundary. Neither substitutes for reading the exact offering contract. The value of the taxonomy is a stable vocabulary for comparison—not permission to infer availability, security, portability, location, cost, or fitness from three letters.

## Why This Matters

“Cloud” is often used to mean a provider, remote datacenter, virtual machine, subscription, or web application. This ambiguity damages design review. Two teams may agree to “use PaaS” while one expects managed runtime patching and the other expects managed application recovery. A regulator may hear “public” as public data access while an engineer means infrastructure offered for open commercial use. Common definitions make hidden assumptions visible.

NIST SP 800-145 remains the official concise U.S. definition: five essential characteristics, three service models, and four deployment models. ISO/IEC 22123-1:2023, 22123-2:2023, and 22123-3:2023 provide current international vocabulary, concepts, and reference architecture, replacing the earlier ISO/IEC 17788 and 17789 foundation. The wordings differ in detail, but both traditions treat cloud as scalable, elastic, shareable resources provided through on-demand interfaces—not simply hardware in another building.

The classification guides engineering and procurement. Moving from IaaS toward PaaS or SaaS generally changes which layers the provider operates and which controls the consumer can exercise. Changing from private to public or hybrid changes community, tenancy, connectivity, governance, and commercial context. These are not linear “better” scales. Each boundary transfers some mechanism work while introducing dependence on provider interfaces, service levels, policy, and evolution.

Precise classification also prevents false assurance. A SaaS vendor can operate application code while the customer remains responsible for users, entitlements, lawful data, configuration, exports, and business continuity. A private cloud can fail its only datacenter. A public IaaS tenant can isolate resources strongly. A hybrid architecture can double operational paths and fail at the identity or data bridge. The selected model describes responsibility placement; it does not prove responsibilities are fulfilled.

## Prerequisites and Retrieval

Retrieve physical and virtual compute, operating systems, networks, storage, applications, APIs, multi-tenancy, identity, elasticity, metering, service contracts, and basic risk. Distinguish ownership from operation, location from access, and product category from implemented guarantee. No provider-specific vocabulary or infrastructure-as-code experience is assumed.

## Learning Objectives

By the end of this module, you should be able to:

1. test a cloud claim against the five essential characteristics;
2. distinguish IaaS, PaaS, and SaaS by offered capability and control boundary;
3. distinguish private, community, public, and hybrid deployment models;
4. explain why service and deployment models form independent axes;
5. classify managed databases, containers, functions, hosted applications, and on-premises systems without relying on marketing names;
6. separate hybrid, multi-cloud, and ordinary use of several services;
7. identify duties and risks that remain after a provider operates more layers;
8. compare exact contracts for interface, service level, tenancy, data, security, portability, metering, support, and exit; and
9. bound executable taxonomy evidence and require human review for high-consequence cloud adoption.

## Core Exposition

Cloud computing begins with an operating model. **On-demand self-service** lets a consumer provision capabilities automatically without routine human interaction with each provider. **Broad network access** makes capabilities available through standard network mechanisms to heterogeneous clients. **Resource pooling** dynamically assigns shared physical or virtual resources, usually with location independence at a provider-defined abstraction. **Rapid elasticity** lets capabilities scale outward and inward, often appearing unlimited within quotas and available capacity. **Measured service** meters use appropriate to the service so consumption can be monitored, controlled, reported, and billed or allocated.

These characteristics are diagnostic, not a binary certification algorithm. A private system can cap capacity and still be cloud-like if it pools, measures, and elastically provisions within that boundary. A public provider can have quotas and capacity shortages. “Rapid” is relative to need and contract. The useful practice is to record evidence for each characteristic instead of arguing from the presence of virtual machines or a web console.

Virtualization is an enabling technology, not the definition. A manually allocated hypervisor guest with a three-week ticket, fixed capacity, no consumer API, and no metering is hosted virtual infrastructure; calling it a private cloud obscures the missing operating characteristics. Conversely, cloud services can expose containers, functions, databases, business applications, or physical dedicated hosts while retaining the cloud operating model.

**Infrastructure as a Service** exposes fundamental resources. The consumer can deploy arbitrary supported software and typically controls guest operating systems, applications, some storage choices, and selected networking. The provider operates facilities, physical resources, and virtualization or allocation layers. “Arbitrary” remains bounded by architectures, images, instance types, policy, quotas, licensing, and interface contracts. IaaS offers control and portability opportunities but gives the consumer patching, hardening, capacity, observability, backup, and application operations work.

**Platform as a Service** exposes an application deployment and execution environment. The consumer supplies or selects application code and configuration; the provider operates the underlying compute, operating environment, and supported runtime mechanisms. PaaS can accelerate delivery and standardize scaling, health, logging, and release integration. It constrains languages, runtime versions, filesystem behavior, networking, background work, observability, extension, and lifecycle. A provider-managed Kubernetes service is not automatically PaaS for every user: cluster administrators may still control nodes, networking, upgrades, and system components, while an internal higher-level application interface over it may be PaaS-like.

**Software as a Service** exposes use of provider applications. Consumers manage users, permissions, tenant configuration, workflows, integrations, and their data responsibilities within allowed settings. Providers operate the application and underlying stack. SaaS can remove enormous implementation burden, but process fit, configuration, identity, export, retention, audit, vendor change, availability, and exit remain. An unmanaged application installed on rented IaaS does not become SaaS merely because users reach it through a browser; the service provider and control boundary matter.

The models describe capabilities, not a universal layer diagram. A managed relational database lets consumers create schemas and queries but not administer the host OS; it may be classified as PaaS or another cloud service category under a chosen taxonomy. Function services are often PaaS-like because consumers deploy functions while the provider operates execution. “Serverless” highlights that the consumer does not manage servers and often receives event-driven scaling and consumption billing; servers and provider operations still exist. Containers likewise span IaaS-like cluster control, PaaS-like application runtimes, and SaaS products.

Product portfolios compose models. A SaaS analytics product may store data in a PaaS database on IaaS resources. The consumer contracts for SaaS; the vendor contracts for underlying services. Responsibilities and failure dependencies follow each relationship. Architecture should name the role from whose perspective it classifies a service, because one party's platform is another party's infrastructure.

Now turn to deployment models. A **private cloud** is provisioned for exclusive use by one organization comprising multiple consumers, and may be owned, managed, and operated by that organization, a third party, or both; it may exist on or off premises. Exclusivity is organizational, not geographic. A private cloud still needs cloud characteristics; exclusive virtualization alone is insufficient.

A **community cloud** is provisioned for exclusive use by a specific community of consumers from organizations with shared concerns such as mission, security requirements, policy, or compliance. It can share specialized controls and cost. Its hard questions are community membership, governance, funding, authority, data separation, service evolution, incident coordination, and exit. It is not merely a private cloud with several arbitrary customers.

A **public cloud** is provisioned for open use by the general public and exists on the provider's premises under the NIST formulation. “Open use” means the service is offered broadly, normally through accounts and contracts; it does not mean all resources or customer data are publicly accessible. Identity, tenancy isolation, network controls, encryption, and customer configuration still govern access.

A **hybrid cloud** composes two or more distinct private, community, or public cloud infrastructures that remain unique but are bound by standardized or proprietary technology enabling data and application portability. A private cloud connected to a public cloud is not meaningfully hybrid merely because packets can cross a VPN; the architecture must state what integration and portability the binding enables. Data synchronization, identity federation, observability, policy, deployment, and recovery can all become cross-boundary concerns.

**Multi-cloud** commonly means intentional use of services from more than one cloud provider. It is useful contemporary vocabulary but not one of NIST SP 800-145's four deployment models. Two public SaaS subscriptions make an organization multi-provider in a loose inventory sense, not a hybrid application architecture. A multi-cloud design may also be hybrid, but only if it includes the relevant distinct infrastructures and binding. Motives—best service, acquisition history, regulatory placement, bargaining, resilience—must be distinguished from claims of workload portability.

Service and deployment axes are independent. One organization can offer private IaaS, community SaaS, public PaaS, or hybrid compositions involving several service types. The mathematical Cartesian product is a teaching aid, not proof that all twelve pairings are equally common or unambiguous. For hybrid, each constituent also has its own service model, provider, and contract; compressing an entire system to one pair can lose critical facts.

Selection starts with workload requirements: data sensitivity and location, user and machine identities, latency, availability, recovery, scalability, performance variance, runtime and protocol needs, administrative control, integration, audit, change cadence, skill, support, cost, portability, and exit. Then inspect exact services. Category-first procurement invites solutions searching for problems.

Control and responsibility are separate. A consumer might lack root access yet remain accountable for lawful processing and continuity. A provider may offer encryption but the consumer chooses keys, identities, or data placement. Module 002 will model shared responsibility in depth. The first principle here is enough: moving the service boundary changes who performs controls, but the system owner still verifies that the combined responsibilities meet requirements.

Contracts matter. Record interfaces and versioning; supported configurations; provider and consumer service objectives; maintenance; incident notification; data location, ownership, use, deletion, and export; subcontractors; security evidence; audit rights; metering and price dimensions; quota; support; suspension and termination; portability; and exit assistance. A model label cannot fill these fields.

Economics are conditional. Cloud can exchange capital purchase for metered service, provide temporary scale, and reduce undifferentiated operations. It can also add steady rent, premium managed-service pricing, data transfer charges, idle resources, support tiers, compliance work, migration, and exit. Elasticity reduces cost only when architecture actually releases resources and pricing follows use. Total cost must include people, risk, and transition, not only hourly compute.

The executable taxonomy below represents three service models and four deployment models, then counts their basic combinations and the illustrative consumer-managed software layers.

<!-- bijux-verify: {"id":"cloud-model-axes-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"service_models=3\ndeployment_models=4\nmodel_combinations=12\niaas_consumer_layers=2\npaas_consumer_layers=1\nsaas_consumer_layers=0\n","stderr":""}} -->
```python
service_models = {
    "iaas": ["operating_system", "deployed_application"],
    "paas": ["deployed_application"],
    "saas": [],
}
deployment_models = ["private", "community", "public", "hybrid"]

combinations = len(service_models) * len(deployment_models)
assert combinations == 12
assert service_models["iaas"][-1] == service_models["paas"][0]
assert service_models["saas"] == []

print(f"service_models={len(service_models)}")
print(f"deployment_models={len(deployment_models)}")
print(f"model_combinations={combinations}")
print(f"iaas_consumer_layers={len(service_models['iaas'])}")
print(f"paas_consumer_layers={len(service_models['paas'])}")
print(f"saas_consumer_layers={len(service_models['saas'])}")
```

Execution establishes only the sizes and relationships encoded in this simplified taxonomy. It does not classify a real service, verify cloud characteristics, assign complete responsibilities, inspect a provider contract, prove isolation, security, reliability, elasticity, cost, portability, legal compliance, or fitness for production.

## Definitions and Notation

Let $C=\{self\text{-}service,network\ access,pooling,elasticity,measurement\}$ be the NIST characteristic set. Let (S=\{IaaS,PaaS,SaaS\}), (D=\{private,community,public,hybrid\}), and (K) an exact service contract. Classification function (f(o,r)) maps offering (o), from consumer role (r)'s perspective, to a service model based on capabilities and control—not branding.

Let (L_c) be layers or capabilities controlled by the consumer and (L_p) those operated by the provider. The sets are not necessarily a clean partition: responsibility can be shared, configuration can be delegated, and third parties can operate components. A **cloud consumer** acquires and uses cloud services; a **provider** makes them available; NIST's reference architecture also names broker, auditor, and carrier roles.

**Tenancy** describes isolation and sharing among consumers; it is not identical to deployment model. **Portability** is the ability to transfer data or applications under stated procedures and compatibility. **Interoperability** is the ability of systems to exchange information and use it. **Exit** includes data export, replacement, migration, deletion verification, and continuing operation during transition.

## Mechanisms, Invariants, or Proof Structure

Use this classification and selection sequence:

1. **Name the consumer role and capability.** State what outcome is acquired and through which interface.
2. **Test cloud characteristics.** Collect evidence for self-service, network access, pooling, elasticity, and measurement.
3. **Classify the service model.** Identify what software or resource capabilities the consumer deploys, configures, and operates.
4. **Classify each deployment context.** Identify eligible consumer population, ownership, operation, location, and any cross-cloud binding.
5. **Build the responsibility map.** Include provider, consumer, broker/integrator, carrier, auditor, and domain authorities as applicable.
6. **Read the contract.** Interfaces, tenancy, service levels, security, data, measurement, support, portability, change, suspension, and exit.
7. **Map workload requirements.** Reject labels that cannot meet explicit technical, legal, operational, and economic constraints.
8. **Verify in practice.** Provision, observe, scale, fail, recover, meter, export, and exit to the degree proportional to the claim.

Review these invariants:

- classification is made from a named consumer/provider relationship;
- all five characteristics have evidence or a documented limitation;
- service and deployment axes remain distinct;
- exact consumer and provider control is stated beyond IaaS/PaaS/SaaS shorthand;
- private/public refers to provisioning community, not data visibility;
- hybrid claims name distinct clouds and the binding that enables portability;
- multi-cloud claims name motive, integration, portability, and correlated dependencies;
- managed layers retain ownership, configuration, identity, data, continuity, and exit duties somewhere;
- model selection includes provider change and termination;
- no category label is used as security, availability, compliance, or cost proof.

Evidence is layered. Standards support vocabulary. Contract review supports declared obligations. Configuration and API evidence support enabled controls. Experiments support observed behavior under tested conditions. Billing data supports measured consumption and price under a time window. Failure and recovery exercises support bounded resilience. Legal, privacy, safety, procurement, financial, and domain reviewers judge consequences automation cannot decide.

## Alternatives and Trade-Offs

**IaaS** maximizes guest and network control among the three baseline models and can ease migration of existing systems. It leaves patching, hardening, runtime, capacity, and much recovery work with the consumer. **PaaS** removes more mechanism work and can standardize deployment and scaling, while constraining runtimes, extensions, diagnostics, and portability. **SaaS** offers the highest complete-application leverage, while giving the least implementation control and creating the strongest process, data, integration, and vendor-fit dependence.

**Private cloud** offers exclusive organizational use and can meet specialized policy or integration needs, but the organization or its contractor must fund scale, engineering, capacity, and lifecycle. **Public cloud** offers broad catalogs and provider scale, but requires careful tenancy, service, location, price, and exit review. **Community cloud** can share specialized controls and economics while adding joint governance. **Hybrid cloud** can place work according to need and support migration or bursting, but introduces cross-environment identity, networking, data, observability, policy, skill, and incident complexity.

**Single-provider depth** can exploit differentiated managed services and reduce integration paths. **Multi-cloud breadth** can satisfy distinct workload or jurisdiction needs and reduce some commercial concentration, but duplicate skills and controls and does not automatically make one application portable or available. **On-premises non-cloud infrastructure** can be correct when deterministic equipment, latency, disconnected operation, or economics dominate; cloud language should not be forced onto it.

## Failure Modes and Misconceptions

- **“Cloud means public provider.”** Private and community models also exist; exact characteristics matter.
- **“On-premises means private cloud.”** Location does not provide self-service, pooling, elasticity, or measurement.
- **“Public cloud means public data.”** The model describes offering and eligible consumer population, not customer access policy.
- **“SaaS transfers all responsibility.”** The consumer retains identities, configuration, data, integrations, lawful use, continuity, and exit obligations.
- **“PaaS has no operations.”** Application behavior, data, service objectives, incident response, dependencies, and provider limits remain.
- **“IaaS is portable by definition.”** Images, networks, identities, disks, APIs, CPU features, and managed dependencies can bind workloads.
- **“Serverless has no servers.”** Server management moves to the provider; runtime, event, data, limit, and application concerns remain.
- **“Managed Kubernetes has one universal service model.”** The offered and consumer-controlled capabilities determine classification.
- **“Two clouds make hybrid.”** Hybrid requires distinct clouds bound to enable data/application portability under the baseline definition.
- **“Multi-cloud guarantees resilience.”** Identity, DNS, data, software, operator, and network dependencies can remain correlated.
- **“Elastic means infinite.”** Quotas, capacity, warm-up, architecture, and contract constrain scaling.
- **“Metered means cheaper.”** Total cost depends on use, price dimensions, people, risk, migration, and exit.

## Worked Examples

### Example 1

**Question:** Is a virtual machine rented through an API public IaaS?

**Reasoning:** It is likely IaaS when the consumer controls the guest OS and applications while the provider operates physical and virtualization resources. It is public deployment when offered for open use under accounts and contracts. Verify all five characteristics and exact controls.

**Conclusion:** Classify by capability and provisioning context, then inspect the contract.

### Example 2

**Question:** Is an on-premises VMware cluster automatically a private cloud?

**Reasoning:** No. Exclusive organizational use supports “private,” but routine manual allocation, fixed assignment, absent metering, and no consumer self-service may fail the cloud operating model.

**Conclusion:** Virtualization plus location does not establish cloud characteristics.

### Example 3

**Question:** How should a managed application runtime be classified?

**Reasoning:** When consumers deploy applications in supported languages while the provider operates the runtime and infrastructure, PaaS is a useful baseline. Review runtime, scaling, network, filesystem, observability, and version controls.

**Conclusion:** PaaS shorthand begins rather than completes the engineering analysis.

### Example 4

**Question:** Is a managed database PaaS?

**Reasoning:** Often it is treated as a platform capability because the consumer manages schemas and data while the provider operates the engine infrastructure. Some taxonomies use specialized categories. Exact backup, failover, patch, identity, and data duties matter more than the label.

**Conclusion:** Record the chosen taxonomy and the real boundary.

### Example 5

**Question:** Does a function service create a fourth universal service model?

**Reasoning:** No under the NIST baseline. It is commonly PaaS-like: the consumer supplies functions and configuration, and the provider operates execution and scaling. Event, duration, concurrency, state, observability, and portability constraints remain.

**Conclusion:** Contemporary product styles can fit or extend a baseline taxonomy without silently rewriting it.

### Example 6

**Question:** A company uses one public cloud for analytics and another for email SaaS. Is it hybrid?

**Reasoning:** It uses multiple providers, but the two services may be unrelated. Without distinct clouds bound for application or data portability, the NIST hybrid definition is not established.

**Conclusion:** Inventory diversity, multi-cloud strategy, and hybrid integration are different claims.

### Example 7

**Question:** Can a public SaaS tenant contain confidential data?

**Reasoning:** “Public” describes broad service availability, not tenant data visibility. Confidential use depends on identity, authorization, isolation, encryption, provider data practices, contracts, location, audit, and customer configuration.

**Conclusion:** Deployment model never substitutes for a data-protection review.

### Example 8

**Question:** Does connecting a private cloud to public IaaS by VPN make a useful hybrid cloud?

**Reasoning:** Connectivity is necessary for many hybrids but insufficient. Name workload/data movement, identity, deployment, compatibility, consistency, recovery, observability, and policy across the binding.

**Conclusion:** Hybrid value comes from governed integration and portability, not a line on a diagram.

### Example 9

**Question:** A hospital moves diagnostic-image analysis to public PaaS. Does the model choice establish clinical and privacy fitness?

**Reasoning:** No. Image identity, integrity, residency, consent, model validity, latency, downtime, clinical workflow, audit, deletion, export, provider change, and incident response require named radiologists and clinicians, clinical informaticians, patient-safety and human-factors specialists, privacy/legal, security, data governance, reliability, procurement, regulators, affected patient representatives, and independent clinical/technical reviewers. No external review is claimed.

**Conclusion:** Service/deployment classification is necessary vocabulary, not high-stakes authorization.

### Example 10

**Question:** When is non-cloud infrastructure preferable?

**Reasoning:** When disconnected operation, deterministic hardware access, latency, equipment integration, existing capacity, regulation, or lifetime economics outweigh cloud characteristics—and the organization can operate it responsibly.

**Conclusion:** Cloud is one operating model, not a universal architectural destination.

## Cross-Program Connections

[Operating Systems](../../22-operating-systems/ROADMAP.md), [Computer Architecture](../../23-computer-architecture/ROADMAP.md), and [Network Engineering](../../24-network-engineering/ROADMAP.md) explain compute, virtualization, storage, and communication beneath cloud abstractions. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) explains remote coordination, partial failure, replication, and consistency.

[Security Engineering](../../25-security-engineering/ROADMAP.md) supplies trust, identity, tenancy, encryption, audit, and threat reasoning. [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) supplies authority, location, lineage, lifecycle, and portability for cloud data.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) composes cloud services into internal developer capabilities but does not redefine provider contracts. [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) maps workload quality attributes and organizational constraints to service choices.

## References

- Peter Mell and Timothy Grance, [NIST SP 800-145: *The NIST Definition of Cloud Computing*](https://doi.org/10.6028/NIST.SP.800-145), 2011. Official five-characteristic, three-service-model, four-deployment-model baseline.
- ISO/IEC, [ISO/IEC 22123-1:2023, *Information technology — Cloud computing — Part 1: Vocabulary*](https://www.iso.org/standard/82758.html), second edition, 2023. Current international cloud-computing terms.
- ISO/IEC, [ISO/IEC 22123-2:2023, *Information technology — Cloud computing — Part 2: Concepts*](https://www.iso.org/standard/80351.html), first edition, 2023. Current detailed cloud concepts, replacing part of ISO/IEC 17788:2014.
- ISO/IEC, [ISO/IEC 22123-3:2023, *Information technology — Cloud computing — Part 3: Reference Architecture*](https://www.iso.org/standard/82759.html), first edition, 2023. Current international cloud reference architecture, replacing ISO/IEC 17789:2014.
- Fang Liu et al., [NIST SP 500-292: *NIST Cloud Computing Reference Architecture*](https://doi.org/10.6028/NIST.SP.500-292), 2011. Vendor-neutral actor/role model for consumer, provider, broker, auditor, and carrier.
- Mark Badger, Tim Grance, Robert Patt-Corner, and Jeffrey Voas, [NIST SP 800-146: *Cloud Computing Synopsis and Recommendations*](https://doi.org/10.6028/NIST.SP.800-146), 2012. Opportunities, risks, service/deployment considerations, contracts, economics, portability, and recommendations.
- ISO/IEC, [ISO/IEC TS 25052-1:2022, *SQuaRE: Cloud Services — Part 1: Quality Model*](https://www.iso.org/standard/78742.html), 2022. Cloud-service quality characteristics for stakeholder evaluation.
- European Union Agency for Cybersecurity, [*Cloud Cybersecurity Market Analysis*](https://www.enisa.europa.eu/publications/cloud-cybersecurity-market-analysis), 2023. Contemporary European market and cybersecurity mapping across cloud attributes and models.

## Exercises

### Exercise 1

Assess a manually provisioned on-premises virtualization environment against the five cloud characteristics. Specify the evidence required and the minimum organizational/technical changes needed before calling it a private cloud.

### Exercise 2

Classify a virtual machine service, managed application runtime, managed relational database, function service, and hosted payroll application by capability and consumer/provider control. State ambiguities and the exact contract facts needed beyond IaaS/PaaS/SaaS.

### Exercise 3

Compare private, community, public, and hybrid deployment for a research consortium. Address eligible consumers, governance, location, tenancy, capacity, funding, security, data, network, operations, audit, portability, and exit.

### Exercise 4

Critique: “We use two public clouds, so the application is hybrid, portable, and resilient.” Construct dependency and evidence maps that could establish or falsify each of the three claims.

### Exercise 5

A national emergency-response agency is selecting cloud models for incident intake, dispatch support, public alerts, responder identity, geospatial data, and evidence records. Recommend a decision method, not a vendor. Define requirements, model combinations, retained duties, failure behavior, evidence, and named human review before operational acceptance.

## Answers to the Exercises

### Answer 1

For self-service, test whether authorized consumers can provision, change, observe, and release resources without routine operator tickets. For broad network access, document standard interfaces and supported clients. For pooling, show dynamic assignment and tenancy/location abstraction while preserving required isolation. For elasticity, measure scale-out and release within capacity, quota, and time bounds. For measured service, show metering, attribution, control, and reporting appropriate to compute, storage, and network use.

A static cluster with manual allocation demonstrates virtualization but not the full model. Minimum changes may include a supported consumer API or portal backed by automatic fulfillment, pooled scheduling, quota and policy, elastic or at least dynamically reassigned capacity, identity and tenancy, consumption telemetry, lifecycle automation, service ownership, support, and recovery. Private deployment follows from exclusive organizational use, whether operation is internal or contracted. Capacity need not be infinite, but limits and provisioning behavior must be honest. Validate the organizational operating model as well as the technical controller.

### Answer 2

The VM service is IaaS-like when consumers control guest OS and applications while the provider operates hardware and virtualization. The application runtime is PaaS-like when consumers deploy code but not the host/runtime substrate. The database is often PaaS-like, although its specialized data interface makes taxonomy choice worth stating. The function service is PaaS-like under the baseline while adding event, duration, concurrency, and consumption semantics. Hosted payroll is SaaS when consumers use the provider-operated application rather than deploying it themselves.

For each, record supported interfaces and versions, configurable and forbidden layers, tenancy/isolation, identity, network, data ownership/use/location/export/deletion, scaling and quota, service objectives, maintenance, observability, backup/recovery, security evidence, audit, metering and price, support, compatibility, suspension, termination, and exit. A managed cluster can shift classification depending on whether the consumer controls nodes and system components or only submits applications. Classify from a named role and contract, not a product family.

### Answer 3

Private cloud gives one consortium organization exclusive use and direct governance but requires it to fund capacity, operation, security, and lifecycle. Community cloud can serve several research institutions sharing mission, data-policy, identity, or grant obligations, but needs joint membership, funding, authority, incident, audit, and exit governance. Public cloud offers provider scale and catalog under broad commercial availability, while the consortium must verify tenant isolation, region/service availability, contracts, data policy, support, and cost. Hybrid can bind a private or community research environment with public services for portability, burst, or specialized analysis, adding cross-boundary identity, connectivity, data consistency, observability, policy, recovery, and skills.

Choose per workload: controlled data, instruments, batch compute, collaboration, public datasets, and archives may justify different combinations. Record eligible users, owner/operator, physical/logical location, shared resources, capacity and quota, cost allocation, identity federation, data authority and residency, network paths, recovery, audit evidence, service levels, export formats, deletion and provider exit. Community membership does not itself guarantee compliance; public deployment does not itself disclose data; hybrid does not itself enable seamless movement.

### Answer 4

“Two public clouds” establishes at most multi-provider use. To claim hybrid under the baseline, identify distinct cloud infrastructures that remain unique and the standardized or proprietary binding enabling actual data or application portability. If both are simply unrelated public services, hybrid is unproven. To claim portability, inventory code, runtime, image, architecture, identities, networks, policies, data formats and volume, consistency, keys, observability, deployment, DNS, quotas, licenses, and operational procedures; execute a time-bounded move and validate behavior and data.

To claim resilience, draw DNS, identity, control-plane, network, software-supply-chain, data authority/replication, key, operator, monitoring, billing, and provider dependencies. Define failure model, service objectives, traffic/failover control, consistency, recovery point/time, capacity headroom, and return path. Exercise loss of each provider and shared dependencies, including partial control-plane failures, stale data, credential failure, quota, and corrupted release. Common code, identity, DNS, data, organization, or operator dependencies may defeat independence. Passing one failover exercise supports only its tested conditions.

### Answer 5

Begin with mission journeys and hazards: intake availability, dispatch decision support, alert timeliness and accessibility, responder authentication, map freshness, evidence integrity, correction, public-record retention, and continuity under regional, network, provider, cyber, power, and surge events. Classify data and authority; set latency, service, recovery, offline, capacity, location, sovereignty, interoperability, audit, cost, procurement, and exit requirements before selecting service models. Consider SaaS for bounded collaboration, PaaS for supported applications, IaaS for unusual control, and private/community/public/hybrid deployment per need—without forcing one model across every function.

Map provider and agency duties for identity, authorization, data quality, keys, network, application, configuration, logging, backup, recovery, legal process, incident notification, support, and termination. Design degraded manual/offline modes, duplicate and delayed intake handling, alert correction/cancellation, geospatial freshness, evidence chain, provider/control-plane outage, capacity exhaustion, compromised credentials, and cross-cloud recovery. Evidence includes standards and contract review, configuration inspection, security/privacy testing, accessibility and multilingual validation, load/surge tests, regional and dependency failure exercises, restore and exit rehearsals, data reconciliation, audit reconstruction, tabletop and field exercises, and monitored pilots.

Named reviewers include dispatchers and incident commanders, police/fire/emergency medical services, public-warning authorities, geospatial specialists, field responders, accessibility and multilingual communication experts, records/evidence officials, cybersecurity and privacy teams, network/cloud/distributed-system/reliability engineers, legal and procurement authorities, telecom and provider representatives, safety and human-factors experts, regulators and affected jurisdictions/communities, plus independent operational and technical assurance. Automation cannot establish emergency doctrine, jurisdictional authority, understandable public action, lawful evidence handling, responder safety, or field readiness; no external acceptance is claimed.
