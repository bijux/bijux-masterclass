# Final defense

The learner must trace one `AnalysisRunCompleted` fact from source transaction through outbox, relay, broker, delivery, inbox/effect, acknowledgement, projection, notification intent, replay, and reconciliation. At each step they name owner, identity, transaction, duplicate window, security decision, and durable oracle.

The examiner then selects one failure: broker outage, crash after effect, poison schema, compromised key, late event, hot partition, or replay storm. The learner must contain, diagnose, recover, and prove correctness.

Non-compensable gates:

1. predecessor handoff exact;
2. every public message and consumer catalogued;
3. contract examples valid;
4. duplicate publication and delivery produce one effect per effect version;
5. retained history remains readable;
6. replay is bounded and side-effect controlled;
7. tenant and producer authorization pass;
8. dead letters and backlog have owners and budgets;
9. rejected candidates and planted defects fail;
10. final handoff and manifest verify after clean extraction.
