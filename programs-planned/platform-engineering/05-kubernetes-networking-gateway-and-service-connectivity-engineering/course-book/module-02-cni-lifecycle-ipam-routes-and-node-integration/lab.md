# Lab — Recover a leaked allocation without stealing a live address

## Goal

Exercise ADD partial failure, repeated DEL, and authoritative GC.

## Safety boundary

Use only the dependency-light simulator or an isolated disposable cluster. Do not alter shared cluster networking, cloud routes, production DNS, or host firewall state.

## Baseline

The model has two Nodes, one allocation pool, three known-good attachments, and one stale cached allocation created by an interrupted ADD.

## Hypothesis

A generation-bound GC request can reclaim the stale allocation, while a name-only cleanup can incorrectly delete a recreated Pod’s address.

## Controlled action

Run `python3 capstone/scripts/cni_lifecycle_lab.py`. Compare safe GC with the planted name-only cleanup defect.

## Oracle

Safe GC removes exactly the stale attachment, repeated DEL is a no-op success, and the live recreated attachment retains its address.

## Required evidence

Generated lifecycle ledger, allocation table before/after, command results, and a written explanation of the authority used by GC.

## Interpretation

The important property is not “free the address.” It is reclaiming only after the old attachment is proved absent within the GC authority boundary.

## Cleanup

Run `make clean`; verify no allocation or report files remain outside fixtures.

## Completion gate

The safe algorithm passes, the name-only mutant is rejected, and the report explains why control-plane deletion alone is not enough.
