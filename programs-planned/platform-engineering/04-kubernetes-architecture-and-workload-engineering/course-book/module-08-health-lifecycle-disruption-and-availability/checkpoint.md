# Checkpoint — availability contract

## Required evidence

- probe semantic matrix;
- startup and termination budgets;
- PDB calculation;
- voluntary versus involuntary disruption transcript;
- topology/capacity assumptions.

## Decision defense

Defend one dependency that belongs in readiness but not liveness and one local failure that should trigger restart.

## Progression gate

Proceed only when readiness, liveness, disruption, rollout, and service reachability are treated as separate claims.
