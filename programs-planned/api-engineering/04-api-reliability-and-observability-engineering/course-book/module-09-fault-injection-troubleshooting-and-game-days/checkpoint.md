# Checkpoint — Module 09: Fault Injection, Troubleshooting, and Game Days

## Required result

A stalled-worker game day burns run-start freshness while API availability remains healthy, then recovers without duplicate completion.

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

## Defend the design

1. Answer the central question: **Can the system and its operators detect a controlled failure, find the durable cause, mitigate it, and return to a verified steady state?**
2. Demonstrate this capstone result: A stalled-worker game day burns run-start freshness while API availability remains healthy, then recovers without duplicate completion.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: faults have hypotheses, blast-radius guards, abort conditions, cleanup, and an oracle that distinguishes the intended failure.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—A stalled-worker game day burns run-start freshness while API availability remains healthy, then recovers without duplicate completion.—all focused checks pass, the **Fault Injection, Troubleshooting, and Game Days** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
