---
module_id: API-073
program: API & Service Engineering
level: 2
module_number: 73
title: Circuit Breaking and Bulkheads
status: complete
last_verified: 2026-09-02
---

# Circuit Breaking and Bulkheads

## One-Page Review

### Governing question

How should a service stop futile calls, isolate scarce resources, admit cautious recovery probes, and preserve useful capacity without turning transient faults into fleet-wide outages?

### Essential definitions

- A **circuit breaker** is a local control that observes classified outcomes and temporarily rejects calls to a dependency when recent evidence says attempts are unlikely to help.
- **closed** admits ordinary calls and records outcomes; **open** rejects ordinary calls; **half-open** admits a small, bounded set of probes to test recovery.
- A **bulkhead** partitions or caps resources so one dependency, tenant, workload, or operation cannot consume every worker, connection, queue slot, or unit of concurrency.
- A **sliding window** is the count- or time-bounded observation set used to calculate failure and slow-call rates.
- A **minimum call count** prevents a breaker from acting on an inadequately small sample.
- A **probe budget** limits half-open recovery traffic.
- **endpoint outlier detection** temporarily removes an unhealthy endpoint from routing; it is not the same as a service-level circuit.
- **load shedding** rejects work because the receiving system lacks current capacity; it is not the same as either a breaker or a bulkhead.

### Central model, mechanism, or theorem

For an observation window containing $n$ eligible calls, of which $f$ are classified failures and $s$ exceed the slow-call threshold,

$$
r_f=\frac{f}{n},\qquad r_s=\frac{s}{n}.
$$

After at least $n_{\min}$ eligible calls, policy may open the circuit when $r_f\ge\theta_f$ or $r_s\ge\theta_s$. A bulkhead separately enforces $I+Q\le C+Q_{\max}$, where $I$ is in-flight work, $C$ the concurrency cap, $Q$ the bounded queue, and $Q_{\max}$ its cap. The circuit answers “is this destination presently worth calling?”; the bulkhead answers “may this caller consume an isolated resource permit?”

### Critical invariants

Breaker identity matches a real failure domain and operation contract. Only eligible dependency outcomes affect its window; validation, authorization, domain rejection, caller cancellation, and deliberate local shedding are not mislabeled as dependency failure. Opening fails fast inside the original deadline and does not fabricate success.

Half-open probes are few, time-bounded, representative, and protected from a fleet-wide herd. Recovery ramps ordinary traffic instead of instantly restoring peak load. Bulkhead admission is bounded by concurrency, queue length, queue age, tenant fairness, and cancellation. Rejected work releases resources promptly. Timeouts, deadlines, idempotency, retry budgets, and semantic fallbacks remain independent obligations.

### Common failures

One global breaker hides endpoint or operation differences; one breaker per request learns nothing; one failure opens a low-volume circuit; business `4xx` outcomes trip dependency health; successful but very slow calls exhaust pools unnoticed; half-open lets every instance probe at once; a single lucky probe restores full traffic; retries bypass the bulkhead; queued requests expire before execution; thread pools wrap nonblocking work and waste threads; one tenant consumes shared permits; per-instance caps multiply after autoscaling; endpoint ejection concentrates load on survivors; fallback cache becomes the next bottleneck; process restart erases protective state; and operators cannot distinguish circuit, capacity, quota, or deadline rejection.

### Compact example

A client sends 500 requests/s to a dependency whose normal mean residence time is 0.2 s, so Little's Law predicts about $L=\lambda W=100$ concurrent requests. A 150-permit bulkhead leaves measured headroom. When latency rises to 1 s, offered work would require about 500 permits; the cap prevents 350 additional calls from occupying every worker. A slow-call breaker then opens after its minimum sample, and ordinary calls fail or degrade while a small half-open budget tests recovery. **Conclusion:** the bulkhead bounds damage immediately; the breaker suppresses calls after evidence accumulates.

### Connections

[Timeout and Deadline Budgets](071-timeout-and-deadline-budgets.md) bound every admitted call, and [Retries and Backoff](072-retries-and-backoff.md) must not bypass circuit or bulkhead policy. [Rate Limits and Quotas](039-rate-limits-and-quotas.md) govern rate and entitlement, while the next modules add API-level load shedding and cross-boundary backpressure.

## Governing Question

For every dependency and workload, what evidence should stop calls, what resource boundary limits the blast radius before that decision, who may probe recovery, and how will the system prove that protection preserves useful work rather than merely moving failure elsewhere?

## Why This Matters

