# Checkpoint — control-system ownership

## Required evidence

- Atlas component ownership map;
- before/during/after reconciliation snapshots;
- proof that repeated recovery does not duplicate children;
- explicit list of transitions not proved without kind or a real cluster.

## Decision defense

Defend the statement: “The Deployment exists” is evidence of persisted intent, not evidence that Atlas is running.

## Progression gate

Proceed only when you can locate every failed transition at the owning component and object boundary.
