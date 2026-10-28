# Final verification — Course 7

## Release identity

- Course: **gRPC and Protobuf Engineering**
- Program sequence: **7**
- Course release: **1.0.0**
- Analysis RPC API: **1.0**
- Protobuf executable baseline: **proto3**
- Protobuf standards frontier: **Edition 2024**
- migration head: **015**

## Learner-facing product

- course-book pages: **61**
- course-book words: **52,020**
- numbered modules: **10**, plus orientation
- exercises: **120**
- matching worked answers: **120**
- labs: **10**
- evidence checkpoints: **10**

## Executed release proof

The dependency-light proof was executed from the course root and passed:

- exact Course 6 predecessor handoff verification;
- reader-facing structure, answer identity, lab, and checkpoint checks;
- proto package, enum-zero, optional-presence, field-tag, service, and method checks;
- semantic parity between the checked descriptor and the Python runtime;
- interaction-boundary and service-ownership checks;
- golden wire, presence, int64, compatibility, status, deadline, retry, streaming, flow-control, security, and lifecycle vectors;
- migrations 001–015 and Python/TypeScript migration parity;
- **31 Python tests**, including a real local gRPC server and client;
- **18 TypeScript/Node tests** after strict TypeScript compilation;
- accepted and rejected RPC release fixtures;
- ten planted-defect assignments;
- exact outgoing Course 8 handoff verification;
- Markdown links, educational depth, and repository hygiene.

The live Python network tests cover unary calls, idempotent replay, safe status codes, authorization, server streaming, client streaming, artifact integrity, watch resumption, and worker hello validation.

## Explicitly unexecuted environment-backed routes

The build environment did not provide:

- independent `protoc` or `grpcio-tools` generation;
- Buf lint and breaking analysis;
- grpcurl reflection inspection;
- the registry-installed grpc-js/proto-loader network stack;
- a live mTLS certificate and rotation topology;
- PostgreSQL concurrency and migration-coexistence proof;
- strict MkDocs rendering;
- a multi-instance external resolver/load-balancer topology.

Their source, commands, expected oracles, and failure criteria are included. They are reported as **not executed**, not converted into passes.

## Evidence boundary

The in-memory reference proves application and protocol mechanisms but does not replace the durable PostgreSQL implementation profile inherited from Course 2. The deterministic TypeScript track proves cross-language semantics but not grpc-js transport behavior until its pinned optional dependencies are installed. The Editions 2024 file is a reviewed frontier artifact and is not labeled executable without an Editions-capable toolchain.

## Release decision

The course is approved as a complete self-learning Course 7 package. Its central release claim is bounded:

> Analysis RPC API 1.0 can be designed, executed through the Python live reference, compared across Python and TypeScript semantics, evolved, secured, operated, and introduced reversibly without changing the public HTTP API or durable Event API in the course profile.

See `reports/capability-execution.json` and `reports/release-verification.json` for machine-readable evidence.
