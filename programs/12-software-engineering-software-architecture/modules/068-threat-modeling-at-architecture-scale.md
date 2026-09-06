---
module_id: SARCH-068
program: Software Engineering: Software Architecture
level: 2
module_number: 68
title: Threat Modeling at Architecture Scale
status: complete
last_verified: 2026-09-06
---

# Threat Modeling at Architecture Scale

## One-Page Review

### Governing question

How can an architecture team reason systematically about adversarial paths across identities, data, software, infrastructure, suppliers, operators, and recovery without mistaking a diagram, checklist, or risk score for security assurance?

### Essential definitions

- an **asset** is something stakeholders value; a **protection need** states the required security property and consequence;
- a **threat** is a circumstance or event with potential adverse impact; a **threat actor** has modeled objectives, access, capability, resources, and constraints;
- a **vulnerability** is a weakness that can be exploited or triggered; an **attack path** is a sequence of conditions and actions leading to an adversarial objective;
- a **trust boundary** is where authority, identity, integrity, confidentiality, or assumptions change—not merely a network segment;
- an **attack surface** is the set of reachable interaction points and conditions available to an adversary;
- an **abuse case** describes intentionally harmful use; a **misuse case** describes use outside intended policy or assumptions;
- an **attack tree** decomposes an adversarial goal into alternative and jointly required subgoals;
- **control coverage** maps preventive, detective, responsive, and recovery mechanisms to specific paths and outcomes;
- **residual risk** is risk remaining after implemented controls and evidence;
- **threat-model drift** is divergence between the model and the deployed system, operation, dependency, or threat environment.

### Central model, mechanism, or theorem

Represent the architecture as typed graphs over assets, actors, identities, authorities, data states, processes, interfaces, deployments, and suppliers. An attack path is feasible only when every required precondition and transition is feasible; alternative paths are OR choices, while jointly required subgoals are AND choices.

For events $A$ and $B$,

$$
P(A\cup B)=P(A)+P(B)-P(A\cap B).
$$

This elementary identity exposes why adding path likelihoods double-counts overlap. In practice, adversarial likelihoods and dependence are rarely known well enough for precise probability multiplication. Architecture threat models should expose assumptions, ordinal uncertainty, and consequence rather than decorate guesses with decimals.

### Critical invariants

- scope includes lifecycle, control, management, build, recovery, and retirement paths;
- every diagram identifies version, environment, trust boundary, authority, and missing knowledge;
- authentication, authorization, identity proofing, session state, and audit remain distinct;
- data is modeled at creation, transit, processing, storage, backup, restore, export, and deletion;
- attacker goals and preconditions are explicit rather than inferred from a category label;
- catalog coverage never becomes completeness;
- controls map to paths, failure modes, evidence, owners, and bypass conditions;
- compromised-admin and compromised-control-plane scenarios remain in scope;
- safety, privacy, accessibility, fraud, abuse, and legal harms are not reduced to confidentiality alone;
- the model changes with architecture and drives verification work.

### Common failures

Common failures include drawing only a data-flow diagram; treating an internal network as trusted; listing STRIDE words without scenarios; starting from CVEs instead of stakeholder harm; omitting administrators, CI/CD, suppliers, support, backups, observability, and recovery; trusting managed services by label; assuming encryption resolves authorization; scoring ordinal likelihood and impact as precise arithmetic; treating ATT&CK or CAPEC coverage as completeness; assigning controls without attack-path mapping; and updating the model only before release.

### Compact example

A support service may legitimately read customer metadata but not production secrets. If an attacker can socially engineer support, reset an administrator identity, mint a production session, and read secrets, the decisive boundaries are human proofing and authority delegation—not the public API firewall. Controls must interrupt that path through strong recovery proofing, limited support capability, independent approval, short-lived credentials, audit, and tested revocation.

### Connections

[SARCH-067](067-availability-and-reliability-models.md) distinguishes accidental failure, adversarial fault, and recovery evidence. [SARCH-069](../ROADMAP.md) next models cost and unit economics. Security Engineering owns deep attack and control disciplines; this module owns their integration into system-wide architecture decisions.

## Governing Question

Threat modeling asks what stakeholders need protected, what the system actually is, what an adversary can cause, and what the architecture will do about it. At architecture scale, the answer crosses organizational and technical boundaries: product, identity, data, build, cloud, physical sites, operators, vendors, customers, and recovery.

The outcome is a maintained set of falsifiable security requirements, attack hypotheses, controls, evidence plans, and accepted residual risks. The diagram is an input, not the deliverable.

