# Lab — Module 09: Fault Injection, Troubleshooting, and Game Days

> **Module 09:** Fault Injection, Troubleshooting, and Game Days

## Objective

Build deterministic fault profiles, an evidence-first troubleshooting method, a controlled game day, stop conditions, cleanup verification, and planted defects proving the checks are sensitive.

## Why this lab matters

This lab turns the module’s governing question—**How can fault injection and game days produce falsifiable evidence without creating uncontrolled damage?**—into a falsifiable experiment. Apply Steady-state hypothesis, Fault model, Blast radius to this module’s capstone increment: Build deterministic fault profiles, an evidence-first troubleshooting method, a controlled game day, stop conditions, cleanup verification, and planted defects proving the checks are sensitive. State one misleading green signal and the durable observation that would overrule it.

It advances the cumulative Analysis Runs Platform by requiring this result: **Design bounded faults, control populations, abort conditions, cleanup contracts, and proof-sensitive planted defects**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **Five versioned SLOs, burn alerts, dashboards, and runbooks govern the Analysis Runs service.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *Can the system and its operators detect a controlled failure, find the durable cause, mitigate it, and return to a verified steady state?*

## Hypothesis

The clean implementation should satisfy this claim: **API availability may remain healthy while run-start freshness fails; Durable accepted jobs remain present and recoverable; Telemetry loss reduces diagnosis quality but not correctness; Mitigation stops budget burn without duplicate completion; Cleanup and reconciliation report no unresolved critical finding.** When the lab introduces this fault—**Plant one missing alert or misleading dashboard panel and demonstrate detection**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Inject worker claim delay while leaving API health green.
2. Observe run-start freshness burn and queue-age alert.
3. Diagnose from accepted run to durable job and worker claim evidence.
4. Introduce a telemetry-export drop as a secondary fault only after primary diagnosis.
5. Mitigate safely, recover workers, and run read-only reconciliation.
6. Plant one missing alert or misleading dashboard panel and demonstrate detection.

### Required planted defect

Remove or bypass the central control for **Fault Injection, Troubleshooting, and Game Days** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Plant one missing alert or misleading dashboard panel and demonstrate detection**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Build deterministic fault profiles, an evidence-first troubleshooting method, a controlled game day, stop conditions, cleanup verification, and planted defects proving the checks are sensitive**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- API availability may remain healthy while run-start freshness fails.
- Durable accepted jobs remain present and recoverable.
- Telemetry loss reduces diagnosis quality but not correctness.
- Mitigation stops budget burn without duplicate completion.
- Cleanup and reconciliation report no unresolved critical finding.

## Required evidence

- baseline transcript proving the previous checkpoint before **Fault Injection, Troubleshooting, and Game Days** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Fault Injection, Troubleshooting, and Game Days**
- focused result for: Predict the failure and first oracle before injection.
- public, durable, security, or operational observation showing: A stalled-worker game day burns run-start freshness while API availability remains healthy, then recovers without duplicate completion.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **bounded fault injection and diagnosis**
- a limitation statement naming every live dependency required to support the strongest **Fault Injection, Troubleshooting, and Game Days** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Fault Injection, Troubleshooting, and Game Days**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Plant one missing alert or misleading dashboard panel and demonstrate detection** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Disable all injector profiles and verify control endpoint state.
2. Drain or resolve synthetic jobs and deliveries.
3. Release permits and remove temporary data.
4. Publish timeline, hypotheses, evidence, remediation, and retained regression.

## Completion gate

The lab is complete only when every listed oracle passes after repair, cleanup restores the stated steady state, and `make module-proof MODULE=09` succeeds on the primary track.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Fault Injection, Troubleshooting, and Game Days**. A green command without the negative case and causal explanation does not satisfy this gate.
