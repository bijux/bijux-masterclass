# API Engineering

## Ten courses, one platform, one progressively stronger engineering story

This program follows the **Analysis Runs Platform** from its first HTTP exchange to a governed multi-protocol API platform. The courses are not ten independent technology surveys. Each course receives an immutable handoff, preserves earlier guarantees, and adds one new engineering responsibility.

```text
01  Specify the public promise
02  Implement the promise durably
03  Defend the promise
04  Observe, diagnose, contain, and recover the promise
05  Sustain the promise under pressure
06  Extend the promise across asynchronous time
07  Engineer typed internal invocation and streaming
08  Distribute ownership deliberately
09  Compose governed client-shaped capabilities
10  Operate APIs as an organizational platform
```

The **course books are the primary product**. Capstones, code, fixtures, labs, and proof routes exist to make the explanations executable. Begin with [Start here](program-book/start-here.md), not by browsing implementation directories.

## The ten courses

| Course | Course book | Responsibility | Governing question |
|---:|---|---|---|
| 1 | [OpenAPI Contract Engineering](01-openapi-contract-engineering/course-book/index.md) | Specify the public promise | What exactly does the API promise, and how can providers and consumers verify that promise? |
| 2 | [Contract-Driven API Service Engineering](02-contract-driven-api-service-engineering/course-book/index.md) | Implement the promise durably | Which application, database, worker, storage, and release mechanisms keep the public contract true under concurrency, restart, and partial failure? |
| 3 | [API Security Engineering](03-api-security-engineering/course-book/index.md) | Defend the promise | How does the API remain trustworthy when callers, credentials, inputs, destinations, dependencies, and networks cannot be trusted by default? |
| 4 | [API Reliability and Observability Engineering](04-api-reliability-and-observability-engineering/course-book/index.md) | Observe, diagnose, contain, and recover the promise | How do operators know whether the user promise is still true, and how do they recover it without making the incident worse? |
| 5 | [API Performance, Capacity, and Traffic Engineering](05-api-performance-capacity-and-traffic-engineering/course-book/index.md) | Sustain the promise under pressure | Where do time and capacity go, what is the first limiting resource, and which measured change improves the system without weakening correctness? |
| 6 | [Event-Driven API Engineering](06-event-driven-api-engineering/course-book/index.md) | Extend the promise across asynchronous time | How can independent producers and consumers share durable facts without confusing intent, delivery attempts, processing effects, and historical truth? |
| 7 | [gRPC and Protobuf Engineering](07-grpc-and-protobuf-engineering/course-book/index.md) | Engineer typed internal invocation and streaming | How should typed internal capabilities be modeled and operated when remote calls can fail ambiguously, stream for long periods, and evolve across language boundaries? |
| 8 | [Distributed API Architecture and Microservices Engineering](08-distributed-api-architecture-and-microservices-engineering/course-book/index.md) | Distribute ownership deliberately | When does a remote service boundary create more value than the coordination, latency, consistency, security, release, and operational costs it introduces? |
| 9 | [GraphQL Schema and Runtime Engineering](09-graphql-schema-and-runtime-engineering/course-book/index.md) | Compose governed client-shaped capabilities | How can clients select graph-shaped data and operations without moving business ownership, authorization, cost, or consistency into an uncontrolled gateway? |
| 10 | [API Platform, Governance, and Developer Experience Engineering](10-api-platform-governance-and-developer-experience-engineering/course-book/index.md) | Operate APIs as an organizational platform | How can an organization make trustworthy API work easier to discover, create, publish, consume, evolve, support, and retire without centralizing domain ownership? |

## What completion means

A learner completes the program by demonstrating the final checkpoint of every course and defending one continuous architecture. Reading pages, running a single green command, or installing a tool is not completion. The final system must preserve public semantics, durable state, security, reliability, performance, asynchronous behavior, RPC compatibility, distributed ownership, graph demand controls, and platform governance at the same time.

## First commands

```bash
make doctor
make structure
make links
make quality
```

Environment-backed proofs remain separate from dependency-light proofs. Missing PostgreSQL, broker, container, documentation, or external standards tooling is recorded as **not executed**, never converted into a synthetic pass.
