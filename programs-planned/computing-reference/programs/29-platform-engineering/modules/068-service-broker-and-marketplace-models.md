---
module_id: PLAT-068
program: Platform Engineering
level: 2
module_number: 68
title: Service Broker and Marketplace Models
status: complete
last_verified: 2026-09-02
---

# Service Broker and Marketplace Models

## One-Page Review

### Governing question

How should a platform expose internal and external capabilities through a marketplace and broker protocol so consumers can discover, provision, bind, update, observe, and retire service instances without collapsing product governance, lifecycle authority, credentials, or provider failure into a portal catalog?

### Essential definitions

- A **marketplace** is an authorization-filtered discovery and governance surface for supported service offerings, versions/plans, terms, evidence, and lifecycle actions.
- A **service offering** is a stable advertised capability with owner, contract, support, lifecycle, and one or more plans.
- A **service plan** is a versioned governed variant defining capacity, isolation, features, policy, cost, SLO, parameters, and allowed lifecycle transitions.
- A **service broker** is an adapter/control-plane component implementing a lifecycle protocol between platform and service provider.
- A **service instance** is one provisioned occurrence of an offering and plan with stable instance identity and provider references.
- A **binding** is a separately governed relationship authorizing or configuring a consumer to use an instance; it may issue credentials, identity references, or routing configuration.
- A **provisioning operation** is the durable request to create/update/delete an instance; an accepted asynchronous operation is not completed work.
- **last-operation state** is the broker/provider evidence for an asynchronous lifecycle request, including in-progress, succeeded, failed, and explanation.
- **orphan mitigation** is controlled reconciliation and cleanup when the platform cannot determine whether a failed/ambiguous provisioning attempt left provider resources.
- A **portfolio** is a curated, audience-specific set of offerings/plans plus access and launch constraints.
- **maintenance information** or **offering revision** binds a lifecycle request to the advertised broker version/configuration it was designed for.
- A **marketplace federation** aggregates offerings from multiple providers while preserving globally stable identity, authority, and collision handling.

### Central model, mechanism, or theorem

Model a marketplace product as

$$
P=(s,p,v,c,g,l),
$$

where $s$ is immutable offering identity, $p$ plan identity, $v$ contract/revision, $c$ capability and parameter contract, $g$ governance/eligibility constraints, and $l$ lifecycle/support contract. A provision request $R=(i,s,p,v,x,o,t)$ uses stable instance ID $i$, validated parameters $x$, owner/tenant $o$, and operation token $t$. The platform authorizes and records intent; the broker maps it idempotently to provider effect and returns synchronous completion or asynchronous operation identity. Bindings $B=(j,i,a,k)$ have separate stable ID $j$, consumer/application identity $a$, and binding kind $k$. Instance existence, binding existence, and operation outcome must be reconciled independently; catalog absence or a transport failure is never sufficient proof of provider absence.

### Critical invariants

- Offering, plan, instance, operation, binding, and consumer identities are distinct and stable; mutable names are presentation attributes.
- Every visible plan has an accountable provider owner, supported version, eligibility, parameter schema, cost, isolation, SLO, data/security, update, binding, and retirement contract.
- Marketplace discovery filters authorization before search, ranking, counts, facets, and details; visibility does not itself grant provisioning.
- One accepted instance occurrence maps to at most one provider instance; retries reuse instance and operation identity and reconcile ambiguous outcomes.
- `accepted` or `in progress` never becomes `succeeded` without authoritative provider/broker evidence.
- Concurrent mutations on one instance or binding are serialized or rejected according to explicit concurrency semantics.
- Bindings use least-privilege workload identity where possible; credential material is single-display or stored only in a secret authority, rotated, revocable, scoped, and never logged.
- Provision, update, bind, rotate, unbind, and deprovision each authenticate, authorize, validate current plan/revision, and record originating identity.
- Provider and broker remain authoritative for external effects; marketplace/index state is a derived product and discovery view.
- Failed or timed-out create/delete enters reconciliation/orphan-mitigation state before retry or cleanup.
- Plan/offering removal cannot strand existing instances; deprecation, upgrade, migration, support, and zero-instance retirement are explicit.
- Multi-provider aggregation preserves source, provenance, API/version compatibility, quotas, blast-radius isolation, and per-broker health.

### Common failures

Marketplace as a page of links; every template called a service; offering name as identity; plan as cosmetic tier; stale broker catalog treated as truth; discover permission equated with provision permission; unbounded free-form parameters; platform passing arbitrary provider IDs; random instance ID after retry; HTTP 202 shown as ready; last-operation polling without deadline; concurrent updates racing; broker state treated as domain truth; binding and instance identity conflated; static shared credentials returned in plaintext; secret values in workflow history or logs; binding deletion assumed to revoke copied credentials; delete retry after ambiguous response; orphan mitigation as blind deprovision; product removal hiding live instances; automatic plan upgrade without compatibility; one failing broker blocking all discovery; and popularity ranking overriding safety/fitness.

### Compact example

A developer selects `postgresql` offering ID `svc-db-17`, plan `ha-small` ID `plan-4`, revision `2026-08`, for tenant `payments`. The marketplace verifies eligibility, displays cost/SLO/data limits, validates bounded parameters, and creates instance `inst-82` with operation key `op-82-create`. Broker returns accepted plus operation `bop-991`; the portal shows provisioning until `last_operation` reports succeeded with provider ID. Binding `bind-5` grants workload identity `payments-api`, not a shared password. Rotation creates a successor binding and atomically switches the secret reference before revoking the old grant. A timed-out deprovision triggers provider lookup and orphan mitigation; the offering cannot retire while `inst-82` or retained obligations remain.

### Connections

