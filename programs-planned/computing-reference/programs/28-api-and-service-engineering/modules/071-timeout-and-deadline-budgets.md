---
module_id: API-071
program: API & Service Engineering
level: 2
module_number: 71
title: Timeout and Deadline Budgets
status: complete
last_verified: 2026-09-02
---

# Timeout and Deadline Budgets

## One-Page Review

### Governing question

How should one end-to-end latency objective become propagated deadlines and bounded queue, connection, attempt, lock, stream, cleanup, and retry budgets so that late work stops instead of consuming capacity or causing ambiguous effects?

### Essential definitions

- A **timeout** is a maximum duration allowed for an operation or phase; a **deadline** is an absolute point after which a result is no longer wanted.
- A **latency SLO** is a statistical objective for a population of valid requests; it is not the timeout of every individual request.
- An **end-to-end budget** is the remaining time from admission to the caller's deadline after transit, response, and safety reserves.
- **deadline propagation** carries the caller's remaining time through downstream calls rather than starting a fresh full timeout at each hop.
- **cancellation** signals loss of interest; cooperative code must stop queued, running, and spawned work and release resources.
- A **phase timeout** bounds DNS, connection, TLS, request write, response headers/body, queue wait, lock wait, or another distinct phase.
- A **minimum useful-work floor** is the least remaining budget in which a server can reasonably begin and complete a class of request.
- An **uncertain outcome** occurs when a deadline/timeout fires after an effect may have committed but before the caller observes its result.

### Central model, mechanism, or theorem

For caller deadline $D$, current monotonic time $t$, response/transit reserve $r$, the usable remaining budget is

$$
B(t)=D-t-r.
$$

For serial stages, planned budgets plus reserves must fit $B$; for parallel branches, the critical-path maximum plus join/response reserve must fit. Every downstream attempt receives at most the current $B(t)$, never the original timeout. If remaining budget is below admission/work floor, fail fast before allocating scarce resources.

### Critical invariants

Every externally initiated request has a realistic deadline derived from user/workflow need and measured distributions. Deadline is propagated as remaining duration using monotonic elapsed time where possible; downstream timeouts never exceed it. Queue wait, connection establishment, lock acquisition, execution, response transfer, retries/hedges, and cleanup are bounded separately where libraries require it.

Expired/cancelled work stops cooperatively across fan-out, workers, database calls, streams, and spawned tasks; stale owners cannot commit. A timeout is not proof of failure: non-idempotent writes use stable idempotency/effect IDs and outcome query/reconciliation. Servers reject impossible budgets and overload early. Metrics distinguish caller deadline, server cancellation, queue timeout, connect/TLS, dependency, lock, body/idle, local overload, late completion, and unknown outcome.

### Common failures

No timeout; one large socket timeout; same timeout restarted at every hop; timeout equal to p99 with no network/queue/tail margin; confusing SLO and deadline; wall-clock timestamps trusted across hosts; negative/expired budget ignored; equal budget split across unequal stages; serial sum omitted; parallel work budgeted as sum or fan-out tail ignored; queue wait excluded; DNS/TLS/connect/body phases unbounded; server continues after caller leaves; cancellation not propagated to child tasks; transaction/lock outlives request; retry begins without enough remaining time; timeout response triggers a new non-idempotent effect; stream idle and total lifetime conflated; and timeout metrics collapsed into generic errors.

### Compact example

A checkout has 900 ms caller deadline. Ingress/egress/safety reserve 120 ms, leaving 780 ms. Two parallel reads receive at most 300 ms each, but the critical path costs 300 ms, not 600; a 350 ms payment authorization follows, leaving 130 ms for join/local commit/response. At 180 ms remaining the server refuses a retry whose measured minimum useful attempt plus response reserve is 220 ms. **Conclusion:** the propagated remaining budget—not per-service defaults—decides whether work can still help.

### Connections

[Deadlines, Cancellation, and Metadata](054-deadlines-cancellation-and-metadata.md) introduces transport propagation. [Delivery and Acknowledgment](066-delivery-and-acknowledgment.md) and [Idempotent Consumers](067-idempotent-consumers.md) handle asynchronous ownership and uncertain effects. The next modules add retry/backoff, circuit breakers/bulkheads, load shedding, and resilience verification.

## Governing Question

Given a user's or workflow's end-to-end willingness to wait, what measured budget and cancellation contract should every synchronous, asynchronous, queued, fan-out, streaming, transactional, and external-effect boundary enforce?

## Why This Matters

