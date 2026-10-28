# Checkpoint — Module 01: Reliability Model and Critical Journeys

## Required result

Create the reliability case, critical-journey populations, failure modes, ownership, residual risk, and negative claims.

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

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Reliability Model and Critical Journeys** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Reliability Model and Critical Journeys**
- focused result for: Define critical journeys and eligible event populations.
- public, durable, security, or operational observation showing: The service gains a reliability case for create, submit, start, complete, retrieve, and notify journeys.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **critical-journey outcome classification**
- a limitation statement naming every live dependency required to support the strongest **Reliability Model and Critical Journeys** claim but not exercised

## Defend the design

1. Answer the central question: **Which user outcomes matter, what can prevent them, and which observation decides whether they succeeded?**
2. Demonstrate this capstone result: The service gains a reliability case for create, submit, start, complete, retrieve, and notify journeys.
3. Show the **Reliability Model and Critical Journeys** defect, the first failing oracle, and the exact regression retained after repair.
4. Explain why this invariant is shared across languages: eligible, good, bad, and excluded populations are defined before telemetry and tied to durable user outcomes.
5. State which environment-backed **Reliability Model and Critical Journeys** route was not run and how that limits the claim.

## Continue only when

Continue when the system again provides this module result—The service gains a reliability case for create, submit, start, complete, retrieve, and notify journeys.—all focused checks pass, the **Reliability Model and Critical Journeys** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
