# Checkpoint 01 — Data Lifetimes, Durability, and Storage Responsibility

## Required evidence

- completed exercise responses and corrections;
- the lab evidence named in `lab.md`;
- one machine-readable Atlas capstone artifact;
- one failure trace that identifies the earliest missing transition;
- one explicit `not-executed` entry for evidence outside the current environment, if applicable.

## Decision defense

Defend this statement in no more than 500 words:

> A machine-readable data catalogue assigns lifetime, authority, RPO, RTO, writer count, retention, and deletion ownership to every Atlas data class.

Your defense must name the authoritative state, the writer or controller allowed to mutate it, the rollback or recovery boundary, and the proof that would falsify the design.

## Progression gate

Do not advance until the evidence supports the governing question: **What must survive, who owns it, and which failure domain is allowed to destroy it?**
