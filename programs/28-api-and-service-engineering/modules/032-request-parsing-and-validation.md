---
module_id: API-032
program: API & Service Engineering
level: 1
module_number: 32
title: Request Parsing and Validation
status: complete
last_verified: 2026-09-01
---

# Request Parsing and Validation

## One-Page Review

### Governing question

How should an API turn bounded untrusted request bytes into one typed application input while rejecting malformed, unsupported, structurally invalid, semantically invalid, and unauthorized requests at the correct layer?

### Essential definitions

- **framing** determines message boundaries before application parsing.
- **decoding** converts encoded octets into characters or decompressed content under declared rules.
- **parsing** converts serialized syntax into a data value and rejects malformed syntax.
- **deserialization** maps parsed data into a host-language representation.
- **structural validation** checks a value against declared types, required fields, shapes, and local constraints.
- **semantic validation** checks cross-field, reference, state, and domain meaning.
- **normalization** intentionally maps several accepted forms to one canonical form.
- A **validation error location** identifies the public request component and path responsible for rejection.

### Central model, mechanism, or theorem

Model the inbound pipeline as partial functions:

$$
B\xrightarrow{f}M\xrightarrow{d}S\xrightarrow{p}V
\xrightarrow{v}V'\xrightarrow{m}A,
$$

where bounded bytes $B$ become framed message $M$, decoded serialization $S$, parsed data $V$, validated data $V'$, and application input $A$. Each stage must either produce exactly one result or a typed rejection. Later stages must never reinterpret bytes rejected or ambiguously accepted by earlier stages.

### Critical invariants

Limits apply before expensive allocation. Framing and security-critical fields use one canonical parser across intermediaries. Method, target, headers, parameters, media type, and body are validated together. Unsupported content is distinguished from malformed content. No implicit coercion turns invalid strings into numbers or booleans unless the contract defines that conversion. Duplicate names, Unicode, percent encoding, null, absence, empty values, and unknown fields have explicit policies. Validation cannot authorize an actor or prove current domain state. Errors are stable and safe, with public locations but no parser internals or secrets.

### Common failures

Reading unbounded bodies; decompressing without output limits; applying business effects before the complete request is known; accepting conflicting `Content-Length` interpretations; treating missing `Content-Type` as JSON; parsing query parameters with body rules; double percent-decoding; silently choosing one duplicate JSON name; locale-dependent numbers; broad type coercion; regex denial of service; trusting a deserializer constructor; reporting every internal schema path; validating fields but not cross-field rules; and using validation to disclose whether a forbidden object exists.

### Compact example

`POST /orders?dryRun=false` carries JSON with `quantity: "2"`. Query parsing may define literal strings and then a precise Boolean conversion, but JSON parsing already produced a string where the schema requires an integer. The server rejects `/quantity` rather than coercing it. A valid integer then reaches domain validation for inventory and authorization for customer access. **Conclusion:** conversion policy is location-specific, and structural success does not imply business permission.

### Connections

[Validation Constraints](025-validation-constraints.md) defines schema predicates. [Transport, Application, and Domain Boundaries](031-transport-application-and-domain-boundaries.md) assigns ownership to the inbound adapter. [Authentication Context Propagation](../ROADMAP.md) next constructs trusted identity context; [Authorization Checks](../ROADMAP.md) determines permitted actions after safe parsing.

## Governing Question

Which ordering, bounds, conversion rules, error taxonomy, and tests ensure that one service and every intermediary interpret an untrusted request consistently without confusing syntax, structure, domain validity, and authorization?

## Why This Matters

An API contract describes data after protocol-specific serialization. A server receives bytes, message metadata, and a target that may have passed through proxies, gateways, runtimes, and framework binders. Each component can impose limits or parse slightly differently. Attackers deliberately seek disagreements: duplicated fields, ambiguous lengths, unusual percent encodings, compressed expansion, duplicate JSON names, deep nesting, and types that libraries coerce differently.

