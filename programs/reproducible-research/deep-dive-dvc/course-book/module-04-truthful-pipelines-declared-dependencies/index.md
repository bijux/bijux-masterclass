# Module 04: Truthful Pipelines and Declared Dependencies

Module 04 turns DVC from a storage story into an execution story.

By now, learners already know two important facts:

- data identity should come from content, not path names
- runtime can influence a result even when code and data look unchanged

The next question is sharper:

can the pipeline itself tell the truth about why a result exists?

A DVC pipeline is only reviewable when its declared graph matches the real work. If a
script reads a file that is not listed, writes an output that is not owned, or uses a
control value that is hidden inside code, DVC can still run. The danger is that it may run
for reasons the team cannot explain, or skip work when the result is already stale.

This module is about replacing "the script usually works" with a declared execution graph
that a reviewer can inspect, challenge, and reproduce.

The capstone corroboration surface for this module is the set of files that show declared
execution truth: `capstone/dvc.yaml`, `capstone/dvc.lock`, `capstone/params.yaml`,
`course-book/capstone-docs/stage-contract-guide.md`, `course-book/capstone-docs/experiment-guide.md`, and
the `make -C capstone verify` route.

## Why this module exists

Many pipelines fail quietly because the graph is incomplete.

Common examples look ordinary at first:

- a preparation script reads a lookup table that is not in `deps`
- a model script uses a threshold literal instead of a value in `params.yaml`
- an evaluation command writes a report but only the metric file is declared as an output
- a shared intermediate directory is reused by two commands without a clear owner
- a stage reruns so often that the team stops investigating why

These are not cosmetic problems. They decide whether `dvc repro` has enough declared
information to make a correct decision.

The point of Module 04 is not to memorize every DVC field. The point is to learn the
review habit:

> If this result changed, could I explain the change from declared dependencies,
> parameters, outputs, command text, and recorded lock evidence?

If the answer is no, the pipeline is not yet truthful enough.

## Study route

```mermaid
flowchart LR
  overview["Overview"] --> core1["Core 1: stage contract"]
  core1 --> core2["Core 2: dependency, parameter, output boundaries"]
  core2 --> core3["Core 3: staleness and lock evidence"]
  core3 --> core4["Core 4: false reruns and stale outputs"]
  core4 --> core5["Core 5: refactoring and shared outputs"]
  core5 --> example["Worked example"]
  example --> practice["Exercises and answers"]
  practice --> glossary["Glossary"]
```

Read the module in that order the first time.

If the problem is already partly clear, use this shortcut:

- open Core 1 when the main confusion is "what is a DVC stage promising?"
- open Core 2 when the main confusion is "what belongs in `deps`, `params`, or `outs`?"
- open Core 3 when the main confusion is "why did `dvc repro` rerun or skip?"
- open Core 4 when the main confusion is "which failure is merely annoying and which is dangerous?"
- open Core 5 when the main confusion is "how do I change pipeline shape without losing provenance?"

## Module map

| Page | Purpose |
| --- | --- |
| `index.md` | explains the module promise and study route |
| `stage-contracts-and-declared-truth.md` | teaches the promise each DVC stage makes |
| `dependency-parameter-output-boundaries.md` | teaches how to place inputs, controls, and outputs in the graph |
| `dvc-repro-staleness-and-lock-evidence.md` | teaches how `dvc repro` decides and how `dvc.lock` records evidence |
| `false-reruns-and-stale-outputs.md` | teaches how to distinguish wasteful reruns from dangerous stale results |
| `safe-pipeline-refactoring-and-shared-outputs.md` | teaches graph change, shared intermediates, and multi-output care |
| `worked-example-repairing-a-deceptive-pipeline.md` | walks through one realistic pipeline review and repair |
| `exercises.md` | gives five mastery exercises |
| `exercise-answers.md` | explains model answers and review logic |
| `glossary.md` | keeps the module vocabulary stable |

## What should be clear by the end

By the end of this module, you should be able to explain:

- what makes a DVC stage truthful rather than merely convenient
- how to decide whether a file belongs in `deps`, `outs`, or neither
- how parameter declaration turns control values into reviewable change
- how `dvc repro` uses declared state and lock evidence to decide what reruns
- why stale outputs are more dangerous than extra reruns
- how to refactor a pipeline without breaking the provenance story

## Commands to keep close

These commands form the evidence loop for Module 04:

```bash
make -C capstone verify
make -C capstone walkthrough
dvc dag
dvc status
dvc repro
```

Use `make -C capstone verify` and `make -C capstone walkthrough` from the capstone root
when you want the course-provided review route. Use `dvc dag`, `dvc status`, and
`dvc repro` inside a DVC workspace when you want to inspect the declared graph and rerun
decision directly.

## Capstone route

Use the capstone after you can describe a single stage in plain language.

Best corroboration surfaces for this module:

- `capstone/dvc.yaml`
- `capstone/dvc.lock`
- `capstone/params.yaml`
- `course-book/capstone-docs/stage-contract-guide.md`
- `course-book/capstone-docs/experiment-guide.md`
- `course-book/capstone-docs/publish-contract.md`

Useful proof route:

```bash
make -C capstone walkthrough
make -C capstone verify
```

The point of that route is not to trust the graph because it exists. It is to practice
asking whether each declared edge matches the real read, write, and control behavior of
the pipeline.
