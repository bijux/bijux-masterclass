# Designing Thread-Aware and Async-Aware APIs

<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Object-Oriented Programming"]
  section["Time Scheduling Concurrency Boundaries"]
  page["Designing Thread-Aware and Async-Aware APIs"]
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

Read the first diagram as a placement map: this page is one concept inside its parent
module, not a detached essay, and the capstone is the pressure test for whether the
idea holds. Read the second diagram as the working rhythm for the page: name the
problem, study the example, identify the boundary, then carry one review question
forward.

## Why this lesson matters

An API is concurrency-aware whether you documented it or not.

If callers can use an object from multiple threads or async tasks, they will form
assumptions about:

- whether calls can overlap safely
- whether a method blocks
- whether it must be awaited
- whether results depend on attachment to a loop or coordinator

If the API does not make those expectations clear, users learn them by failure.

## Concurrency awareness is part of the contract

A public API should help callers understand:

- can this object be called concurrently?
- must calls stay on one thread or one loop?
- is this surface synchronous, asynchronous, or both through a deliberate bridge?
- where does blocking happen?

Those are not implementation trivia. They affect correctness and operability.

## Avoid widening the whole surface by default

One risky pattern is to take one concurrency concern and spread it through every method.

For example:

- one async integration need makes every method `async`
- one shared-state concern makes every consumer manage locks

A stronger approach is to keep concurrency-specific behavior near the boundary that owns
it and keep the rest of the API as narrow and explicit as possible.

## Blocking behavior should be visible

Callers need to know if a method:

- performs only in-memory work
- may block on I/O
- may wait on a queue or lock
- requires an event loop context

Without that, "simple" method calls become hidden coordination points.

That hidden cost is often more damaging than an explicit boundary method would have been.

## Do not confuse availability of use with safety of use

Just because an API can technically be called from many threads or tasks does not mean
it is safe to do so.

A good contract may explicitly say:

- single-threaded only
- caller must serialize access
- safe for concurrent reads but not concurrent mutation
- async-safe only through one supervisor boundary

These are useful constraints. Hiding them helps nobody.

## Common mistakes

- documenting nothing about blocking or concurrency semantics
- exposing the same method to many concurrency modes without a clear ownership story
- turning every surface async because one adapter needed async integration
- leaking lock or event-loop management outward to callers unnecessarily
- implying thread safety through silence

These mistakes make the API broader and less trustworthy than it needs to be.

## Review checklist

| Question | Good sign |
| --- | --- |
| can callers tell whether the API is sync, async, or boundary-bridged? | yes |
| is blocking or waiting behavior visible? | yes |
| are concurrency guarantees and limits stated explicitly? | yes |
| does the API avoid leaking unnecessary runtime coordination outward? | yes |

## Capstone connection

Use the capstone runtime and service boundaries to ask:

- which surfaces should remain plain synchronous domain APIs?
- which surfaces may honestly become async-aware?
- where should callers be told about blocking, serialization, or supervisor requirements?

Those questions keep runtime truth attached to the API contract.

## Exit check

Leave this lesson only when you can do all of these:

- explain why concurrency expectations are part of an API contract
- identify one case where blocking behavior must be visible to the caller
- point to one capstone surface that should stay narrow instead of becoming async-aware everywhere
