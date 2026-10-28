# Checkpoint 04 — Queries, Identifiers, Connections, and Pagination

Do not continue until every condition is supported by executable or inspected evidence.

- [ ] Global IDs are opaque, typed, tenant-neutral identifiers and never act as authorization evidence.
- [ ] Connections use a deterministic total order with a unique tiebreaker.
- [ ] Cursors bind tenant, caller audience, field scope, normalized filters, high-water key, continuation key, version, and expiry.
- [ ] A continued traversal excludes rows inserted above the original high-water key, while a fresh traversal can observe them.
- [ ] Changing filter, tenant, permission audience, or connection coordinate invalidates a cursor.
- [ ] Lab 04 proves no duplicate or skipped edge across the controlled insertion experiment.

**Gate:** run `make module-04-proof`. A green command without the lab report and the listed evidence does not count.
