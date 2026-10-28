# Laboratory 9 — Replayable SSE Channel

**Module 59**

## Product

Build a server-sent event journal and subscription endpoint. It uses monotonic event IDs, bounded history, explicit replay gaps, race-free subscription opening, heartbeat comments, subscriber admission, and slow-consumer removal.

## Governing question

> How can a long-lived HTTP response provide ordered replay and live events while bounding history, subscriber queues, heartbeats, and cleanup?

## Public surface

- `encodeEvent(event)` produces canonical SSE bytes.
- `EventJournal.append` assigns one sequence.
- `open(after, listener)` returns replay plus a disposable live subscription without a gap.
- `serveSse` owns response pressure, heartbeat, and cleanup.

## Required invariants

- Events are encoded and terminated correctly.
- Replay is ordered and complete or explicitly rejected as a gap.
- No event can fall between replay and live registration.
- History and subscriber queues have independent bounds.
- A pressured subscriber cannot block global publication.
- Every subscriber is removed on every terminal path.

The laboratory is complete only when the tests distinguish these invariants from a smaller implementation that happens to pass the normal path.

## Implementation sequence

1. Implement event encoding.
2. Implement bounded journal.
3. Add replay cursor validation.
4. Remove replay-to-live race.
5. Add live subscription.
6. Add pressure-aware queue.
7. Add heartbeat.
8. Add HTTP endpoint and shutdown.

Keep the sequence causal. A later feature should not hide an earlier failure. For example, do not add retry before a single attempt has one clear terminal owner, and do not add shutdown before the normal resource lifecycle is observable.

## Adversarial cases

- multi-line data
- cursor before oldest
- cursor equal latest
- future cursor
- event appended while opening
- write returns false
- queue overflow
- client close
- heartbeat timer cleanup
- service shutdown

For each case, write the predicted state transition and the exact terminal evidence before running the test. Prefer injected clocks, deterministic fake peers, explicit counters, and local ephemeral ports to arbitrary sleeps.

## Prohibited shortcuts

- timestamp event IDs
- subscribe after replay
- one bound for journal and subscribers
- ignore `write()` pressure
- one untracked timer per client
- claiming durable exactly-once delivery

A shortcut is prohibited because it removes the mechanism under study. It is not a style preference.

## Completion evidence

1. wire-format assertions
2. race test
3. replay-gap test
4. slow-subscriber isolation
5. zero remaining subscribers/timers

Also include a small ownership table naming every socket, timer, listener, queue, request, response, or subscription created by the product and its cleanup transition.

## Independent transfer

Design progress SSE for a bounded import and specify snapshot recovery and restart behavior.

The transfer is not complete when only type names change. Reconstruct the protocol, state, capacity, time, and terminal ledgers for the new domain.

## Using the starter

The starter compiles and exposes the domain vocabulary, configuration validation, and one baseline test. It does not implement the difficult mechanism. Extend it without weakening strict TypeScript settings.

Run:

```bash
npm run typecheck
npm test
```

## Comparing with the reference

Open `reference/` only after your normal and adversarial tests pass. Compare:

1. state representation;
2. bound enforcement point;
3. cleanup ownership;
4. failure classification;
5. test evidence.

Adopt a reference difference only when it proves an invariant your design misses or makes the same contract materially easier to inspect.
