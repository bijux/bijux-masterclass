---
module_id: API-085
program: API & Service Engineering
level: 2
module_number: 85
title: Consumer Inventory and Usage Evidence
status: complete
last_verified: 2026-09-02
---

# Consumer Inventory and Usage Evidence

## One-Page Review

### Governing question

Which accountable applications, workloads, partners, humans, jobs, relays, and recovery paths depend on each API contract element, what do they actually use, how confident and fresh is that evidence, and how can it be collected without confusing credentials/traces with consumers or violating privacy and security?

### Essential definitions

- A **consumer** is an accountable logical application/workflow that relies on an API outcome; it is not automatically one credential, IP, process, trace, tenant, or end user.
- A **consumer identity graph** links organization/team/owner, application, deployment/workload, credentials/principals, SDK/client artifact, tenant/use case, and downstream relays.
- **registration evidence** describes declared ownership and intended capability; **observation evidence** describes measured calls/effects; **attestation evidence** is an accountable confirmation.
- **usage evidence** records operation, contract element, version, outcome/effect, cadence, and boundaries needed for a decision—not arbitrary payloads.
- A **blind spot** is a known way consumers or use can be missing/misattributed: shared credentials, gateways, sampling, retention, offline work, header stripping, or uninstrumented paths.
- A **dormant consumer** is legitimate low-frequency/contingency use absent from ordinary windows.
- **evidence provenance** records source, collection method, time range, transformations, sampling, retention, and confidence.
- An **unknown consumer** produces evidence that cannot yet be mapped to an accountable owner/use case.

### Central model, mechanism, or theorem

Let declared registrations be $R$, authenticated principals $A$, observed traffic identities $T$, code/contract dependencies $D$, and partner/support attestations $P$. The candidate inventory is a reconciled graph over

$$
I=R\cup A\cup T\cup D\cup P,
$$

not the count of any one set. Every node/edge carries provenance, time range, and confidence. Absence in sampled telemetry is weak evidence: with independent sampling probability $p$ and $n$ calls, probability of observing zero is $(1-p)^n$. At $p=0.01,n=10$, it is about $90.44\%$.

### Critical invariants

Every production consumer maps to an accountable owner and use case or is tracked as unknown risk. Credential/principal proves authentication context, not logical consumer count; OAuth client identifiers are identifiers, not authentication secrets. Trace context correlates work, not identity. IP/User-Agent are supporting hints, not authority.

Inventory separates logical operations, transport attempts/retries, effects, users, tenants, and workloads. Evidence retains provenance, sampling, blind spots, freshness, and legal purpose. Collection is minimized, access-controlled, retained only as needed, and never logs secrets/tokens/raw sensitive payloads. Retirement requires cross-source reconciliation, dormant/recovery coverage, direct ownership confirmation where risk demands, and observed replacement outcomes—not traffic percentage alone.

### Common failures

Counting API keys as consumers; shared gateway hides hundreds of clients; rotated credentials look like churn; one app's replicas inflate count; trace IDs treated as caller identity; IP/NAT/User-Agent attribution; retries counted as demand; sampling misses rare jobs; 30-day window misses quarterly/yearly/disaster use; success-only logs hide blocked dependencies; route logs cannot prove field/enum/error use; payload logging violates privacy; registration/contact stale; team renamed or dissolved; “unknown” dropped from dashboards; partner/offline/mobile/replay paths absent; telemetry pipeline outage interpreted as zero use; one high-volume client hides many low-volume critical ones; and owner says migrated while old principal still produces effects.

### Compact example

A gateway principal generates 70% of requests. Counting principals says one consumer; gateway registration reveals 300 downstream applications, and only 240 forward a trusted application identifier. The inventory keeps the gateway as a relay, maps the 240, creates unknown-risk records for the other 60, and uses direct attestation/contract repositories to reconcile them. **Conclusion:** identity is a provenance graph, not a distinct-count query.

### Connections

[Preventing Failure Amplification](080-preventing-failure-amplification-across-service-calls.md) separates logical operations from attempts. [Backward and Forward Compatibility](081-backward-and-forward-compatibility.md) defines the supported population, and [Deprecation and Sunset](084-deprecation-and-sunset.md) consumes inventory evidence. Later governance, contract testing, and observability modules operationalize this graph.

## Governing Question

