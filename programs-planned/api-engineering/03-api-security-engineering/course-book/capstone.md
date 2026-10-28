# Capstone — API Security Engineering

## One continuing platform

The capstone is the Analysis Runs Platform. Principals create projects, register datasets, submit analysis runs, observe progress, retrieve verified artifacts, and receive or consume completion facts. Course 3 does not replace the platform; it adds the responsibility **defend the promise**.

## Starting state

The Course 2 API 1.2 durable-service handoff and migrations 001–005.

## Course increments

| Module | Platform increment |
|---:|---|
| 1 | Create a security case that traces threats to requirements, control owners, tests, and residual risk. |
| 2 | Establish host, forwarding, media-type, strict-JSON, body-size, and canonicalization rules before model validation. |
| 3 | Implement issuer, audience, algorithm, key, lifetime, revocation, subject, tenant, and scope validation. |
| 4 | Build explicit authorization decisions for collections, individual resources, fields, support access, and administration. |
| 5 | Harden input parsing, Unicode, traversal, MIME, streaming upload, checksum, query, and error behavior. |
| 6 | Implement destination policy, address classification, peer verification, exact-byte signatures, freshness, rotation, and replay defense. |
| 7 | Add secret-provider boundaries, non-rendering values, redaction, pseudonymization, rotation, and privacy-bounded audit records. |
| 8 | Introduce principal/tenant/operation/cost budgets, concurrency permits, quotas, and bounded degradation. |
| 9 | Build hostile vectors, negative policy tests, planted vulnerabilities, dependency evidence, SBOM/provenance routes, and scanner disposition. |
| 10 | Run a controlled credential and cross-tenant incident with timelines, revocation, rotation, release, and threat-model revision. |


## Language tracks

Choose one primary implementation track. Compare policy decisions and externally observable security outcomes across both languages.

Shared fixtures, vectors, operation maps, releases, and black-box scenarios define parity. Identical class names or directory shape do not.

## Capstone reading order

1. read the module chapter and identify the owning mechanism;
2. inspect the narrow source path named by the chapter;
3. inspect the corresponding test or vector;
4. run the focused proof;
5. perform the lab modification in a working branch;
6. return to the chapter and explain how the implementation realizes the model.

## Handoff discipline

The predecessor material is read-only evidence. The current course may add a compatible public interface, migration, or profile only when its release rules permit it. It must not rewrite earlier history to simplify the present implementation.

**Outgoing handoff:** Security Profile 1.0, migrations 006–007, threat-to-requirement traceability, identity and authorization policy, hostile-input vectors, secure webhook rules, abuse controls, and incident evidence.

## Final capstone question

Can you trace one accepted case and one rejected, failed, overloaded, or duplicated case from the public boundary to the authoritative outcome, then name the proof and limitation at every layer this course owns?
