# Checkpoint — Progressive delivery

## Required evidence

- A canary or blue-green plan with immutable identities.
- Minimum-sample, delay, segment, and missing-data rules.
- A data compatibility matrix and rollback frontier.
- A tested abort that reconciles cluster and Git state.

## Decision defense

- Defend the selected analysis metrics.
- Explain actual versus configured traffic.
- Explain when forward fix replaces rollback.

## Progression gate

Advance only when progressive exposure is a falsifiable experiment with a tested abort path.
