# Evidence Model — OpenAPI Contract Engineering

## Course-specific proof ladder

| Level | Evidence | Minimum record |
|---:|---|---|
| 1 | description parsing and reference resolution | A named claim, version, environment, oracle, and retained artifact |
| 2 | schema fixture validation | A named claim, version, environment, oracle, and retained artifact |
| 3 | provider-neutral HTTP observations | A named claim, version, environment, oracle, and retained artifact |
| 4 | consumer execution and compatibility diff | A named claim, version, environment, oracle, and retained artifact |

## Authority versus diagnosis

For contract claims, the description and independent validators define the allowed surface; provider observations and consumer tests decide whether runtime behavior actually conforms.

## Negative evidence

Every Course 1 lab contains a defect specific to specify the public promise. Predict the first failing oracle, retain the raw counterexample, and keep it after repair; a proof that accepts that defect cannot support the checkpoint claim.

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

When a real provider conformance run and an independent OpenAPI validator is unavailable, run the deterministic evidence that still applies and record the stronger route as `not-executed`. The wording of the claim must shrink with the environment.