This module composes API layers from [PLAT-061](061-platform-api-layers.md), portal discovery from [PLAT-062](062-developer-portal-architecture.md), catalog authority from [PLAT-063](063-software-catalogs.md), ownership from [PLAT-064](064-ownership-and-metadata.md), durable workflows from [PLAT-065](065-workflow-and-orchestration-layers.md), policy enforcement from [PLAT-066](066-policy-decision-and-enforcement-points.md), and account/environment vending from [PLAT-067](067-environment-and-account-vending.md). PLAT-069 adds platform eventing, while PLAT-070 addresses component composition.

## Governing Question

How can a platform offer heterogeneous managed capabilities through one coherent product experience while preserving the distinct lifecycle, identity, security, availability, and commercial semantics of each service provider?

A marketplace helps consumers choose. A broker carries lifecycle commands. A provider control plane creates and operates service effects. These three responsibilities can be implemented by one product, but their semantics must remain distinct.

Uniformity is valuable only where contracts truly align. Databases, message brokers, SaaS accounts, DNS zones, certificates, and internal APIs differ in provisioning duration, binding, isolation, data lifecycle, cost, and reversibility. A lowest-common-denominator interface can hide critical choices.

The platform's job is to make supported choices legible and safe: who can see and request them, what plan means, how progress is observed, how credentials are delivered, what failure leaves behind, and how instances migrate or retire.

## Why This Matters

Tool catalogs often stop at discovery. Users still open tickets, copy credentials, choose undocumented sizes, and guess how to delete. A marketplace becomes useful when discovery connects to governed, durable lifecycle operations.

Brokers concentrate privilege. They can create databases, accounts, routes, credentials, or paid SaaS subscriptions across tenants. Input validation, authorization, least-privilege provider access, and audit are essential.

Provider operations fail ambiguously. A request can commit and lose its response. If the platform retries with a new identity, it creates duplicates; if it assumes failure, it leaks resources and cost. Stable IDs, last-operation state, and reconciliation are core protocol features.

Bindings are a major attack surface. Long-lived static credentials copied into portal responses or application configuration survive unbinding and become difficult to rotate. Workload identity and secret-authority references reduce this risk but require explicit lifecycle.

Offerings also age. Plans change, providers deprecate APIs, prices rise, and security baselines evolve while live instances remain. A marketplace must manage the full installed base, not merely publish new versions.

## Prerequisites and Retrieval

Retrieve product catalogs and portfolios, API contracts/versioning, asynchronous operations, state machines, idempotency, retries and reconciliation, service control planes, multi-tenancy, authorization, workload identity and secrets, schema/defaulting, quotas, billing, SLOs, data lifecycle, sagas/orphan mitigation, catalog/search security, software supply chain, audit, migration, and retirement.

You should distinguish marketplace from software catalog; offering from plan; product definition from provisioned instance; plan revision from instance configuration; instance from binding; consumer identity from requester identity; acceptance from completion; operation ID from instance ID; broker from provider; broker database from provider truth; unbind from credential revocation; deprovision from orphan mitigation; deprecation from deletion; portfolio visibility from provisioning authority; and template rendering from managed-service lifecycle.

## Learning Objectives

After completing this module, you should be able to:

1. define marketplace, offering, plan, portfolio, broker, instance, operation, binding, and provider boundaries;
2. design governed offering/plan contracts and authorization-filtered discovery;
3. implement idempotent synchronous and asynchronous provision/update/deprovision protocols;
4. reconcile ambiguous outcomes, concurrency, broker/provider drift, and orphan resources;
5. design least-privilege binding, secret delivery, rotation, revocation, and audit;
6. aggregate multiple brokers without identity collision, health coupling, or semantic flattening;
7. evolve offering schemas, plans, prices, SLOs, broker APIs, and live instances safely;
8. measure discovery fitness, provision lead time, reliability, adoption, cost, binding risk, drift, and retirement;
9. test malicious parameters, duplicate requests, provider failure, credential leakage, migration, and restore; and
10. retire offerings and brokers only after installed instances, bindings, operations, and retained obligations are disposed.

## Core Exposition

### Separate marketplace, broker, and provider

The marketplace owns presentation and product governance: discoverable offerings, plan comparisons, eligibility, documentation, support, cost, evidence, and user journeys. It may aggregate several sources.

The broker owns the platform-facing lifecycle protocol: catalog advertisement, provision, update, deprovision, bind, unbind, rotation, fetch, and operation status. It translates a stable contract to provider-specific operations.

The provider control plane owns actual service resources and their domain state. A broker can be part of the provider or an adapter maintained by the platform. Either way, provider references and authoritative status must survive broker restart.

Avoid portal plugins that invoke raw provider APIs and keep hidden state. Every interface—portal, CLI, API, workflow, controller—should use the same broker/control-plane contract.

### Decide what qualifies as an offering

An offering is a supported capability with lifecycle and operational responsibility, not any script that creates resources. It needs a provider owner, consumer job, eligibility, support, SLO, security/data contract, cost model, lifecycle, and measurable outcome.

A thin template can still be a marketplace product if its lifecycle is intentionally “generate and hand off,” but say so. Do not promise managed updates, backups, or deletion when ownership transfers entirely to the consumer.

Distinguish managed service, composed resource product, SaaS entitlement, account, and knowledge-only integration. They may share discovery but require different lifecycle/binding protocols.

Review whether a new offering duplicates an existing capability, has sustainable demand, and has a retirement path. Marketplace size is not platform value.

### Make plans governed contracts

A plan expresses meaningful variants: capacity, availability, isolation, tenancy, regions, data durability, backup, encryption, networking, features, maintenance, support, quotas, cost, and lifecycle. It is not just “small/medium/large” marketing.

Give offering and plan immutable IDs; names and descriptions may change. Version schemas and maintenance information. Record which changes are compatible for new provisions, in-place updates, migrations, or only new plan IDs.

Parameters have types, bounds, defaults, immutability, sensitivity, cross-field validation, and authority. Expose only choices the provider and support team can honor. Avoid arbitrary provider configuration blobs.

