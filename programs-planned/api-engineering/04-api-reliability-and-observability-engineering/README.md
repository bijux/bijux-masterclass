# API Reliability and Observability Engineering

**Course 4 of 10 — Observe, diagnose, contain, and recover the promise**

Make failures observable and recoverable through explicit budgets, lifecycle states, telemetry meaning, service-level objectives, fault experiments, and reconciliation.

> How do operators know whether the user promise is still true, and how do they recover it without making the incident worse?

## Begin here

1. [Course book](course-book/index.md)
2. [Start here](course-book/start-here.md)
3. [Study plan](course-book/study-plan.md)
4. [Capstone](course-book/capstone.md)
5. [Orientation](course-book/module-00-orientation/index.md)

The course book is the authoritative learner product. The implementation, tests, fixtures, reports, and release records support its claims.

## Version boundary

API 1.2 and Security Profile 1.0 preserved; Reliability Profile 1.0 introduced; migrations 001–008.

## Commands

```bash
make doctor
make core-proof
make manifest-proof
```

Live infrastructure routes are separate from dependency-light proofs and must be reported as not executed when their environment is absent.
