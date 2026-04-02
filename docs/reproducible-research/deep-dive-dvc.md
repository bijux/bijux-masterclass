# Deep Dive DVC

Deep Dive DVC teaches reproducibility as a question of state: how data,
parameters, metrics, experiments, and recovery evidence acquire stable identity
and remain trustworthy over time.

## Repository Location

`programs/reproducible-research/deep-dive-dvc`

## What It Contains

- A learner entry route and supporting course navigation pages in `course-book/`
- A ten-module program guide in `course-book/`
- A documented capstone entrypoint in `capstone/`
- Local development entrypoints in `Makefile`

## Local Commands

```bash
make PROGRAM=reproducible-research/deep-dive-dvc docs-build
make PROGRAM=reproducible-research/deep-dive-dvc test
```

## Best First Reads

Start with `course-book/start-here.md`, then `course-book/module-00.md`, then
`course-book/capstone-map.md`.
