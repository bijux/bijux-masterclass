---
module_id: API-005
program: API & Service Engineering
level: 1
module_number: 5
title: Content Negotiation
status: complete
last_verified: 2026-09-01
---

# Content Negotiation

## One-Page Review

### Governing question

How should a server select one representation from the variants it can produce while preserving HTTP semantics, cache correctness, privacy, and predictable client behavior?

### Essential definitions

- A **variant** is one available representation of a resource, distinguished by media type, content coding, language, or another declared selection dimension.
- **Proactive negotiation** lets a client send preferences such as `Accept`, `Accept-Encoding`, or `Accept-Language`; the server selects a representation.
- **Reactive negotiation** returns alternatives or links and lets the client choose through another request.
- A **quality value** (`q`) expresses relative preference from 0 through 1; `q=0` means unacceptable.
- **Specificity** distinguishes an exact media range such as `application/json` from wildcards such as `application/*` or `*/*`.
- `Vary` identifies request fields that influenced selection so caches know when a stored response can be reused.

### Central model, mechanism, or theorem

Let $V$ be available variants and $P$ the client's declared preferences. A selection policy chooses $v^*\in V$ from acceptable candidates, or reports that none is acceptable. Preference is only one input: capability, authorization, quality, cost, safety, and server policy also constrain candidates. The chosen response must describe $v^*$ with accurate metadata and expose every request-field selection dimension through cache policy.

### Critical invariants

Never confuse request `Content-Type` with response `Accept`. Treat absent preference fields differently from explicit rejection. Apply wildcard, parameter, and quality semantics before server tie-breaking. Do not negotiate authorization: first restrict variants to those the principal may receive. Send accurate `Content-Type`, `Content-Encoding`, and `Content-Language`. Emit a correct `Vary` value or prevent unsafe shared reuse.

### Common failures

Returning JSON regardless of `Accept`; interpreting an absent `Accept` as JSON-only; treating `q=0` as lowest preference instead of rejection; selecting by list order alone; using filename suffixes while claiming header negotiation; compressing already compressed data wastefully; omitting `Vary`; and allowing language or media-type choices to reveal protected resource facts.

### Compact example

The server offers JSON and CSV. The client sends `Accept: text/csv;q=0.8, application/json;q=1`. Both are acceptable, so JSON wins by the declared preference. If the client sends `application/xml`, the server may return `406 Not Acceptable` because no offered representation matches; silently returning JSON makes the request contract false.

### Connections

Resources and representations define what is selected. Headers define preference and response metadata. Status codes define `406` and `415`. Later modules cover caching, validators, schemas, and versioning. Security engineering constrains variant visibility; internationalization determines language and locale behavior.

## Governing Question

Given a resource, a request, and a set of representations the service can safely produce, which representation should be returned—and what must every participant know for that choice to remain correct?

## Why This Matters

One resource can have JSON for automation, HTML for a browser, CSV for export, multiple natural languages, and compressed or identity-coded transfer. Creating a different URI for every technical encoding can expose implementation detail and fragment identity. Negotiation lets the resource remain stable while messages carry different representations.

The mechanism also creates risk. An incorrect algorithm surprises clients; an incomplete `Vary` value poisons cache reuse; a preference field can contribute fingerprinting information; an authorization-sensitive variant can leak through a shared cache; and excessive combinations can cause a variant explosion. Negotiation therefore needs an explicit bounded policy, not a library default accepted without review.

RFC 9110 defines proactive and reactive negotiation and the `Accept*` fields. RFC 9111 defines how `Vary` affects cache matching. Media-type tokens and registrations are maintained by IANA. These specifications define syntax and generic behavior; an API contract still has to state its available variants, default, failure behavior, and stability guarantees.

## Prerequisites and Retrieval

Retrieve resource identity, representation metadata, field parsing, status-code meaning, media types, wildcards, ordered preferences, authorization, and cache keys. Recall that `Content-Type` labels content already present in a message, while `Accept` expresses preferences for response content.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish proactive, reactive, and request-content negotiation;
2. compute acceptable media-type candidates using ranges, specificity, parameters, and quality values;
3. separate client preferences from server policy and authorization constraints;
4. specify defaults for absent fields and failure for unacceptable explicit preferences;
5. derive the required `Vary` dimensions for cache correctness;
6. reason about media type, language, charset, and content coding independently; and
7. test negotiation boundaries without creating an unbounded cross-product.

## Core Exposition

### Variants and selection dimensions

