# Module 37 Reasoned Solutions — Async Context and Diagnostic Boundaries

## A. Propagation

AsyncLocalStorage associates a store with async execution resources created under a scope. Await continuations and timers created inside the run generally observe the store. A resource created before context entry may not acquire the later store merely because it is awaited inside. Concurrent runs maintain separate associations even when resume order reverses. After the `run` callback completes, the caller’s prior store is restored.

## B. Authority

Tenant selection is a security-sensitive capability and should be an explicit parameter or branded client. Ambient context can be missing, inherited unexpectedly, or hard to audit. Correlation identifiers are observational and safe when small and immutable; large request bodies, mutable user objects, and credentials should not be retained.

## C. Diagnostics

Publishing with no subscribers should be cheap and have no product effect. Subscriber failure policy must be deliberate; the reference isolates it so diagnostics cannot fail the task. A stable channel name prevents unbounded channel creation, while run/task IDs remain structured message fields. Scheduler state, not diagnostics, owns terminal outcomes.

## D. Manager

`run` freezes a copied context and publishes start/end/error around the operation. `child` derives a new task context while preserving parent identity. Error is rethrown unchanged. Controlled deferred tests prove isolation. Subscription disposal proves observer lifetime.

## E. TaskHarbor and transfer

TaskHarbor uses context only to enrich diagnostics and execution logs. Domain decisions still receive explicit task specs and signals. A reusable library publishes to stable channels and behaves normally when no context or subscriber exists; the host application decides whether to subscribe.

## F. Context and signal solutions

Mutating one store object means descendants share the same reference; later edits can change what earlier operations observe. Freeze a copied store at each boundary and create child objects without modifying parent state. Parent restoration then follows `run` scope naturally.

For a broken callback boundary, isolate a minimal test, capture the current context, and invoke the callback inside an appropriate AsyncLocalStorage run or supported resource wrapper. Raw hooks expose every async resource and add complexity and overhead; they are not a substitute for understanding one integration boundary.

Run IDs are useful log/trace fields but poor metric labels. Task kind and bounded status can be labels. Credentials remain explicit secure data and must not enter diagnostics. Payload size can be a metric value or bucket. Tenant identity requires careful cardinality and privacy policy, not automatic ambient propagation.

## G. Context and diagnostics answers

Sharing one mutable store makes correlation schedule-dependent: nested work can overwrite the value observed by its parent or sibling. Use a fresh immutable store per logical operation and call `run` at the authority boundary. Explicit arguments still carry security capabilities and state-changing inputs.

Diagnostic payloads should be small facts published after the relevant transition: task accepted, task started, task terminal. No subscriber is a normal state. Channels should exclude source payloads, secrets, and unbounded error objects; normalize those before publication. A propagation test interleaves two runs and verifies every event’s correlation ID, then removes subscribers and proves product behavior is unchanged.

## H. Retention and boundary answers

The large document and response builder remain reachable as long as any async resource created inside the store remains reachable. Diagnostic context should usually contain stable IDs, attempt numbers, and small immutable tags. Domain objects and capabilities remain explicit parameters whose lifetimes are visible.

A callback adapter captures the current small store and re-enters it only while invoking the callback. The test should show correct correlation and should also decide whether a callback after parent completion is legal. If legal, the bounded context remains retained until callback release; if illegal, unregister or revoke it at the lifecycle boundary.

## I. Provenance answer

Context values need an accountable origin. Correlation IDs may be generated at ingress; validated tenant identities remain explicit capabilities; attempt numbers belong to the supervisor. Descendants may derive a child context but should not mutate the parent store. A small immutable translation at the boundary preserves diagnostic convenience without retaining or authorizing through the full request object.
