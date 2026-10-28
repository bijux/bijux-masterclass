---
module_id: SEC-002
program: Security Engineering
level: 1
module_number: 2
title: Confidentiality, Integrity, Availability, and Authenticity
status: complete
last_verified: 2026-08-29
---

# Confidentiality, Integrity, Availability, and Authenticity

## One-Page Review

### Governing question

How can an engineer turn confidentiality, integrity, availability, and authenticity from broad labels into distinct, testable protection claims for a named asset and adversary?

### Essential definitions

- **Confidentiality** preserves authorized restrictions on information access and disclosure, including content, derived information, and relevant metadata.
- **Integrity** guards against improper modification or destruction and supports confidence that protected state and processing remain within authorized rules.
- **Availability** ensures authorized entities can obtain timely, reliable access to and use of a resource under stated demand, fault, and attack conditions.
- **Authenticity** is the property of being genuine or verifiably from the purported source; it can concern an entity, message, device, artifact, or origin claim.
- **Authentication** is a process for establishing confidence in an authenticity or identity claim; it is not authorization.
- A **security objective** states a protected property; a **mechanism** helps enforce it; **assurance evidence** supports confidence that the mechanism and system satisfy the scoped objective.
- **Freshness** establishes that accepted data or authority is sufficiently recent or non-replayed for its use. It is related to, but not implied by, integrity or authenticity.

### Central model, mechanism, or theorem

Write each objective as

`G_p=(a,s,o,l,\tau,c,v,e),\qquad p\in\{C,I,A,U\},`

where `a` is the asset, `s` authorized or prohibited subjects, `o` operations, `l` lifecycle/location, `\tau` adversary and fault conditions, `c` operating conditions, `v` observable violation or acceptance criterion, and `e` required evidence. Here `U` denotes authenticity to avoid overloading `A`, which denotes availability.

The four properties are neither mutually exclusive nor interchangeable. A control supports only the properties, scopes, and assumptions its evidence establishes.

### Critical invariants

- Every property names an asset, actor, operation, lifecycle stage, threat/fault condition, and evidence boundary.
- Confidentiality claims cover authorized disclosure paths and relevant inference or metadata, not merely encrypted storage.
- Integrity claims distinguish unauthorized change from factual accuracy, source trust, freshness, and completeness.
- Availability claims name authorized users, workload, latency or deadline, degraded mode, dependency, and recovery condition.
- Authenticity claims name exactly what is purported, the verifier, trust anchor, binding, context, and freshness requirement.
- Authentication never silently implies authorization, non-repudiation, safety, or truth.
- Evidence for one property is not promoted into evidence for another without a separate argument.

### Common failures

Typical mistakes are calling encrypted data confidential despite exposed keys or metadata, treating a hash as protection against a malicious modifier, assuming backups create availability without tested restoration, equating uptime with usable service, accepting a valid signature as proof that content is true or current, confusing message authenticity with human identity, ignoring deletion as an integrity event, and reporting “CIA achieved” without scoped criteria.

### Compact example

A valid keyed message tag can show that bytes were produced by an entity with access to the shared key and were not altered outside that trust boundary. The message remains visible, so confidentiality is absent. Replaying the same tagged message can still verify, so freshness is absent. The verifier can be offline, so availability is absent. If several parties share the key, the tag does not identify which party created it.

### Connections

[SEC-001](001-assets-adversaries-trust-and-security-goals.md) supplies assets, stakeholders, adversaries, and trusted propositions. [SEC-003](../ROADMAP.md) turns these property claims into threat models. Later cryptography, identity, access-control, resilience, detection, and assurance modules supply mechanisms and deeper evidence.

## Governing Question

“Protect confidentiality, integrity, and availability” is not yet a requirement. Confidentiality of what, from whom, at which copies and times? Integrity of which state and transition, under whose authority? Availability for which users, workload, and deadline during which failures? Authenticity of a device, message, account, software artifact, or real-world fact?

The four properties are a classification lens. Engineering begins when each label is bound to assets, authority, conditions, falsifying observations, and evidence. The same system can satisfy one property for one asset and violate it for another.

## Why This Matters

