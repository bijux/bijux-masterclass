---
module_id: API-013
program: API & Service Engineering
level: 1
module_number: 13
title: URI Design
status: complete
last_verified: 2026-09-01
---

# URI Design

## One-Page Review

### Governing question

How can an API assign stable, unambiguous, safe, and evolvable URI references to resource identities without turning paths into brittle implementation protocols?

### Essential definitions

- A **URI** is a compact character sequence that identifies an abstract or physical resource.
- A **URI reference** is either a URI or a relative reference resolved against a base URI.
- The generic components are `scheme`, `authority`, `path`, `query`, and `fragment`; their meanings depend on position and scheme.
- **Percent-encoding** represents an octet as `%` followed by two hexadecimal digits; it is component-sensitive encoding, not generic string escaping.
- **normalization** transforms a URI into an equivalent form under justified syntax- or scheme-specific rules.
- **canonical URI** is the owner-selected preferred identifier among aliases.
- A **URI template** expands named variables under defined operators and encoding rules; it is not a URI until expanded.

### Central model, mechanism, or theorem

Parse before interpreting: $U=(s,a,p,q,f)$ denotes scheme, authority, path, query, and fragment. Resolution is a function $\operatorname{resolve}(B,R)=T$ from absolute base URI $B$ and reference $R$ to target URI $T$. Equality of raw strings implies syntactic equality, but different strings can be equivalent under scheme or owner rules; aggressive normalization without authority can merge distinct resources.

### Critical invariants

URI meaning is controlled by its scheme and owning authority. Stable identifiers outlive deployment and storage changes. Components are constructed structurally, never by unsafe concatenation. Path segments, query data, and fragments are encoded according to their distinct grammars. Relative references have a defined base. Canonicalization never changes resource identity. Sensitive, mutable, or high-cardinality data is excluded unless its exposure and lifecycle are intentional.

### Common failures

Embedding database topology or service names; putting actions into every path; treating `/` inside data as path syntax; double-encoding `%`; decoding before structural parsing; changing case in path segments; normalizing with filesystem rules; placing secrets in queries; using fragments as server inputs; resolving relative references against the wrong base; and forcing URI conventions on namespaces owned by others.

### Compact example

For base `https://api.example/orders/42/`, reference `../items?state=open#top` resolves to `https://api.example/orders/items?state=open#top`. The query identifies within the owner-defined resource namespace; `#top` identifies a secondary resource for the client and is not sent in an HTTP request target. Replacing the base with `https://api.example/orders/42` changes the result because the last path segment is then treated as a file-like segment during resolution.

### Connections

Resource Identification decides what URI meaning must remain stable. Collections, filtering, pagination, methods, links, caching, signatures, authorization, gateways, and versioning all depend on exact URI processing. Security engineering owns injection, disclosure, and canonicalization threats.

## Governing Question

Which URI structures preserve resource meaning, interoperability, security, and independent evolution across clients, intermediaries, deployments, and time?

## Why This Matters

URIs cross more boundaries than most API implementation details. They appear in links, caches, logs, browser history, signatures, metrics, events, documentation, allowlists, redirects, and stored business records. A seemingly cosmetic spelling decision can become a compatibility and security contract.

RFC 3986 defines generic URI syntax, reference resolution, normalization, comparison, and security considerations. RFC 9110 applies URI references to HTTP targets and relationships. RFC 8820, BCP 190, updates RFC 3986 with current guidance about URI design and ownership and obsoletes RFC 7320. RFC 6570 defines interoperable URI Templates. These standards define syntax and protocol responsibilities; the resource owner still defines application meaning.

Readable paths can help people and operations, but readability is subordinate to stable identity and correct processing. A URI is an identifier, not a promise that internal files, tables, classes, or service topology have the same hierarchy.

## Prerequisites and Retrieval

Retrieve resource identity, representation, HTTP request targets, origins, percent-encoded octets, Unicode and UTF-8, cache keys, redirects, signatures, same-origin boundaries, and authorization. Recall that URI comparison has a purpose and that the fragment component is excluded from the HTTP request target.

