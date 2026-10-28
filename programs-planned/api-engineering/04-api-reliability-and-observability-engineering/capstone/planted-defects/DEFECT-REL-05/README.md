# DEFECT-REL-05 — Free-form event vocabulary

This planted defect targets Module 05: Telemetry Architecture and Structured Operational Events. It is not active in the reference implementation.

## Defect

Introduce the failure pattern **Free-form event vocabulary** so that the observed symptom is: Queries and alerts silently diverge.

## Expected detection

The decisive oracle is schema conformance. The focused command is `make module-proof MODULE=05`.

## Repair rule

Restore the module invariant without weakening the oracle, then retain a focused regression and run `make core-proof`.

## Safety

Apply only inside a disposable copy or version-control branch. Do not alter predecessor artifacts or shared real data.
