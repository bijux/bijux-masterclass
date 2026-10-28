# Lab — Approve fewer services than you reject

**Module:** Distribution Economics, Boundary Evidence, and Architecture Fitness Functions

## Objective

Use the Course 7 boundary dossier and measured criteria to decide which capabilities deserve extraction.

## Setup

Freeze the predecessor handoff. Load the boundary scorecard and the current transaction, event, RPC, and ownership records.

## Controlled actions

1. Fill every score with a cited source: change history, transaction boundary, workload, security rule, or owner statement.
2. Approve Notification Delivery, conditionally approve Artifact Delivery, and keep Analysis Control cohesive.
3. Reject Project Service, Dataset Table Service, and Idempotency Service with concrete failure paths.
4. Write reversal criteria for every approved and retained boundary.
5. Run `make boundary-proof` and inspect the machine-readable report.

## Correctness oracle

Every approved service has one owner, autonomous writes or an explicitly non-data role, independent value, acceptable coordination cost, and reversal criteria. At least three attractive but harmful services are rejected.

## Required evidence

- `capstone/architecture/boundary-scorecard.yaml`
- `capstone/architecture/adr/0001-keep-analysis-control-cohesive.md`
- `reports/module-01-boundary-proof.json`

## Cleanup

Restore the canonical scorecard after experimentation and remove any unapproved service entries.

## Completion gate

The scorecard and ADR proof pass, and you can defend one rejection as rigorously as one extraction.

A successful command without the required evidence does not complete the lab.
