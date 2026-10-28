# DEFECT-REL-04 — Collapsed health endpoint

This planted defect targets Module 04: Lifecycle, Health, Graceful Shutdown, and Recovery. It is not active in the reference implementation.

## Defect

Introduce the failure pattern **Collapsed health endpoint** so that the observed symptom is: Routers and restart controllers receive the same signal.

## Expected detection

The decisive oracle is separate state and probe tests. The focused command is `make module-proof MODULE=04`.

## Repair rule

Restore the module invariant without weakening the oracle, then retain a focused regression and run `make core-proof`.

## Safety

Apply only inside a disposable copy or version-control branch. Do not alter predecessor artifacts or shared real data.