Document responsibilities: platform, broker owner, provider, application owner, security, data owner, and finance. Include support hours, incident path, maintenance notice, backup/restore, and deletion retention.

### Curate portfolios and discovery

Portfolios group products for audiences such as development, regulated production, data science, or a business unit. They combine visibility, eligibility, constraints, and local governance without cloning product identity.

Filter authorization before search indexing, autocomplete, counts, facets, recommendations, and details. An offering may reveal strategic vendors, restricted regions, prices, or capabilities.

Discovery permission does not grant provisioning. Some users may compare offerings but lack authority for a production instance. Show eligibility and approval needs without leaking hidden policy structure.

Rank by fitness for the declared job—compatibility, supported region, classification, SLO, cost, adoption, and support health—not popularity alone. Avoid steering every workload toward one fashionable service.

### Aggregate broker catalogs safely

Fetch catalogs with authenticated connections, API-version negotiation, timeout, size bounds, schema validation, and provenance. Cache last-known-good under explicit freshness while showing broker health and observation time.

Immutable offering and plan IDs prevent collision across brokers. If a protocol promises global uniqueness, enforce it; otherwise namespace by broker identity. Never merge products because names and tags match.

Catalog metadata is untrusted presentation input. Sanitize Markdown/HTML, links, images, support URLs, and parameter descriptions. Do not allow broker-supplied content to execute script or exfiltrate identity.

One slow or malformed broker should not block all discovery. Isolate fetch, parsing, indexing, quota, and failure state per broker. Quarantine collisions or incompatible schema rather than last-write-wins.

### Design the provisioning contract

The platform chooses stable instance ID and operation/request identity, validates offering/plan revision and parameters, authorizes requester/tenant/owner/cost, and calls the broker with bounded context.

The broker must treat repeat provision of the same instance and semantically identical request as success/no-op or return the existing outcome according to protocol. Reuse with different plan/parameters is conflict, not a second instance.

Store request digest, originating principal/delegation, tenant, owner, cost, product revision, and broker/provider receipt. Context helps audit and placement but should not be an unbounded secret-bearing dump.

Return synchronous success only when the instance is ready under the contract. If work continues, return accepted with stable operation identity and status endpoint/event semantics.

### Operate asynchronous lifecycle explicitly

Long-running provision/update/delete needs durable state: accepted, in progress, succeeded, failed, canceled where supported, and ambiguous/reconciling. Include safe description, retry/repeatability, instance usability, and last progress time.

Poll last-operation with backoff, jitter, deadline, broker rate limits, and stable operation token. Polling the “last” operation without its identity can confuse a newer request; correlate exact occurrence.

Do not infer success from broker HTTP availability, elapsed time, or instance fetch alone unless the contract says which state proves readiness. Verify provider-specific readiness and required baseline.

If status remains unknown beyond deadline, preserve the instance/operation in reconciliation. Do not issue a new create ID or report failure as proof of absence.

### Control concurrent mutations

Provision, update, bind, unbind, rotate, and deprovision can conflict. Define an instance-level state machine and concurrency token. Serialize incompatible operations or reject with a retryable conflict.

Some bindings can be created concurrently; others mutate a shared instance and must serialize. The broker advertises or documents this contract, and the platform does not assume parallel safety.

Use expected instance/plan revision for updates. A consumer cannot overwrite a newer configuration with a stale form. Return current state and a new preview.

Deprovision must fence new binds and updates. Unbinding during delete either completes first, becomes part of cleanup, or returns a defined conflict; it must not race silently.

### Preserve provider truth and reconciliation

The broker stores mappings, operation receipts, and desired contract, but the provider owns actual service existence and state. Reconcile by immutable provider references and operation tokens.

Detect broker-lost/provider-present, broker-present/provider-missing, plan/configuration drift, unexpected bindings, failed credentials, quota changes, and provider-side maintenance. Classify repair versus escalation.

Do not automatically recreate a missing stateful service from broker intent without data/restore semantics. Provider absence may be permission or regional visibility failure. Confirm authority and recovery policy.

Expose observed provider revision/time separately from broker processing time. A recently refreshed row can still describe stale provider evidence.

### Mitigate orphans deliberately

An orphan may arise when provision commits but the platform does not record success, or when deprovision fails after partial cleanup. Orphan mitigation begins with discovery and correlation, not blind deletion.

Use instance ID, operation token, provider receipt, tenant, creation window, immutable tags/metadata where trustworthy, and provider list/get APIs. Quarantine ambiguous matches. Similar name is insufficient.

If a failed provision left resources, decide adopt-and-complete, compensate/delete, or assign manual disposition based on data and side effects. Cleanup uses the original identity and idempotent operations.

Record residual cost, data, credentials, addresses, and support obligations. Mark resolved only after provider evidence and inventory reconciliation, not after sending delete.

### Model binding separately from provisioning

An instance can exist without consumers; a binding grants/configures one consumer's use. Give it stable binding ID, instance ID, consumer/workload identity, binding type, scope, expiry, provider reference, and lifecycle.

Prefer workload identity, federated roles, certificates, or provider-native grants over static usernames/passwords. The binding response can contain a secret reference and nonsecret endpoints rather than raw credentials.

If raw credentials must be returned, make delivery single-use where supported, place them immediately in a secret authority, redact logs/history, and define recovery when the response is lost. “Fetch binding” semantics affect recoverability and exposure.

Binding creation is independently authorized. Owning an application or instance does not automatically permit any scope. The broker enforces tenant, instance, plan, and consumer relationship.

### Rotate and revoke bindings

Rotation is a lifecycle, not overwriting a secret. Create successor credential/grant, distribute it, verify consumer adoption, switch traffic or secret reference, then revoke predecessor. Track overlap deadline.

Use distinct binding occurrences so retry cannot revoke the wrong generation. Provider supports lookup/revoke by immutable grant ID, not username alone.

