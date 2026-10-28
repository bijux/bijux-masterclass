---
module_id: API-015
program: API & Service Engineering
level: 1
module_number: 15
title: Create, Read, Update, and Delete Semantics
status: complete
last_verified: 2026-09-01
---

# Create, Read, Update, and Delete Semantics

## One-Page Review

### Governing question

How should an API express creation, retrieval, replacement, and deletion through HTTP while preserving domain invariants, concurrency, retries, caches, and honest outcome meaning?

### Essential definitions

- **CRUD** groups storage-like create, read, update, and delete operations; it is not an HTTP semantic model.
- **GET** requests transfer of a selected representation of the target resource and is safe.
- **POST** asks the target resource to process enclosed content according to its own semantics.
- **PUT** requests creation or complete replacement of target-resource state with the enclosed representation and is idempotent by intent.
- **DELETE** requests removal of the association between the target URI and current functionality; it does not require physical data erasure.
- A **precondition** makes a method conditional on known resource state, commonly using validators.
- An **ambiguous outcome** occurs when a client cannot know from its observation whether an unsafe operation took effect.

### Central model, mechanism, or theorem

Model resource lifecycle as state machine $(Q,\Sigma,\delta)$, where states include absent, active, archived, or tombstoned; stimuli combine method, target, representation, principal, and preconditions. HTTP constrains method intent and response meaning, while domain transition $\delta$ decides which state change is permitted. A `2xx` reports the request outcome, not universal durability or downstream business completion.

### Critical invariants

GET and HEAD never request unsafe effects. POST and PUT are chosen by target semantics and identifier ownership, not spelling preference. PUT represents complete desired target state unless a narrower media type contract says otherwise. State-changing requests validate authorization and preconditions before effects. Retries preserve logical-operation identity where duplicate effects matter. DELETE states its domain, retention, cascade, and restoration consequences. Responses truthfully distinguish enacted, accepted, rejected, and unknown outcomes.

### Common failures

Equating POST with create and PUT with update; using GET to trigger work; implementing PUT as undocumented merge; returning `200` before durable acceptance; using `404` for every domain conflict; deleting rows while leaving referenced invariants broken; assuming DELETE is physical erasure; retrying POST blindly after timeout; omitting `Location` after server-selected creation; and ignoring cache invalidation or lost updates.

### Compact example

A client knows desired URI `/profiles/ada` and sends `PUT` with a complete profile plus `If-None-Match: *`. If no current representation exists, the server can create it and return `201`; if one exists, the precondition fails with `412`. A retry after a lost response has the same intended state, but authorization, audit, and side effects must also be idempotent.

### Connections

HTTP method, status, idempotency, conditional, cache, resource, URI, and collection modules supply the protocol model. Partial Updates, Long-Running Operations, Bulk Operations, contracts, and error design refine cases that CRUD labels hide.

## Governing Question

What externally observable contract should each lifecycle operation have, and which HTTP method and response express that contract without overstating implementation guarantees?

## Why This Matters

CRUD is useful database vocabulary, but APIs mediate domain behavior across unreliable networks. “Update row” does not answer whether a representation is complete, whether concurrent work can be overwritten, whether an operation is retryable, or whether deletion revokes access, archives evidence, and cascades.

RFC 9110 defines GET, POST, PUT, DELETE, method safety and idempotency, success statuses, `Location`, validators, and conditional requests. RFC 9111 defines cache invalidation after successful unsafe methods. The protocol exposes request intent and response semantics while intentionally hiding implementation. Domain correctness still requires authorization, invariants, durability boundaries, and recovery.

This module uses “create/read/update/delete” to organize common lifecycle needs, then replaces the acronym with precise resource and method semantics. PATCH and partial-change formats belong to API-016.

## Prerequisites and Retrieval

Retrieve method semantics, status codes, resource versus representation, collection/member identity, idempotency, `ETag`, `If-Match`, `If-None-Match`, `Location`, caching, authentication, authorization, transactions, and timeout ambiguity. Recall that response loss and operation failure are different events.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish CRUD categories from HTTP method semantics;
2. select POST or PUT based on target meaning and identifier ownership;
3. design GET without unsafe effects and with explicit representation meaning;
4. define full replacement and omitted-field behavior for PUT;
5. specify DELETE as a domain lifecycle transition rather than storage erasure;
6. apply preconditions to creation, replacement, and deletion;
7. select truthful success, conflict, precondition, and asynchronous statuses; and
8. reason about retry, cache invalidation, concurrency, and ambiguous outcomes.