Distributed systems fail slowly as often as they fail explicitly. A dependency accepts work but queues it; a connection stalls in DNS or TLS; a lock waits; one fan-out shard becomes pathological; a client disconnects while the server continues expensive computation. Without bounds, in-flight work accumulates, consuming memory, threads, sockets, file descriptors, database connections, locks, and downstream capacity.

An arbitrary short timeout also causes harm. Healthy tail requests fail, retries amplify load, cold connections or large valid requests never succeed, and committed effects appear failed to callers. The correct question is not “what timeout is standard?” It is “how long is this outcome useful, what latency distributions and failure modes exist, and how does the remaining budget shrink along the critical path?”

Google SRE documents missed deadlines and cancellation as cascading-failure controls. gRPC defines a deadline as the point past which the client is unwilling to wait, recommends explicit realistic deadlines, and supports propagation as remaining timeout to reduce clock-skew problems. AWS Builders' Library describes selecting timeouts from downstream latency distributions while accounting for false-timeout rate, network/TLS setup, retries, and jitter. These are mechanisms and guidance, not one universal number.

Timeouts also create epistemic uncertainty. A client can time out after a server commits a payment or database write. Cancellation cannot roll back an already committed effect. Safe APIs therefore combine deadlines with idempotency keys, status resources/outcome query, reconciliation, and explicit response semantics.

## Prerequisites and Retrieval

Retrieve [Long-Running Operations](018-long-running-operations.md), [Idempotency Keys](037-idempotency-keys.md), [Rate Limits and Quotas](039-rate-limits-and-quotas.md), [Deadlines, Cancellation, and Metadata](054-deadlines-cancellation-and-metadata.md), [Delivery and Acknowledgment](066-delivery-and-acknowledgment.md), and [Idempotent Consumers](067-idempotent-consumers.md). Be able to draw the request critical path and every queue/resource/effect boundary.

Retrieve user/workflow latency requirements, client/server/proxy/load-balancer/mesh/library timeout semantics and defaults, DNS/connect/TLS/pool behavior, request/response size distributions, service/dependency latency histograms by outcome, queue and saturation behavior, database lock/statement timeouts, retry/hedge policy, stream heartbeat/idle behavior, cancellation APIs, external idempotency/query semantics, and trace/metric conventions.

## Learning Objectives

After completing this module, you can:

1. distinguish timeout, absolute deadline, cancellation, latency SLO, TTL, and lease;
2. derive an end-to-end budget from user value, latency distributions, and reserves;
3. allocate budgets over serial and parallel critical paths without restarting time;
4. propagate remaining time safely across clocks, protocols, queues, and asynchronous work;
5. bound connection, pool, queue, lock, execution, response, streaming, and cleanup phases;
6. reject impossible or stale work before scarce-resource allocation;
7. fit retries and hedges within one deadline and capacity budget;
8. stop cancelled work while protecting committed/uncertain effects with identities;
9. observe and diagnose deadline failures by phase, owner, budget, and saturation; and
10. verify deadlines with tail-load, clock, cancellation, crash, and ambiguous-outcome tests.

## Core Exposition

### Separate the time concepts

A timeout is relative: allow this call/phase up to 200 ms. A deadline is absolute within the request's time domain: result is useful until $D$. At the first hop, timeout can be converted to deadline. Each next hop should receive remaining time after elapsed work, not another 200 ms.

A latency SLO describes a distribution such as 99% of valid reads below 300 ms over a window. It guides capacity and deadline design but is not the per-request cutoff. A deadline may be above the SLO threshold to avoid excessive false timeouts, or lower for an interactive abandonment boundary. Publish both explicitly.

TTL/expiry says when a queued command/message is no longer relevant; a lease/visibility deadline says when ownership may be reassigned. Neither is identical to an RPC deadline. A business command may expire at 15:00 while each delivery attempt has a 2-second processing deadline and 30-second lease.

Cancellation communicates lost interest. It is not rollback, interrupt-safety, or proof no effect happened. Code and dependencies must cooperate; cleanup may need a small bounded non-cancellable context to release resources/record outcome without continuing business work.

### Start with user and workflow value

Define workload classes separately: interactive read, interactive write, machine batch, webhook, administrative export, background workflow, stream establishment. One service-wide timeout ignores different value and cost curves.

For each class ask when the caller abandons, whether a partial/degraded answer is useful, whether work can continue asynchronously, whether the operation is safe to retry, and which terminal outcome the caller needs. Mobile/global clients include network variance distinct from internal RPCs.

Measure successful/error/cancelled latency distributions, queue wait, connection setup, payload sizes, regions, cache hits/misses, hot tenants/keys, deployment cold starts, and saturation. Mean latency hides tails and bimodal failures. Select an acceptable false-timeout rate and test it under load/failure, not only steady-state p99.

