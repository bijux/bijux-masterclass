# Exercises — Module 10 — Event Platform Governance, Release, and Final Defense

Treat governance as executable ownership and evidence. Every answer should identify who approves and what proves the decision.

## 1. Complete a catalogue entry

List required fields for `ArtifactPublished` from owner through lifecycle and runbook.

## 2. Gate a producer release

A candidate has valid schema but non-atomic direct publish. Determine the decision and evidence.

## 3. Gate a consumer release

Analytics v2 reads fixtures but has no replay isolation or rollback. Determine the decision.

## 4. Deprecate v1

Design stages, dates, consumer evidence, retained-history support, and retirement conditions.

## 5. Migrate partitioning

Change a hot tenant-keyed channel to run-keyed partitioning without silently reordering history.

## 6. Reduce retention

A proposal cuts completion retention from 90 to 7 days. Identify required replay/audit/consumer analysis.

## 7. Register an offline consumer

Explain how governance accounts for a monthly batch consumer that telemetry rarely observes.

## 8. Sanitize a handoff

Classify which of contracts, schemas, examples, signing secrets, dead-letter bodies, migrations, incident reports, and vectors should be exported.

## 9. Prove gate sensitivity

Map each release proof to one planted defect it must reject.

## 10. Defend technology neutrality

State which invariants are shared across Python/TypeScript and which implementation choices may differ.

## 11. Trace one completion fact

Name every durable state and failure window from database commit through notification intent.

## 12. Respond to final failure

A compromised producer key may have forged three completion events. Outline containment, reconciliation, correction, and release actions.

## Submission format

Submit Module 10 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
