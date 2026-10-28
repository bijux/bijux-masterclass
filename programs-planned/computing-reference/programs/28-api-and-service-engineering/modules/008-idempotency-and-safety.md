---
module_id: API-008
program: API & Service Engineering
level: 1
module_number: 8
title: Idempotency and Safety
status: complete
last_verified: 2026-09-01
---

# Idempotency and Safety

## One-Page Review

### Governing question

What may clients and intermediaries automate safely when requests can be duplicated, retried, prefetched, reordered, or completed without a visible response?

### Essential definitions

- A method is **safe** when its defined request semantics are essentially read-only: the client does not request an origin-state change.
- A method is **idempotent** when the intended effect of several identical requests is the same as the intended effect of one.
- **Retry safety** is a request-specific operational judgment involving method semantics, replayability, deadlines, authorization, conditions, and evidence about prior application.
- An **incidental side effect** such as logging each request does not change an idempotent method's intended-effect classification.
- **Deduplication** recognizes repeated logical operations. It is a mechanism, not proof of idempotency or exactly-once execution.
- An **ambiguous outcome** occurs when a client cannot tell whether an effect happened, commonly after losing the response.

### Central model, mechanism, or theorem

Let $E(r,S)$ be the intended state effect of request $r$ on server state $S$. Request semantics are idempotent when $E(r,E(r,S))=E(r,S)$ for all states in the contract domain. This equation concerns the requested effect, not identical responses, zero side effects, commutativity with other requests, or fault-free execution. Safe semantics imply idempotent intended effects, but idempotent semantics need not be safe.

### Critical invariants

Safe methods must not hide requested mutation behind query parameters. Idempotent retries must preserve target, semantic fields, content, conditions, principal, and operation identity. Retrying must remain within a deadline and a bounded attempt policy. A deduplication record and the authoritative effect must become consistent under a defined atomicity design. Never convert an ambiguous non-idempotent outcome into a retry based only on a `5xx` class or connection error.

### Common failures

Using GET to delete; assuming “no database write” proves safety; assuming PUT responses are identical; treating idempotency as commutativity; retrying POST after a lost response without operation identity; expiring deduplication state before clients stop retrying; reusing one idempotency key for different payloads; and claiming exactly-once real-world effects because duplicates were suppressed locally.

### Compact example

Two identical `PUT /profiles/p7` requests replace the selected state with the same complete representation. The second may create another audit record and return a different timestamp, yet the intended resource effect converges to the same state. Two identical `POST /charges` requests can create two charges unless the application defines one logical operation and enforces its identity.

### Connections

HTTP methods provide registered safety and idempotency properties. Conditional requests protect state assumptions. Status codes and timeouts communicate partial evidence. Later modules cover idempotency keys, concurrency control, retries, asynchronous messages, and distributed failure amplification.

## Governing Question

Which effects does the request ask for, and what can a client conclude when it must decide whether to repeat that request without knowing whether the earlier attempt was applied?

## Why This Matters

Networks duplicate, delay, lose, and reorder observations. A client can send a request, the origin can commit it, and the response can disappear. Method semantics let generic clients reason conservatively about repetition. Safe methods support crawling and prefetching without requesting mutation. Idempotent methods allow repetition after communication failure because repeated intended effects converge.

These classifications are frequently overclaimed. They do not promise that servers never log, bill internally, emit metrics, or return different responses. They do not prove that downstream systems deduplicate, that a request body can be replayed, that credentials remain valid, or that a client still wants the effect. Engineering retry behavior requires the protocol property plus a concrete failure model and evidence boundary.

RFC 9110 is the current standards authority for safe and idempotent HTTP methods. Fielding's REST dissertation explains why uniform-interface semantics enable intermediaries. An IETF working-group draft proposed an `Idempotency-Key` field for non-idempotent methods, but revision 07 is expired as of retrieval; it is useful design evidence, not an Internet Standard. Production APIs using such a field must publish their own precise contract. Detailed key implementation belongs to API-037.

## Prerequisites and Retrieval

Retrieve method semantics, resources, state transitions, conditional requests, client deadlines, retries, transactions, unique constraints, and the difference between a request, an attempt, and a logical operation. Recall that a missing response is evidence about communication, not proof that the origin did nothing.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish safety, idempotency, retry safety, and deduplication;
2. prove or refute idempotence for a bounded state-transition model;
3. explain why safe implies idempotent while the converse fails;
4. classify GET, PUT, DELETE, POST, and PATCH without relying on CRUD slogans;
5. design bounded recovery after ambiguous completion;
6. identify atomicity and retention requirements for operation deduplication; and
7. review automation, security, and downstream effects without claiming exactly once.

