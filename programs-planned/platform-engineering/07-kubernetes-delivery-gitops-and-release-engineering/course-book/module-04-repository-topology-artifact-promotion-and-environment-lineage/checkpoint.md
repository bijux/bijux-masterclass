# Checkpoint — Repository topology and promotion

## Required evidence

- An authority map for source, artifacts, desired state, and release evidence.
- A three-environment release lineage.
- Immutable artifact and render identities.
- Rejected rebuild and history-rewrite candidates.

## Decision defense

- Defend the repository topology.
- Explain evidence freshness.
- Explain why a revert is a new release decision.

## Progression gate

Advance only when promotion can be audited without trusting mutable tags, branches, or ephemeral pipeline state.
