# Lab — Extract two services and defend keeping the rest together

**Module:** Incremental Extraction, Strangler Migration, and Final Architecture Defense

## Objective

Execute the staged Notification and Artifact extraction, prove rollback and decommission, and publish the Course 9 handoff.

## Setup

Start from the verified modular baseline, extraction plan, service-owned migrations, and clean reconciliation state.

## Controlled actions

1. Shadow and cut over Notification Delivery using event replay with external effects controlled.
2. Backfill and checksum Artifact data, shadow reads, then move write and read authority in stages.
3. Inject candidate divergence and execute rollback before final cutover.
4. Decommission legacy writers and routes only after the declared evidence window.
5. Run `make final-defense-proof`, generate the outgoing handoff, and defend every retained boundary.

## Correctness oracle

Public HTTP, event, and RPC contracts remain valid; extracted services own their data; Analysis Control remains cohesive; rollback works; final reconciliation is empty.

## Required evidence

- `capstone/architecture/extraction-plan.yaml`
- `capstone/final-defense/architecture-summary.json`
- `capstone/handoff/`
- `reports/module-10-final-defense.json`

## Cleanup

Return the laboratory to the accepted distributed-1.0 topology and remove temporary shadow/backfill state.

## Completion gate

Final defense and handoff proofs pass, with zero shared writers, zero sync cycles, and zero unexplained reconciliation findings.

A successful command without the required evidence does not complete the lab.
