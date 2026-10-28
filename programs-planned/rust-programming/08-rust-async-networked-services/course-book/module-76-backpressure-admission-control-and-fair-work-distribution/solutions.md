# Reasoned Solutions — Module 76: Backpressure, Admission Control, and Fair Work Distribution

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the JobWire guide](../capstone.md)

The governing correction is that no single bounded primitive makes a service bounded. Capacity must be traced across every place work, bytes, tasks, timers, and results can wait.

## Part 1 — Prediction solutions

1. No. The semaphore bounds execution, while waiting task count and captured request memory remain unbounded.
2. At least the broker capacity plus the per-connection retained requests, subject to which sends have entered the channel. The service must count all layers.
3. Status, cancellation, duplicate-key lookup, shutdown, and new admission can all block behind capacity acquisition.
4. Compute capacity has become coupled to network consumption. Slow clients reduce job throughput.
5. A synchronized retry wave or thundering herd can occur. Clients need jitter and an overall deadline.
6. Tenant-level domination remains. Connection limits are not identity or tenant quotas.
7. No. Queueing delay may already violate deadlines and small bursts may trigger rejection. Sustained high occupancy is an overload signal.
8. Kernel and runtime buffers may retain substantial data, and flow control does not bound decoded requests, tasks, or application state.

## Part 2 — Repair reasoning

The repaired design limits accepted connections, stops each V1 connection at one in-flight request, uses a bounded broker mailbox, keeps waiting jobs in one bounded scheduler rather than one task each, limits active work, stores only bounded results, and gives writers deadlines. Admission before broker commit can return `BUSY`; after commit, idempotency recovers the outcome.

## Part 3 — Focused exercise guidance

The envelope should state assumptions and overhead exclusions. A useful conservative payload calculation sums per-connection frame/request retention, queued requests, active job inputs and results, and idempotency records. It should not claim exact heap usage.

A fair scheduler needs explicit tenant identity and queue ownership. Round-robin can prevent queue monopolization but does not equalize job cost unless weights or cost classes are added. Saturation tests should hold tasks with notifications, not rely on long sleeps.

## Part 4 — Laboratory comparison

A strong broker preserves responsiveness while work runs. It owns a finite waiting structure, classifies job panic, and releases active permits before waiting on slow reply consumers. Every accepted request gets one terminal reply or a documented cancellation outcome.

## Part 5 — Capstone comparison

JobWire’s broker is state authority. It should record the idempotency entry at commit, schedule bounded work, and cache a bounded terminal result. Connection writers observe results but do not retain compute permits. `STATS` reads a snapshot or uses a priority control path rather than waiting behind saturated work.

## Part 6 — Reconstruction and defense

A complete defense names every accumulation point, its unit, maximum, owner, and saturation behavior. It distinguishes stored latency from active work, commit from admission, transport flow control from application bounds, and fairness policy from primitive implementation details.
