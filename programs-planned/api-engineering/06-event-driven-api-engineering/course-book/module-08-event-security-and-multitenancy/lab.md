# Lab — Reject forged, cross-tenant, sensitive, and replayed events

## Objective

Apply producer and consumer authorization, canonical signatures, tenant isolation, payload minimization, and distinct live/historical replay controls.

## Setup conditions


1. Load `producer-grants.yaml`, channel policy, and security vectors.
2. Create two tenants, two producer identities, and notification/analytics consumers.
3. Generate an active and retiring signing key using synthetic fixture material.
4. Build one valid completed event with fixed bytes and timestamp.
5. Keep all raw secrets outside evidence files.


## Failure action and investigation


Verify the valid event across Python and TypeScript. Then attempt: forged source, forbidden event type,
cross-tenant publication, sensitive payload key, altered body, unknown key ID, stale live timestamp, and
wildcard unauthorized consumer.

Demonstrate normal duplicate delivery of the valid event and an authorized historical replay from trusted
storage. Rotate to the new key under overlap. Plant a noncanonical serializer and require cross-language
signature failure.



### Investigation notes

Before editing, write a one-sentence hypothesis answering: **How are producers authenticated, consumers authorized, tenants isolated, payloads minimized, and event bytes protected?** Record the first observation that contradicts the expected model. After the repair, explain why the capstone can now claim: Add producer policy, tenant-scoped subscriptions/replay, exact-byte signatures, freshness, classification, and privacy rules. A passing command without this causal explanation is insufficient.

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


## Cleanup and reset


Revoke fixture credentials, clear synthetic keys from runtime state, remove planted serializer code, reset
consumer projections, and scan evidence for secret values. Preserve only non-secret digests and policy
results.


## Completion gate


The lab passes only when producer authority is bound to authenticated identity, tenant isolation survives
storage and consumption, signatures are cross-language stable, and the learner can explain why legitimate
replay is allowed without weakening live ingress protection.
