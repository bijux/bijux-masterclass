---
module_id: API-002
program: API & Service Engineering
level: 1
module_number: 2
title: HTTP Methods and Their Semantics
status: complete
last_verified: 2026-08-29
---

# HTTP Methods and Their Semantics

## One-Page Review

### Governing question

How does an HTTP request method communicate the client's intended interaction with a target resource so that clients, origins, intermediaries, caches, retries, security controls, and operators can behave consistently?

### Essential definitions

- A **request method** is a case-sensitive token that states the primary semantics requested for the target resource.
- A **safe method** has defined semantics that are essentially read-only: the client does not request or expect origin-server state change. Logging and other server-chosen side effects do not make the method unsafe.
- An **idempotent method** has the same intended server effect for multiple identical requests as for one. Individual responses, logs, timing, and incidental side effects may differ.
- **GET** requests transfer a current selected representation of the target resource.
- **HEAD** has GET semantics except that the server sends no response content.
- **POST** asks the target resource to process enclosed content according to that resource's own semantics.
- **PUT** asks to create or replace target-resource state with the state defined by the enclosed representation.
- **DELETE** asks to remove the association between the target URI and its current functionality; it does not universally require physical data erasure.
- **OPTIONS** asks for communication options; **TRACE** performs a diagnostic loop-back; **CONNECT** establishes a tunnel.
- **PATCH**, defined separately from core HTTP semantics, applies a patch document rather than replacing the full target state.

### Central model, mechanism, or theorem

Interpret a request as \(R=(m,u,f,c)\): method \(m\), target URI \(u\), fields \(f\), and optional content \(c\). The method specification supplies a semantic relation

