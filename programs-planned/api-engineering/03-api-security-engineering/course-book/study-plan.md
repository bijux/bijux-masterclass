# Two-Week Study Plan — API Security Engineering

## Rhythm

Course 3 uses ten teaching days over two weeks. Orientation freezes the incoming boundary before Day 1; each day moves from the defend the promise model to transfer problems, a controlled experiment, and an evidence defense. The middle weekend is for repairing failed checkpoints, not adding features.

| Day | Module | Required result |
|---:|---|---|
| 1 | [Threat Modeling and Security Requirements](module-01-threat-modeling/index.md) | Create a security case that traces threats to requirements, control owners, tests, and residual risk. |
| 2 | [HTTP Edge and Canonicalization](module-02-http-edge-and-canonicalization/index.md) | Establish host, forwarding, media-type, strict-JSON, body-size, and canonicalization rules before model validation. |
| 3 | [Authentication and Token Validation](module-03-authentication-and-token-validation/index.md) | Implement issuer, audience, algorithm, key, lifetime, revocation, subject, tenant, and scope validation. |
| 4 | [Authorization and Policy Enforcement](module-04-authorization-and-policy-enforcement/index.md) | Build explicit authorization decisions for collections, individual resources, fields, support access, and administration. |
| 5 | [Hostile Input and File Handling](module-05-hostile-input-and-file-handling/index.md) | Harden input parsing, Unicode, traversal, MIME, streaming upload, checksum, query, and error behavior. |
| 6 | [Outbound HTTP, SSRF, and Webhook Integrity](module-06-outbound-http-ssrf-and-webhooks/index.md) | Implement destination policy, address classification, peer verification, exact-byte signatures, freshness, rotation, and replay defense. |
| 7 | [Secrets, Cryptography, and Sensitive Data](module-07-secrets-cryptography-and-sensitive-data/index.md) | Add secret-provider boundaries, non-rendering values, redaction, pseudonymization, rotation, and privacy-bounded audit records. |
| 8 | [Abuse Resistance and Resource Budgets](module-08-abuse-resistance-and-resource-budgets/index.md) | Introduce principal/tenant/operation/cost budgets, concurrency permits, quotas, and bounded degradation. |
| 9 | [Adversarial Verification and Supply-Chain Assurance](module-09-adversarial-verification-and-supply-chain/index.md) | Build hostile vectors, negative policy tests, planted vulnerabilities, dependency evidence, SBOM/provenance routes, and scanner disposition. |
| 10 | [Security Operations and Incident Response](module-10-security-operations-and-incident-response/index.md) | Run a controlled credential and cross-tenant incident with timelines, revocation, rotation, release, and threat-model revision. |

## Suggested day

```text
08:30  retrieval practice and checkpoint repair
09:00  chapter reading and diagram reconstruction
11:00  worked examples and standards review
13:00  primary-track implementation reading
15:00  exercises before answers
17:00  controlled lab
19:30  evidence package and checkpoint defense
```

The two-week schedule is subordinate to evidence. If the defend the promise argument becomes unclear, stop at the last green checkpoint, reduce the counterexample, and resume only after the owning mechanism is understood.

## Weekend synthesis

At the Week 1 boundary, reconstruct how Modules 1–5 change the platform while preserving this incoming state: The Course 2 API 1.2 durable-service handoff and migrations 001–005. Rerun those checkpoints and postpone every feature that does not serve the Course 3 responsibility.

## Recovery route

When a checkpoint fails:

1. isolate the first broken invariant;
2. restore the predecessor baseline if necessary;
3. reduce the failing case;
4. repair the owning mechanism;
5. retain the case as a regression;
6. update your explanation before continuing.
