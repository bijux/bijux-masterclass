---
module_id: DE-090
program: Data Engineering
level: 2
module_number: 90
title: Making Data Discoverable Without Losing Control
status: complete
last_verified: 2026-09-03
---

# Making Data Discoverable Without Losing Control

## One-Page Review

### Governing question

How can people find, understand, evaluate, request, and safely use appropriate data while names, descriptions, schemas, tags, profiles, samples, lineage, search ranks, counts, access requests, and cached indexes remain governed information rather than an unprotected map of the organization?

### Essential definitions

- **Discoverability** is the ability of an authorized subject to locate and assess relevant data or data services for a stated purpose.
- A **cataloged resource** is a dataset, distribution, service, report, model, term, or other governed object represented by a stable identity and metadata record.
- **Metadata visibility** is permission to know a resource or metadata field exists; **data access** is permission to retrieve or act on its content. Neither automatically implies the other.
- A **discovery document** is the authorized search representation of a resource, containing only fields visible to its intended audience.
- **Faceted search** filters candidates by governed dimensions such as domain, owner, class, geography, freshness, quality, format, or access mode.
- **Vocabulary** provides governed terms and relations; a **synonym** connects search language; a **taxonomy** organizes broader/narrower concepts.
- A **metadata projection** selects or transforms catalog fields for one subject, purpose, tenant, and policy context.
- **Existence leakage** reveals that a protected resource, field, person, investigation, customer, project, or relationship exists.
- **Inference leakage** reveals protected facts through counts, ranks, facets, suggestions, profiles, samples, errors, timing, or repeated queries.
- An **entitlement** is a currently effective grant; an **access request** is a governed proposal that may be approved, denied, expired, revoked, or constrained.
- A **use obligation** is a condition attached to access, such as purpose, environment, aggregation, expiry, acknowledgment, or output review.
- **Policy-filtered retrieval** applies authorization to candidates and visible fields before ranking, aggregation, suggestion, preview, or response generation.
- **Freshness** is the age or lag of metadata relative to its authoritative source and stated objective.
- A **decision receipt** records the subject, purpose, candidates or stable query, policy/version, decision, field projection, time, reason, and outcome.

### Central model, mechanism, or theorem

Let $C(q)$ be resources matching query $q$, $Allow(s,r,p,t)$ authorize subject $s$ to discover resource $r$ for purpose $p$ at time $t$, and $Project(s,r,p,t)$ return authorized metadata fields. Safe retrieval is

$$
R(s,q,p,t)=Rank_q\left(\{Project(s,r,p,t):r\in C(q)\land Allow(s,r,p,t)\}\right).
$$

Authorization and projection occur before ranking, facet counts, spelling suggestions, snippets, embeddings, previews, or result totals. Otherwise those derived surfaces can disclose denied candidates. Data access is a separate decision:

$$
Discover(s,r,p,t)\not\Rightarrow ReadData(s,r,p,t).
$$

For authoritative metadata change time $t_a$ and effective searchable policy state $t_s$, exposure lag is $L=t_s-t_a$. A revocation objective must bound the entire propagation path—source, event, processor, index, cache, replica, and client—not merely the policy database update.

### Critical invariants

- Stable resource identity is separate from mutable name, location, owner, version, distribution, and search document.
- Every searchable field has an owner, source, classification, visibility policy, freshness objective, semantic version, and deletion behavior.
- Catalog metadata is classified; “metadata” never means “public” or “harmless.”
- Candidate authorization precedes rank, facets, totals, autocomplete, related-item expansion, embeddings, previews, samples, and generated answers.
- Resource visibility, field visibility, request eligibility, approval, data-plane access, output rights, and downstream reuse are distinct decisions.
- Search never offers a direct object lookup, alternate endpoint, stale cache, graph traversal, or export path that bypasses the same policy.
- Denied and nonexistent resources have intentionally designed error, timing, count, and suggestion behavior.
- Ownership, classification, lineage, schema, quality, freshness, and policy changes invalidate affected documents and caches within measured bounds.
- Search indexes contain only approved projections or enforce document- and field-level filtering that cannot be bypassed by aggregation APIs.
- Tenant, environment, geography, purpose, role, contract, consent, and time context are bound to requests and decisions.
- Preview and sample data use explicit safe generation, classification, row/column policy, size, watermark, expiry, and access evidence.
- Profiles suppress or coarsen small counts, rare values, extrema, free text, and linkable statistics according to risk.
- Access requests identify exact resource/version/scope, purpose, duration, requester, approvers, obligations, environment, and review/revocation.
- Grants expire and revoke automatically; materialization, extracts, notebooks, models, caches, and derived outputs remain governed after approval.
- Metadata mutations, search decisions, requests, approvals, uses, exports, policy changes, and exceptions are auditable without logging sensitive query contents unnecessarily.
- Unknown owner, class, policy, tenant, or index freshness fails to a governed restricted state, not broad discovery.
- Discovery quality is measured only within authorized populations; zero search results do not prove no resource exists.

### Common failures

