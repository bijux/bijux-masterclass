# Lab — Prove unary outcome semantics under expected and ambiguous failures

**Module:** Unary RPCs, Metadata, Status, and Rich Errors

## Objective

Implement `CreateRun`, `GetRun`, and `CancelRun` with shared status vectors, safe metadata policy, and equivalent Python and TypeScript client behavior.

## Setup

Start the in-process Python and TypeScript control-plane references with the same application fixtures. Enable the Python live gRPC server for the network portion when `grpcio` is available.

## Controlled actions

1. Invoke successful CreateRun, GetRun, and CancelRun flows and capture response, metadata, and final status.
2. Exercise every declared application error and compare it with the status-policy table.
3. Inject a duplicate singleton authorization header and confirm edge rejection.
4. Inject a post-commit response failure for CreateRun, then retry with the same and changed request inputs.
5. Cancel a client context before and after application commit and inspect durable state.
6. Run the public HTTP mapping scenarios against the RPC-backed adapter.

## Correctness oracle

Expected application outcomes map to one safe, documented status and details profile. Post-commit response loss never creates a second run when the bound request identifier is reused. Transport cancellation does not falsely imply rollback, and public HTTP behavior remains conformant.

## Required evidence

- `capstone/shared/vectors/status.json`
- `reports/module-04-unary-proof.json`
- `capstone/rpc-case/status-policy.yaml`

## Cleanup

Stop live servers, clear in-memory fixture state, remove ephemeral ports and logs, and rerun the in-process conformance proof.

## Completion gate

Every expected application outcome must have one safe status mapping, and ambiguous committed outcomes must be reconcilable without duplicate effects.

A successful command without this evidence does not complete the lab.
