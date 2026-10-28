---
module_id: API-006
program: API & Service Engineering
level: 1
module_number: 6
title: Conditional Requests
status: complete
last_verified: 2026-09-01
---

# Conditional Requests

## One-Page Review

### Governing question

How can a client make retrieval or mutation depend on the server's current representation state without inventing a private concurrency protocol?

### Essential definitions

- A **validator** is response metadata used to compare a selected representation with a prior observation.
- An **entity tag** is an opaque validator; a strong tag supports byte-for-byte representation comparison, while a weak tag indicates semantic equivalence under the origin's definition.
- `Last-Modified` is a date validator with limited resolution and origin-controlled meaning.
- A **precondition** is a request predicate evaluated against the selected representation before the method is performed.
- `304 Not Modified` is a conditional retrieval response; `412 Precondition Failed` reports a false precondition for other applicable methods.
- `428 Precondition Required` is a policy response requiring clients to make a request conditional.

### Central model, mechanism, or theorem

Let $S$ be current selected-representation state and $P_i(S)$ the predicates supplied by conditional fields. The origin evaluates applicable predicates in the RFC-defined order before performing the requested method. It performs the method only when their conjunction permits it; otherwise it returns `304` or `412` according to method semantics. This is compare-before-act at one authoritative boundary, not a distributed transaction.

### Critical invariants

Validators belong to selected representations, not abstract resources in isolation. Use strong comparison where byte identity or lost-update protection requires it. Evaluate conditions only after ordinary request checks and only when the method would otherwise be performed. Preserve RFC precedence when several conditions appear. Make the comparison and protected state change atomic at the owning authority. Never treat a client timestamp as an authoritative validator.

### Common failures

Reading then writing in separate transactions; using weak tags with `If-Match`; generating one tag for several authorization-specific variants; comparing second-resolution dates for high-rate updates; treating `304` as an empty `200`; returning `409` for every stale validator; letting a proxy evaluate domain state it does not own; and claiming conditional requests prevent all concurrent anomalies.

### Compact example

A client retrieves a document with `ETag: "v7"`, edits it, then sends `PUT` with `If-Match: "v7"`. If the current tag is still `"v7"`, the origin applies the replacement atomically and emits a new validator. If another update produced `"v8"`, the condition is false and the origin returns `412`; the client retrieves, reconciles, and retries deliberately.

### Connections

Headers carry validators and conditions; status codes communicate `304`, `412`, and `428`. Methods determine whether a condition protects retrieval or mutation. Caching consumes validators for revalidation. Later modules cover idempotency, concurrency control, versioning, and distributed consistency.

## Governing Question

What exact fact did the client previously observe, and how can the next method be performed only if that fact still holds at the authority that owns the representation?

## Why This Matters

Without conditions, a cache must download a representation again to learn that it has not changed, and two editors can overwrite one another silently. Conditional requests reuse standard HTTP metadata to avoid unnecessary transfers and to guard writes against stale observations. The same mechanism supports “create only if absent,” “modify only if unchanged,” and “send a range only if it still belongs to the same representation.”

The protection is bounded. A validator can represent the state chosen by one origin for one variant; it does not make several services commit atomically, prove a business invariant, or merge concurrent intent. A correctly rejected stale write still needs a product-level recovery workflow.

RFC 9110 defines validators, conditional fields, precedence, and response behavior. RFC 9111 specifies cache revalidation. RFC 6585 defines `428 Precondition Required`, which lets an origin state that unconditional mutation is unsafe by policy.

## Prerequisites and Retrieval

Retrieve representations, methods, response metadata, status codes, atomic compare-and-swap, timestamps, authorization-dependent views, cache freshness, and the lost-update problem. Recall that an `ETag` is opaque to clients: clients store and return it rather than deriving meaning from its characters.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish strong and weak validators and choose the needed comparison;
2. apply `If-Match`, `If-None-Match`, date conditions, and `If-Range` to their intended cases;
3. trace the standard precondition evaluation order;
4. distinguish `304`, `412`, `409`, and `428`;
5. design an atomic lost-update guard at an API boundary;
6. generate variant-correct validators without exposing sensitive internals; and
7. state what conditional requests do not guarantee across services and time.

## Core Exposition

### Validators name observations

An entity tag is an opaque quoted token assigned by the origin to a selected representation. A strong entity tag changes whenever representation data would differ under strong comparison. A weak tag, written with `W/`, can remain equal across changes the origin considers semantically insignificant. Weakness is explicit because some uses need exact representation identity.

