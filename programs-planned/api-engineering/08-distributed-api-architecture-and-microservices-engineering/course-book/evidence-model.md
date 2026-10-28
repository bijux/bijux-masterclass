# Evidence Model — Distributed API Architecture and Microservices Engineering

## Course-specific proof ladder

| Level | Evidence | Minimum record |
|---:|---|---|
| 1 | ownership and dependency fitness functions | A named claim, version, environment, oracle, and retained artifact |
| 2 | projection and saga state | A named claim, version, environment, oracle, and retained artifact |
| 3 | network partial-failure experiments | A named claim, version, environment, oracle, and retained artifact |
| 4 | shadow, canary, cutover, and rollback evidence | A named claim, version, environment, oracle, and retained artifact |

## Authority versus diagnosis

For distributed-architecture claims, authoritative ownership maps and owner-local durable state decide who may change a fact; traces and gateway responses reveal coordination but not ownership.

## Negative evidence

Every Course 8 lab contains a defect specific to distribute ownership deliberately. Predict the first failing oracle, retain the raw counterexample, and keep it after repair; a proof that accepts that defect cannot support the checkpoint claim.

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

When independent processes, owner-local databases, real routing, mixed versions, and network faults is unavailable, run the deterministic evidence that still applies and record the stronger route as `not-executed`. The wording of the claim must shrink with the environment.
