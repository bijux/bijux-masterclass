---
module_id: API-027
program: API & Service Engineering
level: 1
module_number: 27
title: Examples and Executable Documentation
status: complete
last_verified: 2026-09-01
---

# Examples and Executable Documentation

## One-Page Review

### Governing question

How can API examples communicate representative decisions and exact wire behavior while remaining valid, safe, deterministic, versioned, and executable enough to detect drift?

### Essential definitions

- An **example value** is one concrete member of a contract's admitted input or output set; it does not define the whole set.
- A **scenario fixture** couples request context, serialized exchange, expected outcome, and observable postconditions.
- **executable documentation** is documentation whose machine-checkable claims run in a repeatable verification pipeline.
- A **golden fixture** is reviewed expected output compared bytewise or semantically under an explicit normalization policy.
- A **negative example** is an intentionally rejected input paired with its expected safe failure classification.
- A **boundary witness** is a concrete value at or immediately around a declared constraint boundary.
- A **sanitized example** is synthetic or transformed data with no recoverable secret, personal, tenant, or production identity.

### Central model, mechanism, or theorem

Represent a scenario as $e=(c,q,w,r,o)$: context $c$, logical request $q$, serialized wire exchange $w$, expected response $r$, and later observable outcome $o$. Schema validation checks only selected values; serialization checks $q\leftrightarrow w$; protocol checks status, headers, and media types; behavior checks $o$. An executable example is trustworthy only to the extent that its oracle, environment, dependencies, and observations are controlled and named.

### Critical invariants

Every published example names its purpose and contract version. Data examples validate under the exact resolved schema and dialect. Serialized examples obey media type, parameter style, escaping, and encoding. Request and response status, headers, content, and meaning agree. Failure, boundary, omission, null, concurrency, and authorization cases accompany the happy path. Fixtures use synthetic non-secret identities. Clocks, IDs, order, randomness, and external dependencies are controlled. Executed scenarios run against isolated state and clean it safely. A generated or mocked example never claims deployed behavioral conformance by itself.

### Common failures

One “typical” happy path; examples that violate required fields; schema `examples` treated as exhaustive or validating; singular and plural OpenAPI example fields used together; JSON-shaped examples for non-JSON wire encodings; copying production tokens and personal data; timestamps and IDs that change every run; exact snapshots of irrelevant ordering; mocks that return undocumented outcomes; destructive examples aimed at shared environments; curl commands without status or error handling; and documentation generated once but never checked against source, implementation, or consumers.

### Compact example

A create-order scenario contains a synthetic request, exact `application/json` bytes, `201` status, `Location`, response value, and validator. A second scenario reuses the idempotency key after simulated response loss and expects the same logical order rather than another effect. Schemas validate both bodies, but only execution checks duplicate behavior. **Conclusion:** useful documentation joins shape, wire representation, protocol outcome, and behavioral observation.

### Connections

[OpenAPI Structure](023-openapi-structure.md) places Example Objects at parameters, headers, and media types. [JSON Schema](022-json-schema.md) supplies value validation, and [Validation Constraints](025-validation-constraints.md) supplies negative and boundary witnesses. [API Contracts and Behavioral Guarantees](021-api-contracts-and-behavioral-guarantees.md) supplies the postconditions examples must not overclaim. [Mocking and Consumer Exploration](../ROADMAP.md) later uses these fixtures interactively.

## Governing Question

Which example forms, scenario metadata, checks, environments, and review rules turn API documentation into reliable learning and drift-detection evidence rather than plausible but stale prose?

## Why This Matters

Consumers begin with examples because examples compress a large contract into one concrete path. A good example answers where a value goes, how it is encoded, which fields are supplied, what status and headers return, and what the consumer does next. It also gives producers a fixture for validation, serialization, mocking, testing, review, and compatibility.

That compression creates risk. One example cannot describe all admitted messages, failure branches, concurrency, permissions, or change rules. Consumers may copy incidental field order, ID shapes, enum values, timestamps, or omission behavior as if normative. Producers may update a schema while leaving examples stale. A mock can remain green while the service duplicates effects or reveals restricted fields.

