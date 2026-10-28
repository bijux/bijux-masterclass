# GraphQL Schema and Runtime Engineering

Course 9 adds a graph interface to the distributed Analysis Runs Platform built in Courses 1–8. The goal is not to replace HTTP, events, RPC, or service ownership. The goal is to let clients select a typed response shape while the runtime preserves every guarantee already earned by the platform.

A GraphQL schema is an executable capability model. A field is not merely documentation: it is a promise about type, nullability, authorization, cost, source authority, and failure behavior. A resolver is not a convenient database callback: it is an adapter from a graph field to the service that owns the fact or decision. A query is not harmless because it is read-only: its shape can cause fan-out, repeated work, sensitive-field exposure, and partial failure.

The course follows one cumulative question:

> How can a client-shaped graph remain safe, bounded, observable, and compatible over independently owned services?

## Ten-day path

1. Place GraphQL correctly and trace the operation lifecycle.
2. Design a truthful type system and nullability contract.
3. Implement resolvers that preserve ownership and batch remote work.
4. Build stable queries, identifiers, connections, and cursors.
5. Delegate mutations without losing idempotency or concurrency control.
6. Enforce authorization at every field and tenant boundary.
7. Bound arbitrary demand with validation, trusted documents, and cost policy.
8. Model errors, null propagation, partial data, consistency, and telemetry.
9. Connect subscriptions to durable events with resume and gap detection.
10. Evolve, compose, govern, and defend the graph release.

Begin with [Start here](start-here.md).
