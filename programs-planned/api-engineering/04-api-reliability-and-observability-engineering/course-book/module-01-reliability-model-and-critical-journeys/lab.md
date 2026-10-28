# Lab — Module 01: Reliability Model and Critical Journeys

> **Module 01:** Reliability Model and Critical Journeys

## Objective

Derive the reliability case for six Analysis Runs journeys and connect every reliability requirement to one failure mode and one proof route.

## Why this lab matters

This lab turns the module’s governing question—**Which user journeys matter, what makes them good or bad, and which durable facts establish the outcome?**—into a falsifiable experiment. Apply Critical journey, Good, bad, eligible, excluded, Reliability invariant to this module’s capstone increment: Derive the reliability case for six Analysis Runs journeys and connect every reliability requirement to one failure mode and one verification. State one misleading green signal and the durable observation that would overrule it.

It advances the cumulative Analysis Runs Platform by requiring this result: **Create the reliability case, critical-journey populations, failure modes, ownership, residual risk, and negative claims**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **the orientation baseline** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *Which user outcomes matter, what can prevent them, and which observation decides whether they succeeded?*

## Hypothesis

The clean implementation should satisfy this claim: **Every active REL requirement has a source and proof; Stalled jobs fail run-start freshness while API health remains green; Provider-owned 5xx and timeout outcomes cannot be excluded; Durable state decides terminal correctness.** When the lab introduces this fault—**Plant a component-only availability claim that ignores stalled jobs**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Map every API operation and asynchronous stage to at least one journey.
2. Define good, bad, eligible, and excluded events for every SLO.
3. Plant a component-only availability claim that ignores stalled jobs.
4. Run traceability and show why the weak claim is inadequate.
5. Repair the model and record residual risk for each environment-dependent proof.

### Required planted defect

Remove or bypass the central control for **Reliability Model and Critical Journeys** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Plant a component-only availability claim that ignores stalled jobs**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Derive the reliability case for six Analysis Runs journeys and connect every reliability requirement to one failure mode and one proof route**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- Every active REL requirement has a source and proof.
- Stalled jobs fail run-start freshness while API health remains green.
- Provider-owned 5xx and timeout outcomes cannot be excluded.
- Durable state decides terminal correctness.

## Required evidence

- baseline transcript proving the previous checkpoint before **Reliability Model and Critical Journeys** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Reliability Model and Critical Journeys**
- focused result for: Define critical journeys and eligible event populations.
- public, durable, security, or operational observation showing: The service gains a reliability case for create, submit, start, complete, retrieve, and notify journeys.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **critical-journey outcome classification**
- a limitation statement naming every live dependency required to support the strongest **Reliability Model and Critical Journeys** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Reliability Model and Critical Journeys**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Plant a component-only availability claim that ignores stalled jobs** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Remove the weak planted claim.
2. Regenerate the reliability-case report.
3. Retain only deterministic YAML and Markdown evidence.

## Completion gate

The lab is complete only when every listed oracle passes after repair, cleanup restores the stated steady state, and `make module-proof MODULE=01` succeeds on the primary track.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Reliability Model and Critical Journeys**. A green command without the negative case and causal explanation does not satisfy this gate.