Budget from the outside in. Internal teams do not add their favorite default and force the caller to wait for the sum. If required stages cannot fit the user's useful deadline at safe percentiles, redesign with caching, precomputation, parallelism, degraded response, asynchronous acceptance/status, or a different product contract.

### Compute remaining budget

At ingress record a monotonic start and absolute/relative caller constraint. Reserve response serialization/transit, cleanup, proxy skew/rounding, and safety margin. Then

$$
B(t)=\max(0,D-t-r).
$$

Recompute before each queue, retry, and downstream call. Never cache the initial $B$. If the protocol sends an absolute wall-clock deadline across hosts, clock skew can make it expire too early/late; gRPC propagation converts to remaining timeout while deducting elapsed time. Bound and monitor clock health regardless.

Clamp untrusted caller deadlines to service minimum/maximum policy. A huge deadline must not reserve resources indefinitely; a negative/tiny deadline should fail before authentication-expensive/body-heavy work when safe, while still performing necessary security/accounting. Internal default applies only when the caller omitted a deadline and contract permits it.

Carry deadline/budget separately from trace ID and business command expiry. Intermediaries must not drop or reset it. Document units, precision, overflow, max, and absent/invalid behavior.

### Allocate serial critical paths

For serial stages $i$ with planned upper budgets $b_i$, transit/join/response reserves $r_j$, require

$$
\sum_i b_i+\sum_j r_j\le B_0.
$$

This is a planning constraint, not permission for every stage to consume its full slice regardless of current remaining time. A fast earlier stage leaves more time; a slow stage reduces every later call. Each stage uses $\min(b_i,B(t)-future\ reserve)$.

Allocate based on measured latency/cost/variance/criticality and minimum useful time, not equal division. A 10 ms cache lookup and 300 ms fraud model should not each receive half. Keep a final response/commit reserve so success can be returned before caller departure.

Optional stages have skip/degraded thresholds. If personalization needs 80 ms minimum and 50 ms remains, omit it rather than begin doomed work. Required stage with insufficient floor fails fast with a typed deadline/budget result.

Avoid double-counting overlapping work and omitting hidden stages such as pool acquisition, queueing, serialization, proxy transit, retries, and cleanup.

### Allocate parallel and fan-out paths

For parallel branches, latency critical path is approximately maximum branch completion plus fan-out/join/response—not sum. Resource cost still sums. A 100-way fan-out can meet time budget while exhausting capacity or making tail probability severe.

Give each branch a deadline no later than parent remaining time and cancel losers/unfinished branches once result/quorum/error makes them unnecessary. Bound fan-out width, per-tenant concurrency, response size, and aggregation memory. Decide all, quorum, fastest, partial, or fail-fast semantics.

Tail amplification grows with branch count: even low per-branch slow probability makes at least one slow branch likely. Measure whole request and branch order statistics. Hedging duplicates work and belongs under explicit delay, idempotency, global budget, and cancellation/capacity controls.

Join logic needs budget to aggregate/validate/serialize. Do not let branches consume until parent deadline and then attempt an impossible response.

### Bound every client phase

Many “request timeouts” exclude or blur DNS resolution, connection-pool wait, TCP/QUIC connect, TLS handshake, proxy negotiation, request upload, time to headers, response-body read, and idle gaps. Inspect actual client/runtime semantics.

Set phase bounds under the overall deadline. Connection setup can justify a separate larger first-use allowance, connection prewarming, or deployment readiness; it should not silently recur inside a tiny request timeout. Pool acquisition should fail before request send when saturated.

Response headers are not completion. Bound body/stream read, bytes, decompression, and idle progress. A peer can drip bytes forever under a per-read timeout unless total deadline exists. Conversely, one total timeout may be wrong for a deliberately long stream; define establishment, idle/progress, heartbeat, maximum lifetime/renewal, and cancellation separately.

Record the phase that timed out. Generic “context deadline exceeded” without client/server/phase/dependency loses remediation evidence.

### Budget queues, admission, and execution

Queue wait consumes user deadline and often signals saturation. Carry enqueue time/deadline; use earliest-deadline/priority only with fairness and starvation controls. Drop expired work before execution. Bound queue length, age, bytes, and per-tenant share.

At admission compute remaining budget and predicted/minimum useful work for request class. Reject when impossible, overloaded, dependency unhealthy, or caller already cancelled. Early overload response preserves capacity better than letting all requests time out late.

Separate queue timeout from execution timeout. A request that spent 280 ms queued should not receive the original 300 ms execution allowance. Servers periodically check cancellation/deadline at safe points, especially before expensive fan-out/effects and after checkpoints.

