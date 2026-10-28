---
module_id: API-025
program: API & Service Engineering
level: 1
module_number: 25
title: Validation Constraints
status: complete
last_verified: 2026-09-01
---

# Validation Constraints

## One-Page Review

### Governing question

How should an API constrain untrusted input from bytes through domain action so the exact value executed is bounded, meaningful, authorized, current, and diagnosed without leaking sensitive policy?

### Essential definitions

- **framing validation** checks HTTP message size, transfer, encoding, and media-type requirements before content parsing.
- **syntactic validation** decides whether content can be parsed according to its media type.
- **structural validation** checks types, presence, cardinality, and local constraints against a schema.
- **semantic validation** checks cross-field and domain meaning independent of current mutable state.
- **state validation** checks predicates that depend on current authoritative resources and must often be atomic with effects.
- **normalization** maps accepted equivalent forms to a canonical effective value under an explicit contract.
- A **validation witness** is a concrete boundary or adversarial input with one expected classification and recovery.

### Central model, mechanism, or theorem

Model admission as an ordered conjunction $A(x,c,s)=L(x)\land P(x)\land S(x)\land N(x)\land D(x,c)\land T(x,c,s)\land Z(x,c,s)$: resource limits, parsing, structural constraints, normalization-preserving revalidation, domain meaning, current-state predicates, and authorization. Order is chosen for safety and information control, but success requires all applicable predicates. The effect must consume the same effective value and state basis that passed the final checks.

### Critical invariants

Reject excessive work before expensive parsing. Interpret content under the declared media type and character rules. Reject duplicate or unknown fields according to explicit policy. Validate the post-normalization value or prove preservation. Use exact numeric and Unicode semantics. Cross-field constraints see the complete intended object. State-dependent checks are atomic with commit or protected by versions. Authorization is never inferred from validity. Validation does not build SQL, shell, paths, templates, or URLs safely by itself. Errors support a legitimate next action without disclosing secrets, hidden resources, or internal rules.

### Common failures

One generic `isValid`; client-side validation only; regex as a parser; blacklists for an open input language; converting before bounding size; accepting unknown properties; trimming or case-folding after signatures and idempotency fingerprints; binary floating-point money checks; validating each field but not the relationship; checking uniqueness then racing the insert; fetching caller-supplied URLs during validation; returning every policy threshold to an attacker; using `400` for every rejection; and executing a transformed value different from the validated value.

### Compact example

An order line passes JSON parsing, has string SKU and integer quantity, and satisfies `1 <= quantity <= 100`. The service normalizes an explicitly case-insensitive SKU, rechecks its lexical rule, resolves it in the authorized catalog, and atomically verifies current order state and stock before commit. A valid shape alone does not prove the SKU exists, belongs to the tenant, or remains available. **Conclusion:** validation is a layered, state-aware admission proof with a precisely bounded claim.

### Connections

[JSON Schema](022-json-schema.md) supplies structural evaluation. [Request and Response Modeling](024-request-and-response-modeling.md) supplies field ownership and effective values. [API Contracts and Behavioral Guarantees](021-api-contracts-and-behavioral-guarantees.md) supplies state, authority, and failure meaning. [Reusable Schema Components](../ROADMAP.md) later governs shared constraint ownership.

## Governing Question

Which constraints belong at each API boundary, in what order should they run, and what evidence establishes that invalid, hostile, stale, and unauthorized inputs cannot reach effects under a misleading success path?

## Why This Matters

“Validate input” sounds like one operation, yet an API sees several representations of input. It receives bytes framed by HTTP, decodes content under a media type and character encoding, constructs a data model, normalizes selected fields, maps them into application intent, reads current state, evaluates authorization, and finally executes through interpreters and storage. A check at one stage says little about another.

A JSON Schema can reject a negative quantity. It cannot know whether the referenced product exists now, whether stock changed between check and commit, whether the caller may use the catalog, or whether interpolating the SKU into SQL is safe. An authorization rule can permit an action while a huge body exhausts memory before the rule runs. A database uniqueness constraint can preserve an invariant but still needs safe error translation.

Validation also shapes compatibility. Tightening a maximum, changing a regular expression, enabling format assertion, switching Unicode normalization, rejecting previously ignored fields, or making a cross-field condition mandatory changes the request language. A constraint is a public contract, security control, and operational cost decision—not merely a decorator on a class.

