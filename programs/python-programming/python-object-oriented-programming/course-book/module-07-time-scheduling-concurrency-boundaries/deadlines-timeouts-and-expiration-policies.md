# Deadlines, Timeouts, and Expiration Policies


<!-- page-maps:start -->
## Concept Position

```mermaid
flowchart TD
  family["Python Programming"] --> program["Python Object-Oriented Programming"]
  program --> module["Module 07: Time, Scheduling, and Concurrency Boundaries"]
  module --> concept["Deadlines, Timeouts, and Expiration Policies"]
  concept --> capstone["Capstone pressure point"]
```

```mermaid
flowchart TD
  problem["Start with the design or failure question"] --> example["Study the worked example and trade-offs"]
  example --> boundary["Name the boundary this page is trying to protect"]
  boundary --> proof["Carry that question into code review or the capstone"]
```
<!-- page-maps:end -->

Read the first diagram as a placement map: this page is one concept inside its parent module, not a detached essay, and the capstone is the pressure test for whether the idea holds. Read the second diagram as the working rhythm for the page: name the problem, study the example, identify the boundary, then carry one review question forward.

## Purpose

Represent time-based rules as explicit domain concepts instead of ad hoc integer
arguments scattered across call sites.

## 1. Deadlines and Timeouts Are Not the Same

A deadline is an absolute moment.
A timeout is a duration budget.

Convert between them deliberately. Do not let every caller improvise that math.

## 2. Expiration Deserves a Policy Object

If a rule expires after thirty minutes or an incident must be acknowledged within a
service-level window, represent that policy explicitly. Temporal business rules are
still business rules.

## 3. Keep Timeout Budgets at the Boundary

Infrastructure adapters may need timeout settings for HTTP or database calls. Domain
objects usually should not know socket-level timeout details.

## 4. Make “Timed Out” a Real Outcome

Do not collapse timeout, cancellation, and domain rejection into one generic exception.
They often need different recovery behavior.

## Practical Guidelines

- Model deadlines and durations as distinct types or fields.
- Represent expiration logic in named policies when it matters to the domain.
- Keep low-level adapter timeouts at the boundary layer.
- Return or raise timeout outcomes explicitly enough to support correct recovery.

## Exercises for Mastery

1. Introduce a named expiration policy into one workflow that currently uses raw integers.
2. Separate timeout failures from business-rule failures in one API.
3. Review one adapter and decide whether its timeout configuration leaks too far inward.
