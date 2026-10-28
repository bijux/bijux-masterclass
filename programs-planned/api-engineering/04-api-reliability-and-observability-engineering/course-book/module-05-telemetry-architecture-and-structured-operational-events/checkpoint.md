# Checkpoint — Module 05: Telemetry Architecture and Structured Events

## Required result

API, worker, storage, and webhook paths emit consistent, privacy-safe operational events.

## Demonstrate

- Separate logs, metrics, traces, and audit records by purpose.
- Use stable event names and fields.
- Propagate correlation and trace context safely.
- Bound queues and drop behavior.
- Treat telemetry as evidence about execution, not the authority on durable state.

## Commands

```bash
make module-proof MODULE=05
make core-proof
```

## Defend the design

1. Answer the central question: **What should the system record so an operator can reconstruct behavior without leaking secrets or blocking the request path?**
2. Demonstrate this capstone result: API, worker, storage, and webhook paths emit consistent, privacy-safe operational events.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: events use versioned names and bounded attributes, are recursively redacted, and never replace durable business records.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—API, worker, storage, and webhook paths emit consistent, privacy-safe operational events.—all focused checks pass, the **Telemetry Architecture and Structured Events** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
