# Checkpoint 06 — Databases, Object Storage, and Operator Boundaries

## Required evidence

- completed exercise responses and corrections;
- the lab evidence named in `lab.md`;
- one machine-readable Atlas capstone artifact;
- one failure trace that identifies the earliest missing transition;
- one explicit `not-executed` entry for evidence outside the current environment, if applicable.

## Decision defense

Defend this statement in no more than 500 words:

> Atlas publishes an explicit data-service decision record, transactional-state contract, immutable-artifact contract, and operator responsibility matrix.

Your defense must name the authoritative state, the writer or controller allowed to mutate it, the rollback or recovery boundary, and the proof that would falsify the design.

## Progression gate

Do not advance until the evidence supports the governing question: **Which stateful capabilities should Kubernetes host directly, which should be external services, and which responsibilities may an operator safely automate?**
