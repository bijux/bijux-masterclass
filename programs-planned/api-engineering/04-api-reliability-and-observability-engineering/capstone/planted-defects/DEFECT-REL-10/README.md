# DEFECT-REL-10 — No incident lead

This planted defect targets Module 10: Incident Command, State Reconciliation, and Operational Readiness. It is not active in the reference implementation.

## Defect

Introduce the failure pattern **No incident lead** so that the observed symptom is: Conflicting actions and priorities.

## Expected detection

The decisive oracle is role/timeline audit. The focused command is `make module-proof MODULE=10`.

## Repair rule

Restore the module invariant without weakening the oracle, then retain a focused regression and run `make core-proof`.

## Safety

Apply only inside a disposable copy or version-control branch. Do not alter predecessor artifacts or shared real data.