Unbinding removes the provider grant and secret reference according to contract. Deleting a Kubernetes Secret or portal record does not revoke a copied database password.

Detect leaked, unused, expired, and orphaned bindings. Emergency revocation may precede application migration; expose incident impact and recovery path.

### Secure broker privilege and trust

Authenticate platform to broker and broker callbacks/events. Use TLS, narrow service identity, rotation, audience, replay defense, and network policy. Basic protocol compatibility does not define an organization's strongest authentication.

Broker provider credentials are least privilege per offering/tenant/region where feasible. Separate high-risk providers and do not give one generic broker universal administrator access.

Validate all platform context; a broker is still a policy enforcement point for provider effects. Do not trust arbitrary `organization`, `project`, `region`, or owner fields merely because the call came from the platform.

Audit request identity and originating principal/delegation without placing tokens or personal data into provider tags. Mask secrets in broker errors and decision/operation logs.

### Update instances and plans safely

Define mutable parameters, allowed source/target plans, downtime, cost, capacity, data migration, backups, compatibility, rollback boundary, and instance usability during failure.

Preview changes before execution. Bind the approval and update to current instance/provider revision, plan maintenance info, and parameter digest. Reject stale catalog revisions when semantics changed.

In-place resize can be simple; engine/version or tenancy changes may require a replacement instance and data migration. Do not hide replacement behind “update” if identity, endpoint, or loss risk changes.

Keep the old plan supported until instances migrate or an explicit end-of-support policy applies. New catalog default does not mutate installed instances automatically.

### Handle quotas, cost, and metering

Each offering declares organization/provider capacity, per-tenant instance/binding limits, parameter-driven resource use, and rate limits. Admission occurs before expensive provision where possible.

Cost contract covers setup, recurring, usage, egress, backup, support, and deletion-retention charges. Show estimates/ranges and responsible cost center. Marketplace metadata is not the billing ledger.

Meter provider use with authoritative dimensions and revisions. Avoid double counting retries or broker polling as consumption. Reconcile provisioned inventory to bills.

Capacity exhaustion is a first-class outcome with queue, alternate plan, region, or human capacity workflow. Do not accept indefinitely when fulfillment is impossible.

### Keep marketplace and software catalog distinct

The software catalog describes systems, components, APIs, resources, and ownership. The marketplace advertises supported capabilities consumers may acquire. A provisioned service instance can appear as a catalog resource, but its lifecycle authority stays with broker/provider.

Link offering, instance, bindings, consuming systems, owners, docs, and operations by stable references. Do not let catalog editing create or delete provider services implicitly.

The portal composes marketplace and catalog views. It should show “what can I get?” separately from “what exists and who owns it?” while allowing navigation between them.

Authorization and freshness apply to both. A hidden restricted offering or instance must not leak through cross-links, counts, graphs, or search.

### Federate providers without false portability

A common interface can normalize lifecycle states, identities, operation tracking, and basic plans. It cannot erase differences in data consistency, backup, regions, networking, credentials, maintenance, or deletion.

Define a portable capability contract only for guarantees every conforming provider demonstrates. Expose provider-specific extensions under governed namespaces and prevent policy-critical semantics from hiding in opaque metadata.

Support selection policies such as region, residency, cost, availability, existing commitments, and capacity. Preserve why a provider was selected and whether failover/migration is supported.

Do not silently switch an existing stateful instance to another provider. Replacement requires data and binding migration, identity/endpoint change, verification, and rollback plan.

### Operate brokers as shared control planes

Set SLOs for catalog freshness, provision/update/delete lead time, operation-status freshness, binding delivery/rotation, and request availability. Segment by broker, offering, plan, region, and tenant.

Isolate worker queues, credentials, rate limits, circuit breakers, and quotas so one provider outage does not starve others. Apply backpressure to marketplace and workflows.

Observe lifecycle counts/states, age, retries, ambiguous outcomes, orphan investigations, provider drift, binding age, secret delivery failure, quota/cost, catalog collisions, API version, and deprecated installed base.

Operator actions—adopt, retry, cancel, mark provider evidence, rotate, force unbind, compensate—are authorized durable commands with reason, preview, idempotency, and audit. Never edit broker database rows casually.

### Test the contract and installed base

Run conformance tests for catalog schema, identity stability, provisioning idempotency, asynchronous status, error semantics, fetch, update, binding, rotation, unbinding, and deprovisioning.

Fault-inject before/after provider commit, broker persistence, response, and status. Repeat instance/binding IDs with same and different digests. Test concurrent mutations and stale plan revisions.

Security tests cover unauthorized portfolio/search, malicious catalog content, parameter injection, cross-tenant IDs, forged originating identity, broker credential theft, secret/log leakage, binding replay, and provider callback forgery.

Restore broker/platform state from backup, reconcile provider instances/bindings before dispatch, and test catalog/provider evolution with old installed instances.

### Deprecate and retire responsibly

Deprecation stops recommendation and eventually new provisioning; it does not erase installed instances. Publish dates, successor, migration tooling, support changes, cost, and exception process.

Inventory instances, bindings, operations, provider resources, data, backups, consumers, owners, cost, security findings, and dependencies. Measure migration and zero-use independently of catalog visibility.

Removing a plan from advertised catalog can impair updates/deletes if the broker loses its contract. Retain lifecycle compatibility for installed instances until disposed or migrated.

To retire a broker, stop new provisions, route offerings to successors, drain/update/deprovision installed base, preserve operation/binding histories and decoders, reconcile provider truth, revoke credentials, and test recovery after removal.

## Definitions and Notation

Let $S$ be offerings, $P$ plans, $I$ instances, $J$ bindings, $A$ consumers/applications, $O$ lifecycle operations, $B$ brokers, and $T$ time.

