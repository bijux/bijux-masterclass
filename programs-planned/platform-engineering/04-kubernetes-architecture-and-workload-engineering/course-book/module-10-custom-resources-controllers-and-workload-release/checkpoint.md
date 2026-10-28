# Checkpoint — Atlas Kubernetes Workload 1.0

## Required evidence

- CRD schema and version decision;
- idempotent reconcile transcript;
- child ownership and field-management map;
- current-generation status conditions;
- finalizer repair evidence;
- accepted release report;
- exact Course 5 handoff verification.

## Decision defense

Defend why AtlasWorkload exists, which responsibilities it deliberately excludes, and how it could be retired without trapping owned or external state.

## Progression gate

Course 4 is complete only when the workload can be traced from released image digest through API intent, controller children, scheduling, lifecycle, availability, and connectivity requirements without an unexplained ownership gap.