What minimum, privacy-safe, cross-source evidence establishes who depends on an API, which exact semantics they use, how often and critically they use them, whether they migrated, and what remains unknown before a change or retirement decision?

## Why This Matters

API providers routinely know request volume but not consumers. A key may serve many workloads; one workload may rotate keys; a partner gateway may represent hundreds of applications; a mobile client ID may cover millions of installations. IP addresses shift behind NAT/proxies, User-Agent is spoofable or stripped, and trace IDs identify a request graph rather than the accountable caller.

Usage is multidimensional. An application may call an endpoint but never read the field being removed. Another may depend on one rare error code or run only during disaster recovery. A quarterly financial job can be absent from a 90-day dashboard. Retries can inflate transport calls while unique business effects fall.

Evidence collection itself has risk. Raw URLs, headers, tokens, identities, payloads, query values, and user agents can contain secrets or personal data. High-cardinality labels can make telemetry costly and expose more people. Inventory therefore needs purpose limitation, minimization, access control, retention, and auditable joins.

A defensible inventory combines declared registration, authenticated context, runtime observation, code/contracts, data lineage, partner/support records, and direct attestation. It makes uncertainty visible. This enables compatibility decisions, capacity planning, incident outreach, deprecation, security response, cost attribution, and product ownership without pretending any single log is the truth.

## Prerequisites and Retrieval

Retrieve [Tracing a Request Through Client, Proxy, and Service](010-tracing-a-request-through-client-proxy-and-service.md), [API Contracts and Behavioral Guarantees](021-api-contracts-and-behavioral-guarantees.md), [Authentication Context Propagation](033-authentication-context-propagation.md), [Credential and Token Handling](042-credential-and-token-handling.md), [Preventing Failure Amplification](080-preventing-failure-amplification-across-service-calls.md), [Backward and Forward Compatibility](081-backward-and-forward-compatibility.md), and [Deprecation and Sunset](084-deprecation-and-sunset.md).

Retrieve API/client registrations and contacts; OAuth client IDs, API-key metadata, mTLS/workload identities and credential rotation history; gateway/proxy/service logs and traces; low-cardinality route/version/error/effect metrics; SDK/client metadata; catalog/CMDB/code search/dependency graphs; partner/support/contracts; webhook/subscription and scheduler registries; mobile/offline/replay/failover/recovery paths; billing/quota records; telemetry sampling/drop/retention; privacy/legal basis; ownership directories; and known unknown/unattributed traffic.

## Learning Objectives

After completing this module, you can:

1. distinguish consumer, application, deployment, workload, credential, principal, tenant, user, trace, attempt, and effect;
2. model consumer identity as a temporal provenance graph instead of one identifier;
3. reconcile registration, authentication, telemetry, code, contract, lineage, partner, and attestation sources;
4. measure operation/version/field/error/effect use without unnecessary payload capture;
5. account for retries, sampling, dropped telemetry, shared relays, credential rotation, and high cardinality;
6. discover dormant, periodic, offline, webhook, replay, failover, and disaster consumers;
7. record evidence provenance, freshness, confidence, conflicts, and blind spots;
8. apply data minimization, access, retention, deletion, and security controls to inventory evidence;
9. verify per-consumer migration through target behavior and effects rather than declarations alone; and
10. use inventory for compatibility, deprecation, incident, capacity, security, and ownership decisions.

## Core Exposition

### Define the consumer decision unit

Choose the unit that must act on a change: usually an application/workflow plus accountable owner and deployment population. “Checkout mobile app,” “partner settlement integration,” “nightly fraud export,” and “regional failover controller” are consumers. A human end user or tenant may be a segmentation dimension without being the migration owner.

Separate software product from deployed instance. One commercial client software may have thousands of customer deployments with different versions and owners. RFC 7591 distinguishes client software, client instance, client developer, deployment organization, and API deployment—useful evidence that one `client_id` granularity is a policy choice.

Separate logical operation from transport attempt and domain effect. Retries/redirects/hedges can produce multiple requests for one intent; idempotency can produce one effect. Inventory needs both offered load and unique dependency/effect use.

Define inclusion rules and examples. Otherwise teams count credentials, pods, users, or traces inconsistently and trend changes become meaningless.

### Build a temporal identity graph

