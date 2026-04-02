# Deadlines, Timeouts, and Expiration Policies


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Object-Oriented Programming"]
  section["Time And Concurrency"]
  page["Deadlines, Timeouts, and Expiration Policies"]
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