OpenAPI Specification 3.2.0 has several example locations and distinguishes logical `dataValue` from `serializedValue`, external serialized content, and legacy `value`. It states that media-type examples should match the associated schema and format, while tooling may or may not validate them. JSON Schema's plural `examples` keyword is annotation, not an assertion. Therefore, examples become reliable only when the project adds explicit verification.

Execution raises further concerns. Documentation commands can mutate state, spend money, send messages, create accounts, or disclose credentials. Test environments can drift or be shared. Responses contain dynamic IDs and times. Executable documentation needs the same isolation, least privilege, deterministic controls, and evidence boundaries as other integration tests.

## Prerequisites and Retrieval

Retrieve OpenAPI Example, Media Type, Parameter, and Header Objects; JSON Schema annotations and validation; HTTP messages and status semantics; media-type serialization; request/response ownership; failure contracts; deterministic testing; authentication; data classification; idempotency; state cleanup; and contract testing.

Before publishing an example, retrieve the exact contract version, resolved schema resources, serialization settings, example purpose, data classification, environment, credentials model, setup and teardown, expected observations, and responsible owner.

## Learning Objectives

By the end of this module, you should be able to:

1. choose the correct OpenAPI and JSON Schema example locations;
2. distinguish logical values from serialized parameter, header, and media-type examples;
3. design positive, negative, boundary, workflow, and recovery scenarios;
4. validate examples against schemas and serialization rules;
5. execute scenarios safely with deterministic state and scoped assertions;
6. prevent secret, personal-data, and production-state leakage; and
7. govern example provenance, ownership, compatibility, and drift evidence.

## Core Exposition

### Give every example a job

An example should answer a named consumer question. Useful purposes include:

- smallest successful request;
- ordinary representative response;
- omission versus explicit null;
- exact lower or upper boundary;
- each tagged-union branch;
- invalid syntax or semantic constraint;
- authorization or non-disclosure outcome;
- concurrency conflict and refresh path;
- accepted asynchronous work and terminal observation;
- duplicate or retry reconciliation; and
- compatible handling of unknown response data.

Do not call one object “the example” without stating what it demonstrates. `completeOrder`, `minimumPage`, `staleValidator`, or `paymentDeclined` are better fixture names than `example1` or `sample`. Keep descriptions focused on the decision; the schema remains authoritative for the broader valid set.

A small portfolio beats a huge kitchen-sink message. The smallest valid example exposes true requirements. A representative example helps onboarding. Boundary and failure witnesses protect semantics. A maximal payload often becomes unreadable and accidentally teaches that every optional field should be sent.

### Choose the correct OpenAPI example form

OpenAPI 3.2.0 permits examples in Parameter Objects, Header Objects, and Media Type Objects. Their singular `example` and plural `examples` fields are mutually exclusive. The plural form maps names to Example Objects or references and supports metadata and multiple cases.

Schema Objects also have example annotations: use the current JSON Schema plural `examples` array for data values. The older singular Schema Object `example` is deprecated in current OAS and mainly exists for compatibility. A Schema Object example describes a valid instance independent of a particular HTTP location or serialization; a Media Type or Parameter example can demonstrate use-site and wire semantics.

OpenAPI 3.2.0 Example Objects distinguish:

- `dataValue`: the logical data structure, which must be valid under the relevant schema;
- `serializedValue`: a Unicode string showing the serialized and escaped form;
- `externalValue`: a URI identifying separately stored serialized content; and
- `value`: a legacy/convenience literal, safest for JSON-compatible targets and deprecated for non-JSON serialization targets.

Field coexistence has exact rules. `dataValue` can accompany a matching serialized or external form. `serializedValue`, `externalValue`, and `value` are mutually constrained and should not ambiguously compete. Prefer `dataValue` for JSON and use `serializedValue` or `externalValue` when exact non-JSON encoding matters.

### Separate logical data from wire serialization

The logical query value `{tags: ["red blue", "green"]}` is not the URL text. Parameter location, schema or content, `style`, `explode`, delimiter rules, percent encoding, and media type determine the serialized form. A useful parameter example can include both logical `dataValue` and exact `serializedValue` so tooling and consumers can verify the mapping.

