# Checkpoint — Module 09: Fault Injection, Troubleshooting, and Game Days

## Required result

Design bounded faults, control populations, abort conditions, cleanup contracts, and proof-sensitive planted defects.

## Demonstrate

- Predict the failure and first oracle before injection.
- Control blast radius and synthetic tenants.
- Diagnose from user journey to durable state to telemetry.
- Prove alerts and runbooks are sensitive to planted defects.
- Verify cleanup mechanically.

## Commands

```bash
make module-proof MODULE=09
make core-proof
```

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Fault Injection, Troubleshooting, and Game Days** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Fault Injection, Troubleshooting, and Game Days**
- focused result for: Predict the failure and first oracle before injection.
- public, durable, security, or operational observation showing: A stalled-worker game day burns run-start freshness while API availability remains healthy, then recovers without duplicate completion.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **bounded fault injection and diagnosis**
- a limitation statement naming every live dependency required to support the strongest **Fault Injection, Troubleshooting, and Game Days** claim but not exercised

## Defend the design

1. Answer the central question: **Can the system and its operators detect a controlled failure, find the durable cause, mitigate it, and return to a verified steady state?**
2. Demonstrate this capstone result: A stalled-worker game day burns run-start freshness while API availability remains healthy, then recovers without duplicate completion.
3. Show the **Fault Injection, Troubleshooting, and Game Days** defect, the first failing oracle, and the exact regression retained after repair.
4. Explain why this invariant is shared across languages: faults have hypotheses, blast-radius guards, abort conditions, cleanup, and an oracle that distinguishes the intended failure.
5. State which environment-backed **Fault Injection, Troubleshooting, and Game Days** route was not run and how that limits the claim.

## Continue only when

Continue when the system again provides this module result—A stalled-worker game day burns run-start freshness while API availability remains healthy, then recovers without duplicate completion.—all focused checks pass, the **Fault Injection, Troubleshooting, and Game Days** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
