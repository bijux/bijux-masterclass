# OpenAPI Contract Engineering

Prism is excluded from the installable toolchain because its dependency chain
has unresolved security advisories. Mock/proxy lessons and fixtures remain as
reference material. `make prism-mock` and `make prism-smoke` stop with an explicit
error; `npm run mock` and `npm run proxy:python` are unavailable. Full course
qualification remains blocked until a maintained replacement is qualified.

**Course 1 of 10 — Specify the public promise**

Define a precise, reviewable, executable HTTP API contract without confusing a description, a framework, and a running provider.

> What exactly does the API promise, and how can providers and consumers verify that promise?

## Begin here

1. [Course book](course-book/index.md)
2. [Start here](course-book/start-here.md)
3. [Study plan](course-book/study-plan.md)
4. [Capstone](course-book/capstone.md)
5. [Orientation](course-book/module-00-orientation/index.md)

The course book is the authoritative learner product. The implementation, tests, fixtures, reports, and release records support its claims.

## Version boundary

Public API 1.1; OpenAPI 3.1.2 executable baseline; OpenAPI 3.2.0 standards frontier; no durable database yet.

## Commands

```bash
make doctor
make core-proof
make manifest-proof
```

Live infrastructure routes are separate from dependency-light proofs and must be reported as not executed when their environment is absent.