Use bulkheads/concurrency limits to keep slow tenants/keys from occupying every worker. Little's Law links longer latency with more in-flight work; overly long deadlines can turn a small slow fraction into resource exhaustion.

### Align database and resource timeouts

Bound connection-pool acquisition, transaction duration, statement/query execution, lock wait, and commit response under request remaining time. Configure server-side database limits so work stops even if application cancellation is delayed or connection breaks.

Do not hold a transaction/lock while waiting on an unbounded remote call. Transaction cancellation/rollback and connection reuse need verified driver behavior. A client timeout can leave query running; test cancellation and discard/repair poisoned connections.

Commit is an ambiguity boundary. If client deadline fires during commit, query authoritative transaction/business outcome by stable operation ID. Never retry a non-idempotent write with a new ID. Some cleanup/outcome recording may continue after caller deadline under a separate bounded durable workflow, but this is explicit transfer of ownership—not ignored cancellation.

Lock timeout may be shorter than statement/transaction deadline to fail contention early. Classify serialization/deadlock/lock/deadline outcomes for retry module; all attempts still fit original business deadline.

### Propagate cancellation correctly

When caller disconnects, deadline expires, fatal prerequisite fails, or one parallel result wins, cancel descendant RPCs, queries, queued tasks, hedges, timers, and streams. Do not create a background/root context just to avoid cancellation unless work is durably accepted as a separate operation.

Every spawned task has ownership and join/cleanup. Libraries that do not accept cancellation need isolation and concurrency/time limits. Cancellation handlers are idempotent and bounded; they release leases/locks/buffers and record safe state but do not mask original outcome.

Cancellation races with completion. If effect commits first, cancellation does not undo it; record result. If cancellation wins before commit, conditional/fenced transaction prevents late write. Test both interleavings and stale worker behavior.

Propagate fatal errors upward and cancel siblings; continuing a doomed call consumes resources. For optional branches, typed degradation may keep parent alive.

### Fit retries inside one deadline

An attempt timeout is not the end-to-end deadline. Before retry, reserve backoff, connection/setup, minimum useful attempt, and final response. If they do not fit, return the current best/uncertain outcome instead of a doomed attempt.

Retry only classified transient/idempotent operations, at one chosen layer where possible. Nested retries multiply attempts and consume the deadline unpredictably. Preserve the same operation/effect ID. Exponential backoff with jitter is bounded by remaining time and server `Retry-After`/load signal.

Attempt timeouts may be shorter than overall deadline to allow another endpoint, but too short creates false timeouts and retry load. Derive from measured distribution/failure isolation. Retry budget limits added load independently of time.

Hedging starts another equivalent attempt before first finishes to reduce tail. It is safe only for idempotent/read operations or stable effect identity, uses a percentile-informed hedge delay, counts against capacity, and cancels losers. Do not hedge into an overloaded dependency.

### Handle asynchronous boundaries

For durable asynchronous acceptance, synchronous deadline ends after the service commits inbox/job plus returns operation ID. The workflow then has business deadline/expiry/SLO independent of RPC. Status/result APIs communicate eventual outcome.

Propagate original command expiry/deadline where late execution is unsafe, but each delivery attempt receives its own processing/lease budgets. A broker message TTL does not stop a consumer effect already started; handlers recheck current relevance and cancel/fence work.

Do not keep a request/connection open across an hours-long workflow merely to preserve one deadline. Transfer ownership durably, acknowledge the boundary honestly, and make cancellation/withdrawal a domain command with state-machine semantics.

Dead-letter/redrive revalidates deadline, authorization, idempotency, and effect outcome. Historical replay of facts preserves occurred time but projection processing has a replay-run budget, not the original RPC timeout.

### Design timeout response semantics

Distinguish caller deadline exceeded, server admission insufficient budget, local queue/pool/connect/TLS/lock/statement/response idle, upstream deadline, cancellation, overload, and unknown completion. Map to protocol status without losing machine-readable cause/phase/retryability.

HTTP 408/504 and gRPC `DEADLINE_EXCEEDED` have protocol meanings, but application error bodies/metadata should expose safe operation ID, whether accepted, and status-query guidance. Do not claim “failed” if outcome is unknown. Do not leak topology or sensitive timing.

For writes, prefer `accepted` plus operation resource when durable transfer occurred, confirmed domain result when known, or `unknown—query by id` after ambiguous transport. A gateway timeout does not prove origin rolled back.

Clients must not automatically retry every timeout. Contract states idempotency requirements, same-key behavior, expiry, retry hints, and query/reconciliation.

### Observe budgets and tail behavior

