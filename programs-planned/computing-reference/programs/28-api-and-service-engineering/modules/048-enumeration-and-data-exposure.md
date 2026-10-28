---
module_id: API-048
program: API & Service Engineering
level: 1
module_number: 48
title: Enumeration and Data Exposure
status: complete
last_verified: 2026-09-01
---

# Enumeration and Data Exposure

## One-Page Review

### Governing question

How should an API reveal the minimum data required for an authorized task while preventing unauthorized callers from inferring accounts, objects, relationships, properties, internal structure, or secret state through response differences and repeated queries?

### Essential definitions

- **Enumeration** is systematic probing that turns an observable API distinction into a list or classification of accounts, objects, tenants, properties, states, or capabilities.
- **Data exposure** is disclosure of content or metadata beyond the caller's authorized, task-relevant response contract.
- An **observable transcript** includes status, headers, body/schema, length, ordering, timing, cache behavior, rate-limit behavior, connection effects, and external side effects.
- An **enumeration oracle** is any repeatable transcript difference correlated with a protected fact such as existence, membership, validity, or state.
- **Response equivalence** means secret cases that policy treats alike are made sufficiently indistinguishable under a stated attacker/measurement model.
- **Explicit projection** constructs a response from an allowlisted response DTO/schema instead of serializing an internal object and hiding fields in the client.
- **Existence concealment** maps absent and forbidden targets to the same public outcome when revealing existence is itself unauthorized.
- **Data minimization** returns only fields, rows, aggregates, precision, and metadata needed for the authorized purpose.

### Central model, mechanism, or theorem

For operation $a$, context $c$, object $o$, and purpose $u$, return fields only from

$$
F_{out}=F_{contract}(a)\cap F_{read}(c,a,o)\cap F_{purpose}(u).
$$

Filter authorized objects before projection, aggregation, sorting, counting, pagination, or cache storage.

For protected fact $Z$ and unauthorized observation $\tau=(status,headers,body,length,time,cache,limits,effects)$, group secret cases that policy says must look alike into an equivalence class and design

$$
\mathcal{L}(\tau\mid Z=z_0)\approx\mathcal{L}(\tau\mid Z=z_1).
$$

This is an engineering goal under a declared attacker and noise model, not a proof of zero leakage on real networks.

### Critical invariants

Authorization precedes serialization and all derived output. Internal/domain/persistence entities are never generic response contracts. Every operation, role, field, nested edge, list, count, facet, export, error, and alternate method has an explicit disclosure policy. Forbidden and absent objects use one externally consistent outcome when existence is sensitive. Account login, registration, invitation, recovery, verification, and lookup do not expose existence through status, message, redirect, body shape, timing path, notification, or rate-limit bucket. Random IDs slow guessing but do not authorize or eliminate enumeration through leaked IDs and search. Filters can only narrow an authorized set. Caches/CDNs never serve one principal's projection to another. Logs, traces, metrics, support tools, and analytics are protected data products. Generic responses preserve internal decision evidence without reflecting it publicly. Automation resistance limits an oracle's scale but never substitutes for removing the oracle.

### Common failures

Returning 403 for an existing forbidden ID and 404 for absent; exposing sequential IDs or total counts; using UUIDs as the only control; quick-exiting unknown accounts before password hashing; returning “email already registered”; sending different reset responses/redirects/timings; serializing entire ORM objects and relying on UI hiding; exposing password hashes, tokens, internal IDs, flags, locations, risk scores, stack traces, query text, or relationship metadata; filtering rows after count/page; GraphQL fields that fetch secrets before field authorization; bulk per-ID results that distinguish forbidden from absent; object-only shared cache keys; different CDN cache hits, ETags, HEAD lengths, or rate-limit headers; verbose logs with payloads/tokens; and measuring one happy-path response while ignoring distributed statistical leakage.

### Compact example

Password reset accepts an email. For both known and unknown normalized addresses, the API performs the same bounded public workflow, returns `202` with “If an eligible account exists, instructions will be sent,” uses the same response schema/cache headers and approximately matched processing path, and enforces privacy-aware global/source/destination abuse controls. Only the known eligible account causes an asynchronous protected delivery, which is not disclosed to the requester. **Conclusion:** the API acknowledges the request, not account existence; scale controls bound residual timing and side-effect probes.

### Connections

[Object-Level Authorization](046-object-level-authorization.md) determines which objects may be observed, [Mass Assignment and Overposting](047-mass-assignment-and-overposting.md) constrains write properties, and [Error Translation](035-error-translation.md) defines stable public failures. [Replay and Request Signing](../ROADMAP.md) next protects freshness and message authenticity rather than disclosure.

## Governing Question

Which facts may this caller learn from this operation, at what granularity, and how can every observable—including repeated and indirect observations—be made consistent with that disclosure policy?

## Why This Matters