Common failures include indexing every catalog field into one shared search cluster; filtering only after ranking; leaking denied resources through totals or facets; treating a hidden result as nonexistent while timing differs; revealing column names such as `fraud_investigation`; exposing rare profile values; publishing raw samples; assuming catalog permission grants warehouse access; granting access without purpose or expiry; copying data to an unmanaged notebook after approval; retaining stale documents after revocation; using ownerless resources as globally visible; embedding protected metadata in a vector index; letting direct-ID lookup bypass search filters; and measuring relevance on data users were never authorized to see.

### Compact example

A researcher searches for “regional treatment outcomes.” The catalog first resolves tenant, role, approved study purpose, geography, and policy version. It selects allowed resources, projects safe titles/descriptions and coarse quality/freshness fields, then ranks and computes facets. A restricted clinical dataset is absent from candidates, so its name, rare diagnosis columns, lineage, rank contribution, and result count do not leak. The researcher can discover an approved aggregate and request time-bounded data access; approval provisions access in a controlled workspace and records obligations. Discovery and use remain separate, attributable decisions.

### Connections

[DE-076](076-data-contracts.md) defines consumer-facing promises, [DE-081](081-technical-operational-and-business-metadata.md) supplies metadata classes, [DE-082](082-dataset-and-column-lineage.md) supplies dependency context, [DE-083](083-data-catalogs.md) supplies catalog architecture, [DE-084](084-ownership-and-stewardship.md) assigns decisions, [DE-085](085-classification-and-sensitive-data.md) classifies metadata and data, [DE-086](086-access-control-for-analytical-data.md) enforces analytical access, [DE-087](087-masking-tokenization-and-de-identification.md) constrains previews and profiles, [DE-088](088-retention-and-deletion.md) governs index and grant lifecycle, and [DE-089](089-auditability-and-provenance.md) makes discovery decisions reviewable. [DE-091](../ROADMAP.md) next examines serving stores and query engines.

## Governing Question

Data cannot create value if authorized users cannot find or interpret it. Yet discovery surfaces are themselves information systems. A dataset title can reveal an acquisition, a column can reveal a diagnosis or investigation, lineage can disclose a secret project, a profile can expose a rare person, and autocomplete can confirm a searched term. Hiding row values while exposing unrestricted metadata is not controlled discovery.

The opposite failure is a black-box catalog where users see nothing until they already know what to request. That drives duplicate pipelines, unofficial extracts, tribal knowledge, and broad standing access. The goal is progressive disclosure: reveal enough approved metadata to let a subject assess relevance and request access, then reveal richer metadata or data only as policy, purpose, and environment permit.

Discovery is not one authorization Boolean. A person may know a dataset exists but not see its schema; see a schema but not profiles; request access but not approve it; query governed views but not raw distributions; use results for one purpose but not export or train a model. Model these states explicitly and provide honest explanations without revealing protected policy inputs.

The governing question is therefore end to end: how are resources identified and described, fields classified, candidates authorized, results ranked, previews protected, requests fulfilled, grants revoked, copies governed, indexes refreshed, and evidence retained? Search quality and control quality must be designed together.

## Why This Matters

Discoverability shortens the path from question to trustworthy source. It reduces duplicate datasets, improves reuse of governed products, exposes ownership and quality, and makes contracts and lineage usable. Good discovery lets a consumer compare fitness before incurring access risk or approval cost.

Poor discovery creates two kinds of harm. Overexposure leaks strategy, personal data, security topology, investigations, commercial relationships, and regulated categories. Underexposure makes teams rebuild data, rely on stale extracts, or ask administrators for broad permissions. Both weaken governance.

Search infrastructure magnifies risk because it denormalizes metadata into caches, inverted indexes, embeddings, facets, click histories, and analytics. Revoking the source record may leave multiple searchable copies. Search queries and zero-result patterns can themselves reveal user intent or sensitive investigations.

Access workflows also define organizational behavior. If approval is slow, vague, and permanent, users route around it. If access is exact, purpose-bound, explainable, automated for low risk, reviewed for high risk, and self-expiring, control can improve usability. Friction should correspond to risk and uncertainty rather than organizational accident.

## Prerequisites and Retrieval

Retrieve resource metadata: stable IDs, canonical and alternate names, domain, owner/steward, descriptions, terms, schemas, versions, distributions/services, contracts, lineage, classifications, quality, freshness, temporal/geographic scope, licenses, rights, purposes, lifecycle, endorsements, deprecations, and access methods.

Retrieve subject and context: human and workload identity, tenant, role, team, attributes, training/acknowledgments, geography, contract, study/project, purpose, environment, device/session, time, approvals, entitlements, conflicts of interest, and break-glass status.

Retrieve discovery surfaces: browse pages, search API, direct lookup, autocomplete, spelling, facets, counts, snippets, highlights, related assets, lineage graph, schema browser, glossary, query history, popularity, recommendations, semantic/vector search, chat interface, exports, notifications, and analytics.

Retrieve data-bearing metadata: field names and comments, example values, min/max, distinct and null counts, histograms, sketches, top values, row counts, file paths, partitions, query text, tags, ownership, incidents, quality failures, contracts, access lists, and lineage endpoints. Classify each field independently.

Retrieve policy and lifecycle: candidate and field rules, request eligibility, approver resolution, obligations, provisioning, grants, expiry, recertification, revocation, deletion, holds, index/cache invalidation, backup, derived copies, and incident handling.

