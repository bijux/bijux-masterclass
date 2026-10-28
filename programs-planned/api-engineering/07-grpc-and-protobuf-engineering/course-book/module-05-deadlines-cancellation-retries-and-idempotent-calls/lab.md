# Lab — Bound time and retry safely across ambiguous fault points

**Module:** Deadlines, Cancellation, Retries, and Idempotent Calls

## Objective

Implement deadline-aware CreateRun and GetRun clients, persistent retry semantics, deterministic retry vectors, and fault-injection evidence for failures before invocation, before commit, after commit, and during response delivery.

## Setup

Use deterministic clocks for policy proof and the Python live server for transport evidence. Seed one request identifier and enable fault injection at named phases.

## Controlled actions

1. Run a successful CreateRun under one edge deadline and record remaining budget at each phase.
2. Inject failures before handler entry, before commit, after commit, and during response delivery.
3. Retry safe query and mutation cases with bounded backoff and deterministic jitter.
4. Reuse the request identifier with changed semantic input and confirm conflict.
5. Cancel calls before and after commit and compare caller observation with durable state.
6. Exercise wait-for-ready with a delayed server under both sufficient and exhausted deadlines.

## Correctness oracle

No attempt starts after the absolute deadline, no safe retry exceeds the budget, mutation retries converge on one durable effect, changed input is rejected, and cancellation/status observations never substitute for the durable oracle.

## Required evidence

- `capstone/shared/vectors/deadlines.json`
- `capstone/shared/vectors/retries.json`
- `reports/module-05-deadline-proof.json`

## Cleanup

Disable fault injection, clear idempotency fixtures, stop delayed servers, and reset deterministic clocks.

## Completion gate

Every retryable mutation must be durably idempotent, every call must be bounded by one absolute deadline, and every ambiguous outcome must have an authoritative reconciliation path.

A successful command without this evidence does not complete the lab.