## Core Exposition

### Safety concerns requested semantics

A safe method asks to retrieve or inspect rather than change origin state. GET, HEAD, OPTIONS, and TRACE are safe under RFC 9110. An implementation can still append logs, update metrics, charge an advertising account as an incidental effect, or warm a cache. Safety focuses on what the user requested and can be held responsible for.

This boundary enables automation. Crawlers follow links, browsers prefetch, caches revalidate, and monitoring probes repeat requests. A route such as `GET /documents/7?delete=true` violates GET semantics even if convenient. The unsafe action is selected by the target, but the method still promises safe semantics to generic software.

Safety is not the same as confidentiality, cheapness, or freedom from failure. A safe report query can expose sensitive data, consume large resources, or trigger a bug. Those concerns need authorization, limits, and operational controls. Method safety answers one narrower question: did the client request a state-changing effect?

### Idempotency concerns intended effects

Let a request define state transition $E_r$. Idempotence means applying that same transition twice produces the same intended state as applying it once. Setting a value to 10 is idempotent: `set(10); set(10)` ends at 10. Incrementing by 1 is not: two applications end two units higher.

PUT and DELETE are idempotent by method semantics. Repeating a complete replacement has the same intended effect; repeating removal preserves absence of the target association. Responses can differ: the first DELETE might return `204`, the second `404`; the intended deletion effect is still idempotent. Servers can create two audit entries without changing the classification because those are incidental rather than requested effects.

Idempotency is not commutativity. `PUT value=A` followed by `PUT value=B` ends at B, while the reverse ends at A. Each request is individually idempotent, but distinct requests do not commute. Idempotency is also not immutability: an idempotent request can change state on its first application.

### POST, PATCH, and application semantics

POST is not classified as idempotent because its general semantics allow processing that creates a new subordinate resource or effect on every request. A particular POST contract can define one logical operation and make repetitions converge, but clients need evidence of that contract and a stable operation identity.

PATCH is not generally idempotent. A patch that sets `/status` to `closed` can be idempotent in an application; a patch that increments `/attempts` is not. Patch media type, base version, preconditions, and operation semantics decide. Do not label an endpoint idempotent merely because a happy-path test repeated it once.

### Retry after ambiguous completion

Consider three states: the origin definitely rejected the request, definitely applied it, or application is unknown to the client. A response can provide evidence for the first two, but a connection failure often leaves the third. For an idempotent and replayable request, a bounded retry can recover because repeated intended effects converge. For a non-idempotent request, retry requires operation identity, authoritative status lookup, or evidence that the request was never applied.

Even an idempotent method is not automatically retryable. A streaming body may be non-replayable. A signed request may expire. `If-Match` may cease to hold. Authorization may change. A deadline may have passed. The client may have been canceled. Retry policy therefore combines method semantics with request and user context.

### Operation identity and deduplication

A deduplication key identifies one logical operation across attempts. The server needs a scoped uniqueness rule, a fingerprint of semantically relevant request data, a lifecycle state, a stored outcome or status reference, concurrency behavior, retention, and conflict handling when the same key arrives with different content.

The critical race is between recording the key and applying the effect. If the effect commits but the key does not, a retry can duplicate the effect. If the key commits first and the process fails before the effect, later attempts can be blocked forever. Designs use one transaction where possible, a durable operation resource, an outbox/workflow, or a recoverable state machine. None turns an external payment network into exactly-once execution automatically.

Retention must cover the maximum legitimate retry horizon plus clock and delivery uncertainty. After eviction, the same key can be treated as new. APIs must document this boundary. Deduplication state can contain sensitive fingerprints and outcomes, so it needs authorization, tenant scoping, quotas, and erasure policy.

### Bounded automated behavior

A safe retry policy names eligible methods or operations, maximum attempts, backoff with jitter, total deadline, retryable evidence, replay requirements, and a terminal recovery path. Retry budgets must be coordinated across callers, gateways, and downstream clients; otherwise three attempts at each of four layers can amplify one operation into $3^4=81$ attempts.

Rate limits, `Retry-After`, and `5xx` statuses are inputs, not permission. A `503` can follow an already committed unsafe operation whose response path failed. A `429` can outlive the caller's deadline. Clients must prefer authoritative operation lookup over blind repetition when state is ambiguous.