A service can remain logically correct and still collapse through resource coupling. One slow dependency holds sockets, connections, memory, continuations, threads, and caller deadlines. Queues grow, useful requests wait behind doomed ones, upstreams retry, latency rises, and apparently unrelated endpoints fail. Google SRE identifies overload and retry feedback as common causes of cascading failure and recommends early rejection, graceful degradation, and testing beyond the breaking point.

Circuit breakers and bulkheads interrupt different parts of that cascade. A breaker learns from recent calls and rejects attempts that are presently unlikely to succeed. A bulkhead limits how many resources those attempts can occupy even before the breaker has enough evidence. Either control alone is incomplete: a breaker cannot recover resources already trapped in slow calls, while a bulkhead can remain saturated by calls that should not be attempted.

Microsoft's reliability guidance describes circuit breaking as avoiding continuous calls to an unavailable or malfunctioning dependency and bulkheads as isolating resources to contain failures. The metaphor is useful only when translated into exact scopes, classifications, capacities, and recovery rules. A decorative library annotation with default thresholds is not a reliability design.

The controls also create risk. A wrongly shared circuit can deny healthy tenants or operations. Aggressive endpoint ejection can overload remaining replicas. Independent half-open probes from hundreds of callers can recreate the outage. Excessively narrow bulkheads strand capacity, while broad pools remove isolation. Sound design therefore joins semantic classification, capacity evidence, topology, fairness, telemetry, and fault testing.

## Prerequisites and Retrieval

Retrieve [Rate Limits and Quotas](039-rate-limits-and-quotas.md), [Long-Running Operations](018-long-running-operations.md), [Delivery and Acknowledgment](066-delivery-and-acknowledgment.md), [Timeout and Deadline Budgets](071-timeout-and-deadline-budgets.md), and [Retries and Backoff](072-retries-and-backoff.md).

Retrieve the dependency map and failure domains; client, proxy, mesh, load-balancer, and library breaker settings; per-method error semantics; endpoint selection/ejection behavior; latency distributions and capacity curves; connection, thread, event-loop, semaphore, memory, and queue limits; tenant and priority classes; autoscaling bounds; retry ownership; deadline propagation; fallback/cache contracts; regional failover authority; and metrics for attempts, rejections, saturation, state transitions, and recovery.

## Learning Objectives

After completing this module, you can:

1. distinguish circuit breaking, bulkheading, endpoint ejection, rate limiting, load shedding, and backpressure;
2. choose breaker identity and scope from actual failure domains and operation semantics;
3. classify failures and slow calls without turning normal domain outcomes into health signals;
4. configure observation windows, minimum volume, thresholds, open duration, and half-open probes;
5. design conservative, desynchronized recovery and prevent probe herds;
6. size concurrency and queues from throughput, latency, deadlines, and measured capacity;
7. isolate dependencies, tenants, priorities, and resource types without excessive stranded capacity;
8. compose breakers and bulkheads with timeouts, retries, load shedding, fallbacks, and failover;
9. observe protection decisions and distinguish them from dependency outcomes; and
10. verify behavior under abrupt failure, gradual slowdown, partial outage, overload, restart, autoscaling, and recovery.

## Core Exposition

### Separate four control questions

A circuit breaker asks whether recent classified evidence makes another call to a destination worthwhile. A bulkhead asks whether an isolated resource allocation is available. Endpoint outlier detection asks whether one endpoint should remain in the load-balancer set. Load shedding asks whether current receiving capacity can admit more work. Rate limiting asks whether arrivals fit an allowed rate or entitlement, and backpressure communicates downstream capacity so producers slow.

Keep these answers and rejection codes distinct. An open circuit is not proof that the caller exceeded quota. A full bulkhead is not proof that the dependency is unhealthy. A shed request should not necessarily count as a remote failure. An ejected endpoint does not mean every endpoint in the service is unusable.

Controls may cooperate. A full bulkhead can trigger early admission rejection; sustained eligible slow calls can open a circuit; endpoint outlier detection can route probes elsewhere; service-level load shedding can send pushback. They must not share an ambiguous “unavailable” counter that destroys diagnosis.

### Scope breaker identity to failure domains

A useful breaker key usually includes destination service, operation or method class, and sometimes endpoint, region, tenant, credential/provider account, or traffic priority. The dimensions follow independent health and semantics. A read and a non-idempotent write may have different failure classification and fallback. One provider account can be throttled while another is healthy. One availability zone can fail while the region remains usable.

Avoid cardinality without evidence. Per-user breakers can consume unbounded memory and have too little traffic to learn. Per-request breakers have no history. One global breaker aggregates unrelated dependencies and turns a narrow incident into total denial. Use bounded keys, eviction policy, and a hierarchy: endpoint health for routing, operation/destination circuit for calls, and regional authority for failover.

