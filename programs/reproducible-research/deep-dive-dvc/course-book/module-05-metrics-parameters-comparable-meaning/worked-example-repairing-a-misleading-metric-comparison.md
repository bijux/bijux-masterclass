# Worked Example: Repairing a Misleading Metric Comparison


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive DVC"]
  section["Metrics Parameters Comparable Meaning"]
  page["Worked Example: Repairing a Misleading Metric Comparison"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  predict["predict decisions"] --> mechanics["read DVC diffs"]
  mechanics --> contracts["compare semantic contracts"]
  contracts --> classify["accept, reject, or abstain"]
  classify --> communicate["write bounded review notes"]
```
<!-- page-maps:end -->

This example investigates seven candidates whose numeric outputs tempt the same shortcut:

> The score increased, so the candidate improved.

The investigation will accept two comparisons and reject five. The point is not to make
metric review pessimistic. It is to make the evidence say exactly what changed.

## Run the controlled audit

From the repository root:

```bash
make PROGRAM=reproducible-research/deep-dive-dvc capstone-metric-contract-audit
```

The generated packet is:

```text
artifacts/audit/reproducible-research/deep-dive-dvc/metric-contracts/
├── METRIC_CONTRACT_AUDIT_GUIDE.md
├── manifest.json
├── report.json
├── route.txt
├── summary.tsv
└── workspace/
```

Read `route.txt`. Do not begin with `report.json`; the large report is for traceability,
not first contact.

## Predict before reading classifications

The cases all start from this governed baseline:

```text
F1                 0.7368
population rows    120
threshold          0.65
unit               fraction
schema version     1
```

Predict the decision for each change:

| Case | Deliberate change | Your prediction |
| --- | --- | --- |
| comparable candidate | confusion-matrix outcomes | |
| additive metric | new false-positive-rate field | |
| population drift | population identity, not row count | |
| unit drift | fraction to percent | |
| control drift | threshold `0.65` to `0.50` | |
| schema-version drift | version `1` to `2` | |
| missing population identity | identity field removed | |

Use `ACCEPT`, `REJECT`, or `ABSTAIN`. Later, map abstention to the audit gate’s `REJECT`
decision because an incomplete comparison cannot proceed.

## Establish the baseline claim

Open:

```text
workspace/comparable-candidate/evidence/baseline-metrics.json
```

Reconstruct the claim from the document:

> On population
> `sha256:8d493546a9f0a84d7c18480c35761ed99f491fa79c8125eea415d6709fc519b3`,
> containing 120 rows, at threshold `0.65`, global positive-class binary F1 under schema
> version `1` was `0.7368` on a fraction scale.

That sentence is the comparison reference. Every candidate must preserve its semantic
clauses before its value can enter the same series.

## Investigate the comparable candidate

Read:

```text
workspace/comparable-candidate/evidence/dvc-metrics-diff.json
workspace/comparable-candidate/evidence/dvc-params-diff.json
```

DVC reports:

```text
0.7368 -> 0.7826
delta = 0.0458
```

The parameter diff is empty. Now compare `baseline-metrics.json` with
`candidate-metrics.json`.

All semantic clauses match:

- population identity and row count
- threshold
- schema version
- metric name and definition
- unit and aggregation

Read `comparison.json` only after making that inspection. It records `ACCEPT`.

Write:

> Under the same recorded metric contract, F1 increased by `0.0458`.

Do not write:

> Release the candidate.

Comparability passed. Release sufficiency and safeguards remain open.

## Test the equal-count shortcut

Open the population-drift evidence.

The DVC metric diff again reports `0.0458`. Both populations contain `120` rows. The
identities differ:

```text
baseline  sha256:8d4935...
candidate sha256:ae27d8...
```

Equal counts establish only equal cardinality. They do not establish equal members,
labels, selection policy, or difficulty.

Write:

> F1 increased mechanically, but the evaluation population identity changed. The result
> cannot support a same-population improvement claim.

The repair is not to add more decimals. The repair is either to restore the governed
population or establish a new baseline and explain the new population.

## Join the control diff

Open the control-drift receipts.

The metric delta remains `0.0458`. The parameter receipt reports:

```text
decision.threshold  0.65 -> 0.50
```

The candidate may answer a useful question about threshold policy. It does not answer:

> Did predictions improve under the threshold already in force?

Write:

> F1 increased while the threshold changed. Review this as a threshold-policy candidate,
> not a same-threshold model improvement.

The repair depends on intent:

- rerun at `0.65` for a same-control comparison
- retain `0.50` and review precision-recall safeguards for a policy investigation

## Catch the largest false improvement

Open the unit-drift case.

The primary path is unchanged, and DVC reports:

```text
0.7368 -> 78.26
delta = 77.5241
```

The candidate changed `fraction` to `percent`.

This is the most visually impressive delta in the packet and the least defensible
improvement claim. The arithmetic is correct; the operands are on different scales.

Write:

> The primary key is stable but the unit changed. Normalize both values under one declared
> scale or establish a new contract before comparing.

Stable names are useful routing aids. They are not semantic proof.

## Separate additive evolution from breakage

The additive candidate introduces:

```text
false_positive_rate_at_fixed_threshold
```

and preserves the complete primary F1 contract. Existing F1 history remains comparable;
the new metric begins its own history.

The schema-version candidate changes version `1` to `2` without a compatibility mapping.
Its F1 delta is blocked even though other fields match.

Write two distinct notes:

> The new false-positive-rate field is additive. Existing F1 meaning is preserved.

> Schema version changed without a reviewed compatibility mapping. Direct historical F1
> comparison is blocked.

Do not classify every schema change as breaking. Do not classify every parseable change
as additive.

## Abstain when evidence is missing

The final candidate keeps `rows: 120` and removes population identity.

No evidence demonstrates that the population changed. No evidence demonstrates that it
stayed the same either.

Write:

> Population continuity cannot be established from row count alone. Abstain until identity
> evidence is restored.

This is different from population drift:

- drift evidence proves incompatibility
- missing evidence prevents judgment

Both map to a closed comparison gate.

## Assemble the review packet

Your final packet should contain:

1. the baseline claim
2. a table of all seven predicted and observed decisions
3. the metric and parameter diff for each reviewed candidate
4. the semantic field that permits or blocks comparison
5. one bounded note per case
6. the additional release evidence still needed for accepted comparisons

Use this summary shape:

| Case | Numeric delta | Semantic boundary | Decision | Repair or next review |
| --- | ---: | --- | --- | --- |
| comparable candidate | `0.0458` | contract preserved | accept | apply release policy |
| additive metric | `0.0458` | primary preserved | accept | begin history for new metric |
| population drift | `0.0458` | identity changed | reject | restore population or rebaseline |
| unit drift | `77.5241` | unit changed | reject | normalize or rebaseline |
| control drift | `0.0458` | threshold changed | reject direct claim | rerun or review policy |
| schema-version drift | `0.0458` | version changed | reject | provide mapping or rebaseline |
| missing population identity | `0.0458` | evidence absent | abstain | restore identity evidence |

## Why this is a mastery example

The example requires four separate judgments:

- DVC mechanics: what values and parameters moved?
- contract continuity: are both records measurements of the same claim?
- evidence sufficiency: can continuity be established?
- release authority: is an accepted movement enough to promote?

If those judgments stay separate, metric diffs become useful evidence rather than
scoreboards.
