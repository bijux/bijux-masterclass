---
module_id: SEPAT-090
program: Software Engineering: Patterns
level: 2
module_number: 90
title: Combining Resilience Patterns Without Failure Amplification
status: complete
last_verified: 2026-08-29
---

# Combining Resilience Patterns Without Failure Amplification

## One-Page Review

### Governing question

How should deadlines, retries, idempotency, circuit breakers, bulkheads, rate limits, load shedding, fallbacks and durable messaging compose so a partial failure is contained rather than multiplied into more work, longer queues and a cascading outage?

### Essential definitions

- **failure amplification** occurs when a protective reaction increases work, contention, uncertainty or affected scope beyond the initiating failure.
- An **attempt** is one concrete dependency call; an **operation** is the caller's one semantic intent across attempts.
- A **retry owner** is the single layer authorized to schedule additional attempts for a dependency operation.
- A **retry budget** bounds extra attempts as a count/ratio/token resource across traffic, in addition to an absolute deadline.
- An **absolute deadline** is one end-to-end latest useful completion time propagated through layers; a timeout bounds one attempt/wait.
- A **bulkhead** bounds concurrent work/resources for one scope and isolates capacity.
- A **circuit breaker** suppresses calls recently likely to fail and admits controlled probes during recovery.
- A **rate limiter** enforces temporal policy; **load shedding** rejects/degrades work in response to current overload.
- **goodput** is useful correct outcomes completed within contract per unit time, distinct from attempts or raw responses.
- A **fallback** is an alternate result/path with an explicit authority, quality, cost and failure contract.
- A **recovery herd** is synchronized retries/probes/admission after apparent recovery.

### Central model, mechanism, or theorem

If layer \(i\) permits at most \(a_i\) total attempts for the operation it sees, nested independent retries can generate

\[
A_{max}=\prod_{i=1}^{m} a_i
\]

attempts at the deepest dependency before fan-out/hedging. Five layers with three attempts each can create \(3^5=243\) deepest calls from one original intent. With one retry owner allowing \(a\) total attempts, \(A_{max}=a\). This is a worst-case bound, not a traffic prediction. Runtime amplification also forms feedback: failures trigger retries, retries increase load/latency, which causes more timeouts/failures. Stability requires one end-to-end deadline, one retry authority/budget, bounded admission/concurrency/queues, idempotent effects, correctly scoped breakers, cheap shedding, jittered recovery and evidence from attempts through terminal outcome.

### Critical invariants

- Each semantic operation carries stable identity and one absolute deadline; attempts do not reset either.
- Exactly one layer owns retries for a dependency path; infrastructure/SDK defaults are inventoried and included in the same budget.
- Retry eligibility requires safe/idempotent effect semantics, a plausibly transient class, remaining deadline and available retry tokens.
- Backoff does not hold scarce bulkhead/connection/thread permits; every wait/queue consumes the deadline.
- Admission, queues, concurrency, fan-out and response/body buffers are finite at the resource they protect.
- Breaker state is scoped to a failure domain and observes attempts that reached it; local rejections do not falsely condemn a healthy dependency.
- Half-open probes are isolated, bounded and not multiplied by ordinary client retries.
- Rate limits, shedding and fallback responses communicate a stable retry disposition that upstream layers obey.
- Timeout/cancellation never claims rollback of an issued effect; retries preserve idempotency/effect identity.
- Recovery ramps with hysteresis/jitter and measured downstream headroom; backlog/live work share explicit capacity.
- Success is measured as end-to-end goodput/correctness/latency and terminal accounting, not individual pattern activation.

### Common failures

Common failures include retries in client, gateway, mesh, SDK and service simultaneously; resetting timeout at each hop/attempt; retrying overload, permission and schema errors; retrying non-idempotent calls with new keys; holding bulkhead permits during backoff; placing an unbounded queue before a bulkhead; opening one global breaker for one hot shard; counting local rate-limit rejection as dependency failure; letting every caller probe half-open; fallbacks that call the same failing dependency or bypass authorization; `Retry-After` causing synchronized herds; shedding after expensive/irreversible work; unlimited failover to another stressed region; caches that stampede on expiry; recovery that drains backlog at maximum speed; and dashboards counting attempts as traffic or defaults as authoritative success.

### Compact example

An API has a 900 ms absolute deadline. The gateway is the sole retry owner for an idempotent inventory read: at most three total attempts, but it schedules another only if backoff plus a 250 ms attempt and response reserve fit. A per-shard bulkhead caps in-flight calls; the shard breaker suppresses proven failures and uses isolated half-open probes. Rate policy and early load shedding bound ingress. Backoff releases permits. During outage the retry token bucket empties, breaker opens and low-value traffic sheds. Recovery jitters probes and ramps admission instead of releasing all queued/retrying clients.