An API can deny the requested secret body yet disclose enough to reconstruct it. Different status codes reveal whether an object exists. Pagination totals reveal a tenant's customer count. Autocomplete reveals email membership. Timing reveals which login took the expensive credential path. A reset message reveals a registered account. A GraphQL error names a hidden field's object. A cache hit reveals prior access. Repeated narrow aggregate queries reconstruct individual values.

Enumeration converts a tiny per-request distinction into a dataset. Valid usernames improve credential stuffing and phishing. Valid patient, order, vehicle, repository, or tenant identifiers guide targeted BOLA probes. State distinctions reveal moderation, payment, legal, employment, or health facts. Even public-looking metadata can become sensitive when correlated, timestamped, or collected at scale.

Data exposure is broader than obviously secret columns. OWASP API3:2023 treats excessive data exposure as broken object-property authorization: being allowed to read an object does not imply authority to read every property. Internal IDs enable joins; precise timestamps support activity inference; flags disclose fraud or moderation; counts disclose business volume; relationship edges disclose social/organizational structure. The UI is not a security boundary because callers inspect raw responses.

Perfectly identical behavior is often infeasible and sometimes undesirable. An authorized owner should learn that their order exists; a public directory deliberately supports discovery; network latency is noisy; delivery side effects differ. The engineering task is to classify facts, callers, channels, and acceptable leakage, then remove accidental or disproportionate oracles, bound residual distinguishability, and detect automated exploitation.

## Prerequisites and Retrieval

Retrieve authentication and recovery, object/property authorization, privacy/data classification, response schemas, 401/403/404 semantics, timing and other side channels, probability distributions/statistical tests, random identifiers, pagination/search/aggregation, GraphQL execution, caching/CDNs, rate limits, compression/conditional requests, logs/traces/metrics, threat modeling, data retention, and abuse detection.

Before designing disclosure, retrieve protected fact classes and data owners, public/tenant/private/subject/support audiences, purpose and precision needs, every synchronous/asynchronous observable, identity/account workflows, object ID sources, list/search/count/export paths, nested fields/relationships, response serializers, error maps, cache keys/policies, CDN behavior, alternate HTTP methods, notification and webhook effects, rate-limit scopes/headers, log/trace/analytics sinks, attacker request volume/distribution, legal/privacy requirements, incident evidence, and deletion/retention policy.

## Learning Objectives

By the end of this module, you should be able to:

1. model enumeration as inference from a complete observable transcript;
2. derive explicit object and property projections from authorization and purpose;
3. design account, identifier, error, list, aggregate, GraphQL, bulk, and cache behavior without accidental oracles;
4. distinguish response equivalence from brittle claims of constant network time;
5. balance public discovery and legitimate UX against sensitive existence concealment;
6. minimize and protect logs, metrics, traces, exports, notifications, and derived data; and
7. test statistically and adversarially for direct, indirect, repeated, and cross-channel disclosure.

## Core Exposition

### Model the whole observable transcript

Do not reduce an API response to status/body. An attacker can observe status, headers, content type, body shape and wording, length, compression, ordering, number of errors, redirects, cookies, connection close/retry, latency distribution, cache age/hit headers, ETag/Last-Modified, rate-limit headers, retry windows, HTTP/2 stream behavior, and whether a later side effect occurs.

The oracle may span requests. Registration rejects an existing email, reset accepts it, login takes longer for it, and invitation lookup returns a display name. Any one channel may seem harmless; together they classify accounts confidently. Model a transcript across the workflow and shared infrastructure, including CDN, gateway, identity provider, queue, email/SMS delivery, webhooks, fraud controls, and support notifications.

Define the secret fact $Z$ and which caller class may learn it. Examples: “account for email exists,” “object ID exists but belongs to another tenant,” “patient has an appointment,” “repository is private,” or “moderation flag is set.” Then list observations $\tau$ and expected equivalence classes. Public, authorized, and unauthorized callers may have different policies.

Response equivalence is contextual. It does not require every error in an API to look identical; it requires cases whose distinction is protected to avoid a reliable distinguishing transcript. Preserve an internal reason code/decision ID in protected logs so operations can diagnose without exposing it to the caller.

### Project data explicitly from authorized purpose

OWASP recommends selecting specific response properties rather than generic `to_json()`/`to_string()` and keeping returned structures minimal. Build action-specific response DTOs/schemas. A user summary may include public ID and display name; a self profile adds private email/preferences; support adds carefully scoped case data; none includes password hashes, recovery tokens, signing material, internal risk features, raw identity-provider claims, or unrestricted relationships.

Compute field authorization on current context/object, then construct the response from permitted fields. Redaction after generic serialization is fragile: new fields appear before a denylist knows them, nested objects escape, serialized bytes may be cached/logged before filtering, and null/omission can still reveal classifications. Prefer positive projections near data access and again at the response schema boundary.