## Why This Matters

Local secure coding cannot repair an architecture that grants one identity global authority, makes every tenant share a failure domain, trusts unsigned deployment inputs, exposes recovery through weaker proofing, or cannot revoke compromised control. Architecture determines reachable paths and blast radius before a line-level vulnerability is considered.

Threats also interact with other qualities. Rate limits affect availability; encryption affects recovery; isolation affects cost and operability; audit affects privacy; emergency access affects safety and insider risk. Explicit scenarios let authorized stakeholders make those trade-offs without hiding them in a generic “high risk” label.

## Prerequisites and Retrieval

Retrieve confidentiality, integrity, availability, authenticity, accountability, non-repudiation limits, identity, authentication, authorization, least privilege, complete mediation, separation of privilege, trust boundary, threat, vulnerability, exploit, attack surface, risk, dependency graph, fault tree, state machine, supply chain, incident response, and recovery.

From SARCH-041 through SARCH-050 retrieve integration, data, deployment, and observability boundaries. SARCH-051 through SARCH-060 supply distributed and recovery failure modes. SARCH-061 through SARCH-067 supply scenarios, risk, evidence, dependency, performance, and reliability models. This chapter does not replace penetration testing, secure implementation, privacy engineering, safety analysis, or formal security assessment.

## Learning Objectives

After completing this module, you should be able to:

1. define protection needs and unacceptable outcomes from stakeholder missions;
2. bound a threat model across lifecycle and system-of-systems dependencies;
3. model actors, assets, data, identities, authorities, trust boundaries, and deployment paths;
4. construct abuse cases and attack trees with explicit preconditions;
5. use STRIDE, CAPEC, ATT&CK, and similar lenses without claiming completeness;
6. analyze control, management, build, supplier, recovery, and insider paths;
7. distinguish likelihood evidence, uncertainty, impact, priority, and acceptance authority;
8. map preventive, detective, responsive, and recovery controls to paths and bypasses;
9. design verification that tests mechanisms and residual assumptions;
10. govern model ownership, drift, exceptions, and continuous revision.

## Core Exposition

**Start from protection needs.** Identify stakeholders, assets, missions, legal and ethical constraints, and unacceptable outcomes. Assets include data, money, physical processes, safety, reputation, identities, availability, evidence, intellectual property, and decision authority. State confidentiality, integrity, availability, authenticity, privacy, safety, or accountability needs per asset and lifecycle state.

Do not start with a technology checklist. “Protect the database” is weaker than “prevent one tenant from reading or influencing another tenant's records, backups, indexes, derived analytics, and deletion evidence.”

**Set scope and assumptions.** Name product versions, environments, organizations, providers, networks, physical sites, user groups, administrative planes, and lifecycle stages. Record what is excluded, why, who accepts the exclusion, and which external model owns it.

Assumptions are attack surfaces when false. Examples include trusted time, uncompromised identity issuer, honest build worker, isolated tenant key, reachable revocation, correct supplier artifact, and available human approver. Turn critical assumptions into requirements and tests.

**Model the system that exists.** Inventory processes, stores, data flows, events, identities, credentials, permissions, protocols, endpoints, queues, deployment units, control planes, operators, support tools, build systems, suppliers, backups, and recovery mechanisms. Tie the representation to deployed inventory and configuration.

A static data-flow diagram misses time, authority, state, dynamic discovery, retries, autoscaling, failover, and lifecycle. Add state and sequence views for authentication, privilege change, key rotation, deployment, emergency access, incident response, restore, and retirement.

**Draw trust boundaries by authority.** A boundary occurs wherever identity, policy, integrity, confidentiality, tenancy, ownership, physical control, or assurance changes. Process and container boundaries matter even on one host; administrative and support paths matter even on a private network.

Every crossing records sender and receiver identity, authentication, authorization, data classification, integrity, confidentiality, replay and freshness, failure semantics, logging, rate control, and revocation. “Internal” is topology, not proof of trust.

**Model adversaries.** Describe objective, starting access, knowledge, capability, resources, persistence, acceptable cost, and constraints. Include external attackers, malicious or coerced insiders, compromised customers, suppliers, tenants, devices, workloads, administrators, and automated abuse.

Avoid stereotypes and attribution certainty. The same path may be used by different actors, while an actor name alone supplies no actionable precondition.

