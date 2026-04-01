# Capstone

The course capstone is a compact monitoring system that turns the book's design
claims into executable behavior across the full slice of the course, from value
objects and invariants up through projections, runtime orchestration, and failure
handling.

## What it demonstrates

- immutable value objects for metric names, samples, severities, and threshold rules
- a `MonitoringPolicy` aggregate root that owns registration, activation, retirement, and evaluation
- multiple evaluation strategies without pushing condition ladders into the aggregate
- domain events that describe lifecycle changes and triggered alerts
- read models for active rules and incident history without driving domain state
- a `MonitoringRuntime` facade that coordinates adapters, projections, and commits
- an in-memory unit of work that makes commit and rollback semantics explicit

## Run it

From the repository root:

```bash
make COURSE=python-programming/python-object-oriented-programming test
```

From the capstone directory:

```bash
make confirm
```

## Why it matters

The capstone keeps the course honest. If a chapter claims that aggregates should
own invariants, that strategies should carry evaluation variability, or that
projections should stay downstream of events, the code here shows that shape
directly and the tests enforce it.
