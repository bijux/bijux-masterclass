# Lab — Module 08: SLOs, Error Budgets, Dashboards, and Alerts

## Objective

Calculate rolling SLOs and error budgets, implement multiwindow burn-rate alerts, build a journey-first dashboard, link alerts to tested runbooks, and reject an unobservable release.


## Setup conditions

The previous baseline is: **One run can be followed from client request through worker attempt, artifact publication, outbox dispatch, and receiver acknowledgement.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do operational signals become explicit objectives and actionable decisions rather than decorative dashboards?*

## Failure action and investigation

1. Calculate exact budget remaining for each SLO.
2. Inject a brief spike that fails the fast window but not the slow window.
3. Inject sustained bad events that satisfy both windows.
4. Verify the alert links to the correct runbook and owner.
5. Stop SLI input and confirm the dashboard reports stale/no data.
6. Evaluate the rejected release and a controlled repair-release exception.

### Required planted defect

Remove or bypass the central control for **SLOs, Error Budgets, Dashboards, and Alerts** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

## Operational oracle

- Short transient alone does not page under the paired rule.
- Sustained burn pages with journey, severity, SLO, and runbook.
- No data is not green.
- Budget math uses exact eligible and bad counts.
- The unobservable release is rejected while a documented repair path remains possible.

## Required evidence

- baseline transcript proving the previous checkpoint before **SLOs, Error Budgets, Dashboards, and Alerts** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Choose objectives from critical journeys.
- public, durable, security, or operational observation showing: Five versioned SLOs, burn alerts, dashboards, and runbooks govern the Analysis Runs service.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **SLO and alert mathematics**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore healthy event population.
2. Resolve the synthetic alert with evidence.
3. Remove release exception after the exercise.
4. Retain alert timeline, runbook transcript, and budget report.

## Completion gate

The lab is complete only when every listed oracle passes after repair, cleanup restores the stated steady state, and `make module-proof MODULE=08` succeeds on the primary track.
