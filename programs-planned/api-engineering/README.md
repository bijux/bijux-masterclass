# API Engineering

## Six courses, one platform, one progressively stronger engineering story

This program follows the **Analysis Runs Platform** from its first public HTTP message to a governed asynchronous event API. Each course inherits the exact public artifacts and engineering constraints established by the previous course. The system becomes more capable without pretending that a new library erases an earlier responsibility.

```text
01  Specify the promise
        ↓
02  Make the promise durable
        ↓
03  Defend the promise
        ↓
04  Operate and recover the promise
        ↓
05  Sustain the promise under pressure
        ↓
06  Extend the promise across asynchronous time
```

The course books are the primary product. Capstones, language tracks, fixtures, laboratories, and proof routes exist to make the explanations executable.

## The six courses

| Course | Responsibility | Governing question |
|---:|---|---|
| 1 | [OpenAPI Contract Engineering](01-openapi-contract-engineering/course-book/index.md) | What exactly does the API promise, and how can providers and consumers verify that promise? |
| 2 | [Contract-Driven API Service Engineering](02-contract-driven-api-service-engineering/course-book/index.md) | Which internal mechanisms keep the public contract true under concurrency, restart, and partial failure? |
| 3 | [API Security Engineering](03-api-security-engineering/course-book/index.md) | How does the service remain trustworthy under hostile behavior without hiding behind middleware or scanner output? |
| 4 | [API Reliability and Observability Engineering](04-api-reliability-and-observability-engineering/course-book/index.md) | How do operators know whether the user promise is still true, and how do they recover it without making the incident worse? |
| 5 | [API Performance, Capacity, and Traffic Engineering](05-api-performance-capacity-and-traffic-engineering/course-book/index.md) | Where does time and capacity go, what is the first limiting resource, and which measured change improves the system without weakening its promise? |
| 6 | [Event-Driven API Engineering](06-event-driven-api-engineering/course-book/index.md) | How can independent producers and consumers share durable facts without confusing intent, delivery attempts, processing effects, and historical truth? |


## How to begin

1. Read the [program introduction](program-book/index.md).
2. Use [Start here](program-book/start-here.md) to choose a learning route and implementation track.
3. Follow the [six-course journey](program-book/six-course-journey.md); do not skip predecessor gates casually.
4. Keep the [platform story](program-book/analysis-runs-platform.md) open while studying so every mechanism remains connected to one real system.
5. Use the [evidence model](program-book/evidence-model.md) to distinguish a contract claim, durable-state claim, security claim, operational claim, performance claim, and event-delivery claim.

## Program scale

- six dense two-week courses;
- 60 numbered teaching modules plus six orientation modules;
- one continuous capstone;
- Python/FastAPI and TypeScript/Fastify reference tracks;
- OpenAPI, JSON Schema, PostgreSQL, security, reliability, performance, AsyncAPI, and CloudEvents artifacts;
- exercises, worked answers, failure-oriented labs, checkpoints, and final defenses.

## Verification

```bash
make doctor
make release-proof
make core-proof
make manifest-proof
make docs-build  # when MkDocs and the pinned theme are installed
```

A dependency-light proof establishes only the properties it actually executes. Live PostgreSQL, broker, network, documentation-rendering, and external-tool routes remain separate and are never converted into synthetic passes when their environment is absent.
