---
module_id: SARCH-014
program: Software Engineering: Software Architecture
level: 1
module_number: 14
title: Security and Privacy Tactics
status: complete
last_verified: 2026-09-05
---

# Security and Privacy Tactics

## One-Page Review

### Governing question

How should architecture prevent, limit, detect, respond to, and recover from unauthorized or harmful action while preserving legitimate use and governing personal data throughout its lifecycle?

### Essential definitions

- An **asset** is something stakeholders value and need protected, including data, capability, identity, safety, reputation, money, and service continuity.
- A **threat** is a circumstance or actor capable of causing harm; a **vulnerability** is a weakness that can be exploited or triggered.
- A **trust boundary** is a crossing at which identity, authority, integrity, confidentiality, provenance, or policy must be re-established rather than assumed.
- **Authentication** establishes evidence about an asserted identity; **authorization** decides whether that subject may perform an action on an object in context.
- **Confidentiality** constrains disclosure; **integrity** constrains unauthorized or improper change; **availability** constrains usable access under stated conditions.
- **Accountability** makes relevant action attributable through protected evidence and governed process.
- **Least privilege** grants only the authority required for a defined purpose, scope, and duration.
- **Privacy** governs legitimate processing of data about people, including purpose, collection, use, disclosure, retention, access, correction, and deletion—not confidentiality alone.
- **Defense in depth** uses multiple controls whose assumptions and failure modes are explicitly analyzed; it is not redundant control count.

### Central model, mechanism, or theorem

For subject $s$, action $a$, object $o$, and context $c$, make authorization an explicit predicate:

$$
Allow(s,a,o,c)\in\{true,false\}.
$$

Every protected operation must pass through a tamper-resistant enforcement point that evaluates current authenticated attributes and policy, denies when required evidence is absent, and records appropriate outcomes. This operationalizes complete mediation and least privilege from Saltzer and Schroeder's classic design principles while recognizing modern distributed identities and policy [1]. Architecture surrounds that decision with threat modeling, data protection, isolation, safe failure, monitoring, incident response, recovery, and privacy lifecycle controls.

### Critical invariants

- identify assets, actors, entry points, trust boundaries, threats, and unacceptable harms;
- authenticate and authorize every protected operation at the owning boundary;
- deny safely when required identity, policy, key, state, or dependency evidence is unavailable;
- minimize authority, data, lifetime, exposure, and blast radius;
- preserve data classification, purpose, provenance, integrity, and retention obligations across copies;
- keep secrets and cryptographic keys outside logs, source, images, and broad shared state;
- validate untrusted data before interpretation and encode output for its destination context;
- isolate tenants, workloads, management planes, and recovery authority according to the threat model;
- make security-relevant events observable without creating a new sensitive-data store;
- bind assurance claims to named threats, configurations, evidence, and qualified authority.

### Common failures

Common failures include trusting network location; authenticating once and authorizing nowhere; checking roles without object ownership; using a shared service identity for every action; encrypting data while exposing keys; logging credentials or personal data; collecting data “just in case”; validating syntax but not semantic authority; silently failing open; placing every control behind one identity or management plane; treating compliance as proof of security; adding layers with the same bypass; ignoring administrative, recovery, build, and supplier paths; and calling pseudonymous data anonymous.

### Compact example

A document endpoint receives `/documents/42` from an authenticated user. Authentication alone proves neither ownership nor permission. The owning service resolves document 42, tenant, classification, requested action, sharing state, policy version, and relevant context, then evaluates authorization. It returns a non-disclosing denial when evidence is missing, records a protected decision event, and avoids trusting a caller-supplied tenant field. The invariant is object-level authority on every access, not possession of a valid token.

### Connections

[SARCH-003](003-functional-scope-and-system-context.md) supplies trust-boundary inventory; [SARCH-004](004-quality-attributes-as-architectural-drivers.md) supplies measurable scenarios; [SARCH-005](005-constraints-assumptions-and-risks.md) supplies explicit threat assumptions and residual risk; [SARCH-011](011-availability-and-recovery-tactics.md) supplies safe failure and recovery; and [SARCH-013](013-scalability-and-capacity-tactics.md) supplies isolation and overload interactions. [SARCH-068](../ROADMAP.md) later develops architecture-scale threat modeling in greater depth.

