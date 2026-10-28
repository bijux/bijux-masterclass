---
module_id: DE-083
program: Data Engineering
level: 2
module_number: 83
title: Data Catalogs
status: complete
last_verified: 2026-09-03
---

# Data Catalogs

## One-Page Review

### Governing question

How can an organization build and operate a data catalog that helps authorized people and systems discover, evaluate, access, use, govern, and retire the right data product, while preserving source provenance, temporal state, security boundaries, and uncertainty rather than equating inventory, popularity, a search rank, a certification badge, or a stale indexed page with fitness for use?

### Essential definitions

- A **data catalog** is a governed discovery and workflow product over metadata entities, assertions, relationships, evidence, and actions.
- A **catalog entity** is a stably identified domain, product, dataset, distribution, field, term, contract, owner role, policy, quality result, lineage edge, consumer, or related object.
- A **source assertion** is provenance-bearing metadata collected or curated from an authoritative or evidentiary source.
- A **catalog projection** is a query/search/page-oriented view derived from source assertions; it is not automatically a source of record.
- A **search document** is an authorization-scoped index representation used for retrieval and ranking.
- **Eligibility** is the noncompensable set of conditions a result must satisfy for a user's stated purpose, environment, time, classification, and operational requirements.
- **Ranking** orders eligible results using lexical, semantic, structural, behavioral, or policy signals; it does not establish eligibility.
- **Fitness for use** is a context-specific conclusion based on meaning, technical compatibility, current operational evidence, policy, and consumer requirements.
- **Certification** is a versioned policy decision with scope, authority, evidence, validity interval, and revocation—not a timeless badge.
- A **catalog workflow** coordinates stewardship, ownership, access, issue, contract, deprecation, certification, or policy action with state and evidence.
- **Federated cataloging** distributes metadata ownership among domains while sharing identity, interoperability, discovery, and governance contracts.
- **Index lag** is the delay between authoritative metadata change and searchable projection visibility.
- A **zero-result event** may indicate no matching authorized asset, vocabulary mismatch, stale/incomplete coverage, or hidden results; it must not leak which.
- **Search quality** measures usefulness using judged relevance, task success, reformulation, abandonment, time-to-safe-use, and downstream outcomes—not clicks alone.
- **Active catalog behavior** proposes or performs bounded external actions from metadata, subject to current authorization, version checks, idempotency, and audit.

### Central model, mechanism, or theorem

For user/context $u$ and query/use $q$, authorize and filter before ranking:

$$
C(q,u)=\{e\in E:Authorized(u,e)\land Eligible(e,q,u)\}.
$$

Then return $Rank(C(q,u),q,u)$. Eligibility may require business meaning, environment, contract, freshness, quality, classification, and interface compatibility. Ranking signals such as popularity cannot compensate for failed eligibility. A popular stale legacy orders table must not outrank into selection when the use requires a current, contracted, quality-approved product.

### Critical invariants

- Stable entity identity, environment/tenant, version, lifecycle, and physical incarnation remain distinct from display names and URLs.
- Source assertions retain origin, authority, collector/curator, valid/observation time, confidence, and protection; the index is a rebuildable projection.
- Authorization applies before retrieval, ranking, facets, counts, autocomplete, graph traversal, recommendations, and error construction.
- Eligibility constraints are explicit and noncompensable; rank never converts an ineligible asset into a suitable one.
- Search results expose why they matched, their environment/version, meaning, owner, operational condition, warnings, coverage, and evidence age.
- Technical, operational, and business metadata appear together without flattening their different authorities and clocks.
- Certification, endorsement, deprecation, warning, incident, and quality states identify policy/evidence version, scope, issuer, validity, and revocation.
- A catalog links to access workflows but does not imply that discovery grants underlying data access.
- Access requests bind exact product/distribution/version, purpose, requester, policy, approvers, decision, expiry, and enforcement receipt.
- Owners and stewards are durable roles with effective assignments, escalation, and orphan detection.
- Search/index freshness and source coverage are visible; stale or missing sources cannot silently appear current/complete.
- Zero results and filtered results use nonleaking semantics while providing safe recovery paths.
- Popularity, clicks, recent queries, inferred tags, and generated descriptions are behavioral/inferred signals, not proof of quality or authorization.
- Query text, result clicks, access requests, lineage, samples, classifications, and owner identities are themselves sensitive metadata.
- Catalog APIs have versioning, pagination, consistency, filtering, authorization, deletion, rate-limit, and bulk-export contracts.
- External actions re-read source/current policy and use preconditions, bounded scope, idempotency, receipts, and recovery.
- Deprecation/retirement includes replacements, consumer discovery, migration state, deadlines, policy changes, interfaces, aliases, and audit history.
- Success is measured by safe decision outcomes and coverage, not entity count, filled fields, monthly active users, or visual polish alone.

### Common failures

