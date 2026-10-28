---
module_id: DE-024
program: Data Engineering
level: 1
module_number: 24
title: API-Based Ingestion
status: complete
last_verified: 2026-09-02
---

# API-Based Ingestion

## One-Page Review

### Governing question

How can an ingestion system retrieve every intended API record within a declared scope, despite pagination, mutation, throttling, retries, expiring credentials, and ambiguous failures, while preserving enough evidence to replay and reconcile the result?

### Essential definitions

- An **extraction contract** identifies the API operation, version, authorization scope, query, ordering, pagination, consistency, deletion, error, and retention semantics on which ingestion relies.
- A **request scope** is the normalized endpoint, operation, tenant/principal, filter, order, fields, version, time bounds, and snapshot context held invariant through one traversal.
- A **page token** or **cursor** is provider-issued continuation state; it is not a record watermark or authorization grant unless the contract explicitly says so.
- A **source identity** is the stable resource/event identifier plus source version or event position needed to distinguish legitimate revisions from duplicate delivery.
- An **overlap window** deliberately rereads a bounded interval so late or equal-timestamp changes can be deduplicated instead of skipped.
- A **raw response envelope** preserves request identity, retrieval time, response metadata, body digest, records, and provenance before interpretation.
- A **checkpoint** records only source progress whose raw evidence and required downstream effects are durable.
- **Reconciliation** compares an independently derived source scope, key set, count, digest, or aggregate with the ingested result at a compatible cut.

### Central model, mechanism, or theorem

Let normalized request scope be $Q$, the first request use continuation $c_0=\bot$, and successful page $i$ return records $P_i$ plus provider continuation $c_i$. A traversal follows

$$
(Q,c_{i-1})\rightarrow(P_i,c_i)
$$

without changing the scope-bound parts of $Q$, and terminates only on the provider's documented end condition. The raw batch is the deduplicated union

$$
B=\operatorname{dedupe}\left(\bigcup_{i=1}^{n}P_i,\;K\right),
$$

where $K$ is a source-defined identity/version key. This proves traversal of the observed page chain, not source completeness, unless the API also supplies stable snapshot and closure guarantees.

For checkpoint $C$ and durable source progress $D$, safety requires $C\preceq D$. The system may lag and replay, but it must not advertise progress beyond recoverable evidence.

### Critical invariants

- The exact operation, API/media version, fields, filters, order, tenant, principal, time bounds, and snapshot context stay fixed throughout a page chain.
- Continuation is followed as returned and remains opaque; the client neither invents a next page nor treats cursor contents as authority.
- Ordering is total and stable enough for the advertised traversal, or the API provides an explicit snapshot/export resource.
- Responses are admitted only after status, media type, size, schema, identity, scope, and semantic controls pass.
- Retries are bounded by deadline and attempt budget, limited to safe/idempotent requests or a proven idempotency contract, and honor provider pacing signals.
- Credentials are least-privilege, audience-restricted, short-lived where practical, secret from URLs/logs/raw bodies, and independently rotatable.
- Raw pages and a batch manifest/receipt become durable before page or extraction progress advances.
- Duplicate pages and records produce one governed effect; conflicting bytes or versions under one identity fail closed.
- Incremental queries include tie-breakers or overlap, propagate deletes, and never equate fetch time with source change time.
- Reconciliation and controlled backfill remain available because a successful HTTP traversal alone cannot prove upstream completeness.

### Common failures

Reading only the first page; assuming page size is fixed; synthesizing page numbers instead of following continuation; changing filters midway; offset paging a mutating collection; checkpointing a cursor before durable landing; using `updated_at > last_time` without ties or overlap; deduplicating only by current resource ID and losing revisions; treating `200` as schema or semantic validity; retrying every error; retry storms at reset time; ignoring `Retry-After`; logging bearer tokens; putting credentials in query strings; following arbitrary redirects; trusting an OpenAPI document as runtime proof; silently accepting unknown enum meanings; interpreting `304` as a new empty dataset; and declaring completeness without a snapshot, high bound, or reconciliation.

### Compact example

An API exposes an immutable export snapshot with two cursor pages. The second page repeats event 102 and ends with no continuation. The extractor keeps the query and snapshot ID fixed, honors an initial `429` delay, validates each response, deduplicates on `(event_id, version)`, writes three raw events plus a manifest, and only then commits the terminal cursor. A crash before publication leaves the prior checkpoint intact; replay reaches the same raw identities without a second downstream effect.

### Connections

[DE-021](021-full-and-incremental-extraction.md) chooses full versus incremental capture, [DE-022](022-watermarks-and-high-water-marks.md) defines safe progress, and [DE-023](023-file-arrival-and-manifest-processing.md) supplies manifest publication. API pagination and quota semantics are developed in [API-017](../../28-api-and-service-engineering/modules/017-filtering-sorting-and-pagination.md) and [API-039](../../28-api-and-service-engineering/modules/039-rate-limits-and-quotas.md); the [Data Engineering roadmap](../ROADMAP.md) continues with snapshot and change-data-capture sources.

## Governing Question

What evidence permits an API extractor to claim that one precise source interval or snapshot was retrieved, durably recorded, and made replayable when HTTP success is page-local and the collection can change between requests?

An API is a governed remote computation, not a table exposed over JSON. Its response depends on authenticated identity, authorization policy, endpoint and media version, normalized query, server clock, database state, pagination implementation, rate policy, caches, and provider deployment. Two syntactically equal requests can observe different states; two different credentials can see different universes.

Therefore API ingestion needs a protocol around the calls. It must pin what can be pinned, label what cannot, preserve the provider's continuation chain, distinguish record identity from page delivery, stage evidence before progress, and measure the gaps that transport success cannot reveal.

The desired result is not “the client received only 2xx responses.” It is “under contract version $v$, principal $p$, scope $Q$, and source cut or observation interval $T$, these response envelopes produced this immutable raw generation, these validation and deduplication decisions, this checkpoint, and these reconciliation results.”

## Why This Matters

APIs are common extraction sources because they enforce product ownership and authorization while hiding storage. That abstraction is valuable, but it removes database-level evidence. The client usually cannot open a repeatable-read transaction, inspect a write-ahead log, count hidden rows, or control the service's ordering implementation. Correctness must be negotiated through public contract and tested behavior.

Pagination turns one logical extraction into many independently failing requests. If records are inserted, deleted, or reordered between offset pages, a locally correct response sequence can omit or duplicate members. Even cursor pagination does not imply snapshot isolation unless the provider says the cursor binds a stable view.

Incremental filters create another boundary. A provider's `updated_at` can have coarse precision, late commits, backfills, clock skew, or write paths that do not update it. A client that stores the greatest observed time before durable output can permanently skip data. Overlap plus stable identity reduces that risk but increases replay and cannot recover mutations outside the field's contract.

