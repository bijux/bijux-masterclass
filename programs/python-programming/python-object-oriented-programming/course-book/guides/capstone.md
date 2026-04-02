# Capstone


<!-- page-maps:start -->
## Guide Fit

```mermaid
flowchart TD
  family["Python Programming"] --> program["Python Object-Oriented Programming"]
  program --> pressure["A concrete learner or reviewer question"]
  pressure --> guide["Capstone"]
  guide --> next["Modules, capstone, and reference surfaces"]
```

```mermaid
flowchart TD
  question["Name the exact question you need answered"] --> skim["Skim only the sections that match that pressure"]
  skim --> crosscheck["Open the linked module, proof surface, or capstone route"]
  crosscheck --> next_move["Leave with one next decision, page, or command"]
```
<!-- page-maps:end -->

Read the first diagram as a timing map: this guide is for a named pressure, not for wandering the whole course-book. Read the second diagram as the guide loop: arrive with a concrete question, use only the matching sections, then leave with one smaller and more honest next move.

The capstone is a monitoring-policy system for a team that needs to register rules,
activate them deliberately, evaluate incoming metric samples, emit incidents, and
keep downstream read models in sync without turning the domain model into a pile of
procedural glue.

This is the course's executable reference model. It is intentionally small enough to
read in one sitting, but rich enough to expose the object-oriented pressures the course
is teaching you to reason about.

## Domain primer

The capstone models one operational problem only:

- a team defines monitoring rules for a service
- those rules move through a clear lifecycle
- incoming samples are evaluated against active rules
- incidents are emitted without letting downstream views control the domain

That narrow domain is deliberate. It is small enough that ownership mistakes stay visible
and rich enough that aggregates, policies, events, projections, and runtime orchestration
all become necessary for honest reasons.

## Study goal

Use the capstone to answer one question repeatedly:

> If I changed this behavior tomorrow, which object should absorb that change, and why?

If the course prose is working, the capstone should make those ownership decisions feel
clearer after each module.

## What the capstone demonstrates

- immutable value objects for metric names, samples, severities, and rule definitions
- a `MonitoringPolicy` aggregate root that owns registration, activation, retirement, and evaluation
- strategy objects for different rule-evaluation modes
- domain events that describe lifecycle changes and incidents without mutating projections directly
- projections and read models that stay downstream of authoritative events
- a runtime orchestration surface that coordinates adapters and commits without becoming the domain
- an explicit unit of work that makes rollback semantics visible instead of implicit

## How to use it while reading

- After Module 01, inspect the value objects and equality semantics.
- After Module 02, inspect the split between domain objects, policies, runtime orchestration, and adapters.
- After Module 03, inspect lifecycle states and validation boundaries.
- After Module 04, inspect aggregate ownership, events, and projections.
- After Module 05, inspect unit-of-work boundaries, failure handling, and extension pressure.
- After Module 06, inspect how repositories and codecs could persist the model without weakening invariants.
- After Module 07, inspect where clocks, schedulers, queues, and async adapters should sit relative to the aggregate.
- After Module 08, inspect whether the current tests prove contracts, lifecycles, and public behavior clearly enough.
- After Module 09, inspect which parts of the code should become the supported public facade and extension seam.
- After Module 10, review the whole capstone for hot paths, observability, trust boundaries, and operational readiness.

## Best route by module stage

- Modules 01-03: start with value semantics, lifecycle rules, and aggregate state transitions.
- Modules 04-07: follow ownership through policies, events, repositories, runtime coordination, and time pressure.
- Modules 08-10: switch to bundles, tests, and public review routes to decide whether the design deserves trust.

## Inspect, explain, prove

Use the capstone with one repeated loop:

1. Inspect one file, guide, or saved bundle.
2. Explain which object or boundary owns the behavior you just saw.
3. Prove that claim with one named test or one named command.

That loop keeps the capstone from becoming a repository tour without a learning contract.

## Run it

From the repository root:

```bash
make PROGRAM=python-programming/python-object-oriented-programming test
```

From the capstone directory:

```bash
make confirm
```

Run the scenario walkthrough from the capstone directory:

```bash
make demo
```

Use [Capstone Map](capstone-map.md) when you want the best next page for architecture,
code reading, walkthrough, or proof review.

## Architecture map

```mermaid
graph TD
  source["Metric source"]
  runtime["Runtime orchestration"]
  app["Application commands"]
  uow["Unit of work"]
  aggregate["MonitoringPolicy aggregate"]
  policies["Evaluation policies"]
  events["Domain events"]
  projections["Read models and projections"]
  sink["Incident sink"]

  source --> runtime
  runtime --> app
  app --> uow
  uow --> aggregate
  aggregate --> policies
  aggregate --> events
  events --> projections
  runtime --> sink
```

## What to look for in review

- Which object owns each invariant?
- Which objects are authoritative, and which are derived views?
- Which behavior is stable domain logic, and which is orchestration?
- Where would a new rule mode, new sink, or new read model be added?

## Where to start in code

If you want the most human-friendly entrypoint into the implementation, start with
`application.py`. It exposes the capstone as learner-facing use cases rather than as
raw internals, which makes it easier to connect the design prose to the executable flow.

## Why it matters

The capstone keeps the course honest. If a chapter claims that aggregates should own
invariants, that strategies should carry evaluation variability, or that projections
should stay downstream of events, the code here shows that shape directly and the tests
enforce it.
