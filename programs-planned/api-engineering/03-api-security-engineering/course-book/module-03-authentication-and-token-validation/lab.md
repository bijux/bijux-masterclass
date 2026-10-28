# Lab — Module 03: Authentication and Token Validation

## Objective

Issue controlled valid and invalid tokens, execute the full rejection matrix, rotate JWKS with overlap, revoke one `jti`, and prove API-key verification. Plant an audience bypass and show the cross-audience token is accepted before repair.


## Setup conditions

The previous baseline is: **FastAPI and Fastify reject ambiguous edge input consistently before application models are constructed.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How does a resource server establish one unambiguous caller identity from an untrusted credential?*

## Failure action and investigation

1. Freeze the baseline that currently provides: Fixture credentials are replaced by a deterministic but realistic resource-server validation boundary.
2. Construct the smallest local counterexample to: How does a resource server establish one unambiguous caller identity from an untrusted credential?
3. Implement and test the control needed to accept exactly one credential mechanism.
4. Exercise the valid boundary and at least two hostile boundaries from the shared vectors.
5. Remove or bypass the central control and prove the predicted oracle fails.
6. Restore the control and verify store API-key digests rather than reusable keys.
7. Compare the secondary track through the shared security outcome.
8. Clean runtime state and retain only the minimized regression and named evidence.

### Required planted defect

Remove or bypass the central control for **Authentication and Token Validation** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

## Operational oracle

The system satisfies the chapter’s central question: How does a resource server establish one unambiguous caller identity from an untrusted credential? The result must be visible through public behavior or durable state, not inferred only from logs.

## Required evidence

- baseline transcript proving the previous checkpoint before **Authentication and Token Validation** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Accept exactly one credential mechanism.
- public, durable, security, or operational observation showing: Fixture credentials are replaced by a deterministic but realistic resource-server validation boundary.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **resource-server credential validation**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **Authentication and Token Validation**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
3. Rerun the focused regression and `make module-proof MODULE=03`.
4. Confirm the system again provides this result: Fixture credentials are replaced by a deterministic but realistic resource-server validation boundary.

## Completion gate

- Accept exactly one credential mechanism.
- Select accepted JWT algorithms from server configuration.
- Validate signature, type, issuer, audience, time, subject, tenant, scopes, and token ID.
- Handle key rotation and unknown key identifiers safely.
- Store API-key digests rather than reusable keys.
