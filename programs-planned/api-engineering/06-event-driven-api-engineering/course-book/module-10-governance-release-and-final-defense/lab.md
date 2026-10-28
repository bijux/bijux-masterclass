# Lab — Release Analysis Events 1.0 and defend the complete system

## Objective

Assemble the contract, catalogues, implementations, migrations, failure proofs, lifecycle policy, and sanitized handoff into one release decision.

## Setup conditions


1. Complete Modules 01–09 and collect their checkpoint evidence.
2. Freeze baseline and candidate release directories.
3. Verify catalogues cover every AsyncAPI message and consumer.
4. Prepare accepted-additive, rejected-breaking, and rejected-replay-unsafe candidates.
5. Create `work/module-10/release-dossier/`.


## Failure action and investigation


Run the full dependency-light proof. Evaluate all release candidates and ten planted defects. Perform one
final trace of `AnalysisRunCompleted` through producer, broker, analytics, notification intent, replay, and
reconciliation.

Execute a tabletop failure selected at random from broker outage, crash-after-effect, poison schema,
compromised producer key, late event, hot partition, and replay storm. Build the outgoing handoff and scan
it for secrets, private incident data, unresolved references, and manifest drift.



### Investigation notes

Before editing, write a one-sentence hypothesis answering: **How are event ownership, compatibility, retention, replay, consumers, evidence, and release decisions governed as a platform capability?** Record the first observation that contradicts the expected model. After the repair, explain why the capstone can now claim: Publish the catalogue, consumer declarations, accepted/rejected release candidates, final defense, and Course 7 handoff. A passing command without this causal explanation is insufficient.

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


## Cleanup and reset


Remove planted defects and generated runtime reports, reset deterministic broker/consumer state, sanitize
tabletop evidence, and rebuild the manifest from clean source. Extract the final archive into a new
directory and rerun the core proof there.


## Completion gate


The course is complete only when the learner can defend every asynchronous guarantee with a durable oracle,
every green proof rejects a known defect, the final release is reproducible, and unexecuted live-tool routes
are reported honestly rather than represented as passing.
