---
module_id: API-012
program: API & Service Engineering
level: 1
module_number: 12
title: Resource Identification
status: complete
last_verified: 2026-09-01
---

# Resource Identification

## One-Page Review

### Governing question

Which stable concepts should an API identify as resources, and how can those identities remain meaningful as state, representations, storage, and implementation change?

### Essential definitions

- A **resource** is a conceptual target of interaction; HTTP does not restrict its nature.
- A **resource identifier** distinguishes one resource from others within an identification scope.
- A **representation** communicates a past, current, or desired state of a resource; it is not the resource itself.
- An **entity** is a domain thing that may motivate a resource, but the mapping need not be one entity to one resource.
- A **naming authority** controls the namespace and the continuing meaning assigned to an identifier.
- An **alias** is another identifier for the same intended resource; a **canonical identifier** is the preferred stable reference.
- A **tombstone** is retained information that a formerly realized resource is intentionally gone.

### Central model, mechanism, or theorem

Following the resource model used to explain REST, treat resource $R$ as a time-varying mapping $M_R(t)$ from time $t$ to a set of equivalent values or representations. The identifier names the mapping—the continuing concept—not one database row, file, or serialized value. The set may change or be empty while the resource identity remains meaningful.

### Critical invariants

One identifier has one stable intended meaning. Identity does not change merely because representation, storage location, owner, or implementation changes. Distinct concepts do not silently collapse into one identifier. Authorization controls access but does not redefine identity per caller. Deletion and reuse policies are explicit. Aliases converge without creating redirect loops. Every identified concept has an owner and lifecycle.

### Common failures

Equating a resource with a row or JSON document; naming screens and controller methods; reusing deleted identifiers for unrelated things; changing meaning based on query flags or caller role; exposing unstable database keys; creating a resource for every noun; hiding long-running operations behind request attempts; treating a collection as merely an array; and assuming two equal representations imply one resource.

### Compact example

`the current Stockholm forecast` remains one resource while its representation changes hourly. `the forecast issued at 09:00` is a different, historically fixed resource. A database record, cached JSON, Swedish rendering, and English rendering can all represent either resource without becoming its identity.

### Connections

Outside-in requirements reveal which concepts consumers must reference. The next module assigns durable URI shapes. HTTP methods act on identified resources; representations, caching, conditional requests, authorization, eventing, and compatibility all depend on correct identity and lifetime.

## Governing Question

How do we choose resource boundaries and identities that express durable domain meaning rather than transient storage, workflow, or framework structure?

## Why This Matters

Identification is the backbone of an API. Clients bookmark, cache, authorize, link, retry, audit, and discuss identified concepts. A poor boundary spreads ambiguity everywhere: caching combines unrelated state, permissions apply at the wrong grain, events cannot name their subjects, and migrations break references.

RFC 3986 defines a URI as a compact sequence of characters that identifies an abstract or physical resource and deliberately permits a very broad meaning of resource. RFC 9110 calls the target of an HTTP request a resource and separates resource identification from request semantics. Fielding's REST dissertation explains a resource as a conceptual, time-varying mapping rather than a stored value. These sources provide a model, not an automatic recipe for domain boundaries.

This module decides **what** deserves identity and what that identity means. It does not optimize path spelling, pluralization, character encoding, or URI templates; those belong to URI Design. Nor does it claim every API must satisfy every REST architectural constraint.

## Prerequisites and Retrieval

Retrieve actors and outcomes, resources versus representations, HTTP method semantics, status codes, validators, caches, authorization, idempotency, and state transitions. Recall that equality of bytes, equality of domain state, and identity are different relations.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish resource, entity, representation, identifier, and storage key;
2. select resource boundaries from consumer interactions and invariants;
3. model time-varying, historical, collection, relationship, and operation resources;
4. specify identity, alias, deletion, and reuse lifecycles;
5. separate identification from method semantics and authorization;
6. evaluate composite and subordinate boundaries without mirroring tables; and
7. test resource models against migration, concurrency, privacy, and failure.