Minimize precision and cardinality as well as names. Return an age band rather than birth date if sufficient, coarse region rather than coordinates, boolean availability rather than internal capacity, and capped/rounded aggregates where exact counts are unnecessary. Pseudonymous public identifiers can prevent joins to internal systems, but stable pseudonyms still enable correlation and need lifecycle policy.

Purpose limitation is not inferred from a broad role. A support agent resolving delivery may need address and shipment state, not password/MFA/risk data. A fraud analyst may need risk features under a case, not all message content. Encode distinct actions/projections, justification, expiry, and audit.

### Authorize before list, count, order, and aggregation

For list/search queries, derive the authorized object set first. Apply client filters as a further intersection. Only then project, sort, paginate, count, facet, aggregate, generate cursors, or compute suggestions. Filtering response rows after querying/counting leaks hidden population and produces unstable pages.

Counts and aggregates can expose individuals: query a group, then add/remove one predicate and subtract; issue overlapping ranges; compare before/after an event. Minimum cohort sizes, rounding/noise, query auditing, contribution bounds, budgets, delayed releases, or refusing high-risk filters may be required. These mechanisms involve privacy statistics beyond this chapter, but ordinary authorization alone is not sufficient for inference-resistant analytics.

Search/autocomplete should restrict the indexed corpus and returned properties before ranking. Do not reveal “no exact account” versus “exists but hidden.” Bound query flexibility, wildcard/regex cost, result windows, and repeated prefix scans. Cursors must be opaque/integrity-protected and must not contain raw hidden sort keys or allow resuming into another tenant. A cursor is not lasting authorization; reapply current policy.

Exports are new protected artifacts. Authorize query and properties, record creator/tenant/purpose/classification, cap size, generate under current or explicitly bounded snapshot authority, protect storage/download, expire/revoke, and audit. Do not put a broad export link or file path in ordinary logs.

### Conceal object existence when policy requires it

RFC 9110 permits a server to return 404 instead of 403 to hide a forbidden target's existence. For private objects, use one public response for absent and inaccessible: same status, problem type, body schema/length class, headers, cache policy, and sufficiently similar processing. Do not fetch/render secret content just to equalize; use an authorized lookup or minimal policy projection.

Use 403 when the caller is allowed to know the resource/action exists and different authorization or remediation is meaningful—for example, an active tenant member lacks an approval permission. Concealment is a policy decision, not a universal rule. Document it per resource/caller and keep HEAD, conditional GET, range, alternate formats, nested expansions, storage endpoints, and legacy versions consistent.

Random high-entropy identifiers reduce blind scanning and business-volume inference, but IDs leak and authorized list/search surfaces expose them. Always enforce object authorization. Sequential public IDs may be acceptable for intentionally public resources; do not sacrifice usability without a threat reason. Separate public stable ID from storage key when it reduces correlation or operational disclosure.

Beware secondary signals. Existing forbidden objects might cause database work, relationship service calls, different cache hits, unique constraint errors, redirects to canonical slugs, ETags, object-specific rate buckets, or audit notifications. Align paths where practical; bound rate and monitor systematic probes. Do not claim cryptographic constant-time behavior for a distributed request merely because messages match.

### Make identity and recovery workflows enumeration-resistant

OWASP Authentication guidance recommends generic responses for incorrect credentials, nonexistent, locked, or disabled accounts and notes quick-exit timing discrepancies. Use one login failure status/body for these protected cases. Perform an expensive password-verification-equivalent path for unknown users using a fixed dummy hash configured like real hashes, while still applying account-specific controls only internally. MFA/SSO discovery, organization routing, password policy, and lockout headers must not reintroduce existence leakage.

Password reset/recovery should return a consistent message and approximately uniform public response time for known/unknown accounts. Queue delivery asynchronously after the public response path. Reset requests must not lock accounts or enable mailbox/SMS flooding; use source/global and privacy-aware destination controls without returning per-account counters. Tokens are random, single-use, expiring, securely stored/validated, and unrelated to whether the request endpoint discloses existence.

Registration and invitation are harder because users need actionable feedback. Options include accepting a request and sending an account-specific email, requiring possession verification before revealing conflict, directing existing users through login/recovery, or deliberately revealing membership when the product's public directory policy allows it. Make the tradeoff explicit; do not accidentally expose it through a database uniqueness error.

Account/email/phone availability endpoints are direct enumeration APIs. Avoid them for private identities or gate them behind a verified flow and abuse controls. Contact discovery/address-book matching demands specialized privacy design; hashing low-entropy identifiers does not make membership tests private.

### Prevent property and relationship exposure

OWASP API3:2023 states that access to an object must include access to each exposed property. Response shapes differ by operation and audience. Do not return the full entity and expect a mobile/browser client to hide fields. A sensitive field selected by GraphQL is still sensitive even though the client asked explicitly.

