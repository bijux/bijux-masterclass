# Durable Analysis Runs capstone

Two complete reference tracks implement one frozen predecessor contract with independent databases and migration histories. They share public contract artifacts and proof vectors, not a runtime database.

```bash
make -C capstone core-proof
make -C capstone up TRACK=python RELEASE=1.0
make -C capstone conformance TRACK=python RELEASE=1.0
make -C capstone recovery TRACK=python RELEASE=1.0
make -C capstone artifact TRACK=python RELEASE=1.0
make -C capstone webhook TRACK=python RELEASE=1.0
make -C capstone final TRACK=python RELEASE=1.0
make -C capstone release TRACK=python
```

The application and worker come from the same codebase. PostgreSQL provides durable state, job coordination, cursor handles, and the transactional outbox. No hidden broker or cache is used.
