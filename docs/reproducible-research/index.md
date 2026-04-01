# Reproducible Research

This family contains programs about build graphs, workflow execution, state
identity, publishing, verification, and operational reproducibility.

## Program Map

The long-lived map for this family is:

1. **How systems change**: Make
2. **How state transitions scale**: Snakemake, Nextflow
3. **What states are**: DVC
4. **Where states execute**: containers and execution envelopes
5. **How states survive time and authority**: CI, retention, recovery
6. **How systems explain themselves**: observability and tracing

Current repository coverage:

- `deep-dive-make` covers local build-graph truthfulness.
- `deep-dive-snakemake` covers workflow-scale orchestration.
- `deep-dive-dvc` covers state identity, experiment lineage, and recovery.

## Included Programs

### Deep Dive Make

- Location: `programs/reproducible-research/deep-dive-make`
- Focus: GNU Make as a truthful, parallel-safe build graph engine
- Local entrypoints:
  - `make PROGRAM=reproducible-research/deep-dive-make program-help`
  - `make PROGRAM=reproducible-research/deep-dive-make test`

### Deep Dive Snakemake

- Location: `programs/reproducible-research/deep-dive-snakemake`
- Focus: Snakemake as a reproducible workflow engine with explicit contracts
- Local entrypoints:
  - `make PROGRAM=reproducible-research/deep-dive-snakemake program-help`

### Deep Dive DVC

- Location: `programs/reproducible-research/deep-dive-dvc`
- Focus: DVC as the contract layer for data identity, experiment lineage, and recoverability
- Local entrypoints:
  - `make PROGRAM=reproducible-research/deep-dive-dvc program-help`
  - `make PROGRAM=reproducible-research/deep-dive-dvc docs-build`