State is generally local to a process or proxy. That avoids making a central breaker store a hard dependency, but 100 clients can reach different conclusions and each admit probes. Treat local state as partial evidence, not global truth. If fleet coordination is required, distribute signed/authorized health policy or conservative budgets without putting every request on a remote coordination lookup.

### Classify eligible outcomes

Create a decision table for each operation. Eligible breaker failures commonly include connection refusal, DNS/routing failure in the relevant scope, dependency timeout, reset after an attempt, explicit transient-unavailable responses, and selected server defects. Slow-call classification requires a threshold below the point where resource exhaustion becomes dangerous.

Do not count caller validation, authentication, authorization, domain rejection, conditional conflict, not-found with normal semantics, or local quota failure as dependency unhealthiness. Caller cancellation should not punish the dependency unless telemetry separately proves the dependency caused the missed deadline. Deliberate load shedding is a capacity signal and may drive a distinct overload circuit, but mixing it with defect rate loses meaning.

Responses can be technically successful yet operationally dangerous. If calls return `200` after 20 seconds while the useful deadline is 500 ms, a failure-only breaker remains closed as pools saturate. Configure slow-call rate or a latency-aware signal, but keep a hard timeout: observation never cancels a stuck call by itself.

Record classification reason and source. Proxies may see transport status but not business meaning; application code may know semantics but miss transparent retries. Assign authority explicitly so the same logical operation is not counted inconsistently at several layers.

### Use windows, volume floors, and hysteresis

A count window evaluates the last $N$ eligible calls; a time window evaluates calls in the last $T$. Count windows give stable sample size but can retain stale history at low traffic. Time windows age evidence naturally but can be noisy when volume varies. Choose based on arrival pattern and recovery needs.

Require a minimum call count $n_{\min}$. With a 50% failure threshold, one failure out of one call is 100%, but it is weak evidence. If $n_{\min}=20$, a window with 12 failures yields $12/20=60\%$ and can open. Low-volume critical operations may need health signals, synthetic probes, or longer windows rather than a threshold of one.

Opening and closing at the same threshold causes oscillation. Hysteresis comes from an open interval, limited half-open probes, separate recovery criterion, gradual traffic ramp, and perhaps a longer success requirement. Thresholds are engineering hypotheses to validate against capacity and user outcomes, not universal constants.

Do not average away bursts or partitions. Segment telemetry by endpoint and region, and retain the underlying counts. A “50% failure” metric without denominator, eligibility rule, window, and scope is not actionable.

### Define the state machine precisely

In **closed**, admit calls subject to deadline and bulkhead policy, record eligible results, and open when configured evidence crosses a threshold. In **open**, reject ordinary calls immediately, preserve a reason and transition time, and wait for an open interval or authorized health signal. An open rejection should consume almost no dependency resource and should be visible as a local protection outcome.

In **half-open**, grant only $P$ concurrent or total probe permits. Successful probes advance recovery evidence; eligible failures reopen the circuit. Calls beyond the probe budget fail/degrade instead of silently joining a queue. Define whether a probe is representative: a cheap health endpoint can succeed while the database-backed operation remains broken.

Operational **forced-open** and **disabled** modes can help incidents and tests, but require authorization, audit, expiry, and clear metrics. “Disabled” should not erase configuration silently. Manual overrides that outlive an incident become latent outages.

State transition should be atomic within its scope. Late results from calls admitted in a prior generation must not incorrectly close a newer open circuit. Tag generations or compare transition timestamps. Decide how configuration changes and process restart seed state; starting every replica closed after restart can unleash traffic.

### Design recovery as a capacity event

Recovery is often more dangerous than steady failure. Caches are cold, connections reconnect, leaders warm, queues drain, and every client observes the same timer. If 100 client instances each permit five half-open probes, the dependency receives 500 near-simultaneous probes. Local limits alone do not bound fleet load.

Use conservative per-instance permits, randomized open intervals, retry/probe tokens, server readiness or pushback, and an aggregate recovery budget. Separate probe traffic from ordinary retries. Prefer representative but inexpensive probes with real dependency work; do not mutate business state merely to test health.

One success does not prove peak capacity. Move from half-open to a ramped closed state or progressive traffic percentage, monitoring latency, error, saturation, and queue drain. Reopen quickly on renewed failure. Preserve alternative/fallback capacity until sustained recovery, then withdraw it gradually to avoid another step load.

Failover and recovery authority must agree. Endpoint outlier detection may reintroduce a host while a service breaker remains open; a region manager may restore a region while clients independently probe. Define precedence and observable reasons.

### Choose bulkhead boundaries

