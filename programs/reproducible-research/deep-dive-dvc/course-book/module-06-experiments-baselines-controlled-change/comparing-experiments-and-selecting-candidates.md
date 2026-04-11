# Comparing Experiments and Selecting Candidates

Experiment comparison is not a leaderboard ritual.

The candidate with the highest single metric is not automatically the candidate that
should move forward. A good comparison asks whether the candidate is comparable, what
tradeoff it makes, and whether the result supports the intent that created it.

## Start with comparability

Before ranking candidates, ask whether they can be compared.

Useful checks:

- same baseline or an explicitly named baseline change
- same evaluation population
- same metric definitions
- declared parameter changes
- no hidden data or environment drift
- no unrelated pipeline change mixed into the candidate

If these checks fail, the right next step is not to pick a winner. It is to repair the
comparison story.

## Compare the whole review surface

A candidate can improve one metric and make another worse.

Example:

```text
baseline:
  threshold: 0.65
  f1: 0.81
  precision: 0.78
  recall: 0.84

candidate:
  threshold: 0.50
  f1: 0.84
  precision: 0.75
  recall: 0.95
```

This is not simply "better." It is a threshold tradeoff.

If the release goal is to reduce missed escalations, the candidate may be promising. If
the release goal is to avoid false alarms, it may be unacceptable. The metric values do
not decide without the review objective.

## Use candidate tables carefully

Candidate tables are helpful when they do not hide meaning.

```text
candidate                         threshold    f1     precision    recall    review note
baseline                          0.65         0.81   0.78         0.84      current release
lower-threshold-for-recall        0.50         0.84   0.75         0.95      recall gain, precision cost
stricter-threshold-for-precision  0.75         0.77   0.86         0.68      precision gain, recall cost
```

This table is useful because it shows the control that moved and the tradeoff, not only a
ranked metric.

Weak table:

```text
candidate    f1
a            0.84
b            0.81
c            0.77
```

That table invites a winner without explaining what changed.

## Selection is a decision, not a discovery

The review should distinguish:

- observed metric movement
- parameter or data changes that explain the movement
- known tradeoffs
- release objective
- reason to keep, discard, or promote the candidate

A strong candidate note might say:

> Keep `lower-threshold-for-recall` for promotion review because it improves recall from
> `0.84` to `0.95` on the same evaluation population, with an expected precision drop from
> `0.78` to `0.75`. This matches the current release objective only if the precision cost
> remains acceptable.

That is a decision argument. It is stronger than "best F1."

## Treat inconclusive runs honestly

Not every candidate needs to be promoted or fully explained.

Some runs are inconclusive:

- metric movement is within expected noise
- tradeoff does not match the release objective
- comparability evidence is incomplete
- output changed but the reason is unclear
- candidate combined too many changes to interpret

Inconclusive is a valid outcome. The bad outcome is pretending uncertainty is a win.

## Review checkpoint

You understand this core when you can:

- check comparability before ranking candidates
- compare metrics with parameters and review intent
- explain tradeoffs instead of naming only the highest metric
- identify inconclusive candidates
- write a selection note that another reviewer can challenge

Candidate selection is where experiments become engineering judgment instead of metric
shopping.