Controls fail when their claimed property is unclear. Full-disk encryption can protect data on stolen powered-off media while doing little against an authenticated process exporting records. Replication can improve availability while rapidly copying corruption. A digital signature can authenticate a software publisher's key while signing vulnerable code. Rate limiting can preserve service capacity while denying an emergency workload whose shape was omitted.

Precise decomposition also prevents security theater. A dashboard might show encryption enabled, backups successful, checksums clean, and login multifactor active. None of those observations establishes that the correct people can obtain the correct information, unchanged and on time, from the genuine source, during the named attack.

FIPS 199 organizes federal information and systems by potential impact from loss of confidentiality, integrity, and availability. NIST's authenticity definitions add genuineness and purported origin. These sources provide durable vocabulary, not automatic risk ratings or assurance for a particular system.

## Prerequisites and Retrieval

From [SEC-001](001-assets-adversaries-trust-and-security-goals.md), retrieve asset, harmful outcome, adversary capability, trusted dependency, security goal, and residual risk. You should understand access control, identities, cryptographic hashes and keys at an introductory level, failure modes, service objectives, and the distinction between verification and validation.

Recall:

- unauthorized and incorrect are not synonyms;
- reachable and usable are not synonyms;
- identity and authority are not synonyms;
- preserved bytes and true information are not synonyms.

## Learning Objectives

After completing this module, you should be able to:

- formulate scoped confidentiality, integrity, availability, and authenticity objectives;
- distinguish disclosure from access, inference, traffic analysis, and privacy harm;
- distinguish data integrity, system integrity, correctness, completeness, provenance, and freshness;
- define availability through authorized demand, capacity, delay, dependency, degradation, and recovery;
- distinguish entity, data-origin, artifact, and channel authenticity;
- explain why authentication does not imply authorization or truth;
- map controls to property-specific mechanisms and evidence;
- analyze trade-offs and compositions among the four properties;
- diagnose overclaiming from encryption, hashes, signatures, redundancy, and uptime;
- transfer the framework to a high-consequence system with accountable human review.

## Core Exposition

### A property is a relation

Security properties do not reside in data as simple adjectives. Payroll records are confidential relative to unauthorized employees but intentionally visible to named payroll staff. A deployment artifact has integrity relative to an approved build and release process, not merely relative to yesterday's bytes. A service is available to one tenant while quota policy denies another.

For each claim, identify the protected object, subjects, allowed operations, environment, time, adversary, and observer. “Database confidentiality” can mean contents unavailable to a stolen-disk adversary, rows separated among tenants, query results limited by role, exports controlled, backups protected, or statistics resistant to inference. These are different claims with different mechanisms.

### Confidentiality

Confidentiality prevents unauthorized disclosure. Disclosure includes direct reads, error messages, logs, caches, replicas, backups, crash dumps, analytics, support tools, and human conversation. Derived facts and metadata can matter even when content is encrypted: traffic timing, recipient, volume, access pattern, record existence, and response size may reveal sensitive information.

Access control is a primary mechanism, but access is broader than reading a file. A process can infer a secret through shared state or timing. An authorized analyst can issue individually allowed queries whose combination discloses a prohibited fact. A service can return another tenant's identifier without returning the record body. Confidentiality requirements must name whether such channels are in scope and what leakage is acceptable.

Encryption transforms plaintext under a key and algorithm. It can protect selected representations during storage or transmission when keys, endpoints, algorithms, modes, nonces, implementation, and metadata assumptions hold. Encryption does not correct overbroad application authorization, prevent an endpoint from logging plaintext, hide every traffic feature, or protect data while a compromised authorized component uses it.

Data minimization can be stronger than concealment: data never collected, retained, or replicated cannot leak from that location. Tokenization, aggregation, redaction, separation, access control, secure deletion, and organizational procedures can support confidentiality at different lifecycle stages. Privacy additionally concerns lawful, fair, purpose-bound handling and effects on people; confidentiality alone is not a privacy program.

### Integrity

Integrity protects against improper modification or destruction. The word spans several related claims:

- **data integrity:** protected bytes or records are not changed or destroyed outside authorized rules;
- **system integrity:** components, configuration, and execution remain within authorized state and transition constraints;
- **source integrity or provenance:** confidence in where data came from and how it was produced;
- **correctness and completeness:** information accurately represents the relevant world and includes required facts.

These do not automatically follow from one another. A cryptographic digest stored beside a file detects accidental corruption only if the reference digest itself is trustworthy. An unkeyed hash can be replaced by an adversary who can replace the file. A signed temperature reading can be authentic and unmodified yet wrong because a calibrated sensor failed, the unit was mislabeled, or the reading belongs to another patient.

Integrity policy must define authorized mutation. Immutability is not universally desirable: errors need correction, retention rules require deletion, keys require rotation, and accounts require revocation. An append-only log may preserve events while a malicious producer appends false ones. Review creation, update, deletion, ordering, rollback, version, and reconciliation separately.

Mechanisms include authorization, validation, constraints, transactions, version control, authenticated data structures, message authentication codes, signatures, secure boot, configuration management, separation of duties, audit, replication with conflict rules, backups, and reconciliation against independent sources. Evidence includes negative authorization tests, state invariants, transition review, provenance chains, restore comparisons, tamper detection, and operational audit.

### Availability

Availability is timely and reliable authorized use. A login page returning status 200 is irrelevant if identity services cannot authenticate, downstream data is stale, or the transaction misses its deadline. Define the user population, operation, workload, success semantics, latency distribution, observation window, dependencies, fault/attack condition, degraded service, and recovery objective.

Capacity is part of availability. An adversary can consume CPU, memory, file descriptors, queues, connection state, bandwidth, human support attention, or a paid quota. Legitimate surges can cause the same effect. Admission control, quotas, prioritization, bounded work, caching, backpressure, load shedding, isolation, and autoscaling support availability only under modeled demand and dependency limits.

Redundancy removes a single dependency only if replicas do not share the same failure domain, vulnerable software, identity plane, configuration error, corrupted data, operator action, or provider quota. Failover needs detection, decision, state transfer, capacity, routing, and recovery. Backup existence is not restoration evidence; regularly verified restore objectives, keys, dependencies, and runbooks matter.

Availability also includes safe refusal. Failing open may keep a request path responsive while violating confidentiality or integrity. Failing closed can preserve those properties while blocking essential use. A high-consequence system may need a degraded mode with narrower, locally verified capabilities rather than a universal open/closed choice.

### Authenticity

Authenticity concerns genuineness or purported origin. The subject of the claim must be explicit:

- **entity authenticity:** confidence that the interacting entity is the claimed entity;
- **data-origin authenticity:** confidence that data came from a purported source;
- **artifact authenticity:** confidence that software, firmware, document, or device is the identified artifact from the stated authority;
- **channel or peer authenticity:** confidence about the endpoint of a protected session.

Authentication is the process used to establish that confidence. A password can authenticate knowledge associated with an account. A certificate chain can bind a key to a name under policy. A message authentication code can establish origin within a shared-key group. A digital signature can support public verification of a signing-key origin. Each conclusion depends on enrollment, key custody, algorithms, revocation, context binding, verifier policy, and endpoint integrity.

Authenticity is not authorization. A genuine employee can lack authority to approve a payment. A genuine service can send a malformed or malicious response. A genuine vendor can publish compromised software. Nor is authenticity factual truth: a properly authenticated sensor can be miscalibrated, and a signed assertion can contain incorrect information.

Freshness must often be added. Nonces, sequence numbers, timestamps, epochs, challenge-response, expiration, and replay state can bind a message to a session or time. A valid old command remains authentic to its source but can be unsafe now. Time itself becomes a dependency whose authenticity and availability need analysis.

### Relationships and counterexamples

The properties form a vector, not a ladder:

- encrypted ciphertext may preserve confidentiality while undetected bit changes destroy integrity;
- an authenticated public announcement needs authenticity and integrity but not confidentiality;
- a private, authentic request can be unavailable because a dependency is exhausted;
- highly available replicas can serve identical corrupted data;
- a confidential backup can be unrecoverable, preserving secrecy while failing availability;
- an unchanged file can lack authenticity if its origin is unknown;
- an authentic, unchanged command can be a replay.

