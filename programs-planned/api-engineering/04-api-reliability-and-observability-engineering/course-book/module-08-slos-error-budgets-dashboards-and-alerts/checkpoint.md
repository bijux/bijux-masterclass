# Checkpoint — Module 08: SLOs, Error Budgets, Dashboards, and Alerts

## Required result

Five versioned SLOs, burn alerts, dashboards, and runbooks govern the Analysis Runs service.

## Demonstrate

- Choose objectives from critical journeys.
- Calculate compliance and remaining error budget.
- Use multiwindow burn-rate alerts.
- Design dashboards from outcomes to causes.
- Handle insufficient data and planned exclusions explicitly.

## Commands

```bash
make module-proof MODULE=08
make core-proof
```

## Defend the design

1. Answer the central question: **How do operational signals become explicit objectives and actionable decisions rather than decorative dashboards?**
2. Demonstrate this capstone result: Five versioned SLOs, burn alerts, dashboards, and runbooks govern the Analysis Runs service.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: objectives operate on exact eligible populations and multiwindow burn alerts require both fast and slow evidence with no-data handling.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—Five versioned SLOs, burn alerts, dashboards, and runbooks govern the Analysis Runs service.—all focused checks pass, the **SLOs, Error Budgets, Dashboards, and Alerts** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