### Connections

[SEPAT-081](081-retry-with-bounded-backoff.md) through [SEPAT-089](089-idempotent-consumer.md) provide the individual mechanisms this chapter composes. [SEPAT-079](079-producer-consumer-with-bounded-buffers.md) supplies finite queues, while [SEPAT-070](070-designing-an-integration-flow-from-message-semantics.md) provides end-to-end flow reasoning. The successor [Repository](../ROADMAP.md) begins the data/evolution block and should remain independent of these transport-resilience responsibilities.

## Governing Question

How can engineers compose individually sensible resilience mechanisms into one controlled feedback system with explicit ownership, budgets and evidence—rather than a stack whose hidden defaults multiply calls and prolong failure?

Patterns do not compose automatically. Retry assumes spare capacity and safe repetition; a bulkhead assumes rejected work will not immediately retry elsewhere; a breaker assumes its observations represent the dependency; a timeout assumes late effects are handled; shedding assumes clients do not amplify rejection; fallback assumes lower cost and truthful authority. Each mechanism changes the input seen by the others.

## Why This Matters

Distributed outages often begin as a modest slowdown or loss of one replica. Requests stay resident longer, consuming threads/connections. Timeouts trigger retries. Nested layers multiply attempts. Queues grow and deadlines expire while work continues. Health checks fail, routing moves traffic to fewer peers, and fallback warms cold dependencies. A system designed for redundancy becomes a positive-feedback amplifier.

Conversely, overaggressive protection can cause an avoidable outage: a global breaker opens because one tenant/shard failed; retry budgets exhaust from local validation errors; shedding rejects critical reconciliation; timeouts are shorter than normal TLS setup; half-open probes never receive isolated capacity. Composition needs a causal model, not maximum strictness.

The design unit is an end-to-end critical journey and its resource/effect graph. For each edge, name semantic identity, time budget, concurrency/capacity, failure classification, retry owner, circuit scope, fallback, and terminal evidence. Then test interactions beyond saturation and through recovery.

## Prerequisites and Retrieval

Learners should retrieve:

- offered/admitted load, utilization, queues, Little's Law and nonlinear saturation;
- absolute deadlines, per-attempt timeout, cancellation and ambiguous effects;
- bounded exponential backoff, jitter, retry budgets and idempotency;
- circuit-breaker closed/open/half-open states and failure-domain scope;
- bulkheads, finite queues, rate limiting and load shedding;
- fan-out, hedging, failover, caches and graceful degradation;
- outbox/inbox, durable backlog, saga compensation and reconciliation;
- SLOs, goodput, tracing and fault/load testing.

Before continuing, compute the worst-case deepest attempts when four layers each permit one initial attempt plus two retries, and explain why no individual layer's “only two retries” setting is sufficient evidence.

## Learning Objectives

After this module, learners can:

1. derive layered retry/fan-out amplification bounds and attempt trees;
2. inventory hidden SDK/proxy/mesh retry and timeout behavior;
3. assign one retry owner, global attempt/token budget and absolute deadline;
4. order admission, bulkhead, breaker, attempt timeout, retry and fallback mechanics;
5. scope breaker/bulkhead/limiter/shedding by the resources and failure domains they protect;
6. preserve effect identity and reconcile ambiguity through retries/cancellation;
7. design cheap truthful fallback, failover and durable-backlog behavior;
8. prevent probe, cache, retry and recovery herds with isolation/jitter/ramp;
9. instrument original operations, attempts, outcomes and goodput separately;
10. verify steady state, overload, partial failure, metastability and recovery interactions.

## Core Exposition

### Model the operation and attempt tree

Begin with one semantic operation, not one HTTP/RPC call. It may pass through client library, edge proxy, service, SDK and database driver. Each layer can create attempts, fan out, hedge or fail over. Draw the tree and annotate who owns each branch.

If three nested layers each make at most three total attempts, the deepest worst case is 27. If each deepest attempt fans out to four shards, it is 108 shard calls. Hedging two copies doubles relevant branches. The maximum may not occur often, but capacity and incident response must know it.

For layer total attempts \(a_i\), fan-out \(b_i\) and hedge multiplicity \(h_i\), a coarse bound is

\[
W_{max}=\prod_i a_i b_i h_i.
\]

This overcounts when branches short-circuit and ignores cancellations, but exposes hidden multiplicative structure. Expected work needs conditional failure/latency distributions and correlations; independence assumptions are usually optimistic during common outages.

Count original operations, attempts, downstream calls and terminal outcomes separately. A service can show steady original QPS while dependency calls triple. Attempt telemetry must preserve operation ID, attempt number, retry owner/reason and remaining deadline without unbounded cardinality.

