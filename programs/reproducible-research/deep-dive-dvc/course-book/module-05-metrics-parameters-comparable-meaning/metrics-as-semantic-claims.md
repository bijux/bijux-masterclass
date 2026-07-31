# Metrics as Semantic Claims


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive DVC"]
  section["Metrics Parameters Comparable Meaning"]
  page["Metrics as Semantic Claims"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  orient["Orient on the page map"] --> read["Read the main claim and examples"]
  read --> inspect["Inspect the related code, proof, or capstone surface"]
  inspect --> verify["Run or review the verification path"]
  verify --> apply["Apply the idea back to the module and capstone"]
```
<!-- page-maps:end -->

A metric is not just a number in a file.

It is a claim about a system:

> On this population, using this definition, under these controls, the model behaved this
> way.

That sentence is longer than `accuracy: 0.87`, but it is the sentence reviewers actually
need. Without it, a metric value can look precise while saying something different from
what the team thinks it says.

## The four parts behind one number

Take a simple metric:

```json
{
  "accuracy": 0.87
}
```

The number hides several decisions:

- what examples were evaluated
- which labels counted as correct
- how missing or uncertain labels were handled
- whether the population was balanced or naturally imbalanced
- whether the threshold stayed fixed
- whether the metric was computed per incident, per customer, per day, or per alert

Changing any of those can change the meaning even when the field name stays the same.

```mermaid
flowchart TD
  value["accuracy = 0.87"] --> population["population"]
  value --> definition["metric definition"]
  value --> controls["parameters and thresholds"]
  value --> unit["unit of analysis"]
  value --> decision["review decision"]
```

The diagram is not asking you to write theory in every metric file. It is asking you to
stop treating a bare value as self-explanatory.

## A misleading comparison

Run A reports:

```json
{
  "accuracy": 0.87
}
```

Run B reports:

```json
{
  "accuracy": 0.89
}
```

Mechanically, B is higher by 0.02.

But suppose Run A used a stable holdout set of production-like incidents, while Run B used
a smaller evaluation set filtered to high-confidence labels only. The numeric comparison
is real, but the interpretation "the model improved" is not yet justified.

DVC can help track both files and show the numeric difference. It cannot decide whether
the population change invalidates the conclusion.

That judgment belongs to you and the review contract.

## Build the complete claim from evidence

Run the capstone audit:

```bash
make PROGRAM=reproducible-research/deep-dive-dvc capstone-metric-contract-audit
```

Open:

```text
artifacts/audit/reproducible-research/deep-dive-dvc/metric-contracts/
└── workspace/
    └── comparable-candidate/
        └── evidence/
            ├── baseline-metrics.json
            ├── candidate-metrics.json
            ├── dvc-metrics-diff.json
            └── comparison.json
```

The DVC receipt reports:

```text
0.7368 -> 0.7826
delta = 0.0458
```

That arithmetic becomes a comparison only after you join it to the contract fields:

| Claim part | Evidence in both records | Why it matters |
| --- | --- | --- |
| measurement | `binary_f1_positive_class` | establishes what was calculated |
| scale | `fraction` | makes subtraction meaningful |
| aggregation | `global` | keeps the reduction rule stable |
| population | same SHA-256 identity and `120` rows | establishes who was measured |
| control | decision threshold `0.65` | fixes the classification policy |
| schema | version `1` | establishes the document contract |

Now the strongest supported sentence is:

> On the same identified 120-row evaluation population, under schema version `1` and the
> same `0.65` decision threshold, global positive-class binary F1 increased from `0.7368`
> to `0.7826` on a fraction scale.

Notice what the sentence does **not** claim:

- that the candidate should be released
- that the population represents future production traffic
- that fairness, calibration, latency, or cost stayed acceptable
- that F1 is sufficient for the real decision

Those are separate claims with separate evidence.

## See why the number cannot repair the claim

Compare the accepted candidate with these generated cases:

| Case | DVC reports a delta? | Same metric claim? | Decision |
| --- | --- | --- | --- |
| `comparable-candidate` | yes, `0.0458` | yes | accept the bounded comparison |
| `population-drift` | yes, `0.0458` | no, population identity changed | reject |
| `control-drift` | yes, `0.0458` | no, threshold changed | reject |
| `unit-drift` | yes, `77.5241` | no, fraction became percent | reject |

The first three candidate values are numerically identical. Their review decisions differ
because metric meaning is not stored in the scalar alone.

The unit case is more revealing. A familiar key and a very large positive delta can still
be useless. Subtracting `0.7368` from `78.26` is valid arithmetic and invalid
interpretation because the values use different scales.

```mermaid
flowchart LR
  scalar["numeric delta"] --> mechanics["DVC reports movement"]
  mechanics --> join["join semantic evidence"]
  join --> same["same claim: compare"]
  join --> changed["changed or missing claim: reject or abstain"]
```

The semantic join is not ceremony around the metric. It is the operation that determines
whether the arithmetic answers the review question.

## Metric names are not enough

A metric name can be useful, but it is not a full definition.

`f1_score` may mean:

- binary F1 for the positive class
- macro F1 across several classes
- weighted F1 by support
- F1 after a threshold search
- F1 at a fixed threshold chosen before evaluation

Those are not interchangeable. A stable field name with a drifting definition is a hidden
semantic change.

Prefer names and documentation that make the claim harder to misread:

```json
{
  "incident_escalation": {
    "positive_class_f1_at_fixed_threshold": 0.81,
    "evaluation_population_size": 420
  }
}
```

This still does not prove everything, but it gives reviewers better handles than a lone
`f1_score`.

## What belongs beside a metric

Good metric review usually needs nearby evidence:

- the parameter values that controlled the run
- the evaluation population or dataset identity
- the metric definition or schema
- the output file where the metric was recorded
- the release or review note that says how the metric will be used

This is why Module 05 pairs `metrics.json`, `params.yaml`, `dvc.lock`, and published
release evidence. A metric should not float alone.

## Stability beats cleverness

A less glamorous metric with a stable meaning can be better than a clever metric whose
definition changes every few weeks.

For learning and release review, the first question is not:

> Is this the most advanced possible metric?

The better first question is:

> Can this metric support a fair comparison between the runs we are reviewing?

If the answer is no, the metric may still be useful for exploration, but it is not ready
to carry release authority.

## Review checkpoint

You understand this core when you can take one metric and explain:

- what population it describes
- what unit of analysis it uses
- what definition produced it
- which parameters or thresholds affect it
- what conclusion it can and cannot support
- what evidence a reviewer should inspect beside the metric file

Use `workspace/comparable-candidate/evidence/` to write the complete bounded claim without
copying the sentence above. Then switch only the evidence directory to `population-drift`
and explain exactly which clause becomes unsupported.

The goal is not to distrust every number. It is to make each important number earn the
interpretation attached to it.
