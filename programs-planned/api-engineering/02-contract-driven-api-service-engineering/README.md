# Contract-Driven API Service Engineering

**Course 2 of 10 — Implement the promise durably**

Turn the fixed Course 1 contract into a durable modular service whose important guarantees survive concurrent requests and process failure.

> Which application, database, worker, storage, and release mechanisms keep the public contract true under concurrency, restart, and partial failure?

## Begin here

1. [Course book](course-book/index.md)
2. [Start here](course-book/start-here.md)
3. [Study plan](course-book/study-plan.md)
4. [Capstone](course-book/capstone.md)
5. [Orientation](course-book/module-00-orientation/index.md)

The course book is the authoritative learner product. The implementation, tests, fixtures, reports, and release records support its claims.

## Version boundary

API 1.1 preserved; additive API 1.2 introduced; OpenAPI 3.1.2 preserved; migrations 001–005.

## Commands

```bash
make doctor
make core-proof
make manifest-proof
```

Live infrastructure routes are separate from dependency-light proofs and must be reported as not executed when their environment is absent.
