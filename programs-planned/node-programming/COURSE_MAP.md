# Ten-Course Node.js Programming Map

| Course | Modules | Responsibility | Cumulative product | State |
|---:|---:|---|---|---|
| 1. Node.js and TypeScript Foundations | 1–10 | JavaScript semantics, strict TypeScript, ESM, validation, promises, files, tests, and complete programs | StudyLedger | available |
| 2. JavaScript Object Model and Runtime Protocols | 11–20 | Properties, prototypes, receivers, classes, private state, composition, symbols, iteration, reflection, cloning, and lifecycle | ObjectAtlas | available |
| 3. Advanced TypeScript and Library API Design | 21–30 | Structural assignability, generic relationships, type computation, variance, declarations, exports, schemas, and compatibility | SchemaKit | available |
| 4. Async Node.js and Event-Driven Architecture | 31–40 | Event loop, promise ownership, cancellation, events, clocks, async iteration, context, supervision, and shutdown | TaskHarbor | available |
| 5. Node.js Streams, Filesystems, and Data Pipeline Architecture | 41–50 | Buffers, stream state, backpressure, adapters, transactional files, bounded framing, compression, hashing, subprocesses, fan-out, and publication | FlowLedger | available |
| 6. Node.js Networking, HTTP, and Service Architecture | 51–60 | DNS and addresses, TCP/UDP, HTTP semantics, routing, clients, TLS, HTTP/2, SSE, admission, and service lifecycle | ServiceWire | available |
| 7. Persistence, Messaging, and Distributed Workflows | 61–70 | Databases, transactions, migrations, queues, idempotency persistence, delivery semantics, and workflow state | WorkRelay | planned |
| 8. Workers, Concurrency, and Performance | 71–80 | Worker threads, shared memory, process models, profiling, load, partitioning, and deterministic parallelism | ComputeGrid | planned |
| 9. Security, Observability, Testing, and Delivery | 81–90 | Threat models, dependency security, tracing, metrics, advanced tests, packaging, CI, and rollout | SignalGate | planned |
| 10. Platform and Ecosystem Architecture | 91–100 | Long-lived APIs, plugins, multi-package systems, native boundaries, governance, migration, and a large platform capstone | NodeFoundry | planned |

## Current authored boundary

Courses 1–6 are complete source courses. Courses 7–10 are curriculum boundaries only.

## Cumulative maturity

```text
Course 1: construct a complete strict Node.js program
Course 2: reason about JavaScript object identity and runtime protocols
Course 3: publish a trustworthy typed library
Course 4: own asynchronous work, cancellation, and process lifecycle
Course 5: own sustained byte flow, pressure, resources, and publication
Course 6: own network identity, protocol state, admission, retry, delivery, and service shutdown
```

Course 6 deliberately stops before durable storage and cross-process workflow. ServiceWire is process-local so that transport, HTTP, TLS, client, and lifecycle contracts remain visible. Course 7 will add persistence and distributed coordination without weakening those contracts.