<!-- bijux-verify: {"id":"parameter-data-and-wire-example","mode":"data","language":"yaml","toolchain":"none","reason":"Declarative OpenAPI 3.2 parameter example contrasting logical data with its serialized query form."} -->
```yaml
name: tags
in: query
style: form
explode: false
schema:
  type: array
  items: {type: string}
examples:
  spacedTag:
    summary: Two tags, one containing a space
    dataValue: [red blue, green]
    serializedValue: tags=red+blue,green
```

The exact space representation depends on the defined serialization context; do not invent one from a URL library's defaults. Headers, cookies, matrix-like path encodings, multipart bodies, and form bodies each have their own rules. An example that validates as a JSON value can still be wrong on the wire.

For JSON media types, the JSON-compatible value usually carries both data and serialization meaning without ambiguity. Even then, number precision, duplicate names, Unicode escapes, and byte-level signatures may require a serialized fixture. State whether object member order or whitespace is irrelevant or intentionally canonicalized.

### Place examples near the strongest context

A leaf Schema Object can carry domain-wide value examples such as valid `OrderId` or `Money`. A request Media Type example can demonstrate required fields and direction. A response Media Type example sits under one status and therefore communicates outcome context. A Parameter example communicates location and serialization. An Example Object under `components.examples` can be reused when the whole example meaning is stable.

Avoid distant reuse that removes context. The same JSON body under `201` and `409` cannot be one example merely because both contain `id`. A shared request example can be sound across operations only if ownership, defaults, and meaning agree. Reference reuse carries compatibility coupling just like schema reuse.

External examples are appropriate for large, binary, XML, multipart, or separately maintained fixtures. Their URI resolution, integrity, availability, media type, and version become dependencies. Pin them in an offline build registry and do not let validation fetch arbitrary network locations.

### Validate every positive example

Resolve the exact OpenAPI document, Schema Object dialect, external schema resources, media type, and direction. Validate every `dataValue` and JSON-compatible value against its use-site schema. Check required and unknown properties, formats under the project's policy, exact numbers, unions, conditionals, and read/write direction.

Validation should fail the build on drift. A warning that nobody sees lets invalid documentation ship. Report the named example, operation, status, media type, instance location, and schema location. Do not silently “repair” an example by inserting defaults; that hides the actual contract.

Schema validation is necessary but insufficient. Check that a response example contains no write-only or restricted fields, that a request example contains no read-only or derived fields, and that every referenced ID and enum has meaningful semantics. Validate Problem Details examples against both schema and the status under which they appear.

If examples use dynamic times or IDs, validate a stable templated data form before rendering or substitute deterministic values. A placeholder like `<id>` is not a valid instance unless the schema admits it; use an explicitly documented template language or a valid synthetic ID.

### Verify serialization and parsing round trips

For each logical value $q$ and serialization function $s$, test that parsing its wire representation returns an equivalent value under contract: $p(s(q))\equiv q$. Equality must account for documented normalization, number model, repeated fields, order, and omission. Do not assume client and server libraries agree on arrays or spaces.

Round-trip query parameters, path segments, cookies, headers, form bodies, multipart names, and non-JSON media types with the same libraries or conformance rules used in production. Check `Content-Type`, character encoding, boundaries, content coding, and reserved characters. For response examples, exercise client decoding as well as server encoding.

Golden byte fixtures are useful for signatures, canonical formats, or exact protocol messages. Semantic comparisons are more robust when whitespace, property order, boundary tokens, or generated IDs are irrelevant. Choose and document the comparator; indiscriminate snapshot testing either misses meaning or causes constant noise.

### Make negative examples first-class

Positive examples demonstrate membership in the valid set. Negative examples test the boundary and error contract. Pair each invalid request with one intended primary cause and expected status, problem type, public field locations, recovery, and absence of effects.

Avoid examples with five simultaneous defects. A validator might reject the first while a missing rule remains hidden. Use focused fixtures for missing required field, wrong type, just-outside numeric bound, unknown field, invalid union tag, cross-field inconsistency, stale validator, forbidden property, and hidden target.

Not every rejection belongs to schema validation. Malformed JSON tests parsing; unsupported media type tests negotiation; `413` tests resource limits; `409` tests current state; `412` tests HTTP preconditions; `403` or concealed `404` tests authority. Keep the oracle at the correct layer.

Negative response documentation must not publish a secret, stack trace, database constraint, internal hostname, or another tenant's fact. Use synthetic values and explicitly assert prohibited fields are absent.

