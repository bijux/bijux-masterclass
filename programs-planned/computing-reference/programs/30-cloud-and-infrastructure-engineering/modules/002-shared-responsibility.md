---
module_id: CLOUD-002
program: Cloud & Infrastructure Engineering
level: 1
module_number: 2
title: Shared Responsibility
status: complete
last_verified: 2026-08-29
---

# Shared Responsibility

## One-Page Review

### Governing question

For every required cloud outcome, which actor performs the work, which actor remains accountable, what interface joins their work, and what evidence shows that no obligation has been lost at the boundary?

### Essential definitions

- A **responsibility** is an obligation to perform, decide, approve, monitor, respond, or provide evidence for a defined outcome.
- **Accountability** is the retained answerability for whether an outcome is acceptable; outsourcing performance does not automatically transfer accountability.
- The **shared responsibility model** allocates cloud-related duties among a cloud service provider, cloud service customer, and other actors according to the exact service, contract, configuration, and operating context.
- A **control objective** states the outcome required; a **control implementation** is the mechanism and procedure intended to achieve it.
- **Inherited control** means one actor relies on a control implemented by another within an explicit scope and supported by evidence.
- **shared** must be decomposed into complementary duties. It must never mean that either party may assume the other will act.
- A **responsibility assignment matrix** maps each obligation to performers, an accountable owner, consulted parties, informed parties, interfaces, evidence, and escalation.
- A **boundary control** governs interaction between actors or systems: identity federation, logging delivery, key use, incident notification, support escalation, backup export, or change communication.
- A **residual risk** is risk remaining after selected controls; a customer retains the duty to understand, accept, transfer, avoid, or reduce it through authorized governance.

### Central model, mechanism, or theorem

Let (O) be required obligations and (A) the actors in a cloud system. For every (o in O), a usable assignment records at least one performer (P(o)), exactly one accountable customer-side authority (a(o)), provider and customer interfaces (I(o)), evidence (E(o)), and escalation (X(o)). Coverage requires (P(o) != empty), (a(o) in A), and an evidence path for every applicable obligation. The provider may operate a mechanism, but the customer still determines whether the combined service meets its mission, legal duties, risk tolerance, and continuity needs. Responsibility therefore shifts with IaaS, PaaS, and SaaS; it does not disappear.

### Critical invariants

Classify the exact service before assigning work. Separate control objective from implementation. Distinguish provider, customer organization, platform team, workload team, user, supplier, auditor, and regulator where applicable. Give every obligation one accountable owner and explicit performers. Expand every “shared” cell into complementary verbs. Treat data, identity, configuration, workload behavior, lawful use, monitoring, recovery, and exit as enduring customer concerns even when provider capabilities support them. Verify inherited controls by scope, evidence, exceptions, and validity period. Cover security, privacy, reliability, operations, cost, compliance, incident response, and lifecycle—not security alone. Revisit assignments after service, architecture, contract, organization, threat, or regulation changes.

### Common failures

Teams copy a generic layer diagram; confuse provider capability with enabled protection; infer compliance from provider certification; make “shared” ownerless; assign a department rather than an accountable role; ignore SaaS configuration and data; assume an SLA guarantees workload availability; omit client endpoints, connectivity, integrations, support, deletion, and exit; fail to map subcontractors; retain no provider evidence; or discover responsibilities only during an incident.

### Compact example

A managed database provider patches the service engine and offers encrypted storage, backup, replicas, audit export, and recovery interfaces. The customer still selects topology, enables and scopes encryption and logs, manages identities, classifies data, tests restore, protects application credentials, monitors workload symptoms, and decides whether the service satisfies recovery and legal requirements. “Managed database” transfers mechanisms; it does not prove a recoverable or compliant application.

### Connections

The prerequisite is [Cloud Service and Deployment Models](001-cloud-service-and-deployment-models.md), because the service boundary changes assignment. Successors apply this model to global infrastructure, control planes, managed services, identity, resilience, operations, governance, and migration. Cybersecurity contributes control and assurance reasoning; software architecture contributes system boundaries; platform engineering divides provider, platform, and workload duties; reliability engineering tests operational outcomes.

## Governing Question

How can an organization turn a broad cloud shared-responsibility diagram into an exact, testable operating agreement for a real workload?

The answer is not a universal stack colored “provider” and “customer.” It is a maintained set of obligation records derived from requirements, architecture, service contracts, provider documentation, organizational roles, and evidence. The records must explain who does what, where handoffs occur, how performance is verified, and who acts when an assumption fails.

