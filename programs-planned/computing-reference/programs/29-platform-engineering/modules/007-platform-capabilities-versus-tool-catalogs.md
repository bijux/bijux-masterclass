---
module_id: PLAT-007
program: Platform Engineering
level: 1
module_number: 7
title: Platform Capabilities Versus Tool Catalogs
status: complete
last_verified: 2026-09-02
---

# Platform Capabilities Versus Tool Catalogs

## One-Page Review

### Governing question

When should a platform offer an outcome-oriented capability with an accountable contract, and when should it provide a trustworthy catalog that helps teams discover and choose tools or services they will integrate and operate themselves?

### Essential definitions

- A **platform capability** is a supported ability that lets an eligible consumer accomplish a defined job through stable semantics, interfaces, controls, evidence, and lifecycle ownership, regardless of which tools implement it.
- A **tool** is a product, service, component, library, or executable mechanism used to implement work. Possession of a tool does not establish a consumer outcome.
- A **tool catalog** is a governed inventory of discoverable tools or services with metadata such as purpose, owner, support, compatibility, authority, provenance, cost, lifecycle, and constraints.
- A **software catalog** models software entities, APIs, resources, systems, ownership, lifecycle, and relations. It describes an ecosystem; it does not automatically provision or operate it.
- A **provider** implements all or part of a capability. A capability may compose several providers, and one provider may support several capabilities.
- A **capability contract** states eligible jobs, intent, outputs, state, guarantees, errors, responsibilities, interfaces, support, evidence, compatibility, and retirement.
- **Discovery** helps a consumer find and understand an offering. **Fulfillment** produces or changes a governed outcome. **Operation** sustains the promise after fulfillment.
- **Catalog authority** identifies which source owns each fact and how freshness, conflict, and deletion are handled.

### Central model, mechanism, or theorem

Model capability $c$ as $C_c=(U,J,I,O,S,G,R,L,E)$: eligible consumers $U$, jobs $J$, intent $I$, outcomes $O$, states $S$, guarantees $G$, responsibilities $R$, lifecycle $L$, and evidence $E$. Map providers and tools through a many-to-many relation $M\subseteq C\times T$. Expose the capability when the platform owns coherent semantics and operation; expose catalog entries when consumers need trustworthy discovery but retain selection, integration, and operational ownership. A portal may present both without collapsing them.

### Critical invariants

- Capability names express durable consumer outcomes, not current vendor or implementation names.
- Every capability has one accountable contract even when several teams or providers implement it.
- Catalog entries identify authoritative sources, owner, support state, freshness, compatibility, and lifecycle.
- Search, install, access, provision, readiness, and support are distinct states and actions.
- A catalog does not imply endorsement, permission, interoperability, availability, or platform operation unless those claims are explicit.
- Provider replacement preserves capability semantics or triggers a governed contract change.
- Inventory growth is not treated as increased platform value.

### Common failures

Calling a page of links a platform; wrapping every vendor API and calling it a capability; making tool names the public contract; listing ownerless or stale entries; treating catalog registration as production readiness; offering many overlapping choices without comparison; hiding provider limits; and measuring catalog size, searches, or clicks instead of completed jobs and operating outcomes.

### Compact example

A catalog lists three database products with owners, versions, data classifications, regions, costs, and support states. Separately, the platform offers a “managed relational database” capability: consumers declare owner, data class, region, recovery objectives, and service tier; the platform selects an eligible provider, provisions it, exposes stable status and credentials, operates backups, and owns migration. The catalog supports informed choice for specialist databases; the capability owns the routine outcome.

### Connections