Controls can support several properties. Authenticated encryption is designed to provide confidentiality and integrity/authenticity for protected data under a cryptographic contract. It still does not provide service availability, endpoint correctness, key management, authorization, or necessarily replay protection. A control name is a prompt to inspect its specification, not permission to check multiple boxes.

### Scope across lifecycle

Information moves through collection, input, processing, storage, transmission, display, export, backup, archival, and deletion. Confidentiality can fail in a debug trace. Integrity can fail during format conversion. Authenticity can fail at ingestion even if storage is protected. Availability can fail because deletion and recovery ownership were unclear.

Create a property matrix whose rows are assets and lifecycle states and whose columns are adversaries, property objectives, mechanisms, evidence, owner, and residual risk. Empty cells are questions. Repeated controls are shared dependencies whose failure may defeat several objectives.

### Evidence strength

Configuration inspection can show that encryption is enabled, not that every copy is encrypted or keys are protected. A negative authorization test samples inputs, not all paths. A signature verification proves a mathematical relation under a key, not trustworthy enrollment or content truth. A failover exercise proves one scenario at one time, not universal availability.

Combine evidence: requirements review, architecture and data-flow analysis, formal properties where appropriate, unit and integration tests, adversarial tests, static and dynamic analysis, key and identity lifecycle review, restore and failover exercises, fault injection, monitoring, incident history, and human validation of domain assumptions.

The executable example uses a deliberately non-cryptographic teaching tag because the repository's safe snippet runner does not permit imports. It verifies one original message, rejects one chosen modification, and accepts an exact replay. The plaintext remains directly visible. The function is trivially forgeable and must never be used as a security mechanism.

