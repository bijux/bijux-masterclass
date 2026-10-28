# API Engineering — Program Book

## The program promise

This program teaches API engineering as one cumulative discipline. You begin with messages on the wire and finish with a platform that helps many teams publish and consume trustworthy interfaces. Every layer is taught in the order in which it becomes necessary.

The sequence is deliberately conservative. You do not distribute a service before you can secure, observe, and measure it. You do not add GraphQL before service ownership is explicit. You do not build a platform before the contracts, releases, evidence, and consumer responsibilities it will govern actually exist.

## The learning arc

| Course | Responsibility | New object of reasoning |
|---:|---|---|
| 1 | [OpenAPI Contract Engineering](../01-openapi-contract-engineering/course-book/index.md) | Specify the public promise | What exactly does the API promise, and how can providers and consumers verify that promise? |
| 2 | [Contract-Driven API Service Engineering](../02-contract-driven-api-service-engineering/course-book/index.md) | Implement the promise durably | Which application, database, worker, storage, and release mechanisms keep the public contract true under concurrency, restart, and partial failure? |
| 3 | [API Security Engineering](../03-api-security-engineering/course-book/index.md) | Defend the promise | How does the API remain trustworthy when callers, credentials, inputs, destinations, dependencies, and networks cannot be trusted by default? |
| 4 | [API Reliability and Observability Engineering](../04-api-reliability-and-observability-engineering/course-book/index.md) | Observe, diagnose, contain, and recover the promise | How do operators know whether the user promise is still true, and how do they recover it without making the incident worse? |
| 5 | [API Performance, Capacity, and Traffic Engineering](../05-api-performance-capacity-and-traffic-engineering/course-book/index.md) | Sustain the promise under pressure | Where do time and capacity go, what is the first limiting resource, and which measured change improves the system without weakening correctness? |
| 6 | [Event-Driven API Engineering](../06-event-driven-api-engineering/course-book/index.md) | Extend the promise across asynchronous time | How can independent producers and consumers share durable facts without confusing intent, delivery attempts, processing effects, and historical truth? |
| 7 | [gRPC and Protobuf Engineering](../07-grpc-and-protobuf-engineering/course-book/index.md) | Engineer typed internal invocation and streaming | How should typed internal capabilities be modeled and operated when remote calls can fail ambiguously, stream for long periods, and evolve across language boundaries? |
| 8 | [Distributed API Architecture and Microservices Engineering](../08-distributed-api-architecture-and-microservices-engineering/course-book/index.md) | Distribute ownership deliberately | When does a remote service boundary create more value than the coordination, latency, consistency, security, release, and operational costs it introduces? |
| 9 | [GraphQL Schema and Runtime Engineering](../09-graphql-schema-and-runtime-engineering/course-book/index.md) | Compose governed client-shaped capabilities | How can clients select graph-shaped data and operations without moving business ownership, authorization, cost, or consistency into an uncontrolled gateway? |
| 10 | [API Platform, Governance, and Developer Experience Engineering](../10-api-platform-governance-and-developer-experience-engineering/course-book/index.md) | Operate APIs as an organizational platform | How can an organization make trustworthy API work easier to discover, create, publish, consume, evolve, support, and retire without centralizing domain ownership? |

## One cumulative platform

The capstone is the **Analysis Runs Platform**. A client creates a project, registers or uploads a dataset, submits an analysis, observes durable progress, retrieves a verified artifact, and receives an integration event or webhook. Later courses add typed RPC, service extraction, GraphQL composition, and platform publication without inventing a new domain.

Keeping one domain matters. It makes trade-offs visible. An idempotency key introduced in Course 1 becomes a database record in Course 2, an abuse boundary in Course 3, an operational signal in Course 4, a load-control input in Course 5, an event effect identity in Course 6, an RPC retry guard in Course 7, a cross-service workflow concern in Course 8, a mutation guarantee in Course 9, and a governance requirement in Course 10.

## How the books are organized

Every course has eight guide pages, one orientation module, and ten numbered modules. Every numbered module contains:

1. `index.md` — the authoritative self-contained chapter;
2. `exercises.md` — twelve transfer and design questions;
3. `exercise-answers.md` — matching reasoned answers;
4. `lab.md` — one controlled experiment with a falsifiable oracle;
5. `checkpoint.md` — non-compensable evidence required before progression.

The implementation tree is supporting material. Read the chapter first, predict the expected behavior, and then inspect only the paths named by the lab or chapter.

## What this program does not promise

The repository provides reference implementations and bounded proof routes. It does not claim that local fixtures are an operated identity provider, production broker, multi-region platform, or enterprise control plane. Each course names its evidence boundary so a learner can distinguish a demonstrated mechanism from an environment-dependent operational claim.

Continue with [Start here](start-here.md).