Retrieve product boundaries from [PLAT-004](004-platform-as-product.md), self-service contracts from [PLAT-005](005-self-service-and-guardrails.md), and routes plus provider ownership from [PLAT-006](006-paved-roads-and-escape-hatches.md). The next module examines [internal platforms and external cloud services](../roadmap.md#block-01--platform-engineering-foundations). Later modules own portals, documentation, core capabilities, software catalogs, service brokers, marketplaces, and portal-monolith avoidance in depth.

## Governing Question

How can a platform team distinguish “we help you find a tool” from “we accept durable responsibility for your outcome,” and design each without creating tool sprawl, false endorsement, leaky abstractions, or an untrustworthy catalog?

The distinction is not visual. The same portal can offer a capability request, a catalog record, provider documentation, and status. The difference is the contract and ownership behind the interface. A catalog can be extremely valuable when consumers legitimately own integration. A capability can be valuable when the platform can standardize a recurring undifferentiated outcome. Problems begin when presentation implies a promise the organization has not assigned.

## Why This Matters

Organizations accumulate tools through local choice, acquisitions, providers, experiments, security mandates, and central purchasing. Discoverability becomes difficult: teams cannot find existing services, compare support, identify owners, or know which version is approved. A catalog can reduce duplication and reveal the actual estate.

Discovery alone does not remove integration and operation. A developer who finds a database product must still choose topology, identity, network access, backup, recovery, telemetry, upgrades, cost, support, and retirement. If those decisions recur across teams and the platform has authority and capacity, an outcome-oriented capability can compose the tools into a stable consumer contract.

The reverse error is wrapping everything. A thin API over a vendor may add another failure point without hiding provider semantics or assuming operational responsibility. Consumers must learn both layers, and migrations remain provider-shaped. A capability should exist only when the platform can own meaningful abstraction, evidence, support, and lifecycle.

Current CNCF guidance frames platforms as integrated collections of capabilities around user needs, notes that providers may be internal or external, and separates portals, APIs, golden paths, build, delivery, observability, infrastructure, data, messaging, identity, security, and artifact capabilities. Current Backstage guidance describes its Software Catalog as a system for ownership and metadata, models components, APIs, resources, systems, and domains, and warns that the catalog should be a cache over authoritative sources rather than the ultimate source of truth. These roles complement one another.

## Prerequisites and Retrieval

Retrieve from PLAT-001 the complexity-transfer and total-system boundary. Retrieve jobs and authority from PLAT-002, cognitive-load evidence from PLAT-003, product lifecycle from PLAT-004, self-service and guardrails from PLAT-005, and paved-road provider and escape ownership from PLAT-006.

You should understand APIs, service ownership, metadata, discovery, provider contracts, identity, provisioning, observability, compatibility, migration, support, and retirement. Familiarity with catalogs and portals helps, but the chapter does not depend on one product.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish tools, catalog entries, providers, capabilities, interfaces, and consumer outcomes;
2. write a capability contract that remains stable across provider and interface changes;
3. decide when the platform should own fulfillment and operation versus discovery and enablement;
4. model many-to-many relationships between capabilities and tools without exposing implementation topology as product semantics;
5. design catalog authority, provenance, freshness, ownership, support, and lifecycle rules;
6. prevent false claims of endorsement, readiness, permission, compatibility, and availability; and
7. measure capability outcomes and catalog quality with claim-appropriate evidence.

## Core Exposition

### Begin with the consumer job

Tools answer “with what mechanism?” Capabilities answer “what supported ability can I depend on?” Start with the consumer job and retained responsibility. “Jenkins,” “Kubernetes,” and “Vault” are product or technology names. “Build a verified artifact,” “run a stateless service,” and “issue a short-lived workload credential” are candidate capability outcomes.

Outcome naming is not wordplay. It allows implementations to evolve and prevents a procurement decision from becoming the public domain model. It also exposes whether the platform owns enough to make a promise. If the platform merely links to a tool and the consumer operates it, describe discovery and support honestly rather than inventing a capability label.

### Specify a complete capability

For capability $c$, define

$$
C_c=(U,J,I,O,S,G,R,L,E),
$$

where $U$ is eligible consumers and workload classes, $J$ supported jobs, $I$ declared intent, $O$ outcomes and outputs, $S$ observable states, $G$ guarantees and limits, $R$ responsibility allocation, $L$ lifecycle, and $E$ evidence. Interfaces—portal, CLI, API, IDE, or automation—present this one contract; they are not separate capabilities unless semantics differ materially.

For “managed relational database,” intent might include owner, data class, region, engine compatibility, service tier, and recovery objectives. Outcomes include a reachable instance, identity binding, credentials or workload authorization, backup policy, telemetry, and deletion behavior. States include requested, provisioning, ready, degraded, restoring, deleting, and retired. Guarantees address availability, backup, restore, support, change, and limits. Responsibilities state what platform, provider, and application team own.

The contract must include operation. A template that creates a provider object but leaves upgrades, backup verification, incidents, and deletion to the consumer may be a useful integration accelerator, not a managed capability.

### Model tools and providers separately

Let $C$ be capabilities and $T$ tools or providers. Relation

$$
M\subseteq C\times T
$$

records which tools contribute to which capabilities. It is many-to-many. A deployment capability may use source control, build, artifact storage, policy, orchestration, identity, and telemetry. An identity provider may support login, workload identity, secrets, and audit capabilities.

Do not expose $M$ as the consumer contract unless provider detail changes a consumer-owned decision. Implementation topology belongs in service ownership, dependency maps, incident response, and provenance. Consumers may need provider disclosure for compliance, data location, compatibility, cost, or diagnosis; hiding is not a goal by itself.

Provider replacement is an abstraction test. If consumers must rewrite intent and recovery procedures, the capability contract leaked or changed. That can be acceptable, but it requires explicit compatibility, migration, and product decisions rather than the claim that the provider was always hidden.

### Decide what the platform should own

Candidate capability ownership requires more than popularity. Ask:

1. Is the consumer job recurrent and evidenced across a meaningful segment?
2. Are the semantics sufficiently commonable without erasing domain differences?
3. Does the platform have authority over the mechanism and proposed guarantees?
4. Can it provide end-to-end fulfillment, operation, support, evidence, change, and retirement?
5. Does composition reduce total burden versus provider-direct use or enablement?
6. Can valid exceptions and independent ownership remain explicit?

If the answers are weak, the platform may still offer a curated catalog, documentation, integration kit, reference implementation, purchasing agreement, or enabling-team collaboration. These are durable products when named accurately.

Use a catalog when consumers need legitimate choice because tool semantics are domain-specific, specialized, experimental, or independently operated. Use a capability when repeated choice and integration are undifferentiated and the platform can own the outcome. Use both when a standard capability covers common cases and a catalog supports specialist alternatives.

### Design a trustworthy catalog

A catalog is a data product. Its usefulness depends on a governed metadata contract. Each entry should identify:

- stable identifier, human name, type, purpose, and supported jobs;
- authoritative source and ingestion provenance;
- accountable owner and escalation route;
- lifecycle and support state;
- eligible consumers, access route, and approval context;
- versions, compatibility, dependencies, and known constraints;
- security, privacy, licensing, cost, data-region, and regulatory facts where relevant;
- documentation, interfaces, operational status, and service objectives when authoritative;
- freshness observation, validation result, and conflict state; and
- deprecation, replacement, deletion, and historical-retention behavior.

Do not ask teams to maintain the same fact in several portals. Establish field-level authority. Ownership may come from the organization directory, deployment state from the runtime, cost from billing, API schema from source control, and incidents from an operations system. The catalog composes views and records provenance.

Current Backstage guidance describes catalog entities as ingested from authoritative sources, processed, stored, and exposed through an API. Its catalog-graph guidance explicitly advises treating the catalog as a cache rather than the ultimate source of truth. That principle generalizes: the catalog must survive source delay and conflict without inventing authority.

### Keep discovery claims bounded

Catalog presence can mean only “this entity was ingested.” It must not silently mean:

- the tool is approved for every context;
- the principal is authorized to use it;
- the entry is currently available;
- two listed versions interoperate;
- the platform operates or supports it;
- the software is secure or production ready;
- the metadata is complete or current; or
- the organization endorses the vendor.

Use explicit state and badges with definitions, provenance, evaluation time, and authority. “Approved” without scope and owner is unsafe. “Production” without workload, region, support, and evidence is ambiguous. Search ranking should not become a hidden endorsement algorithm.

### Separate discovery, access, fulfillment, and operation

A consumer journey can traverse several distinct contracts:

1. **discover:** find and compare an offering;
2. **qualify:** determine fit, prerequisites, constraints, and support;
3. **access:** obtain permission or subscription;
4. **fulfill:** create, configure, or bind an instance;
5. **integrate:** connect it to the workload;
6. **operate:** observe, change, recover, support, and pay for it; and
7. **retire:** revoke, delete, migrate, and retain evidence.

A catalog often owns the first two and links to authorities for the rest. A platform capability can own a coherent journey across all seven while composing several providers. A marketplace may add ordering and commercial terms without operating the result. State which contract ends where.

### Check the capability-tool graph

The following synthetic graph shows that one capability can compose several tools and one tool can serve several capabilities. It also identifies a catalog-only tool with no platform capability mapping.

<!-- bijux-verify: {"id":"capability-tool-graph","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"capabilities=3\ntools=4\nedges=5\nmost_composed=deploy-service:2\nmost_reused=identity-provider:2\ncatalog_only=graph-database\n","stderr":""}} -->
```python
mapping = {
    "deploy-service": {"orchestrator", "identity-provider"},
    "issue-credential": {"identity-provider", "policy-engine"},
    "enforce-policy": {"policy-engine"},
}
catalog_tools = {"orchestrator", "identity-provider", "policy-engine", "graph-database"}

tool_use = {tool: sum(tool in tools for tools in mapping.values()) for tool in catalog_tools}
most_composed = sorted(mapping.items(), key=lambda item: (-len(item[1]), item[0]))[0]
most_reused = sorted(tool_use.items(), key=lambda item: (-item[1], item[0]))[0]
catalog_only = sorted(tool for tool, count in tool_use.items() if count == 0)

print(f"capabilities={len(mapping)}")
print(f"tools={len(catalog_tools)}")
print(f"edges={sum(len(tools) for tools in mapping.values())}")
print(f"most_composed={most_composed[0]}:{len(most_composed[1])}")
print(f"most_reused={most_reused[0]}:{most_reused[1]}")
print("catalog_only=" + ",".join(catalog_only))
```

The graph establishes only the declared topology. It does not show consumer fit, ownership, reliability, security, compatibility, support, or whether `graph-database` should become a platform capability.

### Prevent catalog and portal sprawl

A tool catalog can become another tool. If teams must search a portal, wiki, cloud marketplace, architecture list, procurement system, and security register, discoverability worsens. Design a federated metadata model with stable identifiers, field authority, APIs, and views suited to different journeys.

Do not copy all provider schemas into one central model. Normalize durable concepts—owner, lifecycle, support, identity, dependency, data class, cost—and preserve provider-specific details behind typed extensions or links. An all-purpose entity model can become an ungoverned key-value store that no consumer trusts.

Portal composition should follow capability boundaries. The portal can display a capability, its instances, documentation, status, cost, and providers without owning their domain logic. If every workflow is implemented inside the portal backend, it becomes a coordination and deployment monolith. Stable APIs and event contracts let portal, CLI, IDE, and automation share semantics.

### Govern lifecycle and removal

Capability and catalog lifecycles differ. Retiring a capability requires consumer discovery, replacement or exit, migration, service-promise changes, provider cleanup, evidence retention, and support closure. Removing a catalog entry may mean the source disappeared, the entity was deleted, or discoverability ended; underlying resources may still exist.

Use tombstones or historical records where audit and dependency analysis require them. Do not silently delete ownerless entries and lose incident evidence. Conversely, do not keep stale “active” entries to preserve history. Separate current state from retained history.

Providers can change beneath capabilities. Track provider versions and dependencies internally, test contract conformance, publish consumer-relevant changes, and rehearse migration. A tool can leave the catalog while remaining a transitive implementation dependency; the dependency map must not rely only on consumer-facing visibility.

### Measure the right outcome

For capabilities, measure eligible task success, independent completion, time and waits, reliability, recovery, safety, consumer understanding, support, lifecycle, provider incidents, and platform cost. For catalogs, measure coverage against authoritative populations, ownership validity, freshness, conflicts, search success, comparison quality, broken links, unknown or orphan entities, and downstream task completion.

Catalog page views do not prove discovery success. A search with no click may answer the question; a click may reveal a bad result. Tool count can rise because of duplication and sprawl. Capability count can rise because boundaries are fragmented. Use journey research and task outcomes alongside telemetry.

Measure the transition between catalog and capability too: how often consumers find an entry but cannot determine support, request access, integrate, recover, or retire. Those seams reveal false promise and ownership gaps.

## Definitions and Notation

Let $C$ be platform capabilities, $T$ tools and providers, $U$ consumer segments, and $J$ jobs. Capability $c$ has contract $C_c=(U,J,I,O,S,G,R,L,E)$ for intent, outcomes, states, guarantees, responsibilities, lifecycle, and evidence.

Relation $M\subseteq C\times T$ maps implementation contribution. For $c\in C$, provider set $M(c)=\{t\in T\mid(c,t)\in M\}$. For $t\in T$, capability set $M^{-1}(t)=\{c\in C\mid(c,t)\in M\}$. Neither cardinality measures value: a capability with one provider can be critical, and a widely reused tool can be replaceable.

Let catalog record $K_t=(id,type,a,p,o,s,f,d)$ contain stable identity, type, authority source $a$, provenance $p$, owner $o$, support/lifecycle state $s$, freshness $f$, and domain metadata $d$. A **conflict** occurs when sources with overlapping claimed authority disagree. A **tombstone** records that an entity ceased to be current while preserving required identity and history.

**Endorsement** is an authorized recommendation for a stated context. **Approval** is a scoped decision by a named authority. **Availability** is current service state. **Eligibility** is whether a consumer and workload may use an offering. These meanings must not be inferred from catalog presence.

## Mechanisms, Invariants, or Proof Structure

Use this design sequence:

1. Identify consumer segment, job, current alternative, and retained authority.
2. Decide whether the platform should own discovery, enablement, fulfillment, integration, operation, or the entire journey.
3. For a capability, define $C_c$ independently of provider and interface names.
4. Map providers through $M$, assign dependency ownership, and test replacement and failure.
5. For a catalog, define entity types, stable IDs, field authorities, provenance, freshness, conflicts, lifecycle, and access.
6. Bound claims for registration, approval, endorsement, permission, availability, compatibility, support, and readiness.
7. Expose stable APIs so portal, CLI, IDE, automation, and reports share meaning.
8. Test ordinary, stale, conflicting, orphaned, inaccessible, provider-failed, migrated, and deleted cases.
9. Measure capability outcomes and catalog data/task quality separately and at their seams.
10. Consolidate duplicate tools, change capability scope, migrate providers, or retire entries from evidence.

The invariants are **outcome naming**, **contract accountability**, **provider independence with honest disclosure**, **field-level authority**, **state separation**, **bounded catalog claims**, and **lifecycle completeness**.

The claim “our portal lists 500 tools, therefore the platform offers 500 capabilities” fails directly. Entries may be duplicates, unsupported, inaccessible, stale, consumer-operated, or mere components of one outcome. Conversely, one capability may compose many tools. Cardinality of the catalog and cardinality of supported abilities are different quantities.

## Alternatives and Trade-Offs

**Curated small catalog versus comprehensive inventory.** Curation improves decision quality and support clarity but can hide the actual estate. Comprehensive inventory supports governance and incident discovery but can overwhelm consumers. Maintain broad authoritative inventory and present journey-specific curated views with explicit endorsement scope.

**Capability abstraction versus provider-direct use.** A capability reduces repeated integration and permits provider evolution. It adds an abstraction, central dependency, and migration duty. Prefer provider-direct enablement when provider semantics are the consumer's domain or the platform cannot own the outcome.

**Central catalog versus federated metadata.** Central presentation improves search and terminology. Federated authority keeps facts near owners. Compose authoritative feeds into a central query model rather than centralizing authorship of every fact.

**One provider versus provider portability.** One provider keeps semantics and operation simple. Multiple providers improve placement or resilience but create lowest-common-denominator risk. Promise portability only for tested consumer-relevant semantics; expose provider selection when it changes obligations.

**Automatic registration versus manual curation.** Automation improves coverage and freshness but ingests noise. Manual review improves description quality but creates queues and staleness. Automate authoritative facts, validate ownership, and curate claims such as endorsement separately.

**Generic catalog model versus domain-specific entities.** Generic models integrate easily but become vague. Domain models preserve meaning but multiply schemas. Keep a small stable core and governed domain extensions with explicit ownership and compatibility.

## Failure Modes and Misconceptions

- **A catalog is a platform.** Discovery is valuable, but it does not itself fulfill or operate consumer outcomes.
- **A tool is a capability.** Tools implement mechanisms; capability contracts create dependable abilities.
- **A wrapper creates abstraction.** Renaming provider fields without owning semantics adds a layer, not necessarily value.
- **Registration means approval.** Presence, provenance, support, permission, readiness, and endorsement are separate claims.
- **The catalog is the universal source of truth.** Different fields have different authoritative systems; the catalog composes and caches them.
- **More choice improves experience.** Undifferentiated overlapping options increase comparison and integration burden.
- **Provider hiding is always good.** Compliance, locality, compatibility, cost, and incident diagnosis may require disclosure.
- **One tool serves one capability.** Many-to-many mapping is normal and important for blast-radius analysis.
- **Owner metadata proves ownership.** Validate directory identity, responsibility acceptance, and freshness.
- **Deleting an entry deletes the thing.** Catalog lifecycle and underlying resource lifecycle must be coordinated explicitly.

## Worked Examples

### Example 1

**Situation:** A portal lists links to CI, artifact storage, and deployment documentation. **Reasoning:** It improves discovery but consumers still assemble contracts, credentials, status, support, and recovery. Label it a curated delivery tool catalog and use journey evidence to decide whether to compose a build-and-release capability. **Conclusion:** Honest discovery is better than a false capability claim.

### Example 2

**Situation:** The platform exposes every field of one cloud database API under new names. **Reasoning:** Consumers retain provider knowledge, backup decisions, upgrades, incidents, and migration. The wrapper adds authentication consistency but not a managed database outcome. **Conclusion:** Name the actual identity gateway capability and do not claim provider-independent database management.

### Example 3

**Situation:** Three database tools serve ordinary relational, graph, and analytical jobs. **Reasoning:** Offer a managed relational capability where semantics recur; catalog the graph and analytical services with scoped support while domain teams own selection and operation. **Conclusion:** One catalog can contain both capability providers and independently consumed tools.

### Example 4

**Situation:** A catalog says a library is “approved.” **Reasoning:** Security approved one version for internal data in a specific runtime, while the badge has no scope or date. Store authority, version range, context, decision date, expiry, and evidence; show other contexts as unevaluated. **Conclusion:** Approval is a scoped attributable claim.

### Example 5

**Situation:** Ownership in source metadata conflicts with the organization directory. **Reasoning:** Decide which source owns team identity and which owns component responsibility. Surface conflict, notify relevant owners, and avoid silently choosing the newest timestamp. **Conclusion:** Catalog authority is field-specific, not last-write-wins.

### Example 6

**Situation:** The identity provider supports four capabilities and fails. **Reasoning:** A consumer-facing catalog grouped by products may obscure this shared dependency. Use the capability-tool relation for blast-radius analysis, degraded behavior, and communication. **Conclusion:** Provider mapping is operational evidence even when hidden from ordinary interaction.

### Example 7

**Situation:** Search analytics show many queries and few clicks. **Reasoning:** Users may find answers in result summaries, receive irrelevant results, lack permission, or abandon. Conduct task-based search studies and measure successful next actions, not click-through alone. **Conclusion:** Catalog telemetry needs journey interpretation.

### Example 8

**Situation:** A provider is replaced behind an artifact-storage capability. **Reasoning:** Preserve identifiers, integrity, retention, authorization, retrieval, provenance, and failure semantics; migrate content and verify consumers. If limits change, version the contract and communicate. **Conclusion:** Provider replacement tests whether the capability abstraction is real.

### Example 9

**Situation:** An entity disappears from its source repository. **Reasoning:** Determine whether the software retired, moved, or lost metadata. Mark stale, preserve a tombstone if required, discover runtime instances, and coordinate deletion or ownership transfer. **Conclusion:** Absence from ingestion is not proof that underlying risk vanished.

### Example 10

**Situation:** A clinical data catalog lists a cohort service and a feature platform. **Reasoning:** Catalog metadata can describe provenance, steward, permitted purposes, freshness, and access process. A platform capability may fulfill approved, minimum-necessary access with audit and revocation. Neither catalog nor structural fulfillment establishes clinical validity, lawful purpose, or ethical acceptability. **Conclusion:** Discovery and mechanism remain bounded by domain authority.

## Cross-Program Connections

- **API engineering:** stable capability contracts, operation states, errors, compatibility, and provider adapters support multiple interfaces.
- **Data engineering:** catalogs, provenance, freshness, lineage, quality, ownership, and authoritative sources are shared metadata problems.
- **Software architecture:** capability boundaries, systems, components, resources, and APIs separate consumer contracts from implementation graphs.
- **Reliability engineering:** provider dependencies, service promises, readiness, incidents, migrations, and tombstones govern operational truth.
- **Security engineering:** scoped approval, authorization, endorsement, identity, audit, licensing, and data constraints require attributable sources.
- **Product management:** recurrent jobs, alternatives, supportability, adoption confounders, lifecycle, and outcome evidence decide capability scope.
- **Information retrieval:** ranking, metadata quality, result explanation, and task completion determine whether catalogs improve discovery.

## References

- CNCF TAG App Delivery, [*CNCF Platforms White Paper*](https://tag-app-delivery.cncf.io/whitepapers/platforms/), 2023. Current platform definition, provider composition, capability domains, interfaces, optionality, and user-centered ownership.
- DORA, [*Platform Engineering*](https://dora.dev/capabilities/platform-engineering/), updated January 12, 2026. Current product, journey, self-service, complexity, and balanced-outcome guidance.
- DORA, [*2024 Accelerate State of DevOps Report*](https://dora.dev/research/2024/dora-report/), corrected edition v2024.3. Empirical platform, user-centeredness, developer-independence, productivity, throughput, and stability findings with survey limitations.
- Backstage, [*Software Catalog*](https://backstage.io/docs/features/software-catalog/), current documentation retrieved 2026. Ownership, metadata, ecosystem discoverability, and code-adjacent entity sources.
- Backstage, [*System Model*](https://backstage.io/docs/features/software-catalog/system-model/), current documentation retrieved 2026. Components, APIs, resources, systems, domains, visibility, and implementation hiding.
- Backstage, [*The Life of an Entity*](https://backstage.io/docs/features/software-catalog/life-of-an-entity/), current documentation retrieved 2026. Authoritative-source ingestion, processing, storage, APIs, refresh, and entity lifecycle.
- Backstage, [*Creating the Catalog Graph*](https://backstage.io/docs/features/software-catalog/creating-the-catalog-graph/), current documentation retrieved 2026. Source-of-truth boundaries, catalog caching, ownership, relations, and graph design.
- Matthew Skelton and Manuel Pais, *Team Topologies: Organizing Business and Technology Teams for Fast Flow*, IT Revolution, 2019. Practitioner foundation for platform capabilities, team boundaries, cognitive load, interaction modes, and enabling relationships.

## Exercises

### Exercise 1

Classify a portal page that lists five messaging products, links to access forms, and shows owners. What would have to change before the platform could claim a messaging capability?

### Exercise 2

Write a capability contract for “build a verified container image” without naming a particular CI runner, registry, scanner, or signing product. Then map likely providers separately.

### Exercise 3

Design a catalog metadata authority matrix for owner, lifecycle, API schema, runtime status, cost, security approval, and documentation. Explain conflict and freshness behavior.

### Exercise 4

Compare provider-direct enablement with a platform-managed database capability for a specialist graph database. Evaluate semantics, expertise, support, lifecycle, cost, and migration.

### Exercise 5

Transfer the distinction to a national research-data ecosystem containing datasets, analysis tools, compute services, access committees, and reproducibility workflows. Define catalogs and capabilities without absorbing scientific or legal authority.

## Answers to the Exercises

### Answer 1

The page is a curated messaging tool catalog: it supports discovery and ownership lookup but not necessarily qualification, access, fulfillment, integration, operation, or retirement. A messaging capability would need an eligible job and workload boundary, stable intent such as owner, delivery semantics, retention, throughput and data class, observable states and outputs, identity and authorization, provider selection or disclosure, service guarantees, diagnostics, support, cost, compatibility, migration, deletion, and responsibility allocation. The platform would need to operate that promise across one or more products. It can retain the catalog for specialist tools that remain consumer-owned.

### Answer 2

Eligible services declare owner, source reference, build definition, target platform, dependency policy, data sensitivity, and release identity. The capability returns an immutable content-addressed image plus provenance, dependency and vulnerability results, signature or attestation, logs, status, retention, and retrieval identity. States include queued, building, verifying, published, rejected, expired, and deleted. Guarantees bound reproducibility, isolation, integrity, support, and retention; consumers own source truth and risk exceptions. Separate provider mapping can include source control, runner, build engine, dependency proxy, scanner, signing service, policy engine, artifact registry, and audit store. Provider changes preserve the contract or trigger versioned migration.

### Answer 3

Use the organization directory as authority for team identity, and code-adjacent metadata as authority for accepted component responsibility referencing that identity. Source repositories own API schema and documentation source; deployment/runtime systems own observed instance status; billing owns measured cost; the security decision system owns scoped approval with version, context, and expiry. Lifecycle may be owned by the component record but checked against runtime and repository existence. The catalog stores provenance and observation time for each field. On conflict it preserves both claims, marks the affected view uncertain, routes reconciliation to named owners, and never resolves authority merely by newest timestamp. Freshness objectives differ by field: runtime minutes, ownership hours or days, and approval until explicit expiry or revocation.

### Answer 4

Provider-direct enablement preserves full graph semantics and lets a specialist team use vendor capabilities without waiting for a lowest-common-denominator abstraction. That team owns provisioning, integration, upgrades, backup, incidents, cost, and exit; the platform may supply identity, network, audit, and catalog metadata. A managed capability is justified only if the job recurs and the platform has graph expertise and operating capacity. It can simplify access and controls, but it assumes provider lifecycle and migration duties and must not pretend relational semantics cover graph behavior. For one specialist workload, an honestly cataloged independent service is often preferable; repeated common demand may justify a separate graph capability.

### Answer 5

Catalogs should describe datasets, provenance, stewards, permitted-use categories, freshness, schemas, quality evidence, tools, compute providers, access processes, publications, and workflow artifacts with field-level authority. Capabilities can provide reproducible workspaces, approved minimum-necessary dataset access, compute allocation, environment capture, lineage, publication, audit, and revocation for defined classes. Data stewards and access committees retain lawful-purpose and disclosure decisions; researchers own hypotheses, methods, and interpretation; ethics bodies and affected communities govern appropriate use; providers own stated infrastructure mechanisms. Catalog presence does not prove data truth or permission, and successful provisioning does not prove scientific validity or ethical acceptance.
