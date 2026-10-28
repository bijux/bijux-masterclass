# Checkpoint — Module 04: Lifecycle, Health, Shutdown, and Recovery

## Required result

API, worker, and dispatcher processes expose explicit startup, accepting, draining, stopping, and recovery behavior.

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

## Defend the design

1. Answer the central question: **How does a process start, accept work, drain, stop, and recover without lying to orchestrators or losing durable work?**
2. Demonstrate this capstone result: API, worker, and dispatcher processes expose explicit startup, accepting, draining, stopping, and recovery behavior.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: liveness reports process existence, readiness reports safe admission, and draining stops new work before owned work is released.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—API, worker, and dispatcher processes expose explicit startup, accepting, draining, stopping, and recovery behavior.—all focused checks pass, the **Lifecycle, Health, Shutdown, and Recovery** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
