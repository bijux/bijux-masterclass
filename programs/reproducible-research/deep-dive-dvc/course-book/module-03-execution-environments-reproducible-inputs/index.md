# Module 03: Execution Environments as Reproducible Inputs

By Module 03, learners already know that stable data identity matters.

The next surprise is harder:

even when code and data look stable, results can still drift because the execution
environment is part of the input surface.

This module is about making that invisible boundary visible:

- environment is not background weather
- honest runs can diverge without anyone being careless
- DVC can record some environment-adjacent evidence, but it does not own environment
  management by itself
- lockfiles, containers, and CI all solve different parts of the problem

The capstone corroboration surface for this module is the set of files and commands that
make the runtime boundary legible: `make platform-report`, `params.yaml`,
`capstone/docs/experiment-guide.md`, `capstone/docs/architecture.md`, and the install/runtime surface
in the capstone Makefile.

## Why this module exists

Many workflow teams say:

- the code did not change
- the data did not change
- the parameters did not change

and still get different outcomes.

That is where reproducibility gets more honest. The environment is often the missing input
surface hiding in plain sight.

This module exists so learners stop treating runtime as accidental background and start
treating it as part of the system they need to reason about.

## Study route

```mermaid
flowchart LR
  overview["Overview"] --> core1["Core 1: environment as input"]
  core1 --> core2["Core 2: determinism is a spectrum"]
  core2 --> core3["Core 3: what DVC records and what it does not"]
  core3 --> core4["Core 4: lockfiles, containers, and CI"]
  core4 --> core5["Core 5: diagnosing environment drift"]
  core5 --> example["Worked example"]
  example --> practice["Exercises and answers"]
  practice --> glossary["Glossary"]
```

Read the module in that order the first time.

If the problem is already partly clear, use this shortcut:

- open Core 1 when the main confusion is "why does runtime count as input?"
- open Core 2 when the main confusion is "how can honest runs still diverge?"
- open Core 3 when the main confusion is "what part of this is DVC actually helping with?"
- open Core 4 when the main confusion is "which environment strategy fits which pressure?"
- open Core 5 when the main confusion is "how do I review or diagnose drift sanely?"

## Module map

| Page | Purpose |
| --- | --- |
| `index.md` | explains the module promise and study route |
| `execution-environment-as-part-of-the-input-surface.md` | teaches why runtime belongs in the workflow story |
| `determinism-is-a-spectrum-not-a-switch.md` | teaches why divergence can be honest rather than mysterious |
| `what-dvc-records-indirectly-and-what-it-does-not-manage.md` | teaches DVC's boundary around environments |
| `lockfiles-containers-and-ci-as-environment-strategies.md` | teaches the main environment-control approaches and their tradeoffs |
| `reviewing-environment-drift-and-runtime-evidence.md` | teaches how to inspect and diagnose runtime differences without guesswork |
| `worked-example-explaining-a-local-versus-ci-drift.md` | walks through one realistic environment drift story |
| `exercises.md` | gives five mastery exercises |
| `exercise-answers.md` | explains model answers and review logic |
| `glossary.md` | keeps the module vocabulary stable |

## What should be clear by the end

By the end of this module, you should be able to explain:

- why the environment is part of the input surface
- why determinism is often conditional rather than absolute
- which runtime facts DVC helps surface and which it does not manage directly
- how lockfiles, containers, and CI differ as environment strategies
- how to review and diagnose environment drift without superstition

## Commands to keep close

These commands form the evidence loop for Module 03:

```bash
make -C capstone platform-report
make -C capstone verify
make -C capstone walkthrough
```

The point is not to collect more output. The point is to tie environment discussion to
concrete evidence instead of vague intuition.

## Capstone route

Use the capstone only after the runtime boundary already feels concrete.

Best corroboration surfaces for this module:

- `capstone/Makefile`
- `capstone/params.yaml`
- `capstone/docs/experiment-guide.md`
- `capstone/docs/architecture.md`
- `make -C capstone platform-report`

Useful proof route:

```bash
make -C capstone platform-report
make -C capstone walkthrough
make -C capstone verify
```

The point of that route is to make the capstone's declared runtime surface inspectable,
not to pretend the capstone eliminates every environment question by itself.