## Core Exposition

### Identify concepts, not serializations

A resource is whatever the API intends a request target to mean. It can correspond to a customer, today's exchange rate, a search result set, a relationship, a report generation operation, or a policy document. Its representation might be JSON today, CSV tomorrow, or absent for one caller. Changing media type does not create a new resource unless the negotiated form itself is the intended concept.

Do not infer identity from equal bytes. Two invoices can currently render identically while remaining distinct obligations. Conversely, one customer can have summary, detailed, redacted, localized, and historical representations while remaining one resource where the domain meaning is shared.

Storage keys are implementation identities. They can support public identity, but exposing them couples clients to allocation, tenancy, migration, and deletion rules. A stable opaque public identifier may map to several internal records over time. A meaningful external identifier may be appropriate when its authority and lifecycle are genuinely shared with consumers.

### Derive boundaries from interactions and invariants

Start with the outcomes from API-011. A concept usually merits independent resource identity when consumers must link to it, retrieve it independently, authorize it differently, cache it separately, observe its lifecycle, update it conditionally, or refer to it from events and audit records.

These are heuristics, not a noun-extraction algorithm. “Address” may be a value embedded in a customer when it has no independent lifecycle, or a resource when it is verified, shared, versioned, and authorized separately. “Approve” is a verb but an approval decision may be a durable resource with actor, evidence, state, and audit meaning.

Choose a boundary whose invariants can be stated. If line items cannot exist outside an order and change atomically with it, separate writable identities may create invalid intermediate states. If items have independent fulfillment, dispute, and authorization lifecycles, hiding them inside one oversized order resource may be equally wrong.

### Separate current concepts from historical facts

Some resources intentionally vary: current weather, latest account balance, active policy. Others identify an immutable observation or edition: the balance statement issued at month end, policy revision 17, or an audit event. Both are legitimate but must not share an identifier whose meaning changes from “current” to “snapshot.”

Let $M_R(t)$ describe the values associated with resource $R$ at time $t$. A current resource can map to different values as $t$ changes. A historical resource is intended to preserve a particular claim, though corrections and legal annotations may require new representations. Immutability is a contract with a fault and correction policy, not a consequence of a date in a path.

A concept can be identified before it has a current representation. A job identifier may exist while work is queued; a reserved username may exist without a profile. “No representation now” is different from “no such resource was ever identified.” Status and retention policy communicate the distinction.

### Collections are resources too

A collection is not merely a serialized array. It has membership rules, authorization, ordering, filtering, pagination, and change behavior. `all visible orders for tenant T under filter F` can denote a time-varying resource. Different filter semantics may identify different resources even if they happen to return equal members now.

Decide whether a filtered view is a stable linkable concept or only request control over one collection. Do not encode sensitive search criteria into identifiers without considering logs, referrers, caches, browser history, and signatures. Define whether pagination pages are ephemeral views, snapshot resources, or continuations over a changing collection.

Membership and member identity remain distinct. Removing a member from a collection does not necessarily delete the member resource. Deleting a collection does not automatically define cascading deletion. State those effects as domain policy.

### Relationships and subordinate resources

Some relationships deserve identity: a person's membership in a team can carry role, validity interval, approver, and lifecycle distinct from either endpoint. Modeling it only as an array entry makes conditional change, audit, and authorization awkward. Other relationships are simple links and need no independent target.

Hierarchy can communicate scope and ownership, but it must not imply false lifecycle dependence. If an invoice retains identity after a customer account closes, its identity should not become unreachable or semantically reassigned. Multiple containment paths to the same concept need a canonical identity and explicit aliases.

Subordinate resources are useful when the parent establishes namespace or lifecycle. They become harmful when identifiers change after reparenting, paths grow with mutable organization structure, or the same object appears to be different resources under several parents.

### Model commands and long-running work carefully

