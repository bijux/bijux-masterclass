# Course 6 predecessor handoff

Course 7 consumes `capstone/predecessor/handoff/` byte-for-byte from Course 6. The package defines data release order, protected resources, recovery gates, stateful workload identity, storage classes, network/security obligations, known risks, and the evidence boundary.

Delivery automation may order and reconcile declared actions. It may not:

- reinterpret a backup as verified merely because an object exists;
- prune retained volumes, snapshots, backup catalogues, or recovery keys;
- replay a non-idempotent migration because a hook restarted;
- treat application rollback as data rollback;
- acquire backend credentials merely because it can read a deployment repository.