HTTP provides distinct outcomes. RFC 9110 defines `400 Bad Request`, `413 Content Too Large`, `415 Unsupported Media Type`, `422 Unprocessable Content`, `409 Conflict`, and `412 Precondition Failed` with different conditions and recovery implications. Status choice must reflect the actual failed boundary without exposing protected facts. RFC 9457 can carry safe machine-readable problem details; it does not replace status or validation design.

## Prerequisites and Retrieval

Retrieve HTTP framing and media types, request/response ownership, JSON parsing, JSON Schema, Unicode and regular expressions, exact numbers, domain invariants, authentication and authorization, transactions, optimistic concurrency, database constraints, safe interpreters, Problem Details, rate limiting, and observability.

Before adding a constraint, retrieve its owner, decision purpose, accepted set, normalization policy, state basis, enforcement point, error semantics, computational cost, confidentiality, compatibility impact, and evidence. If these are unknown, the constraint is not ready for a public contract.

## Learning Objectives

By the end of this module, you should be able to:

1. design a layered validation pipeline from resource limits through atomic state checks;
2. express presence, type, range, pattern, cardinality, and cross-field constraints precisely;
3. reason about Unicode, exact numbers, timestamps, identifiers, files, and remote references;
4. place normalization without creating validate-one-value/execute-another defects;
5. distinguish validation, authorization, safe interpretation, and database enforcement;
6. return stable, safe, actionable validation problems; and
7. test constraint boundaries, adversarial cost, races, and compatibility changes.

## Core Exposition

### Inventory the representations of input

Write down each form the request takes:

1. HTTP method, target, fields, and framed content bytes;
2. decoded media-type content;
3. parsed JSON, form, multipart, or domain-specific syntax tree;
4. normalized effective values;
5. an application command combined with trusted context;
6. domain objects and current state read for the decision; and
7. parameters passed to persistence, templates, networks, or other interpreters.

Every transition can lose or change information. A duplicate JSON member can disappear when parsed into a map. A Unicode string can have multiple canonically equivalent sequences. A decimal token can become a rounded binary float. A relative path can be joined to a privileged base. A URL can resolve to a private address after DNS changes. Validation evidence must name which representation it covers.

Use immutable or clearly separated values between stages. Avoid mutating the parsed object in place and later claiming the original schema result applies. Record the canonical value used for idempotency, signatures, audit, and execution when equivalence matters.

### Bound resource use before semantics

Reject excessive request-line, field, body, decompressed-content, nesting, collection, string, digit, multipart-part, and file sizes before allocating unbounded memory or performing expensive work. Compressed input needs both compressed and expanded limits. A tiny archive or content-encoded body can expand dramatically.

Parsing and validation have algorithmic costs. Deep recursion, overlapping schema alternatives, pathological regular expressions, enormous exact numbers, `uniqueItems` over complex values, and reference graphs can consume disproportionate CPU or stack. Bound depth, count, complexity, resolution, and wall time. Resource limits are contract constraints even if they are enforced by a proxy.

Authenticate early enough to apply tenant and rate policy, but do not require expensive token, database, or remote work before cheap framing rejection when that enables denial of service. The exact order depends on threat model and information leakage. A gateway rejection is defense in depth; the service still protects bypass and internal paths.

Use `413 Content Too Large` when content exceeds a declared or current processing limit. Do not parse the whole body merely to produce a detailed list of errors after the decisive size failure.

### Validate media type and syntax

`Content-Type` tells the recipient how to interpret request content. Reject unsupported media types with `415`, rather than trying several parsers until one accepts. Validate applicable content coding and character encoding. Sniffing creates ambiguity and can split security controls from application interpretation.

Syntactic validation answers whether the bytes form a document in that media type. Reject malformed JSON, duplicate object members under a strict interoperability policy, invalid UTF encodings, malformed multipart boundaries, or a broken patch instruction before structural validation. Use `400` when the request is malformed at this level under the API's status policy.

Parser configuration is part of the contract evidence. Disable nonstandard NaN and Infinity if the media type is JSON. Bound number digit counts before arbitrary-precision conversion. Decide whether duplicate names are rejected; last-value-wins parsing can let a gateway validate one value while a backend uses another.

### Apply structural constraints under an exact dialect