A variant is not merely a serializer output. It is a representation with data and metadata under a particular context. Variants may differ in media type (`application/json` versus `text/csv`), content coding (`gzip` versus identity), language (`en` versus `sv`), profile or media-type parameters, projection, or fidelity. Only some dimensions belong in generic HTTP negotiation. Authorization, tenant, and time also change representations but must be enforced as policy and cache isolation, not advertised as ordinary client preferences.

Build a finite variant inventory. For each variant state media type and parameters, language, available content codings, semantic completeness, audience, generation cost, cache policy, and stability. If ten independent dimensions each have three values, a theoretical cross-product contains $3^{10}=59{,}049$ combinations. Real systems should generate only meaningful supported variants and reject or default the rest deliberately.

### Proactive negotiation

In proactive negotiation the request carries preferences. `Accept` contains media ranges. An exact type is more specific than a subtype wildcard, which is more specific than `*/*`. Parameters can further constrain matching. A quality value weights relative preference; omission normally implies the default value defined by the field, while zero means the range is unacceptable.

Selection is not “take the first token.” Parse according to the field grammar, match each server variant against the applicable ranges, determine the controlling preference, discard unacceptable candidates, and then apply documented server tie-breaking. A service may prefer a cheaper representation among equal client preferences, but that policy should be stable enough for clients and caches to reason about.

An absent `Accept` means the user agent did not constrain media type through that field; it does not mean `application/json` unless the API declares JSON as its default. An explicit `Accept: application/xml` does constrain selection. If XML is unavailable and no wildcard or other range matches, `406 Not Acceptable` is appropriate when the server chooses not to disregard the preference.

### Languages and codings

`Accept-Language` negotiates natural language, not locale in every domain sense. A selected Swedish narrative may still contain ISO-formatted dates or invariant identifiers. Do not infer billing currency, legal jurisdiction, user identity, or authorization from a language preference. Language ranges can reveal user characteristics, so minimize variation and avoid logging unnecessary detail.

`Accept-Encoding` negotiates content codings such as compression. It does not negotiate media type. Compressibility, size, CPU cost, side-channel risk, intermediary support, and already compressed formats matter. The response's `Content-Encoding` must state the coding actually applied; omitting it after compression makes representation data uninterpretable.

Character encoding is largely governed by media-type rules and modern format specifications. Do not build a generic “charset negotiation” layer merely because older HTTP vocabulary included it. For JSON, follow JSON's current encoding rules rather than inventing per-request character-set variants.

### Reactive and explicit alternatives

Reactive negotiation exposes choices and lets the client select with another request. This can be implemented through links, a list of available formats, or distinct variant URIs. It costs another round trip but makes choice explicit, reduces opaque server scoring, and can improve caching. It is valuable when variants differ semantically or are expensive to generate.

URI suffixes such as `.csv` are not inherently wrong. They are explicit variant identifiers rather than pure proactive negotiation. The contract must decide whether `/reports/7`, `/reports/7.csv`, and a negotiated CSV response identify one resource, related variant resources, or different export jobs. Consistency matters more than aesthetic purity.

### Request-content negotiation

Request `Content-Type` declares the representation sent by the client. If the endpoint cannot process that media type, `415 Unsupported Media Type` is the relevant status, potentially with information about supported formats. This is distinct from `406`, which concerns producing an acceptable response representation. An API might accept JSON and CBOR requests while returning JSON only; the two capability sets need not be symmetric.

### Cache and privacy correctness

If request fields influence response selection, a cache needs that information. `Vary: Accept-Encoding` tells a cache that a stored response selected with one encoding preference cannot be assumed reusable for every other preference. Multiple dimensions may appear in `Vary`. `Vary: *` signals that unspecified request aspects influenced selection and prevents ordinary reuse; it is a correctness escape hatch with poor cache efficiency, not a routine substitute for understanding selection.

`Vary` does not replace access control or `Cache-Control`. If two authorized users receive different private views, naming `Authorization` in `Vary` is not by itself a complete safe caching policy. Decide whether the response is private, non-storeable, or safely partitioned by a controlled cache. Variant selection happens only after filtering to representations that the requester may receive.

