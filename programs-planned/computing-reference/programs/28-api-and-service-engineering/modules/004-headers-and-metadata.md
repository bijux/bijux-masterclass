---
module_id: API-004
program: API & Service Engineering
level: 1
module_number: 4
title: Headers and Metadata
status: complete
last_verified: 2026-09-01
---

# Headers and Metadata

## One-Page Review

### Governing question

How do HTTP fields add control, representation, routing, security, and operational meaning without becoming an invisible, contradictory second API?

### Essential definitions

- An HTTP **field** has a case-insensitive name and a value interpreted by that field's specification and message context.
- **Control data** describes the request or response itself: method, target, status, routing, or conditional behavior.
- **Representation metadata** describes representation data: media type, content coding, language, size, location, or validator.
- A **field list** is not automatically an ordered sequence of independent values; its combination rule is field-specific.
- An **end-to-end field** is intended for the complete request/response path, while a **hop-by-hop field** is specific to a connection or next recipient.

### Central model, mechanism, or theorem

For message $M$, treat a field as a typed relation $f:(name,value,context)\mapsto meaning$. Correctness requires $Parse_f(value)$ and $Allowed_f(context)$, then a coherent relationship with method, status, target, representation, and security policy. A string that merely resembles a header is not metadata until its specification, ownership, scope, and failure behavior are defined.

### Critical invariants

Use registered field semantics where they fit. Do not combine duplicate field lines unless the field definition permits it. Never forward connection-specific fields as end-to-end data. Make cache-affecting, auth-affecting, and routing-affecting fields explicit. Preserve one authority for each correlation, version, locale, and client preference. Treat headers as attacker-controlled input at every trust boundary.

### Common failures

Putting secret tokens in URLs; copying inbound `X-Forwarded-*` blindly; treating `Content-Type` as validation; emitting both conflicting `Content-Length` values; using a comma to join `Set-Cookie`; naming an unregistered private field without contract; logging credentials; trusting a client-supplied request ID; and returning an `ETag` without specifying what representation it validates.

### Compact example

A JSON response with `Content-Type: application/json`, `ETag: "v18"`, `Cache-Control: private`, and `Vary: Accept-Language` says more than its body: how to parse it, which selected representation was observed, who may reuse it, and which request dimension changes the selected variant. Leaving out `Vary` can cause one language to be served to another.

### Connections

Resources and representations provide the object of metadata. Status codes use `Location`, `Allow`, `WWW-Authenticate`, and `Retry-After`. Later modules cover negotiation, conditions, caching, authentication, tracing, and gateways. Network and security engineering explain intermediary trust and header injection.

## Governing Question

Which protocol facts must travel with this message, who may interpret or modify them, and what failure follows if their meaning is absent, duplicated, stale, or forged?

## Why This Matters

Fields determine behavior that bodies cannot safely carry alone. A client needs `Content-Type` before parsing a representation. A cache needs `Cache-Control` and `Vary`; an authenticated client may need `WWW-Authenticate`; an updater may need `ETag`; a recipient of a created resource may need `Location`. These are contracts with generic infrastructure as well as application code.

HTTP/1.1, HTTP/2, and HTTP/3 encode fields differently, but RFC 9110 defines their shared semantics. That separation matters: an application should not assume that its framework's map-like header API preserves wire order, duplicates, casing, or connection rules. Current registered names are maintained by IANA; Structured Fields, RFC 8941, offers a typed grammar for fields explicitly defined to use it.

## Prerequisites and Retrieval

Retrieve HTTP messages, resources, representations, status codes, media types, caches, proxies, TLS termination, authentication, and untrusted-input handling. From API-001, recall that representation data and its metadata are distinct. From API-003, recall that fields and status must communicate one outcome.

## Learning Objectives

By the end of this module, you should be able to:

1. classify a field by its role and path scope;
2. specify field ownership, syntax, cardinality, forwarding, and failure behavior;
3. distinguish request `Content-Type` from response selection and client `Accept` preferences;
4. reason about duplicate and list-valued fields safely;
5. design correlation and forwarding metadata across a trusted proxy boundary;
6. identify cache, redirect, authentication, and concurrency metadata; and
7. review field handling for security, privacy, and observability risks.

