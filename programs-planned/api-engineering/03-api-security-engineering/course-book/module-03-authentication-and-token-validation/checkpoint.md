# Checkpoint — Module 03: Authentication and Token Validation

## Required result

Implement issuer, audience, algorithm, key, lifetime, revocation, subject, tenant, and scope validation.

## Demonstrate

- Accept exactly one credential mechanism.
- Select accepted JWT algorithms from server configuration.
- Validate signature, type, issuer, audience, time, subject, tenant, scopes, and token ID.
- Handle key rotation and unknown key identifiers safely.
- Store API-key digests rather than reusable keys.

## Commands

```bash
make module-proof MODULE=03 TRACK=python
make module-proof MODULE=03 TRACK=typescript
make core-proof
```

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Authentication and Token Validation** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Authentication and Token Validation**
- focused result for: Accept exactly one credential mechanism.
- public, durable, security, or operational observation showing: Fixture credentials are replaced by a deterministic but realistic resource-server validation boundary.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **resource-server credential validation**
- a limitation statement naming every live dependency required to support the strongest **Authentication and Token Validation** claim but not exercised

## Defend the design

1. Answer the central question: **How does a resource server establish one unambiguous caller identity from an untrusted credential?**
2. Demonstrate this capstone result: Fixture credentials are replaced by a deterministic but realistic resource-server validation boundary.
3. Show the **Authentication and Token Validation** defect, the first failing oracle, and the exact regression retained after repair.
4. Explain why this invariant is shared across languages: algorithm, key, type, issuer, audience, time, subject, tenant, token ID, scopes, and revocation are all required by profile.
5. State which environment-backed **Authentication and Token Validation** route was not run and how that limits the claim.

## Continue only when

Continue when the system again provides this module result—Fixture credentials are replaced by a deterministic but realistic resource-server validation boundary.—all focused checks pass, the **Authentication and Token Validation** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