Common failures include building only a crawler inventory; treating the index as authoritative; merging environments; letting names define identity; returning stale badges; ranking popularity before fitness; authorizing after retrieval; leaking restricted existence through facets; showing “owner” without effective role; accepting one-line business definitions; confusing discovery with permission; hiding unresolved metadata conflicts; showing green quality without generation/policy; linking lineage without version or coverage; using clicks as relevance truth; letting generated descriptions overwrite curators; creating permanent access; allowing automation from stale pages; and declaring success from catalog adoption while users still export the wrong data.

### Compact example

A query for “current production orders product” matches `warehouse.legacy_orders` and `finance.orders_product`. The legacy table has ten times more historical queries, so popularity-only ranking selects it. It is stale, uncertified, and lacks the current contract. Eligibility filtering first removes it; the catalog then ranks the current contracted and quality-approved `finance.orders_product`. Popularity remains visible as use evidence, not trust.

### Connections

[DE-049](049-run-metadata-and-operational-state.md) supplies current run/publication evidence, [DE-066](066-time-travel-and-reproducible-reads.md) supplies versioned reads, [DE-074](074-freshness-and-timeliness.md) supplies temporal fitness, [DE-076](076-data-contracts.md) supplies interface obligations, [DE-077](077-producer-and-consumer-responsibilities.md) supplies roles, [DE-078](078-data-incident-detection-and-triage.md) supplies warnings/incidents, [DE-080](080-building-quality-gates-for-a-data-product.md) supplies trust decisions, [DE-081](081-technical-operational-and-business-metadata.md) supplies assertions and authority, and [DE-082](082-dataset-and-column-lineage.md) supplies dependency graphs. DE-084 deepens ownership and stewardship.

## Governing Question

The visible catalog interface is search and entity pages, but the hard system lies underneath: identity resolution, source collection, temporal assertions, authorization, indexing, ranking, graph traversal, stewardship, access integration, workflow state, and operational reliability. A fast search box over stale or ambiguous metadata makes the wrong asset easier to find.

Different users bring different tasks. An analyst asks which table answers a business question. An engineer needs schema and lineage for a change. An incident responder needs the exact affected generation. A privacy specialist needs fields and exports. A finance owner needs a certified definition and control evidence. One generic list sorted by popularity cannot serve these jobs safely.

Catalogs also sit at an information boundary. Even when a user cannot read underlying data, names, descriptions, field lists, classifications, lineage, samples, queries, consumers, and existence can disclose sensitive facts. Search authorization must be structural, not a UI afterthought.

The governing requirement is a catalog as a trustworthy decision workflow: preserve authoritative evidence, understand task/context, authorize and filter eligibility, explain rankings and uncertainty, connect to governed actions, and measure whether users reach safe outcomes.

## Why This Matters

Data organizations lose enormous time rediscovering tables, asking who owns them, reverse-engineering definitions, and learning too late that a familiar dataset is deprecated or stale. Good catalogs reduce search and coordination cost while making quality, lineage, contracts, and policy visible at the decision point.

The cost of the wrong discovery can exceed the cost of no discovery. Similar names and schemas hide different grains, currencies, event times, populations, or legal purposes. A popular legacy table can dominate behavioral ranking long after a governed replacement exists.

Catalogs create a feedback loop. Search behavior reveals vocabulary gaps; access requests reveal demand; incidents reveal missing warnings; lineage reveals shared dependencies; deprecations reveal migration needs. Those signals improve the system only when they are interpreted with coverage and bias, not treated as unquestioned ground truth.

Catalogs become control planes when they launch access, certification, issue, quality, contract, and retirement workflows. That increases leverage and blast radius. Current-state checks, authorization, separation of duties, idempotency, and receipts are required before metadata can safely trigger change.

Finally, catalog usefulness decays if collection, indexing, and stewardship fail. Availability alone is insufficient: a page can load while its owner, quality, lineage, or freshness is weeks stale. Operability needs source-to-index freshness and semantic correctness objectives.

## Prerequisites and Retrieval

Retrieve user jobs: discovery questions, change impact, incident response, compliance, access, reuse, certification, cost, retirement, frequency, urgency, consequence, and current work surfaces.

Retrieve entity model: domain/product/dataset/distribution/field/job/run/term/contract/policy/owner/consumer IDs, aliases, environments, tenants, versions, relationships, lifecycle and merge/split/move history.

Retrieve sources: database/object/schema catalogs, transformation manifests, lineage/run events, quality/freshness/reconciliation, contracts, glossary, identity/ownership, policies/classifications, access logs, costs, incidents, dashboards/models/reports, and curated attestations.

Retrieve authority/provenance: source of record by predicate/scope, collector/curator/version, valid and observed time, confidence, conflict state, freshness expectation, evidence link, and protection.

Retrieve search needs: languages, synonyms, acronyms, term IDs, exact IDs, structured filters, semantic queries, field boosting, spelling, facets, recommendations, saved searches, explainability, pagination, and zero-result recovery.

Retrieve eligibility/ranking: business concept, grain/unit/time/population, environment, contract/certification, operational state, freshness/quality, classification/purpose, interface, cost, criticality, popularity, and user/team context.