## Learning Objectives

By the end of this module, you should be able to:

1. parse and explain the generic components of URI references;
2. distinguish path hierarchy, query data, and client-side fragments;
3. apply percent-encoding at the correct structural layer;
4. resolve relative references using an explicit base URI;
5. choose stable owner-controlled paths without leaking implementation topology;
6. define conservative canonicalization, redirect, and alias policy;
7. use URI Templates without unsafe string substitution; and
8. diagnose traversal, disclosure, ambiguity, and signature failures.

## Core Exposition

### Begin with ownership and resource meaning

URI design follows resource identification. First decide which concept is identified and who owns its namespace. Then choose a stable reference. RFC 8820 warns specifications against imposing substructure on URI authorities and paths they do not own. An application can define its own paths under delegated authority; a generic extension should prefer links, fields, or templates rather than commandeering `/api`, a query name, or a hostname convention everywhere.

Do not encode changeable organization charts, deployment regions, shard numbers, database tables, or microservice names unless they are genuinely part of public resource identity. `https://api.example/eu-west-3/order_service_v2/orders/42` makes routing and implementation into client commitments. An intermediary can route a stable `/orders/42` to new infrastructure without changing its meaning.

Human-readable identifiers have value when their lifecycle is stable and their disclosure is safe. Opaque identifiers avoid rename and enumeration coupling but do not provide authorization. Whichever form is chosen, the owner must define case, normalization, non-reuse, aliases, and lifetime.

### Parse the generic components

RFC 3986 gives the generic form:

<!-- bijux-verify: {"id":"generic-uri-grammar","mode":"schematic","language":"text","toolchain":"none","reason":"The block reproduces the conceptual generic URI component grammar for explanation and is not an executable program."} -->
```text
URI = scheme ":" hier-part [ "?" query ] [ "#" fragment ]
```

For `https://api.example:8443/orders/42?view=summary#payment`, the scheme is `https`, the authority is `api.example:8443`, the path is `/orders/42`, the query is `view=summary`, and the fragment is `payment`. Delimiters are syntax only in their relevant positions; an encoded `%2F` represents an octet within a component and is not automatically interchangeable with `/` as a path separator.

The authority determines the HTTP origin together with scheme and effective port. Host names are case-insensitive, while path and query components are generally case-sensitive unless the owner defines otherwise. Lowercasing an entire URI is therefore unsafe.

Fragments identify a secondary resource according to the representation's media type or other context. User agents remove the fragment before HTTP transmission. A server cannot require `#token` as an authorization input because it never receives it in the request target. Fragments may still appear in browser history or client telemetry.

### Design paths as stable hierarchy

Path hierarchy is useful when it expresses durable containment or navigation. `/orders/42/items/7` can communicate that item `7` is scoped within order `42`, but only if reparenting and independent identity agree with that structure. Deep nesting through mutable organization membership makes references unstable.

Use consistent owner-defined conventions for collection and member paths, but do not mistake grammar preferences for protocol semantics. HTTP method semantics do not come from nouns, plurals, or file extensions in the path. A `GET` remains safe because the method defines it, not because a URI lacks a verb.

Action-like resources can be legitimate when the action has durable identity or lifecycle: `/exports/9` can identify an export operation. Paths such as `/orders/42/cancel` often hide whether cancellation is an unsafe command, a new request resource, or a state transition. Decide the domain model before spelling.

Avoid artificial file extensions for content negotiation unless the suffix is genuinely part of identification. `/reports/9.json` and `/reports/9.csv` may identify two formats of one resource, two distinct generated artifacts, or aliases; the contract must say which. Header-based negotiation preserves one resource identity when formats are representations.

### Use queries for owner-defined identification or control

The query component is part of the URI and can identify a distinct resource. In an API, it commonly expresses filtering, projection, sorting, pagination, or search. Whether `?state=open` identifies a stable filtered collection or modifies processing of one collection is an application semantic decision.

