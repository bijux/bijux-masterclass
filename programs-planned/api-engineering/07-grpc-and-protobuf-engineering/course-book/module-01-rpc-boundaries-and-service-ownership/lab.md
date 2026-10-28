# Lab — Reject the wrong RPCs before generating code

> **Module 01:** RPC Boundaries, Service Ownership, and Interaction Choice

## Objective

Publish an interaction decision record, service-ownership map, and minimal Analysis RPC surface without splitting the platform prematurely.

## Why this lab matters

This lab turns the module’s governing question—**Which interactions deserve a typed RPC boundary, and which should remain HTTP requests, durable events, or local function calls?**—into a falsifiable experiment. The proposed remote boundary is useful only if it preserves that ownership. A gateway can call CreateRun; Analysis Control can still perform the whole transaction. That is a coherent protocol boundary. A weaker design creates the run in one service, the job in another, and asks a third service to publish an event.

It advances the cumulative Analysis Runs Platform by requiring this result: **Publish an interaction decision record, service-ownership map, and minimal Analysis RPC surface without splitting the platform prematurely**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Load the current HTTP operation ledger, event catalogue, and Course 6 ownership records. Do not edit the RPC contract yet.

## Hypothesis

The clean implementation should satisfy this claim: **Every approved RPC has one authority, one caller need for synchronous communication, a deadline owner, a retry position, and a named operational owner. No approved service is merely a table wrapper.** When the lab introduces this fault—**Reject at least three RPC candidates and record the concrete coupling or failure they would introduce**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Classify twelve proposed interactions as local call, HTTP, durable event, unary RPC, server stream, client stream, or bidirectional stream.
2. For every proposed RPC, fill in contract, state, deadline, retry, and operational ownership.
3. Reject at least three RPC candidates and record the concrete coupling or failure they would introduce.
4. Approve the minimal AnalysisControlService, DatasetTransferService, and WorkerPlaneService capability boundaries.
5. Run `make boundary-proof` to compare the decision record with the contract skeleton.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Reject at least three RPC candidates and record the concrete coupling or failure they would introduce**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Publish an interaction decision record, service-ownership map, and minimal Analysis RPC surface without splitting the platform prematurely**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

Every approved RPC has one authority, one caller need for synchronous communication, a deadline owner, a retry position, and a named operational owner. No approved service is merely a table wrapper.

## Required evidence

- `capstone/rpc-case/interaction-decisions.yaml`
- `capstone/rpc-case/service-ownership.yaml`
- `reports/module-01-boundary-proof.json`

## Interpretation and defense

1. Which state or effect is authoritative for **RPC Boundaries, Service Ownership, and Interaction Choice**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Reject at least three RPC candidates and record the concrete coupling or failure they would introduce** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Restore the contract skeleton if experimentation added unapproved services or methods.

## Completion gate

The boundary proof passes and you can defend one rejection as clearly as one approval.

A successful command without this evidence does not complete the lab.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **RPC Boundaries, Service Ownership, and Interaction Choice**. A green command without the negative case and causal explanation does not satisfy this gate.
