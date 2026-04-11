# Worked Example: Auditing a Fragile ML Workflow

This example shows what Module 01 looks like when you apply it to a workflow that seems
fine at first glance.

The point is not to shame the workflow. The point is to learn how to describe its risks
precisely before reaching for DVC.

## The starting repository

A small team has this repository:

- `train.py`
- `evaluate.py`
- `run_all.sh`
- `config.yaml`
- `data/train.csv`
- `metrics.csv`
- `README.md`

The team says:

> everything important is in Git, and we can rerun the project if we need to.

That statement is common. It is also exactly what Module 01 is meant to test.

## Step 1: Ask whether this is repeatable or reproducible

The original author can still run:

```bash
bash run_all.sh
```

and gets a metric close to the previous one.

That is a useful signal, but it does not settle the stronger team question:

- could another teammate recover the same result next month
- from the repository alone
- without asking the author what was done by habit

At this point the workflow has shown local repeatability, not team-grade reproducibility.

## Step 2: Inventory the hidden state

Once the team looks more carefully, they uncover:

- `train.csv` was cleaned manually from a larger raw export
- one threshold is overridden from shell history during some runs
- the author's notebook was used once to generate a feature file that still sits in the
  working directory
- the Conda environment was updated twice since the last release
- `metrics.csv` is trusted in meetings, but nobody can tie it to exact data identity

This is the moment the workflow starts looking less "simple" and more honestly described.

## Step 3: Ask what Git is preserving and what it is not

Git is preserving:

- code history
- the visible config file
- the README

Git is not directly preserving:

- the exact identity of the cleaned dataset
- the relationship between raw data, the feature file, and the metric artifact
- the shell-level threshold override
- the durable recovery path for derived results

That is not Git failing. That is Git being asked to carry a larger story than it owns.

## Step 4: Ask what DVC would help with

At this point a learner can make a stronger statement:

> the problem is not merely that we need version control. The problem is that data
> identity, derived artifacts, and the path from inputs to outputs are still too implicit.

That is where DVC starts to make sense.

DVC would help make explicit:

- which data artifact is actually being referenced
- which stages produce which outputs
- which derived artifacts can be recovered later

But even here, Module 01 insists on discipline:

DVC still would not fix the scientific meaning of the threshold or the quality of the
manual cleaning decision by itself.

## Step 5: Write the first honest inventory

The team rewrites its self-description like this:

- source input: cleaned `train.csv`, but raw-to-clean lineage is weak
- control inputs: `config.yaml` plus one threshold sometimes overridden manually
- execution assumptions: one shared Conda environment and one manually produced feature file
- trusted output: `metrics.csv`
- weak points: unclear data identity, hidden manual preprocessing, weak artifact recovery

This is a much stronger starting point than:

> everything important is in the repo.

## What this example teaches

This workflow is not unusual.

It has many strengths:

- the team writes code down
- the team has a runnable script
- the team stores outputs they care about

But it still has the exact failure shape Module 01 is trying to expose:

- success depends on more than the recorded repository
- the trusted result is not fully defended by explicit state
- the team has local repeatability but weak transferability

## The review note you would want

> The current workflow is locally runnable but not yet reproducible in a team-grade sense.
> Git is preserving code and visible config, but the exact identity of the cleaned dataset,
> the manual preprocessing story, and the control surface for thresholds remain weak. The
> team's trusted artifact is `metrics.csv`, but the repository cannot yet explain it
> without social memory. This is the right moment to make data identity, stage boundaries,
> and recoverable artifacts explicit rather than continuing to rely on convention.

That note is calm, specific, and ready for later DVC modules.

## Why this is a mastery example

This one small story exercises the whole module:

- Core 1: it separates repeatability from reproducibility
- Core 2: it names hidden state directly
- Core 3: it respects Git while naming its limits
- Core 4: it gives DVC a clear, bounded role
- Core 5: it ends with an honest workflow inventory instead of a vague tool wish