Do not assume query order or duplicate-name handling is universally insignificant. `?tag=a&tag=b`, `?tag=b&tag=a`, and `?tag=a,b` are distinct strings; the API must define parsing and equivalence if it accepts them. Libraries vary in whether `+` means space, whether empty values are retained, and how malformed percent encodings are handled. `application/x-www-form-urlencoded` rules are not the generic URI query grammar.

Query values are routinely copied into logs, metrics, browser history, referrers, caches, traces, analytics, and support tools. Credentials, session tokens, personal identifiers, and sensitive search terms therefore need stronger design. Authorization headers or protected request content are usually safer, though all channels require explicit controls.

### Percent-encode at the component boundary

Percent-encoding represents the UTF-8 octets of data characters that cannot appear literally or would conflict with reserved syntax. Construct components from data, encode each component according to its grammar, then assemble the URI. Do not concatenate raw user input and encode the whole result afterward; that either hides intended delimiters or preserves attacker-controlled ones.

Suppose an order key is the data string `north/42`. As one path segment it must not introduce hierarchy; `/orders/north%2F42` preserves the slash octet as segment data if the application and stack retain that distinction. Some frameworks decode `%2F` before routing or reject it. A safer public identifier alphabet may avoid this portability hazard entirely.

Encode once. If `%2F` is encoded again it becomes `%252F`, changing data. Decode only after the URI has been parsed into components and only at the layer that owns the component grammar. Repeated decoding can turn `%252e%252e` into traversal syntax after validation has already passed.

Unicode text is encoded as UTF-8 octets before percent-encoding where required. Unicode normalization, visually confusable characters, and internationalized domain names are separate concerns; never invent equality rules by normalizing identifiers without the naming authority's contract.

### Resolve relative references with an explicit base

Relative references improve portability of representations and allow deployments under different authorities or prefixes. Their meaning depends completely on a base URI. RFC 3986 Section 5 defines resolution, including path merging and removal of complete `.` and `..` segments.

The trailing slash matters. Against `https://example.test/a/b/`, reference `c` resolves to `/a/b/c`; against `https://example.test/a/b`, it resolves to `/a/c`. A representation producer must establish the intended base, and tests must cover redirects and proxy rewriting that can change the effective base.

Never implement reference resolution with filesystem joining or string concatenation. URI paths use slash-delimited syntax but are not local filesystem paths. Backslash, drive letters, network paths, encoded dots, and repeated slashes have platform- and application-specific risks.

### Compare and canonicalize conservatively

Exact string equality is cheap and safe evidence of URI equivalence when comparable characters are used. Different strings may still identify the same resource. RFC 3986 describes a comparison ladder: syntax normalization can lowercase scheme and host, uppercase percent-encoding hex digits, decode encodings of unreserved characters, and remove dot-segments; scheme rules add defaults such as effective ports.

Do not apply these rules blindly to signatures, routing, access control, cache partitioning, or application identity. Every component must be parsed first, and every additional equivalence needs authority. Path case folding, trailing-slash removal, query sorting, duplicate removal, and Unicode normalization can merge distinct owner-defined identifiers.

Choose a canonical URI for generated links and advertise aliases with controlled redirects or link relations. Permanent redirects affect caches and clients; preserve method semantics with the correct status when redirecting unsafe requests. Avoid redirect chains and loops. During origin migrations, retain old authority long enough to honor stored links and define downgrade, credential, and cross-origin policy.

### Use URI Templates as typed expansion rules

RFC 6570 templates express references such as `/orders/{id}{?fields,lang}` with defined operators and percent-encoding. A template variable is data, not pre-encoded URI syntax unless the selected expansion operator explicitly allows reserved characters. Avoid home-grown replacement like `template.replace("{id}", raw)`.

Templates describe possible identifiers; they do not grant authorization, validate domain values, or prove that every expansion exists. Publish variable types, maximum lengths, allowed values, omission behavior, and sensitivity. Treat received URIs as untrusted even when clients were given a template.

### Design for operational and security boundaries

