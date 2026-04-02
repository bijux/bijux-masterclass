# Cancellation, Retries, and Resumable Operations


<!-- page-maps:start -->
## Concept Position

```mermaid
flowchart TD
  family["Python Programming"] --> program["Python Object-Oriented Programming"]
  program --> module["Module 07: Time, Scheduling, and Concurrency Boundaries"]
  module --> concept["Cancellation, Retries, and Resumable Operations"]
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

Design operations so cancellation and retry behavior are explicit instead of becoming
accidental duplicate work.

## 1. Cancellation Is Part of the Contract

If an operation can be cancelled halfway through, callers need to know whether it:

- left no durable effects
- partially completed
- can be resumed safely

That is business-significant behavior.

## 2. Retries Require Idempotent Boundaries

Retrying a metric fetch may be safe.
Retrying "publish incident" may duplicate external alerts unless deduplicated.

The boundary determines whether retry is safe.

## 3. Resumable Work Needs State Markers

Long-running operations often need explicit markers such as:

- pending
- in progress
- published

Those states make restart and recovery possible without guesswork.

## 4. Separate Recovery Policy from Core Domain Behavior

Aggregates should preserve invariants.
Application and runtime layers should decide cancellation handling, retry schedule, and
resume strategy.

## Practical Guidelines

- Document post-cancellation state for important operations.
- Retry only across boundaries that are idempotent or deduplicated.
- Add explicit progress markers for resumable workflows.
- Keep recovery orchestration outside core domain entities.

## Exercises for Mastery

1. Choose one operation and describe its cancellation outcome precisely.
2. Add a deduplication or idempotence key to one retried workflow.
3. Model one long-running workflow with explicit progress states.
