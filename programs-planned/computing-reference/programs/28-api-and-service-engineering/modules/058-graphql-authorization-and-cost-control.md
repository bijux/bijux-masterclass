---
module_id: API-058
program: API & Service Engineering
level: 2
module_number: 58
title: GraphQL Authorization and Cost Control
status: complete
last_verified: 2026-09-02
---

# GraphQL Authorization and Cost Control

## One-Page Review

### Governing question

How should a GraphQL service authorize every selected capability and bound the work graph before and during execution without trusting opaque IDs, query shape alone, gateway placement, persisted documents, or cost estimates as security proofs?

### Essential definitions

- **authentication** establishes a caller identity and credential properties; **authorization** decides whether an actor may perform an action on a resource under context.
- An **object-level decision** controls access to a particular resource instance; a **field-level decision** controls a capability or sensitive property; a **relationship decision** controls traversal from one resource to another.
- **policy enforcement point (PEP)** obtains and enforces a decision; a **policy decision point (PDP)** evaluates governed policy and attributes.
- **deny by default** means access exists only through an explicit applicable allow rule.
- **existence-hiding** intentionally makes forbidden resources observationally resemble absent resources under a defined threat model.
- **operation depth** is the longest relevant selection path; **breadth** counts sibling/alias/fragment-expanded selections; **list depth** counts nested list multipliers.
- A **static cost estimate** assigns conservative weights and cardinality multipliers to a normalized validated operation before execution.
- A **runtime budget** caps observed work such as resolver invocations, rows, bytes, dependency calls, CPU, memory, concurrency, and time.
- A **trusted document** is a server-approved operation identified through a manifest-bound identifier; it is not automatically authorized or cheap.
- **semantic rate limiting** charges an identity/tenant/client according to work or sensitive actions rather than HTTP request count alone.

### Central model, mechanism, or theorem

Authorization is a predicate over explicit state:

$$
Allow(a,action,r,c,p)=true,
$$

where $a$ is authenticated actor, $r$ resolved resource, $c$ request/domain context, and $p$ policy version. Possessing an ID, selecting a schema field, or passing a gateway is not an allow decision.

For selection node $v$ with field weight $w_v$, bounded cardinality multiplier $m_v$, and selected children $ch(v)$, a conservative recursive estimator can use

$$
C(v)=w_v+m_v\sum_{u\in ch(v)}C(u).
$$

Admit only when normalized-operation structural gates pass and $C(O)\le B_{static}$. Continue enforcing $B_{runtime}$ because estimates can be wrong and actual backends vary.

### Critical invariants

Authentication runs once at a trusted boundary and produces immutable request identity; authorization remains resource/action specific. Domain/application services own authoritative policy so every API, batch loader, background path, and subgraph obtains the same decision. Resolvers invoke those boundaries and never infer permission from selection, role text, object ID, parent visibility, or cached data. Direct `node` lookup, nested traversal, edges and nodes, mutations, subscriptions, introspection, aliases, and batch loads follow explicit policy. Cache/loader keys never cross visibility contexts. Denials have stable non-leaking error/null semantics and protected audit evidence.

Before execution, documents are size/token/definition/fragment/depth/breadth/alias/list/cardinality/cost bounded after parsing, validation, directive evaluation assumptions, fragment expansion, and field collection semantics. Page arguments have enforced maxima; omitted/default/variable values are included in cost. HTTP request count, batched operations, aliases, and one-operation fan-out are charged to the same principal/tenant budgets. Trusted documents bind exact canonical operations, client/environment, schema compatibility, and lifecycle. Runtime deadlines, concurrency, rows/bytes/calls, cancellation, and isolation remain mandatory. Cost predictions are calibrated against measured work and fail safely when metadata or variables are unknown.

### Common failures

Treating authentication as authorization; trusting an ID because it is opaque; checking a parent but not a nested resource; authorizing connection edges but exposing nodes through `node(id:)`; field annotations with no runtime enforcement; authorization only at the gateway; subgraphs callable directly; process-global loaders; policy decisions cached without actor/resource/action/policy version; returning different forbidden/absent errors that enable enumeration; masking denials into null inconsistently; debug stack traces; introspection policy used as primary security; depth-only limits; counting raw syntax without fragments/aliases; list multipliers based on caller values without caps; assigning every field cost one; ignoring defaults and custom scalars; cost checks after resolver work starts; HTTP rate limits bypassed with batching/aliases; trusted documents accepted across clients/environments or after manifest deletion; persisted documents assumed safe forever; timeouts without cancellation; unlimited incremental patches; and cost models never compared with dependency calls, bytes, CPU, or tail latency.

