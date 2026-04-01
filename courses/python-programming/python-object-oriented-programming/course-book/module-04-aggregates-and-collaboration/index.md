# Module 04: Aggregates and Collaboration

Systems fail when invariants are scattered. This module shifts the focus from single
objects to coherent collaboration boundaries.

## Why this module matters

Once more than one object collaborates, correctness stops being a local property.
The system needs a rule for who may change what, when events are emitted, and which
downstream views are authoritative versus merely derived.

Without that discipline, teams often end up with one of two failures:

- every object reaches into every other object, so invariants dissolve into convention
- one "manager" object knows everything, so the model collapses into a disguised script

This module is about finding the boundary between those extremes.

## Main questions

- Which objects need to stay consistent together?
- Where should cross-object invariants be enforced?
- How can domain events decouple behavior without collapsing into complexity theater?
- What should a projection know, and what should it never control?
- How do objects collaborate without every class knowing every other class?

## Reading path

1. Start with aggregates and cross-object invariants.
2. Move through lifecycle and event emission before reading projections.
3. Study policies, adapters, and collaboration surfaces after the boundary is clear.
4. Use the refactor chapter as the test of whether the model stays coherent under extension.

## Common failure modes

- emitting events from objects that do not own the underlying invariant
- letting projections become write models in disguise
- mixing orchestration concerns into aggregates because it feels convenient
- letting adapters leak storage or transport assumptions into domain methods
- adding strategies without a stable contract, turning extension into guesswork

## Capstone connection

This module is the direct explanation of the capstone's architecture. The `MonitoringPolicy`
aggregate owns registration, activation, retirement, and alert production; projections stay
downstream of events; policies encapsulate evaluation variation; and the runtime coordinates
without becoming the source of truth. Read this module as the justification for those edges.

## Outcome

You should finish this module able to design aggregate roots, projections, policies,
and adapters that preserve coherence without creating god objects.
