# Release Review Guide

<!-- page-maps:start -->
## Guide Maps

```mermaid
graph TD
  publish["publish/v1/"]
  manifest["manifest.json"]
  params["params.yaml"]
  metrics["metrics.json"]
  report["report.md"]
  decision["downstream trust decision"]

  publish --> manifest
  publish --> params
  publish --> metrics
  publish --> report
  manifest --> decision
  params --> decision
  metrics --> decision
  report --> decision
```

```mermaid
flowchart LR
  candidate["Candidate release bundle"] --> inventory["Check inventory and hashes"]
  inventory --> meaning["Check control surface and metrics meaning"]
  meaning --> review["Read the human review report"]
  review --> decide["Approve, reject, or ask for more evidence"]
```
<!-- page-maps:end -->

Use this guide when the question is no longer "did the pipeline run?" and is now
"what exactly can a downstream reviewer trust?"

## Release review order

1. `manifest.json` for inventory and integrity
2. `params.yaml` for the promoted control surface
3. `metrics.json` for the promoted quantitative story
4. `report.md` for the human-readable summary
5. `predictions.csv` and `data-profile.json` for deeper inspection

## What this route proves

- the promoted boundary is explicit and auditable
- the downstream control surface is small and reviewable
- the release bundle can be defended without forcing a reviewer through the entire repository

## What this route does not prove

- that every internal experiment has been reviewed
- that the local cache is durable
- that the publish bundle replaces `dvc.lock` for internal provenance questions