Bulkheads can isolate by dependency, endpoint class, tenant, workload priority, operation cost, region, or resource type. Mechanisms include semaphore permits, bounded worker pools, connection pools, queue partitions, process/cell isolation, memory budgets, CPU quotas, and separate deployment capacity.

Start with shared-fate analysis. Calls to a slow payment provider should not consume every worker needed for account reads. Interactive traffic should retain capacity when batch enrichment spikes. A hostile tenant should not exhaust common connections. Critical control-plane work may need a reserve inaccessible to bulk data processing.

Isolation has a pooling cost. Ten fixed tenant pools can strand nine pools while one is overloaded. A practical design combines a shared pool with per-class maxima or reserved minima, borrowing only under explicit rules. Measure rejected useful work and idle reserved capacity; adjust from evidence.

Bulkhead identity must match every constrained resource. A semaphore of 100 does not help if each call opens ten database connections or buffers 50 MB. Conversely, a connection-pool cap does not bound application continuations waiting on a slow future. Trace resource acquisition across the entire call path.

### Size concurrency and queues

Little's Law relates average in-system work $L$, throughput $\lambda$, and average residence time $W$: $L=\lambda W$ under stable conditions. At 500 requests/s and 0.2 s, expected concurrency is 100. A cap of 150 provides scenario headroom; it is not automatically safe. At 1 s, offered work requires about 500 concurrent slots, so a 150 cap forces rejection or bounded waiting rather than consuming 500.

Derive caps from measured safe concurrency, downstream capacity, deadline, tail latency, resource per call, tenant fairness, and retry load. Average latency is insufficient; tails and burstiness matter. Validate by increasing load beyond the breaking point and observing throughput, latency, errors, memory, connection use, and recovery.

A queue is not free capacity. It converts rejection into waiting and consumes memory plus deadline. Bound length and age. Before enqueue and before execution, compare remaining deadline with estimated useful service time. Expired or cancelled work leaves promptly. Prefer small queues when overload would otherwise create stale work and head-of-line blocking.

Concurrency cap is not a rate limit. Ten permits can serve thousands of short requests per second or almost none when calls hang. Use rate/quotas for arrivals and entitlement, concurrency for occupancy, and deadlines to bound residence.

### Match the execution model

A semaphore-style bulkhead works for asynchronous/nonblocking calls when permits cover logical in-flight work and are released exactly once on success, failure, timeout, and cancellation. A bounded worker pool can isolate blocking calls, but thread count, queue, stack memory, and scheduling overhead must be included.

Wrapping nonblocking I/O in a large thread pool wastes threads; putting blocking calls on an event loop stalls unrelated work. Identify where blocking occurs, including DNS, TLS, serialization, credential refresh, logs, and fallback. Apply isolation at the resource actually at risk.

Permit acquisition must be cancellable and deadline-aware. Never hold a permit while sleeping for retry backoff unless the design intentionally reserves capacity and proves that choice. Normally each attempt reacquires a permit, so retries compete fairly and cannot monopolize capacity.

Release on every terminal path. Leaked permits create a self-sustaining outage. Double release violates the cap. Use structured lifetime management and invariant metrics comparing admitted, completed, cancelled, and current in-flight work.

### Compose deadlines, retries, and admission

One defensible sequence is: validate request and original deadline; apply caller/tenant rate and quota policy; choose destination; check remaining time; request bulkhead admission; check circuit state or atomically combine admission decisions; execute one bounded attempt; classify outcome; release resources; then let the retry owner decide whether another attempt fits retry, deadline, circuit, and bulkhead budgets.

Exact decorator order changes behavior. If a retry wrapper sits inside a bulkhead and holds one permit across sleep and attempts, it may starve new work. If it sits outside, every attempt reacquires admission but can inflate traffic unless retry tokens apply. If a circuit records every retry attempt while policy expects logical operations, one user request can dominate the window. Specify and test the counting unit.

Timeout remains mandatory. Breakers observe prior results; they do not interrupt a current hang unless a time limiter/deadline does so. Bulkheads bound the number of hangs but not their duration. Cancellation must propagate to dependency and release admission.

Retries must never bypass an open circuit or enter a privileged pool merely because they are retries. Half-open probes are a separate authorized category. Initial useful traffic often deserves priority over speculative retries during constrained recovery.

### Coordinate endpoint ejection and topology

Envoy documents circuit-breaking limits such as maximum connections, pending requests, requests, and retries at the upstream-cluster level, while outlier detection ejects endpoints based on observed errors. Product terms can overlap: always translate configuration into the control question and scope rather than trusting the label.

