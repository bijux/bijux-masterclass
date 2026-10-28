# Checkpoint 08 — Backup, Restore, RPO, RTO, and Disaster Recovery

## Required evidence

- completed exercise responses and corrections;
- the lab evidence named in `lab.md`;
- one machine-readable Atlas capstone artifact;
- one failure trace that identifies the earliest missing transition;
- one explicit `not-executed` entry for evidence outside the current environment, if applicable.

## Decision defense

Defend this statement in no more than 500 words:

> A content-addressed backup repository, manifest chain, empty-destination restore, domain verification, and measured RPO/RTO report form the Atlas recovery dossier.

Your defense must name the authoritative state, the writer or controller allowed to mutate it, the rollback or recovery boundary, and the proof that would falsify the design.

## Progression gate

Do not advance until the evidence supports the governing question: **How can the platform prove that authoritative data can be reconstructed in a clean environment within an agreed loss and time budget?**
