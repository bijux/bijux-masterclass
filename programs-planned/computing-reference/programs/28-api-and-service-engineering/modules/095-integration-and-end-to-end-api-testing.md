---
module_id: API-095
program: API & Service Engineering
level: 2
module_number: 95
title: Integration and End-to-End API Testing
status: complete
last_verified: 2026-09-02
---

# Integration and End-to-End API Testing

## One-Page Review

### Governing question

Which assembled boundaries and complete journeys must be exercised to reveal API failures that unit and contract tests cannot, and how can teams obtain trustworthy evidence without building a slow, unsafe, flaky imitation of production?

### Essential definitions

- An **integration test** verifies interaction among two or more real components across an owned boundary: serialization, middleware, database, broker, identity, proxy, or remote service.
- An **end-to-end (E2E) test** drives a selected externally meaningful journey through its production-like entry point and observes its authoritative outcome across the assembled path.
- A **test boundary** states which components are real, simulated, stubbed, shared, or omitted and which configuration/network path is exercised.
- A **system under test (SUT)** is the exact deployable artifact set, configuration, data, and topology whose behavior the result supports.
- A **test oracle** decides whether observations satisfy protocol and domain invariants; HTTP `200` or “event received” is rarely sufficient.
- **isolation** prevents one test's identity, state, time, traffic, or effects from influencing another.
- A **production-faithful environment** preserves relevant semantics, not necessarily production scale or every dependency.
- A **flake** is a non-deterministic result under materially unchanged inputs/SUT; retrying can measure flakiness but cannot turn it into passing evidence.

### Central model, mechanism, or theorem

For a journey through boundaries $B=\{b_1,\ldots,b_n\}$, a passing test supports only the tested configuration vector $x=(a,c,d,t,v)$: artifact, configuration, data state, topology, and dependency versions. Its evidentiary claim is

$$
P(outcome\mid x,scenario)\ge 1-\epsilon,
$$

where $\epsilon$ is bounded nondeterminism measured across repetitions. It does not prove all vectors in the product space $|A||C||D||T||V|$. Select tests by boundary risk and journey criticality; use lower layers for exhaustive logic and E2E for a small set of composition claims.

### Critical invariants

Each test declares purpose, boundary map, exact artifacts/configuration/protocol versions, identities/tenants, state/setup, clock, dependency doubles, oracle, timeout, cleanup, and evidence. It uses the real public entry point and authoritative outcome where that is the claim. Dependencies are real when their semantics matter; doubles have explicit fidelity and drift checks.

Tests are isolated, parallel-safe, deterministic within bounded asynchronous behavior, and safe for irreversible effects. Poll observed conditions with deadlines rather than fixed sleeps. Failures retain correlated requests, logs, traces, messages, state and environment identity without secrets. Quarantine removes a test from gating only with owner, diagnosis, expiry and risk coverage. Passing E2E tests complement—not replace—contract, robustness, security, performance, resilience and production verification.

### Common failures

Calling controller-plus-mock an integration test; sending directly to an internal service while claiming gateway coverage; sharing mutable accounts/rows/topics; order-dependent cleanup; fixed sleeps; unbounded polling; broad eventual assertions; asserting only status; accepting logs as outcome; using latest unpinned images; environment drift; mock-on-both-sides; simulator unlike wire protocol; real third-party charges/email; leaked credentials; bypassed auth; retry-until-green; quarantined tests without owners; huge all-service E2E suites; tests that mutate global configuration; destructive cleanup by broad prefix; missing error/cancellation/retry/idempotency paths; trace sampling hiding evidence; and assuming staging proves production.

### Compact example

A create-order contract test passes against the service. An integration test starts the deployable service with its real database and discovers that transaction commit occurs after the response. An E2E test through gateway and broker drops the response after commit, retries with the same idempotency key, and observes one order, one payment intent, and the same result. **Conclusion:** each layer adds evidence about composition; only the full selected journey reveals gateway ambiguity plus durable effect behavior.

### Connections

