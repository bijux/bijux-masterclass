# Event-Driven API Engineering

**Course 6 of 10 — Extend the promise across asynchronous time**

Design, evolve, secure, operate, and verify asynchronous message contracts under delay, duplication, reordering, replay, and consumer failure.

> How can independent producers and consumers share durable facts without confusing intent, delivery attempts, processing effects, and historical truth?

## Begin here

1. [Course book](course-book/index.md)
2. [Start here](course-book/start-here.md)
3. [Study plan](course-book/study-plan.md)
4. [Capstone](course-book/capstone.md)
5. [Orientation](course-book/module-00-orientation/index.md)

The course book is the authoritative learner product. The implementation, tests, fixtures, reports, and release records support its claims.

## Version boundary

HTTP API 1.2 preserved; Analysis Events API 1.0 introduced; AsyncAPI 3.1.0; CloudEvents 1.0-compatible profile; migrations 001–012.

## Commands

```bash
make doctor
make core-proof
make manifest-proof
```

Live infrastructure routes are separate from dependency-light proofs and must be reported as not executed when their environment is absent.
