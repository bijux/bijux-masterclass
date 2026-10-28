# Python and TypeScript strategy

Course 8 teaches distributed invariants, not framework imitation.

## Choose one primary track

Implement and modify either:

```text
capstone/tracks/python-distributed
```

or:

```text
capstone/tracks/typescript-distributed
```

Use the other track for comparative review and shared-vector parity.

## Python reference

The Python track emphasizes:

- dataclasses for explicit architecture records;
- enums for state machines;
- deterministic clocks and in-memory transports;
- visible exceptions and transaction-like decisions;
- tests that narrate failure schedules;
- straightforward inspection of owner state.

It is useful for tracing one saga and reconciliation decision step by step.

## TypeScript reference

The TypeScript track emphasizes:

- discriminated unions and exact state values;
- `ReadonlySet` and immutable declarations for ownership;
- safe representation of identifiers and versions;
- explicit runtime validation despite static types;
- promise and cancellation boundaries;
- strict compilation across cross-service models.

It is useful for seeing how structural compatibility can still admit semantically invalid data when runtime checks are missing.

## Required parity

Both tracks must agree on:

- approved, conditional, retained, and rejected boundaries;
- service catalogue and owner classification;
- one-writer data ownership;
- monotonic projection behavior;
- dependency graph cycle and depth rejection;
- saga states, effect identity, and compensation;
- capability claims and validation outcomes;
- route phase behavior;
- version-skew classification;
- extraction transitions;
- reconciliation findings;
- final externally visible outcomes.

They need not agree on:

- package layout;
- class or interface names;
- exception hierarchy;
- dependency-injection style;
- asynchronous primitives;
- testing library syntax.

## Translation exercise

For each module, translate one mechanism—not the whole codebase—into the comparative language. Good candidates are:

- boundary decision function;
- graph cycle detector;
- monotonic projection apply function;
- capability verifier;
- saga transition;
- stable canary router;
- reconciliation finding generator.

Then compare which invariant is enforced statically, dynamically, or only by tests.

## Framework boundary

The executable core is intentionally framework-light. Optional adapters and topology examples show where FastAPI, Fastify, gRPC, HTTP clients, databases, and Kubernetes enter. The architecture should remain understandable without a framework runtime.

A framework route or client call is never the source of business ownership. It adapts a contract to an application decision.