[Predictable Endpoints](040-implementing-a-predictable-service-endpoint.md), [Idempotency Keys](037-idempotency-keys.md), [Asynchronous Replay](070-designing-an-asynchronous-api-for-replay-and-evolution.md), [Deadlines](071-timeout-and-deadline-budgets.md), [Failure Amplification](080-preventing-failure-amplification-across-service-calls.md), [Independent Evolution](090-evolving-an-api-without-coordinated-consumer-releases.md), [Gateway Responsibilities](091-api-gateways-and-edge-responsibilities.md), and [Contract Testing](094-contract-testing.md) define behaviors to assemble. Later modules add fuzzing, observability, capacity, onboarding, and readiness evidence.

## Governing Question

How should teams partition integration and end-to-end coverage, construct faithful isolated environments, test synchronous/asynchronous and failure behavior, diagnose nondeterminism, and operate suites as credible release evidence?

## Why This Matters

Most production API incidents arise from components that were individually “correct”: a gateway strips a header, serializer changes timezone, database isolation exposes a race, DNS selects an old version, broker redelivers, auth policy differs by environment, proxy timeout preempts the application, or deployment configuration points at the wrong dependency.

Unit tests cannot reveal wiring they omit. Contract tests establish selected boundary obligations but usually isolate provider state and dependencies. Integration tests deliberately assemble the smallest real boundary that can reveal a suspected interaction. E2E tests verify a few critical journeys through the delivered system.

Yet realism is not binary. A staging environment can have fake identity, empty data, one replica, no latency, newer dependencies, permissive policies, and different routing. A broad E2E test may fail for dozens of causes and teach nothing. Shared state and time produce intermittent results that teams normalize as “CI noise.”

The discipline is evidence architecture: make each test's claim and omissions explicit, push most coverage down to fast deterministic layers, and reserve expensive assembled tests for risks that truly require assembly.

## Prerequisites and Retrieval

Retrieve [Transport, Application, and Domain Boundaries](031-transport-application-and-domain-boundaries.md), [Idempotency Keys](037-idempotency-keys.md), [Concurrency Control](038-concurrency-control-at-the-api-boundary.md), [Error Translation](035-error-translation.md), [Authentication Context](033-authentication-context-propagation.md), [Object Authorization](046-object-level-authorization.md), [Delivery and Acknowledgment](066-delivery-and-acknowledgment.md), [Idempotent Consumers](067-idempotent-consumers.md), [Timeouts](071-timeout-and-deadline-budgets.md), [Retries](072-retries-and-backoff.md), [Consistency](079-consistency-and-read-after-write-expectations.md), [Gateways](091-api-gateways-and-edge-responsibilities.md), [Discovery](092-service-discovery-and-routing.md), [Service Mesh](093-service-mesh-relationships.md), and [Contract Testing](094-contract-testing.md).

Retrieve journey/risk inventory; topology and trust boundaries; deployable artifact/container and lockfiles; environment/config/feature flags/secrets identities; gateway/mesh/discovery routes; database/broker/cache/object-store versions; migration/seed/reset mechanisms; external dependency simulators/sandboxes; time/ID/random controls; tenant/user/role fixtures; asynchronous completion signals; test history/flakes/quarantine; logs/traces/message/state evidence; production incidents; and CI resource/concurrency/cost budgets.

## Learning Objectives

After completing this module, you can:

1. distinguish unit, component, contract, integration, E2E, smoke, synthetic, and production verification claims;
2. choose the smallest assembled boundary capable of exposing a target risk;
3. define a test manifest binding artifacts, configuration, topology, state, identities, dependencies, tools, and observations;
4. build isolated, reproducible, parallel-safe data and environment lifecycles;
5. select real dependencies versus emulators/stubs from semantic fidelity and failure-control needs;
6. test async completion, retries, cancellation, duplicates, ordering, consistency, and partial failure without sleeps;
7. design domain/protocol/security oracles that verify authoritative outcomes and absence of forbidden effects;
8. preserve actionable artifacts and diagnose test, environment, application, dependency, and timing failures;
9. govern flakes, quarantine, sharding, cost, suite tiers, and release gates; and
10. explain exactly what passing assembled tests do and do not establish about production readiness.