## Core Exposition

### Start with resource transitions, not controller names

For each operation, state target resource, initial state, requested transition, invariants, authoritative completion point, and observable result. Then select an HTTP method whose standardized intent matches. `createCustomer()` in code does not imply POST; client-selected stable identity can make PUT appropriate. `updateOrder()` does not justify PUT if the request is a command or partial mutation.

Storage CRUD collapses meaningful differences. Cancelling an order, approving a payment, rotating a key, and archiving a report may all update rows while having distinct authorization, retry, audit, and terminal-state contracts. Model those domain transitions directly.

### Read with GET and HEAD

GET requests transfer of a selected representation. It is safe: the client does not request a state change. Servers may log, measure, refresh a cache, or charge internal computation, but those incidental effects must not change the requested semantics. A crawler, prefetcher, retry, or cache can issue GET without consenting to purchase, delete, or enqueue work.

GET representation meaning needs freshness, authorization, content negotiation, validators, and absence semantics. `200` with a representation, `304` for a successful cache validator, `404` for no current target under disclosure policy, and `410` for intentionally gone are different. A `200` body containing `{found:false}` discards HTTP's resource-level outcome and can poison caches and client logic.

HEAD is GET without response content but with corresponding selected-representation metadata where applicable. It is useful for validators and metadata, not a cheaper authorization bypass. Implementations must avoid generating materially inconsistent GET and HEAD metadata.

### Create when the server selects identity

POST to a collection or factory-like resource is natural when the server chooses the new member URI or the target processes a submission. A successful creation commonly returns `201 Created` and a `Location` reference identifying the created resource. The response can contain its representation and validator or return minimal metadata under an explicit contract.

POST is not synonymous with create. It can append, submit, execute, process, or create subordinate resources according to the target. It is not idempotent by standardized intent, so a client timeout creates an ambiguous outcome. If duplicate effects matter, supply an operation/idempotency identity, lookup, retention window, request fingerprint, and conflict behavior.

Validate syntactic representation, authentication, authorization, domain invariants, quotas, and uniqueness before claiming creation. Distinguish malformed content, unsupported media type, forbidden action, semantic rejection, uniqueness conflict, and dependency unavailability rather than returning one generic `400`.

### Create or replace when the client selects identity

PUT targets the desired resource directly. The enclosed representation is intended to create or replace the state of that target. If the resource did not exist and is created, `201` is appropriate. If existing state is replaced, `200` can return a representation or `204` can report success without content.

PUT's idempotent intent means repeating the same request should have the same intended effect. Incidental audit records, metrics, or version timestamps must not create externally significant duplicate effects that violate the contract. If each retry sends email or appends a history event as a new domain effect, the implementation is not honoring the intended idempotence.

Use `If-None-Match: *` to request create-only at a known target and `If-Match` with a strong entity tag to prevent overwriting changed state. Preconditions are evaluated before performing the method; false conditions normally yield `412 Precondition Failed`.

### Define complete replacement

PUT means replacement of target state as represented, not “update whichever fields happen to be present.” The media type can define server-managed, computed, immutable, or omitted fields, but that rule must be explicit. If omitted optional fields retain old values unpredictably, PUT has become a hidden patch.

Clients need to know what representation they can round-trip. Server-generated identifiers, timestamps, and links may be read-only. Unknown fields can be rejected, ignored, or preserved according to compatibility policy. Blind read-modify-PUT can still erase fields the client does not understand; validators prevent concurrent overwrites, not schema ignorance.

Replacement must preserve domain invariants. A requested representation is desired externally visible state, not permission to set audit owners, balances, or derived risk decisions. The server can reject or transform content as allowed by the representation contract and must not return a validator for representation bytes it did not actually store or select consistently.

### Delete a URI association under domain policy

RFC 9110 describes DELETE as requesting removal of the association between target URI and current functionality. It does not guarantee physical bit erasure, cascade, immediate completion, or disappearance of every representation. The domain defines archive, tombstone, retention, legal hold, anonymization, restoration, and related-resource consequences.

After enacted deletion, `204` is appropriate when no status representation is needed; `200` can carry status; `202` means accepted but not yet enacted. A repeated DELETE may return the same successful terminal meaning, `404`, or `410` according to the disclosure and lifecycle contract. Do not let repeated calls create new destructive effects.

Request content on DELETE has no generally defined semantics and can interact badly with intermediaries. Prefer a distinct operation resource or explicit protocol when deletion needs reasons, approvals, schedules, or complex options.

