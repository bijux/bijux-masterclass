# Course Guide


<!-- page-maps:start -->
## Guide Fit

```mermaid
flowchart TD
  family["Python Programming"] --> program["Python Functional Programming"]
  program --> pressure["A concrete learner or reviewer question"]
  pressure --> guide["Course Guide"]
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

This guide explains how the course is shaped and why the sequence matters. The course is
not a pile of functional programming topics. It is a route from local reasoning to
systems that remain testable and reviewable under operational pressure.

## Course Spine

The course has four linked layers:

1. entry pages and orientation
2. module work from purity to sustainment
3. capstone proof in one executable repository
4. review surfaces for evidence, comparison, and extension decisions

## The Four Arcs

### Purity and dataflow

Modules 01 to 03 establish the semantic floor:

- what purity really buys you
- how data-first APIs change refactoring pressure
- how lazy pipelines remain understandable without hidden execution

Without this floor, later abstractions feel clever instead of necessary.

### Failure and modelling

Modules 04 to 06 turn pipelines into something survivable:

- failures become typed values instead of scattered exception paths
- domain states and validations become explicit shapes
- chained flows keep context visible instead of implicit

### Effects and async pressure

Modules 07 to 08 move the course from local transforms to real systems:

- capabilities, ports, and adapters define what effectful code may do
- retries, resources, and transactions become reviewable policy choices
- async work gains explicit pressure-control and testable boundaries

### Interop and sustainment

Modules 09 to 10 ask whether the design can survive a team and a production lifecycle:

- can the functional core coexist with normal Python libraries
- can performance and observability be improved without blurring boundaries
- can the codebase evolve without turning the functional vocabulary into ceremony

## How The Capstone Fits

- Modules 01 to 03 explain the capstone's pure helpers, configuration shapes, and stream stages.
- Modules 04 to 06 explain its failure containers, modelling choices, and compositional pipeline style.
- Modules 07 to 08 explain its shells, adapters, policies, and async coordination layers.
- Modules 09 to 10 explain its interop surfaces, review workflow, and sustainment story.

## Support Pages To Keep Open

- [Module Dependency Map](module-dependency-map.md) when you need the sequence justified
- [Module Promise Map](module-promise-map.md) when you want the promise and evidence route for each module
- [Module Checkpoints](module-checkpoints.md) when you need exit criteria before moving on
- [Practice Map](practice-map.md) when you want the module-to-proof loop in one place
- [History Guide](history-guide.md) when you need the generated comparison route
- [Proof Matrix](proof-matrix.md) when you want the fastest route from a claim to executable evidence
- [FuncPipe Capstone Guide](capstone.md) and [Capstone Map](capstone-map.md) when you want the repository route kept explicit

## Honest Expectation

If you rush, the course will feel heavier than necessary. If you read it in order and
keep the capstone in view, the later modules should feel like consequences of earlier
boundary decisions instead of unrelated advanced techniques.
