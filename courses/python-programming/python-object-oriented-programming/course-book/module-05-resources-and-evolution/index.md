# Module 05: Resources and Evolution

Correct object models still fail if they leak resources, blur failure handling, or
cannot evolve safely. This module treats survivability as part of design quality.

## Why this module matters

A design can look elegant in greenfield code review and still fail in production because
it leaks cleanup responsibilities, retries unsafely, widens public surfaces casually, or
cannot absorb a new requirement without violating old assumptions.

This module treats operational survivability as part of object-oriented design rather
than as a later concern owned by "infrastructure people."

## Main questions

- Who owns files, sockets, connections, and cleanup obligations?
- How do you group changes and failure boundaries coherently?
- What makes retries safe or unsafe?
- Which modules are public contracts and which are implementation detail?
- How do you add new behavior without quietly breaking old callers?

## Reading path

1. Start with resource ownership and unit-of-work boundaries.
2. Read cleanup, retries, and error propagation as one operational cluster.
3. Then move to public API boundaries, smells, copying, and compatibility.
4. Finish with the refactor chapter to test whether the design can evolve without collapse.

## Common failure modes

- making callers responsible for cleanup details they cannot reliably remember
- retrying operations that are not idempotent and duplicating side effects
- logging everywhere without deciding what contract the logs actually support
- exposing internal modules as accidental public API
- adding new features by bypassing existing invariants instead of extending them cleanly

## Capstone connection

The capstone's in-memory unit of work, runtime facade, and repository boundary are
small on purpose, but they model the pressure this module is about: who owns failure,
who commits change, which surfaces are public, and how new rule behavior can be added
without rewriting the rest of the system.

## Outcome

You should finish this module able to shape object-oriented Python systems that stay
operable and maintainable under long-term change rather than only under greenfield conditions.
