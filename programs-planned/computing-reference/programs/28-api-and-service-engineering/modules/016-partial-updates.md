---
module_id: API-016
program: API & Service Engineering
level: 1
module_number: 16
title: Partial Updates
status: complete
last_verified: 2026-09-01
---

# Partial Updates

## One-Page Review

### Governing question

How can a client request a bounded change to resource state without turning omission, null, arrays, concurrency, authorization, and retries into silent data corruption?

### Essential definitions

- **PATCH** requests application of changes described by a patch document to the target resource.
- A **patch media type** defines the instruction language; PATCH alone does not define how content changes state.
- **JSON Patch** (`application/json-patch+json`) is an ordered sequence of `add`, `remove`, `replace`, `move`, `copy`, and `test` operations using JSON Pointer paths.
- **JSON Merge Patch** (`application/merge-patch+json`) describes changes by example; object member `null` removes that member.
- **atomic application** means every change in one patch succeeds or none becomes visible.
- A **base point** is the target state against which patch instructions were prepared.
- A **precondition** rejects application when current target state differs from the client's declared basis.

### Central model, mechanism, or theorem

Let patch document $P$ denote partial function $A_P:S\rightharpoonup S$ over valid resource states. Application succeeds only when $A_P(s)$ is defined, authorized, satisfies invariants, and any HTTP precondition holds; then the state changes atomically from $s$ to $A_P(s)$. Otherwise state remains $s$. The media type determines $A_P$, not the word PATCH.

### Critical invariants

Patch media type is explicit and supported. All operations validate before commit and become visible atomically. Field-level authorization is evaluated on intended effects, not only syntax. Omitted, null, empty, and removed are distinct where the domain requires them. Array positions are not stable identity under concurrency. Base-dependent changes use strong validators. Retries preserve operation meaning and do not repeat non-idempotent effects accidentally.

### Common failures

Sending partial JSON with `application/json`; treating PATCH as merge-by-default; using Merge Patch where null is a real value; addressing array members by unstable index; applying operations one by one before a later failure; validating the document but not resulting state; accepting changes to read-only fields; losing concurrent updates; logging sensitive patch content; and advertising PATCH without supported media types.

### Compact example

Starting state has `name="Ada"`, `locale="en"`, and `phone=null`. Merge Patch `{"locale":"sv","phone":null}` changes locale and removes `phone`; it cannot express “retain an explicit JSON null” for that member. JSON Patch can distinguish replacing `/phone` with null from removing `/phone`, but still needs authorization and an `If-Match` base validator.

### Connections

Complete PUT replacement, validators, content types, idempotency, JSON Pointer, schemas, error responses, and authorization all constrain partial update. Later modules develop contracts, JSON Schema, OpenAPI, and versioning.

## Governing Question

Which partial-change language, preconditions, validation, and response semantics let an API update only intended state while preserving the whole resource's invariants?

## Why This Matters

Partial updates save bandwidth and reduce read-modify-write ergonomics, but they introduce a second language over the resource representation. Omission can mean “unchanged,” `null` can mean remove or a real value, and an array index can move between read and write. A syntactically valid patch can create invalid or unauthorized resulting state.

RFC 5789 defines PATCH and requires the entire set of changes to be applied atomically. It does not make PATCH safe or idempotent and uses `Accept-Patch` to advertise supported patch media types. RFC 6902 defines JSON Patch and its ordered operations. RFC 7396 defines JSON Merge Patch, including special removal semantics for null object members. RFC 9110 supplies validators, preconditions, statuses, and general HTTP semantics.

The correct format follows domain needs. Merge Patch is compact for object-dominated documents without meaningful explicit nulls. JSON Patch is more expressive for precise operations and tests but exposes representation paths and array-index hazards. A domain-specific command can be clearer when change meaning is behavioral rather than document editing.

## Prerequisites and Retrieval

Retrieve PUT replacement, media types, ETags, `If-Match`, `If-None-Match`, JSON objects and arrays, JSON Pointer, authorization, domain invariants, atomic transactions, idempotency, and ambiguous outcomes. Recall that a representation path is not automatically a stable domain identity.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish PATCH method semantics from patch-document semantics;
2. compare JSON Patch and JSON Merge Patch precisely;
3. specify omission, null, removal, empty, and default behavior;
4. apply patches atomically and validate resulting resource state;
5. protect base-dependent changes with strong preconditions;
6. authorize fields, paths, transitions, and side effects;
7. reason about array indices, retries, duplicate effects, and errors; and
8. decide when PUT or a domain operation is safer than PATCH.