Bound URI length and component counts even though RFC 9110 recommends support for at least 8000 octets in protocol elements. Application limits must be documented and produce safe errors across gateways and origins. Excessive queries can exhaust parsing, logging, signature, or cache resources before application code runs.

Normalize once at a defined trust boundary and preserve both a safe original form and canonical parsed form only when needed. Route, authorize, sign, and cache using compatible interpretations. If a gateway authorizes `/public/%2e%2e/admin` differently from the origin after decoding, the boundary is exploitable.

Metrics should use route templates rather than raw URIs to avoid cardinality and disclosure. Logs should redact sensitive query values and control characters. Never reflect a raw URI into HTML or headers without context-appropriate output encoding.

## Definitions and Notation

Represent parsed URI $U$ as tuple $(s,a,p,q,f)$. Let $B$ be an absolute base URI and $R$ a reference; $\operatorname{resolve}(B,R)$ is the RFC 3986 target URI. Let $N_c(U)$ be a canonicalization function for a declared comparison context $c$. A sound policy requires $N_c(U_1)=N_c(U_2)$ only when treating $U_1$ and $U_2$ as equivalent is safe for context $c$.

A **reserved character** can delimit syntax in a component. An **unreserved character** is an ASCII letter, digit, hyphen, period, underscore, or tilde. An **octet** is eight bits; percent-encoding works on octets. A **base URI** establishes the context for relative resolution. An **absolute URI** has a scheme. A **network-path reference** begins `//` and inherits the base scheme; it is often undesirable in security-sensitive API content because it can switch authority.

## Mechanisms, Invariants, or Proof Structure

Use this design and processing sequence:

1. Resolve the resource identity and owning naming authority.
2. Define stable path hierarchy and query semantics without implementation topology.
3. Define component-specific alphabets, cardinality, length, sensitivity, and case rules.
4. Construct structured components, percent-encode data once, and assemble the reference.
5. Establish base URIs and test relative resolution, including trailing-slash boundaries.
6. Define comparison context and the smallest justified normalization function.
7. Select canonical references and governed redirect/alias behavior.
8. Publish URI Templates with typed variables when clients need expansion.
9. Align gateway, origin, cache, signature, authorization, and logging interpretations.
10. Test malformed encoding, traversal, ambiguity, disclosure, migration, and resource exhaustion.

The **ownership invariant** prevents third parties from commandeering namespaces. The **structural invariant** requires parsing before decoding or comparison. The **single-encoding invariant** prevents delimiter injection and double decoding. The **semantic-stability invariant** preserves identity across deployment changes. The **contextual-equivalence invariant** forbids one global normalizer from deciding every security and cache question.

## Alternatives and Trade-Offs

**Readable versus opaque segments.** Readable slugs improve support and sharing but can change, collide, disclose data, and require Unicode/case policy. Opaque identifiers are stable and compact but hard to diagnose and do not prevent enumeration when sequential. Stable opaque identity plus an optional mutable slug can separate concerns.

**Path versus query.** Paths work well for stable hierarchy and direct identity; queries work well for optional dimensions, filtering, and searches. Neither component is inherently more secure or more “RESTful.” Choose based on meaning, cardinality, cache behavior, and evolution, then define it precisely.

**Relative versus absolute links.** Relative links support authority and prefix portability but depend on a correct base and can break after relocation. Absolute links are unambiguous but couple content to an authority and complicate environment migration. Generated hypermedia can use either with an explicit deployment and signature policy.

**Redirect versus permanent alias response.** Redirects teach clients a canonical URI and can consolidate caches, but add latency and interact with methods, credentials, and cross-origin rules. Serving aliases directly avoids the hop but preserves duplicate cache and link identities. Select per migration and client capability.

## Failure Modes and Misconceptions

URIs are not file paths, SQL keys, or controller names. “Pretty” is not a correctness property. A query is not automatically non-identifying or non-cacheable. A fragment is not sent to the server. Percent-encoding does not encrypt data. Encoding the same octets twice changes them. Decoding before parsing can create delimiters. Lowercasing the whole reference is unsafe. A valid URI can still identify an unauthorized or nonexistent resource. Templates neither sanitize received input nor prove resource existence.

