# Lab — Module 01: Reliability Model and Critical Journeys

## Objective

Derive the reliability case for six Analysis Runs journeys and connect every reliability requirement to one failure mode and one proof route.


## Setup conditions

The previous baseline is: **the orientation baseline** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *Which user outcomes matter, what can prevent them, and which observation decides whether they succeeded?*

## Failure action and investigation

1. Map every API operation and asynchronous stage to at least one journey.
2. Define good, bad, eligible, and excluded events for every SLO.
3. Plant a component-only availability claim that ignores stalled jobs.
4. Run traceability and show why the weak claim is inadequate.
5. Repair the model and record residual risk for each environment-dependent proof.

### Required planted defect

Remove or bypass the central control for **Reliability Model and Critical Journeys** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

## Operational oracle

- Every active REL requirement has a source and proof.
- Stalled jobs fail run-start freshness while API health remains green.
- Provider-owned 5xx and timeout outcomes cannot be excluded.
- Durable state decides terminal correctness.

## Required evidence

- baseline transcript proving the previous checkpoint before **Reliability Model and Critical Journeys** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Define critical journeys and eligible event populations.
- public, durable, security, or operational observation showing: The service gains a reliability case for create, submit, start, complete, retrieve, and notify journeys.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **critical-journey outcome classification**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Remove the weak planted claim.
2. Regenerate the reliability-case report.
3. Retain only deterministic YAML and Markdown evidence.

## Completion gate

The lab is complete only when every listed oracle passes after repair, cleanup restores the stated steady state, and `make module-proof MODULE=01` succeeds on the primary track.
