# Module 05: Metrics, Parameters, and Comparable Meaning

Module 05 turns successful pipeline execution into defensible interpretation.

By now, learners know how to reason about content identity, runtime boundaries, and
truthful pipeline declarations. That is necessary, but it is not enough. A workflow can
run honestly and still invite a bad conclusion if its metrics and parameters do not mean
the same thing across runs.

This module is about comparability:

- what a metric claims to measure
- which population the metric describes
- which parameter values belong to the comparison surface
- which plot or table conventions must stay stable
- when a numeric difference is meaningful and when it is only mechanical

The central learner question is:

> Are these two results describing the same reality under comparable controls?

If the answer is unclear, `dvc metrics diff` can still show numbers, but the team does not
yet have a defensible comparison.

The capstone corroboration surface for this module is the set of files that tie
parameters, metrics, and release evidence together: `capstone/params.yaml`,
`capstone/metrics/metrics.json`, `capstone/plots/`, `capstone/publish/v1/metrics.json`,
`capstone/docs/RELEASE_REVIEW_GUIDE.md`, `capstone/docs/PUBLISH_CONTRACT.md`, and
the `make -C capstone release-audit` route.

## Why this module exists

Many teams can answer:

- did the run finish
- did the data match
- did the pipeline rerun correctly
- did the metric move

and still fail to answer:

- did the test population stay comparable
- did the metric definition change
- did the threshold or split policy move
- did the plot compare the same slice of data
- should this number be used for a release decision

That is where DVC usage needs interpretation discipline. DVC can track metric files,
diff values, and connect parameter changes to runs. It cannot decide by itself whether a
metric comparison is semantically valid.

The point of Module 05 is not to collect more numbers. The point is to defend the meaning
of the numbers already being used.

## Study route

```mermaid
flowchart LR
  overview["Overview"] --> core1["Core 1: metrics as claims"]
  core1 --> core2["Core 2: parameter comparison surface"]
  core2 --> core3["Core 3: metric files and schemas"]
  core3 --> core4["Core 4: metrics diff and review limits"]
  core4 --> core5["Core 5: plots and release interpretation"]
  core5 --> example["Worked example"]
  example --> practice["Exercises and answers"]
  practice --> glossary["Glossary"]
```

Read the module in that order the first time.

If the problem is already partly clear, use this shortcut:

- open Core 1 when the main confusion is "why isn't a metric just a number?"
- open Core 2 when the main confusion is "which parameter changes affect comparability?"
- open Core 3 when the main confusion is "what makes a metric file stable enough to review?"
- open Core 4 when the main confusion is "what can `dvc metrics diff` prove and not prove?"
- open Core 5 when the main confusion is "when are plots or release numbers safe to use?"

## Module map

| Page | Purpose |
| --- | --- |
| `index.md` | explains the module promise and study route |
| `metrics-as-semantic-claims.md` | teaches why metric values need population, definition, and intent |
| `parameters-as-comparison-controls.md` | teaches which controls belong to `params.yaml` and review |
| `metric-files-schemas-and-stability.md` | teaches stable metric file structure and meaning over time |
| `metrics-diff-and-review-boundaries.md` | teaches what DVC diffs can show and what humans must still judge |
| `plots-and-release-interpretation.md` | teaches plots, visual evidence, and release-facing metric discipline |
| `worked-example-repairing-a-misleading-metric-comparison.md` | walks through one realistic comparison repair |
| `exercises.md` | gives five mastery exercises |
| `exercise-answers.md` | explains model answers and review logic |
| `glossary.md` | keeps the module vocabulary stable |

## What should be clear by the end

By the end of this module, you should be able to explain:

- why a metric is a semantic claim, not only a scalar value
- how parameter changes alter the comparison surface
- why metric schemas and naming conventions need stability
- what `dvc metrics diff` can show without judging meaning
- how plots can mislead when population, sorting, aggregation, or rendering drift
- what evidence belongs in a release review before trusting a metric movement

## Commands to keep close

These commands form the evidence loop for Module 05:

```bash
make -C capstone release-audit
make -C capstone prediction-review
dvc metrics show
dvc metrics diff
dvc params diff
```

Use the `make` routes for the course-provided capstone review. Use the `dvc` commands
inside a DVC workspace when you want to inspect metric and parameter differences directly.

## Capstone route

Use the capstone after the metric meaning question is clear.

Best corroboration surfaces for this module:

- `capstone/params.yaml`
- `capstone/metrics/metrics.json`
- `capstone/plots/`
- `capstone/publish/v1/metrics.json`
- `capstone/publish/v1/params.yaml`
- `capstone/docs/RELEASE_REVIEW_GUIDE.md`
- `capstone/docs/RELEASE_REVIEW_GUIDE.md`
- `capstone/docs/PUBLISH_CONTRACT.md`

Useful proof route:

```bash
make -C capstone prediction-review
make -C capstone release-audit
```

The point of that route is not to accept a number because it appears in a metric file. It
is to ask whether the parameter surface, population, metric definition, and published
evidence support the comparison a reviewer wants to make.
