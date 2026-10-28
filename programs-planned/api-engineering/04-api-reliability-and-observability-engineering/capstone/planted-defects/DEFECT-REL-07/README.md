# DEFECT-REL-07 — Async child misuse

This planted defect targets Module 07: Distributed Tracing Across HTTP, Workers, Storage, and Webhooks. It is not active in the reference implementation.

## Defect

Introduce the failure pattern **Async child misuse** so that the observed symptom is: Trace appears hours long and cancellation semantics lie.

## Expected detection

The decisive oracle is topology review. The focused command is `make module-proof MODULE=07`.

## Repair rule

Restore the module invariant without weakening the oracle, then retain a focused regression and run `make core-proof`.

## Safety

Apply only inside a disposable copy or version-control branch. Do not alter predecessor artifacts or shared real data.
