# Exercises — Module 06 — Consumer Architecture and Asynchronous Workflows

Design consumers as owned applications. Every workflow answer must identify state, transaction, and authoritative input.

## 1. Classify four consumers

Classify notification, analytics, audit, and run coordination as projection, external effect, audit sink, or process manager. Give each a distinct effect identity.

## 2. Choose choreography

Explain why analytics and audit should react independently to completion instead of passing through one orchestrator.

## 3. Choose orchestration

A run requires start, deadline, cancellation, and reconciliation. Explain why a process manager is justified.

## 4. Model command state

Define process states before and after publishing `StartAnalysis`, and after receiving `AnalysisRunStarted`.

## 5. Handle rejection

The start command is rejected because the dataset is quarantined. Define the authoritative message and process transition.

## 6. Design a durable timer

Specify identity, generation, deadline, and stale-fire behavior for a start timeout.

## 7. Handle out-of-order events

`ArtifactPublished` arrives before `AnalysisRunCompleted`. Choose buffer, projection independence, or reconciliation and justify.

## 8. Separate replay policy

Define replay behavior for analytics, notification, audit, and process manager.

## 9. Plan compensation

A run was queued but its dataset is later revoked. Design cancellation/compensation without claiming rollback.

## 10. Avoid command duplication

The process crashes after writing the start command but before acknowledgement. Explain how the command remains one logical intent.

## 11. Version a consumer

Deploy analytics v2 while v1 continues. Define group, inbox, target, and cutover identities.

## 12. Draw a consumer contract

For notification-v1, list accepted types, owned state, outputs, transaction, deadlines, retries, and recovery.

## Submission format

Submit Module 06 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