### Compact example

A query asks for 50 projects, each with 100 members and a salary field. The actor may view only 8 projects and no salaries. Authorization is pushed into project eligibility, membership traversal is reauthorized, and salary is denied at its domain capability. Static cost uses enforced maxima, not observed authorized count: `projects` multiplier 50 and `members` multiplier 100. If cost exceeds the actor's budget, reject before execution; otherwise runtime row/call/deadline budgets still apply. **Conclusion:** authorization limits permission; admission limits requested work; neither substitutes for the other.

### Connections

[GraphQL Schema Design](055-graphql-schema-design.md) defines capabilities, [GraphQL Execution, Resolvers, and Batching](056-graphql-execution-resolvers-and-batching.md) creates the work graph, and [GraphQL Pagination and Incremental Delivery](057-graphql-pagination-and-incremental-delivery.md) bounds collections and response lifecycle. [Authorization Checks](034-authorization-checks.md) and [Rate Limits and Quotas](039-rate-limits-and-quotas.md) supply transport-independent foundations.

## Governing Question

For every selected response position or mutation effect, which trusted component proves the actor–action–resource decision, and which pre-execution and runtime mechanisms ensure the authorized operation cannot consume disproportionate shared resources?

## Why This Matters

GraphQL exposes a connected capability graph. A caller can reach the same object through a root lookup, nested edge, search result, union, batch, mutation payload, subscription event, or globally identified node. One missing authorization path is enough for disclosure or effect. Schema visibility and opaque IDs reduce convenience for attackers but do not decide access.

The same flexibility creates asymmetric work. A small document can traverse cycles, multiply nested lists, repeat expensive fields through aliases, or bundle many operations/object lookups into one HTTP exchange. A gateway counting requests may see one call while databases and services receive thousands. Authorization may reduce returned data but cannot be the capacity plan: even denied lookups can be expensive, and cost admission must not depend on secret visibility facts.

Static complexity analysis is therefore a safety estimate, not prediction truth. It can reject clearly excessive operations before work begins, while runtime budgets handle data skew, cache misses, retries, inefficient resolvers, and changing dependencies. Trusted documents reduce arbitrary query surface but still need authorization, lifecycle, cost review, and runtime controls.

## Prerequisites and Retrieval

Retrieve [Authorization Checks](034-authorization-checks.md), [Rate Limits and Quotas](039-rate-limits-and-quotas.md), [API Threat Modeling](041-api-threat-modeling.md), [GraphQL Schema Design](055-graphql-schema-design.md), [GraphQL Execution, Resolvers, and Batching](056-graphql-execution-resolvers-and-batching.md), and [GraphQL Pagination and Incremental Delivery](057-graphql-pagination-and-incremental-delivery.md). Be able to distinguish identity from policy, schema coordinate from response path, validation from execution, request count from work, and static upper bound from observed cost.

## Learning Objectives

After completing this module, you can:

1. place object-, field-, relationship-, and action-level authorization at durable domain boundaries;
2. specify deny/absence/error and auditing behavior without creating avoidable side channels;
3. preserve authorization through loaders, caches, federation, mutations, subscriptions, and direct-node access;
4. normalize an operation for depth, breadth, alias, fragment, list, and cardinality analysis;
5. derive and explain a weighted recursive cost estimate with safe argument bounds;
6. combine static admission, runtime budgets, timeouts, concurrency limits, and semantic quotas;
7. design trusted-document registration, binding, rotation, revocation, and fallback policy;
8. govern introspection and developer tooling according to exposure rather than obscurity; and
9. verify policy completeness and cost calibration adversarially.

## Core Exposition

### Separate identity establishment from authorization

Authenticate at the transport/application entry using supported credential mechanisms. Create an immutable request identity containing verified subject, issuer/audience, tenant/delegation, credential strength, and relevant expiry—not raw token claims copied blindly. Anonymous is an explicit identity class.

Authorization then evaluates actor, action, resolved resource, and context. A role is one attribute, not a universal decision. Relationship, ownership, tenancy, resource state, purpose, location, time, consent, and policy version may matter. Deny when required facts are missing or ambiguous.

Resolvers should not each reinvent rules. Domain/application operations such as `viewInvoice`, `listProjectMembers`, `approveClaim`, or `readSalary` own the decision close to invariant/data access. The GraphQL resolver is a PEP that invokes the boundary and maps its result. The same service remains protected when invoked by REST, jobs, loaders, subgraphs, or tests.

### Authorize every reachable capability

