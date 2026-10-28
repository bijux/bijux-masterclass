# Reference — Sync, health, journey, and data gates

Sync asks whether owned live fields match desired state. Health asks whether resource-specific status indicates readiness or success. Journey asks whether users receive useful behavior. Data gates ask whether migration, fencing, backup, and restore conditions remain valid.

Release decisions should display each independently and never average them into one unexplained green state.

## Extended reader notes

**Sync** compares owned live fields with rendered desired fields. **Health** interprets resource status and observed generation. **Journey correctness** evaluates real user or system outcomes. **Data correctness** evaluates writer authority, migration compatibility, integrity, backup, and restore.

These signals form neither substitutes nor a simple sequence. A synchronized Deployment may be unhealthy because no replicas are available. A healthy workload may be wrong because it returns corrupted metadata. Journeys may pass while restore evidence is expired. During a dependency incident, a workload may be intentionally degraded but still operating according to policy.

Release dashboards should expose each population separately with source, time, and subject. The final categorical decision can summarize them, but it must preserve failed, review-required, unavailable, and not-executed components.
