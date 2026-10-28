# Deterministic broker model

The executable deterministic broker lives in the two reference tracks:

- `../../tracks/python-fastapi/src/event_engineering/broker.py`
- `../../tracks/typescript-fastify/src/event-engineering/broker.ts`

This directory names the transport-independent proof surface. The local model deliberately exposes publication, delivery attempts, acknowledgement, negative acknowledgement, redelivery, per-partition offsets, and dead-letter transitions without requiring an external broker. It is the governing semantic oracle for dependency-light tests. NATS JetStream is an optional environment-backed transport and must satisfy the same observable invariants.
