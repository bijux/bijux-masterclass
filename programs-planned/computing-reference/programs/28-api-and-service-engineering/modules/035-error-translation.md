---
module_id: API-035
program: API & Service Engineering
level: 1
module_number: 35
title: Error Translation
status: complete
last_verified: 2026-09-01
---

# Error Translation

## One-Page Review

### Governing question

How should a service translate parsing, identity, policy, domain, dependency, and unexpected failures into stable HTTP semantics that help legitimate clients recover without exposing internal causes or inventing retry safety?

### Essential definitions

- An **internal outcome** is a typed success or failure produced by a boundary inside the service.
- A **public problem type** is a stable machine-readable identity for one API-level failure meaning.
- **error translation** maps an owned internal outcome and request context to an HTTP status, headers, and safe representation.
- **cause preservation** retains diagnostic causal evidence inside trusted telemetry even when the public response intentionally loses detail.
- **retryability** states whether, when, and under which idempotency and deadline conditions another attempt is reasonable.
- A **safety boundary** catches an unclassified defect at the outermost request boundary, records it, and returns a generic server problem.
- **Problem Details** is the RFC 9457 data model commonly serialized as `application/problem+json`.

### Central model, mechanism, or theorem

Let $O$ be typed internal outcomes, $C$ safe request context, and $H$ public HTTP responses. Translation is a total function

$$
T:O\times C\rightarrow H.
$$

It deliberately partitions internal outcomes into public equivalence classes. Two causes may map to the same public response when distinction would leak information or would not change client recovery. Correctness requires that $T$ preserve client-actionable semantics, obey HTTP, conceal internal evidence, and provide a safe fallback for every otherwise unclassified outcome.

### Critical invariants

HTTP status describes the request at the HTTP boundary, while problem `type` describes stable API-specific meaning. Clients branch on type or documented extensions, not human `detail`. Internal exception text, stack traces, SQL constraints, hostnames, tokens, and hidden identifiers never cross the public boundary. Concealed absence and denial remain observationally aligned. The HTTP status line and Problem Details `status` agree. Retry advice includes scope and timing and never overrides method or idempotency safety. An unknown defect becomes a generic `500`, retains an opaque occurrence identifier, and preserves the cause only in protected telemetry.

### Common failures

Returning every failure as `400` or `500`; mapping exception class names directly to status codes; parsing database messages to discover business outcomes; exposing stack traces; using `200` with an error body; changing problem types with prose or localization; asking clients to parse `detail`; returning `409` for failed HTTP preconditions; confusing origin unavailability with gateway failure; treating every `503` as safe to retry; emitting `Retry-After` without a meaningful estimate; wrapping downstream bodies verbatim; generating a new correlation ID instead of preserving trusted request context; and catching errors so broadly that cancellation or process-fatal conditions are swallowed.

### Compact example

A repository reports typed `DuplicateOrderNumber`, retaining the database uniqueness violation as its private cause. The application returns domain outcome `duplicate_order`; the HTTP translator emits `409`, type `https://api.example.test/problems/duplicate-order-number`, a stable title, and safe detail. Logs bind the request and occurrence IDs to the original constraint and stack. **Conclusion:** public semantics remain stable even if persistence technology changes, while operators retain the true cause.

### Connections

[Request Parsing and Validation](032-request-parsing-and-validation.md), [Authentication Context Propagation](033-authentication-context-propagation.md), and [Authorization Checks](034-authorization-checks.md) produce earlier typed outcomes. [Request-Scoped Transaction Boundaries](../ROADMAP.md) next determines when failures occur relative to commit; later idempotency and concurrency modules refine safe retry and precondition behavior.

## Governing Question

Which outcome taxonomy, translation ownership, HTTP status, Problem Details shape, disclosure rule, retry contract, logging evidence, and compatibility policy lets an API communicate failures predictably across changing implementations and unreliable dependencies?

## Why This Matters

An API error is part of the contract, not residue from an implementation. Clients use it to decide whether to correct input, authenticate, ask for permission, refresh state, wait, retry, compensate, alert a person, or stop. Operators use the same occurrence to find a failing component and causal chain. Attackers use differences in status, body, headers, latency, and wording to enumerate hidden resources and technologies.

