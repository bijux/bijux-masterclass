# Publish Contract

<!-- page-maps:start -->
## Guide Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive DVC"]
  guide["Capstone docs"]
  section["PUBLISH_CONTRACT"]
  page["Publish Contract"]
  proof["Proof route"]

  family --> program --> guide --> section --> page
  page -.checks against.-> proof
```

```mermaid
flowchart LR
  question["What may a downstream reviewer trust"] --> inventory["Read the promoted inventory"]
  inventory --> meaning["Read the promoted control, model, metric, and record surfaces"]
  meaning --> limit["Decide what this contract covers and what it does not"]
```
<!-- page-maps:end -->

`publish/v1/` is the stable downstream interface for this DVC capstone. It is smaller
than the full repository on purpose. A downstream reviewer should not need the entire
internal training story to understand what was promoted.

## Published files

| File | Meaning | Why it belongs in the promoted contract |
| --- | --- | --- |
| `data-profile.json` | row counts and population profile from the split step | it explains what population the evaluation summarizes |
| `metrics.json` | promoted accuracy, precision, recall, f1, threshold, and eval row count | it is the first quantitative review surface |
| `model.json` | trained model coefficients and metadata | it preserves the promoted scoring behavior |
| `params.yaml` | promoted split, training, and decision parameters | it keeps the semantic control surface explicit |
| `predictions.csv` | promoted eval predictions with identifiers and outcomes | it supports spot checks on real rows |
| `report.md` | human-readable summary of the promoted state | it gives a concise review surface without forcing raw file inspection |
| `manifest.json` | promoted inventory with hashes and training summary | it binds the release boundary into one auditable record |

## What this contract is not

`publish/v1/` is not:

- the entire internal repository history
- a substitute for `dvc.lock`
- a full experiment log
- proof that the local cache is durable

Those questions still belong to the wider repository and its recorded execution state.

## Good review order

1. `manifest.json`
2. `data-profile.json`
3. `params.yaml`
4. `model.json`
5. `metrics.json`
6. `report.md`
7. `predictions.csv`

That route moves from contract inventory into control surface, then into evaluation, then
into record-level evidence.

## Companion routes

- use `make manifest-summary` when you want the promoted inventory rendered into one compact surface
- use `make release-review` when you need the surrounding summaries and saved review bundle
- use `STATE_LAYER_GUIDE.md` when the next question is why `publish/v1/` is authoritative for downstream trust but not for the entire repository story
