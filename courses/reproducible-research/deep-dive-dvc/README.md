# Deep Dive DVC

Deep Dive DVC is a course-book and executable capstone for reasoning about data and pipeline state in reproducible research systems. It focuses on DVC as the layer that gives datasets, parameters, experiments, and recovery procedures durable mechanical contracts.

Within the broader `reproducible-research` family, this course covers the question: what exactly is the state a system claims to reproduce?

## What this course covers

- Why reproducibility fails in data-heavy work even when code is versioned
- Why content-addressed data identity matters more than filenames and paths
- Why environments, parameters, metrics, and experiments must be treated as declared inputs
- How DVC stages, locks, remotes, and experiments become auditable operational contracts
- How collaboration, CI, retention, and incident recovery determine whether a system survives contact with time

## Course structure

- `course-book/` contains the published course material.
- `capstone/` contains the reference repository that exercises the course contracts end to end.
- `Makefile` exposes stable course-level entrypoints inside the monorepo.

## Quickstart

Preview the course book locally from the repository root:

```bash
make COURSE=reproducible-research/deep-dive-dvc docs-serve
```

Run the course-level verification target:

```bash
make COURSE=reproducible-research/deep-dive-dvc test
```

Run the capstone directly:

```bash
make -C courses/reproducible-research/deep-dive-dvc/capstone confirm
```

That confirmation suite performs `dvc repro`, runs the Python tests, pushes artifacts to the local training remote, deletes workspace state and cache, and restores the publish boundary via `dvc pull` plus `dvc checkout`.

## Module map

- `00` Orientation
- `01` Why Reproducibility Fails
- `02` Data Identity and Content Addressing
- `03` Execution Environments as Inputs
- `04` Pipelines as Truthful DAGs
- `05` Metrics, Parameters, and Meaning
- `06` Experiments Without Chaos
- `07` Collaboration, CI, and Social Contracts
- `08` Production, Scale, and Incident Survival

## License

MIT — see the repository root [LICENSE](https://github.com/bijux/deep-dive-series/blob/master/LICENSE).
