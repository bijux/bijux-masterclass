# DEFECT-REL-02 — Relative timeout reset

This planted defect targets Module 02: Deadlines, Timeouts, Cancellation, and Retry Budgets. It is not active in the reference implementation.

## Defect

Introduce the failure pattern **Relative timeout reset** so that the observed symptom is: Nested operations exceed caller budget.

## Expected detection

The decisive oracle is absolute expiry assertion. The focused command is `make module-proof MODULE=02`.

## Repair rule

Restore the module invariant without weakening the oracle, then retain a focused regression and run `make core-proof`.

## Safety

Apply only inside a disposable copy or version-control branch. Do not alter predecessor artifacts or shared real data.