Ejecting a bad endpoint can improve success, but it redistributes load. If one of ten replicas is removed at 90% aggregate utilization, survivors may exceed capacity and be ejected in turn. Limit maximum ejection percentage, incorporate host count and locality, and shed load rather than pretending remaining endpoints have infinite headroom.

An endpoint-level detector needs enough local samples and may disagree across clients. Active health checks can complement passive outcomes but may not exercise the failing operation. A service-level breaker should not open merely because one endpoint is bad if routing can safely avoid it; conversely, endpoint ejection cannot solve a shared database outage.

Cross-region failover changes consistency, data residency, idempotency scope, capacity, and cost. Only an authorized regional mechanism should make that decision. Circuit state is evidence, not automatic permission to violate topology contracts.

### Make fallback semantically honest

Open-circuit and bulkhead rejection need explicit outcomes: fail fast, return stale cached data, omit an optional field, use a local approximation, enqueue durable work, or route to proven spare capacity. The fallback must satisfy the API contract and expose freshness, completeness, provenance, or pending status as needed.

Never return fabricated success for a write. If an effect may have committed, use stable idempotency identity and outcome reconciliation. If durable enqueue accepts responsibility, return the correct asynchronous status and lifecycle, not a synchronous success claim.

Fallback capacity is a dependency. A shared cache can be overwhelmed by every caller when the primary opens. Protect it with its own capacity model, bulkhead, and staleness rules, and prevent recursive fallback loops. Security and authorization still apply to cached or degraded responses.

Measure fallback use and correctness. A breaker that keeps user-visible errors low by serving week-old data can conceal an unacceptable outage unless age and quality objectives are explicit.

### Protect fairness and security

A tenant can deliberately or accidentally consume every permit, cause failures that trip a shared breaker, or trigger expensive probes. Partition or cap per tenant/class, reserve critical capacity, authenticate before expensive admission where safe, and rate-limit high-cardinality breaker keys.

Do not expose internal circuit topology or raw dependency details in public errors. Return stable, documented retryability and optional pushback while logging internal reason under controlled access. Metrics labels must avoid unbounded tenant/request cardinality and sensitive identifiers.

Manual breaker controls and configuration changes are privileged operations. Require audit, expiry, rollout guardrails, and rollback. An attacker who can force-open a payment circuit has a denial-of-service primitive; one who can disable a bulkhead can induce cascade.

### Observe protection and outcomes

For each bounded scope, record circuit state and transition reason/generation; eligible call count; failure and slow-call rates with denominators; open rejections; half-open permits, successes, failures, and suppressed probes; time in state; configuration version; and override status.

For each bulkhead, record limit, in-flight work, queue length/age, admission wait, admission/rejection by tenant/priority/operation, cancellation, timeout, permit leaks, utilization, service time, and borrowed/reserved capacity. Separate local protection rejection from remote response and from deadline/quota/rate/load-shed outcomes.

Trace logical operation and attempt, but control label cardinality. Correlate breaker opening with dependency latency/error, pool saturation, retry amplification, endpoint ejection, fallback load, and user outcomes. Alert on sustained open state, oscillation, all probes failing, never-opening despite saturation, excessive fallback, and idle reserve with high rejection.

Success metrics include preserved throughput and latency for unaffected work, bounded resources, fast recovery without herd, and semantically correct degradation—not simply “breaker opened.”

### Verify faults, overload, and recovery

Test sudden unavailability, gradual latency growth, intermittent failure around thresholds, low traffic, one bad endpoint, one bad region, partial method failure, overload shedding, stuck calls, partial responses, caller cancellation, fallback failure, and dependency recovery with cold caches.

Test configuration rollout, process restart, clock movement where timers use wall time, autoscaling from one to many callers, scale-in, network partition, telemetry loss, manual override expiry, and simultaneous recovery. Confirm aggregate probe/retry traffic rather than only per-instance limits.

Drive load beyond safe capacity. Verify admission rejects early, queues remain bounded, deadlines are not consumed waiting, critical pools retain capacity, and throughput recovers after load falls. Inject tenant-skewed traffic to prove fairness and prevent shared-circuit abuse.

Check invariants automatically where possible: in-flight never exceeds cap; queue never exceeds bound; every permit is released once; open rejects ordinary calls; half-open never exceeds probe budget; ineligible outcomes do not alter failure rate; late generations cannot close a newer circuit; retries reacquire admission and obey the original deadline; and fallback never claims an unconfirmed effect.

## Definitions and Notation

Let $n$ be eligible calls in the observation window, $f$ eligible failures, $s$ eligible slow calls, $n_{\min}$ minimum volume, and $\theta_f,\theta_s$ opening thresholds. Let $P$ be the half-open probe permit limit, $T_o$ the open interval, and $g$ the circuit generation.