Retrieve workflow: access enforcement systems, issue/stewardship queues, owner escalation, certification authority, exceptions, approvals, expiry, deprecation, notifications, action receipts, and recovery.

Retrieve security/privacy: catalog visibility, attribute/relationship filtering, tenant isolation, hidden-result behavior, query/click logging, sample/query redaction, bulk export, cache scope, audit, retention, deletion, and inference risks.

Retrieve operations: source coverage/lag, ingestion errors/dead letters, graph/index lag, API/search latency/availability, stale cache, authorization health, queue backlog, recovery objectives, and disaster rebuild.

Distinguish entity from search document; source assertion from projection; match from fitness; eligibility from rank; popularity from trust; certification from timeless truth; discovery from data access; owner role from person; zero results from no existing asset; click from successful use; current page from current source; active proposal from authorized action; and catalog adoption from safe outcome.

Create a catalog result contract:

| Concern | Required evidence and behavior |
|---|---|
| Query | Text/ID/filters, intended use, environment, time and user context |
| Authorization | Principal, tenant, purpose, policy/version and filtered surfaces |
| Identity | Stable entity/distribution/version, aliases and lifecycle |
| Eligibility | Meaning, technical fit, operational state, policy and evidence |
| Rank | Signals, weights/model/version, explanation and uncertainty |
| Result | Definition, owner, schema/interface, freshness/quality, lineage, warnings |
| Access | Separate entitlement state, request target/purpose/expiry and receipt |
| Freshness | Source observation, index build, cache and staleness/gap indicators |
| Feedback | Reformulation/click/request/use/outcome with bias and protection |
| Action | Preconditions, authority, preview, scope, idempotency and receipt |

Write a falsifiable claim: “For authenticated context U7 and use Q3, catalog snapshot C91 evaluates 1,240 authorized entities, filters 38 technical matches to three semantically and operationally eligible products under policy P8, ranks them with model R4 while exposing matched concept/contract/freshness/quality evidence, selects product D17 generation G42, routes purpose-bound access request A5 to enforcement system Z2 without claiming access, and records source/index lag, result explanation, and downstream successful-use confirmation while restricted entities remain nonobservable.”

## Learning Objectives

After completing this module, you should be able to:

1. define a data catalog as a governed discovery/workflow product rather than a crawler inventory;
2. design an architecture from provenance-bearing assertions through graph/current projections and authorization-scoped search indexes;
3. separate authorization, eligibility, ranking, certification, access, and actual use;
4. design catalog entity pages and APIs that expose meaning, versions, operations, lineage, quality, ownership, warnings, and evidence limits;
5. build lexical, semantic, structured, graph, and behavioral discovery without treating popularity as trust;
6. handle source/index lag, conflict, incomplete coverage, zero results, and nonleaking authorization;
7. integrate stewardship, access, certification, issue, deprecation, and retirement workflows safely;
8. protect sensitive metadata, search behavior, samples, relationships, bulk exports, and caches;
9. measure relevance, task success, time-to-safe-use, escaped misuse, source coverage, and operational reliability; and
10. test catalog ranking, authorization, freshness, workflows, rebuild, and active actions under adversarial conditions.

## Core Exposition

### Begin with user decisions and a stable entity model

Inventory is a means, not the outcome. Interview and observe users completing high-value jobs: finding a governed metric, choosing an event source, changing a field, responding to an incident, requesting access, migrating a deprecated product, or tracing sensitive data. Record decision criteria and failure consequences.

Model stable entities before indexing text. Separate logical products from physical distributions, datasets from versions, jobs from runs, terms from labels, owner roles from people, and certification decisions from colored badges. Include environment and tenant in identity.

Connect entities with typed temporal relationships. A product `hasDistribution`, a field `implementsConcept`, a run `producesGeneration`, a contract `governsProduct`, a role `ownsScope`, a consumer `usesDistribution`, and a product `supersedesProduct`. Preserve provenance and effective intervals.

Support aliases, redirects, moves, merges, and splits without silent identity collapse. A familiar table name may resolve to a deprecated incarnation while the logical product has moved. Search should guide migration while retaining history.

### Build assertions first and projections second

Collect technical, operational, and business assertions from their appropriate sources. Preserve origin, authority, collector/curator, valid/observation time, confidence, classification, and conflict. Do not let the search index become the only copy of meaning.

Use an assertion/entity graph or equivalent governed metadata store as the integration layer. Build current views, entity documents, relationship indexes, aggregates, recommendations, and search documents as reconstructable projections. Record source and projection versions.

Event ingestion improves freshness; periodic snapshots and reconciliation recover missed changes. Make collectors idempotent and replayable. Quarantine malformed events and expose permission/coverage gaps. Index updates use stable entity/version keys and tombstones.

When sources disagree, show material conflicts and resolution state. A contract may declare an owner and schema while identity service says the group is empty and the warehouse observes a different type. One current page can explain each claim rather than selecting the most recent blindly.

### Authorize every discovery surface

Determine catalog visibility policy separately from underlying data permission. Some assets may be discoverable but not readable; others must be undiscoverable. Apply authorization before retrieval and graph expansion, not after ranking.