<!-- bijux-verify: {"id":"negotiate-media-range","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"selected=application/json\nrejected=image/png\n","stderr":""}} -->
```python
offers = {"application/json", "text/csv"}
preferences = [
    ("application/json", 1.0),
    ("text/csv", 0.8),
    ("image/png", 0.0),
]

acceptable = [(quality, media) for media, quality in preferences if quality > 0 and media in offers]
selected = max(acceptable)[1]
print(f"selected={selected}")
print("rejected=image/png")
```

This executable example checks one exact-match toy policy. It does not implement RFC 9110 wildcard precedence, parameters, duplicate ranges, parsing, caching, or authorization.

## Definitions and Notation

Let $V$ be the finite set of server variants. Each $v\in V$ has attributes $m(v)$ for media type, $l(v)$ for language, $c(v)$ for content coding, and $a(v)$ for its authorization predicate. For request $r$, define the authorized candidates $V_r=\{v\in V\mid a(v,r)=true\}$. Preference matching assigns a score only within $V_r$.

A **media range** matches one or more media types. A **wildcard** broadens the range. A **quality value** is a normalized preference weight, not a probability or server performance guarantee. A **server tie-breaker** is policy used after client preference comparison. A **default variant** is the documented result when the relevant preference is absent or underspecified.

## Mechanisms, Invariants, or Proof Structure

Use this selection procedure:

1. Identify the target resource and request method.
2. Enumerate implemented, current, and authorized variants.
3. Parse each applicable preference field; reject malformed input by documented policy.
4. Match specificity, parameters, and quality values; remove `q=0` candidates.
5. Apply stable server tie-breakers among remaining candidates.
6. If none remains, select the documented failure or reactive-alternative behavior.
7. Emit accurate representation metadata and the selected content.
8. Emit complete cache variation and storage controls.
9. Record the decision without logging sensitive preference or identity data unnecessarily.

The **authorization-first invariant** is $Selected(r)\in V_r$. The **metadata invariant** requires response metadata to describe the bytes actually transferred. The **cache-selection invariant** requires any request field used by selection to be represented in `Vary` or an equivalently safe non-shared policy. The **determinism invariant** requires the same offers, preferences, and policy version to yield the same selection.

## Alternatives and Trade-Offs

**Header negotiation versus explicit format URI.** Headers preserve one resource identifier and use HTTP machinery. Explicit URIs improve discoverability, links, and cache keys. Either can work if resource identity and variant relationships are documented.

**Strict `406` versus default fallback.** Strict rejection respects explicit client constraints and detects integration errors. Fallback may improve human browsing when preferences are broad or misconfigured. Never choose a representation explicitly excluded with `q=0`; document any policy that disregards other preferences.

**Many variants versus a narrow contract.** More variants broaden accessibility and client choice but multiply tests, cache entries, source-of-truth questions, security review, and evolution obligations. Offer variants with clear consumer value and owned lifecycle.

## Failure Modes and Misconceptions

A quality value is not a probability. Header order alone is not preference. `Accept` does not label request content. `Content-Type` does not say what response the client wants. `Vary` does not authorize users. Language preference does not define locale, nationality, or legal jurisdiction. Compression support does not mean compression is always beneficial or safe. Returning an undocumented default after explicit rejection hides contract errors.

## Worked Examples

### Example 1

The server offers JSON and CSV. `Accept: text/csv;q=0.8, application/json;q=1` makes both acceptable and JSON more preferred. Select JSON and emit `Content-Type: application/json`. The conclusion follows from quality after matching, not server list order.

### Example 2

The request has no `Accept`. The API contract names JSON as its default. Return JSON; do not pretend the absence is the same as `Accept: application/json`. The distinction matters if the default changes or a generic client accepts any type.

### Example 3

The client sends `Accept: application/json;q=0, */*;q=0.5`. The more specific range rejects JSON even though the wildcard is positive. If JSON is the only offer, no acceptable candidate remains. Return the documented `406` outcome rather than selecting JSON.

### Example 4

The server offers `application/json` and `application/problem+json`. A request for `application/*` matches both. The endpoint's outcome and server policy choose the semantically appropriate representation; wildcard matching does not erase the distinction between success and problem formats.

### Example 5

A report is available in English and Swedish. `Accept-Language: sv, en;q=0.7` selects Swedish. The response emits `Content-Language: sv` and `Vary: Accept-Language`. The body remains governed by the same domain facts; only its natural-language representation varies.

### Example 6

A client accepts `gzip`, but the response is a tiny, already compressed image. The server uses identity coding under its cost policy and states metadata accurately. A preference makes a coding acceptable, not mandatory unless the contract and field semantics make alternatives unacceptable.

### Example 7

`POST /imports` receives `Content-Type: application/xml`, while only JSON input is supported. Return `415`. This is request-content capability, not `406`; the service might still be able to produce an acceptable JSON problem response.

### Example 8

A cache stores an English JSON response selected by `Accept` and `Accept-Language`, but the origin emits only `Vary: Accept`. A later French client receives English. Add both selection fields to `Vary` or use a safer caching design. One omitted dimension invalidates reuse.

### Example 9

An administrator can receive a detailed JSON variant; a viewer cannot. The server first filters by authorization, then applies both users' identical `Accept` values. The viewer must never receive the administrator variant. Negotiation ranks allowed variants; it does not expand permissions.

### Example 10

An export has expensive PDF and cheap HTML variants with equal client quality. A stable server policy prefers HTML for ordinary requests and offers an explicit PDF job link. This avoids unpredictable load while preserving choice. The tie-breaker is documented production policy, not an accidental serializer order.

## Cross-Program Connections

[Resources, Representations, and Messages](001-resources-representations-and-messages.md) defines variants. [Headers and Metadata](004-headers-and-metadata.md) defines field parsing, trust, and `Vary`; [Status Codes and Error Meaning](003-status-codes-and-error-meaning.md) separates `406` from `415`. Caching, conditional requests, API contracts, accessibility, security, and internationalization all consume the selection model developed here.

## References

- Fielding, R., Nottingham, M., and Reschke, J. *HTTP Semantics*, RFC 9110, IETF Standards Track, June 2022, Section 12. Retrieved 2026-09-01. https://www.rfc-editor.org/rfc/rfc9110.html
- Fielding, R., Nottingham, M., and Reschke, J. *HTTP Caching*, RFC 9111, IETF Standards Track, June 2022, Section 4.1. Retrieved 2026-09-01. https://www.rfc-editor.org/rfc/rfc9111.html
- Internet Assigned Numbers Authority. *Media Types Registry*. Retrieved 2026-09-01. https://www.iana.org/assignments/media-types/media-types.xhtml

## Exercises

### Exercise 1

Distinguish `Accept`, `Content-Type`, `Content-Encoding`, and `Accept-Language` by direction and meaning.

### Exercise 2

The server offers JSON and CSV. Trace selection for `Accept: text/*;q=0.6, application/json;q=0.9, text/csv;q=0`. State the result and why.

### Exercise 3

Design the negotiation contract for an invoice available as JSON and localized PDF. Include defaults, explicit rejection, language, authorization, caching, and failure behavior.

### Exercise 4

Compare header negotiation with `/invoices/7.pdf`. Explain resource identity, caching, discoverability, and evolution trade-offs.

### Exercise 5

An API selects variants using `Accept`, `Accept-Language`, tenant, and authorization but returns `Cache-Control: public` with no `Vary`. Diagnose the failures and propose a safe design.

## Answers to the Exercises

### Answer 1

`Accept` is a request preference for response media type. `Content-Type` labels content actually carried in either request or response. `Content-Encoding` states a coding applied to carried content. `Accept-Language` is a request preference for natural language of the response. None substitutes for another, and none alone establishes schema conformance or authorization.

### Answer 2

JSON matches the exact `application/json` range at `q=0.9`. CSV matches both `text/*;q=0.6` and the more specific `text/csv;q=0`; the specific rejection controls, so CSV is unacceptable. Select JSON. The wildcard cannot override the explicit exclusion of CSV.

### Answer 3

Define JSON as the default when `Accept` is absent, support `application/json` and `application/pdf`, and return `406` when every offered type is explicitly unacceptable. For PDF, select only supported languages and state the fallback rule; emit `Content-Language`. Filter variants by invoice authorization before preference ranking. Emit `Vary` for the actual preference fields and make tenant/user-specific invoices private or non-storeable rather than relying on `Vary` as access control.

### Answer 4

Header negotiation keeps one invoice URI and makes representation choice part of the request, but caches need correct `Vary` and links may not expose the PDF choice clearly. A `.pdf` URI creates an explicit link and cache key, but the contract must state whether it identifies a representation-specific resource or a variant of the invoice. Explicit URIs often suit downloadable artifacts; header negotiation suits interchangeable views of one resource.

### Answer 5

The response is unsafe because public caches can reuse a tenant- or authorization-specific representation, and absent `Vary` hides both declared selection fields. First authorize and isolate tenant data. Prefer `Cache-Control: private` or `no-store` unless a controlled cache has a proven partition key. Add `Vary: Accept, Accept-Language` for those negotiation dimensions. Do not place tenant or credential values in a public variation scheme as a substitute for access control.