## Core Exposition

### Start from risk and claim

Write the suspected failure first: “gateway loses tenant context,” “transaction and outbox diverge,” “old client cannot decode new enum,” “retry duplicates charge,” or “watch misses updates after reconnect.” Identify the minimum real boundary needed to make that failure possible.

A component test may run the deployable service through its network listener with in-process substitutes. An integration test might add the actual database/broker/proxy. E2E adds the external entry, identity, routing, downstreams and outcome surface for one journey. Names matter less than a boundary manifest.

Avoid a universal pyramid ratio. Risk, change frequency, protocol, cost, determinism and diagnosis determine layer. Keep exhaustive validation and domain transitions below E2E; keep configuration, serialization and wiring above units.

### Define the system under test precisely

Record source revision and artifact digest for every owned component; dependency images and schema/migration versions; environment identity; config/flags/policies; gateway/mesh/discovery revisions; seed digest; clock mode; tool/browser/client version; and test selection.

Pin images and dependencies. “Latest” destroys reproducibility. Build artifacts once and promote them rather than rebuilding different binaries for test and release. A result for p9 with config c3 does not automatically support p9 with c4.

Capture topology: entry URL, DNS, TLS identity, proxies, regions/zones, replicas, network policies, brokers/topics, databases/schemas and external doubles. State explicitly what is bypassed.

### Select real dependencies by semantics

Use a real database when transaction isolation, constraints, migrations, query encoding, locking, time types or driver behavior are at risk. Use a real broker when partitioning, acknowledgments, redelivery, ordering, headers, compression or consumer groups matter. Lightweight containers make pinned disposable infrastructure practical, but containerization itself does not guarantee production configuration or topology.

Use a stub when only a narrow deterministic response matters, or when the real third party is unsafe/unavailable. A protocol simulator should parse real messages, enforce the relevant state machine, expose invocations and inject failures. Verify it against the provider's sandbox or contract to limit drift.

Do not mock both sides of the boundary whose integration you claim. If service A's HTTP client and fake B share the same generated model, both may reproduce the same wrong assumption. Contract and real-provider tests counter this common-mode error.

### Build isolated state

Prefer fresh per-test namespaces, databases/schemas, tenant IDs, account IDs, topics/consumer groups, object prefixes, browser contexts and credentials. Unique IDs make parallel execution safe. Cleanup should target exact owned resources; never delete by an ambiguous shared prefix.

Starting clean is stronger than compensating cleanup because failed cleanup and unobservable caches/session state leak. Playwright documents fresh browser contexts as its isolation mechanism; the durable principle applies beyond browsers.

If full environments are expensive, pool immutable infrastructure but isolate logical data and reset with verified snapshots. Test the reset itself. Serialize only tests that truly mutate a singleton; do not hide races by disabling parallelism globally.

Use synthetic data. Never copy unredacted production personal data or tokens. Model locales, Unicode, time zones, large values, tenants, roles and lifecycle states deliberately.

### Control time, randomness and identity

Inject or virtualize clocks at owned boundaries while retaining integration tests for actual protocol timestamps, TTLs and clock skew. Record random seeds and generated IDs. Avoid asserting exact real time; assert bounded relations.

Identity fixtures include issuer, audience, tenant, subject, scopes/roles, expiry and key revision. Exercise valid, expired, future, wrong audience/issuer/tenant and rotated-key overlap through the real authentication middleware. Do not install a “test admin” bypass on the claimed path.

Protect session/auth state. Playwright warns that stored browser authentication can contain impersonating cookies/headers; keep it out of source and artifacts, scope it to synthetic accounts, encrypt/rotate it and redact evidence.

### Construct strong oracles

Observe at the authoritative boundary. A create test checks response semantics plus durable authoritative record, expected event/outbox, and absence of duplicate/forbidden side effects. Do not declare success from a log line or intermediate queue alone.

Check both positive and negative space: expected status/body/headers, state transition, actor/tenant ownership, effect count, audit entry and telemetry correlation; also no cross-tenant access, no secret/error leak, no second charge, no unexpected event and no state after rejection.

