# Start Here

<!-- page-maps:start -->
## Guide Fit

```mermaid
flowchart TD
  family["Reproducible Research"] --> program["Deep Dive Make"]
  program --> pressure["A concrete learner or reviewer question"]
  pressure --> guide["Start Here"]
  guide --> next["Modules, capstone, and reference surfaces"]
```

```mermaid
flowchart TD
  question["Name the current pressure"] --> route["Choose one starting route"]
  route --> orient["Anchor in Module 00"]
  orient --> next_move["Leave with one stable next module or guide"]
```
<!-- page-maps:end -->

Read the first diagram as a timing map: this page is for choosing the first honest route,
not for replacing the course. Read the second diagram as the loop: choose one route,
anchor in Module 00, and leave with one stable next move.

Deep Dive Make is not a syntax catalog. It is a correctness-first course about truthful
graphs, safe publication, bounded proof, and long-lived build-system judgment.

## Use this page when

- Make still feels new and you want the safest ramp
- the build is already hurting and you need the smallest justifiable route
- you steward a build system and need the course without random browsing

## Do not use this page to

- replace the module sequence with support-page browsing
- enter the capstone before the local concept is legible
- choose the heaviest proof route by default

## Best first pass

1. Read [Course Home](../index.md).
2. Read [Course Guide](course-guide.md).
3. Read [Learning Contract](learning-contract.md).
4. Read [Module 00](../module-00-orientation/index.md).
5. Continue to [Module 01](../module-01-build-graph-foundations-truth/index.md).

Stop there before opening more shelves. That is enough to make the reading contract,
proof contract, and capstone timing visible.

## Choose the route that matches your pressure

| If you need... | Read next | Keep nearby |
| --- | --- | --- |
| first contact with Make | [Module 01](../module-01-build-graph-foundations-truth/index.md), [Module 02](../module-02-parallel-safety-project-structure/index.md) | [Module Checkpoints](module-checkpoints.md) |
| repair of an existing build | [Pressure Routes](pressure-routes.md), [Module 04](../module-04-rule-semantics-precedence-edge-cases/index.md), [Module 05](../module-05-portability-hermeticity-failure-modes/index.md) | [Anti-Pattern Atlas](../reference/anti-pattern-atlas.md) |
| stewardship of a long-lived build system | [Module 03](../module-03-determinism-debugging-self-testing/index.md), [Module 07](../module-07-build-architecture-layered-includes-apis/index.md), [Module 08](../module-08-release-engineering-artifact-contracts/index.md) | [Capstone Review Worksheet](../capstone/capstone-review-worksheet.md) |

## What to keep open

- [Course Guide](course-guide.md)
- [Module Promise Map](module-promise-map.md)
- [Module Checkpoints](module-checkpoints.md)
- [Proof Ladder](proof-ladder.md)
- [Capstone Guide](../capstone/index.md), but only as a later corroboration surface

## Success signal

You are using the course correctly if you can explain:

- why a target rebuilt using `make --trace`
- why the capstone is not your first lesson
- which support page answers the next question without opening everything
- which proof route is proportionate to the claim in front of you
