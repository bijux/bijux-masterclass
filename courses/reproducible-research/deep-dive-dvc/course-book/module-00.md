# Module 00 — Orientation

Deep Dive DVC is the part of the reproducible-research sequence that answers a stubborn question:

> When we claim a result is reproducible, what exact state are we claiming to recover?

Make and Snakemake teach how systems change. DVC teaches how the system names, stores, compares, promotes, and restores the states that those systems operate on.

## Where this course fits

The reproducible-research family is developing along a long-lived program map:

1. **How systems change**: Make
2. **How state transitions scale**: Snakemake, Nextflow
3. **What states are**: DVC
4. **Where states execute**: Containers
5. **How states survive time and authority**: CI, retention, recovery
6. **How systems explain themselves**: observability and tracing

This course owns the third layer. Its concern is not just data versioning in the narrow sense, but the full mechanical contract around:

- dataset identity
- stage inputs and outputs
- parameter scope
- metric meaning
- experiment lineage
- remote durability
- recovery under failure

## What this course is not

This is not a generic DVC command reference and not an ML tutorial. It is a correctness-first course about using DVC to make state explicit enough that teams can reason about it, verify it, and recover it.

## What the capstone will become

`capstone/` is reserved for a reference repository that will make the course executable. The target shape is a small but realistic DVC-driven project with:

- tracked datasets and remotes
- a truthful `dvc.yaml` pipeline
- declared params and metrics
- experiment workflows
- CI-backed recovery checks

Until that reference project lands, the course-book is the authoritative material.

## Reading path

Read the modules in order:

1. Why reproducibility fails
2. Data identity and content addressing
3. Execution environments as inputs
4. Pipelines as truthful DAGs
5. Metrics, parameters, and meaning
6. Experiments without chaos
7. Collaboration, CI, and social contracts
8. Production, scale, and incident survival

The sequence is deliberate: each module adds one invariant that the next module depends on.