HTTP tests honor RFC 9110 method/status/header/content semantics through real serialization/intermediation. Exercise conditional requests, content negotiation, compression, redirects, caching boundaries, malformed input and disconnect/cancellation as relevant.

For multi-step workflows, assert invariant after each meaningful operation, not only final UI text. A test that creates through API then reads the database may diagnose persistence; a user-journey E2E should also read through the supported API/UI.

### Wait for evidence, not time

Fixed sleep $s$ is both slow when completion is fast and flaky when completion exceeds $s$. Poll a meaningful externally observable predicate with deadline, backoff and diagnostic sampling, or subscribe from a known sequence/revision.

For async APIs, establish observation before triggering to avoid lost wakeups. Correlate by unique journey ID. Account for at-least-once duplicates, reordering within declared boundaries, consumer lag and eventual read model. A broad “eventually some order exists” can accept another test's data.

Kubernetes watch semantics illustrate a general pattern: list at a resource version then watch from it to avoid a gap, while handling compaction/reconnect. Never assume a watch/bookmark arrives at a fixed interval.

Bound every phase: setup, request, completion, assertions and cleanup. On timeout, preserve last observed state/revision/lag and correlated trace rather than only “timed out.”

### Test failure and ambiguity

Inject failures at defined points: before request write, after server receive, before/after commit, after response headers, dependency timeout, broker ack loss, proxy reset, replica restart and stale discovery. Confirm error mapping, cancellation, retries, idempotency and outcome lookup.

Use transport-level failure controls rather than application flags when testing transport ambiguity. Application hooks can deterministically expose commit boundaries, but must be test-only, authenticated, not shipped enabled, and clearly distinct from product behavior.

Verify partial failure and recovery: no forbidden effect, bounded retry, deduplicated effect, resumable stream, compensating state, reconciler convergence or explicit unknown outcome. Test restart with persisted state, not only in-memory happy paths.

### Design a small E2E journey portfolio

Choose critical/high-risk journeys: authentication and tenant boundary, primary value creation, read-after-write, idempotent retry, failure/recovery, permissions, async completion and one upgrade/compatibility path. Cover representative clients/protocols and negative outcomes.

Do not multiply every role × locale × browser × region × version at E2E. Pairwise/risk-based selection reduces combinations; lower layers cover exhaustive validation. If dimensions have 4 browsers, 5 roles, 3 locales, 2 API versions and 3 regions, the full product is $4\times5\times3\times2\times3=360$ runs before data/failure cases.

Smoke tests provide rapid deploy verification of route/identity/dependency basics. Wider integration suites run per change or merge. Critical E2E gates release. Destructive/resilience/security suites run in controlled environments. Production synthetics use read-only or safely idempotent operations and distinct telemetry.

### Make failures diagnosable

Assign a run/journey/correlation identifier propagated through gateway, services, messages and state where safe. Collect sanitized requests/responses, structured logs, traces, metrics snapshots, broker offsets/keys, database state, config/artifact digests and environment events.

OpenTelemetry defines a distributed trace as events/spans for a logical operation; traces aid causality but sampling/instrumentation gaps mean absence is not proof. For test environments, use deterministic capture for test correlation where feasible and validate telemetry health separately.

Classify: assertion/contract defect, test setup/cleanup, environment capacity/control plane, dependency, product defect, timeout budget, race/nondeterminism, or observability gap. Preserve first failure before retry. Reproduce with the same seed/artifacts/config/state topology.

### Govern flakiness and suite economics

Estimate flake amplification. If each of $n$ independent tests has false-failure probability $f$, suite false-failure probability is

$$
1-(1-f)^n.
$$

At $n=100$ and $f=0.01$, this is approximately $1-0.99^{100}\approx63.4\%$. Small flakes make large gates unusable.

Retry once only to classify/reproduce; report both attempts. A test that passes on retry is flaky, not green evidence. Quarantine requires owner, linked defect, risk/coverage substitute, expiry and visible debt. Fix root causes: isolation, condition waits, resource headroom, deterministic state, pinned dependencies and stronger diagnostics.

