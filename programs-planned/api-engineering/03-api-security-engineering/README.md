# API Security Engineering

**Course 3 of 6 — Defend the promise**

Preserve the API and durable-service guarantees when callers, credentials, inputs, destinations, and dependencies are not trusted by default.

> How does the service remain trustworthy under hostile behavior without hiding behind middleware or scanner output?

## Begin with the course book

1. Read [Course introduction](course-book/index.md).
2. Complete [Start here](course-book/start-here.md) and [orientation](course-book/module-00-orientation/index.md).
3. Follow the ten modules in order.
4. Use the capstone and implementation tracks only through the reading routes named in each chapter.
5. Preserve checkpoint evidence before progressing.

## Modules

01. [Threat Modeling and Security Requirements](course-book/module-01-threat-modeling/index.md)
02. [HTTP Edge and Canonicalization](course-book/module-02-http-edge-and-canonicalization/index.md)
03. [Authentication and Token Validation](course-book/module-03-authentication-and-token-validation/index.md)
04. [Authorization and Policy Enforcement](course-book/module-04-authorization-and-policy-enforcement/index.md)
05. [Hostile Input and File Handling](course-book/module-05-hostile-input-and-file-handling/index.md)
06. [Outbound HTTP, SSRF, and Webhook Integrity](course-book/module-06-outbound-http-ssrf-and-webhooks/index.md)
07. [Secrets, Cryptography, and Sensitive Data](course-book/module-07-secrets-cryptography-and-sensitive-data/index.md)
08. [Abuse Resistance and Resource Budgets](course-book/module-08-abuse-resistance-and-resource-budgets/index.md)
09. [Adversarial Verification and Supply-Chain Assurance](course-book/module-09-adversarial-verification-and-supply-chain/index.md)
10. [Security Operations and Incident Response](course-book/module-10-security-operations-and-incident-response/index.md)

## Program boundary

**Incoming:** The Course 2 API 1.2 durable-service handoff and migrations 001–005.

**Outgoing:** Security Profile 1.0, migrations 006–007, threat-to-requirement traceability, identity and authorization policy, hostile-input vectors, secure webhook rules, abuse controls, and incident evidence.

## Implementation strategy

Choose one primary implementation track. Compare policy decisions and externally observable security outcomes across both languages.

## Verification

```bash
make doctor
make core-proof
make manifest-proof
```

Environment-dependent routes are reported separately. Missing infrastructure is never represented as a passing live proof.