## Core Exposition

### PATCH carries instructions, not a partial representation by itself

PATCH requests that instructions in its content be applied to the target. `Content-Type` identifies the instruction language. `application/json` only says the content is JSON; it does not say omitted members remain unchanged, null deletes, or arrays merge. An API that accepts ad hoc “partial JSON” must register or document a media type and exact algorithm rather than borrowing ambiguous folklore.

The origin can advertise supported formats with `Accept-Patch`, commonly in an OPTIONS response. Capability discovery does not replace contract documentation: clients still need allowed paths, types, invariants, authorization, maximum operations, and response behavior.

PATCH can affect related resources when application semantics require it, but atomicity covers the directly affected change set declared by the patch contract. Do not claim distributed all-or-nothing behavior across services unless a mechanism and evidence support it.

### Apply all or none

RFC 5789 requires atomic application: a concurrent GET must not observe half a patch, and if any operation fails none of the changes apply. Implement by parsing and bounding the entire document, resolving paths, authorizing intended changes, computing candidate state, validating whole-resource and cross-field invariants, then committing under an appropriate transaction or compare-and-set.

Validation must cover the result, not only each instruction. Replacing `start` and `end` separately can make each type-correct while producing `start > end`. Removing a parent object can invalidate a child reference. Limits and uniqueness may span several operations.

If the storage engine cannot atomically apply the declared scope, narrow the patch contract, use a durable workflow with compensating semantics, or reject the operation. Applying three of five changes and returning an error violates PATCH atomicity.

### JSON Merge Patch

Merge Patch resembles the target JSON. For an object patch, members absent from the patch remain unchanged; present non-null values replace or recursively merge; a null member removes the target member. A non-object patch replaces the entire target value.

This simplicity has sharp limits. It cannot distinguish setting an object member to JSON null from removing it. Arrays are replaced as whole values rather than merged by element identity. The algorithm describes JSON document transformation, not field authorization, schema defaults, domain transitions, or persistence mapping.

Merge Patch works well for shallow profile-like objects where null means absence and arrays are intentionally whole-value fields. It is poor for nullable medical fields, ordered collaborative lists, or resources where removal and explicit unknown are distinct.

### JSON Patch

JSON Patch is an ordered array of operation objects. `add`, `remove`, `replace`, `move`, `copy`, and `test` address locations with JSON Pointer. Each operation consumes the result of previous operations. A failure terminates evaluation, and PATCH atomicity means the overall resource remains unchanged.

`test` can assert a representation value before later operations, enabling fine-grained guards. It is not a substitute for HTTP `If-Match` when the whole selected representation or intermediary behavior matters. A server can use both: `If-Match` protects the resource base, while `test` asserts a specific document condition.

Path syntax couples clients to representation structure. Renaming or nesting fields can break stored patches even when domain meaning remains compatible. Treat patch paths as public contract and include them in version and compatibility review.

### Arrays and identity

JSON Patch array locations use indices and `-` for append. Indices describe representation position, not stable member identity. If another writer inserts at index 0, a patch targeting `/items/3` may mutate a different item. Strong `If-Match` rejects the changed base; without it, positional changes are unsafe.

For domain collections, prefer operations addressed by stable member identity or a domain-specific relationship resource. Replacing a whole small array through Merge Patch can be acceptable under `If-Match`; for large collaborative collections, separate member operations often give clearer concurrency and authorization.

Never invent “merge arrays by ID” under standard Merge Patch. That is a distinct custom algorithm needing its own media type, duplicate rules, order semantics, and tests.

### Omission, null, empty, default, and removal

Write a truth table for every mutable field. Omitted may mean unchanged in a patch. Explicit null may mean store unknown, clear a value, or remove a member depending on format and schema. Empty string, empty array, and empty object are values, not automatic removal. Default application may occur only at creation, on every update, or never; document it.

Server-managed and computed fields must be rejected or ignored consistently. Rejecting is often safer because a client learns that its intended effect did not occur. Silently ignoring an attempted `role="admin"` while applying other fields can produce false client beliefs.