Not every action needs an action-named endpoint. Standard methods can express state transfer on resources. Yet commands with their own acceptance, progress, cancellation, result, and audit lifecycle are naturally modeled as operation resources. The resource is the durable operation, not the transient POST request that created it.

Separate requested intent from resulting domain state. A transfer request may be rejected, accepted, settled, reversed, or expire. Its identifier lets clients recover after a timeout and observe a terminal outcome. Reusing the destination account identifier as the operation identifier would conflate what changes with the attempt to change it.

### Define identity equality and canonicalization

State what makes two references denote the same resource. String equality alone is insufficient when aliases, redirects, case rules, percent-encoding, default ports, or migrated authorities exist. Conversely, aggressive normalization can merge identifiers whose owner treats them as distinct. URI equivalence details belong to the next module; the resource model must supply the semantic answer.

When several identifiers denote one resource, choose a canonical identifier for generated links, cache coordination, signatures, and audit correlation. Redirect or link aliases according to migration and method-safety policy. Detect loops and preserve authorization. An alias is not permission to expose a private canonical target.

### Govern deletion, absence, and reuse

Deletion can mean soft deletion, removal from a collection, revocation, anonymization, archival, scheduled destruction, or loss of access. Specify which resource ceases to have a representation, which facts remain, who may observe them, and whether restoration is possible.

Identifier reuse is dangerous because caches, logs, events, bookmarks, and delayed messages outlive application rows. Reassigning `/accounts/42` from Alice to Bob can disclose or misapply stale actions. Durable public identities should normally never be reassigned to an unrelated resource. If a bounded namespace forces reuse, include generation identity and a proven expiry model.

A tombstone can distinguish intentional removal from temporary outage and prevent silent rebinding. It still has retention, privacy, and authorization costs. After tombstone expiry, the service may return less specific absence while continuing never to reuse the identity.

### Keep authorization orthogonal to identity

The same resource can yield different representations or no accessible representation for different principals. That does not make it a different resource per caller. Authorization decides whether an action or representation is allowed; identification decides the intended target.

Sometimes actor-specific views are genuinely different resources because their semantics differ, such as a public aggregate and a regulator's signed report. Make that a deliberate boundary, not an accidental consequence of filtering fields after retrieval. Error disclosure policy may intentionally make forbidden and unknown targets observationally indistinguishable.

### Validate the model under change

Walk every resource through creation, mutation, transfer, merge, split, deletion, restoration, migration, and archival. Test concurrent rename, ownership change, duplicate import, delayed event, stale cache, replayed request, and cross-tenant lookup. Ask whether old references retain one meaning and whether new implementations can honor it.

Maintain a resource inventory with owner, semantic definition, identity source, lifecycle, canonicalization, authorization boundary, representation families, and events. The inventory supports review; it does not replace executable contract tests or domain governance.

## Definitions and Notation

Let $I$ be identifiers, $R$ resources, $V$ possible values, and time domain $T$. Assignment $A:I\to R$ records the intended denotation within one naming authority. Mapping $M_R:T\to\mathcal{P}(V)$ gives the values associated with resource $R$ at time $t$. Identifier stability requires $A(i)$ not be silently rebound to unrelated $R'$ over the supported lifetime.

An **identity key** distinguishes a domain concept. A **surrogate key** is implementation-assigned. A **natural key** comes from domain meaning but can still change or be reused. **Canonicalization** selects a preferred identifier among intended aliases. **Dereference** means attempting interaction through an identifier; identification does not guarantee current dereferenceability.

## Mechanisms, Invariants, or Proof Structure

For each candidate resource:

1. State its semantic definition without representation or storage vocabulary.
2. Name actors and independent interactions requiring reference to it.
3. State identity equality and non-equality examples.
4. Define current, historical, collection, relationship, or operation character.
5. Define creation, mutation, transfer, deletion, tombstone, restoration, and reuse policy.
6. Identify the naming authority, canonical identity, and aliases.
7. State authorization independently for each action and representation.
8. Test migration, concurrency, stale evidence, delayed messages, and privacy.
9. Trace the boundary back to outside-in requirements.

