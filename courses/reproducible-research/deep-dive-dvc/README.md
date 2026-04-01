# Deep Dive DVC

Deep Dive DVC is the state-management course in the `reproducible-research` family.
It treats data identity, parameters, metrics, experiments, remotes, and recovery as
engineering contracts instead of convenience features.

This course exists to answer one hard question clearly:

> When a team says a result is reproducible, what exact state can it recover, prove,
> compare, and restore?

## Who this course is for

- Engineers who already use Git and pipelines but still lose trustworthy state
- Researchers and platform teams who need data and experiment lineage to survive time
- Reviewers who want sharper criteria than "the notebook still runs on my machine"
- Maintainers who need recovery drills, retention rules, and promotion discipline

## Who this course is not for

- Readers looking for a command reference without system design trade-offs
- People treating DVC as a thin wrapper around file syncing
- Teams that want experiment freedom without auditability or recovery guarantees

## What you will be able to do

By the end of the course, you should be able to:

- explain why path names are not stable data identity
- distinguish workspace state, Git state, cache state, and remote durability
- design truthful `dvc.yaml` pipelines with declared parameters, metrics, and outputs
- run experiments without turning baseline history into guesswork
- define promotion, retention, and recovery rules that survive real team pressure

## Reading contract

This is not a browse-at-random reference. The reading order matters:

1. Learn why reproducibility fails before evaluating tools.
2. Learn state identity before discussing pipelines and experiments.
3. Learn truthful pipeline state before comparing metrics or promoting runs.
4. Learn experiments before governance, CI, retention, and incident recovery.

If you skip that order, later material will still be readable, but the operational
trade-offs will feel procedural instead of principled.

## What this course covers

- why reproducibility fails even when code is versioned
- why content-addressed identity matters more than filenames and paths
- why environments, parameters, and metrics are part of state rather than side notes
- how DVC stages, locks, remotes, and experiments become auditable contracts
- how collaboration, CI, retention, and recovery decide whether the system survives

## How the capstone fits

[`capstone/`](https://github.com/bijux/deep-dive-series/tree/master/courses/reproducible-research/deep-dive-dvc/capstone)
is the executable proof for the course. It is a DVC repository built around an
incident-escalation prediction workflow with:

- a committed source dataset
- a truthful four-stage `dvc.yaml` graph
- declared parameters and tracked metrics
- a stable `publish/v1/` boundary
- a recovery drill that restores state from a DVC remote after cache loss

The course should make that repository easier to reason about. The capstone should make
the course’s claims harder to hand-wave.

## Working locally

From the repository root:

```bash
make COURSE=reproducible-research/deep-dive-dvc docs-serve
make COURSE=reproducible-research/deep-dive-dvc test
```

Run the capstone directly:

```bash
make -C courses/reproducible-research/deep-dive-dvc/capstone confirm
```

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