### Cover boundaries and partitions deliberately

For an inclusive range $a\le x\le b$, useful witnesses include $a$, a representative interior value, $b$, and just-outside values when the number model defines them. For string length, include empty, minimum, maximum, and one beyond. For arrays, include zero, one, maximum, overflow, duplicates, and order-sensitive cases. For unions, include every branch, unknown tag, missing tag, and overlap.

Partition by semantics, not combinatorial explosion. Currency, actor role, state, media type, and locale might produce hundreds of combinations. Use pairwise or risk-based coverage, then add cases for high-consequence interactions such as restricted fields in cached localized responses.

Every boundary example should trace to a constraint owner and expected classification. A pile of fixtures without a coverage map can repeat easy cases while omitting null, retries, concurrency, or authorization.

### Write scenario fixtures around whole exchanges

A scenario fixture expands beyond one value. Record:

- contract and fixture version;
- purpose and source owner;
- preconditioned state and actor capability;
- method, target, request headers, and content;
- exact or semantic wire expectations;
- response status, headers, media type, and body;
- later observable effects or state;
- permitted nondeterminism and normalization;
- cleanup and isolation strategy; and
- evidence limitations.

<!-- bijux-verify: {"id":"scenario-fixture-shape","mode":"data","language":"yaml","toolchain":"none","reason":"Declarative scenario fixture showing context, request, response, and postcondition fields for executable documentation."} -->
```yaml
id: create-order-minimum
contract: orders-2026-09
context:
  actor: synthetic-buyer
  tenant: fixture-tenant
request:
  method: POST
  target: /orders
  contentType: application/json
  body: {currency: SEK, lines: [{sku: ABC-1, quantity: 1}]}
expect:
  status: 201
  headers: [Location, ETag]
  bodySchema: OrderResponse
  postcondition: one-order-with-request-identity
```

The fixture does not embed a real bearer token. The runner obtains a least-privilege short-lived credential through its environment and never prints it. The fixture's actor label selects capability; it is not the credential itself.

### Turn examples into layered checks

One pipeline can derive several checks from the same fixture:

1. parse the example artifact strictly;
2. resolve references and validate data values against schemas;
3. serialize logical values and compare expected wire forms;
4. lint status, headers, media types, security, and response coverage;
5. render documentation and verify links and code blocks;
6. configure a mock and run consumer parsing;
7. execute against an isolated provider;
8. assert immediate response and later postconditions; and
9. compare compatibility against prior contract versions.

Each result has a different claim. Schema success proves structural membership under one configuration. Mock success proves the consumer handles that configured fixture. Provider execution proves one observed scenario in one environment. None proves all behavior or every valid input.

The bounded checker below audits a tiny fixture catalog for schema classification, status coherence, unique names, and coverage categories. It is not an HTTP runner or OpenAPI validator.

