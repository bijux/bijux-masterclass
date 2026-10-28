# DEFECT-REL-09 — No hypothesis

This planted defect targets Module 09: Fault Injection, Troubleshooting, and Game Days. It is not active in the reference implementation.

## Defect

Introduce the failure pattern **No hypothesis** so that the observed symptom is: Experiment produces anecdotes.

## Expected detection

The decisive oracle is plan validation. The focused command is `make module-proof MODULE=09`.

## Repair rule

Restore the module invariant without weakening the oracle, then retain a focused regression and run `make core-proof`.

## Safety

Apply only inside a disposable copy or version-control branch. Do not alter predecessor artifacts or shared real data.
