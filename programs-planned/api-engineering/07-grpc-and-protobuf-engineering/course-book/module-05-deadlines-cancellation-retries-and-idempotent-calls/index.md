# Deadlines, Cancellation, Retries, and Idempotent Calls

**Module 05 of 10**

> **Governing question:** How can callers bound remote work and recover from transient failure without multiplying timeouts or duplicating durable effects?

## Place in the program

Module 04 defined stable unary outcomes. This module controls time and repetition. Remote calls fail ambiguously: a deadline can expire after commit, cancellation can arrive too late, and a retry can repeat an effect. The learner now treats one absolute deadline, propagated cancellation, retry classification, persistent idempotency, and reconciliation as one design problem.

## Learning outcomes

- derive child RPC budgets from one absolute edge deadline
- separate caller cancellation from application rollback
- classify transparent and configured retries without assuming all transient statuses are safe
- bind mutation retries to durable idempotency records and semantic fingerprints
- apply bounded backoff, jitter, attempt limits, and retry throttling
- reconcile ambiguous outcomes when a deadline or connection fails after commit

## Capstone result

Implement deadline-aware CreateRun and GetRun clients, persistent retry semantics, deterministic retry vectors, and fault-injection evidence for failures before invocation, before commit, after commit, and during response delivery.

## One absolute deadline owns the journey

A timeout attached independently to every hop is not a budget. If an edge request has five seconds and it calls three services with five-second timeouts, the user-visible journey can consume much more than five seconds, especially with retries. Start with one absolute deadline at the caller that knows when the result loses value. Propagate the remaining duration to each child call after reserving time for local work and response translation.

A deadline is a point in time; a timeout is a relative duration. Relative values are vulnerable to queue delay and repeated resetting. The client adapter computes `remaining = deadline - monotonic_now`, rejects work when the budget is exhausted, and applies a bounded child allowance. Servers inspect the deadline and stop optional work when the result can no longer arrive usefully. Use monotonic time for elapsed-budget calculations and wall time only for interoperable timestamps.

The evidence records edge budget, queue delay, each attempt start and finish, backoff, server-observed remaining time, and final outcome. This exposes hidden timeout multiplication.

## Cancellation is cooperative, not transactional

Client cancellation means “I no longer need this result.” The runtime propagates a cancelled context, but application and database work may already be committed. A server should stop expensive optional work, avoid starting new dependencies, release permits, and terminate streams promptly. It must not report that durable state was rolled back unless the transaction actually did so.

Application cancellation is a separate command with its own authorization, state preconditions, request identity, and durable event. A cancelled `CreateRun` client context can still leave a created run; a later `CancelRun` may be required. This distinction is essential for correct user interfaces and incident analysis.

Cancellation tests inject the signal before handler entry, during validation, during a dependency call, before commit, after commit, and during response serialization. The oracle is durable state plus final transport outcome, not the exception observed by the caller.

## Transparent retries and configured retries

gRPC libraries may perform limited transparent retries when a call is known not to have reached application handling or when transport setup fails under narrow conditions. Configured retries are policy-driven re-attempts for selected status codes. Neither category makes a mutation safe. The application must know whether a repeated request can produce another effect.

The course declares retry behavior by fully qualified method. Read-only `GetRun` can retry selected transient failures within the deadline. `CreateRun` can retry only with a persistent request identifier bound to the semantic input. `CancelRun` likewise requires idempotency and version semantics. Streaming methods have different reconnection and resume rules; unary retry configuration does not apply automatically.

Service configuration is versioned and reviewed with the RPC contract. Hidden client-library defaults are recorded in the capability matrix.

## Persistent idempotency closes the ambiguity

An in-memory deduplication map does not survive process restart and cannot coordinate replicas. The service stores request identifier, principal or tenant scope, method identity, canonical request fingerprint, state, and replayable outcome in the same authoritative database boundary as the command effect. Competing identical calls converge on one record. Changed input under the same identifier fails visibly.

The fingerprint includes semantic request fields after normalization, not volatile metadata such as trace identifiers. It excludes server-derived identity only if the identity is stored separately in the binding. The persisted outcome includes status, response bytes or canonical fields, and selected safe trailing metadata needed for equivalent replay.

If a client cannot safely retry, it reconciles through an authoritative lookup. Exactly what can be queried must be designed before failure. “Just try again” is not a reconciliation strategy.

## Backoff, jitter, and retry budgets

Retries add demand precisely when a dependency is unhealthy. Use exponential backoff with jitter, a maximum delay, a maximum attempt count, and one overall deadline. Full or decorrelated jitter prevents synchronized clients from producing retry waves. The deterministic test profile injects a seeded random source so Python and TypeScript can prove the same bounds without claiming identical production schedules.

A retry budget limits retries relative to useful requests or a fixed capacity. It prevents one failing method from consuming all traffic capacity. Retry throttling may suppress attempts when recent success is too low. Client and server metrics distinguish original calls from attempts.

Honor `Retry-After`-like structured guidance only when it fits within the caller deadline and method policy. Server guidance cannot authorize an unsafe replay.

## Wait-for-ready is not infinite patience

