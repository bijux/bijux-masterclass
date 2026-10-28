# Lab — Module 01 lab — Freeze the performance case and reject a false baseline

> **Module 01:** Measurement Contract and Critical Workloads

## Objective

Build the six-workload catalogue, run three baseline envelopes, and prove that the comparison layer rejects workload drift and correctness failure.

## Why this lab matters

This lab turns the module’s governing question—**What exactly is being measured, under which workload and environment identity, and which correctness oracle still applies?**—into a falsifiable experiment. A baseline is not the first number produced. It is an accepted, reproducible envelope whose workload and environment are suitable for the intended comparison. Store raw samples when practical, summary algorithm names, warmup and measurement windows, start time, source revision, and all outcome counts.

It advances the cumulative Analysis Runs Platform by requiring this result: **Freeze six critical workloads, measurement envelopes, outcome populations, evidence classes, and comparable baselines**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

- `make predecessor-proof` passes
- the packaged performance-profile schema is available
- no prior baseline is treated as authoritative
- the primary track is selected

## Hypothesis

The clean implementation should satisfy this claim: **three baseline envelopes have the same identity-bearing fields; offered, started, completed, and failed counts reconcile; candidate A is rejected for workload-hash mismatch; candidate B is rejected for correctness failure; candidate C is comparable; the report states Class B local-process evidence.** When the lab introduces this fault—**Build the six-workload catalogue, run three baseline envelopes, and prove that the comparison layer rejects workload drift and correctness failure**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Run the local benchmark for `WL-PROJECT-READ` three times.
2. Validate each envelope and compare its workload/environment identities.
3. Create candidate A by changing payload size without changing the workload ID.
4. Create candidate B by bypassing the correctness oracle.
5. Create candidate C with no semantic changes.
6. Run `python capstone/scripts/compare_runs.py` or the TypeScript equivalent.
7. Document why A and B are rejected before any latency claim.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Build the six-workload catalogue, run three baseline envelopes, and prove that the comparison layer rejects workload drift and correctness failure**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Build the six-workload catalogue, run three baseline envelopes, and prove that the comparison layer rejects workload drift and correctness failure**, and identify one attractive implementation that would pass the happy path while failing the oracle.

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

## Interpretation and defense

1. Which state or effect is authoritative for **Measurement Contract and Critical Workloads**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Build the six-workload catalogue, run three baseline envelopes, and prove that the comparison layer rejects workload drift and correctness failure** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

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

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Measurement Contract and Critical Workloads**. A green command without the negative case and causal explanation does not satisfy this gate.
