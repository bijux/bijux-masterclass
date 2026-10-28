---
module_id: API-038
program: API & Service Engineering
level: 1
module_number: 38
title: Concurrency Control at the API Boundary
status: complete
last_verified: 2026-09-01
---

# Concurrency Control at the API Boundary

## One-Page Review

### Governing question

How should an API expose and enforce assumptions about current resource state so concurrent clients cannot silently overwrite, duplicate, or invalidate one another's work?

### Essential definitions

- A **lost update** occurs when a later write overwrites an earlier concurrent write without incorporating or rejecting it.
- A **validator** is opaque metadata representing a selected resource representation's state; an entity tag is an HTTP validator.
- A **precondition** makes method execution contingent on current resource state, such as `If-Match` or `If-None-Match`.
- **optimistic concurrency control** lets work proceed without holding a client-visible lock and rejects a write when its observed version is stale.
- **pessimistic concurrency control** blocks or serializes contenders through locks or exclusive ownership.
- A **domain conflict** means the requested transition is invalid in current business state even if an HTTP precondition passed.
- A **serialization failure** aborts a transaction whose concurrent history cannot safely commit under the selected isolation guarantee.

### Central model, mechanism, or theorem

Let a client observe resource state $(x,v)$ and propose transformation $g$. A compare-and-set update is

$$
\operatorname{CAS}(v,g)=
\begin{cases}
x' = g(x),\;v'=v+1 & \text{if current version}=v,\\
\text{reject stale} & \text{otherwise}.
\end{cases}
$$

The comparison and write must be one atomic operation or transaction. At the HTTP boundary, a strong entity tag can carry an opaque representation validator and `If-Match` can express the precondition. This prevents the covered lost update; it does not by itself protect cross-resource invariants, remote effects, or reads not represented by the validator.

### Critical invariants

The server generates opaque validators from authoritative committed state. A write precondition is evaluated after normal authentication/authorization/request checks and immediately before the action under the same consistency boundary as the write. `If-Match` uses strong comparison. Missing required preconditions, false preconditions, and domain conflicts remain distinct. Every successful state-changing response exposes the new validator when the representation contract supports it. Database predicates, versions, constraints, locks, or serializable execution enforce the condition; application read-then-write alone does not. Concealment and field authorization survive conflict responses.

### Common failures

Accepting blind updates after advertising ETags; comparing an ETag in memory then issuing an unconditional write; using weak ETags with `If-Match`; deriving validators from timestamps with insufficient resolution; exposing raw database transaction IDs; sharing one ETag across byte-different negotiated representations; returning `409` for every failed precondition; requiring a precondition but returning `412` when it is absent; resolving mismatch with last-write-wins silently; retrying stale writes automatically without merging user intent; holding an HTTP lock across user think time; and assuming one row version protects a multi-row invariant.

### Compact example

Two editors GET document `d7` with ETag `"v12-json"`. Editor A sends `PUT` with `If-Match: "v12-json"`; the database update includes `WHERE id='d7' AND version=12`, writes the new document, increments to 13, and returns ETag `"v13-json"`. Editor B's later request still carries `v12`; zero rows match and the API returns `412`. B fetches, merges, and resubmits. **Conclusion:** the stale assumption is rejected atomically instead of overwriting A.

### Connections

[Request-Scoped Transaction Boundaries](036-request-scoped-transaction-boundaries.md) supplies the atomic database boundary, [Idempotency Keys](037-idempotency-keys.md) protects retries of one logical command, and [Error Translation](035-error-translation.md) separates `428`, `412`, `409`, and safe concealment. [Rate Limits and Quotas](../ROADMAP.md) next controls competing demand rather than state correctness.

## Governing Question

Which resources require conditional requests, what validator represents their visible state, where is the condition enforced atomically, how are domain and database conflicts translated, and what recovery can a client safely perform?

## Why This Matters

HTTP clients operate on observations from the past. A user loads a profile, pauses, and submits an edit after another actor changed it. A controller reads remaining capacity while another request reserves it. Two workers both observe a pending job. Without concurrency control, each request can be locally valid and the combined history wrong.

Last-write-wins is a concurrency policy, not an absence of policy. It is acceptable for some telemetry, replaceable preferences, or convergent registers, but destructive for documents, limits, approvals, money, inventory, and workflow transitions. Even when overwriting is technically allowed, users need to know whether another change was discarded.