The two audiences need different information. A client needs stable semantics and safe recovery facts. An operator may need exception type, stack, dependency address, constraint name, request identity, and timing. Copying operator detail into a response creates disclosure risk; removing it from both response and telemetry makes incidents opaque. Translation must therefore be intentionally lossy outward and causally rich inward.

Framework exception handlers often encourage an accidental public contract based on implementation classes. A database migration then changes `UniqueViolation` into `ConditionalCheckFailed`; a new proxy changes a timeout into a vendor payload; localized messages change a client parser. Stable API outcomes break this coupling. They also force teams to distinguish “the request was invalid,” “the requested transition conflicts with current state,” “a supplied precondition was false,” and “the service cannot currently complete valid work.”

## Prerequisites and Retrieval

Retrieve HTTP method and status semantics; representation and media-type negotiation; request validation; authentication challenges; authorization concealment; domain invariants and state transitions; optimistic concurrency and conditional requests; dependency ownership; timeouts, deadlines, cancellation, and circuit breaking; idempotency; logging, tracing, and privacy; schema compatibility; and localization.

Before adding a public error, retrieve the failing operation, actor-visible facts, exact client recovery action, whether the target is concealable, whether an effect might already have committed, method idempotency, idempotency-key behavior, retry budget, status and cache semantics, existing problem registry, observability fields, retention policy, and owners of both the internal outcome and public contract.

## Learning Objectives

By the end of this module, you should be able to:

1. separate internal causes, application outcomes, and public HTTP problems;
2. construct a total, loss-aware translation pipeline with an explicit fallback;
3. select HTTP statuses by protocol semantics rather than convenience;
4. define stable RFC 9457 Problem Details and bounded extensions;
5. express retry, concealment, partial-effect, and intermediary behavior safely;
6. preserve useful causal evidence without leaking implementation detail; and
7. test error mappings, compatibility, disclosure, and failure-path observability.

## Core Exposition

### Establish three vocabularies

Keep three related but distinct vocabularies:

1. **adapter causes**, such as malformed JSON, database timeout, TLS failure, or a vendor rejection;
2. **application/domain outcomes**, such as invalid command, duplicate order number, stale version, forbidden transition, or dependency unavailable; and
3. **public problems**, such as `invalid-request`, `duplicate-order-number`, `precondition-failed`, or `temporarily-unavailable`.

An adapter owns translation from its technology into a port-level outcome. The application owns domain meaning. The HTTP adapter owns translation from owned outcome to protocol response. Do not let the HTTP handler inspect SQLSTATE, vendor strings, or stack frames. That would make transport behavior depend on a technology it does not own.

The original cause remains attached internally through exception chaining or a typed causal record. Translation changes classification; it must not erase diagnosis. Record the public problem type alongside the internal outcome category so telemetry can answer both “what did clients observe?” and “what actually failed?”

### Make translation total and explicit

A translator should cover every declared outcome and include one narrow unknown fallback. A missing mapping must not accidentally serialize an object, expose a framework page, or close the connection without evidence.

Treat the mapping as a reviewed registry rather than scattered catch blocks. For each public problem specify:

- stable type URI and title;
- normal HTTP status and required headers;
- safe detail template and allowed extensions;
- concealment and localization policy;
- client correction or retry semantics;
- logging severity and diagnostic category; and
- compatibility owner and tests.

Exhaustiveness checks are valuable when the language supports closed variants. In open exception hierarchies, convert known failures to a closed application outcome before the transport layer. The outer safety boundary handles only unexpected defects. It should not be the normal path for expected rejection.

Cancellation and process-fatal signals require special treatment. A request cancelled because the client disconnected or the server is shutting down is not automatically an application `500`, and language-level memory or runtime corruption conditions may be unsafe to catch. Follow the platform's documented fatal/cancellation model while ensuring the request terminates and telemetry remains honest.

### Select status by HTTP meaning

