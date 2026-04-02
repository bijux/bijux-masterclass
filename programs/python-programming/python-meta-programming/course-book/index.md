# Python Metaprogramming


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Course home"]
  page["Python Metaprogramming"]
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

This course teaches Python metaprogramming as a discipline of runtime honesty. The goal
is not to make code look advanced. The goal is to understand what Python is doing when
code inspects, wraps, validates, or registers other code and objects.

## Start with these pages

- [Start Here](start-here.md)
- [Course Guide](course-guide.md)
- [Learning Contract](learning-contract.md)
- [Runtime Power Ladder](runtime-power-ladder.md)

## What the course is organized around

### A clear ladder of power

The course moves from plain observation to invasive runtime control:

1. introspection
2. decorators
3. descriptors
4. metaclasses
5. governance boundaries around dynamic execution and global hooks

### One executable proof

The [Capstone Guide](capstone.md) points to a single plugin runtime that keeps the major
mechanisms visible in one place. Use [Capstone Map](capstone-map.md) and
[Capstone File Guide](capstone-file-guide.md) while reading.

### Review judgment

Use [Review Checklist](review-checklist.md), [Practice Map](practice-map.md), and
[Capstone Proof Checklist](capstone-proof-checklist.md) to keep the material pedagogic
instead of ornamental.

## Module route

- [Module 00](module-00.md) defines the reading discipline.
- [Modules 01-03](module-01.md) through [module-03.md](module-03.md) build the object and inspection model.
- [Modules 04-06](module-04.md) through [module-06.md](module-06.md) explain wrappers and class decorators.
- [Modules 07-09](module-07.md) through [module-09.md](module-09.md) explain descriptors and metaclasses.
- [Modules 10-11](module-10.md) through [module-11.md](module-11.md) convert mechanisms into governance and mastery review.

## Failure modes this course is designed to prevent

- using dynamic power because it feels clever
- breaking signatures, metadata, or tracebacks during wrapping
- putting class-creation behavior into code that should stay ordinary and explicit
- teaching metaclasses before the learner understands descriptors
- approving meta-heavy code without a proof route
