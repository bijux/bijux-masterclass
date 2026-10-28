# Checkpoint — Module 10: Performance Regression and Release Engineering

## Required result

Build correctness-first regression gates, environment comparability, accepted/rejected/inconclusive candidates, and a performance dossier.

## Demonstrate

- explain the governing question: How does a performance change become a reproducible release decision rather than a favorable chart?
- show one accepted case and one rejected or failed case;
- identify the authoritative owner and decisive oracle;
- state one evidence limitation.

## Commands

```bash
make module-proof MODULE=10 TRACK=${TRACK:-python}
```

## Evidence to retain

Create:

```text
work/module-10/
├── release-policy.yaml
├── baseline-series/
├── candidate-series/
├── accepted-decision.json
├── rejected-decision.json
├── inconclusive-decision.json
├── sensitivity.json
├── rollback.md
├── remeasurement.md
└── final-dossier.md
```

`final-dossier.md` must link each conclusion to machine-readable evidence and state the strongest evidence class reached. Include one rejected optimization from earlier modules.

## Defend the design

Answer without reading from the chapter:

1. Why is your accepted candidate actually comparable?
2. Which earlier gate rejects the fastest invalid candidate?
3. What exact condition triggers remeasurement or rollback?

## Continue only when

The course fails if a faster incorrect candidate can pass, if a baseline is overwritten without lineage, or if inconclusive evidence is reported as a performance win.

You may not compensate for a failed correctness, identity, or reproducibility gate with a better latency number.

The module is incomplete when the result is asserted but the failure path, authoritative evidence, or cross-language invariant is missing. Retain enough evidence for another reader to reproduce the decision that build correctness-first regression gates, environment comparability, accepted/rejected/inconclusive candidates, and a performance dossier.