### Treat resilience as feedback control

Let original offered rate be \(\lambda_0\) and mean extra-attempt ratio be \(r\). Dependency offered rate is approximately \(\lambda=\lambda_0(1+r)\) before fan-out. But \(r\) depends on failure/timeout probability, which depends on \(\lambda\):

\[
\lambda=\lambda_0[1+r(p(\lambda))].
\]

When overload raises latency and failure, retries raise load, creating positive feedback. Backoff/jitter changes timing but does not guarantee reduced total work. A retry budget/token bucket introduces negative feedback: recent successful originals replenish a limited pool; retries consume it; widespread failure fails fast rather than spending the recovery capacity.

Breakers suppress likely-failing calls, bulkheads cap residency, shedding reduces admitted load and deadlines stop useless work. Each feedback loop has delay and thresholds. Poorly aligned windows can oscillate: breaker closes as load-shedder recovers, all retries resume, overload returns. Use hysteresis, randomized probes and gradual admission.

### Establish one operation contract

At ingress assign/validate:

- stable operation/effect/idempotency identity;
- authenticated criticality/tenant and cost envelope;
- one absolute deadline based on monotonic elapsed time locally;
- allowed terminal/degraded outcomes;
- retry owner and total attempt/token budget;
- known fan-out/hedging/failover limits;
- effect ambiguity/reconciliation behavior.

Child calls receive a smaller deadline reserving response/commit/reconciliation time. They do not reset to “30 seconds from now” at every hop. An attempt begins only if queue wait + estimated minimum attempt + response reserve fits. Timeouts are selected from dependency latency/cost and false-timeout trade-offs, not copied universally.

Cancellation stops future/cancellable work; it does not undo issued effects. A retried mutation uses the same effect key/fingerprint. If outcome is unknown, query/reconcile before incompatible action. Idempotency makes safe repetition possible; budgets decide whether repetition is wise.

### Assign one retry owner

Retries can exist in browsers, mobile clients, gateways, meshes, service libraries, SDKs, drivers, workers and orchestrators. Inventory configured and default behavior—including transparent transport retries and connection failover. Disable or integrate overlapping layers.

Choose the layer that knows operation semantics, remaining deadline, effect identity and end-to-end budget. Infrastructure can retry only narrowly safe failures (for example, a connection failure proven before application bytes/effect possibility) and must charge the same attempt budget. A lower SDK's unavoidable retry behavior is part of the upper operation's attempt count/capacity model.

Retry only when:

1. failure class is plausibly transient and not overload/permanent policy/schema/auth rejection;
2. repetition is idempotent or effect outcome is known absent;
3. retry token and attempt count remain;
4. backoff + next attempt + reserve fit the absolute deadline;
5. breaker/admission/bulkhead policy permits it;
6. retry does not violate ordering, compensation or caller cancellation policy.

Full/decorrelated jitter spreads synchronized clients. Honor server retry advice only if it fits the operation contract and is trustworthy; `Retry-After` is not authorization to retry a non-idempotent or expired intent.

### Compose admission and attempt mechanics

A useful conceptual order—not a universal middleware stack—is:

1. cheap protocol/size/abuse controls;
2. bounded authentication and semantic classification;
3. deadline/operation/idempotency validation;
4. rate/tenant/criticality policy and current-load shedding;
5. finite queue or immediate bulkhead admission;
6. breaker permission for the correctly scoped dependency;
7. per-attempt timeout and dependency call;
8. release scarce permit promptly;
9. classify outcome/effect ambiguity and update breaker from relevant evidence;
10. if eligible, consume retry budget, wait with jitter without holding permit, and re-enter admission;
11. choose truthful fallback/terminal/reconciliation behavior.

Ordering varies: some systems consult an open breaker before acquiring scarce dependency permits; others use an isolated breaker-probe bulkhead. The invariant is more important: no long backoff while holding capacity, no unbounded queue before protection, no breaker poisoning by calls that never reached the dependency, and retries re-enter current admission rather than bypassing limits.

### Scope every mechanism to its protected thing

A global breaker for a partitioned dependency converts one hot shard into total outage. A breaker per individual host can defeat load balancing and create cardinality/oscillation. Choose a stable failure domain: operation + dependency cluster/shard/region, sometimes tenant where quotas differ. Bulkheads usually align with scarce pools/failure domains but critical flows may need reserved subcapacity.

Rate limiter policy may be per tenant/API/resource and based on cost; load shedding responds to executor, memory, queue, dependency or cell pressure. Circuit breakers infer likely dependency failure, not current caller quota. Keep signals/reasons distinct so one mechanism does not misdiagnose another:

- local rate-limit/shed/bulkhead rejection should not count as dependency failure;
- an open breaker should not consume dependency concurrency;
- attempt timeout after reaching dependency may count according to scope;
- caller cancellation/deadline may not indicate dependency health;
- business rejection (insufficient funds) is healthy service behavior.

### Half-open and recovery are dangerous

When a breaker opens, many callers may wait. If all probe when the interval expires, half-open becomes a load test at the weakest moment. Give probe authority to a bounded coordinator or very small randomized token set, isolate probe capacity, apply attempt deadlines, and do not wrap probes in ordinary retries/hedges. Require enough representative success and downstream resource recovery—not one lucky response.

Closing the breaker is only one recovery signal. Load shedding uses lower recovery threshold/dwell; bulkhead queues drain; retry tokens refill gradually; rate/failover routing ramps; caches/connections warm. Pace durable backlog alongside live work. Jitter scheduled clients and preserve static headroom. A cold recovering region cannot safely receive all failover traffic immediately.

### Breakers, retries and timeouts

Timeout too long lets calls occupy permits until queues collapse; too short creates false failures and duplicate work. A breaker then opens on client-induced timeouts, suppressing a healthy but slower dependency. Calibrate against latency distributions at realistic load, include connection/DNS/TLS setup and distinguish phases where possible.

Retry can help rare independent transient faults. Under overload, it competes with originals and delays recovery. Let breaker state and retry budget suppress attempts quickly, but do not use breaker as a substitute for rate/concurrency admission. Breakers react after observations; bulkheads and shedding provide hard bounds.

Avoid counting multiple attempts from one operation as statistically independent evidence without considering correlation. A burst of retries can trip a breaker faster than original-operation failures. Metrics should report both attempt and operation failure; breaker design states which it uses.

### Bulkheads, queues and backpressure

A semaphore of 50 behind an unbounded queue still allows unbounded memory/latency. Define queue count, bytes, age/deadline and tenant fairness. Prefer immediate rejection for interactive work that cannot wait usefully; durable asynchronous acceptance requires a committed queue/outbox and backlog policy.

Retries should reacquire permits after backoff and may receive lower priority than first attempts, preventing retry traffic from starving fresh work. Reserve small reconciliation/control capacity. Do not reserve so much critical capacity that normal work permanently starves; all classes are finite.

If downstream itself can signal credits/demand, propagate backpressure. Large upstreams should not infer a smaller service's live capacity solely from stale metrics. Rejection/fail-fast disposition must stop upstream retry loops.

### Limiting, shedding and retry semantics

Rate limits enforce a known temporal share/quota even when healthy. Load shedding reacts to current inability to complete useful work. A caller needs a machine-readable stable distinction: quota violation, local task overload, cluster overload, dependency unavailable, permanent rejection, outcome unknown. Status codes alone may be insufficient and platform contracts vary.

A local-task overload might permit one load-balanced attempt if the global budget allows; cluster overload should normally stop retries. Every retry counts as offered/admitted traffic and consumes tenant/global budget. Do not let “retry” headers exempt attempts from rate policy.

Shed before expensive parsing, queue, fan-out and irreversible effects where possible. Work already issued with uncertain effects must be reconciled even if the synchronous caller is shed/timed out. Cheap rejection paths cannot depend on the saturated database/logging system.

### Fallback, cache and failover

A fallback is safe only when:

- it is cheaper and independently available;
- its authority/freshness/quality is explicitly acceptable;
- it does not bypass authentication, revocation or safety policy;
- it has independent capacity and its own timeout/bounds;
- responses label degraded/default/partial truth;
- it is continuously tested under primary failure.

A fallback that calls the same dependency through another route amplifies. Multiple fallback layers can create a search tree. Cache fallback can stampede on expiry or serve revoked/stale authority. Use request coalescing, stale-while-revalidate only where policy permits, bounded refresh and precomputed static defaults with explicit semantics.

Failover transfers load; it does not create capacity. Reserve proven headroom, budget the fraction/ramp, consider shared dependencies and stop if the target degrades. Never let each upstream independently fail over/retry across every region.

### Durable work and messaging

For asynchronous flows, broker lag is often safer than immediate dependency retry, if backlog is bounded and deadlines/expiry semantics are explicit. Consumer concurrency bulkheads, retry topics/delays and dead-letter quarantine prevent one poison message or outage from hot-looping. Idempotent consumers absorb redelivery; outbox preserves publication intent.

Do not repeatedly requeue a permanent failure as “new” work with new identity. Preserve event/effect identity and attempt history. Retry queues themselves need capacity/age/fairness; a large delayed-retry wave can become a recovery herd. Pace release and share capacity with live events.

Saga compensation and reconciliation are high-value work. Give them isolated finite capacity and different retry policy; a failed forward workflow should not create unlimited compensations that overload the same dependency.

