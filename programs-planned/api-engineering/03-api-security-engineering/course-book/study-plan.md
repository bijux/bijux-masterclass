# Ten-Day Study Plan — API Security Engineering

This is a dense two-week course with one numbered module per weekday. Orientation is required before Day 1 and is not counted as a teaching module. The middle weekend contains no hidden new curriculum.

| Day | Module | Main intellectual move | Required result |
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


## Daily rhythm

A productive day uses four blocks:

- **Model:** read the chapter and reconstruct the governing diagram or state machine;
- **Transfer:** answer the exercises and compare with the reasoned answers;
- **Experiment:** perform the lab, including the failure or pressure condition;
- **Defense:** complete the checkpoint and preserve evidence.

Do not treat “morning to night” as uninterrupted screen time. Use deliberate breaks. Stop blind copying when fatigue removes your ability to predict outcomes.

## Middle weekend

Use Saturday for at most one focused repair cycle per failed checkpoint and for a cross-module synthesis note. Sunday contains no required implementation. Rerun predecessor and accumulated course proofs before Week 2.

## Recovery rule

When behind, reduce breadth before reducing evidence. Complete one language track deeply, keep the comparison focused, and do not skip the failure experiment. A copied second implementation is less valuable than one defended invariant.
