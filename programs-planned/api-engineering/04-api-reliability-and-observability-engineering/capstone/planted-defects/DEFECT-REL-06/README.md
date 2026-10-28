# DEFECT-REL-06 — Unique-ID label

This planted defect targets Module 06: Metrics and Service-Level Indicators. It is not active in the reference implementation.

## Defect

Introduce the failure pattern **Unique-ID label** so that the observed symptom is: Series grow with traffic.

## Expected detection

The decisive oracle is series cardinality test. The focused command is `make module-proof MODULE=06`.

## Repair rule

Restore the module invariant without weakening the oracle, then retain a focused regression and run `make core-proof`.

## Safety

Apply only inside a disposable copy or version-control branch. Do not alter predecessor artifacts or shared real data.
