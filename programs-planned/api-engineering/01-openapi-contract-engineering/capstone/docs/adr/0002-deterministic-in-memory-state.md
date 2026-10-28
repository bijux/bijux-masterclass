# ADR 0002: deterministic in-memory state

**Status:** accepted

## Context

Asynchronous work, idempotency, concurrency, and ownership usually interact with persistence and queues. Those systems make a ten-day course harder to run and easier to fail for unrelated reasons.

## Decision

Use process-local deterministic state and advance run status on retrieval. Reset state by restarting the provider.

## Consequences

The capstone proves protocol and contract semantics, not durability or distributed execution. State transitions remain explicit, reproducible, and testable in both languages.