### Deterministic amplification budget

The following arithmetic model compares three nested layers with three total attempts each against one retry owner. Each deepest attempt fans out to four downstream calls. It also evaluates how many 250 ms attempts fit a 900 ms deadline with 100 ms then 200 ms backoff and no extra response reserve.

<!-- bijux-verify: {"id":"sepat-090-amplification-budget","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"layered-max-attempts=27\nlayered-downstream-calls=108\nsingle-owner-max-attempts=3\nsingle-owner-downstream-calls=12\ndeadline-feasible-attempts=2\n","stderr":""}} -->
```python
layer_attempts = [3, 3, 3]
layered = 1
for attempts in layer_attempts:
    layered *= attempts

fan_out = 4
single_owner = 3
deadline_ms = 900
attempt_ms = 250
backoffs_ms = [100, 200]
elapsed_ms = 0
feasible = 0

for attempt_number in range(single_owner):
    if elapsed_ms + attempt_ms > deadline_ms:
        break
    elapsed_ms += attempt_ms
    feasible += 1
    if attempt_number < len(backoffs_ms):
        elapsed_ms += backoffs_ms[attempt_number]

print("layered-max-attempts=" + str(layered))
print("layered-downstream-calls=" + str(layered * fan_out))
print("single-owner-max-attempts=" + str(single_owner))
print("single-owner-downstream-calls=" + str(single_owner * fan_out))
print("deadline-feasible-attempts=" + str(feasible))
```

This execution proves exact integer multiplication and fixed deadline arithmetic only. It does not model concurrency, queueing, probabilities, correlations, jitter, cancellation, actual latency, resource limits, breaker dynamics, retries, network calls, effects, goodput or stability.

### Observability and verification

For each critical journey record original offered/admitted/terminal operations, attempts per operation/layer/reason, remaining deadline, queue/bulkhead wait, breaker state/probes, rate/shed reason, retry tokens, fallback/failover path, dependency calls, effect identity/uncertainty and useful on-time outcome. Use trace links to show attempt trees, but durable effect records remain truth. Bound tenant/ID cardinality.

Dashboards show amplification ratio `attempts/original operations`, fan-out calls, retry success *and cost*, protected goodput, late work, queue age, resource pressure, circuit-open duration/probe success, shedding, fallback quality/freshness, failover headroom and backlog/live recovery. A high retry success rate can hide waste if first attempts would have recovered without it.

Verification combines deterministic policy tests with load/fault experiments in isolated owned environments:

- enumerate configured/default retries/timeouts across every layer;
- fail before/after effect issue and verify stable identity/reconciliation;
- sweep latency/error/overload and correlated failures, not only independent faults;
- saturate each bulkhead/resource and verify queue/memory/deadline bounds;
- open/half-open/close breakers with shard-local and global cases;
- exhaust/replenish retry tokens and test jitter distributions;
- overload shed paths, telemetry/control plane and fallbacks;
- fail cache/shared identity/DNS/region dependencies;
- build durable backlog, recover with live traffic and cold capacity;
- test configuration rollout/skew and emergency controls;
- measure end-to-end goodput/correctness throughout.

## Definitions and Notation

Let original operation rate be \(\lambda_0\), dependency attempt rate \(\lambda\), per-layer total attempts \(a_i\), fan-out \(b_i\), hedge copies \(h_i\), deepest work bound \(W_{max}\), retry ratio \(r\), load-dependent failure probability \(p(\lambda)\), absolute deadline \(D\), remaining budget \(R(t)=D-t\), per-attempt bound \(\tau_j\), backoff \(\delta_j\), bulkhead capacity \(K\), retry tokens \(B_r\), and goodput \(G\).

Let operation/effect identity \(o,e\) persist across attempts \(j\). A terminal outcome is success, truthful degradation, definite failure, compensated/reconciled state or owned uncertainty—not merely the last attempt's status.

## Mechanisms, Invariants, or Proof Structure

**Multiplicative bound.** Independent nested attempt loops produce Cartesian combinations; deepest attempts are at most \(\prod_i a_i\), multiplied by fan-out/hedging bounds. One owner collapses retry factors to its one total-attempt bound.

**Deadline feasibility.** An attempt is eligible only if accumulated waits/work plus next attempt and reserve fit \(D\). Resetting relative timeouts removes this finite end-to-end bound.

**Capacity safety.** Finite admission/queue/bulkhead bounds cap resident work in their named scope. They do not guarantee throughput or protect unmodeled shared resources.

**Retry stability condition.** Retry tokens, one owner, backoff/jitter, breaker suppression and shedding limit positive feedback. Stability under a real workload is empirical because \(p(\lambda)\), costs and controller delays are workload-dependent.

**Effect safety.** Stable idempotency identity plus outcome reconciliation prevents retries from intentionally multiplying one semantic effect under their retention/participant assumptions. Timeout/cancellation alone proves nothing about remote commit.

**Breaker validity.** A breaker predicts only its scoped dependency from calls that reached that scope. Misclassified local rejection, business failure or cross-shard aggregation invalidates the signal.

**Recovery safety.** Isolated randomized probes, hysteresis and ramp bound synchronized re-entry. Without headroom/backlog pacing, closing mechanisms can recreate overload.

## Alternatives and Trade-Offs

| Strategy | Prefer when | Limitation or risk |
|---|---|---|
| no automatic retry | overload/permanent/unsafe ambiguity dominates | lower availability for rare transient faults |
| one semantic-layer retry owner | operation semantics/deadline/effect identity are known | infrastructure faults must be surfaced/accounted |
| narrow infrastructure retry | failure proves no app effect and transport recovery is cheap | hidden multiplication and weak semantic knowledge |
| circuit breaker | recent scoped failures predict near-term failure | delayed/oscillatory signal; no hard capacity bound |
| bulkhead | concurrency/resource isolation is required | rejection/queue policy still needed |
| rate limiter | contractual temporal fairness/cost is known | may miss current capacity degradation |
| load shedding | current overload threatens goodput | intentional availability/quality loss |
| truthful fallback | cheaper independent lower-authority result has value | staleness/security/cost/complexity |
| durable defer | work may complete asynchronously | backlog, expiry, idempotency and operations burden |
| regional failover | independent target has proven spare capacity | shared failures and transferred overload |
| capacity/autoscaling | growth can be predicted/reacted to in time | cold start, quotas and dependency impairment remain |

## Failure Modes and Misconceptions

- **Every layer may retry twice safely.** Layered loops multiply, not add.
- **Backoff solves retry storms.** It spreads timing but can preserve excess total work.
- **Timeout is cancellation/rollback.** Late or ambiguous effects remain.
- **Idempotency makes unlimited retry free.** Attempts consume capacity and deadline.
- **Circuit breaker protects capacity.** It predicts failures; bulkheads/admission provide hard bounds.
- **One breaker per service is enough.** Shards/operations/regions can have different failure domains.
- **All errors count toward breaker.** Local rejection and business outcomes can poison it.
- **Half-open means everyone tries again.** Probes need isolated bounded ownership.
- **A semaphore bounds the system.** An unbounded queue/buffer before it does not.
- **Rate limit equals overload shedding.** Policy rate and current resource state differ.
- **503 always means retry.** Scope, identity, budget and deadline decide.
- **Fallback improves availability automatically.** It may double work or lie about authority/freshness.
- **Failover creates capacity.** It transfers correlated load.
- **Closing the breaker ends recovery.** Cold caches, backlog and synchronized clients remain.
- **Pattern metrics prove reliability.** Only end-to-end goodput/correctness/terminal evidence does.

## Worked Examples

### Example 1

Client, gateway, service and SDK each allow three total attempts. One operation can create \(3^4=81\) deepest calls; a five-shard fan-out makes 405. The team assigns the gateway one three-attempt semantic budget, disables service retries and charges unavoidable SDK transport retries to it. The bound becomes 15 shard calls before cancellation effects.

### Example 2

Every attempt gets a fresh 2 s timeout across four hops and three retries, so a nominal 2 s request lasts far longer. One absolute deadline is propagated; each hop reserves return/reconciliation time and refuses attempts that cannot fit. Relative attempt timeouts remain smaller bounds, not renewed user patience.

### Example 3

A worker acquires one of ten database permits, fails, then sleeps one second while holding it. Ten failures block all fresh work. It releases the permit before jittered backoff and must reacquire under current deadline/retry priority. Backoff must not reserve scarce execution capacity.

### Example 4

One customer shard fails and a global breaker opens all reads. The breaker is re-scoped to operation/shard cluster; shared-auth failure can still open a broader dependency breaker based on separate evidence. Scope follows failure domains, not code reuse.

### Example 5

The local rate limiter returns 429, but middleware records it as dependency failure and opens the remote breaker. The pipeline classifies local admission outcomes before dependency attempt; only calls that reach the dependency contribute eligible breaker evidence. Business `insufficient_funds` also counts as healthy response.

### Example 6

A breaker interval expires and 5,000 callers each send a probe wrapped in two retries. Recovery collapses. One coordinator releases a few jittered isolated probes with no ordinary retry; success must include latency/resource evidence, then admission/retry tokens ramp gradually.

### Example 7

The primary recommendation service fails; fallback synchronously calls a cold replica using the same database and doubles fan-out. The product instead omits recommendations with explicit degraded metadata and no dependency call. Authorization/account data never fall back to stale snapshots. Lower functionality yields higher truthful goodput.

### Example 8

Broker consumers retry a database outage immediately while concurrency is saturated. Retry topics release waves every minute. Shared retry tokens, bounded consumer bulkhead, jittered delay, per-event deadline/identity and backlog pacing allow lag to grow within budget, then recover alongside live traffic without a herd.

### Example 9

A region at 80% capacity receives 60% failover traffic and overloads. Routing then fails back, oscillating. The design keeps static failover headroom, caps transferred fraction, checks shared dependencies, uses hysteresis/jittered ramp and sheds low-criticality work rather than claiming unlimited redundancy.

### Example 10

A safety command times out after issue. Client retry, gateway retry and device retry could multiply actuation. One durable orchestrator owns attempts under stable command/device-generation identity; bulkheads reserve reconciliation, device fencing rejects stale duplicates, and uncertainty triggers signed state read-back/manual review. Named safety/controls/security reviewers approve terminal/fail-safe policy; resilience activation is not a safety proof.

## Cross-Program Connections

- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md): critical journeys, dependency/failure domains, fallback authority and blast radius.
- [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md): interaction, chaos, load, recovery and controller-configuration tests.
- [Operating Systems](../../22-operating-systems/ROADMAP.md): queues, schedulers, memory, threads, connections and resource residency.
- [Network Engineering](../../24-network-engineering/ROADMAP.md): transport timeouts, connection setup, routing/failover and correlated network failure.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): abuse amplification, authenticated priority, replay/idempotency and degraded authorization.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): partial failure, ambiguity, feedback, ordering, failover and liveness.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): proxy/SDK defaults, policy rollout, autoscaling, observability and recovery automation.