The **semantic-stability invariant** forbids rebinding. The **representation-independence invariant** permits format and implementation evolution without identity change. The **authority invariant** assigns one owner for namespace meaning. The **non-aliasing invariant** prevents distinct resources from accidentally sharing identity. The **lifecycle invariant** makes absence, deletion, and reuse explicit.

## Alternatives and Trade-Offs

**Natural versus opaque identifiers.** Natural identifiers can be recognizable and interoperable but may change, reveal sensitive facts, or be controlled elsewhere. Opaque identifiers improve stability and privacy but require lookup and offer little human diagnosis. Use domain identifiers only when their authority and lifecycle match the resource contract.

**Embedded value versus independent resource.** Embedding simplifies atomic reads and writes. Independent identity enables linking, authorization, caching, conditional mutation, and lifecycle. Split only when the concept has meaningful independence.

**Stable current resource versus immutable versions.** A current identity is convenient for latest state. Version identities support reproducibility and audit. Many domains need both, linked explicitly, rather than forcing one identifier to serve incompatible meanings.

## Failure Modes and Misconceptions

A resource is not necessarily a database row, object instance, file, microservice, or JSON body. Equal representations do not imply equal identity. Different representations do not imply different identity. Authentication does not define the target. A `404` alone does not specify whether identity never existed, is gone, is hidden, or is temporarily unavailable. Hierarchical identifiers do not prove aggregate ownership. “RESTful” naming cannot rescue an unstable domain model.

## Worked Examples

### Example 1

The “current exchange rate from SEK to EUR” changes every minute, while a signed rate used for invoice 817 must remain reproducible. Model a current resource and a distinct historical rate observation linked from the invoice. **Conclusion:** current and historical meanings need different identities even when one once represented the other.

### Example 2

Two customers have identical names and addresses. Their JSON is equal, but their obligations, permissions, and histories differ. They remain distinct resources. **Conclusion:** representation equality is not identity equality.

### Example 3

A customer moves and its record migrates from one database shard to another. Its public identifier remains assigned to the same customer concept. **Conclusion:** storage movement must not rebind public identity.

### Example 4

An order address is edited only with the order and has no separate permission or history. Making it independently writable would allow an address state the order invariant rejects. **Conclusion:** keep a value embedded when it lacks an independent lifecycle.

### Example 5

A team membership has role, start/end dates, approver, suspension, and audit events. Model it as a relationship resource rather than an unaddressable array slot. **Conclusion:** behavior and lifecycle, not grammatical nouns, justify resource identity.

### Example 6

A report request returns `202`; generation continues for minutes and may be cancelled. A durable operation resource records queued, running, succeeded, failed, or cancelled and links to the result. **Conclusion:** long-running work needs identity separate from its initiating request attempt.

### Example 7

Account 42 is deleted, then its database sequence later emits 42 for a new account. Old events update the new account. The service switches to non-reused public identities and retains authorized tombstones. **Conclusion:** identifier reuse violates semantic stability across delayed evidence.

### Example 8

`/people/7` and an imported legacy reference identify the same person. Generated representations link only the canonical identity; the alias redirects under a bounded migration policy. **Conclusion:** governed aliases support migration without inventing two resources.

### Example 9

A caller cannot access an existing case and receives the same response as for an unknown case. Internally both references have different identity facts, but disclosure policy makes them observationally equal. **Conclusion:** authorization can hide identity evidence without redefining identity.

### Example 10

A filtered collection returns no members today. The saved compliance query still has stable definition, owner, and schedule, so it can be a resource whose current value set is empty. **Conclusion:** an empty representation or membership set does not necessarily mean no resource exists.

## Cross-Program Connections

