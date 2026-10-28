# Capstone — API Security Engineering

## Cumulative system

Course 3 continues the Analysis Runs Platform at the point where the previous course stopped. Its capstone exists to defend the promise while preserving the same projects, datasets, runs, artifacts, identities, and user journeys.

## Inherited state

The Course 2 API 1.2 durable-service handoff and migrations 001–005.

The inherited boundary is read-only: The Course 2 API 1.2 durable-service handoff and migrations 001–005. A difficult implementation is not permission to rewrite predecessor contracts, migrations, profiles, or evidence; the current course must solve the problem at its own owning layer.

## Course additions

- threat modeling and security requirements;
- strict request and credential validation;
- tenant-, scope-, role-, and ownership-aware authorization;
- hostile input, file, outbound request, and webhook controls;
- secrets, audit, abuse, supply-chain, and incident-response evidence;

## Increment map

| Module | Mechanism | Cumulative result |
|---:|---|---|
| 1 | Threat Modeling and Security Requirements | Create a security case that traces threats to requirements, control owners, tests, and residual risk. |
| 2 | HTTP Edge and Canonicalization | Establish host, forwarding, media-type, strict-JSON, body-size, and canonicalization rules before model validation. |
| 3 | Authentication and Token Validation | Implement issuer, audience, algorithm, key, lifetime, revocation, subject, tenant, and scope validation. |
| 4 | Authorization and Policy Enforcement | Build explicit authorization decisions for collections, individual resources, fields, support access, and administration. |
| 5 | Hostile Input and File Handling | Harden input parsing, Unicode, traversal, MIME, streaming upload, checksum, query, and error behavior. |
| 6 | Outbound HTTP, SSRF, and Webhook Integrity | Implement destination policy, address classification, peer verification, exact-byte signatures, freshness, rotation, and replay defense. |
| 7 | Secrets, Cryptography, and Sensitive Data | Add secret-provider boundaries, non-rendering values, redaction, pseudonymization, rotation, and privacy-bounded audit records. |
| 8 | Abuse Resistance and Resource Budgets | Introduce principal/tenant/operation/cost budgets, concurrency permits, quotas, and bounded degradation. |
| 9 | Adversarial Verification and Supply-Chain Assurance | Build hostile vectors, negative policy tests, planted vulnerabilities, dependency evidence, SBOM/provenance routes, and scanner disposition. |
| 10 | Security Operations and Incident Response | Run a controlled credential and cross-tenant incident with timelines, revocation, rotation, release, and threat-model revision. |

## Implementation route

Build the complete Course 3 increment in one primary track. Use the second track only after the chapter model is clear, then run shared vectors to test whether **defend the promise** survives an idiomatic implementation in another runtime.

## Final state

Security Profile 1.0, migrations 006–007, a threat-to-requirement security case, identity and authorization policy, hostile-input vectors, SSRF and webhook protections, abuse controls, and incident evidence.

## Handoff discipline

The successor receives only the settled result: Security Profile 1.0, migrations 006–007, a threat-to-requirement security case, identity and authorization policy, hostile-input vectors, SSRF and webhook protections, abuse controls, and incident evidence. Local caches, secrets, ad-hoc reports, and environment-specific artifacts remain outside the handoff.