A marketplace product is $P_m=(s,p,v,c,g,l)$. A provision request is $R=(i,s,p,v,x,o,t)$ with stable instance ID $i$ and operation token $t$. Let $Provider(i)$ be the immutable provider reference discovered or created for $i$.

A binding is $B_j=(j,i,a,k,v,t_x)$, where $j$ is binding ID, $a$ consumer, $k$ kind/scope, $v$ binding generation or provider grant, and $t_x$ optional expiry. Instance deletion does not prove every copied credential was revoked; authoritative grant evidence is required.

For operation $o$, status function $L(i,o)$ yields in-progress, succeeded, failed, or unknown with provider revision and observation time. Succeeded must be terminal for that exact occurrence; “last” without operation identity is ambiguous under concurrent or later operations.

Let $N_p$ be active instances of deprecated plan $p$ in an independent provider/broker inventory. Plan retirement requires $N_p=0$ plus disposition of bindings, operations, retained data, and compatibility obligations; hidden catalog count is insufficient.

## Mechanisms, Invariants, or Proof Structure

### Marketplace and broker protocol

1. Define consumer jobs, offering eligibility, provider ownership, lifecycle authority, and non-goals.
2. Publish immutable offering/plan IDs with versioned capability, parameter, governance, cost, SLO, binding, update, and retirement contracts.
3. Curate authorization-filtered portfolios and aggregate broker catalogs with provenance, isolation, validation, and freshness.
4. Accept stable instance/operation identity, validate parameters/plan revision, and authorize requester, tenant, owner, cost, and provider scope.
5. Provision idempotently; distinguish synchronous completion from asynchronous acceptance and track exact operation state.
6. Serialize conflicting mutations and reconcile broker/provider state after timeout, crash, restore, or external change.
7. Investigate and mitigate orphan effects using immutable identity and provider evidence.
8. Create bindings as separate least-privilege grants; deliver secrets safely and support rotation/revocation.
9. Update or migrate instances under current revisions, preview, compatibility, data, cost, and rollback contracts.
10. Observe broker/provider health, lifecycle age, drift, binding exposure, quotas, installed versions, and enforcement.
11. Test conformance, duplicates, ambiguous commits, concurrency, tenancy, malicious content, secret handling, and recovery.
12. Deprecate and retire only after installed instances, bindings, operations, data, consumers, and provider effects are disposed.

### Core invariants

- **Identity separation:** product, plan, instance, operation, binding, consumer, and provider references never collapse.
- **Product completeness:** every plan has a supported lifecycle/security/cost/operations contract.
- **Discovery confidentiality:** authorization filters every marketplace-derived surface.
- **Idempotent occurrence:** one accepted instance/binding occurrence produces at most one intended provider effect.
- **Completion honesty:** accepted/in-progress/unknown never appears succeeded.
- **Mutation serialization:** incompatible lifecycle operations cannot race silently.
- **Credential containment:** binding secrets/grants are scoped, protected, rotated, revocable, and evidenced.
- **Authority preservation:** provider/broker evidence decides effects; marketplace/catalog views remain derived.
- **Orphan restraint:** ambiguity triggers reconciliation, not duplicate creation or blind deletion.
- **Installed-base continuity:** catalog/plan evolution preserves lifecycle for existing instances.
- **Federation isolation:** one broker cannot corrupt identity or availability of the aggregate.
- **Retirement evidence:** zero advertised products does not equal zero instances or obligations.

### Proof sketch: asynchronous acceptance cannot prove readiness

Assume an accepted response proved instance readiness. Consider two broker executions that both return accepted: in world A the provider later completes; in world B it later fails after exhausting capacity. At acceptance time the platform observes the same response but the final readiness outcomes differ. Therefore acceptance contains insufficient information to distinguish ready from failed. The platform must observe terminal status and contract-specific readiness evidence. This is a proof sketch of insufficiency, not a claim that polling is the only valid observation mechanism.

### Executable broker-state audit

This synthetic audit classifies ten instance-operation observations. It demonstrates state accounting, not broker conformance or provider readiness.

