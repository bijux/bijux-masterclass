# The Six-Course Journey

## Why this order matters

The curriculum is ordered by responsibility, not by technology popularity. Each stage establishes a capability that the next stage must preserve. Skipping ahead can produce code that runs while leaving the underlying claim undefined.

## Course 1 — OpenAPI Contract Engineering

**Responsibility:** Define and verify the public HTTP contract.

**Central question:** What exactly does the API promise, and how can providers and consumers verify that promise?

**Incoming boundary:** Basic programming ability and no assumed OpenAPI experience.

**Outgoing boundary:** A frozen API 1.1 contract, operation ledger, schema fixtures, security decisions, workflows, and provider-neutral behavioral scenarios.

| Module | Question | Platform increment |
|---:|---|---|
| 1 | How do raw HTTP exchanges become a public contract without confusing documentation with runtime behavior? | Establish health and project operations as raw messages, OpenAPI operations, and equivalent provider behavior. |
| 2 | How are parameters, request bodies, media types, status codes, and headers modeled without ambiguity? | Complete project and dataset messages, including pagination inputs, creation responses, and problem representations. |
| 3 | How do schemas reject invalid states while remaining usable for providers, clients, and future evolution? | Define precise project, dataset, run, artifact, and problem schemas with a shared valid/invalid fixture corpus. |
| 4 | How can a multi-document contract remain understandable, relocatable, and deterministically buildable? | Split the contract into owned documents, resolve every reference offline, and produce deterministic bundles. |
| 5 | How should an HTTP API express asynchronous work, retries, conflicts, conditional updates, and machine-readable failures? | Add the analysis-run workflow, idempotency key, status resource, ETags, cancellation, and Problem Details. |
| 6 | How do design-first and code-first descriptions relate, and how is semantic drift detected? | Map every operation to both providers and compare generated observations with the canonical contract. |
| 7 | How do mocks, generated clients, examples, property tests, and stateful tests provide different evidence? | Build the consumer and contract-test ladder against the mock and both real providers. |
| 8 | What can the public contract say about authentication and authorization, and what remains a runtime responsibility? | Describe API-key and OAuth-style schemes, scopes, anonymous overrides, and documented security failures. |
| 9 | How can a published API evolve without silently breaking request writers or response readers? | Create compatible and rejected release candidates, compatibility gates, and public/partner audience views. |
| 10 | How do current OpenAPI features express streaming, webhooks, links, query methods, and multi-step workflows? | Publish the OpenAPI 3.2 frontier, streaming and webhook contracts, links, and an Arazzo workflow. |

## Course 2 — Contract-Driven API Service Engineering

**Responsibility:** Implement the fixed contract with durable application, database, worker, storage, and release mechanisms.

**Central question:** Which internal mechanisms keep the public contract true under concurrency, restart, and partial failure?

**Incoming boundary:** The immutable Course 1 API 1.1 handoff and its provider-neutral proof corpus.

**Outgoing boundary:** A durable API 1.2 service handoff with migrations 001–005, idempotency, optimistic concurrency, stable pagination, worker recovery, artifact integrity, and transactional webhook delivery.

| Module | Question | Platform increment |
|---:|---|---|
| 1 | How does a public operation become an application use case without letting the framework own the system? | Create transport, application, and adapter boundaries for the fixed operation ledger. |
| 2 | Which state transitions and invariants must remain true regardless of framework or database? | Implement project, dataset, run, cancellation, and artifact rules as testable domain behavior. |
| 3 | How should relational structure and migrations reinforce rather than merely store application invariants? | Persist principals, projects, datasets, runs, artifacts, and ownership with constraints and deterministic migrations. |
| 4 | How do idempotency and conditional updates remain atomic under concurrent requests and process restarts? | Implement persistent request fingerprints, replayed outcomes, version columns, ETags, and transaction rollback. |
| 5 | How do filters, stable cursors, and authorization-aware queries remain correct while data changes? | Implement owner-bound, filter-bound, high-water keyset traversal and evidence-backed query plans. |
| 6 | What makes a 202 Accepted operation honest after the API process or worker dies? | Add durable jobs, leases, heartbeats, fencing, cancellation, duplicate-safe effects, and abandoned-work recovery. |
| 7 | How can large uploads, progress streams, and artifacts remain bounded, durable, and integrity-checked? | Implement streamed upload, content-addressed publication, checksums, SSE/NDJSON progress, and authorized download. |
| 8 | How can a committed business change reliably produce an external webhook without a dual write? | Add a transactional outbox, signed deliveries, retry state, deduplication, and destination constraints. |
| 9 | How do tests prove transactions, concurrency, restart, storage, and delivery guarantees rather than only happy paths? | Assemble pure, integration, concurrent, process-kill, conformance, and planted-defect proofs. |
| 10 | How can old and new service versions coexist through a database change and still preserve the public contract? | Build lifecycle controls, compatible expand/backfill/enforce migrations, rollback evidence, and release proof. |

