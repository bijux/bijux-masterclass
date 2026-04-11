# Exercise Answers

These answers are model explanations, not the only acceptable wording.

What matters is whether the reasoning keeps metric meaning, parameter controls, and
comparison evidence connected.

## Answer 1: Explain the metric claim

The metric appears to claim:

- the incident escalation workflow produced a positive-class F1 value of `0.82`
- the metric was computed at a fixed threshold
- the evaluation population contained `420` records

Additional meaning a reviewer still needs:

- which population those 420 records represent
- which class is the positive class
- what fixed threshold was used
- whether the F1 definition is binary, macro, weighted, or something else
- which model and parameter values produced the metric

Why population size is useful but not enough:

- it helps catch obvious population movement
- it does not prove the same records, label rules, or slice definitions were used

The main lesson is that the metric file gives handles for review, not complete meaning by
itself.

## Answer 2: Classify parameter controls

Likely comparison controls:

- `fit.model_family`, because it changes the model being compared
- `fit.random_seed`, because it can affect repeatability and learned output
- `evaluate.threshold`, because it changes metric interpretation
- `evaluate.minimum_population_size`, because it affects whether evaluation is valid

Probably not part of the comparison surface:

- `plot.title`, unless release policy or downstream automation depends on it
- `tmp.file_suffix`, because it sounds like temporary implementation plumbing

The main lesson is to ask whether a value changes the result, comparison, or release
judgment. Important controls belong in review; harmless plumbing should not turn
`params.yaml` into noise.

## Answer 3: Diagnose schema drift

Strong review note:

> This is a meaning-changing schema change, not a simple improvement. The previous metric
> was positive-class F1 at a fixed threshold. The new metric is macro F1 after threshold
> search. The new value may be useful, but it should not be read as an increase from
> `0.81` to `0.84` for the same metric. The review should either keep the old metric for
> continuity or clearly mark this as a new comparison contract.

This is not merely additive because the old key disappeared and the metric definition
changed.

## Answer 4: Interpret metric and parameter diffs

Strong interpretation:

> Fixed-threshold F1 increased from `0.81` to `0.84`, but the evaluation threshold changed
> from `0.65` to `0.50`. That means the comparison is not a same-threshold model
> improvement claim. It may support a threshold-policy review or a combined model-control
> comparison, but the conclusion must state that the control surface changed.

The main lesson is that parameter diff changes what metric diff can mean.

## Answer 5: Review a plot for release evidence

Evidence to check before trusting the plot:

- the same evaluation population or a clearly documented population change
- the same aggregation or binning rule
- deterministic sorting and rendering choices
- whether the plot supports or complicates the scalar metric movement
- whether the plot speaks to the actual release decision

Responsible release sentence:

> The calibration plot uses the same evaluation population and binning rule as the prior
> release, and it supports the fixed-threshold metric movement without replacing the
> precision-recall tradeoff review.

The main lesson is that a plot should support a bounded claim. It should not be treated as
visual authority by itself.

## Self-check

If your answers consistently explain:

- what a metric claims
- which controls change the comparison
- whether schema movement preserves meaning
- what DVC diffs show without proving
- how plots and release notes should bound interpretation

then you are using Module 05 correctly.
