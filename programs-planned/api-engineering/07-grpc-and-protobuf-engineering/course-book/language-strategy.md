# Python and TypeScript strategy

Course 7 keeps one contract and two idiomatic implementations.

## Python track

The Python track includes checked-in descriptor-backed generated-equivalent modules, a real gRPC server and client, interceptors, application adapters, stream handlers, and network tests. It is the complete live reference available in the build environment.

## TypeScript track

The TypeScript track includes complete contract models, wire helpers, deadline and retry policy, status mapping, bounded stream primitives, authorization policy, service catalogue, and in-process conformance tests. An optional `@grpc/grpc-js` adapter and proto-loader integration are included for a provisioned environment.

## What parity means

Parity means agreement on method paths; message field numbers, types, presence, oneof, and enum semantics; golden bytes where declared; metadata policy; status mapping; deadline, retry, and idempotency behavior; frame order and flow control; security decisions; health transitions; and release outcomes.

It does not mean matching class names, async primitives, or folder layouts.
