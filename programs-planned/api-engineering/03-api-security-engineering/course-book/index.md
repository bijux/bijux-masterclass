# API Security Engineering

**Course 3 of 10 — Defend the promise**

## Course promise

Derive, implement, and adversarially verify security properties around the durable service without replacing engineering judgment with middleware or scanner output.

> **Governing question:** How does the API remain trustworthy when callers, credentials, inputs, destinations, dependencies, and networks cannot be trusted by default?

## Place in the program

**Incoming boundary:** The Course 2 API 1.2 durable-service handoff and migrations 001–005.

**Outgoing boundary:** Security Profile 1.0, migrations 006–007, a threat-to-requirement security case, identity and authorization policy, hostile-input vectors, SSRF and webhook protections, abuse controls, and incident evidence.

Course 3 treats its incoming handoff as historical evidence, not editable scaffolding. It may add only the defend the promise mechanisms governed here; any public or durable change requires an explicit compatibility and release decision.

## What you will add

- threat modeling and security requirements;
- strict request and credential validation;
- tenant-, scope-, role-, and ownership-aware authorization;
- hostile input, file, outbound request, and webhook controls;
- secrets, audit, abuse, supply-chain, and incident-response evidence;

## Course-level learning outcomes

- Identify assets, actors, entry points, and trust boundaries.
- Define direct-client and trusted-proxy behavior.
- Accept exactly one credential mechanism.
- Separate authentication from authorization.
- Distinguish schema validation from semantic security validation.
- Reject forbidden schemes, ports, credentials, fragments, and address ranges.
- Distinguish hashing, HMAC, encryption, and password hashing.
- Choose rate-limit dimensions from abuse paths.
- Trace tests to threats and requirements.
- Design actionable security events and audit records.

## Module map

| Day | Chapter | Governing question | Capstone increment |
|---:|---|---|---|
| 1 | [Threat Modeling and Security Requirements](module-01-threat-modeling/index.md) | Which assets, actors, trust boundaries, abuse cases, and assumptions define the real security problem? | Create a security case that traces threats to requirements, control owners, tests, and residual risk. |
| 2 | [HTTP Edge and Canonicalization](module-02-http-edge-and-canonicalization/index.md) | Which raw HTTP message should the application trust after proxies, parsers, duplicate fields, and size limits intervene? | Establish host, forwarding, media-type, strict-JSON, body-size, and canonicalization rules before model validation. |
| 3 | [Authentication and Token Validation](module-03-authentication-and-token-validation/index.md) | How should a resource server validate bearer tokens and API keys without trusting convenient claims? | Implement issuer, audience, algorithm, key, lifetime, revocation, subject, tenant, and scope validation. |
| 4 | [Authorization and Policy Enforcement](module-04-authorization-and-policy-enforcement/index.md) | How are scopes, roles, ownership, tenant membership, relationships, assurance, and freshness combined under default deny? | Build explicit authorization decisions for collections, individual resources, fields, support access, and administration. |
| 5 | [Hostile Input and File Handling](module-05-hostile-input-and-file-handling/index.md) | How are hostile strings, numbers, paths, filenames, uploads, and serialized structures constrained at the correct boundary? | Harden input parsing, Unicode, traversal, MIME, streaming upload, checksum, query, and error behavior. |
| 6 | [Outbound HTTP, SSRF, and Webhook Integrity](module-06-outbound-http-ssrf-and-webhooks/index.md) | How can outbound HTTP and webhook delivery avoid SSRF, rebinding, redirect abuse, tampering, and replay? | Implement destination policy, address classification, peer verification, exact-byte signatures, freshness, rotation, and replay defense. |
| 7 | [Secrets, Cryptography, and Sensitive Data](module-07-secrets-cryptography-and-sensitive-data/index.md) | How should secrets, cryptographic keys, sensitive fields, logs, retention, and audit evidence be handled? | Add secret-provider boundaries, non-rendering values, redaction, pseudonymization, rotation, and privacy-bounded audit records. |
| 8 | [Abuse Resistance and Resource Budgets](module-08-abuse-resistance-and-resource-budgets/index.md) | How can the service resist brute force and resource exhaustion without turning traffic control into false authorization? | Introduce principal/tenant/operation/cost budgets, concurrency permits, quotas, and bounded degradation. |
| 9 | [Adversarial Verification and Supply-Chain Assurance](module-09-adversarial-verification-and-supply-chain/index.md) | How do adversarial tests and supply-chain evidence show that controls fail closed and that the proof is sensitive? | Build hostile vectors, negative policy tests, planted vulnerabilities, dependency evidence, SBOM/provenance routes, and scanner disposition. |
| 10 | [Security Operations and Incident Response](module-10-security-operations-and-incident-response/index.md) | How is a suspected compromise detected, contained, investigated, rotated, patched, and converted into improved requirements? | Run a controlled credential and cross-tenant incident with timelines, revocation, rotation, release, and threat-model revision. |

## Deliberate boundaries

This course does not claim or teach the following as part of its completion:

- building a production authorization server;
- generic penetration-testing instruction;
- compliance certification;
- operated key-management infrastructure;

Those boundaries prevent the course from becoming a survey of adjacent tools and make its completion claims defensible.

## How to study

Begin with [Start here](start-here.md). In Course 3, read each chapter around the question **How does the API remain trustworthy when callers, credentials, inputs, destinations, dependencies, and networks cannot be trusted by default?**; then use the exercises, controlled lab, and checkpoint to turn the explanation into evidence. [Language strategy](language-strategy.md) and [Evidence model](evidence-model.md) define how implementation and proof support—not replace—the course book.

## Completion

Complete all ten checkpoints, the capstone release or defense, and the outgoing handoff. A green command without a defensible claim and evidence boundary is not sufficient.