Let $C$ be bulkhead concurrency, $I$ current in-flight work, $Q_{\max}$ maximum queued work, $Q$ current queue length, $A_q$ queue age, $\lambda$ throughput, and $W$ mean residence time. Under stable conditions Little's Law gives $L=\lambda W$; it is a measurement relationship, not a promise that a chosen cap is safe.

A **failure domain** is a component or scope expected to fail together. **Blast radius** is the set of workloads/resources harmed by a fault. **Hysteresis** uses different evidence/time for entering and leaving a protective state. A **permit** is admission to a bounded resource. A **fallback** is an alternate result path whose semantics must be part of the API contract.

## Mechanisms, Invariants, or Proof Structure

**Bounded-occupancy argument.** If admission is atomic, every admitted call owns one permit, and every terminal path releases exactly once, then $I\le C$. A dependency can make all $C$ calls hang until timeout, but cannot occupy more than $C$ units in that bulkhead. This argument says nothing about unbounded resources outside the permit or about safe value of $C$.

**Circuit-suppression argument.** While generation $g$ is open, ordinary calls are rejected locally and only authorized probes can execute. Therefore attempted dependency calls during the interval are bounded by the probe policy plus calls admitted before opening. This requires all call paths and retries to consult the same effective policy; hidden clients invalidate the bound.

**Isolation argument.** Suppose tenant A has at most 20 of a 100-permit service pool and cannot borrow protected reserve. Even if A saturates its allowance, at least 80 permits remain outside A's owned maximum. This preserves capacity, not guaranteed success: a shared downstream failure or shared CPU/memory limit can still harm all tenants.

**Recovery counterexample.** A five-probe half-open policy per process appears small. Across 100 synchronized processes it permits 500 calls, and a transition to fully closed can release all ordinary traffic. Hence per-instance probe bounds do not establish fleet-safe recovery; jitter, aggregate budget, server feedback, or progressive ramp is required.

Operational invariants are: classification is semantic and scoped; ordinary open calls never reach the dependency; half-open probes are bounded; occupancy and queue/age are bounded; rejection releases resources; original deadlines and cancellation survive every layer; retries receive no admission exemption; fallback preserves truth; topology authority is explicit; and metrics expose the reason for every protection decision.

## Alternatives and Trade-Offs

A static concurrency limit is simple and predictable but may underuse changing capacity. Adaptive concurrency can track latency/queue signals, yet bad feedback, correlated clients, and insufficient floors/ceilings can oscillate. Start with measured bounds and adopt adaptation only with stable signals and adversarial tests.

Semaphore bulkheads are lightweight for asynchronous work; isolated worker pools contain blocking work but consume threads and add queues. Deployment/cell isolation offers stronger blast-radius control at higher infrastructure and capacity cost.

Local circuit state is available and fast but inconsistent across callers. Shared state can coordinate recovery but adds latency, availability, partition, and trust problems. Conservative local controls plus server-side admission and fleet telemetry often give a safer layered design.

Count windows give fixed sample size; time windows forget stale failures. Passive results represent actual work but disappear when open; active probes provide evidence but may not represent the operation. Use multiple signals without allowing a health endpoint to override real saturation.

Fail-fast minimizes wasted work but reduces chance of a coincidental success. Queuing can absorb short bursts but worsens latency and memory under sustained overload. Fallback improves continuity only when semantics and capacity are real. Excessively fine isolation wastes capacity; broad pooling increases blast radius.

## Failure Modes and Misconceptions

- “The breaker makes calls safe.” It suppresses attempts; it does not create idempotency, atomicity, authorization, or outcome certainty.
- “The bulkhead replaces timeouts.” It caps concurrent harm but hung calls keep permits until cancellation/timeout.
- “Every `5xx` is a failure and every `4xx` is not.” Classification depends on operation, phase, proxy, and overload semantics.
- “One failed call should open.” Without sufficient volume/evidence, low traffic becomes random denial.
- “Only failures matter.” Slow successes can exhaust capacity before errors rise.
- “Half-open means normal traffic resumes.” It is a bounded experiment, followed by progressive recovery.
- “Five probes is small.” Per-instance limits multiply across the fleet.
- “One shared breaker is simpler.” It couples unrelated operations, endpoints, tenants, credentials, or regions.
- “Per-tenant everything is safest.” High cardinality and stranded capacity can make the control itself fail.
- “A queue prevents rejection.” It delays rejection, consumes deadlines/memory, and can create head-of-line blocking.
- “Concurrency equals rate.” Occupancy is rate multiplied by residence time; each control answers a different question.
- “Retries happen after the bulkhead.” Decorator order determines whether permits are held, reacquired, or bypassed.
- “Endpoint ejection removes bad capacity.” It also adds load to survivors and can cascade ejections.
- “A health endpoint proves recovery.” It may omit the database, payload cost, authorization, and actual operation.
- “Fallback is free.” Caches, alternate regions, queues, and approximations have capacity and semantic limits.
- “Restart clears the incident.” Starting closed can flood a dependency; starting open without evidence can prolong denial.
- “An open circuit is an error metric.” It is a local policy decision whose underlying cause and user outcome need separate metrics.

