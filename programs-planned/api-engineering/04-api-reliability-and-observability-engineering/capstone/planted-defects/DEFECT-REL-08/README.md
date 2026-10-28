# DEFECT-REL-08 — Unversioned objective

This planted defect targets Module 08: SLOs, Error Budgets, Dashboards, and Alerts. It is not active in the reference implementation.

## Defect

Introduce the failure pattern **Unversioned objective** so that the observed symptom is: Historical numbers change meaning.

## Expected detection

The decisive oracle is catalog history. The focused command is `make module-proof MODULE=08`.

## Repair rule

Restore the module invariant without weakening the oracle, then retain a focused regression and run `make core-proof`.

## Safety

Apply only inside a disposable copy or version-control branch. Do not alter predecessor artifacts or shared real data.