Structural validation covers instance types, required fields, allowed properties, lengths, cardinalities, numeric intervals, enumeration, patterns, and local conditionals. For JSON Schema, pin Draft 2020-12 or another exact dialect, resource registry, format assertion policy, and output configuration.

Constrain objects deliberately. `properties` does not imply presence; `required` does not imply type. Reject unknown request fields unless a documented extension mechanism needs them. An extension map should still bound names, values, count, and ownership. Never accept arbitrary fields simply because future compatibility might need them.

Constrain arrays by minimum, maximum, item schema, and uniqueness semantics. Schema-level uniqueness compares values, not domain identities in a database. Bound array size before quadratic or memory-heavy checks. For tuples, use dialect-correct positional keywords.

Constrain strings by semantic alphabet and length, not a broad regex copied from a blog. JSON Schema length uses Unicode code points, which is not bytes or grapheme clusters. Apply transport byte limits and user-facing length rules at their appropriate layers.

### Prefer positive languages to blacklists

Define what is allowed for structured identifiers, country codes, currencies, state tokens, sort fields, expansion paths, and operation names. An allowlist is especially appropriate for a finite language. A blacklist of quotes, angle brackets, slashes, or SQL words neither defines a domain nor prevents injection across encodings and interpreters.

Regular expressions are useful for regular lexical languages such as a bounded internal code. Anchor them when whole-string matching is intended, test Unicode behavior, and bound input length. They are poor substitutes for parsers for URLs, email addresses, programming languages, or nested formats. Use maintained parsers and then apply domain policy to the parsed components.

Validation never makes string interpolation safe. Use parameterized database queries, context-aware output encoding, fixed command argument arrays, sandboxed template systems, safe path APIs, and allowlisted network destinations. The same valid string can be dangerous in SQL, HTML, shell, LDAP, or a filesystem because those interpreters have different grammars.

### Define normalization as contract

Normalization can trim whitespace, case-fold an identifier, canonicalize Unicode, parse equivalent timestamps, or map aliases to a canonical code. Apply it only where the domain defines equivalence. Passwords, signatures, opaque tokens, filenames, and user-authored text often must preserve exact code points or bytes.

Let normalization be function $n:X\rightarrow X'$. If validation predicate $C$ was applied to $x$ but execution uses $n(x)$, require either $C(n(x))$ or a proven property $C(x)\Rightarrow C(n(x))$. Revalidation is normally clearer. Do not validate a short string, normalize it into a longer expansion, and execute without rechecking limits.

The order affects identity. Normalize before uniqueness lookup if the unique key uses the same canonical form. Bind idempotency fingerprints and request signatures to the documented form. If signatures cover transmitted bytes, do not trim first and then claim signature evidence applies to transformed content.

Unicode normalization follows defined forms such as NFC or NFKC, but compatibility normalization can erase distinctions. Case folding differs from locale-sensitive presentation casing. State the algorithm and version policy where stable identifiers depend on it; do not apply a global lowercase-and-trim rule to every field.

### Use exact numeric constraints

Define numeric domain, units, scale, rounding, sign, inclusive or exclusive bounds, and overflow behavior. A JSON number is not inherently an IEEE 754 double. Parse money and other exact decimals into decimal or rational types, or use integer units when the domain supports a fixed exponent.

Test minimum, maximum, just-inside, just-outside, zero, negative zero if observable, excessive fractional precision, exponent forms, huge digit counts, and conversions into storage types. `multipleOf: 0.01` expresses a mathematical constraint; a binary floating-point remainder is not adequate evidence.

Cross-field numeric rules may include subtotal equals sum of lines, start no later than end, lower bound no greater than upper bound, and percentages totaling a defined amount. Decide which values the caller may assert and which the service calculates. Validating a client total does not make it authoritative.

### Make time and identifier rules semantic

A timestamp constraint needs a lexical format, offset policy, precision, allowed interval, authoritative clock, and event meaning. A syntactically valid future timestamp may be semantically wrong for `occurredAt` but valid for `expiresAt`. Account for clock uncertainty when comparing client and server times; do not use a one-second equality rule as hidden clock synchronization.

Identifiers may be opaque strings, caller-selected keys, or references to other resources. Validate lexical shape and length cheaply, but existence, tenant scope, lifecycle, and visibility require authorized lookup. Differentiate malformed identifier from well-formed but absent-or-hidden target only when disclosure policy allows.

