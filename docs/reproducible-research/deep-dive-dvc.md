# Deep Dive DVC

Deep Dive DVC teaches reproducibility through state identity, declared experiments,
promotion boundaries, and recovery discipline. It is the route to choose when filenames
and notebooks are no longer enough to explain what result is authoritative.

## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive DVC"]
  course["Course home"]
  capstone["Capstone guide"]

  family --> program --> course
  course --> capstone
```

```mermaid
flowchart LR
  overview["Read this overview"] --> start["Open Start Here or Course Home"]
  start --> module["Study the state model, pipeline, or recovery pages"]
  module --> capstone["Inspect the incident-escalation capstone"]
  capstone --> compare["Return here when comparing with Make or Snakemake"]
```

## What This Program Covers

- content-addressed data identity and state boundaries
- truthful `dvc.yaml` pipelines with declared parameters and metrics
- experiments, promotion, retention, and auditability
- recovery drills that prove a result can be restored after loss

## Local Catalog Route

- Course home: [Program guide](../library/reproducible-research/deep-dive-dvc/course-book/index.md)
- Learner entry: [Start Here](../library/reproducible-research/deep-dive-dvc/course-book/start-here.md)
- Capstone guide: [Capstone README](../library/reproducible-research/deep-dive-dvc/capstone/README.md)

## Local Commands

```bash
make PROGRAM=reproducible-research/deep-dive-dvc docs-serve
make PROGRAM=reproducible-research/deep-dive-dvc test
make PROGRAM=reproducible-research/deep-dive-dvc capstone-confirm
```

## Honesty Boundary

This program is for readers who need exact answers to "what state exists", "what state
is recoverable", and "what proof turns a reproducibility claim into an engineering contract".