\[
\llbracket m \rrbracket:(S_u,f,c,\Gamma)\rightarrow
  \mathcal{P}(S'_u,O,E),
\]

where \(S_u\) is target-resource state, \(\Gamma\) is request context, \(S'_u\) is resulting state, \(O\) is response outcome, and \(E\) is allowed related effect. Fields may condition or specialize the request without contradicting \(m\). Safety constrains requested state change; idempotency constrains repeated identical intended effects. Neither property alone proves retry success, authorization, concurrency safety, or business correctness.

### Critical invariants

- Method meaning comes from its specification and target-resource semantics, not its spelling as an arbitrary route action.
- Safe methods never expose an unsafe action through query parameters or handler side effects attributable to the client.
- GET and HEAD select the same resource semantics; HEAD omits response content rather than selecting a cheaper, inconsistent resource.
- PUT represents complete replacement intent at a client-known target; PATCH represents change instructions under a patch media type.
- POST does not automatically mean “create,” and DELETE does not automatically mean hard erasure.
- Identical idempotent requests converge on the same requested effect while still producing legitimate different responses.
- Automatic retry policy accounts for method semantics, request replayability, preconditions, deadlines, overload, and effect evidence.
- Authorization is evaluated for the method, target, representation, current state, and actor.

### Common failures

Teams use GET for deletion; reduce methods to CRUD; use POST for every operation; implement PUT as a silent partial merge; assume DELETE means storage destruction; attach private request-content semantics to GET; return a body to HEAD; equate safe with side-effect-free; equate idempotent with identical response; blindly retry POST; retry a PUT whose streamed content cannot be replayed; omit preconditions on overwrites; return 404 for every disallowed method; or invent verbs without extension and intermediary analysis.

### Compact example

`PUT /profiles/p7` with a complete profile representation asks the origin to make target state correspond to that representation. Repeating the identical request has the same intended effect, so PUT is idempotent. The first response can be `201 Created` and the second `200 OK` or `204 No Content`; idempotency does not require response equality. If the API instead merges only supplied members, it has not implemented ordinary PUT replacement semantics and should choose an explicit patch model.

### Connections

[API-001](001-resources-representations-and-messages.md) separated resources, representations, and messages. Status codes, fields, content negotiation, conditions, caching, safety/idempotency design, idempotency keys, concurrency control, retries, and security receive dedicated later modules. Method semantics is the shared vocabulary that keeps those mechanisms composable.

## Governing Question

What does the client ask the target resource to do, and which protocol participants are entitled to infer safety, replay behavior, cache interaction, content meaning, and authorization from that method?

The method is not merely routing metadata. Crawlers invoke safe methods automatically. Proxies may retry idempotent methods after a connection failure. Caches key behavior partly by method. Security policies distinguish observation from mutation. A handler that contradicts the method creates failures outside its own code because other participants correctly rely on standardized semantics.

## Why This Matters

HTTP's uniform interface lets independent software act without knowing handler names or storage schemas. RFC 9110 defines core semantics across HTTP versions; IANA maintains an extensible method registry containing safety, idempotency, and specification references. The registry is active, so memorizing eight tokens is insufficient. Engineers need a method for reading and preserving semantics.

Method choice affects human consent and automation. A crawler can follow a GET link; prefetch can issue GET before a user clicks; a client can retry PUT after losing a response. If `GET /invoices/7?do=pay` charges money, the resource violates safe semantics and shifts harm onto an automated caller. If PUT performs an increment, a retry can increment twice despite PUT's advertised idempotency.

Semantics also bounds claims. Idempotency describes intended effect, not delivery exactly once. A safe request can consume resources or log access. A successful DELETE need not satisfy legal erasure. A conditional PUT can prevent a lost update but cannot validate the business facts in the representation. Method correctness is necessary interface evidence, not proof of domain correctness, authorization quality, or real-world safety.

## Prerequisites and Retrieval

Retrieve from [API-001](001-resources-representations-and-messages.md) the target resource, selected representation, message fields, request content, response content, origin server, intermediary, and cache. Recall distributed timeout ambiguity: absence of a response does not reveal whether the origin applied a request.

You should understand set relations, state transitions, equality of intended effects, authorization, and basic URI syntax. Keep distinct:

- method semantics and handler implementation;
- target-resource effect and related side effect;
- request replay and content replayability;
- protocol idempotency and application deduplication;
- conditional execution and idempotency;
- successful protocol outcome and validated real-world outcome.

## Learning Objectives

By the end of this module, you should be able to:

1. explain methods as standardized semantic tokens rather than route labels;
2. distinguish safety, idempotency, cacheability, replayability, and deduplication;
3. apply GET, HEAD, POST, PUT, DELETE, CONNECT, OPTIONS, and TRACE according to RFC 9110;
4. distinguish full replacement by PUT from partial modification by PATCH;
5. explain why POST can represent many processing semantics and is not synonymous with create;
6. reason about repeated requests whose responses legitimately differ;
7. reject unsafe actions exposed through safe methods;
8. select 405 versus 501 behavior and use Allow appropriately;
9. evaluate extension methods from their registry and defining specifications; and
10. design method-specific evidence without overclaiming domain, safety, or authorization correctness.

## Core Exposition

### Method tokens and resource semantics

The request method is case-sensitive because it can be a gateway to object-based systems with case-sensitive names. Standard methods use uppercase by convention. Once a server parses a target URI, it evaluates the method against the target resource's current semantics. Allowed methods can change with state or authorization context.

Fields specialize requests: conditions can make an action contingent on current validators; Range can specialize GET; content metadata describes enclosed content. Such fields cannot redefine GET into mutation or PUT into arbitrary processing. Private reinterpretation breaks intermediaries that see only standard semantics.

General-purpose servers must support GET and HEAD; other methods are optional. If an origin does not recognize or implement a method, RFC 9110 recommends 501. If it knows and implements the method but the target does not allow it, 405 is appropriate, and a 405 response must include the target's currently supported methods in Allow. Authorization policy can limit disclosure; status behavior is itself part of the security contract.

### Safety

Safety is about requested semantics and accountability. GET, HEAD, OPTIONS, and TRACE are safe in RFC 9110. A server may log each request, update metrics, charge an advertising account, refresh a cache, or incur compute cost. Those server-selected effects do not mean the client requested resource mutation.

This distinction enables crawling, link checking, prefetching, and safe user-interface presentation. Resource owners must disable unsafe actions reached with safe methods. Query parameters do not rescue `GET /records?delete=all`: the method remains GET, and automated retrieval is entitled not to cause the requested deletion.

Safe does not mean cheap, private, harmless under abuse, authorized, cacheable, or guaranteed to succeed. An expensive search GET can be abused. A safe endpoint can disclose sensitive data. Rate limits, authorization, input bounds, and observability remain necessary.

### Idempotency and retries

GET, HEAD, OPTIONS, TRACE, PUT, and DELETE are idempotent by their registered semantics. Multiple identical requested effects equal one intended effect. An origin may log every attempt, retain revisions, return different validators, or change status because state evolved.

Idempotency is valuable when the connection closes before a response. A client can repeat an idempotent request, but “can” is not “always should.” Request content must be replayable; credentials and preconditions may expire; deadlines and retry budgets remain; overload can worsen; concurrent actors may change state; and a response might be recoverable through status lookup instead.

A client should not automatically retry a non-idempotent method unless it knows the actual operation is idempotent or knows the original was not applied. An idempotency key can give a POST operation stable application identity, but the key's scope, request fingerprint, persistence, concurrent handling, result replay, and retention determine the guarantee. API-037 develops that mechanism.

### GET and HEAD

GET requests transfer a current selected representation of the target resource. It is the primary retrieval mechanism and the focus of HTTP performance optimizations. Range can request selected parts. GET responses are cacheable unless controls say otherwise.

Request content on GET has no generally defined semantics, cannot alter the request's target or meaning, and can trigger rejection because of request-smuggling risk. A client should not send it except to a directly known origin that has indicated support; an origin should not depend on private agreements that intermediaries cannot know. Prefer standardized URI or method semantics.

HEAD is identical to GET except that the server must not send response content. It obtains representation metadata efficiently. The origin should send the same fields as GET, though fields computed only while generating content may be omitted. HEAD is not an independent “metadata resource” whose validators, selection, or authorization can drift from GET.

### POST

POST asks the target resource to process enclosed content according to its own semantics. RFC 9110 examples include providing data to a processing operation, posting a message, creating a resource not yet identified by the origin, and appending data. The target is the processing resource, not necessarily the resource ultimately created or changed.

POST is neither safe nor idempotent by default. It can nonetheless be designed with application-level idempotency, and a response can identify created resources or redirect to a cacheable retrieval resource. Its breadth is useful for commands, computation, submissions, and server-selected identifiers, but every endpoint must document exact effect, authority, response, duplication, and recovery behavior.

### PUT

PUT asks to create or replace target-resource state with the state defined by the request representation. The client knows the target URI. If the origin selects a new URI after processing, POST is normally the better semantic fit. PUT can create or replace; status communicates which outcome occurred.

PUT is idempotent even though related effects can occur, such as revision creation. Partial merge-by-omission contradicts replacement intent because a client cannot know whether omitted members are preserved or removed. Use PATCH or a purpose-built operation for partial change. Preconditions are often needed to prevent one client's replacement from overwriting a newer state.

An origin can validate representation constraints or transform content. RFC 9110 restricts successful PUT validators: a validator such as ETag must not be sent unless the content was saved without transformation and the validator reflects the new representation. This prevents the client from treating its retained bytes as validated server state when the origin changed them.

### DELETE

DELETE asks the origin to remove the association between the target URI and current functionality. It resembles removing a name mapping; storage, history, replicas, backups, audit records, related resources, and legal retention lie beyond the universal HTTP definition. An API must state its own tombstone, restoration, purge, retention, and compliance behavior.

DELETE is idempotent by intended effect: after successful removal, repeating the same request still asks for the association to be absent. The second response might be 404, 410, 204, or another contractually justified outcome. Request content has no generally defined DELETE semantics and brings the same intermediary and request-smuggling concerns as GET content.

### OPTIONS, TRACE, and CONNECT

OPTIONS asks for communication options for the target resource or server. It can support capability discovery, but Allow is not a complete authorization or workflow schema, can change dynamically, and does not replace an API contract. The asterisk request target addresses the server in general rather than a resource.

TRACE asks the final recipient to reflect the received request, subject to diagnostic controls. It is safe and idempotent but can expose sensitive fields; RFC 9110 forbids clients from sending credentials or sensitive data that might be disclosed and forbids request content. Many deployments disable it. Diagnostic usefulness never overrides disclosure risk.

CONNECT asks a proxy to establish a tunnel to the identified host and port. It is neither safe nor idempotent. Once successful, data is blind-forwarded until closure. Proxies must restrict tunnel destinations to prevent access to unintended services. Extended CONNECT usage is specified by protocol-specific extensions, not improvised by an origin route.

### PATCH and extension methods

RFC 5789 defines PATCH for a patch document applied to the target resource. It is neither safe nor idempotent in the registry, though a particular patch request can be constructed idempotently. Some patch formats require a known base; strong conditional requests prevent applying instructions to an unintended version. The server must apply the directly affected patch atomically or not apply it.

HTTP is extensible. The IANA registry records method name, safety, idempotency, and specification. WebDAV methods and newer registrations show why switch statements hard-coded to an old list are brittle. A new method specification must define semantics, content, status interaction, safety, idempotency, caching, conditions, redirects, security, and interoperability. Prefer an existing registered method when it expresses the intended semantics.

### Deterministic method-property evidence

The following artifact checks a compact registry-derived table and demonstrates that safe is a subset of idempotent for these selected methods, while idempotent does not imply safe.

<!-- bijux-verify: {"id":"method-property-table","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"GET safe=True idempotent=True retry=semantic\nPOST safe=False idempotent=False retry=requires-evidence\nPUT safe=False idempotent=True retry=semantic\nDELETE safe=False idempotent=True retry=semantic\nPATCH safe=False idempotent=False retry=requires-evidence\nsafe_subset_idempotent=True\nidempotent_implies_safe=False\n","stderr":""}} -->
```python
properties = {
    "GET": (True, True),
    "POST": (False, False),
    "PUT": (False, True),
    "DELETE": (False, True),
    "PATCH": (False, False),
}

for method in ("GET", "POST", "PUT", "DELETE", "PATCH"):
    safe, idempotent = properties[method]
    retry = "semantic" if idempotent else "requires-evidence"
    print(
        f"{method} safe={safe} idempotent={idempotent} "
        f"retry={retry}"
    )

safe_subset = all(idempotent for safe, idempotent in properties.values() if safe)
idempotent_implies_safe = all(
    safe for safe, idempotent in properties.values() if idempotent
)
print(f"safe_subset_idempotent={safe_subset}")
print(f"idempotent_implies_safe={idempotent_implies_safe}")
```

The run verifies only the encoded Boolean classifications and implications. It does not prove the table complete, a handler conformant, a retry prudent, a request replayable, effects deduplicated, authorization correct, or any business outcome safe.

## Definitions and Notation

Let \(M\) be registered methods, \(U\) target resources, \(F\) request-field values, \(C\) optional request content, and \(\Gamma\) actor, intermediary, and representation context. A method defines allowed interpretations rather than one implementation function.

For method \(m\):

- \(Safe(m)\) means the client requests no origin state change;
- \(Idem(m)\) means repeating identical requests has the same intended server effect as one;
- \(Cacheable(m)\) means its specification permits response reuse subject to cache rules;
- \(Allowed(m,u,\Gamma)\) is the origin's current authorization-aware allowance decision;
- \(Replayable(R)\) means the client can reproduce the same relevant request content and fields; and
- \(Applied(R)\) is evidence about a particular request occurrence, not a method property.

Safety implies idempotency for the registered core safe methods, but idempotency does not imply safety: PUT and DELETE are counterexamples. Idempotency does not imply commutativity. Two different PUT requests to one resource can overwrite in order-dependent ways even though each request is individually idempotent.

An **identical request** for method-property reasoning preserves target, semantic fields, content, and relevant actor context. Byte equality may be insufficient when credentials expire; semantic equality may be insufficient for a signed replay. State these boundaries when deriving a retry policy.

A **method extension** is a separately specified method token, ideally IANA-registered. A URI action name is not an extension method. A **method override** field or parameter asks infrastructure to reinterpret another method and can confuse caches, signatures, authorization, observability, and intermediaries; use only in a governed compatibility boundary.

## Mechanisms, Invariants, or Proof Structure

Use this review sequence:

1. **Name the target resource.** State what the request is about, not merely the handler path.
2. **State client intent.** Retrieve, inspect metadata, process content, replace state, apply changes, remove association, discover options, diagnose, or tunnel.
3. **Select the registered method.** Read its current specification and registry properties.
4. **Define request content.** Media type, completeness, base version, units, identity, and replayability.
5. **Define effect boundaries.** Target state, related resources, external authorities, events, and irreversible effects.
6. **Define conditions and concurrency.** Validators, creation-only or replacement-only constraints, conflicts, and atomicity.
7. **Define outcomes.** Success and failure status, fields, representation meaning, validators, and recovery links.
8. **Define automation.** Retry, redirect, cache, crawler, prefetch, gateway, and client-generation behavior.
9. **Define authorization and abuse controls.** Actor, target, method, object, fields, rate, and sensitive evidence.
10. **Verify across the path.** Client, proxy, gateway, origin, downstream effect, observability, timeout, duplicate, and recovery.

The **semantic-conformance invariant** requires the target handler and every intermediary policy to preserve the registered method meaning. The **safe-action invariant** rejects client-requested mutation for safe methods even if a query parameter or routing framework makes it convenient. The **replacement invariant** requires PUT omissions to mean absence in the desired complete state unless the representation contract defines otherwise without contradicting replacement.

The **retry invariant** requires repeated automated attempts to preserve logical operation, content, conditions, authority, deadline, and effect semantics. Method idempotency supplies only the intended-effect premise. The **evidence invariant** keeps response receipt, origin application, downstream completion, and real-world outcome distinct.

Test method matrices rather than happy paths: allowed/disallowed method, missing/invalid content, conditional pass/fail, duplicate before/after response loss, concurrent different request, redirect, cache invalidation, gateway policy, unauthorized object, and downstream partial failure. Record each attempt identity and authoritative effect.

## Alternatives and Trade-Offs

**POST versus PUT.** POST lets the target choose processing and often the resulting URI; PUT expresses complete desired state at a known target and is idempotent. Choose from intent, not a blanket “create/update” rule.

**PUT versus PATCH.** PUT transfers a replacement representation and offers simple convergent retry semantics. PATCH can reduce transfer and express changes but depends on patch media type, base state, atomic application, and conflict handling.

**DELETE versus domain command.** DELETE fits removal of a URI association. `POST /subscriptions/s7:cancellation` or a cancellation resource can better represent a reversible, audited business transition whose entity remains addressable. Avoid assuming one verb fits every domain lifecycle.

**Safe query URI versus request content.** URI query parameters interoperate with GET, caches, links, and tooling but can leak through logs and length limits. A registered safe method with content may suit complex queries where deployed support exists. Private GET-content semantics have weak intermediary interoperability.

**Generic POST versus extension method.** POST is widely supported and resource-specific. A registered extension can expose reusable semantics and intermediary properties. New methods impose specification, tooling, gateway, security, and deployment costs.

**Automatic retry versus recovery query.** Repeating idempotent requests is simple. Status lookup can reduce load and ambiguity for expensive operations. Combine bounded attempts, deadlines, operation identity, and authoritative recovery evidence.

## Failure Modes and Misconceptions

1. **“Methods are CRUD labels.”** HTTP methods express resource interaction semantics; domain lifecycles are richer.
2. **“GET can mutate if documented.”** Automated participants rely on safe semantics.
3. **“Safe means no side effects.”** Server-chosen logging and metrics are compatible; requested mutation is not.
4. **“Idempotent means same response.”** State and response status can differ while intended effect converges.
5. **“Idempotent means retry forever.”** Replayability, deadlines, load, conditions, and evidence still govern.
6. **“POST always creates.”** It requests target-specific processing and can compute, append, command, or create.
7. **“PUT means update supplied fields.”** Ordinary PUT communicates complete create-or-replace state.
8. **“DELETE proves erasure.”** HTTP specifies removal of target association, not every storage/legal consequence.
9. **“HEAD is a separate cheap endpoint.”** It must preserve GET selection and metadata semantics while omitting content.
10. **“GET content is forbidden, so private semantics are safe.”** Framing allows it, but semantics are undefined and intermediaries may reject it.
11. **“PATCH is idempotent.”** The registry says no; a specific request can be constructed to be idempotent.
12. **“405 and 501 are interchangeable.”** One means known but disallowed for the target; the other means unrecognized or unimplemented.
13. **“Allow is permanent and universal.”** It can vary dynamically and is not a substitute for authorization or workflow documentation.
14. **“A framework route proves compliance.”** Runtime behavior through gateways and downstream effects determines conformance.

## Worked Examples

### Example 1

**Question:** May `GET /documents/d9?delete=true` delete the document?

**Reasoning:** No. The parameter does not change GET's safe semantics. Crawlers, previews, and prefetchers can invoke it without user mutation intent.

**Conclusion:** Expose deletion through an unsafe method with explicit authorization and confirmation.

### Example 2

**Question:** Can HEAD return a different ETag from GET because it uses a faster metadata store?

**Reasoning:** That would misdescribe the selected representation and can corrupt cache validation. Computation-only fields may be omitted, but present metadata must remain semantically consistent.

**Conclusion:** Optimize implementation without creating a second resource truth.

### Example 3

**Question:** A client POSTs a report request and the origin creates a job. Is POST synonymous with create?

**Reasoning:** No. The target processes a submission; creation is one outcome. The response can identify the job and a retrieval resource.

**Conclusion:** Document processing, created-resource identity, duplicate behavior, and recovery.

### Example 4

**Question:** First PUT creates `/themes/t1` and a repeat replaces the same state. Must responses match?

**Reasoning:** No. The first can return 201 and the second 204. The intended target state after either is equivalent.

**Conclusion:** Idempotency concerns intended effect, not response equality.

### Example 5

**Question:** An API preserves omitted members on PUT. What ambiguity results?

**Reasoning:** Clients cannot know whether omission means delete, default, retain, or unauthorized hidden state. Replacement and patch semantics collapse.

**Conclusion:** Make PUT complete or select an explicit patch/command contract.

### Example 6

**Question:** Does successful DELETE of a user URI prove backups and audit records are erased?

**Reasoning:** No. HTTP removes the URI association. Erasure scope, legal retention, tombstones, replicas, backups, and restoration are application and governance claims.

**Conclusion:** State deletion and erasure guarantees separately.

### Example 7

**Question:** Should a gateway retry a streamed PUT after upstream connection loss?

**Reasoning:** PUT is idempotent, but the gateway may not possess replayable complete content, valid conditions, or remaining deadline. It also needs attempt correlation and overload controls.

**Conclusion:** Method idempotency is necessary but not sufficient retry evidence.

### Example 8

**Question:** The server supports PATCH generally but not for one immutable resource. Which response fits?

**Reasoning:** PATCH is known and implemented but disallowed for that target, so 405 with an accurate Allow field fits. Unsupported patch media type is a different issue.

**Conclusion:** Separate method allowance from content-format support.

### Example 9

**Question:** Can TRACE be enabled for authenticated production traffic because it is safe?

**Reasoning:** Safety does not mean confidentiality. Reflection can disclose credentials or sensitive fields and enlarge diagnostic attack surface. Apply the specification's sensitive-data restrictions and deployment threat model.

**Conclusion:** Evaluate disclosure and operational need independently of safety.

### Example 10

**Question:** May an infusion-management API rely on PUT idempotency to establish that a dosage command is clinically safe?

**Reasoning:** No. PUT only constrains intended repeated HTTP effect. Patient identity, prescription authority, units, concentration, device state, timing, stale orders, concurrent clinicians, physical delivery, overrides, downtime, audit, and adverse-event response require named clinical, pharmacy, nursing, biomedical, human-factors/accessibility, safety, security, privacy, operations, regulatory, and independent assurance review. No external review is claimed.

**Conclusion:** Protocol semantics cannot authorize a high-consequence real-world action.

## Cross-Program Connections

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) explains timeout ambiguity, duplicate attempts, stable operation identity, and external-effect boundaries. HTTP idempotency exposes useful retry intent but does not implement distributed deduplication.

[Network Engineering](../../24-network-engineering/ROADMAP.md) owns transport, proxy paths, connection failure, and request-smuggling mechanics. [Security Engineering](../../25-security-engineering/ROADMAP.md) owns actor identity, authorization, abuse, credential disclosure, and adversarial replay. Method semantics supplies inputs to both policies.

[Software Engineering: Patterns, Architecture, and Practice](../../11-software-engineering-patterns/ROADMAP.md) supplies application boundaries and domain behavior. [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies transactions, concurrency control, and persistence that may implement target-state transitions.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects protocol behavior to operators, people, hazards, validation, and lifecycle evidence. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) governs gateways and developer platforms that must preserve registered methods instead of freezing an obsolete allowlist.

## References

- R. Fielding, M. Nottingham, and J. Reschke, editors, [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html), Internet Standard 97, 2022. Current core definitions for methods, safety, idempotency, caching eligibility, method behavior, status interaction, and extensibility.
- IANA, [Hypertext Transfer Protocol (HTTP) Method Registry](https://www.iana.org/assignments/http-methods/), current registry retrieved 2026-08-29. Authoritative method names, safety/idempotency classifications, and defining references.
- L. Dusseault and J. Snell, [RFC 5789: PATCH Method for HTTP](https://www.rfc-editor.org/rfc/rfc5789), 2010. Patch-document semantics, atomic application, conditional use, discovery, and security.
- R. Fielding, M. Nottingham, and J. Reschke, editors, [RFC 9111: HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111), Internet Standard 98, 2022. Cache storage, reuse, invalidation, and method interaction.
- R. Fielding, [*Architectural Styles and the Design of Network-based Software Architectures*](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm), doctoral dissertation, University of California, Irvine, 2000. Uniform-interface and resource interaction foundations.
- M. Nottingham, [RFC 9205: Building Protocols with HTTP](https://www.rfc-editor.org/rfc/rfc9205), BCP 56, 2022. Guidance for selecting and preserving HTTP semantics in application protocols.
- R. Fielding and J. Reschke, editors, [RFC 4918: HTTP Extensions for Web Distributed Authoring and Versioning](https://www.rfc-editor.org/rfc/rfc4918), 2007. Registered extension-method examples and conditional authoring semantics.
- M. Bishop, editor, [RFC 9114: HTTP/3](https://www.rfc-editor.org/rfc/rfc9114), 2022. Demonstrates that core method semantics remain independent of version-specific transport mapping.

## Exercises

### Exercise 1

Classify GET, HEAD, POST, PUT, DELETE, OPTIONS, TRACE, CONNECT, and PATCH by safety and idempotency. For each, state the requested intent and one common misconception.

### Exercise 2

Design interfaces for client-selected document replacement, server-selected job creation, partial profile modification, subscription cancellation, and report retrieval. Justify method and target; define content, conditions, duplicate behavior, outcome, and recovery.

### Exercise 3

Audit a gateway configured to retry every GET, PUT, DELETE, and POST twice. Analyze request-content replayability, preconditions, redirects, overload, idempotency keys, attempt identity, downstream effects, and response loss. Produce a safer policy.

### Exercise 4

Specify a method conformance test matrix for a resource supporting GET, HEAD, PUT, and DELETE but not PATCH. Include 405/501, Allow, content, validators, conditions, repeated requests, cache invalidation, authorization, and gateway behavior.

### Exercise 5

A regional energy operator exposes APIs for telemetry retrieval, schedule replacement, curtailment commands, device disconnection, and emergency control. Choose methods and define semantic, concurrency, retry, security, operational, and named human-review evidence required before use.

## Answers to the Exercises

### Answer 1

GET, HEAD, OPTIONS, and TRACE are safe and idempotent. GET transfers a selected representation; HEAD requests the same semantics without response content; OPTIONS requests communication options; TRACE requests diagnostic loop-back. Misconceptions respectively include “GET may delete through a parameter,” “HEAD is unrelated metadata,” “Allow describes every workflow and authorization,” and “safe TRACE cannot disclose secrets.”

PUT and DELETE are unsafe and idempotent. PUT requests complete create-or-replace state at a known target; DELETE removes the target URI's association with current functionality. Misconceptions are “PUT merges supplied fields” and “DELETE proves physical/legal erasure.” POST, CONNECT, and PATCH are unsafe and non-idempotent in the registry. POST requests target-specific processing, CONNECT creates a tunnel, and PATCH applies a patch document. A particular POST or PATCH operation can add application idempotency, but that does not change the registered default. Cacheability and response-content rules are separate dimensions.

### Answer 2

Use PUT on a client-known document URI with a complete representation, strong precondition when overwriting, replayable content, and 201 versus 200/204 outcomes. Use POST to a jobs collection or processing resource when the server assigns job identity; return the job link and define an idempotency-key/recovery contract where duplicate creation is unacceptable. Use PATCH on the profile URI with a registered patch media type, strong If-Match for base-dependent formats, atomic application, and Accept-Patch discovery.

Cancellation is a domain transition rather than necessarily resource erasure. POST to a cancellation/transition resource can preserve the subscription and audit history; define whether repeated cancellation returns the existing result. Retrieve a report with GET at its stable resource URI, with authorization, representation selection, cache controls, and conditions. For every interface, document authoritative effect, related effects, status and representation meaning, timeout ambiguity, and status lookup.

### Answer 3

Do not retry solely from a method allowlist. GET is semantically idempotent, but cap attempts by deadline and overload budget, respect authentication and redirects, and avoid amplifying expensive queries. Buffering or regenerating a complete identical PUT is required; preserve validators so a retry cannot overwrite intervening state. DELETE retry must preserve target and authority, and the client contract must tolerate a different second response.

POST is not automatically retryable. Retry only when the operation has a durable logical identity and request fingerprint with authoritative outcome replay, or when transport evidence establishes that the origin did not apply it. Preserve the same key, payload, actor, and deadline across attempts. Count gateway and client retries together, use backoff/jitter where appropriate, prevent multiplicative downstream retries, record attempt IDs under one operation ID, and prefer status lookup when an expensive effect may already be running. Test response loss after every commit/downstream boundary.

### Answer 4

For GET, verify safe retrieval, no mutation through query parameters, representation/status agreement, conditional and range behavior, authorization, and cache controls. For HEAD, compare selection, status, validators, Content-Type, Vary, and other available fields with GET while asserting no response content. For PUT, test creation and replacement, complete-state omission semantics, media constraints, strong precondition success/failure, transformed-content validator restrictions, identical replay, response-loss retry, concurrent different PUT, and stored-cache invalidation. For DELETE, test removal association, repeat outcomes, no private request-content dependence, related-resource policy, and invalidation.

PATCH is known by the deployment but disallowed at this resource: return 405 and accurate Allow. Test a genuinely unimplemented extension method separately for 501 policy. Verify Allow changes with resource state and permitted disclosure. Exercise client, gateway, origin, cache, and downstream records; method filtering and authorization must agree without converting methods, losing content, or treating 404 as a universal substitute.

### Answer 5

Use GET/HEAD for authorized telemetry representations without mutation; freshness, timestamp, units, provenance, uncertainty, and cache policy remain explicit. Use conditional PUT for complete replacement of a client-known schedule resource when the representation truly defines complete desired state. A curtailment command is target-specific processing, commonly POST to a command/operation resource with durable operation identity, status lookup, deadlines, and duplicate-result replay. DELETE fits removal of a controllable URI association only if that is the real intent; physical device disconnection or de-energization is better modeled as an explicit command/resource transition. Emergency control needs an explicit unsafe command contract, not a misleading safe method.

Define actor/device identity, object- and action-level authority, approvals, command epoch, units, bounds, interlocks, schedule version, conditions, freshness, target set, expiry, cancellation, acknowledgement levels, partial outcomes, manual fallback, and audit. Retry only with stable identity and authoritative effect/status evidence; prevent stale or duplicate physical action. Test lost requests/responses, gateway retry, concurrent commands, stale telemetry, partition, overload, compromised credentials, device mismatch, clock failure, failover, rollback, and restoration in simulation and staged field exercises.

Named reviewers include grid/control-room operators, protection and power-systems engineers, field technicians, equipment vendors, safety and reliability authorities, cybersecurity, communications/network and API engineers, human factors/accessibility, emergency management, legal/regulatory and market authorities, affected utilities/customers, and independent technical assurance. The accountable operator and regulator accept residual risk. Protocol conformance, simulation, or internal course review supplies no permission to operate the grid and no external review is claimed.
