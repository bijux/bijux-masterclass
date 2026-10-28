# Module 10 lab — Conduct the final performance release review

## Objective

Evaluate an accepted candidate, reject a faster invalid candidate, classify an uncertain candidate, and publish a complete reproducible dossier.

## Setup conditions

- all prior module checkpoints pass
- baseline registry is immutable
- performance profile thresholds are fixed
- accepted/rejected/inconclusive candidate fixtures exist

## Failure action and investigation


1. Run the complete critical workload suite for baseline and candidate in alternating order.
2. Run conformance, security, reliability, and durable correctness checks.
3. Evaluate outcome coverage, latency, throughput, CPU, memory, DB, cache, and traffic fields.
4. Activate each planted defect and verify the intended gate fails.
5. Evaluate the deliberately faster-but-wrong candidate.
6. Create an environment-mismatched or noisy candidate and classify it inconclusive.
7. Write release, rollback, and remeasurement decisions.
8. Build and verify the sanitized Course 6 handoff manifest.



### Investigation notes

Before editing, write a one-sentence hypothesis answering: **How does a performance change become a reproducible release decision rather than a favorable chart?** Record the first observation that contradicts the expected model. After the repair, explain why the capstone can now claim: Build correctness-first regression gates, environment comparability, accepted/rejected/inconclusive candidates, and a performance dossier. A passing command without this causal explanation is insufficient.

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
