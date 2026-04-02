# Module 06: Persistence and Schema Evolution

Objects do not stop being objects when they cross a process boundary. This module
teaches how to persist aggregates, serialize state, and evolve stored representations
without letting storage concerns dissolve the domain model.

## Why this module matters

Many Python systems start with a clean object model and lose discipline the moment
they touch a database, a message payload, or a file format. Repositories become
opaque bags of side effects, JSON shapes leak into domain methods, and old data
silently becomes incompatible with new code.

This module treats persistence as another design boundary that must preserve object
semantics instead of flattening them away.

## Main questions

- What contract should a repository expose to the rest of the system?
- How do you translate between domain objects and storage records without leaking schemas inward?
- When should you serialize snapshots, events, or both?
- How do you version stored data and upgrade old representations safely?
- How do you detect conflicting writes without pretending concurrency does not exist?

## Reading path

1. Start with repository contracts, mappings, and codecs.
2. Then study snapshots, schema versioning, and conflict detection as one evolution cluster.
3. Move into transactional publication, testing, and migration strategy after the storage boundary is clear.
4. Finish with the refactor chapter to see persistence added without corrupting the domain.

## Common failure modes

- letting ORM or JSON models become the domain model by default
- exposing storage-specific identifiers and nullable columns directly to domain code
- changing a serialized shape without a compatibility plan for existing data
- persisting partially valid aggregates because repository code bypasses constructors
- treating write conflicts as impossible until production traffic proves otherwise

## Capstone connection

The monitoring capstone currently uses an in-memory repository and unit of work.
This module shows how that design can grow into file-backed, database-backed, or
message-driven persistence without changing who owns invariants. Read it as the bridge
between a teachable in-memory model and a production storage boundary.

## Outcome

You should finish this module able to add persistence, serialization, and schema
change to an object-oriented Python system without sacrificing aggregate integrity
or compatibility discipline.