## Course 3 — API Security Engineering

**Responsibility:** Preserve the API and durable-service guarantees when callers, credentials, inputs, destinations, and dependencies are not trusted by default.

**Central question:** How does the service remain trustworthy under hostile behavior without hiding behind middleware or scanner output?

**Incoming boundary:** The Course 2 API 1.2 durable-service handoff and migrations 001–005.

**Outgoing boundary:** Security Profile 1.0, migrations 006–007, threat-to-requirement traceability, identity and authorization policy, hostile-input vectors, secure webhook rules, abuse controls, and incident evidence.

| Module | Question | Platform increment |
|---:|---|---|
| 1 | Which assets, actors, trust boundaries, abuse cases, and assumptions define the real security problem? | Create a security case that traces threats to requirements, control owners, tests, and residual risk. |
| 2 | Which raw HTTP message should the application trust after proxies, parsers, duplicate fields, and size limits intervene? | Establish host, forwarding, media-type, strict-JSON, body-size, and canonicalization rules before model validation. |
| 3 | How should a resource server validate bearer tokens and API keys without trusting convenient claims? | Implement issuer, audience, algorithm, key, lifetime, revocation, subject, tenant, and scope validation. |
| 4 | How are scopes, roles, ownership, tenant membership, relationships, assurance, and freshness combined under default deny? | Build explicit authorization decisions for collections, individual resources, fields, support access, and administration. |
| 5 | How are hostile strings, numbers, paths, filenames, uploads, and serialized structures constrained at the correct boundary? | Harden input parsing, Unicode, traversal, MIME, streaming upload, checksum, query, and error behavior. |
| 6 | How can outbound HTTP and webhook delivery avoid SSRF, rebinding, redirect abuse, tampering, and replay? | Implement destination policy, address classification, peer verification, exact-byte signatures, freshness, rotation, and replay defense. |
| 7 | How should secrets, cryptographic keys, sensitive fields, logs, retention, and audit evidence be handled? | Add secret-provider boundaries, non-rendering values, redaction, pseudonymization, rotation, and privacy-bounded audit records. |
| 8 | How can the service resist brute force and resource exhaustion without turning traffic control into false authorization? | Introduce principal/tenant/operation/cost budgets, concurrency permits, quotas, and bounded degradation. |
| 9 | How do adversarial tests and supply-chain evidence show that controls fail closed and that the proof is sensitive? | Build hostile vectors, negative policy tests, planted vulnerabilities, dependency evidence, SBOM/provenance routes, and scanner disposition. |
| 10 | How is a suspected compromise detected, contained, investigated, rotated, patched, and converted into improved requirements? | Run a controlled credential and cross-tenant incident with timelines, revocation, rotation, release, and threat-model revision. |

## Course 4 — API Reliability and Observability Engineering

**Responsibility:** Detect, diagnose, contain, reconcile, and recover when processes, dependencies, networks, or operators fail.

**Central question:** How do operators know whether the user promise is still true, and how do they recover it without making the incident worse?

**Incoming boundary:** The Course 3 API 1.2 service protected by Security Profile 1.0 and migrations 001–007.

**Outgoing boundary:** Reliability Profile 1.0, migration 008, critical journeys, deadlines, resilience policies, lifecycle controls, telemetry contracts, SLOs, alerts, runbooks, game-day evidence, and reconciliation plans.

