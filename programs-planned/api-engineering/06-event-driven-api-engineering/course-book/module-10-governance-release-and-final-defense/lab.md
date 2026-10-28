# Lab — Release Analysis Events 1.0 and defend the complete system

> **Module 10:** Event Platform Governance, Release, and Final Defense

## Objective

Assemble the contract, catalogues, implementations, migrations, failure proofs, lifecycle policy, and sanitized handoff into one release decision.

## Why this lab matters

This lab turns the module’s governing question—**How are event ownership, compatibility, retention, replay, consumers, evidence, and release decisions governed as a platform capability?**—into a falsifiable experiment. Python and TypeScript must agree on catalogue identity, compatibility classification, replay safety, release status, and exported handoff digests. A candidate accepted by one and rejected by the other is a release blocker until the policy or implementation difference is resolved.

It advances the cumulative Analysis Runs Platform by requiring this result: **Publish the catalogue, consumer declarations, accepted/rejected release candidates, final defense, and Course 7 handoff**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

1. Complete Modules 01–09 and collect their checkpoint evidence.
2. Freeze baseline and candidate release directories.
3. Verify catalogues cover every AsyncAPI message and consumer.
4. Prepare accepted-additive, rejected-breaking, and rejected-replay-unsafe candidates.
5. Create `work/module-10/release-dossier/`.

## Hypothesis

The clean implementation should satisfy this claim: **Only the additive candidate is accepted. Breaking and replay-unsafe candidates fail for exact reasons. Every public message and consumer is catalogued. The completion trace preserves one fact and one effect per effect version under duplicate windows. The tabletop has containment, recovery, reconciliation, and residual risk. The handoff is complete, deterministic, and sanitized.** When the lab introduces this fault—**Perform one final trace of AnalysisRunCompleted through producer, broker, analytics, notification intent, replay, and reconciliation**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

Run the full dependency-light proof. Evaluate all release candidates and ten planted defects. Perform one
final trace of `AnalysisRunCompleted` through producer, broker, analytics, notification intent, replay, and
reconciliation.

Execute a tabletop failure selected at random from broker outage, crash-after-effect, poison schema,
compromised producer key, late event, hot partition, and replay storm. Build the outgoing handoff and scan
it for secrets, private incident data, unresolved references, and manifest drift.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Perform one final trace of AnalysisRunCompleted through producer, broker, analytics, notification intent, replay, and reconciliation**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Assemble the contract, catalogues, implementations, migrations, failure proofs, lifecycle policy, and sanitized handoff into one release decision**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

Only the additive candidate is accepted. Breaking and replay-unsafe candidates fail for exact reasons.
Every public message and consumer is catalogued. The completion trace preserves one fact and one effect per
effect version under duplicate windows. The tabletop has containment, recovery, reconciliation, and residual
risk. The handoff is complete, deterministic, and sanitized.

## Required evidence

- `work/module-10/release-dossier/decision.json`
- `work/module-10/release-dossier/trace.md`
- final catalogue and consumer inventory
- candidate comparison reports
- planted-defect matrix
- tabletop timeline and reconciliation
- handoff manifest and secret-scan result
- output from `make core-proof` and `make manifest-proof`

## Interpretation and defense

1. Which state or effect is authoritative for **Event Platform Governance, Release, and Final Defense**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Perform one final trace of AnalysisRunCompleted through producer, broker, analytics, notification intent, replay, and reconciliation** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Remove planted defects and generated runtime reports, reset deterministic broker/consumer state, sanitize
tabletop evidence, and rebuild the manifest from clean source. Extract the final archive into a new
directory and rerun the core proof there.

## Completion gate

The course is complete only when the learner can defend every asynchronous guarantee with a durable oracle,
every green proof rejects a known defect, the final release is reproducible, and unexecuted live-tool routes
are reported honestly rather than represented as passing.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Event Platform Governance, Release, and Final Defense**. A green command without the negative case and causal explanation does not satisfy this gate.
