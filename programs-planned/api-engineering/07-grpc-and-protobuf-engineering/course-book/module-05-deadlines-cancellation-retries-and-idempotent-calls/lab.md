# Lab — Bound time and retry safely across ambiguous fault points

> **Module 05:** Deadlines, Cancellation, Retries, and Idempotent Calls

## Objective

Implement deadline-aware CreateRun and GetRun clients, persistent retry semantics, deterministic retry vectors, and fault-injection evidence for failures before invocation, before commit, after commit, and during response delivery.

## Why this lab matters

This lab turns the module’s governing question—**How can callers bound remote work and recover from transient failure without multiplying timeouts or duplicating durable effects?**—into a falsifiable experiment. The course declares retry behavior by fully qualified method. Read-only GetRun can retry selected transient failures within the deadline. CreateRun can retry only with a persistent request identifier bound to the semantic input. CancelRun likewise requires idempotency and version semantics. Streaming methods have different reconnection and resume rules; unary retry configuration does not apply automatically.

It advances the cumulative Analysis Runs Platform by requiring this result: **Implement deadline-aware CreateRun and GetRun clients, persistent retry semantics, deterministic retry vectors, and fault-injection evidence for failures before invocation, before commit, after commit, and during response delivery**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Use deterministic clocks for policy proof and the Python live server for transport evidence. Seed one request identifier and enable fault injection at named phases.

## Hypothesis

The clean implementation should satisfy this claim: **No attempt starts after the absolute deadline, no safe retry exceeds the budget, mutation retries converge on one durable effect, changed input is rejected, and cancellation/status observations never substitute for the durable oracle.** When the lab introduces this fault—**Inject failures before handler entry, before commit, after commit, and during response delivery**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Run a successful CreateRun under one edge deadline and record remaining budget at each phase.
2. Inject failures before handler entry, before commit, after commit, and during response delivery.
3. Retry safe query and mutation cases with bounded backoff and deterministic jitter.
4. Reuse the request identifier with changed semantic input and confirm conflict.
5. Cancel calls before and after commit and compare caller observation with durable state.
6. Exercise wait-for-ready with a delayed server under both sufficient and exhausted deadlines.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Inject failures before handler entry, before commit, after commit, and during response delivery**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Implement deadline-aware CreateRun and GetRun clients, persistent retry semantics, deterministic retry vectors, and fault-injection evidence for failures before invocation, before commit, after commit, and during response delivery**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

No attempt starts after the absolute deadline, no safe retry exceeds the budget, mutation retries converge on one durable effect, changed input is rejected, and cancellation/status observations never substitute for the durable oracle.

## Required evidence

- `capstone/shared/vectors/deadlines.json`
- `capstone/shared/vectors/retries.json`
- `reports/module-05-deadline-proof.json`

## Interpretation and defense

1. Which state or effect is authoritative for **Deadlines, Cancellation, Retries, and Idempotent Calls**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Inject failures before handler entry, before commit, after commit, and during response delivery** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Disable fault injection, clear idempotency fixtures, stop delayed servers, and reset deterministic clocks.

## Completion gate

Every retryable mutation must be durably idempotent, every call must be bounded by one absolute deadline, and every ambiguous outcome must have an authoritative reconciliation path.

A successful command without this evidence does not complete the lab.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Deadlines, Cancellation, Retries, and Idempotent Calls**. A green command without the negative case and causal explanation does not satisfy this gate.