<!-- bijux-verify: {"id":"idempotent-transition-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"set-idempotent=True\nincrement-idempotent=False\nretry-amplification=81\n","stderr":""}} -->
```python
def set_ten(state):
    return {**state, "value": 10}

def increment(state):
    return {**state, "value": state["value"] + 1}

initial = {"value": 0}
print(f"set-idempotent={set_ten(set_ten(initial)) == set_ten(initial)}")
print(f"increment-idempotent={increment(increment(initial)) == increment(initial)}")
print(f"retry-amplification={3 ** 4}")
```

This execution verifies two finite transition comparisons and one multiplication. It does not prove a production endpoint idempotent, a transaction atomic, a retry safe, or an external effect deduplicated.

## Definitions and Notation

Let $S$ be authoritative state, $r$ one semantic request, and $E_r:S\to S$ its intended-effect transition within an explicit domain. Idempotence is $E_r\circ E_r=E_r$. Requests $r_1$ and $r_2$ commute only if $E_{r_1}\circ E_{r_2}=E_{r_2}\circ E_{r_1}$; this independent property is not implied by idempotence.

An **attempt** is one transmission/processing occurrence. A **logical operation** groups attempts intended to cause one business effect. A **request fingerprint** binds operation identity to relevant target, method, content, principal, and conditions. A **retry horizon** is the maximum time during which another attempt may legitimately refer to the same operation.

## Mechanisms, Invariants, or Proof Structure

Review an operation in this order:

1. State the client-requested effect and its authoritative state boundary.
2. Classify method safety and idempotency from semantics, not handler naming.
3. Model repetition on initial, already-applied, stale, and concurrent states.
4. Identify incidental and downstream effects separately.
5. Define request replayability, deadline, cancellation, and authorization behavior.
6. For non-idempotent recovery, define operation identity, fingerprint, atomicity, status, and retention.
7. Bound retries and amplification across every layer.
8. Test response loss before receipt, before commit, after commit, and during downstream work.

The **semantic identity invariant** requires all attempts grouped under one operation to have the same relevant fingerprint. The **atomic-record invariant** requires deduplication state and the authoritative effect to reach a recoverable consistent state. The **retention invariant** requires operation evidence to outlive legitimate retries. The **bounded-automation invariant** caps attempts and total time across the call graph.

## Alternatives and Trade-Offs

**Naturally idempotent operation versus deduplication key.** A set/replace semantic is simpler and survives deduplication-record loss. Keys can protect create or command semantics but add state, retention, fingerprint, and recovery complexity. Prefer a naturally convergent model when it matches the domain.

**Synchronous replay versus operation lookup.** Replaying an eligible request is simple. A durable operation resource provides stronger recovery for long-running or costly effects and exposes terminal status. It requires lifecycle, authorization, retention, and cleanup design.

**Reject duplicates versus return stored outcome.** Rejection signals that a key was seen but forces clients to discover the outcome elsewhere. Returning the stored result improves recovery but requires safe response retention and rules for headers, status, representation evolution, and authorization changes.

## Failure Modes and Misconceptions

Safe does not mean authorized or cheap. Idempotent does not mean side-effect-free, commutative, or response-identical. A UUID does not provide deduplication without server enforcement. A unique database row does not deduplicate external effects committed outside that transaction. “Exactly once” cannot be inferred from one service's key table. Automatic retries without a total budget amplify overload. An expired Internet-Draft is not a finalized HTTP standard.

## Worked Examples

### Example 1

`GET /reports/7?delete=true` removes a report. Although GET is defined as safe, the handler implements requested mutation. Crawlers or prefetchers can delete data. Move deletion to an unsafe method and disable it under GET. The method promise governs automation.

### Example 2

Two identical PUT requests replace a profile with `{name: "Ada"}`. The second adds another access-log entry and returns a later `Date`, but the requested profile effect is unchanged. The operation remains idempotent; response equality was never required.

### Example 3

The first DELETE removes a membership and returns `204`; the second finds none and returns `404`. Both leave the membership absent. This counterexample shows that different statuses do not refute idempotent intended effects.

### Example 4

`PATCH {"op":"increment","path":"/credits","value":1}` applies twice and adds two credits. Repetition changes the intended result, so this patch is non-idempotent. Replacing credits with a specific value could be idempotent under appropriate conditions.

### Example 5

A client sends POST to create a charge, the origin commits it, and the response is lost. Blind retry creates another charge. A durable operation identity or authoritative charge lookup is required; a connection error does not prove non-application.

### Example 6

Two concurrent attempts use one operation key but different amounts. The server compares fingerprints and rejects the mismatch rather than returning the first result. Key equality without semantic identity would let a caller accidentally or maliciously alias distinct operations.

### Example 7

The charge commits, then the process crashes before writing its deduplication row. A retry duplicates the charge. The design moves intent and operation state into a recoverable transaction/workflow and reconciles external provider identity. A separate key table was insufficient.

### Example 8

A client retries after 24 hours, but the service retained keys for only one hour. The same key is now new. Either extend retention beyond the published retry horizon or require status lookup/manual recovery after expiry. Silent key reuse makes the contract time-dependent and unsafe.

### Example 9

Four layers each make up to three attempts. The worst-case request count is $3\times3\times3\times3=81$. Centralize or budget retries, propagate deadlines, and ensure downstream work is not multiplied independently. Local resilience can create global failure amplification.

### Example 10

A PUT body is streamed from a one-shot source. The method is idempotent, but after a connection failure the client cannot reproduce identical content. The attempt is not replayable. Buffer safely, use resumable transfer, or surface an ambiguous outcome rather than confusing method idempotency with transport replayability.

## Cross-Program Connections

[HTTP Methods and Their Semantics](002-http-methods-and-their-semantics.md) defines method properties, [Conditional Requests](006-conditional-requests.md) protects stale state assumptions, and [Status Codes and Error Meaning](003-status-codes-and-error-meaning.md) bounds recovery evidence. Distributed systems owns delivery ambiguity and exactly-once limitations; database engineering owns transaction and uniqueness mechanisms; API-037 later develops idempotency-key implementation in depth.

## References

- Fielding, R., Nottingham, M., and Reschke, J. *HTTP Semantics*, RFC 9110, IETF Standards Track, June 2022, Sections 9.2.1–9.2.2. Retrieved 2026-09-01. https://www.rfc-editor.org/rfc/rfc9110.html
- Fielding, R. *Architectural Styles and the Design of Network-based Software Architectures*, doctoral dissertation, University of California, Irvine, 2000, Chapter 5. Retrieved 2026-09-01. https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm
- Jena, J., and Dalal, S. *The Idempotency-Key HTTP Header Field*, draft-ietf-httpapi-idempotency-key-header-07, October 2025, expired Internet-Draft as of retrieval 2026-09-01; cited as non-standard design evidence. https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/

## Exercises

### Exercise 1

Distinguish safe, idempotent, retryable, and deduplicated with one sentence and counterexample for each.

### Exercise 2

For transitions `set status=closed`, `append audit entry`, and `increment balance`, determine idempotence by applying each twice.

### Exercise 3

Design recovery for a POST payment after the client loses the response. Include identity, fingerprint, atomicity, status lookup, retention, and authorization.

### Exercise 4

Compare naturally idempotent PUT replacement with POST plus an idempotency key for creating a client-known resource.

### Exercise 5

A gateway retries three times, the service retries a dependency four times, and the dependency sends two attempts to an external provider. Calculate amplification and redesign the budget.

## Answers to the Exercises

### Answer 1

Safe means the client requests no origin-state change; a safe GET can still be expensive or logged. Idempotent means repeated identical requested effects converge; DELETE can return different responses and remain idempotent. Retryable means this attempt can be reproduced within deadline and evidence constraints; an idempotent PUT with a one-shot body is not replayable. Deduplicated means a mechanism recognizes one logical operation; a key table can still fail to cover an external effect.

### Answer 2

Setting status to closed twice leaves the same intended status as setting it once, so that transition is idempotent. Appending one audit entry twice creates two entries, so the append transition is not idempotent if the entry is the requested effect; incidental request logging is classified separately. Incrementing balance twice changes it by two increments, so it is not idempotent. The proof is direct comparison of $E(E(S))$ with $E(S)$.

### Answer 3

Assign one tenant-scoped operation ID and bind it to target, amount, currency, beneficiary, principal, and conditions through a canonical fingerprint. Atomically record intent and local transition, or use a durable workflow/outbox that can reconcile the provider's own operation identity. Repeated matching attempts return or link to the same authorized operation; mismatched fingerprints fail. Retain evidence beyond the documented retry horizon and provide an authenticated status resource for ambiguous outcomes.

### Answer 4

If the client can choose the target URI and complete desired representation, conditional PUT with `If-None-Match: *` gives natural create-if-absent and convergent replay semantics. POST suits server-selected identity or command processing but needs an additional logical-operation contract and durable deduplication. PUT is simpler only when replacement semantics truthfully match the domain; forcing an event-like command into replacement would be misleading.

### Answer 5

The uncoordinated worst case is $3\times4\times2=24$ provider attempts per original request. Give the end-to-end operation one deadline and identity, permit retries at one chosen layer, and cap provider attempts within the remaining budget. Other layers should propagate failure or perform status lookup rather than multiply attempts. Add jitter and load shedding, but recognize that those controls do not repair missing operation identity.
