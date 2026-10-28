# Checkpoint — Module 08: Event Security, Multi-Tenancy, Privacy, and Trust

## Required result

Add producer policy, tenant-scoped subscriptions/replay, exact-byte signatures, freshness, classification, and privacy rules.

## Demonstrate

- Distinguish broker authentication, publication authorization, message integrity, and business truth.
- Explain tenant scope across envelope, broker, inbox, projection, replay, and audit.
- Describe exact-byte signing and cross-language canonicalization.
- Separate live replay attack prevention from authorized historical replay.

## Commands

```bash
make security-proof
make vector-proof
make module-proof MODULE=08 TRACK=$TRACK
```

## Evidence to retain

- `work/module-08/authorization-matrix.yaml`
- `work/module-08/signature-vectors.json`
- `work/module-08/rejection-evidence.json`
- `work/module-08/key-rotation-timeline.md`
- cross-tenant projection assertions
- live-versus-historical replay comparison
- output from `make security-proof`

## Defend the design

- Verify one Python-signed message in TypeScript.
- Demonstrate a cross-tenant rejection at publication and projection boundaries.
- Defend the retained payload’s data minimization.
- Walk through routine rotation and compromise response.

## Continue only when

- Producer envelope claims are trusted without authenticated binding.
- A consumer has unnecessary wildcard tenant/type access.
- Raw secrets or sensitive payloads enter event evidence.
- Freshness is confused with durable event deduplication.

The **Event Security, Multi-Tenancy, Privacy, and Trust** checkpoint is complete only when the commands pass, the retained artifacts explain the event-system state, and you can defend the result without treating broker delivery, ordering, or replay as magic.
