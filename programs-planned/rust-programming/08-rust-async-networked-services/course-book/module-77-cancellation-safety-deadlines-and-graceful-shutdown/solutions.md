# Reasoned Solutions — Module 77: Cancellation Safety, Deadlines, and Graceful Shutdown

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the JobWire guide](../capstone.md)

The governing correction is that cancellation is not rollback. It destroys one local future state at a suspension boundary while external systems may already contain prefixes, queued messages, or committed operations.

## Part 1 — Prediction solutions

1. The send future is dropped. Some bytes may already be buffered or written, so the connection policy must decide whether continuation is valid.
2. No. The broker may receive and commit after the caller stops waiting. Idempotency or status recovery is required.
3. No. Tasks observe cancellation when polled and when their code selects or checks the token.
4. No. Abort is cooperative at task poll boundaries; nonyielding code monopolizes its worker until it returns.
5. Yes. Admission must stop before draining descendants.
6. No. Dropping aborts as a backstop, but awaiting joins provides terminal evidence and panic/cancellation classification.
7. No. Total latency can be the sum of stage budgets. Carry one overall deadline.
8. No. Cancellation safety is operation-specific and may include data, ordering, and external effects.

## Part 2 — Repair reasoning

The repaired top-level owner records one shutdown reason, closes or cancels admission loops, tells connections and broker to stop accepting new work, drains committed work for a finite grace, aborts leftovers, and awaits every handle. The broker must remain alive while connections need terminal replies. Only after descendants finish does the top-level process return.

## Part 3 — Focused exercise guidance

The commit race should use an explicit gate around broker insertion. Before insertion, cancellation leaves no record. After insertion, retry with the same key observes in-progress or completed state. Paused time proves the deadline without waiting in wall-clock time.

Blocking jobs require separate policy. Cooperative work checks a flag. A noncooperative native call may delay runtime shutdown or require process isolation if a hard deadline is essential.

## Part 4 — Laboratory comparison

A strong task tree has one owner for every handle and one downward cancellation path. Repeated shutdown signals do not create competing drains. The test waits for task terminal states rather than inferring completion from token cancellation.

## Part 5 — Capstone comparison

JobWire should stop TCP and HTTP admission first. Connections stop accepting commands. The broker preserves committed jobs and rejects new submissions. After grace, connection and job sets are aborted and drained. The broker exits last so in-flight idempotency outcomes remain authoritative through drain.

## Part 6 — Reconstruction and defense

A complete defense names the local state dropped, external state preserved, commit boundary, deadline budget, and exact shutdown phase. It never uses “graceful” as a synonym for “sent a cancellation signal.”
