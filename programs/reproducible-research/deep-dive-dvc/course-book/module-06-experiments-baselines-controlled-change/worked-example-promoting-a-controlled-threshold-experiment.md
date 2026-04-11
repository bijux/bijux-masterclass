# Worked Example: Promoting a Controlled Threshold Experiment

This example shows how Module 06 fits together when a candidate run looks promising but
still needs a promotion decision.

The goal is not to promote the best-looking number. The goal is to decide whether the
candidate should become part of history.

## The situation

The current baseline says:

```yaml
evaluate:
  threshold: 0.65
```

and reports:

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

The release objective is to reduce missed escalations, even if precision drops slightly.

You write the candidate intent before running it:

> Lower `evaluate.threshold` to `0.50` to test whether recall improves enough to justify a
> precision tradeoff.

That sentence keeps the candidate narrow.

## Step 1: Run a declared candidate

You run a candidate by changing the declared control:

```bash
dvc exp run --set-param evaluate.threshold=0.50
```

The important part is not the exact command syntax. The important part is that the
threshold change is visible in the parameter surface.

This is better than editing a Python literal and hoping everyone remembers what changed.

## Step 2: Compare against the baseline

The candidate reports:

```json
{
  "incident_escalation": {
    "positive_class_f1_at_fixed_threshold": 0.84,
    "precision_at_fixed_threshold": 0.75,
    "recall_at_fixed_threshold": 0.95,
    "evaluation_population_size": 420
  }
}
```

You compare the whole review surface:

```text
baseline threshold: 0.65
candidate threshold: 0.50

f1:        0.81 -> 0.84
precision: 0.78 -> 0.75
recall:    0.84 -> 0.95
population size: 420 -> 420
```

This is not a generic model improvement. It is a threshold tradeoff: recall improves,
precision decreases, and the population size appears stable.

## Step 3: Check scope

You confirm:

- no model family change
- no evaluation population change
- no metric key change
- no unrelated workspace edits
- only the threshold control moved

That gives the candidate a coherent story.

If you had also changed feature filtering and metric definition, the candidate
would not be a clean threshold experiment anymore. It might still be useful, but it would
need a different review claim.

## Step 4: Decide whether promotion is justified

The release objective favors recall. The candidate improves recall from `0.84` to `0.95`.
Precision drops from `0.78` to `0.75`.

You write a promotion argument:

> Promote the lower-threshold candidate because it substantially reduces missed
> escalations under the same metric schema and apparent population size. The precision
> drop is acceptable for this release objective.

That is a decision, not just a metric observation.

## Step 5: Apply and inspect before committing

You apply the candidate:

```bash
dvc exp apply <candidate-id>
git diff
git status
```

You check that the workspace contains only intended changes:

- `params.yaml` threshold change
- updated metric evidence
- any expected lock or output evidence

If unrelated local files appear, you stop and clean up before committing.

Applying is not promotion by itself. Promotion happens when the reviewed state is committed
with a clear rationale.

## The review note you would want

> Promote the threshold candidate that changes `evaluate.threshold` from `0.65` to `0.50`.
> Compared with the baseline, fixed-threshold F1 moves from `0.81` to `0.84`, recall moves
> from `0.84` to `0.95`, and precision moves from `0.78` to `0.75` on the same reported
> evaluation population size. This is a recall-oriented policy tradeoff, not a pure model
> improvement claim. Promotion is justified only because the current release objective
> prioritizes reducing missed escalations.

That note is strong because it names the control change, metric movement, tradeoff, and
release basis.

## Why this is a mastery example

This one story exercises the whole module:

- Core 1: the baseline anchored the comparison
- Core 2: the candidate stayed scoped to one review question
- Core 3: DVC experiment mechanics preserved a candidate record
- Core 4: selection considered tradeoffs, not only best F1
- Core 5: promotion happened only after applying and inspecting the workspace

The candidate became part of history because the review argument was defensible, not
because the number looked better.
