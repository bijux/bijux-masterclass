# Module 60 Solutions — Integrated Service Architecture

## Prediction reasoning

An open listener does not make the service ready when it cannot accept its promised submission workload. Existing keep-alive connections can continue to send requests after listener close unless application admission rejects them. A job can succeed while the request terminates as disconnect or deadline. GOAWAY begins HTTP/2 closure but active streams still require completion and join. Discovery advertising readiness after quiescence sends stale service-state information.

## Repair reasoning

The capacity map names each resource, unit, limit, owner, admission failure, release transition, and shutdown path. It should include transports, requests, domain records, journal, subscribers, and clients.

Health reports whether the runtime can make progress. Readiness reports whether supported traffic is currently admitted. Quiescing is live but not ready.

Startup should build resources privately, publish only after all required binds succeed, and close in reverse order after failure. Inject failure after each stage to test rollback.

Application submission checks runtime state even on already accepted connections. That closes the keep-alive admission gap.

Create one shutdown deadline. Start subsystem drains concurrently. At expiry, abort remaining owners. Do not start another full timeout for each component.

Maintain separate terminal models for requests and jobs. Join network owners, then reconstruct job outcomes. The final report reconciles accepted and terminal counts.

## Construction notes

A runtime state union is clearer than several Booleans:

```ts
type RuntimeState =
  | { readonly kind: 'starting' }
  | { readonly kind: 'ready' }
  | { readonly kind: 'quiescing'; readonly deadlineMs: number }
  | { readonly kind: 'stopped'; readonly report: TerminalReport }
  | { readonly kind: 'failed'; readonly error: Error };
```

State transitions occur under one runtime authority.

Use `Promise.allSettled()` for cleanup where every owner must be observed. Preserve failures rather than stopping after the first close error.

Tests should avoid relying on handle-count internals alone. Expose owned registries and terminal reports, then supplement with process tests that terminate naturally.

## Laboratory evidence

The independent audit should include:

- capacity table;
- startup state machine;
- injected startup failures;
- overload at several layers;
- quiesce with existing keep-alive connection;
- accepted job after response loss;
- SSE slow subscriber;
- HTTP/2 active stream;
- one grace deadline;
- forced abort;
- final reconciliation;
- deterministic report.

## Conditional cancellation extension

A valid cancellation route first validates job ID and `If-Match`. A stale tag returns 412 without state change. A queued or cooperatively running job transitions to cancelled, increments revision, and appends event. Terminal jobs follow documented conflict or idempotent policy. Repeating cancellation must not increment revision again.

The HTTP/2 adapter calls the same application command. The client exposes a typed cancellation method. Shutdown-induced cancellation and user-requested cancellation have distinct causes in events and diagnostics.

A synchronous operation may finish before cancellation is observed; the state authority decides the winner based on actual transition order. Do not claim preemption JavaScript cannot provide.

## Process-local limitations

The base course does not guarantee:

- jobs survive process restart;
- idempotency records survive restart;
- event history is durable;
- several service instances coordinate job IDs or capacity;
- exactly-once behavior across failures;
- distributed authorization or discovery trust.

Those are explicit inputs to Course 7.

## Defense summary

The final architecture succeeds when every layer has one authority and every accepted resource has a bounded path to one terminal observation. Coherence is proved by cross-layer change, not by adding more endpoints.

## Incident-simulation solution

The terminal table must account independently for each resource class. Connections end as gracefully closed or forcibly destroyed; HTTP/2 streams as completed or reset; jobs as succeeded, failed, or cancelled; subscribers as disposed; discovery as closed; timers as cleared; agents as destroyed. “Shutdown completed” is not a substitute for these categories.

The initiating shutdown cause remains the primary event. Cleanup failures are collected in a bounded list attached to the terminal report. Throwing only the last cleanup failure would erase why shutdown began; swallowing cleanup errors would falsely claim complete cleanup.

A strong design defense starts with one application authority, typed commit points, independent capacity bounds, one deadline per operation, causal error classes, and idempotent lifecycle owners. Node APIs are implementation mechanisms underneath those contracts. Public cancellation must update the route, precondition, controller, state transition, revision, event journal, client, shutdown race policy, tests, and documentation together.

## Release-checklist solution

Each claim needs a named adversarial test: chunked over-limit body, lost-response idempotent replay, matching and stale ETag, trusted and wrong TLS name, reset HTTP/2 stream with healthy sibling, cursor older than retained SSE history, unrelated UDP nonce, capacity-full 503 without commit, second-listener startup failure with first listener cleaned, and shutdown with a deliberately slow job and subscriber. The observable evidence is terminal state and remaining handle counts, not merely absence of thrown errors.
