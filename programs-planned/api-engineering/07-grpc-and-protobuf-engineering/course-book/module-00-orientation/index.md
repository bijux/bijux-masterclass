# Orientation — Lock the asynchronous predecessor and prepare the RPC laboratory

Course 7 begins by verifying, not rewriting, the Course 6 handoff. The public HTTP API, event contract, migrations 001–012, security and operational profiles, and event ownership remain fixed.

## Orientation outcomes

You will:

- verify every predecessor file against its manifest;
- inspect the HTTP, event, state, and ownership boundaries inherited from Course 6;
- choose a primary language track;
- run descriptor, Python, TypeScript, and source audits;
- distinguish dependency-light and environment-backed proof routes;
- confirm that gRPC is an internal addition rather than a replacement public API.

## Commands

```bash
make doctor
make predecessor-proof
make orientation-proof
make capstone-tour
```

## Readiness questions

Before Module 1, explain:

1. why a timed-out mutation may still have committed;
2. why a worker stream cannot replace durable leases;
3. why an internal progress frame is not automatically a public integration event;
4. why an HTTP resource API should not be replaced solely because gRPC is typed;
5. why field numbers become permanent once bytes are published.

If any answer is uncertain, revisit the predecessor material before continuing.


## Laboratory boundary

All attack, failure, and traffic experiments are confined to the checked-in local fixtures and processes that you start for this course. Do not point retry storms, malformed streams, credential tests, reflection tools, or certificate experiments at systems you do not own and explicitly control.

The fixture tokens, keys, and insecure local channel exist only to make mechanisms reproducible. They are intentionally recognizable and must never be copied into a real deployment. A live production profile requires an operated identity system, certificate lifecycle, secret storage, network policy, database, observability, and incident ownership.

Before beginning, create a clean working copy and record:

- Python, Node, TypeScript, gRPC, and Protobuf runtime versions;
- whether `protoc`, Buf, grpcurl, MkDocs, PostgreSQL, and TLS tooling are available;
- which language is your primary implementation track;
- which environment-backed proofs will remain not executed;
- the digest of the predecessor handoff.

This record prevents a common learning failure: treating a missing tool as a failed concept or treating a simulator as production evidence.