### Separate acceptance from completion

`201`, `200`, and `204` report successful request handling at the documented boundary. If work has only entered a queue, use `202 Accepted`, expose an operation resource, and define progress, terminal outcome, cancellation, retention, and failure. Returning `200` while discarding work later lies about the lifecycle transition.

Define durability precisely. A database commit may not mean search indexing, event delivery, replica visibility, or fulfillment completion. The response contract can state which effects are authoritative at return and which are eventual. Do not claim universal consistency from one successful response.

### Make failures semantically useful

Different failure classes drive different recovery. Authentication missing, permission denied, target absent, invalid representation, current-state conflict, failed precondition, rate limit, dependency outage, and internal fault are not interchangeable.

Use `409 Conflict` when the request conflicts with current resource state and the client might resolve it under application semantics. Use `412` when an HTTP precondition evaluates false. Use `422 Unprocessable Content` for syntactically valid content that cannot be processed under its instructions where that meaning fits. Include stable machine-readable problem types and safe details, developed in later error modules.

Never expose sensitive existence through more precise failures than authorization policy permits. A uniqueness conflict can leak that an email is registered. Consistency across create, read, update, delete, and search matters.

### Handle concurrency explicitly

Without preconditions, two clients can GET version 7, edit independently, and PUT; the last write silently loses the first. Require `If-Match` for overwrite-sensitive resources and return a strong ETag with reads. The client refetches, reconciles, and retries intentionally.

When the origin requires a conditional request but none was supplied, `428 Precondition Required` from RFC 6585 can explain that the client must resubmit with a precondition. This differs from `412`, which reports that a supplied precondition evaluated false. A `428` response is not cacheable.

Preconditions protect the target representation under their validator model. They do not make a multi-resource invariant atomic unless the server implements an appropriate transaction or coordination mechanism. Updating an account with `If-Match` does not by itself protect a separate quota resource.

For create-if-absent at a client-selected URI, `If-None-Match: *` prevents accidental overwrite. Database uniqueness alone can implement part of the atomic decision, but the HTTP response and retry contract still need correct semantics.

### Account for caches and derived views

GET and HEAD responses may be cacheable under their controls. Successful unsafe requests invalidate cached responses for the target URI along the traversed cache path under RFC 9111. Other affected URIs, such as a parent collection, may require explicit invalidation, short freshness, validators, event-based purge, or versioned keys.

HTTP invalidation is not a global cache-coherence proof. A write through one path cannot reach every private cache or alternate route. Design freshness bounds and recovery for individual and collection representations, and ensure authorization dimensions appear in cache keys or prohibit shared storage.

### Recover from ambiguous outcomes

If a connection fails after sending an unsafe request, the client might not know whether the origin applied it. PUT and DELETE are idempotent by intent, but retries still need the same target, representation, preconditions, credentials, and domain operation identity. A stale `If-Match` on retry might fail after the original succeeded; RFC 9110 allows an origin to recognize already-successful duplicate state-changing requests, but this requires evidence.

For POST, use a logical-operation key or operation resource when retry is required. Store request fingerprint, outcome, and retention long enough for the recovery window. Never infer non-application from timeout, missing trace, or lack of immediate read-your-write visibility.

## Definitions and Notation

Let resource state machine be $(Q,\Sigma,\delta)$ with transition $\delta(q,x)=q'$ when stimulus $x$ is authorized and valid. Let validator $v(q)$ represent selected state for a declared representation. Conditional replacement with supplied validator $v_c$ is admissible only when strong comparison establishes $v_c=v(q)$ under the server's validator contract.

An operation is **safe** when the client does not request state change. It is **idempotent** when multiple identical requests have the same intended effect as one. **Creation** establishes a new resource mapping or member under the domain contract. **Replacement** supplies complete desired target state. **Deletion** changes availability or association under policy. **Durable acceptance** is the recorded point after which the system owns eventual resolution, not necessarily business completion.

## Mechanisms, Invariants, or Proof Structure

Design each lifecycle operation in this order:

1. Identify target resource and valid initial/terminal domain states.
2. State requested effect, invariants, authorization, and completion boundary.
3. Select GET, POST, PUT, or DELETE by standardized intent.
4. Define representation completeness, server-managed fields, and validation.
5. Define preconditions, concurrency scope, and duplicate-operation identity.
6. Choose status, `Location`, representation, validators, and problem details truthfully.
7. Define cache behavior and affected derived resources.
8. Define timeout ambiguity, retry, lookup, and retention.
9. Test related-resource, cascade, privacy, and partial-failure consequences.
10. Verify every response against authoritative state and declared evidence limits.

