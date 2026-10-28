# Checkpoint — controller fit and retry semantics

## Required evidence

- controller-choice dossier;
- Job duplicate-attempt transcript;
- exactly-once effect record;
- CronJob overlap decision;
- DaemonSet ownership and privilege justification.

## Decision defense

Choose one proposed Atlas task that should not be a CronJob and explain the better owner.

## Progression gate

Proceed only when controller completion semantics and business-effect semantics are no longer conflated.
