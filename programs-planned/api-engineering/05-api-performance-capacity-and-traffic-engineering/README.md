# API Performance, Capacity, and Traffic Engineering

**Course 5 of 10 — Sustain the promise under pressure**

Measure, model, and control latency, throughput, resource use, fairness, and overload behavior with comparable evidence.

> Where do time and capacity go, what is the first limiting resource, and which measured change improves the system without weakening correctness?

## Begin here

1. [Course book](course-book/index.md)
2. [Start here](course-book/start-here.md)
3. [Study plan](course-book/study-plan.md)
4. [Capstone](course-book/capstone.md)
5. [Orientation](course-book/module-00-orientation/index.md)

The course book is the authoritative learner product. The implementation, tests, fixtures, reports, and release records support its claims.

## Version boundary

API 1.2, Security Profile 1.0, and Reliability Profile 1.0 preserved; Performance Profile 1.0 introduced; migrations 001–009.

## Commands

```bash
make doctor
make core-proof
make manifest-proof
```

Live infrastructure routes are separate from dependency-light proofs and must be reported as not executed when their environment is absent.