<!-- bijux-verify: {"id":"broker-operation-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"succeeded=4\nin_progress=2\nfailed=1\nunknown=1\norphan=1\nstale=1\n"}} -->
```python
from collections import Counter

observations = [
    "succeeded", "succeeded", "succeeded", "succeeded",
    "in_progress", "in_progress", "failed", "unknown", "orphan", "stale",
]

counts = Counter(observations)
for state in ("succeeded", "in_progress", "failed", "unknown", "orphan", "stale"):
    print(f"{state}={counts[state]}")
```

Expected output reports four succeeded, two in progress, and one each failed, unknown, orphan, and stale. Production classification must use exact operation identity, provider revision/time, readiness contract, and independent resource inventory.

### Verification strategy

Catalog tests validate immutable ID stability, collisions, schema/version, plan constraints, sanitized content, API negotiation, broker isolation, authorization-filtered discovery, and stale-source behavior.

Lifecycle tests repeat identical/different instance and operation requests; inject crash/timeout before and after provider commit and broker persistence; poll stale/wrong operation IDs; race update/bind/delete; and reconcile provider drift.

Binding tests cover consumer/tenant authorization, workload identity, single-delivery secret loss, secret-store failure, rotation overlap, old grant revocation, copied credential, unbind during delete, and emergency revoke.

Security tests fuzz parameters/context, forge originating identity, cross tenants, steal broker credentials, inject catalog markup/links, expose logs/history, and bypass platform policy through provider APIs.

Evolution/recovery tests update offering/plan/API schemas with old instances, migrate data/bindings, restore broker state, reconcile provider resources before retry, drain a broker, and prove zero installed-base obligations before retirement.

## Alternatives and Trade-Offs

1. **Marketplace versus documentation catalog.** Documentation is cheap and flexible; a marketplace connects governed discovery to managed lifecycle at greater operational cost.
2. **Generic broker protocol versus provider-specific API.** A generic protocol standardizes identity/lifecycle; native APIs expose richer semantics. Use extensions without hiding critical guarantees.
3. **One broker per service versus shared broker.** Dedicated brokers isolate ownership and credentials; shared adapters reuse infrastructure but expand blast radius.
4. **Synchronous versus asynchronous provisioning.** Synchronous results simplify clients; long provider work needs durable async status and deadlines.
5. **Polling versus events/callbacks.** Polling reconciles lost messages; events reduce latency/load. Hybrid operation identity is robust.
6. **Static credentials versus workload identity.** Credentials are widely compatible; identity grants improve rotation/revocation but depend on provider support.
7. **Raw secret response versus secret reference.** Raw output simplifies protocol; references reduce exposure and centralize access auditing.
8. **Coarse plans versus many parameters.** Coarse plans are supportable; parameter flexibility fits workloads but increases variants, validation, and drift.
9. **In-place update versus replacement/migration.** In-place change preserves identity; replacement can reduce risk for incompatible changes but requires data/binding migration.
10. **Broker authority versus provider reconciliation.** Broker-only state is fast; provider reads reveal drift and ambiguous commits. Use both with clear authority.
11. **Automatic orphan cleanup versus quarantine.** Automation reduces leakage; ambiguity can delete legitimate data. Match confidence and reversibility.
12. **Global marketplace versus portfolios.** Global discovery aids reuse; portfolios support local eligibility and constraints. Preserve product identity across views.
13. **Federated providers versus single provider.** Federation adds resilience/choice; it complicates semantics, cost, migration, and operations.
14. **Automatic upgrades versus consumer-scheduled migration.** Automation reduces vulnerable versions; stateful/data changes may need explicit maintenance and rollback.
15. **Remove deprecated plan versus keep hidden lifecycle support.** Removal reduces clutter; installed instances still require update/delete/migration contracts.

## Failure Modes and Misconceptions

1. **A marketplace is a page of links.** Useful products connect discovery to governed lifecycle and support.
2. **Every template is a managed service.** Lifecycle ownership and guarantees must be explicit.
3. **Offering name is stable identity.** Names change and collide; immutable IDs correlate lifecycle.
4. **A plan is only price or size.** It defines operational, security, data, support, and lifecycle semantics.
5. **Visibility grants provisioning.** Discovery and effect authorization are separate.
6. **Catalog metadata is trusted content.** Brokers can provide malicious or malformed markup, links, and parameters.
7. **One broker outage should hide everything.** Isolate sources and expose stale/health state.
8. **HTTP success means service ready.** Accepted asynchronous work remains incomplete.
9. **Elapsed time proves completion.** Only terminal provider/broker evidence under readiness contract does.
10. **Retry with a new instance ID is safe.** It can duplicate committed resources and cost.
11. **The last operation is unambiguous.** Concurrent or later operations require exact occurrence identity.
12. **Concurrent binds and updates always commute.** Some providers mutate shared instance state.
13. **Broker database is provider truth.** External state can diverge after crash or manual change.
14. **Orphan mitigation means delete.** First discover; then adopt, compensate, or assign disposition.
15. **Similar names identify an orphan.** Mutable names can target unrelated resources.
16. **A binding is the instance.** It is one consumer's grant/configuration relationship.
17. **Owning an app permits every binding.** Scope, tenant, plan, and instance policy still apply.
18. **Deleting a secret revokes access.** Copied/provider credentials persist until authoritative revocation.
19. **Rotation means overwriting one password.** Safe rotation manages successor, adoption, overlap, and predecessor revocation.
20. **Unbind always succeeds after instance deletion.** Operation ordering and provider cleanup contract matter.
21. **New plan default upgrades instances.** Installed configurations remain until governed update/migration.
22. **A failed update leaves the instance unchanged.** Providers can partially change; expose usability and reconcile.
23. **Catalog removal retires a plan.** Live instances, bindings, data, and operations remain.
24. **Common API makes providers interchangeable.** Data, consistency, identity, region, cost, and maintenance differ.
25. **Popularity identifies the best product.** Fitness depends on workload requirements and supported guarantees.
26. **Restoring broker state permits immediate replay.** Reconcile external effects first.

## Worked Examples

### Example 1

**Situation.** Two brokers advertise `postgres` with different IDs and guarantees.

**Reasoning.** Preserve both immutable offering/plan identities and provenance; compare plans by explicit capability/SLO/data/cost attributes; never merge by name or tag. Portfolios can recommend one for a workload class.

**Conclusion.** Federation aggregates products without erasing identity or semantics.

### Example 2

**Situation.** Provision returns 202 and the portal immediately displays “ready.”

**Reasoning.** Store operation token, show provisioning, poll or consume events for that occurrence, enforce deadline, and require terminal success plus contract readiness. Failure remains visible with safe repair.

**Conclusion.** Acceptance and readiness are distinct states.

### Example 3

**Situation.** Provider creates a database but the broker crashes before persisting success.

**Reasoning.** Retry uses the same instance/operation identity. Broker searches by provider receipt/idempotency metadata, verifies tenant and request digest, adopts the resource, and continues baseline rather than creating another.

**Conclusion.** Reconciliation closes the commit/record ambiguity.

### Example 4

**Situation.** An update to `ha-large` races with deprovision.

**Reasoning.** Instance concurrency token and state machine serialize or reject the second mutation. Deprovision fences new operations; stale update receives conflict and current state rather than mutating a closing resource.

**Conclusion.** Lifecycle mutations need explicit serialization.

### Example 5

**Situation.** Binding returns a database password in a portal response and the browser closes before it is stored.

**Reasoning.** Prefer broker-to-secret-authority delivery and return a reference. If single-display raw credentials are required, provide controlled binding fetch/reissue or rotate the lost binding; never log/history the secret.

**Conclusion.** Binding delivery failure is a security and recoverability state.

### Example 6

**Situation.** A Secret object is deleted, but a copied credential still connects.

**Reasoning.** Unbind/revoke the immutable provider grant, verify denial, remove secret references/copies where governed, and audit consumers. Secret-container deletion alone does not change provider authorization.

**Conclusion.** Revocation must occur at the effect authority.

### Example 7

**Situation.** A failed provision leaves two similarly named provider clusters.

**Reasoning.** Correlate instance ID, operation token, provider receipts, immutable metadata, tenant, request digest, and time. Quarantine ambiguity; do not delete by name. Adopt the verified intended effect and disposition any confirmed duplicate.

**Conclusion.** Orphan mitigation begins with identity proof.

### Example 8

**Situation.** A plan price and maintenance window change while instances remain.

**Reasoning.** Publish a new revision with effective dates; retain installed-instance contract or communicate governed change; require current maintenance info on updates; show cost/support impact and migration options.

**Conclusion.** Offering evolution must address the installed base.

### Example 9

**Situation.** A restricted offering name appears in search counts for unauthorized users.

**Reasoning.** Filter authorization before indexing/query, counts, facets, autocomplete, ranking, and cross-links. Discovery leakage is not repaired by denying only provision or detail.

**Conclusion.** Marketplace metadata can be sensitive.

### Example 10

**Situation.** The platform replaces a broker while thousands of instances and bindings exist.

**Reasoning.** Stop new provision on old broker, migrate immutable mappings and compatible lifecycle semantics, reconcile provider truth, route operations by ownership/version, test bindings and status, drain installed base, then revoke old credentials at zero obligation.

**Conclusion.** Broker replacement is a live control-plane migration.

## Cross-Program Connections

1. **API & Service Engineering:** resource identity, async operations, idempotency, schemas, errors, versioning, and callbacks define broker contracts.
2. **Distributed Systems:** ambiguous commit, retries, concurrency, eventual consistency, polling, events, and reconciliation govern lifecycle.
3. **Security Engineering:** least privilege, workload identity, secret containment, tenant isolation, broker trust, and audit protect bindings/effects.
4. **Database Systems:** state machines, uniqueness, operation ledgers, optimistic concurrency, materialized catalogs, and recovery shape implementation.
5. **Product Management:** consumer jobs, portfolios, plan design, adoption, support, pricing, fitness, and retirement shape marketplace value.
6. **Reliability Engineering:** SLOs, readiness, backpressure, broker isolation, fault injection, drift, and disaster recovery protect shared service.
7. **Data Engineering:** stateful migration, backup, retention, lineage, metering, and orphaned data complicate service lifecycle.
8. **Cloud Infrastructure:** provider APIs, accounts, quotas, networks, identities, regions, and managed services supply effects.
9. **Software Architecture:** adapters, anti-corruption layers, bounded contexts, control planes, sagas, and federation preserve ownership.
10. **FinOps:** price, usage metering, bills, quotas, reservations, installed base, and deletion charges determine economic governance.

## References

1. Open Service Broker API. [Specification v2.17](https://github.com/openservicebrokerapi/servicebroker/blob/v2.17/spec.md). Retrieved 2026-09-02.
2. Open Service Broker API. [OpenAPI Definition v2.17](https://github.com/openservicebrokerapi/servicebroker/blob/v2.17/openapi.yaml). Retrieved 2026-09-02.
3. Cloud Foundry. [Services Overview](https://docs.cloudfoundry.org/services/overview.html). Retrieved 2026-09-02.
4. Cloud Foundry. [Managing Service Brokers](https://docs.cloudfoundry.org/services/managing-service-brokers.html). Retrieved 2026-09-02.
5. AWS. [AWS Service Catalog Documentation](https://docs.aws.amazon.com/servicecatalog/). Retrieved 2026-09-02.
6. AWS. [AWS Service Catalog Concepts](https://docs.aws.amazon.com/servicecatalog/latest/adminguide/what-is_concepts.html). Retrieved 2026-09-02.
7. AWS. [AWS Service Catalog API Overview](https://docs.aws.amazon.com/servicecatalog/latest/adminguide/service-catalog-api-overview.html). Retrieved 2026-09-02.
8. Crossplane. [Managed Resources](https://docs.crossplane.io/latest/managed-resources/managed-resources/). Retrieved 2026-09-02.
9. Crossplane. [Compositions](https://docs.crossplane.io/latest/composition/compositions/). Retrieved 2026-09-02.
10. Kubernetes SIG Service Catalog. [Service Catalog Project](https://github.com/kubernetes-sigs/service-catalog). Retrieved 2026-09-02; project status considered when assessing current use.
11. Kubernetes. [Service Accounts](https://kubernetes.io/docs/concepts/security/service-accounts/). Retrieved 2026-09-02.
12. SPIFFE. [SPIFFE Concepts](https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/). Retrieved 2026-09-02.
13. CNCF TAG App Delivery. [CNCF Platforms White Paper](https://github.com/cncf/tag-app-delivery/blob/main/platforms-whitepaper/latest/index.md). Retrieved 2026-09-02.
14. IETF. [RFC 6749: The OAuth 2.0 Authorization Framework](https://datatracker.ietf.org/doc/html/rfc6749). October 2012. Retrieved 2026-09-02.

## Exercises

### Exercise 1

Define marketplace, offering, plan, broker, provider, portfolio, instance, operation, binding, last-operation state, orphan mitigation, and maintenance revision. State four non-equivalences.

### Exercise 2

Trace provision through authorization, validation, 202 acceptance, polling, provider commit before broker crash, reconciliation, readiness, and handoff. Specify every identity and authoritative state.

### Exercise 3

Design binding and rotation for a database service used by human developers, workloads, CI, and an external partner. Cover identity, secret delivery, scope, expiry, overlap, revocation, and audit.

### Exercise 4

Design a federated marketplace across twelve brokers with restricted offerings, colliding names, varying API versions, stale catalogs, regional failure, quotas, and provider-specific plan semantics.

### Exercise 5

Design retirement of a deprecated stateful plan and its broker while 5,000 instances, 18,000 bindings, retained backups, long updates, and unknown orphan resources exist.

## Answers to the Exercises

### Answer 1

A marketplace is the governed discovery/lifecycle surface. An offering is a stable advertised capability; a plan is its governed operational/cost variant. A broker implements the platform-facing lifecycle protocol; a provider owns actual effects. A portfolio is an audience-specific product/constraint view.

An instance is one provisioned occurrence; an operation is one lifecycle request occurrence; a binding is a consumer-specific access/configuration relationship. Last-operation state reports asynchronous progress for an exact operation. Orphan mitigation discovers and disposes uncertain leftover provider effects. Maintenance revision binds requests to current advertised semantics.

Non-equivalences include offering $\ne$ instance; plan $\ne$ arbitrary parameters; instance $\ne$ binding; acceptance $\ne$ readiness; broker state $\ne$ provider truth; unbind $\ne$ deleting a local secret; and deprecation $\ne$ installed-instance deletion.

### Answer 2

The platform chooses immutable offering/plan IDs, stable instance ID, operation ID/token, request digest, owner/tenant/cost, and originating principal. It validates the exact plan/revision and bounded parameters and authorizes provision independently from discovery. It persists intent before calling a mutually authenticated broker.

The broker validates platform/context and maps instance/operation idempotently to a provider request. A 202 response includes stable broker operation identity; the platform records it and shows provisioning. Polling uses that exact operation with backoff/deadline and observed time.

If provider commits then broker crashes before recording completion, repeated provision uses the same instance and digest. Broker reconciles provider receipt/idempotency metadata and immutable provider ID, records/adopts the existing effect, and never generates a new instance identity. Mismatch becomes conflict/quarantine.

Terminal success requires broker/provider status plus plan readiness: reachable endpoint, required baseline, health, backup/security, or other contract checks. Provider owns existence/readiness facts; broker owns mapping/translation; platform owns request and marketplace operation state. Handoff records provider/broker references, plan revision, owner/support, binding next action, cost, and evidence.

### Answer 3

Create distinct binding IDs and scopes per consumer. Developers use federated, time-bounded user roles with MFA/approval appropriate to data; workloads use SPIFFE/provider workload identity; CI uses a dedicated workload identity scoped to migration/schema actions; the partner uses a separately governed federated identity or certificate restricted to required API/data scope and expiry.

The broker authorizes consumer-instance-tenant relationship and plan capability. Prefer provider-native grants and return secret-authority references plus endpoints. If a credential is unavoidable, deliver once into the secret store, redact all logs/history, bind request digest, and rotate on lost response rather than exposing retrieval broadly.

Rotation creates successor grant generation under stable rotation occurrence, publishes it, verifies each consumer can use it, observes adoption, then revokes predecessor by immutable provider grant ID. Define overlap and terminal deadline; prevent a retry from creating/revoking another generation. External partner overlap can be longer but is explicitly approved.

Unbind revokes at provider, verifies denial where safe, removes secret references, and records residual copies as risk. Emergency compromise revokes first and routes service impact. Audit includes requester/delegation, instance/binding/grant IDs, scope, provider result, secret reference—not value—expiry, rotations, and revocation evidence.

### Answer 4

Give every broker a stable identity, trust configuration, supported API range, owner, quotas, health, and isolation budget. Fetch catalogs independently with authentication, timeout, pagination/size bounds, schema validation, sanitization, ETag/revision, and last observation. Preserve last-known-good only within declared freshness and show degraded broker state.

Namespace offering/plan IDs by broker unless global uniqueness is verified; quarantine duplicate immutable IDs. Never merge colliding names. Store source provenance and expose plan comparison only over governed capability fields. Provider-specific guarantees remain namespaced extensions with documented consumers.

Apply authorization before broker ingestion enters user-visible search/index/count/facet/autocomplete. Portfolios select eligible offerings by tenant, region, classification, organization, and support. Provision authorization is separate and verifies current plan/revision. Regional broker outage cannot block unrelated indexes or operation workers; queues, credentials, circuits, and quotas are isolated.

Negotiate compatible protocol versions and retain adapters for installed instances. Reject catalog versions the platform cannot safely interpret. Measure catalog freshness, collisions, invalid products, API skew, provision health, quota/capacity, and restricted-data leaks. Test malicious metadata, one huge catalog, partial response, identity collision, stale removal, provider outage, and recovery.

### Answer 5

Stop new provisions and recommendation while keeping lifecycle APIs for installed instances. Build independent inventory joining immutable plan/instance/binding/operation/provider IDs, owner, consumer, data/backups, cost, version, status, last observation, and orphan candidates. Publish successor plans, end-of-support dates, migration paths, downtime/data/endpoint/credential impact, and exception policy.

Migrate cohorts with preview, backup, data verification, capacity reservation, replacement instance where necessary, binding successor creation/adoption, consumer cutover, old grant revocation, and rollback boundary. Long updates remain routed to compatible old broker workers until completion or governed recovery. Do not remove plan contract from catalog storage used for fetch/update/delete.

Investigate unknown orphans by operation tokens, provider receipts, immutable metadata, tenants, and request digests. Quarantine ambiguity; adopt legitimate resources or deprovision confirmed leftovers using idempotent original identities. Dispose retained backups and legal obligations separately from live instance count.

Reach verified zero for active instances, bindings/provider grants, in-progress/unknown operations, billable resources, retained data obligations, callbacks, consumers, exceptions, and recovery dependencies. Then revoke broker provider credentials, stop workers/routes, archive protected history/decoders, remove product from portfolios/indexes, and test restore without reactivating dispatch. Catalog invisibility alone proves none of these conditions.
