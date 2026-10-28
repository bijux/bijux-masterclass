# Lab — Module 02: HTTP Edge and Canonicalization

> **Module 02:** HTTP Edge and Canonicalization

## Objective

Run the same hostile raw-message corpus through Python and TypeScript adapters. Plant a trust-all forwarding mode and a plain JSON parser, capture the policy bypasses, repair them, and retain regressions.

## Why this lab matters

This lab turns the module’s governing question—**Which raw HTTP message should the application trust after proxies, parsers, duplicate fields, and size limits intervene?**—into a falsifiable experiment. Register a Fastify content-type parser for JSON that receives text or bytes, applies the same duplicate/depth/number profile, and returns a parsed value. Use an onRequest hook for raw headers and proxy policy before authentication. Avoid relying on plain JSON.parse for duplicate-member detection.

It advances the cumulative Analysis Runs Platform by requiring this result: **Establish host, forwarding, media-type, strict-JSON, body-size, and canonicalization rules before model validation**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **The capstone gains a machine-readable threat catalog, security requirements, operation policies, and residual-risk record.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *Which bytes and proxy assertions does the application actually trust before framework parsing begins?*

## Hypothesis

The clean implementation should satisfy this claim: **Define direct-client and trusted-proxy behavior; Reject ambiguous singleton headers and duplicate JSON members; Normalize only after preserving raw evidence; Enforce content type and body limits before model validation; Separate browser CORS policy from API authentication.** When the lab introduces this fault—**Remove or bypass the central control and prove the predicted oracle fails**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Freeze the baseline that currently provides: FastAPI and Fastify reject ambiguous edge input consistently before application models are constructed.
2. Construct the smallest local counterexample to: Which bytes and proxy assertions does the application actually trust before framework parsing begins?
3. Implement and test the control needed to define direct-client and trusted-proxy behavior.
4. Exercise the valid boundary and at least two hostile boundaries from the shared vectors.
5. Remove or bypass the central control and prove the predicted oracle fails.
6. Restore the control and verify separate browser CORS policy from API authentication.
7. Compare the secondary track through the shared security outcome.
8. Clean runtime state and retain only the minimized regression and named evidence.

### Required planted defect

Remove or bypass the central control for **HTTP Edge and Canonicalization** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Remove or bypass the central control and prove the predicted oracle fails**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Run the same hostile raw-message corpus through Python and TypeScript adapters. Plant a trust-all forwarding mode and a plain JSON parser, capture the policy bypasses, repair them, and retain regressions**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- Define direct-client and trusted-proxy behavior.
- Reject ambiguous singleton headers and duplicate JSON members.
- Normalize only after preserving raw evidence.
- Enforce content type and body limits before model validation.
- Separate browser CORS policy from API authentication.

## Required evidence

- baseline transcript proving the previous checkpoint before **HTTP Edge and Canonicalization** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **HTTP Edge and Canonicalization**
- focused result for: Define direct-client and trusted-proxy behavior.
- public, durable, security, or operational observation showing: FastAPI and Fastify reject ambiguous edge input consistently before application models are constructed.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **raw HTTP edge evaluation**
- a limitation statement naming every live dependency required to support the strongest **HTTP Edge and Canonicalization** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **HTTP Edge and Canonicalization**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Remove or bypass the central control and prove the predicted oracle fails** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Restore the control changed for **HTTP Edge and Canonicalization**.
2. Remove the temporary data, faults, credentials, permits, files, or delivery state created by the **HTTP Edge and Canonicalization** experiment.
3. Rerun the focused regression and `make module-proof MODULE=02`.
4. Confirm the system again provides this result: FastAPI and Fastify reject ambiguous edge input consistently before application models are constructed.

## Completion gate

- Define direct-client and trusted-proxy behavior.
- Reject ambiguous singleton headers and duplicate JSON members.
- Normalize only after preserving raw evidence.
- Enforce content type and body limits before model validation.
- Separate browser CORS policy from API authentication.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **HTTP Edge and Canonicalization**. A green command without the negative case and causal explanation does not satisfy this gate.
