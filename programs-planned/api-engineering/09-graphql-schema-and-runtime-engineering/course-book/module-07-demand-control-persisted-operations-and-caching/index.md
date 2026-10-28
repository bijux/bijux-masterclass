# Demand Control, Persisted Operations, and Caching

**Module 07 of 10**

> **Governing question:** How can a client-shaped query language remain bounded under adversarial and accidental demand?

## Place in the program

Courses 1–8 established the contract, durable implementation, security, operations, performance, asynchronous events, typed RPC, and distributed ownership. Module 07 applies those guarantees to the graph interface; none are reset at the GraphQL boundary.

## Learning outcomes

- separate validity from affordability

- analyze aliases, fragments, and lists

- operate a trusted-document registry

- design authorization-aware caching

- reject overload truthfully

## Capstone result

Admit only bounded trusted operations and record cost evidence.

## Validity is not affordability

A valid operation can repeat an expensive field under many aliases, expand fragments, request the maximum list size at several levels, and trigger several remote services. Demand control begins before execution with document size, token, depth, alias, root-field, cost, and fan-out budgets.

No single metric is sufficient. Depth alone misses broad alias storms. Field count ignores list cardinality. Static cost misses runtime filter selectivity. The course combines conservative admission with runtime telemetry and source-service limits.

## Cost must follow executed occurrences

Aliases create distinct response entries and may execute a resolver repeatedly. Cost analysis counts each occurrence, not unique field names. Fragment spreads are expanded along executed paths; cyclic fragments are rejected. Inline fragments contribute cost when their type conditions can apply.

List fields multiply nested cost by an enforced cardinality. The analyzer uses the `first` variable when present and a default otherwise. Values above the schema policy are rejected before source calls.

## Trusted documents and APQ are different

A trusted document registry admits only operations reviewed for schema, cost, ownership, and client lifecycle. The client sends the SHA-256 digest of the exact UTF-8 document. Runtime variables remain validated and budgeted.

Automatic Persisted Queries primarily reduce request bytes by caching documents discovered at runtime. APQ is not automatically an allowlist and should not be described as a security control. A system may combine both mechanisms, but the policy names which one is active.

## Caching needs identity and source versions

GraphQL response caching is difficult because one response may depend on several services, permissions, variables, and source versions. A cache key must include operation identity, normalized variables, principal or authorization partition, schema version, and relevant representation variants. Invalidation must follow source ownership.

Request-scoped DataLoader caching is not response caching. It only collapses repeated keys during one operation and is safe to discard afterward.

## Overload remains truthful

Admission rejection is preferable to accepting a query that cannot complete within its deadline. The runtime returns a stable code such as `QUERY_BUDGET_EXCEEDED`; it does not silently drop selected fields. Per-client concurrency and cost budgets connect Course 5 traffic controls to GraphQL operation identity.

Persisted operations make traffic classification stronger because each operation has an owner and known shape. Unknown operations can be rejected in production while a development environment permits exploration under stricter limits.

## A valid operation can still be hostile demand

GraphQL validation answers whether a document is legal for the schema. It does not answer whether the operation is affordable for this service, client, tenant, or moment. An operation can be shallow but wide, deeply nested but cheap, or use aliases and fragments to repeat an expensive field many times.

Demand control therefore occurs after standard validation and variable coercion but before source execution. The admission decision uses the selected operation, expanded fragments, actual coerced cardinality variables, field weights, service fan-out, client trust, and current traffic policy.

Rejected demand must produce zero source-service calls. This is a non-negotiable proof because a cost calculator that runs after partial execution does not protect anything.

## Cost is based on field occurrences

A field name appearing once in SDL can execute many times in one response. Cost follows occurrences in the expanded operation and estimated parent cardinality.

A simplified course model is:

```text
field cost = base weight
           × parent cardinality
           × declared list multiplier
           × occurrence count

operation cost = sum(field costs)
               + service fan-out penalty
               + depth/alias policy adjustments
```

This is not a universal GraphQL standard. It is a versioned operational profile. Its value is predictability and falsifiability. The profile states which fields have base weights, which arguments are multipliers, how defaults and variables are read, how fragments and aliases expand, and what happens when a variable is unknown.

For example, `analysisRuns(first: 50) { edges { node { artifacts { ... } } } }` incurs the run connection multiplier and an artifact-source penalty. Repeating `artifacts` under five aliases produces five occurrences unless the executor can prove and govern safe deduplication. Admission should not assume resolver caching will make repeated demand free.

## Depth is only one signal

A depth limit catches pathological recursion-like shapes but misses broad expensive queries. An alias limit catches repeated sibling work but misses one huge list. A page-size limit catches one cardinality source but misses nested products. A service fan-out limit catches architecture amplification but not expensive local computation.

