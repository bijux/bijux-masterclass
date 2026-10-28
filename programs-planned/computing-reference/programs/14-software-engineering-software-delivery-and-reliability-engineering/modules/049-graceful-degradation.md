---
module_id: SDRE-049
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 49
title: Graceful Degradation
status: complete
last_verified: 2026-09-06
---

# Graceful Degradation

## One-Page Review

### Governing question

How can a service deliberately preserve its highest-value and safest behavior when capacity or dependencies fail, while making reduced quality explicit, bounded, observable, reversible, and testable?

### Essential definitions

- **graceful degradation** is a designed transition from full service to a declared lower-capability or lower-quality mode that preserves prioritized value and invariants;
- a **core function** is behavior that must remain for the degraded mode to be useful;
- an **optional function** can be removed or reduced without violating the degraded contract;
- a **hard dependency** is required for a function under the current design; a **soft dependency** has a defined fallback or omission path;
- a **degradation mode** is a named state with entry conditions, provided behavior, unavailable behavior, safeguards, telemetry, and exit conditions;
- **feature shedding** disables work whose value is lower than the resources or risk it consumes;
- **quality reduction** returns a cheaper result with explicitly weaker fidelity, freshness, completeness, resolution, or latency;
- **partial result** contains a valid declared subset rather than pretending to be complete;
- **stale fallback** serves previously validated state within a declared age and safety bound;
- **fail closed** refuses an operation when a required safety or authorization condition cannot be established;
- **fail open** permits an operation despite unavailable validation and is acceptable only under an explicit risk decision;
- **hysteresis** uses different entry and exit conditions to reduce rapid mode oscillation;
- **load shedding** rejects selected work to preserve system stability; it is one possible degraded behavior, not a synonym for all graceful degradation;
- **failback** is the controlled return from degraded to fuller service;
- **degradation debt** is the user harm, queued work, stale state, or reconciliation obligation accumulated while degraded.

### Central model, mechanism, or theorem

Let service features be $F$, mode $m$ provide subset $F_m\subseteq F$, and each feature have declared utility weight $w_f\ge0$ for a specific user population and situation. A simple mode utility is

$$
U(m)=\sum_{f\in F_m}w_f,
$$

subject to hard constraints for correctness, safety, security, capacity, and legal obligations. Optimization never permits violating those constraints. A mode is graceful only when it preserves a useful contract, stays within resource limits, labels weakened semantics, and has a verified route into, through, and out of the mode.

### Critical invariants

- rank functions by user consequence before failure, not during crisis;
- specify each degraded mode as an external and internal contract;
- preserve correctness, authorization, durability, and safety unless a formally owned policy defines otherwise;
- mark stale, partial, approximate, delayed, or read-only results honestly;
- bound resource consumption so degradation stabilizes rather than amplifies overload;
- use trustworthy entry signals, hysteresis, dwell time, and independent emergency control;
- keep retry, queue, and fallback traffic from overloading the failing dependency;
- isolate modes by tenant, operation, or failure domain when impacts differ;
- account for deferred work, replay, state reconciliation, and failback capacity;
- test mode entry, sustained behavior, compounding failures, and exit under representative load.

### Common failures

Failures include treating any error response as graceful, hiding incomplete results, serving unbounded stale authorization, returning fabricated success, preserving decorative features while core work fails, triggering from one noisy metric, flapping between modes, synchronizing every instance into a costly fallback, retrying the failed dependency, filling an unbounded deferred queue, dropping high-consequence work by volume alone, weakening tenant isolation, failing to signal clients, forgetting degraded-mode SLOs, and restoring full traffic before dependencies and caches are ready.

### Compact example

A product page normally combines price, stock, recommendations, reviews, and personalization. If recommendation and review dependencies fail, it serves current price and stock, omits the unavailable panels, labels the page as reduced, and suppresses calls to those dependencies. If stock authority fails, checkout fails closed instead of accepting an order it cannot validate. The mode preserves browsing and safe purchase decisions without pretending every feature or invariant is substitutable.

### Connections

[SDRE-047](047-failure-domains.md) identifies the dependencies and scopes that can fail together. [SDRE-048](048-redundancy-and-diversity.md) attempts to preserve full service; degradation defines the bounded behavior when redundancy is insufficient or deliberately uneconomic. [SDRE-050](../ROADMAP.md) next incorporates these contracts and tests into a production-readiness review.