Fail-fast behavior returns when no ready channel is available; wait-for-ready may queue the call until connectivity recovers. It is useful for startup races and brief control-plane reconnection, but every waiting call still needs a deadline and admission bound. Unbounded wait-for-ready converts an unavailable service into growing client memory and delayed overload.

Use it selectively for operations whose result remains valuable after a short wait. Interactive HTTP-backed requests usually need fast failure within the edge budget. Background control clients may tolerate a longer bounded wait. Record queue time separately from server execution.

A readiness policy must not hide authorization, name-resolution, or permanent configuration failures as connectivity problems.

## Deadline propagation across protocols

The public HTTP edge owns the user-visible deadline. It passes a reduced budget to internal gRPC. If the control plane emits an event, that event is not governed by the expired HTTP deadline; it represents a durable committed fact. A worker assignment has a lease expiry, not the original request deadline. Mixing these time concepts causes work to be cancelled long after it became independently owned.

Trace attributes record deadline remaining at each synchronous boundary. Event metadata records causation but not a promise to complete before the old deadline. Worker protocols carry lease timing explicitly. Course 7 therefore distinguishes request deadline, stream idle timeout, assignment lease, retry delay, and event retention.

This temporal model is part of the handoff to distributed architecture.

## Ambiguous failure reconciliation

After a deadline or connection failure, the client asks two questions: could the server have committed, and is the operation idempotently identifiable? For `CreateRun`, retry with the same request identifier or query the idempotency outcome. For `CancelRun`, re-read the run and compare state/revision. For a pure query, a retry is sufficient if the result is still useful.

Do not infer non-commit from `CANCELLED`, `DEADLINE_EXCEEDED`, or `UNAVAILABLE`. Status describes the call observation, not necessarily authoritative state. Rich error details may indicate a precondition or known rejection, but absence of success is not proof of absence of effect.

The reconciliation report pairs every injected fault point with caller observation and durable oracle. This becomes the foundation for Course 8 saga and partial-failure reasoning.

## Cross-language timing proof

Real clocks make tests flaky and obscure rules. Both tracks define an injected monotonic clock, deterministic scheduler, and seeded jitter source for policy tests. Network tests use broad bounded windows only for transport integration; they do not assert millisecond equality.

Shared vectors describe absolute deadline, attempt durations, status sequence, backoff parameters, request safety, and expected final decision. Python and TypeScript must agree on whether another attempt is allowed and on maximum possible elapsed budget. Their internal timers and exception types may differ.

A production profile uses runtime clocks and gRPC contexts. The course never extrapolates deterministic simulator throughput or timing to production.

## Worked timing review: a five-second public journey

An HTTP client gives the gateway five seconds. The gateway validates the request for 120 ms, waits 180 ms for an admission permit, and then calls `CreateRun`. A weak implementation assigns a five-second timeout to the RPC. The user journey can now exceed its budget before retries even begin. The correct adapter carries one absolute monotonic deadline, reserves response-mapping time, and passes only the remaining allowance.

Assume the first attempt reaches Analysis Control, commits in 300 ms, but the connection fails before the response. The caller observes `UNAVAILABLE` with roughly four seconds left. Retrying is safe only because `CreateRun` carries a persistent request identifier bound to the verified principal and normalized semantic input. The second attempt reaches another instance, locks or reads the same idempotency record, and returns the stored outcome. It does not execute the mutation again.

Now change the dataset while reusing the identifier. The server returns the declared idempotency conflict. Replaying the first result would be dangerous because the caller might believe the second dataset was analyzed. Creating another run would make the identifier meaningless. The fingerprint and binding turn a retry mechanism into an integrity guarantee.

Backoff still matters. Hundreds of gateways may see the same transient fault. Immediate retries create a recovery storm. The policy applies bounded exponential backoff with jitter and a retry budget. Before each attempt, the client asks whether the next delay and estimated call can fit in the remaining absolute deadline. If not, it stops and reconciles. A server-provided delay never authorizes a replay that the method profile forbids.

Cancellation is tested at several phases. Before handler entry, no effect should exist. During a dependency call, cooperative cancellation may stop work. After commit, cancellation only stops response work; the run remains created. The final status describes the caller’s observation, while the database and idempotency record describe the authoritative outcome.

The design review also distinguishes other clocks. A worker lease can extend beyond the original HTTP deadline because the accepted run became durable. Event retention lasts much longer and is unrelated to user patience. A WatchRun idle timeout governs a stream connection, not run execution. Naming these clocks prevents accidental propagation of a dead request deadline into independently owned asynchronous work.

## Implementation reading

Read `capstone/rpc-case/deadline-retry-policy.yaml`, `capstone/shared/vectors/deadlines.json`, and `retries.json`. Compare the Python and TypeScript budget/retry engines and the persistent idempotency design inherited from Course 2.

## Failure checklist

- Does every synchronous journey have one absolute owner deadline?
- Can a child call reset or exceed the remaining budget?
- Is cancellation incorrectly treated as rollback?
- Can any configured retry repeat a mutation without persistent idempotency?
- Are retry demand, backoff, and attempt counts bounded?
- Is there an authoritative reconciliation path after post-commit response loss?

## Transition

After preserving the checkpoint evidence, continue to **Streaming RPCs, Flow Control, and Backpressure**. Do not progress while the non-compensable gate remains unresolved.