Database transactions prevent partial local commits, but their default isolation may still permit nonrepeatable reads, phantoms, write skew, or application-level lost intent. HTTP conditional requests let a client state the version assumption it made. The database must then enforce that assumption at the actual write.

Concurrency failures also need exact public meaning. A missing required condition tells the client to supply one. A false condition tells it to refresh or reconcile. A domain conflict says current state rejects the transition. A serialization failure may permit a bounded server replay when the whole transaction is pure and protected. Treating all four as `409 conflict` hides the recovery protocol.

## Prerequisites and Retrieval

Retrieve HTTP representation metadata, ETags, conditional requests, and precondition precedence; `412 Precondition Failed` and `428 Precondition Required`; request parsing and authorization; database atomic updates, isolation, constraints, locks, and serialization failure; version columns; PATCH/PUT semantics; idempotency; caches and content negotiation; multi-region consistency; domain state machines; and deterministic concurrency testing.

Before choosing a mechanism, retrieve the resource and representation identity, negotiated variants, current-state assumptions made by the client, invariant scope, acceptable concurrent histories, write set, database semantics, conflict frequency, merge policy, blind-write policy, conditional header requirements, concealment policy, response validator rules, server retry purity, region/read consistency, batch atomicity, and operational conflict metrics.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish transport preconditions, optimistic versions, locks, constraints, and isolation;
2. issue correct strong ETags for selected representations;
3. enforce `If-Match` and `If-None-Match` atomically with state changes;
4. select `428`, `412`, `409`, retry, merge, or concealment by failure meaning;
5. extend concurrency reasoning to PATCH, creates, deletes, batches, and workflows;
6. handle cache variants, authorization, side effects, and multi-region reads safely; and
7. test interleavings, conflict recovery, and validator correctness.

## Core Exposition

### Name the anomaly and protected assumption

Do not begin with “add an ETag.” Begin with the invariant and concurrent history. Common cases include:

- **lost update:** two clients replace state observed at the same version;
- **duplicate create:** two clients believe a named resource is absent;
- **check-then-act race:** capacity or balance changes between check and write;
- **invalid transition race:** two actors independently advance one workflow state;
- **write skew:** transactions update different rows after reading a shared predicate;
- **phantom:** a concurrent row changes the result of a predicate query; and
- **double ownership:** two workers claim the same task or lease.

A single-resource version protects assumptions summarized by that resource. It cannot protect “there are fewer than five active approvers across this tenant” unless the validator and atomic enforcement cover the set or a separate aggregate/counter owns that invariant.

Write down which observation the client relied on. For full replacement it is usually the selected representation. For an action endpoint it may be workflow state and version. For a create it is absence. For a batch it may be every item version plus collection membership.

### Treat entity tags as opaque representation validators

RFC 9110 defines an entity tag as an opaque validator for a selected representation. Clients echo it; they do not decode version numbers, timestamps, hashes, or storage topology from it.

A strong validator changes whenever representation data changes in a way material to strong comparison. A weak tag prefixed `W/` can support cache validation when representations are semantically equivalent despite byte differences, but `If-Match` uses strong comparison, so weak tags cannot satisfy it.

An internal monotonically increasing row version can contribute to an ETag, but the public value should be encoded opaquely and account for representation identity. If JSON and CSV variants have different representation data, do not emit the same strong tag merely because they came from one row version. Include representation/profile generation in the opaque construction or give each selected representation its own validator.

Cryptographic hashing of bytes is one option, not a requirement. Hashing can be expensive, can expose equality, and still fails if generated before all representation-dependent transformations. A version counter is efficient when every relevant change increments it. Never expose a database's internal transaction ID if wraparound, topology, or information leakage makes it unsuitable as a durable public validator.

### Use `If-Match` for update preconditions

A client GETs or otherwise receives a representation and its ETag, then sends the state-changing request with `If-Match`. The origin server evaluates the condition against the current selected representation using strong comparison just before the action. If none of the supplied tags matches, it normally returns `412 Precondition Failed` and performs no effect.

`If-Match: *` means the operation proceeds only if the origin server has a current representation of the target. It can protect “update/delete only if it exists,” but does not say the client observed a particular version.

Require `If-Match` for operations where blind overwrite is unsafe. RFC 6585 defines `428 Precondition Required` for a request that must be conditional and gives lost-update avoidance as its typical use. A missing required condition is `428`; a supplied condition that evaluates false is `412`. Explain how to obtain and resubmit a validator without revealing a concealed resource.

