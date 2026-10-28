# gRPC and Protobuf Engineering

**Course 7 of 10 — Engineer typed internal invocation and streaming**

Design and verify Protobuf schemas and gRPC interactions without pretending that generated stubs turn remote calls into local functions.

> How should typed internal capabilities be modeled and operated when remote calls can fail ambiguously, stream for long periods, and evolve across language boundaries?

## Begin here

1. [Course book](course-book/index.md)
2. [Start here](course-book/start-here.md)
3. [Study plan](course-book/study-plan.md)
4. [Capstone](course-book/capstone.md)
5. [Orientation](course-book/module-00-orientation/index.md)

The course book is the authoritative learner product. The implementation, tests, fixtures, reports, and release records support its claims.

## Version boundary

HTTP API 1.2 and Events API 1.0 preserved; RPC API 1.0 introduced; proto3 baseline; Edition 2024 frontier; migrations 001–015.

## Commands

```bash
make doctor
make core-proof
make manifest-proof
```

Live infrastructure routes are separate from dependency-light proofs and must be reported as not executed when their environment is absent.
