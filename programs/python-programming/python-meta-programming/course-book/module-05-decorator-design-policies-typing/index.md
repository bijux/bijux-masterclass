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

For many learners, this is the first module where "I understand the syntax" stops being
enough. A policy-heavy decorator can look tidy while still hiding retry rules, timeout
behavior, validation scope, cache lifetimes, and operational controls that another
maintainer must eventually own.

This module now uses the same ten-file learning surface as the deep-dive series so the
overview, five cores, worked example, practice set, answers, and glossary each have one
clear job.

Treat this module as one full review day on wrapper ownership. The goal is not to collect
more decorator patterns. The goal is to leave with a stable way to answer:

- what policy was captured once at definition time
- what policy now changes behavior at each call boundary
- what evidence still keeps that policy inspectable
- when the decorator should stop growing and hand ownership elsewhere

## What this module is for

By the end of Module 05, you should be able to explain five things clearly:

- how decorator factories capture configuration at definition time
- how resilience wrappers change control flow and error behavior
- what annotation-aware runtime checks can and cannot promise honestly
- how cache policy differs from a thin wrapper and why `lru_cache` exposes control hooks
- when wrapper policy should move to an explicit object, field, or service boundary instead

You should also be able to reject weak explanations such as:

- "the decorator just makes this more convenient"
- "the retry logic is still basically transparent"
- "warning mode is good enough to call it safe"
- "the cache only changes performance"
- "we can always move the policy out later if it grows"

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

## The review route through the module

Use this route if you want one stable teaching sequence instead of ten disconnected files:

| Review question | Why it comes now | Page |
| --- | --- | --- |
| what policy is captured before the function ever runs? | learners need the timing boundary before policy gets heavier | [Decorator Factories and Parameter Capture](decorator-factories-and-parameter-capture.md) |
| how does this wrapper now change execution, waiting, or failure flow? | resilience wrappers are where control-flow policy becomes impossible to ignore | [Resilience and Control-Flow Wrappers](resilience-and-control-flow-wrappers.md) |
| what limited runtime contract can this wrapper support honestly? | typing-aware decorators overclaim easily unless the supported surface is named early | [Annotation-Aware Runtime Contracts](annotation-aware-runtime-contracts.md) |
| what state, history, and operational hooks does the cache now own? | cache policy is the cleanest example of history-dependent wrapper behavior | [Cache Policy and lru_cache Behavior](cache-policy-and-lru-cache-behavior.md) |
| when should the decorator give up ownership altogether? | the earlier cores only help if they culminate in a real design judgment | [Wrapper Policy Boundaries](wrapper-policy-boundaries.md) |

## The running question

Carry this question through every page:

> Which part of this behavior still belongs in a wrapper, and which part should move to an explicit object, field, or service boundary instead?

Strong Module 05 answers usually mention one or more of these:

- configuration captured once in a decorator factory
- retries, timeouts, or limits changing call semantics
- annotation-aware checks staying partial and reviewable
- explicit cache introspection and reset surfaces
- policy pressure strong enough to reject another decorator layer

Strong answers also say what the wrapper does **not** prove or solve automatically:

- explicit configuration does not make broad policy harmless
- preserved metadata does not cancel control-flow or state complexity
- partial runtime validation does not replace static analysis
- a standard-library cache still needs an honest operational story
- a decorator that "still works" may still be the wrong owner

## Learning outcomes

By the end of this module, you should be able to:

- review policy-heavy decorators without mistaking them for thin transformations
- preserve metadata and callable visibility even when wrappers grow more powerful
- keep annotation-driven runtime behavior honest about its limits
- reject wrapper designs that should become explicit services, objects, or later course mechanisms

## Mid-module warning signs

Slow down and review more carefully if any design in this module does one or more of
these:

- captures multiple interacting policy knobs in one decorator factory
- changes how many times the underlying callable may run
- changes waiting, retry, backoff, or abort behavior
- claims runtime typing guarantees broader than its supported hint subset
- owns state that must be inspected, reset, or tuned operationally
- keeps growing even though an explicit object would reveal ownership more clearly

These are not reasons to ban the design. They are reasons to stop calling it "just a
decorator" without stronger proof.

## Evidence packet to build while you learn

By the time you finish the worked example and exercises, you should have a small packet
that another learner can inspect:

- one hand-desugared decorator factory showing what was captured once
- one resilience wrapper with a named control-flow rule and stopping rule
- one partial validator with a named supported surface and a refused feature
- one cache example with explicit inspection and reset hooks
- one redesign note explaining why a broad wrapper should move to an explicit owner

## Exit standard

Do not move on until all of these are true:

- you can explain what a decorator factory captures and when it runs
- you can name how retries, timeouts, or rate limits change semantics at the call boundary
- you can say which annotation-aware checks remain partial rather than pretending to replace static typing
- you can judge when a decorator has become hidden policy that should move elsewhere

Do not move on if you still need phrases like "it just handles policy for us" or "the
decorator keeps things simple" to explain the design. Module 05 is only complete when you
can state the captured configuration, the runtime policy rule, the unsupported claim, and
the likely explicit owner in plain language.

When those feel ordinary, Module 05 has done its job and the course can move into
class-level customization with a clearer sense of wrapper ownership.
