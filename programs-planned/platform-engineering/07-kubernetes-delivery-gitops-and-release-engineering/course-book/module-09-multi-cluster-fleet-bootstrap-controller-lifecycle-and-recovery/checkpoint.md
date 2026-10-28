# Checkpoint — Fleet delivery and recovery

## Required evidence

- A canonical cluster catalogue.
- A topology-aware promotion wave plan.
- Controller and CRD upgrade evidence.
- A clean recovery proof with expired bootstrap authority.

## Decision defense

- Defend central versus per-cluster reconciliation.
- Explain source outage versus retirement.
- Explain why Git is necessary but insufficient for recovery.

## Progression gate

Advance only when one fleet metadata or controller failure cannot silently become platform-wide deletion or credential expansion.
