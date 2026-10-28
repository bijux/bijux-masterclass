# The Node.js Reasoning Model

The program uses one cumulative model. Later courses add dimensions; they do not discard earlier ones.

## 1. Runtime value and representation

Name the actual runtime entity: primitive, object, function, promise, iterator, signal, listener, timer, `Buffer`, typed-array view, stream, file handle, child process, socket, worker, native handle, or module namespace.

For byte-oriented work, also name the representation: raw file bytes, compressed bytes, decoded text, framed record, validated object, canonical bytes, or published file. Two values may describe the same logical information while having different byte identities and hashes.

## 2. Static contract

State what TypeScript established, which source and target types participated, how inference operated, and what remains unproved after type erasure. A `Buffer` type does not prove length, ownership, encoding, framing, or trust.

## 3. Authority

Identify the one parser, constructor, module, store, scheduler, protocol state machine, stream owner, transaction, package entry point, or migration allowed to establish each fact. Observation is not authority: a counter can report bytes without owning publication, and an event can report a transition without authoring it.

## 4. Identity, aliasing, and mutation

Distinguish domain identity, reference identity, backing-store identity, view identity, prototype identity, private brand, persisted identity, schema identity, task identity, process identity, and attempt identity. State which aliases observe mutation and whether a returned byte sequence is a copy or a view.

## 5. Object operation

For an object operation, identify its property key and descriptor, prototype traversal, receiver, call or construct mode, symbol protocol, reflection boundary, and lifecycle consequence.

## 6. Type relationship

For a TypeScript operation, identify source and target types, generic relationships, inference-owning positions, conditional or mapped computation, producer and consumer positions, declaration output, and unsupported runtime claims.

## 7. Package and consumer surface

Trace:

```text
consumer specifier
  → package exports condition
  → declaration target
  → JavaScript target
  → internal module graph
  → runtime behavior
```

A file is not public merely because it exists. A type is not honest merely because it checks inside the producer package.

## 8. Scheduling and task ownership

For asynchronous work, record:

- what synchronous work runs before the first suspension;
- which operation makes the continuation ready;
- who owns the returned promise;
- which tasks may run concurrently;
- which capacity bounds admission and active work;
- which identity reconstructs deterministic output;
- who observes rejection and complete cleanup.

## 9. Dataflow, pressure, and buffering

For every pipeline edge, record:

| Question | Required answer |
|---|---|
| Representation | What exact values or bytes cross the edge? |
| Mode | Byte mode or object mode? What unit does capacity count? |
| Producer | Who may offer the next item? |
| Consumer | Who accepts it and signals temporary exhaustion? |
| Queue | Where can accepted-but-unprocessed state accumulate? |
| Bound | Which high-water mark or semantic limit constrains it? |
| Completion | Which promise or terminal state proves the edge is complete? |
| Failure | Who destroys sibling stages and preserves the causal error? |

Backpressure regulates connected queue growth; it does not automatically bound an unfinished line, decompressed expansion, diagnostic retention, child output, or a user-defined cache.

## 10. Network and protocol boundary

A network endpoint is not one value. Keep distinct:

- logical service identity;
- hostname and port;
- resolved address candidates;
- bound local address;
- peer address;
- authenticated TLS identity;
- application authorization.

For each protocol, record representation, state machine, semantic authority, capacities, time budget, failure taxonomy, and terminal evidence. TCP stream order does not create message boundaries. HTTP completion does not prove domain commit. A trusted certificate chain does not replace hostname verification.

## 11. Resource and publication lifecycle

Name acquisition, active use, terminal transition, cleanup, and publication separately for every resource:

```text
acquire
  → use under a named owner
  → stop accepting new work
  → finish or cancel in-flight work
  → close, destroy, or reap
  → publish candidate if all required owners agree
```

For files, distinguish pathname, open handle, written bytes, flushed stream, synchronized file, renamed destination, synchronized directory, and durability claim. For child processes, distinguish spawn, stdin completion, stdout/stderr completion, exit, close, signal termination, and reaping.

## 12. Cancellation, time, and lifecycle

Separate wall time, monotonic duration, deadline, timeout, retry delay, and process grace period. State which `AbortSignal` carries each request, where cancellation is checked, what completed effects survive cancellation, and who disposes listeners and timers.

Lifecycle analysis names startup acquisition, quiesce, drain, abort, complete join, report construction, output flush, and exit-status ownership separately.

## 13. Observation and context

Events and metrics report facts; they do not silently become state authority. Ambient context carries small diagnostic facts; it does not replace explicit authorization or domain arguments. Record publication timing, payload mutability, subscription ownership, context lifetime, cardinality, and whether live counters are advisory or authoritative.

## 14. Failure

Separate invalid source usage, malformed external data, encoding failure, framing failure, domain rejection, declaration/runtime mismatch, package resolution, asynchronous rejection, cancellation, timeout, pressure failure, stream destruction, child status, cleanup failure, commit failure, operating-system failure, and process termination.

A later cleanup error must not casually replace the earlier causal failure. A post-publication durability error must not be reported as though the old product were still visible.

## 15. Evidence

Choose the smallest evidence capable of falsifying the claim: compiler case, runtime case, descriptor assertion, type test, emitted declaration, consumer fixture, controlled scheduler, chunk-partition test, pressure trace, digest, staged-file inspection, child-process test, lifecycle report, compatibility fixture, or benchmark.

## Course-specific ledgers

| Course | Additional ledger |
|---:|---|
| 1 | runtime, static contract, authority, mutation, failure, time, and evidence |
| 2 | descriptor, prototype, receiver, brand, protocol, graph, and lifecycle |
| 3 | source/target, inference, type computation, variance, declaration, package path, and compatibility |
| 4 | schedule, promise ownership, deadline, cancellation, event, context, capacity, and process lifecycle |
| 5 | representation, backing store, chunk, queue, pressure, framing, resource tree, digest domain, terminal state, and commit point |
| 6 | protocol, connection, admission, deadline, and service lifecycle |
| 7 | persistence authority, transaction, message delivery, and distributed state |
| 8 | worker ownership, synchronization, partitioning, and performance |
| 9 | threat, signal, test evidence, artifact, and rollout |
| 10 | platform boundary, extension, compatibility, and ecosystem evolution |


Course 6 adds the endpoint, protocol, capacity, deadline, idempotency, TLS-identity, session/stream, replay, and shutdown ledgers. These are refinements of the same model: representation, authority, bounded state, failure, and terminal evidence.
