# Reference Answers — Module 01: Threat Modeling and Security Requirements

Read after attempting all twelve Threat Modeling and Security Requirements exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Rewrite “attackers may steal data” as a concrete threat.

**Answer.** A tenant-authenticated caller enumerates artifact IDs, supplies an ID owned by another tenant, and receives bytes because the retrieval query checks scope but not tenant ownership.

## 2. Distinguish an asset from a security property.

**Answer.** The artifact content is the asset; confidentiality and integrity are properties the system aims to preserve.

## 3. Why is a private JWKS signing key in a fixture directory an assumption and an asset?

**Answer.** It is an asset because compromise enables forged fixture tokens; its controlled custody is an assumption because the course does not operate an HSM or production key service.

## 4. What makes a requirement falsifiable?

**Answer.** It names actor, object, condition, required decision, and observable failure or success so a counterexample can contradict it.

## 5. Why can one threat map to several requirements?

**Answer.** A stolen token may require short lifetime, revocation, authorization, audit, and abuse budgets; no single control covers the whole scenario.

## 6. Why can one requirement answer several threats?

**Answer.** A default-deny owner-aware query can reduce cross-tenant reads through multiple endpoints and identifier substitution paths.

## 7. Give one trust boundary inside a single process.

**Answer.** The boundary between raw HTTP bytes and parsed application data changes interpretation and must reject ambiguous representations.

## 8. What is wrong with “all dependencies are trusted”?

**Answer.** It is too broad, hides supply-chain and failure assumptions, and cannot guide verification or incident response.

## 9. When should a threat be accepted rather than mitigated?

**Answer.** When residual impact and likelihood are understood, within tolerance, and the acceptance has an owner, expiry/review condition, and monitoring or rationale.

## 10. What proof detects an orphan requirement?

**Answer.** A traceability checker that requires each requirement ID to be referenced by at least one proof and control owner.

## 11. Trace threat-to-control traceability in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_security/models.py` and `capstone/tracks/typescript-fastify/src/security/models.ts`. The required invariant is that every accepted threat names an asset, boundary, security requirement, control owner, test, and residual risk.

## 12. Compare threat-to-control traceability across Python and TypeScript

Both tracks must preserve this invariant: every accepted threat names an asset, boundary, security requirement, control owner, test, and residual risk. The intentional difference is that Python dataclasses and TypeScript interfaces differ; threat identifiers and policy facts are shared artifacts.
