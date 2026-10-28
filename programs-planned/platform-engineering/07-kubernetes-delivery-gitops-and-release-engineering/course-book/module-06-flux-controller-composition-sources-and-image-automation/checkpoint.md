# Checkpoint — Flux controller composition

## Required evidence

- A source-to-apply dependency graph.
- Generation-aware readiness expressions.
- A bounded image automation policy.
- Equivalent Atlas safety invariants for Argo CD and Flux.

## Decision defense

- Explain source artifact identity.
- Explain HelmRelease lifecycle differences.
- Explain controller upgrade and CRD coupling.

## Progression gate

Advance only when the learner can identify the first failed controller-owned transition and preserve immutable promotion identity.
