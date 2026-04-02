# Course Guide


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  start["Start Here"] --> home["Course Home"]
  home --> guide["Course Guide"]
  guide --> modules["Modules 01-10"]
  modules --> capstone["FuncPipe capstone review"]
```

```mermaid
flowchart TD
  semantics["Modules 01-03\npurity and dataflow"] --> failure["Modules 04-06\nfailure modelling and lawful composition"]
  failure --> effects["Modules 07-08\neffect boundaries and async pressure"]
  effects --> sustainment["Modules 09-10\ninterop, governance, and sustainment"]
```
<!-- page-maps:end -->

This guide explains how the course is shaped and why the sequence matters. The course is
not a pile of functional programming topics. It is a route from local reasoning to
systems that remain testable and reviewable under operational pressure.

## The four arcs

## Purity and dataflow

Modules 01 to 03 establish the semantic floor:

- what purity really buys you
- how data-first APIs change refactoring pressure
- how lazy pipelines remain understandable without hidden execution

Without this floor, later abstractions feel clever instead of necessary.

## Failure and modelling

Modules 04 to 06 turn pipelines into something survivable:

- failures become typed values instead of scattered exception paths
- domain states and validations become explicit shapes
- chained flows keep context visible instead of implicit

## Effects and async pressure

Modules 07 to 08 move the course from local transforms to real systems:

- capabilities, ports, and adapters define what effectful code may do
- retries, resources, and transactions become reviewable policy choices
- async work gains explicit pressure-control and testable boundaries

## Interop and sustainment

Modules 09 to 10 ask whether the design can survive a team and a production lifecycle:

- can the functional core coexist with normal Python libraries
- can performance and observability be improved without blurring boundaries
- can the codebase evolve without turning the functional vocabulary into ceremony

## How the capstone fits the arc

- Modules 01 to 03 explain the capstone's pure helpers, configuration shapes, and stream stages.
- Modules 04 to 06 explain its failure containers, modelling choices, and compositional pipeline style.
- Modules 07 to 08 explain its shells, adapters, policies, and async coordination layers.
- Modules 09 to 10 explain its interop surfaces, review workflow, and sustainment story.

## Module-end comparison route

Every module should end with the same honest routine:

1. read the module's `refactoring-guide.md`
2. run `make PROGRAM=python-programming/python-functional-programming history-refresh` if the local history surface is missing or stale
3. compare your work with `_history/worktrees/module-XX`
4. name the boundary you are trying to preserve before moving to the next module

Use [History Guide](history-guide.md) when you need the generated tag and worktree rules,
not just the study order.

## Honest expectation

If you rush, the course will feel heavier than necessary. If you read it in order and
keep the capstone in view, the later modules should feel like consequences of earlier
boundary decisions instead of unrelated advanced techniques.

Use [Module Dependency Map](module-dependency-map.md) when you need to understand why the
sequence is shaped this way, use [Practice Map](practice-map.md) to keep each module tied
to code and verification, use [History Guide](history-guide.md) when you need the
generated comparison route, and use [Proof Matrix](proof-matrix.md) when you need the
shortest route from a design claim to capstone evidence.