Retrieve operations: source events, crawl schedules, queues, document builders, policy engines, search clusters, vector stores, caches, replicas, clients, service accounts, failure modes, lag, dead letters, reindex, rollback, audit receipts, metrics, and adversarial tests.

Distinguish discoverability from access; resource visibility from field visibility; metadata from data; abstract dataset from distribution/service; match from authorized candidate; rank from authorization; empty from denied; request from grant; grant from effective enforcement; current entitlement from cached document; purpose from free-text justification; approval from unrestricted reuse; sample from harmless data; and personalization from permission.

Create a discovery control record:

| Concern | Required design evidence |
|---|---|
| Resource | Stable ID, type, version, domain, owner and lifecycle |
| Metadata | Field source, class, visibility, semantics and freshness |
| Candidate policy | Subject, tenant, purpose, environment, rule/version and deny behavior |
| Derived surfaces | Rank, facet, total, suggestion, relation, embedding and preview controls |
| Access workflow | Exact scope, purpose, approvers, obligations, provision, expiry and revoke |
| Propagation | Source change, event, index/cache/vector update, lag and reconciliation |
| Evidence | Query reference, decision receipt, request/grant/use and minimized audit data |

Write a falsifiable claim: “For tenant T and purpose P, every search surface resolves identity/context at policy Q17, filters resource candidates and field projections before ranking or aggregation, suppresses protected counts/suggestions, serves only index generation G whose classification and ownership inputs meet freshness S, reconciles source-to-index IDs, sends access request A to current accountable approvers, provisions bounded grant E into workspace W with obligations O, expires and revokes all enforcement points within L, and records minimized receipts without exposing denied objects or raw query secrets.”

## Learning Objectives

After completing this module, you should be able to:

1. distinguish catalog visibility, metadata-field visibility, request eligibility, approval, data access, output rights, and reuse;
2. inventory discovery surfaces and recognize existence, inference, profile, lineage, ranking, count, timing, and query-history leakage;
3. design stable resource identities, vocabularies, descriptions, semantic versions, ownership, quality, and freshness for useful retrieval;
4. apply candidate authorization and metadata projection before ranking, facets, totals, suggestions, embeddings, previews, or generation;
5. design safe samples, profiles, semantic search, recommendations, and explanations under classification and purpose;
6. implement purpose-bound, least-privilege, time-bounded access requests, approvals, provisioning, obligations, review, and revocation;
7. govern downstream workspaces, extracts, notebooks, models, caches, and exports after access is granted;
8. bound source-to-index revocation lag and reconcile document, cache, vector, replica, and client state;
9. measure discovery relevance within authorized populations alongside control coverage, lag, leakage, and request outcomes; and
10. test denied/nonexistent behavior, stale policy, cross-tenant isolation, inference, enumeration, compromised index, and lifecycle failure.

## Core Exposition

### Design useful metadata with stable semantics

Discovery begins with durable identity and meaning. Separate an abstract dataset from its versions, distributions, and access services. Names and locations change; stable IDs preserve bookmarks, policies, lineage, receipts, and deprecation. DCAT provides interoperable catalog, resource, dataset, distribution, service, rights, version, checksum, and relation concepts, but a vocabulary does not choose local visibility policy.

Descriptions should answer what the resource represents, grain, population, time and geography, important exclusions, owner, source, freshness, quality, permitted purposes, access path, and known limitations. Govern synonyms and business terms so search vocabulary evolves without rewriting resource identity. Record whether metadata is declared, harvested, inferred, profiled, or user-contributed.

Freshness is field-specific. A description can tolerate more lag than revocation, classification, or owner changes. Store authoritative source, observed time, version, and objective. Show staleness honestly and restrict a resource when control-critical metadata becomes unknown.

### Make authorization part of retrieval

Filter candidates before ranking. Post-filtering the top 20 of a global result set can return too few results, distort ranking, leak total matches, and permit side channels through latency or pagination. The authorization predicate must apply to every candidate page and direct lookup, while field projection removes unauthorized metadata before snippets or rendering.

Bind policy to subject, effective role, tenant, purpose, environment, geography, contract, resource version, and time. Use deny-by-default for unknown owner/class/policy. Cache decisions only with all relevant context and safe expiry/invalidation. Record policy/version and projection in a decision receipt.

Design denied versus nonexistent behavior intentionally. Identical responses reduce enumeration but can frustrate legitimate requests. A permitted coarse stub—“a restricted source may exist; contact steward role”—can enable progressive disclosure when policy allows. Never reveal the protected title merely to explain denial.

### Control derived search surfaces

Facets, result totals, ranking scores, spelling corrections, autocomplete, related resources, popularity, recent queries, and recommendations are computations over candidates. Compute them from the authorized set. A count of zero or one, a rank shift, or a suggested secret project name can leak even when documents are hidden.

Semantic search introduces embeddings, chunks, prompts, model providers, caches, and generated answers. Create embeddings only from authorized projections or partition them by policy domain; a query-time filter cannot remove secrets already encoded into shared generated text. Treat vector indexes and interaction logs as governed derived stores. Require citations to visible stable resources and authorize retrieval before generation.

