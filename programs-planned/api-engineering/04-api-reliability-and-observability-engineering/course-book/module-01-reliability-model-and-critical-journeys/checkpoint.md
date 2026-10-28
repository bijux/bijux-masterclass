# Checkpoint — Module 01: Reliability Model and Critical Journeys

## Required result

The service gains a reliability case for create, submit, start, complete, retrieve, and notify journeys.

## Demonstrate

- Define critical journeys and eligible event populations.
- Separate prevention, mitigation, repair, and verification.
- Choose public or durable correctness oracles before telemetry.
- Catalog failure modes and residual risks.
- Trace reliability requirements to tests, runbooks, and owners.

## Commands

```bash
make module-proof MODULE=01
make core-proof
```

## Defend the design

1. Answer the central question: **Which user outcomes matter, what can prevent them, and which observation decides whether they succeeded?**
2. Demonstrate this capstone result: The service gains a reliability case for create, submit, start, complete, retrieve, and notify journeys.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: eligible, good, bad, and excluded populations are defined before telemetry and tied to durable user outcomes.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—The service gains a reliability case for create, submit, start, complete, retrieve, and notify journeys.—all focused checks pass, the **Reliability Model and Critical Journeys** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