Quotas and overload affect correctness as well as speed. An extractor that fans out pages until it receives `429`, then launches synchronized retries, may be banned or amplify a provider incident. A run that stops at a quota boundary must retain exact progress and resume the same scope safely.

Credentials expand the blast radius. Long-lived owner tokens copied into configuration, query strings, traces, exception reports, or raw archives can turn a data pipeline into an account compromise. Authentication proves a credential presentation; the extractor still needs least privilege, tenant binding, endpoint trust, object-level scope, and audited rotation.

Finally, API contracts evolve. Fields become nullable, new enum values appear, error shapes change, versions sunset, and endpoint meanings shift. A tolerant parser that silently drops meaning can be more dangerous than a visible failure. Preserve raw evidence, version the interpretation, quarantine incompatible data, and reconcile independent controls.

## Prerequisites and Retrieval

Retrieve the provider and consumer owners; data purpose and legal basis; API base URL and allowed hosts; protocol/TLS requirements; operation and method; API and media versions; schema or OpenAPI description plus known runtime differences; authentication flow; credential owner, audience, scopes, expiry, refresh, rotation, revocation, and storage; tenant/account context; filters and normalized query; time-zone and timestamp semantics; ordering and tie-breaker; pagination style, token scope, expiry, and end condition; snapshot or export semantics; maximum/default page size; response and decompression limits; record identity and version; create/update/delete representation; backfill behavior; rate and quota dimensions; concurrency rules; retryable statuses and provider error codes; `Retry-After` and reset conventions; conditional request behavior; cache and consistency semantics; webhook or event alternatives; source retention; raw landing format; checkpoint transaction; downstream merge; reconciliation endpoints or counts; privacy/classification; observability; support/escalation; recovery objectives; and deprecation notices.

Distinguish API host from a response-supplied URL; TLS peer identity from application authorization; token scope from returned record scope; API version from schema version; request time from source commit time; page number from continuation; cursor from durable watermark; response `200` from valid media/schema/content; empty page from terminal page; missing field from explicit null; resource identity from version/event identity; duplicate delivery from repeated business state; ordering from snapshot consistency; `429` from general `503` overload; server delay advice from a reservation; conditional `304` from an empty collection; raw archival from credential/header archival; and traversal completion from source completeness.

Before implementation, write a contract matrix:

| Concern | Evidence to record |
|---|---|
| Interface | Provider, operation, base host, API/media/schema version, deprecation horizon |
| Visibility | Credential identity, tenant/account, scopes/audience, filters and exclusions |
| Traversal | Order, page limit, continuation field/link, token expiry, snapshot/live semantics |
| Change | Source timestamp/version/event position, low/high bounds, ties, deletes, late data |
| Reliability | Timeout, deadline, attempts, retry classes, pacing, concurrency, quota ownership |
| Validation | Status, content type, byte/decompression bounds, schema and semantic invariants |
| Evidence | Request fingerprint, response time/ID/validators/digest, raw object and batch manifest |
| Progress | Prior/next checkpoint, durable receipt, downstream commit, replay and repair procedure |
| Assurance | Independent counts/keys/aggregates, drift thresholds, incident and provider escalation |

## Learning Objectives

After completing this module, you should be able to:

1. translate an API's public behavior into an explicit extraction contract;
2. keep scope invariant while traversing provider-issued pagination;
3. distinguish live traversal, fixed high-water extraction, and stable snapshot export;
4. design timestamp/version overlap with stable identity and delete propagation;
5. classify HTTP, provider, schema, and semantic failures for bounded recovery;
6. coordinate rate limits, deadlines, backoff, jitter, and concurrency without retry amplification;
7. secure credentials, endpoints, redirects, logs, and raw response evidence;
8. validate and preserve response envelopes before advancing checkpoints;
9. make page and batch replay idempotent by effect; and
10. reconcile API-derived data without overstating what finite observations prove.

## Core Exposition

### Treat the API as a source contract

Begin with the provider's supported operation, not an observed browser request or internal endpoint. Record the base URL, method, version selection, media type, parameters, pagination, errors, rate policy, authentication, deprecation, and support owner. Pin generated clients and schemas to a reviewed artifact; a floating “latest” contract makes reprocessing non-reproducible.

Machine-readable descriptions help enumerate paths, parameters, response schemas, and security schemes. The [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) defines those description structures, but an OpenAPI document does not prove server authorization, pagination stability, historical completeness, rate behavior, or runtime conformance. Contract tests and production reconciliation remain necessary.

Document provider-specific behavior rather than projecting one API's conventions onto another. `next`, `next_page_token`, `Link: rel="next"`, `since`, page number, scroll ID, and asynchronous export job can all mean different things.

### Define one normalized request scope

Represent a traversal scope as

$$
Q=(H,O,V,P,F,S,L,A,T),
$$

where $H$ is allowed host and operation, $O$ is the HTTP operation/method, $V$ is interface/media version, $P$ is principal/tenant visibility, $F$ is normalized filter/fields, $S$ is sort, $L$ is page-size policy, $A$ is source interval or snapshot, and $T$ is other stable options.

Canonicalize only according to the provider contract. Reordering repeated parameters, changing omitted defaults into explicit values, or normalizing timestamps may change meaning. Store a request fingerprint over the stable contract fields without secrets.