Track duration distribution, queue time, flake rate, failure yield, diagnosis time, quarantine age, coverage by journey/risk, escaped defects and cost. Delete redundant low-yield E2E tests after equivalent lower-level coverage exists.

### Relate test to production evidence

Staging proves the declared staging vector. Production differs in scale, traffic mix, topology, credentials, data, caches, tenancy, dependency policies and failures. Use progressive delivery, canaries, health/SLO signals, shadow-safe comparison and rollback to bridge the gap.

OWASP's testing guidance emphasizes API security testing across authentication, authorization, input, error and exposure concerns. Integration/E2E functional tests should include security invariants, but do not replace dedicated adversarial review and testing.

After incidents, ask which boundary could have caught the defect cheapest and faithfully. Add evidence at that layer, not automatically another giant E2E test.

## Definitions and Notation

Let $A,C,D,T,V$ be relevant artifact, configuration, data, topology and dependency-version sets. Let $x\in A\times C\times D\times T\times V$ identify the tested vector. Let $J$ be critical journeys, $B(j)$ their traversed boundaries, $O(j)$ the oracle, and $\epsilon$ measured false-result probability under stable conditions.

A **fixture** provisions controlled preconditions. A **double** substitutes a dependency with documented fidelity. A **sandbox** is an externally operated nonproduction dependency environment. A **synthetic** continuously exercises a safe journey. A **quarantine** is a governed temporary removal from gating, not deletion or success.

## Mechanisms, Invariants, or Proof Structure

**Boundary-minimality argument.** If failure F depends on interaction of boundaries X and Y, tests omitting either cannot reproduce F. Adding unrelated Z increases setup/failure causes without increasing evidence for F. Therefore the smallest faithful assembly containing X and Y maximizes diagnostic specificity for that risk.

**Sleep counterexample.** Completion time varies; choose a run with $t>s$ and fixed sleep $s$. The assertion executes early and fails although the system would satisfy the contract. Increasing s cannot prove an upper bound and slows all faster runs. Condition-plus-deadline is the correct mechanism.

**Combinatorial derivation.** Independent dimension enumeration multiplies. The illustrative $4\cdot5\cdot3\cdot2\cdot3=360$ E2E combinations justify risk/pairwise selection and exhaustive lower-layer tests, not untested dimensions.

**Flake amplification.** With independent per-test false-failure f, probability no test flakes is $(1-f)^n$; complement yields $1-(1-f)^n$. Independence is an approximation; shared-state correlation can be worse and must be measured.

## Alternatives and Trade-Offs

In-process integration is fast/debuggable but may omit real network, process, serialization and lifecycle. Disposable containers improve protocol/version fidelity and isolation but add startup/resources and not full topology. Shared staging approaches deployment wiring but accumulates contention/drift. Ephemeral full environments isolate well but cost more and may still differ from production.

Real third parties provide fidelity but cause nondeterminism, quotas, costs and unsafe effects. Sandboxes may differ from production. Simulators provide control and fault injection but drift. Combine contract verification, simulator conformance and a few sandbox checks.

Database inspection gives strong internal diagnostic oracles but couples schema; public reads prove external behavior but may hide exact durable state. Use internal assertions in integration tests and external outcomes in E2E according to claim.

Serial execution reduces collisions but hides concurrency bugs and lengthens feedback. Logical isolation enables parallelism. Full reset is stronger but slower than transactional rollback, which misses commits, background workers and external state.

## Failure Modes and Misconceptions

- “Uses HTTP, therefore E2E” ignores bypassed gateway, auth, routing and dependencies.
- “All dependencies real” does not imply correct configuration/topology or safe effects.
- “Staging equals production” ignores traffic, scale, data, identity and failure differences.
- “Sleep longer” trades speed for a different flake threshold.
- “Eventually true” without unique correlation can observe another test's state.
- “Retry passed” is evidence of nondeterminism, not original success.
- “One shared admin account” destroys tenant/role/isolation coverage.
- “Cleanup after test” fails when the process crashes; provision isolated ownership first.
- “A trace proves no call occurred” ignores sampling and instrumentation gaps.
- “Test database details in every E2E” couples journeys and bypasses public outcomes.
- “Run every combination” creates slow low-signal suites and still misses failure states.
- “E2E covers security/performance” confuses selected behavior with adversarial/distribution evidence.
- “Quarantine is harmless” leaves a silent release-risk gap.
- “Green staging authorizes production” skips progressive verification and rollback.