## Worked Examples

### Example 1

A payment-read circuit has a 20-call count window, $n_{\min}=20$, and $θ_f=50\%$. The first call fails, but the breaker stays closed because volume is insufficient. After 20 eligible calls, 12 have failed, so $r_f=12/20=60\%$ and it opens. Validation failures were excluded. The decision has both denominator and semantic evidence.

### Example 2

An inventory operation returns success in 1.8 s against a 500 ms useful deadline. A failure-only circuit stays closed while 300 threads fill. Adding a 400 ms slow-call threshold and hard per-attempt deadline makes the hazard visible and releases calls. Slow-call evidence may open future traffic; the timeout stops current occupancy.

### Example 3

A service handles 500 requests/s with 0.2 s mean residence time, implying about 100 in flight. Engineers validate a 150-permit cap. When latency grows to 1 s, demand becomes about 500 in flight; at most 150 execute while excess work is rejected or briefly queued under a deadline. The bulkhead prevents the slow dependency from owning all service workers.

### Example 4

Tenant A receives at most 20 permits from a 100-permit dependency pool; 80 remain for other tenants and protected work. A sends 1,000 expensive requests and saturates its allocation. A is rejected, but B can still execute. This bounds A's concurrency blast radius, though shared CPU must also be measured.

### Example 5

One hundred API instances simultaneously open for 30 seconds. Each permits five half-open probes. A deterministic timer releases 500 calls at once. Randomized eligibility plus an aggregate 40-probe/s recovery budget and server pushback avoid the herd. Per-instance configuration alone was not a fleet bound.

### Example 6

A client retries three times inside a bulkhead wrapper that retains its permit during two seconds of backoff. Fifty failing requests occupy all 50 permits while doing no work. Moving retry ownership outside makes each attempt reacquire admission and spend a retry token; backoff holds neither worker nor permit. Initial work remains eligible.

### Example 7

One of ten endpoints fails when the cluster is already at 90% utilization. Ejecting it sends its share to nine survivors, pushing each toward 100%; latency rises and more endpoints appear unhealthy. The load balancer caps ejection, the service sheds excess demand, and the regional breaker remains separate. Ejection without capacity reasoning would create a cascade.

### Example 8

A profile API falls back to a cache when its database circuit opens. The cache can serve only half of normal traffic and its entries may be 15 minutes old. The API marks freshness, omits unsupported writes, gives the cache its own bulkhead, and sheds beyond safe capacity. It does not present stale data as current or treat fallback as unlimited.

### Example 9

A process restarts during a dependency outage and initializes its breaker closed. Every restarted replica sends a full observation window, repeatedly probing a known failure. The revised design restores a short-lived signed health directive or starts with a conservative randomized probation state, while avoiding a synchronous central lookup on every request.

### Example 10

A write times out after the provider may have committed. The circuit opens, but the API does not return “payment failed” or enqueue a new-key retry. It retains the same effect ID, queries outcome when permitted, and reports pending/unknown until reconciled. Circuit breaking limits attempts; idempotency and outcome protocol preserve truth.

## Cross-Program Connections

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies partial-failure, coordination, replication, and recovery models. Circuit states are local knowledge, not consensus about dependency truth.

[Operating Systems](../../22-operating-systems/ROADMAP.md) explains threads, scheduling, queues, memory, file descriptors, and resource isolation underlying bulkhead behavior.

[Network Engineering](../../24-network-engineering/ROADMAP.md) contributes connection pools, DNS, routing, load balancing, resets, timeouts, and endpoint health. These signals require scoped interpretation.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns reusable client/proxy policies, safe defaults, deployment cells, configuration rollout, autoscaling interaction, telemetry, and override governance.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) frames blast radius, feedback loops, common-mode failure, graceful degradation, and recovery testing across boundaries.

[Security Engineering](../../25-security-engineering/ROADMAP.md) contributes tenant isolation, privileged control, denial-of-service analysis, sensitive telemetry, and authorization-preserving fallback.

## References