**Write abuse cases.** Express actor, initial condition, target outcome, sequence, system response, observable evidence, and consequence. Include authorization abuse through intended features, not only technical exploits. Fraud, scraping, resource exhaustion, coercion, unsafe actuation, privacy inference, and evidence destruction can use valid credentials and valid syntax.

Negative scenarios complement ordinary use cases: “A tenant submits a valid identifier belonging to another tenant,” “support recovery is attempted without the original factor,” or “a signed but revoked artifact is deployed during partition.”

**Use structured elicitation.** STRIDE prompts spoofing, tampering, repudiation, information disclosure, denial of service, and elevation of privilege. Apply categories to elements and crossings, then write concrete scenarios. Category completion does not prove model completeness.

Attack trees decompose goals into OR alternatives and AND prerequisites. Misuse cases, CAPEC attack patterns, ATT&CK techniques, kill-chain views, fault trees, and domain hazard analysis expose other perspectives. Choose multiple lenses based on scope; catalogs reflect known abstractions and evolve over time.

**Trace data through its lifecycle.** Model collection, derivation, transit, processing, caching, indexing, storage, backup, replication, export, logging, analytics, model training, support access, restore, retention, and deletion. Derived and metadata can be sensitive even when source fields are encrypted.

Encryption protects particular properties under a key and protocol model. It does not decide who may request decryption, prevent an authorized service from leaking plaintext, guarantee deletion, or keep keys available during recovery.

**Trace identity and authority.** Separate proofing, authentication, session creation, authorization, delegation, impersonation, emergency access, revocation, audit, and recovery. Map which principal can read, write, approve, deploy, rotate, restore, disable evidence, or change policy.

Analyze confused-deputy paths in which a more privileged service exercises authority on an attacker's behalf. Bind authorization to the requesting principal, resource, action, tenant, context, and current policy at the enforcement point.

**Include control and management planes.** Orchestrators, identity systems, DNS, secrets, observability, feature flags, deployment, fleet management, and support tools often have broader authority than data-plane services. Compromise can cross every region while ordinary request paths appear isolated.

Model management APIs, break-glass paths, workstation and device trust, approval, automation identity, credential issuance, and recovery. Secure control also needs an independently usable recovery path; otherwise compromise can disable its own remediation.

**Include software supply chain.** Trace source, review, dependencies, build inputs, build workers, artifact identity, signing, provenance, registries, promotion, deployment, update, rollback, and retirement. Ask who can substitute an input, reuse a credential, alter policy, suppress evidence, or promote a revoked artifact.

Third-party code and managed services remain within the threat model as dependencies with contracts, evidence, notification, isolation, exit, and recovery assumptions. Procurement is not a trust proof.

**Model multi-tenancy and shared resources.** Tenant identity, authorization, data partition, compute isolation, cache keys, queues, rate limits, observability, support, encryption keys, and deletion must align. Noisy-neighbor and resource-exhaustion paths are both availability and isolation concerns.

Quantify blast radius by affected assets and authorities, not node count. Per-tenant controls contain some faults, but a root key, control plane, deployment, or operator can remain global.

**Treat availability as a security property.** Adversaries exploit expensive requests, retries, state exhaustion, locks, queues, control loops, and dependencies. Apply capacity models from SARCH-066 to malicious workload classes. Authentication itself can be a denial-of-service bottleneck.

Prefer cheap rejection before expensive work, bounded resources, tenant and priority isolation, idempotency, retry budgets, and graceful modes that preserve critical security properties. A degraded insecure response is not resilience.

**Analyze risk without fake arithmetic.** Separate consequence, path feasibility, exposure, actor capability, existing controls, evidence, uncertainty, and time horizon. Ordinal labels support triage but multiplication of category numbers does not create calibrated probability or loss.

Use ranges, scenarios, sensitivity, and explicit unknowns. High-consequence paths with uncertain likelihood can deserve design action. Risk acceptance belongs to an authorized owner with affected stakeholder input, not to a threat-model facilitator alone.

**Map controls to paths.** Prevention removes preconditions or authority; detection observes state or behavior; response contains and revokes; recovery restores trustworthy operation and evidence. Defense in depth requires failure diversity and independence, not multiple controls sharing one bypass.

For each control record owner, protected path, configuration, dependency, evidence, failure mode, bypass, alert, response, recovery, exception, and expiry. Link to requirements and architecture decisions.

**Design verification.** Static analysis, configuration checks, unit and integration tests, authorization matrices, fuzzing, property testing, penetration testing, adversary emulation, red teaming, fault injection, restore exercises, and incident review provide different evidence. Test negative outcomes and control failure, not merely expected success.

