# Checkpoint 09 — Subscriptions, Resume, and Incremental Delivery

Do not continue until every condition is supported by executable or inspected evidence.

- [ ] The subscription resolver produces a source stream from the event owner and executes the selected response for each event.
- [ ] Resume begins after an explicit sequence, suppresses duplicates, and stops on a gap rather than silently skipping history.
- [ ] Buffers, connection lifetime, concurrent subscriptions, and tenant scope are bounded.
- [ ] Authorization is checked at subscription start and again when policy or credential freshness requires it.
- [ ] Client cancellation closes the stream and releases source resources.
- [ ] Lab 09 proves ordered resume, duplicate suppression, gap detection, slow-consumer handling, and cleanup.

**Gate:** run `make module-09-proof`. A green command without the lab report and the listed evidence does not count.
