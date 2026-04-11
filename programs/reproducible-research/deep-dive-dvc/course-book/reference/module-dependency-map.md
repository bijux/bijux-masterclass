# Module Dependency Map


<!-- page-maps:start -->
## Reference Position

```mermaid
flowchart TD
  family["Reproducible Research"] --> program["Deep Dive DVC"]
  program --> reference["Module Dependency Map"]
  reference --> review["Design or review decision"]
  review --> capstone["Capstone proof surface"]
```

```mermaid
flowchart TD
  trigger["Hit a naming, boundary, or trade-off question"] --> lookup["Use this page as a glossary, map, rubric, or atlas"]
  lookup --> compare["Compare the current code or workflow against the boundary"]
  compare --> decision["Turn the comparison into a keep, change, or reject call"]
```
<!-- page-maps:end -->

Read the first diagram as a lookup map: this page is part of the review shelf, not a first-read narrative. Read the second diagram as the reference rhythm: arrive with a concrete ambiguity, compare the current work against the boundary on the page, then turn that comparison into a decision.

Deep Dive DVC is not ten independent essays. Later modules assume earlier state concepts,
and the course becomes much easier when that dependency shape is explicit.

---

## The Main Sequence

```mermaid
graph TD
  m01["01 Why Reproducibility Fails"]
  m02["02 Data Identity"]
  m03["03 Environments as Inputs"]
  m04["04 Truthful DAGs"]
  m05["05 Metrics and Parameters"]
  m06["06 Experiments"]
  m07["07 Collaboration and CI"]
  m08["08 Incident Survival"]
  m09["09 Promotion and Auditability"]
  m10["10 Mastery"]

  m01 --> m02 --> m03 --> m04 --> m05 --> m06
  m05 --> m07 --> m08 --> m09 --> m10
  m06 --> m09
  m07 --> m10
  m08 --> m10
```

---

## Why The Sequence Looks Like This

| Module | Depends most on | Reason |
| --- | --- | --- |
| 01 | none | it defines the reproducibility problem precisely |
| 02 | 01 | state identity is the first real repair boundary |
| 03 | 01-02 | environments only make sense once data identity is stable |
| 04 | 02-03 | truthful pipelines require stable inputs and explicit environment boundaries |
| 05 | 04 | params and metrics only matter if the pipeline contract is honest |
| 06 | 04-05 | experiments depend on a trustworthy baseline and comparison surface |
| 07 | 04-06 | social rules need a technical contract worth defending |
| 08 | 02-07 | durability depends on state identity, remotes, and human process |
| 09 | 05-08 | promotion requires comparable state plus long-lived trust |
| 10 | all earlier modules | stewardship judgment requires the whole model |

---

## Fastest Safe Paths

### First pass through the course

Read Modules 01 through 10 in order.

### Working maintainer

Start with Modules 04, 07, 08, and 09, then backfill earlier modules when you find a gap
in your state model.

### Reproducibility steward

Start with Modules 05, 08, 09, and 10, then revisit earlier modules when a boundary
question points back to fundamentals.

---

## Where The Capstone Helps Most

| Stage | Best capstone use |
| --- | --- |
| after 02 | inspect state layers, lockfiles, and publish boundaries |
| after 04-05 | inspect truthful stages, params, and metrics |
| after 06-08 | inspect experiment, collaboration, and recovery surfaces |
| after 09-10 | review the repository as a stewardship specimen |