The tag need not be a database version, hash, or timestamp. A version counter can work when every byte-affecting selection input changes the counter. A digest can work when canonical representation bytes and disclosure risks are controlled. A random revision identifier can work when stored atomically. Exposing a raw row version may leak write frequency or couple the public contract to storage. The durable requirement is validator semantics, not a favored generator.

`Last-Modified` represents the origin's belief about modification time. Dates have coarser resolution and clock limitations; multiple changes within one second may be indistinguishable. Entity tags are generally preferable when correctness depends on exact state. Dates remain valuable where file-like modification time is meaningful or tag generation is unavailable.

### Retrieval revalidation

A cache or client with an entity tag sends `If-None-Match`. For GET or HEAD, if a current selected representation matches, the origin returns `304 Not Modified` rather than transferring the representation data. The response still carries metadata needed to update the stored response. A `304` is not a normal success with a mysteriously missing body; it has specific revalidation semantics and applies to a stored representation.

`If-Modified-Since` provides date-based revalidation. When both entity-tag and date conditions are supplied, RFC precedence prevents a recipient from inventing an arbitrary conjunction. `If-None-Match` takes precedence over `If-Modified-Since` because entity tags are generally more precise. Implement the specified ordering, including method applicability, instead of evaluating fields in map iteration order.

### Mutation guards

`If-Match` requires the current selected representation to match one of the supplied entity tags under strong comparison. It is the usual lost-update guard for PUT, PATCH, or DELETE. The wildcard form `If-Match: *` requires a current representation to exist, useful when a method must not create a missing target.

`If-None-Match: *` expresses the opposite existence condition: perform the method only if no current representation exists. This supports create-if-absent at a client-selected URI. The comparison and creation must occur atomically inside the authority; an application-level read followed later by insert still races.

`If-Unmodified-Since` is a date-based mutation guard when entity tags are unavailable. Its resolution makes it weaker for rapid changes. A service should not accept a body member such as `updatedAt` as an equivalent precondition unless it explicitly defines and enforces the same authoritative atomic comparison.

### Status and evaluation timing

Conditional fields are evaluated only when the request would otherwise produce a success or redirect under ordinary processing. Authentication, authorization, method applicability, and basic request validity are not bypassed by a matching validator. This ordering prevents conditions from becoming an existence oracle or from masking an unauthorized request.

A false conditional GET/HEAD revalidation yields `304`; a false condition for other methods normally yields `412`. `428` means the request omitted a condition the origin requires. `409 Conflict` is different: it reports a conflict with current resource state that is not simply the false HTTP precondition. Keep protocol predicate failure distinct from domain reconciliation.

If the requested state change is already reflected, RFC semantics allow an origin in limited circumstances to report success rather than `412`, but only when it can verify that the same user agent's requested change already succeeded. Do not generalize this into guessing about duplicated operations; use operation identity and idempotency mechanisms where required.

### Atomicity and scope

The authority must evaluate the validator and apply the mutation in one concurrency boundary: one transaction, compare-and-swap, conditional write, or equivalent serialization mechanism. A handler that loads version 7, checks it, then performs an unconditional write after another transaction commits version 8 has implemented a check-shaped race, not a precondition.

Validators are representation-specific. JSON and CSV variants can have different bytes and strong tags. Language, content coding, projection, or authorization may affect the selected representation. The origin must avoid a tag that lets one user infer another user's version or causes a cache to validate the wrong variant. `Vary`, cache partitioning, and access control remain part of correctness.

### Ranges and `If-Range`

`If-Range` combines a range request with a validator. If the validator matches, the server may send the requested partial representation. If it does not, the server ignores the range and sends the complete selected representation. This prevents a client from stitching bytes from different revisions. It is not a general mutation precondition and uses stricter validator rules appropriate to byte ranges.

