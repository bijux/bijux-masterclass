# Checkpoint — Helm chart engineering

## Required evidence

- A values API and JSON Schema.
- Previous-to-current upgrade fixtures.
- Chart and render digests.
- A rejected unsafe hook candidate and repaired migration design.

## Decision defense

- Explain chart version versus application version versus image digest.
- Defend the CRD ownership choice.
- Explain the selected GitOps Helm integration mode.

## Progression gate

Advance only when chart rendering, package identity, upgrade compatibility, and side-effect ownership are separately evidenced.
