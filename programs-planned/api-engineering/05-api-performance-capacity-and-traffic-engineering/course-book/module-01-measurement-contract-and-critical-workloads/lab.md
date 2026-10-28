# Module 01 lab — Freeze the performance case and reject a false baseline

## Objective

Build the six-workload catalogue, run three baseline envelopes, and prove that the comparison layer rejects workload drift and correctness failure.

## Setup conditions

- `make predecessor-proof` passes
- the packaged performance-profile schema is available
- no prior baseline is treated as authoritative
- the primary track is selected

## Failure action and investigation


1. Run the local benchmark for `WL-PROJECT-READ` three times.
2. Validate each envelope and compare its workload/environment identities.
3. Create candidate A by changing payload size without changing the workload ID.
4. Create candidate B by bypassing the correctness oracle.
5. Create candidate C with no semantic changes.
6. Run `python capstone/scripts/compare_runs.py` or the TypeScript equivalent.
7. Document why A and B are rejected before any latency claim.



### Investigation notes

Before editing, write a one-sentence hypothesis answering: **What exactly is being measured, under which workload and environment identity, and which correctness oracle still applies?** Record the first observation that contradicts the expected model. After the repair, explain why the capstone can now claim: Freeze six critical workloads, measurement envelopes, outcome populations, evidence classes, and comparable baselines. A passing command without this causal explanation is insufficient.

## Operational oracle

- three baseline envelopes have the same identity-bearing fields
- offered, started, completed, and failed counts reconcile
- candidate A is rejected for workload-hash mismatch
- candidate B is rejected for correctness failure
- candidate C is comparable
- the report states Class B local-process evidence

## Required evidence

Create:

```text
work/module-01/
├── performance-case.yaml
├── baseline-1.json
├── baseline-2.json
├── baseline-3.json
├── candidate-a.json
├── candidate-b.json
├── candidate-c.json
└── decision.md
```

`decision.md` must state the exact comparison order: identity, correctness, coverage, then performance. Include one limitation that requires a live dependency or representative environment.

## Cleanup and reset

Stop the local laboratory server, remove only transient PID and socket files, and retain all envelopes. Restore the packaged workload files from version control if you experimented with copies in place.

## Completion gate

- [ ] workload catalogue contains six distinct critical workloads
- [ ] all semantic workload fields are hash-bound
- [ ] baseline repetition and variability are reported
- [ ] false workload drift is detected
- [ ] fast-but-wrong candidate is rejected
- [ ] evidence class and limitations are explicit

The lab is incomplete when the candidate is merely faster. It must preserve the inherited correctness oracle and explain the observed resource change.