| Module | Question | Platform increment |
|---:|---|---|
| 1 | Which user journeys matter, what makes them good or bad, and which durable facts establish the outcome? | Create the reliability case, critical-journey populations, failure modes, ownership, residual risk, and negative claims. |
| 2 | How is one absolute time budget propagated through retries, dependencies, and cancellation without multiplying work? | Implement monotonic deadlines, child budgets, safe retry classification, backoff, Retry-After handling, and cancellation. |
| 3 | How should circuits, bulkheads, and degradation be scoped so they contain rather than hide dependency failure? | Add dependency-local state machines, bounded probes, concurrency isolation, and truthful degraded responses. |
| 4 | How do APIs, workers, and dispatchers start, become ready, drain, stop, and recover without losing accepted work? | Implement lifecycle states, liveness/readiness separation, graceful draining, lease handling, and startup reconciliation. |
| 5 | Which operational events are useful, bounded, redacted, versioned, and clearly separated from business truth? | Create the telemetry vocabulary, correlation rules, bounded sinks, exporter failure behavior, and privacy policy. |
| 6 | How are counters, gauges, histograms, and SLI populations defined so the math means what operators think it means? | Implement bounded metric dimensions, units, good/bad/eligible/excluded populations, and aggregation semantics. |
| 7 | How does trace context cross HTTP, queues, workers, storage, retries, and webhooks without inventing false parentage? | Implement validated context, synchronous parent-child spans, asynchronous links, attempts, queue time, and privacy-safe attributes. |
| 8 | How do versioned SLOs, exact error budgets, burn rates, dashboards, alerts, and runbooks drive decisions? | Publish five journey SLOs, multiwindow alerts, owner-linked runbooks, and release policy. |
| 9 | How can fault injection and game days produce falsifiable evidence without creating uncontrolled damage? | Design bounded faults, control populations, abort conditions, cleanup contracts, and proof-sensitive planted defects. |
| 10 | How do responders command an incident, reconcile durable state, repair safely, and decide whether a release is operationally ready? | Run incident roles, read-only reconciliation, stable repair plans, verification, retrospective, and observable release gates. |

## Course 5 — API Performance, Capacity, and Traffic Engineering

**Responsibility:** Preserve correctness, latency, throughput, fairness, and bounded resource use as demand and data volume grow.

**Central question:** Where does time and capacity go, what is the first limiting resource, and which measured change improves the system without weakening its promise?

**Incoming boundary:** The Course 4 observable and recoverable API 1.2 service with Security and Reliability Profiles 1.0 and migrations 001–008.

**Outgoing boundary:** Performance Profile 1.0, migration 009, workload identities, benchmark evidence, HTTP and query optimizations, concurrency and cache policy, traffic controls, capacity models, and performance release gates.

| Module | Question | Platform increment |
|---:|---|---|
| 1 | What exactly is being measured, under which workload and environment identity, and which correctness oracle still applies? | Freeze six critical workloads, measurement envelopes, outcome populations, evidence classes, and comparable baselines. |
| 2 | How do open and closed demand, warmup, sample size, missing outcomes, variation, and statistical uncertainty change benchmark meaning? | Build reproducible benchmark profiles, repeated runs, quantile and interval summaries, and accepted/rejected/inconclusive comparisons. |
| 3 | Where do HTTP connections, representations, compression, conditional requests, range delivery, and streaming consume time and bytes? | Optimize artifact and metadata delivery while preserving authorization, ETags, ranges, and bounded memory. |
| 4 | Which query plan, index, lock, pool, or pagination behavior is the first persistence bottleneck for a declared workload? | Capture before/after plans, add evidence-backed indexes, size database connections, and preserve owner-aware query semantics. |
| 5 | Which Python or Node.js runtime phase consumes wall time, CPU, allocations, event-loop capacity, or serialization effort? | Profile named phases, detect blocking work, bound profiling overhead, and prove mechanism-level improvements. |
| 6 | How do arrival rate, service time, queue depth, concurrency, fairness, and backpressure determine overload behavior? | Implement bounded admission, per-operation limits, queue accounting, permit release, and recovery after pressure. |
| 7 | Which data is safe to cache, for whom, for how long, and who owns invalidation after mutation or failure? | Build authorization-aware keys, TTL/capacity policy, source-version invalidation, single-flight fills, and failure semantics. |
| 8 | How should quotas, priorities, cost budgets, and load shedding preserve fairness and truthful 429/503 outcomes? | Implement multi-dimensional fixed-point budgets, tenant isolation, staged shedding, and rollback of partial reservations. |
| 9 | What capacity does the current system have, what uncertainty surrounds it, and which resource becomes the first bottleneck as demand grows? | Model CPU, connections, workers, queues, storage, egress, cost, headroom, and scaling decisions. |
| 10 | How does a performance change become a reproducible release decision rather than a favorable chart? | Build correctness-first regression gates, environment comparability, accepted/rejected/inconclusive candidates, and a performance dossier. |

