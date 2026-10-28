# Checkpoint — Module 02: Benchmark Design and Statistical Interpretation

## Required result

Build reproducible benchmark profiles, repeated runs, quantile and interval summaries, and accepted/rejected/inconclusive comparisons.

## Demonstrate

- explain the governing question: How do open and closed demand, warmup, sample size, missing outcomes, variation, and statistical uncertainty change benchmark meaning?
- show one accepted case and one rejected or failed case;
- identify the authoritative owner and decisive oracle;
- state one evidence limitation.

## Commands

```bash
make module-proof MODULE=02 TRACK=${TRACK:-python}
```

## Evidence to retain

Create:

```text
work/module-02/
├── thresholds.yaml
├── closed-events.jsonl
├── open-events.jsonl
├── closed-summary.json
├── open-summary.json
├── run-series.json
└── decision.md
```

Include a diagram or table showing how many arrivals were scheduled during the pause and how each model represented them. State client schedule coverage.

## Defend the design

Answer without reading from the chapter:

1. How did the closed model hide demand during the pause?
2. Why is one run with one million requests still one environment realization?
3. What would cause the load generator to become the bottleneck?

## Continue only when

The module fails if scheduled-but-not-started work disappears or if the candidate threshold was selected after inspecting results.

You may not compensate for a failed correctness, identity, or reproducibility gate with a better latency number.

The module is incomplete when the result is asserted but the failure path, authoritative evidence, or cross-language invariant is missing. Retain enough evidence for another reader to reproduce the decision that build reproducible benchmark profiles, repeated runs, quantile and interval summaries, and accepted/rejected/inconclusive comparisons.
