# Metric Contract Specimen

This isolated DVC project separates two questions that are often collapsed:

1. Did a metric value change?
2. Are the old and new values measurements of the same claim?

The `evaluate_metric_contract` stage renders a metric document from a selected case and a
declared decision threshold. Every case uses deterministic confusion-matrix counts. The
cases differ only in the evidence needed to decide whether a comparison is valid.

## Evidence surfaces

- `cases/baseline.json` is the governed reference measurement.
- `cases/comparable-candidate.json` changes predictions on the same population and under
  the same metric contract.
- `cases/additive-metric.json` preserves the primary contract and adds a new metric.
- `cases/population-drift.json` keeps the row count stable but changes population identity.
- `cases/unit-drift.json` keeps the familiar metric name but changes fractions to percent.
- `cases/schema-version-drift.json` announces an incompatible contract version.
- `cases/missing-population-identity.json` removes evidence needed for review.
- `params.yaml` declares the decision threshold that gives fixed-threshold metrics meaning.
- `metrics/metrics.json` is generated evidence, not an authored answer.

The audit also creates a control-drift case by changing `decision.threshold` while keeping
the selected candidate otherwise comparable.

## Direct use

From this directory:

```bash
dvc init --no-scm
dvc repro
dvc metrics show
```

The course audit runs each comparison in its own generated Git and DVC workspace so it can
capture a real `dvc metrics diff` against the baseline revision without modifying this
source specimen.