Field policy covers values and existence. Omitting `suspension_reason` only for suspended users can reveal state; a nullable stable schema may reduce shape leakage but can still reveal through null versus value. Decide which fact is protected. Sometimes the caller may learn “restricted” but not reason; return an explicit coarse classification instead of accidental null patterns.

Relationships are data: owner identity, team membership, follower graph, tenant links, approver, beneficiary, shared-with list, and counts. Authorize every nested edge and direction. A caller who may view a document may not view all collaborators' emails. Apply minimization to relationship metadata, timestamps, roles, and pagination totals.

Internal identifiers, database keys, bucket paths, hostnames, trace IDs, policy rule names, stack traces, dependency versions, query text, and infrastructure topology can aid correlation/exploitation. Some request/trace IDs are valuable to clients; use opaque public correlation IDs that map internally rather than exposing storage or security tokens.

### Secure GraphQL, batches, and alternative views

GraphQL selection prevents automatic over-returning only if the schema omits secrets or resolvers enforce field/object policy. Introspection reveals schema by design but does not grant data; decide whether schema names themselves are sensitive, while avoiding reliance on disabled introspection as data authorization. Gate fields before fetching/side effects, cover aliases/fragments/interfaces/unions/node lookups/federation, and define null/error behavior that does not disclose hidden object state.

Avoid error extensions containing database messages, stack traces, paths to secret fields, internal exception types, or unauthorized object IDs. Batched queries and aliases can amplify enumeration; enforce per-subject/object/action policy and aggregate cost/rate, not one check per HTTP request only. Subscription authorization must be checked at subscription and over its lifetime; event shape/count/timing can leak changes.

Bulk REST/RPC results can become a high-throughput existence oracle when each submitted ID returns `missing`, `forbidden`, or `success`. For an unauthorized caller, collapse protected cases, cap batch size, and choose atomic, filtered, or per-item semantics deliberately. Input/output correlation may itself confirm IDs. Internal diagnostics retain precise reasons under access control.

Content negotiation, mobile/legacy versions, CSV/PDF exports, print/email views, HEAD/OPTIONS, thumbnails, and debug/support endpoints need the same projection. Attackers choose the least protected representation.

### Include caches, compression, and infrastructure in disclosure policy

Cache only a representation safe for everyone addressed by its key. Private/user/tenant/role/field-level responses need corresponding key dimensions or `private`/`no-store`; `Vary` must match actual selection. Validate CDN configuration so authorization headers, cookies, query parameters, and host/tenant partitions cannot collide. Invalidate on permission/data changes within the stated exposure bound.

Cache hits/misses and `Age`, ETag, Last-Modified, object length, range support, and conditional status can reveal existence or change activity. Opaque validators should not encode secrets. Apply authorization before honoring conditional/range requests. Do not share negative caches across security contexts if that creates cross-user state inference or blocks a newly authorized object.

Compression and response size make field/value differences observable and can create specialized side channels when attacker-controlled and secret text share a compression context. Avoid reflecting attacker input beside high-value secrets, disable inappropriate compression/context reuse, and minimize secrets. This chapter does not claim to solve transport compression attacks universally.

Gateways/WAFs can normalize coarse errors and rate-limit probes but may add their own distinctive bodies/headers/timing. The origin remains responsible for authorization and projection. Test end to end through production-like proxy, CDN, cache, and identity routes.

### Protect operational and side-effect data

Logs, traces, metrics, audit, crash reports, analytics, support exports, and replay tools are data stores with different audiences. Do not log access/refresh/recovery tokens, passwords, raw authorization headers, sensitive payloads, or unrestricted response bodies. Pseudonymize/bound identifiers, control access/retention, encrypt transport/storage, and audit queries/exports.

Metrics require bounded labels; raw user/object/search strings cause both privacy leakage and cardinality failure. Traces can record safe route templates and decision IDs, not raw URLs with secrets or database rows. Debug modes and exception pages must never be reachable merely by a header/query parameter in production.

Side effects can disclose existence: a known account receives mail/SMS/push, an object's owner gets a notification, a webhook fires, or a rate-limit counter changes. An attacker who controls/observes the destination can sometimes learn the fact legitimately; otherwise queue asynchronously, minimize content, authenticate destination changes, and avoid reflecting delivery status. Threat-model insiders, shared inboxes, SIM/forwarding, webhook tenants, and notification flooding.

Audit itself should be more precise than the public response: absent versus forbidden, known versus unknown, field policy, policy revision, source/client, normalized target pseudonym, and trace. Restrict it because the audit stream is an enumeration gold mine.

### Test distinguishability and inference, not only equality

Build paired cases for secret-equivalent states: absent/forbidden object; unknown/known-locked/disabled/wrong-password account; hidden/public property; zero/one hidden row; cache cold/warm; notification eligible/ineligible. Compare status, headers, body schema/content/length, redirects, cookies, connection, rate-limit headers, logs visible to caller, and externally observable side effects.

