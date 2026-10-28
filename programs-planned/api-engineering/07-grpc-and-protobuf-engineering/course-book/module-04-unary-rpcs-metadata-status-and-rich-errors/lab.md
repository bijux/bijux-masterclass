# Lab — Prove unary outcome semantics under expected and ambiguous failures

> **Module 04:** Unary RPCs, Metadata, Status, and Rich Errors

## Objective

Implement `CreateRun`, `GetRun`, and `CancelRun` with shared status vectors, safe metadata policy, and equivalent Python and TypeScript client behavior.

## Why this lab matters

This lab turns the module’s governing question—**How should a unary RPC expose success and failure so that generated clients receive stable application meaning rather than transport accidents or leaked internals?**—into a falsifiable experiment. Now inject response loss after the cancellation transaction commits. The client receives UNAVAILABLE, not success. Transport status cannot prove that cancellation failed. A retry with the same request identity can replay the stored outcome, or the client can call GetRun and reconcile.

It advances the cumulative Analysis Runs Platform by requiring this result: **Implement `CreateRun`, `GetRun`, and `CancelRun` with shared status vectors, safe metadata policy, and equivalent Python and TypeScript client behavior**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Start the in-process Python and TypeScript control-plane references with the same application fixtures. Enable the Python live gRPC server for the network portion when `grpcio` is available.

## Hypothesis

The clean implementation should satisfy this claim: **Expected application outcomes map to one safe, documented status and details profile. Post-commit response loss never creates a second run when the bound request identifier is reused. Transport cancellation does not falsely imply rollback, and public HTTP behavior remains conformant.** When the lab introduces this fault—**Inject a duplicate singleton authorization header and confirm edge rejection**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Invoke successful CreateRun, GetRun, and CancelRun flows and capture response, metadata, and final status.
2. Exercise every declared application error and compare it with the status-policy table.
3. Inject a duplicate singleton authorization header and confirm edge rejection.
4. Inject a post-commit response failure for CreateRun, then retry with the same and changed request inputs.
5. Cancel a client context before and after application commit and inspect durable state.
6. Run the public HTTP mapping scenarios against the RPC-backed adapter.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Inject a duplicate singleton authorization header and confirm edge rejection**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Implement CreateRun, GetRun, and CancelRun with shared status vectors, safe metadata policy, and equivalent Python and TypeScript client behavior**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

Expected application outcomes map to one safe, documented status and details profile. Post-commit response loss never creates a second run when the bound request identifier is reused. Transport cancellation does not falsely imply rollback, and public HTTP behavior remains conformant.

## Required evidence

- `capstone/shared/vectors/status.json`
- `reports/module-04-unary-proof.json`
- `capstone/rpc-case/status-policy.yaml`

## Interpretation and defense

1. Which state or effect is authoritative for **Unary RPCs, Metadata, Status, and Rich Errors**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Inject a duplicate singleton authorization header and confirm edge rejection** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Stop live servers, clear in-memory fixture state, remove ephemeral ports and logs, and rerun the in-process conformance proof.

## Completion gate

Every expected application outcome must have one safe status mapping, and ambiguous committed outcomes must be reconcilable without duplicate effects.

A successful command without this evidence does not complete the lab.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Unary RPCs, Metadata, Status, and Rich Errors**. A green command without the negative case and causal explanation does not satisfy this gate.
