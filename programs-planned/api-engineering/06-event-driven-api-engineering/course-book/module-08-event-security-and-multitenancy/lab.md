# Lab — Reject forged, cross-tenant, sensitive, and replayed events

> **Module 08:** Event Security, Multi-Tenancy, Privacy, and Trust

## Objective

Apply producer and consumer authorization, canonical signatures, tenant isolation, payload minimization, and distinct live/historical replay controls.

## Why this lab matters

This lab turns the module’s governing question—**How are producers authenticated, consumers authorized, tenants isolated, payloads minimized, and event bytes protected?**—into a falsifiable experiment. An attacker replays the signed body through live ingress after the freshness window; ingress rejects it. An authorized operator later launches a bounded historical replay from the trusted retained stream; that path uses replay authorization and event dedupe rather than pretending the original signature is fresh.

It advances the cumulative Analysis Runs Platform by requiring this result: **Add producer policy, tenant-scoped subscriptions/replay, exact-byte signatures, freshness, classification, and privacy rules**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

1. Load `producer-grants.yaml`, channel policy, and security vectors.
2. Create two tenants, two producer identities, and notification/analytics consumers.
3. Generate an active and retiring signing key using synthetic fixture material.
4. Build one valid completed event with fixed bytes and timestamp.
5. Keep all raw secrets outside evidence files.

## Hypothesis

The clean implementation should satisfy this claim: **Only the valid authorized event, legitimate duplicate, and approved historical replay reach handlers. Forged, cross-tenant, sensitive, altered, unknown-key, stale-ingress, and unauthorized-subscription cases are rejected with safe evidence. Both languages agree on signature bytes. Rotation has no rejection gap.** When the lab introduces this fault—**Plant a noncanonical serializer and require cross-language signature failure**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

Verify the valid event across Python and TypeScript. Then attempt: forged source, forbidden event type,
cross-tenant publication, sensitive payload key, altered body, unknown key ID, stale live timestamp, and
wildcard unauthorized consumer.

Demonstrate normal duplicate delivery of the valid event and an authorized historical replay from trusted
storage. Rotate to the new key under overlap. Plant a noncanonical serializer and require cross-language
signature failure.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Plant a noncanonical serializer and require cross-language signature failure**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Apply producer and consumer authorization, canonical signatures, tenant isolation, payload minimization, and distinct live/historical replay controls**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

Only the valid authorized event, legitimate duplicate, and approved historical replay reach handlers.
Forged, cross-tenant, sensitive, altered, unknown-key, stale-ingress, and unauthorized-subscription cases are
rejected with safe evidence. Both languages agree on signature bytes. Rotation has no rejection gap.

## Required evidence

- `work/module-08/authorization-matrix.yaml`
- `work/module-08/signature-vectors.json`
- `work/module-08/rejection-evidence.json`
- `work/module-08/key-rotation-timeline.md`
- cross-tenant projection assertions
- live-versus-historical replay comparison
- output from `make security-proof`

## Interpretation and defense

1. Which state or effect is authoritative for **Event Security, Multi-Tenancy, Privacy, and Trust**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Plant a noncanonical serializer and require cross-language signature failure** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Revoke fixture credentials, clear synthetic keys from runtime state, remove planted serializer code, reset
consumer projections, and scan evidence for secret values. Preserve only non-secret digests and policy
results.

## Completion gate

The lab passes only when producer authority is bound to authenticated identity, tenant isolation survives
storage and consumption, signatures are cross-language stable, and the learner can explain why legitimate
replay is allowed without weakening live ingress protection.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Event Security, Multi-Tenancy, Privacy, and Trust**. A green command without the negative case and causal explanation does not satisfy this gate.