Model nodes: organization/partner, team/owner/contact, application/workflow, environment/deployment, workload/service/job/device population, credential/principal/client registration, SDK/client artifact/version, tenant/use case, relay/gateway, and external agreement. Model directed typed edges such as owns, deploys, authenticates-as, calls-through, uses-version, performs-use-case, replaced-by, and rotated-to.

Edges have valid-from/to times and provenance. Credential `key-7` may rotate to `key-9` for the same application; a service transfers between teams; a gateway starts forwarding trusted downstream identity; an SDK release rolls gradually. Without temporal edges, inventory falsely creates/deletes consumers.

Use stable internal inventory identifiers independent of credentials or display names. Keep aliases/history and merge/split events auditable. Never merge solely on IP or similar heuristic.

Represent unknown nodes explicitly. “Unknown behind gateway G” is an inventory object with volume/surface/risk and investigation owner, not discarded noise.

### Understand identity evidence and trust

Authenticated workload/client principal is strong evidence about the credential holder under the authentication system, but may still be shared. RFC 6749 says an OAuth client identifier represents registration information, is not secret, and must not be used alone for client authentication. Pair it with verified token/mTLS context and registration metadata.

Client-supplied application IDs, versions, User-Agent, and custom headers are useful only under a trust model. Public callers can spoof them. A gateway can overwrite a trusted internal identifier after authenticating/mapping downstream clients; origins reject direct untrusted copies.

W3C Trace Context propagates trace correlation. It is not authorization or durable consumer identity, and privacy considerations include cross-request correlation. Join trace/effect evidence to authenticated inventory context server-side rather than encode personal identity in `traceparent`/`tracestate`.

IP/network peer can locate an immediate connection or NAT/proxy, not a logical consumer. Use network signals for corroboration/anomaly, never sole ownership.

### Make registration a product control

Require each production client/workload/subscription to register owner/team, support/escalation contacts, application/use case, environment, criticality, expected operations/versions/volume/cadence, data/security classification, SDK/runtime, credentials/principals, downstream relay status, disaster/batch use, and lifecycle dates.

Validate ownership/contact automatically against directories and require periodic attestation. Registration changes when ownership transfers, credentials rotate, applications split/merge, or support ends. Stale records are risks with explicit state.

RFC 7591 defines client metadata including names, URIs, scopes, contacts, and distinctions around registration. It does not make an OAuth registration a complete API consumer inventory; enrich it with API-specific accountability under local policy.

Gate new credentials/subscriptions through registration where feasible. Legacy discovery remains necessary; never assume unregistered means unauthorized or nonexistent without investigating.

### Collect observation evidence at the right grain

Record time bucket, API/operation route template, requested/resolved version, authenticated principal, trusted consumer/deployment ID if available, SDK/client artifact, environment/region, result/status/stable error, latency/size/cost, logical operation/effect ID where safe, retry/attempt classification, and deprecation/default/capability path.

Use route templates rather than raw paths to avoid resource IDs/high cardinality. Do not label metrics by unbounded user/tenant/request identifiers; keep controlled secure logs or warehouse joins for investigations. OpenTelemetry HTTP conventions distinguish route, request method, status, resend count, addresses, and user agent, and warn that capturing arbitrary headers risks sensitive leakage.

Count success and failure. Rejected old-version calls, auth failures after credential expiry, or validation errors can prove dependence. Separate synthetic/health/test traffic.

Create explicit completeness metrics for instrumentation: expected versus ingested events, drop/sampling rate, parser/header loss, unknown route/identity, clock lag, and pipeline outages.

### Observe fields and semantics without payload hoarding

Endpoint calls do not reveal which response fields clients read. Server cannot generally observe client-side field access for ordinary REST responses. Use explicit partial-response masks/GraphQL selections, consumer contract tests, code search/SDK instrumentation with consent, or direct attestation. Do not claim field-level evidence from full response logs.

For request fields, instrument a curated Boolean/enum-presence decision at validation/mapping time rather than store raw values. For response variants/errors, record stable type codes emitted to each authenticated consumer; whether the client handled them safely still needs tests/attestation.

GraphQL operation/field selection is observable from validated documents; persist normalized operation identifiers/field aggregates under privacy/cost policy rather than raw variables. Persisted query registries provide strong declared evidence but can miss ad hoc documents.

For webhooks/events, subscription filters, schema registry, delivery/acknowledgment, consumer group/offset, and effect/deduplication evidence reveal different facets. Delivery is not proof of correct consumption.