## References

1. Brooker, Marc. “Timeouts, Retries, and Backoff with Jitter.” Amazon Builders' Library. <https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/>
2. Brooker, Marc. “Exponential Backoff and Jitter.” AWS Architecture Blog, 2015; update 2023. <https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/>
3. Amazon Web Services. “REL05-BP03 Control and Limit Retry Calls.” AWS Well-Architected Framework. <https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_mitigate_interaction_failure_limit_retries.html>
4. Amazon Web Services. “Retry Behavior.” AWS SDKs and Tools Reference Guide. <https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html>
5. Google. “Addressing Cascading Failures.” *Site Reliability Engineering*, Chapter 22. <https://sre.google/sre-book/addressing-cascading-failures/>
6. Google. “Handling Overload.” *Site Reliability Engineering*, Chapter 21. <https://sre.google/sre-book/handling-overload/>
7. Nygard, Michael T. *Release It!*, 2nd ed. Pragmatic Bookshelf, 2018.
8. gRPC Authors. “Retry.” <https://grpc.io/docs/guides/retry/>
9. gRPC Authors. “Deadlines.” <https://grpc.io/docs/guides/deadlines/>
10. Envoy Authors. “Circuit Breaking.” <https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/circuit_breaking>
11. Envoy Authors. “Overload Manager.” <https://www.envoyproxy.io/docs/envoy/latest/configuration/operations/overload_manager/overload_manager>
12. OpenTelemetry Authors. “Semantic Conventions.” <https://opentelemetry.io/docs/specs/semconv/>

