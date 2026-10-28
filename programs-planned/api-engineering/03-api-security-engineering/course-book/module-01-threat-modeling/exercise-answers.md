# Worked Answers — Module 01: Threat Modeling and Security Requirements

Use these solutions to audit your reasoning for **Threat Modeling and Security Requirements**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Rewrite “attackers may steal data” as a concrete threat.

A tenant-authenticated caller enumerates artifact IDs, supplies an ID owned by another tenant, and receives bytes because the retrieval query checks scope but not tenant ownership.

The chapter’s decisive distinction is this: A useful threat model is a set of claims that can be revised, not a diagram created once and archived. Begin with an asset and the security property that matters. “Artifact” is an asset category; “a principal cannot read an artifact owned by another tenant” is a security property. The second statement can drive an authorization rule, a database-query constraint, an adversarial test, an audit event, and an incident signal.

## 2. Distinguish an asset from a security property.

The artifact content is the asset; confidentiality and integrity are properties the system aims to preserve.

In the cumulative capstone, the rule becomes concrete: A useful threat model is a set of claims that can be revised, not a diagram created once and archived. Begin with an asset and the security property that matters. “Artifact” is an asset category; “a principal cannot read an artifact owned by another tenant” is a security property. The second statement can drive an authorization rule, a database-query constraint, an adversarial test, an audit event, and an incident signal.

## 3. Why is a private JWKS signing key in a fixture directory an assumption and an asset?

It is an asset because compromise enables forged fixture tokens; its controlled custody is an assumption because the course does not operate an HSM or production key service.

A useful way to reason about the boundary is: A passed unit test does not erase risk. The local course issuer does not prove production identity assurance. An in-process rate limiter does not prove multi-replica enforcement. A hash-chained local audit file does not prevent a privileged operator from replacing both the file and its anchor. Record those boundaries rather than hiding them.

## 4. What makes a requirement falsifiable?

It names actor, object, condition, required decision, and observable failure or success so a counterexample can contradict it.

The implementation consequence is: A control may mitigate several threats, and one threat may require several controls. Do not collapse the chain into one row called “OAuth.” OAuth can establish or transport authorization information; it does not by itself constrain object ownership, filenames, webhook destinations, or storage paths.

**Evidence.** Remove the central guard in a planted variant and require the negative security suite to detect the exact unauthorized or leaked outcome.

## 5. Why can one threat map to several requirements?

A stolen token may require short lifetime, revocation, authorization, audit, and abuse budgets; no single control covers the whole scenario.

The important nuance is: Use dataclasses or frozen Pydantic models for assets, threats, requirements, and proof links. The checker must reject duplicate IDs, unknown references, requirements without proof, and accepted threats without disposition. Keep the model independent from FastAPI.

**Evidence.** Remove the central guard in a planted variant and require the negative security suite to detect the exact unauthorized or leaked outcome.

## 6. Why can one requirement answer several threats?

A default-deny owner-aware query can reduce cross-tenant reads through multiple endpoints and identifier substitution paths.

Under concurrency or failure, the distinction becomes: Accepted residual risk also needs an owner and review trigger. A risk accepted for a local single-tenant fixture may become unacceptable after multi-tenant exposure; a control considered sufficient before public webhook registration may no longer cover the new egress path. Incidents and planted defects feed back into the model: update the failed assumption or requirement, add the minimized counterexample, and preserve the new regression.

## 7. Give one trust boundary inside a single process.

The boundary between raw HTTP bytes and parsed application data changes interpretation and must reject ambiguous representations.

The design remains honest only if: Model the system through data flows. For each flow, record the sender, receiver, protocol, credential, mutable fields, durable effect, and trust transition. In the Analysis Runs platform, the transition from public API to application use case is different from the transition from worker to artifact store, even when both execute inside one repository. A trust boundary is not synonymous with a network hop.

## 8. What is wrong with “all dependencies are trusted”?

It is too broad, hides supply-chain and failure assumptions, and cannot guide verification or incident response.

The consumer-facing consequence is: Security work begins with an explicit argument about assets, attacker capabilities, trust changes, requirements, assumptions, and residual risk. A long vulnerability list without prioritization or proof ownership is not a security model.

**Counterexample.** A happy-path control accepts semantically hostile input or leaks the evidence needed to refine an attack.

**Evidence.** Remove the central guard in a planted variant and require the negative security suite to detect the exact unauthorized or leaked outcome.

## 9. When should a threat be accepted rather than mitigated?

When residual impact and likelihood are understood, within tolerance, and the acceptance has an owner, expiry/review condition, and monitoring or rationale.

The operational consequence is: Risk ranking should change sequencing, not create false precision. Use likelihood and impact descriptions tied to assumptions: whether identifiers are guessable, whether the endpoint is Internet-reachable, whether a credential already exists, and whether compromise crosses tenants. Revisit the rank when an assumption changes. A low-ranked internal webhook threat becomes different after a proxy route exposes registration publicly.

## 10. What proof detects an orphan requirement?

A traceability checker that requires each requirement ID to be referenced by at least one proof and control owner.

The strongest engineering interpretation is: Use discriminated TypeScript types for threat disposition and proof status. A never exhaustiveness check should make a newly introduced disposition fail compilation until handling is added. Parse machine-readable files into unknown values before validation.

**Evidence.** Remove the central guard in a planted variant and require the negative security suite to detect the exact unauthorized or leaked outcome.

## 11. Trace threat-to-control traceability in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_security/models.py` and `capstone/tracks/typescript-fastify/src/security/models.ts`. The required invariant is that every accepted threat names an asset, boundary, security requirement, control owner, test, and residual risk.

The defect-oriented view is: The Threat Modeling and Security Requirements cases are bounded course fixtures. Trace the attacker-controlled value through every interpreter, then identify the policy decision and smallest rejection evidence; do not target external systems.

## 12. Compare threat-to-control traceability across Python and TypeScript

Both tracks must preserve this invariant: every accepted threat names an asset, boundary, security requirement, control owner, test, and residual risk. The intentional difference is that Python dataclasses and TypeScript interfaces differ; threat identifiers and policy facts are shared artifacts.

Across the Python and TypeScript tracks, the invariant is: Version the security case with the service. Re-review it when an operation, credential type, trust boundary, dependency, data classification, administrative capability, or deployment route changes. A release diff should state which threats were added, retired, re-ranked, or left unchanged and which assumptions were invalidated. “No security impact” is a conclusion that needs evidence, not a default label.