## Governing Question

Systems rarely move cleanly from perfect to unavailable. A dependency slows, one data source lags, capacity falls, a region loses state, or a control plane stops accepting changes. Without a designed intermediate mode, the service may keep attempting full work until queues, retries, and resource exhaustion turn a local fault into total failure.

Graceful degradation chooses useful loss. It may omit recommendations, lower media resolution, return a valid partial search, accept reads but refuse writes, use bounded cached data, or defer nonurgent work. The choice is not purely technical. Product owners identify user value; security and safety owners define inviolable constraints; engineers prove resource and state behavior; operators need clear controls and evidence. The governing question asks how to make the weaker service honest and dependable rather than an improvised collection of fallbacks.

## Why This Matters

Google's SRE discussion of cascading failures distinguishes load shedding, which drops work to preserve stability, from graceful degradation, which reduces work per accepted request by returning a cheaper result [1]. It recommends realistic overload testing because rarely exercised degraded paths can fail, and warns that complex controls can create feedback cycles or synchronized failure [1].

Current AWS reliability guidance describes graceful degradation as transforming applicable hard dependencies into soft dependencies so core function can continue with stale, alternate, or absent secondary data [2]. It warns against inconsistent partial transactions and destructive refresh behavior. This is source-specific guidance, not a claim that every dependency can safely become soft.

Current Microsoft architecture guidance similarly treats graceful degradation as a distinct workflow entered in response to failed components, with detection, routing, and user notification [3]. Its throttling guidance describes feature reduction as trading response completeness for availability so essential features retain resources [4]. Current details were checked on 2026-09-06; the durable lesson is to define which value and semantics survive.

Graceful degradation is not permission to compromise correctness silently. A stale product description may be acceptable; stale revocation state may be dangerous. A partial search result can be useful when labeled; a partially committed financial transfer is corruption. Every fallback needs a property-specific contract and a consequence analysis.

## Prerequisites and Retrieval

Retrieve service contract, SLI, SLO, dependency, failure domain, redundancy, capacity, overload, saturation, latency, queue, timeout, retry, correctness, freshness, completeness, authorization, durability, priority, idempotency, reconciliation, and user communication.

From SDRE-038 retrieve actionable signals. From SDRE-042 retrieve honest measurement populations and good-event predicates. From SDRE-045 retrieve policy and budgets. From SDRE-047 retrieve domain and propagation analysis. From SDRE-048 retrieve survivor capacity, state, and failover. Detailed retry, backpressure, shedding, queue stability, and cascading-failure mechanics appear in SDRE-061 through SDRE-070.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish graceful degradation from failure, load shedding, failover, and fabricated success;
2. classify core, optional, deferrable, and prohibited behavior by user consequence;
3. convert a hard dependency into a justified soft dependency contract;
4. specify stale, partial, approximate, read-only, and deferred modes precisely;
5. preserve correctness, authorization, durability, safety, and tenant isolation;
6. design stable mode entry and exit using hysteresis and evidence;
7. reason about fallback resource cost and dependency amplification;
8. expose degraded semantics to clients, users, telemetry, and operators;
9. plan reconciliation, debt draining, and controlled failback;
10. test degradation under representative and compound failures.

## Core Exposition

**Define value and nonnegotiable constraints.** Start with user journeys and consequences. Separate functions into core, optional, deferrable, and prohibited-under-uncertainty. The classification can differ by operation and population. Browsing cached inventory may be useful; placing an order against unknown stock may create unacceptable oversell. An emergency communication service may prioritize message delivery over presence indicators.

Write hard constraints first: never disclose another tenant's data; never acknowledge a durable write before the required persistence rule; never authorize from data older than the revocation bound; never present an approximation as exact. A weighted utility model can rank remaining features only within those constraints. High convenience cannot compensate for violated safety.

Include product, support, security, compliance, data, accessibility, and operations owners. A feature engineers call optional may be essential to a user with assistive technology or to a regulated workflow. Record authority and disagreement before incidents.

