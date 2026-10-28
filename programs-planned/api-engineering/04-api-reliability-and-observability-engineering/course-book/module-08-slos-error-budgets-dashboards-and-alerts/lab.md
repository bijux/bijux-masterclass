# Lab — Module 08: SLOs, Error Budgets, Dashboards, and Alerts

> **Module 08:** SLOs, Error Budgets, Dashboards, and Alerts

## Objective

Calculate rolling SLOs and error budgets, implement multiwindow burn-rate alerts, build a journey-first dashboard, link alerts to tested runbooks, and reject an unobservable release.

## Why this lab matters

This lab turns the module’s governing question—**How do versioned SLOs, exact error budgets, burn rates, dashboards, alerts, and runbooks drive decisions?**—into a falsifiable experiment. Apply Objective, Error budget, Rolling window to this module’s capstone increment: Calculate rolling SLOs and error budgets, implement multiwindow burn-rate alerts, build a journey-first dashboard, link alerts to tested runbooks, and reject an unobservable release. State one misleading green signal and the durable observation that would overrule it.

It advances the cumulative Analysis Runs Platform by requiring this result: **Publish five journey SLOs, multiwindow alerts, owner-linked runbooks, and release policy**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **One run can be followed from client request through worker attempt, artifact publication, outbox dispatch, and receiver acknowledgement.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do operational signals become explicit objectives and actionable decisions rather than decorative dashboards?*

## Hypothesis

The clean implementation should satisfy this claim: **Short transient alone does not page under the paired rule; Sustained burn pages with journey, severity, SLO, and runbook; No data is not green; Budget math uses exact eligible and bad counts; The unobservable release is rejected while a documented repair path remains possible.** When the lab introduces this fault—**Inject a brief spike that fails the fast window but not the slow window**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Calculate exact budget remaining for each SLO.
2. Inject a brief spike that fails the fast window but not the slow window.
3. Inject sustained bad events that satisfy both windows.
4. Verify the alert links to the correct runbook and owner.
5. Stop SLI input and confirm the dashboard reports stale/no data.
6. Evaluate the rejected release and a controlled repair-release exception.

### Required planted defect

Remove or bypass the central control for **SLOs, Error Budgets, Dashboards, and Alerts** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Inject a brief spike that fails the fast window but not the slow window**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Calculate rolling SLOs and error budgets, implement multiwindow burn-rate alerts, build a journey-first dashboard, link alerts to tested runbooks, and reject an unobservable release**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- Short transient alone does not page under the paired rule.
- Sustained burn pages with journey, severity, SLO, and runbook.
- No data is not green.
- Budget math uses exact eligible and bad counts.
- The unobservable release is rejected while a documented repair path remains possible.

## Required evidence

- baseline transcript proving the previous checkpoint before **SLOs, Error Budgets, Dashboards, and Alerts** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **SLOs, Error Budgets, Dashboards, and Alerts**
- focused result for: Choose objectives from critical journeys.
- public, durable, security, or operational observation showing: Five versioned SLOs, burn alerts, dashboards, and runbooks govern the Analysis Runs service.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **SLO and alert mathematics**
- a limitation statement naming every live dependency required to support the strongest **SLOs, Error Budgets, Dashboards, and Alerts** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **SLOs, Error Budgets, Dashboards, and Alerts**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Inject a brief spike that fails the fast window but not the slow window** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Restore healthy event population.
2. Resolve the synthetic alert with evidence.
3. Remove release exception after the exercise.
4. Retain alert timeline, runbook transcript, and budget report.

## Completion gate

The lab is complete only when every listed oracle passes after repair, cleanup restores the stated steady state, and `make module-proof MODULE=08` succeeds on the primary track.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **SLOs, Error Budgets, Dashboards, and Alerts**. A green command without the negative case and causal explanation does not satisfy this gate.