Use a portfolio of bounded rules:

- maximum document bytes and token count;
- maximum operation count and fragment count;
- maximum depth;
- maximum aliases and repeated coordinates;
- maximum page size and nested cardinality product;
- maximum total cost;
- maximum distinct downstream services;
- maximum synchronous dependency depth;
- trusted-operation policy by client.

The values come from Course 5 workload evidence and Course 4 reliability budgets. They are not arbitrary “best practices.”

## Trusted documents, APQ, and registration

A persisted-operation hash proves document identity only when the registry binds the hash to exact normalized bytes. A trusted-document policy additionally binds it to client, schema release, cost, and lifecycle state.

Registration is a release action, not an anonymous runtime feature:

1. client submits a named document in source control;
2. CI validates it against the candidate schema;
3. admission cost and service fan-out are computed;
4. field authorization and data-class review run;
5. the document is registered for named client releases;
6. runtime requests send the digest and variables;
7. unknown digests fail without accepting arbitrary text.

Development and privileged tools may use arbitrary documents under separate limits. Public clients use the trusted registry. This distinction preserves the interactive strengths of GraphQL without making the production endpoint accept unreviewed programs from every caller.

## Caching without violating identity or correctness

GraphQL caching is not one mechanism. Separate:

- parsed-document cache;
- validation and execution-plan cache;
- request-scoped loader cache;
- source-service or application cache;
- response cache;
- client normalized cache.

Each has different keys and invalidation rules. A parsed-document cache can be keyed by schema release and document digest. A request loader must include tenant and authorization dimensions. A response cache must include operation digest, canonical variables, principal or audience class, source versions, and consistency profile. Caching by raw URL or operation name alone is unsafe.

Mutations and subscriptions change cache assumptions. A client normalized cache can merge nodes by global ID, but the server cannot assume that fixes stale source data. A mutation result should return enough authoritative state or invalidation metadata for clients to reconcile.

Do not cache partial errors as successful complete responses without an explicit policy. A cached `artifacts: null` caused by a temporary outage can outlive the failure and mislead clients. The cache record must preserve completeness and source-version semantics.

## Overload and truthful rejection

Course 5 introduced traffic control; GraphQL adds operation-specific demand. Admission can reject before execution with a stable code, retry guidance when meaningful, and an operation identity for telemetry. Under severe overload, the host may reject before parsing arbitrary documents while still permitting a small set of critical trusted operations.

Do not “degrade” by silently dropping selected fields or reducing page sizes. The response would no longer match the requested program. Valid degradation follows declared schema semantics: nullable remote fields may fail with path errors, a stale projection may be returned with age metadata, or the whole operation may be rejected.

Rate limits and cost budgets must be charged consistently. A tenant should not evade limits by splitting one expensive operation into many cheap-looking aliases, nor should an invalid document consume the same source budget as executed work. The policy defines whether rejected admission consumes a smaller control-plane budget to resist validation abuse.

## Worked admission example

A mobile client sends a registered `GetProjectOverview` operation with `first=20`. The registry confirms client and document identity. Standard validation passes. Cost evaluation expands fragments, reads the coerced page size, counts artifact and delivery fields, and predicts two downstream services. The total fits the client's budget, so execution begins.

An untrusted tool sends the same shape with `first=500`, repeats artifacts under aliases, and adds a broad search. Standard validation can still pass. Admission rejects it before any source call. The proof report records rule IDs and bounded totals, not the full sensitive document.

## Demand-control review checklist

Verify that:

- calculations use the selected operation and coerced variables;
- fragments and aliases cannot hide occurrences;
- every list has a declared bound;
- nested cardinality is considered;
- service fan-out and dependency depth enter policy;
- unknown persisted digests cannot self-register on the trusted endpoint;
- cache keys include schema, document, variables, tenant, policy, and source version as required;
- partial responses are never cached as complete by accident;
- rejected demand makes zero source calls;
- policy changes are versioned and replayable against active operations.

## Worked capstone review

An alias storm repeats one nested field forty times. A naïve analyzer counts one field name and admits it. The course analyzer counts executed occurrences and rejects the operation before any service call. A trusted operation can still be rejected when runtime `first` exceeds one hundred.

## Python and TypeScript implications

Both tracks parse the course operation subset and produce the same budget outcomes. Complete framework adapters must also run standard GraphQL validation before the course-specific admission rules.

## Evidence required before the next module

Complete the lab and checkpoint. The decisive artifact is the module report under `reports/module-07-*.json`; prose claims without its oracle do not pass.
