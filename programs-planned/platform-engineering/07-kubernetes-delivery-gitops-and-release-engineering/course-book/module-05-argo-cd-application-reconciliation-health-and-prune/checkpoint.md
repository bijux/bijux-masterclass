# Checkpoint — Argo CD reconciliation

## Required evidence

- Application and AppProject authority definitions.
- A sync, health, journey, and data gate matrix.
- Wave and hook evidence.
- Protected-resource prune rejection and no-op steady state.

## Decision defense

- Defend Application boundaries.
- Explain the difference among auto-sync, self-heal, and prune.
- Explain repository and controller outage behavior.

## Progression gate

Advance only when the learner can diagnose the earliest failed Argo CD transition and bound the controller’s authority.
