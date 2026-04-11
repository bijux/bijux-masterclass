# Metric Files, Schemas, and Stability

A metric file is small, but it carries a lot of meaning.

When a workflow writes `metrics/metrics.json`, reviewers are not only looking at values.
They are trusting a structure:

- which keys exist
- what each key means
- which units the values use
- which population the values describe
- whether missing values are allowed
- whether new keys are additive or meaning-changing

That structure is a schema, even if nobody wrote a formal schema file.

## A simple metric file still has a contract

Example:

```json
{
  "incident_escalation": {
    "positive_class_f1_at_fixed_threshold": 0.81,
    "precision_at_fixed_threshold": 0.78,
    "recall_at_fixed_threshold": 0.84,
    "evaluation_population_size": 420
  }
}
```

This file says more than four numbers. It says the metrics belong to incident escalation,
the threshold is fixed, and the population size is part of review.

That is easier to defend than:

```json
{
  "f1": 0.81,
  "precision": 0.78,
  "recall": 0.84
}
```

Short keys are not always wrong, but vague keys make future comparison harder.

## Schema drift changes interpretation

Schema drift happens when the file structure changes in a way that affects meaning.

Examples:

- `f1` changes from positive-class F1 to macro F1
- `accuracy` changes from all incidents to only high-confidence incidents
- `population_size` disappears
- a value changes from a fraction to a percentage
- null handling changes without explanation
- a nested key moves and downstream review scripts silently read the old path

Some changes are legitimate. The problem is not change. The problem is pretending that a
meaning-changing file change is just a normal metric update.

When schema meaning changes, say so in review and avoid comparing old and new values as
if they were the same measurement.

## Stable additions versus breaking changes

Adding a new metric can be safe if existing metric meanings stay unchanged.

Example of a mostly additive change:

```json
{
  "incident_escalation": {
    "positive_class_f1_at_fixed_threshold": 0.81,
    "precision_at_fixed_threshold": 0.78,
    "recall_at_fixed_threshold": 0.84,
    "evaluation_population_size": 420,
    "false_positive_rate_at_fixed_threshold": 0.09
  }
}
```

The existing keys still mean the same thing. Reviewers can compare them across runs while
learning about the new key.

Example of a breaking change:

```json
{
  "incident_escalation": {
    "macro_f1_after_threshold_search": 0.84,
    "precision_after_threshold_search": 0.79,
    "recall_after_threshold_search": 0.91
  }
}
```

This may be a better evaluation design, but it is not the same metric contract. It should
not be interpreted as a simple improvement over fixed-threshold F1.

## Metric files should be boring to parse

Metric files are not a place for surprise.

Prefer:

- deterministic key names
- deterministic ordering when humans review diffs
- explicit units in names or documentation
- stable nesting
- clear missing-value behavior
- one canonical output path for the metric surface

Avoid:

- timestamped keys
- randomly ordered tables
- metric names that depend on the data slice at runtime
- mixed units under similar names
- silently replacing a metric definition while keeping the key

DVC can track file changes, but a stable file shape makes those changes easier for people
to review.

## Where to document meaning

The metric meaning can live in more than one place:

- the metric file key names
- a release review guide
- a model evaluation guide
- a schema or contract note
- the code that computes the metric
- the review note attached to a release

Do not rely on only one of these if the metric supports important decisions. A reviewer
should not need to reverse-engineer the metric definition from Python after every release.

## Review checkpoint

You understand this core when you can inspect a metric file and answer:

- what each key means
- whether the unit and population are clear
- whether a file change is additive or meaning-changing
- whether old and new values are safe to compare
- which documentation or review surface explains the metric contract

The learner goal is a metric file that ages well. Two years later, the team should still
know what the number meant.