Status codes describe how generic HTTP components should understand the response. Problem type adds application meaning.

- `400 Bad Request` fits malformed request syntax, framing, or other request conditions that prevent processing.
- `401 Unauthorized` means valid authentication credentials are absent; include the applicable `WWW-Authenticate` challenge.
- `403 Forbidden` communicates understood but refused access. Where disclosure policy requires, RFC 9110 permits concealing a forbidden target with `404`.
- `404 Not Found` covers no current representation or deliberate concealment. `410 Gone` makes a stronger, intentionally disclosed claim that the resource is no longer available and likely permanent.
- `409 Conflict` represents conflict with current resource state that the client may be able to resolve, such as a forbidden domain transition or uniqueness collision.
- `412 Precondition Failed` is the result when a request header precondition such as `If-Match` evaluates false. Do not flatten it to `409` merely because both involve current state.
- `415 Unsupported Media Type` says the representation format is unsupported. `422 Unprocessable Content` says syntax and media type were understood but instructions could not be processed.
- `429 Too Many Requests` describes rate limiting of a requester under the server's policy.
- `500 Internal Server Error` is the safe generic origin response for an unexpected inability to fulfill the request.
- `502 Bad Gateway` and `504 Gateway Timeout` apply when a server acting as a gateway or proxy receives an invalid upstream response or misses the upstream response in time. `503 Service Unavailable` means temporary inability or overload at the responding service.

An origin service calling an internal dependency is not necessarily a public “gateway” in the semantic role visible to its client. It may own the operation and translate dependency failure to its own `503` or stable domain problem. Architecture diagrams do not determine status; the public HTTP role and contract do.

Avoid status invention. If a standard status expresses the generic condition, use it. Avoid collapsing distinct correction paths into one type. Conversely, do not create a new type merely to mirror every internal exception. Public distinction is justified only when it gives callers stable, permitted information and changes handling.

### Use Problem Details as a stable envelope

RFC 9457 defines Problem Details and obsoletes RFC 7807. JSON uses `application/problem+json`. Its standard members are:

- `type`: URI reference identifying problem semantics; consumers use it as the primary identifier;
- `status`: advisory copy of the HTTP status generated for the occurrence;
- `title`: short human-readable summary stable for the type except localization;
- `detail`: occurrence-specific human explanation focused on correction, not debugging; and
- `instance`: URI reference identifying this occurrence, possibly opaque and non-dereferenceable.

Prefer absolute type URIs under a controlled, durable namespace. If dereferenceable, they can serve human documentation, but clients must not need a network lookup to handle a response. Treat changing a type URI as changing machine identity. Deprecate and migrate it like another public enum value.

The status line is authoritative to generic HTTP software. Generate the HTTP code and body `status` from one value so they cannot diverge. An intermediary can still change the status in transit, so clients must not blindly trust contradictory layers.

`title` and `detail` are for people. Clients must not parse them, compare English strings, or depend on punctuation. Put machine-actionable data in documented typed extensions, such as bounded validation violations with `field` and `code`, or a safe `retryable` classification. Extension names and values are contract surface; govern them as rigorously as top-level fields.

### Design a problem registry

A registry prevents type proliferation and conflicting mappings. A useful entry might specify type `https://api.example.test/problems/stale-representation`; title `Stale representation`; status `412`; optional extension `currentVersion` only when the caller may observe it; recovery by fetching the current representation, reconciling, and issuing a new conditional request; and no concealment distinction after target visibility is established.

Document conditions rather than implementation triggers. “Order number already exists in the tenant” remains meaningful after a database change; “constraint orders_tenant_number_key failed” does not. Keep titles stable. Localize titles and details through representation negotiation if supported, while type and extension codes remain language-neutral.

Validation problems require bounded structure. Report only fields the caller submitted and is authorized to know, cap the number and depth of violations, use stable codes, and define ordering. A huge recursive error tree can become a reflection or resource-exhaustion vector. If validation order could reveal a concealed object, authorize or conceal before returning that detail.

### Preserve concealment across translation