### Reconcile independent sources

Start with union $I=R\cup A\cup T\cup D\cup P$: registrations, authentication/principals, traffic, declared code/contracts, and partner/support/attestation. Add scheduler, webhook, lineage, billing/quota, network, and recovery catalogs as needed.

Normalize identifiers with source-scoped namespaces; never assume equal strings across identity providers/environments. Join using authoritative mappings, time validity, and reviewed heuristics. Retain source records and confidence rather than overwrite conflicts.

Examples of conflict: registered but never observed; observed principal has no registration; code declares operation but no traffic; owner attests migrated while deprecated version still appears; traffic disappears without replacement effect; one principal maps to several applications. Each generates an investigation state.

Publish reconciliation coverage/unknowns and last successful source refresh. A pretty inventory built from a stale failed pipeline is worse than visible uncertainty.

### Measure usage as distributions and sets

Per consumer, measure logical operations and attempts, success/failure/error types, unique effects, route/version/media/capability, field presence/selection, volume and cost distribution, concurrency, response size, latency/deadline, regions/environments, first/last seen, days/weeks active, and cadence/seasonality.

Request share and consumer share answer different questions. One client can create 99% of requests while 100 low-volume clients each carry distinct migration obligations. Segment criticality/business effect as well.

Use exact counts where low-cardinality and privacy-safe; use sketches/sampling where volume requires, but attach error/sampling semantics. Do not use sampled “zero” as exact absence.

Compare replacement uptake to old-path decline and business/effect parity. A drop in old traffic without target success can be outage, lost observability, or abandoned functionality.

### Account for sampling and telemetry loss

If each call is independently sampled with probability $p$, a consumer making $n$ calls has probability $(1-p)^n$ of being completely missed. At 1% sampling and ten calls, $0.99^{10}\approx0.9044$: over 90% miss probability. Independence can also fail, making this model optimistic or pessimistic.

Head sampling can miss errors/rare consumers; tail sampling may preserve errors but depends on completed traces; aggregation can erase identity; retention can delete a full seasonal cycle. Maintain an unsampled privacy-safe low-cardinality access counter or registration/attestation path for retirement-critical evidence when feasible.

Track dropped spans/logs, exporter/backpressure, ingestion lag, sampling policy/version, schema changes, and clock/timezone. Evidence provenance includes these limitations.

Use negative evidence only after validating collection health and combining independent sources across an adequate horizon.

### Find dormant and contingency consumers

Inventory expected cadence and next execution: hourly, month-end, quarter-end, annual tax, certificate renewal, disaster test, cache rebuild, regional failover, backup restore, replay/redrive, or manual incident tool. Observation windows cover at least one governed cycle or the path is explicitly exercised/attested.

Schedulers/workflow definitions, runbooks, IaC, DR plans, queue retention, replay catalogs, and code dependency search reveal sleepers. Direct owner confirmation includes a test result, not “probably unused.”

Synthetic exercises can prove the replacement path but must be labeled and cannot prove the real production credential/data/config works unless rehearsal is representative.

Dormant does not mean low criticality. Contingency consumers often have zero steady traffic and maximal incident impact.

### Decompose shared relays and credentials

Gateways, integration platforms, service accounts, API keys, NAT, and message consumer groups aggregate callers. Model the relay as a node and require downstream attribution when trustworthy. Possible mechanisms include gateway registration mapping, signed/overwritten application context, per-client credentials, contract repository, subscription metadata, or owner attestation.

Do not forward an end-user or arbitrary public `X-Consumer-Id` as trusted. The authenticating relay maps it, strips the external field, and emits protected internal context. Authorization still evaluates the real subject/tenant/resource.

When decomposition is impossible, record the shared population as one high-uncertainty risk with owner and downstream count/coverage. Retirement cannot declare every downstream migrated because the gateway's own calls moved.

Credential rotation creates old/new principals for one consumer; overlap is expected. Link rotation and retire stale credentials after cutover rather than double-count.

### Establish accountable ownership and attestation

Every logical consumer has primary technical owner, business/service owner, escalation, and organization. Contacts are roles/groups with individuals where needed, not one employee email. Validate they exist and acknowledge responsibility.

