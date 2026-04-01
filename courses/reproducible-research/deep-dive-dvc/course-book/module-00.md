# Module 00 — Orientation

Deep Dive DVC is the reproducible-research course about **state**. Make and Snakemake
teach how systems change. DVC teaches what those systems are changing, how that state
acquires identity, and how teams recover it after time, drift, and failure.

## The question this course owns

Keep one question in view while reading:

> When a result is challenged six months later, which exact state can the team recover,
> compare, and prove?

If the answer is vague, reproducibility is still aspirational.

## Where this course fits

The reproducible-research family is converging on a durable program map:

1. **How systems change**: Make
2. **How state transitions scale**: Snakemake and similar workflow engines
3. **What state is**: DVC
4. **Where state executes**: containers and runtime isolation
5. **How state survives authority and time**: CI, retention, recovery, and auditability

This course owns the third layer, but it necessarily touches the fourth and fifth
because state only matters if it can survive real execution pressure.

## What this course is trying to change in the learner

By the end of the course, you should stop treating these as side details:

- dataset filenames
- parameter files
- metric reports
- experiment branches
- remotes and caches
- recovery procedures

They are not administrative overhead. They are the state contract.

## How to read the modules

Read the modules in order. Each one establishes an invariant the next one depends on:

1. **Why reproducibility fails**: identify the actual failure modes before reaching for tools.
2. **Data identity and content addressing**: define stable identity before discussing pipeline behavior.
3. **Execution environments as inputs**: treat runtimes as part of state, not external luck.
4. **Pipelines as truthful DAGs**: make stage boundaries inspectable and enforceable.
5. **Metrics, parameters, and meaning**: ensure comparisons remain semantically valid.
6. **Experiments without chaos**: explore without corrupting baseline history.
7. **Collaboration, CI, and social contracts**: make good behavior enforceable across people.
8. **Production, scale, and incident survival**: design for retention, recovery, and time.

## What the capstone proves

[`capstone/`](https://github.com/bijux/deep-dive-series/tree/master/courses/reproducible-research/deep-dive-dvc/capstone)
is the course’s executable proof. It is a small but real DVC repository centered on an
incident-escalation prediction workflow. It gives the course a concrete place to test:

- committed source data versus derived state
- truthful pipeline declarations in `dvc.yaml`
- declared parameters and tracked metrics
- a stable `publish/v1/` output contract
- experiment-ready inputs in `params.yaml`
- recovery from remote after local cache loss

If a module claim cannot be pointed to in the capstone, the claim should be treated with suspicion.

## Questions to keep asking while you read

- Which state is authoritative, and which state is only a projection?
- Which changes should invalidate a run, and which should not?
- Which artifacts are safe to compare across time?
- Which promotion or recovery rule would fail first under team pressure?

## What not to expect

This course is not a catalog of DVC commands and not a generic machine-learning tutorial.
It is a correctness-first course about making state durable enough that another person can
trust it under review, CI, and recovery.
