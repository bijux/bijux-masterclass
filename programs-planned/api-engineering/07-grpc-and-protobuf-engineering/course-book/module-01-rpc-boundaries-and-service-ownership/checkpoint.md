# Checkpoint — Module 01: RPC Boundaries, Service Ownership, and Interaction Choice

## Required result

Publish an interaction decision record, service-ownership map, and minimal Analysis RPC surface without splitting the platform prematurely.

## Demonstrate

- [ ] Distinguish local calls, public http operations, durable events, and internal rpcs by ownership, coupling, latency, and failure semantics.
- [ ] Recognize when grpc improves a boundary and when it merely makes a distributed monolith more efficient.
- [ ] Design rpc services around stable capabilities rather than database tables or existing classes.
- [ ] Separate control-plane commands from event facts and bulk data movement.
- [ ] Identify caller, callee, deadline owner, retry owner, and authoritative state for every proposed rpc.
- [ ] Reject unjustified service extraction with explicit evidence rather than architectural fashion.

## Commands

```bash
make core-proof
```

## Evidence to retain

- [ ] `capstone/rpc-case/interaction-decisions.yaml` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/rpc-case/service-ownership.yaml` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-01-boundary-proof.json` exists, is reproducible, and you can explain its oracle.

## Defend the design

1. Answer the central question in one paragraph: Which interactions deserve a typed RPC boundary, and which should remain HTTP requests, durable events, or local function calls?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **RPC Boundaries, Service Ownership, and Interaction Choice** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
