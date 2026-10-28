# Checkpoint — Module 10: HTTP, Events, and gRPC in One Architecture: Release and Final Defense

## Required result

Release Analysis RPC API 1.0 behind the unchanged public HTTP API and Event API, execute the final defense, and publish a sanitized service-boundary dossier rather than prematurely splitting the system.

## Demonstrate

- [ ] Assign distinct public, asynchronous, local, and rpc responsibilities in one architecture.
- [ ] Migrate an internal call path with shadow, compare, bounded cutover, and rollback.
- [ ] Preserve database authority, transactional event publication, and public http conformance.
- [ ] Design an rpc release gate spanning schema, generated code, runtime, security, reliability, and performance.
- [ ] Reject distributed-monolith boundaries even when the rpc implementation is efficient.
- [ ] Produce a service-boundary dossier for course 8 based on measured ownership and failure evidence.

## Commands

```bash
make core-proof
```

## Evidence to retain

- [ ] `capstone/final-defense/trace.json` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/releases/rpc-1.0/release-report.json` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/handoff/service-boundary-dossier.yaml` exists, is reproducible, and you can explain its oracle.

## Defend the design

1. Answer the central question in one paragraph: How do we introduce an internal RPC control plane without breaking the public HTTP contract, durable event history, database authority, security profile, or rollback path?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **HTTP, Events, and gRPC in One Architecture: Release and Final Defense** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