## Course 6 — Event-Driven API Engineering

**Responsibility:** Design, evolve, secure, operate, and verify asynchronous contracts when delivery may be delayed, duplicated, reordered within declared limits, or replayed.

**Central question:** How can independent producers and consumers share durable facts without confusing intent, delivery attempts, processing effects, and historical truth?

**Incoming boundary:** The Course 5 API 1.2 service with Security, Reliability, and Performance Profiles 1.0 and migrations 001–009.

**Outgoing boundary:** Analysis Events API 1.0, Event Profile 1.0, AsyncAPI 3.1.0 contract, CloudEvents 1.0 envelope profile, migrations 010–012, replay and dead-letter policy, and governed consumer declarations.

| Module | Question | Platform increment |
|---:|---|---|
| 1 | Which interactions are commands, immutable facts, queries, notifications, or private domain events, and who owns each public fact? | Create the minimal message taxonomy, publication decision record, owner catalogue, and synchronous/asynchronous boundary. |
| 2 | How do AsyncAPI, CloudEvents, schemas, channels, operations, bindings, and examples form one governed event contract? | Publish Analysis Events API 1.0 with canonical envelopes, message schemas, examples, operation ownership, and deterministic bundles. |
| 3 | What do acknowledgement, redelivery, ordering, partitioning, lag, and consumer groups actually guarantee? | Implement deterministic delivery attempts, partition order, group independence, acknowledgement expiry, negative acknowledgement, and redelivery. |
| 4 | How do producers avoid dual writes and consumers obtain exactly-once effects on top of at-least-once delivery? | Implement transactional outbox publication, inbox deduplication, effect-version identity, and atomic consumer effects. |
| 5 | How do event schemas evolve while retained historical events remain immutable and replay remains intelligible? | Classify compatibility, add upcasters, preserve source bytes, define retention, and run bounded dry-run replay. |
| 6 | How do idempotent consumers, projections, and process managers coordinate asynchronous workflows without hidden synchronous coupling? | Build notification, analytics, audit, and orchestration consumers with stable derived-command identities and explicit state. |
| 7 | How do event time, processing time, windows, watermarks, lateness, and corrections affect derived results? | Implement windowed analysis metrics, watermark progression, late-event correction revisions, and quarantine. |
| 8 | How are producers authenticated, consumers authorized, tenants isolated, payloads minimized, and event bytes protected? | Add producer policy, tenant-scoped subscriptions/replay, exact-byte signatures, freshness, classification, and privacy rules. |
| 9 | How do lag, backpressure, retry, poison messages, dead-letter custody, broker failure, and replay storms affect recovery? | Implement failure classification, bounded retry, dead-letter records, lag health, replay controls, and operational runbooks. |
| 10 | How are event ownership, compatibility, retention, replay, consumers, evidence, and release decisions governed as a platform capability? | Publish the catalogue, consumer declarations, accepted/rejected release candidates, final defense, and Course 7 handoff. |

## The maturity curve

By the end of Course 1, you can specify and test a public interface. By the end of Course 2, you can explain why its guarantees survive restart and concurrency. Course 3 removes the assumption of benign input and identity. Course 4 removes the assumption of healthy processes and dependencies. Course 5 removes the assumption of modest demand. Course 6 removes the assumption that the producer and consumer interact at the same time.

The sequence is cumulative. “We now use events” never means “HTTP semantics no longer matter.” “We now have observability” never means “logs are authoritative state.” “We now have a cache” never means “authorization can be omitted from the key.” The final skill is the ability to hold all six layers in one design without confusing their owners or evidence.
