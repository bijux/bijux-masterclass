# Module 01: Reproducibility Failures in Real Teams

Module 01 starts from the failure surface, not from the tool.

Before DVC can make sense, the learner has to see why ordinary Git-plus-script workflows
still leave teams unable to recover, compare, or defend results later.

This module is about naming those failures clearly:

- why a rerun can "work" and still fail trust
- why repeatability and reproducibility are not the same promise
- which hidden inputs make ML and data workflows fragile
- why Git and notebooks help but do not solve the whole problem
- what DVC is actually responsible for, and what remains outside its authority

The capstone corroboration surface for this module is the set of review guides that make
state, recovery, and published truth visible: `docs/STAGE_CONTRACT_GUIDE.md`,
`docs/RECOVERY_GUIDE.md`, `docs/PUBLISH_CONTRACT.md`, `make walkthrough`, and
`make proof`.

## Why this module exists

Many teams believe they have a reproducible workflow because:

- the code is in Git
- there is a README with the commands
- someone on the team can still rerun it locally
- the latest metrics were written down somewhere

Those are useful habits. They are not yet a reproducibility system.

This module exists to make that gap concrete before the course starts teaching DVC
mechanics. If learners do not see the failure model first, the rest of the program looks
like a collection of features instead of a coherent trust model.

## Study route

```mermaid
flowchart LR
  overview["Overview"] --> core1["Core 1: repeatability versus reproducibility"]
  core1 --> core2["Core 2: hidden state and undeclared inputs"]
  core2 --> core3["Core 3: why Git and scripts are not enough"]
  core3 --> core4["Core 4: what DVC does and does not own"]
  core4 --> core5["Core 5: your first honest workflow inventory"]
  core5 --> example["Worked example"]
  example --> practice["Exercises and answers"]
  practice --> glossary["Glossary"]
```

Read the module in that order the first time.

If the problem is already partly clear, use this shortcut:

- open Core 1 when the main confusion is "isn't rerunning enough?"
- open Core 2 when the main confusion is "what exactly is missing from the story?"
- open Core 3 when the main confusion is "why doesn't Git solve this already?"
- open Core 4 when the main confusion is "what problem is DVC actually responsible for?"
- open Core 5 when the main confusion is "how do I inspect my own workflow honestly?"

## Module map

| Page | Purpose |
| --- | --- |
| `index.md` | explains the module promise and study route |
| `repeatability-versus-reproducibility.md` | teaches the difference between local reruns and durable trust |
| `hidden-state-and-undeclared-inputs.md` | teaches which influential inputs ordinary workflows usually leave out |
| `why-git-and-scripts-are-not-enough.md` | teaches what Git does well and where it stops |
| `what-dvc-does-and-does-not-own.md` | teaches DVC's authority, boundaries, and non-goals |
| `the-first-honest-workflow-inventory.md` | teaches how learners audit their own workflow before touching DVC |
| `worked-example-auditing-a-fragile-ml-workflow.md` | walks through one realistic Git-plus-script failure story |
| `exercises.md` | gives five mastery exercises |
| `exercise-answers.md` | explains model answers and review logic |
| `glossary.md` | keeps the module vocabulary stable |

## What should be clear by the end

By the end of this module, you should be able to explain:

- why repeatability is weaker than reproducibility
- which hidden inputs make ordinary ML and data workflows hard to defend later
- what Git and ad hoc scripts can preserve, and what they cannot
- what DVC is meant to make explicit, and what still remains outside DVC's scope
- how to describe your own workflow's weak points without jumping straight to tools

## Commands to keep close

These commands form the review loop for Module 01:

```bash
git log --oneline -5
make -C capstone walkthrough
make -C capstone proof
```

This module is intentionally light on commands. The real work here is diagnosis and
language. The commands matter because they give the learner something concrete to inspect
instead of speaking only in abstractions.

## Capstone route

Use the capstone only after the failure model is already clear.

Best corroboration surfaces for this module:

- `capstone/docs/STAGE_CONTRACT_GUIDE.md`
- `capstone/docs/RECOVERY_GUIDE.md`
- `capstone/docs/PUBLISH_CONTRACT.md`
- `capstone/docs/REVIEW_ROUTE_GUIDE.md`
- `capstone/Makefile`

Useful proof route:

```bash
make -C capstone walkthrough
make -C capstone proof
```

The point of that route is not to learn DVC by osmosis from the capstone. It is to see
that real repositories need visible state layers, recovery routes, and contract language
before anyone can claim reproducibility with a straight face.
