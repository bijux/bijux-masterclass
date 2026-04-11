# Release Review Guide

<!-- page-maps:start -->
## Guide Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive DVC"]
  guide["Capstone docs"]
  section["Docs"]
  page["Release Review Guide"]
  proof["Proof route"]

  family --> program --> guide --> section --> page
  page -.checks against.-> proof
```

```mermaid
flowchart LR
  orient["Read the guide boundary"] --> inspect["Inspect the named files, targets, or artifacts"]
  inspect --> run["Run the confirm, demo, selftest, or proof command"]
  run --> compare["Compare output with the stated contract"]
  compare --> review["Return to the course claim with evidence"]
```
<!-- page-maps:end -->

Use this guide when the question is no longer "did the pipeline run?" and is now
"what exactly can a downstream reviewer trust?"

## Release review order

1. `manifest.json` for inventory and integrity
2. `data-profile.json` for the promoted population story
3. `params.yaml` for the promoted control surface
4. `model.json` for the promoted scoring behavior
5. `metrics.json` for the promoted quantitative story
6. `report.md` for the human-readable summary
7. `predictions.csv` for deeper inspection

## What this route proves

- the promoted boundary is explicit and auditable
- the downstream control surface is small and reviewable
- the release bundle can be defended without forcing a reviewer through the entire repository

Use `threshold-review.json`, `predictions.csv`, and `report.md` together when the release
question depends on concrete false negatives, false positives, or borderline promoted rows.

## What this route does not prove

- that every internal experiment has been reviewed
- that the local cache is durable
- that the publish bundle replaces `dvc.lock` for internal provenance questions

Read [EXPERIMENT_GUIDE.md](experiment-guide.md) when a release question is really a
comparability question about params, thresholding, or metric movement.