Schema validation tools often validate the patch document as though it were a resource representation, which is wrong. A Merge Patch schema must account for removal markers; a JSON Patch schema validates operations and path/value constraints; the candidate resulting resource must then satisfy the resource schema and domain invariants.

### Preconditions and collision control

Many patches depend on a known base. Use a strong ETag from GET and require `If-Match` on PATCH. If current selected representation differs, return `412` without applying the document. A server can return `428` when policy requires a condition and the client omitted it.

JSON Patch `test` narrows conditions but can leak protected current values through success/failure and is evaluated under application authorization. It also depends on representation equality rules, not arbitrary domain equivalence.

Preconditions do not solve every race. If the patch changes one resource based on another resource's quota, transaction or coordinated invariant enforcement is still required. Field-level versioning can increase concurrency but adds merge semantics and client complexity.

### Idempotency and retries

PATCH is not idempotent by standard definition, though a particular patch can be. Replacing `/status` with `closed` is usually idempotent in intent; adding 1 to a counter or appending an array entry is not. JSON Patch `add` to a fixed object member can be idempotent or conflicting depending on prior state, while appending with `-` repeats occurrences.

After a lost response, retry only with known semantics. `If-Match` may fail if the original succeeded, which is useful evidence but not a complete operation lookup. For non-idempotent business effects, use an operation key and retained outcome. Never generate a new logical key for an automatic retry.

### Authorization and sensitive changes

Authorize the target, each addressed path, the old-to-new transition, and side effects. A user allowed to edit display name may not edit tenant ID, verification status, balance, ownership, or role. `move` and `copy` need authorization on source disclosure and destination mutation.

Avoid revealing protected field existence through distinct errors. Bound path length, operation count, document size, nesting, and evaluation cost. Reject prototype-pollution keys or dangerous mapping behavior in implementation languages even when valid JSON names are supplied.

Patch documents can contain secrets and personal data. Redact request logging, traces, error echoes, and audit access. Audit the semantic effect with protected before/after evidence or changed-field names according to policy, not necessarily the raw patch.

### Responses and cache effects

After successful application, return `204` when no representation is supplied or `200` with a representation of resulting state. If returning a validator, ensure it corresponds to the actual selected representation after transformation. Asynchronous partial change is usually better modeled as a submitted operation resource because PATCH atomicity and eventual multi-step behavior otherwise become unclear.

PATCH errors distinguish unsupported method, unsupported patch media type, malformed document, invalid path, failed test/precondition, domain conflict, forbidden transition, and unavailable dependency. Stable problem types help clients decide whether to correct, refetch, reconcile, or stop.

Successful PATCH makes cached target responses stale under its defined semantics. Derived collections and related resources need their own invalidation and freshness strategy. A response to PATCH has narrow cacheability requirements; do not assume mutation responses are generally reusable as GET responses.

## Definitions and Notation

