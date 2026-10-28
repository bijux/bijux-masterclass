# Checkpoint — Event Security, Multi-Tenancy, Privacy, and Trust

Do not progress because the chapter has been read. Progress when the following evidence can be reproduced from a clean working tree.

## Demonstrate

- Distinguish broker authentication, publication authorization, message integrity, and business truth.
- Explain tenant scope across envelope, broker, inbox, projection, replay, and audit.
- Describe exact-byte signing and cross-language canonicalization.
- Separate live replay attack prevention from authorized historical replay.

## Required result

- `work/module-08/authorization-matrix.yaml`
- `work/module-08/signature-vectors.json`
- `work/module-08/rejection-evidence.json`
- `work/module-08/key-rotation-timeline.md`
- `work/module-08/residual-risk.md`

## Commands

```bash
make security-proof
make vector-proof
make module-proof MODULE=08 TRACK=$TRACK
```

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

The checkpoint is complete only when all commands pass, all artifacts are reviewable, and each oral-defense question can be answered without appealing to a broker feature as magic.
