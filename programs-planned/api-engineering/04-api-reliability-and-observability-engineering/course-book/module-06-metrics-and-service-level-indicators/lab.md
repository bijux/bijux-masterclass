# Lab — Module 06: Metrics and Service-Level Indicators

## Objective

Implement bounded counters, gauges, and histograms; define journey SLIs; add recording rules; and prove cardinality limits and event-population semantics.


## Setup conditions

The previous baseline is: **API, worker, storage, and webhook paths emit consistent, privacy-safe operational events.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *Which numeric observations describe user outcomes without exploding cardinality or hiding the tail?*

## Failure action and investigation

1. Record counters, gauges, and histograms in both cores.
2. Evaluate API availability, latency, run-start freshness, terminal correctness, and webhook freshness populations.
3. Enable the run-ID label and generate enough runs to exceed the series guard.
4. Confirm the guard fails before unbounded export.
5. Repair with bounded labels and trace correlation.
6. Evaluate empty, low-traffic, and counter-reset windows.

### Required planted defect

Remove or bypass the central control for **Metrics and Service-Level Indicators** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

## Operational oracle

- Instrument type matches event semantics.
- Series count remains within declared maximum.
- Provider-owned failures remain in the denominator.
- Latency tail is visible in histogram buckets.
- Empty population reports insufficient data.

## Required evidence

- baseline transcript proving the previous checkpoint before **Metrics and Service-Level Indicators** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Choose metric instruments from the measured quantity.
- public, durable, security, or operational observation showing: The capstone exports bounded metrics and SLIs for availability, run start, completion, artifact access, and webhook delivery.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **metrics and SLI populations**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Remove the planted high-cardinality metric.
2. Reset the in-memory registry.
3. Regenerate recording-rule and SLI reports.
4. Retain series-growth evidence and repaired schema.

## Completion gate

The lab is complete only when every listed oracle passes after repair, cleanup restores the stated steady state, and `make module-proof MODULE=06` succeeds on the primary track.