## Why This Matters

Cloud services move mechanisms across organizational boundaries. A provider may operate buildings, hosts, hypervisors, runtimes, databases, or an entire application. Customers gain leverage but cannot directly inspect everything they depend upon; providers cannot know each customer's data meaning, business tolerance, application logic, or legal context.

Shared responsibility is the discipline for making that dependency governable. AWS describes security and compliance as shared and distinguishes security “of” its cloud from customer security “in” it. Microsoft publishes different responsibility allocations for on-premises, IaaS, PaaS, and SaaS while retaining customer duties for data, identities, accounts, access, configuration, and endpoints. Google emphasizes that every service has a distinct configuration profile and extends responsibility language with “shared fate,” in which the provider supplies opinionated guidance and secure foundations. These formulations are useful, but none replaces the exact service contract and architecture.

The topic is broader than security. For reliability, providers operate infrastructure while customers design workloads and test recovery. For privacy, providers supply processing mechanisms while customers determine purpose, data, retention, access, and lawful use. For cost, providers meter services while customers control architecture, demand, commitments, and anomaly response. During incidents, each party detects different signals and exchanges information through contractual channels.

A missing assignment appears at the worst time: nobody enables audit export, tests restore, configures legal hold, or rejects a long-lived credential. Every component can behave as documented while the combined system fails.

NIST SP 800-144 addresses accountability when outsourcing to public cloud. CISA warns that allocations differ by provider and change over time. The Cloud Security Alliance's Cloud Controls Matrix 4.1 gives provider-neutral control and ownership guidance. These are analysis baselines, not attestations about one deployment.

## Prerequisites and Retrieval

Retrieve the service and deployment models from Module 001; confidentiality, integrity, availability, privacy, risk, threat, vulnerability, control, identity, authorization, encryption, backup, recovery, monitoring, service-level objective, contract, and evidence. Distinguish:

- a desired outcome from a product feature;
- the party that performs work from the party answerable for the result;
- design-time claims from runtime evidence;
- service availability from workload availability;
- a provider certification from customer-system compliance; and
- a generic service category from an exact service, tier, region, and configuration.

No provider console or certification is required. Examples use generic services so the reasoning survives product changes.

## Learning Objectives

By the end of this module, you should be able to:

1. explain why cloud responsibility moves but does not vanish;
2. distinguish responsibility, accountability, control objective, implementation, inheritance, assurance, and residual risk;
3. derive assignments from an exact service and workload rather than a generic layer picture;
4. decompose a “shared” label into complementary provider and customer duties;
5. model provider, customer, internal teams, users, suppliers, auditors, and authorities without losing ownership;
6. build and validate an obligation register with interfaces, evidence, and escalation;
7. reason about security, privacy, reliability, operations, cost, and lifecycle together;
8. identify gaps, overlaps, invalid inheritance, and changes that invalidate an assignment;
9. evaluate provider evidence without treating it as universal compliance proof; and
10. escalate high-consequence legal, safety, privacy, and continuity judgments to named authorized humans.

## Core Exposition

Begin with the cloud relationship. A **cloud service provider** makes a service available. A **cloud service customer** acquires and uses it. Real systems add customer business owners, cloud administrators, platform teams, workload teams, data owners, security operations, privacy and legal functions, network carriers, managed-service partners, software suppliers, auditors, regulators, and end users. One company can occupy several roles: a central platform group is a customer of a public cloud and a provider of internal capabilities to application teams.

A responsibility statement needs a verb and object. “Customer: data” is too vague. “The data owner classifies records,” “the platform team enforces encryption,” and “security operations reviews access alerts” are actionable. Each statement names scope, timing, owner, performer, evidence, and failure response.

**Accountability does not equal execution.** A provider can execute physical security and hypervisor patching. A customer executive or system owner remains accountable for selecting a service whose provider controls and evidence are adequate for the workload. Within the customer, a platform team can execute organization-wide guardrails while a workload owner remains accountable for application risk. Avoid assigning two “accountable” actors to one obligation; split the obligation if two decisions genuinely exist.

**Control objectives and implementations differ.** “Only authorized subjects access production data” is an objective. Identity APIs, role definitions, federation, workload authorization, reviews, and alerts are implementations. The provider secures its plane and exposes IAM; the customer configures permissions; the application may enforce record-level access. Coloring all “identity” one color loses these duties.

