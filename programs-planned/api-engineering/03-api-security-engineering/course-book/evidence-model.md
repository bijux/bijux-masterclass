# Evidence Model — API Security Engineering

## Course-specific proof ladder

| Level | Evidence | Minimum record |
|---:|---|---|
| 1 | threat-to-requirement traceability | A named claim, version, environment, oracle, and retained artifact |
| 2 | negative identity and authorization decisions | A named claim, version, environment, oracle, and retained artifact |
| 3 | hostile-input and SSRF vectors | A named claim, version, environment, oracle, and retained artifact |
| 4 | incident and secret-rotation evidence | A named claim, version, environment, oracle, and retained artifact |

## Authority versus diagnosis

For security claims, the policy decision plus protected-resource state decides authorization; logs and scanner findings are diagnostic and never grant access.

## Negative evidence

Every Course 3 lab contains a defect specific to defend the promise. Predict the first failing oracle, retain the raw counterexample, and keep it after repair; a proof that accepts that defect cannot support the checkpoint claim.

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

When an operated issuer, live network boundaries, and a real policy-enforcement path is unavailable, run the deterministic evidence that still applies and record the stronger route as `not-executed`. The wording of the claim must shrink with the environment.
