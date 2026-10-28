# Checkpoint — Module 01: Measurement Contract and Critical Workloads

## Required result

Freeze six critical workloads, measurement envelopes, outcome populations, evidence classes, and comparable baselines.

## Demonstrate

- explain the governing question: What exactly is being measured, under which workload and environment identity, and which correctness oracle still applies?
- show one accepted case and one rejected or failed case;
- identify the authoritative owner and decisive oracle;
- state one evidence limitation.

## Commands

```bash
make module-proof MODULE=01 TRACK=${TRACK:-python}
```

## Evidence to retain

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

## Defend the design

Answer without reading from the chapter:

1. Why can a closed workload hide overload?
2. Which field makes your most recent two runs comparable?
3. What correctness oracle would reject the easiest benchmark shortcut?

## Continue only when

The module fails if any performance result lacks a workload hash, environment fingerprint, or correctness result.

You may not compensate for a failed correctness, identity, or reproducibility gate with a better latency number.

The module is incomplete when the result is asserted but the failure path, authoritative evidence, or cross-language invariant is missing. Retain enough evidence for another reader to reproduce the decision that freeze six critical workloads, measurement envelopes, outcome populations, evidence classes, and comparable baselines.
