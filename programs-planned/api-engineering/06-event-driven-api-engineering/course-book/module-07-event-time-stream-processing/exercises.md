# Exercises — Module 07 — Event-Time Stream Processing, Windows, Watermarks, and Corrections

Use explicit timestamps and window identities. Every answer must address replay and late data.

## 1. Name four clocks

For a completed event delayed by a broker outage, assign event, ingestion, processing, and observation times.

## 2. Choose a window

Select tumbling, sliding, or session windows for five-minute completion totals, rolling 30-minute failure rate, and user upload sessions.

## 3. Define a watermark

Propose a watermark for four partitions and explain how an idle partition affects it.

## 4. Handle late-but-accepted data

Describe output identity and revision when a unique event arrives after initial emission but within allowed lateness.

## 5. Handle too-late data

Design the durable record and runbook path for an event outside allowed lateness.

## 6. Separate duplicate and late

Give one duplicate-on-time and one unique-late example and state each decision.

## 7. Plan a checkpoint

List state that must commit together for a durable window processor.

## 8. Prevent output duplication

A crash occurs after publishing revision 2 but before checkpoint. Design an output boundary.

## 9. Correct an algorithm

A bug undercounted failed runs. Explain how to issue corrected results without rewriting old output.

## 10. Bound state

Identify dimensions that drive window-state cardinality and controls for each.

## 11. Protect replay determinism

List five sources of nondeterminism in a stream handler and replacements.

## 12. Separate business and telemetry

Compare event-derived completion rate with OpenTelemetry request count and state which can rebuild business history.

## Submission format

Submit Module 07 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
