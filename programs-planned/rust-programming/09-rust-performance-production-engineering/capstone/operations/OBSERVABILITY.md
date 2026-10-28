# MetricRail Observability Contract

## Operational questions

Signals must answer:

- Is the process alive?
- Is it ready to admit new work?
- Are queues or connection permits saturated?
- Are records rejected as malformed, overloaded, or invalid domain transitions?
- Is queue residence or service time driving latency?
- Is series or identifier retention approaching a limit?
- Are snapshots failing because of size or broker availability?
- Which artifact and profile are running?

## Span hierarchy

```text
connection
└── command
    ├── ingest
    ├── snapshot
    ├── health
    └── quit
```

Stable fields include connection ID, command kind, outcome class, observed queue depth, series count, and record bytes. Tenant, metric, payload, and credentials are excluded by default.

## Metrics

Counters:

- accepted records;
- invalid rejections;
- overload rejections;
- completed snapshots.

Gauges:

- active connections observed;
- queue depth observed.

These gauges are advisory. The broker store is authoritative for series state.

## Health

Liveness means the process can answer. Readiness additionally requires the listener and broker to be available and the service not to be quiescing. A degraded snapshot policy, if enabled, must be represented explicitly rather than reported as fully healthy.

## Redaction

Production events must not contain raw telemetry values, tenant names, metric names, authorization material, or input lines. Tests inspect diagnostic output for representative secrets.
