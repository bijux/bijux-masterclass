# Checkpoint — Module 03: Authentication and Token Validation

## Required result

Fixture credentials are replaced by a deterministic but realistic resource-server validation boundary.

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

## Defend the design

1. Answer the central question: **How does a resource server establish one unambiguous caller identity from an untrusted credential?**
2. Demonstrate this capstone result: Fixture credentials are replaced by a deterministic but realistic resource-server validation boundary.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: algorithm, key, type, issuer, audience, time, subject, tenant, token ID, scopes, and revocation are all required by profile.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—Fixture credentials are replaced by a deterministic but realistic resource-server validation boundary.—all focused checks pass, the **Authentication and Token Validation** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
