# Lab — Reject the wrong RPCs before generating code

**Module:** RPC Boundaries, Service Ownership, and Interaction Choice

## Objective

Publish an interaction decision record, service-ownership map, and minimal Analysis RPC surface without splitting the platform prematurely.

## Setup

Load the current HTTP operation ledger, event catalogue, and Course 6 ownership records. Do not edit the RPC contract yet.

## Controlled actions

1. Classify twelve proposed interactions as local call, HTTP, durable event, unary RPC, server stream, client stream, or bidirectional stream.
2. For every proposed RPC, fill in contract, state, deadline, retry, and operational ownership.
3. Reject at least three RPC candidates and record the concrete coupling or failure they would introduce.
4. Approve the minimal AnalysisControlService, DatasetTransferService, and WorkerPlaneService capability boundaries.
5. Run `make boundary-proof` to compare the decision record with the contract skeleton.

## Correctness oracle

Every approved RPC has one authority, one caller need for synchronous communication, a deadline owner, a retry position, and a named operational owner. No approved service is merely a table wrapper.

## Required evidence

- `capstone/rpc-case/interaction-decisions.yaml`
- `capstone/rpc-case/service-ownership.yaml`
- `reports/module-01-boundary-proof.json`

## Cleanup

Restore the contract skeleton if experimentation added unapproved services or methods.

## Completion gate

The boundary proof passes and you can defend one rejection as clearly as one approval.

A successful command without this evidence does not complete the lab.
