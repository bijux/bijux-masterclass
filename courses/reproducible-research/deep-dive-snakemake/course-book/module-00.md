# Orientation

Deep Dive Snakemake is a course about workflow truthfulness under pressure. The goal is
not to memorize more flags. The goal is to learn how to build workflows whose behavior
you can defend when the data grows, the executor changes, or the team revisits the code
months later.

## What this course is not

- It is not an introductory syntax guide to Snakemake rules and wildcards.
- It is not a collection of bioinformatics recipes detached from workflow semantics.
- It is not a catalog of executor flags without a model of what the workflow itself guarantees.

## What this course is

- A semantics-first guide to file contracts, rebuild truth, and publish boundaries
- A design guide for dynamic DAGs, checkpoints, and deterministic discovery
- An operations guide for profiles, retries, staging, CI, and long-lived workflow governance
- A capstone-backed course where the main claims are always visible in executable workflow behavior

## Readiness check

You are ready for this course if you can already do most of the following without looking up syntax:

- read a simple Snakemake rule and identify its inputs and outputs
- use `snakemake -n` and explain what the dry-run is planning
- tell the difference between workflow code and shell code embedded in a rule
- read a small YAML config and understand how a workflow consumes it
- explain why an undeclared input is a correctness bug, not just a style issue

If those are still shaky, you can continue, but you should move slowly and verify every example by running it.

## Key terms used throughout the course

- **file contract**: the explicit promise a rule makes through its declared inputs and outputs
- **dynamic DAG**: a workflow whose full job graph is discovered in stages rather than all at parse time
- **checkpoint**: a rule that allows downstream DAG construction to be re-evaluated after discovery
- **publish boundary**: the stable versioned interface that downstream consumers are allowed to trust
- **profile**: site or executor policy encoded separately from workflow semantics
- **proof artifact**: logs, summaries, manifests, reports, or other outputs that let you verify what happened

## Study map

This sequence is deliberate:

1. Module 01 teaches the semantic floor: truthful file contracts and rebuild behavior.
2. Module 02 adds dynamic DAGs, integrity, environments, and performance patterns.
3. Module 03 moves into production operation: profiles, retries, staging, and governance.
4. Module 04 focuses on scaling boundaries: modularity, CI gates, and executor-proof semantics.

If Module 02 feels unstable, the usual cause is that Module 01 has not become second nature yet.

## Capstone roadmap

The capstone evolves from “reference workflow” into “executable proof” as you move through the course:

- Module 01 explains why its file contracts and publish boundary are structured the way they are.
- Module 02 explains its checkpoint behavior, discovery discipline, and integrity artifacts.
- Module 03 explains its profiles, retries, dry-runs, and verification targets.
- Module 04 explains its module boundaries, file API, and CI-style gate structure.

## How to use the course well

- Read each module overview before the deeper module body.
- Treat diagrams as semantic claims, not decoration.
- Keep the capstone open while reading so workflow design stays attached to real files.
- Re-run proof-oriented targets frequently instead of only at the end.
