# Start Here

<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Metaprogramming"]
  section["Start Here"]
  page["Start Here"]
  route["Course guide and modules"]

  family --> program --> section --> page --> route
```

```mermaid
flowchart LR
  begin["Read the course boundary"] --> choose["Choose the first reading path"]
  choose --> overview["Open the course guide"]
  choose --> orientation["Open Module 00"]
  overview --> module["Continue into the first module"]
  orientation --> module
```
<!-- page-maps:end -->

Start here if you are deciding whether this course matches your current problem. Python
metaprogramming only pays for itself when the runtime behavior stays visible, testable,
and easier to justify than a simpler alternative.

## Use This Course If

- you need to inspect, wrap, validate, or register Python objects without lying about runtime behavior
- you review frameworks or libraries that already rely on decorators, descriptors, or metaclasses
- you want a disciplined ladder for deciding when a higher-power hook is justified

## Do Not Start Here If

- you still need a first introduction to classes, callables, attributes, and ordinary object design
- you want clever tricks without the debugging and maintenance costs
- the problem can still be solved honestly with plain functions, plain classes, or explicit composition

## Best Reading Route

1. Read [Course Home](../index.md) for the course promise and support surfaces.
2. Read [Course Guide](course-guide.md) for the module arc and page roles.
3. Read [Learning Contract](learning-contract.md) before you start Module 01.
4. Read [Module 00](../module-00-orientation/index.md) for the power ladder and study model.
5. Keep [Runtime Power Ladder](../reference/runtime-power-ladder.md) open while reading so every stronger hook is judged against a lower-power alternative.
6. Use [Capstone Map](capstone-map.md) and [Capstone Guide](capstone.md) when you want the executable route.

## Route By Pressure

### Route 1: Reviewer under pressure

1. Read [Course Guide](course-guide.md).
2. Read [Module 00](../module-00-orientation/index.md).
3. Read [Module 04](../module-04-function-wrappers-and-decorators/index.md), [Module 07](../module-07-descriptor-mechanics-and-lookup/index.md), and [Module 09](../module-09-metaclass-design-and-class-creation/index.md) as the three main review hotspots.
4. Cross-check the [Capstone Guide](capstone.md).

### Route 2: Full mastery path

1. Read [Course Guide](course-guide.md).
2. Read [Learning Contract](learning-contract.md).
3. Read every module in order from [Module 00](../module-00-orientation/index.md) through [Module 10](../module-10-runtime-governance-and-mastery/index.md), then finish with [Mastery Review](../module-10-runtime-governance-and-mastery/mastery-review.md).
4. Keep [Capstone Map](capstone-map.md) open while reading so every mechanism stays tied to one executable surface.

## Success Signal

By the end of the course, you should be able to explain:

- what happens at import time, class-definition time, and call time
- what metadata or signatures must survive wrapping
- why a descriptor owns an invariant better than a decorator in some cases
- when a metaclass is justified and when it is only hiding design confusion

## First Pages To Keep Open

- [Course Home](../index.md)
- [Course Guide](course-guide.md)
- [Module 00](../module-00-orientation/index.md)
- [Capstone Guide](capstone.md)