Inventory schema coordinates and reachability. Root queries, `node`/`nodes`, search, nested relationships, interfaces/unions, connection edges/nodes, computed fields, mutation inputs/payloads, subscriptions, and deprecated aliases can reach the same domain facts.

Object authorization asks whether this actor can act on this resource. Field authorization asks whether a property/capability is visible even on an allowed object. Relationship authorization asks whether traversal itself is allowed; parent visibility does not imply every child. Mutation authorization covers both action and requested state transition, not just access to the mutation name.

Push tenant/visibility predicates into data selection so hidden rows do not influence pagination/counts or consume needless work. Still authorize each materialized resource at the trusted boundary; filters can be misconfigured, queries can change, and direct loaders can bypass them.

Opaque/global IDs require resolution then authorization. Never decode a type/tenant prefix and treat it as permission. Prevent cross-type substitution and verify expected resource kind. An ID's guessability affects enumeration risk, not authorization correctness.

### Define denial and existence-hiding deliberately

A public lookup may return null for both absent and forbidden to reduce resource enumeration. This works only if status/error messages, response time, cache behavior, total counts, page density, sibling fields, audit/logs, and mutation behavior do not expose the distinction. Internal clients may instead receive a stable forbidden code when product needs it.

GraphQL execution errors include paths; messages/extensions must be stable and redacted. Do not expose policy rule names, roles, SQL, stack traces, resource attributes, or “user exists but belongs to tenant X.” Protected audit logs record actor, action, resource reference, policy version, decision/reason class, correlation, and outcome without tokens or excessive sensitive data.

Field-level denial can be null only if the schema permits it and null semantics are documented. A non-null sensitive field cannot be silently hidden without bubbling data away. Prefer schema/domain shapes that reflect legitimate partial visibility, but do not manufacture role-specific duplicate schemas casually.

### Keep loaders and caches inside authorization scope

A process-global loader keyed only by raw ID can return an authorized result from actor A to actor B. Construct request-scoped loaders after authentication or include the complete visibility context—tenant, actor/policy equivalence, action, policy version, snapshot, projection—in a governed key. Reauthorize resolved resources.

Batch policy decisions must return one aligned decision per actor/action/resource input. Do not authorize the batch container once and infer every item. Missing, denied, and dependency-error slots follow the field's leakage policy. Avoid caching transient PDP errors as denial/absence unless policy explicitly fails closed for the request only.

Shared caches store only data with a declared visibility class and authorization-on-read. Cache invalidation includes policy/relationship change, not merely resource mutation. Negative authorization caches require short bounded lifetimes and policy-version keys.

### Preserve policy through federation and background execution

A gateway can reject operations and propagate authenticated context, but a subgraph/domain service remains an enforcement boundary if reachable through any other path or if gateway plans evolve. Authenticate service identity, validate signed/delegated end-user context, bind audience, and authorize in the owning service. Never trust arbitrary identity headers.

Federated entity resolution is direct object lookup and requires policy. Composition directives/metadata can describe policy, but runtime enforcement and failure behavior must be tested. Prevent one subgraph from receiving fields/identifiers it does not need.

Subscriptions authorize when establishing the source and when delivering each event if membership/policy can change. Durable/background work records the initiating identity, delegated authority, policy/action, and reauthorization rules; it must not keep an expired request object as implicit permission.

### Normalize operation shape before cost analysis

Parse and validate before ordinary execution, but bound raw bytes/tokens/definitions/fragments early to protect parsing/validation. Select the named operation; resolve variables/defaults; account for `@skip`/`@include` conservatively when values are unknown; expand fragments safely with cycle validation; group compatible selections so syntactic duplicates are not naively double-charged; and retain aliases as separate response positions when they vary arguments.

Track maximum selection depth, list depth, self-reference depth, breadth, aliases, root fields, fragment spreads/definitions, variable/input sizes, and response-size estimates. Depth alone misses a shallow query with thousands of aliases. Breadth alone misses nested list multiplication. Limit validation errors/work so intentionally invalid documents cannot consume unbounded diagnostics.

Introspection has different legitimate depth patterns and may use separate authenticated tooling budgets. Do not exempt it from bounds.

### Assign weights and cardinality multipliers

Give each field a baseline weight reflecting resolver/dependency/serialization risk, not business sensitivity. Leaf fields already present on a parent may be cheap; search, aggregation, remote fan-out, cryptography, file URLs, and unindexed filters cost more. Use schema coordinates and version-controlled metadata owned with the resolver.

For list/connection children, multiply by an enforced cardinality bound derived from validated variables/defaults and capped by server maximum. If no safe bound exists, reject or use the maximum, never assume one. Nested lists multiply. Add separate dimensions when one scalar score hides constraints: CPU, database rows, external calls, bytes, and concurrency.