## Governing Question

A system can use encryption, strong passwords, and a firewall while remaining insecure because authorization is missing, recovery credentials are exposed, one tenant can read another, or a build pipeline can replace trusted code. It can protect confidentiality while violating privacy through excessive collection and indefinite retention. What architectural structure turns security and privacy objectives into enforceable, reviewable behavior?

The governing question is how to select tactics for explicit assets, threats, harms, trust boundaries, and data purposes, then verify that controls hold during normal operation, change, failure, attack, response, and recovery. No architecture is “secure” without a bounded claim and evidence.

## Why This Matters

Security failures exploit composition. A secure component can be called with excessive authority, a validated token can cross into the wrong tenant, encrypted traffic can terminate before an untrusted hop, and a recovery path can bypass normal controls. Architecture owns the placement, independence, state, and failure behavior of controls across the complete system.

Privacy failures can occur without an attacker. Excessive data collection, secondary use, opaque inference, long retention, inaccessible correction, and uncontrolled copies can harm people while every byte remains encrypted. Privacy therefore changes data models, flows, storage, analytics, operations, and deletion—not merely access control.

Controls also affect availability, latency, usability, cost, and operability. Stronger authentication can lock out legitimate emergency use; detailed logs can expose secrets; aggressive blocking can enable denial of service; key separation can slow recovery. These are trade-offs to govern, not excuses to remove protection.

## Prerequisites and Retrieval

Retrieve asset, actor, threat, vulnerability, exploit, harm, control, trust boundary, identity, credential, principal, subject, object, authentication, authorization, policy, least privilege, confidentiality, integrity, availability, accountability, privacy, personal data, encryption, key, secret, audit, isolation, incident, and residual risk.

From earlier modules, retrieve system context, stakeholder concerns, ASRs, constraints and assumptions, trade-off points, decision records, failure models, overload behavior, partition ownership, and evidence limits. You should be able to distinguish a policy statement from its enforcement mechanism and a control from evidence that it works.

## Learning Objectives

After completing this module, you should be able to:

1. frame security and privacy as stakeholder-visible quality scenarios;
2. identify assets, threats, harms, trust boundaries, and control ownership;
3. separate authentication, authorization, enforcement, and accountability;
4. apply least privilege, complete mediation, separation of privilege, and safe defaults;
5. place isolation and defense-in-depth controls by independent failure assumptions;
6. protect data, secrets, and keys across storage, transit, use, backup, and recovery;
7. govern personal-data purpose, minimization, retention, access, correction, and deletion;
8. design secure failure, incident response, and recovery paths;
9. plan claim-specific verification, adversarial testing, and operational evidence;
10. state residual risk and qualified human authority honestly.

## Core Exposition

**Frame assets and harms.** Begin with valued outcomes, not a control catalogue. Identify data, money, identity, capability, safety, intellectual property, service continuity, evidence, and human rights as applicable. Describe harmful disclosure, modification, destruction, denial, deception, surveillance, discrimination, or loss of control.

Define threat actors by capability, access, incentives, and constraints: anonymous external actor, authenticated user, tenant administrator, insider, supplier, compromised workload, lost device, or accidental operator. Avoid assuming every actor is equally capable or that insiders are automatically trusted.

**Map attack and data surfaces.** Inventory entry points, APIs, user interfaces, files, messages, devices, administrative tools, build and deployment paths, observability, backups, recovery, suppliers, and physical interfaces. Map sensitive-data creation, transformation, copy, transport, access, inference, retention, and deletion.

A context diagram shows crossings but not trust. For each crossing ask who asserts identity, who validates it, how integrity and confidentiality are protected, which policy applies, what is logged, how failure behaves, and how keys or credentials are obtained.

**Authenticate with bounded evidence.** Authentication evidence can include possession, knowledge, inherence, device state, workload identity, and channel binding. Strength depends on enrollment, issuance, storage, rotation, revocation, recovery, phishing resistance, verifier behavior, and context—not factor count alone.

