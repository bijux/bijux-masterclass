---
module_id: API-001
program: API & Service Engineering
level: 1
module_number: 1
title: Resources, Representations, and Messages
status: complete
last_verified: 2026-08-29
---

# Resources, Representations, and Messages

## One-Page Review

### Governing question

How should an API distinguish the thing being addressed, the information used to describe it, and the protocol exchange that carries that information?

### Essential definitions

- A **resource** is the conceptual target of an interaction: an account, report, collection, workflow, capability, or other abstraction identified by a URI. It is not automatically a database row, class, file, or handler.
- **Resource state** is the authoritative condition of that resource at some logical time, according to its owning domain. It can exceed everything exposed through an API.
- A **representation** is information intended to reflect a past, current, or desired state of a resource. In HTTP it comprises representation metadata and a potentially unbounded stream of representation data.
- A **representation variant** is one possible representation selected by media type, language, projection, authorization, time, or another dimension.
- A **message** is one protocol communication. An HTTP request communicates a method, target, fields, and optional content; a response communicates status, fields, and optional content.
- A **URI** identifies a resource. A route maps request targets into implementation behavior. An endpoint is an operational boundary. These related ideas are not synonyms.
- A **media type** labels the format and processing model of representation data. `application/json` establishes JSON syntax, not the domain meaning of each member.
- A **link** combines a target with a relation meaningful in context. A bare URI-valued string does not necessarily communicate what following it means.

### Central model, mechanism, or theorem

Use three distinct layers. Let (R) be a resource identified by URI (u), let (S_R(t)) be its authoritative state at logical time (t), let (V=f(S_R(t), c)) be a selected representation under context (c), and let (M=g(V, q)) be a protocol message under interaction context (q). Neither (V=S_R(t)) nor (M=V) follows in general. A representation may omit, transform, localize, aggregate, or protect state; a message adds method or status, control data, metadata, and delivery context. Good API design preserves these distinctions while stating how they relate.

### Critical invariants

A stable resource identity is not silently coupled to one encoding or implementation. Every representation has defined semantics, media type, provenance, authorization boundary, and relevant time or version context. A partial view never claims to be the whole state. Message metadata and content agree. Request representations describe intended meaning without pretending the server has already accepted it. Response status and representation describe the same outcome. Links state relations. Sensitive fields are minimized per audience. No serializer, schema, successful request, or example exchange is treated as proof that the domain model or real-world state is correct.

### Common failures

Teams call every route a resource; expose database tables as public identity; treat JSON, a schema, or an OpenAPI Path Item as the resource; assume one resource has one representation; confuse message content with domain state; put meaning in field names without units or lifecycle rules; return partial data as if complete; attach the wrong media type; interpret a response body independently of status and fields; version URIs around implementation releases; omit authorization-dependent variation; or believe transport success proves the represented fact is true.

### Compact example

`https://api.example.test/projects/prj-7` identifies one project resource. An authorized client may receive a detailed JSON representation; a reporting client may receive CSV; a screen reader workflow may receive localized text. Each message has its own status, fields, and content. The project remains the same conceptual resource, the representations differ, and none must disclose every authoritative project fact.

### Connections

URI and HTTP standards provide the common protocol vocabulary. Domain modeling determines resource identity and lifecycle. Security changes which representations are permitted. Distributed systems explain stale observations and lost exchanges. Data architecture governs authoritative state and lineage. Later API modules add methods, status codes, headers, negotiation, caching, contracts, evolution, and operations.

## Governing Question

What must remain distinct when a client asks a service to observe or change something through HTTP?

The resource is what the interaction is about. The representation is the communicable information selected to describe a state of that resource. The message is the request or response carrying protocol semantics and, sometimes, representation data. Conflating them makes APIs brittle: storage leaks into identity, encodings become impossible to evolve, partial views masquerade as truth, and clients attach meaning to accidental transport details.

## Why This Matters

HTTP is a uniform interface to resources, not a remote database protocol. RFC 9110 defines semantics independently of a particular HTTP wire version and describes communication through messages that transfer or manipulate representations. RFC 3986 defines a URI as an identifier for an abstract or physical resource. These abstractions let independently implemented clients, intermediaries, and services interact without sharing object layouts or database technology.