Do not probe every possible reference before object-level authorization. A detailed “customer exists but belongs to another tenant” validation response leaks information. Bind lookup to the authorized universe or return a deliberately indistinguishable result.

### Express cross-field and conditional constraints

Field-local decorators cannot express every valid object. Model implications such as “if delivery is scheduled, `deliverAt` is required,” exclusions such as “exactly one of card token or bank mandate,” relationships such as `start <= end`, and cardinality such as at least one approver from an eligible set.

Make conditional guards require their discriminator fields. In JSON Schema, `properties` alone does not require a trigger; an `if` branch can succeed vacuously and apply an unintended `then`. Tagged unions with required constant tags often give clearer diagnostics than overlapping `oneOf` branches.

Validate the complete effective request after defaulting and normalization. For PATCH, validate both the instruction document and the candidate resulting resource. A sequence of individually valid field changes can violate a whole-resource invariant.

Choose whether to collect independent errors or stop early. Collecting field-local errors improves user repair. Stop after framing, parse, authority-sensitive, or cascading structural failures where later messages would be unreliable, expensive, or revealing. Preserve deterministic ordering and stable rule identifiers.

### Separate domain meaning from current state

Some constraints are stable domain rules: quantity must be positive, an interval must be ordered, and a command tag must be recognized. Others depend on mutable state: SKU is active, username remains unique, account has balance, transition is permitted, inventory is available, and version is current.

State validation can race. “Check username then insert” permits two requests to pass. Preserve uniqueness with a database or domain constraint at commit and translate the loser safely. “Check balance then debit” needs an atomic conditional transition, serializable rule, or versioned compare-and-set. Validation far from the effect is only advisory.

HTTP preconditions such as `If-Match` protect a declared state basis and normally fail with `412`. A domain lifecycle conflict can use `409` when the current state conflicts with the requested action. Content that is understood but violates stable semantic constraints can use `422` under a documented taxonomy. Do not decide status from which exception class happened to surface.

### Keep authorization distinct and ordered safely

Validation asks whether an input belongs to an admitted language and satisfies applicable rules. Authorization asks whether this actor may perform this action on this target and properties under current context. A perfectly valid transfer is still forbidden if the source account belongs to someone else.

There is no universal rule that all validation precedes authorization. Cheap syntax and size checks often precede lookup. Object authorization may need to precede detailed domain diagnostics to prevent existence and policy leaks. Field-level authorization must evaluate normalized intended effects. State and authority may need one transaction or policy snapshot.

Error equivalence is a security decision. Returning identical `404` for absent and unauthorized objects can preserve concealment. Timing, body size, validation detail, counts, and cache behavior must not defeat that choice. Log richer internal evidence under access control without echoing it to the caller.

### Validate files and remote references as hostile capabilities

For uploads, bound byte size and part count before buffering. Check declared and detected media characteristics, but do not treat a filename extension or client-provided MIME type as authoritative. Generate storage names, prevent traversal, isolate processing, scan where policy requires, and serve with safe content disposition and type. Image dimensions, archive expansion, parser complexity, and embedded active content matter beyond file size.

A well-formed URL is not safe to fetch. Parse it, restrict schemes and destinations, resolve and validate every address, prevent private and link-local access, control redirects, pin DNS behavior as needed, remove ambient credentials, bound response size and time, and use an isolated egress client. Validation that performs a fetch can itself be the SSRF effect.

References to internal resource IDs have analogous concerns: authorize target type and relationship, bind tenant scope, limit fan-out, and avoid existence oracles. Never accept arbitrary paths or service URLs in a batch merely because they match a regular expression.

### Make asynchronous and batch boundaries explicit

An asynchronous endpoint can perform admission validation before `202`, then fail later when mutable state or content processing changes. State which checks are complete at acceptance and which can still produce a terminal problem. Do not return `202` for obviously malformed or unauthorized input merely to simplify a queue producer.

For batch input, validate envelope size, item count, client item identifiers, dependency graph, and common fields before dispatch. Then validate and authorize every item under normal policy. Define atomic, best-effort, or dependency-aware outcome semantics. A per-item error model must not expose hidden targets through different classifications.

Cap the number and size of returned validation errors. An attacker can create thousands of failures to amplify CPU and response bytes. Indicate truncation and allow a legitimate consumer to repair deterministically.

### Implement a staged admission gate