## Worked Examples

### Example 1

Gateway test sends a tenant token through the public host; service receives wrong tenant because header mapping changed. Direct-service integration passed. **Conclusion:** include the intermediary when its transformation is the risk.

### Example 2

Two parallel tests edit account `demo`; outcomes alternate. Give each a unique tenant/account and exact cleanup namespace. **Conclusion:** isolation removes shared-state order dependence rather than masking it with serialization.

### Example 3

Job usually completes in 200 ms but sometimes 1.2 s; test sleeps 500 ms. Poll its unique public status to a 3 s deadline and capture transitions. **Conclusion:** condition waiting is faster and more truthful.

### Example 4

Order response returns before DB commit; process crash loses order. Service+real-database integration crashes at the boundary and catches the defect. **Conclusion:** real transaction/lifecycle semantics justify dependency inclusion.

### Example 5

Retry after response loss creates two payment intents. E2E injects drop after commit and asserts same response plus one authoritative effect. **Conclusion:** ambiguous transport and durable idempotency require full selected path.

### Example 6

Event arrived but wrong partition key reordered account updates. Test subscribes before trigger, records key/offset, sends two correlated updates and asserts order. **Conclusion:** payload receipt alone is an incomplete oracle.

### Example 7

Five dimensions produce 360 combinations. Risk analysis selects all auth roles at API integration, browser pairwise journeys, and one regional failover E2E. **Conclusion:** distribute coverage by cheapest faithful layer.

### Example 8

At one-percent independent flake rate, 100-test suite false-fails about 63.4%. Unique resources and bounded waits reduce f to 0.001, yielding about 9.5%. **Conclusion:** flake reduction has nonlinear gate value.

### Example 9

Browser authentication state is committed accidentally. Rotate credentials, revoke account, purge history/artifacts and create runtime secret provisioning. **Conclusion:** test evidence and fixtures are security assets.

### Example 10

Staging E2E passes with one replica; canary reveals stale discovery routes to old version. Add mixed-version integration and route telemetry, retain progressive gate. **Conclusion:** test environments do not eliminate production verification.

## Cross-Program Connections

