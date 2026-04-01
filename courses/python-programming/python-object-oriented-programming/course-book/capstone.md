# Capstone

The course capstone is a compact monitoring system that turns the book's design
claims into executable behavior.

## What it demonstrates

- immutable value objects for metric names, samples, severities, and threshold rules
- a `MonitoringPolicy` aggregate root that owns registration, activation, retirement, and evaluation
- domain events that describe lifecycle changes and triggered alerts
- a projection that tracks active rules by metric without driving domain state
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
own invariants or that projections should stay downstream of events, the code here
shows that shape directly and the tests enforce it.
