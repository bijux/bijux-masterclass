# Checkpoint 09 — Storage Performance, Observability, Quotas, and Failure Diagnosis

## Required evidence

- completed exercise responses and corrections;
- the lab evidence named in `lab.md`;
- one machine-readable Atlas capstone artifact;
- one failure trace that identifies the earliest missing transition;
- one explicit `not-executed` entry for evidence outside the current environment, if applicable.

## Decision defense

Defend this statement in no more than 500 words:

> Atlas publishes storage SLOs, capacity budgets, failure signatures, quota policy, and before/after evidence for one service-tier mutation.

Your defense must name the authoritative state, the writer or controller allowed to mutate it, the rollback or recovery boundary, and the proof that would falsify the design.

## Progression gate

Do not advance until the evidence supports the governing question: **How do we distinguish slow applications, saturated storage, controller lag, mount failure, quota exhaustion, and capacity risk before data service quality collapses?**