Official AWS, Google SRE, gRPC, Envoy and OpenTelemetry sources were checked on 2026-08-29. Exact transparent retries, token algorithms, timeout phases, breaker accounting, overload actions and status semantics are library/product/version/configuration specific and must be verified in the deployed stack.

## Exercises

### Exercise 1

A request crosses five layers, each configured for one initial attempt plus two retries, then fans out to six shards. Compute the worst-case deepest attempts and shard calls. Redesign retry ownership.

### Exercise 2

An operation has a 1,200 ms deadline, 100 ms response reserve, per-attempt bound 300 ms, and backoffs 100 ms then 250 ms. Starting at time zero with negligible other overhead, derive how many attempts can be scheduled without violating the reserve.

### Exercise 3

Diagnose a stack with an unbounded gateway queue, global breaker, SDK/gateway/service retries, permits held during backoff, local 429s counted as dependency failures, fallback to a cold shared database and immediate full recovery. Redesign and specify decisive evidence.

### Exercise 4

Design an interaction policy for live requests plus a six-hour durable-event backlog after database recovery. Include concurrency, retries, breaker probes, rate/shedding, fairness, ordering/idempotency and recovery pacing.

### Exercise 5

Design a resilience composition for high-stakes remote actuation spanning API, durable workflow, provider and device. Include ambiguous effects, authorization, failover, observability, fault evidence and named review.

## Answers to the Exercises

### Answer 1

