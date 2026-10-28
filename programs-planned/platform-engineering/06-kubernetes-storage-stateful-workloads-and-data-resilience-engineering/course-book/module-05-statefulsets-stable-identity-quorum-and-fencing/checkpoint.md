# Checkpoint 05 — StatefulSets, Stable Identity, Quorum, and Fencing

## Required evidence

- completed exercise responses and corrections;
- the lab evidence named in `lab.md`;
- one machine-readable Atlas capstone artifact;
- one failure trace that identifies the earliest missing transition;
- one explicit `not-executed` entry for evidence outside the current environment, if applicable.

## Decision defense

Defend this statement in no more than 500 words:

> A StatefulSet planner creates deterministic identities, while a fencing registry—not the Pod name—authorizes the current writer and delays readiness until recovery completes.

Your defense must name the authoritative state, the writer or controller allowed to mutate it, the rollback or recovery boundary, and the proof that would falsify the design.

## Progression gate

Do not advance until the evidence supports the governing question: **When does stable ordinal identity help, and what additional mechanisms prevent two replicas from believing they own the same data?**
