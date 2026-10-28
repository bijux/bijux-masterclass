# Checkpoint — Module 04: Unary RPCs, Metadata, Status, and Rich Errors

## Required result

Implement `CreateRun`, `GetRun`, and `CancelRun` with shared status vectors, safe metadata policy, and equivalent Python and TypeScript client behavior.

## Demonstrate

- [ ] Implement thin unary server adapters around application use cases.
- [ ] Separate transport metadata from business request fields.
- [ ] Map application outcomes to stable grpc status codes.
- [ ] Design safe structured error details without leaking internal state.
- [ ] Compose interceptors for authentication, authorization, tracing, and policy without hiding business logic.
- [ ] Translate internal grpc outcomes back to the existing public http problem details contract.

## Commands

```bash
make core-proof
```

## Evidence to retain

- [ ] `capstone/shared/vectors/status.json` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-04-unary-proof.json` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/rpc-case/status-policy.yaml` exists, is reproducible, and you can explain its oracle.

## Defend the design

1. Answer the central question in one paragraph: How should a unary RPC expose success and failure so that generated clients receive stable application meaning rather than transport accidents or leaked internals?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Unary RPCs, Metadata, Status, and Rich Errors** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