For node $v$, the teaching model $C(v)=w_v+m_v\sum C(child)$ is conservative only when weights/multipliers upper-bound implementation behavior. Shared loaders may reduce calls but should not make admission depend on cache hits. Aliases with different IDs remain distinct work. Fragments collected to the same response field should match executor semantics.

<!-- bijux-verify: {"id":"graphql-static-cost","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"cheap_query=3\nnested_lists=61\nadmit_cheap=True\nadmit_nested=False\n","stderr":""}} -->
```python
def estimate(node):
    children = sum(estimate(child) for child in node.get("children", []))
    return node["weight"] + node.get("multiplier", 1) * children

cheap = {"weight": 1, "children": [{"weight": 1}, {"weight": 1}]}
nested = {
    "weight": 1,
    "multiplier": 5,
    "children": [
        {"weight": 1},
        {"weight": 1, "multiplier": 10, "children": [{"weight": 1}]},
    ],
}
budget = 50
print("cheap_query=" + str(estimate(cheap)))
print("nested_lists=" + str(estimate(nested)))
print("admit_cheap=" + str(estimate(cheap) <= budget))
print("admit_nested=" + str(estimate(nested) <= budget))
```

The model exposes multiplication; a production analyzer must understand its GraphQL implementation, schema wrappers, directives, fragments, variables, abstract types, incremental selections, and operation batching.

### Admit before execution and enforce runtime budgets

After authentication and cheap structural validation, compute cost under the principal/client/tenant policy. Reject over-budget operations before resolvers, transactions, or dependency work. Return a stable error with safe high-level limits; detailed field weights can help trusted developers but may aid probing.

Static admission cannot foresee database skew, cold caches, retries, downstream latency, resolver regressions, or policy filtering. Runtime context therefore tracks deadline, resolver/dependency calls, rows/items, response bytes, CPU/memory where feasible, concurrent branches, and incremental patch lifecycle. Stop scheduling new work when exhausted, cancel children cooperatively, and release resources. A timeout that leaves downstream work running is not a complete control.

Use bulkheads/queues/pool limits and OS/container limits as final containment. One expensive accepted operation must not monopolize shared dependencies. Apply per-field/page maxima independently of total cost.

### Charge quotas by work and sensitive action

Rate limit by authenticated actor, tenant, client/application, and anonymous network signals as appropriate. HTTP request count is insufficient because one request can contain many operations, aliases, node lookups, or a large work graph. Charge estimated/actual cost tokens and separately rate-limit sensitive actions such as login, password reset, invitation, export, or OTP verification.

Decide reservation/refund semantics: reserve estimated cost before execution, charge actual under a floor/ceiling after, and never let repeated failures bypass charges. Distributed counters have consistency/availability trade-offs; local emergency shedding still protects instances. Return policy-safe retry information.

HTTP batching, if supported, has maximum operations/body/cost and each operation is authorized/admitted. GraphQL aliases are not transport batching but can perform similar enumeration; object/action counters catch both.

### Govern trusted documents rather than trusting hashes

A trusted-document system maps an opaque identifier to exact server-approved canonical document plus allowed operation name, client/application, environment, schema compatibility, owner, cost class/override, expiry, and status. Registration occurs through authenticated build/deployment governance, not arbitrary runtime upload by public callers.

Reject unknown IDs and mismatched accompanying text. Prevent hash collision/substitution using an approved digest or random server ID and exact document comparison. Bind manifests to release/environment; stage additions before client rollout and retain old entries through client adoption. Revoke compromised/abusive documents and audit use.

Trusted documents reduce arbitrary shape and can cache parsing/cost decisions. They do not authorize current actors/resources, validate variables/domain state, prevent excessive repetition, or remain safe after resolver/schema cost changes. Recompute/approve on relevant changes and retain runtime budgets/rates.

### Choose an introspection and tooling policy

Introspection is a specified GraphQL capability and valuable for public APIs, tooling, accessibility, and governance. Hiding it does not fix exposed fields: attackers can guess and validation suggestions may disclose names. Decide by intended audience and threat model.

Public developer APIs may expose bounded introspection intentionally. Private graphs may restrict it to authenticated developer/tool identities or trusted documents. Disable interactive IDEs/debug modes in production unless explicitly authenticated/needed. Treat schema descriptions/deprecations/directives as information disclosure and review them.

Whether enabled or disabled, enforce authorization, cost/depth/list/fragment limits, error redaction, and monitoring. Avoid per-user dynamically filtered schemas unless composition/caching/type correctness and leakage are fully governed; field policy at execution is generally clearer.

### Calibrate and verify cost controls

Log predicted cost with bounded operation identity, schema version, admitted/rejected outcome, actual resolver/dependency calls, rows/items, bytes, duration, CPU/memory samples, cache/batch behavior, cancellation, and errors. Do not log raw variables/tokens/sensitive documents. Compare distributions by coordinate/client and investigate underestimation.

Use representative registered operations plus generated adversarial documents: deep cycles, wide aliases, repeated fragments, nested max lists, omitted/default/variable sizes, abstract types, introspection, multiple operations, HTTP batches, incremental directives, and invalid-document floods. Assert analyzer and executor agree on selection semantics.

Authorization tests form an actor × action × resource-state × reachability-path matrix. Include cross-tenant equal IDs, direct/nested/node/search/edge/payload/subscription paths, relationship/policy changes, cache hits, batch order, federation bypass, confused deputy, and denial side channels. Mutation tests verify both permission and state transition/effect.

## Definitions and Notation

Let actor $a$, action $x$, resource $r$, context $c$, policy version $p$, and decision $A(a,x,r,c,p)\in\{allow,deny\}$. Let validated normalized operation $O$ have selection nodes $V$, field weight $w_v\ge0$, multiplier $m_v\ge1$, and children $ch(v)$. Let $C(O)$ be the sum/recursive estimate over root nodes.

Let $B_s(a,client,tenant)$ be static admission budget; $B_r$ a vector of runtime limits; $Q$ a quota balance over a window; and observed work $W=(calls,rows,bytes,cpu,time,concurrency,patches)$. A trusted document record $D=(id,text,operation,client,environment,schema,owner,cost,lifecycle)$.

Security requires authorization independently at every effect/disclosure boundary and admission $C(O)\le B_s$ before execution. Availability additionally requires $W\preceq B_r$ and quota charge under $Q$; none of these implications runs backward to prove authorization.

## Mechanisms, Invariants, or Proof Structure

Possession of identifier cannot imply authorization: construct two authenticated actors with the same syntactically valid resource ID but different tenant/relationship. If ID possession allowed both, one receives an unauthorized resource. Therefore resolve identity then evaluate actor–action–resource context.

Parent authorization cannot imply child authorization when relationship targets have independent policy. A visible project can reference a confidential member profile. An explicit traversal/resource decision is necessary unless a proven domain invariant establishes identical visibility.

Depth limits do not bound breadth: a depth-two operation can contain $n$ aliases. Breadth limits do not bound nested list multiplication: two list fields bounded by $m$ can expose $m^2$ child positions. Thus structural gates and weighted cardinality cost are complementary.

Static estimates cannot guarantee runtime bounds because identical operation/schema values can execute under different data cardinality, cache state, dependency behavior, and retries. Runtime controls are logically independent containment. Trusted-document membership fixes text, not actor/resource state or implementation cost, so it implies neither authorization nor bounded execution by itself.

## Alternatives and Trade-Offs

Resolver-local policy is close to fields but duplicates rules and misses non-GraphQL paths. Central domain policy is durable but resolvers must invoke/map it correctly. Gateway policy rejects early but cannot safely be the only boundary. Use layered enforcement with one semantic owner.

RBAC is simple for coarse capabilities; attribute/relationship-based policy expresses tenant, ownership, consent, and state but needs governed data and explainability. Avoid embedding a general policy language in GraphQL arguments/directives.

Null-for-forbidden reduces some enumeration but blurs diagnostics and may still leak through timing/counts. Explicit forbidden errors aid trusted clients but disclose existence. Choose consistently by field/threat model and test all channels.

Depth/breadth limits are cheap and understandable; weighted cost models reflect work better but require metadata/calibration. Trusted documents offer strongest arbitrary-shape restriction but complicate client rollout and public exploration. Combine based on exposure rather than selecting one silver bullet.

Introspection enables ecosystem tooling; restricting it reduces convenient reconnaissance and sensitive descriptions. It never replaces authorization. Static budgets reject early; runtime budgets contain estimator error but spend some resources. Both are necessary for exposed flexible graphs.

## Failure Modes and Misconceptions

- **“Authenticated means authorized.”** Identity is input to a resource/action decision, not its outcome.
- **“The parent was allowed, so every child is allowed.”** Relationships and sensitive fields can have independent policy.
- **“Opaque IDs prevent BOLA/IDOR.”** Guessability changes; permission still requires server evaluation.
- **“Authorization middleware covers the graph.”** Direct node, nested, batch, federation, subscription, and background paths must reach the semantic boundary.
- **“Null hides existence.”** Timing, counts, page density, errors, caches, and logs can still distinguish states.
- **“Depth limiting stops expensive queries.”** Wide aliases and nested list multipliers evade a depth-only gate.
- **“Cost one per field is objective.”** Resolver/data/dependency behavior and cardinality vary; weights require ownership and calibration.
- **“A high timeout is a cost limit.”** Work can saturate resources before timeout and continue after client termination.
- **“One HTTP request consumes one rate token.”** Batches, aliases, and one work graph can contain many sensitive actions.
- **“Persisted means trusted, authorized, and cheap.”** A document is text under lifecycle governance; actor/resource/variables/runtime still change.
- **“Disabling introspection secures the API.”** It hides convenient schema discovery, not exposed capabilities or guessed fields.
- **“Gateway enforcement protects subgraphs.”** Direct/replanned/confused-deputy paths require owner-side authorization.

## Worked Examples

### Example 1

**Situation:** User A guesses user B's opaque node ID. **Reasoning:** resolver resolves the node, verifies expected type, then domain policy denies view under A's tenant/relationship; response follows existence policy. **Conclusion:** IDs locate candidates, not permission.

### Example 2

**Situation:** Actor can view a project but not contractor compensation. **Reasoning:** `Project.members` authorizes traversal and each member; `Member.compensation` invokes a separate capability. Parent allow does not flow automatically. **Conclusion:** authorize at semantic granularity.

### Example 3

**Situation:** Global loader caches employee 7 for HR, then serves manager context. **Reasoning:** raw-ID cache crossed visibility policy. Use request-scoped/policy-keyed loader and authorize-on-read. **Conclusion:** cache scope is an authorization boundary.

### Example 4

**Situation:** A depth-two operation has 10,000 aliased `user(id:)` fields. **Reasoning:** depth gate passes while enumeration and backend work explode. Bound aliases/root fields/breadth, estimate each distinct argument load, and charge object requests. **Conclusion:** depth is one dimension.

### Example 5

**Situation:** `projects(first:50){members(first:100){name}}`. **Reasoning:** nested potential is 5,000 member positions plus parents/leaves, regardless of small syntax. Enforce maxima and multiply child cost. **Conclusion:** list cardinality drives cost.

### Example 6

**Situation:** Static cost 40 is admitted under budget 50, but a resolver scans a million rows. **Reasoning:** model metadata/query plan is wrong. Runtime row/time/cancellation budget stops work; telemetry triggers recalibration/index repair. **Conclusion:** admission needs containment.

### Example 7

**Situation:** Ten password-reset mutations are aliased in one operation. **Reasoning:** gateway sees one HTTP request. Mutation/action quota charges ten attempts and may forbid repeated sensitive aliases. **Conclusion:** rate limiting follows semantics.

### Example 8

**Situation:** Trusted mobile operation becomes expensive after resolver migration. **Reasoning:** unchanged hash no longer proves reviewed cost. Recalculate at schema/resolver release, canary, enforce runtime budget, and revoke/override if necessary. **Conclusion:** trust has lifecycle.

### Example 9

**Situation:** Gateway authorizes salary field, but subgraph accepts direct internal calls. **Reasoning:** compromised/misrouted workload bypasses gateway. Subgraph validates service/delegated identity and enforces salary domain policy. **Conclusion:** owner boundary remains authoritative.

### Example 10

**Situation:** Introspection is disabled but validation says “Did you mean secretPayroll?”. **Reasoning:** discovery remains possible and payroll resolver still needs authorization. Govern suggestion/error disclosure while enforcing policy/cost. **Conclusion:** obscurity is not control.

## Cross-Program Connections

- **Security Engineering:** BOLA/BFLA, least privilege, deny-default, relationship policy, confused deputies, side channels, and audit shape enforcement.
- **Algorithms and Compilers:** parsing, fragment expansion, field collection, graph traversal, and abstract interpretation implement static cost analysis.
- **Distributed Systems Engineering:** gateway/subgraph trust, policy propagation/versioning, partial failure, quotas, and cancellation constrain enforcement.
- **Performance Engineering:** cardinality, queues, bulkheads, cost calibration, and predicted-versus-observed work protect capacity.
- **Database Engineering:** row-level predicates, indexes, query plans, counts, scans, and transaction state determine actual work and leakage.
- **Product/Client Engineering:** trusted-document manifests, rollout windows, developer tooling, and stable denial UX make controls usable.

## References

1. GraphQL Foundation, “GraphQL Specification, September 2025,” validation, field collection, execution, introspection, response errors, and type behavior, verified 2026-09-02. [GraphQL specification](https://spec.graphql.org/September2025/).
2. GraphQL Foundation, “Authorization,” official guidance to delegate authorization to the business logic layer, verified 2026-09-02. [GraphQL documentation](https://graphql.org/learn/authorization/).
3. GraphQL Foundation, “Security,” official depth/breadth/batch/rate/trusted-document/demand-control guidance, verified 2026-09-02. [GraphQL documentation](https://graphql.org/learn/security/).
4. GraphQL Foundation, “Performance,” official N+1, batching, caching, pagination, and demand-oriented evidence guidance, verified 2026-09-02. [GraphQL documentation](https://graphql.org/learn/performance/).
5. OWASP Cheat Sheet Series, “GraphQL Cheat Sheet,” input, DoS, depth/amount/cost/rate, access-control, batching, introspection, and error guidance, verified 2026-09-02. [OWASP](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html).
6. OWASP Cheat Sheet Series, “Authorization Cheat Sheet,” least privilege, deny-default, every-request validation, object IDs, enforcement placement, logging, and testing, verified 2026-09-02. [OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html).

## Exercises

### Exercise 1

Define authentication, authorization, object/field/relationship decision, PEP, PDP, static cost, runtime budget, trusted document, and semantic rate limiting. Explain why none substitutes for another.

### Exercise 2

Using $C(v)=w_v+m_v\sum C(child)$, compute a query with root weight 2; `orders` weight 3, maximum 20; and children `id` weight 1 plus `items` weight 2, maximum 10, with child `price` weight 2. State limitations.

### Exercise 3

Design authorization for `node(id:)`, `Project.members`, `Member.salary`, `inviteMember`, and project-event subscription across two tenants. Include loaders, denial semantics, audits, policy change, and tests.

### Exercise 4

Diagnose a public graph protected only by depth 12, IP request rate, disabled introspection, global loaders, and SHA-256 persisted queries uploaded by callers. Provide a layered repair and calibration plan.

### Exercise 5

Design authorization and cost control for an emergency coordination graph spanning gateway and incident/responder/location subgraphs. Dispatch mutations and location fields are sensitive; mobile uses trusted documents; responders are paginated and optionally deferred. Specify trust, policy, cost model, runtime/quotas, federation, lifecycle, observability, and adversarial evidence.

## Answers to the Exercises

### Answer 1

Authentication verifies identity/credential context. Authorization decides actor–action–resource-context under policy. Object decisions protect instances, field decisions protect properties/capabilities, and relationship decisions protect traversal. A PEP requests/enforces a decision; a PDP evaluates governed rules/attributes. Static cost conservatively estimates normalized selected work before execution; runtime budget caps observed calls/rows/bytes/CPU/time/concurrency. A trusted document is approved exact operation text under a manifest lifecycle. Semantic rate limiting charges work or sensitive actions per identity/tenant/client.

Authentication supplies actor but not permission. Authorization says allowed, not affordable. Static cost can be wrong; runtime limits contain actual behavior. Runtime limits do not decide disclosure. Trusted text does not decide current actor/resource/variables or future resolver cost. Rate limiting distributes usage across time but cannot repair one unauthorized or catastrophically large accepted operation.

### Answer 2

`price` costs 2. `items` costs $2+10(2)=22$. Per-order selected children cost `id` 1 plus `items` 22, or 23. `orders` costs $3+20(23)=463$. Root total is $2+463=465$ under this tree convention.

The number is meaningful only if list maxima are enforced and weights conservatively model implementation. It omits shared batching/caches, retries, data skew, authorization filtering, bytes, CPU, concurrency, abstract-type branches, directives/fragments, and downstream nonlinear behavior. Use it for early admission with structural gates, then enforce multidimensional runtime budgets and calibrate against observations.

### Answer 3

Authenticate once and create immutable actor/tenant/delegation context. `node(id:)` resolves expected type without trusting ID contents, then domain `viewMember/project` policy decides. `Project.members` applies tenant/relationship visibility in selection and authorizes traversal/resources. `Member.salary` invokes a distinct compensation capability; project visibility never implies it. `inviteMember` authorizes inviter, target tenant/project, action, role constraints, current project state, and mutation effect/idempotency. Subscription authorizes project/event source at connect and each event delivery when membership/policy may change.

Loaders are request-scoped or keyed by complete actor/tenant/action/policy/snapshot equivalence, return aligned per-resource decisions, and reauthorize on read. Cross-request shared caches contain visibility-classified data and policy-version invalidation. Choose null-for-absent/forbidden for public lookups only with timing/count/cache consistency; use stable redacted forbidden/domain errors where trusted UX requires. Audit actor, action, opaque resource reference, tenant, policy version, decision/reason class, and effect—not tokens/salary.

Test actor/action/resource-state matrices through node, nested edge/node, search, alias, mutation payload, subscription, cache hit, batch, and direct service paths; cross-tenant equal IDs; role/relationship revocation; policy version changes; stale cache; absent versus forbidden timing/count/error; enumeration; and audit completeness/redaction.

### Answer 4

Depth 12 misses shallow breadth, aliases, nested list multiplication, huge variables, HTTP operation batches, invalid-document floods, and expensive fields. IP rate fails behind shared networks and one-request fan-out. Disabled introspection is not authorization and suggestions/schema guessing remain. Global loaders can leak cross-user data. Caller upload makes “persisted” documents untrusted; a hash proves identity, not approval.

Add raw body/token/definition/fragment/validation-error bounds; normalized depth, list depth, self-reference, breadth, aliases, root fields, batch count, input/cardinality maxima; weighted coordinate cost with enforced list multipliers; principal/client/tenant static budgets; and request rejection before execution. Add deadlines/cancellation, resolver/dependency/row/byte/CPU/concurrency/response/patch budgets, bulkheads, and instance containment. Charge estimated/actual work and sensitive object/actions by authenticated identity/tenant/client plus anonymous network signals.

Move authorization into domain boundaries for every root/nested/node/edge/mutation/subscription path, use request-scoped policy-aware loaders, and govern absence/error/audit. Replace upload with build-authorized manifests bound to exact text, operation, client, environment, schema, owner, cost, expiry/status; reject unknown/mismatched documents and retain rollout/revocation. Choose bounded introspection by audience rather than assuming hiding secures fields.

Calibrate predicted cost against calls, rows, bytes, duration, CPU/memory, cache/batches, errors, and cancellation by bounded operation ID/schema version. Fuzz deep/wide/list/alias/fragment/abstract/introspection/batch/invalid operations; test cross-principal caches and policy paths; tune thresholds/weights and canary changes.

### Answer 5

Gateway authenticates user/device and propagates audience-bound signed delegation plus workload identity; each subgraph validates both and incident/responder/location domain services remain authoritative PDP/PEPs. Policies bind actor, tenant/jurisdiction, incident state, purpose, resource, action, credential strength, and policy version. Location has distinct field capability and minimization; dispatch mutation authorizes transition/assignment and durable effect identity. Existence-hiding and redacted errors are consistent across gateway/subgraphs, counts/connections, and caches. Audit protected decision/effect evidence.

Normalize operations at gateway using composed schema: body/token/fragment/depth/list/self-reference/breadth/alias/root/batch/input gates; weighted coordinates for remote hops, location, search, responder connection, dispatch, and deferred work; cardinality from enforced page maxima; conservative abstract/subgraph branches. Subgraphs also enforce local structural/runtime limits against direct/replanned calls. Admit against actor/client/tenant budgets before planning/execution.

Create request-scoped loaders keyed by actor/tenant/action/policy/snapshot/projection; authorize aligned items. Runtime context propagates one deadline/cancellation and caps subgraph calls, rows/responders, bytes, concurrency, CPU/memory, and incremental patches/duration. Bulkheads isolate location/dispatch. Semantic quotas charge dispatch attempts and responder/location lookups even through aliases/batches; reserve predicted cost and record actual under governed refund rules.

Mobile trusted documents are registered by signed build pipeline and bound to exact operation/name, app/version/environment, composed schema, owner, reviewed cost, rollout/expiry/status; unknown/mismatched text fails, old versions overlap adoption, and emergency revocation exists. They never bypass current authorization, variable/page validation, quotas, or runtime budgets. Recompute after resolver/composition/cost changes.

Deferred responder fragments remain included in total static cost and have patch/open-duration/buffer limits; unsupported clients use ordinary or follow-up queries. Cancellation releases loaders/subgraph work, not committed dispatch. Record bounded operation/schema/document/policy identity, predicted/actual dimensions, subgraph plan/calls, decisions, quotas, errors, cancellation, and no sensitive variables/location/token.

Test every reachability path and direct subgraph, cross-tenant IDs, forged delegation, gateway bypass, revocation during subscription/defer, cache policy change, deep/wide/alias/nested-max operations, batch dispatch brute force, invalid floods, underpriced resolver, dependency slowness, disconnect, patch amplification, and policy/error/timing/count leakage. Compare predicted with actual calls/rows/bytes/CPU/latency and rehearse manifest/policy rollback.
