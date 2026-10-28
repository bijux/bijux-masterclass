# Laboratory 10 — Network Service Audit

**Module 60**

## Product

Build an independent mini job service with one finite HTTP endpoint, one event channel, explicit capacity, startup state, quiesce, one grace deadline, abort, and terminal report. The focus is architecture audit rather than protocol breadth.

## Governing question

> How can a complete service prove bounded admission, startup rollback, overload semantics, graceful shutdown, and terminal accounting across all transports?

## Public surface

- `AuditService.start(config)` publishes only after required resources succeed.
- `submit()` rejects before commit when not ready or at capacity.
- `close()` quiesces, drains, aborts, joins, and returns one report.
- Health and readiness are distinct typed views.

## Required invariants

- No resource is published before startup completion.
- Startup failure rolls back in reverse order.
- Quiescing closes application admission even on existing connections.
- All drains share one grace deadline.
- Every accepted job and subscriber terminates once.
- Final counts reconcile accepted and terminal work.

The laboratory is complete only when the tests distinguish these invariants from a smaller implementation that happens to pass the normal path.

## Implementation sequence

1. Create capacity table and runtime state union.
2. Implement staged startup with injected failure.
3. Add bounded submission and terminal jobs.
4. Add subscriber registry.
5. Implement readiness and health.
6. Implement quiesce/drain/abort/join.
7. Create authoritative report.
8. Add independent cancellation design.

Keep the sequence causal. A later feature should not hide an earlier failure. For example, do not add retry before a single attempt has one clear terminal owner, and do not add shutdown before the normal resource lifecycle is observable.

## Adversarial cases

- failure at every startup stage
- capacity full while process healthy
- keep-alive request during quiesce
- response loss after commit
- slow subscriber
- deadline with active work
- repeated close
- cleanup failure

For each case, write the predicted state transition and the exact terminal evidence before running the test. Prefer injected clocks, deterministic fake peers, explicit counters, and local ephemeral ports to arbitrary sleeps.

## Prohibited shortcuts

- ready before all binds
- one capacity number
- listener close as quiesce
- fresh grace per subsystem
- first cleanup error stops cleanup
- live counters as final proof

A shortcut is prohibited because it removes the mechanism under study. It is not a style preference.

## Completion evidence

1. startup fault-injection matrix
2. capacity map
3. one-deadline trace
4. terminal reconciliation
5. second close returns same report
6. no active owned resources

Also include a small ownership table naming every socket, timer, listener, queue, request, response, or subscription created by the product and its cleanup transition.

## Independent transfer

Add conditional cancellation with a revision precondition and list every layer that must change.

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
