# Lab — Module 10 lab — Conduct the final performance release review

> **Module 10:** Performance Regression and Release Engineering

## Objective

Evaluate an accepted candidate, reject a faster invalid candidate, classify an uncertain candidate, and publish a complete reproducible dossier.

## Why this lab matters

This lab turns the module’s governing question—**How does a performance change become a reproducible release decision rather than a favorable chart?**—into a falsifiable experiment. The checkpoint from Capacity Modeling and Scaling Decisions established this result: Model CPU, connections, workers, queues, storage, egress, cost, headroom, and scaling decisions. This module builds on that evidence rather than reopening the predecessor. Its result becomes the prerequisite for the course final defense and handoff .

It advances the cumulative Analysis Runs Platform by requiring this result: **Build correctness-first regression gates, environment comparability, accepted/rejected/inconclusive candidates, and a performance dossier**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

- all prior module checkpoints pass
- baseline registry is immutable
- performance profile thresholds are fixed
- accepted/rejected/inconclusive candidate fixtures exist

## Hypothesis

The clean implementation should satisfy this claim: **accepted candidate passes all earlier and performance gates; faster wrong candidate is rejected before latency approval; incomparable/noisy candidate is inconclusive; all ten planted defects are detected by the intended proof; baseline lineage remains immutable; rollback and remeasurement triggers are explicit; handoff contains no secret or ephemeral evidence.** When the lab introduces this fault—**Create an environment-mismatched or noisy candidate and classify it inconclusive**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Run the complete critical workload suite for baseline and candidate in alternating order.
2. Run conformance, security, reliability, and durable correctness checks.
3. Evaluate outcome coverage, latency, throughput, CPU, memory, DB, cache, and traffic fields.
4. Activate each planted defect and verify the intended gate fails.
5. Evaluate the deliberately faster-but-wrong candidate.
6. Create an environment-mismatched or noisy candidate and classify it inconclusive.
7. Write release, rollback, and remeasurement decisions.
8. Build and verify the sanitized Course 6 handoff manifest.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Create an environment-mismatched or noisy candidate and classify it inconclusive**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Evaluate an accepted candidate, reject a faster invalid candidate, classify an uncertain candidate, and publish a complete reproducible dossier**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- accepted candidate passes all earlier and performance gates
- faster wrong candidate is rejected before latency approval
- incomparable/noisy candidate is inconclusive
- all ten planted defects are detected by the intended proof
- baseline lineage remains immutable
- rollback and remeasurement triggers are explicit
- handoff contains no secret or ephemeral evidence

## Required evidence

Create:

```text
work/module-10/
├── release-policy.yaml
├── baseline-series/
├── candidate-series/
├── accepted-decision.json
├── rejected-decision.json
├── inconclusive-decision.json
├── sensitivity.json
├── rollback.md
├── remeasurement.md
└── final-dossier.md
```

`final-dossier.md` must link each conclusion to machine-readable evidence and state the strongest evidence class reached. Include one rejected optimization from earlier modules.

## Interpretation and defense

1. Which state or effect is authoritative for **Performance Regression and Release Engineering**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Create an environment-mismatched or noisy candidate and classify it inconclusive** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Stop benchmark and lab processes, reset disposable databases/caches/limiters, remove secrets and raw identifiers from the handoff, and verify course and handoff manifests.

## Completion gate

- [ ] complete suite is reproducible
- [ ] correctness-first gate order is demonstrated
- [ ] accepted, rejected, and inconclusive states are exercised
- [ ] all planted defects trigger failure
- [ ] baseline lineage is preserved
- [ ] rollback and remeasurement are actionable
- [ ] Course 6 handoff manifest passes

The lab is incomplete when the candidate is merely faster. It must preserve the inherited correctness oracle and explain the observed resource change.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Performance Regression and Release Engineering**. A green command without the negative case and causal explanation does not satisfy this gate.