Security testing demonstrates observed behavior in scope. It does not prove absence of unknown paths. Protect production, people, data, and external systems through authorization, rules of engagement, stop conditions, and recovery.

**Maintain the model.** Trigger review on new data, identity, privilege, interface, dependency, supplier, deployment, region, tenant, model, protocol, operator workflow, incident, vulnerability class, or threat intelligence. Compare inventory and configuration against the model to detect drift.

Keep stable scenario and control identities across revisions. Track resolved, accepted, transferred, and open risks with rationale and expiry. A stale threat model can be more dangerous than no model because it creates unwarranted confidence.

## Definitions and Notation

Let an architecture threat model contain:

- $A$ as assets and protection needs;
- $P$ as principals, identities, and authorities;
- $S$ as system states and lifecycle stages;
- $E$ as typed transitions or interactions;
- $G$ as adversarial goals;
- $C$ as controls;
- $H$ as harms or unacceptable outcomes;
- $\pi=(s_0,e_1,s_1,\ldots,e_n,s_n)$ as a candidate attack path;
- $pre(e_i)$ as the preconditions for transition $e_i$;
- **feasible path** as one whose initial access and every transition precondition can be satisfied under the model;
- **control coverage** as traceability from a control to declared path transitions and outcomes, not a percentage of universal security;
- **residual risk** as accepted or unresolved risk after implemented controls and evidence.

An attack path set is not a probability distribution. Costs, times, and likelihoods can be aggregated only when their meanings, dependence, and scales justify the operation.

## Mechanisms, Invariants, or Proof Structure

### Architecture-scale threat-modeling procedure

1. Establish stakeholders, assets, missions, protection needs, and unacceptable outcomes.
2. Bound versions, environments, lifecycle, dependencies, exclusions, and assumptions.
3. Model data, identity, authority, state, flow, control, deployment, supplier, and recovery structures.
4. Describe threat actors by objective, access, capability, resources, and constraints.
5. Elicit abuse cases and attack paths with several appropriate lenses.
6. Analyze preconditions, common causes, blast radius, consequence, evidence, and uncertainty.
7. Map preventive, detective, responsive, and recovery controls to specific paths.
8. Convert selected paths into security requirements and verification plans.
9. Assign risk and control owners, exceptions, residual decisions, and expiry.
10. Reconcile with deployment and evidence continuously as the system changes.

### Executable attack-path calculation

This example enumerates additive illustrative effort along a fixed acyclic graph. The lowest number is a review priority under the supplied toy assumptions, not an attack probability or a claim about real attacker behavior.