Services need identities too. A shared credential makes every instance indistinguishable and broadens compromise. Prefer short-lived, scoped workload credentials tied to a trusted issuance path. Protect bootstrap and recovery because they can mint or restore authority.

**Authorize at the owning boundary.** Evaluate subject, action, object, tenant, relationship, purpose, environment, and policy version where authoritative object state is known. A gateway can reject obviously invalid requests but usually cannot replace resource-level authorization inside the owning service.

Roles simplify administration but may be too coarse. Attributes, relationships, capabilities, or policy rules can express context more precisely. Whatever the model, define default denial, conflict resolution, delegation, revocation, cache lifetime, emergency override, and explanation without leaking sensitive state.

**Enforce complete mediation.** Every path to protected behavior—including batch, message, administrative, import, support, migration, and recovery paths—must meet the relevant policy. Enforcement points should be tamper resistant relative to the threat model and small enough to review. Complete mediation does not require one global component; distributed enforcement needs consistent policy semantics and versioning.

Fail closed when absence of evidence makes an action unsafe. Some safety or emergency contexts require a governed break-glass path rather than ordinary denial. Break glass must be narrowly scoped, strongly authenticated, time bounded, conspicuous, independently logged, reviewed, and revocable.

**Minimize privilege and authority.** Grant subjects only required actions, objects, tenants, environments, and duration. Separate routine operation from administration, deployment, key management, audit, and recovery. Use just-in-time elevation and independent approval where consequence warrants it.

Minimize transitive authority too. A front end with a broad database credential can bypass service policy. A message consumer may inherit authority from data it should treat as untrusted. Preserve caller or delegated identity where accountability and policy require it, and never let user input manufacture authority.

**Protect data in transit, at rest, and in use.** Transport protection requires endpoint authentication, protocol configuration, certificate lifecycle, name validation, and termination placement. RFC 8446 specifies TLS 1.3 protocol behavior; using its name alone does not prove correct endpoint or key management [7]. At-rest encryption requires key separation, access policy, rotation, backup, recovery, deletion, and protection from privileged paths.

Encryption does not validate input, authorize use, prevent deletion, hide all metadata, or constrain a recipient after decryption. Classify data and protect each representation, cache, index, export, log, backup, and derived feature according to its content and purpose.

**Manage secrets and keys as systems.** Define generation, provenance, storage, access, distribution, use, rotation, revocation, escrow if authorized, backup, recovery, destruction, and audit. Avoid long-lived secrets in source, configuration snapshots, container images, command lines, telemetry, or tickets. A secret manager becomes a critical dependency whose availability and recovery require separate analysis.

Cryptographic design requires qualified review. Architecture should choose well-reviewed protocols and libraries, separate keys by purpose and environment, bind ciphertext to relevant context, and define algorithm and key migration. Inventing a cipher or unauthenticated composition is not an acceptable tactic.

**Validate before interpretation.** Treat external and cross-boundary data as untrusted even when it comes from an authenticated peer. Check size, type, range, encoding, schema, semantic invariants, authorization, freshness, and resource cost before dangerous interpretation. Use destination-specific output encoding and parameterized interfaces.

Parsing should be bounded in time and memory. Decompression, recursive structures, regex behavior, image processing, and archive extraction can become denial-of-service paths. Validation is not sanitizing one string into universal safety; interpretation depends on destination context.

**Isolate by consequence.** Separate tenants, workloads, networks, processes, data, credentials, keys, administration, build, and recovery where the threat model justifies it. Isolation limits blast radius only if shared control planes, kernels, hardware, operators, and suppliers are considered.

Defense in depth needs independently useful layers. Two controls based on the same identity issuer, policy cache, or administrator may fail together. Record which threat each layer addresses, how it is bypassed, and how failure is detected.

**Preserve availability under attack.** Authentication, cryptography, validation, and logging consume resources. Bound request size, parsing, authentication attempts, expensive queries, concurrency, queues, and per-principal rates. Distinguish abusive from legitimate peaks cautiously; rate limits can deny shared networks or vulnerable populations.

