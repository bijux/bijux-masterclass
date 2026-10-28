# Evidence Model — Event-Driven API Engineering

## Course-specific proof ladder

| Level | Evidence | Minimum record |
|---:|---|---|
| 1 | canonical message bytes | A named claim, version, environment, oracle, and retained artifact |
| 2 | broker delivery attempts and acknowledgements | A named claim, version, environment, oracle, and retained artifact |
| 3 | inbox effects and replay state | A named claim, version, environment, oracle, and retained artifact |
| 4 | compatibility and dead-letter custody | A named claim, version, environment, oracle, and retained artifact |

## Authority versus diagnosis

For event claims, producer-owned facts, broker delivery evidence, and consumer inbox/effect state answer different questions; an offset alone cannot prove a business effect.

## Negative evidence

Every Course 6 lab contains a defect specific to extend the promise across asynchronous time. Predict the first failing oracle, retain the raw counterexample, and keep it after repair; a proof that accepts that defect cannot support the checkpoint claim.

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

When a live durable broker with retention, redelivery, consumer restart, and replay is unavailable, run the deterministic evidence that still applies and record the stronger route as `not-executed`. The wording of the claim must shrink with the environment.
