# Lab — Module 06: Metrics and Service-Level Indicators

> **Module 06:** Metrics and Service-Level Indicators

## Objective

Implement bounded counters, gauges, and histograms; define journey SLIs; add recording rules; and prove cardinality limits and event-population semantics.

## Why this lab matters

This lab turns the module’s governing question—**How are counters, gauges, histograms, and SLI populations defined so the math means what operators think it means?**—into a falsifiable experiment. Apply Metric instrument, Event population, Label dimension to this module’s capstone increment: Implement bounded counters, gauges, and histograms; define journey SLIs; add recording rules; and prove cardinality limits and event-population semantics. State one misleading green signal and the durable observation that would overrule it.

It advances the cumulative Analysis Runs Platform by requiring this result: **Implement bounded metric dimensions, units, good/bad/eligible/excluded populations, and aggregation semantics**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **API, worker, storage, and webhook paths emit consistent, privacy-safe operational events.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *Which numeric observations describe user outcomes without exploding cardinality or hiding the tail?*

## Hypothesis

The clean implementation should satisfy this claim: **Instrument type matches event semantics; Series count remains within declared maximum; Provider-owned failures remain in the denominator; Latency tail is visible in histogram buckets; Empty population reports insufficient data.** When the lab introduces this fault—**Remove or bypass the central control for Metrics and Service-Level Indicators in a temporary branch**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Record counters, gauges, and histograms in both cores.
2. Evaluate API availability, latency, run-start freshness, terminal correctness, and webhook freshness populations.
3. Enable the run-ID label and generate enough runs to exceed the series guard.
4. Confirm the guard fails before unbounded export.
5. Repair with bounded labels and trace correlation.
6. Evaluate empty, low-traffic, and counter-reset windows.

### Required planted defect

Remove or bypass the central control for **Metrics and Service-Level Indicators** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Remove or bypass the central control for Metrics and Service-Level Indicators in a temporary branch**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Implement bounded counters, gauges, and histograms; define journey SLIs; add recording rules; and prove cardinality limits and event-population semantics**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- Instrument type matches event semantics.
- Series count remains within declared maximum.
- Provider-owned failures remain in the denominator.
- Latency tail is visible in histogram buckets.
- Empty population reports insufficient data.

## Required evidence

- baseline transcript proving the previous checkpoint before **Metrics and Service-Level Indicators** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Metrics and Service-Level Indicators**
- focused result for: Choose metric instruments from the measured quantity.
- public, durable, security, or operational observation showing: The capstone exports bounded metrics and SLIs for availability, run start, completion, artifact access, and webhook delivery.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **metrics and SLI populations**
- a limitation statement naming every live dependency required to support the strongest **Metrics and Service-Level Indicators** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Metrics and Service-Level Indicators**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Remove or bypass the central control for Metrics and Service-Level Indicators in a temporary branch** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Remove the planted high-cardinality metric.
2. Reset the in-memory registry.
3. Regenerate recording-rule and SLI reports.
4. Retain series-growth evidence and repaired schema.

## Completion gate

The lab is complete only when every listed oracle passes after repair, cleanup restores the stated steady state, and `make module-proof MODULE=06` succeeds on the primary track.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Metrics and Service-Level Indicators**. A green command without the negative case and causal explanation does not satisfy this gate.
