# API Security Engineering

**Course 3 of 6 — Defend the promise**

> **Central question:** How does the service remain trustworthy under hostile behavior without hiding behind middleware or scanner output?

## Course responsibility

Preserve the API and durable-service guarantees when callers, credentials, inputs, destinations, and dependencies are not trusted by default. The course inherits earlier guarantees rather than restating them as new work. Its purpose is to add one mature engineering responsibility to the same Analysis Runs Platform.

## Incoming and outgoing boundaries

**Incoming boundary:** The Course 2 API 1.2 durable-service handoff and migrations 001–005.

**Outgoing boundary:** Security Profile 1.0, migrations 006–007, threat-to-requirement traceability, identity and authorization policy, hostile-input vectors, secure webhook rules, abuse controls, and incident evidence.

## What you will be able to do

After completing the course, you can:

- create a security case that traces threats to requirements, control owners, tests, and residual risk.
- establish host, forwarding, media-type, strict-JSON, body-size, and canonicalization rules before model validation.
- implement issuer, audience, algorithm, key, lifetime, revocation, subject, tenant, and scope validation.
- build explicit authorization decisions for collections, individual resources, fields, support access, and administration.
- harden input parsing, Unicode, traversal, MIME, streaming upload, checksum, query, and error behavior.
- implement destination policy, address classification, peer verification, exact-byte signatures, freshness, rotation, and replay defense.
- add secret-provider boundaries, non-rendering values, redaction, pseudonymization, rotation, and privacy-bounded audit records.
- introduce principal/tenant/operation/cost budgets, concurrency permits, quotas, and bounded degradation.
- build hostile vectors, negative policy tests, planted vulnerabilities, dependency evidence, SBOM/provenance routes, and scanner disposition.
- run a controlled credential and cross-tenant incident with timelines, revocation, rotation, release, and threat-model revision.

## Ten-module learning path

| Day | Module | Governing question | Capstone result |
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


## How the book is organized

Each numbered module has five learner-facing files:

1. `index.md` — the complete explanation, worked designs, implementation reading, failure analysis, and transition;
2. `exercises.md` — twelve transfer questions;
3. `exercise-answers.md` — matching reasoned reference answers;
4. `lab.md` — one controlled failure, pressure, or release experiment;
5. `checkpoint.md` — the evidence required before progression.

The course book is authoritative. Capstone source, fixtures, reports, and proof scripts make the material executable; they do not replace the explanation.

## Completion standard

You complete the course only when every module checkpoint, the capstone proof, and the final defense pass. A strong result states not only what worked but which claim was established, which evidence class supports it, and what remains unexecuted.

Continue with [Start here](start-here.md).