Authorization can intentionally group absent, cross-tenant, and forbidden outcomes into one public `404`. Translation must preserve that equivalence. Do not attach `reason=wrong_tenant`, different type URIs, object-specific links, distinguishable cache headers, or public request diagnostics to one branch.

Internal telemetry can retain separate categories under access control. Correlation does not require disclosure: an opaque `instance` such as `/problems/occurrences/01J...` can let support find a protected record without encoding tenant, host, timestamp precision, database ID, or exception type.

Body equality alone does not prove concealment. Compare status, headers, media type, length class, caching, validation precedence, links, timing, and behavior of `HEAD`, lists, bulk results, and retries. Perfect timing equality is rarely feasible, but avoid obvious work differences that cheaply enumerate a sensitive target.

### Treat retry as a compound decision

“Retryable” is not a property of a status code alone. A safe decision depends on:

$$
R=(m,k,e,d,b,a),
$$

where $m$ is method semantics, $k$ is idempotency protection, $e$ is knowledge of whether an effect occurred, $d$ is remaining deadline, $b$ is retry budget/backoff policy, and $a$ is server advice.

A `503` after a read is often a retry candidate; a `503` after a non-idempotent create whose commit outcome is unknown may duplicate an effect. An idempotency key can make the repeated logical operation safe only if the server durably binds it to request identity and outcome. A `409` may be correctable but not repeatable unchanged. A `412` normally asks the caller to fetch/reconcile, not blindly repeat. A `429` can include `Retry-After`, but the caller still observes its deadline and budget.

`Retry-After` may be a delay in seconds or an HTTP date under HTTP semantics. Emit it only when the estimate has useful meaning. Clients add bounded exponential backoff and jitter where appropriate, honor the larger applicable delay, stop at a deadline, and avoid synchronized retry storms. A public Boolean `retryable=true` is too weak unless its exact scope is defined.

When the original effect is unknown, say so through a stable problem contract only if that fact is safe and actionable. Prefer a status resource or idempotency lookup over inviting a blind replay. The next modules develop transaction and idempotency boundaries that make this classification reliable.

### Translate dependency failures at ownership boundaries

Do not forward downstream status and body reflexively. An inventory service's `404` might mean “SKU not found” to the order service, but a payment provider's `404` might be a provider protocol defect or concealed remote object. Translate through the owned port contract.

Separate at least:

- expected remote business rejection;
- local deadline expiry before useful response;
- connection, DNS, TLS, or protocol failure;
- invalid or untrusted remote representation;
- remote overload or rate limit;
- breaker-open synthetic rejection; and
- ambiguous effect after connection loss.

Preserve the vendor status, endpoint identity, attempts, and timings privately. Publicly expose only the service's owned semantics. Do not copy remote HTML, trace IDs, headers, or JSON into the client response without an explicit, reviewed proxy contract.

### Keep causal telemetry and public data separate

Create or accept a trusted request correlation identifier at ingress under length and character limits. Create an occurrence identifier for each public problem when useful. Record their relationship with trace/span identity, internal outcome, exception cause chain, dependency, duration, retry attempts, actor/tenant pseudonymous references, public type/status, and effect state.

Log structured fields, not one concatenated exception message. Sanitize user input and prevent log injection. Never log access tokens, credentials, secret request bodies, or unrestricted personal data merely because an error occurred. Apply access, retention, and deletion policy.

Severity reflects operational impact, not HTTP class alone. Expected client validation is not a server error alert. A wave of `401`, `403`, or concealed `404` may be security-relevant through aggregation. An isolated dependency timeout can be expected degradation; exhausted error budget or ambiguous financial effects deserve escalation.

If logging fails, error handling must still avoid leaking or changing an authorization outcome. Use metrics and health evidence to detect telemetry failure, but do not return the stack to compensate.

### Handle batches and asynchronous work

For batches, define whether the HTTP response describes envelope failure or item outcomes. A syntactically invalid envelope can be one `400`; a successfully processed non-atomic batch might return a normal batch representation containing per-item success/problem objects. Do not use arbitrary multi-status patterns without defining atomicity, ordering, concealment, and retry for each item.