## Worked Examples

### Example 1

An API changes from service `order-v1` to `fulfillment-core`. Existing URI `/order-v1/orders/42` exposes the old deployment, so clients and stored links need migration. A stable `/orders/42` would allow routing to change internally. **Conclusion:** public paths should encode resource meaning, not service topology.

### Example 2

Parse `https://api.example:8443/orders/42?view=summary#payment`. The authority is `api.example:8443`; `/orders/42` is the path; `view=summary` is the query; `payment` is the fragment. The HTTP server receives no `#payment`. **Conclusion:** component position determines processing ownership.

### Example 3

The raw identifier is `north/42`. Concatenating it into `/orders/` creates two path segments and possibly a different route. Component-aware expansion either encodes the slash as segment data, if every layer safely supports it, or rejects the identifier in favor of a portable alphabet. **Conclusion:** data must not become unintended delimiter syntax.

### Example 4

Input `%2F` is encoded again and becomes `%252F`. One decoder yields `%2F`; a second yields `/`. Gateway validation after one decode and origin routing after two can disagree. **Conclusion:** define one structural parse and one decoding layer; repeated decoding is a security defect.

### Example 5

Base `https://example.test/a/b/` plus `c` yields `https://example.test/a/b/c`; base `https://example.test/a/b` plus `c` yields `https://example.test/a/c`. The difference follows RFC 3986 path merging. **Conclusion:** a trailing slash changes relative-reference semantics and requires tests.

### Example 6

`HTTP://EXAMPLE.COM:80/%7Ealice` and `http://example.com/~alice` can normalize equivalently under HTTP scheme and syntax rules. Lowercasing `/~Alice`, however, could identify a different owner-defined path. **Conclusion:** normalize scheme, host, default port, and unreserved encodings only under applicable rules; path case remains significant by default.

### Example 7

`?tag=a&tag=b` reaches a gateway that keeps both values, but the origin library retains only the last. Authorization checked membership in `a`; execution uses only `b`. The contract selects an ordered-list interpretation and both layers use the same parser. **Conclusion:** duplicate query semantics are part of the security boundary.

### Example 8

A password-reset token is placed in `?token=...`. It appears in access logs and support analytics. The design moves it to protected request content, redacts unavoidable correlation values, and sets retention/access policy. **Conclusion:** TLS protects transport, not every URI copy made by participants.

### Example 9

Template `/reports/{id}{?format}` is expanded with `id="q3/board"` by raw substitution, producing accidental hierarchy. An RFC 6570 processor encodes variable data under the selected operator, and allowed-value validation rejects unsupported formats. **Conclusion:** templates require defined expansion and domain validation.

### Example 10

Old authority redirects an unsafe POST to a new origin using a status that a client historically rewrites to GET. The migration loses the operation. The owner uses method-preserving redirect semantics where clients support them, avoids credential forwarding across untrusted origins, and retains idempotent recovery. **Conclusion:** URI migration is also HTTP, security, and retry design.

## Cross-Program Connections

[Resource Identification](012-resource-identification.md) supplies the semantic target; [Headers and Metadata](004-headers-and-metadata.md) and [Caching](007-caching.md) supply intermediary effects. The next module, Collections and Individual Resources, applies path and query decisions to membership. Security Engineering owns canonicalization and injection threats; Networking owns origin and routing; Platform Engineering owns gateway consistency and deployment migration.

## References

