# Distributed API Architecture and Microservices Engineering

**Course 8 of 10 — Distribute ownership deliberately**

Use ownership and failure evidence to approve, reject, extract, operate, and reverse service boundaries without creating a distributed monolith.

> When does a remote service boundary create more value than the coordination, latency, consistency, security, release, and operational costs it introduces?

## Begin here

1. [Course book](course-book/index.md)
2. [Start here](course-book/start-here.md)
3. [Study plan](course-book/study-plan.md)
4. [Capstone](course-book/capstone.md)
5. [Orientation](course-book/module-00-orientation/index.md)

The course book is the authoritative learner product. The implementation, tests, fixtures, reports, and release records support its claims.

## Version boundary

HTTP API 1.2, Events API 1.0, and RPC API 1.0 preserved; distributed architecture profile 1.0 introduced; owner-local migration histories begin.

## Commands

```bash
make doctor
make core-proof
make manifest-proof
```

Live infrastructure routes are separate from dependency-light proofs and must be reported as not executed when their environment is absent.