Filter search documents, source fields, snippets, samples, definitions, owner identities, lineage nodes/edges, quality failures, incidents, query history, counts, facets, recommendations, and autocomplete. Prevent tenant-crossing identifiers and shared cache contamination.

Nonleaking zero-result semantics balance help with confidentiality. Offer safe query reformulation, term suggestions, or contact routes without revealing whether protected matches exist. Equalize error shape where necessary and monitor inference probes.

Cache keys include principal/tenant/purpose/policy/catalog version. Reauthorize on use and invalidate promptly when entitlements change. Bulk export and subscriptions require separate controls because they magnify aggregation and retention risk.

### Filter eligibility before ranking

Translate a query into both retrieval and use constraints. “Revenue” may require net recognized USD at daily grain for a certified financial report; “orders” may require production, hourly freshness, stable contract, and API access. Ask for or infer context conservatively, then display it.

Retrieve broad candidates using exact IDs/names, lexical terms, controlled vocabulary, synonyms, descriptions, fields, code, graph neighbors, and semantic embeddings. Apply authorization and noncompensable eligibility: environment, lifecycle, meaning, contract, freshness/quality, classification/purpose, compatibility and critical warnings.

Rank only eligible candidates. Signals may include concept/field match, endorsed domain/product, owner context, lineage proximity, documentation completeness, recency, quality evidence, usage, team affinity, and cost. Version the ranking model/features and preserve explanations.

Popularity is exposure-biased: old assets accumulate users and clicks; prominent ranks create more clicks. Treat it as behavioral evidence, debias where possible, and never let it override ineligibility. Generated semantic similarity can improve recall but may invent conceptual closeness.

### Design pages around fitness and action

Lead with stable identity, environment, lifecycle, definition, business concept, grain/unit/time/population, owner roles, contract/certification, and current generation. Show physical distributions and interfaces rather than conflating them with the product.

Expose schema/fields, examples only when safe, quality/freshness/reconciliation with exact generation and policy, lineage with version/coverage, recent incidents/warnings, critical consumers, usage evidence, cost, change/deprecation history, and replacements.

Every badge answers who asserted what, for which version/scope, using which evidence, when it became valid, when last checked, and how it can expire/revoke. A “certified” badge without these fields creates false assurance.

Provide actions at the decision point: preview contract, compare versions, run impact, request access, contact role, subscribe, report issue, propose definition, acknowledge deprecation, or open a governed workflow. Make action state and results visible.

### Integrate access without conflating discovery and entitlement

The catalog can initiate access but the enforcing system remains authoritative. Bind request to stable product/distribution, environment, requested scope, purpose, classification, requester, policy, approvers, duration, and conditions. Show current entitlement state from an enforcement receipt.

Support least privilege, time bounds, review, revocation, and purpose changes. Owner approval alone may be insufficient for privacy/security/legal conditions. Separate dataset discovery visibility from row/column/query permissions.

Avoid “request access” buttons that send vague email. Use explicit workflow states, owners/escalation, evidence, service expectations, denial reasons safe to disclose, expiry and audit. Detect orphaned owners and stuck requests.

After grant, verify enforcement rather than assuming the approval changed permissions. On retirement or classification change, identify entitlements and downstream exports that need review/revocation.

### Operate stewardship, certification, and lifecycle workflows

Curated metadata should live near engineering and business work. Offer templates for precise definitions, concept mappings, owner roles, contract links, quality expectations and examples. Allow proposals from code/change workflows and review by appropriate authorities.

Certification is policy evaluation, not decoration. Define eligible product/version, required metadata and control evidence, certifying role, validity, review cadence, exceptions and revocation. Preserve failed/expired decisions. Distinguish enterprise certification, domain endorsement, and consumer-specific acceptance.

Issue workflows connect a finding to exact entity/version, evidence, impact, owner, priority, state and resolution. Do not let users overwrite source assertions to “fix” a catalog symptom when the authoritative source must change.

Deprecation names reason, replacement, compatibility, milestones, consumers, owner and migration evidence. Search ranks valid replacements while retaining the deprecated result and warning where authorized. Retirement checks actual and declared use, aliases, access, reports/models/exports, active policies, and legal/audit retention.

### Expose reliable APIs and guarded active behavior

Provide stable entity lookup, search, structured filters, facets, graph traversal, as-of/version views, comparisons, subscriptions/change feeds, workflow operations and bulk export. Specify pagination, ordering, snapshot consistency, versioning, rate/size limits, cancellation and error semantics.

Search responses include catalog/index/source timestamps, policy/ranking versions, match explanation, eligibility facts, warnings and gap indicators. Clients must not infer complete absence from partial/filtered results.

Active behavior can schedule validation, notify consumers, open issues, propose classifications, enforce deprecation, or request policy change. Before mutation, re-read current authoritative assertions and policy, authorize actor and service, preview exact scope, bound fan-out, use version preconditions/idempotency, and record receipt.