[Outside-In API Requirements](011-outside-in-api-requirements.md) supplies actor outcomes and acceptance evidence. [Resources, Representations, and Messages](001-resources-representations-and-messages.md) supplies the foundational distinction, and the next module, URI Design, encodes the chosen identities. Domain-driven design informs aggregates and value objects; databases own internal keys and persistence; security owns principal and disclosure policy; distributed systems owns delayed messages and partial observation.

## References

1. R. Fielding, M. Nottingham, and J. Reschke, *RFC 9110: HTTP Semantics*, Internet Standard 97, June 2022, Sections 3.1–3.2 and 4. Checked 2026-09-01. https://www.rfc-editor.org/rfc/rfc9110.html
2. T. Berners-Lee, R. Fielding, and L. Masinter, *RFC 3986: Uniform Resource Identifier (URI): Generic Syntax*, Internet Standard 66, January 2005, as updated by RFC 7320 and RFC 8820. Checked 2026-09-01. https://www.rfc-editor.org/rfc/rfc3986.html
3. R. T. Fielding, *Architectural Styles and the Design of Network-based Software Architectures*, doctoral dissertation, University of California, Irvine, 2000, Section 5.2.1.1. Checked 2026-09-01. https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm

## Exercises

### Exercise 1

Explain why a resource, a representation, a domain entity, and a database row can be related without being interchangeable.

### Exercise 2

For a news service, distinguish identities for “current front page,” “front page edition issued at 09:00,” an article, and the article's current English representation. State which can change over time.

### Exercise 3

Decide whether a shipping address should be embedded or independently identified for an order API. Analyze lifecycle, sharing, authorization, audit, conditional update, and aggregate invariants.

### Exercise 4

Compare natural email addresses, sequential integers, and opaque random identifiers as public customer identities under rename, privacy, enumeration, import, merge, deletion, and reuse.

### Exercise 5

A university merges two student records discovered to represent one person, while transcripts and historical submissions already reference both. Design a resource-identity and alias policy that preserves audit history, authorization, and future linking.

## Answers to the Exercises

### Answer 1

A resource is the API's conceptual interaction target. A representation communicates some state of it. A domain entity is one modeling approach that may motivate the target. A row is a persistence mechanism. One resource can have many representations and rows; one representation can aggregate many entities; one entity can support current, historical, and actor-specific resources. Correct analysis states each relation instead of assuming one-to-one equality.

### Answer 2

The current front page is a time-varying resource whose selected stories and layout can change. The 09:00 edition is a distinct historical resource intended to remain fixed except for governed correction metadata. An article has its own continuing identity and may change under editorial policy. Its current English representation is one negotiated or linked expression of that article, not necessarily a separate resource; it becomes separate only if the service assigns independently linkable semantics and lifecycle to that edition/language concept.

### Answer 3

Embed the address when it exists only as order state, changes atomically with the order, shares its authorization, and is never linked or audited independently. Identify it separately when it is verified or shared across orders, has independent permissions/history, needs conditional update, or must survive order lifecycle changes. A hybrid can reference an address-book resource while copying an immutable fulfillment snapshot into the order. The choice must preserve the rule that later address-book edits do not silently rewrite an accepted shipment destination.

### Answer 4

Email is recognizable and interoperable but mutable, personally identifying, and sometimes recycled. Sequential integers are compact but enumerable, reveal volume, and collide across imports unless namespaced; non-reuse still needs enforcement. Opaque random identifiers are stable and hard to enumerate but require lookup and careful collision generation. A durable design normally uses a non-reused opaque public identity, treating email as mutable contact/lookup data and retaining external natural identifiers with explicit authorities when integration requires them.

### Answer 5

Choose one canonical student resource only after an authorized merge decision. Preserve both former identifiers as non-reassignable aliases under controlled resolution, and retain immutable provenance on every transcript and submission showing the identifier and authority used at creation. Access checks resolve aliases to the canonical subject without exposing merge history to unauthorized callers. Conflicting facts require governed reconciliation rather than silent overwrite. New links use the canonical identifier; audit exports retain original references; an erroneous merge needs a compensating split process that never reuses either historical identity for an unrelated person.
