<a id="top"></a>

# Pressure Routes


<!-- page-maps:start -->
## Guide Fit

```mermaid
flowchart TD
  family["Reproducible Research"] --> program["Deep Dive Snakemake"]
  program --> pressure["A concrete learner or reviewer question"]
  pressure --> guide["Pressure Routes"]
  guide --> next["Modules, capstone, and reference surfaces"]
```

```mermaid
flowchart TD
  question["Name the exact question you need answered"] --> skim["Skim only the sections that match that pressure"]
  skim --> crosscheck["Open the linked module, proof surface, or capstone route"]
  crosscheck --> next_move["Leave with one next decision, page, or command"]
```
<!-- page-maps:end -->

Read the first diagram as a timing map: this guide is for a named pressure, not for wandering the whole course-book. Read the second diagram as the guide loop: arrive with a concrete question, use only the matching sections, then leave with one smaller and more honest next move.

This page fixes a human problem, not a technical one: learners do not always arrive with
the calm, ideal “read everything in order” mindset. Sometimes they are new. Sometimes
they are debugging a fragile workflow. Sometimes they are reviewing a repository that
other people already depend on.

Use this page when your pressure is shaping what you can realistically read.

---

## Four Common Pressures

| Pressure | What you need first | Best route |
| --- | --- | --- |
| first contact | a safe mental model and low cognitive load | `start-here` -> Module 00 -> Modules 01-02 -> `capstone-walkthrough` |
| inherited workflow repair | fast diagnosis and high-value repairs | Module 03 -> Module 04 -> Module 08 -> `capstone-tour` |
| publish and stewardship review | downstream trust, architecture, and migration judgment | Module 06 -> Module 07 -> Module 10 -> `proof` |
| incident pressure | quickest route from symptom to owning boundary | Module 09 -> `incident-review-guide` -> `proof` |

[Back to top](#top)

---

## Route Details

### First Contact

Use this when Snakemake still feels foreign.

1. [`start-here.md`](start-here.md)
2. [`module-00-orientation/index.md`](../module-00-orientation/index.md)
3. Modules 01 and 02
4. [`module-checkpoints.md`](module-checkpoints.md)
5. [`capstone-walkthrough.md`](capstone-walkthrough.md)

### Inherited Workflow Repair

Use this when you already have a workflow that runs but is hard to trust.

1. [`anti-pattern-atlas.md`](../reference/anti-pattern-atlas.md)
2. Module 03
3. Module 04
4. Module 08
5. [`capstone-map.md`](capstone-map.md)

### Publish And Stewardship Review

Use this when the concern is downstream trust and long-lived workflow ownership.

1. Module 06
2. Module 07
3. Module 10
4. [`proof-ladder.md`](proof-ladder.md), then `capstone-confirm`

### Incident Pressure

Use this when the workflow already failed and you need the shortest route to responsible diagnosis.

1. [`incident-review-guide.md`](incident-review-guide.md)
2. Module 09
3. [`command-guide.md`](command-guide.md)
4. [`capstone-map.md`](capstone-map.md)
5. `proof`

[Back to top](#top)

---

## Pressure Mistakes This Page Prevents

This page exists to prevent these clumsy reading mistakes:

* starting in Module 07 when the real problem is still file-contract truth
* using the capstone as first exposure during panic
* reading every support page when one pressure-specific route would do
* treating governance pages as a substitute for repair knowledge

[Back to top](#top)

---

## Best Companion Pages

Use these with the pressure routes:

* [`course-guide.md`](course-guide.md) for the stable support hub
* [`module-promise-map.md`](module-promise-map.md) to keep titles honest
* [`proof-ladder.md`](proof-ladder.md) to size proof correctly
* [`topic-boundaries.md`](../reference/topic-boundaries.md) to know what the course does and does not center

[Back to top](#top)
