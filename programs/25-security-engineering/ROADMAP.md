# 25. Security Engineering

**Program code:** `SEC`

**Purpose:** Develop adversarial, risk-based command of designing, building, operating, and assessing trustworthy software and infrastructure.

**Level-II professional outcome:** Ready to perform threat modeling, design identity and access controls, secure applications and platforms, assess vulnerabilities, monitor attacks, and lead remediation and incident response.

**Prerequisites:** systems, networking, and software engineering fundamentals; basic probability; programming and command-line skills.

**Primary ownership:** security principles and risk; applied cryptography; identity and access; application security; systems and network security; cloud and infrastructure security; data and privacy security; software supply chain; detection and incident response; security architecture and assurance.

**Explicit exclusions:** cryptographic complexity theory (Program 15); network engineering ownership (Program 24); delivery mechanics (Program 14); platform implementation ownership (Program 29).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — Security Principles, Threats, and Risk

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **Assets, Adversaries, Trust, and Security Goals** | `001-assets-adversaries-trust-and-security-goals.md` |
| 002 | **Confidentiality, Integrity, Availability, and Authenticity** | `002-confidentiality-integrity-availability-and-authenticity.md` |
| 003 | **Threat Modeling** | `003-threat-modeling.md` |
| 004 | **Attack Surfaces and Trust Boundaries** | `004-attack-surfaces-and-trust-boundaries.md` |
| 005 | **Least Privilege** | `005-least-privilege.md` |
| 006 | **Defense in Depth** | `006-defense-in-depth.md` |
| 007 | **Fail-Safe Defaults** | `007-fail-safe-defaults.md` |
| 008 | **Security Economics and Incentives** | `008-security-economics-and-incentives.md` |
| 009 | **Risk Assessment and Treatment** | `009-risk-assessment-and-treatment.md` |
| 010 | **Writing Actionable Security Requirements** | `010-writing-actionable-security-requirements.md` |

### Block 02 — Applied Cryptographic Foundations

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **Randomness, Entropy, and Nonces** | `011-randomness-entropy-and-nonces.md` |
| 012 | **Cryptographic Hash Functions** | `012-cryptographic-hash-functions.md` |
| 013 | **Message Authentication Codes** | `013-message-authentication-codes.md` |
| 014 | **Symmetric Encryption** | `014-symmetric-encryption.md` |
| 015 | **Authenticated Encryption** | `015-authenticated-encryption.md` |
| 016 | **Public-Key Encryption** | `016-public-key-encryption.md` |
| 017 | **Digital Signatures** | `017-digital-signatures.md` |
| 018 | **Key Agreement** | `018-key-agreement.md` |
| 019 | **Certificates and Public-Key Infrastructure** | `019-certificates-and-public-key-infrastructure.md` |
| 020 | **Choosing Cryptographic Constructions Without Inventing Protocols** | `020-choosing-cryptographic-constructions-without-inventing-protocols.md` |

### Block 03 — Identity, Authentication, and Authorization

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **Digital Identity and Identity Proofing** | `021-digital-identity-and-identity-proofing.md` |
| 022 | **Password Storage and Authentication** | `022-password-storage-and-authentication.md` |
| 023 | **Multi-Factor Authentication** | `023-multi-factor-authentication.md` |
| 024 | **Session Management** | `024-session-management.md` |
| 025 | **Single Sign-On** | `025-single-sign-on.md` |
| 026 | **OAuth 2.x Authorization** | `026-oauth-2-x-authorization.md` |
| 027 | **OpenID Connect Identity Flows** | `027-openid-connect-identity-flows.md` |
| 028 | **Role-Based Access Control** | `028-role-based-access-control.md` |
| 029 | **Attribute- and Policy-Based Access Control** | `029-attribute-and-policy-based-access-control.md` |
| 030 | **Designing Authorization Around Resources and Actions** | `030-designing-authorization-around-resources-and-actions.md` |

### Block 04 — Application and API Security

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **Input Validation and Canonicalization** | `031-input-validation-and-canonicalization.md` |
| 032 | **Injection Vulnerabilities** | `032-injection-vulnerabilities.md` |
| 033 | **Cross-Site Scripting** | `033-cross-site-scripting.md` |
| 034 | **Cross-Site Request Forgery** | `034-cross-site-request-forgery.md` |
| 035 | **Server-Side Request Forgery** | `035-server-side-request-forgery.md` |
| 036 | **Broken Access Control** | `036-broken-access-control.md` |
| 037 | **Deserialization and Object Injection** | `037-deserialization-and-object-injection.md` |
| 038 | **File Upload and Path Security** | `038-file-upload-and-path-security.md` |
| 039 | **API Abuse, Rate Limits, and Enumeration** | `039-api-abuse-rate-limits-and-enumeration.md` |
| 040 | **Threat Modeling a Web and API Application** | `040-threat-modeling-a-web-and-api-application.md` |