Item problems need caller-supplied safe references rather than hidden server IDs. Bound item count and error size. If one item is concealed, its result must not reveal whether it was absent or forbidden. An atomic batch reports no committed items when any required condition fails; a partial batch reports enough durable outcome identity to retry only unknown or failed items safely.

For accepted asynchronous work, the initial `202` means acceptance, not success. Terminal job state later carries a stable problem type and occurrence metadata. Store the internal cause and authorization-safe public outcome separately. A polling client should not have to infer permanent failure from a job that remains “running” forever.

### Test the contract and the negative space

Create table-driven tests for every declared application outcome and assert exact status, media type, required headers, type, title, extension schema, and forbidden fields. Assert unknown outcomes produce a generic `500` and that telemetry retains the cause.

Test malformed parser input, invalid fields, absent credentials and challenges, denial and concealment, stale preconditions, domain conflicts, rate limits, origin overload, every dependency failure mode, cancellation, ambiguous commit, and unexpected exceptions. Inject SQL and vendor messages containing secrets to prove they do not escape.

Contract tests verify type stability and additive extension rules. Consumer tests should branch on type/code, never `detail`. Differential tests compare concealed branches. Fault injection checks observability and partial-effect classification. Property tests can assert that response bodies contain none of a secret corpus and that body `status` always equals the generated HTTP status.

The following executable model demonstrates total translation for selected typed outcomes. It illustrates mapping and safe fallback; it does not validate an HTTP server, intermediary behavior, or production disclosure controls.