Correct parsing is therefore both interoperability and security work. The service must know which bytes belong to the message, which representation they encode, how each parameter location serializes values, and which schema dialect applies. Rejection must occur before business effects. A later validator cannot repair a framing disagreement or recover the exact input after a lossy binder changed it.

Validation is layered rather than one library call. Transport validity says the message can be interpreted safely. Structural validity says a data value belongs to a declared set. Application and domain validity concern current references, invariants, and transitions. Authorization concerns an actor's permission and disclosure. Keeping these layers separate yields accurate errors, reusable domain policy, and resistant boundaries.

## Prerequisites and Retrieval

Retrieve HTTP messages, fields, content metadata, negotiation, status semantics, URI and percent encoding, OpenAPI parameter styles, JSON grammar, JSON Schema dialect and validation, request models, null and absence, Unicode, numeric representations, resource limits, authentication, authorization, domain invariants, and boundary mapping.

Before implementing a parser, retrieve the deployed HTTP stack and proxy chain, maximum request and decompressed sizes, accepted media types and character encodings, parameter serialization, duplicate-name policy, schema resources and dialect, format policy, normalization rules, public error convention, and observability/data-classification constraints.

## Learning Objectives

By the end of this module, you should be able to:

1. order framing, limits, decoding, parsing, validation, mapping, and authorization;
2. parse path, query, header, cookie, form, multipart, and body inputs by their own rules;
3. prevent parser differentials, unsafe coercion, duplicate ambiguity, and resource exhaustion;
4. separate structural, semantic, state, and authorization failures;
5. design stable safe validation errors with precise public locations;
6. test boundaries and adversarial representations; and
7. verify that gateways, frameworks, and application code enforce compatible policies.

## Core Exposition

### Treat the request as one security object

Do not validate the JSON body while ignoring method, target, headers, content coding, and parameters. The meaning of body bytes depends on `Content-Type`; conditional behavior depends on validators; authentication and signatures may depend on the exact target and selected headers; content negotiation affects the response.

Process the complete request headers before applying effects. RFC 9110 warns that later fields can contain conditionals, credentials, or misleading duplicates. The network server or trusted proxy owns wire framing, but the application must know which normalization and rejection policies it applied. Do not deploy proxy and origin configurations that accept different message boundaries.

Define one effective request model after trusted proxy processing: external scheme and authority, normalized target, method, selected client identity context, complete fields, and content stream. Forwarded metadata is trusted only from authenticated configured proxies.

### Bound work before parsing

Apply limits as early as the responsible layer can enforce them:

- request line and target length;
- number and aggregate size of fields;
- body wire size;
- decompressed size and compression ratio;
- nesting depth, array/object members, and string length;
- multipart part count, field size, filename length, and aggregate size;
- parser time or token count; and
- temporary storage and concurrent request budgets.

HTTP does not impose one universal field limit, so implementations set appropriate limits and reject excess with a suitable client error. Silently dropping a security-relevant field can change meaning and enable request smuggling.

Reject oversized content before buffering where possible. Stream to a bounded sink when the operation supports streaming. A `Content-Length` below the limit does not protect against compressed expansion or chunked input. Limits must cover the representation after every expansion stage.

Choose errors carefully. `413 Content Too Large` communicates request content limits; `414 URI Too Long` applies to the target; field-limit handling may use an appropriate `4xx` under the service contract. Do not reveal internal memory thresholds when that creates avoidable reconnaissance.

### Separate framing, decoding, parsing, and validation

Framing identifies message components. Content decoding reverses declared content codings. Character decoding interprets bytes where a media type requires text. Parsing recognizes grammar. Validation applies predicates to the resulting data.

These stages produce different failures. Unsupported `Content-Encoding: br` is not malformed JSON. Invalid UTF-8 is not a missing required property. A well-formed JSON string where an integer is required is structural invalidity. A positive integer exceeding available inventory is domain invalidity.