`If-Unmodified-Since` is a fallback where entity tags are unavailable, but HTTP dates have finite resolution and clock/last-modified semantics can miss rapid changes. Prefer strong ETags for precise write concurrency.

### Use `If-None-Match` for create-if-absent

`If-None-Match: *` on an unsafe method makes execution conditional on no current representation existing. It is useful for `PUT` to a client-chosen URI when the client intends create-only behavior. If a representation exists, the condition fails and non-GET/HEAD methods receive `412`.

Still enforce storage uniqueness. Two requests can evaluate absence concurrently unless condition evaluation and insertion share an atomic constraint/transaction. Map the unique collision back to the same failed-precondition semantics when it represents the exact `If-None-Match` race.

Do not confuse create-if-absent with idempotency. Repeating `PUT` with `If-None-Match: *` after a successful lost response will now fail the precondition; an idempotency key or recognition that the requested state already exists may provide better recovery. RFC 9110 allows limited success treatment when the server can determine the requested state-changing operation already succeeded, but use this only with reliable operation identity and avoid guessing between similar writers.

### Evaluate preconditions at the correct boundary

RFC 9110 requires normal request checks before received preconditions and evaluation just before processing the content/action. This prevents conditional headers from bypassing authentication, authorization, method, or request validity and reduces side-channel leakage.

The critical implementation shape is not:

1. select row and compare in application memory;
2. do unrelated work;
3. issue unconditional update.

Instead use an atomic conditional statement such as update where ID, tenant, and version all match; a locked row checked and changed in one transaction; or an isolation/constraint mechanism that rejects invalid concurrent histories. Zero affected rows needs safe disambiguation among absent, concealed, and stale according to authorization policy.

For field-level authorization, verify the requested patch and actor before applying. A stale response must not reveal a current version or field the caller may no longer observe. Reevaluate object/state authorization inside or bind it to the same protected version as the effect.

### Separate protocol and domain conflicts

Use failure categories consistently:

- **`428 Precondition Required`:** a required condition was absent.
- **`412 Precondition Failed`:** the supplied HTTP precondition evaluated false.
- **`409 Conflict`:** the request conflicts with current resource/domain state outside a false HTTP precondition, and the client may resolve it.
- **`404` concealment/absence:** the resource is absent or policy makes inaccessible and absent observationally equivalent.
- **server retry/internal transient outcome:** a serialization failure or deadlock may be replayed internally if safe; exhausted retries can become a documented temporary service failure.

A correct `If-Match` does not guarantee a domain action is legal. The resource may still be non-cancellable, quota may be exhausted, or a unique name may collide elsewhere. Return the stable domain conflict, not `412`, because the supplied representation precondition was true.

Conversely, do not return `409` just because “something changed” when an `If-Match` actually failed. Clients then cannot distinguish refresh/merge from a different business repair.

### Design PUT, PATCH, actions, and DELETE explicitly

For full replacement `PUT`, require the ETag of the selected current representation and validate that omitted fields mean replacement, not accidental deletion. Return the new ETag on success.

For JSON Merge Patch or JSON Patch, a precondition protects the base on which the patch was authored. Some operations are commutative or path-disjoint, but automatically applying a stale patch requires a proven merge rule. Array indices, moves, tests, and nested object replacement often depend on exact base state.

Action endpoints such as `/orders/{id}:cancel` can accept `If-Match` for the order representation or a documented action-version field. The server checks both the precondition and domain transition. Avoid inventing an ETag for an action response that does not correspond to the target representation.

DELETE can use `If-Match` so a caller does not delete a resource that changed since review. Repeating a successful DELETE is method-idempotent in intended effect, but a lost response plus stale condition may produce `404` or `412` according to current existence and contract. Idempotency records can preserve the original operation outcome when that distinction matters.

### Choose merge and conflict UX deliberately

Rejecting stale state is only half the user experience. Provide a safe way to fetch the current representation, compare it with the client's base and proposed changes, and resubmit with the new validator.

Three-way merge uses base, current server state, and client proposal. It can automatically combine disjoint fields but needs field semantics, ordering rules, deletion meaning, authorization, and conflict presentation. Never let a generic JSON merge decide domain invariants or hidden fields.

