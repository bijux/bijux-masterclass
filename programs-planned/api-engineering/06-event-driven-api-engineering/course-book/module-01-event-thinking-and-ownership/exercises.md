# Exercises — Module 01 — Event Thinking, Ownership, and Message Taxonomy

Answer from semantics and durable ownership, not from broker features.

## 1. Classify the run-submission flow

Classify the HTTP submission, durable job request, run-queued fact, worker lease acquisition, and completion notification as command, event, query, internal domain event, or notification. Justify each classification from ownership and rejection semantics.

## 2. Reject an unnecessary event

A proposal introduces `ProjectViewed` whenever a user opens a project page. No current consumer exists. Decide whether it belongs in the public event API and name the evidence that could change your decision.

## 3. Repair an imperative event

The catalogue contains `org.bijux.analysis.generate.artifact.v1`. Determine whether this is a command or event, rename it, and state who owns the resulting fact.

## 4. Find the authoritative source

The worker and control-plane service both have enough information to announce completion. Choose the authoritative producer and describe the handoff between them.

## 5. Separate five identities

For a completed run, propose values for event ID, subject, correlation ID, causation ID, and partition key. Explain why none is redundant.

## 6. Choose event granularity

Compare one `RunLifecycleChanged` union event with separate requested, started, completed, and failed events. Identify one benefit and one cost of the separate-event design.

## 7. Protect the private model

An internal aggregate contains retry counters, a worker lease token, owner data, and an exception stack. Decide which fields, if any, belong in `AnalysisRunFailed`.

## 8. Keep a synchronous boundary

A client must know whether a dataset belongs to its tenant before starting an analysis. Explain why an event-only authorization flow is unsafe.

## 9. Distinguish domain and integration events

Design an internal transition event and a public integration event for artifact publication. Show which data is intentionally removed at the boundary.

## 10. Evaluate temporal decoupling

A billing simulation can run minutes after completion; artifact metadata must be committed before the completion response is visible. Decide which interaction can be asynchronous.

## 11. Identify a notification

A consumer sends a user-facing email after completion. Is the email request an event, command, or notification? Explain which fact should drive it.

## 12. Write the publication test

Write a five-question decision test for adding `DatasetScanned` to the event API and state the rejection outcome when no durable owner exists.

## Submission format

Submit Module 01 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
