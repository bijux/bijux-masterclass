# Standards and tool profile

## Canonical executable baseline

Analysis RPC API 1.0 uses proto3 syntax for broad Python and TypeScript generator support. The repository also contains an Editions 2024 frontier example and a capability matrix. Editions are studied as the current language-evolution model, but the executable baseline does not claim every selected generator supports every frontier feature.

## gRPC semantics

The course follows the official gRPC models for unary, client-streaming, server-streaming, and bidirectional RPCs; canonical status codes; deadlines and cancellation; retry configuration; health checking; reflection; and wait-for-ready.

## Schema governance

The full toolchain uses Buf for lint and breaking-change detection and protoc-compatible generators. The dependency-light proof uses checked-in descriptor JSON, golden bytes, and a local policy checker. The local checker’s scope is stated precisely; it is not presented as Buf or full compiler conformance.

## Current tool pins

See `tool-versions.json`. Tool versions are reproducibility evidence, not part of the RPC API version.

## Reading discipline

Normative specifications answer what the protocol promises. Runtime documentation answers how one implementation exposes it. Every chapter identifies which claims are normative, course-profile-specific, implementation-specific, or illustrative.


## Contract and runtime layers

The course uses four layers of authority:

1. **Protobuf source** defines packages, fields, numbers, enums, services, and method shapes.
2. **gRPC profile** defines metadata, status, deadline, retry, stream, health, and security behavior that the proto alone cannot express.
3. **Application contract** defines state ownership, idempotency, authorization, and durable effects.
4. **Release evidence** proves selected generators, runtimes, consumers, and deployments satisfy the first three layers.

A compiler success covers only part of layer one. A generated client call covers part of layers one and two. Database and cross-protocol tests are needed for layers three and four.

## Tool capability policy

The executable baseline is chosen for broad, reproducible support. The Editions 2024 source is a standards-frontier artifact. Each capability is recorded separately:

- parse;
- lint;
- generate;
- compile generated source;
- run unary;
- run each stream shape;
- preserve optional presence and unknown fields;
- expose reflection;
- perform breaking-change analysis.

A tool may support some and not others. The course never writes “supports Protobuf” as a substitute for this matrix.

## Selected external references

The complete chapters are self-contained. For normative confirmation and future changes, consult:

- Protocol Buffers language and Editions documentation;
- gRPC concepts, deadlines, cancellation, status codes, retry, health, reflection, and wait-for-ready documentation;
- Buf lint and breaking-change documentation;
- HTTP, OpenAPI, AsyncAPI, OAuth, security, reliability, and performance sources inherited from Courses 1–6.

External references update implementation details; the course’s engineering invariants remain stable.