<!-- bijux-verify: {"id":"error-translation-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"malformed=400 invalid-request retry=no\nstale=412 stale-representation retry=refresh\nduplicate=409 duplicate-order-number retry=correct\nthrottled=429 rate-limited retry=after\nunavailable=503 temporarily-unavailable retry=bounded\nunknown=500 internal-error retry=no\n","stderr":""}} -->
```python
MAPPINGS = {
    "malformed": (400, "invalid-request", "no"),
    "stale": (412, "stale-representation", "refresh"),
    "duplicate": (409, "duplicate-order-number", "correct"),
    "throttled": (429, "rate-limited", "after"),
    "unavailable": (503, "temporarily-unavailable", "bounded"),
}

def translate(outcome):
    return MAPPINGS.get(outcome, (500, "internal-error", "no"))

for outcome in ["malformed", "stale", "duplicate", "throttled", "unavailable", "unknown"]:
    status, problem_type, retry = translate(outcome)
    print(f"{outcome}={status} {problem_type} retry={retry}")
```

## Definitions and Notation

Let internal outcome $o\in O$ carry a stable category and a private cause chain. Let safe request context $c\in C$ contain only facts permitted to influence public semantics. Let public response $h\in H$ contain status $s$, headers $q$, and representation $p$.

Translation $T(o,c)=h$ is **total** when every possible owned outcome has exactly one response or reaches one generic fallback. A public equivalence relation $o_1\sim_c o_2$ holds when $T(o_1,c)=T(o_2,c)$ for the observations governed by disclosure policy. Concealment intentionally requires absent and forbidden internal outcomes to be equivalent under that observation model.

A **problem registry** is the versioned set of public types, statuses, fields, recovery semantics, and owners. A **safe detail** contains only caller-observable facts needed for correction. An **occurrence identifier** identifies one failure instance without revealing its cause. **Ambiguous effect** means the service cannot establish whether an externally visible mutation committed. **Retry budget** bounds attempts, elapsed time, and load consumed by retries.

## Mechanisms, Invariants, or Proof Structure

1. Convert technology-specific failures into typed port outcomes at the owning adapter.
2. Convert domain and application rejection into stable owned outcomes.
3. Establish disclosure, concealment, effect-state, and recovery facts.
4. Select an HTTP status according to protocol role and semantics.
5. Select a registered problem type only when it adds actionable API meaning.
6. Construct title, safe detail, occurrence identity, headers, and bounded extensions.
7. Derive retry guidance from method, idempotency, effect knowledge, deadline, and budget.
8. Record the private cause chain and public result in protected telemetry.
9. Route all unclassified defects through a generic safety fallback.
10. Verify exhaustiveness, status/body agreement, non-disclosure, concealment equivalence, and compatibility.

The principal safety property is non-disclosure with recoverability: for every response, all public facts are authorized and sufficient for the documented client action, while sensitive causal evidence remains available only to trusted operations. A finite mapping test supplies evidence for registered cases, not proof that arbitrary framework failures or deployment paths cannot bypass the translator.

## Alternatives and Trade-Offs

One generic error type is simple and minimizes disclosure, but forces legitimate clients and operators to guess recovery. Many fine-grained types improve correction but expand compatibility and enumeration surface. Distinguish outcomes only when the distinction is stable, safe, and actionable.

Mapping exceptions directly in middleware is convenient for small services but couples the API to frameworks and adapters. Typed outcomes add design work and can feel repetitive, yet preserve ownership and make exhaustiveness testable. Use exceptions or result values internally according to language conventions; the important boundary is conversion to an owned closed vocabulary.

Problem Details gives a standard envelope and stable machine identity. An established domain-specific error representation may fit an existing API better. Do not migrate formats solely for fashion; preserve compatibility or negotiate explicitly. Never call a proprietary envelope RFC 9457-compatible if member semantics conflict.

Returning every validation violation helps interactive correction but increases response size and can disclose validation order. Returning the first is bounded but causes round trips. Prefer a deterministic capped list containing only authorized submitted fields.

Specific `503`, `429`, and retry advice can improve resilience, but automated clients may amplify overload. Conservative advice reduces storms but increases visible failure. Combine server estimates with client budgets, jitter, deadlines, and idempotency.

Exposing a correlation or occurrence ID accelerates support. A predictable or information-bearing value can leak topology or volume. Use opaque values, validate incoming correlation IDs, control dereferencing, and keep diagnostic records protected.

## Failure Modes and Misconceptions

- **“Exceptions are the API taxonomy.”** Implementation classes do not express stable client meaning.
- **“Every invalid request is 400.”** Unsupported media, understood but invalid content, authentication, authorization, conflict, and failed preconditions have distinct semantics.
- **“409 and 412 are interchangeable.”** `412` specifically reports a false request-header precondition.
- **“Problem type is a message.”** It is a stable machine identity, normally a URI.
- **“Clients can parse detail.”** Detail is human-readable and may vary or localize.
- **“Status in the JSON is authoritative.”** Generic HTTP software uses the status line; generate both consistently.
- **“Forward the downstream response.”** It may have different ownership, trust, disclosure, and semantics.
- **“A 5xx is always retryable.”** Method semantics and effect uncertainty can make replay unsafe.
- **“A 4xx is never retryable.”** `408`, `409`, `412`, and `429` can lead to a corrected, refreshed, or delayed new attempt.
- **“Retry-After guarantees success.”** It is advice, not capacity reservation or deadline extension.
- **“Concealment ends at 404.”** Bodies, headers, validation, time, counts, and logs visible to callers can still enumerate.
- **“Correlation IDs are harmless.”** Unvalidated or structured identifiers can leak data or poison logs.
- **“Catch everything.”** Cancellation and fatal runtime conditions require platform-specific handling.
- **“Logging the stack makes leakage acceptable.”** Telemetry needs its own minimization, access, integrity, and retention policy.
- **“A mapping test proves safety.”** Bypass paths, proxies, serializers, and production configuration also require verification.

## Worked Examples

### Example 1

**Situation:** JSON ends halfway through an object. **Reasoning:** The representation cannot be parsed, so return `400` with type `invalid-request`, a safe byte/location hint if policy permits, and no parser stack. **Conclusion:** syntax failure is translated before domain execution.

### Example 2

**Situation:** The endpoint accepts JSON but receives `text/csv`. **Reasoning:** The problem is representation support, not malformed JSON. Return `415` and document acceptable media types through the contract and appropriate headers. **Conclusion:** media-type semantics remain distinct from content validation.

### Example 3

**Situation:** `If-Match: "v7"` is false because the current visible representation is `"v8"`. **Reasoning:** The caller supplied a failed HTTP precondition, so return `412`; reveal the current validator only if authorized. The client fetches, reconciles, and submits a new condition. **Conclusion:** do not use generic `409` for a formal precondition failure.

### Example 4

**Situation:** A valid command attempts to cancel an already shipped order without a conditional header. **Reasoning:** Domain state conflicts with the requested transition. Return `409` with a stable `order-not-cancellable` type and permitted recovery actions. **Conclusion:** domain conflict is public meaning, not an exception name.

### Example 5

**Situation:** A caller requests another tenant's order. **Reasoning:** Internal outcomes distinguish cross-tenant denial from absence for audit, while disclosure policy maps both to the same `404`, type, body shape, and headers. **Conclusion:** translation preserves authorization concealment.

### Example 6

**Situation:** The database uniqueness constraint rejects an order number. **Reasoning:** The repository maps the constraint to `DuplicateOrderNumber`; the public translator returns `409 duplicate-order-number`. Constraint name and SQL remain in protected cause telemetry. **Conclusion:** adapter translation isolates the public contract from persistence.

### Example 7

**Situation:** An origin service cannot reach its inventory dependency before its deadline. **Reasoning:** The origin owns order availability and returns its documented `503 inventory-temporarily-unavailable`, not the dependency's body. Read retries may be bounded; a mutation with unknown effect needs reconciliation or idempotency. **Conclusion:** dependency topology does not leak through error forwarding.

### Example 8

**Situation:** A client exceeds a per-principal rate window. **Reasoning:** Return `429`, safe scope information, and `Retry-After` only when the reset estimate is meaningful. The client still applies deadline, budget, backoff, and jitter. **Conclusion:** retry advice coordinates load but does not guarantee acceptance.

### Example 9

**Situation:** A non-atomic batch has two successes, one invalid submitted field, and one concealed object. **Reasoning:** The envelope records accepted processing; item results use caller references, bounded public problems, and a generic unavailable outcome for the concealed item. Each committed item has durable identity for selective retry. **Conclusion:** item errors must preserve both partial-effect truth and concealment.

### Example 10

**Situation:** An unexpected null dereference reaches the outer request boundary. **Reasoning:** Record the cause chain, trace, request identity, and effect knowledge under protection. Return generic `500 internal-error` with an opaque occurrence ID and no class, stack, source line, or raw input. **Conclusion:** the fallback is safe and observable, not descriptive debugging output.

## Cross-Program Connections

[Security Engineering](../../25-security-engineering/ROADMAP.md) supplies information-disclosure, enumeration, and logging threat analysis. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies partial failure, deadlines, retries, backoff, and ambiguous outcomes. [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies contract, fault-injection, property, and differential testing. [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies constraint and transaction outcomes. This API module owns their translation into one public HTTP failure contract.

## References

1. M. Nottingham, E. Wilde, and S. Dalal, [*RFC 9457: Problem Details for HTTP APIs*](https://www.rfc-editor.org/rfc/rfc9457.html), July 2023. Obsoletes RFC 7807. Checked 2026-09-01.
2. R. Fielding, M. Nottingham, and J. Reschke, [*RFC 9110: HTTP Semantics*](https://www.rfc-editor.org/rfc/rfc9110.html), especially Sections 10.2.3 and 15, June 2022. Checked 2026-09-01.
3. M. Nottingham and R. Fielding, [*RFC 6585: Additional HTTP Status Codes*](https://www.rfc-editor.org/rfc/rfc6585.html), especially `428` and `429`, April 2012. Checked 2026-09-01.
4. OWASP Foundation, [*Error Handling Cheat Sheet*](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html). Checked 2026-09-01.
5. OWASP Foundation, [*Logging Cheat Sheet*](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html). Checked 2026-09-01.

## Exercises

### Exercise 1

Classify malformed JSON, unsupported JSON media profile, missing bearer credentials, concealed denial, duplicate order number, false `If-Match`, rate-window exhaustion, origin overload, invalid upstream response, and unexpected defect into internal outcome, status, public type, and retry action.

### Exercise 2

Design an RFC 9457 registry entry for an order whose items changed between quote and purchase. Specify safe fields, localization, compatibility, concealment, and client recovery.

### Exercise 3

Diagnose a handler that catches every exception, returns `200 {"error": exception.message}`, copies a vendor trace ID, logs the bearer token, and tells clients to retry any timeout three times.

### Exercise 4

Define error behavior for a payment create whose database commit succeeded but whose response was lost after a downstream timeout. Compare behavior without and with a durable idempotency key.

### Exercise 5

Create a verification strategy for a multi-tenant batch endpoint with per-item validation, concealed authorization, partial commits, dependency failures, localization, and an outer safety boundary.

## Answers to the Exercises

### Answer 1

Malformed JSON becomes a parsing outcome, `400 invalid-request`, corrected request rather than blind retry. Unsupported profile becomes representation outcome, normally `415 unsupported-media-type`. Missing credentials becomes authentication outcome, `401` plus applicable challenge. Concealed denial and absence share `404 not-found`. Duplicate number becomes domain conflict, `409 duplicate-order-number`, requiring a different number. False `If-Match` becomes `412 stale-representation`, requiring fetch and reconciliation. Rate exhaustion becomes `429 rate-limited`, delayed under `Retry-After`, budget, and deadline. Origin overload is `503 temporarily-unavailable`. A server acting publicly as a gateway can use `502` for invalid upstream response; an owning origin normally maps it to its own dependency/unavailable outcome. Unexpected defect becomes generic `500 internal-error`. Every retry decision also considers method, idempotency, effect state, and budget.

### Answer 2

Define type `https://api.example.test/problems/quote-items-changed`, stable title `Quoted items changed`, and normal status `409`. Safe extensions can list bounded caller-visible item references and stable change codes, never supplier internals or hidden items. Detail explains that the client must retrieve a new quote; clients branch on type and codes, so localization may change title/detail only. Additive optional fields follow the compatibility policy; changing meaning requires a new type. If item visibility changed, omit or generically classify it under concealment. Recovery is to fetch an authorized current quote, present changes to the user, and submit a new purchase with its validator—not replay unchanged.

### Answer 3

`200` defeats HTTP failure semantics and caches/tooling; exception messages expose internal detail and are unstable; vendor trace IDs cross a trust boundary; bearer-token logging creates credential compromise; catch-all may swallow cancellation or fatal conditions; and unconditional timeout replay can duplicate non-idempotent effects. Introduce adapter and application outcome vocabularies, a total HTTP mapping, correct 4xx/5xx statuses, stable Problem Details types, generic unknown fallback, opaque occurrence IDs, protected sanitized causal logs, platform-aware fatal/cancellation handling, and retry logic conditioned on method, idempotency, effect knowledge, deadline, and budget.

### Answer 4

Without idempotency protection, the service must classify the effect as ambiguous. It should not invite blind retry; provide an operation lookup, reconciliation path, or human escalation using an opaque occurrence/operation identity. A second create might charge twice. With a durable idempotency key scoped to caller, operation, and canonical request, the server records the committed result and returns that same logical outcome on replay. Retry is then bounded and safe only if idempotency storage committed consistently with the payment effect or can authoritatively reconcile it; a volatile cache or key recorded after the effect does not close the ambiguity.

### Answer 5

Build table tests for envelope and every item outcome, asserting exact status/type/header/schema and capped deterministic ordering. Replace item IDs across tenants and compare absent/forbidden observations, including timing classes and localization. Inject parser, validator, policy, repository, and dependency failures before and after each commit point; assert atomic or partial outcome truth and selective retry identities. Property-test that secret corpus values, exception strings, tokens, hidden IDs, and vendor bodies never appear publicly, and that HTTP/body status agree. Contract-test stable types and language-neutral codes across locales. Force an unknown exception and verify generic `500` plus protected cause telemetry. Trace committed effects against response outcomes and review the remaining timing, intermediary, and operational limitations.