Preserve the distinction internally even if public policy groups some errors. It determines monitoring, ownership, remediation, and tests. Never catch all failures as “validation error.”

The pipeline is intentionally one-way. Once a form parser turns `+` into space or a duplicate map entry is discarded, the original representation cannot be reconstructed. Make ambiguity policy before lossy conversion and retain exact bytes only where authorized and safely bounded; routine logs should not capture sensitive bodies.

### Select media type before parsing content

Match request `Content-Type` against the operation's supported media types, including parameters under media-type rules. Do not sniff JSON because a payload begins with `{`. Sniffing creates different interpretations across clients, gateways, security scanners, and servers.

If a required body has no content type, follow the documented API policy rather than a framework default. Unsupported media types normally produce `415`. Malformed content under a supported media type produces the contract's parsing error. An unacceptable response media request concerns `Accept` and can produce `406`; it is not request-body validation.

Character sets are media-type-specific. JSON exchanged over networks uses UTF-8 for interoperability under RFC 8259. A generic text decoder that replaces invalid byte sequences can transform hostile input into accepted content. Use strict decoding unless the media type explicitly defines another recovery behavior.

### Parse each parameter location by its rules

Path, query, header, and cookie parameters are not a single string map. Their delimiter, percent-encoding, repetition, case, whitespace, and ordering rules differ. OpenAPI `style`, `explode`, schema, and `content` describe the intended mapping.

For query parameters, decide repeated-name behavior, empty value versus absent value, flag-like name without `=`, order, and percent decoding. Decode exactly once at the appropriate layer. `%252F` becomes `%2F` after one decode and must not silently become `/` after a second.

Path matching and decoding order can affect routing and security. A proxy, router, and application must agree on encoded slashes, dot segments, and normalization. Use the router's captured parameter under a documented policy; do not rebuild authorization targets from differently decoded strings.

HTTP field names are case-insensitive, but field values follow each field's grammar. Do not comma-join fields whose semantics do not permit it. Parse validators, dates, authorization, signatures, and media types with their registered grammar, not string splitting.

Cookies have their own grammar and security attributes; a Cookie header is not generic query syntax. Multipart parsing must validate boundaries, part headers, content dispositions, file names, and per-part media types with independent limits.

### Parse JSON strictly

RFC 8259 defines JSON grammar and highlights interoperability problems when object names are not unique. Parsers differ: some keep the last pair, some the first, and some expose all. At a public trust boundary, reject duplicate object member names before mapping unless the contract establishes another interoperable policy.

Also define:

- maximum nesting and value counts;
- valid Unicode and handling of unpaired surrogate escapes;
- accepted top-level value shape;
- numeric magnitude and precision before host conversion;
- trailing content after the JSON value;
- byte-order mark policy; and
- nonstandard comments, trailing commas, `NaN`, and infinity rejection.

A parser's permissive mode should not define the API accidentally. Configure strict settings and test the actual deployed library version. A floating parser upgrade can change duplicate, number, or Unicode behavior.

Avoid converting JSON numbers to binary floating point before deciding exact constraints. Money, identifiers, and high-precision values may require decimal or string representations. Reject overflow rather than saturating or wrapping.

### Avoid hidden coercion

Framework binders often convert `"42"` to integer, `"false"` to Boolean, an empty string to null, or one value to a list. Such convenience changes the accepted set and can disagree between languages.

Coercion is allowed only where serialization rules require an explicit conversion. Query parameters arrive as serialized text, so a contract can define which lexical strings represent integers and booleans. JSON already carries string, number, Boolean, null, array, and object distinctions; do not blur them after parsing.

Define lexical grammar, sign, leading zeros, exponent notation, whitespace, case, range, and overflow. Locale must not change decimal separator or case folding. Parse `false` as false only under a declared exact or case policy; never rely on a language rule where every nonempty string is truthy.

Record the original public location for errors even after conversion. The consumer needs `query.limit`, not the name of a generated integer constructor.

### Apply the exact schema and dialect