1. Microsoft Azure Architecture Center, [Circuit Breaker pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker).
2. Microsoft Azure Architecture Center, [Bulkhead pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/bulkhead).
3. Google, *Site Reliability Engineering*, [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/).
4. Envoy Proxy, [Circuit breaking](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/circuit_breaking).
5. Envoy Proxy, [Outlier detection API](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/cluster/v3/outlier_detection.proto).
6. Resilience4j, [Introduction](https://resilience4j.readme.io/docs/getting-started).

## Exercises

### Exercise 1

Design a circuit policy for a read operation with bursty traffic and a separate write operation with low volume. Specify breaker keys, eligible outcomes, windows, minimum volume, slow-call handling, and why the policies differ.

### Exercise 2

A service receives 800 requests/s. Mean dependency residence time is 0.15 s normally and 0.9 s during degradation. Calculate implied mean concurrency in each case. Propose a bulkhead and bounded-queue policy, stating what additional evidence is needed before production use.

### Exercise 3

Audit a stack in which the SDK retries twice, the mesh has a cluster circuit and endpoint ejection, and application code has a semaphore plus fallback. Draw the decision order and identify double counting, hidden attempts, permit lifetime, and recovery-herd risks.

### Exercise 4

Design half-open recovery for 200 client instances calling a dependency that can safely accept only 100 recovery requests/s. Include timer desynchronization, aggregate/local limits, representative probes, ramp, failure response, restart, and metrics.

### Exercise 5

Threat-model a multi-tenant bulkhead and breaker system. Cover a noisy tenant, high-cardinality keys, forced-open controls, fallback overload, metric leakage, and a timeout-after-commit write. State invariants and tests.

## Answers to the Exercises

### Answer 1

Key the read circuit by destination, region/endpoint class, and read-operation family if those share semantics; use a time window for bursty traffic, a measured minimum count, transient/timeout/server-defect eligibility, and slow-call rate below resource danger. Exclude validation, authorization, normal not-found, local shedding, and caller cancellation. The low-volume write cannot rely on a short percentage window: use a longer window and authoritative provider health, keep write identity separate, and never use a cheap read probe to authorize effects. Timeout-after-send follows outcome reconciliation. The difference follows volume, semantic risk, and representative evidence.

### Answer 2

Normally $L=800\times0.15=120$ requests. During degradation, offered concurrency is $800\times0.9=720$. A candidate cap might be 160 only if load tests prove the dependency and caller resources remain safe there. Use a small queue whose maximum age leaves enough original deadline for useful execution, with early rejection and tenant/priority reserves. Production evidence still needs tail latency, burst distribution, resource per call, downstream concurrency limit, retry rate, deadline distribution, autoscaling multiplication, throughput at/after saturation, and recovery behavior. Little's Law describes occupancy; it does not choose the safe cap.

### Answer 3

Inventory SDK transparent/configured attempts first. A viable order is semantic validation/deadline, rate/quota, endpoint selection, semaphore admission, circuit decision, one bounded SDK attempt under an explicitly reduced/disabled retry policy, classification, release, and application retry decision if it is the owner. Decide whether mesh circuit counts transport attempts and keep endpoint ejection distinct. Do not hold the semaphore during backoff or fallback. Protect fallback separately. Test that one logical call cannot contribute three ambiguous failures, retries cannot bypass admission, endpoint ejection cannot overload survivors, and hundreds of mesh/client instances cannot synchronize probes.

### Answer 4

Two hundred instances each admitting one probe simultaneously already exceed the 100/s recovery allowance. Randomize open eligibility over a window, use a fleet token signal or conservative cohort schedule bounded below 100/s, and honor server pushback. Probe the real operation with non-mutating or idempotent semantics and a strict deadline. Require a success sample, then ramp ordinary traffic by cohorts while monitoring latency, saturation, error, and queue drain; reopen on renewed eligible failure. Restarts join probation without resetting to full closed. Metrics include eligible instances, tokens, probes/s, suppressed probes, outcomes, state generation, ramp share, and dependency capacity signals.

### Answer 5

Cap tenant concurrency and key creation, reserve protected shared capacity, and evict bounded breaker keys safely. Authenticate and rate-limit expensive paths. Forced-open/disabled controls require privileged authorization, audit, expiry, and rollout limits. Give fallback its own capacity and freshness/security contract. Aggregate metrics without sensitive or unbounded labels. For timeout-after-commit, preserve effect ID and reconcile; never translate circuit rejection into proof of failure. Test skewed tenant floods, key-cardinality attacks, override abuse, cache saturation, cancellation/permit release, hidden retries, restart, and ambiguous writes. Invariants are bounded occupancy and keys, unaffected-tenant reserve, truthful outcomes, controlled operations, and one-time permit release.