The distinction has practical consequences. A customer can persist for years while its JSON shape evolves. One URI can support accessible HTML, machine-oriented JSON, and an exported document. A response can represent a computed forecast rather than stored bytes. A request can carry a proposed future state that is rejected. A successful response can carry no representation data. A representation can remain syntactically valid yet be stale, unauthorized, misleading, or semantically wrong.

The distinction also bounds claims. An API can prove that bytes match a schema and that message metadata is internally consistent. It cannot infer that a patient took a medication, a payment legally settled, or a sensor measured reality correctly. Those claims depend on authoritative processes, time, identity, domain rules, uncertainty, and named human review. Protocol correctness is necessary evidence, not universal truth.

## Prerequisites and Retrieval

Retrieve client-server communication, byte encodings, basic JSON, sets and functions, identifiers, state machines, authorization, and the difference between syntax and semantics. Recall that a database row is an implementation record and a domain entity is an enduring concept with identity and rules. No prior mastery of HTTP methods, caching, OpenAPI, or REST constraints is assumed; those subjects receive dedicated treatment later.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish a resource, its authoritative state, a representation, representation data, message content, and a protocol message;
2. explain why a URI identifies rather than necessarily revealing storage location or implementation;
3. model several representations of one resource without changing its identity;
4. distinguish a route, endpoint, handler, schema, JSON object, and database row from a resource;
5. identify representation metadata and explain what a media type does and does not specify;
6. reason about current, past, desired, partial, derived, and authorization-specific representations;
7. review whether request and response control data agree with their content;
8. state invariants for identity, provenance, completeness, links, security, and time; and
9. calibrate executable, standards, operational, and human-review evidence without overclaiming correctness.

## Core Exposition

Start with the resource. Fielding's REST model treats a resource as a conceptual mapping to a set of entities or values over time. The abstraction can be concrete, such as a particular purchase order; collective, such as current open incidents; computed, such as today's weather forecast; procedural, such as a password-reset workflow; or informational, such as a policy document. The useful test is not “is there a table?” but “does this concept have identity, semantics, ownership, and a lifecycle worth addressing?”

A URI supplies an identifier within a naming scheme. In `https://api.example.test/projects/prj-7`, the scheme, authority, and path contribute to identification, but the path need not mirror a server directory or primary key. The service might compute the resource from several stores, forward the request, or retire its original database. Identity should survive implementation change when the conceptual resource survives. URI design details belong to later modules; the foundational rule is to avoid equating an identifier with a storage locator.

The same resource can change over time. Let (S_R(t)) denote its domain state at logical time (t). The state might include confidential attributes, internal workflow facts, audit history, and derived values unavailable to a particular client. “Current” must also be qualified: a replica, cache, projection, or export may reflect an earlier authoritative state. A response should therefore avoid implying freshness, completeness, or authority it cannot establish.

A representation is selected information about a resource state. RFC 9110 allows a representation to reflect past, current, or desired state. A response to a retrieval request often carries a current-state representation. An audit endpoint might return a historical representation. A modification request may carry a desired-state representation: the client proposes values, while the authority validates, authorizes, normalizes, rejects, or commits them. Receiving proposed JSON does not make it authoritative state.

Representations have metadata and data. Metadata tells a recipient how to interpret representation data: media type, content coding, language, and sometimes a more specific location or validator. The exact fields and negotiation algorithms come later, but the invariant begins here: bytes cannot safely interpret themselves. `{"temperature": 20}` lacks a unit, measurement time, sensor identity, uncertainty, and semantic vocabulary even though it is valid JSON.

Media type identifies a data format and processing model. `application/json` says the representation data follows JSON's grammar and interoperability rules. It does not say whether `20` means Celsius, a count, a code, or an identifier. Domain semantics require a contract: member meanings, required and optional states, null behavior, units, identifier scope, lifecycle, invariants, and compatibility rules. A more specific registered media type can carry additional semantics, but its specification must still be reviewed.

A resource can have multiple representation variants. Selection context (c) can include the requested media type, natural language, projection, role, locale, feature set, time, and policy. A detailed employee representation shown to payroll and a directory representation shown to colleagues may identify the same employee but disclose different attributes. That variation must be deliberate and protected; changing the serializer alone is not access control.

Conversely, equal bytes do not prove equal representations. The bytes `20` under `application/json` and `text/plain` invoke different processing models. Identical JSON obtained at different times may have different provenance or validators. The meaning of content depends on representation metadata and interaction context, not solely on a byte comparison. Content-addressed systems deliberately make byte identity important, but even there the surrounding resource and relation semantics remain explicit.