Design failure recovery. Notification failure after a state change is not rolled into ambiguous “catalog error.” Record whether external mutation committed, retry safely, reconcile target state, and expose partial outcomes.

### Measure discovery quality and catalog reliability

Build judged query sets from real jobs across domains, vocabulary, exact IDs, ambiguous terms, sparse languages, deprecated/restricted assets, and zero-result cases. Measure retrieval recall, ranking precision/nDCG or suitable metrics, eligibility violations, authorization leakage, freshness and explanation correctness.

Behavioral metrics need interpretation. Click-through can reward prominent wrong results. Access requests can indicate value or poor defaults. Time-on-page can mean useful study or confusion. Combine reformulation, abandonment, successful access/use, downstream validation, user judgment and incident evidence.

Measure time to safe usable data, wrong-asset incidents, stale-badge incidents, unresolved conflicts, owner response, access completion, deprecation migration, source/entity/field coverage, source-to-index lag, dead letters, API/search SLOs, and rebuild/recovery.

Continuously test authorization, ranking, stale sources, index rebuild, tombstones, aliases, conflicts, workflow retries, cache invalidation, bulk limits and active actions. A catalog is trustworthy only if its metadata and control plane remain observable and recoverable.

## Definitions and Notation

Let:

- $E$ be catalog entities and $S_t\subseteq E$ the entities represented in catalog snapshot $t$;
- $u$ be authenticated principal/tenant/purpose context;
- $q$ be a query plus intended-use requirements;
- $A(u,e)$ mean $u$ may discover entity $e$ and the returned attributes/relationships;
- $F(e,q,u,t)$ mean $e$ satisfies noncompensable fitness/eligibility conditions at $t$;
- $x(e,q,u,t)$ be ranking features visible and valid in context;
- $R_\theta(x)$ be ranking score under versioned model/policy $\theta$; and
- $L(source,index)$ be source-to-index lag for a claim/entity class.

Candidate selection is

$$
C(q,u,t)=\{e\in S_t:A(u,e)\land F(e,q,u,t)\}.
$$

The result order is a permutation of $C$ induced by $R_\theta$; ranking never expands the set. If authorization or required evidence is unknown under policy, the entity is omitted or explicitly held for review—not assumed eligible. Search completeness is bounded by source coverage, authorization and snapshot time.

## Mechanisms, Invariants, or Proof Structure

Proof sketch that popularity-first ranking cannot guarantee fitness:

1. Let `warehouse.legacy_orders` have popularity 1,000 and `finance.orders_product` popularity 100.
2. Both match the lexical/technical query “orders.”
3. The requested use requires production, a current contract, quality approval, and freshness at most 60 minutes.
4. Legacy is 1,440 minutes old, uncertified/uncontracted for the use; the product is 15 minutes old, contracted, and quality-approved.
5. Popularity-first ranking places legacy first because $1000>100$.
6. Eligibility-first selection removes legacy and retains the product.
7. Therefore popularity order over raw matches cannot guarantee a suitable first result; fitness constraints must precede ranking.

The proof does not claim popularity is useless. Among already eligible products it can help expose established use, subject to bias and context. It cannot compensate for a failed noncompensable requirement.

The executable reproduces the counterexample. It is a deterministic teaching model, not a search engine, semantic model, catalog, identity provider, policy engine, access system, or universal ranking formula.