Resolve the operation, media type, direction, Schema Object, dialect, and external resources before validation. Validate the complete parsed data value; do not cherry-pick recognized properties before an unknown-property rule can see them.

JSON Schema Draft 2020-12 distinguishes assertion and annotation behavior and makes `format` behavior vocabulary-dependent. Decide whether each format is annotation or assertion, which implementation checks it, and whether the same rule is available in every supported environment.

Validation output should retain instance location, schema location for internal diagnostics, keyword, and stable public classification. Do not expose internal file paths, component names that reveal structure, regex internals, or arbitrary schema messages.

Schemas are immutable release artifacts for one request. Do not fetch arbitrary remote references during request processing. Resolve and compile allowed resources at build or startup, bound reference graphs, and fail deployment on unresolved or cyclic behavior the validator cannot support safely.

### Layer structural and semantic validation

Structural validation covers declared value membership: types, required properties, ranges, patterns, array constraints, and union structure. Application validation covers use-case relationships such as path ID agreeing with a body ID or fields allowed only under one operation option. Domain validation covers authoritative current state and business invariants.

Examples:

- JSON cannot parse: syntax failure;
- `quantity` is string: structural failure;
- `start > end`: cross-field semantic failure;
- customer reference does not exist: application/domain reference outcome;
- inventory is insufficient now: domain state outcome;
- actor cannot order for customer: authorization outcome.

Do not query a database for every malformed request; reject cheap deterministic failures first. But do not call an existence check “schema validation.” It can race and is subject to disclosure policy.

Validation ordering affects observable errors. Prefer safe deterministic precedence, but do not promise every internal ordering. Authentication may occur before parsing a large body to limit anonymous work, while body-size limits occur even earlier. Authorization that depends on parsed target fields follows safe parsing. Threat modeling decides the exact sequence.

### Keep authorization separate

A valid request is not necessarily permitted. Schema validation cannot establish that a principal owns `customerId`, may set a field, or may observe whether a target exists. Conversely, authorization logic should consume typed validated identifiers rather than raw strings.

Some validation details can leak policy or existence. An unauthorized actor should not learn that a hidden resource has state `shipped` because domain validation ran before concealment. Load and validate under an authorization-aware application flow, map outcomes through disclosure policy, and equalize only where the threat model requires it.

Field-level authorization needs allowlisted mapping after actor context is known. A property can be structurally defined yet forbidden to this actor. Reject, ignore, or conceal under the explicit public contract—never let generic binding set it first and check afterward.

### Normalize only with an explicit contract

Normalization can improve consistency: trimming a display label, canonicalizing a case-insensitive identifier, or converting an international domain name under a named standard. It can also change signatures, idempotency fingerprints, uniqueness, and user intent.

Define which stage normalizes, whether the canonical value is returned, and whether validation applies before or after normalization. Security comparisons and storage must use the same canonical form. Never normalize one component for authorization and another form for lookup.

Keep raw bytes for signature verification when the signature protocol requires them. Parse and normalize only after verification as specified. Do not reserialize JSON and assume it reproduces signed bytes.

Unicode normalization and case folding are domain-specific. Usernames, identifiers, search text, and passwords have different requirements. Do not apply a universal lowercase-and-trim function.

### Design a stable error contract

Return a safe Problem Details representation or equivalent with stable problem type, status, title, instance/correlation identifier, and a bounded list of public violations where appropriate. A violation can include:

- public location such as `body.lines[2].quantity` or `query.limit`;
- stable rule code such as `required`, `type`, or `maximum`;
- safe human-readable message; and
- allowed metadata such as declared bound.

Do not echo untrusted values, credentials, raw bodies, parser stack traces, schema filesystem paths, database facts, or complex regexes. Bound the number of reported errors and response size. Sorting violations deterministically improves tests and client display without promising validator traversal order.

Decide fail-fast versus accumulated errors. Accumulation helps interactive correction but spends more work and may reveal more. Parse errors are usually singular; structural errors can be safely bounded; state and authorization failures often should not be aggregated.

