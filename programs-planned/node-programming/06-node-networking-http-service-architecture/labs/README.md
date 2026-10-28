# Course 6 Laboratories

The ten laboratories isolate one network or service boundary at a time. They are smaller than ServiceWire so that a failure has a narrow causal surface. None is a tutorial copy of the capstone: each product has its own state machine, limits, and adversarial tests.

Build from `starter/`. Open `reference/` only after your own normal, boundary, and failure cases pass. When the reference differs, compare the contracts rather than counting lines of code.

| Module | Laboratory | Mechanism isolated |
|---:|---|---|
| 51 | Address Resolution Observatory | logical identity, candidate order, fallback, and one connect deadline |
| 52 | Bounded TCP Frame Server | arbitrary chunking, framing, half-close, pressure, and socket ownership |
| 53 | Reliable Datagram Protocol | correlation, retry, duplicates, stale responses, and replay cache |
| 54 | Strict HTTP Message Server | method semantics, bounded bodies, header policy, and response completion |
| 55 | Typed HTTP Router | route grammar, runtime validation, problem responses, idempotency, and ETags |
| 56 | Deadline-Aware HTTP Client | agents, reusable bodies, redirects, bounded responses, retry, and close |
| 57 | Local TLS Identity Lab | trust anchors, hostname identity, SNI, ALPN, deadlines, and cleanup |
| 58 | Multiplexed HTTP/2 Service | sessions, independent streams, limits, reset, GOAWAY, and close |
| 59 | Replayable SSE Channel | event IDs, replay, gaps, heartbeats, slow subscribers, and teardown |
| 60 | Network Service Audit | admission, overload, startup rollback, drain, abort, join, and terminal report |

## Before coding

For each laboratory, write four short artifacts in your notebook:

1. **State machine** — legal states and transitions.
2. **Capacity map** — every queue, retained collection, or peer-controlled value and its unit.
3. **Ownership map** — who closes sockets, agents, timers, streams, subscriptions, and child tasks.
4. **Failure table** — malformed input, overload, timeout, cancellation, peer close, internal failure, and expected terminal evidence.

This work is part of the laboratory. It is not optional documentation added after the implementation.

## Test order

Use this sequence:

```text
normal case
    ↓
smallest boundary case
    ↓
smallest malformed or timed-out case
    ↓
cleanup after failure
    ↓
independent transfer
```

Avoid arbitrary sleeps. Prefer injected resolvers and clocks, ephemeral local ports, explicit readiness signals, bounded deadlines, and complete close/join observations. A test that passes only because localhost happened to deliver one chunk is not a framing test.

## Using the reference

After your version passes, compare these questions:

- Does either design accept more syntax or retain more state than the brief allows?
- Can a peer force an unbounded allocation, queue, error string, or retry loop?
- Does a timeout merely stop waiting, or does it also own cancellation and cleanup?
- Is the causal error preserved when several components fail during teardown?
- Does every accepted operation receive one terminal outcome?
- Is product completion stronger than the last low-level event observed?

Adopt a reference difference only when it proves a missing contract or makes the same proof materially clearer.

## Completion

A laboratory is complete when its tests pass, its independent transfer is implemented, all resources close, the stated limits are enforced at the boundary where growth occurs, and you can explain why the most tempting shortcut is incorrect.