## Core Exposition

### Fields have semantics, not just names

An HTTP field is a name-value component of a message. Its name is case-insensitive, but its value grammar and combination rules come from the field definition. Some fields are lists, some are singletons, some have structured syntax, and some must not be combined. A framework that turns all duplicates into one comma-separated string is therefore unsafe by default: `Set-Cookie` is a familiar counterexample because its date syntax contains commas and each cookie is a separate field value.

Classify a field before adding it. **Control data** includes request-target and response status context. **Request context** can describe credentials, preconditions, preferences, or tracing. **Response context** can provide a location, retry interval, method allowance, or challenge. **Representation metadata** describes content. **Payload metadata** can identify the message content rather than a selected representation. **Connection fields** control one connection and must not be forwarded as end-to-end semantics.

### Scope, authority, and forwarding

At a proxy boundary, ask who is authoritative for each field. A public edge may remove any client-provided `Forwarded`, `X-Forwarded-For`, or correlation field and then add a trusted value. An origin must not infer the original scheme, host, client address, or authenticated identity from an arbitrary inbound value. A gateway's trust configuration—known peer, authenticated transport, overwrite rule, and allowed header set—is part of the API security model.

Hop-by-hop fields govern the current connection rather than the end-to-end request. RFC 9110's `Connection` field can nominate additional connection-specific fields for HTTP/1.1; they must not be forwarded. Modern protocol framing has additional rules, but the durable lesson remains: application metadata must not be confused with transport connection state. Intermediaries may add or transform permitted fields, so signed or security-sensitive metadata needs a defined canonicalization and trust boundary.

### Representation, negotiation, and validation metadata

`Content-Type` declares how to interpret message content. It is not a promise that the data conforms to an application schema, is authorized, or is safe. `Accept` expresses response media-type preferences; it does not label the request body. `Content-Encoding` identifies applied content codings, while `Content-Language` identifies intended audience language. These differ from a JSON field such as `language`, which is domain data and may be needed even when no natural-language representation selection occurs.

Validators such as `ETag` identify a selected representation for conditional requests and caching. They do not automatically name a database row version or prove business freshness. The service must specify whether a change of authorization-sensitive view, projection, locale, or media type changes the validator. If response selection depends on `Accept-Language`, a shared cache needs `Vary: Accept-Language` or an equivalent safe policy; otherwise it may reuse the wrong variant.

### Field design and private extensions

First search the IANA field-name registry and relevant specifications. Reuse a standard field only when its semantics exactly fit. A private field needs a durable name, syntax, cardinality, permitted request/response contexts, producer, consumers, intermediaries, privacy class, size limit, propagation rule, validation, error behavior, versioning story, and observability policy. Prefixing a name with `X-` does not solve ownership or collision; it often makes temporary conventions permanent.

Structured Fields can improve parsing for fields designed for RFC 8941: its dictionaries, lists, items, parameters, and binary values avoid ad hoc delimiter grammars. They are not a universal parser for existing fields. Do not apply a structured-field parser to a legacy field unless its definition explicitly adopts that syntax.