Use appropriate statuses under the contract: malformed syntax commonly `400`, unsupported media type `415`, content too large `413`, failed HTTP precondition `412`, and semantic/domain conflicts according to their meaning. A project may use `422` for well-formed but semantically invalid content where that distinction is documented. Status is not a substitute for stable problem meaning.

### Resist algorithmic abuse

Validate cost as well as value. Deep recursive schemas, catastrophic regexes, enormous numeric literals, long unique-item arrays, multipart part explosions, and reference cycles can consume CPU or memory within nominal byte limits.

Use linear-time or bounded regex engines/patterns, depth and token budgets, collection limits, request deadlines, and worker isolation. Measure worst cases with adversarial fixtures. `uniqueItems` over large complex objects can be costly even when valid.

Fail closed without crashing the process. Rate limiting and quotas complement per-request limits but do not replace them. A single authorized request must not exhaust the service.

### Make the pipeline explicit

The executable model below classifies a small set of pre-parsed requests through media, parse, structure, and semantic stages. It demonstrates precedence and typed outcomes; it is not an HTTP or JSON parser.

<!-- bijux-verify: {"id":"request-validation-pipeline","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"unsupported=unsupported_media\nmalformed=malformed_json\nwrong_type=structural:/quantity\ninvalid_range=semantic:quantity_positive\nvalid=accepted\n","stderr":""}} -->
```python
def classify(case):
    if case["media"] != "application/json":
        return "unsupported_media"
    if not case["parsed"]:
        return "malformed_json"
    value = case["value"]
    if type(value.get("quantity")) is not int:
        return "structural:/quantity"
    if value["quantity"] <= 0:
        return "semantic:quantity_positive"
    return "accepted"

cases = {
    "unsupported": {"media": "text/plain", "parsed": True, "value": {}},
    "malformed": {"media": "application/json", "parsed": False, "value": {}},
    "wrong_type": {"media": "application/json", "parsed": True, "value": {"quantity": "2"}},
    "invalid_range": {"media": "application/json", "parsed": True, "value": {"quantity": 0}},
    "valid": {"media": "application/json", "parsed": True, "value": {"quantity": 2}},
}
for name, case in cases.items():
    print(f"{name}={classify(case)}")
```

Real pipelines also enforce framing, limits, encodings, parameter rules, schema resources, actor context, and domain state. The example deliberately does not imply that positive quantity is sufficient to create an order.

### Verify every deployed parsing layer

Unit-test lexical converters and error locations. Feed parsers duplicate names, invalid Unicode, deep nesting, enormous numbers, trailing content, malformed percent encodings, repeated parameters, headers with dangerous controls, and multipart boundary failures. Test just below, at, and above every limit.

Contract tests exercise exact OpenAPI serialization and request schemas. Differential tests send the same corpus through gateway, framework, and application to detect disagreement. Fuzz parsers in isolated bounded environments and preserve minimized failing inputs under safe controls.

Integration tests verify real server configuration, decompression, buffering, temporary files, timeouts, and public errors. Observe rejection rates by stable categories without logging raw sensitive values. Re-run after proxy, runtime, parser, schema validator, or framework upgrades.

Property tests can assert that every accepted request maps to one typed input, no rejected input reaches effects, serialization round-trips under declared equivalence, and normalization is idempotent: $n(n(x))=n(x)$ for accepted $x$.

## Definitions and Notation

Let $B_L$ be byte strings satisfying early limit policy $L$. Each pipeline stage is partial: framing $f:B_L\rightharpoonup M$, decoding $d:M\rightharpoonup S$, parsing $p:S\rightharpoonup V$, structural validation $v:V\rightharpoonup V'$, and mapping $m:V'\times C\rightharpoonup A$ with trusted context $C$.

Accepted request set is:

$$
A_R=\operatorname{dom}(m\circ v\circ p\circ d\circ f).
$$

Each rejection belongs to the first stage whose contract is violated. This ordering is a policy and cost model; it does not authorize domain effects.

A normalization function $n$ is **idempotent** when $n(n(x))=n(x)$. A **parser differential** is a message for which two pipeline components derive materially different structures or boundaries. A **lexical grammar** defines which serialized strings convert to a typed value. A **lossy binder** discards or coerces information before policy can inspect it.

## Mechanisms, Invariants, or Proof Structure

1. Define the effective request and trusted proxy boundary.
2. Apply framing, field, body, expansion, depth, and cost limits early.
3. Select content coding, media type, and character decoding strictly.
4. Parse each parameter location and content format by its own grammar.
5. Reject duplicate or ambiguous representations before lossy binding.
6. Apply the exact schema dialect and structural constraints without hidden coercion.
7. Normalize only under a named idempotent policy.
8. Map into allowlisted application input with verified context.
9. Apply semantic, state, and authorization decisions under their owners.
10. Emit bounded safe errors and test every deployed parsing layer adversarially.

The main invariant is single interpretation: every accepted byte sequence has one contractually intended application value, and every rejected sequence reaches no business effect. Tests can establish this for selected corpora and models, not all possible runtimes or inputs.

## Alternatives and Trade-Offs

Buffering simplifies parsing and error collection but increases memory and expansion risk. Streaming supports large content and early processing but complicates atomic validation and rollback. Use streaming only when the media type and operation define partial processing safely.

Fail-fast validation limits work and disclosure. Bounded accumulation improves consumer correction. Accumulate independent structural errors within strict count and cost limits; avoid speculative state and authorization errors.

Strict rejection maximizes interoperability and security. Tolerant parsing can support legacy clients but creates a larger accepted set and migration burden. Any tolerance needs explicit scope, telemetry, expiry, and canonical output.

Generated binders reduce code but can hide coercion, defaults, unknown fields, and error details. Direct data validation before typed construction is more explicit. Whichever route is used, test the actual generated/runtime behavior against the contract.

Schema validation centralizes structural rules. Handwritten validation expresses cross-field and domain meaning more clearly. Avoid duplicating one rule in both unless one is deliberate defense with equivalence tests.

Gateway validation rejects bad traffic early but may diverge from the service and cannot own current domain policy. Service validation remains authoritative; gateways enforce compatible coarse limits and contract checks with shared version identity.

## Failure Modes and Misconceptions

- **“Parsing and validation are the same.”** Parsing establishes syntax; validation applies predicates to parsed data.
- **“The framework handles HTTP safely.”** Proxy, server, router, binder, and application configurations can disagree.
- **“Content length bounds the body.”** Chunking and decompression require independent limits.
- **“If it looks like JSON, parse it.”** Media type determines interpretation; sniffing creates ambiguity.
- **“All parameters are strings.”** They are serialized text with location-specific grammar and declared conversion.
- **“Decode until readable.”** Double decoding changes targets and authorization meaning.
- **“Duplicate JSON names are harmless.”** Parsers choose differently; reject ambiguity at a public boundary.
- **“Coercion is user-friendly.”** Undeclared coercion expands the contract differently across languages.
- **“`format` is always validated.”** JSON Schema behavior depends on dialect, vocabulary, and implementation policy.
- **“Schema success means the request is valid.”** References, domain state, authorization, and concurrency remain.
- **“Validate everything before authentication.”** Ordering must consider cost and disclosure; cheap limits come first.
- **“Return all errors.”** Unlimited aggregation creates work and may disclose policy or hidden state.
- **“Regex validates safely.”** Pattern complexity and engine behavior can create denial of service.
- **“Gateway validation replaces service validation.”** Gateways can be bypassed or skewed and lack domain authority.
- **“A green parser test covers deployment.”** Real proxies, limits, content decoding, and framework versions matter.

## Worked Examples

### Example 1

**Situation:** A 2 KB gzip request expands to 200 MB JSON. **Reasoning:** Wire-size validation passes, so stream decompression through an output and ratio budget before JSON parsing; reject before allocation. **Conclusion:** every expansion stage needs its own limit.

### Example 2

**Situation:** JSON contains `{"role":"user","role":"admin"}`. **Reasoning:** First-wins and last-wins parsers disagree, and validation after map construction cannot see the duplicate. Reject duplicate names during parsing. **Conclusion:** ambiguity must be handled before lossy binding.

### Example 3

**Situation:** Query `active=false` becomes true because a language converts every nonempty string to Boolean. **Reasoning:** Define accepted lexical forms, compare exactly, and reject other strings. **Conclusion:** host-language truthiness is not an API grammar.

### Example 4

**Situation:** Path contains `%252F`; proxy decodes once and application twice. **Reasoning:** The layers authorize different resource identifiers. Establish one decoding boundary and test encoded reserved characters end to end. **Conclusion:** parser agreement is an authorization prerequisite.

### Example 5

**Situation:** Body has `quantity:"2"`, and a binder coerces it to integer. **Reasoning:** JSON already distinguishes strings from numbers; reject the string at `/quantity`. Query-string conversion policy does not apply to JSON. **Conclusion:** coercion rules are serialization-location-specific.

### Example 6

**Situation:** Schema accepts positive quantity, but requested SKU has only one item available. **Reasoning:** Structural validation completes first; domain policy evaluates current inventory within the use case and returns a stable business outcome. **Conclusion:** schema and state validation have different owners and evidence.

### Example 7

**Situation:** Unauthorized caller submits a valid hidden order ID and receives “already shipped.” **Reasoning:** Domain error ordering disclosed resource state. Apply authorization-aware loading and concealment before exposing state-specific rejection. **Conclusion:** technically accurate validation can still violate disclosure policy.

### Example 8

**Situation:** Validation returns 4,000 violations for one huge array. **Reasoning:** Bound array length early and cap deterministic public errors; retain aggregate internal metrics without echoing values. **Conclusion:** error reporting itself needs resource and disclosure limits.

### Example 9

**Situation:** Gateway ignores an oversized header while origin uses it for a signature. **Reasoning:** Silent dropping changes semantics. Align field limits and reject the request at the first component with an appropriate client error. **Conclusion:** intermediaries must share security-critical parsing policy.

### Example 10

**Situation:** A parser upgrade begins accepting trailing commas. **Reasoning:** Strict adversarial corpus and deployment integration tests detect the accepted-set widening. Pin or configure the parser, assess compatibility, and retain the public JSON grammar. **Conclusion:** dependency upgrades can change the API contract without schema changes.

## Cross-Program Connections

[Network Engineering](../../24-network-engineering/ROADMAP.md) owns HTTP transport, proxy, and routing foundations. [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies parser differential, resource exhaustion, trust, and disclosure analysis. [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies boundary, property, differential, and fuzz testing. [Compiler and Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md) supplies lexical, parsing, grammar, and error-location foundations. This module applies them to public service request boundaries.

## References

1. R. Fielding, M. Nottingham, and J. Reschke, [*RFC 9110: HTTP Semantics*](https://www.rfc-editor.org/rfc/rfc9110.html), especially fields, limits, content, conditional requests, and status semantics, June 2022. Checked 2026-09-01.
2. T. Bray, [*RFC 8259: The JavaScript Object Notation (JSON) Data Interchange Format*](https://www.rfc-editor.org/rfc/rfc8259.html), especially parser limits, Unicode, numbers, and object-name interoperability, December 2017. Checked 2026-09-01.
3. OpenAPI Initiative, [*OpenAPI Specification 3.2.0*](https://spec.openapis.org/oas/v3.2.0.html), Parameter, Request Body, Media Type, serialization, parsing, and data conversion sections, 19 September 2025. Checked 2026-09-01.
4. A. Wright, H. Andrews, B. Hutton, and G. Dennis, [*JSON Schema: A Media Type for Describing JSON Documents, Draft 2020-12*](https://json-schema.org/draft/2020-12/json-schema-core), 16 June 2022. Checked 2026-09-01.
5. A. Wright, H. Andrews, B. Hutton, and G. Dennis, [*JSON Schema Validation, Draft 2020-12*](https://json-schema.org/draft/2020-12/json-schema-validation), 16 June 2022. Checked 2026-09-01.
6. M. Nottingham, E. Wilde, and S. Dalal, [*RFC 9457: Problem Details for HTTP APIs*](https://www.rfc-editor.org/rfc/rfc9457.html), Standards Track, July 2023. Checked 2026-09-01.

## Exercises

### Exercise 1

Classify these failures by stage: conflicting framing, unsupported gzip, invalid UTF-8, malformed JSON, string instead of integer, end before start, missing referenced customer, and forbidden customer.

### Exercise 2

Trace query `tags=red+blue,green` and JSON body `{"limit":10}` through media selection, location-specific decoding, parsing, schema validation, mapping, and errors. State where double decoding and coercion could enter.

### Exercise 3

Design limits and failure behavior for a multipart document upload with metadata JSON, ten files, compression, filenames, and a streaming virus scanner.

### Exercise 4

Compare fail-fast and accumulated validation for a public form API under interactive use, hostile traffic, authorization concealment, and expensive domain checks.

### Exercise 5

Design a differential verification suite for a gateway, framework, and service after upgrading their HTTP parser, JSON parser, and schema validator versions.

## Answers to the Exercises

### Answer 1

Conflicting framing belongs to the HTTP server/proxy and must be rejected before effects. Unsupported gzip is content-decoding capability. Invalid UTF-8 is strict character decoding. Malformed JSON is syntax parsing. String instead of integer is structural schema validation. End before start is cross-field application/domain validation. Missing referenced customer is a current reference/state outcome. Forbidden customer is authorization and disclosure policy. Public statuses can group some results, but internal ownership remains distinct.

### Answer 2

Select the operation and media type first. Query parsing follows its declared style: form-like decoding may turn `+` into space, then delimiter and explode rules determine whether values are `red blue` and `green`; decoding happens exactly once. JSON body bytes decode strictly as UTF-8, parse into an object with numeric `limit`, then validate schema. Mapping creates typed application values and preserves public locations. Double decoding can occur between proxy/router/application; coercion can occur if a generic binder treats all query and body values alike. Round-trip fixtures must pin the declared rules.

### Answer 3

Limit total wire bytes, decompressed aggregate and ratio, part count to metadata plus ten files, each part size, total file bytes, header and filename lengths, nesting/tokens in metadata, temporary storage, scanner time, and concurrency. Parse multipart boundaries strictly and validate each part's media type. Sanitize display filenames but generate storage names; never use client paths. Stream files through bounded storage and scanner without committing business state until every required part validates. On scanner timeout or failure, quarantine or delete the isolated upload and return a stable safe outcome. No partial document becomes visible.

### Answer 4

Fail fast for framing, size, decoding, syntax, authentication cost controls, and any condition whose continuation is unsafe. For a validated authenticated interactive form, accumulate a bounded deterministic set of independent structural field errors to improve correction. Do not aggregate hidden resource existence, field authorization, or expensive domain checks; those need disclosure-aware sequencing and may stop early. Cap error count and work, omit submitted sensitive values, and give each public violation a stable location and code.

### Answer 5

Pin old and new component versions and send one corpus through each layer alone and the composed deployment. Include framing duplicates, field limits and controls, percent-encoding variants, repeated parameters, media types, compression expansion, invalid UTF-8, duplicate JSON names, deep nesting, huge numbers, trailing data, every schema boundary, `format` cases, and external-reference failures. Compare acceptance, parsed canonical value, error category, location, status, and absence of effects. Any differential is reviewed against the contract, not automatically accepted. Fuzz within resource limits, preserve minimized safe cases, and rerun full composition tests before promotion.
