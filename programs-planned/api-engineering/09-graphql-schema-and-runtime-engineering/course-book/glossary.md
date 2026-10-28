# Glossary — GraphQL Schema and Runtime Engineering

These terms have precise meanings in Course 9. Use them with the program glossary at `program-book/glossary.md`, which preserves shared meanings across the complete sequence.

## schema

The GraphQL type system and root operation definitions that describe selectable fields, inputs, results, and relationships.

## object type

A named GraphQL type whose fields can be selected when the runtime value has that object type.

## interface

An abstract type declaring fields shared by implementing object types and resolved to a concrete runtime type.

## union

An abstract result that may be one of several object types without requiring common fields beyond `__typename`.

## nullability

The type-level statement of whether a field may return null and how null propagates through non-null parents.

## resolver

Runtime logic that obtains or computes one field while preserving source ownership, policy, batching, and error semantics.

## field source

The authoritative service or computation responsible for the fact exposed by a GraphQL field.

## batch loader

A request-scoped mechanism that combines multiple field keys into bounded source calls and caches only within the safe request context.

## global ID

An opaque, type-aware identifier used by the graph to route node lookup without exposing or authorizing by raw database keys.

## connection

A pagination model containing edges, nodes, and page information over a stable ordered traversal.

## edge

A connection entry that pairs one node with its traversal cursor and optional relationship metadata.

## cursor

An opaque, integrity-protected continuation token bound to tenant, audience, field, filters, ordering, high-water position, and expiry.

## mutation

A root operation that requests a state-changing command while preserving the source service’s validation, idempotency, and concurrency rules.

## client mutation ID

A caller-supplied correlation value echoed in a mutation result; it is not automatically an idempotency key.

## persisted operation

A reviewed GraphQL document admitted by exact identity rather than accepting arbitrary production query text.

## demand cost

A pre-execution estimate of structural work, list cardinality, source fan-out, or other bounded resource demand.

## partial data

A response containing valid fields alongside field-specific errors when the schema’s nullability permits unaffected data to survive.

## error path

The ordered response field and list-index path identifying exactly where a GraphQL execution error occurred.

## subscription

A long-lived operation producing multiple result events, with transport, resume, gap, buffering, and authorization policies.

## federation

A composition approach in which multiple subgraphs publish owned portions of a graph under explicit entity, field, and release rules.
