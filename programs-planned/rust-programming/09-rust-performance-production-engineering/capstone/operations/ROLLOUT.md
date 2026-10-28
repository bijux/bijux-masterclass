# MetricRail Rollout and Rollback

## Before rollout

- build the exact distribution artifact;
- verify artifact and lockfile digests;
- run behavior, load, security, installation, and rollback checks;
- freeze configuration;
- confirm dashboards, alerts, and runbook ownership;
- record the previous artifact and configuration.

## Stages

1. Offline corpus verification.
2. Shadow or non-authoritative execution.
3. Canary with a small bounded population.
4. Expansion in measured steps.
5. Full promotion after the observation window.

## Promotion criteria

- no semantic mismatch;
- accepted p95 and p99 within the declared objective;
- no unexplained memory trend;
- rejection within policy;
- readiness stable;
- no secret or cardinality regression;
- artifact and configuration identity confirmed.

## Rollback criteria

- correctness mismatch;
- readiness failure;
- error-budget burn above the rollout threshold;
- memory or queue growth without recovery;
- security or diagnostic disclosure;
- incompatible protocol or configuration behavior.

Rollback restores both artifact and compatible configuration. It has been rehearsed in a clean environment before canary traffic.