Timing needs repeated distributions under controlled and realistic noise, not one stopwatch value. Random sleep is usually a weak patch: attackers average samples, sleep harms capacity, and paths still differ. Prefer equalized necessary work, asynchronous responses, bounded deadlines, caching controls, and rate limits. Use statistical tests/plots as detection evidence while avoiding claims that failure to distinguish proves equivalence.

Exercise repeated adaptive queries: ID walking, prefix search, binary search over time/ranges, overlapping aggregates, GraphQL aliases, batch arrays, conditional requests, cache priming, concurrent probes, and distributed sources. Verify that rate limits combine source, account/target, tenant, client, and global controls without exposing which target exists. Monitor high miss/deny ratios, sequential/prefix patterns, diverse target probes, reset/registration storms, and aggregate differencing.

The executable model demonstrates normalized reset and private-object outcomes plus explicit public field projection. It models response values, not real latency, delivery, caches, or network distributions.

<!-- bijux-verify: {"id":"minimal-equivalent-responses","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"reset_known=202|If an eligible account exists, instructions will be sent.\nreset_unknown=202|If an eligible account exists, instructions will be sent.\nprivate_peer=404|not_found\nprivate_absent=404|not_found\nfields=display_name,id\n","stderr":""}} -->
```python
accounts = {"alice@example.test"}
profiles = {"alice": {"id": "alice", "display_name": "Alice", "email": "alice@example.test",
                      "risk_score": 91, "tenant_id": "north"}}

def request_reset(email):
    normalized = email.strip().lower()
    delivery_eligible = normalized in accounts  # queued privately; never reflected
    _ = delivery_eligible
    return 202, "If an eligible account exists, instructions will be sent."

def get_private_profile(actor, profile_id):
    profile = profiles.get(profile_id)
    if profile is None or actor != profile_id:
        return 404, "not_found"
    return 200, {"id": profile["id"], "display_name": profile["display_name"]}

for label, email in (("known", "alice@example.test"), ("unknown", "nobody@example.test")):
    status, message = request_reset(email)
    print(f"reset_{label}={status}|{message}")
print("private_peer=" + "|".join(map(str, get_private_profile("mallory", "alice"))))
print("private_absent=" + "|".join(map(str, get_private_profile("mallory", "missing"))))
public = {key: profiles["alice"][key] for key in ("id", "display_name")}
print("fields=" + ",".join(sorted(public)))
```

The output is necessary evidence for these branches only. A production review still needs real serializer schemas, proxy/cache behavior, timing samples, notification visibility, logs, rate limits, analytics inference, and attack testing.

## Definitions and Notation

Let protected fact $Z$ take values in a policy-defined set, caller/context be $c$, and complete observable transcript be random variable $\tau$. $\mathcal{L}(\tau\mid Z=z)$ denotes the distribution of observations when the secret case is $z$. Exact equality is rarely established for a distributed API; the design goal is bounded distinguishability for cases policy groups together under a declared query budget and observation model.

Let $O_c$ be objects authorized for context $c$, $Q$ the set selected by a client query, and $F_{contract}$, $F_{read}$, $F_{purpose}$ the contract, authorization, and task-relevant field sets. A correct ordinary response uses objects $Q\cap O_c$ and fields $F_{out}=F_{contract}\cap F_{read}\cap F_{purpose}$. Counts/aggregates over unauthorized objects are not made safe merely by omitting their rows afterward.

An **oracle** is a mapping from requests and hidden state to observations with useful correlation. **Direct disclosure** returns the fact/value. **Differential disclosure** reveals it through case differences. **Inferential disclosure** derives it by combining allowed observations. **Amplification** uses batching, automation, concurrency, or distributed identities to turn weak leakage into a dataset.

## Mechanisms, Invariants, or Proof Structure

1. Classify data, existence, membership, relationship, state, and aggregate facts by caller and purpose.
2. Inventory every observation across origin, gateway/CDN/cache, identity, queue/delivery, logs/analytics, and repeated workflows.
3. Define explicit authorized object and field projections; filter before ordering, pagination, counts, aggregation, serialization, caching, or export.
4. Group protected secret cases into response-equivalence classes and specify status/body/header/cache/timing/side-effect behavior.
5. Make identity/recovery/registration and private-object paths generic where disclosure is unauthorized; retain precise protected internal reasons.
6. Secure nested relationships, GraphQL fields, batches, alternate formats/methods, validators, and infrastructure metadata.
7. Minimize precision/cardinality and apply inference controls for flexible search/analytics.
8. Partition or disable caching appropriately and protect operational data products and notification/webhook effects.
9. Add query-cost/rate/abuse controls that bound scale without revealing target existence through their own behavior.
10. Test paired transcripts and repeated adaptive inference end to end; monitor residual enumeration and revisit the accepted leakage model.

If every response row is drawn from $Q\cap O_c$ and every property from $F_{out}$, then direct row/property output lies within those declared sets, assuming the sets and serializer are correct. This does not establish that counts, timing, lengths, errors, order, cache state, or repeated queries reveal nothing. Response-equivalence testing similarly supplies evidence against a chosen distinguisher; it cannot prove universal noninterference.

## Alternatives and Trade-Offs

Precise errors improve legitimate UX and support but can reveal existence/state. Generic errors conceal more but frustrate recovery and can hide actionable permissions. Choose by sensitivity and relationship; provide safe next steps and internal decision IDs rather than secret reason detail.

404 concealment reduces private-object enumeration; 403 communicates authorization remediation where existence is already known. Uniformly using either code without matching bodies, headers, timing, caches, methods, and nested paths is incomplete. Random IDs reduce scanning efficiency while stable human slugs improve sharing/discovery. Neither decision replaces authorization.

Strict minimal response DTOs reduce exposure and coupling but add mapping/schema work and can require new operations for new purposes. Generic entity serialization is convenient and evolves automatically—the exact qualities that make it unsafe. GraphQL gives clients field choice and can reduce overfetch, but field-level authorization/cost/inference remain server obligations.

Exact totals help navigation and analytics; capped/approximate/no totals reveal less and can be cheaper. Public aggregate products may need formal privacy mechanisms, cohort thresholds, and budgets; internal authorization alone does not address differencing. Coarsening loses utility, so document purpose and acceptable error.

Equalized computation reduces timing differences but consumes resources for invalid requests. Asynchronous acknowledgment can isolate delivery/work but changes semantics. Random delays are costly and statistically averageable. Prefer uniform necessary work, dummy credential verification, async queues, bounded deadlines, and abuse limits, then measure residual distributions.

Rate limits and bot challenges bound enumeration but can impair shared networks/accessibility and become account-existence oracles if scoped/returned differently. Combine privacy-preserving source/client/global/target controls with risk signals and recovery, and treat them as amplification controls rather than confidentiality proof.

## Failure Modes and Misconceptions

- **“We return 404.”** Other status/body/header/timing/cache/side-effect differences may still reveal existence.
- **“IDs are UUIDs.”** IDs leak; authorized list/search and correlation still enable enumeration.
- **“The mobile app hides the field.”** Raw API callers receive whatever the server serialized.
- **“GraphQL returns only requested fields.”** Attackers request hidden fields; resolver policy and schema design remain mandatory.
- **“Counts are harmless metadata.”** Totals, facets, cursors, ordering, and differencing can expose hidden populations/individuals.
- **“The message is generic.”** Quick exits, hashing, redirects, cookies, cache hits, delivery, and rate buckets can distinguish cases.
- **“We added random sleep.”** Repeated samples average noise while consuming capacity and preserving path differences.
- **“Rate limiting fixes enumeration.”** It only changes scale and can itself reveal per-target state.
- **“We redact after serialization.”** New/nested fields may leak to cache/logs or through shape before redaction.
- **“Null means no disclosure.”** Field presence/null patterns can classify object state or caller privilege.
- **“Filtering rows is enough.”** Pre-filter counts, aggregation, sorting, cursor, and timing can still include hidden data.
- **“The gateway normalizes errors.”** Origins and alternate paths still own authorization/projection; gateways add observables.
- **“Logs are internal.”** Support, analytics, vendors, exports, and incident tooling expand their audience and retention.
- **“No statistical difference found.”** A chosen finite test cannot prove no adversary/channel can distinguish.
- **“Public data needs no limits.”** Collection at scale and correlation can change privacy/abuse risk even for individual public records.

## Worked Examples

### Example 1

**Situation:** Login returns “user not found,” “wrong password,” and “account locked.” **Reasoning:** These classify registered accounts and state. Return one public failure for protected cases, run a comparable password verification using real or dummy hash, keep lock/disabled reason internal, and rate-limit without target-specific public counters. Successful login remains distinguishable because the authenticated session is intended output. **Conclusion:** equivalence applies to unauthorized failure cases, not to deliberately successful authentication.

### Example 2

**Situation:** Private project 7 returns 403 while absent project 8 returns 404. **Reasoning:** An outsider now enumerates project IDs. Authorized retrieval maps both to one 404 contract, aligns headers/cache/body, and monitors ID walks. An existing project member lacking `archive` can receive 403 because membership already authorizes knowledge of existence. **Conclusion:** existence disclosure depends on caller relationship, not a global status-code slogan.

### Example 3

**Situation:** `/patients?condition=x` returns no rows but `total=1`. **Reasoning:** Filtering occurred after count, directly disclosing a hidden patient. Apply tenant/relationship/property policy in the base query before count, filter, page, facets, and cursor. For small-cohort analytics, exact authorized counts may still permit differencing, so thresholds/budgets may be needed. **Conclusion:** every derived value must use the authorized population.

### Example 4

**Situation:** A user response includes `password_hash`, `mfa_secret_present`, `risk_score`, and internal tenant ID; the UI shows only name. **Reasoning:** The server exposed protected properties. Build a public summary DTO with opaque public ID/display name and self/support projections for their tasks. Do not merely redact known secrets from the entity. Contract tests fail on unexpected fields. **Conclusion:** readable object authority is not readable-all-properties authority.

### Example 5

**Situation:** Password reset messages match, but known accounts take 180 ms and unknown accounts 4 ms. **Reasoning:** Quick exit is a timing oracle. Execute comparable normalization/lookup and fixed-cost credential-related work or acknowledge asynchronously, avoid data-dependent redirects/cache, and compare repeated distributions. Rate limits bound averaging. **Conclusion:** text equality without processing-path analysis is insufficient.

### Example 6

**Situation:** GraphQL `reportUser` returns the reported user's recent location in a nested object only when the user exists. **Reasoning:** The mutation needs a stable receipt, not target profile. Remove that field/object from the response contract or field-authorize it; make nonexistent/inaccessible targets follow the same safe report outcome when appropriate, prevent aliases/batching amplification, and audit abuse. **Conclusion:** nested mutation responses can combine property exposure and enumeration.

### Example 7

**Situation:** A batch endpoint returns `{id, result: missing|forbidden}` for 1,000 IDs. **Reasoning:** One request becomes a high-throughput oracle. Cap batch size, authorize every ID, collapse protected missing/forbidden outcomes, and choose atomic/filtered/per-item semantics without exposing input correlation beyond policy. Apply total and per-target/source limits. **Conclusion:** batch design controls both disclosure vocabulary and amplification.

### Example 8

**Situation:** Alice's private invoice is cached by URL; Bob receives it, while cache headers reveal recent access. **Reasoning:** The CDN omitted authorization dimensions. Mark private/no-store or partition on tenant/subject/projection and validate actual cache keys; strip unsafe cache diagnostics, authorize conditional/range requests, and purge permission changes. **Conclusion:** cache infrastructure is part of property authorization and observable transcript.

### Example 9

**Situation:** An analytics API permits counts for any filters; an analyst subtracts counts for adjacent age ranges to isolate one person. **Reasoning:** Each query is authorized but their composition discloses an individual. Enforce minimum cohorts, limit dimensions/precision, audit correlated queries, bound contributions/budgets, delay/round/noise where the product requires. **Conclusion:** inferential exposure requires cross-query controls beyond row-level authorization.

### Example 10

**Situation:** Public profile data is legitimate, but an attacker scrapes the entire directory using prefix search and sequential pages. **Reasoning:** Confidentiality is not the only harm; collection enables spam/harassment. Define intended discoverability, minimize fields/precision, require bounded queries, cap pages, rate/risk-limit automation, provide robots/terms only as non-security signals, and monitor collection patterns. Do not pretend public fields are secret. **Conclusion:** separate intentional disclosure from abusive amplification and control each honestly.

## Cross-Program Connections

- **Security Engineering:** side channels, reference monitoring, least privilege, defense in depth, and abuse economics frame observables and amplification.
- **Privacy Engineering:** minimization, purpose limitation, linkability, aggregation, differencing, retention, and formal privacy mechanisms bound inference.
- **Identity and Access Management:** account lifecycle, login/recovery/registration/invitations, lockout, MFA, and directory discovery are enumeration hotspots.
- **Database Engineering:** authorized projections, filtered counts, query plans, indexes, row policy, views, and snapshot semantics determine direct/derived output.
- **Distributed Systems:** caches, replicas, queues, delivery, mixed paths, timeouts, retries, and timing noise create cross-component transcripts.
- **Statistics:** hypothesis testing, effect size, sample size, multiple observations, and distributions are required to assess timing/inference evidence carefully.
- **GraphQL and Language Design:** schema visibility, resolver/field semantics, aliases, null/error behavior, and query expressiveness shape disclosure.
- **Observability Engineering:** safe logs, bounded metric labels, trace redaction, protected audit, sampling, vendors, and retention turn telemetry into a governed dataset.

## References

1. OWASP Foundation. [API1:2023 Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/). OWASP API Security Top 10, 2023. Checked 2026-09-01.
2. OWASP Foundation. [API3:2023 Broken Object Property Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/). OWASP API Security Top 10, 2023. Checked 2026-09-01.
3. OWASP Foundation. [Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html). OWASP Cheat Sheet Series. Checked 2026-09-01.
4. OWASP Foundation. [Forgot Password Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html). OWASP Cheat Sheet Series. Checked 2026-09-01.
5. Fielding, R., Nottingham, M., and Reschke, J. [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html). IETF, June 2022. Checked 2026-09-01.
6. MITRE. [CWE-203: Observable Discrepancy](https://cwe.mitre.org/data/definitions/203.html). CWE 4.20. Checked 2026-09-01.

## Exercises

### Exercise 1

Inventory the observable transcript and protected equivalence classes for login, signup, invite acceptance, password reset, email change, and account lookup. Specify legitimate disclosure and generic behavior.

### Exercise 2

Given a multi-tenant search endpoint with filters, exact totals, facets, sortable sensitive fields, cursor pagination, and CSV export, derive authorized/minimized query and response semantics and identify inference attacks.

### Exercise 3

Diagnose private-object endpoints whose body/status match for absent and forbidden cases but whose cache, ETag, HEAD, timing, rate-limit, notification, and logs differ. Propose end-to-end tests and fixes.

### Exercise 4

Design role/purpose-specific REST and GraphQL projections for a health record used by patient, clinician, billing, researcher, support, and public-health workflows. Include nested relationships and errors.

### Exercise 5

Transfer enumeration analysis to a physical access API exposing badge validation, room occupancy, visitor invitations, emergency overrides, access logs, and building-directory search.

## Answers to the Exercises

### Answer 1

Protected facts include account existence, locked/disabled state, login method/MFA enrollment, organization membership, pending invitation, recovery eligibility, and destination. Observe status/body/schema/length, redirects/cookies/headers, latency, CAPTCHA/limit headers, email/SMS/push, account lock, and support events across workflows. Failed login uses one response and real/dummy comparable verification; reset uses one asynchronous acknowledgment; signup may accept and email existing/new users or reveal only after possession verification; invitation tokens reveal only their own bounded state after validation; email change requires authenticated subject and verification. Internal audit distinguishes reasons. Successful authentication, verified invitation ownership, and authenticated self-service intentionally reveal necessary facts. Global/source/privacy-aware target controls and monitoring bound probes without returning per-account existence.

### Answer 2

Build the base set from trusted tenant and object/property authorization, then intersect client filters. Permit only approved filter/sort fields; never sort or facet on hidden properties for callers lacking them. Compute rows, exact/rounded/capped total, facets, cursor, and export from the authorized set. Cursors are opaque/integrity-protected, tenant/query/projection/version bound, and reauthorized. Prevent arbitrary tiny cohorts, overlapping-range differencing, presence/absence comparisons, prefix walking, and repeated high-dimensional queries with cohort thresholds, dimension/precision limits, query auditing/budgets, and rate/cost controls. CSV is a separate expiring protected artifact with the same or narrower columns/rows and download authorization; it does not expose internal IDs or broader precision.

### Answer 3

Matching origin body/status is insufficient. Existing objects may hit data/relationship/cache paths, produce different ETags/lengths, make HEAD/conditional/range responses, consume object-specific buckets, notify owners, or emit caller-visible logs/support IDs. Use authorized lookup/minimal policy projections, one error serializer/cache policy, authorization before validators/method variants, opaque non-object-derived public decision IDs, and async/no owner notification for unauthorized probes. Partition/disable caches and hide unsafe cache diagnostics; make rate-limit responses privacy-safe; protect logs. Test paired absent/forbidden cases cold/warm, all methods/formats/headers, concurrency and repeated timing distributions through CDN/gateway/origin, limit exhaustion, notification observation, and log visibility. Monitor rather than claim perfect constant network time.

### Answer 4

Define distinct actions/projections. Patient sees own clinical summary/results/appointments but not internal risk/audit; clinician sees assigned-care clinical details and necessary team relationships; billing sees coded service/coverage/amount, not unrelated notes; researcher receives approved de-identified/minimized cohorts with inference controls; support sees case-bound contact/workflow metadata, not clinical content; public health receives legally authorized purpose/precision-limited reports; no public record exists. REST response DTOs and GraphQL field resolvers share canonical field/edge policy, filter objects first, minimize timestamps/identifiers, authorize attachments and clinician/patient relationships, and use safe null/error semantics. Exports/subscriptions/caches/logs preserve projection. Emergency access is explicit, time/case bound, heavily audited, and does not silently broaden every endpoint.

### Answer 5

Protected facts include valid badge IDs, employee/visitor identity, room membership/occupancy, invitation existence, access decisions, schedules, and emergency state. Badge validation returns a minimal actuator decision over an authenticated channel, not person details; invalid/unauthorized/revoked cases expose only what the door needs and use comparable processing. Directory search is audience/purpose limited and resists prefix scraping. Invitation lookup requires a high-entropy one-time token and reveals only bounded host/location/time after validation. Occupancy is coarse/capped for ordinary users and precise only for authorized safety roles. Emergency override uses strong device/operator identity, time/location/action scope, physical safety policy, expiry, and immutable protected audit. Access logs are highly sensitive, with subject self-view or case/legal access, retention and export controls. Rate/anomaly detection handles badge walking without causing unsafe denial of emergency egress.