Personalization should improve ordering among allowed candidates, not expand authority. Click history can reveal interests, medical conditions, investigations, or strategy; minimize it, restrict reuse, and provide retention controls. Do not train cross-tenant recommendations on protected interactions without explicit authority.

### Govern profiles and previews

Schema names and descriptions can be sensitive. Profiles are closer to data: minima, maxima, top values, distinct counts, histograms, sketches, null patterns, and rare categories can identify people or business events. Classify and project individual fields. Suppress small groups, coarsen ranges, exclude free text and direct identifiers, and assess repeated-query differencing.

Samples require a defined purpose and method. Synthetic examples can teach shape without disclosing rows but must not be labeled representative without validation. Masking may preserve linkability or rare values. Aggregated previews need thresholding and query budgets where inference risk exists. Watermark generated samples and give them their own version, expiry, owner, and provenance.

Preview authorization is separate from discovery and full access. A user might see safe schema and documentation, then request a controlled preview, then receive a governed view. Progressive stages reduce broad grants while making the request informed.

### Build access as a lifecycle

An access request names stable resource/version or governed view, requested operations and columns/rows, purpose, project, duration, environment, output/export needs, requester and workload, training/terms, and urgency. Resolve current owners and policy-based approvers; avoid approval by a stale catalog string or the requester alone.

Automate low-risk requests when evidence satisfies policy. Route exceptional, sensitive, conflicting, or novel use to accountable review. Provide approvers classification, purpose compatibility, lineage, downstream risk, current entitlements, environment, duration, and alternatives. Record reason, conditions, and policy—not merely an approval button.

Provision through idempotent workflows to every enforcement point. Verify effective row/column/view/workspace permissions rather than trusting a ticket state. Grants expire by default, recertify when justified, and revoke on owner/classification/purpose/role/employment/contract changes. Record incomplete provisioning and revocation as incidents by consequence.

### Govern use after approval

Approval does not end governance. Bind obligations to the accessible product and workspace: allowed purpose, approved consumers/workloads, storage, joins, aggregation, export, publication, model training, sharing, retention, attribution, and deletion. Make obligations machine-enforceable where possible and visible where human judgment remains.

Track governed derivatives through lineage and workspaces. An analyst who copies a dataset into a notebook, CSV, BI extract, feature set, or model creates new scope. Apply classification, access, retention, and export controls. Revoke source credentials and manage existing legitimate derivatives according to policy; do not assume revocation deletes them.

Offer safe product forms. A governed aggregate, clean room, query service, masked view, or purpose-specific data product may satisfy a need with less exposure than raw access. Product owners should design these alternatives from recurring requests rather than making every consumer negotiate custom exceptions.

### Keep indexes synchronized with governance

Map the propagation graph: authoritative catalog/policy change, event/outbox, queue, document projection, text and vector indexes, cache, replicas, browser/client cache, exports, and backups. Measure each segment. A source revocation is incomplete while stale search surfaces expose the resource.

Use stable source/version and document-generation IDs, monotonic or causally guarded updates, idempotent consumers, tombstones, replay, dead-letter handling, and full reconciliation. Late older updates must not resurrect deleted or restricted documents. Rebuilds apply current policy and tombstones before serving.

For high-risk changes, invalidate or deny immediately at a query-time policy layer even if background reindex takes longer. If the policy service is unavailable, choose fail-closed, bounded cached decisions, or risk-tier degradation explicitly. Never silently switch to unfiltered global search.

### Measure discovery and control together

Relevance metrics must use authorized judgments: success rate, time to useful resource, reformulation, zero-result rate, precision/recall at $k$, freshness, abandoned request, and reuse. Global relevance against hidden resources is not a valid user experience target.

Control metrics include resource, owner, classification, policy, field-visibility, and lifecycle coverage; source/index generation drift; revocation and update lag; orphan/stale documents; cross-tenant tests; unauthorized facet/suggestion/preview results; decision-cache age; request decision/provision/revoke latency; standing and expired grants; ungoverned derivatives; exceptions; and audit retrieval.

Test with canary resources that must never cross roles or tenants. Exercise exact name, prefix, typo, rare tag, facet, pagination, direct ID, graph traversal, related items, embedding similarity, generated response, timing, cache, export, stale update, rebuild, policy outage, role change, owner loss, classification upgrade, and deletion. Discovery is safe only across all interfaces.

## Definitions and Notation

Let $U$ be subjects, $D$ cataloged resources, $F(r)$ metadata fields of resource $r$, $P$ purposes, and $T$ time. Candidate authorization is $A:U\times D\times P\times T\rightarrow\{allow,deny,unknown\}$. Field visibility is $V(u,r,f,p,t)$, and projection is

$$
\Pi(u,r,p,t)=\{(f,value_r(f)):f\in F(r)\land V(u,r,f,p,t)=allow\}.
$$

For textual match function $M(q,r)$, safely ranked results are produced from $S=\{\Pi(u,r,p,t):M(q,r)\land A(u,r,p,t)=allow\}$. Every aggregate $g$, including counts and facets, must be $g(S)$ rather than $g(C(q))$ followed by document filtering.

