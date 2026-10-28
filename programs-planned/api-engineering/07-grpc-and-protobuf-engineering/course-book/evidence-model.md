# Evidence Model — gRPC and Protobuf Engineering

## Course-specific proof ladder

| Level | Evidence | Minimum record |
|---:|---|---|
| 1 | descriptor and golden-wire evidence | A named claim, version, environment, oracle, and retained artifact |
| 2 | live unary and streaming observations | A named claim, version, environment, oracle, and retained artifact |
| 3 | deadline, cancellation, and flow-control schedules | A named claim, version, environment, oracle, and retained artifact |
| 4 | method policy and compatibility candidates | A named claim, version, environment, oracle, and retained artifact |

## Authority versus diagnosis

For RPC claims, the published descriptors and observed status, metadata, messages, deadlines, and stream termination decide conformance; generated stubs cannot prove network behavior.

## Negative evidence

Every Course 7 lab contains a defect specific to engineer typed internal invocation and streaming. Predict the first failing oracle, retain the raw counterexample, and keep it after repair; a proof that accepts that defect cannot support the checkpoint claim.

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

When generated descriptors, a networked gRPC stack, TLS identity, and streaming peers is unavailable, run the deterministic evidence that still applies and record the stronger route as `not-executed`. The wording of the claim must shrink with the environment.
