# Module 05: Decorator Design, Policies, and Typing

<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Decorator Design Policies Typing"]
  page["Module 05: Decorator Design, Policies, and Typing"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  orient["Orient on the page map"] --> read["Read the main claim and examples"]
  read --> inspect["Inspect the related code, proof, or capstone surface"]
  inspect --> verify["Run or review the verification path"]
  verify --> apply["Apply the idea back to the module and capstone"]
```
<!-- page-maps:end -->

Module 05 takes the wrapper mechanics from Module 04 and pushes them into harder design
territory: retries, timeouts, rate limits, annotation-aware validation, and cache policy.
The module is not here to celebrate decorator power. It is here to teach where that power
starts to become expensive, misleading, or better owned by an explicit object or service
boundary.

This module now uses the same ten-file learning surface as the deep-dive series so the
overview, five cores, worked example, practice set, answers, and glossary each have one
clear job.

## What this module is for

By the end of Module 05, you should be able to explain five things clearly:

- how decorator factories capture configuration at definition time
- how resilience wrappers change control flow and error behavior
- what annotation-aware runtime checks can and cannot promise honestly
- how cache policy differs from a thin wrapper and why `lru_cache` exposes control hooks
- when wrapper policy should move to an explicit object, field, or service boundary instead

## Keep these pages open

- [Mid-Course Map](../module-00-orientation/mid-course-map.md)
- [Pressure Routes](../guides/pressure-routes.md)
- [Anti-Pattern Atlas](../reference/anti-pattern-atlas.md)
- [Capstone Walkthrough](../capstone/capstone-walkthrough.md)

## The ten files in this module

1. Overview (`index.md`)
2. [Decorator Factories and Parameter Capture](decorator-factories-and-parameter-capture.md)
3. [Resilience and Control-Flow Wrappers](resilience-and-control-flow-wrappers.md)
4. [Annotation-Aware Runtime Contracts](annotation-aware-runtime-contracts.md)
5. [Cache Policy and lru_cache Behavior](cache-policy-and-lru-cache-behavior.md)
6. [Wrapper Policy Boundaries](wrapper-policy-boundaries.md)
7. [Worked Example: Building a Partial `@validated` Decorator](worked-example-building-a-partial-validated-decorator.md)
8. [Exercises](exercises.md)
9. [Exercise Answers](exercise-answers.md)
10. [Glossary](glossary.md)

## How to use the file set

| If you need to... | Start here |
| --- | --- |
| understand how configurable decorators capture policy parameters | [Decorator Factories and Parameter Capture](decorator-factories-and-parameter-capture.md) |
| inspect retries, timeouts, and rate limits as control-flow changes instead of ornament | [Resilience and Control-Flow Wrappers](resilience-and-control-flow-wrappers.md) |
| judge annotation-driven runtime behavior without pretending it is a full type system | [Annotation-Aware Runtime Contracts](annotation-aware-runtime-contracts.md) |
| compare bounded caches with the standard-library cache model | [Cache Policy and lru_cache Behavior](cache-policy-and-lru-cache-behavior.md) |
| decide when policy has outgrown a decorator | [Wrapper Policy Boundaries](wrapper-policy-boundaries.md) |
| see those tradeoffs inside one partial runtime validator | [Worked Example: Building a Partial `@validated` Decorator](worked-example-building-a-partial-validated-decorator.md) |
| test your understanding before class-level customization begins | [Exercises](exercises.md) |
| compare your reasoning against a reference answer | [Exercise Answers](exercise-answers.md) |
| stabilize the policy and typing vocabulary | [Glossary](glossary.md) |

## The running question

Carry this question through every page:

> Which part of this behavior still belongs in a wrapper, and which part should move to an explicit object, field, or service boundary instead?

Strong Module 05 answers usually mention one or more of these:

- configuration captured once in a decorator factory
- retries, timeouts, or limits changing call semantics
- annotation-aware checks staying partial and reviewable
- explicit cache introspection and reset surfaces
- policy pressure strong enough to reject another decorator layer

## Learning outcomes

By the end of this module, you should be able to:

- review policy-heavy decorators without mistaking them for thin transformations
- preserve metadata and callable visibility even when wrappers grow more powerful
- keep annotation-driven runtime behavior honest about its limits
- reject wrapper designs that should become explicit services, objects, or later course mechanisms

## Exit standard

Do not move on until all of these are true:

- you can explain what a decorator factory captures and when it runs
- you can name how retries, timeouts, or rate limits change semantics at the call boundary
- you can say which annotation-aware checks remain partial rather than pretending to replace static typing
- you can judge when a decorator has become hidden policy that should move elsewhere

When those feel ordinary, Module 05 has done its job and the course can move into
class-level customization with a clearer sense of wrapper ownership.