Subsequent pages may change only continuation and provider-permitted controls such as a reduced page size. Google [AIP-158](https://google.aip.dev/158) is one approved API-design profile: it expects other request arguments to remain the same across page tokens and says tokens are opaque continuation rather than authorization. Treat this as an example profile, not a universal protocol.

### Choose an extraction mode explicitly

A small bounded endpoint may support a complete full traversal. A large resource collection may require incremental queries. An asynchronous export API may create a server-side immutable snapshot and later return manifest/files. A webhook can lower discovery latency while periodic API reads repair missed events.

Name steady-state and repair modes separately. Incremental polling might be the daily path while a snapshot export supplies bootstrap and drift repair. If the provider offers neither history nor a consistent full snapshot, state the assurance limit instead of inventing completeness.

Estimate request count before choosing a mode. For expected visible records $N$ and effective page size $L>0$, the lower-bound page count for a static collection is

$$
n=\left\lceil\frac{N}{L}\right\rceil.
$$

This estimate omits retries, empty intermediate pages, server caps, live growth, nested endpoints, and per-record expansion. Use observed distributions and quota headroom for scheduling, not the formula alone.

### Authenticate with a workload identity

Prefer a provider-supported machine/workload identity owned by the integration, not a person's token. Request only needed read scopes, resources, tenant, and audience. Separate production and nonproduction credentials and source accounts. Keep acquisition/refresh in a secret-aware component; deliver tokens in authorization headers, never query strings.

The current OAuth security BCP, [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html), recommends restricting access-token privilege and audience and discusses sender-constrained tokens. Apply the actual provider profile: OAuth terminology alone does not make a token correctly scoped.

Use short-lived access where practical and protect refresh/private-key material more strongly. Rotate without losing checkpoint identity. A credential change must not silently expand or shrink the visible universe inside one traversal; restart or create a new explicitly scoped generation when visibility changes.

Redact authorization, cookies, API keys, signed query parameters, refresh tokens, and sensitive error details from logs, metrics, traces, raw envelopes, exception dumps, and support bundles. Hashing a low-entropy secret is not safe redaction.

### Constrain network destinations

Allowlist scheme, exact host, port, path family, and resolver/egress policy. Verify TLS and do not disable hostname or certificate validation to “fix” ingestion. Protect DNS and proxy configuration according to the deployment threat model.

Treat provider-supplied pagination and redirect URLs as untrusted inputs. Resolve relative Web Links using the applicable URI rules, then require the resulting destination to remain within the allowed origin and operation policy. Never forward credentials to an arbitrary redirected host. Reject credentials embedded in URLs.

Bound redirect count, response bytes, decompressed bytes, header count/size, nesting, records, strings, and time. A trusted provider can still return malformed or unexpectedly huge content because of bugs or compromise.

### Pin version and representation

Send the required API-version and `Accept` headers explicitly. Record the selected response version/media type. Validate `Content-Type` before parsing and treat HTML login/error pages returned with an unexpected status or proxy-generated `200` as failures.

Schema identity is broader than a JSON shape. Record field meanings, absence/null/default behavior, numeric range and precision, time format/time zone, identifier case, enum extensibility, ordering, and delete semantics. Preserve unknown fields in raw evidence even if the current projection ignores them.

When a provider announces deprecation or sunset, inventory extraction runs, replay readers, raw historical versions, generated clients, and rollback. Test the replacement against contract and data invariants before switching. A new endpoint returning equal counts is not evidence of equal records.

### Prefer a stable source cut

The strongest API extraction exposes an immutable export/snapshot ID or a query high bound whose semantics cover all writes. Pin that cut in $Q$ and carry it through every page. Record expiry and complete the traversal within its retention.

If the API offers `updated_at <= h`, select $h$ from provider time or a documented source position, not blindly from the client clock. Verify whether rows can be committed later with earlier timestamps and whether every mutation path updates the field.

A fixed high timestamp bounds growth but does not create snapshot isolation. Rows can change membership or sort keys under the same bound during traversal. Label the result as a bounded live observation unless the provider promises a stable view.

### Traverse pagination as a state machine

Model states `ready`, `requesting`, `received`, `validated`, `landed`, `page-committed`, `terminal`, `paused`, and `failed`. Persist request/page identity and transition evidence so recovery can decide whether to retry, replay landed data, or resume.

Start with the documented initial request. Follow the returned continuation field or typed `next` link exactly after validating destination and scope. RFC 8288 [Web Linking](https://www.rfc-editor.org/rfc/rfc8288.html) defines typed links and Link header serialization; it does not give every API snapshot semantics.

Do not guess that `page + 1` exists, parse an opaque cursor, or stop merely because a page contains fewer rows than requested. Some APIs cap page size, return zero rows with continuation, filter results after internal pagination, or omit last-page links. Use the documented terminal condition.

Detect cursor cycles, repeated page digests with new cursors, excessive page count, scope mismatch, and impossible transitions. These are protocol failures or provider incidents, not invitations to skip forward.

### Understand offset, keyset, and cursor risks

Offset/page-number traversal is adequate for a stable snapshot or small collection where drift is acceptable. In a live ordered collection, insertion before an offset can duplicate a prior record; deletion can shift a record behind the next offset and omit it.

Keyset pagination using a total order such as `(updated_at,id)` avoids offset shifting around the boundary, but mutable sort keys and non-snapshot membership can still create duplicates or misses. Include a stable unique tie-breaker. Do not substitute a client-generated predicate for a provider cursor unless the public contract defines that predicate.

Opaque cursor pagination can bind internal snapshot and order, or merely encode offset. The client cannot infer which. Record the provider's stated semantics, token expiry, and allowed recovery. If a cursor expires halfway, restarting from the beginning into the same dedupe domain is safer than inventing an internal offset; for very large exports, use a provider snapshot facility.

GitHub's [pagination documentation](https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api) illustrates a concrete provider contract in which clients follow `Link` response headers and endpoint-specific `per_page` behavior. It is evidence for GitHub, not a template whose exact limits apply elsewhere.

### Make incremental windows replayable

Let committed source watermark be $w$, chosen next high bound be $h$, and safety overlap be $\epsilon\ge0$. Query the documented interval

$$
[w-\epsilon,h]
$$

or its precise inclusive/exclusive equivalent. The next watermark becomes $h$ only after every page in the interval is validated, raw-published, and covered by the receipt. Overlap trades extra reads for protection against ties, bounded lateness, and ambiguous prior completion.

Choose $\epsilon$ from evidence: timestamp precision, maximum known commit/reporting delay, clock behavior, observed late arrivals, provider guarantees, and repair objective. There is no universal “five-minute overlap.” Mutations arriving later than $\epsilon$ remain vulnerable, so reconciliation or a source event stream is still required.

Deduplicate by stable mutation identity when supplied, such as event ID or `(resource_id,version)`. Deduplicating only by resource ID collapses legitimate versions. If only current resource state is available, use source version for monotonic upsert and preserve every raw observation; admit that intermediate changes may be unrecoverable.

### Handle equal timestamps and total order

Second-resolution timestamp filters frequently contain many rows at one value. A predicate `updated_at > w` after consuming part of the tie loses the rest. Complete all pages through a fixed bound before storing the bound, or use a documented lexicographic cursor `(updated_at,id)`.

Define timestamp parsing, offset, precision, leap-second behavior, and inclusive boundaries. Preserve the provider string plus normalized representation. Client truncation can turn distinct source positions into one apparent time.

Never use maximum time observed in a partial page as the interval commit. A later page may contain another row at the same time, and a failed page may be necessary for the cut to be complete.

### Propagate deletions and restricted visibility

Current-state list endpoints often cannot distinguish a hard-deleted resource from a permission/filter change or failed traversal. Use an explicit deletion/tombstone event feed, versioned snapshot replacement, or authoritative key-set reconciliation according to the contract.

Soft-delete fields work only if every deletion sets them and the integration can retrieve them. Provider retention may expire tombstones. Record the last version and deletion identity, then apply deletes idempotently without resurrecting a newer state from delayed pages.

Authorization changes can make records disappear. Do not automatically translate disappearance into business deletion. Record principal/scope revision, classify the visibility event, and require source evidence before destructive propagation.

### Validate the response envelope

Classify the response before parsing records:

1. Verify status and provider machine-readable error code.
2. Verify allowed content type, encoding, compression, and size bounds.
3. Parse with bounded depth/number/string/collection limits and reject duplicate keys where ambiguity matters.
4. Validate envelope schema: records, continuation, snapshot/cut, request ID, warnings, and count fields.
5. Validate every record's identity, version, tenant/scope, field types, units, timestamps, and domain invariants.
6. Validate page relationships: fixed scope, order, cursor transition, unique identities, and high bound.
7. Preserve rejected raw evidence securely and quarantine without advancing progress.

A `200 OK` means the HTTP request succeeded according to the origin/intermediary semantics. It cannot by itself prove a complete result or valid application payload. Some providers return an error object with `200`; handle that only through explicit provider contract, not a permissive heuristic.

Empty data needs its own validation. An empty terminal snapshot may be valid; an empty page with a continuation may also be valid for some APIs. A missing `data` member, `null`, truncated body, or cached authorization error is not interchangeable with either.

### Preserve raw response evidence

Land each accepted response in an immutable run/page object before projection. Include provider, endpoint/operation, normalized nonsecret request fingerprint, credential identity reference (not token), tenant/scope, API/media/schema version, source bounds/snapshot, request and response times, status, safe headers, provider request ID, continuation digest/reference, body length/digest, retrieval attempt lineage, and extractor version.

Store the exact body when permitted, or a governed canonical envelope plus digest when policy forbids it. Raw archives can contain personal data and secrets echoed by a defective provider; apply encryption, access control, retention, deletion, and scanning.

After all pages validate, publish a DE-023-style batch manifest listing their immutable identities and totals. Downstream jobs consume the manifest, not an in-progress run directory.

### Coordinate checkpoints with durable publication

Let $D$ be the greatest source interval or terminal snapshot whose raw manifest is durable and validated, and $C$ the advertised extraction checkpoint. The core invariant is

$$
C\preceq D.
$$

Write the raw page before recording page continuation. Prefer one transactional record that links run/scope, prior checkpoint, next checkpoint, manifest identity, receipt, status, lease/fence, and software version. If storage systems cannot share a transaction, use immutable manifests plus conditional/fenced checkpoint updates and reconciliation.

A crash after fetch but before landing refetches. A crash after landing but before page receipt replays the page. A crash after full raw manifest but before checkpoint discovers the manifest and conditionally completes the receipt. These cases duplicate delivery, not effect.

Never advance on a quarantined record merely to keep the pipeline green unless an explicit partial-success contract defines the skipped scope, compensation, repair, and downstream meaning. “Last successful row” inside a failed page is rarely a safe provider cursor.

### Make duplicates harmless

HTTP GET is safe in the protocol sense, but retrieving a page twice still creates duplicate client-side deliveries. The sink needs idempotence over source identity:

$$
apply(k,v,apply(k,v,S))=apply(k,v,S).
$$

Use unique constraints or conditional writes on event/page identity and source-version-aware merges. Store a request/page digest to distinguish exact replay from conflicting content under the same source identity.

Do not infer duplicates from equal payload alone. Two legitimate events can have equal fields. Conversely, one resource ID can have several ordered versions. Select the key from source semantics.

### Budget retries end to end

[RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) defines safe and idempotent method semantics and explains why a client can automatically retry an idempotent request after certain communication failures. Still bound retries by one end-to-end deadline, maximum attempts, response/body replayability, and provider policy.

Retry classified transient conditions: selected connection failures, timeouts with safe operation semantics, `429`, and selected `5xx` codes when the provider contract permits. Do not retry malformed credentials, forbidden scope, unknown API version, invalid query, expired cursor requiring restart, incompatible schema, or semantic corruption as though waiting will repair them.

Use exponential backoff with randomized jitter and a cap. Respect a valid provider `Retry-After` as a minimum policy delay within the run deadline. Persist a pause rather than holding a worker indefinitely. Avoid retry multiplication across client library, workflow engine, proxy, and task runner; assign one owner and count every attempt.

Ambiguous response loss is safe for GET only if the provider honors safe GET semantics and the client effect is deduplicated. Some nominal GET endpoints trigger exports or mutate read markers; document and treat actual semantics.

### Respect rate limits, quotas, and concurrency

[RFC 6585](https://www.rfc-editor.org/rfc/rfc6585.html) defines `429 Too Many Requests` and permits `Retry-After`, while leaving counting identity and mechanism unspecified. Provider-specific headers and bodies decide the operational details.

Throttle proactively from a shared provider/account budget. Limit concurrent requests, pages, endpoints, and tenants; cap response bytes and in-flight memory. Reserve headroom for urgent or reconciliation work. A higher concurrency can reduce wall time while increasing throttling, cost, page drift, and provider load.

GitHub's current [REST API rate-limit documentation](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api) is a useful concrete example: it describes primary and secondary limits, provider headers, `403` or `429`, and delay guidance. Do not hard-code those semantics for a different provider.

Treat reset time as advice, not capacity reservation. Add jitter so all workers do not resume simultaneously. If the extraction cannot finish before snapshot/cursor expiry under sustainable quota, reduce scope, schedule an export, obtain an approved allocation, or negotiate a stronger source interface; aggressive retries cannot solve an infeasible budget.

### Use conditional requests carefully

ETag/`If-None-Match` or modification validators can avoid downloading unchanged representations when the endpoint supports them. Persist the validator with the exact normalized scope, authorization context, version, and cached raw representation.

`304 Not Modified` means reuse the selected cached representation under HTTP conditional semantics; it is not a new empty body. If the cached object is missing, corrupt, outside retention, or came from different authorization/version scope, a `304` cannot complete ingestion.

Validators on a collection page do not generally prove later pages or the entire source are unchanged. Likewise, a validator for current state is not a mutation watermark. Use conditional requests for bandwidth and quota optimization only within their stated contract.

### Separate transport and domain errors

Maintain a taxonomy with stable recovery ownership:

- network/TLS/DNS/proxy failures;
- HTTP authentication/authorization, throttling, client, and server statuses;
- provider machine-readable error codes;
- pagination/snapshot/cursor protocol violations;
- envelope/media/schema incompatibility;
- record-level identity/domain invariant failures;
- raw storage/checkpoint/downstream publication failures; and
- reconciliation drift or source-assurance failures.

Record safe status, error type/code, request ID, attempt, delay, and state transition. Do not record secrets or uncontrolled bodies in high-cardinality metrics. Quarantine deterministic data failures; retry bounded transient failures; pause on quota; escalate contract or permission failures; restart a generation only through explicit policy.

### Reconcile independently

Transport logs show calls, not missing source records. Obtain an independent source control where possible: snapshot-scoped count, key inventory, event-position range, page-independent aggregate, export manifest, or provider audit report.

Compare at compatible scope and cut. A live count at 12:05 cannot validate a traversal spanning 12:00–12:30. Pin snapshot IDs or account for documented mutation. Compare exact key/version sets before counts alone; missing and extra records can cancel.

Schedule reconciliation independently of the incremental loop so the same bug does not produce both data and proof. Repair into a new raw generation, preserve the drift evidence, and apply supersession rather than silently rewriting accepted history.

Finite reconciliation gives evidence for covered identities/fields at one cut. It cannot prove the provider never hid a record, timestamps were always correct, or future executions will be complete.

### Operate for contract evolution

Monitor request and record rates, pages per run, duplicate/version conflict rate, response sizes, latency, retries by class, `429`/`5xx`, quota remaining/reset, cursor age/expiry, source-to-ingest lag, empty results, schema/enum drift, raw/checkpoint commits, quarantine age, reconciliation drift, credential expiry/rotation, and deprecation headers/notices.

Alert on invariant threats rather than every retry: checkpoint without manifest, repeated cursor, changing snapshot ID, missing tie-breaker, conflict under one source version, sustained lag versus retention, permission-scope change, and reconciliation mismatch.

Test provider sandbox behavior, but do not assume it matches production scale, data, quotas, or deployment. Use recorded synthetic fixtures without secrets for deterministic parsing and page-state tests; use limited live probes for contract conformance and operational budgets.

Write runbooks for revoked/expired credentials, provider outage, throttle storms, cursor expiry, schema change, partial traversal, corrupt raw page, checkpoint conflict, deletion-feed gap, and reconciliation drift. Recovery must state whether to resume, replay, restart from overlap, create a new snapshot generation, or escalate to the provider.

## Definitions and Notation

Let:

- $Q$ be the normalized nonsecret request scope;
- $p$ be the authenticated principal/tenant visibility context;
- $v$ be the pinned API/media/schema contract version;
- $c_i$ be the provider continuation used after page $i$;
- $P_i$ be the record multiset returned by page $i$;
- $K(r)$ be the stable identity/version key for record or event $r$;
- $w$ be the prior committed source watermark;
- $h$ be the chosen high bound or terminal source position;
- $\epsilon$ be the deliberate overlap duration/position;
- $M$ be the immutable raw batch manifest;
- $D$ be durable validated source progress represented by raw evidence;
- $C$ be the advertised extraction checkpoint; and
- $S$ be downstream state.

The page transition is

$$
(Q,c_{i-1})\rightarrow(P_i,c_i).
$$

The observed batch is

$$
B=\operatorname{dedupe}\left(\bigcup_{i=1}^{n}P_i,K\right).
$$

For interval polling, a representative next read is $[w-\epsilon,h]$ with inclusivity defined by contract. Replay safety is

$$
apply(B,apply(B,S))=apply(B,S),
$$

and checkpoint safety is

$$
C\preceq D.
$$

Define “terminal” from the provider contract: absent next link, null/empty token, explicit completion state, or completed export manifest. A short or empty page is terminal only if the contract says so.

Define “complete” with a qualifier: complete traversal of observed page chain; complete as-of stable snapshot; complete through event position; or empirically reconciled for a named key/field scope. Never leave the qualifier implicit.

## Mechanisms, Invariants, or Proof Structure

**Scope-invariance condition.** For a single chain, all $Q_i$ must equal canonical $Q$ except the documented continuation component. Changing tenant, filter, order, fields, version, or cut creates a different traversal.

**Continuation-chain invariant.** Request $i+1$ uses exactly the validated continuation derived from response $i$. Persisted edges form one acyclic chain ending only in the documented terminal state.

**Snapshot-completeness theorem, conditional.** If the provider contract guarantees that one snapshot fixes authorized membership and total order; each page partitions the remaining members without omission; continuation is valid for the extraction duration; the client follows every validated edge under unchanged $Q$; and all pages validate, then the union contains every member of that snapshot. Without those assumptions, the conclusion is only observed-chain completion.

**Proof sketch.** The initial page covers the first partition by provider guarantee. Assume pages through $i$ cover the first $i$ disjoint partitions. The guaranteed continuation identifies the next remaining partition, so page $i+1$ extends coverage without omission. Induction reaches the terminal edge, after which no partition remains. Client validation cannot create the provider guarantee; it merely preserves its premises.

**Checkpoint-safety invariant.** $C\preceq D$ ensures recovery never begins after evidence known to be durable. If $C\prec D$, recovery may replay; stable identities make replay harmless. If $C\succ D$, a crash can lose the advertised interval permanently.

**Overlap coverage condition.** If every source mutation becomes query-visible no later than delay $\delta$, timestamps/order are correct, $\epsilon\ge\delta$, and each interval is later reconciled/deduplicated, overlap prevents lateness within that bound from falling between consecutive reads. It says nothing about delay greater than $\epsilon$ or writes that never update the queried field.

**Identity idempotence invariant.** A repeated page or record with the same $K(r)$ and digest/version yields the prior receipt/effect. The same key with conflicting bytes is an integrity/contract failure; a newer source version is a legitimate new mutation under source ordering.

**Retry-budget invariant.** Every library, proxy, workflow, and worker attempt consumes one shared deadline/attempt/quota budget. No layer independently resets the budget or retries a non-idempotent operation without a proven protection.

**Credential invariant.** Every request uses an approved principal, audience, scope, environment, and allowed destination; no raw artifact, URL, log, trace, metric, error, or support record contains reusable credential material.

**Validation-before-publication invariant.** Status, media, size, parse, schema, identity, scope, order, cursor, and batch controls pass before manifest publication; failures quarantine and leave source progress unchanged.

**Deletion monotonicity.** A tombstone/source version can remove state only if it is newer than the stored version; a delayed older record cannot resurrect it.

**Reconciliation boundary.** Equality of snapshot-scoped exact key/version sets and covered payload digests is strong empirical evidence for those fields at that cut. Count equality alone and comparisons across moving cuts are weaker and cannot establish hidden source truth.

<!-- bijux-verify: {"id":"api-page-chain-replay","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"requests=3\nraw_records=3\nduplicate_records=1\nretry_after_honored=True\nterminal_cursor=done\nreplay_idempotent=True\nfailed_run_checkpoint_unchanged=True\nsnapshot_complete=True\n","stderr":""}} -->
```python
responses = {
    None: [
        {"status": 429, "retry_after": 2},
        {
            "status": 200,
            "snapshot": "export-7",
            "records": ((101, 1, "a"), (102, 1, "b")),
            "next": "page-2",
        },
    ],
    "page-2": [
        {
            "status": 200,
            "snapshot": "export-7",
            "records": ((102, 1, "b"), (103, 1, "c")),
            "next": None,
        }
    ],
}

def extract(checkpoint, publish=True):
    cursor = checkpoint
    raw = {}
    requests = 0
    duplicates = 0
    waited = []
    offsets = {key: 0 for key in responses}
    while True:
        reply = responses[cursor][offsets[cursor]]
        offsets[cursor] += 1
        requests += 1
        if reply["status"] == 429:
            waited.append(reply["retry_after"])
            continue
        assert reply["status"] == 200
        assert reply["snapshot"] == "export-7"
        for event_id, version, value in reply["records"]:
            key = (event_id, version)
            if key in raw:
                assert raw[key] == value
                duplicates += 1
            raw[key] = value
        cursor = reply["next"]
        if cursor is None:
            break
    manifest = tuple(sorted(raw.items())) if publish else None
    next_checkpoint = "done" if manifest is not None else checkpoint
    return requests, raw, duplicates, waited, next_checkpoint, manifest

requests, raw, duplicates, waited, checkpoint, manifest = extract(None)
_, replayed, _, _, replay_checkpoint, replay_manifest = extract(None)
_, _, _, _, failed_checkpoint, failed_manifest = extract(None, publish=False)

print(f"requests={requests}")
print(f"raw_records={len(raw)}")
print(f"duplicate_records={duplicates}")
print(f"retry_after_honored={waited == [2]}")
print(f"terminal_cursor={checkpoint}")
print(f"replay_idempotent={manifest == replay_manifest and checkpoint == replay_checkpoint}")
print(f"failed_run_checkpoint_unchanged={failed_manifest is None and failed_checkpoint is None}")
print(f"snapshot_complete={set(raw) == {(101, 1), (102, 1), (103, 1)}}")
```

The execution demonstrates one finite synthetic snapshot, one throttle response, one duplicate event, and an in-memory publication decision. It does not prove provider snapshot isolation, durable storage, real waiting, credential security, schema compatibility, or production transactionality.

## Alternatives and Trade-Offs

**Direct API polling versus provider export.** Polling offers low latency and selective fields but spends quota and may traverse live state. Export can provide a stable large cut and manifest but adds job latency and lifecycle handling.

**Polling versus webhooks/events.** Polling is pull-controlled and repairs missed notifications but discovers slowly and rereads. Webhooks reduce latency but duplicate, reorder, expire, and need endpoint security. Combine event discovery with periodic authoritative reads/reconciliation.

**Full traversal versus incremental filter.** Full traversal reduces watermark assumptions and repairs drift, but cost grows with all state. Incremental reads scale with change volume but depend on complete version/time/delete semantics.

**Offset versus provider cursor.** Offset is inspectable and can jump, but drifts on mutable collections and may become expensive. Provider cursor can preserve internal context but is opaque, scope-bound, and may expire.

**Live keyset versus immutable snapshot.** Keyset gives efficient monotonic boundaries but not stable membership under mutable sort keys. Snapshot gives reproducibility at provider resource and retention cost.

**No overlap versus overlap.** Non-overlapping intervals reduce reads but make boundary/lateness defects permanent. Overlap catches bounded lateness with duplicate cost; stable identities and reconciliation are mandatory.

**Sequential versus concurrent pages.** Sequential requests naturally preserve cursor dependencies and lower provider pressure. Concurrent partition endpoints improve throughput only when scopes are independently complete and budgeted; guessing future cursors breaks protocol.

**Generated client versus small explicit adapter.** Generated clients accelerate schema coverage but can hide retry/default/pagination choices and change with generator versions. An explicit adapter exposes policy but needs maintenance. Pin and wrap either behind extraction invariants.

**Strict schema stop versus tolerant projection.** Strict failure prevents silent semantic corruption but can halt on harmless additions. Preserve raw, allow known additive fields under compatibility policy, quarantine unknown required meaning, and version projections.

**Raw bodies versus normalized envelopes.** Exact bodies maximize replay/audit but may retain secrets or personal data and provider-specific noise. Governed normalization reduces risk/volume but can discard future meaning. Choose by legal, security, and recovery requirements.

**Conditional requests versus unconditional reads.** Validators reduce bytes and sometimes quota but require retained matching cache state and exact scope. Unconditional reads are simpler and stronger for raw evidence at higher cost.

**Provider rate headers versus local shaping.** Headers reveal provider-specific current state but may be absent or approximate. Local shared pacing protects budgets proactively but must track account-wide consumers and provider changes. Use both under explicit semantics.

**Checkpoint per page versus per extraction.** Page checkpoints reduce refetch after long runs but expose partial-generation state and cursor expiry complexity. Whole-extraction commit is simpler and atomic but may replay many pages. Preserve immutable pages either way and publish only complete scope.

**Current-state upsert versus event ledger.** Upsert efficiently serves latest state but loses intermediate changes. An event ledger preserves mutation evidence if the API supplies identities/order; build current state as a derived view.

## Failure Modes and Misconceptions

- **“The endpoint is REST, so GET is always harmless.”** Actual provider semantics and side effects must match the method contract.
- **“The OpenAPI file proves the implementation.”** It is a description artifact, not runtime evidence.
- **“A valid token can read the intended tenant.”** Audience, scope, subject, resource, and tenant still need binding.
- **“Put the token in the URL for simplicity.”** URLs leak through histories, proxies, logs, and referrers.
- **“TLS means any redirect is safe.”** A valid attacker host can receive forwarded credentials.
- **“A 2xx response is valid data.”** Media, schema, scope, and semantic validation remain.
- **“An empty array means the source is empty.”** It can be a filtered page, lost permission, wrong tenant, or provider defect.
- **“One page is the full collection.”** Most list operations are bounded.
- **“Fewer than requested means last page.”** Server caps and filtered pagination can violate that assumption.
- **“Increment page numbers until empty.”** Continuation/end behavior is provider-owned.
- **“Cursor is just encoded offset.”** Its format and semantics are opaque.
- **“Cursor grants access to the next page.”** Authorization is re-evaluated independently.
- **“A cursor always freezes the collection.”** Only an explicit snapshot contract does.
- **“Offset is deterministic with sort.”** Concurrent mutation still shifts positions.
- **“Order by timestamp is total.”** Ties need a stable unique key.
- **“Maximum observed timestamp is safe progress.”** Partial traversal and equal timestamps can remain.
- **“Client time is source time.”** Clocks and commit visibility differ.
- **“A fixed overlap guarantees all late data.”** It covers only delays within its proven bound.
- **“Deduplicate by resource ID.”** Legitimate versions can be lost.
- **“Equal payload means duplicate event.”** Separate events may carry equal values.
- **“Missing from list means deleted.”** Visibility, filter, and traversal failures also cause absence.
- **“Retry every exception.”** Deterministic auth/query/schema failures do not heal with delay.
- **“The SDK owns retries, so the workflow can retry too.”** Layered attempts multiply load.
- **“Reset time reserves a request.”** Many clients compete after reset.
- **“More concurrency always finishes faster.”** It can trigger throttling and reduce goodput.
- **“304 is an empty successful page.”** It instructs reuse of a cached representation.
- **“Collection ETag is a change watermark.”** It may not cover record history or all pages.
- **“Store the next cursor immediately.”** A crash can skip an uncommitted page.
- **“Skip one malformed record and advance.”** The skipped scope becomes silent loss.
- **“Raw means safe to retain forever.”** Raw responses inherit privacy, secrets, and deletion duties.
- **“Counts match, so migration is equal.”** Missing and extra identities can cancel.
- **“No alerts means complete.”** The same ingestion bug may also suppress its own metrics.
- **“Sandbox success proves production behavior.”** Data, quotas, scale, and releases differ.
- **“Provider uptime proves source correctness.”** Availability and semantic completeness are separate.

## Worked Examples

### Example 1

An orders endpoint returns 100 records by default, but the tenant has 14,320. The client persists only the first response because it assumed the requested `limit=5000` would be honored.

The corrected adapter reads the documented effective limit and follows each provider continuation until the explicit terminal condition. It records actual page sizes and alerts when their distribution changes. **Conclusion:** requested size is not completion evidence.

### Example 2

A client reads page 1 at offset 0. A new newest-first record arrives before page 2; the prior last record shifts into offset 100 and appears again, while another boundary member later disappears after a deletion.

For exact exports, the team switches to an immutable provider export snapshot. For low-latency approximate browsing data, it uses keyset pagination and documents live drift. **Conclusion:** locally correct offset pages do not compose into a stable live snapshot.

### Example 3

An incremental customer run finishes part of the rows at timestamp 12:00:00 and stores `12:00:00`. Another customer with the same second remained on a failed page. The next query uses `updated_at > 12:00:00` and loses it.

The extractor chooses high bound 12:05, exhausts every cursor for an inclusive overlap interval, deduplicates on `(customer_id,version)`, publishes one manifest, then commits 12:05. **Conclusion:** interval completion, not page maximum, controls progress.

### Example 4

The first request returns `429` with a two-minute `Retry-After`. Two hundred workers each retry every second because their library ignores the header; the provider extends the restriction.

A shared account limiter pauses new attempts, persists the resume time, adds jitter after the minimum delay, caps attempts by deadline, and reduces concurrency. **Conclusion:** throttle handling is coordinated flow control, not a tight error loop.

### Example 5

An OAuth access token is stored in the raw request URL, copied into object names, and emitted in trace attributes. Storage is encrypted, but thousands of analysts can list those paths.

The integration moves tokens to authorization headers, uses an audience-restricted workload identity and read-only scopes, redacts at HTTP boundaries, rotates the leaked credential, audits access, and scans historical artifacts. **Conclusion:** encrypted storage does not repair secret propagation.

### Example 6

A pagination `next` URL unexpectedly points from `api.vendor.example` to `collect.attacker.example`. A generic HTTP client follows it and forwards the bearer token.

The adapter resolves the link, rejects any scheme/host/port/path outside the allowlist, never forwards credentials across origin without an explicit reviewed rule, and raises a provider security incident. **Conclusion:** continuation is untrusted routing input.

### Example 7

Page four is fetched and its cursor checkpointed, but object storage fails before the response is landed. A restart begins at page five and permanently skips page four.

The corrected workflow writes immutable page four, validates its digest, updates a page receipt conditionally, and advances only then. If the receipt write fails, replay deduplicates by page and event identities. **Conclusion:** lag is recoverable; progress ahead of durability is not.

### Example 8

An endpoint adds enum value `REVIEWING`. The parser maps unknown values to `FAILED`, and the downstream system closes valid cases.

Raw envelopes preserve the new value, schema monitoring trips, records quarantine without interval progress, and owners deploy an explicit unknown-compatible model before replay. **Conclusion:** permissive parsing can create destructive semantics.

### Example 9

An hourly list no longer contains account 42. The pipeline emits a deletion, but investigation shows the integration's permission scope was reduced during credential rotation.

The system restores the approved principal, starts a new scope generation, and reconciles exact keys. Deletion propagation requires a tombstone/version feed rather than list absence. **Conclusion:** visibility loss is not source deletion.

### Example 10

An extractor completes all cursor pages and counts 9,999 records. The provider's snapshot manifest declares 10,000 and identifies a missing key range caused by an internal shard timeout that still returned `200`.

The run remains unpublished, records provider request IDs, and is replayed after the provider resolves the defect. **Conclusion:** independent reconciliation can detect semantically incomplete successful traversals.

## Cross-Program Connections

- [Database Engineering](../../18-database-engineering/ROADMAP.md): source snapshots, indexes, versions, transaction time, and deletion history determine what an API can promise.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md): authoritative ownership, contracts, lineage, privacy, and reconciliation define the extraction boundary.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md): batching, partitioning, backpressure, throughput, and replay shape high-volume API capture.
- [Operating Systems](../../22-operating-systems/ROADMAP.md): clocks, sockets, files, process failure, and durable writes underlie timeout and checkpoint behavior.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): workload identity, secret management, SSRF defenses, egress, least privilege, and retention constrain the client.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): partial failure, idempotence, retries, leases, and consistency explain why page-local success is insufficient.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md): method, pagination, error, authorization, quota, compatibility, and deprecation semantics form the provider contract.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): connector runtimes, credential delivery, shared limiters, observability, and repair workflows make the protocol operable.