<!-- bijux-verify: {"id":"catalog-eligibility-before-ranking","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"popularity_first=warehouse.legacy_orders\npopularity_first_is_suitable=False\neligible_products=('finance.orders_product',)\nselected_product=finance.orders_product\n","stderr":""}} -->
```python
matches = {
    "warehouse.legacy_orders": {
        "popularity": 1000,
        "environment": "production",
        "freshness_minutes": 1440,
        "contracted": False,
        "quality_approved": False,
    },
    "finance.orders_product": {
        "popularity": 100,
        "environment": "production",
        "freshness_minutes": 15,
        "contracted": True,
        "quality_approved": True,
    },
}

def suitable(item):
    return (
        item["environment"] == "production"
        and item["freshness_minutes"] <= 60
        and item["contracted"]
        and item["quality_approved"]
    )

popularity_first = max(matches, key=lambda name: matches[name]["popularity"])
eligible = tuple(name for name, item in matches.items() if suitable(item))
selected = max(eligible, key=lambda name: matches[name]["popularity"])

print(f"popularity_first={popularity_first}")
print(f"popularity_first_is_suitable={suitable(matches[popularity_first])}")
print(f"eligible_products={eligible}")
print(f"selected_product={selected}")
```

## Alternatives and Trade-Offs

1. **Central versus federated catalog:** central discovery improves consistency; federation preserves domain authority. Shared identity/contracts with domain-owned assertions can combine them.
2. **Graph versus document index:** graphs express relationships/as-of evidence; indexes provide fast retrieval/ranking. Use governed source model plus rebuildable projections.
3. **Lexical versus semantic search:** lexical retrieval is explainable and precise for names; semantic retrieval improves conceptual recall but can create false similarity.
4. **Strict filters versus conversational clarification:** filters are auditable; conversation helps ambiguous users but must expose inferred constraints and avoid hidden assumptions.
5. **Popularity versus policy/meaning rank:** popularity reflects use; policy and semantic signals protect suitability. Popularity belongs after eligibility.
6. **Open discovery versus restricted existence:** openness encourages reuse; some metadata is sensitive. Attribute/relationship-aware authorization determines visibility.
7. **Rich previews versus minimization:** samples/profiles speed evaluation; they can expose protected values and distributions. Prefer governed aggregates/synthetic examples where possible.
8. **One certification versus scoped decisions:** one badge is simple; scope/version/use-specific decisions are honest and actionable.
9. **Catalog-local edits versus source-owned changes:** local edits are fast; source ownership prevents drift. Use proposals and write-back workflows with receipts.
10. **Integrated access versus separate portal:** integration reduces friction; enforcement separation preserves authority. Link precise request and enforcement state.
11. **Real-time indexing versus batch rebuild:** real-time updates reduce lag; periodic rebuild validates completeness and recovers missed events. Mature systems use both.
12. **Automatic action versus human review:** automation scales reversible well-specified actions; review handles novel/high-impact ambiguity at latency and consistency cost.

## Failure Modes and Misconceptions

- **“A catalog is an inventory.”** Inventory alone does not establish meaning, state, policy, access or use.
- **“Crawling everything creates trust.”** Crawlers observe limited technical facts with freshness and permission gaps.
- **“The search index is the source of truth.”** It is a lagging rebuildable projection.
- **“Names are stable IDs.”** Names collide, move, split, merge and get reused.
- **“One page equals one product.”** Logical products can have multiple distributions and versions.
- **“Search match means suitable.”** Eligibility depends on use, meaning, state and policy.
- **“The most popular table is best.”** Legacy exposure and rank feedback can amplify bad assets.
- **“Clicks prove relevance.”** Position, curiosity, confusion and lack of alternatives bias clicks.
- **“Semantic search understands the business.”** Similarity is retrieval evidence, not approved meaning.
- **“Documentation completeness means quality.”** Well-described data can be wrong or stale.
- **“A green badge is timeless.”** Certification has scope, version, evidence, authority and expiry/revocation.
- **“Freshness alone proves fitness.”** Current wrong or unauthorized data remains unfit.
- **“Lineage shows actual impact.”** Versions, fields, runtime reads and consumer evidence matter.
- **“Owner means the displayed person.”** Durable role, current assignment and escalation matter.
- **“Discovery grants access.”** Underlying enforcement is a separate authoritative decision.
- **“Owner approval is always sufficient.”** Security, privacy, legal and consumer authorities may apply.
- **“A request email is a workflow.”** State, evidence, policy, expiry, enforcement and audit are required.
- **“Authorize after search.”** Ranking, snippets, facets, counts and timing can already leak.
- **“Hide the result but show its lineage.”** Relationships can disclose protected existence.
- **“Shared caches are harmless.”** They can cross principals, tenants and policy versions.
- **“Zero results means no asset exists.”** Authorization, coverage, vocabulary and lag may explain it.
- **“Generated descriptions can fill every gap.”** Inference needs provenance, confidence and review.
- **“Catalog-local corrections fix source metadata.”** They can create another conflicting copy.
- **“More entities mean success.”** Duplication and junk can worsen discovery.
- **“Monthly active users prove value.”** Users may repeatedly fail or select unsafe data.
- **“Index freshness is page availability.”** A responsive page can show stale claims.
- **“Deprecation is a warning banner.”** Consumers, access, aliases, replacements and milestones require workflow.
- **“Retirement means delete from search.”** Interfaces, exports, policies and audit history remain.
- **“Active metadata can trust its own page.”** Re-read current authority/policy before mutation.
- **“Catalog recovery is restoring the UI.”** Source ingestion, graph, index, authorization and workflows need reconciliation.

## Worked Examples

### Example 1

An analyst searches “active customers.” Controlled concepts distinguish daily active accounts, monthly paying organizations, and currently entitled individuals. Result explanations show grain, population, time and owner before access.

### Example 2

A crawler sees a table renamed. Stable product identity retains reviews, contract and consumers; physical distribution history and alias redirect guide users without treating the old path as current.

### Example 3

Quality badge Q7 applies to generation G41, while current G42 is still evaluating. The entity page shows G41 approved and G42 pending rather than carrying green state forward.

### Example 4

One source's events stop. Search documents remain but display source observation and index age; critical operational fields become unknown, and eligibility excludes products requiring current status.

### Example 5

A restricted dataset matches a query. Authorization removes its document, facets, autocomplete and graph neighbors before ranking. The zero-result response offers safe glossary refinement without confirming hidden existence.

### Example 6

An access request targets product P17's warehouse distribution in production for 30-day fraud analysis. Approval and enforcement receipt remain separate; the catalog reports granted only after the data platform confirms policy-bound access.

### Example 7

An inferred description says net revenue, but the contract and steward say gross bookings. The inferred assertion remains visible to reviewers with confidence, search stops boosting it, and conflict workflow corrects the model/source.

### Example 8

Behavioral ranking favors legacy orders because years of dashboards depend on it. Eligibility removes the deprecated table for new use while migration views still expose its consumer graph to authorized owners.

### Example 9

Two concurrent deprecation actions target different catalog snapshots. Version preconditions accept the first and reject the stale second; idempotent receipts prevent duplicate notifications.

### Example 10

A disaster rebuild replays source assertions, reconstructs the graph and search documents, re-applies authorization policy, reconciles counts/digests, and resumes workflows from receipts instead of restoring only a stale index backup.

## Cross-Program Connections

- **Information Retrieval:** tokenization, fields, lexical/semantic retrieval, filters, ranking, relevance judgments, feedback bias and evaluation power catalog search.
- **Knowledge Representation:** stable entities, controlled vocabularies, concepts, aliases, provenance, temporal assertions and typed relationships support meaning.
- **API and Service Engineering:** contracts, pagination, consistency, versioning, rate limits, subscriptions, authorization and error semantics shape catalog APIs.
- **Platform Engineering:** portals, paved integrations, source ingestion, policy services, workflows, self-service and operability turn catalogs into platforms.
- **Security Engineering:** authorization-before-retrieval, tenant isolation, inference resistance, audit, cache safety and supply-chain trust protect metadata.
- **Privacy Engineering:** purpose, minimization, samples/profiles, search behavior, lineage, access, retention and deletion constrain catalog use.
- **Reliability Engineering:** source/index freshness, SLOs, telemetry, alerting, replay, rebuild, reconciliation and incident response keep projections trustworthy.
- **Organizational Design:** federated domains, ownership, stewardship, decision rights, incentives, review and escalation determine catalog quality.
- **Product Management:** user jobs, task success, workflow friction, discovery outcomes, adoption interpretation and feedback loops shape priorities.
- **Governance and Risk:** certification, obligation, policy, exceptions, access decisions, deprecation and audit make catalog claims accountable.

## References

1. W3C. [Data Catalog Vocabulary (DCAT) Version 3](https://www.w3.org/TR/vocab-dcat-3/). Accessed 2026-09-03. Authoritative vocabulary for catalogs, datasets, distributions, data services, versions, relationships, provenance and coverage.
2. Dublin Core Metadata Initiative. [DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/). Accessed 2026-09-03. Authoritative terms for resource identity, descriptions, subjects, relations, dates, formats, rights, provenance and controlled values.
3. W3C. [SKOS Simple Knowledge Organization System Reference](https://www.w3.org/TR/skos-reference/). Accessed 2026-09-03. Authoritative model for concepts, schemes, labels, semantic relations, notation, collections and mapping properties.
4. Schema.org. [Dataset](https://schema.org/Dataset). Accessed 2026-09-03. Primary vocabulary documentation for datasets, catalogs, distributions, creators, variables, spatial/temporal scope, measurement and provenance.
5. DataCite. [Metadata Schema](https://schema.datacite.org/). Accessed 2026-09-03. Primary schema resources for persistent identification, citation, versions, creators, publisher, dates, subjects, rights, funding and relationships.
6. DataHub. [Search](https://docs.datahub.com/docs/how/search). Accessed 2026-09-03. Primary project documentation for full-text and advanced search, filters, exact matches, ranking signals, structured queries and discovery behavior.
7. OpenMetadata. [Data Discovery](https://docs.open-metadata.org/latest/how-to-guides/data-discovery). Accessed 2026-09-03. Primary project guidance for discovering assets through search, filters, metadata, lineage, ownership, tags, domains and related context.
8. Apache Atlas. [Architecture](https://atlas.apache.org/2.0.0/Architecture.html). Accessed 2026-09-03. Primary project documentation for type/entity metadata, ingestion, graph repository, search, lineage, classification and notification integration.
9. Amundsen. [Architecture](https://www.amundsen.io/amundsen/architecture/). Accessed 2026-09-03. Primary project documentation for metadata ingestion, search, frontend, metadata service, graph/search backends and data discovery architecture.
10. Amazon Web Services. [Amazon DataZone data catalog](https://docs.aws.amazon.com/datazone/latest/userguide/data-catalog.html). Accessed 2026-09-03. Primary product documentation for business catalog assets, metadata forms, subscriptions, publishing, discovery and governance workflows.
11. Google Cloud. [Search for data assets in Dataplex Universal Catalog](https://cloud.google.com/dataplex/docs/search-assets). Accessed 2026-09-03. Primary product documentation for asset search, query syntax, filters, facets, permissions and discovery results.
12. Backstage. [System Model](https://backstage.io/docs/features/software-catalog/system-model/). Accessed 2026-09-03. Primary project documentation for catalog entities, ownership, systems, components, resources, APIs, domains and relationships applicable to platform catalogs.
13. Bitol. [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/). Accessed 2026-09-03. Primary open specification for product identity, schema, quality, service levels, ownership, roles, authoritative definitions and custom properties.
14. OpenLineage. [Object model](https://openlineage.io/docs/spec/object-model/). Accessed 2026-09-03. Primary specification documentation for run, job, dataset, namespace, version, event and extensible facet identities used in runtime catalog evidence.

## Exercises

### Exercise 1

Design a catalog architecture for federated domains. Include source assertions, identity, provenance/authority, graph/current views, authorization-scoped indexing, search/ranking, pages/APIs, workflows, coverage, operations and rebuild.

### Exercise 2

Design search for “current customer revenue” when candidates differ by gross/net meaning, grain, currency, environment, freshness, quality, certification, classification and popularity. Specify clarification, authorization, eligibility, rank and explanations.

### Exercise 3

Threat-model catalog search, autocomplete, facets, counts, samples, lineage, recommendations, access requests, behavior logs, caches and bulk export in a restricted multi-tenant environment.

### Exercise 4

Define certification and access workflows for a regulated product. Include identity/version, required evidence, authorities, exceptions, expiry/revocation, enforcement receipts, stale metadata, retries and audit.

### Exercise 5

Design catalog effectiveness and reliability evaluation. Include judged queries, retrieval/ranking, eligibility and authorization, behavioral bias, time-to-safe-use, source/index freshness, workflows, wrong-asset incidents and disaster recovery.

## Answers to the Exercises

### Answer 1

Let domains own contracts, meanings, roles and quality obligations under shared entity/assertion schemas and stable namespaces. Collect source APIs/events/artifacts into provenance-bearing raw and normalized assertions with predicate-specific authority, valid/observed time, confidence and protection. Resolve current/as-of projections without deleting conflicts. Build graph, entity documents and principal/tenant/policy-scoped search indexes as reconstructable projections; use event updates plus periodic reconciliation/full rebuild. Services provide authorized search, exact lookup, as-of comparison, lineage, subscriptions and workflows. Measure eligible/captured entities/fields/edges, source/index lag, conflicts, dead letters and stale critical claims. Operate queues/store/index/API/auth/workflows with SLOs, backups, event replay, count/digest reconciliation and tested recovery.

### Answer 2

Ask or expose inferred purpose, reporting context, daily/monthly grain, net/gross, currency, as-of/event time and freshness. Authorize before candidate retrieval. Match controlled concepts, definitions, fields, aliases and exact IDs, then require production environment, requested semantic definition/grain/unit, compatible interface, current contract/certification, quality/freshness and permitted classification/purpose. Exclude ineligible assets regardless of popularity. Rank eligible results by exact concept/contract match, operational evidence, domain/owner context and then responsible usage signals. Explain matched concept, grain/currency/time, physical distribution, generation, quality/freshness evidence, owner, access state, warnings, source/index age and why alternatives were filtered where safe. Treat uncertainty as clarification or hold, not silent fit.

### Answer 3

Authorize before retrieval/ranking and filter document attributes, snippets, autocomplete, spell suggestions, facets/counts, samples/profiles, lineage nodes/edges, recommendations and errors. Prevent tenant-crossing IDs; use nonleaking zero-result semantics and rate-limit inference probes. Replace sensitive samples/query text with governed aggregates/synthetic examples or protected references. Cache by principal/tenant/purpose/policy/catalog version and invalidate on entitlement changes. Access requests minimize purpose/scope and do not reveal approvers/policies unnecessarily. Protect behavior logs as sensitive, limit retention and secondary use. Bulk export needs distinct authority, size/rate/field/retention controls, watermark/receipt and audit. Test timing/count leakage, hidden neighbors, pagination totals, stale caches and shared identities.

### Answer 4

Certification targets exact product/distribution/generation and policy version; requires approved definition/grain/unit, contract, ownership, classification, lineage/coverage, quality/reconciliation/freshness and consumer evidence. An authorized certification role records decision, scope, evidence digest, valid interval, review, exceptions and revocation triggers; badge never outlives evidence. Access binds requester, purpose, least-privilege field/row/interface scope, classification, conditions, approvers and expiry. Governance roles supplement product owner where required. Re-read current state before action, reject stale approvals with version preconditions, use idempotency, and confirm enforcement receipt before reporting granted. Preserve failed/expired decisions, retry only safe uncommitted actions, reconcile external permissions, alert on stale critical metadata and audit every transition.

### Answer 5

Maintain versioned judged queries across domains, exact IDs, synonyms, ambiguity, languages, deprecated/restricted items and zero-result cases. Measure recall, precision/nDCG or suitable rank metrics, eligibility violations, authorization leaks and explanation accuracy by cohort. Interpret clicks with position/exposure bias; combine reformulation, abandonment, access completion, validated use, user judgment and incident outcomes. Measure time to safe usable data, wrong-asset/stale-badge incidents, owner/steward response, access duration, migration, eligible/source coverage, source-to-index lag, dead letters and API/search/workflow SLOs. Inject source outage, stale policy, hidden result, alias move, tombstone, conflict, cache failure and action retry. Rebuild from assertions/events, reapply authorization, reconcile graph/index counts and digests, and resume workflows from receipts.
