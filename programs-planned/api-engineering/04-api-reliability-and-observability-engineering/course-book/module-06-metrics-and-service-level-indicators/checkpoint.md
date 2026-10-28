# Checkpoint — Module 06: Metrics and Service-Level Indicators

## Required result

The capstone exports bounded metrics and SLIs for availability, run start, completion, artifact access, and webhook delivery.

## Demonstrate

- Choose metric instruments from the measured quantity.
- Control label dimensions and series count.
- Measure latency distributions rather than averages.
- Define good, bad, eligible, and excluded events.
- Use durable timestamps for asynchronous journey indicators.

## Commands

```bash
make module-proof MODULE=06
make core-proof
```

## Defend the design

1. Answer the central question: **Which numeric observations describe user outcomes without exploding cardinality or hiding the tail?**
2. Demonstrate this capstone result: The capstone exports bounded metrics and SLIs for availability, run start, completion, artifact access, and webhook delivery.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: instrument type, labels, eligibility, good/bad classification, and reset handling are explicit and bounded.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—The capstone exports bounded metrics and SLIs for availability, run start, completion, artifact access, and webhook delivery.—all focused checks pass, the **Metrics and Service-Level Indicators** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
