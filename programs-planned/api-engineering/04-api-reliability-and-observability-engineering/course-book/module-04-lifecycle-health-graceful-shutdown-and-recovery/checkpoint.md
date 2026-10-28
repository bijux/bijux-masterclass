# Checkpoint — Module 04: Lifecycle, Health, Shutdown, and Recovery

## Required result

Implement lifecycle states, liveness/readiness separation, graceful draining, lease handling, and startup reconciliation.

## Demonstrate

- Separate startup, liveness, and readiness.
- Stop accepting before draining.
- Bound graceful shutdown and preserve durable claims.
- Recover incomplete work on startup.
- Make health endpoints report service ability, not every dependency detail.

## Commands

```bash
make module-proof MODULE=04
make core-proof
```

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Lifecycle, Health, Shutdown, and Recovery** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Lifecycle, Health, Shutdown, and Recovery**
- focused result for: Separate startup, liveness, and readiness.
- public, durable, security, or operational observation showing: API, worker, and dispatcher processes expose explicit startup, accepting, draining, stopping, and recovery behavior.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **explicit lifecycle and health**
- a limitation statement naming every live dependency required to support the strongest **Lifecycle, Health, Shutdown, and Recovery** claim but not exercised

## Defend the design

1. Answer the central question: **How does a process start, accept work, drain, stop, and recover without lying to orchestrators or losing durable work?**
2. Demonstrate this capstone result: API, worker, and dispatcher processes expose explicit startup, accepting, draining, stopping, and recovery behavior.
3. Show the **Lifecycle, Health, Shutdown, and Recovery** defect, the first failing oracle, and the exact regression retained after repair.
4. Explain why this invariant is shared across languages: liveness reports process existence, readiness reports safe admission, and draining stops new work before owned work is released.
5. State which environment-backed **Lifecycle, Health, Shutdown, and Recovery** route was not run and how that limits the claim.

## Continue only when

Continue when the system again provides this module result—API, worker, and dispatcher processes expose explicit startup, accepting, draining, stopping, and recovery behavior.—all focused checks pass, the **Lifecycle, Health, Shutdown, and Recovery** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