Server-side automatic replay can work for commands expressed as intent—“add label X if absent”—rather than replacement—“set labels to this stale complete array.” Design operations to be commutative or conditionally atomic when possible. A guarded increment or set-add can reduce conflicts, but still enforce caps and permissions.

Last-write-wins is valid only when explicitly acceptable. Record that choice and consider returning the current validator so clients understand state progression. Do not call silent overwrite optimistic concurrency control.

### Match database mechanisms to invariant scope

An optimistic version column protects one aggregate if every relevant write checks and advances it. Database constraints protect uniqueness and referential invariants. Atomic predicates protect counters and capacity. Row locks serialize known records. Serializable isolation rejects histories inconsistent with any serial execution, but can abort work that must be retried.

Snapshot or repeatable-read isolation does not universally prevent write skew; database behavior differs. PostgreSQL's current documentation, for example, distinguishes isolation phenomena and states that serialization anomalies remain possible below `SERIALIZABLE`. Retrieve the actual engine semantics rather than assuming names are portable.

For multi-row invariants, options include making one aggregate/version row own the predicate, locking the relevant key/range, using a materialized counter with a constraint, or using serializable transactions. An API ETag can represent the aggregate version, but the database still enforces it.

Internal serialization/deadlock retries rerun the entire request-scoped transaction from fresh reads. They differ from asking the client to merge a stale representation. Bound retries by deadline; do not repeat remote side effects; preserve the same idempotency identity.

### Address batches and multi-resource commands

A batch update needs an explicit condition model:

- one validator for an aggregate collection snapshot;
- one validator per item;
- a condition expression over a submitted version map; or
- unconditional items with documented partial conflict results.

Define atomicity. An all-or-nothing batch checks every condition before any effect and commits together. A partial batch returns per-item outcomes and does not claim a single ETag covers unrelated resources. Cap item count and avoid revealing hidden items through mismatch detail.

Cross-service workflows cannot share one HTTP ETag or local transaction. Each participant enforces its own version/state transition. The workflow carries expected versions or command identities and compensates/replans conflicts. Holding a database lock while waiting for another service or user is not a scalable distributed concurrency protocol.

### Keep validators coherent across caches and regions

ETags also serve cache validation, so representation generation and concurrency cannot be designed independently. Apply `Vary` and content negotiation correctly. Intermediaries may serve cached GETs, but origin servers evaluate `If-Match`; do not let a gateway compare stale cached validators for writes.

After a write, return or make retrievable the new validator. If a client is routed to a replica that has not observed the commit, it can read an older ETag and create false conflicts or regress its view. Use read-your-writes routing, consistency tokens, leader reads, or a documented staleness model for write-following reads.

In active-active regions, two regions cannot independently accept the same expected version without coordination unless the data type has a valid merge rule. A globally unique version label alone does not serialize effects. Define home-region, consensus, conditional storage, or conflict-resolution semantics.

### Test actual interleavings

Use barriers to make two requests read the same version, then control which reaches the compare-and-write. Assert one success, one `412`, no lost field, and correct new ETag. Repeat across nodes and regions under the supported consistency model.

Test missing, malformed, weak, multiple, wildcard, current, stale, and unauthorized validators; `If-None-Match: *` create races; DELETE after change; PATCH path conflicts; a correct precondition followed by domain conflict; and concealed target behavior. Verify RFC precondition precedence when multiple conditional fields appear.

Change every representation-relevant field and ensure strong ETag changes. Verify unchanged representation data does not accidentally churn if stability is promised. Test negotiated media types, encodings, profiles, localization, projections, and redaction so strong validators do not cross byte-different representations incorrectly.

Inject serialization failures and deadlocks and assert bounded whole-transaction retries without duplicate outbox/remote effects. Monitor conflict rate by operation and safe category, retry success, merge abandonment, lock time, and validator-generation errors without using raw ETags as metric labels.

The executable compare-and-set model below illustrates missing, current, stale, and create-only preconditions. It does not model HTTP parsing, representation variants, database isolation, or distributed coordination.