Attestation asks concrete questions: exact operations/versions/fields/errors; use case/effects; production and dormant paths; SDK/deployment; replacement test/deploy evidence; next expected run; downstream consumers; and retirement consent/exception. Timestamp, signer, evidence, scope, and expiry.

Attestation is evidence, not truth overriding telemetry. If an owner declares migration but old authenticated effects continue, investigate credential sharing, stale deployment, retries, or false scope. Conversely, traffic may be synthetic or replay and not a live consumer.

Unknown/stale ownership has escalation and risk acceptance. Do not assign the API provider as permanent owner of every mystery client.

### Record evidence confidence and freshness

For each claim store source, collection/query/version, time range, sampling/drop, join/transformation, scope, collector owner, generated time, expiry/freshness, confidence rationale, and contradicting evidence. Make raw-to-derived lineage reproducible.

Use qualitative evidence states—confirmed, corroborated, inferred, unknown, contradicted—rather than average numeric scores that hide a fatal gap. A verified principal-to-app mapping plus recent target effect is stronger than User-Agent similarity.

Freshness depends on decision and cadence. A 60-day-old attestation may be adequate for stable partner ownership but not a daily deployment version. Define per-field/service-level refresh.

Maintain snapshots/history so migration and incidents can reconstruct what was believed at decision time. Correct records rather than rewrite evidence invisibly.

### Protect privacy and security

Define purpose and lawful/organizational basis. GDPR Article 5 includes data minimization and storage limitation principles; apply equivalent local obligations where relevant. Collect only attributes required for ownership, compatibility, operations, or security decisions.

Never log access/refresh tokens, secrets, full Authorization/cookies, raw request/response bodies by default, sensitive query values, or unnecessary user identifiers. Hash/pseudonymize stable technical identifiers with rotation/access controls where joins require. Remember hashes of stable identifiers can remain personal/linkable data.

Use access controls, tenant separation, encryption, audit, retention/deletion, export restrictions, incident response, and safe dashboards. High-cardinality inventory is an attractive map of systems/owners.

OpenTelemetry warns arbitrary HTTP header capture can leak sensitive information; allowlist and redact at collection, not after broad replication. W3C Trace Context also has correlation/privacy considerations.

### Turn inventory into operating controls

Onboarding checks registration/owner/contacts/criticality/cadence and issues scoped credentials. Runtime flags unregistered or mapping-conflicted traffic. Periodic jobs reattest, rotate credentials, and update versions. Ownership transfer and offboarding are workflows.

Compatibility review queries affected consumers by operation/version/field/error/SDK/state. Incidents identify owners and blast radius quickly. Capacity planning segments logical demand/cost rather than attempts. Security response finds affected credentials/artifacts and contact paths.

Deprecation creates per-consumer migration work, tracks notices and replacement evidence, and blocks retirement on unknown/dormant/recovery gaps. The inventory is therefore a maintained product/control plane, not an annual spreadsheet.

Measure inventory quality: owned/mapped registrations, unattributed traffic/effects, stale contacts, shared identities without decomposition, source refresh health, expected versus observed cadences, and resolved contradictions.

### Prove migration and retirement evidence

For each required consumer, confirm new contract artifact/config, successful representative tests, deployed environments/regions, replacement logical operations/effects, old-path cessation after retry/queue horizon, state/idempotency continuity, and owner attestation. Record exception or intentional consumer retirement.

Require old-traffic zero/within explained terminal noise across a horizon appropriate to cadence, with healthy telemetry. Include failed calls, gateway downstreams, webhooks/events, offline versions, replay, DR, backups, and support/manual tools.

Reconcile business outcomes: orders, settlements, notifications, projections—not only HTTP counts. A consumer can stop calling because it broke.

Retirement decision lists unresolved unknowns/blind spots and explicit risk acceptance. “No evidence of use” becomes defensible only after a documented search; it never becomes proof of nonexistence in an open world.

## Definitions and Notation

Let $R$ be declared registrations, $A$ authenticated principals, $T$ observed traffic identities, $D$ code/contract dependencies, and $P$ partner/support/attestation records. Candidate evidence universe is $I=R\cup A\cup T\cup D\cup P$, reconciled as a temporal graph rather than counted naively.

Let $U$ be credible required logical consumers and $M$ confirmed migrated, with $m=M/U$ only for $U>0$. Let $Q$ be transport requests, $L$ logical operations, and $E$ committed effects. Let sampling probability be $p$ and a consumer's calls be $n$; under independent sampling the zero-observation probability is $(1-p)^n$.