Let change $c$ occur at authoritative time $t_0$, become enforced at source $t_1$, text index $t_2$, vector index $t_3$, cache $t_4$, and client $t_5$. Effective exposure lag is

$$
L(c)=\max(t_1,t_2,t_3,t_4,t_5)-t_0.
$$

If any state is unknown, $L$ is not proven bounded. Let $I_v$ be source-visible resource IDs at policy/version $v$ and $J_v$ served document IDs. Reconciliation requires $J_v\subseteq I_v$ for exposure safety; $I_v\setminus J_v$ measures discoverability loss, while $J_v\setminus I_v$ is unauthorized or stale exposure requiring urgent investigation.

## Mechanisms, Invariants, or Proof Structure

### Governed discovery mechanism

1. Inventory resources, discovery surfaces, metadata fields, derivatives, identities, purposes, policies, sources, owners, and lifecycle obligations.
2. Assign stable IDs; define typed metadata and vocabulary; classify each field; record source, semantics, version, confidence, and freshness.
3. Resolve subject, tenant, purpose, environment, policy/version, resource candidate decision, and field projection for every request.
4. Rank, count, facet, suggest, relate, embed, preview, or generate only over the authorized projected set.
5. Offer purpose-specific product forms and a precise access request with accountable approval, conditions, duration, and alternatives.
6. Provision idempotently at data/workspace/export enforcement points; verify effective permissions; propagate obligations and record receipts.
7. Track grants and derivatives; expire, recertify, or revoke them; apply current policy on rebuild/restore and prevent stale resurrection.
8. Propagate metadata/policy changes through all indexes and caches with versions, tombstones, lag objectives, reconciliation, and alerts.
9. Audit minimized query decisions, requests, approvals, provisioning, access, exports, changes, exceptions, and evidence access.
10. Measure authorized relevance and control coverage together; adversarially test every interface and remediate discovery/control debt.

### Safety and liveness claims

**Safety claim.** If every response-derived operation is computed exclusively over candidates for which current $A=allow$ and fields for which current $V=allow$, no bypass surface exists, and caches/indexes are consistent with that state, then the discovery service does not disclose denied catalog fields through its represented outputs.

**Proof sketch.** Candidate construction excludes denied resources; projection excludes denied fields; closure requires rank, aggregate, suggestion, preview, graph, and generation to consume only that projected set. Therefore represented outputs contain no denied input. Timing, resource consumption, compromised components, external knowledge, and statistical inference require additional controls and keep the claim conditional.

**Liveness claim.** If every relevant resource has a stable identity, sufficient authorized description, reachable owner or automatable policy, and an eventually available request/provisioning path, then an authorized consumer can eventually discover or obtain a reasoned route to an appropriate resource.

**Proof sketch.** Indexing makes the authorized projection reachable; retrieval ranks it for matching queries; the request path terminates in grant, deny with governed reason, alternative, or escalated exception. Missing ownership, vocabulary, metadata, policy, or service availability breaks liveness and becomes measured debt.

### Executable policy-filtered search

This deterministic fixture filters resource and field visibility before ranking and counting. It illustrates a small policy invariant, not production authorization, inference resistance, or search relevance.

