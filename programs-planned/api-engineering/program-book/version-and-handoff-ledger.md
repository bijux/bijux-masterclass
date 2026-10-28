# Version and Handoff Ledger

## Independent version axes

The program never uses “version” without naming the axis. The important axes are independent:

- **interface specification version** — for example OpenAPI 3.1.2 or AsyncAPI 3.1.0;
- **public API version** — the semantics consumers depend on, such as API 1.1 or 1.2;
- **service release version** — a deployable implementation release;
- **database migration revision** — the ordered durable-schema history;
- **engineering profile version** — security, reliability, performance, or event policy shared across artifacts.

A service release can change without changing the public API. A migration can expand storage while both old and new service releases coexist. A new profile can strengthen proof requirements while preserving request and response schemas.

## Program ledger

| Course | Public interfaces | Profiles | Migration head | Handoff purpose |
|---:|---|---|---:|---|
| 1 | HTTP API 1.1; OpenAPI 3.1.2 baseline and 3.2.0 frontier | — | — | Freeze the public promise and provider-neutral evidence. |
| 2 | API 1.1 preserved; compatible HTTP API 1.2 added | — | 005 | Freeze the durable-service mechanisms and API 1.2 behavior. |
| 3 | HTTP API 1.2 preserved | Security 1.0 | 007 | Freeze security requirements, policy, vectors, and sanitized public identity material. |
| 4 | HTTP API 1.2 preserved | Security 1.0; Reliability 1.0 | 008 | Freeze critical journeys, telemetry semantics, SLOs, alerts, and runbooks. |
| 5 | HTTP API 1.2 preserved | Security 1.0; Reliability 1.0; Performance 1.0 | 009 | Freeze workloads, comparison rules, traffic policy, and capacity assumptions. |
| 6 | HTTP API 1.2 preserved; Analysis Events API 1.0 added | Security 1.0; Reliability 1.0; Performance 1.0; Event 1.0 | 012 | Freeze event contracts, envelopes, catalogue, replay policy, and consumer declarations. |

## Handoff discipline

Every predecessor directory is read-only evidence. A current course may add an explicitly compatible release or profile; it must not rewrite the earlier contract to make implementation easier. Each outgoing handoff contains only material required by the next responsibility:

- public contracts and operation ownership;
- shared fixtures and deterministic vectors;
- ordered migrations;
- profile and policy records;
- sanitized examples and public keys;
- release and evidence metadata.

Private fixture keys, runtime caches, generated logs, local databases, environment secrets, and unbounded reports do not belong in a handoff.

## How to review a change

When a file changes, ask which version axis it belongs to. Then ask which consumers, service releases, migrations, profiles, tests, and handoffs must move with it. A change is incomplete when the code advances but the version ledger, contract, evidence, or migration coexistence story does not.
