# Course 7 — gRPC and Protobuf Engineering

This is the seventh course in the Bijux Masterclass API Engineering program.

It continues the same Analysis Runs Platform built through contracts, durable service implementation, security, reliability, performance, and event-driven integration. Course 7 adds a typed internal RPC control plane without replacing the public HTTP API or the durable Event API.

## Governing responsibility

> Engineer strongly typed unary and streaming RPC boundaries with safe wire evolution, deadlines, cancellation, retries, security, lifecycle, and release evidence.

## Start

```bash
make help
make doctor
make predecessor-proof
make core-proof
make capstone-tour
```

Then read [`course-book/start-here.md`](course-book/start-here.md).

## Learner product

The authoritative product is `course-book/`: 59 navigated pages, ten complete modules, 120 exercises with matching worked answers, ten failure-oriented labs, and ten evidence checkpoints.

The capstone, Python and TypeScript tracks, proto contracts, vectors, migrations, and proof scripts support that book. They do not replace it.

## Course boundary

The course preserves:

- Public HTTP API 1.2 and OpenAPI 3.1.2
- Analysis Events API 1.0 and AsyncAPI 3.1.0
- Security, reliability, and performance profiles 1.0
- migrations 001–012

It adds:

- Analysis RPC API 1.0
- proto3 executable baseline
- Protobuf Editions 2024 design frontier
- gRPC Service Profile 1.0
- migrations 013–015
- a service-boundary dossier for Course 8

The course does **not** assume that adding gRPC justifies microservices.
