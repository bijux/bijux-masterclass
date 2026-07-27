# Experiment Comparability Specimen

This specimen asks one bounded question:

> Does lowering the escalation threshold improve recall enough to justify its precision
> cost on the same review population?

The baseline is deliberately small. Eight incident records carry fixed scores and
review outcomes. `params.yaml` owns the decision threshold and the names of the population
and metric contracts. `scripts/evaluate_candidate.py` turns those inputs into a reviewable
metric record.

The specimen separates four kinds of evidence:

| Surface | File | Question |
| --- | --- | --- |
| baseline identity | `experiment-contract.json` | What state is approved as the comparison anchor? |
| declared controls | `params.yaml` | Which control may the candidate change? |
| evaluation population | `data/evaluation.csv` | Are baseline and candidate measured on the same records? |
| metric result | `metrics/metrics.json` | What moved, and under which contracts? |

The baseline threshold is `0.65`. A controlled candidate lowers only
`decision.threshold` to `0.50`. The audit surrounding this specimen also constructs
contaminated candidates so learners can see why a successful run is weaker than a valid
comparison.

Run the specimen directly:

```bash
dvc repro
cat metrics/metrics.json
```

Use the course audit for the complete set of controlled and rejected cases:

```bash
make experiment-comparability-audit
```