<!-- bijux-verify: {"id":"optimistic-concurrency-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"missing=428 precondition-required\nclient_a=200 value:1 version:2\nclient_b=412 stale current:2\ncreate=201 version:1\nduplicate_create=412 already-exists\n","stderr":""}} -->
```python
resource = {"value": 0, "version": 1}

def update(expected, value):
    if expected is None:
        return "428 precondition-required"
    if expected != resource["version"]:
        return f"412 stale current:{resource['version']}"
    resource["value"] = value
    resource["version"] += 1
    return f"200 value:{value} version:{resource['version']}"

created = {}
def create_if_absent(identity):
    if identity in created:
        return "412 already-exists"
    created[identity] = {"version": 1}
    return "201 version:1"

print("missing=" + update(None, 1))
print("client_a=" + update(1, 1))
print("client_b=" + update(1, 2))
print("create=" + create_if_absent("doc-9"))
print("duplicate_create=" + create_if_absent("doc-9"))
```

## Definitions and Notation

Let selected representation state be $(x,v)$, where $v$ is an opaque validator exposed to the client. Client proposal $g$ was formed from base $x$ observed at $v$. Atomic conditional transition $\operatorname{CAS}(v,g)$ commits $g(x)$ only if authoritative current version equals $v$.

A **strong validator** changes whenever representation data relevant to strong comparison changes. A **weak validator** indicates semantic equivalence suitable for weaker cache comparison and is marked `W/`; it cannot satisfy strong `If-Match` comparison. A **blind write** supplies no state precondition. A **merge** combines base, current, and proposed state under field/domain rules.

Let invariant scope $A$ be the set of facts a version summarizes. A successful version check proves freshness only for $A$ under the atomic enforcement boundary. **Write skew** involves individually valid writes to different facts whose combined history violates a shared predicate. **Read-your-writes** means a client can subsequently observe at least its committed version.

## Mechanisms, Invariants, or Proof Structure

1. Name the concurrent anomaly and exact client observation to protect.
2. Define resource, selected representation, variant, and invariant scope.
3. Generate an opaque strong validator from authoritative committed representation state.
4. Require the appropriate condition for unsafe blind writes where needed.
5. Perform normal request, authentication, authorization, and disclosure checks.
6. Evaluate the condition immediately before the action using RFC precedence.
7. Bind comparison and write atomically through version predicate, lock, constraint, or isolation.
8. Separate missing, false, concealed, domain, and internal serialization outcomes.
9. Return the new validator and a safe fetch/merge/retry path.
10. Test interleavings, variants, regions, batches, side effects, and operational conflict behavior.

The lost-update safety property applies only to state summarized by the validator and enforced by the atomic write. Passing selected interleaving tests does not prove all database histories serializable or all distributed participants conflict-free.

## Alternatives and Trade-Offs

Optimistic concurrency avoids long-held client locks and works well when conflicts are infrequent, but clients must refresh and merge. Pessimistic locking reduces conflicts inside a short server transaction but increases blocking and cannot safely span user think time.

Opaque version counters are cheap and stable when every relevant change advances them. Content hashes naturally track generated bytes but cost computation and depend on exact representation generation. Timestamps are familiar but can collide under clock/resolution limits. Choose by representation and enforcement properties.

Requiring `If-Match` prevents blind overwrite but adds a read round trip for clients without a validator. Action-oriented atomic commands can avoid a full representation read when intent is commutative or domain-guarded. Provide both only with clear semantics.

Automatic three-way merge reduces user conflicts but can combine changes that violate meaning or authorization. Manual merge is slower but preserves intent for sensitive documents. Field-specific merge policies sit between and require durable ownership.

Serializable isolation handles broad invariants without exposing every version but raises abort/retry cost. Explicit aggregate versions make conflicts visible to clients but can become hot spots. Constraints and atomic predicates are simpler for narrow invariants.

Strong cross-region coordination preserves one version order but increases latency and can reduce availability under partition. Home-region writes or convergent data types improve availability with narrower semantics. State the chosen consistency to clients.

## Failure Modes and Misconceptions

- **“ETag is just a hash.”** It is an opaque representation validator with strong/weak semantics.
- **“One row version covers the domain.”** It covers only the facts every relevant write advances.
- **“Compare in the handler, then update.”** The comparison and write must be atomic.
- **“Weak ETags work with If-Match.”** `If-Match` uses strong comparison.
- **“Timestamp means precise version.”** Resolution, clocks, and unchanged fields can make it unsafe.
- **“Missing and stale are both 412.”** Required-but-missing is `428`; false supplied precondition is `412`.
- **“Every conflict is 409.”** Protocol preconditions and domain conflicts have different recovery.
- **“Passing If-Match guarantees success.”** Domain rules, constraints, and authorization can still reject.
- **“412 means retry immediately.”** Fetch, compare, merge, and submit a new condition.
- **“PUT lost-response recovery is solved.”** Create/update recognition may still need idempotency identity.
- **“Serializable means no aborts.”** Abort and whole-transaction retry preserve serializability.
- **“Snapshot isolation prevents write skew everywhere.”** Retrieve the actual database guarantee.
- **“One collection ETag covers every batch item.”** Define the aggregate snapshot and atomicity explicitly.
- **“A global version string coordinates regions.”** Uniqueness is not conditional-write serialization.
- **“Locks can span user editing.”** Use optimistic versions across request/user time.

## Worked Examples

### Example 1

**Situation:** Two profile PUTs are based on version 8. **Reasoning:** The first atomic version predicate succeeds and creates version 9; the second affects zero rows and returns `412`. **Conclusion:** stale replacement cannot silently erase the first edit.

### Example 2

**Situation:** Client omits `If-Match` on a protected document update. **Reasoning:** The server requires conditional writes and returns `428` with safe instructions to GET an authorized validator. **Conclusion:** absence differs from a false condition.

### Example 3

**Situation:** Client uses `W/"catalog-7"` in `If-Match`. **Reasoning:** Weak tags do not match under the required strong comparison, so the precondition fails. Issue an appropriate strong representation ETag for write concurrency. **Conclusion:** cache equivalence is not write identity.

### Example 4

**Situation:** Two clients `PUT` a chosen URI with `If-None-Match: *`. **Reasoning:** A unique storage constraint arbitrates the absence race; one creates, the other receives `412` without overwrite. **Conclusion:** HTTP condition still needs atomic persistence enforcement.

### Example 5

**Situation:** Correct ETag accompanies cancellation of an already shipped order. **Reasoning:** The representation is current, so `If-Match` passes, but the domain transition is illegal. Return `409 order-not-cancellable`. **Conclusion:** freshness and business validity are independent.

### Example 6

**Situation:** Two JSON Patches change disjoint scalar fields from one base. **Reasoning:** A policy may reject the second conservatively or perform a verified three-way merge. It must not assume disjoint top-level paths imply no nested/domain conflict. **Conclusion:** merge is typed domain policy.

### Example 7

**Situation:** Two on-call assignments update different rows after both count one current assignee. **Reasoning:** Per-row versions pass yet the maximum-two invariant is violated. Lock/version an aggregate count, enforce an atomic predicate, or use serializable execution. **Conclusion:** write skew exceeds single-row ETags.

### Example 8

**Situation:** A success response returns old ETag after version advanced. **Reasoning:** The next client write falsely appears stale or overwrites from an incorrect base. Generate the response validator from committed new representation state. **Conclusion:** success must close the version loop.

### Example 9

**Situation:** After a write in region A, a GET from lagging region B returns the prior ETag. **Reasoning:** The client can regress and encounter false conflict. Route by consistency token/home region or serve a version at least as new as the commit. **Conclusion:** read topology affects API concurrency UX.

### Example 10

**Situation:** A batch contains one stale visible item and one concealed item. **Reasoning:** For atomic behavior, perform no writes and return only disclosure-safe conflict information; for partial behavior, identify outcomes by caller reference without exposing concealment. **Conclusion:** batch concurrency and authorization must compose.

## Cross-Program Connections

[Database Engineering](../../18-database-engineering/ROADMAP.md) supplies isolation phenomena, constraints, locks, versions, and serialization. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies consistency, coordination, partitions, and convergent alternatives. [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) supplies intent-preserving conflict and merge rules. [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies deterministic interleavings and model-based tests. This API module exposes current-state assumptions and recovery through HTTP.

## References

1. R. Fielding, M. Nottingham, and J. Reschke, [*RFC 9110: HTTP Semantics*](https://www.rfc-editor.org/rfc/rfc9110.html), especially Sections 8.8, 13, and 15.5.13, June 2022. Checked 2026-09-01.
2. M. Nottingham and R. Fielding, [*RFC 6585: Additional HTTP Status Codes*](https://www.rfc-editor.org/rfc/rfc6585.html), especially `428 Precondition Required`, April 2012. Checked 2026-09-01.
3. PostgreSQL Global Development Group, [*Transaction Isolation*](https://www.postgresql.org/docs/current/transaction-iso.html), PostgreSQL current documentation. Checked 2026-09-01.
4. Microsoft, [*Web API Implementation: Use ETags to Support Optimistic Concurrency*](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-implementation#use-etags-to-support-optimistic-concurrency), Azure Architecture Center. Checked 2026-09-01.
5. H. Berenson et al., [“A Critique of ANSI SQL Isolation Levels”](https://www.microsoft.com/en-us/research/publication/a-critique-of-ansi-sql-isolation-levels/), *Proceedings of SIGMOD*, 1995.

## Exercises

### Exercise 1

Design conditional GET, PUT, PATCH, and DELETE behavior for a negotiated document resource. Define strong ETag generation, required headers, status mapping, and successful response validators.

### Exercise 2

Analyze a tenant rule allowing at most five active API credentials when two requests create different credential rows concurrently. Explain why per-row ETags are insufficient and design atomic enforcement.

### Exercise 3

Diagnose an API that emits a weak timestamp ETag for JSON and CSV, compares it in middleware, issues an unconditional ORM save, returns `409` for missing/stale conditions, and retries a stale PUT automatically.

### Exercise 4

Design merge and authorization behavior when two users patch different visible fields but one also loses permission to observe a hidden field changed concurrently.

### Exercise 5

Create a verification campaign for an active-active multi-region batch update with per-item versions, atomic promise, idempotency keys, outbox events, replica lag, region partition, and concealed resources.

## Answers to the Exercises

### Answer 1

Generate a distinct opaque strong ETag for each selected byte-relevant representation/profile and return it on GET and every successful mutation representation. Conditional GET uses `If-None-Match` and can return `304`; writes use strong `If-Match`. Require the condition for blind-sensitive PUT/PATCH/DELETE: absent yields `428`, false yields `412`, concealed/absent follows authorization policy, and a passed condition can still yield a typed `409` domain conflict. Bind comparison to an atomic version predicate/transaction and increment every representation-relevant version. For PATCH, validator identifies the base; do not auto-merge without typed rules. DELETE uses the reviewed current version. Return the committed new ETag on update; do not reuse a strong tag across different JSON/CSV bytes.

### Answer 2

Each create targets a new row, so neither has an existing row ETag to conflict with; both can count four credentials and insert, producing six. Make the invariant owned by one tenant aggregate/counter row and conditionally increment only below five, lock the tenant's credential namespace/range, or run the predicate and inserts under database serializable isolation with bounded whole-transaction retry. A constraint on a materialized active-slot allocation can also enforce five unique slots. The API may expose the tenant credential-set version if clients need a precondition, but database enforcement remains authoritative. Exhausted capacity is a domain conflict; serialization abort is an internal replay candidate.

### Answer 3

Weak tags cannot satisfy `If-Match`; timestamps can miss rapid changes; one tag cannot be strong for byte-different JSON and CSV; middleware comparison races the unconditional save; missing required condition should be `428`; stale supplied condition should be `412`; and automatic stale PUT replay overwrites intent without merge. Generate opaque strong per-representation validators from an authoritative version, compare and advance in one guarded write, return the new tag, separate status categories, and require clients to fetch/merge/resubmit. Keep weak tags only for cache semantics where appropriate. Add simultaneous-write and representation-variant tests.

### Answer 4

Authenticate and authorize current target/fields before precondition detail. Treat the submitted ETag as the base of only the representation the user was allowed to observe. On mismatch, do not reveal the hidden field, its change, current full validator derivation, or another actor. Construct authorized base/current/proposed projections and apply typed field merge only to still-writable visible fields. If hidden state participates in a domain invariant, evaluate it internally and return a generic authorized conflict. If permission loss makes even the resource concealed, return the concealment outcome and no merge data. A successful merge writes against the current authoritative version and returns a new authorized-representation ETag.

### Answer 5

Define one authoritative coordinator/home or globally consistent conditional transaction capable of checking every visible submitted item version and committing all writes/outbox/idempotency outcome atomically; otherwise the atomic cross-region promise is unsupported. Use barriers to make same-version batches race in two regions, partition replication/coordination, and assert only one compatible commit or safe unavailability. Lose response after commit and replay the same idempotency key to the one batch outcome. Delay replicas and enforce read-your-writes/version monotonicity. Inject stale, absent, concealed, and domain-conflict items without revealing hidden existence. Crash before/after outbox and commit; assert no partial item state or events. Verify per-representation ETags, bounded whole-operation retries, stable event IDs, pool/lock recovery, and conflict metrics without raw validator labels.