<!-- bijux-verify: {"id":"policy-filtered-catalog-search","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"visible_count=2\nvisible_ids=public-health,regional-outcomes\nsecret_visible=false\nall_fields_allowed=true\n","stderr":""}} -->
```python
resources = [
    {"id": "public-health", "text": "regional public outcomes", "visibility": "all", "secret": "no"},
    {"id": "fraud-case", "text": "regional investigation outcomes", "visibility": "restricted", "secret": "yes"},
    {"id": "regional-outcomes", "text": "regional treatment outcomes", "visibility": "research", "secret": "no"},
]
subject_groups = {"all", "research"}
query_terms = {"regional", "outcomes"}


def allowed(resource: dict[str, str]) -> bool:
    return resource["visibility"] in subject_groups


def score(resource: dict[str, str]) -> int:
    return len(query_terms.intersection(resource["text"].split()))


candidates = [resource for resource in resources if allowed(resource)]
ranked = sorted(candidates, key=lambda resource: (-score(resource), resource["id"]))
visible = [{"id": resource["id"], "text": resource["text"]} for resource in ranked]

print(f"visible_count={len(visible)}")
print("visible_ids=" + ",".join(resource["id"] for resource in visible))
print(f"secret_visible={any(resource['id'] == 'fraud-case' for resource in visible)}".lower())
print(f"all_fields_allowed={all(set(resource) == {'id', 'text'} for resource in visible)}".lower())
```

## Alternatives and Trade-Offs

1. **Global catalog versus domain catalogs.** Global search improves reuse; domain ownership preserves semantics. Federated projections can combine both but need stable identity and policy interoperability.
2. **Hide resource versus expose a stub.** Hiding reduces existence leakage; a coarse stub supports legitimate requests. Choose by classification and threat, not one universal rule.
3. **Index-time versus query-time filtering.** Separate indexes reduce accidental exposure; query-time policy handles dynamic context. Defense in depth costs more synchronization and testing.
4. **Keyword versus semantic search.** Keywords are interpretable and cheap; semantic retrieval handles concepts but introduces embeddings, providers, opacity, and new leakage surfaces.
5. **Profiles versus documentation only.** Profiles improve fitness assessment but approach data disclosure. Use risk-based suppression, coarse summaries, or controlled previews.
6. **Synthetic versus masked samples.** Synthetic data may reduce direct disclosure but misrepresent distributions; masking can retain linkage and rare values. Neither is automatically safe or representative.
7. **Manual versus automated approval.** Manual review handles nuance but creates delay and inconsistency. Policy automation scales known low-risk patterns; exceptions need accountable humans.
8. **Standing versus just-in-time grants.** Standing grants reduce friction but accumulate. Time-bound grants improve least privilege while requiring reliable renewal and revocation.
9. **Central versus owner approval.** Central review standardizes risk; owners know purpose and semantics. Policy can assign both without creating indefinite serial queues.
10. **Rich explanations versus non-disclosure.** Explanations build trust, but rule inputs can reveal hidden facts. Provide safe reason categories and escalation routes.
11. **Popularity ranking versus quality/fitness ranking.** Popularity reinforces existing access and can reveal behavior; quality and purpose fitness better support governed reuse but require metadata maintenance.
12. **Immediate deny on stale state versus bounded degraded service.** Fail-closed protects high-risk resources; cached decisions preserve availability. Risk-tiered explicit bounds avoid silent fail-open.

## Failure Modes and Misconceptions

1. **“Metadata is harmless.”** Names, schemas, tags, lineage, profiles, owners, and incidents can be highly sensitive.
2. **“Discoverable means readable.”** Catalog and data permissions are separate.
3. **“Readable once means reusable forever.”** Purpose, duration, output, sharing, and retention obligations continue.
4. **“Filter the final page.”** Rank, totals, facets, timing, and missing slots may already leak denied candidates.
5. **“Field filtering is enough.”** Resource existence and relationships can still be protected.
6. **“A 404 prevents enumeration.”** Timing, totals, autocomplete, and direct-ID patterns can distinguish states.
7. **“Profiles contain no rows.”** Rare values, extrema, counts, and combinations can identify subjects.
8. **“Masked samples are anonymous.”** Linkability, rare values, and auxiliary data may preserve identity.
9. **“Embeddings cannot reveal source text.”** Treat vector stores and generated outputs as governed derived data.
10. **“Personalization only changes order.”** It can reveal other users' interests or protected resources.
11. **“Ownerless data should remain open.”** Missing accountability is uncertainty and should restrict exposure.
12. **“Approval in a ticket equals access.”** Provisioning can fail or overgrant; verify enforcement state.
13. **“Revoking the role removes every copy.”** Extracts, notebooks, caches, models, and backups need lifecycle handling.
14. **“The source changed, so search changed.”** Index, vector, replica, and client caches can remain stale.
15. **“Reindexing is harmless.”** A rebuild can resurrect deleted documents if current tombstones/policy are absent.
16. **“Zero results means no data exists.”** Denial, vocabulary, metadata, freshness, or index failure may explain it.
17. **“High click-through proves relevance.”** Ranking position, standing access, and popularity bias confound it.
18. **“All users need the same description.”** Field projections may differ by tenant, purpose, and role.
19. **“A free-text purpose is a policy.”** Purpose needs governed vocabulary, evidence, binding, expiry, and review.
20. **“Catalog admins may see everything.”** Least privilege, separation, and audit apply to metadata administrators.
21. **“Lineage should always be public internally.”** It can reveal protected inputs, projects, incidents, or topology.
22. **“Search logs are ordinary telemetry.”** Queries reveal intent and sensitive topics and need minimization/lifecycle.
23. **“A deny needs no explanation.”** Safe reason categories and routes reduce circumvention and duplicate requests.
24. **“Control friction is always security.”** Arbitrary delay drives shadow copies; friction should match risk.

## Worked Examples

### Example 1

**Situation.** A global facet says “investigations (1)” although its only resource is denied. **Reasoning.** Compute facets after candidate authorization or suppress them; post-filtering documents is too late. **Conclusion.** Aggregates are disclosure surfaces.

### Example 2

**Situation.** A public title is safe, but columns reveal acquisition code names. **Reasoning.** Project the title and owner route while withholding schema and lineage until a stronger purpose-bound stage. **Conclusion.** Visibility is field-granular.

### Example 3

**Situation.** A classification changes from internal to restricted. **Reasoning.** Query-time policy denies immediately; versioned events invalidate text/vector indexes and caches; reconciliation detects remaining documents. **Conclusion.** Revocation latency spans the whole propagation graph.

### Example 4

**Situation.** A health profile exposes a category count of one. **Reasoning.** Suppress or coarsen small groups, restrict repeated queries, and offer a governed aggregate preview. **Conclusion.** Statistics can disclose individuals without rows.

### Example 5

**Situation.** Semantic search cites a resource the user cannot open. **Reasoning.** The shared embedding corpus included protected text. Rebuild from authorized projections or policy partitions and authorize retrieval before generation. **Conclusion.** A final link filter cannot retract generated leakage.

### Example 6

**Situation.** A contractor requests raw data for a three-week analysis. **Reasoning.** Policy approves a narrower view in a controlled workspace, binds purpose/export restrictions, expires the grant, and tracks derivatives. **Conclusion.** The safest useful product may differ from the requested resource.

### Example 7

**Situation.** An approval ticket is closed, but one warehouse role failed to provision and another gained all columns. **Reasoning.** Reconcile requested entitlements with effective grants, correct both outcomes, and retain per-target receipts. **Conclusion.** Workflow state is not enforcement truth.

### Example 8

**Situation.** A departed employee's search cache still returns titles. **Reasoning.** Role change invalidates policy decisions, server caches, tokens, and client state within a measured bound; sensitive results fail closed. **Conclusion.** Identity lifecycle is part of discovery freshness.

### Example 9

**Situation.** An ownerless legacy table ranks highly by popularity. **Reasoning.** Missing owner/classification/policy puts it in restricted remediation, while users receive governed alternatives and an escalation route. **Conclusion.** Popularity cannot substitute for accountability.

### Example 10

**Situation.** Search quality falls after least-privilege filtering. **Reasoning.** Evaluate recall against resources the subject may discover, improve synonyms and descriptions, and create safe product forms. Do not restore hidden candidates to inflate metrics. **Conclusion.** Relevance and authority share the same eligible population.

## Cross-Program Connections

- [DE-076](076-data-contracts.md) makes descriptions, semantics, quality, freshness, and use conditions consumer-facing commitments.
- [DE-081](081-technical-operational-and-business-metadata.md) distinguishes metadata classes and authoritative sources.
- [DE-082](082-dataset-and-column-lineage.md) enriches discovery while requiring protected graph projection.
- [DE-083](083-data-catalogs.md) provides catalog ingestion, identity, search, glossary, stewardship, and operating foundations.
- [DE-084](084-ownership-and-stewardship.md) assigns request, exception, metadata, and remediation authority.
- [DE-085](085-classification-and-sensitive-data.md) classifies every search field, index, profile, sample, query log, and derivative.
- [DE-086](086-access-control-for-analytical-data.md) supplies subject/action/object/context decisions and enforcement at data/query layers.
- [DE-087](087-masking-tokenization-and-de-identification.md) bounds claims about previews, profiles, pseudonyms, and synthetic examples.
- [DE-088](088-retention-and-deletion.md) governs documents, embeddings, grants, query histories, derivatives, caches, backups, and tombstones.
- [DE-089](089-auditability-and-provenance.md) supplies decision receipts, completeness, tamper evidence, and investigation custody.
- [API-017](../../28-api-and-service-engineering/modules/017-filtering-sorting-and-pagination.md) applies typed filter and pagination contracts; [API-034](../../28-api-and-service-engineering/modules/034-authorization-checks.md) reinforces authorize-before-response behavior.
- [DE-091](../ROADMAP.md) turns discovered products into governed query and serving choices.

## References

- World Wide Web Consortium, *Data Catalog Vocabulary (DCAT) — Version 3*, W3C Recommendation, 2024. <https://www.w3.org/TR/vocab-dcat-3/>
- National Institute of Standards and Technology, *Security and Privacy Controls for Information Systems and Organizations*, SP 800-53 Rev. 5 Update 1, 2020. <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>
- Amazon Web Services, “What Is Amazon DataZone?”, current documentation. <https://docs.aws.amazon.com/datazone/latest/userguide/what-is-datazone.html>
- Amazon Web Services, “What Is AWS Lake Formation?”, current documentation. <https://docs.aws.amazon.com/lake-formation/latest/dg/what-is-lake-formation.html>
- Apache Software Foundation, “Apache Atlas Architecture,” version 2.0 documentation. <https://atlas.apache.org/2.0.0/Architecture.html>
- OpenMetadata Authors, “Data Discovery,” current documentation. <https://docs.open-metadata.org/latest/how-to-guides/data-discovery>
- DataHub Project, “Search,” current documentation. <https://docs.datahub.com/docs/how/search>
- Open Policy Agent Authors, “Policy Language,” current documentation. <https://www.openpolicyagent.org/docs/policy-language>
- OWASP Foundation, “Authorization Cheat Sheet,” current guidance. <https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html>
- National Institute of Standards and Technology, *Attribute Based Access Control*, SP 800-162, 2014. <https://csrc.nist.gov/pubs/sp/800/162/upd2/final>

## Exercises

### Exercise 1

Distinguish resource, dataset, distribution, service, catalog record, discovery document, metadata visibility, request eligibility, entitlement, and data access. Give one example where each distinction prevents a control or usability error.

### Exercise 2

A query matches 100 resources. Policy allows 30; only 24 have an allowed description, owner, and current classification. A post-filter system ranks all 100, returns the first 10, then hides seven. Compare it with pre-filter/projection behavior and define honest result and coverage measures.

### Exercise 3

Design a safe catalog experience for clinical research containing restricted names, sensitive schemas, profiles, lineage, semantic search, samples, and access requests. Cover progressive disclosure, inference controls, purpose, workspace obligations, expiry, and evidence.

### Exercise 4

A restriction change reaches the policy service in 10 seconds, text index in 4 minutes, vector index in 12 minutes, server cache in 3 minutes, and client cache in 20 minutes. Compute effective exposure lag, identify the controlling path, and design immediate containment plus durable reconciliation.

### Exercise 5

A merged company has three catalogs, duplicate IDs, conflicting terms, stale owners, 8,000 unclassified resources, permanent grants, and unknown notebook copies. Design a recovery that improves discovery without exposing unknowns or freezing all legitimate work. Define completion metrics.

## Answers to the Exercises

### Answer 1

A **resource** is the broad cataloged object; a **dataset** is an identifiable collection; a **distribution** is an accessible representation such as a file; a **service** provides access or processing; and a **catalog record** describes the resource and its catalog history. Separating them prevents one file URL or catalog-edit date from being mistaken for dataset identity or content freshness.

A **discovery document** is the indexed authorized projection, not the authoritative catalog record. **Metadata visibility** permits specific descriptive facts; **request eligibility** permits proposing access; an **entitlement** is an effective grant; **data access** is the enforcement decision on an operation. These prevent a searchable title from granting a download, a request button from promising approval, a ticket approval from being confused with warehouse enforcement, and a stale search document from overriding current policy.

### Answer 2

Post-filtering ranks denied candidates and can leak their existence through rank changes, totals, latency, missing slots, facets, or pagination. It returns only three visible items even though more allowed resources may exist below the global top ten. Pre-filtering selects 30 allowed candidates, projects permitted fields, excludes or restricts six without minimum discovery metadata, and ranks the 24 usable projections. It can return ten authorized useful items without processing denied candidates into response-derived surfaces.

Report `matched_authorized=30`, `discoverable_projection=24`, `metadata_blocked=6`, and up to 24 results, but expose these counts to the requester only if count policy permits. Metadata readiness coverage is $24/30=80\%$ for the authorized population. Relevance is evaluated against those 24, while the six gaps create owner/classification remediation. Never report the global 100 to an unauthorized subject.

### Answer 3

Begin with coarse approved domain and aggregate descriptions. Resolve identity, institution, study purpose, geography, training, agreements, and policy. Candidate-filter before rank/facets/suggestions; project names, schemas, lineage, quality, and profiles field by field. Hide restricted existence where necessary and offer safe steward routes. Suppress small profile cells, rare categories and extrema; budget repeated aggregate previews. Generate synthetic shape examples with clear nonrepresentative labeling or controlled masked samples only after separate assessment.

Build embeddings from approved projections in policy partitions, authorize retrieval before generation, and cite only visible stable resources. A request specifies study, resource/view, fields/cohort, operations, duration, workspace, collaborators, export/publication, and model use. Accountable data and privacy roles approve or offer a safer view. Provision a controlled workspace with row/column constraints, egress/output review, monitoring, expiry, deletion, and derivative lineage. Evidence records minimized search decisions, policy/version, request, approval/reason, effective grants, queries/exports, recertification/revocation, and lifecycle receipts without copying clinical content.

### Answer 4

Effective exposure lag is the maximum path time: $L=20$ minutes, controlled by client cache. The 10-second policy update is not the completion time. Immediately make the query-time policy service deny the resource, revoke download/query grants as applicable, purge high-risk server/client cache keys or invalidate their generation, disable semantic generation for the resource, and alert if a surface cannot honor current policy.

Durably emit a versioned restriction event and tombstone; update text/vector documents, caches, replicas, suggestions, facets, related graphs, and exports idempotently; reject late older updates; and reconcile every served document ID/version against the authoritative visible set. Measure each segment, require acknowledgments, inspect dead letters, run canary searches across roles/tenants/interfaces, and keep incident status until no unauthorized or unknown served state remains. Redesign client caching so sensitive policy changes meet a shorter explicit maximum.

### Answer 5

Establish a cross-catalog identity mapping without prematurely merging ambiguous resources. Preserve source IDs and versions; define canonical IDs only after ownership and equivalence review. Federate authorized projections while harmonizing a governed core vocabulary and retaining domain-specific terms, synonyms, provenance, and conflict flags.

Restrict the 8,000 unknown-class/owner resources from broad discovery and new grants, but inventory and prioritize them by observed use, sensitivity signals, exposure, business criticality, and lineage. Existing legitimate access continues under monitored time-bounded exceptions where risk owners approve; high-risk unknowns fail closed. Assign remediation owners, classify fields and profiles, reconcile policies, and provide users safe alternatives and escalation rather than silent zero results.

Inventory effective grants at every enforcement point, map them to purpose/owner/resource, expire or recertify in risk cohorts, and stop creating permanent grants. Scan workspace, query, lineage, storage, endpoint, and export evidence for notebooks and copies; register, contain, classify, retain, or dispose under policy. Rebuild indexes from authorized projections with tombstones and cross-tenant canaries.

Measure identity resolution and duplicate/conflict rates; resource, owner, classification, policy and field-visibility coverage; stale/orphan documents; index generation and revocation lag; vocabulary/search success within authorized populations; permanent grants and effective-grant drift; request/provision/revoke time; known and unknown derivatives; exception age; cross-tenant/leakage tests; and incidents. Completion means every active resource and discovery field has stable identity, accountable ownership, classification, current policy, bounded propagation, governed access lifecycle, and reconciled derivatives—or a named, time-bounded, approved exception.
