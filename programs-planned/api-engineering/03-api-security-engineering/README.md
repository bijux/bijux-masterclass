# API Security Engineering

**Course 3 of 10 — Defend the promise**

Derive, implement, and adversarially verify security properties around the durable service without replacing engineering judgment with middleware or scanner output.

> How does the API remain trustworthy when callers, credentials, inputs, destinations, dependencies, and networks cannot be trusted by default?

## Begin here

1. [Course book](course-book/index.md)
2. [Start here](course-book/start-here.md)
3. [Study plan](course-book/study-plan.md)
4. [Capstone](course-book/capstone.md)
5. [Orientation](course-book/module-00-orientation/index.md)

The course book is the authoritative learner product. The implementation, tests, fixtures, reports, and release records support its claims.

## Version boundary

API 1.2 preserved; Security Profile 1.0 introduced; migrations 001–007.

## Commands

```bash
make doctor
make core-proof
make manifest-proof
```

Live infrastructure routes are separate from dependency-light proofs and must be reported as not executed when their environment is absent.
