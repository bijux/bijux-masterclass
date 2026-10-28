# Glossary — Contract-Driven API Service Engineering

Use this glossary alongside `program-book/glossary.md`. Program terms keep one meaning across all six courses; the entries below add course-specific distinctions.

Terms are defined as used in this program. When an Internet or OpenAPI specification gives a narrower normative meaning, the chapter and standards page name it.

## Use case

An application-level behavior that coordinates domain rules and ports for one business outcome without depending on HTTP or a database driver.

## Port

An interface owned by the application or domain that describes a required capability.

## Adapter

A framework, database, storage, or network implementation of a port.

## Composition root

The single place where concrete adapters, configuration, and application services are assembled.

## Domain invariant

A rule that must remain true regardless of transport, persistence, process, or language.

## State machine

An explicit set of states and legal transitions with defined guards and effects.

## Repository

An application-facing persistence abstraction whose methods align with transactional use cases rather than tables alone.

## Migration

An ordered, owned change to database structure or durable data, recorded exactly once.

## Constraint

A database rule—such as uniqueness, foreign key, check, or nullability—that rejects invalid durable state.

## Transaction boundary

The set of reads and writes that must commit or roll back atomically for one application decision.

## Isolation

The database behavior controlling how concurrent transactions observe and conflict with one another.

## Optimistic concurrency

A conditional update that succeeds only when the version read by the caller remains current.

## Persistent idempotency

Durable binding of operation, principal, key, request fingerprint, and stored response so retries survive restart.

## Request fingerprint

A deterministic digest of the operation and canonical request identity used to detect conflicting idempotency-key reuse.

## Cursor

An opaque or server-managed continuation position bound to one ordered query traversal.

## High-water position

The maximum eligible ordering position captured when a traversal begins, preventing later inserts from entering that traversal.

## Lease

Time-bounded ownership of a durable job that another worker may recover after expiry.

## Fencing token

A monotonically changing ownership generation used to reject effects from stale workers.

## At-least-once execution

A delivery or work model in which an item may be attempted more than once, requiring idempotent effects.

## Staging

Writing content to a non-public temporary location before validation and atomic publication.

## Content-addressed storage

Storage in which the key derives from the content digest, allowing integrity checks and idempotent publication.

## Transactional outbox

A durable event record committed in the same transaction as the domain state it announces.

## Inbox deduplication

Receiver-side durable tracking that prevents repeated delivery identifiers from applying an effect twice.

## Expand/backfill/enforce

A compatible migration sequence that first adds permissive structure, populates data, and only then tightens constraints.

## Coexistence window

The deployment period during which old and new service versions must both operate against an expanded schema.

## Durable oracle

A database or storage observation authoritative enough to decide whether a behavior survived failure.

## Modular monolith

One deployable application with explicit internal boundaries; it is not a synonym for unstructured code.

## Public model

A request or response shape governed by the API contract and kept separate from persistence rows.

## Rollback limit

A point after which application or schema rollback is unsafe without a forward repair.

## Proof sensitivity

The demonstrated ability of a verification route to fail when the mechanism it claims to test is deliberately broken.