[Software Engineering: Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies test levels, doubles, property testing, mutation, coverage, flake analysis and oracles.

[Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) supplies artifact promotion, CI/CD gates, progressive delivery, rollback, environments and incident learning.

[Database Engineering](../../18-database-engineering/ROADMAP.md) supplies transactions, constraints, isolation, migrations, concurrency and recovery.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies time, partial failure, retries, messaging, ordering, consistency, failure injection and recovery.

[Security Engineering](../../25-security-engineering/ROADMAP.md) supplies identity, tenant isolation, secret/test-data controls, abuse cases, adversarial testing and evidence integrity.

## References

1. IETF, [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html), June 2022.
2. Testcontainers, [Modules](https://testcontainers.com/modules/).
3. Microsoft, [Playwright Test Isolation](https://playwright.dev/docs/browser-contexts).
4. Microsoft, [Playwright Authentication](https://playwright.dev/docs/auth).
5. Kubernetes, [API Concepts: Efficient Detection of Changes](https://kubernetes.io/docs/reference/using-api/api-concepts/#efficient-detection-of-changes).
6. OpenTelemetry, [Specification Overview](https://opentelemetry.io/docs/specs/otel/overview/).
7. OWASP, [Web Security Testing Guide: API Testing Overview](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/12-API_Testing/00-API_Testing_Overview).

## Exercises

### Exercise 1

For an order API backed by PostgreSQL, broker, payment provider and search index, assign risks to unit, contract, component, integration, E2E and production verification layers.

### Exercise 2

A suite has 200 independent tests with 0.5% false-failure probability each. Compute suite false-failure probability and propose evidence-preserving remediation.

### Exercise 3

Design an isolated async E2E test for create order → authorize payment → publish event → update read model, including response loss, duplicate delivery and delayed indexing.

### Exercise 4

Compare a shared staging environment, per-branch disposable environment and local container integration for a gateway/service/database/broker migration. Select a portfolio.

### Exercise 5

Diagnose a release gate where tests fail only in parallel: wrong tenants appear, timeouts cluster, traces are missing, cleanup deletes other runs, and retry passes. Define stabilization and durable corrections.

## Answers to the Exercises

### Answer 1

Unit: validation, pricing/state transitions, retry/idempotency algorithm, mapping. Contract: consumer-required HTTP/errors/events and provider behavior. Component: deployable service listener with controlled doubles for handler/middleware/serialization. Integration: real PostgreSQL constraints/transactions/migrations/outbox; real broker key/ack/redelivery; search mapping; payment simulator protocol/state/failures. E2E: public gateway+identity journey for create/read, response-loss retry, tenant denial, async completion and one failure/recovery path, asserting authoritative order and single payment intent plus event/read outcome. Sandbox check covers payment provider compatibility without real charge. Production canary/synthetics verify actual routing/config/scale/dependency policies; security, capacity and chaos remain separate evidence.

### Answer 2

$1-(1-0.005)^{200}=1-0.995^{200}\approx1-0.367=0.633$, about 63.3%. Preserve first-attempt outcome; one diagnostic rerun classifies rather than erases. Measure per-test and correlated failures, then fix unique data/tenant/resources, condition waits, pinned artifacts/config, resource headroom, deterministic clocks/seeds and dependency health. Split gate by risk only when feedback timing requires it, not to hide flakes. Quarantine a specific test only with owner, defect, expiry and substitute coverage. The independence calculation is approximate; clustered environment failures require conditioning on shared causes.

### Answer 3

Provision unique tenant/user/order/idempotency key, payment-simulator account, topic/consumer group and read namespace; subscribe/record offset before trigger. Run exact artifact/config through gateway/auth with real DB/broker/read consumer and stateful payment simulator. Drop response after durable commit, retry same key, and require same logical result, one order, one payment authorization intent/effect and one logical event despite possible duplicate delivery. Inject duplicate event and assert consumer dedupe. Poll unique public order/read status with bounded deadline/backoff, recording revisions/lag; no fixed sleep. Assert tenant ownership, amounts/state, event key/envelope/order, audit and absence of cross-tenant/duplicate effects. Capture sanitized correlated trace/log/message/state; cleanup exact namespace, retaining evidence on failure.

### Answer 4

Local disposable containers give fast deterministic database/broker migration and gateway/service protocol tests, including old/new schema and rollback; they omit managed identity/network/topology. Per-branch disposable environment adds real deployment manifests, gateway policies, TLS/discovery and parallel isolation at higher cost; use for merge/release candidates and migration rehearsal. Shared staging best resembles managed dependencies/identity but suffers contention/drift; reserve it for a small serial smoke/E2E and external sandbox, with immutable environment/config identity and namespaced data. Promote the same artifacts through all three, pin versions, run compatibility matrices for old/new service/schema/consumer, and use production canary/rollback because none reproduces production traffic/scale.

### Answer 5

Stop treating retry as pass; preserve first failures and reduce concurrency only as temporary stabilization. Assign run/tenant/resource IDs and prove collision from requests/state. Replace shared accounts/rows/topics with per-test namespaces; make cleanup exact-owner and crash-safe, disabling destructive broad cleanup immediately. Separate environment saturation via CPU/memory/connection/queue telemetry and cap workers until sized. Replace sleeps with correlated condition waits/deadlines. Configure deterministic trace capture for test correlation and diagnose propagation/exporter gaps; missing trace is not no call. Pin artifacts/config/dependencies and record seeds. Classify each failure, repair isolation/resources/observability, re-enable parallel cohorts progressively, and require repeated clean runs at target concurrency. Quarantines need owners/expiry/substitute gates; audit any data deleted by prior cleanup.
