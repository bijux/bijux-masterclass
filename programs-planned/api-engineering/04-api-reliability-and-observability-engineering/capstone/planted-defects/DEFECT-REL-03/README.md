# DEFECT-REL-03 — Global circuit

This planted defect targets Module 03: Dependency Resilience and Graceful Degradation. It is not active in the reference implementation.

## Defect

Introduce the failure pattern **Global circuit** so that the observed symptom is: Unrelated operations fail together.

## Expected detection

The decisive oracle is operation-scoped state. The focused command is `make module-proof MODULE=03`.

## Repair rule

Restore the module invariant without weakening the oracle, then retain a focused regression and run `make core-proof`.

## Safety

Apply only inside a disposable copy or version-control branch. Do not alter predecessor artifacts or shared real data.
