# Language Strategy — gRPC and Protobuf Engineering

## Strategy

Choose one primary track for the complete build and lab repairs. Use the second as an idiomatic comparison and shared-vector parity reference. The course deliberately avoids making learners type the same architecture twice.

## What must match

- public messages and documented statuses;
- named state, security, reliability, performance, event, RPC, architecture, graph, or governance decisions owned by this course;
- canonical bytes when signatures, digests, wire compatibility, or cross-language identity depends on them;
- accepted, rejected, and review-required release classifications;
- shared negative vectors and evidence boundaries.
- the Course 7 outcome: Analysis RPC API 1.0, gRPC Profile 1.0, proto3 executable baseline, Edition 2024 frontier, migrations 013–015, streaming protocols, method policy, and compatibility evidence.

## What may differ

generated APIs, async iterators, 64-bit representations, interceptors, and channel libraries differ; compare wire bytes, metadata, status, deadlines, and stream state.

## Reading implementation examples

For each example:

1. name the invariant before reading code;
2. identify the owner and state boundary;
3. find the negative test;
4. find cleanup and failure behavior;
5. compare the second track only after you can explain the first;
6. never infer a protocol rule from one framework default.