The **safe-read invariant** forbids requested effects on GET/HEAD. The **target-semantics invariant** distinguishes POST processing from PUT replacement. The **complete-replacement invariant** rejects undocumented merge behavior. The **precondition invariant** evaluates conditions before effects. The **outcome invariant** prevents accepted, enacted, durable, and business-complete states from being conflated.

## Alternatives and Trade-Offs

**Server-selected POST versus client-selected PUT.** POST centralizes identity allocation and supports arbitrary processing but needs explicit duplicate recovery. PUT enables deterministic target and idempotent replacement but exposes identity choice and requires complete-state semantics.

**Immediate versus asynchronous lifecycle.** Immediate responses simplify clients when effects fit bounded request latency. Asynchronous acceptance handles long or failure-prone workflows but adds operation identity, status, retention, cancellation, and eventual-failure handling.

**Hard delete versus tombstone/archive.** Hard deletion reduces retained data but can break audit and delayed references. Tombstones and archives preserve history and prevent reuse but carry privacy, cost, and authorization obligations.

**Unconditional versus conditional writes.** Unconditional last-write-wins is simple but can lose intent. Preconditions expose conflicts and require client reconciliation. Server-side merge can improve ergonomics only when domain semantics make conflicts safely composable.

## Failure Modes and Misconceptions

POST is not always create. PUT is not merely update. DELETE is not guaranteed physical erasure. GET with a “do” query remains unsafe if it triggers work. Idempotent does not mean side-effect-free, identical response, or safe. `202` does not mean completion. `204` cannot carry a response representation. A validator prevents only the conflicts represented by its scope. Successful cache invalidation along one path does not purge every cache. Timeout does not prove failure.

## Worked Examples

### Example 1

A crawler follows `GET /reports/9?send=true`, causing email delivery. Because GET is safe by contract, retries and prefetching send duplicates. The API models a delivery request as an unsafe operation instead. **Conclusion:** requested behavior, not endpoint naming, determines safety.

### Example 2

A client POSTs to `/orders`; the server selects `/orders/817`, commits the resource, returns `201`, `Location: /orders/817`, a representation, and ETag. **Conclusion:** POST to a collection plus Location expresses server-selected creation.

### Example 3

A client owns stable profile name `ada` and sends complete state to `/profiles/ada` with `If-None-Match: *`. Creation returns `201`; an existing target yields `412`. **Conclusion:** client-selected create-if-absent fits conditional PUT.

### Example 4

Existing profile has `name`, `locale`, and `timezone`. PUT body omits `timezone`; implementation silently preserves it. Another client expects replacement and expects it removed/defaulted. The media type is corrected to define every field and omission. **Conclusion:** undocumented merge violates PUT replacement semantics.

### Example 5

Two clients read ETag `"v7"`. First PUT with `If-Match: "v7"` succeeds and returns `"v8"`; second receives `412`, refetches, and reconciles. **Conclusion:** strong conditional replacement prevents silent lost update.

### Example 6

DELETE of `/users/42` removes login access but legal records must remain encrypted for seven years. Response `204` means the defined deactivation occurred, not every bit vanished. **Conclusion:** deletion semantics require domain retention and evidence boundaries.

### Example 7

A report deletion requires minutes. Returning `204` immediately falsely claims enactment. The API returns `202` with an operation resource and later terminal outcome. **Conclusion:** accepted and enacted are separate states.

### Example 8

A POST payment commits but its response is lost. Blind retry creates another payment. An operation key with request fingerprint returns the stored outcome for the replay. **Conclusion:** non-idempotent creation needs explicit ambiguous-outcome recovery.

### Example 9

PUT `/orders/7` succeeds, invalidating a cached individual response along its path, but `/orders?state=open` remains fresh in another cache. The design gives collection views validators and bounded freshness plus purge events. **Conclusion:** target invalidation is not global derived-view coherence.

### Example 10

Deleting a team is assumed to delete its documents, but policy requires ownership transfer. The server rejects with a resolvable conflict until a successor owner is assigned. **Conclusion:** domain invariants decide deletion admissibility; storage cascade is not the contract.

## Cross-Program Connections