## References

1. IETF, [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html). Defines method safety/idempotence, selected representations, conditional requests, status semantics, and `Retry-After`.
2. IETF, [RFC 6585: Additional HTTP Status Codes](https://www.rfc-editor.org/rfc/rfc6585.html). Defines `429 Too Many Requests` and its optional `Retry-After` guidance without prescribing the provider's counting policy.
3. IETF, [RFC 9700: Best Current Practice for OAuth 2.0 Security](https://www.rfc-editor.org/rfc/rfc9700.html). Updates OAuth security guidance, including access-token privilege and audience restriction and sender-constrained tokens.
4. Google, [AIP-158: Pagination](https://google.aip.dev/158). Documents one approved opaque page-token contract, stable request arguments, page-size behavior, and the separation of continuation from authorization.
5. IETF, [RFC 8288: Web Linking](https://www.rfc-editor.org/rfc/rfc8288.html). Defines typed links and Link header serialization used by some APIs for pagination.
6. OpenAPI Initiative, [OpenAPI Specification](https://spec.openapis.org/oas/latest.html). Defines machine-readable API descriptions, operations, parameters, responses, schemas, and security scheme structures.
7. GitHub, [Using Pagination in the REST API](https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api). Documents GitHub-specific Link-header traversal and effective per-page behavior.
8. GitHub, [Rate Limits for the REST API](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api). Documents GitHub-specific primary/secondary limits, headers, response codes, and retry timing advice.

## Exercises

### Exercise 1

Design a complete extraction contract for a vendor invoices API that exposes OAuth, `updated_since`, cursor pagination, 15-minute timestamp precision, mutable current resources, a deletion endpoint retained for 30 days, and 1,000 requests per hour. State assumptions, identities, bounds, retry policy, raw evidence, checkpoint, and reconciliation.

### Exercise 2

A live newest-first endpoint contains keys `A,B,C,D` with page size two. Page one returns `A,B`; then `X` is inserted before `A` and `B` is deleted before page two at offset two. Show a possible duplicate/omission result. Compare offset, keyset, and snapshot guarantees.

### Exercise 3

Place crash points in an extractor that fetches three cursor pages, writes immutable raw pages, publishes a batch manifest, merges current state, and commits a checkpoint. For each point, specify restart behavior and the identity that prevents duplicate effect.

### Exercise 4

An API returns `429 Retry-After: 120` after 40 pages. The cursor expires in ten minutes, 80 pages remain, sustainable throughput after delay is ten pages per minute, and four other jobs share the account quota. Decide whether retrying can complete safely and design an operational response.

### Exercise 5

A migration from API version 1 to version 2 produces equal counts and no HTTP errors. Version 2 changes absent `discount` to numeric zero, adds enum `REVIEWING`, changes pagination, and uses a new credential with broader tenant scope. Design evidence that can accept or reject equivalence without exposing secrets or personal data.

## Answers to the Exercises

### Answer 1

Pin provider/base host, invoice list and deletion operations, API/media/schema version, workload credential identity, audience, read-only invoice/deletion scopes, tenant, fields, ordering, cursor rules, timestamp inclusivity, error/rate behavior, and support owner. Never archive tokens or permit cross-host continuation.

Use a provider-time high bound $h$ and query an inclusive overlap beginning at least one 15-minute precision bucket before committed $w$, enlarged by measured reporting delay. Exhaust every cursor with unchanged scope; validate invoice ID plus source version, currency/amount, tenant, timestamps, and next transition. Deduplicate `(invoice_id,version)` while preserving raw observations. Poll the deletion feed by stable tombstone ID/position within its retention; alert when lag threatens 30 days and reconcile current keys before that horizon.

Shape all jobs below the shared 1,000/hour quota with reserved repair headroom, bounded concurrency, deadline, jittered backoff, and documented `429` handling. Land immutable response envelopes and a manifest before conditionally committing $h$ and deletion position. Periodically obtain a snapshot-scoped invoice count/key inventory or provider export and compare exact key/version sets plus monetary control totals. State that overlap covers only bounded lateness and current-resource polling cannot reconstruct intermediate versions the API never exposes.

### Answer 2

Initially offsets are `[A,B]` then `[C,D]`. After insertion and deletion, the live order can be `[X,A,C,D]`; offset two returns `[C,D]`. In that schedule the traversal yields `A,B,C,D` and omits newly inserted `X`, which may be acceptable only under a declared live cutoff. In another schedule where insertion occurs but deletion does not, offset two returns `[B,C]`, duplicating `B` and omitting `D` if the client stops after two pages based on an old count.

Keyset after stable key `B` avoids positional shift for items that stay ordered relative to that boundary, but it can still omit a newly inserted `X` before the boundary and is vulnerable when sort keys mutate. It provides no historical deletion evidence by itself. A provider-guaranteed immutable snapshot fixes authorized membership and order; following every continuation can prove coverage under that contract. If exact export is required, use the snapshot and record its ID/expiry rather than calling live keyset “complete.”

### Answer 3

Crash before any response: retry page one under the same run/scope. After fetch but before raw write: refetch; provider page/cursor plus response digest identifies replay. During raw write: the object remains unpublished or fails checksum and is rewritten under an immutable attempt identity. After page write but before page receipt: discover/validate the object and conditionally establish the receipt, or refetch and deduplicate by page/request plus record source identities.

After all pages but before manifest: reconstruct only from validated page receipts and publish one manifest. After manifest but before merge: consume the same manifest. During/after merge before checkpoint: replay merge using `(resource_id,version)` or event IDs and a manifest receipt. After checkpoint: verify it references the durable manifest/downstream receipt and begin the next interval. Cursor progress never exceeds the durable page chain, and interval progress never exceeds the complete manifest.

### Answer 4

After the mandated two-minute wait, only eight minutes remain. At ten pages per minute, the theoretical capacity is 80 pages with no further delay, retries, shared-job traffic, or jitter. Because four jobs share quota and the bound has zero safety margin, safe completion before cursor expiry is not credible.

Pause competing jobs if policy permits, preserve run/cursor and provider request IDs, and determine whether the snapshot/cursor expiry can be extended or an asynchronous export can replace traversal. If not, let the run fail explicitly and restart from a new snapshot/initial request into the same stable deduplication domain, without advancing the checkpoint. Reduce scope into independently complete provider-supported partitions only if their union and cut are specified. Obtain quota increase through provider process rather than violating `Retry-After`; add feasibility admission so future runs reject before starting when sustainable quota cannot meet retention.

### Answer 5

Treat version, missing/null/default, enum, pagination, and authorization scope as separate compatibility dimensions. Capture nonsecret normalized request scopes and exact contract artifacts. Run v1 and v2 at the same provider snapshot/high bound and intended tenant principal, writing separate immutable raw generations. Reject the broader v2 credential or constrain it to the same tenant universe before comparison.

Compare exact `(resource_id,version)` sets, not counts; classify missing and extra keys. On shared keys, compare canonical field presence separately from value so absent and zero cannot collapse. Preserve and enumerate unknown enum values such as `REVIEWING`; define a non-destructive projection before acceptance. Validate that every v2 continuation under fixed scope covers the same snapshot and inject page-boundary mutation/cursor-expiry tests. Compare deletion identities, monetary aggregates, selected payload digests, errors, rate behavior, and source-to-ingest lag.

Store only protected identifiers/digests or approved synthetic fixtures in reports, never credentials or unnecessary personal fields. Equal covered key/version sets and semantic projections at compatible cuts provide bounded migration evidence; they do not prove future provider behavior, so canary, drift monitoring, rollback, and deprecation-horizon observation remain.