Each layer has \(a_i=3\), so deepest attempts are \(3^5=243\). Six-way fan-out yields at most \(243\times6=1,458\) shard calls before hedging/fallback/failover. The fact that each layer allows “only two retries” hides multiplication.

Choose the highest layer with operation semantics, stable identity and absolute deadline as retry owner, perhaps three total attempts. Disable retries elsewhere; account narrowly proven transparent SDK/transport retry within that same budget. Then the simple bound is three deepest attempts and 18 shard calls. Further reduce through per-operation fan-out limits, deadline feasibility, retry tokens, breaker/bulkhead admission and no retry of overload/permanent/unsafe outcomes.

### Answer 2

Reserve means work/backoff must finish by 1,100 ms. Attempt 1 ends at 300; backoff 100 gives 400. Attempt 2 ends at 700; backoff 250 gives 950. A third attempt would end at 1,250, beyond 1,100, so it must not start. Two attempts are feasible under the simplified deterministic bounds.

Real code checks remaining monotonic deadline before waiting and again before acquiring/starting; queue/connection/serialization time and uncertainty consume budget too. It releases scarce permits during backoff. If the first attempt's remote effect is ambiguous, safe identity/query semantics—not remaining time alone—decide retry eligibility.

### Answer 3

The unbounded queue defeats concurrency bounds and retains expired work. Global breaker spreads one scope's fault. Three retry owners multiply. Sleeping permits exhaust capacity. Local admission rejection poisons breaker evidence. Shared cold fallback doubles pressure. Full reopening creates a herd.

Bound queue count/bytes/age and prefer deadline-aware early shed. Scope breaker/bulkhead to operation/resource/shard and isolate reconciliation/probes. Assign one retry owner with stable effect key, absolute deadline, classified errors, retry tokens and jitter; disable/integrate SDK defaults. Release permits before backoff and reacquire. Only reached-dependency technical evidence updates its breaker. Replace fallback with cheaper independently authoritative degradation or omit it. Recover with isolated probes, lower thresholds/dwell, token/admission ramp, cache/connection warming and headroom checks.

Evidence inventories actual attempt tree/defaults; injects crashes/ambiguity; saturates queues/resources; tests shard versus shared faults, local rejections, half-open concurrence, fallback dependency failure and cold recovery. Measure originals, attempts, goodput, deadline correctness, memory/queue bounds, effect uniqueness/uncertainty and recovery without oscillation.

### Answer 4

Separate finite live and backlog concurrency shares with weighted work-conserving fairness; reserve small control/reconciliation capacity. Consumers use stable event/effect identity, atomic inbox/effect, per-key order/gap policy and bounded attempt/deadline age. The database breaker admits only isolated jittered probes; ordinary retries are suppressed while open. One consumer retry owner uses shared tokens and releases permits during delay.

On recovery, confirm probe latency/resource health, then ramp total database concurrency below measured sustainable capacity. Pace delayed retries/backlog, prioritize by semantic deadline/criticality without starving old required events, and admit live work within its share. Load shedding or durable-ingress backpressure activates before database/outbox/broker budgets; permanent/expired/poison items quarantine rather than hot retry. Monitor backlog count/bytes/oldest age, live/backlog goodput, attempts, DB saturation, sequence gaps and terminal outcomes. Fault tests rebuild the six-hour backlog and validate recovery with live traffic, cold caches/connections and recurring faults.

### Answer 5

Create one authenticated operation/command identity bound to tenant, device, generation, payload fingerprint, authority and absolute validity deadline. A durable workflow—not client/gateway/SDK layers—owns attempts. Its local state/outbox commits atomically; provider/device calls reuse stable downstream identity. Timeout after issue becomes outcome-unknown and triggers authoritative provider/device query or signed read-back, not a new key. Idempotent consumer/inbox and device fencing prevent duplicate/stale actuation.

Use finite per-device/provider bulkheads, bounded queues, rate/criticality policy and load shedding that preserves acknowledgement/reconciliation capacity. Breakers scope provider/region/device-fleet failures and use isolated no-retry probes. Failover occurs only to an independently safe endpoint with proven headroom/identity continuity; otherwise enter hazard-defined fail-safe/manual review. Cancellation blocks future work but cannot claim rollback.

Telemetry separates original command, attempts, issue/ack/read-back, breaker/admission decisions and durable physical-state evidence with privacy/audit. Tests inject failure at every commit/send/ack boundary, duplicate/reorder/stale generation, authority expiry, partitions, provider/device ambiguity, region failover and recovery herd. Named controls/device, functional-safety, security, reliability/operations, human-factors and regulatory reviewers approve hazard analysis, fail-safe states, compensation/manual action and evidence; pattern composition alone is not safety certification.
