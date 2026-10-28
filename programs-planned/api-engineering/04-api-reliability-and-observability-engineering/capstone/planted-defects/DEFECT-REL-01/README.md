# DEFECT-REL-01 — Component-only dashboard

This planted defect targets Module 01: Reliability Model and Critical User Journeys. It is not active in the reference implementation.

## Defect

Introduce the failure pattern **Component-only dashboard** so that the observed symptom is: All processes green while accepted runs stall.

## Expected detection

The decisive oracle is journey SLI and durable-state check. The focused command is `make module-proof MODULE=01`.

## Repair rule

Restore the module invariant without weakening the oracle, then retain a focused regression and run `make core-proof`.

## Safety

Apply only inside a disposable copy or version-control branch. Do not alter predecessor artifacts or shared real data.
