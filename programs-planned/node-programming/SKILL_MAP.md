# Node.js Skill Map

## Course 1 entry

Basic programming in another language: values, branches, loops, functions, collections, and simple tests.

## Course 1 exit / Course 2 entry

You can build a strict TypeScript ESM package, distinguish static and runtime facts, validate external JSON, model domain state, own promise lifecycles, persist a versioned file, and test library and process behavior.

## Course 2 exit / Course 3 entry

You can reason through descriptors, prototypes, receivers, construction, private brands, symbols, iteration, reflection, object graphs, cloning, persistence records, and deterministic cleanup.

## Course 3 exit / Course 4 entry

You can preserve relationships through generics and type computation, emit and inspect declarations, publish restrained ESM entry points, validate runtime values into inferred static outputs, and review source, type, runtime, package, error, and data compatibility separately.

## Course 4 exit / Course 5 entry

You can:

- distinguish readiness, execution, settlement, product completion, and process completion;
- derive partial scheduling orders without depending on incidental traces;
- own every started promise and preserve rejection causes;
- compose caller cancellation, parent shutdown, and one absolute deadline;
- design typed event contracts without turning observers into state authority;
- inject clocks and test timing without probabilistic sleeps;
- implement bounded async iterables with explicit close behavior;
- propagate small immutable diagnostic context without hiding authorization;
- supervise lazy tasks under bounded admission and active-work limits;
- account for every accepted task with one terminal result;
- model startup rollback and graceful shutdown as explicit state machines;
- test real process signals, output, cleanup, and exit status;
- implement a cross-layer async feature from an impact map.

This is the prerequisite for Course 5. Streams introduce byte and object buffering, producer-consumer backpressure, and resource-heavy pipelines; those mechanisms require the task ownership and lifecycle discipline established here.

## Course 5 exit / Course 6 entry

You can:

- distinguish `Buffer`, `Uint8Array`, backing stores, copies, and views;
- name byte representations and hash domains precisely;
- implement Readable, Writable, Duplex, and Transform contracts without confusing events with product completion;
- reason about byte-mode and object-mode capacity units;
- preserve backpressure through manual writes and `pipeline` ownership;
- express streaming sequences through Node streams, async iterables, and Web Stream adapters with explicit close behavior;
- own file handles, staged candidates, synchronization, replacement, and cleanup while stating durability limits honestly;
- frame NDJSON incrementally under encoded-byte limits and fatal UTF-8 validation;
- compose compression, hashing, counting, and validation without collapsing their representation domains;
- supervise direct child processes with bounded stdin, stdout, and retained stderr policies;
- coordinate required branches and distinguish one-file replacement from multi-file publication;
- prove chunk-boundary independence, terminal record accounting, deterministic output, and preservation of an existing destination after failure;
- evolve FlowLedger through a cross-layer rejects-bundle or equivalent feature.

This is the prerequisite for Course 6. HTTP bodies, sockets, connection admission, and service shutdown are sustained dataflow systems; they require the byte, pressure, framing, process, and publication discipline established here.

## Cross-program comparison

| Skill | Node.js/TypeScript emphasis | Rust emphasis |
|---|---|---|
| object identity | references, prototypes, descriptors, private brands, proxies | ownership, borrowing, trait objects, interior mutability |
| type relationships | structural assignability, inference, conditional/mapped types, declarations | traits, associated types, lifetimes, generic bounds |
| absence/failure | `undefined`, unions, exceptions, rejected promises, validation | `Option`, `Result`, panic boundaries |
| cleanup | `try/finally`, abort listeners, explicit disposal, process ownership | RAII, `Drop`, ownership scopes |
| async ownership | promises, event loop, abort signals, task registries | futures, runtimes, cancellation, structured task ownership |
| package contract | ESM resolution, `exports`, declarations, npm artifacts | crates, modules, features, semver, Cargo artifacts |

Cross-standardization preserves a shared reasoning discipline while allowing each language’s strongest mechanisms to remain visible.


## Course 6 exit / Course 7 entry

After Course 6, you can:

- separate logical identity, address resolution, transport endpoints, TLS identity, and authorization;
- reconstruct bounded application messages from arbitrary TCP chunks;
- design correlated UDP request/response behavior with duplicate and stale-message policy;
- implement strict HTTP method, header, body, status, and response-completion semantics;
- place routing and runtime validation before one application commit authority;
- use idempotency keys and semantic fingerprints to handle ambiguous commit;
- design pooled clients with one deadline, bounded responses, explicit redirects, safe retries, and owned close;
- configure and test trust anchors, hostname verification, SNI, and ALPN;
- distinguish HTTP/2 session state from independent stream state and capacity;
- provide bounded SSE replay, heartbeat, slow-consumer, and disconnect behavior;
- map every service queue and retained structure to a unit, owner, and bound;
- implement startup rollback and quiesce, drain, abort, join, and report shutdown.

Course 7 may add durable databases, migrations, queues, and distributed workflows only after these network and semantic boundaries are stable. Durable idempotency, persisted events, and multi-instance coordination must strengthen rather than silently replace the Course 6 contracts.
