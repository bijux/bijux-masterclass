# Mid-Course Map

<!-- page-maps:start -->
## Concept Position

```mermaid
flowchart TD
  family["Python Programming"] --> program["Python Functional Programming"]
  program --> module["Module 00: Orientation and Study Practice"]
  module --> concept["Mid-Course Map"]
  concept --> capstone["Capstone pressure point"]
```

```mermaid
flowchart LR
  ready["Foundations feel stable"] --> failures["Modules 04 to 06"]
  failures --> effects["Modules 07 to 08"]
  effects --> capstone["Inspect the matching capstone route"]
  capstone --> decision["Decide whether interop and sustainment are now the right next pressure"]
```
<!-- page-maps:end -->

Use this page when Modules 01 to 03 no longer feel like the blocker, but the second half
of the course still feels too large to enter cleanly. The goal is to turn the middle of
the course into a readable bridge from semantic clarity to system pressure.

## Modules 04 to 06: survivable failure and modelling

Use this stretch when the main pressure is no longer "what is pure?" but instead:

- how failures should become explicit values instead of hidden control flow
- how domain states should stay legible under validation and branching
- how context should remain visible while dependent work composes

Capstone check:

- inspect `src/funcpipe_rag/result/`
- inspect `src/funcpipe_rag/fp/validation.py`
- read `tests/unit/result/` and `tests/unit/fp/`

## Modules 07 to 08: effect boundaries and async pressure

Use this stretch when the design pressure moves outward into real system boundaries:

- resource handling, retries, and idempotent effects
- adapters, protocols, and capability boundaries
- async backpressure, fairness, and deterministic coordination proof

Capstone check:

- inspect `src/funcpipe_rag/boundaries/`
- inspect `src/funcpipe_rag/domain/effects/`
- inspect `src/funcpipe_rag/domain/effects/async_/`
- read `tests/unit/domain/`

## How to know you are ready for Module 09

Move into interop and sustainment when you can answer:

- where your pure core ends
- where failures become values instead of implicit branching
- where effects enter and how those boundaries are tested
- which capstone file you would open first for a resource, retry, or async review question

## Best companion pages

- [Functional Programming Course Map](course-map.md)
- [Mastery Map](mastery-map.md)
- [Engineering Question Map](../guides/engineering-question-map.md)
- [Capstone Map](../capstone/capstone-map.md)
