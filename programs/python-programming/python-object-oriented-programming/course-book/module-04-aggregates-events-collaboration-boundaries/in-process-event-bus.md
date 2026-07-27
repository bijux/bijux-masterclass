# In-Process Event Bus

<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Object-Oriented Programming"]
  section["Aggregates Events Collaboration Boundaries"]
  page["In-Process Event Bus"]
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

Once domain events exist, the next question is how nearby reactions hear about them.

An in-process event bus is one answer for local dispatch inside the same running
application.

It can help reduce direct coupling, but it can also become a hiding place for confusing
side effects if used carelessly.

## What it is

An in-process event bus is a local mechanism that:

- receives an event
- finds interested handlers
- dispatches the event inside the same process

This is not yet distributed messaging. It is local coordination.

## Why it can help

It helps when:

- several local reactions should happen after one domain event
- you want to reduce direct knowledge between publishers and handlers
- the event flow is still small enough to reason about inside one runtime

It gives the system one explicit place for "who reacts to what?"

## What it does not solve

An in-process event bus does not automatically solve:

- delivery guarantees across processes
- persistence and replay concerns
- boundary ownership mistakes
- hidden ordering problems

It is a local coordination tool, not a magic architecture layer.

## Common mistakes

- using the event bus for every local call whether decoupling is needed or not
- hiding critical synchronous logic in far-away handlers
- making it impossible to tell which side effects follow an event
- treating local dispatch as if it had the guarantees of a real durable message system

If readers cannot trace the consequences of an event, the bus is reducing clarity instead
of improving it.

## A practical test

Ask:

1. Are there several local reactions worth decoupling?
2. Will an event bus make those reactions easier to reason about rather than harder?
3. Are the guarantees and ordering expectations still explicit?

If yes, a small in-process bus can help.

If the event flow becomes opaque, direct orchestration may still be better.

## Review checklist

| Question | Good sign |
| --- | --- |
| can you trace what reacts to a given event? | yes |
| is critical invariant logic still outside the bus? | yes |
| are local dispatch assumptions explicit? | yes |
| is the bus used where decoupling helps, not everywhere by habit? | yes |

## Capstone connection

In the capstone, an in-process bus may be useful for:

- local projection updates
- notifications
- audit-style follow-up
- non-authoritative reactions to accepted aggregate changes

If the capstone currently wires every reaction directly and the call graph is becoming
hard to follow, this page points to one possible local decoupling move.

## Exit check

Leave this lesson only when you can do all of these:

- explain an in-process event bus in plain language
- explain what it helps with and what it does not solve
- identify one capstone reaction flow where a local bus might help or hurt clarity