1. T. Berners-Lee, R. Fielding, and L. Masinter, *RFC 3986: Uniform Resource Identifier (URI): Generic Syntax*, Internet Standard 66, January 2005, especially Sections 2–6; updated by RFC 8820. Checked 2026-09-01. https://www.rfc-editor.org/rfc/rfc3986.html
2. M. Nottingham, *RFC 8820: URI Design and Ownership*, BCP 190, June 2020; obsoletes RFC 7320 and updates RFC 3986. Checked 2026-09-01. https://www.rfc-editor.org/rfc/rfc8820.html
3. J. Gregorio, R. Fielding, M. Hadley, M. Nottingham, and D. Orchard, *RFC 6570: URI Template*, Standards Track, March 2012. Checked 2026-09-01. https://www.rfc-editor.org/rfc/rfc6570.html
4. R. Fielding, M. Nottingham, and J. Reschke, *RFC 9110: HTTP Semantics*, Internet Standard 97, June 2022, Section 4. Checked 2026-09-01. https://www.rfc-editor.org/rfc/rfc9110.html

## Exercises

### Exercise 1

Parse `https://api.example:9443/teams/a%2Fb/members?role=owner&active=true#contact` into components. State which portions reach the HTTP origin and why `%2F` must not be treated casually.

### Exercise 2

Resolve `../items/7?view=full` against bases `https://api.example/orders/42/` and `https://api.example/orders/42`. Show the intermediate path merge and final references.

### Exercise 3

Diagnose a gateway that authorizes after decoding once while an origin routes after repeated percent-decoding. Construct an adversarial path and specify a consistent processing invariant.

### Exercise 4

Compare `/customers/{email}`, `/customers/{sequence}`, and `/customers/{opaque-id}` under stability, disclosure, enumeration, encoding, supportability, and migration. Recommend a public identity policy.

### Exercise 5

A research archive moves from `http://old.example/archive/v1/` to `https://records.example/` while publications contain absolute and relative links, cached redirects, and signed download URIs. Design a migration preserving identity, reference resolution, security, and audit evidence.

## Answers to the Exercises

### Answer 1

Scheme is `https`; authority is `api.example:9443`; path is `/teams/a%2Fb/members`; query is `role=owner&active=true`; fragment is `contact`. The HTTP request target includes path and query but excludes the fragment. `%2F` represents a slash octet inside what appears syntactically to be one segment; stacks differ on whether they preserve, decode, or reject it. The API must define and test this or use an identifier alphabet that avoids encoded separators.

### Answer 2

With base path `/orders/42/`, the final empty segment makes it directory-like. Merging `../items/7` gives `/orders/42/../items/7`, and dot-segment removal yields `/orders/items/7`; final URI is `https://api.example/orders/items/7?view=full`. With base path `/orders/42`, resolution first removes the last segment `42`, merges to `/orders/../items/7`, and removes dot segments to `/items/7`; final URI is `https://api.example/items/7?view=full`. The different result is required by the resolution algorithm.

### Answer 3

An adversary can send `/public/%252e%252e/admin`. After one decode it is `/public/%2e%2e/admin`, which a gateway might authorize as public data; another decode produces `/public/../admin`, which origin normalization can route to `/admin`. Parse components once, reject malformed encoding, perform exactly the documented decoding and dot-segment policy at a shared boundary, and pass a canonical structured target that downstream layers cannot reinterpret. Authorization, routing, caching, and signing must use compatible canonical data.

### Answer 4

Email is human-recognizable but mutable, personal, case/Unicode-sensitive, and sometimes recycled. A sequence is compact and operationally easy but enumerable, volume-revealing, and collision-prone across imports. A random opaque identifier is stable and difficult to guess but less support-friendly and still needs authorization and non-reuse. Prefer a non-reused opaque public identity, keep email as mutable lookup/contact data, use route templates in telemetry, and provide authorized support correlation. If an external natural identifier is required, name its authority and lifecycle explicitly.

### Answer 5

Retain control of the old authority and map each old absolute identity to one stable new canonical identity with method-safe redirects, no HTTPS downgrade, bounded credential forwarding, loop detection, and long-lived tombstones where content is removed. Re-render archive representations with an explicit new base and test every relative reference under RFC 3986; do not assume textual prefix replacement preserves meaning. Version or reissue signed download URIs because scheme, authority, and canonicalization affect signatures. Preserve original identifiers and redirect decisions in audit metadata, monitor broken-link and cache behavior, and keep old links valid for the archive's declared citation lifetime.
