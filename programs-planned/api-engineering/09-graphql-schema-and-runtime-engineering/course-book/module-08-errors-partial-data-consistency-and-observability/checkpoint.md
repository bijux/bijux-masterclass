# Checkpoint 08 — Errors, Partial Data, Consistency, and Observability

Do not continue until every condition is supported by executable or inspected evidence.

- [ ] Request errors prevent execution; execution errors identify exact response paths and can coexist with partial data.
- [ ] Nullable remote fields fail as null plus structured errors, while non-null failures bubble to the nearest nullable ancestor.
- [ ] Unavailable data is never represented as an authoritative empty list.
- [ ] Staleness and observation time are visible where the graph serves eventually consistent projections.
- [ ] Telemetry records bounded operation and field coordinates without object IDs or sensitive variables as metric labels.
- [ ] Lab 08 correlates one controlled source outage across data, errors, traces, service calls, and cache behavior.

**Gate:** run `make module-08-proof`. A green command without the lab report and the listed evidence does not count.
