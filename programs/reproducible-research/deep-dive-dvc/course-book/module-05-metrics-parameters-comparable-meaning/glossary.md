# Module Glossary

This glossary belongs to **Module 05: Metrics, Parameters, and Comparable Meaning** in
**Deep Dive DVC**.

Use it to keep the module language stable while you move between the core lessons, the
worked example, the exercises, and capstone review.

## How to use this glossary

Read the directory index first. Return here when a metric review, parameter diff, plot, or
release discussion starts to feel vague.

The goal is not extra theory. The goal is shared language for deciding whether two results
are meaningfully comparable.

## Terms in this directory

| Term | Meaning in this directory |
| --- | --- |
| metric | A recorded value that claims something about workflow behavior on a defined population under defined controls. |
| metric claim | The human interpretation attached to a metric value, including population, definition, and decision context. |
| comparison surface | The set of metrics, parameters, data identity, and review evidence needed to compare two runs fairly. |
| parameter control | A value that influences result behavior or interpretation and should be visible in review. |
| control surface | The parameter values that shape training, evaluation, publishing, or release decisions. |
| metric schema | The structure, names, units, nesting, and missing-value rules of a metric file. |
| schema drift | A change in metric file structure or meaning that can invalidate direct comparison. |
| additive metric change | A new metric or field added while existing metric meanings remain stable. |
| meaning-changing metric change | A metric change that alters definition, population, unit, threshold policy, or review interpretation. |
| population | The examples, records, incidents, or slice being measured by a metric or plot. |
| unit of analysis | The level at which a metric is computed, such as per incident, per customer, per day, or per alert. |
| fixed threshold | A threshold chosen before evaluation and kept stable for comparison. |
| threshold search | A procedure that chooses a threshold during or after evaluation, changing what fixed-threshold metrics can mean. |
| `dvc metrics diff` | A DVC command that reports changed metric values without judging semantic validity. |
| `dvc params diff` | A DVC command that reports changed parameter values that may alter metric interpretation. |
| baseline | The prior state chosen as the comparison reference for a review. |
| release metric | A metric promoted into a release boundary as evidence for downstream readers. |
| plot evidence | A visual artifact used to support a bounded review claim. |
| rendering noise | Plot change caused by unstable rendering, ordering, timestamps, or presentation behavior rather than meaningful data movement. |
| aggregation rule | The rule that combines records into a displayed or reported value, such as binning or averaging. |
| release note | A written review statement that names what changed, what stayed comparable, and what conclusion is justified. |
| semantic validity | The condition where a metric comparison actually supports the human claim being made from it. |

## Stable review questions

Use these questions when the module feels abstract:

- What does this metric claim?
- Which population and unit of analysis does it describe?
- Which parameter values control the comparison?
- Did the metric schema stay stable?
- Does the diff answer the review question being asked?
- Did a plot change because of evidence or rendering noise?
- Is this number ready for release evidence, or only exploratory review?
- What conclusion can be written without overstating the metric movement?