A **principal** is an authenticated identity; a **credential** proves/obtains authentication under policy; a **relay** intermediates several consumers; a **registration** is declared metadata; a **claim** is a derived inventory assertion; **lineage** connects claim to source/transformation; **freshness** is fitness in time for a decision.

## Mechanisms, Invariants, or Proof Structure

**Union/reconciliation argument.** Each evidence set can contain consumers absent from another: registered-but-dormant in $R$, observed-unregistered in $T$, code-only/recovery dependency in $D$, partner integration in $P$. Therefore any single set is an incomplete candidate universe; union plus identity/time reconciliation is necessary, though still not proof of all possible consumers.

**Sampling derivation.** Under independent Bernoulli sampling, each of $n$ calls is missed with probability $1-p$, so all missed is $(1-p)^n$. For $p=.01,n=10$, $0.99^{10}=0.904382\ldots$, about 90.44%. Thus sampled absence is especially weak for rare consumers.

**Credential counterexample.** One gateway credential can authenticate 300 downstream applications, while one application can rotate through two credentials. Hence the mapping between credentials and consumers is many-to-many; distinct credential count is neither an upper nor lower reliable consumer count.

**Traffic-share counterexample.** One migrated consumer can generate 99% of calls while 100 unmigrated low-volume consumers generate 1%. Therefore request-weighted migration cannot prove consumer-complete migration.

Operational invariants are: consumer unit explicit; identity graph temporal/provenanced; authentication and correlation not conflated; logical operations/attempts/effects distinct; cross-source contradictions visible; sampling/blind spots disclosed; dormant/recovery covered; data minimized; ownership accountable; and migration verified by representative target outcomes.

## Alternatives and Trade-Offs

Per-consumer credentials improve attribution, revocation, quotas, and outreach but increase provisioning/rotation burden and do not identify downstream users automatically. Shared credentials simplify integration but create uncertainty and blast radius. Use scoped registration and relays with protected downstream attribution.

Unsampled detailed logs improve rare-event evidence but increase cost/privacy/security risk. Aggregated metrics minimize data but cannot reconstruct ownership/field use. Combine privacy-safe unsampled counters with controlled sampled traces/logs and registry/attestation.

Automatic discovery scales but can misjoin identities. Manual attestation captures context but becomes stale and optimistic. Reconcile both and escalate conflicts.

Long retention covers seasonal consumers but increases storage/privacy exposure. Short retention reduces risk but requires scheduler/code/catalog evidence and explicit rehearsals. Set attribute-specific retention from purpose/horizon.

Client instrumentation can reveal response-field use but requires consent/trust/version coverage and can be spoofed. Server-side selection (GraphQL/field masks) is stronger where protocol provides it. Otherwise contract tests/code/attestation are more honest than payload surveillance.

A centralized inventory improves consistency and lifecycle automation but becomes sensitive critical infrastructure. Federated ownership reduces central data but complicates joins. Keep a minimal central graph with source-linked domain evidence.

## Failure Modes and Misconceptions

- “One key equals one consumer.” Credentials and consumers are many-to-many.
- “OAuth client ID authenticates the client.” It is an identifier, not a secret/auth proof alone.
- “Trace ID identifies the caller.” It correlates a request graph.
- “IP/User-Agent is ownership.” Proxies, NAT, spoofing, and stripping break that inference.
- “Requests equal demand.” Retries and probes inflate attempts; effects can differ.
- “Endpoint call proves field use.” Ordinary REST servers cannot observe response-field reads.
- “No sampled events means no consumer.” Rare-use miss probability can be high.
- “Thirty days is enough.” Quarterly, annual, offline, and disaster paths sleep longer.
- “Success logs are enough.” Failed old calls still prove dependency.
- “One gateway migrated.” Its downstream population may not have.
- “Registration is truth.” Ownership and intended use become stale.
- “Attestation overrides telemetry.” Contradictions need investigation.
- “99% traffic migrated.” Many critical low-volume consumers may remain.
- “Zero old traffic proves success.” Telemetry failure or consumer outage can look identical.
- “Log all headers/payloads for certainty.” That leaks secrets/personal data and still may not prove behavior.
- “A confidence score decides.” Averages can hide a critical unknown.
- “Inventory is a deprecation spreadsheet.” It is an ongoing operational/security product.