The bounded fixture below separates cheap structural rules, normalization, domain lookup, and current-state validation. It does not model HTTP parsing, authorization, races, or a production validator.

<!-- bijux-verify: {"id":"staged-validation-gate","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"valid=accepted:ABC-1x2\nbad_shape=type:quantity\nbad_range=range:quantity\nunknown_field=unknown:role\nunsupported_sku=domain:sku\nstale_stock=state:stock\nchecks=6\nevidence=bounded_staged_validation\n","stderr":""}} -->
```python
catalog = {"ABC-1": {"stock": 8}}
allowed = {"sku", "quantity"}

def admit(request):
    unknown = sorted(set(request) - allowed)
    if unknown:
        return "unknown:" + unknown[0]
    if not isinstance(request.get("sku"), str):
        return "type:sku"
    if not isinstance(request.get("quantity"), int) or isinstance(request["quantity"], bool):
        return "type:quantity"
    if not 1 <= request["quantity"] <= 100:
        return "range:quantity"
    effective_sku = request["sku"].strip().upper()
    if not effective_sku or len(effective_sku) > 12:
        return "lexical:sku"
    product = catalog.get(effective_sku)
    if product is None:
        return "domain:sku"
    if request["quantity"] > product["stock"]:
        return "state:stock"
    return f"accepted:{effective_sku}x{request['quantity']}"

fixtures = {
    "valid": {"sku": " abc-1 ", "quantity": 2},
    "bad_shape": {"sku": "ABC-1", "quantity": "2"},
    "bad_range": {"sku": "ABC-1", "quantity": 0},
    "unknown_field": {"sku": "ABC-1", "quantity": 2, "role": "admin"},
    "unsupported_sku": {"sku": "ZZZ-9", "quantity": 1},
    "stale_stock": {"sku": "ABC-1", "quantity": 9},
}

for label, request in fixtures.items():
    print(f"{label}={admit(request)}")
print(f"checks={len(fixtures)}")
print("evidence=bounded_staged_validation")
```

In a real service, the stock check must share an atomic basis with reservation or return a state conflict. The normalized SKU must be the value used for lookup, fingerprinting, audit, and execution. Authorization must bind the catalog and product to the actor's legitimate scope.

### Return errors as bounded public contracts

Define a stable problem type for each recovery-relevant category. Include safe invalid-parameter entries with a public location syntax, stable rule code, and optionally a non-sensitive bound. Do not make localized messages, validator-library wording, regular expressions, schema paths, database constraints, or rejected secret values into machine contracts.

One request can have several independent field errors. Preserve deterministic order and cap entries. For cross-field errors, point to all relevant public fields or to the request root. For state conflicts, avoid calling a valid value “invalid” when the actual remedy is to refresh or change state.

Status and body must agree. Use `415` for unsupported request media type, `400` for malformed syntax under the chosen taxonomy, `422` for understood content that cannot be processed semantically, `409` for a conflict with current state where applicable, `412` for a failed HTTP precondition, and `413` for content limits. Authorization or non-disclosure can override the detail exposed.

### Treat constraint changes as API changes

Maintain each constraint with owner, reason, enforcement location, error code, examples, limits, and compatibility classification. A validator rule should trace to a consumer or invariant decision, not aesthetic preference. Remove redundant contradictory enforcement or prove the layers use the same source.

Before tightening, replay representative accepted requests, generate boundary witnesses, identify consumers, and stage telemetry that does not log sensitive content. A new rejection rate can reveal undocumented dependencies. Security fixes may require immediate enforcement, but still need incident handling, safe communication, and explicit compatibility accounting.

Validation rules can also loosen. Accepting more input can introduce ambiguous canonical forms, larger cost, new interpreter characters, or states the domain never handled. Review a widening with the same discipline as a narrowing.

## Definitions and Notation

Let raw request $r$ pass a sequence of partial transformations and predicates:

$$
r\xrightarrow{L}b\xrightarrow{P}x\xrightarrow{S}x\xrightarrow{n}x'\xrightarrow{D,c}q\xrightarrow{T,Z,c,s}q.
$$

$L$ enforces resource limits and framing, $P$ parses bytes $b$ into instance $x$, $S$ checks structure, $n$ normalizes into effective instance $x'$, $D$ checks stable domain meaning and maps to intent $q$, $T$ checks current state $s$, and $Z$ checks authorization under trusted context $c$. Each arrow can fail with a bounded public classification.

The admitted request language under context and state is:

$$
\mathcal{A}_{c,s}=\{r\mid L(r)\land P(r)\land S(P(r))\land D(n(P(r)),c)\land T(q,c,s)\land Z(q,c,s)\}.
$$

This notation suppresses operational ordering details and does not prove atomicity. A **local constraint** depends on one value. A **relational constraint** depends on several values. A **state constraint** depends on mutable authoritative state. A **commit constraint** is preserved at the effect boundary. A **canonical form** is the chosen representative of an equivalence class. A **validation oracle** maps a fixture to its expected accepted or rejected classification.

## Mechanisms, Invariants, or Proof Structure

1. Bound framing, encoded and expanded size, nesting, count, digits, and work.
2. Select the declared media type and parse strictly without interpretation guessing.
3. Validate schema under a pinned dialect, registry, number model, and format policy.
4. Reject forbidden or policy-disallowed unknown fields.
5. Normalize only documented equivalence classes and validate the effective value.
6. Evaluate cross-field and stable domain constraints on the complete intent.
7. Bind authorized references and property changes to trusted context.
8. Check mutable state atomically with effects or under explicit preconditions.
9. Execute through safe interpreters using the same accepted effective value.
10. Emit bounded actionable problems and test boundaries, costs, races, and changes.

The invariants are bounded work, single interpretation, exact value preservation, explicit normalization, full-object consistency, authorized reference scope, atomic state basis, interpreter safety, non-disclosing diagnostics, and reproducible constraint configuration.

## Alternatives and Trade-Offs

Fail-fast validation minimizes cost and leakage but forces repeated repair cycles. Collecting independent errors improves human and client ergonomics but increases computation and response amplification. Stop at framing, syntax, and authority-sensitive boundaries; collect a bounded deterministic set of trustworthy field errors afterward.

Edge validation rejects cheaply and standardizes common constraints. Service validation protects bypass paths and knows domain state. Database constraints close races and preserve storage invariants. Use all applicable layers from one governed contract where possible; do not let a gateway's looser copy or database's opaque error become the public authority.

Strict unknown-field rejection catches mistakes and overposting. Tolerant input supports some extension models. Prefer closed stable request objects with an explicitly bounded extension namespace when extensibility is a real requirement. Response readers can follow a more tolerant evolution policy.

Normalization improves matching and uniqueness but can alter user intent and create collisions. Preserve exact values where identity is opaque; normalize only fields whose domain equivalence is specified. Store display and canonical forms separately when both matter.

Synchronous state validation gives immediate errors but can increase latency and contention. Asynchronous validation supports expensive processing but moves some failures after acceptance. State the boundary honestly and reject cheap decisive failures before queueing.

## Failure Modes and Misconceptions

- **“Validation is a schema call.”** Schema is one structural layer; domain, state, authority, limits, and execution remain.
- **“Client validation protects the service.”** Clients are untrusted and can bypass it; server enforcement is authoritative.
- **“A regex makes input safe.”** Safety depends on the target interpreter and domain, not a character blacklist.
- **“Normalize after validation for convenience.”** Then execution can consume a value that never passed constraints.
- **“All Unicode strings with the same appearance are equal.”** Code points, normalization, graphemes, confusables, and domain identity differ.
- **“JSON numbers are doubles.”** The format's number model is broader; conversion must preserve required range and precision.
- **“Uniqueness validation prevents duplicates.”** A precheck races; preserve uniqueness at commit.
- **“Existence is a harmless validation detail.”** It can reveal another tenant's resources or policy.
- **“A valid URL is safe to retrieve.”** Destination, redirects, DNS, credentials, size, and egress policy remain.
- **“`422` is the validation status.”** Status follows the failed semantic boundary; malformed, unsupported, stale, and unauthorized cases differ.
- **“Return every error to be helpful.”** Unbounded or sensitive diagnostics enable amplification and information leakage.
- **“Accepted by the queue means valid.”** Asynchronous work must declare which checks can still fail later.
- **“Database constraints are implementation details.”** They can be the only atomic invariant enforcement, though errors need public translation.
- **“Loosening a rule is always compatible.”** It can create ambiguity, cost, unsafe characters, and unhandled states.
- **“Validation prevents injection.”** Parameterization and context-specific safe APIs prevent interpreter confusion.

## Worked Examples

### Example 1

**Situation:** A 100-byte gzip body expands to hundreds of megabytes. **Reasoning:** Enforce compressed and expanded limits during streaming decompression before materializing the document. **Conclusion:** byte validity without resource bounds is unsafe.

### Example 2

**Situation:** JSON contains two `role` keys, and a gateway and service retain different ones. **Reasoning:** Reject duplicate object names at the parser boundary. **Conclusion:** one message must have one interpretation across controls.

### Example 3

**Situation:** Username is length-valid before NFKC normalization but expands or collides afterward. **Reasoning:** Use only the domain's chosen normalization, then revalidate length and uniqueness on the canonical form. **Conclusion:** normalize-and-revalidate as one contract.

### Example 4

**Situation:** Price `0.29` fails a floating-point multiple-of-cent check. **Reasoning:** Parse into exact decimal or integer minor units under currency policy. **Conclusion:** numeric evidence must match mathematical constraints.

### Example 5

**Situation:** `start` and `end` each match timestamp format but `start > end`. **Reasoning:** Apply a relational constraint after parsing both instants and defining offset semantics. **Conclusion:** field validity does not imply object validity.

### Example 6

**Situation:** Two registrations both pass “username available.” **Reasoning:** Enforce canonical uniqueness in the commit and translate one result to a stable conflict. **Conclusion:** state validation must survive concurrency.

### Example 7

**Situation:** A caller supplies a well-formed customer ID from another tenant. **Reasoning:** Scope lookup to authorized customers or conceal the distinction; lexical validity grants nothing. **Conclusion:** references combine shape, state, and authority.

### Example 8

**Situation:** A URL field passes an RFC parser, then the service fetches `http://169.254.169.254/`. **Reasoning:** Use a controlled egress policy, address checks, redirect rules, and isolation; validation must not perform an unsafe probe. **Conclusion:** well-formed is not safe-to-dereference.

### Example 9

**Situation:** A batch of 10,000 invalid items returns 40,000 error objects. **Reasoning:** Reject the item-count limit early or cap deterministic errors with truncation metadata. **Conclusion:** diagnostics need amplification bounds.

### Example 10

**Situation:** A schema-valid PATCH changes `approved=true` without transition authority. **Reasoning:** Validate the patch document and resulting resource, then authorize the intended property transition atomically. **Conclusion:** structural validity does not confer domain permission.

## Cross-Program Connections

[Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) supplies parsing and interpretation models. [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies complexity and adversarial-cost analysis. [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies atomic constraints and uniqueness. [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies injection, SSRF, authorization, and disclosure reasoning. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies races, stale state, and atomicity boundaries.

## References

1. R. Fielding, M. Nottingham, and J. Reschke, [*RFC 9110: HTTP Semantics*](https://www.rfc-editor.org/rfc/rfc9110.html), especially request content and status semantics, Internet Standard, June 2022. Checked 2026-09-01.
2. A. Wright, H. Andrews, B. Hutton, and G. Dennis, [*JSON Schema Validation: A Vocabulary for Structural Validation of JSON, Draft 2020-12*](https://json-schema.org/draft/2020-12/json-schema-validation), 16 June 2022. Checked 2026-09-01.
3. A. Wright, H. Andrews, B. Hutton, and G. Dennis, [*JSON Schema: A Media Type for Describing JSON Documents, Draft 2020-12*](https://json-schema.org/draft/2020-12/json-schema-core), 16 June 2022. Checked 2026-09-01.
4. OWASP Foundation, [*Input Validation Cheat Sheet*](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html), OWASP Cheat Sheet Series. Checked 2026-09-01.
5. Unicode Consortium, [*Unicode Standard Annex #15: Unicode Normalization Forms*](https://unicode.org/reports/tr15/), living technical report. Checked 2026-09-01.
6. M. Nottingham, E. Wilde, and S. Dalal, [*RFC 9457: Problem Details for HTTP APIs*](https://www.rfc-editor.org/rfc/rfc9457.html), Standards Track, July 2023. Checked 2026-09-01.

## Exercises

### Exercise 1

Design an ordered validation pipeline for `POST /payments` covering framing, media type, parsing, schema, normalization, money, cross-field rules, payment-instrument reference, state, authority, idempotency, and safe execution. State which value each stage sees.

### Exercise 2

Specify constraints and boundary fixtures for a globally displayed username with a case-insensitive canonical identity. Cover bytes, Unicode normalization, grapheme expectations, allowed characters, length, confusables, uniqueness, reserved names, and compatibility.

### Exercise 3

Classify these failures and choose safe HTTP outcomes: oversized content, unsupported XML, malformed JSON, negative quantity, stale `If-Match`, closed order, unauthorized hidden order, rate exhaustion, and database uniqueness race. Explain where disclosure policy can change detail.

### Exercise 4

Threat-model an import request containing 50 files and a callback URL. Define pre-acceptance limits, asynchronous checks, file isolation, callback validation, terminal errors, and evidence that validation itself cannot become SSRF or decompression abuse.

### Exercise 5

A team plans to trim all strings, enable email format assertion, lower page-size maximum from 1000 to 100, reject unknown request fields, and loosen an enum. Classify each as normalization or constraint change, identify risks, and design rollout evidence.

## Answers to the Exercises

### Answer 1

Stream-bound request and expanded body size, select supported media type, parse strict JSON with duplicate rejection and exact decimals, then validate the operation-specific schema and reject unknown fields. Normalize only explicitly equivalent identifiers, not opaque tokens. Revalidate canonical values; check currency, positive exact amount, and cross-field instrument rules. Bind the instrument lookup to the authenticated tenant, check current instrument and payment state, and bind idempotency identity to the canonical intent. Commit eligibility and effect atomically or with a defined reconciliation mechanism. Parameterize every persistence/provider call. The executed command uses the same canonical amount, currency, instrument, actor, tenant, and idempotency fingerprint that passed validation.

### Answer 2

Set byte and code-point limits before expensive processing, choose a Unicode normalization form for identity, and recheck the canonical string. If display length is user-facing, separately bound grapheme clusters with a maintained Unicode implementation. Define a positive allowed language rather than banning a few characters. Decide whether visually confusable names are rejected, warned, or disambiguated without claiming normalization solves spoofing. Enforce canonical uniqueness atomically and apply reserved-name policy without exposing the whole list unnecessarily. Test empty, exact bounds, combining sequences, compatibility characters, case-fold expansions, script mixing, confusables, and collisions. Changing any algorithm or Unicode-dependent identity rule requires collision analysis and migration.

### Answer 3

Use `413` for the content limit, `415` for unsupported XML, `400` for malformed JSON under the stated taxonomy, and `422` for a well-formed negative quantity. A false HTTP validator uses `412`. A valid action conflicting with closed lifecycle can use `409`. An absent-or-hidden order can use the same `404` when concealment requires it, suppressing detailed validation. Rate exhaustion uses `429` under the rate contract. A uniqueness race is often a `409` domain conflict after atomic enforcement, not a `500`. Problem bodies state safe recovery and never contradict status; authority policy can deliberately reduce specificity and equalize timing or content.

### Answer 4

Limit total encoded and expanded bytes, file count, per-file bytes, filenames, archive members, nesting, declared formats, and callback field length before `202`. Authenticate and authorize import intent before queueing. Store with generated names in quarantine; isolate parsers, detect actual content, cap dimensions and expansion, scan under policy, and never execute embedded active content. Parse callback URL without fetching, restrict schemes and destinations, resolve through controlled egress, recheck redirect targets and addresses, remove ambient credentials, and cap response time and size. The operation resource distinguishes rejected-at-admission from later invalid-file, scan, processing, callback, cancellation, and expiry outcomes without exposing internal paths. Test archives, parser bombs, DNS/redirect changes, private addresses, and retry amplification.

### Answer 5

Global trimming is a normalization change and is unsafe for secrets, signatures, opaque identifiers, and authored text; scope it field by field and compare canonical collisions. Enabling email format assertion narrows accepted instances and can reveal validator differences. Lowering page size rejects former inputs and needs usage evidence, warning, and migration unless urgent capacity risk requires faster enforcement. Rejecting unknown fields tightens the request language but improves typo and overposting defense; observe current unknowns and provide an explicit extension path where justified. Loosening an enum widens input and can create unsupported states or ambiguity. Replay sampled redacted requests, generate boundary witnesses, compare validators, exercise downstream state machines, stage metrics, notify consumers, and document security-driven exceptions.
