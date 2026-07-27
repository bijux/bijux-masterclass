# Exercise Answers


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive DVC"]
  section["Metrics Parameters Comparable Meaning"]
  page["Exercise Answers"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  claim["name the metric claim"] --> control["separate semantic controls"]
  control --> compare["test whether runs are comparable"]
  compare --> decide["write a bounded decision rule"]
  decide --> packet["assemble a reviewable comparison packet"]
```
<!-- page-maps:end -->

These answers are model explanations, not the only acceptable wording.

## How to use the answer page well

Do not read the model answer first and then collapse every comparison back into "the
score went up."

A better rhythm is:

1. finish the exercise with your own comparison packet
2. name the claim, metric definition, population, and nearby controls
3. compare your reasoning with the model answer
4. revise anywhere your answer skips schema continuity, parameter meaning, or bounded
   interpretation

What matters is whether the reasoning keeps metric meaning, parameter controls, and
decision discipline connected.

Strong Module 05 answers usually do five things:

- they say what the metric actually claims
- they identify which controls change the meaning of the comparison
- they detect schema changes before reading score movement as improvement
- they treat plots as supporting evidence, not visual authority
- they predeclare decision rules instead of improvising them after the run

The strongest self-study packets also leave behind six concrete artifacts:

- one metric claim explanation
- one control-classification table
- one schema continuity judgment
- one manual recomputation
- one decision rule
- one independent-review packet

If your answers rely only on "higher is better," the reasoning is still too thin.

## Answer 1: Explain the metric claim

The metric appears to claim:

- the incident escalation workflow produced a positive-class F1 value of `0.82`
- the metric was computed at a fixed threshold
- the evaluation population contained `420` records

Additional meaning a reviewer still needs:

- which records those `420` cases represent
- which class counts as positive
- what fixed threshold was used
- whether the F1 definition is binary, macro, or something else
- which model, data identity, and parameter values produced the metric

Why population size is useful but not enough:

- it helps catch obvious population movement
- it does not prove the same records, labels, split logic, or metric definition were used

A bounded release question this metric could support is:

> Does the current candidate maintain acceptable positive-class escalation quality under
> the declared threshold policy for the governed evaluation population?

## Answer 2: Classify parameter controls

Likely comparison controls:

- `fit.model_family`
- `fit.random_seed`
- `evaluate.threshold`
- `evaluate.minimum_population_size`

Probably not part of the semantic comparison surface:

- `plot.title`
- `tmp.file_suffix`

Why:

- the first four can alter learned behavior, evaluation meaning, or whether the result is
  valid for review
- the last two usually affect presentation or temporary plumbing rather than semantic
  interpretation

One edge case:

- a cosmetic field becomes semantically important if downstream automation or published
  consumer contracts depend on it as an identifier rather than as mere decoration

## Answer 3: Diagnose schema drift

Strong review note:

> This is a meaning-changing schema change, not a simple improvement. The previous metric
> was positive-class F1 at a fixed threshold. The new metric is macro F1 after threshold
> search. The new value may be useful, but it should not be read as an increase from
> `0.81` to `0.84` for the same metric. The review should either keep the old metric for
> continuity or clearly mark the new metric as a new comparison contract.

What the team should preserve for continuity:

- the prior metric key and definition, or an explicit compatibility policy that states how
  the new schema relates to the old one

## Answer 4: Interpret metric and parameter diffs

Strong interpretation:

> Fixed-threshold F1 increased from `0.81` to `0.84`, but the evaluation threshold also
> changed from `0.65` to `0.50`. That means this is not a same-threshold model
> improvement claim. It may support a threshold-policy review or a combined-control
> comparison, but the conclusion must state that the evaluation rule changed with the
> metric.

One conclusion that would be too strong:

- "The model improved by three F1 points under the same evaluation conditions."

The main lesson is that parameter movement changes what the metric movement can mean.

## Answer 5: Review a plot for release evidence

Before trusting the plot, check:

- whether it uses the same evaluation population or a clearly documented new one
- whether binning or aggregation rules stayed stable
- whether sorting and rendering are deterministic enough for review
- whether the shape supports or contradicts the scalar metric movement
- whether the plot speaks to the actual release decision rather than only looking cleaner

Responsible release sentence:

> The calibration plot uses the same governed population and binning rule as the prior
> comparison and supports the fixed-threshold review, but it does not replace the scalar
> metric and threshold-policy decision.

## Answer 6: Predict the metric contract audit

Expected classifications:

| Case | Metric delta | Parameter diff | Semantic boundary | Decision |
| --- | ---: | --- | --- | --- |
| comparable candidate | `0.0458` | empty | none of the required fields change | `ACCEPT` |
| additive metric | `0.0458` | empty | new metric key only | `ACCEPT` |
| population drift | `0.0458` | empty | population identity changes | `REJECT` |
| unit drift | `77.5241` | empty | fraction becomes percent | `REJECT` |
| control drift | `0.0458` | threshold `0.65 -> 0.50` | evaluation rule changes | `REJECT` |
| schema-version drift | `0.0458` | empty | version `1 -> 2` | `REJECT` |
| missing population identity | `0.0458` | empty | required identity disappears | `ABSTAIN` |

The audit summary represents abstention as `REJECT` because the comparison gate is
closed. The review explanation should preserve the reason: incompatibility is observed in
drift cases; compatibility is unknown when evidence is missing.

`PASS / REJECT` means the audit successfully reproduced a defect that a direct metric
comparison must reject. `PASS` evaluates the audit observation. `REJECT` evaluates the
candidate comparison.

## Answer 7: Reconstruct and recompute the accepted claim

Baseline confusion matrix:

```text
TP = 42
FP = 12
FN = 18
TN = 48
```

Baseline calculations:

```text
precision = 42 / (42 + 12) = 42 / 54 = 0.7778
recall    = 42 / (42 + 18) = 42 / 60 = 0.7000
F1        = 2 * 0.777777... * 0.7 / (0.777777... + 0.7)
          = 0.7368
```

Candidate confusion matrix:

```text
TP = 45
FP = 10
FN = 15
TN = 50
```

Candidate calculations:

```text
precision = 45 / (45 + 10) = 45 / 55 = 0.8182
recall    = 45 / (45 + 15) = 45 / 60 = 0.7500
F1        = 2 * 0.818181... * 0.75 / (0.818181... + 0.75)
          = 0.7826
```

Using the rounded values recorded by the specimen:

```text
delta = 0.7826 - 0.7368 = 0.0458
```

Bounded claim:

> On the same identified 120-row population, under schema version `1`, threshold `0.65`,
> fraction units, and global positive-class binary F1, the candidate increased from
> `0.7368` to `0.7826`.

This does not establish representativeness, fairness, calibration, operational cost, or a
release decision. Those claims are outside the packet.

## Answer 8: Defeat two plausible shortcuts

### Equal row counts

Tempting evidence:

- baseline and candidate both report `rows: 120`
- DVC reports a `0.0458` increase

Defeating evidence:

- baseline population starts `sha256:8d4935...`
- candidate population starts `sha256:ae27d8...`

Safe note:

> The metric increased mechanically, but equal population counts do not establish equal
> population identity. Reject the same-population claim.

Repair:

- evaluate on the governed baseline population, or establish and document a new baseline
  for the changed population

### Stable metric key

Tempting evidence:

- both records use `positive_class_f1_at_fixed_threshold`
- DVC reports a positive `77.5241` delta

Defeating evidence:

- baseline unit is `fraction`
- candidate unit is `percent`

Safe note:

> The metric path is stable, but the values use incompatible scales. The reported
> subtraction cannot support an improvement claim.

Repair:

- normalize both records to one declared unit and regenerate the comparison, or establish
  a new baseline

DVC reports both deltas because its job is to compare recorded numeric values. Population
identity and unit compatibility belong to the semantic review.

## Answer 9: Separate policy change, schema evolution, and missing evidence

| Case | Classification | Reason | Next action |
| --- | --- | --- | --- |
| control drift | useful result answering a different policy question | threshold changes to `0.50` | review threshold-specific precision and recall, or rerun at `0.65` |
| additive metric | compatible extension | primary contract remains stable; false-positive rate is added | compare prior F1 and begin new history for FPR |
| schema-version drift | incompatible direct comparison | version changes without a compatibility mapping | provide a reviewed mapping or establish a new baseline |
| missing population identity | abstention | continuity cannot be established from row count | restore governed population identity |

The control-drift result can answer:

> What classification tradeoff results from lowering the decision threshold from `0.65`
> to `0.50`?

It cannot answer:

> Did the candidate improve under the threshold already in force?

The additive rule is:

> Existing metrics remain comparable only when their complete contracts remain unchanged;
> each added metric begins its own history.

## Answer 10: Produce an independent comparison review

One specimen-level rule, written before selecting a case, could be:

```text
Accept a candidate for the exercise only when:
1. F1 improves by at least 0.03.
2. Precision does not decrease by more than 0.01.
3. Recall does not decrease.
4. Population identity, schema version, threshold, definition, unit, and aggregation match.
5. Missing required evidence causes abstention.
```

The comparable candidate passes this exercise rule:

- F1 delta is `+0.0458`
- precision changes from `0.7778` to `0.8182`
- recall changes from `0.7000` to `0.7500`
- semantic contract checks pass

The additive candidate also preserves the primary contract and values, so the same F1
judgment applies while the new false-positive-rate metric begins separate history.

The other cases cannot enter the rule as direct comparisons:

- population, unit, control, and schema-version drift violate continuity
- missing population identity forces abstention

An independent reviewer should be able to decide those points from relative paths in the
packet. The packet still cannot authorize a real release because its exercise rule does
not include domain-specific fairness, calibration, latency, cost, or population
representativeness evidence.

## Self-check

If your answers consistently explain:

- what a metric claims
- which controls change the comparison
- whether schema movement preserves meaning
- what DVC diffs show without proving
- how plots and release notes should bound interpretation

then you are using Module 05 correctly.
