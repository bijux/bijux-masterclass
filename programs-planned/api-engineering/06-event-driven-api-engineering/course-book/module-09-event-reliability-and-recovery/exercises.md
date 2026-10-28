# Exercises — Module 09: Event Reliability, Backpressure, Dead Letters, and Recovery

Work through all twelve problems before opening the answers. In **Event Reliability, Backpressure, Dead Letters, and Recovery**, every response must settle this question: **How do lag, backpressure, retry, poison messages, dead-letter custody, broker failure, and replay storms affect recovery?** The strongest answer distinguishes specification, implementation, and operational evidence, then demonstrates where a plausible shortcut would fail.

## 1. Classify failures

Classify schema invalidity, authorization rejection, database timeout, broker outage, hot partition, and unsupported version.

## 2. Build a retry budget

Define attempts, delay, total age, and dependency concurrency for a transient database failure.

## 3. Calculate drain feasibility

Backlog is 120,000, arrival 500/s, service 800/s. Estimate net drain time and state assumptions.

## 4. Interpret two lags

Compare one partition with age 30 minutes/count 1 and another with age 20 seconds/count 20,000.

## 5. Design backpressure

Outbox bytes approach the database budget during broker outage. Define staged admission responses.

## 6. Design a dead letter

List fields and safe-detail constraints for a failed analytics event.

## 7. Repair a poison record

Describe the steps from dead-letter diagnosis through approved replay without looping.

## 8. Protect live traffic

A projection rebuild needs 50 million events. Define replay rate, priority, canary, pause, and abort controls.

## 9. Test crash recovery

Choose three process kill points and the durable oracle after restart.

## 10. Handle partition imbalance

One tenant dominates a partition. Identify short-term and long-term remedies without changing keys casually.

## 11. Reconcile after manual offset change

List stores and comparisons needed to prove no effect was skipped.

## 12. Define recovery complete

Write a completion criterion after a 30-minute broker outage.

## Submission format

Submit Module 09 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