Record client-requested deadline bucket, remaining budget at ingress/egress/downstream start, queue/pool/connect/TLS/lock/execution/serialization durations, attempt number, cancellation source, timeout phase/type, response after caller cancellation, unknown outcomes, and resource saturation. Avoid raw user-controlled high-cardinality values.

Trace parent/child critical path and parallel overlap. OpenTelemetry RPC conventions identify RPC methods/status/errors; add stable application deadline/budget events/attributes under governed conventions rather than inventing inconsistent labels.

Plot full latency distributions by success/error/cancel and workload class, plus deadline utilization ratio and wasted-after-cancel work. Timeout-induced censoring means observed successful p99 excludes slower timed-out requests; view timeouts and latency together.

Alert on shifts in queue age, near-deadline starts, upstream-versus-local timeouts, cancellation propagation delay, late completions, retry amplification, and unknown effect age—not a raw timeout count alone.

### Verify under realistic faults

Unit/property tests use fake monotonic clocks to ensure remaining budgets only decrease, children never exceed parent, expired work does not start, and serial/parallel allocation fits. Test absent, zero, negative, maximum, overflow, rounding, clock skew, and cancellation/completion races.

Integration tests stall DNS/connect/TLS/headers/body, exhaust pools, queue work, hold locks, slow queries, disconnect callers, ignore cancellation, delay commit response, fan out to slow shards, retry/hedge, and interrupt streams. Assert resource release, child cancellation, idempotent outcomes, and typed errors.

Load tests create realistic bimodal/tail latency, cold connections, payload sizes, hot tenants, saturation, deploy/restart, and dependency outage. Verify deadlines prevent in-flight explosion while false-timeout/error budget remains acceptable.

Chaos tests break propagation at one hop, skew wall clocks, lose cancellation packets/connections, and make dependencies complete after timeout. Reconcile operation IDs/effects so “timed out” never substitutes for verified outcome.

## Definitions and Notation

Let caller deadline be $D$, monotonic current time $t$, response/safety reserve $r$, and usable budget $B(t)=\max(0,D-t-r)$. Let serial stage budgets be $b_i$, parallel branch completion times $p_j$, queue time $q$, and minimum useful-work floor $w_{min}$.

Admission requires $B(t)\ge w_{min}+r_{local}$ for the required work class. A serial plan requires $\sum b_i+\sum r_i\le B_0$; parallel critical time is approximately $\max_j p_j$ plus fan-out/join reserves, while resource work is closer to $\sum_j p_j$.

Let arrival rate be $\lambda$, mean in-system time $W$, and mean in-flight work $L$. Under stable Little's Law assumptions, $L=\lambda W$; long timeout-driven $W$ can exhaust bounded concurrency even when only a small fraction stalls.

## Mechanisms, Invariants, or Proof Structure

1. Define workload-specific user/workflow usefulness, latency SLO, expiry, and accepted false-timeout rate.
2. Measure full phase/tail distributions under normal, cold, saturated, and failed conditions.
3. Establish one caller deadline and reserve response, cleanup, transit, skew, and safety time.
4. Recompute/propagate remaining budget; clamp untrusted extremes and reject expired/impossible work early.
5. Allocate serial/parallel critical paths and bound pool/queue/connect/TLS/lock/execution/body/stream phases.
6. Propagate cooperative cancellation to every child/query/task and fence late commits.
7. Fit classified retries/hedges/backoff plus final response within the original deadline and capacity budget.
8. Transfer long work durably to asynchronous operation state instead of extending RPC indefinitely.
9. Resolve timeout-after-effect ambiguity with stable IDs, status query, ledger, and reconciliation.
10. Observe phase/budget/tail/waste and verify propagation, resource release, ambiguity, and overload under faults.

Proof sketch: if every child deadline is no later than its parent's current remaining budget, all queued/running descendants observe cancellation, and admission rejects work below completion floor, then work cannot intentionally outlive caller usefulness except separately durable accepted workflows/cleanup. This bounds resource residence under stated cancellation latency. It does not prove an effect did not commit before timeout; that requires idempotency/outcome protocols.

## Alternatives and Trade-Offs

**Relative timeout versus absolute deadline.** Relative is easy locally but restarts accidentally; absolute preserves end-to-end intent but needs safe clock/translation. Propagate remaining duration with monotonic elapsed accounting.

**Static per-hop budgets versus dynamic remaining budget.** Static is predictable but wastes slack/fails under path variation. Dynamic uses available time but needs downstream floors/reserves and prevents one stage consuming all.

**Tight timeout versus loose timeout.** Tight reduces resource residence but raises false failures/retries. Loose accommodates tails/cold paths but can amplify saturation. Measure class-specific distribution and error budget.

