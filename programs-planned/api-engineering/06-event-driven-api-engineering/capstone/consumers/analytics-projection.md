# Analytics projection consumer

**Inputs:** terminal run facts.

**Effect:** maintain tenant-scoped event-time windows and duration aggregates.

**Identity:** `(tenant, analytics, effectVersion, eventId)`. Rebuilding a projection uses a new effect version so the old result remains inspectable until cutover.

**Replay:** projection-safe with a bounded plan and external side effects disabled.