<!-- bijux-verify: {"id":"compare-and-update","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"first=updated:v8\nsecond=precondition-failed:current-v8\nvalue=beta\n","stderr":""}} -->
```python
state = {"tag": "v7", "value": "alpha"}

def conditional_put(expected_tag, value):
    if state["tag"] != expected_tag:
        return f"precondition-failed:current-{state['tag']}"
    next_version = int(state["tag"][1:]) + 1
    state.update(tag=f"v{next_version}", value=value)
    return f"updated:{state['tag']}"

print(f"first={conditional_put('v7', 'beta')}")
print(f"second={conditional_put('v7', 'gamma')}")
print(f"value={state['value']}")
```

The single-process trace checks one in-memory comparison and update. It does not prove database transaction isolation, crash durability, distributed serialization, authorization, or correct HTTP parsing.

## Definitions and Notation

Let $R_u(c)$ be the selected representation of resource $u$ under context $c$, and $tag(R_u(c))$ its entity tag. Strong comparison $=_s$ requires both tags to be non-weak and character-for-character equal; weak comparison $=_w$ ignores the weakness distinction when opaque values match as specified.

For current state $S$, a mutation precondition $P(S)$ guards transition $T$. Correct implementation has the atomic form `if P(S) then S := T(S)`, not a separately observable read/check/write sequence. A **lost update** occurs when a later write based on stale state overwrites an intervening write without deliberate reconciliation.

## Mechanisms, Invariants, or Proof Structure

Use this review procedure:

1. Identify the selected representation and every dimension that changes it.
2. Choose strong entity tags, weak tags, or dates according to the comparison claim.
3. Emit validators only after successful selection and authorization.
4. Parse conditions and apply RFC precedence and method applicability.
5. Evaluate conditions at the authoritative state boundary.
6. Perform the comparison and protected method atomically.
7. Return `304`, `412`, `428`, or the ordinary method result with coherent metadata.
8. Test absent, matching, stale, weak, wildcard, variant, duplicate, race, and response-loss cases.

The **atomic guard invariant** requires no intervening write between predicate evaluation and transition. The **variant invariant** requires a validator to compare only representations within its defined selection context. The **opacity invariant** forbids clients from depending on the validator's internal generation scheme. The **precedence invariant** requires the same conditional fields to produce the RFC-defined decision regardless of header storage order.

## Alternatives and Trade-Offs

**Entity tag versus modification date.** Tags can represent exact revisions and avoid clock resolution limits, but require careful variant-aware generation. Dates are familiar and cheap for file-like resources but weaker under rapid or derived changes.

**Conditional request versus domain command version.** `If-Match` gives interoperable HTTP precondition semantics. A domain version in a command may be useful across non-HTTP transports or aggregate boundaries. If both exist, define one authoritative comparison and keep failures coherent rather than creating two races.

**Reject stale write versus automatic merge.** Rejection preserves intent and lets a user resolve conflicts. Automatic merge improves flow for provably commutative or field-independent changes but needs explicit merge laws, conflict evidence, and tests. A validator mismatch alone does not prove a merge is safe.

## Failure Modes and Misconceptions

An ETag is not automatically a hash, row version, or resource version. Weak tags are not suitable for `If-Match` strong comparison. A `304` response does not mean the resource never changed; it means the selected representation matches under the evaluated condition now. `If-Match` does not serialize changes in other services. An atomic database update without correct variant semantics can still validate the wrong representation. A client must not manufacture tags or interpret `v9` as ordered after `v8` unless a separate contract says so.

## Worked Examples

### Example 1

A client caches JSON with `ETag: "j7"` and later sends GET with `If-None-Match: "j7"`. The representation still matches, so the origin returns `304` with the required current metadata. The client reuses its stored body. The conclusion is transfer avoidance, not a new representation body.

### Example 2

Two editors retrieve tag `"v4"`. Editor A updates with `If-Match: "v4"` and receives `"v5"`. Editor B submits `"v4"`; the origin atomically sees `"v5"` and returns `412`. B must retrieve and reconcile, so A's work is not silently overwritten.

### Example 3

A client sends `PUT /keys/k1` with `If-None-Match: *`. No current representation exists, so creation succeeds. A simultaneous request loses the atomic create race and receives `412`. A prior GET check would not provide this guarantee.

### Example 4

A client sends DELETE with `If-Match: *` for a missing target. The existence condition is false and yields `412`. This communicates “perform only if present,” which differs from an unconditional DELETE's ordinary missing-target behavior.

### Example 5

The server emits `W/"summary-7"` for semantically equivalent HTML layouts. A client sends it in `If-Match` for a write. Strong comparison fails because the tag is weak. The conclusion is that semantic cache validation and lost-update protection have different comparison needs.

### Example 6

A resource changes twice within one second while `Last-Modified` remains at second resolution. `If-Unmodified-Since` can miss the intervening update. Use a strong entity tag when the write guard needs revision precision.

### Example 7

A request contains both `If-None-Match` and `If-Modified-Since`. The implementation follows RFC precedence and evaluates the entity-tag condition; it does not require both conditions or whichever field the framework returns first. Deterministic precedence prevents client and intermediary disagreement.

### Example 8

An endpoint requires guarded updates but receives PATCH without a precondition. It returns `428 Precondition Required` with instructions to retrieve an ETag and resubmit with `If-Match`. The request was not stale; it lacked required concurrency evidence.

### Example 9

A client requests bytes 100–199 with `If-Range: "file9"`, but the current tag is `"file10"`. The server sends the complete current representation rather than mixing old and new byte ranges. The conclusion is representation integrity across resumed transfer.

### Example 10

An API checks `If-Match` in application code, commits the check transaction, then issues an unconditional write. Another transaction updates between those steps, and the stale write wins. Moving comparison into the conditional database update restores atomicity. HTTP syntax alone never supplied the missing concurrency mechanism.

## Cross-Program Connections

[Headers and Metadata](004-headers-and-metadata.md) defines validator field handling, [Content Negotiation](005-content-negotiation.md) defines selected variants, and [Status Codes and Error Meaning](003-status-codes-and-error-meaning.md) distinguishes precondition outcomes. Database engineering supplies conditional updates and transactions; distributed systems bounds what one authority can guarantee; later API modules extend this model to caching, idempotency, and boundary concurrency.

## References

- Fielding, R., Nottingham, M., and Reschke, J. *HTTP Semantics*, RFC 9110, IETF Standards Track, June 2022, Sections 8.8 and 13. Retrieved 2026-09-01. https://www.rfc-editor.org/rfc/rfc9110.html
- Fielding, R., Nottingham, M., and Reschke, J. *HTTP Caching*, RFC 9111, IETF Standards Track, June 2022, Section 4.3. Retrieved 2026-09-01. https://www.rfc-editor.org/rfc/rfc9111.html
- Nottingham, M., and Fielding, R. *Additional HTTP Status Codes*, RFC 6585, April 2012, Section 3. Retrieved 2026-09-01. https://www.rfc-editor.org/rfc/rfc6585.html

## Exercises

### Exercise 1

Distinguish strong and weak entity tags and identify one appropriate use for each.

### Exercise 2

Trace two concurrent PUT requests that both begin from `ETag: "v12"`. State the atomic operations and outcomes.

### Exercise 3

Design create-if-absent behavior for `PUT /aliases/green` using a standard precondition, including success and failure responses.

### Exercise 4

Compare `412`, `409`, and `428` for update failures and give a recovery path for each.

### Exercise 5

A multilingual resource emits one ETag for English and Swedish, is publicly cached, and accepts `If-Match` updates. Diagnose the risks and propose a validator/cache design.

## Answers to the Exercises

### Answer 1

A strong tag identifies representation data precisely enough for strong comparison and is appropriate for `If-Match` lost-update guards or range integrity. A weak tag declares semantic equivalence despite permitted byte differences and suits cache revalidation where those differences do not matter. A weak tag cannot satisfy strong `If-Match` comparison merely because its opaque text matches.

### Answer 2

Each request performs an atomic conditional transition: update from version 12 only where the current version equals 12. One request wins, stores its value, and changes the validator to `"v13"`. The other condition then matches zero current rows and maps to `412`. If both independently read 12 and later write unconditionally, the guard is broken and a lost update remains possible.

### Answer 3

The client sends PUT with `If-None-Match: *`. The origin atomically inserts only when no current representation exists. Success returns the normal creation outcome, commonly `201` with `Location` and a new validator. If another representation already exists or wins a concurrent insertion, the origin returns `412`. A preceding HEAD request is useful discovery but cannot replace the atomic precondition.

### Answer 4

`412` means a supplied HTTP precondition evaluated false; retrieve current state and validator, reconcile, and retry conditionally. `428` means the required precondition was absent; retrieve a validator and resubmit. `409` means a current domain-state conflict not reducible to the failed conditional field; follow the problem-specific resolution, such as choosing another name or transition. The statuses communicate different missing evidence and recovery.

### Answer 5

One strong tag is invalid if English and Swedish bytes differ, and shared caching without language variation can serve the wrong representation. Generate variant-correct tags and emit `Vary: Accept-Language`, or use explicit variant URIs with safe cache keys. For updates, compare against the authoritative state version rather than accidentally treating a language-specific presentation tag as the whole domain version; if the public contract exposes both, document their relationship and keep comparison atomic and authorization-safe.