**Fail fast versus queue.** Fail-fast protects capacity and tail under overload; queue absorbs brief bursts but consumes deadline/memory and hides saturation. Use bounded age/length/fairness.

**Synchronous wait versus asynchronous acceptance.** Sync gives immediate outcome but holds resources. Async handles long work but requires operation state, notification/polling, expiry/cancel, and durable ownership.

**All-result fan-out versus quorum/partial.** All preserves completeness but amplifies tail; quorum/partial improves latency/availability only when product semantics disclose and tolerate missing data.

**Retry versus hedge.** Retry follows failure/timeout and adds latency/load; hedge overlaps attempts and reduces tail at higher immediate cost. Both require idempotency, one deadline, and budgets.

**Total stream deadline versus idle/progress timeout.** Total caps resource lifetime; idle supports legitimate long streams. Often use establishment+idle+max-lifetime renewal with explicit semantics.

## Failure Modes and Misconceptions

1. No deadline or effectively infinite library default.
2. One timeout starts anew at every hop, making end-to-end time unbounded.
3. Latency SLO percentile is copied directly into per-request timeout.
4. Mean/healthy p99 ignores errors, cold starts, queueing, network, or bimodal tail.
5. Caller wall-clock deadline is trusted without skew/remaining-time conversion.
6. Negative/tiny/huge untrusted deadline is not clamped or rejected.
7. Equal per-hop split ignores criticality, variance, floors, and response reserve.
8. Parallel branch resource cost/tail amplification is ignored.
9. DNS, connect, TLS, pool, upload, headers, body, lock, or queue is outside the bound.
10. Server/client child work continues after caller cancellation/deadline.
11. Database query/transaction/lock outlives request and consumes pool capacity.
12. Retry/hedge starts without room for backoff, useful attempt, and response.
13. Nested retries multiply attempts and deadline consumption.
14. Timeout is treated as proof that write/payment/email did not happen.
15. New idempotency/effect ID is generated after ambiguous timeout.
16. Async command TTL, lease, RPC deadline, and workflow SLO are conflated.
17. Long stream uses only per-read timeout and can drip forever.
18. All timeouts become one generic metric/status, obscuring owner and remediation.

## Worked Examples

### Example 1

A 500 ms read reserves 60 ms for response/transit and 40 ms safety. Cache gets 30 ms; on miss, database gets at most current remaining minus 100 ms. If queueing consumes 250 ms, the database call is not granted the original 370 ms.

### Example 2

Three serial services each start a 1-second timeout from one 1-second caller request. Worst path approaches 3 seconds plus transit. Propagating remaining duration makes the second/third reject or shorten work instead of resetting intent.

### Example 3

Twenty parallel shards each have 1% chance of exceeding deadline independently. Probability at least one is slow is $1-0.99^{20}\approx18.2\%$. An all-shard join has much worse tail than one shard; quorum/partial or architecture may be needed.

### Example 4

TLS setup consumes 180 ms only on new connections while warm calls take 25 ms. A 100 ms total timeout fails deployments/cold clients. The system prewarms connections and budgets setup separately rather than making every request wait indefinitely.

### Example 5

A request waits 240 ms in a queue with 300 ms deadline and needs at least 100 ms execution plus response. Admission rejects immediately at dequeue, saving database work that cannot arrive on time.

### Example 6

Client times out during payment commit. It retries `capture-71` with the same effect ID/status query. Provider reports captured; API returns recorded outcome. A fresh key would risk double capture.

### Example 7

One fan-out branch succeeds and supplies quorum; parent cancels nine siblings. Each sibling cancels its database query and releases pool slot. Without propagation, the user sees fast response while backend still pays full cost.

### Example 8

A streaming subscription has 5-second establishment deadline, 45-second idle/heartbeat timeout, and 30-minute renewable lifetime. One 45-second total deadline would incorrectly kill healthy long sessions; no lifetime would leak abandoned resources.

### Example 9

Five percent of 1,000 QPS stalls for 100 seconds: stalled work alone demands 5,000 concurrent slots. Reducing/failing the pathological path early and bulkheading tenants prevents a small slow fraction from consuming a 1,000-worker frontend.

### Example 10

A batch job is durably accepted in 400 ms and returns operation ID under the RPC deadline. Its 2-hour workflow SLO, per-step deadlines, retries, cancellation command, and result state are separate; the original HTTP connection is not held open.