<!-- bijux-verify: {"id":"classify-field-scope","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"content-type=representation\nretry-after=response-control\nconnection=hop-by-hop\nvary=cache-selection\n","stderr":""}} -->
```python
roles = {
    "content-type": "representation",
    "retry-after": "response-control",
    "connection": "hop-by-hop",
    "vary": "cache-selection",
}

for name in ("content-type", "retry-after", "connection", "vary"):
    print(f"{name}={roles[name]}")
```

The run checks only this illustrative classification table. It does not validate a message parser, a proxy configuration, field syntax, cache behavior, or security policy.

## Definitions and Notation

Let $H(M)$ be the multiset of field lines in message $M$. For a field name $n$, $Values(n,M)$ is its received value sequence and $Rule_n$ is the field-specific parsing and combination rule. A field is **single-valued** when its definition permits at most one effective value; **list-valued** when its grammar specifies a list; and **non-combinable** when separate lines must remain separate.

An **authority boundary** is the point at which an actor becomes trusted to assert a field. A **selected representation** is the variant whose metadata appears in a response. A **cache key dimension** is a request property that changes selection and therefore must be represented in cache policy. A **correlation identifier** relates evidence about one operation; it is not authorization and must be bounded against spoofing and log injection.

## Mechanisms, Invariants, or Proof Structure

Use this field review sequence:

1. State the message direction, field role, and authoritative producer.
2. Cite the registered definition or write the complete private-field contract.
3. Define grammar, cardinality, duplicate behavior, size limit, and invalid-input response.
4. Define intermediary forwarding, overwriting, stripping, signing, and trust assumptions.
5. Define interaction with status, method, target, representation, cache, authentication, and logging.
6. Test absent, malformed, duplicate, oversized, forged, stale, and intermediary-modified cases.

The **field-coherence invariant** requires field semantics to agree with status and content. The **authority invariant** requires every security-relevant field to have one trusted producer at each boundary. The **selection invariant** requires every representation-selection dimension to be reflected in cache policy. The **non-combination invariant** prohibits generic joining of fields without their definition's permission.

## Alternatives and Trade-Offs

**Header versus body member.** Use a field for protocol, transport, representation, or intermediary semantics; use a body member for domain state. A body field is easier to version in a schema, but generic HTTP machinery cannot act on it.

**Standard versus private field.** A standard field gains interoperable behavior but carries its exact semantics. A private field can fit a bounded domain but demands documentation and proxy support. Do not overload `Content-Type`, `Authorization`, or `ETag` for unrelated purposes.

**Client-generated versus server-generated correlation ID.** Client IDs help end-to-end support, but must be validated and cannot be trusted as a security principal. Server-generated IDs have a clear authority but need an agreed propagation response field. Many systems retain both, with distinct names and roles.

## Failure Modes and Misconceptions

`Content-Type: application/json` does not validate JSON schema. A response body cannot replace `Location` when clients or generic tools need creation location semantics. `X-Forwarded-For` is not a client identity without a configured trusted proxy chain. A request ID is not a trace context, and a trace context is not authorization. A private cache without correct `Vary` can leak a personalized variant. A new header without a size limit can become a denial-of-service vector. Logging every header usually logs secrets.

## Worked Examples

### Example 1

A service receives two `Content-Length` values that disagree. The message framing is ambiguous and can enable request smuggling. Reject it at the HTTP boundary; do not choose the first value. The conclusion is that framing metadata is security-critical input.

### Example 2

A client sends JSON with `Content-Type: text/plain`. The bytes may look valid, but the declared request media type is unsupported by this endpoint. Return `415 Unsupported Media Type` if that is the documented contract. Parsing JSON anyway silently broadens the protocol.

### Example 3

An edge receives client-supplied `X-Forwarded-Proto: https`. It strips the field and emits its own value after authenticated TLS termination. The origin trusts only the edge's network identity. The conclusion is that forwarding metadata requires a trust boundary, not a naming convention.

### Example 4

An invoice is returned in English or French according to `Accept-Language`. The response sends `Vary: Accept-Language`; otherwise a shared cache could serve the first language variant to another user. The conclusion is that negotiation affects cache correctness.

### Example 5

An update response includes `ETag: "invoice-18"`. The contract says it identifies this JSON representation under this authorization projection, not a globally portable database version. A later conditional request can use it only under the documented comparison rules.

### Example 6

An API tries to merge two `Set-Cookie` headers with a comma. A cookie expiry date already contains a comma, so a client cannot reconstruct the intended cookies. Keep separate field lines. The conclusion is that duplicate handling is field-specific.

### Example 7

An origin returns `201 Created` but omits `Location`, forcing clients to parse an ad hoc `id` body member. Add the creation location where feasible. The body can add domain detail; the field supplies interoperable response context.

### Example 8

A service returns `429 Too Many Requests` with `Retry-After: 30`. A client respects 30 seconds but its own deadline is 5 seconds. It stops rather than waiting. The conclusion is that a field is a server hint within a broader request budget.

### Example 9

A team creates `X-User-Role` and lets a browser set it. An attacker sends `admin`. Replace it with authenticated server-side identity propagation under a gateway trust policy. The conclusion is that client-supplied headers cannot assert privileges.

### Example 10

A private `Trace-Token` is added for support. Its contract caps length, restricts characters, returns a server-generated token, redacts it from public analytics, and defines that it is correlation evidence only. The conclusion is that a private field needs full lifecycle ownership.

## Cross-Program Connections

[Resources, Representations, and Messages](001-resources-representations-and-messages.md) defines representation metadata's object. [HTTP Methods and Their Semantics](002-http-methods-and-their-semantics.md) supplies method context, and [Status Codes and Error Meaning](003-status-codes-and-error-meaning.md) supplies response-field context. Network engineering owns proxy topology; security engineering owns trusted identity and secret handling; later API modules apply these concepts to negotiation, caching, conditions, and gateways.

## References

- Fielding, R., Nottingham, M., and Reschke, J. *HTTP Semantics*, RFC 9110, IETF Standards Track, June 2022, Sections 5–8 and 16. Retrieved 2026-09-01. https://www.rfc-editor.org/rfc/rfc9110.html
- Nottingham, M., and colleagues. *Structured Field Values for HTTP*, RFC 8941, IETF Standards Track, February 2021. Retrieved 2026-09-01. https://www.rfc-editor.org/rfc/rfc8941.html
- Internet Assigned Numbers Authority. *Hypertext Transfer Protocol (HTTP) Field Name Registry*. Retrieved 2026-09-01. https://www.iana.org/assignments/http-fields/http-fields.xhtml

## Exercises

### Exercise 1

Explain why an API cannot define one generic duplicate-header rule, and give one combinable and one non-combinable field example.

### Exercise 2

Trace an `Accept-Language` request through response selection and a shared cache. Derive the cache-policy requirement.

### Exercise 3

Specify a private `Support-Case` response field: syntax, producer, cardinality, forwarding, privacy, size limit, invalid behavior, and what it must not be used for.

### Exercise 4

Compare trusting `X-Forwarded-For` directly with accepting it only from a configured edge that overwrites inbound values. Identify the threat and the residual assumptions.

### Exercise 5

Review a proposed response containing `200 OK`, `Content-Type: text/plain`, `ETag: "v2"`, and a JSON body saying that a conditional update failed. State all incoherences and design a correct response.

## Answers to the Exercises

### Answer 1

Field definitions choose their own combination semantics. A list-defined field such as `Accept` has grammar for multiple alternatives and can be interpreted under that grammar. `Set-Cookie` must remain separate because generic comma joining changes its parseability. A robust implementation stores received field lines and applies each field's defined rule rather than normalizing all names to one string.

### Answer 2

The request preference selects an English or French representation. Because the same URI can produce different responses as `Accept-Language` changes, a shared cache must key or vary reuse on that request field, normally by sending `Vary: Accept-Language`. Without it, the cache can reuse an English response for a French preference even when each origin response was individually correct.

### Answer 3

`Support-Case` can be a response-only ASCII token of at most 64 characters, emitted once by the support service and never accepted as client authority. Proxies may forward it unchanged only within the service trust domain; public logs redact it if it can link customer evidence. Invalid or duplicate values are rejected or discarded at the boundary by documented policy. It correlates a support case; it is not authentication, authorization, tracing context, or a resource identifier.

### Answer 4

Direct trust lets any client claim an address, possibly bypassing allowlists, rate limits, or audit attribution. A configured edge first discards client values, authenticates its upstream connection, and writes a controlled value, giving the origin a trusted producer. Residual assumptions remain: the edge configuration, internal network isolation, proxy-chain correctness, and IPv4/IPv6/address parsing all need review.

### Answer 5

`200` conflicts with a failed conditional update; it should ordinarily be `412 Precondition Failed`. `text/plain` conflicts with a JSON problem body and should be `application/problem+json` or the documented JSON media type. The `ETag` must describe a selected representation; if returning the current representation after failure, specify it accordingly, otherwise omit it. A correct response uses `412`, a coherent problem representation, safe detail, and the appropriate current validator only when its semantics are explicit.