Use layered admission, cheap early rejection, quotas, backpressure, isolation, and degradation without bypassing safety or authorization. Coordinate retry and challenge behavior so controls do not amplify load.

**Make security events observable.** Record sufficient identity, action, target, decision, policy version, time, provenance, and correlation to investigate relevant events. Protect log integrity, access, retention, clock assumptions, and availability. Separate operational detail from sensitive content; redact, tokenize, aggregate, or omit values not needed for the purpose.

Logs are evidence, not infallible truth. Compromised components can omit or forge events. Use independent collection or append-resistant mechanisms where the threat warrants it. Alert design must define response ownership, false-positive load, and safe automation.

**Govern privacy across the lifecycle.** State the legitimate purpose and authority for each personal-data element. Minimize collection and precision; separate purposes; restrict access and disclosure; publish retention; support required access, correction, portability, objection, or deletion; and propagate lifecycle rules to caches, replicas, analytics, models, exports, backups, and suppliers.

Deletion may be immediate from active access and delayed in protected backups under a documented recovery policy. Say what deletion means in each store and prevent restored backups from silently resurrecting expired data. Pseudonymization reduces some linkability but does not establish anonymity when re-identification or auxiliary data remains possible.

The [NIST Privacy Framework](https://www.nist.gov/privacy-framework) presents privacy risk as effects on individuals arising from data processing, complementing rather than replacing security risk. Privacy architecture therefore includes human consequences and governance, not merely breach prevention.

**Secure change and supply paths.** Define provenance and authorization for source, dependencies, builds, artifacts, configuration, deployment, infrastructure, and emergency changes. Verify integrity at transitions, separate build from release authority, constrain runners and tokens, retain evidence, and support revocation and rollback.

Signatures establish integrity and signer identity only relative to protected keys and verification policy. They do not prove that code is safe, reviewed, reproducible, or free of malicious logic. Supplier attestations similarly need scope, freshness, and independent validation.

**Respond and recover securely.** Define detection, triage, containment, evidence preservation, credential and key revocation, clean rebuild, data validation, communication, legal and privacy authority, restoration, and lessons. Recovery credentials and images must not share every compromise path with production.

Containment can destroy evidence or service; delayed containment can extend harm. Pre-authorize decision criteria and exercise them. After compromise, restoring availability without re-establishing identity, integrity, and trust can restore the attacker too.

**Build layered assurance.** Review design and data flows; verify policy and configuration; test positive, negative, boundary, abuse, and recovery cases; analyze dependencies; scan artifacts; perform authorized adversarial testing; exercise incidents; and monitor production outcomes. Follow current control catalogues such as [NIST SP 800-53 Rev. 5](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) and verification catalogues such as the [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) as coverage aids, not proof that every applicable risk is controlled.

No finite test proves absence of vulnerabilities. Record threat-model scope, versions, configuration, environment, evidence, exceptions, and residual risk. Reassess after architecture, dependency, threat, data-purpose, law, or operational changes.

## Definitions and Notation

Let $S,A,O,C$ be sets of subjects, actions, objects, and contexts. Authorization policy is a predicate

$$
Allow:S\times A\times O\times C\rightarrow\{true,false\}.
$$

Default denial means an operation proceeds only when the predicate is affirmatively true under current required evidence. Let $P(s)$ be authority granted to subject $s$ and $R(s)$ the authority required for its declared duties. Least privilege seeks $P(s)\subseteq R(s)$ while preserving required operation; excess authority is $P(s)\setminus R(s)$.

For threat scenarios $i=1,\ldots,n$, a simplified expected-loss model is

$$
R=\sum_{i=1}^{n}p_iL_i,
$$

where $p_i$ is a bounded probability estimate and $L_i$ a consequence measure in compatible units. The expression is useful for sensitivity, not a complete security decision: adversaries adapt, events correlate, probabilities are uncertain, losses can be incomparable or catastrophic, and distribution and equity matter.

Define control coverage as a relation $Covers(control, threat, asset, condition)$. A control count has no meaning without this relation, bypass assumptions, evidence, and failure behavior.

## Mechanisms, Invariants, or Proof Structure

Use this security and privacy mechanism.

1. **Frame value and harm:** identify assets, people, purposes, unacceptable outcomes, authority, and constraints.
2. **Map surfaces:** inventory actors, entry points, data flows, trust boundaries, administration, build, suppliers, and recovery.
3. **Model threats:** describe capabilities, preconditions, attack paths, harms, common causes, and residual assumptions.
4. **Mediate authority:** authenticate evidence, authorize at the owning boundary, default deny, minimize privilege, and separate duties.
5. **Protect information:** classify, minimize, validate, encrypt appropriately, manage keys, isolate, retain, and delete.
6. **Limit propagation:** constrain blast radius, resource use, tenants, management planes, dependencies, and control authority.
7. **Observe and respond:** produce protected decision evidence, detect abuse, investigate, contain, revoke, communicate, and recover trust.
8. **Secure change:** establish provenance, integrity, approval, compatibility, revocation, and rollback for software and configuration.
9. **Verify claims:** combine design review, automated checks, negative tests, adversarial assessment, exercises, and production observation.
10. **Govern residual risk:** record evidence limits, exceptions, owners, expiry, and triggers for reassessment.

The governing invariants are explicit assets and harms, complete mediation, least authority, safe defaults, protected identity and keys, bounded interpretation, lifecycle privacy, independent containment, observable decisions, secure recovery, and claims limited to evidence.

## Alternatives and Trade-Offs

**Centralized or distributed policy enforcement.** Centralization improves policy consistency and audit but adds latency and dependency concentration. Distributed enforcement preserves local ownership and resilience but requires semantic consistency, trusted policy distribution, versioning, and revocation.

**Roles or fine-grained attributes and relationships.** Roles simplify administration and review but can accumulate privilege. Fine-grained policies express object and context constraints but increase data, policy, cache, and explanation complexity.

**Fail closed or governed degraded access.** Fail closed protects against missing evidence but can block critical legitimate work. A break-glass path supports exceptional need but creates powerful authority requiring narrow scope, independent evidence, and review.

**More logging or data minimization.** Detailed events help investigation and accountability but can expose personal data, secrets, and behavior. Purpose-specific structured logging with access, integrity, and retention controls balances the concerns.

**Shared or isolated controls.** Shared identity, policy, and key services reduce duplication but enlarge blast radius. Isolation limits propagation but increases operational and consistency burden. Choose boundaries from threats and consequences.

## Failure Modes and Misconceptions

- **“Inside the network is trusted.”** Identity and policy must be evaluated at resource boundaries.
- **“Authenticated means authorized.”** Identity evidence does not grant an action on an object.
- **“The gateway checks access.”** Internal, message, batch, support, and recovery paths still require mediation.
- **“Encryption makes data safe.”** Endpoint, key, metadata, use, integrity, retention, and deletion remain.
- **“We use zero trust.”** A slogan does not specify assets, policy, enforcement, telemetry, or recovery.
- **“More controls mean defense in depth.”** Shared assumptions can make layers fail together.
- **“Logs should contain everything.”** Logs become a sensitive, high-value data system.
- **“Pseudonymous means anonymous.”** Linkage and auxiliary information can preserve identifiability.
- **“Compliance proves security.”** A control baseline and audit scope do not prove every threat is controlled.
- **“Fail closed is always safe.”** Safety-critical contexts may require governed emergency behavior.
- **“A signature proves software is good.”** It proves a relation to a key and verification policy, not benign behavior.
- **“Security is finished at release.”** threats, dependencies, data purposes, configuration, and evidence change.

## Worked Examples

### Example 1

**Question:** An authenticated user requests another tenant's invoice by changing an identifier. Where must the control act?

**Reasoning:** The invoice-owning service resolves the object and tenant from authoritative state and evaluates subject, action, object, tenant relationship, and policy. It does not trust a caller-supplied tenant value or assume the gateway's authentication grants object access. Denial should avoid revealing whether the invoice exists.

**Conclusion:** Object-level authorization belongs at every authoritative access path.

### Example 2

**Question:** A report generator has a broad storage credential because it occasionally reads one protected bucket. What is the architectural defect?

**Reasoning:** Its granted authority $P$ exceeds required authority $R$ for ordinary work. Split duties or issue short-lived, purpose- and bucket-scoped credentials through a controlled path. Constrain export destinations and record use. A compromised generator then has a smaller blast radius.

**Conclusion:** Least privilege minimizes scope and duration, including transitive service authority.

### Example 3

**Question:** Should authorization fail open when the policy service times out?

**Reasoning:** For a protected write, absence of current policy evidence normally requires denial or a safe deferred state. If emergency access is necessary, design a separate pre-authorized break-glass mode with strong identity, narrow actions, duration, conspicuous notice, independent audit, reconciliation, and review. Silent allow is not graceful degradation.

**Conclusion:** Failure behavior is part of the policy and must match consequence.

### Example 4

**Question:** Traffic uses TLS to a load balancer and plaintext from the load balancer to a service. Is the data protected in transit?

**Reasoning:** Only to the termination point. Evaluate the internal network, co-tenancy, operator access, routing, packet capture, workload identity, and integrity threats. If the boundary remains untrusted, authenticate and protect the internal hop too. Also govern certificate issuance, name validation, rotation, revocation, and keys.

**Conclusion:** Protocol presence does not erase trust boundaries or key lifecycle.

### Example 5

**Question:** Two controls each block an attacker with estimated probability 0.9. Is combined protection automatically 0.99?

**Reasoning:** Only under a justified independence model would failure probability multiply to $0.1\times0.1=0.01$. If both rely on one identity issuer, policy administrator, parser, or configuration, one cause can bypass both. Security evidence rarely supports naive independence.

**Conclusion:** Defense in depth requires analyzed failure diversity, not probability multiplication by assumption.

### Example 6

**Question:** Two threat scenarios have rough annual estimates $(p_1,L_1)=(0.02,100{,}000)$ and $(p_2,L_2)=(0.001,5{,}000{,}000)$ in compatible monetary units. What simplified expected loss results?

**Reasoning:** $R=0.02(100{,}000)+0.001(5{,}000{,}000)=2{,}000+5{,}000=7{,}000$. The result is highly sensitive to uncertain probabilities and omits correlated events, distribution, non-monetary harm, catastrophic limits, and adversarial adaptation.

**Conclusion:** Expected loss can compare assumptions but cannot decide security or privacy acceptability alone.

### Example 7

**Question:** May a debugging system log authorization headers and full customer records for faster diagnosis?

**Reasoning:** No default need justifies credentials or complete records. Define diagnostic purpose and fields, omit or tokenize identifiers, redact secrets before emission, restrict access, protect integrity, set retention, audit queries, and provide a time-bounded exceptional workflow if legitimately required. Test redaction against nested and malformed input.

**Conclusion:** Observability must minimize and protect its own sensitive data.

### Example 8

**Question:** A service deletes a user profile from its primary database but restores it from a monthly backup during recovery. Was deletion complete?

**Reasoning:** No. Define deletion semantics for active replicas, caches, indexes, analytics, exports, supplier copies, and backups. Record deletion tombstones or equivalent governed state so restoration reapplies expired obligations. State any lawful backup delay, access isolation, and destruction schedule honestly.

**Conclusion:** Privacy lifecycle rules must survive replication and recovery.

### Example 9

**Question:** An artifact is signed by the build system. What may deployment infer?

**Reasoning:** Verification can establish that artifact bytes match what a holder of a particular protected key signed under a policy. It cannot establish source review, dependency safety, build isolation, reproducibility, or benign behavior. Bind provenance, source revision, builder identity, tests, approval, environment, revocation, and deployment policy separately.

**Conclusion:** Integrity evidence has precise scope; it is not a universal safety certificate.

### Example 10

**Question:** How should security and privacy be architected for a remote medication dispenser?

**Reasoning:** Identify patient safety, prescription authority, medication inventory, identity, personal data, physical access, device software, network, time, support, and recovery. Authenticate commands and devices, authorize each dispense against current prescription and context, prevent replay, protect keys, limit offline behavior, preserve audit, and define safe failure and emergency authority. No external clinical, medical-device, safety, privacy, accessibility, regulatory, cybersecurity, hardware, human-factors, or practitioner review is claimed; named qualified authorities must validate hazards, policy, controls, evidence, release, and residual risk.

**Conclusion:** High-consequence protection must preserve safe authorized physical outcomes, not merely pass an application checklist.

## Cross-Program Connections

- [Software Engineering: Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns systematic verification, negative testing, oracles, and evidence quality.
- [Software Engineering: Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) owns secure delivery operations, observability, incidents, and recovery practice.
- [Network Engineering](../../24-network-engineering/ROADMAP.md) owns protocol, channel, routing, and network-attack mechanisms.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns detailed cryptography, identity, application, infrastructure, adversarial, and assurance mechanisms.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects security to hazards, physical systems, operators, suppliers, and lifecycle assurance.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns shared identity, policy, secrets, isolation, and developer-control implementation.
- [Cloud & Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) owns provider infrastructure identity, networking, encryption, logging, and governance mechanisms.

## References

1. Jerome H. Saltzer and Michael D. Schroeder. [“The Protection of Information in Computer Systems.”](https://doi.org/10.1109/PROC.1975.9939) *Proceedings of the IEEE* 63(9), 1975, pp. 1278–1308. Economy of mechanism, fail-safe defaults, complete mediation, open design, separation of privilege, least privilege, and psychological acceptability.
2. NIST. [Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework), February 2024. Govern, identify, protect, detect, respond, and recover outcomes; consulted 2026-09-05.
3. NIST. [SP 800-53 Rev. 5, Security and Privacy Controls for Information Systems and Organizations](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final), September 2020, Release 5.2.0 issued August 2025. Control families and assessment context; consulted 2026-09-05.
4. Scott Rose et al. [NIST SP 800-207, Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final), August 2020. Resource-centric access, policy decision and enforcement, identity, telemetry, and deployment models; consulted 2026-09-05.
5. NIST. [Privacy Framework](https://www.nist.gov/privacy-framework), version 1.0, January 2020. Privacy-risk governance and data-processing outcomes; consulted 2026-09-05.
6. OWASP Foundation. [Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/), version 5.0.0, May 2025. Application-security requirements and verification coverage; consulted 2026-09-05.
7. Eric Rescorla. [RFC 8446: The Transport Layer Security (TLS) Protocol Version 1.3](https://www.rfc-editor.org/rfc/rfc8446), IETF, August 2018. TLS 1.3 protocol requirements.
8. Ross Anderson. *Security Engineering: A Guide to Building Dependable Distributed Systems*, third edition, Wiley, 2020. Security models, protocols, access control, economics, usability, operations, and system failure.

## Exercises

### Exercise 1

Define the difference among authentication, authorization, enforcement, and accountability for a payroll-record read.

### Exercise 2

Given granted permissions $P=\{read,write,export,admin\}$ and required permissions $R=\{read,export\}$, compute excess authority and propose a correction.

### Exercise 3

Diagnose an architecture with one shared service credential, gateway-only authorization, plaintext internal traffic, full-payload logs, indefinite analytics retention, unsigned deployments, and a fail-open policy cache.

### Exercise 4

Compare centralized and service-local authorization for a multi-tenant document platform. Address authority, consistency, availability, latency, revocation, audit, and failure.

### Exercise 5

Design security and privacy assurance for an unfamiliar municipal emergency-shelter registry. Separate automated checks, adversarial and operational exercises, qualified authority, and release blockers.

## Answers to the Exercises

### Answer 1

Authentication establishes evidence that the requester corresponds to an asserted employee or workload identity through a defined enrollment, credential, verifier, and recovery process. Authorization evaluates whether that subject may perform `read` on the specific payroll object in the current tenant, relationship, purpose, time, and policy context. Enforcement ensures every path to the record—including UI, API, export, batch, support, and recovery—cannot proceed unless the authorization decision permits it. Accountability preserves appropriately protected evidence of requester, action, object reference, decision, policy version, time, and outcome for governed investigation and review.

None substitutes for another. A valid identity can lack permission; a correct policy can be bypassed by an unmediated export; and a log entry alone neither prevents access nor proves an uncompromised component reported truthfully. The architecture must state owners, failure behavior, privacy limits, and evidence for all four.

### Answer 2

Excess authority is

$$
P\setminus R=\{write,admin\}.
$$

Issue a role or scoped capability containing only `read` and `export` for the relevant objects, tenant, purpose, environment, and required duration. If administration is sometimes legitimate, require separate just-in-time elevation with independent approval and audit rather than leaving it ambient. Ensure export destinations and data classifications are also authorized; reducing verb count alone is incomplete.

### Answer 3

The shared credential prevents workload attribution and expands compromise. Gateway-only authorization misses direct, message, batch, support, and internal object paths. Plaintext internal traffic leaves an unassessed trust crossing. Full logs create a sensitive store and may expose secrets. Indefinite analytics violates purpose and retention governance. Unsigned deployment lacks even bounded artifact-integrity evidence. Fail-open cached policy silently grants access when evidence is missing.

Map assets, data, actors, trust and build boundaries, and threats. Issue scoped short-lived workload identities; authorize objects at owning services; protect relevant internal channels; minimize and protect logs; establish analytics purpose, access, retention, deletion, and supplier propagation; bind artifact provenance and approval; and default deny or use an explicit governed emergency path. Test revocation, cache staleness, direct paths, tenant isolation, malformed input, dependency outage, incident response, key recovery, and restored-data lifecycle rules.

### Answer 4

A centralized decision service can provide consistent policy semantics, rapid policy change, concentrated review, and uniform decision records. It can also add latency, availability concentration, data disclosure, and a powerful compromise point. Service-local decisions retain object context and can continue during central outage, but policy distribution, versioning, cache invalidation, revocation, and cross-service consistency become harder.

A sound hybrid often centralizes policy administration and signed or authenticated distribution while services enforce decisions with authoritative object state. Define which attributes are authoritative, policy versions, freshness bounds, revocation behavior, tenant isolation, default denial, emergency operation, and independent audit. Measure end-to-end authorization latency and availability, but never improve them by accepting stale unsafe policy. Test direct and asynchronous paths, central outage, partition, stale cache, compromised service, policy rollback, and recovery.

### Answer 5

Identify residents, families, staff, volunteers, shelters, medical and accessibility needs, location, eligibility, occupancy, reunification, identity evidence, emergency authority, suppliers, and public reporting. Model harms including exclusion, stalking, trafficking, discrimination, unsafe disclosure, duplicate allocation, record tampering, denial of service, coercion, insider misuse, and recovery failure. Minimize collected data and precision by purpose; separate public, operational, medical, and safeguarding views; authorize every object action; use time-bounded emergency roles; protect devices, channels, keys, exports, logs, backups, and deletion.

Automation can verify schemas, policy rules, object and tenant isolation, default denial, credential scope and expiry, configuration, secret absence, artifact provenance, logging minimization, retention state, trace links, and evidence freshness. Authorized adversarial work can test enumeration, privilege escalation, injection, resource exhaustion, stolen devices, policy outage, and supplier boundaries. Exercises can test surge registration, offline shelters, emergency access, revocation, incident communication, clean recovery, reconciliation, and restored-data deletion.

No external emergency-management, safeguarding, social-services, medical, privacy, accessibility, equity, regulatory, cybersecurity, human-factors, or practitioner review is claimed. Named qualified authorities and affected-community representatives must own lawful purpose, safeguarding policy, emergency authority, acceptable risk, validation, release, and oversight. Unclear data purpose, unsafe public exposure, unmediated access path, failed isolation, unavailable revocation, missing offline protection, failed recovery, or unresolved high-severity harm blocks the corresponding readiness claim.