**Name modes as contracts.** Avoid one boolean `degraded`. A service may need `recommendations-omitted`, `catalog-stale-read`, `checkout-read-only`, or `regional-capacity-limited`. Each mode declares trigger, scope, offered functions, weakened qualities, hard invariants, response metadata, user message, resource budget, retry behavior, telemetry, owner, maximum duration, escalation, and exit.

Specify client semantics. Does the response remain cacheable? Is data stale as of a timestamp? Are results partial, and which sources are missing? Is a write accepted, durably queued, or rejected? Which status or application code distinguishes the outcome? A successful transport status must not conceal a failed business operation.

Version degraded contracts like normal APIs. Clients may not understand a new partial-result shape during the first incident. Compatibility and fallback behavior need contract tests and staged rollout.

**Transform only appropriate dependencies.** A hard dependency causes the function to fail when it is unavailable. A soft dependency has an alternate behavior. Softening is a design decision, not catching every exception. Identify what the dependency supplies, maximum safe absence, substitute source, consistency and age requirements, and recovery obligations.

If recommendations fail, omission is usually semantically safe. If price authority fails, a cached value may be unsafe after its validity interval. If identity is unavailable, existing short-lived sessions might remain valid under policy, while new login and privilege elevation fail closed. If the ledger is unavailable, accepting a transfer as complete is false; a durable, explicitly pending command may be possible only with idempotency and later reconciliation.

Fallbacks must not depend transitively on the same failed domain. A secondary catalog backed by the same database is not a fallback for that database failure. A cache that synchronously refreshes on every miss can turn dependency failure into a stampede. Trace every mode through failure-domain and capacity maps.

**Choose a degradation form.** Feature shedding omits optional work. Quality reduction selects cheaper computation, lower resolution, smaller search scope, or less frequent refresh. Partial results return available valid components. Stale fallback serves a previous value within declared bounds. Read-only mode preserves observation while preventing unsafe mutation. Deferred mode acknowledges only durable acceptance for later processing. Static fallback supplies a predetermined response suitable for limited content.

Approximation must preserve its declared error or use boundary. A lower-resolution image remains an image; an approximate financial balance might be unacceptable. A partial aggregate needs provenance and missing-part metadata. Never use placeholder data that looks authoritative.

**Budget the degraded path.** A fallback intended to save the service can cost more. Cache misses may trigger expensive regeneration. Error logging can consume more CPU than successful requests. Recomputing a cheap approximation may fan out to several dependencies. Measure CPU, memory, I/O, locks, queue growth, network, and downstream work in every mode.

Compute useful throughput, not merely request acceptance. If full requests cost 10 work units and degraded requests cost 4, capacity can theoretically serve 2.5 times as many under the same bottleneck, subject to fixed costs and other resources. Load tests must verify the real nonlinear boundary.

Set a retry policy per mode. Suppress calls to a known failed optional dependency rather than timing out repeatedly. Bound probes and use a circuit state. Tell clients when retry is useful, unsafe, or pointless. Detailed backoff and load-shedding design comes later, but degradation must not assume infinite retry capacity.

**Enter modes from robust evidence.** Signals can include dependency success, latency, saturation, queue age, error-budget burn, state freshness, capacity, and operator declaration. One metric can be delayed or noisy. Use a condition tied to the failure mechanism and user impact, with minimum evidence or corroboration proportional to consequence.

Hysteresis separates entry and exit thresholds. Entering at 90% saturation and exiting only below 70% prevents oscillation near 90%. A minimum dwell time can allow queues and caches to stabilize. Hysteresis delays restoration, so tune from observed dynamics rather than folklore.

The controlled example demonstrates a simple global state transition. A real controller needs scoped instances, timestamps, missing-signal behavior, concurrency, manual authority, and persistence.