**Inheritance** is scoped reliance. If a provider's audited physical-access control covers datacenters supporting a named service during a named period, a customer can inherit that mechanism within those boundaries. It cannot infer that customer IAM, application authorization, or regulatory compliance is covered. Valid inheritance records the control objective, provider implementation, covered service and locations, evidence source and period, customer prerequisites, exceptions, and complementary customer controls. An assurance report can reduce uncertainty; it does not transfer the customer's decision.

Service models shift typical mechanisms. In **IaaS**, the provider usually operates facilities, physical network and compute, and virtualization, while the customer operates guest systems, applications, identities, data, and much network configuration. In **PaaS**, the provider also operates more runtime, middleware, scaling, and patching; the customer retains application code and configuration, identities, data, dependency use, and workload behavior. In **SaaS**, the provider operates the application stack, while the customer still owns tenant configuration, users, entitlements, data governance, integrations, endpoint use, workflow fit, monitoring, continuity, and exit. These statements are starting hypotheses. A managed Kubernetes service, database, analytics service, or SaaS extension platform can place individual duties differently.

Deployment model also matters. Private cloud may move provider duties to an internal infrastructure group or contractor. Community cloud adds joint governance. Hybrid and multi-provider designs multiply contracts and boundary controls. A workload may depend on a public identity provider, private network, managed database, SaaS application, and external support partner. Responsibility must follow the dependency graph rather than one vendor matrix.

Use an **obligation register**. For each required outcome, capture:

1. obligation identifier and precise result;
2. source: requirement, threat model, law, policy, architecture decision, contract, or operational need;
3. applicable service, resource, data, environment, and lifecycle stage;
4. accountable customer-side role;
5. provider, customer, partner, and user performance duties;
6. handoff interface and timing;
7. preventive, detective, responsive, and recovery mechanisms;
8. evidence producer, evidence consumer, location, cadence, and retention;
9. escalation path, deadline, and decision authority;
10. dependencies, exceptions, residual risk, approval, and review trigger.

The register connects inventory, policy, deployment checks, runbooks, evidence, provider notices, and risk review. Machines can find blank owners or expired reviews; humans judge whether obligations and evidence are adequate.

Security illustrates complementary work. The provider protects its personnel, facilities, hardware, service software, and privileged administration according to the service. The customer selects approved services, protects customer identities, configures resources, hardens customer-controlled software, classifies data, manages application authorization, collects relevant telemetry, and responds to its incidents. Both sides manage vulnerabilities in different layers and exchange incident information. A customer error does not prove provider security; a provider certification does not make a publicly exposed customer resource safe.

Privacy and data governance begin before deployment. The customer determines purposes, data categories, lawful basis where applicable, minimization, retention, data-subject processes, access, acceptable locations, and downstream disclosure. The provider implements contracted processing, location, protection, deletion, and assistance mechanisms. Customer teams must configure and exercise those mechanisms. Subprocessors and support access create further actors. No infrastructure engineer should independently decide that a service is legally permissible merely because it advertises encryption or a certification.

Reliability separates platform capability from workload outcome. A provider may design a service for an availability target and supply zones, replicas, backups, health signals, and support. The customer chooses topology, removes single points of failure in its design, sizes capacity and quotas, sets recovery objectives, handles provider API failure, protects data, and runs restoration and failover exercises. An SLA describes contractual terms and possible remedy under stated conditions; it is not proof that the application meets its service objective or that business loss is bounded.

Operational responsibility spans routine and exceptional work: provisioning, configuration, patching, certificate and secret rotation, capacity, quota, observation, alert response, changes, deprecation, support, incident coordination, forensics, backup, recovery, and deletion. Managed services remove some procedure execution, but the customer still watches service health, consumes notices, maintains contacts, validates configuration, and integrates evidence into operations.

Economic responsibility also has a handoff. Providers define meters, prices, invoices, and discount instruments. Customers choose architecture, tag ownership, forecast demand, approve commitments, detect anomalies, and remove waste. Only the customer knows whether consumption creates value.

The following executable check models a small register. It demonstrates structural coverage, not the correctness of the assignments.

