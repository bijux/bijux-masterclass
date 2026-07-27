# Practice Map

Use this page when you want to see the full hundred-exercise route as a learning system
rather than as ten separate module checklists. A good practice map answers four questions:

1. what am I building
2. what is this exercise trying to teach
3. what evidence should I keep
4. when should I widen from local practice to capstone review

## The hundred-exercise route

Each module has ten exercises. Exercises 1-5 should make the local concept legible.
Exercises 6-10 should make that concept transferable under pressure, review, or change.

| Module | Exercises 1-5 teach | Exercises 6-10 teach | Evidence to retain |
| --- | --- | --- | --- |
| 01 File Contracts | targets, convergence, wildcards, config, atomic outputs | build, plan, selective rebuild, missing-input diagnosis, tiny project completion | dry-runs, DAG views, rebuild notes |
| 02 Dynamic DAGs | discovery, fan-out, checkpoint choice, integrity, discovery overhead | validated registry, paired records, runtime discovery, change trials, publish bundle reasoning | discovery artifacts, graph comparisons |
| 03 Production Operations | policy, failure classes, storage, proof routes, review habits | profile comparison, failure injection, staged data, clean-room runs, policy review | profile diffs, failure logs, summary outputs |
| 04 Scaling Boundaries | rule families, module choice, file APIs, gates, resources | include refactors, module design, schema break tests, resource mapping, scaling review | graph comparisons, boundary notes |
| 05 Software Boundaries | placement, runtime surfaces, hidden inputs, wrappers, drift | script extraction, package tests, environment reproduction, drift checks, boundary review | tests, provenance notes, environment evidence |
| 06 Publish Contracts | public boundary, compatibility, integrity, roles, drift | bundle construction, manifest verification, consumer tests, change classification, version migration | consumer checks, manifests, checksum results |
| 07 Workflow Architecture | entrypoints, splits, file APIs, coupling, refactor choices | artifact tracing, responsibility maps, drift detection, design comparison, repository review | ownership maps, architectural findings |
| 08 Operating Contexts | profile safety, retries, storage, contexts, leaks | policy matrixes, plan comparison, resource mapping, scratch promotion, drift gates | normalized context audits |
| 09 Incident Response | cost classes, evidence choice, triage, tuning, runbook thinking | baselines, evidence packets, controlled tuning, context regression checks, runbook rehearsal | measurements, incident bundles, review notes |
| 10 Governance and Migration | current truth, migration order, governance, anti-patterns, handoff | inventories, characterization, owner migration, policy enforcement, tool-handoff design | stewardship records, equivalence evidence |

## The study rhythm for every module

Keep the same rhythm across the whole course:

1. build the smallest local example first
2. complete Exercises 1-5 without consulting the answers
3. retain the evidence named for that module
4. complete Exercises 6-10 under a little more pressure
5. compare your reasoning with the model answers
6. widen into the capstone only after the local concept is legible

This rhythm matters because the course is trying to build independent judgment, not just
successful command execution.

## What evidence to keep and why

The evidence column is part of the exercise, not optional bookkeeping.

| Evidence type | Why it matters |
| --- | --- |
| dry-runs and DAG views | they prove planned behavior before execution |
| discovery artifacts | they make dynamic graphs reviewable later |
| profile diffs and context audits | they separate policy variation from semantic drift |
| manifests and consumer checks | they show whether published outputs are trustworthy downstream |
| tests and provenance notes | they expose helper-boundary and environment claims |
| measurements and incident bundles | they keep diagnosis from collapsing into memory |
| stewardship records | they explain how the workflow should change over time |

If you finish an exercise without retaining the named evidence, you have completed an
activity but weakened the learning record.

## Reusable proof loops

Use these small command loops whenever you need a fast, honest check.

### Contract loop

Use when you are checking whether rule graph and output claims are explicit enough.

```bash
snakemake -n
snakemake --summary
```

### Discovery loop

Use when you are checking whether dynamic behavior remains inspectable.

```bash
snakemake -n
snakemake --dag
snakemake --summary
```

### Operating loop

Use when you are checking whether policy changes context without changing meaning.

```bash
snakemake --profile profiles/local -n
snakemake --profile profiles/ci -n
```

### Incident loop

Use when you are investigating slow, noisy, or surprising behavior.

```bash
snakemake -n -p
snakemake --summary
snakemake --list-changes input code params
```

### Layer-review loop

Use when the main question is where a change belongs before you implement it.

```bash
snakemake --list-rules
snakemake -n
snakemake --summary
```

## When to enter the capstone

Enter the capstone when one of these becomes true:

- you can explain the local exercise result without reading the answer page
- you want to see the same concept inside a larger governed repository
- you need to compare multiple boundaries at once
- you need to retain stronger evidence than a toy example can provide

Do not enter the capstone just because it feels more advanced. Enter it when the local
concept is stable enough to survive scale.

## Signs you are practicing badly

Slow down if:

- you can run the command sequence but cannot say what the evidence proves
- you keep skipping the retained-evidence step
- every harder exercise feels like a totally new topic
- you are using the answer page before making a prediction
- the capstone feels like a rescue from weak local understanding

## Good stopping point

Stop when you can name:

1. what you built
2. what the exercise was trying to teach
3. what evidence you retained
4. what the next exercise adds that the current one did not

## Companion pages

- [Module Dependency Map](module-dependency-map.md)
- [Self-Review Prompts](self-review-prompts.md)
- [Completion Rubric](completion-rubric.md)
- [Capstone Map](../capstone/capstone-map.md)