<!-- bijux-verify: {"id":"attack-path-priority","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"lowest-cost path=internet -> helpdesk -> identity -> production cost=11\n","stderr":""}} -->
```python
graph = {
    "internet": [("web", 4), ("helpdesk", 2)],
    "web": [("identity", 8)],
    "helpdesk": [("identity", 3)],
    "identity": [("production", 6)],
    "production": [],
}

paths = []

def visit(node, cost, path):
    if node == "production":
        paths.append((cost, path))
        return
    for next_node, edge_cost in graph[node]:
        visit(next_node, cost + edge_cost, path + [next_node])

visit("internet", 0, ["internet"])
cost, path = min(paths)
print(f"lowest-cost path={' -> '.join(path)} cost={cost}")
```

### Invariants

- every modeled threat reaches a named asset or unacceptable outcome;
- every path records actor starting access and transition preconditions;
- every trust-boundary crossing records identity, authority, data, protocol, and revocation;
- every control names the path it interrupts and how failure or bypass is detected;
- catalogs and categories seed analysis but do not close it;
- risk priority never disguises ordinal judgment as calibrated probability;
- compromised administrator, supplier, control plane, evidence, and recovery paths stay in scope;
- model drift, open assumptions, exceptions, and residual risk remain visible.

## Alternatives and Trade-Offs

- **Asset-centric versus system-centric:** asset focus follows protection across copies; system focus reveals shared mechanisms and dependencies.
- **Data-flow diagram versus state model:** flows communicate interactions; state models capture privilege, sequence, revocation, and recovery.
- **STRIDE versus attack tree:** STRIDE broadens category prompts; trees expose goal structure and preconditions.
- **Catalog versus bespoke abuse cases:** catalogs transfer known patterns; bespoke cases capture domain-specific harm and valid-feature abuse.
- **Qualitative versus quantitative risk:** qualitative scales tolerate sparse evidence; calibrated models support comparison but demand real data and dependence.
- **Prevent versus detect/respond:** prevention removes opportunity; detection and response cover bypass but require trustworthy telemetry and authority.
- **Central authority versus distributed enforcement:** central policy simplifies consistency; distributed enforcement can contain compromise but risks drift.
- **Shared platform versus tenant isolation:** sharing reduces cost and inconsistency; isolation reduces selected blast radius and raises operational complexity.
- **Short credentials versus offline continuity:** short life limits replay; offline operation needs bounded delegated authority and safe renewal failure.
- **Transparency versus secret minimization:** rich evidence aids investigation; excessive logs create privacy, access, and retention threats.
- **Automated response versus human approval:** automation is fast; human checks resist some automation compromise but add delay and coercion paths.
- **Frequent model revision versus governance load:** continuous drift detection keeps relevance; review effort must be risk-triggered and owned.

## Failure Modes and Misconceptions

1. **“The diagram is the threat model.”** Outcomes, actors, paths, controls, evidence, decisions, and ownership make it actionable.
2. **“Inside the network is trusted.”** Workload, process, tenant, identity, and administrative boundaries remain.
3. **“STRIDE completion means completeness.”** Categories prompt questions; they do not enumerate the system or adversary.
4. **“Known attack catalogs cover the future.”** Catalogs evolve and cannot contain domain-specific or novel paths.
5. **“Encryption secures the data.”** Key authority, endpoint plaintext, metadata, integrity, retention, and recovery remain.
6. **“Authentication proves authorization.”** Identity does not grant a specific action on a specific resource.
7. **“Managed means trusted.”** Provider identity, control, tenancy, supply chain, notification, and recovery need evidence.
8. **“Valid credentials imply benign use.”** Abuse, fraud, coercion, and confused deputies often use valid credentials.
9. **“Likelihood times impact is precise risk.”** Ordinal categories and dependent guesses do not become calibrated by multiplication.
10. **“Low probability means no action.”** High consequence, uncertainty, irreversibility, or legal constraints can dominate.
11. **“More controls mean defense in depth.”** Controls sharing one authority, implementation, or bypass may fail together.
12. **“Logging is detection.”** Evidence must be complete enough, protected, observed, actionable, and linked to response.
13. **“Availability is not security.”** Resource exhaustion and control disruption are adversarial outcomes.
14. **“Backups solve destructive attack.”** Attackers may delete, encrypt, corrupt, age out, or capture restore authority.
15. **“Regions or clouds are independent.”** identity, DNS, suppliers, software, people, and recovery may remain common.
16. **“Penetration testing proves security.”** It observes selected paths under bounded time, access, skill, and rules.
17. **“The security team owns every risk.”** Business, safety, privacy, operations, and mission authorities own consequences and acceptance.
18. **“Annual review keeps the model current.”** Architectural and threat changes create drift between calendar reviews.

## Worked Examples

### Example 1

**Find the real trust boundary.**

**Situation.** Support can reset an administrator's authentication factor after a phone call, and administrators can mint production sessions.

**Reasoning.** The attack path is social engineering to support, weak recovery proofing, privileged reset, session creation, then production access. A web firewall does not interrupt it. Bound support authority, require independent recovery evidence and approval, notify the original channels, shorten session life, log impersonation, and test revocation.

**Conclusion.** Human identity recovery is an architecture trust boundary with production consequence.

### Example 2

**Turn STRIDE labels into scenarios.**

**Situation.** A tenant sends object identifiers to a shared export service.

**Reasoning.** “Spoofing” becomes forged or confused tenant identity; “tampering” becomes altered export selection; disclosure becomes another tenant's object; denial becomes expensive wildcard exports; elevation becomes export-service authority used beyond caller scope. Requirements bind tenant and object authorization at retrieval, cap work, sign manifests, isolate queues, and audit actor-to-object decisions.

**Conclusion.** Categories become useful only after concrete preconditions, outcomes, and controls are written.

### Example 3

**Calculate overlapping alternative events.**

**Situation.** Evidence estimates $P(A)=0.10$, $P(B)=0.20$, and $P(A\cap B)=0.05$ for two path-enabling events in one period.

**Reasoning.** $P(A\cup B)=0.10+0.20-0.05=0.25$. Adding yields 0.30 by double-counting overlap; assuming independence yields $0.10+0.20-0.02=0.28$, also inconsistent with the stated joint evidence.

**Conclusion.** Alternative-path aggregation requires dependence, which is often the least defensible input.

### Example 4

**Interpret an attack tree cost.**

**Situation.** The toy graph offers web-to-identity-to-production cost $4+8+6=18$ and helpdesk-to-identity-to-production cost $2+3+6=11$.

**Reasoning.** Under additive comparable edge-cost assumptions, the helpdesk path is the minimum and merits review. Real steps may share setup, be conditional, occur in parallel, alert defenders, or be infeasible for the actor. The number prioritizes questions rather than predicting compromise.

**Conclusion.** Attack-tree arithmetic is bounded by the meaning and dependence of its inputs.

### Example 5

**Expose a confused deputy.**

**Situation.** A report service with broad storage access accepts a customer-supplied object path after authenticating the customer.

**Reasoning.** Authentication establishes caller identity but does not constrain the service's more powerful storage authority. Bind every requested object to caller tenant and action, enforce at the data access point, avoid ambient credentials, canonicalize identity before policy, and test traversal, aliases, race, and indirect references.

**Conclusion.** The deputy must authorize the requested resource, not merely trust an authenticated caller.

### Example 6

**Model supply-chain promotion.**

**Situation.** Builds are signed, but the same CI identity can build, approve, promote, and alter verification policy.

**Reasoning.** A valid signature only proves use of that identity. Compromise permits malicious build and policy bypass. Separate source review, hermetic build, signing, policy administration, and promotion authorities; bind provenance; protect keys; require independent approval; test revoked artifact and verifier failure.

**Conclusion.** Signing without separated authority can attest a compromised process faithfully.

### Example 7

**Quantify blast radius honestly.**

**Situation.** One key encrypts 100 tenants. Per-tenant keys would normally limit one data-key compromise to one tenant.

**Reasoning.** Per-tenant keys reduce selected data-key blast radius from 100 to one, but root key service, policy administrator, application plaintext access, deployment, and backup paths may remain global. Measure each authority layer and exercise revocation and restore.

**Conclusion.** Granular keys contain one path; they do not prove tenant isolation end to end.

### Example 8

**Trade replay window for dependency.**

**Situation.** An offline command token lifetime falls from 60 minutes to 10 minutes.

**Reasoning.** Maximum nominal replay window falls by 50 minutes, but devices now depend more often on renewal availability, time accuracy, and identity service. Define bounded offline authority, clock tolerance, revocation, failure-safe behavior, and recovery before choosing the lifetime.

**Conclusion.** A tighter credential can reduce replay exposure while increasing availability and recovery coupling.

### Example 9

**Treat denial as an architectural path.**

**Situation.** A syntactically valid search fans out to 500 partitions and triggers expensive ranking before quota is checked.

**Reasoning.** The attacker needs no memory corruption. Move authentication and tenant budget before fan-out, bound query complexity, reserve critical capacity, propagate cancellation, cap retries, isolate partitions, and detect cost per admitted principal. Validate useful throughput and fairness under malicious mixes.

**Conclusion.** Valid-feature resource amplification is both a security and capacity concern.

### Example 10

**Reject an ordinal risk tie.**

**Situation.** One team scores likely/low impact as $5\times1=5$ and rare/catastrophic as $1\times5=5$.

**Reasoning.** The categories are ordinal, so multiplication and equality lack interval meaning. The catastrophic scenario may also have legal thresholds, irreversibility, deep uncertainty, or safety authority that prohibits acceptance. Compare consequence narratives, feasibility evidence, uncertainty, controls, and decision rights separately.

**Conclusion.** A risk matrix can triage discussion but cannot settle unlike consequences through arithmetic.

## Cross-Program Connections

- **Security Engineering:** owns deep cryptography, authentication, authorization, vulnerability, attack, defense, assurance, and incident disciplines.
- **Systems Engineering:** owns mission, safety, human, physical, supplier, lifecycle, and system-of-systems risk boundaries.
- **Distributed Systems Engineering:** owns trust under partition, consensus, replication, state, and distributed failure assumptions.
- **Platform Engineering:** owns shared identity, policy, tenancy, orchestration, deployment, secrets, observability, and recovery controls.
- **Software Delivery and Reliability Engineering:** owns build and release integrity, production change, detection, response, and recovery evidence.
- **API and Service Engineering:** owns interface authentication, authorization, abuse resistance, rate control, and protocol semantics.
- **Database and Data Architecture Engineering:** own data authority, isolation, lineage, retention, deletion, backup, and restore mechanisms.
- **Networking:** owns segmentation, transport security, routing, denial resistance, and traffic evidence.
- **Testing and Quality Engineering:** owns negative testing, fuzzing, adversary emulation evidence, and oracle limits.
- **Law, privacy, safety, fraud, and domain specialists:** retain interpretation and acceptance authority; this architecture module does not certify compliance.

## References

1. Jerome H. Saltzer and Michael D. Schroeder, “The Protection of Information in Computer Systems,” *Proceedings of the IEEE* 63(9), 1975. <https://doi.org/10.1109/PROC.1975.9939>
2. Michael Howard and Steve Lipner, *The Security Development Lifecycle*, Microsoft Press, 2006.
3. Adam Shostack, *Threat Modeling: Designing for Security*, Wiley, 2014.
4. Ron Ross, Mark Winstead, and Michael McEvilley, *Engineering Trustworthy Secure Systems*, NIST SP 800-160 Vol. 1 Rev. 1, November 2022. <https://doi.org/10.6028/NIST.SP.800-160v1r1>
5. Joint Task Force Transformation Initiative, *Guide for Conducting Risk Assessments*, NIST SP 800-30 Rev. 1, September 2012. <https://doi.org/10.6028/NIST.SP.800-30r1>
6. Bruce Schneier, *Secrets and Lies: Digital Security in a Networked World*, Anniversary ed., Wiley, 2015.
7. MITRE, *Adversarial Tactics, Techniques, and Common Knowledge (ATT&CK)*, retrieved 2026-09-06. <https://attack.mitre.org/>
8. MITRE, *Common Attack Pattern Enumeration and Classification (CAPEC)*, retrieved 2026-09-06. <https://capec.mitre.org/>
9. OWASP Foundation, *Threat Modeling Cheat Sheet*, retrieved 2026-09-06. <https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html>
10. Ross Anderson, *Security Engineering: A Guide to Building Dependable Distributed Systems*, 3rd ed., Wiley, 2020. <https://www.cl.cam.ac.uk/~rja14/book.html>

## Exercises

### Exercise 1

Define asset, protection need, threat, threat actor, vulnerability, attack path, attack surface, trust boundary, abuse case, attack tree, control coverage, residual risk, and threat-model drift. Explain why “internal service” is not a trust decision.

### Exercise 2

An attack goal has two alternative enabling events with $P(A)=0.08$, $P(B)=0.15$, and $P(A\cap B)=0.04$ in one carefully defined period. Compute the union. Then explain why this calculation cannot normally be copied to speculative architecture paths.

### Exercise 3

Diagnose a threat model containing only public API boxes, generic STRIDE labels, CVSS scores, and firewall controls. It omits tenant identities, support, CI/CD, secrets, control planes, backups, suppliers, mobile clients, fraud, safety, and recovery. Design corrected artifacts and evidence.

### Exercise 4

Compare centralized authorization, service-local policy, capability tokens, and human approval for emergency production changes. Address revocation, offline operation, compromised control, audit, separation of privilege, availability, and recovery.

### Exercise 5

Design an architecture-scale threat model for a municipal water-control system with sensors, pumps, local controllers, operator consoles, radio links, cloud analytics, supplier updates, emergency manual control, safety envelopes, public reporting, and privacy-sensitive household data. Include missions, harms, actors, states, trust boundaries, attack paths, controls, validation, recovery, uncertainty, ownership, and residual risk without claiming safety or regulatory certification.

## Answers to the Exercises

### Answer 1

An **asset** has stakeholder value; a **protection need** states the security property and consequence. A **threat** is a potentially harmful circumstance or event; a **threat actor** has modeled objective, access, capability, resources, and constraints. A **vulnerability** is exploitable or triggerable weakness. An **attack path** is a preconditioned sequence to an adversarial objective. **Attack surface** covers reachable interaction points and conditions.

A **trust boundary** is a change in authority or security assumptions. An **abuse case** uses the system intentionally to cause harm. An **attack tree** decomposes a goal into alternative and joint subgoals. **Control coverage** traces controls to paths and outcomes. **Residual risk** remains after controls and evidence. **Drift** is divergence between model and reality. “Internal” describes location; separately compromised workloads, tenants, processes, identities, operators, and control planes can cross trust boundaries inside one network.

### Answer 2

Inclusion-exclusion gives $P(A\cup B)=0.08+0.15-0.04=0.19$. A simple sum would double-count the 0.04 intersection. Architecture threat-path values usually lack a common population, time window, observation process, calibrated event definition, and joint-dependence evidence. Attackers adapt, steps share prerequisites, controls detect paths, and exposure changes. The identity is valid, but inserting ordinal guesses produces false precision. Use the calculation only when data and event semantics support it; otherwise use scenarios, ranges, sensitivity, and explicit uncertainty.

### Answer 3

Begin with stakeholders, assets, protection needs, unacceptable outcomes, environments, lifecycle, exclusions, and assumptions. Reconstruct deployed data, identity, authority, process, interface, event, store, tenant, deployment, control, build, supplier, operator, client, backup, restore, and retirement views. Add state and sequence models for proofing, sessions, privilege, support impersonation, secret rotation, artifact promotion, failover, incident response, emergency access, restore, and deletion.

Turn category labels into actor-specific abuse cases and attack trees with starting access, preconditions, target outcomes, observables, and consequences. Use vulnerability scores only as one implementation input; add valid-feature abuse, fraud, denial, privacy inference, unsafe action, insider, compromised-admin, supply-chain, evidence-destruction, and recovery paths. Map preventive, detective, response, and recovery controls to each path with owners, dependencies, bypasses, alerts, tests, exceptions, and expiry. Verify through inventory reconciliation, authorization matrices, negative tests, configuration analysis, fuzzing, controlled adversary exercises, recovery tests, incident evidence, and specialist review. Track residual risks and drift continuously.

### Answer 4

Central authorization yields consistent policy and rapid revocation but creates latency, availability, and compromise concentration. Service-local policy supports autonomy and containment but can drift and requires trustworthy distribution, versioning, and audit. Capability tokens make delegated authority explicit and can work offline, but scope, audience, expiry, attenuation, storage, clock, replay, and revocation require careful design. Human approval adds contextual and separation checks but introduces delay, coercion, fatigue, collusion, identity recovery, and unavailable-person risks.

For emergency changes, use least-privilege short-lived capability scoped to action and target, strong proofing, independent approval for high consequence, local safety constraints, tamper-resistant audit, original-channel notification, rapid revocation, and tested offline and compromised-controller procedures. Separate request, approval, issuance, execution, policy administration, and evidence authority. Predefine when autonomy is permitted, what happens if central policy or time is unavailable, how conflicting authority is fenced, and how trustworthy recovery occurs. No mechanism alone covers every threat.

### Answer 5

Define missions for safe local water control, operator command, emergency manual action, telemetry, maintenance, public reporting, household-data use, update, incident response, and recovery. Unacceptable outcomes include unsafe pressure or chemistry, uncontrolled pumps, unavailable manual control, falsified readings, hidden alarms, cross-zone spread, prolonged water loss, privacy disclosure, fraudulent reports, and destruction of trustworthy evidence. Include external actors, malicious or coerced insiders, compromised households, radios, suppliers, technicians, cloud tenants, operator workstations, and automation.

Model sensor-to-controller, controller-to-pump, radio, console, identity, cloud, reporting, update, key, time, power, physical access, maintenance, support, backup, restore, and emergency authority boundaries. States include normal, disconnected local safety, degraded sensing, stale policy, maintenance, manual control, incident containment, update, rollback, and recovery. Attack paths cover spoofed sensor data, replayed command, stolen operator identity, support recovery abuse, malicious supplier artifact, control-plane compromise, radio denial, unsafe cloud recommendation, privacy linkage, alarm suppression, evidence alteration, and restore sabotage.

Controls include independent physical safety envelopes, authenticated and fresh commands, least privilege, separation of command and policy authority, bounded offline capabilities, local interlocks, network and tenant isolation, signed provenance with independent promotion, protected logging, anomaly and process-state detection, safe defaults, manual fallbacks, inventory, revocation, spare and repair access, and tested recovery. Map each to specific paths, dependencies, bypasses, alerts, response, and evidence. Validate with authorized simulation, hardware-in-loop and negative tests, replay and partition cases, bad updates, credential compromise, operator and accessibility exercises, restore, repeated faults, and supplier scenarios under strict safety controls.

Use ranges and adversarial scenarios where probabilities are unsupported. Water operators, safety engineers, security, privacy, accessibility, maintenance, suppliers, emergency services, legal authorities, and affected communities retain decision authority. Record excluded physical and regulatory analyses, open assumptions, exceptions, control limitations, and residual risk. Internal threat modeling informs but does not certify safety, public-health outcomes, privacy, or regulatory compliance.