## Cross-Program Connections

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies partial failure, clocks, cancellation, leases, retries, and ambiguity. [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies scheduling, queues, threads, sockets, timers, and resource cleanup.

[Database Engineering](../../18-database-engineering/ROADMAP.md) supplies transactions, locks, statements, cancellation, idempotency, and commit uncertainty. [Network Engineering](../../24-network-engineering/ROADMAP.md) supplies DNS, connection, TLS, transport, congestion, and proxy phase behavior.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns client/mesh defaults, admission, telemetry, load tests, and rollout policy. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes end-to-end budgets, interface allocation, margins, failure analysis, and verification. [Security Engineering](../../25-security-engineering/ROADMAP.md) contributes abuse-resistant clamps, tenant fairness, and safe error disclosure.

## References

1. gRPC Authors. “Deadlines.” Retrieved 2026-09-02. <https://grpc.io/docs/guides/deadlines/>
2. gRPC Authors. “Cancellation.” Retrieved 2026-09-02. <https://grpc.io/docs/guides/cancellation/>
3. Amazon Web Services. “Timeouts, Retries, and Backoff with Jitter.” Amazon Builders' Library. <https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/>
4. Beyer, Betsy, et al. “Addressing Cascading Failures.” *Site Reliability Engineering*. <https://sre.google/sre-book/addressing-cascading-failures/>
5. Beyer, Betsy, et al. “Service Level Objectives.” *Site Reliability Engineering*. <https://sre.google/sre-book/service-level-objectives/>
6. OpenTelemetry Authors. “Semantic Conventions for RPC Spans.” Retrieved 2026-09-02. <https://opentelemetry.io/docs/specs/semconv/rpc/rpc-spans/>
7. IETF. “RFC 9110: HTTP Semantics.” June 2022. <https://www.rfc-editor.org/rfc/rfc9110>

## Exercises

### Exercise 1

Design a 1.2-second end-to-end budget for checkout with ingress/auth, two parallel reads, serial fraud and payment, local commit, and response. Allocate floors/reserves, show the critical path, define degraded/early rejection, and state how remaining time is propagated.

### Exercise 2

A frontend handles 2,400 QPS. Normally 97% complete in 80 ms; 3% stall until a 20-second deadline. Estimate mean in-flight work by Little's Law under this mixture. Recompute with a 2-second deadline for the stalled class and explain assumptions/risks.

### Exercise 3

Design timeout/cancellation semantics for a write that acquires a pool connection, waits on a lock, commits a database transaction, and calls an idempotent payment provider. Include phase budgets, propagation, transaction boundaries, ambiguous outcomes, retries, cleanup, and response codes.

### Exercise 4

Design deadlines for an API that fans out to 60 shards and can return either all results or a documented 55-of-60 partial. Include branch budgets, tail amplification, quorum cancellation, concurrency/bulkheads, retry/hedge, aggregation reserve, and observability.

### Exercise 5

Create a verification plan for deadline propagation across browser, gateway, three services, database, queue-backed workflow, and stream. Cover clocks, missing/invalid metadata, every timeout phase, cancellation, late effects, overload, cold starts, telemetry, and disaster/failover.

## Answers to the Exercises

### Answer 1

Reserve 100 ms ingress/auth, 100 ms response/transit/safety, leaving 1,000 ms internal. Run inventory and customer reads in parallel with 220 ms branch caps plus 30 ms fan-out/join; their critical allowance is 250 ms, not 470. Allocate fraud 220 ms, payment 350 ms, local transaction 100 ms, and 80 ms slack/serialization between stages: $100+250+220+350+100+80+100=1,200$ ms.

At runtime these are caps/floors, not reset timeouts. Gateway converts caller constraint to deadline; each service deducts monotonic elapsed and downstream/final reserves, passing `min(stage cap,current remaining-future reserve)`. Reads can degrade only if contract permits—for example omit recommendations, never inventory correctness. If fraud/payment remaining time is below measured useful floor plus commit/response reserve, reject/return typed deadline result before call.

Cancel the other read if a required sibling/fatal prerequisite makes checkout impossible; cancel all descendants on caller loss. Payment receives stable effect ID and outcome-query path because deadline during authorization is ambiguous. Metrics record requested/remaining budgets and phase durations; load tests validate the 1.2-second plan under cold/TLS, queue, tail, and saturation.

### Answer 2

Mean residence time under the simplified two-point mixture is $0.97\times0.08+0.03\times20=0.6776$ seconds. Little's Law gives $L=2{,}400\times0.6776=1{,}626.24$ mean in-flight requests.

With a 2-second deadline for the stalled 3%, mean residence is $0.97\times0.08+0.03\times2=0.1376$ seconds, giving $L=2{,}400\times0.1376=330.24$. The shorter bound reduces modeled in-flight demand by about 1,296.

This assumes stable arrivals, independent fixed classes, immediate cancellation/resource release at deadline, no queueing/retries/secondary slowdown, and capacity sufficient for the resulting concurrency. A 2-second cutoff may create false failures, retry amplification, or interrupt useful long operations. Measure the real distribution/outcomes, fail pathological work earlier when identifiable, propagate cancellation, bulkhead, and verify user SLO/error budget rather than choosing 2 seconds only from arithmetic.

### Answer 3

From one caller deadline reserve final response/status query and cleanup. Bound pool acquisition first; if saturated or remaining below transaction floor, fail before begin. Start a short transaction; set database transaction/statement/lock timeouts below remaining deadline, with lock wait shorter than execution. Do not hold the database transaction across payment network call.

Persist operation/effect intent plus business preconditions durably, then call payment under `min(provider cap,remaining-payment reserve)` using stable payment effect ID. Provider timeout moves intent to uncertain; query/retry same ID according to provider contract. On confirmed payment, a new bounded local transaction conditionally commits business state/outbox under operation ID/fencing. If local commit response is lost, query operation/business state before retry.

Propagate cancellation to pool wait, lock/query, provider, and child tasks, but cancellation cannot undo committed payment/DB. Cleanup releases/discards connections, rolls back open transaction, records safe uncertain state, and schedules reconciliation under a separate bounded durable workflow. Do not continue the business call on a detached context.

Return confirmed success/domain failure when known; insufficient-budget/admission/deadline with machine phase and retry guidance when no effect began; accepted+operation ID after durable async transfer; or unknown+status URI/operation ID when effect may have committed. HTTP/gRPC mapping follows protocol, but contract never equates timeout with rollback. Retries preserve IDs and fit original business deadline or async workflow policy.

### Answer 4

Define two operations/modes: strict all-60 and explicitly partial 55-of-60 with missing-shard metadata/freshness semantics. Parent reserves fan-out dispatch, aggregation/validation, serialization/response. Each branch receives no later than current parent deadline and a measured cap; bound total and per-tenant fan-out concurrency/bytes. Bulkhead shard/client pools so 60 calls per request cannot exhaust the service.

For strict mode, whole latency follows the maximum branch; calculate/measure order statistics and reject when remaining cannot cover branch plus join. For partial mode, once 55 valid results arrive and product criteria hold, cancel the five outstanding branches/queries and aggregate. Fatal consistency/security errors may fail fast instead of partial.

Retry only classified idempotent branch reads and only if backoff+minimum attempt+join fits. A percentile-delayed hedge may target unusually slow shards under a global hedge/retry budget and spare capacity; cancel loser, avoid overloaded shards, and never multiply across layers. Consider caching/preaggregation if all-60 tail is intrinsically incompatible.

Observe parent mode/result count, branch latency/error/deadline, slow/missing shards, remaining budget at dispatch/completion, fan-out width, retries/hedges/cancellations, work after cancel, pool/queue saturation, aggregation duration, partial rate, and live SLO. Test correlated shard failures—not just independent 1% tails—plus cold starts, one hot shard, network partition, and cancellation races.

### Answer 5

Create an end-to-end test matrix for present/absent/zero/negative/huge/malformed/overflow deadlines, browser/gateway maximums, units/rounding, wall-clock skew, monotonic elapsed deduction, metadata loss/reset at each hop, and client disconnect. Assert every child deadline is no later than parent remaining and final response reserve remains.

Fault each phase: DNS, connect, TLS, gateway queue, pool acquisition, request upload, headers/body idle, service queues/execution, fan-out, database lock/statement/commit response, broker acceptance, workflow step, stream establishment/heartbeat/idle/lifetime. Exhaust pools/workers/tenant quotas and run cold deploy/failover. Verify early admission/load shedding, bounded in-flight work, typed phase/status, and false-timeout/error-budget behavior.

At each service cancel parent and assert descendant RPCs, queries, queued jobs not durably accepted, timers, hedges, and streams stop/release resources within an SLO. Race cancellation with local/external commit and reconcile stable operation/effect IDs. Durable queue acceptance must return operation ID and transfer to workflow deadline; expired commands do not execute. Stream tests distinguish idle from total lifetime and renew safely.

Telemetry assertions cover client/server spans, method/status/error, requested/remaining budget buckets, per-phase durations, queue age, attempt, cancellation source/latency, late completion, unknown outcome, resource saturation, and trace continuity without sensitive/high-cardinality leakage. Disaster tests restart gateway/services/database/queue during calls and restore operation/workflow state; final reconciliation proves every effect/outcome rather than counting timeouts as failures.