Now separate the message. An HTTP request message supplies method semantics, a target, fields, and optional content. A response supplies a status code, fields, and optional content. Message fields can govern authentication, negotiation, caching, conditional evaluation, tracing, and connection-independent semantics. Content is carried within one message; when it is intended as a representation, representation metadata describes how to interpret its representation data.

Not every message carries a representation. Some requests have no content. Some successful responses intentionally have no content. A `HEAD` response communicates selected representation metadata without transferring the corresponding representation data. Informational and certain other responses have special content rules. Those details matter later; for now, never make “response equals body” the mental model.

Message semantics are compositional. Status, fields, and content must tell one coherent story. A body that says an operation failed paired with a success status confuses generic clients, monitoring, intermediaries, and humans. JSON marked as `text/plain` may be displayed rather than processed. A cached representation served without the right variation controls may disclose one user's data to another. Correct body shape cannot repair contradictory message control data.

An implementation route is a dispatch rule such as `/projects/{id}`. A handler is code selected by that rule. An endpoint usually denotes an addressable operation at a service boundary. An OpenAPI Path Item describes operations associated with a path template. None is automatically the resource. Several handlers can operate on one resource; one handler can generate representations for several resource types; a gateway can change routes without changing public resource identity.

The database is likewise behind the boundary. Treating each table as a resource tends to expose internal joins, surrogate keys, normalization choices, deletion flags, and transaction boundaries. Useful API resources instead follow consumer tasks and domain authority. A project summary may combine project, membership, budget, and risk records. A workflow resource may have no durable row of its own. The API contract should remain meaningful if storage changes.

Partial and derived representations need honest semantics. A list item containing `id`, `name`, and `status` is often a projection, not a malformed full object. Marking fields “optional” without explaining omission leaves clients unable to distinguish unavailable, unauthorized, not applicable, not requested, unknown, and intentionally redacted. A derived risk score should name its observation time, model or rule version where relevant, and uncertainty; otherwise a client may treat a historical estimate as current fact.

Links connect resources through typed relations. RFC 8288 defines a link as a relation between a context resource and a target resource. A member named `url` is only a string unless the contract states its relation and use. Relations such as `next`, `self`, or domain-specific transitions let clients understand why a target matters. Links do not automatically grant permission, prove reachability, or make a transition safe.

Error information is also representational. RFC 9457 defines a reusable Problem Details format for HTTP APIs, but a problem document represents details of an error occurrence; it is not necessarily the application resource targeted by the request. Status remains protocol control data. The body can add a stable problem type, human-readable context, and occurrence-specific fields without inventing a second contradictory status system.

Representations are security boundaries. Minimize fields, authorize the resource and the selected view, prevent object-level enumeration, and account for caches, logs, analytics, traces, and intermediaries. “The UI does not render it” does not protect a field already transferred. Representation design should treat tenant identity, subject identity, purpose, consent, retention, and redaction as first-class where the domain requires them.

The executable model below constructs two representations of the same resource and places them in two messages. It checks identity and media-type distinctions without opening a network connection.