## Worked Examples

### Example 1

One API key is mounted by 40 batch jobs owned by six teams. Credential count says one; registry/scheduler joins reveal 40 deployments and six accountable consumer groups. The key is replaced with scoped principals over time.

### Example 2

Application `billing-export` rotates principal A to B with a seven-day overlap. Temporal `rotated-to` edges keep one logical consumer while telemetry sees both. After overlap, calls from A become a security/inventory anomaly.

### Example 3

A gateway principal represents 300 downstream applications. It forwards trusted mapped IDs for 240, leaving 60 unattributed. The inventory reports 240 mapped nodes plus one 60-client unknown-risk population; it does not report one fully migrated consumer.

### Example 4

A quarterly tool makes ten calls in a window sampled at 1%. Its probability of zero observations is $0.99^{10}\approx90.44\%$. Scheduler/runbook registration and a representative exercise are required; sampled traces cannot retire it.

### Example 5

One migrated client produces 99% of calls. One hundred low-volume clients share the remaining 1%. Volume migration looks excellent while consumer migration may be only $1/101\approx0.99\%$.

### Example 6

A REST response always includes `legacyCode`; access logs show endpoint use but not whether clients read it. The provider uses consumer contract/code evidence and an opt-in field mask experiment instead of logging response bodies and claiming field-level certainty.

### Example 7

A settlement job last ran 88 days ago and is scheduled every quarter. A 30-day zero-use query would miss it. Inventory stores expected cadence/next run and blocks sunset until the replacement executes the quarterly scenario.

### Example 8

An SDK retries twice before success. Logs show three HTTP requests, one logical operation ID, and one committed effect. Capacity analysis counts attempts; migration/use-case analysis counts the logical operation/effect.

### Example 9

An owner attests “migrated,” but the old principal still creates production effects in another region. The claim becomes contradicted; deployment/credential mapping reveals a missed regional workload before retirement.

### Example 10

Inventory initially stores raw authorization headers and email addresses. A review replaces them with authenticated principal IDs and role-based contact references, allowlists telemetry attributes, encrypts/audits access, and sets separate evidence retention—preserving joins without unnecessary secrets/personal data.

## Cross-Program Connections

[Data Engineering](../../19-data-engineering/ROADMAP.md) supplies lineage, identity resolution, data quality, sampling, reconciliation, retention, and trustworthy derived evidence.

[Security Engineering](../../25-security-engineering/ROADMAP.md) governs authentication context, credentials, least privilege, privacy, audit, sensitive telemetry, and unknown-client response.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) explains retries, traces, idempotency, effects, queues, relays, partial observation, and failure/recovery paths.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects stakeholder/interface inventories, configuration baselines, evidence confidence, suppliers, dormant modes, and lifecycle decisions.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns registration/catalog workflows, identity propagation, telemetry pipelines, schema, dashboards, alerts, ownership integration, and deprecation gates.

[Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) provides dependency graphs, ownership boundaries, gateways, adapters, and application/workload decomposition.

## References

