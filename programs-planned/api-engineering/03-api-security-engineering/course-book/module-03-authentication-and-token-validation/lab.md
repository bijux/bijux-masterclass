# Lab — Module 03: Authentication and Token Validation

> **Module 03:** Authentication and Token Validation

## Objective

Issue controlled valid and invalid tokens, execute the full rejection matrix, rotate JWKS with overlap, revoke one `jti`, and prove API-key verification. Plant an audience bypass and show the cross-audience token is accepted before repair.

## Why this lab matters

This lab turns the module’s governing question—**How should a resource server validate bearer tokens and API keys without trusting convenient claims?**—into a falsifiable experiment. Issue controlled valid and invalid tokens, execute the full rejection matrix, rotate JWKS with overlap, revoke one jti, and prove API-key verification. Plant an audience bypass and show the cross-audience token is accepted before repair.

It advances the cumulative Analysis Runs Platform by requiring this result: **Implement issuer, audience, algorithm, key, lifetime, revocation, subject, tenant, and scope validation**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **FastAPI and Fastify reject ambiguous edge input consistently before application models are constructed.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How does a resource server establish one unambiguous caller identity from an untrusted credential?*

## Hypothesis

The clean implementation should satisfy this claim: **Accept exactly one credential mechanism; Select accepted JWT algorithms from server configuration; Validate signature, type, issuer, audience, time, subject, tenant, scopes, and token ID; Handle key rotation and unknown key identifiers safely; Store API-key digests rather than reusable keys.** When the lab introduces this fault—**Remove or bypass the central control and prove the predicted oracle fails**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

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

### Investigation notes

Before editing code, predict the first observable divergence caused by **Remove or bypass the central control and prove the predicted oracle fails**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Issue controlled valid and invalid tokens, execute the full rejection matrix, rotate JWKS with overlap, revoke one jti, and prove API-key verification. Plant an audience bypass and show the cross-audience token is accepted before repair**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- Accept exactly one credential mechanism.
- Select accepted JWT algorithms from server configuration.
- Validate signature, type, issuer, audience, time, subject, tenant, scopes, and token ID.
- Handle key rotation and unknown key identifiers safely.
- Store API-key digests rather than reusable keys.

## Required evidence

- baseline transcript proving the previous checkpoint before **Authentication and Token Validation** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Authentication and Token Validation**
- focused result for: Accept exactly one credential mechanism.
- public, durable, security, or operational observation showing: Fixture credentials are replaced by a deterministic but realistic resource-server validation boundary.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **resource-server credential validation**
- a limitation statement naming every live dependency required to support the strongest **Authentication and Token Validation** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Authentication and Token Validation**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Remove or bypass the central control and prove the predicted oracle fails** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Restore the control changed for **Authentication and Token Validation**.
2. Remove the temporary data, faults, credentials, permits, files, or delivery state created by the **Authentication and Token Validation** experiment.
3. Rerun the focused regression and `make module-proof MODULE=03`.
4. Confirm the system again provides this result: Fixture credentials are replaced by a deterministic but realistic resource-server validation boundary.

## Completion gate

- Accept exactly one credential mechanism.
- Select accepted JWT algorithms from server configuration.
- Validate signature, type, issuer, audience, time, subject, tenant, scopes, and token ID.
- Handle key rotation and unknown key identifiers safely.
- Store API-key digests rather than reusable keys.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Authentication and Token Validation**. A green command without the negative case and causal explanation does not satisfy this gate.