<!-- bijux-verify: {"id":"representation-message-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"resource_uri=/projects/prj-7\nrepresentation_variants=2\nmedia_types=application/json,text/plain\nsame_resource=true\nsame_representation=false\nmessage_count=2\n","stderr":""}} -->
```python
resource_uri = "/projects/prj-7"

representations = [
    {
        "resource_uri": resource_uri,
        "media_type": "application/json",
        "data": '{"id":"prj-7","name":"Atlas","status":"active"}',
    },
    {
        "resource_uri": resource_uri,
        "media_type": "text/plain",
        "data": "Atlas (active)",
    },
]

messages = [
    {"status": 200, "content_type": item["media_type"], "content": item["data"]}
    for item in representations
]

assert {item["resource_uri"] for item in representations} == {resource_uri}
assert len({item["media_type"] for item in representations}) == 2
assert representations[0]["data"] != representations[1]["data"]
assert all(message["status"] == 200 for message in messages)

print(f"resource_uri={resource_uri}")
print(f"representation_variants={len(representations)}")
print("media_types=" + ",".join(sorted(item["media_type"] for item in representations)))
print("same_resource=true")
print("same_representation=false")
print(f"message_count={len(messages)}")
```

This execution establishes only the distinctions encoded in a small deterministic data model. It does not implement HTTP, content negotiation, authorization, caching, schema validation, distributed freshness, domain invariants, interoperability, or production safety, and it does not prove that either representation is truthful.

## Definitions and Notation

Let (R) be a resource and (u(R)) its URI. Let (S_R(t)) be authoritative resource state at logical time (t). A representation-selection function produces (V=f(S_R(t), c)), where context (c) can contain media preferences, language, projection, authorization, and policy. (V=(m,d)), with representation metadata (m) and representation data (d).

Let an HTTP message be (M=(k,h,x)), where (k) is request control data or response status, (h) is message fields, and (x) is optional content. When (x) carries representation data, relevant representation metadata appears in (h) or is otherwise defined by the protocol. This notation abstracts framing and HTTP-version details.

A **current representation** reflects a selected current state under stated freshness assumptions. A **historical representation** reflects an earlier state. A **desired-state representation** communicates a proposed target state. A **projection** exposes a subset or transformation. A **derived representation** computes information from one or more sources. **Provenance** records origin and transformation sufficient for the claim. **Authority** is the system or process empowered to decide the governed state; it is not merely the last component that serialized bytes.

## Mechanisms, Invariants, or Proof Structure

Review an API boundary through five layers:

1. **Resource semantics.** Name identity, owner, lifecycle, authority, and relationships independently of transport and storage.
2. **Representation semantics.** Define variants, media types, member meanings, completeness, time, provenance, authorization, and transformation.
3. **Operation semantics.** State what the client asks to observe or change, including preconditions and possible outcomes; later modules add full method design.
4. **Message semantics.** Ensure target, method or status, fields, content, and representation metadata agree.
5. **Implementation mapping.** Map routes, handlers, schemas, stores, and downstream systems without exposing them as accidental public identity.

Apply these invariants:

- **Identity stability:** changing encoding, handler, database, or deployment does not change resource identity unless the conceptual identity changes.
- **Interpretability:** every transferred representation has enough metadata and contract semantics to interpret its data.
- **Honest scope:** projections, redactions, estimates, historical views, and stale views do not claim completeness or immediacy.
- **Authority:** representations state or imply no stronger authority than their provenance supports.
- **Coherence:** message status and fields agree with content and outcome.
- **Security:** selection and disclosure are authorized for the subject, tenant, purpose, and context.
- **Link meaning:** a linked target has a defined relation; presence neither grants access nor promises success.
- **Evolution:** clients depend on documented semantics rather than field order, implementation paths, or incidental serializer behavior.

Evidence must match the claim. Parsing proves syntax. Schema validation proves declared structural constraints. Contract tests sample expected exchanges. Interoperability tests exercise real implementations. Authorization tests challenge views and object identity. Data-lineage checks support provenance. Domain experts review meaning and hazardous outcomes. Operational observation measures deployed behavior. None alone proves the entire chain.

## Alternatives and Trade-Offs

**Resource-oriented interfaces** organize identity and operations around enduring concepts. They gain uniformity, cacheability opportunities, and evolvable representations, but poor resource modeling can disguise command-heavy workflows. **Operation-oriented interfaces** expose verbs or procedures directly. They can express domain commands clearly, but may couple clients to service behavior and weaken uniform intermediaries. The right choice follows interaction semantics, not fashion.

**Generic media types** such as `application/json` maximize tooling and familiarity. They require external contracts for domain meaning. **Domain-specific media types** can state stronger semantics and evolution rules but add registration, documentation, negotiation, and client-support cost. A generic type with a well-governed schema can be sufficient; a suffix or vendor label alone does not create rigor.

**One comprehensive representation** reduces round trips and variant count but increases payload, coupling, exposure, and authorization complexity. **Purpose-specific projections** minimize data and support consumer tasks but add selection rules and incomplete-view hazards. **Embedded related data** improves locality while increasing staleness and duplication; **links** preserve boundaries but add round trips and availability dependencies.

**Stable opaque identifiers** protect implementation freedom but are less readable. **Semantically meaningful identifiers** aid debugging and communication but can leak sensitive facts or become invalid when the domain changes. **Client-assigned identifiers** can support retry and offline creation; **server-assigned identifiers** centralize naming. Each needs collision, scope, authorization, and lifecycle rules.

## Failure Modes and Misconceptions

- **“The JSON object is the resource.”** It is one representation; the resource can outlive, precede, or lack that encoding.
- **“A URI is a database location.”** It identifies within a scheme; implementation mapping is separate.
- **“Every endpoint is a resource.”** An endpoint exposes interaction behavior, while a resource is the conceptual target.
- **“Valid JSON has defined meaning.”** JSON defines syntax and basic data-model interoperability, not domain semantics.
- **“The response body tells the whole result.”** Status, fields, and content jointly define the message.
- **“Equal bytes mean the same thing.”** Media type, provenance, time, target, and interaction context can differ.
- **“A schema is the state model.”** It can constrain representation shape while omitting lifecycle, authority, temporal, and cross-field rules.
- **“Optional means absent for any reason.”** Omission needs semantics: unknown, forbidden, unrequested, inapplicable, or redacted are distinct.
- **“A link proves access.”** It states a relation; authorization and current availability remain separate.
- **“A successful request proves reality changed.”** It proves only the outcome defined by the authority's protocol, under its evidence and failure limits.
- **“Hidden UI fields are protected.”** Transferred fields can leak through clients, caches, logs, traces, and inspection.
- **“REST means JSON over HTTP.”** REST is an architectural style with constraints; neither JSON nor HTTP usage alone establishes conformance.

## Worked Examples

### Example 1

**Question:** Is the JSON returned by `/projects/prj-7` the project?

**Reasoning:** No. It is one representation selected for a client and time. The project resource has identity, authority, lifecycle, relationships, and possibly state the representation omits.

**Conclusion:** Describe the representation as evidence about the resource, not the resource itself.

### Example 2

**Question:** Can the same report URI return JSON and CSV?

**Reasoning:** Yes, if both variants have defined semantics and selection is unambiguous. Column flattening, types, missing values, order, locale, and precision must be specified; equal identity does not imply equal data model.

**Conclusion:** One resource can have materially different, contract-governed representations.

### Example 3

**Question:** A client sends a desired shipping address. Is it now resource state?

**Reasoning:** Not until the authority authenticates, authorizes, validates, applies domain rules, resolves concurrency, and commits or otherwise defines acceptance. The request content represents a proposal.

**Conclusion:** Desired-state representations and accepted authoritative state are distinct.

### Example 4

**Question:** Must `/orders/{id}` map to an `orders` table and `OrderHandler`?

**Reasoning:** No. The service can compose ledgers, fulfillment, customer, and policy data. It can reorganize handlers or storage while preserving the resource contract.

**Conclusion:** Public identity should not encode an accidental implementation map.

### Example 5

**Question:** Are bytes `20` self-describing?

**Reasoning:** No. Under different media types or contracts they may be text, a JSON number, degrees Celsius, an item count, or a code. Time and provenance can further change meaning.

**Conclusion:** Interpret data through metadata and contract semantics.

### Example 6

**Question:** A collection item omits an expensive `riskAnalysis`. Is its representation invalid?

**Reasoning:** Not if the collection projection explicitly defines omission and provides a relation or operation for permitted detail. Calling it the complete project representation would be misleading.

**Conclusion:** Projections are legitimate when their scope is explicit.

### Example 7

**Question:** Does `{"next":"/projects?page=2"}` define a link?

**Reasoning:** Only if the contract assigns `next` a link relation, establishes the context, target resolution, and expected interaction. The string alone does not provide these semantics.

**Conclusion:** Links require typed relationships, not merely URI-shaped text.

### Example 8

**Question:** Is a Problem Details document the failed account resource?

**Reasoning:** Usually no. It represents an error occurrence associated with the request. The HTTP status carries generic outcome semantics; the problem type and fields add machine and human detail.

**Conclusion:** Error representations supplement rather than replace protocol outcome semantics.

### Example 9

**Question:** A medication API returns a valid patient-allergy representation. May dispensing software treat it as complete clinical truth?

**Reasoning:** No. Patient matching, consent, source authority, observation time, reconciliation, unknown allergies, terminology, units, interactions, downtime, overrides, and human workflow remain. Named pharmacists, prescribers, nurses, clinical informaticians, patient-safety and human-factors specialists, privacy/legal and security staff, operations teams, regulators, and independent clinical/technical reviewers must assess use in context. No external review is claimed.

**Conclusion:** Structural and protocol validity cannot authorize a high-stakes clinical decision.

### Example 10

**Question:** Should a representation URI change whenever a service release adds a field?

**Reasoning:** Usually not. If the conceptual resource and compatible contract remain, implementation release identity should stay separate. Breaking semantic change may require a new representation contract or resource model, decided through compatibility analysis.

**Conclusion:** Version enduring semantics, not routine deployment history.

## Cross-Program Connections

[Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) supplies identity, value, aggregate, lifecycle, and ubiquitous-language decisions behind resources. [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) supplies authority, lineage, canonical meaning, quality, and temporal context behind represented state.

[Network Engineering](../../24-network-engineering/ROADMAP.md) explains transport paths and protocol layering. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) explains why a representation may be delayed, duplicated, stale, or observed after authority changes. [Security Engineering](../../25-security-engineering/ROADMAP.md) governs identity, authorization, disclosure, integrity, provenance, and adversarial interpretation.

[Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) places APIs at component and system boundaries. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) can supply gateways, catalogs, policy, and developer workflows, but it cannot choose domain resource meaning on behalf of service owners.

## References

- R. Fielding, M. Nottingham, and J. Reschke, [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html), Internet Standard STD 97, 2022. Current normative foundation for HTTP resources, representations, messages, methods, status, fields, and content.
- Tim Berners-Lee, Roy Fielding, and Larry Masinter, [RFC 3986: Uniform Resource Identifier (URI): Generic Syntax](https://www.rfc-editor.org/rfc/rfc3986.html), Internet Standard STD 66, 2005; updated by RFCs 7320 and 8820. Normative resource-identification and generic URI syntax.
- Roy Thomas Fielding, [*Architectural Styles and the Design of Network-based Software Architectures*](https://ics.uci.edu/~fielding/pubs/dissertation/top.htm), doctoral dissertation, University of California, Irvine, 2000. Primary REST architectural derivation and resource/representation model.
- W3C Technical Architecture Group, [*Architecture of the World Wide Web, Volume One*](https://www.w3.org/TR/webarch/), W3C Recommendation, 2004. Web architecture principles for identification, interaction, and representation.
- Tim Bray, [RFC 8259: The JavaScript Object Notation (JSON) Data Interchange Format](https://www.rfc-editor.org/rfc/rfc8259.html), Internet Standard STD 90, 2017. Normative JSON syntax and interoperability requirements.
- Ned Freed, John Klensin, and Tony Hansen, [RFC 6838: Media Type Specifications and Registration Procedures](https://www.rfc-editor.org/rfc/rfc6838.html), BCP 13, 2013; updated by RFC 9694. Media-type semantics, specification requirements, and registration procedures.
- Mark Nottingham, [RFC 8288: Web Linking](https://www.rfc-editor.org/rfc/rfc8288.html), Internet Standard STD 95, 2017. Normative framework for context, target, and link relations.
- Erik Wilde, Sanjay Dalal, and Roberto Peon, [RFC 9457: Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457.html), 2023. Current standard error-detail representation, obsoleting RFC 7807.

## Exercises

### Exercise 1

For a project-management API, distinguish the project resource, authoritative state, detailed JSON representation, list projection, request message, response message, URI, route, handler, schema, and database records. State which relationships are contractually stable.

### Exercise 2

Design JSON and CSV representations of one monthly billing-report resource. Specify media types, member/column semantics, missing values, ordering, currency, precision, observation period, provenance, authorization, and how a client discovers each variant.

### Exercise 3

Review a request containing a desired account address and a response containing the accepted address. Trace proposal, validation, authorization, normalization, commit, representation selection, message status, and failure points without assuming request bytes become state directly.

### Exercise 4

Critique the contract `200 OK {"success": false, "data": null}` and a JSON response labeled `text/plain`. Explain the effects on generic clients, observability, caching, security review, and future evolution; propose coherent alternatives.

### Exercise 5

A national emergency-alert API exposes alerts in JSON, Common Alerting Protocol XML, localized text, audio, and low-bandwidth projections. Define resources, representation variants, message invariants, authority, provenance, timing, security, degraded behavior, verification, and named human review required before public use.

## Answers to the Exercises

### Answer 1

The project resource is the enduring conceptual project identified by a stable URI and governed by domain lifecycle. Authoritative state is the owning system's accepted facts at a logical time, potentially spanning several stores. Detailed JSON and list-item data are two representations; the list view is explicitly partial. A request message contains method, target, fields, and perhaps a desired-state representation. A response contains status, fields, and perhaps a selected current or historical representation. The URI is public identity; the route is an implementation dispatch pattern; the handler is code; the schema constrains representation shape; database records persist implementation state. Contractually stabilize resource identity, domain semantics, operation outcomes, representation meanings, media types, link relations, authorization, and compatibility rules. Permit routes behind gateways, handlers, schemas within compatible bounds, and storage layouts to evolve without pretending they are the resource.

### Answer 2

Identify one report resource such as `/billing-reports/2026-07`, with an authority, account scope, closed/open state, generation time, and revision or validator. The JSON representation can preserve nested line items and typed decimal strings; the CSV representation needs documented UTF-8 encoding, header names, row grain, quoting, line endings, ordering, null marker, and flattening rules. Both define ISO 4217 currency, decimal scale and rounding, inclusive/exclusive period boundaries, timezone, tax semantics, and whether adjustments after generation appear. Record source systems and generation timestamp without exposing internal secrets. Authorize the resource and each included field; protect caches and exports. Use documented negotiation or distinct typed links as the later interface design chooses. Test golden examples, parsing, cross-variant totals, empty and large reports, locale independence, malicious spreadsheet values, authorization, and regeneration. Equal totals do not prove the source ledger is correct.

### Answer 3

The request content is a desired-state representation tied to the account target. Parse it according to its media type, authenticate the caller, authorize the account and fields, validate syntax and domain constraints, normalize only under documented rules, check concurrency/preconditions, and commit through the account authority. Rejection leaves authoritative address state unchanged. Acceptance may store a normalized state different from the proposed spelling. Select a permitted response representation from the committed result and return status and metadata consistent with that outcome. Failures can occur before receipt, during parsing, authorization, validation, coordination, commit, representation generation, or reply delivery; a client timeout alone does not reveal which. Use operation identities, conditional requests, status lookup, or reconciliation as later modules prescribe.

### Answer 4

`200` conventionally communicates successful handling, while `success:false` creates a competing application status channel. Generic clients, alerts, proxies, traces, service-level indicators, and retry logic may record success while humans see failure. `data:null` does not distinguish absence, rejection, redaction, or pending work. Labeling JSON as `text/plain` tells recipients to apply the wrong processing model, can disable validators and security controls, and makes later negotiation ambiguous. Return the HTTP status appropriate to the actual outcome and, when useful, a typed Problem Details representation whose stable type and fields extend that status. For an accepted asynchronous operation, return the deliberately documented accepted outcome and status resource rather than a false failure. Label JSON with an appropriate JSON media type and define its schema and semantics. Test status/body coherence and content-type enforcement.

### Answer 5

Model an alert as an authoritative, versioned public-safety communication with stable identity, issuing authority, geographic and audience scope, severity, certainty, urgency, effective/expiry times, cancellation/correction relationships, languages, and provenance. JSON, CAP XML, localized text, synthesized or recorded audio, and low-bandwidth views are representation variants; none may silently omit a safety-critical instruction. Messages must carry coherent status, media type, language, freshness/validator, integrity and cache controls, and must distinguish draft, active, superseded, cancelled, expired, test, and exercise alerts. Authenticate and strongly authorize issuers, preserve audit and nonrepudiation evidence appropriate to law, constrain enumeration of nonpublic drafts, and plan key compromise and false-message response.

Define authoritative clocks and location semantics, offline and congested behavior, retries and duplicate suppression, ordering of correction/cancellation, CDN and carrier propagation, regional partition, overload, fallback formats, accessibility, and uncertainty when freshness cannot be established. Verify schemas and signatures, cross-format semantic equivalence, multilingual and audio fidelity, geospatial boundaries, device interoperability, cache invalidation, delayed/duplicate/reordered delivery, failover, overload, cyberattack, observability, restoration, and public drills. Named review must include alert-originating authorities, emergency managers, meteorological/geological or hazard specialists as applicable, telecom and broadcast operators, CAP and API engineers, accessibility and human-factors experts, professional translators and local communities, cybersecurity and cryptography reviewers, privacy/legal/records authorities, reliability and network engineers, device vendors, public communications teams, regulators, and independent operational/technical assurance. Automated checks cannot establish that instructions are understandable, lawful, geographically correct, timely in real networks, or safe for every affected population; no external acceptance is claimed.
