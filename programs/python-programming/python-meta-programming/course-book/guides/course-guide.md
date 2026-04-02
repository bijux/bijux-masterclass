# Course Guide

<!-- page-maps:start -->
## Page Maps

```mermaid
graph TD
  guide["Course Guide"]
  orientation["Orientation and reading contract"]
  ladder["Runtime power ladder"]
  modules["Mechanics modules"]
  capstone["Capstone proof route"]
  review["Review and mastery"]

  guide --> orientation --> ladder --> modules --> capstone --> review
```

```mermaid
flowchart LR
  novice["Need conceptual grounding"] --> m00["Module 00"]
  novice --> m01["Modules 01-03"]
  wrappers["Need wrapper discipline"] --> m04["Modules 04-06"]
  attributes["Need attribute control"] --> m07["Modules 07-08"]
  classes["Need class creation control"] --> m09["Module 09"]
  governance["Need policy and review"] --> m10["Modules 10-11"]
```
<!-- page-maps:end -->

This guide explains how the course is organized and what each part is trying to teach.
The learner goal is not "know more hooks." The learner goal is "choose the lowest-power
hook that solves the problem without damaging debuggability."

## Course spine

The course has four linked layers:

1. orientation and reading discipline
2. runtime mechanics from introspection through metaclasses
3. capstone proof in a single plugin runtime
4. review surfaces for judgment, debugging, and extension decisions

## What each stage owns

### Orientation

- [Start Here](start-here.md) decides whether the course matches your current problem.
- [Module 00](../module-00-orientation/index.md) defines the power ladder and the rules for reading the course.

### Runtime mechanics

- [Modules 01-03](../module-01-runtime-object-model/index.md) through [module-03-inspect-signatures-and-provenance/index.md](../module-03-inspect-signatures-and-provenance/index.md) explain objects, safe observation, and `inspect` as runtime evidence.
- [Modules 04-06](../module-04-function-wrappers-and-decorators/index.md) through [module-06-class-customization-before-metaclasses/index.md](../module-06-class-customization-before-metaclasses/index.md) explain wrappers, policy-bearing decorators, and the last honest class-level tools before descriptors.
- [Modules 07-09](../module-07-descriptor-mechanics-and-lookup/index.md) through [module-09-metaclass-design-and-class-creation/index.md](../module-09-metaclass-design-and-class-creation/index.md) explain descriptors, framework-shaped attribute systems, and the narrow case for metaclasses.

### Governance

- [Module 10](../module-10-runtime-governance-and-mastery/index.md) defines red lines for dynamic execution and high-power runtime hooks.
- [Mastery Review](../module-10-runtime-governance-and-mastery/mastery-review.md) closes the course with explicit exit criteria instead of sequel marketing.

### Capstone proof

- [Capstone Guide](capstone.md) explains the executable proof route.
- [Capstone Map](capstone-map.md) and [Capstone File Guide](capstone-file-guide.md) keep the mechanism-to-file mapping explicit.

## Recommended reading pattern

- Read one module.
- Inspect the named capstone file immediately.
- Run the smallest proof command that confirms the claim.
- Write down where the mechanism would become dishonest in real code.

## What the ten-module flow is trying to prevent

- jumping to metaclasses before attribute lookup is mechanical in your head
- treating decorators, descriptors, and metaclasses as interchangeable kinds of cleverness
- learning a stronger hook before you can explain why the weaker one stopped being enough
- reading the capstone as a framework stunt instead of as executable evidence for each boundary

## What to avoid while studying

- skipping straight to metaclasses before you can explain descriptors cleanly
- treating `inspect` output as harmless when it can trigger assumptions about runtime identity
- copying patterns into production code before you can say what they cost to debug
