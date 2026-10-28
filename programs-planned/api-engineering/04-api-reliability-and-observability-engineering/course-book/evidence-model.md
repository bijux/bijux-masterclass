# Evidence Model — API Reliability and Observability Engineering

## Course-specific proof ladder

| Level | Evidence | Minimum record |
|---:|---|---|
| 1 | critical-journey outcome records | A named claim, version, environment, oracle, and retained artifact |
| 2 | deadline and lifecycle traces | A named claim, version, environment, oracle, and retained artifact |
| 3 | metrics, logs, traces, alerts, and runbooks | A named claim, version, environment, oracle, and retained artifact |
| 4 | fault injection and durable reconciliation | A named claim, version, environment, oracle, and retained artifact |

## Authority versus diagnosis

For reliability claims, the critical-journey population and durable outcome decide whether the promise held; telemetry explains causality but does not manufacture success.

## Negative evidence

Every Course 4 lab contains a defect specific to observe, diagnose, contain, and recover the promise. Predict the first failing oracle, retain the raw counterexample, and keep it after repair; a proof that accepts that defect cannot support the checkpoint claim.

## Evidence package

Each checkpoint should retain:

```text
claim and owner
input, workload, or candidate identity
software and contract versions
environment identity
command or procedure
raw result
interpreted decision
known exclusions
cleanup state
```

## Unavailable infrastructure

When a multiprocess topology with telemetry export, injected dependency failure, and recovery is unavailable, run the deterministic evidence that still applies and record the stronger route as `not-executed`. The wording of the claim must shrink with the environment.
