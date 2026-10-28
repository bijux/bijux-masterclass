# Checkpoint 07 — Snapshots, Clones, Populators, and Consistency

## Required evidence

- completed exercise responses and corrections;
- the lab evidence named in `lab.md`;
- one machine-readable Atlas capstone artifact;
- one failure trace that identifies the earliest missing transition;
- one explicit `not-executed` entry for evidence outside the current environment, if applicable.

## Decision defense

Defend this statement in no more than 500 words:

> A snapshot coordinator records consistency level, application checkpoint, source generation, grouped volumes, retention, and restore verification.

Your defense must name the authoritative state, the writer or controller allowed to mutate it, the rollback or recovery boundary, and the proof that would falsify the design.

## Progression gate

Do not advance until the evidence supports the governing question: **What does a point-in-time copy actually contain, and what coordination is required before it can be trusted for recovery or testing?**
