# Checkpoint — Drift and Migration

## Required evidence

- [ ] differences are classified before remediation;
- [ ] refresh-only behavior is explained accurately;
- [ ] import includes complete configuration, post-import plan review, and data-plane validation;
- [ ] moved mappings preserve every intended remote identity;
- [ ] module and provider upgrades are separated or explicitly justified;
- [ ] state-split ownership has no duplicate writer;
- [ ] emergency drift has an owner, incident ID, and expiry or final decision;
- [ ] state surgery, if used, has backup, lock, transcript, and recovery commands;
- [ ] decommissioning distinguishes preserve, transfer, and destroy;
- [ ] final behavior is verified outside the state file.

## Decision defense

Choose one migration and explain how you proved identity preservation, writer ownership, safe intermediate states, and recoverability. Contrast the evidence for a refactor, an import, and a real remote change; a clean final plan alone cannot distinguish them.

## Progression gate

Progression requires a migration dossier with before-and-after addresses, remote IDs, plans, commands, behavioral evidence, and rollback or roll-forward instructions. A successful command transcript alone does not pass.