### Block 05 — Host, Network, and Operational Security

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **Operating-System Hardening** | `041-operating-system-hardening.md` |
| 042 | **Process Isolation and Sandboxing** | `042-process-isolation-and-sandboxing.md` |
| 043 | **Patch and Vulnerability Management** | `043-patch-and-vulnerability-management.md` |
| 044 | **Firewalls and Network Segmentation** | `044-firewalls-and-network-segmentation.md` |
| 045 | **TLS Configuration** | `045-tls-configuration.md` |
| 046 | **Secure Remote Administration** | `046-secure-remote-administration.md` |
| 047 | **Secrets Management Principles** | `047-secrets-management-principles.md` |
| 048 | **Logging for Security** | `048-logging-for-security.md` |
| 049 | **Backups Against Destructive Attack** | `049-backups-against-destructive-attack.md` |
| 050 | **Building a Hardened Service Baseline** | `050-building-a-hardened-service-baseline.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — Cloud, Container, and Infrastructure Security

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **Cloud Shared-Responsibility Models** | `051-cloud-shared-responsibility-models.md` |
| 052 | **Cloud IAM and Permission Boundaries** | `052-cloud-iam-and-permission-boundaries.md` |
| 053 | **Account, Project, and Subscription Isolation** | `053-account-project-and-subscription-isolation.md` |
| 054 | **Network Security in Virtual Clouds** | `054-network-security-in-virtual-clouds.md` |
| 055 | **Container Image Security** | `055-container-image-security.md` |
| 056 | **Container Runtime Isolation** | `056-container-runtime-isolation.md` |
| 057 | **Kubernetes Security** | `057-kubernetes-security.md` |
| 058 | **Infrastructure-as-Code Security** | `058-infrastructure-as-code-security.md` |
| 059 | **Cloud Security Posture and Drift** | `059-cloud-security-posture-and-drift.md` |
| 060 | **Reviewing a Cloud Workload from Identity to Data** | `060-reviewing-a-cloud-workload-from-identity-to-data.md` |

### Block 07 — Data, Privacy, and Cryptographic Systems

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **Data Classification** | `061-data-classification.md` |
| 062 | **Encryption at Rest and in Transit** | `062-encryption-at-rest-and-in-transit.md` |
| 063 | **Key Management and Hardware Security Modules** | `063-key-management-and-hardware-security-modules.md` |
| 064 | **Tokenization and Pseudonymization** | `064-tokenization-and-pseudonymization.md` |
| 065 | **Privacy Threat Modeling** | `065-privacy-threat-modeling.md` |
| 066 | **Consent, Purpose, and Data Minimization** | `066-consent-purpose-and-data-minimization.md` |
| 067 | **Secure Multiparty Computation Concepts** | `067-secure-multiparty-computation-concepts.md` |
| 068 | **Differential Privacy Concepts** | `068-differential-privacy-concepts.md` |
| 069 | **Using Trusted Execution Environments for Data Protection** | `069-using-trusted-execution-environments-for-data-protection.md` |
| 070 | **Designing Data Protection Across Its Lifecycle** | `070-designing-data-protection-across-its-lifecycle.md` |

### Block 08 — Software Supply Chain and Product Security

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **Dependency and Package Risk** | `071-dependency-and-package-risk.md` |
| 072 | **Build-System Threats** | `072-build-system-threats.md` |
| 073 | **Artifact Provenance** | `073-artifact-provenance.md` |
| 074 | **Signing and Verification** | `074-signing-and-verification.md` |
| 075 | **SBOMs in Supply-Chain Security** | `075-sboms-in-supply-chain-security.md` |
| 076 | **Secure Development Lifecycles** | `076-secure-development-lifecycles.md` |
| 077 | **Static, Dynamic, and Composition Analysis** | `077-static-dynamic-and-composition-analysis.md` |
| 078 | **Fuzzing for Security** | `078-fuzzing-for-security.md` |
| 079 | **Coordinated Vulnerability Disclosure** | `079-coordinated-vulnerability-disclosure.md` |
| 080 | **Securing a Product from Source to Customer Update** | `080-securing-a-product-from-source-to-customer-update.md` |

### Block 09 — Detection, Investigation, and Incident Response

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **Adversary Tactics, Techniques, and Procedures** | `081-adversary-tactics-techniques-and-procedures.md` |
| 082 | **Security Telemetry and Detection Engineering** | `082-security-telemetry-and-detection-engineering.md` |
| 083 | **Endpoint Detection** | `083-endpoint-detection.md` |
| 084 | **Network Detection** | `084-network-detection.md` |
| 085 | **Identity Threat Detection** | `085-identity-threat-detection.md` |
| 086 | **Security Alert Triage** | `086-security-alert-triage.md` |
| 087 | **Digital Forensics Foundations** | `087-digital-forensics-foundations.md` |
| 088 | **Containment and Eradication** | `088-containment-and-eradication.md` |
| 089 | **Incident Communication and Legal Coordination** | `089-incident-communication-and-legal-coordination.md` |
| 090 | **Learning from a Security Incident Without Losing Evidence** | `090-learning-from-a-security-incident-without-losing-evidence.md` |

### Block 10 — Security Architecture, Assurance, and Adversarial Review

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **Zero-Trust Architecture** | `091-zero-trust-architecture.md` |
| 092 | **Capability-Secure Design** | `092-capability-secure-design.md` |
| 093 | **Security Architecture Patterns** | `093-security-architecture-patterns.md` |
| 094 | **Abuse-Case and Misuse-Case Analysis** | `094-abuse-case-and-misuse-case-analysis.md` |
| 095 | **Penetration Testing Methodology** | `095-penetration-testing-methodology.md` |
| 096 | **Red, Blue, and Purple Teaming** | `096-red-blue-and-purple-teaming.md` |
| 097 | **Security Assurance and Certification** | `097-security-assurance-and-certification.md` |
| 098 | **Security for High-Assurance and Regulated Systems** | `098-security-for-high-assurance-and-regulated-systems.md` |
| 099 | **Balancing Security, Usability, Reliability, and Cost** | `099-balancing-security-usability-reliability-and-cost.md` |
| 100 | **Conducting an Adversarial Security Architecture Review** | `100-conducting-an-adversarial-security-architecture-review.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
