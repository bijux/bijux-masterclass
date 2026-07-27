# Experiment Scope and Change Boundaries


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive DVC"]
  section["Experiments Baselines Controlled Change"]
  page["Experiment Scope and Change Boundaries"]
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

An experiment should be different enough to teach something and narrow enough to review.

That balance is the scope problem.

If a candidate run changes one threshold, the review can ask whether the threshold tradeoff
is worth it. If it changes threshold, model family, feature filtering, evaluation
population, and metric definition at once, the review may only know that "something
changed."

Module 06 treats scope as part of experiment quality.

## One question per candidate is a useful default

A good candidate often starts with one review question:

- What happens if the escalation threshold moves from `0.65` to `0.50`?
- Does a tree-based model improve recall compared with the baseline model?
- Does adding the incident age feature help the same evaluation population?
- Does a stricter minimum population size make the release metric more stable?

The question keeps the candidate from absorbing every interesting idea at once.

It also makes the result easier to reject. If the threshold change improves recall but
hurts precision too much, the team can discard that candidate without wondering whether
some unrelated model change caused the tradeoff.

## Controlled change belongs in declared surfaces

Controlled changes should appear where the course has already taught you to look:

- parameter changes in `params.yaml`
- pipeline changes in `dvc.yaml`
- metric changes in metric files and review notes
- data identity changes in DVC-tracked state
- environment changes in environment evidence

Example candidate:

```yaml
evaluate:
  threshold: 0.50
```

This is reviewable if the baseline had:

```yaml
evaluate:
  threshold: 0.65
```

The change is visible, comparable, and easy to explain.

Declaration is necessary, but it is not sufficient. A changed value can be:

- declared by the pipeline
- visible in the experiment diff
- reproducible on another machine
- unrelated to the candidate's stated question

That last condition still breaks attribution.

## Declared is not the same as allowed

The experiment contract separates the full parameter surface from the candidate's allowed
change set.

Baseline parameters:

```json
{
  "decision": {"threshold": 0.65},
  "evaluation": {
    "population_id": "incident-review-v1",
    "metric_schema": "classification-v1"
  }
}
```

Candidate permission:

```json
{
  "allowed_changes": ["decision.threshold"],
  "target_threshold": 0.5
}
```

The audit computes the actual changed paths and requires an exact match with
`allowed_changes`. Exactness matters:

- no changed path means the intervention did not happen
- a missing allowed path means the candidate is incomplete
- an extra path means the candidate exceeds its question

`MIXED_CONTROL_CHANGE` changes both `decision.threshold` and
`decision.review_capacity`. Both values are visible. Only one belongs to the intent, so
the audit returns `BLOCK_COMPARISON`.

## Classify changes by their effect on the claim

Do not rely on a fixed rule that every candidate must change exactly one file. Instead,
classify the semantic role of each change.

| Change role | Example | Treatment |
| --- | --- | --- |
| intervention | lower `decision.threshold` | allowed candidate change |
| required consequence | updated metrics and lockfile | expected output evidence |
| comparison control | population ID, metric schema | must remain stable |
| implementation support | code needed solely to express the intervention | review for inseparability |
| unrelated policy change | change review capacity | split into another candidate |
| baseline repair | correct mislabeled evaluation rows | establish a new baseline |

A candidate can legitimately touch several files when those files express one intervention
and its consequences. “One question” is a semantic boundary, not a file-count limit.

## Use the diff to test the question

After a run, ask the diff three questions:

1. Which changed paths express the planned intervention?
2. Which changed files are deterministic consequences?
3. Which changes belong to neither category?

For the controlled specimen, the answer should be:

```text
planned intervention:
  decision.threshold: 0.65 -> 0.50

deterministic consequences:
  metrics/metrics.json
  dvc.lock

unrelated changes:
  none
```

If `evaluation.metric_schema` appears, do not explain it away because the run succeeded.
That path changes what the result means.

Weak candidate:

```text
Changed the threshold in Python, tried a different split file, and copied a notebook
result into the report.
```

This is not controlled exploration. It is a lineage gap.