<!-- bijux-verify: {"id":"cloud-responsibility-register-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"obligations=4\ncomplete=3\ngaps=1\ngap_ids=['COST-01']\nshared_duties=3\n","stderr":""}} -->
```python
obligations = [
    {
        "id": "IAM-01",
        "accountable": "system_owner",
        "performers": ["provider", "identity_team", "workload_team"],
        "evidence": ["provider_assurance", "role_review"],
        "escalation": "security_duty_manager",
    },
    {
        "id": "REC-01",
        "accountable": "service_owner",
        "performers": ["provider", "workload_team"],
        "evidence": ["restore_test"],
        "escalation": "continuity_owner",
    },
    {
        "id": "LOG-01",
        "accountable": "security_owner",
        "performers": ["provider", "platform_team"],
        "evidence": ["delivery_probe", "retention_report"],
        "escalation": "security_duty_manager",
    },
    {
        "id": "COST-01",
        "accountable": "",
        "performers": ["provider"],
        "evidence": [],
        "escalation": "",
    },
]

required = ("accountable", "performers", "evidence", "escalation")
gaps = [
    item["id"]
    for item in obligations
    if any(not item[field] for field in required)
]
shared_duties = sum(
    "provider" in item["performers"] and len(item["performers"]) > 1
    for item in obligations
)

print(f"obligations={len(obligations)}")
print(f"complete={len(obligations) - len(gaps)}")
print(f"gaps={len(gaps)}")
print(f"gap_ids={gaps}")
print(f"shared_duties={shared_duties}")
```

Execution proves only that the four synthetic records satisfy the encoded non-emptiness rule and that the reported counts follow from the data. It does not prove that the obligations are complete, assignments are authorized, provider evidence is valid, controls work, risks are acceptable, or any real cloud system is secure, private, reliable, compliant, or cost-effective.

Responsibility needs **evidence paths**. Provider evidence includes service documentation, assurance reports, service health, notices, support records, and commitments. Customer evidence includes configuration, access reviews, audit logs, alert tests, restore results, exercises, invoices, and risk approvals. Judge provenance, scope, independence, freshness, completeness, and relevance.

An audit opinion has boundaries. Read the system description, included services and regions, control period, criteria, complementary user-entity controls, subservice treatment, exceptions, and auditor opinion. A certification often demonstrates that a management system or defined scope met criteria; it does not certify the customer's configuration or application. Marketing badges are indexes to evidence, not evidence substitutes.

Shared responsibility changes over time. Providers add features, change defaults, retire interfaces, add regions or subprocessors, and revise terms. Customers change architecture, data, teams, risk, integrations, and usage. Create review triggers for new service adoption, major version or tier change, new data classification, material incident, provider control exception, expired assurance, regulation change, ownership transfer, and recovery-test failure. Periodic review catches silent drift, but event-driven review is equally important.

During incidents, generic ownership is too slow. Define detection sources, severity translation, provider support entitlement, authorized case openers, required artifacts, secure communication, notification deadlines, decision authority, evidence preservation, status cadence, public communication, recovery validation, and post-incident follow-up. Provider and customer timelines must be correlated without assuming either clock or log is complete.

Finally, distinguish **responsibility from blame**. The model exists to enable prevention and coordinated action. After failure, ask whether duties were explicit, feasible, resourced, evidenced, and exercised; whether interfaces and assumptions held; and whether organizational incentives encouraged silence. Blame-oriented matrices produce defensive gaps. Outcome-oriented agreements produce testable boundaries.

## Definitions and Notation

Let (A) be actors, (O) obligations, (S) exact services, and (R) resources. An obligation (o) has scope (scope(o) subseteq S times R), source (src(o)), performer set (P(o) subseteq A), accountable owner (a(o) in A), interface set (I(o)), evidence set (E(o)), and escalation (X(o)).

A structurally covered obligation satisfies:

(covered(o) = applicable(o) implies (P(o) != empty and a(o) != empty and I(o) != empty and E(o) != empty and X(o) != empty)).

“Exactly one accountable owner” is an operating invariant, not a theorem about organizations. If two authorities make different decisions, define two obligations. Several performers may cooperate. A provider, customer, or partner may both perform and provide evidence.

A **RACI** matrix labels Responsible, Accountable, Consulted, and Informed roles. It can support communication but omits control source, scope, provider/customer split, evidence, interface, timing, and escalation unless extended. A **complementary customer control** is a customer action assumed by a provider control environment. A **complementary subservice control** concerns another service organization. A **service-level agreement (SLA)** states contractual commitments and remedies; a **service-level objective (SLO)** is a target for service behavior. Neither alone assigns all reliability work.

**Assurance** is justified confidence based on evidence. **Attestation** is a claim by a responsible party, sometimes examined by an independent practitioner. **Certification** confirms conformity within a stated scheme and scope. **Compliance** is satisfaction of applicable obligations by the evaluated subject. These are related but not interchangeable.

## Mechanisms, Invariants, or Proof Structure

Use this derivation:

1. **Bound the system.** Inventory exact services, tiers, regions, accounts, data, identities, networks, endpoints, integrations, suppliers, and lifecycle stages.
2. **Elicit obligations.** Derive outcomes from mission, threats, architecture, law, policy, contract, operations, resilience, cost, and exit.
3. **Read primary sources.** Inspect current provider service documentation, terms, SLAs, assurance scope, notices, and customer prerequisites.
4. **Decompose controls.** Separate objective from provider mechanisms, customer mechanisms, partner mechanisms, and boundary controls.
5. **Assign actors.** Name one accountable customer authority, all performers, consulted specialists, evidence producers and consumers, and escalation.
6. **Trace interfaces.** Specify configuration APIs, identity trust, log delivery, support, notification, export, recovery, deletion, and change channels.
7. **Attach evidence.** Require evidence with scope, cadence, retention, owner, and failure response.
8. **Find gaps and overlaps.** Reject no-owner, no-performer, no-evidence, conflicting-action, and unjustified-inheritance records.
9. **Exercise the agreement.** Test provisioning, access review, alert delivery, support escalation, restore, provider impairment, credential compromise, and exit as applicable.
10. **Govern change.** Monitor provider and customer changes and reauthorize residual risk.

Check invariants:

- the assignment names an exact service and configuration, not only IaaS/PaaS/SaaS;
- every applicable obligation has a customer-side accountable authority;
- “shared” is expanded into non-overlapping or deliberately coordinated verbs;
- provider capability is distinguished from customer enablement and use;
- inherited evidence matches service, region, control, period, and prerequisites;
- every cross-boundary dependency has a technical or organizational interface owner;
- security, privacy, reliability, operations, economics, incident response, and exit are covered;
- SLA remedies are not mistaken for workload resilience;
- certifications are not extended beyond their scope;
- changes and exceptions trigger review;
- evidence failure creates an action, not a silently green status; and
- high-consequence judgments have named authorized human reviewers.

The completeness argument is a reviewable trace, not a mathematical proof of safety. Requirements generate obligations; each applicable obligation maps to actors, mechanisms, evidence, and escalation; tests challenge representative boundaries; residual risks receive authorized decisions. Counterexamples—such as an unowned restore, inaccessible log, expired report, or undocumented subprocessor—falsify a completion claim. Passing structural checks supports consistency but cannot establish that the requirement set is exhaustive.

## Alternatives and Trade-Offs

A **generic provider matrix** is fast and educational. It helps teams understand how duties usually shift by service model. It is too coarse for operational approval. Use it as an index into service-specific documentation, never as the final agreement.

A **RACI matrix** is familiar and compact. It clarifies internal communication but becomes enormous and ambiguous when one row says “security” or “backup.” An obligation register costs more to maintain but captures scope, evidence, interfaces, and triggers. A practical design uses a concise RACI view generated from richer records.

**Centralized ownership** can standardize identity, networking, guardrails, evidence, and provider relationships. It can also create bottlenecks and distance decision makers from workload meaning. **Federated ownership** gives workload teams autonomy and context but can duplicate controls and create inconsistent coverage. A platform model often centralizes safe foundations and evidence while workload teams retain application and data outcomes.

**Preventive guardrails** reject unsafe configurations before deployment. They provide fast, repeatable coverage but cannot encode every contextual judgment. **Detective controls** observe drift and behavior but allow a window of exposure. **Manual review** handles nuance but is slower and inconsistent without criteria. Mature systems layer them and name who responds when each fails.

**Provider-native controls** can integrate deeply and reduce operating burden. **Independent controls** can offer cross-provider consistency and evidence outside the failure domain. Independence adds integration, cost, privilege, and data paths. Choose according to threat, assurance, portability, and operational capacity rather than a universal preference.

**Shared fate** usefully asks providers to help customers achieve secure outcomes through defaults, blueprints, guidance, and partnership. It does not erase the need for precise assignments, contracts, customer authorization, or residual-risk decisions. Treat it as a stronger cooperation posture built on explicit responsibility.

## Failure Modes and Misconceptions

- **“The provider handles security.”** Providers handle defined layers and controls; customers retain service selection, identity, data, configuration, application, monitoring, and risk duties.
- **“The customer owns everything in the cloud.”** The provider also has material duties. Pretending otherwise prevents valid inheritance and coordinated response.
- **“Shared means fifty-fifty.”** Duties divide by mechanism and authority, not equal percentages.
- **“Both teams are accountable.”** Dual accountability often means neither can decide. Split obligations or name one authority.
- **“The feature exists, so the control works.”** Availability, enablement, correct configuration, monitoring, and exercise are distinct.
- **“Managed means backed up.”** A provider snapshot feature may not meet retention, isolation, restore, or business recovery requirements.
- **“An SLA guarantees our application.”** SLA scope, exclusions, measurement, architecture prerequisites, and remedies differ from workload objectives.
- **“Provider compliance makes us compliant.”** Provider evidence covers a defined subject; customer processing, configuration, and complementary controls remain.
- **“SaaS leaves nothing technical to operate.”** Tenant settings, identity, endpoints, integrations, logs, retention, export, and incident channels remain.
- **“Responsibility ends at deployment.”** Patch, change, deprecation, evidence renewal, incident, recovery, deletion, and exit extend through the lifecycle.
- **“A spreadsheet is governance.”** Records without enforcement, evidence, tests, review triggers, and escalation are documentation theater.
- **“Responsibility analysis can approve legal or safety risk.”** Engineers produce evidence; authorized domain experts and accountable leaders make high-consequence judgments.

## Worked Examples

### Example 1

**Question:** Who patches a web application running on an IaaS virtual machine?

**Reasoning:** The provider normally patches physical hosts and the virtualization layer. The customer normally patches the guest operating system, installed runtime, libraries, and application. An image supplier may publish updates, while the workload team must rebuild and deploy them. The system owner owns the risk decision; security may define deadlines and verify evidence.

**Conclusion:** “Patching is shared” expands into layer-specific publication, deployment, verification, and escalation duties.

### Example 2

**Question:** A provider encrypts object storage by default. Is the data-protection obligation complete?

**Reasoning:** Default encryption covers a provider mechanism at rest. The customer must still classify data; choose service, region, key and access models; authorize identities; protect data in clients and transit; set retention; monitor access; and validate deletion. If customer-managed keys are chosen, availability and rotation duties increase.

**Conclusion:** One inherited mechanism cannot stand for the whole data-protection objective.

### Example 3

**Question:** A managed database advertises daily backups. Can the team claim a 30-minute recovery-point objective and a two-hour recovery-time objective?

**Reasoning:** Daily backup cannot by itself meet a 30-minute RPO. The team must select suitable replication or point-in-time recovery, verify retention and failure-domain independence, provision permissions and capacity, define application reconciliation, and run timed restores. Provider service availability and customer recovery workflow are complementary.

**Conclusion:** Recovery claims require architecture and exercise evidence, not a backup checkbox.

### Example 4

**Question:** Why is “IAM: shared” an unusable matrix row?

**Reasoning:** The provider secures its workforce identities and implements service authentication and authorization mechanisms. The customer federates workforce identity, manages lifecycle and roles, constrains privileged access, configures workload identity, and reviews activity. The application may enforce business-object authorization. Each duty has different evidence and escalation.

**Conclusion:** Decompose a broad domain until each obligation has an observable verb and owner.

### Example 5

**Question:** What can a provider audit report establish?

**Reasoning:** It can support reliance on described controls for included services, locations, systems, criteria, and period, subject to exceptions, complementary controls, and any subservice carve-outs. It cannot establish the customer's configuration, current state after the period, application correctness, or compliance with requirements outside scope.

**Conclusion:** Assurance is scoped evidence, not a transferable compliance label.

### Example 6

**Question:** A SaaS employee system is fully provider-operated. What remains with the customer?

**Reasoning:** The customer decides lawful use, accepted data, user lifecycle, roles, tenant settings, integrations, endpoint security, retention, exports, support access, monitoring, continuity, and exit. The provider operates application and infrastructure according to contract. Human-resources, privacy, security, procurement, and system owners still have distinct decisions.

**Conclusion:** SaaS moves application operation while retaining substantial organizational and configuration responsibility.

### Example 7

**Question:** Two internal teams both believe the other owns log delivery from cloud accounts.

**Reasoning:** The platform team created the organization sink; the security team created the analysis service; neither owns delivery tests or failure response. Define separate obligations: platform configures and probes export, security validates ingestion and alerting, and one security service owner is accountable for end-to-end detection evidence.

**Conclusion:** Boundary controls need end-to-end accountability even when components have local owners.

### Example 8

**Question:** A serverless service removes server management. Which reliability duties remain?

**Reasoning:** The provider operates hosts, runtime scheduling, and documented service behavior. The customer designs idempotency, timeout and retry behavior, concurrency limits, dependency handling, data durability, observability, regional strategy, quota response, and recovery. Provider scaling cannot repair non-idempotent business logic or an exhausted downstream database.

**Conclusion:** Managed execution changes mechanisms but not responsibility for workload behavior.

### Example 9

**Question:** A hospital wants to process identifiable clinical data in a new cloud analytics service. Can a passing technical matrix approve production use?

**Reasoning:** The matrix can show encryption, identities, locations, logs, deletion, incident interfaces, provider evidence, and gaps. It cannot determine lawful basis, clinical safety impact, contractual sufficiency, acceptable residual risk, or whether data minimization is adequate. Named privacy, legal, clinical-safety, security, data, and accountable business reviewers must examine current evidence.

**Conclusion:** Technical validation informs but never impersonates authorized high-consequence review.

### Example 10

**Question:** A provider announces retirement of an audit-log export API in 90 days. Whose responsibility is continuity?

**Reasoning:** The provider owns accurate notice and replacement documentation according to contract. The platform team owns inventory and migration of export configuration; security owns validation that required events arrive and alerts still work; procurement checks contractual implications; the system owner accepts any temporary evidence gap. A trigger in the register opens and tracks these actions.

**Conclusion:** Change management is a shared, time-bounded obligation with explicit evidence and escalation.

## Cross-Program Connections

- [Cloud Service and Deployment Models](001-cloud-service-and-deployment-models.md) supplies the service-boundary vocabulary on which responsibility assignments depend.
- [Assets, Adversaries, Trust, and Security Goals](../../25-security-engineering/modules/001-assets-adversaries-trust-and-security-goals.md) explains why a control claim requires scope and evidence.
- [Architecture as Significant Design Decisions](../../12-software-engineering-software-architecture/modules/001-architecture-as-significant-design-decisions.md) frames cloud boundaries as decisions with consequences and assumptions.
- [Platform Engineering as Complexity Management](../../29-platform-engineering/modules/001-platform-engineering-as-complexity-management.md) shows how an internal platform becomes both cloud customer and capability provider.
- [From Source Change to Deployable Artifact](../../14-software-engineering-software-delivery-and-reliability-engineering/modules/001-from-source-change-to-deployable-artifact.md) connects ownership and evidence across delivery boundaries.
- [Systems, Boundaries, Environments, and Context](../../26-systems-engineering/modules/001-systems-boundaries-environments-and-context.md) helps discover actors and lifecycle obligations that a technology-only matrix misses.

## References

1. Peter Mell and Timothy Grance, “The NIST Definition of Cloud Computing,” NIST SP 800-145, September 2011, [official publication and DOI](https://csrc.nist.gov/pubs/sp/800/145/final).
2. Wayne Jansen and Timothy Grance, “Guidelines on Security and Privacy in Public Cloud Computing,” NIST SP 800-144, December 2011, [official publication and DOI](https://csrc.nist.gov/pubs/sp/800/144/final).
3. CISA, USDS, and FedRAMP, “Cloud Security Technical Reference Architecture,” version 2, June 2022, [official CISA publication](https://www.cisa.gov/resources-tools/resources/cloud-security-technical-reference-architecture).
4. Cloud Security Alliance, “Cloud Controls Matrix and CAIQ v4.1,” released January 27, 2026, [official framework package](https://cloudsecurityalliance.org/artifacts/cloud-controls-matrix-v4-1).
5. Cloud Security Alliance, “Introductory Guidance to CCM,” released February 13, 2026, [official shared-responsibility guidance](https://cloudsecurityalliance.org/artifacts/introductory-guidance-to-ccm).
6. Amazon Web Services, “Shared Responsibility Model,” accessed August 29, 2026, [official documentation](https://aws.amazon.com/compliance/shared-responsibility-model/).
7. Microsoft, “Shared responsibility in the cloud,” updated July 24, 2026, [official Azure documentation](https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility).
8. Microsoft, “Shared Responsibility for Reliability,” updated June 1, 2026, [official Azure reliability documentation](https://learn.microsoft.com/en-us/azure/reliability/concept-shared-responsibility).
9. Google Cloud, “Shared responsibilities and shared fate on Google Cloud,” last reviewed August 21, 2023, [official architecture guidance](https://cloud.google.com/architecture/framework/security/shared-responsibility-shared-fate).
10. AICPA, “SOC 2 — SOC for Service Organizations: Trust Services Criteria,” accessed August 29, 2026, [official overview](https://www.aicpa-cima.com/resources/landing/system-and-organization-controls-soc-suite-of-services).

## Exercises

### Exercise 1

Define responsibility, accountability, control objective, control implementation, inherited control, and residual risk. Explain why “the provider is compliant” does not establish that a customer's workload is compliant.

### Exercise 2

For an application on IaaS, derive complementary duties for guest patching, network access, data encryption, audit logging, and incident response. Name provider and customer work, evidence, and escalation.

### Exercise 3

A managed database has automated backups and an availability SLA. Diagnose the evidence required before claiming a four-hour RTO and one-hour RPO. Identify at least two gaps a generic provider matrix would miss.

### Exercise 4

Compare a generic RACI matrix with an obligation register for a SaaS human-resources system. Design a minimum useful record schema and explain the maintenance trade-off.

### Exercise 5

A municipal benefits agency proposes using a new cloud document-analysis service for applications containing identity, income, disability, and family data. Construct a responsibility-review plan covering data, identity, provider evidence, reliability, incidents, deletion, cost, change, and exit. State which claims automation may check and which require named human authorities.

## Answers to the Exercises

### Answer 1

A responsibility is an obligation to perform or decide defined work. Accountability is answerability for the outcome and authority to resolve it. A control objective states the required result; an implementation is a mechanism and procedure intended to achieve it. An inherited control is reliance on another actor's implementation within explicit scope and evidence. Residual risk remains after controls and requires authorized treatment. A provider compliance or certification claim has a subject, criteria, service scope, locations, period, exceptions, and complementary customer controls. The customer's identities, configuration, application, data use, integrations, and legal obligations lie outside some or all of that scope. Workload compliance therefore requires mapping provider evidence and customer evidence to the customer's exact requirements.

### Answer 2

For guest patching, the provider patches hosts and virtualization; the customer inventory owner rebuilds or patches guests, and evidence includes provider assurance plus image age and deployment reports. Security escalation follows missed deadlines. For network access, the provider operates isolation and policy APIs; the customer network owner defines segmentation and workload teams request least privilege; evidence includes configuration evaluation and flow tests. For encryption, the provider supplies cryptographic service mechanisms while the data and platform owners choose scope, keys, access, and rotation; evidence includes configuration and key-use logs. For audit logging, the provider emits documented events while the platform exports them and security validates delivery, retention, and alerts. For incidents, both detect their layers, preserve evidence, and communicate through tested support channels; the customer incident commander owns customer response. Exact service documentation and contract can shift these assignments.

### Answer 3

The team needs a business-approved RTO and RPO definition, exact backup and point-in-time recovery behavior, retention and isolation, failure-domain and regional scope, permissions, encryption-key availability, quota and replacement capacity, application dependency order, data reconciliation, runbooks, alerting, and repeated timed restore evidence. It must understand SLA measurement, exclusions, prerequisites, and remedies without equating them to recovery. Generic matrices miss whether backups meet a one-hour RPO, whether a usable target can be provisioned within four hours, whether keys and dependencies survive, and whether the application can verify recovered data. Provider capability plus a successful representative customer exercise supports a bounded claim; neither guarantees every disaster.

### Answer 4

A generic RACI is a compact communication view but invites rows such as “data” or “security,” loses service scope and evidence, and ages poorly. A minimum obligation record should include identifier, outcome, source, scope, accountable owner, performers with explicit verbs, interface, evidence producer and consumer, cadence, escalation, dependencies, exception or residual risk, and review triggers. For SaaS HR, records should cover user lifecycle, role review, data categories, retention, legal hold, integration credentials, endpoint use, logs, support access, incidents, export, deletion, continuity, and exit. Rich records cost more to establish and update, so generate concise views from them and automate structural checks. The added maintenance is justified where an unowned boundary could create material harm.

### Answer 5

First inventory exact service, regions, subprocessors, model use, training-data terms, documents, identities, integrations, support paths, logs, and lifecycle. Map obligations for purpose limitation, minimization, lawful processing, classification, access, encryption, key ownership, model and output handling, accuracy limits, human decision review, retention, deletion, audit, notification, recovery, capacity, spend, provider change, export, termination, and verified disposal. Assign one agency authority for each outcome; decompose provider, platform, security, case-system, records, procurement, and user duties; and attach current evidence and exercises. Automation may check complete records, configuration policies, identity rules, log arrival, retention settings, budget alerts, backup jobs, expiry dates, and export test results. It cannot determine lawful basis, discrimination risk, accessibility, acceptable decision error, contractual adequacy, harm tolerance, or residual-risk acceptance. Named privacy, legal, benefits-policy, records, accessibility, security, procurement, continuity, and accountable executive reviewers must approve within their authority. No external or human review is claimed by this model answer; production approval requires actual named review records.