1. IETF, [RFC 6749: The OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/rfc/rfc6749.html).
2. IETF, [RFC 7591: OAuth 2.0 Dynamic Client Registration Protocol](https://www.rfc-editor.org/rfc/rfc7591.html).
3. W3C, [Trace Context](https://www.w3.org/TR/trace-context/).
4. OpenTelemetry, [Semantic Conventions for HTTP Spans](https://opentelemetry.io/docs/specs/semconv/http/http-spans/).
5. Google, [Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/).
6. European Union, [Regulation (EU) 2016/679, Article 5](https://eur-lex.europa.eu/eli/reg/2016/679/oj).
7. IETF, [RFC 9745: The Deprecation HTTP Response Header Field](https://www.rfc-editor.org/rfc/rfc9745.html).

## Exercises

### Exercise 1

Design the consumer identity graph for an API used through OAuth clients, shared gateways, mobile installations, rotating workload identities, partner keys, batch jobs, and human tenants. Define authoritative versus supporting edges.

### Exercise 2

Create a privacy-safe telemetry and evidence schema that supports version/operation/field/error/effect migration analysis under retries, sampling, proxies, and retention limits. State what is deliberately not collected.

### Exercise 3

At 0.5% independent sampling, a monthly consumer makes 20 calls. Compute the probability it is entirely missed. Design evidence sufficient to retire its old version without increasing broad sensitive logging.

### Exercise 4

Reconcile these claims: 50 registrations, 47 authenticated principals, 42 observed client IDs, 55 code dependencies, eight unknown gateway identities, and 48 owner attestations. Explain why these numbers cannot simply be summed or intersected.

### Exercise 5

Define a migration/retirement evidence package for a critical API version with quarterly finance, disaster recovery, webhooks, shared relays, offline clients, and one owner attestation contradicted by old-region effects.

## Answers to the Exercises

### Answer 1

Create stable logical consumer nodes for applications/workflows and link organizations/teams/role contacts, software product, deployments/environments, workloads/jobs/device populations, credentials/principals/client registrations, tenants/use cases, SDK artifacts, and relays. OAuth registration/principal mapping is authoritative for the registered/authenticated context but not automatically logical ownership; workload identity attestation is authoritative within its issuer; directory/catalog ownership is authoritative for teams; gateway-minted protected downstream context is authoritative only after its mapping/authentication. IP, User-Agent, trace, network, and self-declared IDs are supporting hints. Add valid-time/provenance to rotations, transfers, splits/merges, and gateway mappings. Model public mobile software separately from installations/versions where provider cannot uniquely identify devices. Unknown gateway/partner populations remain explicit risk nodes.

### Answer 2

Record bounded time bucket, route template/operation ID, requested/resolved API version, authenticated principal plus trusted mapped consumer/deployment ID, SDK artifact if trustworthy, environment/region, stable result/error, latency/size/cost buckets, logical operation/attempt/resend classification, privacy-safe effect correlation, and curated request-field presence or GraphQL/persisted selection identifiers. Record sampling/drop/pipeline/schema provenance. Join high-cardinality identity in access-controlled storage, not metric labels. Do not collect tokens/secrets/cookies, raw Authorization, unrestricted headers, raw URL/query values/resource IDs, bodies, GraphQL variables, personal emails/users, or trace-baggage identity. Use role contact references, pseudonymous technical IDs, attribute allowlists, encryption/audit, tenant controls, and purpose-specific retention/deletion.

### Answer 3

With $p=0.005$ and $n=20$, miss probability is $(1-0.005)^{20}=0.995^{20}\approx0.9046$, about 90.46%. Sampling is therefore nearly useless as absence proof for this consumer. Use scheduler/registration and accountable owner evidence, an unsampled low-cardinality authenticated-principal/route counter if lawful and feasible, code/contract dependency, and a representative monthly execution against the replacement. Confirm business effect, state/idempotency, old-path cessation across retry horizon, and telemetry health. Store no payload; retain only minimized identity/operation/outcome evidence for the required cycle.

### Answer 4

Sets overlap and use different units. One registration can map to several principals/deployments; principals rotate; one observed client ID can be shared; code dependencies can be stale, libraries, tests, or multiple repos for one consumer; one gateway can hide many consumers; attestations can cover/miss or contradict observations. Build the union of source-scoped records, then reconcile temporal graph edges using authoritative mappings and evidence provenance. Investigate registered-not-observed, observed-not-registered, dependency-not-owned, unknown gateway, attested-migrated-but-old-use, and missing sources separately. Report confirmed/corroborated/inferred/unknown/contradicted claims and source freshness; never sum 50+47+42+55+8+48 or use their intersection as the consumer count.

### Answer 5

List every logical consumer/owner/use case and identity mapping, including gateway downstream decomposition, offline version populations, webhook subscriptions/ack/effects, quarterly schedule, DR/runbooks, regions, queues/replay, and state/backups. For each, attach notice/ack, replacement contract/SDK/config, representative semantic/auth/limit tests, deployed regions, target logical operations/effects, old-path cessation after retry/queue cadence, and attestation. Execute quarter-end and DR rehearsals; reconcile webhook occurrence/effect identity and offline adoption horizon. Treat the contradicted attestation as blocked: map the old regional principal/deployment, migrate or explicitly except it, then observe target effect and no unexplained old effect. Validate telemetry/sampling/retention, replacement capacity/security, idempotency/state/rollback, terminal response, and unknown-relay population. Retirement records unresolved blind spots/risk acceptance and requires the full conjunction, not aggregate traffic.
