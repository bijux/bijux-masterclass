# Evidence Model — Contract-Driven API Service Engineering

## Course-specific proof ladder

| Level | Evidence | Minimum record |
|---:|---|---|
| 1 | pure domain transitions | A named claim, version, environment, oracle, and retained artifact |
| 2 | live database constraints and transactions | A named claim, version, environment, oracle, and retained artifact |
| 3 | process restart and lease recovery | A named claim, version, environment, oracle, and retained artifact |
| 4 | artifact bytes and webhook delivery records | A named claim, version, environment, oracle, and retained artifact |

## Authority versus diagnosis

For service claims, durable database state and transaction outcomes are authoritative; HTTP responses and traces explain exposure and execution but cannot rewrite committed truth.

## Negative evidence

Every Course 2 lab contains a defect specific to implement the promise durably. Predict the first failing oracle, retain the raw counterexample, and keep it after repair; a proof that accepts that defect cannot support the checkpoint claim.

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

When concurrent PostgreSQL transactions, process termination, and migration coexistence is unavailable, run the deterministic evidence that still applies and record the stronger route as `not-executed`. The wording of the claim must shrink with the environment.
