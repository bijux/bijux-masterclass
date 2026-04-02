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

1. `course-book/guides/start-here.md`
2. `course-book/guides/index.md`
3. `course-book/guides/course-guide.md`
4. `course-book/guides/pressure-routes.md` if you need the fastest honest route by work pressure
5. `course-book/guides/module-promise-map.md` and `course-book/guides/module-checkpoints.md` to keep the module promises and exit bars visible
6. `course-book/module-00-orientation/index.md`
7. Modules `01` to `10` in order, following the state, execution, collaboration, and governance arc
8. `course-book/capstone/index.md`, `course-book/capstone/capstone-map.md`, and `course-book/guides/proof-ladder.md` once the state model feels stable

The route matters because the program is trying to build judgment, not only command recall.

The course-book now has four stable top-level surfaces:

- `course-book/guides/` for learner routes, proof selection, and reading pressure
- `course-book/capstone/` for repository entry, command routing, recovery review, and release review
- `course-book/reference/` for durable maps, glossary pages, and review standards
- `course-book/module-00-orientation/` plus Modules `01` to `10` for the core teaching arc

If you are choosing where to enter, use:

- `course-book/guides/pressure-routes.md` for the smallest honest route by problem shape
- `course-book/guides/module-promise-map.md` for what each module truly promises
- `course-book/guides/module-checkpoints.md` for module-end readiness checks
- `course-book/guides/proof-ladder.md` for how to escalate from tour to stronger proof
- `course-book/capstone/index.md` and `course-book/capstone/capstone-map.md` for the repository entry shelf once the state model is stable
- `course-book/reference/topic-boundaries.md` for what this course treats as central, adjacent, or out of scope
- `course-book/reference/anti-pattern-atlas.md` for common reproducibility failures and where the course addresses them

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
make PROGRAM=reproducible-research/deep-dive-dvc capstone-confirm
```

Run the published capstone routes from the repository root:

```bash
make PROGRAM=reproducible-research/deep-dive-dvc capstone-confirm
make PROGRAM=reproducible-research/deep-dive-dvc capstone-walkthrough
```

`make install` inside `programs/reproducible-research/deep-dive-dvc/capstone/` is the network-dependent setup step because it creates
the managed virtual environment and installs DVC there. Use
`course-book/guides/platform-setup.md` and `course-book/reference/version-support-guide.md`
when you need the exact support contract before running proof commands.

## Module map

| Module | Title | Main focus |
| --- | --- | --- |
| `00` | Orientation and Study Practice | establish the learner route, proof surfaces, and capstone timing |
| `01` | Why Reproducibility Fails in Real Teams | name the failure modes before teaching tools |
| `02` | Data Identity and Content Addressing | separate stable paths from stable bytes and stable meaning |
| `03` | Execution Environments as Reproducible Inputs | treat environment assumptions as part of the contract |
| `04` | Truthful Pipelines and Declared Dependencies | make workflow edges visible enough to trust reruns |
| `05` | Metrics, Parameters, and Comparable Meaning | keep comparisons honest as experiments evolve |
| `06` | Experiments, Baselines, and Controlled Change | organize experimentation without mutating the truth surface |
| `07` | Collaboration, CI, and Social Contracts | make team pressure and automation part of the state model |
| `08` | Recovery, Scale, and Incident Survival | rehearse failure, recovery, and retained authority under pressure |
| `09` | Promotion, Registry Boundaries, and Auditability | treat release and registry state as explicit trust boundaries |
| `10` | Migration, Governance, and DVC Boundaries | finish with stewardship, migration, and tool-boundary judgment |

## License

MIT — see the repository root [LICENSE](https://github.com/bijux/bijux-masterclass/blob/master/LICENSE).