<!-- bijux-verify: {"id":"example-catalog-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"create_minimum=valid-success\nmissing_currency=invalid-validation\nstale_version=valid-conflict\nunauthorized_order=valid-nondisclosure\nexamples=4\ncategories=4\nunique_names=true\nevidence=bounded_example_catalog\n","stderr":""}} -->
```python
catalog = {
    "create_minimum": {"schema": "valid", "outcome": "success"},
    "missing_currency": {"schema": "invalid", "outcome": "validation"},
    "stale_version": {"schema": "valid", "outcome": "conflict"},
    "unauthorized_order": {"schema": "valid", "outcome": "nondisclosure"},
}

allowed = {
    ("valid", "success"),
    ("invalid", "validation"),
    ("valid", "conflict"),
    ("valid", "nondisclosure"),
}
for name, fixture in catalog.items():
    classification = (fixture["schema"], fixture["outcome"])
    assert classification in allowed
    print(f"{name}={classification[0]}-{classification[1]}")

categories = {fixture["outcome"] for fixture in catalog.values()}
print(f"examples={len(catalog)}")
print(f"categories={len(categories)}")
print("unique_names=true")
print("evidence=bounded_example_catalog")
```

### Control nondeterminism

IDs, clocks, random choices, ordering, pagination cursors, signatures, and asynchronous completion make examples unstable. Prefer deterministic injected clocks, seeded data generators, fixed fixture identities, isolated namespaces, and stable sort tie-breakers. Normalize only fields declared irrelevant to the oracle.

Do not replace every dynamic value with a wildcard. Wildcards can hide missing, malformed, or cross-tenant data. Use predicate assertions: ID matches the public format and is stable across retry; timestamp falls between recorded start and end; `Location` matches response identity; collection order follows the declared comparator.

Concurrency examples need controlled scheduling or deterministic state transitions. For stale-update behavior, create version 1, read its validator, advance to version 2, then submit with the stale validator and expect `412`. A sleep is not a correctness mechanism.

Asynchronous examples should poll through a bounded documented observation contract or use a controlled event signal. Assert allowed intermediate states and terminal outcome without promising a timing bound the service does not guarantee.

### Execute without harming shared systems

Default executable documentation to a local or ephemeral isolated environment. Use fixture tenants, generated resource namespaces, least-privilege credentials, quotas, egress restrictions, and no real payment, email, SMS, or webhook effects. Destructive operations require disposable targets created by the scenario itself.

Setup and cleanup must be idempotent. Prefer automatic expiration and namespace deletion after explicit target validation. Preserve failure artifacts under access control without leaving live state indefinitely. Never make cleanup broad enough to target a workspace root, production account, or unrelated tenant.

If a read-only public sandbox is the only environment, limit execution to authorized safe operations and make mutation examples non-executable with a stated reason. Documentation commands should not instruct consumers to paste long-lived tokens into shell history or URLs.

Network calls from examples need bounded timeouts, retries only under contract, redacted logs, and an allowlisted destination. A runner must not follow an example's arbitrary callback or external URL with ambient credentials.

### Keep examples synthetic and non-sensitive

Do not copy production payloads and replace only the obvious name. Quasi-identifiers, timestamps, addresses, free text, IDs, rare combinations, signed URLs, tokens, and error instances can reidentify people or systems. Prefer purpose-built synthetic fixtures with clearly reserved domains and impossible production tenant namespaces.

Use `example.test`, `example.com`, and other reserved documentation domains appropriately. Use obviously synthetic phone numbers and payment test tokens supplied by the relevant sandbox. Never embed private keys, real bearer tokens, cookies, API keys, database IDs, internal DNS names, or proprietary incident text.

Secret scanning is defense in depth, not sanitization proof. Review data lineage and classification. External examples and generated artifacts need the same checks as the OpenAPI source. Documentation screenshots can leak data too, even if machine fixtures are clean.

### Make examples accessible and useful to humans

Explain prerequisites, shell assumptions, placeholders, and expected output. Commands should fail visibly on unexpected status. Show headers when they matter. Avoid screenshots of text that cannot be copied or read by assistive technology. Provide language-neutral HTTP examples before generated client-specific variants where possible.

Keep examples small enough to scan and annotate only non-obvious decisions. Do not repeat the entire schema in prose. Link from failures to recovery and from accepted asynchronous work to observation. A user should be able to tell which fields to replace and which are fixed synthetic fixtures.

Generated SDK examples must compile under a pinned released SDK. Avoid using unreleased method names. If snippets omit production error handling for focus, say so and provide a durable complete reference nearby.

### Govern provenance and drift

Treat example files as contract artifacts with owner, source, contract version, generation method, and verification status. Store external fixtures beside governed sources or in an immutable registry, not on a personal paste site. Review example changes with the schema or behavior they demonstrate.

Generate documentation from verified fixtures where practical, so visible examples and executed bytes share one source. If prose needs abbreviation, link it to the full fixture and test that the excerpt remains meaningful. Do not regenerate reviewed examples from random schemas on every build.

Track coverage by operation, status family, media type, union branch, constraint boundary, role, retry, and state transition. Coverage counts guide review but do not prove completeness. Retire examples when their purpose disappears; do not leave obsolete deprecated calls as the first onboarding path.

On each contract change, identify impacted fixtures, validate against old and new schemas, run consumer and provider scenarios, and publish changed expectations with migration guidance. A stale example is a contract defect, not cosmetic documentation debt.

## Definitions and Notation

Let scenario fixture be:

$$
e=(v,p,c,q,w,r,o,\alpha),
$$

where $v$ is contract version, $p$ purpose, $c$ controlled context, $q$ logical request, $w$ serialized exchange, $r$ expected immediate response, $o$ later observable outcome, and $\alpha$ the allowed nondeterminism and comparison policy.

For serializer $s$ and parser $d$, a round-trip fixture requires $d(s(q))\equiv_\alpha q$. Execution observation $\hat{o}$ passes only when $\hat{o}\models_\alpha o$ under the named environment. This is evidence for one scenario, not universal conformance.

Let coverage map $K:E\rightarrow 2^C$ assign each example a set of categories such as operation, outcome, boundary, role, and media type. Coverage is the union $\bigcup_{e\in E}K(e)$; counts do not establish that partitions were chosen correctly.

An **oracle** is the expected classification or observation. A **comparator** defines exact, semantic, predicate, or normalized equality. A **fixture namespace** isolates created state. A **template placeholder** is a declared substitution token, not an invalid value disguised as an example. **Provenance** records where an example came from and how it was verified.

## Mechanisms, Invariants, or Proof Structure

1. Assign each example a consumer question, owner, and contract version.
2. Choose Schema, Parameter, Header, Media Type, or scenario scope deliberately.
3. Separate logical `dataValue` from serialized and external representations.
4. Validate positive data and focused negative classifications under exact schemas.
5. Round-trip serialization using declared media-type and parameter rules.
6. Check status, headers, content, problem types, and later postconditions together.
7. Control clocks, IDs, order, randomness, dependencies, and comparison policy.
8. Execute only in isolated least-privilege environments with safe cleanup.
9. scan and review every source and generated artifact for sensitive data.
10. Track coverage, provenance, consumer evidence, and drift on every change.

The invariants are named purpose, schema consistency, wire accuracy, protocol coherence, behavioral scope, focused oracles, deterministic execution, non-sensitive data, isolated effects, and versioned provenance.

## Alternatives and Trade-Offs

Inline examples maximize local context but duplicate values. Referenced Example Objects centralize a stable scenario but can hide operation-specific meaning. Reuse only when status, media type, direction, and purpose agree, not merely when bodies resemble each other.

Hand-authored examples optimize pedagogy and edge cases. Generated examples cover broad schemas and reduce labor but often choose meaningless strings, omit behavioral context, and change nondeterministically. Use generation to propose or fuzz, then review and pin durable public examples.

Golden byte snapshots detect exact drift but are brittle around irrelevant formatting and dynamic fields. Semantic or predicate comparisons reduce noise but can become too permissive. Choose the narrowest comparator that ignores only contractually irrelevant variation.

Provider execution gives strong scenario evidence but costs environment setup and can be flaky or dangerous. Static validation is cheap and safe but misses behavior. Layer both, keeping non-executable destructive or third-party scenarios clearly labeled.

One end-to-end fixture is realistic but hard to diagnose and slow. Focused component and contract fixtures localize failures. Maintain a small number of representative end-to-end journeys plus many precise lower-level examples.

## Failure Modes and Misconceptions

- **“An example defines the contract.”** It is one instance; schemas and behavioral rules define the supported set.
- **“Schema `examples` are validated assertions.”** They are annotations unless project tooling performs explicit checks.
- **“OpenAPI validates every example automatically.”** The specification permits tool choice; the build must require verification.
- **“A JSON-shaped parameter example shows the URL.”** Serialization style, explosion, delimiters, and encoding still apply.
- **“`example` and `examples` can coexist.”** They are mutually exclusive in applicable OpenAPI objects.
- **“One happy path is enough for onboarding.”** Consumers also need failure, boundary, retry, and authorization decisions.
- **“A mock proves the provider works.”** It proves behavior of the configured mock and consuming code for that fixture.
- **“A placeholder is automatically valid.”** `<id>` can violate the schema; use a declared template or valid synthetic value.
- **“Snapshots should ignore every dynamic field.”** Broad wildcards can hide malformed, missing, or cross-tenant values.
- **“Sleep makes asynchronous examples deterministic.”** Poll a bounded observation contract or use controlled signals.
- **“Cleanup can delete everything in the test account.”** Target only the validated fixture namespace and prefer automatic expiry.
- **“Redacting a name sanitizes production data.”** Quasi-identifiers, free text, IDs, and rare combinations can remain sensitive.
- **“curl success means HTTP success.”** Commands must inspect status and expected content, not only process exit.
- **“Generated SDK snippets are documentation by default.”** They need compilation, released-version pinning, and error-path review.
- **“Coverage percentage proves completeness.”** Categories and oracles can be wrong or omit entire risks.

## Worked Examples

### Example 1

**Situation:** The only create example supplies every optional field. **Reasoning:** Add the smallest valid request to reveal true requirements and keep a separate representative rich case. **Conclusion:** minimal and typical examples answer different questions.

### Example 2

**Situation:** Query `tags=["red blue","green"]` is shown as JSON after `?tags=`. **Reasoning:** Apply declared parameter serialization and percent encoding, then show logical and serialized forms. **Conclusion:** data validity does not prove wire accuracy.

### Example 3

**Situation:** A request example includes server-generated `id` and `createdAt`. **Reasoning:** Validate direction and field ownership, then remove derived fields. **Conclusion:** schema compatibility without direction can teach overposting.

### Example 4

**Situation:** A `409` example uses a success body with `error: true`. **Reasoning:** Put it under the `409` response with `application/problem+json`, stable type, and recovery fields. **Conclusion:** status and body must model one outcome.

### Example 5

**Situation:** A negative quantity fixture also omits currency and adds an unknown field. **Reasoning:** Split it into focused examples so each rule has an unambiguous oracle. **Conclusion:** one primary defect improves diagnostic evidence.

### Example 6

**Situation:** Response snapshots fail because IDs and timestamps differ. **Reasoning:** Assert public ID format and cross-field identity, and bound timestamps by the scenario clock window. **Conclusion:** predicate comparison controls legitimate nondeterminism without wildcards.

### Example 7

**Situation:** An idempotency example only checks two `201` bodies. **Reasoning:** Simulate response loss, replay the same logical identity, and assert one durable resource/effect plus the documented duplicate response. **Conclusion:** behavioral examples observe effects, not only shapes.

### Example 8

**Situation:** Documentation embeds a real expired bearer token “because it no longer works.” **Reasoning:** History, token structure, account metadata, and accidental reactivation remain risks. Replace it with a synthetic placeholder and environment-provided credential flow. **Conclusion:** expired secrets do not belong in examples.

### Example 9

**Situation:** A destructive DELETE tutorial runs against whichever base URL is exported. **Reasoning:** Require an allowlisted local host, create a fixture-owned target, validate its namespace, and clean only that target. **Conclusion:** executable docs need destructive-action guards.

### Example 10

**Situation:** An example still validates after an enum addition, but an old generated client crashes. **Reasoning:** Add an unknown-enum consumer fixture and compile it against the supported client version. **Conclusion:** structural validity is not consumer compatibility evidence.

## Cross-Program Connections

[Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies fixtures, oracles, partitions, snapshots, and deterministic execution. [Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) supplies isolated pipelines and release evidence. [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies secret handling, data classification, least privilege, and safe environments. [Developer Experience in Platform Engineering](../../29-platform-engineering/ROADMAP.md) consumes verified examples in portals and templates. The API program retains ownership of public meaning.

## References

1. OpenAPI Initiative, [*OpenAPI Specification 3.2.0*](https://spec.openapis.org/oas/v3.2.0.html), especially Example Object, Working with Examples, Media Type, Parameter, Header, and serialization sections, 19 September 2025. Checked 2026-09-01.
2. A. Wright, H. Andrews, B. Hutton, and G. Dennis, [*JSON Schema Validation: A Vocabulary for Structural Validation of JSON, Draft 2020-12*](https://json-schema.org/draft/2020-12/json-schema-validation), including metadata annotations, 16 June 2022. Checked 2026-09-01.
3. A. Wright, H. Andrews, B. Hutton, and G. Dennis, [*JSON Schema: A Media Type for Describing JSON Documents, Draft 2020-12*](https://json-schema.org/draft/2020-12/json-schema-core), including annotation collection and output, 16 June 2022. Checked 2026-09-01.
4. R. Fielding, M. Nottingham, and J. Reschke, [*RFC 9110: HTTP Semantics*](https://www.rfc-editor.org/rfc/rfc9110.html), Internet Standard, June 2022. Checked 2026-09-01.
5. M. Nottingham, E. Wilde, and S. Dalal, [*RFC 9457: Problem Details for HTTP APIs*](https://www.rfc-editor.org/rfc/rfc9457.html), including security considerations for problem detail, Standards Track, July 2023. Checked 2026-09-01.
6. IANA, [*IANA-Managed Reserved Domains*](https://www.iana.org/domains/reserved), including documentation domains. Checked 2026-09-01.

## Exercises

### Exercise 1

Design an example portfolio for `POST /orders`, including minimum success, representative success, two constraint boundaries, malformed input, semantic rejection, forbidden target, stale precondition, duplicate retry, and asynchronous alternative. Name each purpose and oracle.

### Exercise 2

Create OpenAPI 3.2 examples for an array-valued query parameter, a JSON request, and an XML response. Decide where `dataValue`, `serializedValue`, or `externalValue` belongs and how each is verified.

### Exercise 3

Turn a prose tutorial for create, retrieve, update with `If-Match`, and delete into safe executable scenarios. Specify environment guards, fixture state, credentials, deterministic values, assertions, and cleanup.

### Exercise 4

Audit a documentation repository containing copied production payloads, random generated IDs, live callback URLs, screenshots, singular and plural example fields, and uncompiled SDK snippets. Prioritize repairs and evidence.

### Exercise 5

An API change adds a response enum, tightens request maximum, changes query serialization, adds a `409`, and changes asynchronous timing. Identify affected example layers and design the compatibility verification matrix.

## Answers to the Exercises

### Answer 1

Use named fixtures such as `minimum_order_created`, `multi_line_order_created`, `quantity_minimum`, `quantity_above_maximum`, `malformed_json`, `end_before_start` where relevant, `customer_not_visible`, `stale_order_version`, `duplicate_request_identity`, and `order_acceptance_operation`. Each records logical and serialized request, context, expected status/media type/problem type, safe field assertions, and absence or presence of effects. Focus each negative case on one primary failure. The retry oracle counts one logical order and external effect. The async case expects `202`, an operation URI, allowed intermediate states, and a terminal link rather than a fixed sleep.

### Answer 2

For the query array, put a named Example Object on the Parameter Object with logical `dataValue` and exact `serializedValue` matching `style` and `explode`; round-trip it with the parameter codec. For JSON, put `dataValue` on the `application/json` Media Type example and validate it against the resolved request schema; a separate serialized form is usually unnecessary unless exact bytes matter. For XML, store logical `dataValue` when useful and use `externalValue` for the exact serialized document, pinned locally with media-type and schema/encoding checks. Do not combine singular `example` with plural `examples` at one location.

### Answer 3

Require an allowlisted ephemeral base URL and a fixture tenant, acquire a short-lived least-privilege credential without logging it, inject a clock and stable request identity, and create a uniquely prefixed resource. Assert `201`, `Location`, representation identity, and validator; GET and compare the authorized projection; update using that validator and assert the new validator; test one stale update; delete only the exact fixture URI and verify the documented absence state. Cleanup is idempotent and validates tenant and ID prefix before deletion, with automatic expiry as fallback. No command can run against production or an arbitrary exported URL.

### Answer 4

First revoke and investigate any credentials or reachable callbacks, remove sensitive payloads and history where policy permits, and replace them with synthetic fixtures. Review screenshots and external artifacts for personal or internal data. Add strict checks for mutually exclusive example fields, schema validity, serialization, and link resolution. Replace random public examples with reviewed deterministic values or explicit predicates. Pin and compile SDK snippets against released versions and exercise errors. Add provenance, owners, secret scanning, data-classification review, isolated execution, and a failing CI gate; scanners alone do not prove sanitization.

### Answer 5

The enum addition needs a new response example and old-client unknown-value test. The tightened maximum needs old boundary, new boundary, and changed-classification witnesses plus captured-request replay. Query serialization requires logical/wire round trips across supported clients and server parser. The new `409` needs status, Problem Details, recovery, mock, and provider scenarios. Timing changes require asynchronous fixtures that assert only the declared observation and terminal contract; update any objective bounds if truly contractual, never merely increase sleeps. Run schema, serialization, mock-consumer, isolated provider, postcondition, and old/new compatibility layers for every impacted operation.
