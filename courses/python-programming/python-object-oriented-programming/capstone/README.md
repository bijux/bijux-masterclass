# Python Object-Oriented Programming Capstone

This capstone is a compact monitoring-system reference implementation. It exists to
make the course concrete: value objects, entities, rule lifecycles, aggregate roots,
domain events, projections, and unit-of-work boundaries are all exercised in runnable
code instead of only in chapter prose.

## What it models

- threshold-based monitoring rules with explicit lifecycle states
- a `MonitoringPolicy` aggregate root that owns rule transitions and evaluation
- domain events for registration, activation, retirement, and alert triggering
- a projection that tracks active rules per metric
- an in-memory unit of work with rollback semantics

## Run it

From this directory:

```bash
make confirm
```

Or from the repository root:

```bash
make COURSE=python-programming/python-object-oriented-programming test
```

## Design intent

The implementation deliberately stays small. The goal is not framework breadth. The
goal is to demonstrate a Python object model that remains readable under change:

- value types stay immutable and validated
- aggregates own invariants instead of scattering them
- events describe what happened without mutating projections directly
- repositories and unit-of-work boundaries make persistence intent explicit

## Layout

- `src/service_monitoring/` contains the domain and supporting infrastructure.
- `tests/` contains executable behavioral checks.