[Collections and Individual Resources](014-collections-and-individual-resources.md) supplies membership boundaries; [Conditional Requests](006-conditional-requests.md), [Idempotency and Safety](008-idempotency-and-safety.md), and [Caching](007-caching.md) supply protocol mechanisms. API-016 develops partial updates, API-018 asynchronous operations, and API-019 batch semantics. Databases supply atomic mechanisms but not HTTP meaning; security supplies authorization and erasure policy.

## References

1. R. Fielding, M. Nottingham, and J. Reschke, *RFC 9110: HTTP Semantics*, Internet Standard 97, June 2022, Sections 9, 10.2.2, 13, and 15. Checked 2026-09-01. https://www.rfc-editor.org/rfc/rfc9110.html
2. R. Fielding, M. Nottingham, and J. Reschke, *RFC 9111: HTTP Caching*, Internet Standard 98, June 2022, Section 4.4. Checked 2026-09-01. https://www.rfc-editor.org/rfc/rfc9111.html
3. M. Nottingham and R. Fielding, *RFC 6585: Additional HTTP Status Codes*, Standards Track, April 2012, Section 3 (`428 Precondition Required`). Checked 2026-09-01. https://www.rfc-editor.org/rfc/rfc6585.html

## Exercises

### Exercise 1

Explain why POST=create, GET=read, PUT=update, and DELETE=delete is an incomplete mapping. Give one counterexample for POST, PUT, and DELETE.

### Exercise 2

Trace two concurrent complete replacements using GET, ETag, `If-Match`, and `412`. State exactly what conflict the validator detects and what it does not protect.

### Exercise 3

Diagnose an API that returns `200` immediately after enqueueing account deletion, sends DELETE request content through several proxies, and physically deletes audit rows before asynchronous work completes.

### Exercise 4

Compare POST to `/devices` and PUT to `/devices/{serial}` for device registration. Evaluate identity authority, duplicate retry, replacement completeness, unauthorized claims, and factory reset/re-registration.

### Exercise 5

A spacecraft can lose connectivity after transmitting a configuration change. Design create/read/replace/delete semantics for configuration resources under delayed messages, stale validators, non-reused identities, safety interlocks, and ambiguous outcomes.

## Answers to the Exercises

### Answer 1

HTTP methods express request intent toward a resource, while CRUD names broad storage effects. POST can submit a calculation or append an event without creating a retrievable resource. PUT can create a client-selected target as well as replace it. DELETE removes the target URI's association with current functionality but may archive data and retain related resources. GET maps most closely to read but also includes negotiation, validators, ranges, and cache semantics that database “read” omits.

### Answer 2

Both clients GET ETag `"v4"`. Client A sends complete representation A with `If-Match: "v4"`; the origin compares strongly, applies it, and publishes `"v5"`. Client B sends representation B with `If-Match: "v4"`; comparison fails and the server does not perform the method, returning `412`. This detects change to the selected target representation since B's observation. It does not automatically protect another resource, an invariant spanning several resources, external side effects, or fields excluded from validator state.

### Answer 3

`200` overstates completion if only queue acceptance is durable; return `202` with an operation resource and terminal states, or wait for the declared deletion boundary. DELETE content has no generally defined semantics and can be rejected or mishandled by intermediaries, so model reason/approval/schedule in a separately documented operation. Deleting audit evidence can violate retention and make recovery impossible; define deactivation, anonymization, legal hold, archive, cascade, and physical-erasure steps with authorization and rollback before enacting any effect.

### Answer 4

POST fits when the server owns device identity or registration is processing under collection semantics; it needs a logical-operation key or serial uniqueness plus replay lookup after timeout. PUT fits when the serial is an authorized, stable, non-reused public identity and the client supplies complete desired registration state; `If-None-Match: *` supports claim-if-absent and `If-Match` supports replacement. Attackers must not claim another device merely by knowing a serial. Factory reset and re-registration require explicit generation, ownership transfer, tombstone, and key-rotation policy rather than silent identity reuse.

### Answer 5

Give every configuration and change operation stable non-reused identity. GET returns signed/validated current configuration, observation time, and strong validator. Complete PUT requires `If-Match`, authorization, safety-envelope validation, and a durable operation identity; acceptance is distinct from activation. Delayed duplicates return the stored outcome for the same fingerprint. Stale validators fail before effects and require deliberate reconciliation. DELETE means deactivation/tombstoning under retention policy, never blind erasure of flight evidence. When contact is lost, ground systems query the operation and authoritative spacecraft state; neither timeout nor trace absence proves non-application. Safety interlocks dominate retry convenience.