<!-- bijux-verify: {"id":"property-boundary-toy-tag","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"original_verified=True\ntampered_verified=False\nreplay_verified=True\nplaintext_visible=True\navailability_proved=False\n","stderr":""}} -->
```python
key = 73
message = b"transfer=100;to=acct-7;seq=42"


def toy_tag(candidate):
    return (key + sum((index + 1) * value for index, value in enumerate(candidate))) % 65521


def verifies(candidate, candidate_tag):
    return toy_tag(candidate) == candidate_tag


tag = toy_tag(message)
tampered = b"transfer=900;to=acct-7;seq=42"
print(f"original_verified={verifies(message, tag)}")
print(f"tampered_verified={verifies(tampered, tag)}")
print(f"replay_verified={verifies(message, tag)}")
print(f"plaintext_visible={b'transfer=100' in message}")
print("availability_proved=False")
```

This run proves only the five observations for one deterministic, forgeable function. It provides no cryptographic integrity or authenticity. It does not justify embedded keys, authenticate any holder, resist collision or forgery, establish authorization or freshness, conceal content or metadata, provide availability, verify another implementation, or validate a financial system. Later cryptography modules define safe constructions and key lifecycles in depth.

## Definitions and Notation

Let `O` be objects, `S` subjects, `Op` operations, `T` times, and `E` environments. Let policy `Permitted(s,op,o,t,e)` determine authorized actions.

- Confidentiality violation: information about `o` is disclosed to `s` beyond the authorized leakage function.
- Integrity violation: state or behavior involving `o` leaves the set of authorized values or transitions without an accepted, attributable recovery path.
- Availability violation: an authorized request by `s` for operation `op` fails its declared success, deadline, capacity, or recovery criterion under in-scope conditions.
- Authenticity violation: a verifier accepts a false binding between an entity, message, artifact, or origin and its purported identity/context.

These are modeling templates. Real policies include uncertainty, partial disclosure, probabilistic service, revocation, human action, and competing obligations.

Define a property claim:

`Claim=(asset,property,scope,assumptions,mechanism,evidence,residual\ risk,owner).`

**Non-repudiation** concerns evidence intended to prevent a party from successfully denying an action under legal and procedural rules; ordinary authenticity does not automatically establish it. **Accountability** links actions to responsible entities with evidence and governance. **Resilience** is the ability to withstand, adapt to, and recover from adverse conditions; it can support availability and integrity but is broader than either.

## Mechanisms, Invariants, or Proof Structure

Use the following review chain for every property.

1. Select the asset and stakeholder harm from [SEC-001](001-assets-adversaries-trust-and-security-goals.md).
2. State one property without naming a product.
3. Define authorized subjects, operations, disclosures, mutations, service conditions, or origin bindings.
4. Name adversary capabilities, accidents, dependencies, and lifecycle scope.
5. Select mechanisms and map each to one enforceable obligation.
6. Define decisive positive, negative, boundary, fault, and recovery evidence.
7. Identify properties and channels the mechanisms do not cover.
8. Assign residual-risk ownership and review triggers.

For composition, require a traceable implication:

`assumptions \land mechanism\ properties \land integration\ invariants \Rightarrow scoped\ objective.`

Review each premise. “Encrypted,” “signed,” “replicated,” and “authenticated” are not premises precise enough for this implication.

Confidentiality review follows every representation and observer. Integrity review follows every authorized transition and reference of truth. Availability review follows every critical dependency, bottleneck, queue, and recovery path. Authenticity review follows enrollment, credentials/keys, binding, verification context, freshness, revocation, and compromise recovery.

No finite checklist proves security. A counterexample can refute a universal claim, while passing evidence increases confidence only within its scope. Preserve negative findings and residual risks rather than averaging them into a property score.

## Alternatives and Trade-Offs

**Confidentiality versus observability.** Detailed logs and traces improve diagnosis and accountability but can disclose content, identifiers, timing, and relationships. Use minimization, access controls, structured redaction, protected debugging, retention limits, and tested emergency access.

**Integrity versus change velocity.** Separation of duties, review, signing, and controlled deployment reduce unauthorized change but add delay and operational burden. Risk-based paths can differ while every emergency path remains authenticated, scoped, logged, reviewed, and reversible.

**Availability versus strict denial.** Fail-closed behavior protects confidentiality and integrity when policy cannot be evaluated; it can deny essential service. Fail-open behavior preserves some access while expanding unauthorized action. Explicit degraded modes and local safety constraints are usually more rigorous than one global default.

**Authenticity versus anonymity.** Strong identity binding can support accountability while increasing surveillance, correlation, and breach harm. Some systems need proof of entitlement or group membership without civil identity. Define the actual binding required.

**Centralized versus distributed trust.** Central identity, key, and policy services simplify administration but concentrate outage and compromise impact. Distribution improves fault tolerance and autonomy while complicating consistency, revocation, and recovery.

**Prevention versus detection and recovery.** Prevention reduces successful violations; complete prevention is rarely plausible. Tamper-evident logs, anomaly detection, backup, rollback, incident response, and reconciliation reduce duration and consequence only when exercised.

**Uniform versus asset-specific controls.** Uniform controls are simpler and reduce configuration variation. Asset-specific treatment aligns cost and assurance to harm but increases classification and policy complexity. Shared baselines plus explicit high-impact additions are common.

## Failure Modes and Misconceptions

1. **Encryption equals confidentiality.** Keys, endpoints, authorization, copies, metadata, and lifecycle determine the claim.
2. **An unkeyed hash stops tampering.** An adversary able to replace data may replace the hash.
3. **Integrity means factually correct.** Untampered data can be wrong, incomplete, stale, or associated with the wrong subject.
4. **Deletion always violates integrity.** Authorized deletion can be required; unauthorized destruction is the issue.
5. **Availability equals uptime.** Authorized use can fail through latency, stale dependencies, exhausted capacity, or broken semantics.
6. **Replication guarantees availability.** Common dependencies and replicated corruption can defeat every copy.
7. **A backup is recovery.** Restoration needs tested data, keys, infrastructure, people, priorities, and time.
8. **A valid signature proves truth.** It supports a key-origin and integrity claim, not real-world correctness.
9. **Authentication grants access.** Authorization still evaluates subject, action, object, context, and policy.
10. **Authentic implies fresh.** Old authentic messages can be replayed.
11. **The CIA properties are exhaustive.** Privacy, safety, accountability, usability, non-repudiation, and resilience can add distinct obligations.
12. **One severity applies to the whole system.** Impact varies by asset, property, stakeholder, context, and duration.
13. **A control supports every property equally.** Each mechanism needs a separate mapping and evidence chain.

## Worked Examples

### Example 1

**Question:** Is an encrypted customer export confidential?

**Reasoning:** Ask who holds keys, where plaintext exists, whether filenames and sizes disclose facts, how recipients are authorized, and whether temporary files and logs persist.

**Conclusion:** Encryption supports a bounded representation claim; lifecycle confidentiality requires the entire disclosure path.

### Example 2

**Question:** A downloaded file matches a public SHA-256 digest on the same compromised website. Is integrity established?

**Reasoning:** The attacker can replace both file and digest. The calculation detects transmission errors but lacks an independent trusted reference.

**Conclusion:** Integrity evidence needs a protected binding to the expected digest or artifact authority.

### Example 3

**Question:** A signed build artifact verifies. Is it safe to deploy?

**Reasoning:** Verification can bind bytes to a signing key. The build may contain vulnerabilities, the key or build system may be compromised, approval may be absent, or the version may be revoked.

**Conclusion:** Artifact authenticity and integrity are necessary inputs, not safety or release authorization.

### Example 4

**Question:** A service reports 99.99% process uptime. Is availability proved?

**Reasoning:** Users may face dependency failures, timeouts, corrupted responses, geographic isolation, or insufficient capacity. The denominator and eligible operations are unknown.

**Conclusion:** Define authorized workload, success, deadlines, dependencies, conditions, and recovery before measuring.

### Example 5

**Question:** Does a read-only database have integrity?

**Reasoning:** It resists ordinary mutation but can contain false initial data, stale records, incomplete imports, wrong subject associations, or unauthorized deletion through another path.

**Conclusion:** Read-only access is one mutation control, not complete integrity or correctness.

### Example 6

**Question:** Two regions contain identical replicas. What properties follow?

**Reasoning:** Geographic separation can reduce some availability failures. Shared identity, software, configuration, control plane, keys, and corrupted replication can remain common dependencies.

**Conclusion:** Demonstrate failure-domain independence, degraded capacity, data correctness, failover, and restoration.

### Example 7

**Question:** A user completes multifactor authentication. May the user approve a payment?

**Reasoning:** Authentication increases confidence in an account binding under assumptions. Payment authority depends on role, amount, separation of duties, context, transaction binding, and current policy.

**Conclusion:** Authenticate first; authorize the exact operation independently.

### Example 8

**Question:** A valid MAC-protected command arrives twice. Should both be executed?

**Reasoning:** Both copies can pass origin/integrity verification. The protocol needs a sequence, nonce, epoch, expiry, and durable replay decision appropriate to retries.

**Conclusion:** Authenticity without freshness and idempotency can preserve an unsafe replay.

### Example 9

**Question:** Ransomware encrypts a database. Which properties can fail?

**Reasoning:** Unauthorized replacement destroys data integrity; loss of usable access harms availability; exfiltration before encryption harms confidentiality; forged operator messages can harm authenticity.

**Conclusion:** Incidents cross property categories; response evidence should classify each affected asset and stage.

### Example 10

**Question:** A digitally signed medication order is authentic. May an infusion system execute it automatically?

**Reasoning:** The signature does not prove patient association, prescriber authority for this drug, dose and unit correctness, freshness, revocation, allergy checks, device state, or safe delivery. Availability pressure must not bypass clinical controls.

**Conclusion:** Named clinical, pharmacy, biomedical, security, safety, and regulatory authorities must validate the full workflow and residual risk. This chapter claims no certification or external review.

## Cross-Program Connections

[Database Engineering](../../18-database-engineering/ROADMAP.md) owns constraints, transactions, durability, and recovery mechanisms that support—but do not define—security integrity and availability. [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies isolation, privilege, and resource governance. [Network Engineering](../../24-network-engineering/ROADMAP.md) supplies reachability, transport, segmentation, and denial evidence.

[Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) develops service objectives, incident response, change controls, backup, and recovery. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) develops replication, consistency, ordering, and partial-failure models.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects security properties to stakeholder needs, hazards, verification, validation, and lifecycle assurance. [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) owns application request identity, authorization semantics, idempotency, and error contracts.

## References

- National Institute of Standards and Technology, [*FIPS 199 — Standards for Security Categorization of Federal Information and Information Systems*](https://csrc.nist.gov/pubs/fips/199/final), 2004, official current record checked 2026-08-29. Primary confidentiality, integrity, availability, and impact definitions in its federal categorization scope.
- NIST Computer Security Resource Center, [*Authenticity — Glossary*](https://csrc.nist.gov/glossary/term/authenticity), current source-linked definitions checked 2026-08-29. Genuineness, verifiability, trust, and purported data origin across NIST publications.
- Joint Task Force, [*NIST SP 800-53 Rev. 5 — Security and Privacy Controls for Information Systems and Organizations*](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final), current final control catalog and Release 5.2.0 materials checked 2026-08-29.
- Ron Ross, Mark Winstead, and Michael McEvilley, [*NIST SP 800-160 Vol. 1 Rev. 1 — Engineering Trustworthy Secure Systems*](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final), 2022. Systems-security engineering, protection needs, assurance, and lifecycle reasoning.
- National Institute of Standards and Technology, [*The NIST Cybersecurity Framework 2.0*](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20), 2024. Current Govern, Identify, Protect, Detect, Respond, and Recover outcome framework.
- ISO/IEC, [*ISO/IEC 27000:2026 — Information Security Management Systems: Overview*](https://committee.iso.org/standard/27000), sixth edition, official published record checked 2026-08-29. Current overview of ISMS concepts, principles, and standards relationships; not a requirements standard.
- Robert Shirey, [*RFC 4949 — Internet Security Glossary, Version 2*](https://www.rfc-editor.org/info/rfc4949/), IETF Informational, 2007. Detailed distinctions among confidentiality, data integrity, source integrity, authentication, availability, and related services.
- Jerome H. Saltzer and Michael D. Schroeder, [*The Protection of Information in Computer Systems*](https://doi.org/10.1109/PROC.1975.9939), `Proceedings of the IEEE` 63(9), 1975. Foundational protection design principles and access-control framing.

## Exercises

### Exercise 1

For a university transcript service, write one scoped objective each for confidentiality, integrity, availability, and authenticity. Name the asset, actors, lifecycle, violation criterion, mechanism candidates, and evidence.

### Exercise 2

Classify what a keyed message authentication code can and cannot establish. Cover byte integrity, data origin, individual identity, confidentiality, authorization, freshness, non-repudiation, availability, key compromise, and factual correctness.

### Exercise 3

A three-region service has replicated application and database tiers but one global identity provider and one deployment control plane. Construct the availability argument, common-failure counterexamples, degraded-mode requirements, and decisive exercises.

### Exercise 4

Review an analytics platform that encrypts source records, publishes aggregate statistics, signs reports, retains extensive debug logs, and restores nightly backups. Identify at least two unproven obligations for each of confidentiality, integrity, availability, and authenticity.

### Exercise 5

A regional electricity operator receives authenticated control commands through redundant networks. Build an assurance plan for confidentiality, integrity, availability, authenticity, freshness, safety, degraded operation, incident recovery, and named human review.

## Answers to the Exercises

### Answer 1

Confidentiality: only the student, explicitly authorized staff, and approved recipients may receive that student's transcript content or existence metadata through portals, exports, logs, backups, and support tools; foreign disclosure is violation. Integrity: every grade, credit, identity binding, correction, and deletion must follow authorized academic rules with attributable before/after evidence; any bypass or untraceable change is violation. Availability: authorized students and staff can retrieve or update permitted records within declared deadlines and capacity during registration peaks and named failures, with a defined read-only degraded mode and recovery time. Authenticity: a verifier can establish that an issued transcript corresponds to the institution, student, version, issuance time, and revocation state under the approved credential policy.

Candidate mechanisms include tenant/record authorization, encryption and minimization, workflow constraints, separation of duties, signed/versioned artifacts, resilient dependencies, quotas, backup/restore, monitoring, and revocation. Evidence combines data-flow inspection, cross-student negative tests, transition invariants, privileged-path review, peak/failure exercises, restore tests, credential vectors, revocation tests, and registrar validation. Each objective separately records administrators, compromised endpoints, inference, disaster scope, and external-recipient behavior as included risks or exclusions.

### Answer 2

Under a suitable construction and secret-key assumptions, a MAC can establish that protected bytes were not modified outside the key-holding trust boundary and that a party with the shared key produced the tag. It does not distinguish individual holders of a shared key. It does not conceal plaintext, authorize the requested operation, prove freshness, prevent replay, prove service availability, establish factual correctness, or ordinarily provide non-repudiation because verifiers with the key can also create tags.

The protocol must bind algorithm, context, identities/roles, complete message fields, sequence or nonce, version, and key identifier as appropriate. Key generation, distribution, storage, rotation, revocation, compromise detection, and recovery are part of the claim. After key compromise, both past and future conclusions depend on construction and timeline; a successful comparison alone cannot locate when or by whom a tag was created.

### Answer 3

The three regions remove some regional compute, storage, network, and facility failures if each has sufficient capacity, consistent state, independent dependencies, routable health decisions, and tested recovery. The global identity provider can still block all new sessions or authorization. The deployment plane can distribute a destructive configuration or revoke healthy capacity everywhere. Shared software, secrets, DNS, certificate authority, provider account, quotas, telemetry, operators, and replicated corruption are additional common failures.

Define which existing sessions continue when identity is unavailable, what locally cached authority is safe and for how long, which operations become read-only or denied, how revocation risk is bounded, and how regional operators recover without the global deployment plane. Exercise identity outage, stale/revoked credentials, control-plane compromise and unavailability, bad global release, regional partition, database corruption, secret loss, capacity after one/two regions fail, failback, and backup restoration. Correlate user outcomes, security violations, latency, state divergence, and accountable decisions; a traffic failover alone is inadequate.

### Answer 4

Confidentiality remains unproved for debug logs, encryption keys and endpoints, aggregate inference, small groups, metadata, temporary files, exports, analyst access, and deletion. Integrity remains unproved for source correctness, transformation logic, dataset/version lineage, authorized corrections, report content before signing, signing-key custody, and backup corruption. Availability remains unproved for key and identity dependencies, query capacity, restore duration, backup completeness, regional/provider failures, denial attacks, and usable degraded outputs. Authenticity remains unproved for source identity, analyst and pipeline authority, report-to-dataset binding, signer enrollment, version/freshness, revocation, recipient verification policy, and whether a genuine report describes reality correctly.

Evidence should trace selected records through ingestion, transformation, aggregation, report signing, publication, logging, retention, backup, and restore; test inference and cross-tenant access; compare transformations with independent invariants; exercise key loss, corrupted backups, capacity and dependency failure; and validate signature context, lineage, version, expiry, and revocation. Encryption, aggregation, signatures, logs, and backups are mechanism facts, not completed property claims.

### Answer 5

Inventory commands, telemetry, topology, credentials, keys, operator authority, clocks, logs, recovery artifacts, grid assets, and human/physical safety outcomes. Confidentiality scope covers control data and sensitive topology where disclosure creates harm. Integrity binds command type, target, parameters, units, constraints, state, approval, and execution feedback. Authenticity binds operators/devices, control centers, software, and message origin to governed enrollment and revocation. Freshness uses durable sequence/epoch, bounded time, replay state, and restart rules. Availability defines authorized command and observation deadlines, capacity, partitions, denial load, dependency failure, and safe degraded operation.

Test unauthorized disclosure, privilege crossing, malformed and conflicting commands, replay, reordering, duplication, stale clocks, key compromise/rotation, identity outage, network partition, site and power failure, control-plane failure, corrupted updates, overload, failover/failback, manual operation, independent protection, restoration, and incident communications. Validate that loss of communications or security services moves equipment to a physically safe and operable state under the hazard analysis rather than a generic fail-open or fail-closed rule.

Named grid operations, protection/control, electrical safety, SCADA/OT, network, identity/cryptography, cybersecurity, reliability, human-factors, incident-response, field maintenance, vendor, regulatory, and independent assurance authorities review their evidence. The accountable operator and authorized regulator or assessor own residual-risk acceptance. Internal tests, HMAC examples, and this course review provide no operational authorization, certification, or external review.