Let valid state set be $S$. Patch $P$ denotes partial function $A_P:S\rightharpoonup S$ because some instructions are undefined for some states. With authorization predicate $Z(p,P,s)$, invariant predicate $I(s')$, and precondition $H(v_c,v(s))$, commit is allowed only when $s'=A_P(s)$ exists and $Z\land I(s')\land H$ is true. Atomic failure leaves state exactly $s$.

A **patch document** is a representation of change instructions. A **target document** is the selected representation state the format transforms. A **JSON Pointer** identifies a location through reference tokens; it is not a domain identifier. A **candidate state** is the uncommitted result used for validation. A patch is **base-dependent** when correct interpretation requires the state the client observed.

## Mechanisms, Invariants, or Proof Structure

Process a partial update in this order:

1. Authenticate, authorize target access, and bound request size.
2. Select and validate the exact patch media type.
3. Evaluate required HTTP preconditions against current selected state.
4. Parse all operations and resolve paths without applying visible effects.
5. Authorize source, destination, field, transition, and side effects.
6. Compute candidate result using the media type's exact algorithm.
7. Validate candidate schema, cross-field invariants, uniqueness, and related constraints.
8. Commit every directly affected change atomically or none.
9. Return truthful resulting state, validator, or problem outcome.
10. Invalidate affected views and retain retry/audit evidence under policy.

The **format invariant** prevents ambiguous “partial JSON.” The **atomicity invariant** prohibits partial visibility or commit. The **result invariant** validates whole candidate state. The **base invariant** requires conditions for positional or state-dependent patches. The **authorization invariant** checks semantic effect rather than accepted field names alone.

## Alternatives and Trade-Offs

**PUT versus PATCH.** PUT has simple complete replacement and idempotent intent but sends full state and can erase unknown fields. PATCH expresses bounded change but adds an instruction language, atomic evaluation, and path compatibility.

**Merge Patch versus JSON Patch.** Merge Patch is compact and readable for object-shaped data but reserves null for removal and replaces arrays wholesale. JSON Patch distinguishes operations and supports `test`, move, and copy but is verbose and position/path sensitive.

**Generic patch versus domain operation.** Generic patch reduces endpoint count and supports field editing. A domain operation such as “approve,” “transfer ownership,” or “increment quota” can express authorization, invariants, idempotency, and audit meaning more safely than document surgery.

**Whole-resource versus field-level concurrency.** One ETag is simple and prevents all stale patches but can reject non-conflicting edits. Field versions or server merge increase concurrency but require formal conflict and invariant semantics.

## Failure Modes and Misconceptions

PATCH does not mean merge. `application/json` does not define partial update. JSON Merge Patch null means member removal, not stored null. JSON Patch paths expose representation structure. Array indices are not member IDs. `test` is not universal authorization or transaction isolation. Atomicity cannot be replaced by compensation after exposing partial state. An idempotent-looking patch can still trigger duplicate domain side effects. Schema-valid candidate state can still violate authorization or cross-resource policy.

## Worked Examples

### Example 1

An API accepts `application/json` body containing only `{"locale":"sv"}` and preserves every omitted field. No media type defines this merge. One client assumes replacement and another assumes patch. **Conclusion:** partial semantics require an explicit patch format.

### Example 2

Target has `phone:null` meaning “explicitly unknown.” Merge Patch `{"phone":null}` removes the member, losing the distinction. The API chooses JSON Patch replace with null or redesigns the field model. **Conclusion:** Merge Patch is unsuitable when null and absence differ.

### Example 3

JSON Patch replaces `/items/2/name`; another writer inserted at index 0 after the client's read. With required `If-Match`, the patch receives `412` instead of editing the wrong item. **Conclusion:** positional paths need a stable base.

### Example 4

A patch first changes `start`, then removes required `owner`, and the second operation fails. An implementation that already persisted `start` violates atomicity. Candidate-state evaluation followed by one transaction leaves both unchanged. **Conclusion:** every instruction succeeds or none applies.

### Example 5

Each of `start=20` and `end=10` is type-valid, but together violate `start <= end`. The server validates the complete candidate and rejects without commit. **Conclusion:** operation validation cannot replace resulting-state invariants.

### Example 6

A profile editor sends a patch to change `/role` to `admin`. The path exists and value is schema-valid, but the principal lacks transition permission. The entire patch is forbidden. **Conclusion:** authorization concerns semantic old-to-new effects.

### Example 7

JSON Patch contains `test /status = draft` then `replace /status = published`. `If-Match` also protects the full base representation. Both pass and the transition commits. **Conclusion:** document assertions and HTTP preconditions can serve complementary scopes.

### Example 8

A JSON Patch appends to `/tags/-`; response is lost and an automatic retry appends twice. The API uses a stable relationship identity or operation key instead. **Conclusion:** PATCH and append are not inherently idempotent.

### Example 9

Merge Patch replaces a 50,000-element array to modify one member. Payload, conflict rate, and validation cost spike. The design exposes independently identified membership operations. **Conclusion:** partial document syntax cannot repair a poor resource boundary.

### Example 10

A service logs raw password-reset and medical-preference patches for debugging. Access logs become a secondary sensitive database. The service records bounded changed-field audit evidence with restricted before/after access. **Conclusion:** patch observability requires data-minimization policy.

## Cross-Program Connections

[Create, Read, Update, and Delete Semantics](015-create-read-update-and-delete-semantics.md) supplies PUT and lifecycle behavior; [Conditional Requests](006-conditional-requests.md) supplies validators; [Content Negotiation](005-content-negotiation.md) supplies media-type selection. JSON Schema, OpenAPI, authorization, errors, versioning, and testing later govern patch contracts. Database transactions can implement atomicity but do not define document semantics.

## References

1. L. Dusseault and J. Snell, *RFC 5789: PATCH Method for HTTP*, Standards Track, March 2010. Checked 2026-09-01. https://www.rfc-editor.org/rfc/rfc5789.html
2. P. Bryan and M. Nottingham, *RFC 6902: JavaScript Object Notation (JSON) Patch*, Standards Track, April 2013. Checked 2026-09-01. https://www.rfc-editor.org/rfc/rfc6902.html
3. P. Hoffman and J. Snell, *RFC 7396: JSON Merge Patch*, Standards Track, October 2014. Checked 2026-09-01. https://www.rfc-editor.org/rfc/rfc7396.html
4. R. Fielding, M. Nottingham, and J. Reschke, *RFC 9110: HTTP Semantics*, Internet Standard 97, June 2022, Sections 8.8, 13, and 15. Checked 2026-09-01. https://www.rfc-editor.org/rfc/rfc9110.html

## Exercises

### Exercise 1

Distinguish PATCH method semantics, patch media type, patch document, target representation, candidate state, and committed resource state.

### Exercise 2

Starting with `{"name":"Ada","phone":null,"tags":["math","code"]}`, derive results for Merge Patch `{"phone":null,"tags":["logic"]}` and for JSON Patch that replaces `/phone` with null and adds `logic` at the array end.

### Exercise 3

Diagnose an implementation that streams JSON Patch operations directly to a database, authorizes only the target URI, and returns an error after the fourth of five operations fails.

### Exercise 4

Compare Merge Patch, JSON Patch, complete PUT, and domain-specific operations for editing a bank account's mailing address, owner, status, and balance.

### Exercise 5

A collaborative robot fleet updates mission plans containing ordered waypoints while robots may be offline. Design partial-update format, identity, concurrency, atomicity, safety validation, retry, and audit semantics.

## Answers to the Exercises

### Answer 1

PATCH says the target should apply enclosed change instructions. The media type defines the instruction language. The patch document is one instance of those instructions. The target representation supplies the base document view. Candidate state is the computed but uncommitted result used for authorization and invariant validation. Committed resource state is the authoritative result after an atomic successful transition; it may have server-managed fields and representations beyond the transformed document.

### Answer 2

Merge Patch removes member `phone` because null is the removal marker and replaces the entire `tags` array, yielding `{"name":"Ada","tags":["logic"]}`. JSON Patch `replace /phone` with JSON null retains the member as null; `add /tags/-` with `logic` appends, yielding `{"name":"Ada","phone":null,"tags":["math","code","logic"]}`. The latter append is base-sensitive and non-idempotent under blind retry.

### Answer 3

Visible database writes before full evaluation violate PATCH atomicity; failure must leave the target unchanged. Target-level authorization misses forbidden fields, move/copy source disclosure, and transitions. Parse and bound all operations, evaluate preconditions, authorize every semantic effect, compute candidate state, validate resulting invariants, and commit through one transaction or compare-and-set. If the declared scope cannot be atomic, reject it or redesign as a workflow rather than compensating after exposure.

### Answer 4

Merge Patch can edit an address compactly if null means removal and nested-object merging is acceptable. JSON Patch can precisely replace address fields and test status but exposes paths. Complete PUT suits a round-trippable complete account representation but should not allow client control of server-managed balance. Owner transfer, status transition, and balance movement are high-value domain operations with specialized authorization, evidence, invariants, and idempotency; generic field patching is unsafe. A sound API may permit address patching while requiring dedicated commands for the others.

### Answer 5

Give mission, waypoint, and change operation stable identities; do not address waypoints only by array index. Require a strong mission-plan ETag and retained logical operation key. Use a domain-specific patch or JSON Patch constrained to waypoint IDs and allowed transitions, with explicit order semantics. Compute the complete candidate, validate collision avoidance, bounds, authorization, firmware capability, and emergency interlocks, then commit atomically to authoritative mission state. Offline robots reconcile versions before activation. Lost responses use operation lookup; repeated changes never append twice. Audit source version, intended change, validation evidence, authorization, activation version, and each robot's acknowledged state.
