# Module 05: Resources, Failures, and Safe Evolution


<!-- page-maps:start -->
## Module Position

```mermaid
flowchart TD
  family["Python Programming"] --> program["Python Object-Oriented Programming"]
  program --> module["Module 05: Resources, Failures, and Safe Evolution"]
  module --> lessons["Lesson pages and worked examples"]
  module --> checkpoints["Exercises and closing criteria"]
  module --> capstone["Related capstone evidence"]
```

```mermaid
flowchart TD
  purpose["Start with the module purpose and main questions"] --> lesson_map["Use the lesson map to choose reading order"]
  lesson_map --> study["Read the lessons and examples with one review question in mind"]
  study --> proof["Test the idea with exercises and capstone checkpoints"]
  proof --> close["Move on only when the closing criteria feel concrete"]
```
<!-- page-maps:end -->

Read the first diagram as a placement map: this page sits between the course promise, the lesson pages listed below, and the capstone surfaces that pressure-test the module. Read the second diagram as the study route for this page, so the diagrams point you toward the `Lesson map`, `Exercises`, and `Closing criteria` instead of acting like decoration.

Correct object models still fail if they leak resources, blur failure handling, or
cannot evolve safely. This module treats survivability as part of design quality.

Keep one question in view while reading:

> Who owns the cost when this behavior fails, retries, leaks, or needs to evolve under an existing contract?

That question keeps operational concerns attached to ownership instead of dissolving into
general “infrastructure” language.

## Preflight

- You should already be able to name the ownership boundary for domain behavior before attaching operational concerns to it.
- If retries, cleanup, or public API boundaries still feel like "someone else’s layer," treat this module as design work, not operations trivia.
- Keep asking who pays for failure, leakage, or compatibility drift when a change goes wrong.

## Learning outcomes

- assign cleanup, failure handling, retries, and compatibility pressure to explicit owners
- distinguish domain errors from system-boundary failures without flattening them into generic exceptions
- evaluate idempotency, unit-of-work boundaries, and public surface discipline as long-term design contracts
- extend behavior without bypassing invariants or widening the accidental public API

## Why this module matters

A design can look elegant in greenfield code review and still fail in production because
it leaks cleanup responsibilities, retries unsafely, widens public surfaces casually, or
cannot absorb a new requirement without violating old assumptions.

This module treats operational survivability as part of object-oriented design rather
than as a later concern owned by "infrastructure people."

## Main questions

- Who owns files, sockets, connections, and cleanup obligations?
- How do you group changes and failure boundaries coherently?
- Which failures belong in the domain contract, and which belong at the system boundary?
- What makes retries safe or unsafe?
- Which modules are public contracts and which are implementation detail?
- How do you add new behavior without quietly breaking old callers?

## Reading path

1. Start with resource ownership and unit-of-work boundaries.
2. Read cleanup, domain errors, retries, and error propagation as one operational cluster.
3. Then move to public API boundaries, smells, copying, and compatibility.
4. Finish with the refactor chapter to test whether the design can evolve without collapse.

## Keep these support surfaces open

- `../guides/outcomes-and-proof-map.md` when you want the survivability promise tied to executable evidence.
- `../guides/pressure-routes.md` when failure ownership still feels mixed with persistence or runtime pressure.
- `../reference/self-review-prompts.md` when you want to test whether cleanup, retry, and compatibility questions now sound like ownership decisions.

## Review route for failure ownership

1. Inspect `capstone/docs/ARCHITECTURE.md` and `capstone/docs/EXTENSION_GUIDE.md`.
2. Read `src/service_monitoring/runtime.py` and `src/service_monitoring/repository.py`.
3. Inspect the unit-of-work and runtime test surfaces before escalating to the strongest proof route.

Use that route to keep one distinction explicit: domain truth should stay in the model,
while retries, cleanup, publication, and rollback stay reviewable at the surrounding boundary.

## Common failure modes

- making callers responsible for cleanup details they cannot reliably remember
- flattening all failures into generic exceptions with no recovery contract
- retrying operations that are not idempotent and duplicating side effects
- logging everywhere without deciding what contract the logs actually support
- exposing internal modules as accidental public API
- adding new features by bypassing existing invariants instead of extending them cleanly

## Exercises

- Pick one operation and explain who owns cleanup, who owns retry policy, and which failures should remain visible to callers.
- Review one public surface and state which modules are contract and which modules should remain implementation detail.
- Describe one feature addition that should extend the existing model and one that would be a bypass around current invariants.

## Capstone connection

The capstone's in-memory unit of work, runtime facade, and repository boundary are
small on purpose, but they model the pressure this module is about: who owns failure,
who commits change, which surfaces are public, and how new rule behavior can be added
without rewriting the rest of the system.

## Honest completion signal

You are ready to move on when you can name:

- who owns cleanup for one change path
- where retry policy may live without redefining domain meaning
- which compatibility promise belongs to the public surface rather than the repository internals

## Closing criteria

You should finish this module able to shape object-oriented Python systems that stay
operable and maintainable under long-term change rather than only under greenfield conditions.

## Directory glossary

Use [Glossary](glossary.md) when you want the recurring language in this module kept stable while you move between lessons, exercises, and capstone checkpoints.
