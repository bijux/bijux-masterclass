# Analysis Events capstone

The capstone extends the Course 5 Analysis Runs platform with asynchronous contracts and independent consumers while preserving HTTP API 1.2.

The dependency-light broker is the semantic reference. PostgreSQL migrations model durable outbox, inbox, replay, dead-letter, and contract-catalogue state. NATS JetStream is an optional integration target.

Start with `make capstone-tour`, then follow the module proofs rather than browsing files randomly.
