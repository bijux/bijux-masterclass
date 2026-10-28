# Checkpoint — Secrets and trust gates

## Required evidence

- A secret authority and plaintext-lifetime map.
- Separated repository read and automation write identities.
- Digest-bound artifact policy evidence.
- A completed rotation with no plaintext leakage.

## Decision defense

- Defend the selected secret strategy.
- Explain layered policy locations.
- Explain why admission and GitOps ownership must align.

## Progression gate

Advance only when delivery convenience does not create universal secret or artifact authority.
