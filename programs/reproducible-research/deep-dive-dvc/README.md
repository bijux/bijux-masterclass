# Deep Dive DVC

Deep Dive DVC is the state-management program in the `reproducible-research` family.
It treats data identity, parameters, metrics, experiments, remotes, promotion, and
recovery as engineering contracts instead of convenience features, from first-contact
reproducibility thinking to long-lived repository stewardship.

This course exists to answer one hard question clearly:

> When a team says a result is reproducible, what exact state can it recover, prove,
> compare, and restore?

## Who this program is for

- Readers who want a beginner-to-mastery path through DVC instead of only a command reference
- Engineers who already use Git and pipelines but still lose trustworthy state
- Researchers and platform teams who need data and experiment lineage to survive time
- Reviewers who want sharper criteria than "the notebook still runs on my machine"
- Maintainers who need recovery drills, retention rules, and promotion discipline

## Who this program is not for

- Readers looking for a command reference without system design trade-offs
- People treating DVC as a thin wrapper around file syncing
- Teams that want experiment freedom without auditability or recovery guarantees

## What you will be able to do

By the end of the program, you should be able to:

- explain why path names are not stable data identity
- distinguish workspace state, Git state, cache state, and remote durability
- design truthful `dvc.yaml` pipelines with declared parameters, metrics, and outputs
- run experiments without turning baseline history into guesswork
- define promotion, retention, and recovery rules that survive real team pressure

## Learner route

Use the course in this order:

1. `course-book/start-here.md`
2. `course-book/course-guide.md`
3. `course-book/learning-contract.md`
4. `course-book/module-00.md`
5. Modules `01` to `10` in order
6. `course-book/readme-capstone.md` and `course-book/capstone-map.md` once the state model feels stable

The route matters because the program is trying to build judgment, not only command recall.

## What this program covers

- why reproducibility fails even when code is versioned
- why content-addressed identity matters more than filenames and paths
- why environments, parameters, and metrics are part of state rather than side notes
- how DVC stages, locks, remotes, and experiments become auditable contracts
- how collaboration, CI, retention, and recovery decide whether the system survives

## How the capstone fits

[`capstone/`](https://github.com/bijux/bijux-masterclass/tree/master/programs/reproducible-research/deep-dive-dvc/capstone)
is the executable proof for the course. It is a DVC repository built around an
incident-escalation prediction workflow with:

- a committed source dataset
- a truthful four-stage `dvc.yaml` graph
- declared parameters and tracked metrics
- a stable `publish/v1/` boundary
- a recovery drill that restores state from a DVC remote after cache loss
- an experiments route that varies parameters without damaging the baseline contract
- a release review route that keeps downstream trust smaller than the internal repository story

The program should make that repository easier to reason about. The capstone should make
the program’s claims harder to hand-wave.

## Working locally

From the repository root:

```bash
make PROGRAM=reproducible-research/deep-dive-dvc docs-serve
make PROGRAM=reproducible-research/deep-dive-dvc test
make PROGRAM=reproducible-research/deep-dive-dvc capstone-tour
```

Run the capstone directly:

```bash
make -C programs/reproducible-research/deep-dive-dvc/capstone confirm
make -C programs/reproducible-research/deep-dive-dvc/capstone walkthrough
```

## Module map

- `00` Program outline
- `01` Why reproducibility fails
- `02` Data identity and content addressing
- `03` Execution environments as inputs
- `04` Pipelines as truthful DAGs
- `05` Metrics, parameters, and meaning
- `06` Experiments without chaos
- `07` Collaboration, CI, and social contracts
- `08` Production, scale, and incident survival
- `09` Promotion, registry boundaries, release contracts, and auditability
- `10` Mastery: migration, governance, anti-patterns, and tool boundaries

## License

MIT — see the repository root [LICENSE](https://github.com/bijux/bijux-masterclass/blob/master/LICENSE).