## Separate experiment change from baseline boundary work

Some changes are too structural to hide inside an ordinary candidate comparison.

Examples:

- changing the evaluation population definition
- replacing the metric definition
- changing the pipeline graph so outputs no longer mean the same thing
- fixing a data quality bug that invalidates earlier metrics
- changing the runtime strategy in a way that affects results

Those changes may be necessary. But they should be reviewed as boundary changes before
candidate ranking.

The generated `POPULATION_DRIFT` case makes this concrete. Its declared threshold change
is correct, and the experiment runs. One additional incident record changes:

- record count
- record identity digest
- observed metric values

The candidate must not be ranked against the baseline because the cohort changed beneath
the question.

The safer order is:

1. repair or redefine the baseline boundary
2. record the new baseline evidence
3. run candidates against the new baseline

This avoids pretending that two incomparable states are ordinary experiment alternatives.

## Bundle related changes only when the story is explicit

Sometimes a candidate needs more than one changed value.

Example:

```yaml
fit:
  model_family: tree_boosting
  max_depth: 4
  random_seed: 20260411
```

Those values can belong together because `max_depth` is part of testing that model family.
The review note should say that the candidate evaluates a tree-boosting configuration, not
just "a parameter tweak."

The key is that the bundle has one story.

Use a bundle test before accepting multiple changes:

| Question | If the answer is no |
| --- | --- |
| Would removing any changed control make the intervention incomplete? | split the candidate |
| Do all changed controls serve the same causal question? | split the candidate |
| Are comparison controls unchanged? | establish a new baseline |
| Can a reviewer predict the intended changed paths before seeing the diff? | rewrite the intent |
| Can one promotion decision accept or reject the bundle coherently? | separate the decisions |

This test avoids two unhelpful extremes: one candidate per line, and one candidate per
brainstorm.

Weak bundle:

```yaml
fit:
  model_family: tree_boosting
evaluate:
  threshold: 0.50
data:
  include_weekends: false
```

This might be valid if the review question is a full policy proposal. It is not a clean
model-family comparison.

## A scope review table

| Change | Usually safe in one candidate? | Review concern |
| --- | --- | --- |
| one evaluation threshold | yes | compare precision-recall tradeoff |
| model family plus model-specific hyperparameters | yes, if named clearly | compare model configuration, not one isolated value |
| threshold plus evaluation population change | usually no | metric meaning may change |
| metric definition replacement | usually no | baseline may need redefinition |
| data correction that invalidates old metrics | no | new baseline evidence needed |
| plot styling only | usually not an experiment | may be documentation or report cleanup |

Use the table to slow down, not to avoid judgment.

## Turn the scope review into evidence

Extend the table with an evidence column when reviewing a real candidate:

| Changed path | Role | Allowed? | Evidence |
| --- | --- | --- | --- |
| `decision.threshold` | intervention | yes | candidate params and experiment diff |
| `metrics/metrics.json` | consequence | yes | candidate metric record |
| `evaluation.population_id` | comparison control | no | baseline and candidate population records |
| `decision.review_capacity` | unrelated policy | no | changed-path audit |

The table forces a reason for each change. “DVC recorded it” is evidence of visibility,
not a reason for inclusion.

Run:

```bash
make -C programs/reproducible-research/deep-dive-dvc/capstone experiment-comparability-audit
```

Compare `CONTROLLED_THRESHOLD` with `MIXED_CONTROL_CHANGE` in `summary.tsv`, then open
each `candidate-params.json` and `finding.json`. The difference is not whether DVC can
execute them. It is whether the actual changed paths still match the predeclared question.

## Review checkpoint

You understand this core when you can:

- state the review question for one candidate run
- name the declared surface where each change belongs
- distinguish ordinary candidate variation from baseline boundary work
- explain when a bundle of changes has one coherent story
- reject candidates that are too mixed to interpret
- explain why a declared extra control can still invalidate attribution
- classify intervention, consequence, control, support, and unrelated changes

Experiment scope is what keeps exploration from becoming folklore with metric files.
