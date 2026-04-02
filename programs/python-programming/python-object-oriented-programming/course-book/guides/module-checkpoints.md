# Module Checkpoints


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  checkpoints["Module checkpoints"]
  read["Read the module"]
  explain["Explain the design shift"]
  prove["Verify in code or capstone"]

  checkpoints --> read
  checkpoints --> explain
  checkpoints --> prove
```

```mermaid
flowchart LR
  finish["Finish a module"] --> pause["Pause before advancing"]
  pause --> explain["Explain the new ownership rule"]
  explain --> verify["Review the proof route"]
  verify --> next["Advance only when the checkpoint is true"]
```
<!-- page-maps:end -->

Use this page at the end of each module. A strong course needs a clear exit bar, not
just more reading. These checkpoints are the smallest honest claims you should be able
to make before moving deeper into the course.

## Checkpoints by module

### Module 01: Object Model

- You can explain when identity matters more than value equality.
- You can describe why aliasing or mutable hashing creates non-local bugs.
- You can justify whether a type should expose data-model hooks or stay opaque.

### Module 02: Design and Layering

- You can place behavior in values, entities, services, policies, or adapters with reasons.
- You can explain why composition or protocols are better than inheritance in a given case.
- You can sketch a composition root without letting wiring logic leak into the domain.

### Module 03: State and Typestate

- You can make illegal states hard to construct.
- You can describe which transitions are allowed and who guards them.
- You can explain when dataclasses, descriptors, or explicit factories fit the state model.

### Module 04: Aggregates and Collaboration

- You can name the aggregate root and defend why it owns the invariant.
- You can separate authoritative objects from projections or debug views.
- You can explain what an event means without pretending every system needs event sourcing.

### Module 05: Resources and Evolution

- You can name who owns cleanup, retries, and failure translation.
- You can describe which errors are part of the public contract and which stay internal.
- You can extend behavior without bypassing invariants or widening the public surface casually.

### Module 06: Persistence and Schema Evolution

- You can explain how a repository rehydrates aggregates without flattening the domain.
- You can separate storage records from domain objects and query models.
- You can describe how old stored data survives schema or codec changes.

### Module 07: Time and Concurrency

- You can say where time enters the model and why that boundary is explicit.
- You can explain which object owns mutation when threads, queues, or tasks appear.
- You can show where sync and async code meet without leaking event-loop assumptions inward.

### Module 08: Testing and Verification

- You can choose behavior tests, stateful tests, contract tests, or property tests deliberately.
- You can explain what confidence each proof layer buys and what it does not.
- You can design test fixtures that clarify ownership instead of hiding it.

### Module 09: Public APIs and Extension Governance

- You can name the stable public surface and the internal surface.
- You can explain what extension points are allowed and what must remain closed.
- You can describe how examples, docs, and compatibility suites defend the public contract.

### Module 10: Performance, Observability, and Security

- You can identify hot paths without changing semantics prematurely.
- You can explain which telemetry signals help review object boundaries in production.
- You can describe where serialization, secrets, and public inputs cross trust boundaries.

## How to use these checkpoints

- If you cannot explain the checkpoint in plain language, re-read the module overview and the module refactor chapter.
- If the checkpoint sounds true only in prose, use the capstone and tests to force a concrete example.
- If a later module feels unclear, come back here and find the first checkpoint that is still fuzzy.

These checkpoints turn the course from “many advanced pages” into a sequence of earned
design abilities.
