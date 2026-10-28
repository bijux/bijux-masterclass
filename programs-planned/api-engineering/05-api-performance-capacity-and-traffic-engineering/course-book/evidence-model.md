# Evidence Model — API Performance, Capacity, and Traffic Engineering

## Course-specific proof ladder

| Level | Evidence | Minimum record |
|---:|---|---|
| 1 | workload and environment identity | A named claim, version, environment, oracle, and retained artifact |
| 2 | complete outcome envelopes | A named claim, version, environment, oracle, and retained artifact |
| 3 | query plans and runtime profiles | A named claim, version, environment, oracle, and retained artifact |
| 4 | capacity and release comparisons | A named claim, version, environment, oracle, and retained artifact |

## Authority versus diagnosis

For performance claims, comparable workload envelopes and correctness oracles govern the decision; a faster result from a changed workload or missing outcomes is invalid evidence.

## Negative evidence

Every Course 5 lab contains a defect specific to sustain the promise under pressure. Predict the first failing oracle, retain the raw counterexample, and keep it after repair; a proof that accepts that defect cannot support the checkpoint claim.

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

When representative load against a provisioned database and measured resource limits is unavailable, run the deterministic evidence that still applies and record the stronger route as `not-executed`. The wording of the claim must shrink with the environment.