<!-- bijux-verify: {"id":"control-degradation-mode","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"sample=1 saturation=0.70 mode=full\nsample=2 saturation=0.92 mode=degraded\nsample=3 saturation=0.88 mode=degraded\nsample=4 saturation=0.76 mode=degraded\nsample=5 saturation=0.68 mode=degraded\nsample=6 saturation=0.69 mode=full\n","stderr":""}} -->
```python
samples = [0.70, 0.92, 0.88, 0.76, 0.68, 0.69]
mode = "full"
healthy_samples = 0

for number, saturation in enumerate(samples, start=1):
    if mode == "full" and saturation >= 0.90:
        mode = "degraded"
        healthy_samples = 0
    elif mode == "degraded":
        healthy_samples = healthy_samples + 1 if saturation <= 0.70 else 0
        if healthy_samples >= 2:
            mode = "full"
            healthy_samples = 0
    print(f"sample={number} saturation={saturation:.2f} mode={mode}")
```

Avoid controller herding. If every instance changes mode at the same threshold from the same delayed metric, synchronized fallback can shift load abruptly. Scope decisions to the failure domain where possible, apply bounded jitter or coordinated control where safe, and observe aggregate resource effects.

Provide an emergency lever independent enough to work during the target failure. It needs authentication, authorization, audit, discoverability, bounded scope, and expiry. Manual override should not silently fight an automatic reconciler; define precedence and handback.

**Protect truth and trust.** Mark freshness with source time and maximum acceptable age. Do not reset age when copying stale data between caches. Preserve provenance so users and downstream systems can decide. If no safe value exists, omission or explicit unavailability is more graceful than a lie.

Partial results need completeness metadata. If three of five shards answer, a search can state which scope was covered or use a contract saying results may be partial. Do not compute an aggregate denominator from available shards and label it global. Downstream composition must carry quality metadata rather than discard it.

Authorization and safety deserve explicit fail posture. Fail closed for operations where unverified permission or state could cause unacceptable harm. Carefully bounded fail open may be justified for low-consequence continuity, but it needs named authority, threat analysis, duration, telemetry, and retrospective review. “Availability” alone does not decide.

Preserve tenant isolation and fairness. A large tenant's optional analytics should not consume capacity needed for another tenant's core path. Reserve or partition resources, apply priority within contractual and ethical constraints, and monitor each affected cohort. Do not consistently sacrifice a quiet population because global utility weighting favors volume.

**Coordinate across layers.** A frontend may omit a panel, but if it still calls the failed backend, no load is saved. A backend may shed optional computation while the client retries because it interprets the response as failure. Specify end-to-end mode signals and behavior across clients, gateways, services, queues, and data stores.

Prevent contradictory modes. One layer may serve stale data while another rejects it as expired, creating retry loops. Maintain a mode compatibility matrix and bound who owns the decision. Prefer local autonomy for local failures with global coordination only where shared resources require it.

In distributed systems, mode state itself can partition. Design a safe default for missing control state. A central feature flag offers fast coordination but is a shared dependency; cached last-known-good policy and local hard safety limits can preserve control. Avoid unbounded global synchronization during an incident.

**Account for degradation debt.** Deferred commands, reduced indexing, stale caches, skipped enrichment, suppressed notifications, and partial replicas create work to reconcile. Record durable identities and ordering. Bound queue size and age. If capacity to drain later is absent, deferral converts an immediate failure into a delayed one.

Estimate catch-up load. A queue accumulating at 100 jobs/second for one hour contains 360,000 jobs. If recovered processing has only 20 jobs/second spare capacity, drain takes five hours even with no additional failure. Retention, deadlines, deduplication, and user cancellation may change which work remains valuable.

Failback is a change. Confirm dependency stability, survivor headroom, state freshness, and compatibility. Restore features progressively, warm caches without stampeding dependencies, drain deferred work under a budget, and monitor user outcomes. If full mode reactivates faster than resources recover, the system can flap into another incident.

**Make degradation observable and honest.** Record mode, reason, scope, start time, trigger evidence, controlling policy version, affected functions, response-quality fields, resource behavior, and owner. Dashboards should show user success under the degraded contract and separately show loss from the full contract. A green core SLI must not hide prolonged feature loss.

Define mode-specific objectives and duration limits. A service might target 99.9% correct core reads and separately bound recommendation omission. Product and support need cohort evidence. Error budgets cannot make silent degradation free; the SLI must classify the behavior according to user expectations.

Tell users what changed in language they can act on. “Some results are unavailable; displayed inventory is current as of 14:05 UTC; checkout is paused” is better than a generic success or mystery spinner. Avoid exposing internal details that create security risk, but do not conceal material limits.

**Test the uncommon path.** Unit-test selection and invariants. Contract-test clients against partial, stale, read-only, pending, and explicit-unavailable responses. Fault-test dependencies, stale control state, and signal loss. Load-test full-to-degraded transitions, sustained degraded capacity, retry behavior, debt accumulation, recovery, and failback.

Exercise one bounded production cohort where safe so configuration, routing, and telemetry are real. Test compound failures: degraded cache plus identity loss, one failed zone plus overload, or control-plane loss during manual override. Stop conditions and user safeguards are part of the test.

Review incidents for mode entry that was too late, too early, ineffective, or harmful. Remove unused complexity and update rankings when user needs change. Gracefulness is demonstrated by bounded user outcomes and stable recovery, not by the existence of fallback code.

## Definitions and Notation

Let $F$ be service functions and $M$ named modes. Mode $m$ provides $F_m\subseteq F$. For context-specific nonnegative weights $w_f$, nominal utility is $U(m)=\sum_{f\in F_m}w_f$. Let hard predicates be $H_j(m)$ for correctness, security, safety, durability, capacity, or regulation. A feasible mode requires $H_j(m)=1$ for every applicable $j$; utility never offsets a false hard predicate.

Let resource vector $R(m)=(r_1(m),\ldots,r_q(m))$ and usable limits $C=(c_1,\ldots,c_q)$. A necessary stability condition is $r_i(m)\le c_i$ for every resource $i$. Measured nonlinear interactions and downstream limits determine whether it is sufficient.

For entry signal $x_t$, upper threshold $u$, lower threshold $l<u$, and required healthy count $h$, a simple hysteretic controller enters degraded mode when $x_t\ge u$ and exits only after $h$ qualifying observations with $x_t\le l$. Sampling interval, missing data, scope, and dwell time are part of the controller.

For cached value generated at time $t_g$ and evaluated at $t$, age is $a=t-t_g$. It is eligible only when $0\le a\le A_{max}$ and all property-specific validity predicates hold. Copy time is not generation time.

For deferred backlog $B_0$, new arrival rate $\lambda$, and recovery service rate $\mu>\lambda$, idealized drain time is $T=B_0/(\mu-\lambda)$. If $\mu\le\lambda$, backlog does not drain under the constant-rate model.

## Mechanisms, Invariants, or Proof Structure

**Constraint-before-utility argument.** If a mode violates a hard safety predicate, increasing optional-feature utility cannot make the violation acceptable. Therefore filter infeasible modes before ranking feasible utility.

**Soft-dependency condition.** A dependency becomes soft for function $f$ only if an alternate path supplies a declared acceptable result for $f$ without transitively requiring the same failed domain. Catching an exception without a valid result merely changes failure presentation.

**Resource-stability argument.** If any required resource demand exceeds usable capacity, queues or rejection must grow until arrival, work, or capacity changes. A degradation that does not reduce the limiting resource cannot stabilize that overload.

**Hysteresis argument.** With entry $u$ and exit $l<u$, measurements in $(l,u)$ preserve current mode, so small oscillations around one threshold do not force transitions. Hysteresis reduces but does not eliminate flapping from large oscillations or correlated signals.

**Freshness invariant.** Copying a cached value cannot decrease its semantic age because the underlying observation time remains $t_g$. Resetting the timestamp manufactures false freshness.

**Debt-stability derivation.** During recovery, backlog changes at rate $\lambda-\mu$. Only $\mu>\lambda$ gives negative drift, yielding ideal drain $B_0/(\mu-\lambda)$. Retries, failures, priorities, and variable rates require a richer model.

**Truthfulness invariant.** If a response omits, approximates, delays, or stales a property material to client decisions, the contract and evidence must represent that weaker property. Otherwise transport availability improves by misclassifying user failure.

## Alternatives and Trade-Offs

**Omission versus stale fallback.** Omission avoids outdated truth but may remove useful context. Stale data preserves continuity when age is acceptable. Choose by consequence, provenance, and bounded validity.

**Partial versus all-or-nothing results.** Partial results preserve some value and complicate client reasoning. Atomic failure simplifies semantics and discards usable work. Never make a non-decomposable transaction partial.

**Read-only versus deferred writes.** Read-only mode preserves consistency with explicit rejection. Durable deferral can preserve intent but creates ordering, duplication, cancellation, capacity, and reconciliation obligations.

**Automatic versus manual entry.** Automation reacts quickly to well-modeled evidence. Humans interpret novel, high-consequence ambiguity. Provide safe automation, bounded authority, and an independent governed override.

**Global versus scoped degradation.** Global mode is simple and can overreact to local failure. Per-cell, tenant, operation, or feature modes limit harm but add coordination and test combinations. Align scope with failure domains and resource sharing.

**Quality reduction versus load shedding.** Cheaper accepted work preserves breadth with weaker results. Shedding preserves quality for fewer requests. User consequences and limiting resources determine the mix.

**Rapid exit versus cautious failback.** Rapid restoration reduces feature loss but risks stampedes and flapping. Staged failback costs time while validating dependency, state, capacity, and debt drain.

## Failure Modes and Misconceptions

- **“Any partial service is graceful.”** It must preserve useful declared behavior and hard invariants.
- **“Return success and hide the missing feature.”** Misclassification destroys client decisions and SLI honesty.
- **“Every dependency should be soft.”** Some authority, safety, correctness, and durability dependencies must fail closed.
- **“Cached means safe.”** Age, provenance, revocation, corruption, and domain sharing determine eligibility.
- **“Fallback is cheaper.”** Cache regeneration, logging, retries, and fan-out can cost more than normal work.
- **“One saturation threshold is enough.”** Noise and delay can cause oscillation; entry, exit, dwell, and scope need design.
- **“Feature flags guarantee control.”** The flag service and synchronized activation are themselves failure domains.
- **“Deferred means completed later.”** Durable identity, capacity, ordering, expiry, and reconciliation are required.
- **“Global utility is fair.”** Volume-weighted choices can repeatedly sacrifice a small or vulnerable cohort.
- **“Redundancy removes the need for degradation.”** Correlated failure, capacity loss, and economics leave residual scenarios.
- **“Degraded mode needs no SLO.”** Prolonged feature loss and weak quality must remain visible.
- **“Recovery means turn everything on.”** Failback can overload dependencies and create a second incident.
- **“Fallback code passed unit tests.”** Cross-layer contracts, load, real configuration, and compound failures remain unproven.
- **“Availability justifies weaker security.”** Fail-open behavior requires a separate explicit risk authority and bounds.

## Worked Examples

### Example 1

**Situation.** Product pages require price and stock but also call a recommendation engine that is timing out.

**Reasoning.** Recommendations are optional for the purchase journey. The frontend omits the panel, stops recommendation calls through a bounded circuit state, and marks omission telemetry. Price and stock remain authoritative.

**Conclusion.** The recommendation dependency becomes soft for browsing without weakening purchase correctness.

### Example 2

**Situation.** Catalog authority is unavailable. A cached description is 20 minutes old; policy permits 60 minutes, but cached price is valid for only five.

**Reasoning.** Description can be served with its generation time. Price is ineligible despite sharing the cache entry. Copying the entry now cannot reset either age.

**Conclusion.** Serve labeled description, omit or reject price-dependent actions, and preserve field-specific freshness.

### Example 3

**Situation.** A ledger cannot confirm writes, and a transfer API considers returning success after placing the request in process memory.

**Reasoning.** Memory is not the promised durable acceptance point. A crash could lose the transfer while the user believes it completed. Either reject explicitly or durably enqueue an idempotent pending command with status and later reconciliation.

**Conclusion.** Do not trade financial correctness for apparent transport availability.

### Example 4

**Situation.** Search queries 20 shards; 18 return before deadline and two are unavailable.

**Reasoning.** A partial result can be useful if ranking remains valid over the available set and the response states coverage or partial status. Calling it complete makes counts and absence claims false.

**Conclusion.** Return a contractually partial result with missing-scope metadata, or fail if the client requires completeness.

### Example 5

**Situation.** Video encoding costs exceed capacity during a spike.

**Reasoning.** Lower resolution reduces compute and bandwidth while preserving viewing. Protect accessibility tracks and core playback, shed expensive optional transformations, and avoid clients retrying for unavailable quality.

**Conclusion.** Quality reduction is graceful when users can identify and use the weaker result and the limiting resources actually fall.

### Example 6

**Situation.** Saturation alternates between 89% and 91% with a single 90% mode threshold.

**Reasoning.** Every sample changes mode, repeatedly warming caches and shifting load. Entering at 90%, exiting below 70% after two samples, and applying a minimum dwell prevents these small crossings from toggling state.

**Conclusion.** Hysteresis and dwell stabilize mode selection, but still require tests for large oscillations.

### Example 7

**Situation.** Identity is unreachable. A read request has a signed session issued ten minutes ago; a privilege-elevation request has no current authorization evidence.

**Reasoning.** Policy may permit the bounded session for low-risk reads until its original expiry. Privilege elevation changes authority and fails closed. Copying session state cannot extend expiry.

**Conclusion.** Degrade by operation and consequence; availability does not justify unverified privilege.

### Example 8

**Situation.** A queue accumulates 360,000 deferred jobs. New jobs arrive at 100 per second after recovery, and processing capacity is 120 per second.

**Reasoning.** Spare drain rate is 20 per second. Ideal drain time is $360{,}000/20=18{,}000$ seconds, or five hours. Retries and failures would extend it.

**Conclusion.** Deferred mode needs five hours of modeled catch-up capacity plus expiry, priority, and deduplication policy.

### Example 9

**Situation.** A global controller drops all low-volume tenant work first because this maximizes completed request count.

**Reasoning.** Aggregate utility hides concentrated exclusion and may violate tenant commitments. Reserve core capacity per cohort or apply a declared fair policy before optimizing optional work.

**Conclusion.** Graceful degradation must protect bounded cohort outcomes, not only global throughput.

### Example 10

**Situation.** A dependency recovers, and all 500 service instances immediately restore enrichment and refresh empty caches.

**Reasoning.** Synchronized failback creates a request surge that can fail the dependency again. Confirm stability, stagger restoration, rate-limit refresh, retain degraded behavior during warmup, and monitor debt and saturation.

**Conclusion.** Failback is a progressive production change, not a boolean reversal.

## Cross-Program Connections

- **Software architecture:** soft dependencies, functional decomposition, and bounded contexts determine what can be omitted independently.
- **API engineering:** partial, stale, pending, and unavailable outcomes need versioned machine-readable contracts.
- **Data engineering:** provenance, freshness, completeness, replay, and backlog lineage keep degraded data honest.
- **Database engineering:** read-only modes, durable queues, idempotency, consistency, and reconciliation protect mutation semantics.
- **Security:** fail posture, session age, revocation, least privilege, override authority, and audit constrain continuity.
- **Distributed systems:** partitions, timeouts, retries, stale state, coordination, and feedback make modes partially observed.
- **Platform engineering:** cell-scoped controls, feature flags, capacity reservations, and emergency levers operationalize modes.
- **Human factors:** clear user communication and operator controls prevent ambiguity and unsafe improvisation.
- **Systems engineering:** utility under hard constraints, hazard analysis, degraded mission modes, and recovery evidence connect technology to consequence.

## References

1. Mike Ulrich and K. V. Vishwanath, “Addressing Cascading Failures,” in *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly Media, 2016. [Official online edition](https://sre.google/sre-book/addressing-cascading-failures/). Accessed 2026-09-06.
2. Amazon Web Services, “REL05-BP01 Implement graceful degradation to transform applicable hard dependencies into soft dependencies,” *AWS Well-Architected Framework: Reliability Pillar*, current online edition. [Official documentation](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_mitigate_interaction_failure_graceful_degradation.html). Accessed 2026-09-06.
3. Microsoft, “Architecture strategies for self-healing and self-preservation,” Azure Well-Architected Framework. [Official documentation](https://learn.microsoft.com/en-us/azure/well-architected/reliability/self-preservation). Accessed 2026-09-06.
4. Microsoft, “Throttling pattern,” Azure Architecture Center. [Official documentation](https://learn.microsoft.com/en-us/azure/architecture/patterns/throttling). Accessed 2026-09-06.
5. Google, “A Collection of Best Practices for Production Services,” in *Site Reliability Engineering: How Google Runs Production Systems*. [Official online edition](https://sre.google/sre-book/service-best-practices/). Accessed 2026-09-06.
6. Google, “Reliable Product Launches at Scale,” in *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly Media, 2016. [Official online edition](https://sre.google/sre-book/reliable-product-launches/). Accessed 2026-09-06.

Current vendor claims are source-specific and were checked on 2026-09-06. Quantitative examples are explicit educational models, not universal thresholds or production guarantees.

## Exercises

### Exercise 1

For an online store, classify product descriptions, current price, recommendation panels, stock validation, checkout authorization, and confirmation email as core, optional, deferrable, or prohibited when their dependency is unavailable. State assumptions rather than asserting one universal classification.

### Exercise 2

Full requests cost 12 CPU units and degraded requests cost 5. A fixed overhead consumes 2,000 of 20,000 CPU units per second. Calculate ideal full and degraded request capacities. Explain why the ratio is not a production guarantee.

### Exercise 3

Design a stale-fallback contract for a permissions-dependent read API. Include source timestamp, maximum age, revocation risk, operation classes, response metadata, fail posture, telemetry, and recovery.

### Exercise 4

A service enters degraded mode at 85% queue utilization and exits at 80% after one sample. Production oscillates between 79% and 86%. Diagnose the control problem and propose entry, exit, dwell, and scope improvements with a validation plan.

### Exercise 5

A dependency outage lasts 45 minutes. Deferred work arrives at 80 jobs/second. After recovery, total processing capacity is 140 jobs/second while live arrivals remain 80. Compute ideal backlog and drain time, then design a failback that accounts for expiry, priority, retries, and another dependency slowdown.

## Answers to the Exercises

### Answer 1

A defensible example assumes browsing is valuable but purchase correctness is nonnegotiable. Descriptions may use bounded stale data; recommendations are optional and omitted. Current price and stock validation are core for committing checkout and become prohibited when no safe authority or validity interval exists. Checkout authorization is core and fails closed if identity or payment authority cannot be verified. Confirmation email is deferrable only after the order itself is durably committed and the notification command is durably recorded. Different legal, inventory, or product contracts can change the choices; every classification needs owners, age bounds, and user-visible semantics.

### Answer 2

Usable variable CPU is $20{,}000-2{,}000=18{,}000$ units per second. Ideal full capacity is $18{,}000/12=1{,}500$ requests/second. Ideal degraded capacity is $18{,}000/5=3{,}600$ requests/second, 2.4 times full capacity. The ratio assumes CPU is the only limit, costs are constant and additive, fixed overhead does not change, request mix is identical, and no cache, queue, memory, network, lock, dependency, or transition effects intervene. Load tests and user SLIs must establish actual stable capacity.

### Answer 3

Record the original authority observation time and policy version; never reset time on cache copy. Define maximum age by operation and data sensitivity. Permit only low-risk reads whose permission was valid at generation and whose revocation exposure is accepted by the named security owner; deny new access, privilege elevation, sensitive export, and any request beyond age. Return a machine-readable `degraded`, `authorization_as_of`, and expiry field plus appropriate user message. Count use, cohort, age, denials, identity health, and override state. On recovery, revalidate before restoring full scope, invalidate revoked entries, reconcile audit logs, and review any access during the interval. If policy forbids stale authorization, fail closed for all operations.

### Answer 4

Entry and exit thresholds are close, and one sample gives no persistence, so noise crosses both boundaries. Measure queue dynamics and user latency, then consider entering at 90%, exiting below 65–70% after several consecutive observations, and enforcing a minimum dwell sufficient for queue drain. Scope degradation to the saturated cell or operation unless the queue is truly global. Validate through replay and controlled load ramps, abrupt spikes, missing metrics, multiple instances, manual override, and recovery; observe transition count, queue age, useful throughput, dependency load, and user outcomes. Thresholds are evidence-driven examples, not universal values.

### Answer 5

Ideal backlog is $45\times60\times80=216{,}000$ jobs. Spare drain rate is $140-80=60$ jobs/second, so ideal drain time is $216{,}000/60=3{,}600$ seconds, or one hour. Before replay, remove expired or cancelled jobs under declared policy, deduplicate by stable identity, and prioritize consequence and deadlines. Reserve capacity for live work and dependency headroom, ramp replay gradually, and reduce it when latency or downstream saturation rises. Keep degraded admission available until backlog and state reconcile. If total safe capacity falls to 80 or less, pause draining rather than destabilize live service; if another dependency fails, follow its scoped mode and preserve ordering and audit evidence.
